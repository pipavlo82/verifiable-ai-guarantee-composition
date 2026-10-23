"""Reproduce the pilot, transport controls, physical mutations and frozen history."""
import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent_harness as h


def validate(out):
    out.mkdir(parents=True, exist_ok=True)
    commands = []
    def run(name, args, optimized=False):
        cmd = [sys.executable, '-B', *(['-O'] if optimized else []), *args]
        start = time.perf_counter()
        p = subprocess.run(cmd, cwd=h.ROOT, capture_output=True, timeout=600)
        (out / (name + '.stdout')).write_bytes(p.stdout)
        (out / (name + '.stderr')).write_bytes(p.stderr)
        commands.append({'name': name, 'argv': cmd, 'exit_code': p.returncode,
                         'seconds': time.perf_counter() - start,
                         'stdout_sha256': h.sha(p.stdout), 'stderr_sha256': h.sha(p.stderr)})
        h.write(out / 'commands.json', commands)
        print(name, p.returncode, flush=True)
        if p.returncode:
            raise RuntimeError(name + ': see preserved logs')
        return p.stdout
    run('vector-reconstruction', ['tools/harness_v0/build_vectors.py'])
    run('core-conformance', ['evidence/erc8404/core/conformance/rvr-v0/adapter.py', '--check'])
    run('core-conformance-optimized', ['evidence/erc8404/core/conformance/rvr-v0/adapter.py', '--check'], True)
    run('core-history-integrity', ['tools/erc8404/integrity.py'])
    run('integration-history-integrity', ['tools/integration/integrity.py'])
    observations = []
    for name, optimized in [('normal', False), ('repeat', False), ('optimized', True)]:
        run('transport-' + name, ['-m', 'unittest', 'discover', '-s', 'tests/harness_v0', '-v'], optimized)
        run('pilot-' + name, ['tools/agent_harness.py', 'run', '--out', str(out / name)], optimized)
        observations.append((out / name / 'projected.json').read_bytes())
    run('physical-mutations', ['tools/harness_v0/mutations.py', '--out', str(out / 'mutations')])
    # Original files are read from the independently pinned baseline inventory.
    pin = json.loads(h.LOCK.read_bytes())['research-base']['commit']
    baseline = json.loads(subprocess.check_output(['git', 'show', pin + ':artifacts.sha256.json'], cwd=h.ROOT))['files']
    changed = [p for p, digest in baseline.items() if not (h.ROOT / p).is_file() or h.sha((h.ROOT / p).read_bytes()) != digest]
    if changed:
        raise RuntimeError('historical bytes changed: ' + repr(changed[:10]))
    report = json.loads((out / 'normal/report.json').read_bytes())
    mutations = json.loads((out / 'mutations/report.json').read_bytes())
    deterministic = len(set(observations)) == 1
    summary = {'schema': 'agent-harness.validation.v0', 'passed': deterministic,
               'deterministic_normal_repeat_optimized': deterministic,
               'unchanged_baseline_files': len(baseline), 'scenario_count': len(report['rows']),
               'conformant_scenarios': sum(r['backend_conformance'] == 'PASS' for r in report['rows']),
               'authorization_counts': {s: sum(r['observed_behavior']['authorization']['status'] == s for r in report['rows'])
                                        for s in ('VERIFIED', 'REFUTED', 'UNVERIFIABLE')},
               'mutations': mutations['counts'], 'python': sys.version,
               'platform': platform.platform(), 'node': subprocess.check_output(['node', '--version'], text=True).strip(),
               'source_lock_sha256': h.sha(h.LOCK.read_bytes()), 'commands': commands}
    h.write(out / 'summary.json', summary)
    if not deterministic:
        raise RuntimeError('semantic determinism failed')
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--out', type=Path, default=h.ROOT / 'build/agent-harness-v0/validation')
    args = p.parse_args(); result = validate(args.out.resolve())
    print(json.dumps({k: result[k] for k in ('passed', 'scenario_count', 'authorization_counts', 'mutations')}, sort_keys=True))
