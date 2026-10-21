"""Three layers over actual crypto facts; contracts are independent input artifacts.

The trusted contract is not inferred from this dispatch table or the catalog.
No VERIFIED field in evidence is consumed. Missing prerequisites remain unknown.
"""
import base64, hashlib, json, subprocess
from pathlib import Path
from src.v2.composition import native_path

ROOT=Path(__file__).resolve().parents[2]
V='VERIFIED'; R='REFUTED'; U='UNVERIFIABLE'
def load(p): return json.loads(Path(p).read_bytes())
def combine(values):
    v=list(values)
    return R if R in v else U if not v or U in v else V
def check(value): return U if value is None else V if value else R
def equal(*values): return None if any(v is None for v in values) else len(set(map(lambda x:json.dumps(x,sort_keys=True),values)))==1

def facts(case):
    payload={}
    for k,p in case['files'].items():
        if p is None: continue
        try: payload[k]=(ROOT/p).read_bytes()
        except OSError: pass
    request={'documents':case['documents'],'bytes':{k:base64.b64encode(v).decode() for k,v in payload.items()}}
    crypto={}; native={'status':U}; commands=[]
    cmd=['node',str(ROOT/'src/v2/crypto.mjs')]
    try:
        run=subprocess.run(cmd,input=json.dumps(request).encode(),capture_output=True,timeout=30)
        commands.append({'command':cmd,'exit':run.returncode,'stdout':run.stdout.decode(),'stderr':run.stderr.decode()})
        if run.returncode==0: crypto=json.loads(run.stdout)
        if crypto.get('known_answers')!={'keccak_empty':True,'ether_mail_recovery':True}: crypto={}
    except (OSError,ValueError,subprocess.TimeoutExpired): pass
    if all(k in payload for k in ('input','weights','output','proof')):
        cmd=[str(native_path()),'verify',*[str(ROOT/case['files'][k]) for k in ('input','weights','output','proof')]]
        try:
            run=subprocess.run(cmd,capture_output=True,timeout=60)
            commands.append({'command':cmd,'exit':run.returncode,'stdout':run.stdout.decode(),'stderr':run.stderr.decode()})
            d=json.loads(run.stdout)
            if run.returncode in (0,1) and set(d)=={'native_verified','output_recomputed','statement_bound'} and all(type(v) is bool for v in d.values()): native={'status':check(run.returncode==0 and all(d.values())),**d}
        except (OSError,ValueError,subprocess.TimeoutExpired): pass
    return {'bytes':payload,'hashes':crypto.get('hashes',{}),'signatures':crypto.get('signatures',{}),'native':native,'commands':commands}

def predicates(case,f):
    h=f['hashes']; b=f['bytes']; docs=case['documents']; c=case['claim']; p=case.get('policy')
    def msg(role,key): return (docs.get(role) or {}).get('message',{}).get(key)
    def sig(role): return f['signatures'].get(role,{}).get('status',U)
    def common(key,*extra): return check(equal(*extra,*(msg(r,key) for r in ('provenance','judgment','receipt'))))
    def transform():
        if any(k not in b for k in ('raw_input','input','transform')) or docs.get('provenance') is None: return U
        spec=load(ROOT/'fixtures/v4/source-lock.json')['identity_spec_sha256']
        return check(hashlib.sha256(b['transform']).hexdigest()==spec and b['raw_input']==b['input'] and msg('provenance','inputHash')==h.get('input') and msg('provenance','sanitizationPipelineHash')==h.get('identity_pipeline'))
    def model():
        if p is None or 'model' not in b or 'weights' not in b: return U
        m=json.loads(b['model'])
        return combine([common('modelHash',c.get('modelHash'),p.get('modelHash'),h.get('model')),check(m.get('weights_sha256')==hashlib.sha256(b['weights']).hexdigest())])
    def judgment():
        checks=[sig('judgment'),check(equal(c.get('proofHash'),h.get('proof'),msg('judgment','proofHash'),msg('receipt','proofHash')))]
        for k in ('subject','action'): checks.append(check(equal(c.get(k),msg('judgment',k),msg('receipt',k))))
        if p is None: checks.append(U)
        else: checks.append(check(c.get('action')==p.get('action')))
        return combine(checks)
    def authority():
        if p is None:return U
        return combine(check(equal((docs.get(r) or {}).get('signer'),p.get('authorized',{}).get(r))) for r in ('provenance','judgment','receipt'))
    def receipt(): return combine([sig('receipt'),check(equal(c.get('executionId'),msg('receipt','executionId'),msg('judgment','executionId')))])
    def context():
        if p is None:return U
        policy_match=check(equal(p,json.loads(b['policy']))) if 'policy' in b else U
        return combine([policy_match,*(check(equal((docs.get(r) or {}).get('domain'),p.get('domain'))) for r in docs),check(equal(c.get('policyHash'),h.get('policy'),msg('judgment','policyHash'),msg('receipt','policyHash'))),check(equal(c.get('nonce'),msg('judgment','nonce'),msg('receipt','nonce'))),check(c.get('nonce') not in case['consumed_nonces'])])
    def scope():
        if p is None:return U
        return combine([check(equal(c.get('scope'),p.get('scope'),msg('judgment','scope'),msg('receipt','scope'))),check(c.get('claimKind')=='recompute-output')])
    return {
      'attestation_signature':lambda:sig('provenance'),
      'native_proof':lambda:f['native']['status'],
      'raw_preimage':lambda:check(equal(h.get('raw_input'),msg('provenance','rawInputHash'))),
      'transform_replay':transform,
      'input_binding':lambda:common('inputHash',c.get('inputHash'),h.get('input')),
      'model_binding':model,
      'judgment_inference':judgment,
      'authority':authority,
      'receipt_binding':receipt,
      'receipt_evidence':lambda:combine([check(equal(h.get('result'),msg('receipt','resultHash'))),check(equal(h.get('observation'),msg('receipt','observationHash')))]),
      'policy_domain_context':context,
      'evidence_scope':scope,
      'output_binding':lambda:common('outputHash',c.get('outputHash'),h.get('output')),
    }

