"""Offline replay after locked npm dependencies are installed in build/formal-v1/crypto."""
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='build/formal-v1/validation')
    parser.add_argument('--dependencies', default='build/formal-v1/crypto')
    parser.add_argument('--record', action='store_true', help='Record deterministic snapshots for an intentional new research version')
    args = parser.parse_args()
    out = (REPO / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    def execute(name, command, count=None):
        p = subprocess.run(command, cwd=REPO, capture_output=True, timeout=180)
        (out / (name + '.stdout.log')).write_bytes(p.stdout)
        (out / (name + '.stderr.log')).write_bytes(p.stderr)
        row = {'name': name, 'exit': p.returncode, 'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
               'stderr_sha256': hashlib.sha256(p.stderr).hexdigest(), 'passed': p.returncode == 0}
        if count is not None:
            matches = re.findall(rb'Ran (\d+) tests?', p.stderr)
            row['tests'] = int(matches[-1]) if matches else 0
            row['passed'] = row['passed'] and row['tests'] == count
        rows.append(row)
        return p.stdout
    models = []
    for name, optimize in [('normal', []), ('repeat', []), ('optimized', ['-O'])]:
        execute('tests-' + name, [sys.executable, '-B', *optimize, '-m', 'unittest', 'discover', '-s', 'research/formal-v1/tests', '-v'], 11)
        models.append(execute('model-' + name, [sys.executable, '-B', *optimize, 'research/formal-v1/model.py']))
    crypto = [execute('crypto-' + name, ['node', 'research/formal-v1/crypto/check.mjs', args.dependencies]) for name in ('normal', 'repeat')]
    mutation = execute('mutations-normal', [sys.executable, '-B', str(HERE / 'run_mutations.py'), args.dependencies, str(out / 'mutants')])
    mutation_optimized = execute('mutations-optimized', [sys.executable, '-B', '-O', str(HERE / 'run_mutations.py'), args.dependencies, str(out / 'mutants-optimized')])
    snapshots = {'model.json': models[0], 'crypto.json': crypto[0], 'mutations.json': mutation}
    if args.record:
        for name, data in snapshots.items():
            (HERE / 'evidence' / name).write_bytes(data)
    committed_matches = {name: (HERE / 'evidence' / name).read_bytes() == data for name, data in snapshots.items()}
    deterministic = len(set(models)) == 1 and len(set(crypto)) == 1 and mutation == mutation_optimized
    result = {'schema': 'formal-v1-validation', 'python': platform.python_version(),
              'node': subprocess.check_output(['node', '--version'], text=True).strip(), 'runs': rows,
              'deterministic': deterministic, 'committed_snapshots_match': committed_matches,
              'passed': all(r['passed'] for r in rows) and deterministic and all(committed_matches.values())}
    (out / 'report.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
