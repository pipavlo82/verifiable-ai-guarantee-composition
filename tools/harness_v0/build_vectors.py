"""Author the finite profile from preserved artifacts; never import the verifier.

Expectations below are policy decisions, not captured implementation outputs.
The supplied scenario contract's adequacy remains an external assumption.
"""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'conformance/agent-harness-v0/erc8404'


def encoded(x):
    return (json.dumps(x, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()


def sha(x):
    return hashlib.sha256(x).hexdigest()


def b64(raw):
    return base64.b64encode(raw).decode()


def base(family='independent'):
    case = json.loads((ROOT / f'fixtures/erc8404/lab/{family}.json').read_bytes())
    case.pop('variants', None)
    case['bundle_bytes'] = b64((ROOT / 'fixtures/erc8404/rvr-bundle.json').read_bytes())
    case['receipt_bytes'] = b64((ROOT / 'fixtures/erc8404/receipt.json').read_bytes())
    return case


def variant(case, name, family='independent'):
    case['documents']['judgment'] = json.loads((ROOT / f'fixtures/erc8404/lab/{family}.json').read_bytes())['variants'][name]


def permitted_scope(case):
    contract = json.loads(base64.b64decode(case['contract_bytes']))
    return {'scenario': contract['scenario'], 'claim_type': contract['claim_type'],
            'contract_sha256': sha(base64.b64decode(case['contract_bytes'])),
            'verified_claim_scope': {k: case['claim'][k] for k in contract['consumed_fields']},
            'receipt_sha256': sha(base64.b64decode(case['receipt_bytes'])),
            'unconsumed_claim_fields': [],
            'limits': ['artifact identity and authenticated review only',
                       'no inference truth, external execution or judgment correctness']}


def build():
    rows = []
    def add(name, case, obligation, status='REFUTED', receipt='VERIFIED', decision=None,
            gate='ACCEPTED', recomputation='REPRODUCED', outcome='VERIFIED'):
        rows.append({'name': name, 'input': case, 'obligations': obligation,
                     'expected': {'behavior': {'receipt_status': receipt, 'decision_status': decision or status,
                                               'core_gate': gate, 'recomputation_status': recomputation,
                                               'verification_outcome': outcome},
                                  'authorization': {'status': status, 'authorized': status == 'VERIFIED',
                                                    'scope': permitted_scope(case) if status == 'VERIFIED' else None}}})
    add('permitted_review', base(), ['RVR-IDENTITY', 'POL-CLAIM'], 'VERIFIED')
    add('separation_not_required', base('self_allowed'), ['POL-O14'], 'VERIFIED')
    c = base(); c['claim']['claimType'] = 'EXECUTE_PAYMENT'; add('unsupported_claim', c, ['POL-CLAIM'])
    c = base('self_allowed'); variant(c, 'unauthorized', 'self_allowed'); add('wrong_authority', c, ['POL-AUTHORITY'])
    c = base(); variant(c, 'wrong_subject'); add('wrong_subject', c, ['POL-SUBJECT'])
    c = base('statement_scope'); variant(c, 'wrong_scope', 'statement_scope'); add('wrong_signed_scope', c, ['POL-SCOPE'])
    c = base(); b = json.loads(base64.b64decode(c['bundle_bytes'])); b['payloadsBase64'] = {}; c['bundle_bytes'] = b64(encoded(b))
    add('missing_payload', c, ['RVR-AVAILABLE'], 'UNVERIFIABLE', 'UNVERIFIABLE', recomputation='CANNOT_RECOMPUTE', outcome=None)
    c = base(); c['documents']['judgment'] = None; add('missing_judgment', c, ['POL-SIGNATURE'], 'UNVERIFIABLE')
    c = base(); c['context']['contract_sha256'] = 'ff' * 32; add('mismatched_contract', c, ['POL-CONTRACT'])
    c = base(); variant(c, 'wrong_contract'); add('wrong_signed_policy', c, ['POL-POLICY'])
    c = base(); variant(c, 'wrong_artifact'); add('cross_component_loss', c, ['POL-ARTIFACT'])
    c = base(); c['claim']['paymentAuthorized'] = True; add('downstream_promotion', c, ['POL-FIELDS'])
    c = base('self'); c['catalog'].pop('O14'); add('missing_independence_coverage', c, ['POL-COVERAGE'])
    add('self_judgment', base('self'), ['POL-O14'])
    c = base(); c['documents']['judgment']['signature'] = '0x' + '00' * 65; add('invalid_signature', c, ['POL-SIGNATURE'])
    c = base(); c['contract_bytes'] = None; add('missing_contract_preimage', c, ['POL-PREIMAGE'], 'UNVERIFIABLE')
    c = base(); record = permitted_scope(c); record['scenario'] = 'another-scenario'; c['presented_authorization'] = record
    add('tampered_admission', c, ['POL-ADMISSION'], decision='VERIFIED')
    c = base(); r = json.loads(base64.b64decode(c['receipt_bytes'])); r['outcome'] = 'REFUTED'; c['receipt_bytes'] = b64(encoded(r))
    add('contradictory_receipt', c, ['RVR-PROJECTION'], receipt='REFUTED', gate='rvr.gate.result_projection_mismatch', recomputation=None, outcome=None)
    return {'profile': 'rvr-reviewed-artifact-v0', 'vectors': rows}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); args = parser.parse_args()
    raw = encoded(build()); path = DEST / 'vectors.json'
    if args.write:
        path.write_bytes(raw)
        suite = {'id': 'agent-harness-rvr-reviewed-artifact-v0',
                 'vectors': {'path': 'vectors.json', 'sha256': sha(raw)},
                 'obligations': {'path': 'obligations.json', 'sha256': sha((DEST / 'obligations.json').read_bytes())}}
        (DEST / 'suite.json').write_bytes(encoded(suite))
    if path.read_bytes() != raw:
        raise SystemExit('vector reconstruction differs')
    print('18 independently declared vectors reconstructed byte-identically')


if __name__ == '__main__':
    main()
