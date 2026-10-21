"""Claim-scoped authorization over an unchanged, pinned RVR receipt.

The caller supplies a trusted scenario contract separately from the catalog.
Authorization is a local decision, not a transferable credential or RVR field.
"""
import base64
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / 'evidence/erc8404/core'
V, R, U = 'VERIFIED', 'REFUTED', 'UNVERIFIABLE'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    def validate(x):
        if x is None or type(x) is bool: return
        if isinstance(x, str):
            if any(0xd800 <= ord(c) <= 0xdfff for c in x): raise ValueError('surrogate')
        elif isinstance(x, list):
            for v in x: validate(v)
        elif isinstance(x, dict):
            for k, v in x.items():
                if not isinstance(k, str): raise ValueError('key')
                validate(k); validate(v)
        else: raise ValueError('numbers/unsupported type')
    validate(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def strict(raw):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d: raise ValueError('duplicate key')
            d[k] = v
        return d
    obj = json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('constant')))
    canonical(obj)
    return obj

def combine(values):
    v = list(values)
    return R if R in v else U if not v or U in v else V

def check(value):
    return U if value is None else V if value else R

def same(*values):
    return None if any(v is None for v in values) else all(v == values[0] for v in values)

def load_adapter():
    pins = json.loads((ROOT/'fixtures/erc8404/core-lock.json').read_bytes())
    for p, digest in pins.items():
        if sha((CORE/p).read_bytes()) != digest: raise ValueError('frozen Core identity mismatch: '+p)
    spec = importlib.util.spec_from_file_location('frozen_rvr_adapter', CORE/'conformance/rvr-v0/adapter.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

ADAPTER = load_adapter()
PROFILE = strict((CORE/'conformance/rvr-v0/verification-profile.json').read_bytes())
PROFILE_DIGEST = sha(canonical(PROFILE))
SCHEMA = ADAPTER.load_json(CORE/'conformance/rvr-v0/rvr.schema.json')

def rvr(case):
    """Keep Core gate/status/outcome axes separate from consumer tri-state."""
    bundle = {}
    try:
        bundle = strict(base64.b64decode(case['bundle_bytes'], validate=True))
        # Never allow the caller to choose another procedure under this consumer.
        if canonical(bundle['verificationProfile']) != canonical(PROFILE):
            return {'gate': 'PROFILE_NOT_SUPPORTED', 'consumer_status': R}
        receipt_raw = base64.b64decode(case['receipt_bytes'], validate=True)
        bundle['receipt'] = strict(receipt_raw)
        result = ADAPTER.recompute(bundle, bundle, PROFILE_DIGEST, SCHEMA)
        status = result.get('recomputationStatus')
        consumer = result.get('verificationOutcome', U) if status == 'REPRODUCED' else U if status == 'CANNOT_RECOMPUTE' else R
        return {**result, 'gate': 'ACCEPTED', 'consumer_status': consumer, 'receipt_sha256': sha(receipt_raw), 'claim': bundle['claim']}
    except (KeyError, ValueError, TypeError, ADAPTER.RvrError) as e:
        return {'gate': getattr(e, 'reason_code', 'MALFORMED_INPUT'), 'consumer_status': R, 'claim': bundle.get('claim', {})}

def crypto(case):
    cmd = ['node', str(ROOT/'src/v2/crypto.mjs')]
    request = {'documents': case['documents'], 'bytes': {}}
    try:
        p = subprocess.run(cmd, input=json.dumps(request).encode(), capture_output=True, timeout=30)
        data = json.loads(p.stdout)
        if p.returncode or data['known_answers'] != {'keccak_empty': True, 'ether_mail_recovery': True}: return {}
        return data['signatures']
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired): return {}

def resolve_contract(case):
    raw = case.get('contract_bytes')
    if raw is None: return None  # MUTATE: contract_preimage
    data = base64.b64decode(raw, validate=True)
    contract = strict(data)
    if data != canonical(contract): raise ValueError('noncanonical contract bytes')
    expected = {'schema','scenario','claim_type','scope','domain','authorized','identity_namespace','actions','separation','requirements','consumed_fields','unconsumed_policy','adequacy'}
    if not isinstance(contract, dict) or set(contract) != expected: raise ValueError('contract schema')
    for k in ('domain','authorized','actions','requirements'):
        if not isinstance(contract[k], dict): raise ValueError('contract mapping')
    if not isinstance(contract['separation'], list) or any(not isinstance(pair,list) or len(pair)!=2 or any(not isinstance(r,str) for r in pair) for pair in contract['separation']): raise ValueError('role pairs')
    if not isinstance(contract['consumed_fields'],list) or any(not isinstance(k,str) for k in contract['consumed_fields']): raise ValueError('fields')
    if contract['unconsumed_policy'] not in ('REJECT','LIST'): raise ValueError('field policy')
    for item in contract['requirements'].values():
        if not isinstance(item,dict) or set(item)!={'procedure','dependencies'} or not isinstance(item['dependencies'],list) or any(not isinstance(d,str) for d in item['dependencies']): raise ValueError('requirement')
    return contract