def evaluate(case,f=None,mode=None):
    f=f or facts(case); cat=case['catalog']; contract=case.get('contract'); funcs=predicates(case,f)
    components={k:f['signatures'].get(k,{}).get('status',U) for k in ('provenance','judgment','receipt')}
    components['native']=f['native']['status']
    if mode=='A':return combine(components.values())
    checks={}; coverage={}; executed=[]
    def verify(oid):
        if oid not in cat: return
        procedure=cat[oid].get('verification_procedure'); executed.append(oid)
        try: checks[oid]=funcs[procedure]() if procedure in funcs else U
        except (KeyError,ValueError,TypeError): checks[oid]=U
    def force(oid):
        if oid in cat: checks[oid]=V; executed.append(oid)
    # Each site is separately mutated, never a runtime bypass option.
    verify('O01')
    verify('O02')
    verify('O03')
    verify('O04')
    verify('O05')
    verify('O06')
    verify('O07')
    verify('O08')
    verify('O09')
    verify('O10')
    verify('O11')
    verify('O12')
    verify('O13')
    for oid in cat:
        if oid not in checks:checks[oid]=U
    if mode=='B':return combine(checks.values())
    requirements={} if contract is None else contract.get('requirements',{})
    def presence(oid):
        if oid in requirements:coverage[oid]=check(oid in cat)
    presence('O01')
    presence('O02')
    presence('O03')
    presence('O04')
    presence('O05')
    presence('O06')
    presence('O07')
    presence('O08')
    presence('O09')
    presence('O10')
    presence('O11')
    presence('O12')
    presence('O13')
    # Unknown contract requirements cannot be silently ignored by the implementation.
    for oid in requirements:
        if oid not in {'O01','O02','O03','O04','O05','O06','O07','O08','O09','O10','O11','O12','O13'}: coverage[oid]=U
    if contract is None:
        coverage['contract']=U; composition=U
    else:
        coverage['context']=check(case['scenario']==contract['scenario'])
        definitions=[]
        for oid,req in requirements.items():
            if oid in cat:definitions.append(check(all(cat[oid].get(k)==v for k,v in req.items())))
        coverage['definitions']=combine(definitions)
        coverage['dependency_closure']=check(all(dep in requirements for req in requirements.values() for dep in req['dependencies']))
        composition=check(case['requested_claim']==contract['claim_type'])
    a=combine(components.values()); bv=combine(checks.values()); cv=combine([combine(coverage.values()),bv,composition])
    return {'A':{'status':a,'authorized':a==V},'B':{'status':bv,'authorized':bv==V,'claimed_coverage':'IMPLEMENTATION_INVENTORY_ONLY'},'C':{'status':cv,'authorized':cv==V},'coverage':coverage,'verification':checks,'composition':composition,'components':components,'executed':executed,'all_declared_pass':bv==V,'required':sorted(requirements),'missing_obligations':sorted(set(requirements)-set(cat)),'chain_status':'PARTIAL_CHAIN_VERIFIED'}
