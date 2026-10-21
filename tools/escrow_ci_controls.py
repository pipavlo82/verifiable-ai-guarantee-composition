"""Real subprocess failures in disposable copies, never in the source checkout."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = 'evidence/v2/capture/b/proof.bin'


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--baseline-mutations', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    need(out.is_relative_to((ROOT / 'build').resolve()), 'Control output must remain under build/')
    out.mkdir(parents=True, exist_ok=True)
    py = [sys.executable, '-B', '-X', 'utf8']
    commands = []
    rows = []

    def run(name, command, cwd=ROOT, env=None, expected=0):
        p = subprocess.run(list(map(str, command)), cwd=cwd, env=env, capture_output=True, timeout=1800)
        for stream in ('stdout', 'stderr'):
            (out / (name + '.' + stream + '.log')).write_bytes(getattr(p, stream))
        commands.append({'name': name, 'command': list(map(str, command)), 'cwd': str(cwd), 'exit': p.returncode})
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n', encoding='utf8', newline='\n')
        need(p.returncode == expected, name + ': unexpected exit, not a successful negative control')
        return p

    run('original-inventory', py + ['tools/verify_artifacts.py'])
    manifest_raw = (ROOT / 'artifacts.sha256.json').read_bytes()
    manifest = json.loads(manifest_raw)['files']
    before = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in manifest}
    with tempfile.TemporaryDirectory(prefix='inventory-', dir=out) as tmp:
        carrier = Path(tmp)
        need(carrier.resolve().is_relative_to(out), 'Unsafe disposable inventory directory')
        for rel in [*manifest, 'artifacts.sha256.json']:
            dest = carrier / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dest)
        git_dir = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=ROOT, text=True).strip()
        env = dict(os.environ, GIT_DIR=git_dir, GIT_WORK_TREE=str(carrier))
        original = (carrier / PINNED).read_bytes()
        for name in ('changed_pinned_artifact', 'missing_expected_file', 'unlisted_file'):
            run(name + '-positive', py + ['tools/verify_artifacts.py'], carrier)
            if name == 'changed_pinned_artifact':
                (carrier / PINNED).write_bytes(original + b'negative-control')
                expected = PINNED
            elif name == 'missing_expected_file':
                (carrier / PINNED).unlink()
                expected = PINNED
            else:
                (carrier / 'unlisted-negative-control.txt').write_bytes(b'not in the inventory\n')
                expected = 'unlisted-negative-control.txt'
            p = run(name + '-negative', py + ['tools/verify_artifacts.py'], carrier, expected=1)
            result = json.loads(p.stdout)
            need(result['passed'] is False and result['mismatches'] == [expected], 'Wrong inventory witness')
            if name == 'unlisted_file':
                (carrier / expected).unlink()
            else:
                (carrier / PINNED).write_bytes(original)
            run(name + '-restored', py + ['tools/verify_artifacts.py'], carrier)
            rows.append({'id': name, 'negative_exit': 1, 'positive_exit': 0, 'restored_exit': 0,
                         'classification': 'EXPECTED_FAILURE_OBSERVED', 'mismatches': [expected]})
        # Rehashing a changed old artifact must not make the new manifest exception
        # hide a baseline violation. This is an intentional isolated negative copy.
        run('baseline-refresh-positive', py + ['experiments/verdict_escrow/integrity.py'], carrier, env)
        (carrier / PINNED).write_bytes(original + b'changed-and-rehashed')
        run('rehash-control-only', py + ['tools/verify_artifacts.py', '--write'], carrier)
        run('rehashed-inventory-valid', py + ['tools/verify_artifacts.py'], carrier)
        p = run('rehashed-original-rejected', py + ['experiments/verdict_escrow/integrity.py'], carrier, env, 1)
        result = json.loads(p.stdout)
        need(result['passed'] is False and PINNED in result['baseline_changed'] and
             result['manifest_refresh']['old_entries_preserved'] is False, 'Baseline enforcement bypassed')
        (carrier / PINNED).write_bytes(original)
        (carrier / 'artifacts.sha256.json').write_bytes(manifest_raw)
        run('baseline-refresh-restored', py + ['experiments/verdict_escrow/integrity.py'], carrier, env)
        rows.append({'id': 'rehashed_original_artifact', 'negative_exit': 1,
                     'positive_exit': 0, 'restored_exit': 0, 'classification': 'EXPECTED_FAILURE_OBSERVED'})

    gate = py + ['tools/escrow_ci.py', '--mutation-report', args.baseline_mutations, '--kind', 'adapter']
    run('mutation-gate-positive', gate)
    with tempfile.TemporaryDirectory(prefix='survivor-', dir=out) as tmp:
        need(Path(tmp).resolve().is_relative_to(out), 'Unsafe disposable mutation directory')
        carrier = Path(tmp) / 'experiments/verdict_escrow'
        carrier.mkdir(parents=True)
        source = ROOT / 'experiments/verdict_escrow'
        for rel in ('adapter.py', 'vectors.py', 'mutations.py', 'profile.json',
                    'vendor/invinoveritas/examples/decision-receipt/bip340.py'):
            dest = carrier / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / rel, dest)
        original = (carrier / 'adapter.py').read_bytes()
        line = next(s for s in original.decode().splitlines() if s.endswith('# guard scope'))
        shadow = line.replace("check('scope',", "check('scope_shadow',").replace('# guard scope', '# isolated redundant control')
        changed = original.decode().replace(line, line + '\n' + shadow)
        need(changed != original.decode(), 'Survivor setup not applied')
        (carrier / 'adapter.py').write_text(changed, encoding='utf8', newline='\n')
        env = dict(os.environ, PYTHONPATH=str(ROOT))
        probe = "import vectors; p=vectors.make('positive'); n=vectors.make('A_wrong_scope'); import json; print(json.dumps({'positive':p['adapter']['authorized'],'negative':n['adapter']['authorized']})); raise SystemExit(0 if p['adapter']['authorized'] is True and n['adapter']['authorized'] is False else 1)"
        run('survivor-positive-and-negative', py + ['-c', probe], carrier, env)
        mutation_out = out / 'deliberate-survivor'
        run('actual-surviving-mutation', py + [carrier / 'mutations.py', mutation_out], ROOT, env, 1)
        report = json.loads((mutation_out / 'report.json').read_bytes())
        need(report['counts'] == {'KILLED': 16, 'SURVIVED': 1, 'CRASHED': 0, 'NOT_APPLIED': 0, 'UNVERIFIABLE': 0},
             'Not the isolated surviving scope mutation')
        survivor = next(r for r in report['mutations'] if r['id'] == 'scope')
        need(survivor['classification'] == 'SURVIVED' and survivor['baseline'] is False and
             survivor['mutant'] is False and survivor['restored'] is False and survivor['positive_mutant'] is True,
             'Survivor witness crashed or changed the positive')
        rejected = run('ci-rejects-survivor', py + ['tools/escrow_ci.py', '--mutation-report', mutation_out / 'report.json'], expected=1)
        diagnostic = json.loads(rejected.stderr)
        need(diagnostic == {'passed': False, 'error': 'Mutation coverage failure'},
             'CI failed for an unrelated reason, not the surviving mutation')
        (carrier / 'adapter.py').write_bytes(original)
        run('survivor-source-restored-positive', py + ['-c', probe], carrier, env)
        run('mutation-gate-restored', gate)
        rows.append({'id': 'authorization_mutation_survives', 'classification': 'EXPECTED_FAILURE_OBSERVED',
                     'actual_mutation_counts': report['counts'], 'negative_exit': 1, 'positive_exit': 0,
                     'restored_exit': 0, 'scope': 'Artificial redundant scope guard in a disposable copy; not a stock survivor'})
    after = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in manifest}
    need(before == after and (ROOT / 'artifacts.sha256.json').read_bytes() == manifest_raw, 'Original source changed')
    run('original-inventory-after', py + ['tools/verify_artifacts.py'])
    result = {'passed': True, 'controls': rows, 'source_unchanged': True, 'commands': commands}
    (out / 'report.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'passed': True, 'negative_controls': len(rows)}))


if __name__ == '__main__':
    main()
