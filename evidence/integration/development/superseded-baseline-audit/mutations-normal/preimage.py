"""Exact claim-scoped conjunction. Neither imported profile nor ERC8404 Core is edited.

The consumer supplies its trusted contract preimage on every call. Contract adequacy,
key custody and the local verifier/toolchain are explicit assumptions. No result is
a bearer credential. A joint subject pair is NOT an assertion of entity equivalence.
"""
import base64, hashlib, json
from pathlib import Path
from src.v4_1 import model as inference
from src.erc8404 import engine as review

V,R,U = inference.V,inference.R,inference.U
ROOT=inference.ROOT
CLAIM_TYPE='LAB_REPLAY_AND_REVIEWED_PROOF_IDENTITY'
SCOPE='local-output-replay-and-proof-byte-review'
KNOWN={'J01','J02','J03','J04','J05','J06','J07','J08','J09'}
FIELDS={'scenario','claim_type','scope','inference_subject','review_subject','proof_sha256','inputHash','modelHash','outputHash'}
INFERENCE_FIELDS={'subject','inputHash','outputHash','modelHash','proofHash','action','scope','executionId','policyHash','nonce','claimKind'}
REVIEW_FIELDS={'scenario','claimType','scope','subject','artifactSha256'}
ASSUMPTIONS=[
 'Consumer independently selects an adequate scenario contract and its policies.',
 'Pinned local verifiers, runtimes and filesystem are trusted during this call.',
 'Distinct recovered keys do not establish distinct real-world controllers.',
 'Laboratory attestations establish authenticity, not judgment truth or external admission.',
 'ReceiptOS records and RVR identity receipts do not establish historical external execution.',
 'The two subject labels retain separate meanings; no entity-equivalence claim is made.'
]
def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return review.canonical(value)
def eq(a,b):return U if a is None or b is None else V if a==b else R
def combined(values):return inference.combine(values)
def contract_bytes(contract):return base64.b64encode(canonical(contract)).decode()
def parse_contract(encoded):
    if encoded is None:return None
    raw=base64.b64decode(encoded,validate=True);c=review.strict(raw)
    if raw!=canonical(c):raise ValueError('Noncanonical joint contract')
    required={'schema','scenario','claim_type','scope','profiles','requirements','checker_policy','controller_policy','adequacy'}
    if not isinstance(c,dict) or set(c)!=required:raise ValueError('Contract shape')
    if not all(isinstance(c[k],str) for k in ('schema','scenario','claim_type','scope','checker_policy','controller_policy','adequacy')):raise ValueError('Contract scalar types')
    if not isinstance(c['profiles'],dict) or set(c['profiles'])!={'inference','review'} or not all(isinstance(v,str) and len(v)==64 for v in c['profiles'].values()):raise ValueError('Profile pins')
    if not isinstance(c['requirements'],dict) or not c['requirements']:raise ValueError('Empty requirements')
    for k,v in c['requirements'].items():
        if not isinstance(k,str) or not isinstance(v,dict) or set(v)!={'procedure','dependencies'} or not isinstance(v['procedure'],str) or not isinstance(v['dependencies'],list) or not all(isinstance(d,str) for d in v['dependencies']):raise ValueError('Requirement shape')
    return c

