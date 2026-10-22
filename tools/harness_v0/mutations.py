"""Physical one-check mutations in a disposable consumer copy; never edit Core."""
import argparse
from collections import Counter
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent_harness as h


def mutations(source):
    rows = []
    for procedure, witness in [('authority', 'wrong_authority'), ('subject', 'wrong_subject'),
                               ('judgment', 'wrong_signed_scope'), ('artifact', 'cross_component_loss'),
                               ('independence', 'self_judgment')]:
        rows.append((procedure, witness, f"'{procedure}': {procedure}", f"'{procedure}': lambda: V"))
    for guard, witness in [('claim_type', 'unsupported_claim'), ('contract_commitment', 'mismatched_contract'),
                           ('signed_contract', 'wrong_signed_policy'), ('field_policy', 'downstream_promotion'),
                           ('coverage', 'missing_independence_coverage')]:
        line = next(x for x in source.splitlines() if f"statuses['{guard}'] =" in x)
        rows.append((guard, witness, line, f"    statuses['{guard}'] = V  # physical mutant"))
    rows.append(('contract_preimage', 'missing_contract_preimage', "statuses['contract_preimage'] = U", "statuses['contract_preimage'] = V"))
    rows.append(('admission', 'tampered_admission', "return check(record == fresh['authorization_scope'])", "return V"))
    return rows


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    corpus = json.loads((h.DEFAULT.parent / 'vectors.json').read_bytes())
    source_path = h.ROOT / 'src/erc8404/engine.py'
    original = source_path.read_bytes()
    source = original.decode()
    results = []
    with tempfile.TemporaryDirectory(prefix='physical-', dir=out) as tmp:
        target = Path(tmp)
        for name in ('src/erc8404/engine.py', 'src/v2/crypto.mjs', 'fixtures/erc8404/core-lock.json'):
            dest = target / name; dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(h.ROOT / name, dest)
        shutil.copytree(h.ROOT / 'evidence/erc8404/core', target / 'evidence/erc8404/core')
        shutil.copytree(h.ROOT / 'build/formal-v1/crypto', target / 'build/formal-v1/crypto')
        edited = target / 'src/erc8404/engine.py'
        for name, witness, old, new in mutations(source):
            folder = out / name; folder.mkdir(exist_ok=True)
            selected = [v for v in corpus['vectors'] if v['name'] in ('permitted_review', witness)]
            h.write(folder / 'vectors.json', {**corpus, 'vectors': selected})
            shutil.copyfile(h.DEFAULT.parent / 'obligations.json', folder / 'obligations.json')
            suite = {'id': name, 'vectors': {'path': 'vectors.json', 'sha256': h.sha((folder / 'vectors.json').read_bytes())},
                     'obligations': {'path': 'obligations.json', 'sha256': h.sha((folder / 'obligations.json').read_bytes())}}
            h.write(folder / 'suite.json', suite)
            row = {'id': name, 'witness': witness, 'classification': 'NOT_APPLIED',
                   'original_sha256': h.sha(original), 'old': old, 'new': new}
            def execute(label):
                return h.execute(folder / 'suite.json', h.DEFAULT.parent / 'adapter.json', folder / label, target)
            baseline = execute('baseline')
            if baseline['exit_code'] != 0:
                row['classification'] = 'UNVERIFIABLE'
            elif source.count(old) == 1:
                changed = source.replace(old, new).encode()
                edited.write_bytes(changed)
                (folder / 'mutant.py').write_bytes(changed)
                row['mutant_sha256'] = h.sha(changed)
                try:
                    observed = execute('mutant')
                finally:
                    edited.write_bytes(original)
                restored = execute('restored')
                witness_row = next((r for r in observed['rows'] if r['id'] == witness), None)
                positive = next((r for r in observed['rows'] if r['id'] == 'permitted_review'), None)
                if observed.get('adapter_exit_code', 0) != 0:
                    row['classification'] = 'CRASHED'
                elif restored['exit_code'] != 0 or observed['exit_code'] == 2:
                    row['classification'] = 'UNVERIFIABLE'
                elif (observed['exit_code'] == 1 and witness_row and positive and
                      positive['backend_conformance'] == 'PASS' and
                      witness_row['observed_behavior']['authorization']['authorized'] is True):
                    row['classification'] = 'KILLED'
                else:
                    row['classification'] = 'SURVIVED'
                row['baseline_exit'] = baseline['exit_code']
                row['mutant_exit'] = observed['exit_code']
                row['restored_exit'] = restored['exit_code']
                row['unsupported_authorization_observed'] = bool(witness_row and witness_row['observed_behavior']['authorization']['authorized'])
                row['restored_sha256'] = h.sha(edited.read_bytes())
            results.append(row)
    if source_path.read_bytes() != original:
        raise RuntimeError('original source changed')
    summary = {'schema': 'agent-harness.mutations.v0', 'mutations': results,
               'counts': dict(Counter(r['classification'] for r in results)),
               'core_mutated': False, 'historical_reports_modified': False}
    h.write(out / 'report.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, default=h.ROOT / 'build/agent-harness-v0/mutations')
    args = parser.parse_args(); result = run(args.out.resolve())
    print(json.dumps(result['counts'], sort_keys=True))
    raise SystemExit(0 if all(r['classification'] == 'KILLED' for r in result['mutations']) else 1)