def decide(case, mode='C'):
    core = rvr(case)
    statuses = {'receipt': core['consumer_status']}
    missing = []; unconsumed = []; scope = None
    def output():
        status = combine(statuses.values())
        return {'status': status, 'authorized': status == V, 'authorization_scope': scope if status == V else None,
                'missing_obligations': sorted(missing), 'unconsumed_claim_fields': sorted(unconsumed),
                'checks': statuses, 'rvr': core, 'contract_sha256': digest, 'mode': mode}
    digest = None
    if mode == 'A': return output()
    try: contract = resolve_contract(case)
    except (ValueError, TypeError):
        statuses['contract_format'] = R; return output()
    if contract is None:
        statuses['contract_preimage'] = U; return output()
    digest = sha(canonical(contract))
    claim = case['claim']; catalog = case['catalog']; context = case['context']
    if not all(isinstance(x,dict) for x in (claim,catalog,context,case['documents'])) or any(not isinstance(e,dict) for e in catalog.values()) or any(d is not None and not isinstance(d,dict) for d in case['documents'].values()):
        statuses['input_format'] = R; return output()
    signatures = crypto(case); docs = case['documents']
    def msg(role, field): return (docs.get(role) or {}).get('message', {}).get(field)
    def signed(role): return signatures.get(role, {}).get('status', U)
    def identity(role):
        if signed(role) != V: return None
        if (docs.get(role) or {}).get('domain') != contract.get('domain'): return None
        return signatures[role].get('signer')
    def authenticity(): return combine(combine([signed(r), check((docs.get(r) or {}).get('type') == 'LabJudgment')]) if docs.get(r) is not None else U for r in ('producer', 'judgment'))
    def artifact():
        return check(same(claim.get('artifactSha256'), core.get('claim', {}).get('expectedDigest'),
                          *[(msg(r, 'proofHash') or '')[2:] or None for r in ('producer', 'judgment')]))
    def subject(): return check(same(claim.get('subject'), msg('producer', 'subject'), msg('judgment', 'subject')))
    def authority():
        return combine(check(same(identity(r), contract.get('authorized', {}).get(r))) for r in ('producer', 'judgment'))
    def domain(): return combine(check(same((docs.get(r) or {}).get('domain'), contract.get('domain'))) for r in ('producer', 'judgment'))
    def judgment():
        return combine([*(check(same(msg(r, 'action'), contract['actions'].get(r))) for r in ('producer', 'judgment')),
                        *(check(same(msg(r, 'scope'), contract.get('scope'))) for r in ('producer', 'judgment'))])
    def independence():
        results = []
        for a, b in contract.get('separation', []):
            ia, ib = identity(a), identity(b)
            ns = contract.get('identity_namespace')
            ea, eb = contract.get('authorized', {}).get(a), contract.get('authorized', {}).get(b)
            results.append(check(None if any(x is None for x in (ia, ib, ea, eb)) or ns != 'eip155:31337:secp256k1' else ia == ea and ib == eb and ia != ib))
        return combine(results)
    procedures = {'signature': authenticity, 'artifact': artifact, 'subject': subject, 'authority': authority,
                  'domain': domain, 'judgment': judgment, 'independence': independence}
    required = contract.get('requirements', {})
    verification = {}
    for oid, entry in catalog.items():
        fn = procedures.get(entry.get('procedure'))
        verification[oid] = fn() if fn else U
    # MUTATE: each independent verification boundary in isolated source copies.
    statuses.update(verification)
    if mode == 'B': return output()
    missing = sorted(set(required) - set(catalog))
    statuses['coverage'] = check(not missing)  # MUTATE: coverage
    statuses['definitions'] = check(all(catalog.get(k) == v for k, v in required.items() if k in catalog))  # MUTATE: definitions
    statuses['dependency_closure'] = check(all(d in required for v in required.values() for d in v['dependencies']))
    statuses['supported_contract'] = check(contract.get('schema') == 'claim-aware.external.v1' and contract.get('claim_type') == 'REVIEWED_ARTIFACT_IDENTITY' and contract.get('scope') == 'artifact-byte-identity' and bool(required))  # MUTATE: supported_contract
    statuses['contract_commitment'] = check(same(digest, context.get('contract_sha256')))  # MUTATE: contract_commitment
    statuses['scenario'] = V
    statuses['claim_type'] = check(same(claim.get('claimType'), contract.get('claim_type')))  # MUTATE: claim_type
    statuses['scope'] = check(same(claim.get('scope'), contract.get('scope')))  # MUTATE: scope
    # A signed assertion identifies this exact contract; a caller digest is insufficient.
    statuses['signed_contract'] = check(same('0x'+digest, msg('producer', 'policyHash'), msg('judgment', 'policyHash')))  # MUTATE: signed_contract
    consumed = contract.get('consumed_fields', [])
    unconsumed = sorted(set(claim) - set(consumed))
    statuses['field_policy'] = check(not unconsumed or contract.get('unconsumed_policy') == 'LIST')  # MUTATE: field_policy
    statuses['consumed_semantics'] = check(set(consumed) == {'scenario','claimType','scope','subject','artifactSha256'})
    scope = {'scenario': contract['scenario'], 'claim_type': contract['claim_type'], 'contract_sha256': digest,
             'verified_claim_scope': {k: claim[k] for k in consumed if k in claim},
             'receipt_sha256': core.get('receipt_sha256'), 'unconsumed_claim_fields': unconsumed,
             'limits': ['artifact identity and authenticated review only', 'no inference truth, external execution or judgment correctness']}
    return output()

def consume_authorization(record, case):
    """Re-evaluate; a copied/forged JSON authorization is never a bearer token."""
    fresh = decide(case)
    if fresh['status'] != V: return fresh['status']
    return check(record == fresh['authorization_scope'])  # MUTATE: reuse