def evaluate(case,mode='C'):
    """A=components, B=declared joint checks, C=scenario-complete composition.
    Modes are experimental baselines, never accepted by admit().
    """
    checks={};missing=[];unconsumed=[];digest=None;contract=None;scope=None;refs={};reports={}
    def output():
        status=combined(checks.values());authorized=status==V
        return {'status':status,'authorized':authorized,'scenario':contract.get('scenario') if contract else None,
          'claim_type':contract.get('claim_type') if contract else None,'contract_sha256':digest,
          'verified_scope':scope if authorized else None,'missing_obligations':missing,
          'unconsumed_claim_fields':unconsumed,'evidence_references':refs,'assumptions':ASSUMPTIONS,
          'checks':checks,'components':reports,'evidence_level':'LABORATORY_VERIFIED',
          'chain_status':'PARTIAL_CHAIN_VERIFIED','mode':mode}
    try:contract=parse_contract(case.get('contract_bytes'))
    except (TypeError,ValueError,KeyError):checks['contract']=R;return output()
    if contract is None:checks['contract']=U;return output()  # GUARD preimage
    digest=sha(canonical(contract))
    try:
        i=case.get('inference');r=case.get('review');claim=case.get('claim');catalog=case.get('catalog')
        if not all(isinstance(x,dict) for x in (i,r,claim,catalog)):checks['evidence_shape']=U;return output()
        # The legacy verifier reads local paths. Do not let an evidence carrier escape ROOT.
        paths=i.get('files',{})
        if not isinstance(paths,dict) or any(p is not None and (not isinstance(p,str) or Path(p).is_absolute() or '..' in Path(p).parts or not (ROOT/p).resolve().is_relative_to(ROOT.resolve())) for p in paths.values()):
            checks['local_paths']=R;return output()
        f=inference.facts(i);ir=inference.evaluate(i,f);rr=review.decide(r)
        reports={'inference':ir['C']['status'],'review':rr['status']}
        refs={'inference_files':{k:sha(v) for k,v in f['bytes'].items()},'rvr_receipt_sha256':sha(base64.b64decode(r['receipt_bytes'],validate=True)) if r.get('receipt_bytes') else None,
              'documents_sha256':sha(json.dumps({'inference':i.get('documents'),'review':r.get('documents')},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())}
        if mode=='A':checks.update(inference=ir['A']['status'],receipt=review.rvr(r)['consumer_status']);return output()
        ic=i.get('contract');rc=review.resolve_contract(r)
        rawproof=f['bytes'].get('proof');proof_sha=sha(rawproof) if rawproof is not None else None
        core=review.rvr(r);review_digest=core.get('claim',{}).get('expectedDigest')
        expected={'scenario':contract['scenario'],'claim_type':contract['claim_type'],'scope':contract['scope'],
          'inference_subject':i['claim'].get('subject'),'review_subject':r['claim'].get('subject'),
          'proof_sha256':proof_sha,'inputHash':f['hashes'].get('input'),'modelHash':f['hashes'].get('model'),'outputHash':f['hashes'].get('output')}
        def profile_pins():
            return combined([eq(inference.contract_digest(ic) if ic else None,contract['profiles']['inference']),eq(sha(canonical(rc)) if rc else None,contract['profiles']['review'])])
        def keys():
            if contract['checker_policy']=='SCENARIO_PROFILES':return V
            if contract['checker_policy']!='DISTINCT_KEYS_IN_EACH_PROFILE':return U
            pairs=[V if ic and rc and 'O14' in ic.get('requirements',{}) and 'O14' in rc.get('requirements',{}) and ['producer','judgment'] in rc.get('separation',[]) else R]
            recovered=review.crypto(r)
            if not rc or rc.get('identity_namespace')!='eip155:31337:secp256k1':pairs.append(U)
            for signatures,left,right in ((f['signatures'],'provenance','judgment'),(recovered,'producer','judgment')):
                a=signatures.get(left,{});b=signatures.get(right,{})
                if a.get('status')!=V or b.get('status')!=V or not a.get('signer') or not b.get('signer'):pairs.append(U)
                else:pairs.append(eq(a['signer'].lower()!=b['signer'].lower(),True))  # GUARD key_identity
            return combined(pairs)
        def controllers():return V if contract['controller_policy']=='NOT_CLAIMED' else U
        def supported_scope():
            if not (contract['schema']=='claim-aware.integration.v1' and contract['claim_type']==CLAIM_TYPE and contract['scope']==SCOPE and ic and rc and ic.get('claim_type')=='LAB_OUTPUT_REPLAY_ADMISSIBLE'):return R
            # A named legacy profile can be weakened by its caller. Require the
            # published minimum procedures, not merely its type or Oxx/Sxx labels.
            imin=json.loads((ROOT/'fixtures/v4/contracts/output.json').read_bytes())['requirements']
            rmin=json.loads((ROOT/'fixtures/erc8404/lab/independent.json').read_bytes())['contract']['requirements']
            native_floor=all(ic.get('requirements',{}).get(k)==v for k,v in imin.items())  # GUARD inference_semantics
            review_floor=all(rc.get('requirements',{}).get(k)==v for k,v in rmin.items() if k!='O14')  # GUARD review_semantics
            return V if native_floor and review_floor else R
        procedures={
          'inference_profile':lambda:ir['C']['status'],
          'review_profile':lambda:rr['status'],
          'proof_byte_binding':lambda:eq(proof_sha,review_digest),
          'profile_commitments':profile_pins,
          'claim_values':lambda:combined(eq(claim.get(k),v) for k,v in expected.items()),
          'claim_fields':lambda:V if not unconsumed else R,
          'key_policy':keys,
          'controller_scope':controllers,
          'supported_scope':supported_scope,
        }
        unconsumed=sorted((set(claim)-FIELDS)|{'inference.'+k for k in set(i['claim'])-INFERENCE_FIELDS}|{'review.'+k for k in set(r['claim'])-REVIEW_FIELDS})
        for oid,entry in catalog.items():
            if not isinstance(entry,dict):checks[oid]=U;continue
            fn=procedures.get(entry.get('procedure'))
            checks[oid]=fn() if oid in KNOWN and fn else U
        if mode=='B':return output()
        required=contract['requirements'];missing=sorted(set(required)-set(catalog))
        # The supported claim type has a separately published minimum contract.
        # Caller-defined weaker contracts do not retain the same broad claim type.
        floor=json.loads((ROOT/'fixtures/integration/scenario-contract.json').read_bytes())['requirements']
        checks['scope_floor']=V if all(k in required and required[k]['procedure']==v['procedure'] and set(v['dependencies'])<=set(required[k]['dependencies']) for k,v in floor.items()) else R  # GUARD scope_floor
        checks['coverage']=V if not missing else R  # GUARD coverage
        checks['definitions']=V if all(catalog[k]==v for k,v in required.items() if k in catalog) else R  # GUARD definitions
        checks['dependencies']=V if all(d in required for v in required.values() for d in v['dependencies']) else R  # GUARD dependencies
        scope={k:claim.get(k) for k in sorted(FIELDS)}
        return output()
    except (KeyError,TypeError,ValueError,AttributeError):
        checks['malformed_evidence']=R;return output()

def admit(presented,case):
    """Fresh consumer verification against its own request/evidence/contract.
    Canonical serialization makes bool vs integer and extra fields unambiguous.
    """
    fresh=evaluate(case)
    if fresh['status']!=V:return {'status':fresh['status'],'authorized':False,'recomputed':fresh}  # GUARD admission_status
    try:matches=canonical(presented)==canonical(fresh)
    except (TypeError,ValueError):matches=False
    status=V if matches else R  # GUARD admission_equality
    return {'status':status,'authorized':status==V,'recomputed':fresh}
