"""Strict local/CI entrypoint. Never writes a manifest or accepts partial coverage."""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_IDS = {'authorization', 'record', 'scope', 'scenario', 'evidence', 'profile',
               'chain', 'escrow', 'recipient', 'amount', 'payment', 'nonce', 'expiry',
               'revocation', 'trusted_signer', 'consumption', 'verdict_preimage'}
CHAIN_IDS = {'chain', 'escrow_address', 'trusted_signer', 'replay_guard', 'state_consumption'}


def require(value, message):
    if not value:
        raise ValueError(message)


def check_mutations(report, kind):
    """Require executed, distinguishing controls; a success exit alone is insufficient."""
    expected = ADAPTER_IDS if kind == 'adapter' else CHAIN_IDS
    rows = report['mutations']
    require(len(rows) == len(expected) and {r['id'] for r in rows} == expected,
            'Missing, duplicate or unknown mutation IDs')
    require(report['counts'] == {'KILLED': len(expected), 'SURVIVED': 0,
            'CRASHED': 0, 'NOT_APPLIED': 0, 'UNVERIFIABLE': 0}, 'Mutation coverage failure')
    require(report['source_unchanged' if kind == 'adapter' else 'original_source_unchanged'] is True,
            'Mutation source was not restored')
    for row in rows:
        require(row['classification'] == 'KILLED', 'Non-killed mutation: ' + row['id'])
        if kind == 'adapter':
            require(row['baseline'] is False and row['mutant'] is True and row['restored'] is False,
                    'Negative witness does not distinguish the mutant')
            require(all(row[k] is True for k in ('positive', 'positive_mutant', 'positive_restored')),
                    'Positive control failed')
        else:
            require(row['baseline']['negative_authorized'] is False and
                    row['mutant']['negative_authorized'] is True and
                    row['mutant']['negative_delta'] == 1000000 and
                    row['restored']['negative_authorized'] is False,
                    'No distinguishing mock-token execution')
            require(all(row[k]['positive'] is True for k in ('baseline', 'mutant', 'restored')),
                    'Positive EVM control failed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='build/escrow/ci')
    parser.add_argument('--mutation-report', type=Path)
    parser.add_argument('--kind', choices=('adapter', 'onchain'), default='adapter')
    args = parser.parse_args()
    if args.mutation_report:
        check_mutations(json.loads(args.mutation_report.read_bytes()), args.kind)
        print(json.dumps({'passed': True, 'kind': args.kind}))
        return 0
    out = (ROOT / args.out).resolve()
    require(out.is_relative_to((ROOT / 'build').resolve()), 'CI output must be under ignored build/')
    out.mkdir(parents=True, exist_ok=True)
    commands = []
    py = [sys.executable, '-B', '-X', 'utf8']

    def run(name, command):
        start = time.perf_counter()
        p = subprocess.run([str(x) for x in command], cwd=ROOT, capture_output=True, timeout=3600)
        for stream in ('stdout', 'stderr'):
            (out / (name + '.' + stream + '.log')).write_bytes(getattr(p, stream))
        commands.append({'name': name, 'command': list(map(str, command)), 'cwd': str(ROOT),
                         'exit': p.returncode, 'seconds': time.perf_counter() - start})
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n', encoding='utf8', newline='\n')
        print(name, p.returncode, flush=True)
        require(p.returncode == 0, name + ' failed; see raw logs')

    for name, script in [('inventory-before', 'tools/verify_artifacts.py'),
                         ('experiment-inventory', 'tools/escrow_inventory.py'),
                         ('baseline-before', 'experiments/verdict_escrow/integrity.py'),
                         ('frozen-core', 'tools/integration/integrity.py')]:
        run(name, py + [script])
    run('escrow-validation', py + ['experiments/verdict_escrow/validate.py', '--out', out / 'validation'])
    validation = json.loads((out / 'validation/report.json').read_bytes())
    require(validation['passed'] is True and validation['source_unchanged'] is True and
            all(validation['determinism'].values()), 'Semantic determinism/source failure')
    require(len(validation['commands']) == 28 and all(c['exit'] == 0 for c in validation['commands']),
            'Incomplete final suite')
    require(validation['comparison']['scenario_count'] == 31, 'Missing scenario execution')
    for mode in ('normal', 'repeat', 'optimized'):
        check_mutations(json.loads((out / ('validation/mutations-' + mode + '/report.json')).read_bytes()), 'adapter')
    check_mutations(json.loads((out / 'validation/onchain-mutations/report.json').read_bytes()), 'onchain')
    run('negative-ci-controls', py + ['tools/escrow_ci_controls.py', '--out', out / 'controls',
                                    '--baseline-mutations', out / 'validation/mutations-normal/report.json'])
    run('inventory-after', py + ['tools/verify_artifacts.py'])
    run('baseline-after', py + ['experiments/verdict_escrow/integrity.py'])
    result = {'passed': True, 'commands': commands, 'escrow_scenarios': 31,
              'new_mutations': {'KILLED': 22, 'SURVIVED': 0, 'CRASHED': 0},
              'separate_absent_onchain_checks': {'NOT_APPLIED': 6},
              'negative_controls': json.loads((out / 'controls/report.json').read_bytes()),
              'validation_sha256': hashlib.sha256((out / 'validation/report.json').read_bytes()).hexdigest()}
    (out / 'report.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'passed': True, 'new_mutations': result['new_mutations']}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'passed': False, 'error': str(error)}), file=sys.stderr)
        raise SystemExit(1)
