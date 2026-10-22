"""Actual pinned RVR execution plus existing external consumer, no test oracle."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--implementation-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.implementation_root.resolve()
    path = root / 'src/erc8404/engine.py'
    spec = importlib.util.spec_from_file_location('subject_under_test', path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    request = engine.strict(sys.stdin.buffer.read())
    if set(request) != {'schema', 'profile', 'cases'} or request['schema'] != 'agent-harness.request.v0' or request['profile'] != 'rvr-reviewed-artifact-v0':
        raise ValueError('unsupported request')
    rows = {}
    for item in request['cases']:
        if set(item) != {'id', 'input'} or item['id'] in rows:
            raise ValueError('case transport')
        case = item['input']
        decision = engine.decide(case)
        record = case.get('presented_authorization', decision['authorization_scope'])
        status = engine.consume_authorization(record, case)
        core = decision['rvr']
        rows[item['id']] = {
            'behavior': {'receipt_status': core['consumer_status'], 'decision_status': decision['status'],
                         'core_gate': core['gate'], 'recomputation_status': core.get('recomputationStatus'),
                         'verification_outcome': core.get('verificationOutcome')},
            'authorization': {'status': status, 'authorized': status == 'VERIFIED',
                              'scope': record if status == 'VERIFIED' else None},
            'evidence': {'decision': decision, 'signature_verification': engine.crypto(case),
                         'implementation_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'core_profile_sha256': engine.PROFILE_DIGEST,
                         'input_sha256': engine.sha(engine.canonical(case)),
                         'level': 'LABORATORY_VERIFIED',
                         'limits': ['No native inference verification is performed by this adapter.',
                                    'Key separation does not establish controller independence.',
                                    'No external execution or judgment truth is established.']}}
    sys.stdout.buffer.write((json.dumps({'schema': 'agent-harness.observation.v0', 'observations': rows},
                                       sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n').encode())


if __name__ == '__main__':
    main()
