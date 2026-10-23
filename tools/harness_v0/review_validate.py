"""Fresh-checkout replay of supplemental reviewer controls with exact command logs."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent_harness as h
from review_controls import REVIEWED_HEAD, require


def validate(out):
    out.mkdir(parents=True, exist_ok=True)
    commands = []
    def run(name, args, optimized=False):
        argv = [sys.executable, '-B', *(['-O'] if optimized else []), *args]
        start = time.perf_counter()
        process = subprocess.run(argv, cwd=h.ROOT, capture_output=True, timeout=900)
        (out / (name + '.stdout')).write_bytes(process.stdout)
        (out / (name + '.stderr')).write_bytes(process.stderr)
        commands.append({'name': name, 'argv': argv, 'exit_code': process.returncode,
                         'seconds': time.perf_counter() - start,
                         'stdout_sha256': h.sha(process.stdout), 'stderr_sha256': h.sha(process.stderr)})
        h.write(out / 'commands.json', commands)
        print(name, process.returncode, flush=True)
        require(process.returncode == 0, name + ': see raw logs')
    run('vectors', ['tools/harness_v0/review_vectors.py'])
    run('classification-controls', ['-m', 'unittest', 'discover', '-s', 'tests/harness_review', '-v'])
    for mode, optimized in [('normal', False), ('optimized', True)]:
        run('physical-' + mode, ['tools/harness_v0/review_controls.py', '--out', str(out / mode)], optimized)
    reports = [json.loads((out / mode / 'report.json').read_bytes()) for mode in ('normal', 'optimized')]
    for mode in ('normal', 'optimized'):
        r = json.loads((out / mode / 'report.json').read_bytes())
        require(r['original_18']['counts'] == {'KILLED': 1, 'SURVIVED': 4} and
                r['isolated']['counts'] == {'KILLED': 4}, 'unexpected mutation outcome')
    semantic = [(out / mode / repeat / 'projected.json').read_bytes()
                for mode in ('normal', 'optimized') for repeat in ('normal', 'repeat')]
    require(len(set(semantic)) == 1, 'normal/repeat/-O observations differ')
    require(reports[0]['original_18'] == reports[1]['original_18'] and
            reports[0]['isolated'] == reports[1]['isolated'], 'mutation reports differ under -O')
    baseline = json.loads(subprocess.check_output(['git', 'show', REVIEWED_HEAD + ':artifacts.sha256.json'], cwd=h.ROOT))['files']
    changed = sorted(p for p, digest in baseline.items()
                     if not (h.ROOT / p).is_file() or h.sha((h.ROOT / p).read_bytes()) != digest)
    allowed = {'conformance/agent-harness-v0/README.md', 'research/harness-v0/LIMITATIONS.md'}
    require(set(changed) <= allowed, 'unexpected historical change: ' + repr(changed))
    summary = {'schema': 'agent-harness.review-validation.v0', 'passed': True,
               'reviewed_head': REVIEWED_HEAD, 'scenario_count': 5,
               'deterministic_normal_repeat_optimized': True,
               'reviewer_experiment_counts': reports[0]['original_18']['counts'],
               'isolated_mutation_counts': reports[0]['isolated']['counts'],
               'original_inventory_files': len(baseline), 'intentional_documentation_changes': changed,
               'unchanged_original_files': len(baseline) - len(changed), 'commands': commands}
    h.write(out / 'summary.json', summary)
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--out', type=Path, default=h.ROOT / 'build/harness-review/validation')
    args = p.parse_args(); result = validate(args.out.resolve())
    print(json.dumps({k: result[k] for k in ('passed', 'scenario_count', 'reviewer_experiment_counts', 'isolated_mutation_counts')}))
