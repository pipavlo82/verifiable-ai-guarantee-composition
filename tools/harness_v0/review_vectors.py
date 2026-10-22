"""Independent supplemental expectations; never import the consumer under test."""
import argparse
import copy
import json
from pathlib import Path

from build_vectors import base, encoded, permitted_scope, sha

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'conformance/agent-harness-review-v0'
GUARDS = ('scope', 'scenario', 'definitions', 'supported_contract')


def build():
    cases = [('permitted_review', base(), 'VERIFIED')]
    c = base(); c['claim']['scope'] = 'external-task-success'
    cases.append(('scope_only', c, 'REFUTED'))
    c = base(); c['claim']['scenario'] = 'another-scenario'
    cases.append(('scenario_only', c, 'REFUTED'))
    c = base(); c['catalog']['S04']['procedure'] = 'signature'
    cases.append(('definitions_only', c, 'REFUTED'))
    # Reuse existing genuine laboratory signatures over this unsupported contract.
    # Claim and contract agree; only the consumer's supported-contract gate refuses.
    cases.append(('supported_contract_only', base('unsupported_claim'), 'REFUTED'))
    rows = []
    for name, case, status in cases:
        obligation = 'POL-CLAIM' if name == 'permitted_review' else 'REVIEW-' + name.removesuffix('_only').upper()
        rows.append({'name': name, 'input': case, 'obligations': [obligation],
                     'expected': {'behavior': {'receipt_status': 'VERIFIED', 'decision_status': status,
                                               'core_gate': 'ACCEPTED', 'recomputation_status': 'REPRODUCED',
                                               'verification_outcome': 'VERIFIED'},
                                  'authorization': {'status': status, 'authorized': status == 'VERIFIED',
                                                    'scope': permitted_scope(case) if status == 'VERIFIED' else None}}})
    return {'profile': 'rvr-reviewed-artifact-v0', 'vectors': rows}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--write', action='store_true'); args = p.parse_args()
    requirements = {
        'scope': 'Requested claim scope must equal the signed scenario contract scope.',
        'scenario': 'Requested scenario must equal the exact scenario contract scenario.',
        'definitions': 'Catalog procedure and dependency definitions must equal the independently supplied contract requirements.',
        'supported_contract': 'A contract for EXTERNAL_TASK_SUCCESS is outside this consumer even when signatures and claim bindings agree.'}
    original = json.loads((ROOT / 'conformance/agent-harness-v0/erc8404/obligations.json').read_bytes())
    obligations = {'POL-CLAIM': copy.deepcopy(original['POL-CLAIM'])}
    for guard, requirement in requirements.items():
        obligations['REVIEW-' + guard.upper()] = {
            'kind': 'RESEARCH_POLICY', 'requirement': requirement,
            'source': 'https://github.com/trustless-ai/verifiable-execution-claim-authorization/blob/0e17c97e896916b4d9505072cc9ebe2018329b01/research/erc8404/CLAIM_AWARE_PROFILE.md',
            'version': 'rvr-reviewed-artifact-v0 / supplemental review v0',
            'coverage': 'One isolated finite witness; not exhaustive predicate or policy coverage.'}
    artifacts = {'vectors.json': encoded(build()), 'obligations.json': encoded(obligations)}
    artifacts['suite.json'] = encoded({'id': 'agent-harness-review-boundaries-v0',
        'vectors': {'path': 'vectors.json', 'sha256': sha(artifacts['vectors.json'])},
        'obligations': {'path': 'obligations.json', 'sha256': sha(artifacts['obligations.json'])}})
    DEST.mkdir(parents=True, exist_ok=True)
    for name, raw in artifacts.items():
        if args.write:
            (DEST / name).write_bytes(raw)
        if (DEST / name).read_bytes() != raw:
            raise RuntimeError('independent reconstruction differs: ' + name)
    print('5 supplemental vectors reconstructed byte-identically')


if __name__ == '__main__':
    main()
