"""v4.1: two obligations v4 does not state, added without editing v4.

O14 checker_independence: where the scenario contract requires independent judgment, the
recovered judgment signer must differ from the recovered provenance (producer) signer. v4's
authority() compares each role's signer to policy only, so a policy that authorizes one key
for both roles passes O01-O13.

C binding: an authorized C names what it was established against,
{scenario, claim_type, contract_sha256}, with contract_sha256 recomputed here from the exact
contract object, never copied from the claim or from a result. Claim fields that no
contract-required obligation reads are listed as unconsumed_claim_fields and refuse C
(UNVERIFIABLE instead when a required check was itself UNVERIFIABLE, so its reads are unknown).
Consumption is observed (reads of the claim during each obligation's check), not declared.

admit() is the consumer side: it recomputes the digest from the contract the consumer holds.
"""
import hashlib, json
from src.v4.model import ROOT,load,V,R,U,combine,check,facts,predicates

KNOWN={f'O{i:02}' for i in range(1,15)}
def contract_digest(contract):
    return hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()

class Tracked(dict):
    """Claim view that records which keys a predicate reads."""
    def __init__(self,d):super().__init__(d);self.reads=set()
    def get(self,k,default=None):self.reads.add(k);return super().get(k,default)
    def __getitem__(self,k):self.reads.add(k);return super().__getitem__(k)

def independence(f):
    s=f['signatures']
    if any(s.get(r,{}).get('status')!=V or not s.get(r,{}).get('signer') for r in ('provenance','judgment')):return U
    return check(s['provenance']['signer'].lower()!=s['judgment']['signer'].lower())

def evaluate(case,f=None,mode=None):
    f=f or facts(case); cat=case['catalog']; contract=case.get('contract')
    claim=Tracked(case['claim'] or {}); funcs=predicates({**case,'claim':claim},f)
    funcs['checker_independence']=lambda:independence(f)
    components={k:f['signatures'].get(k,{}).get('status',U) for k in ('provenance','judgment','receipt')}
    components['native']=f['native']['status']
    if mode=='A':return combine(components.values())
    checks={}; coverage={}; executed=[]; reads={}
    def verify(oid):
        if oid not in cat: return
        procedure=cat[oid].get('verification_procedure'); executed.append(oid); claim.reads=set()
        try: checks[oid]=funcs[procedure]() if procedure in funcs else U
        except (KeyError,ValueError,TypeError): checks[oid]=U
        reads[oid]=sorted(claim.reads)
    def force(oid):
        if oid in cat: checks[oid]=V; executed.append(oid)
    for oid in sorted(KNOWN-{'O14'}):verify(oid)
    # Each new site is separately mutated, never a runtime bypass option.
    verify('O14')
    for oid in cat:
        if oid not in checks:checks[oid]=U
    if mode=='B':return combine(checks.values())
    requirements={} if contract is None else contract.get('requirements',{})
    def presence(oid):
        if oid in requirements:coverage[oid]=check(oid in cat)
    for oid in sorted(KNOWN-{'O14'}):presence(oid)
    presence('O14')
    for oid in requirements:
        if oid not in KNOWN: coverage[oid]=U
    consumed=set().union(*(reads.get(oid,[]) for oid in requirements))
    unconsumed=sorted(set(case['claim'] or {})-consumed)
    if contract is None:
        coverage['contract']=U; composition=U; claim_fields=U; binding=None
    else:
        coverage['context']=check(case['scenario']==contract['scenario'])
        definitions=[check(all(cat[oid].get(k)==v for k,v in req.items())) for oid,req in requirements.items() if oid in cat]
        coverage['definitions']=combine(definitions)
        coverage['dependency_closure']=check(all(dep in requirements for req in requirements.values() for dep in req['dependencies']))
        composition=check(case['requested_claim']==contract['claim_type'])
        # A catalogued required check that ended UNVERIFIABLE may not have read its fields.
        # Required obligations absent from the catalog are coverage's alarm, not this one.
        determinate=all(checks[oid] in (V,R) for oid in requirements if oid in cat)
        claim_fields=check(not unconsumed) if determinate else U
        binding={'scenario':contract['scenario'],'claim_type':contract['claim_type'],'contract_sha256':contract_digest(contract)}
    a=combine(components.values()); bv=combine(checks.values()); cv=combine([combine(coverage.values()),bv,composition,claim_fields])
    return {'A':{'status':a,'authorized':a==V},'B':{'status':bv,'authorized':bv==V,'claimed_coverage':'IMPLEMENTATION_INVENTORY_ONLY'},
            'C':{'status':cv,'authorized':cv==V,'binding':binding},'coverage':coverage,'verification':checks,'composition':composition,
            'claim_fields':claim_fields,'unconsumed_claim_fields':unconsumed,'claim_reads':reads,'components':components,'executed':executed,
            'all_declared_pass':bv==V,'required':sorted(requirements),'missing_obligations':sorted(set(requirements)-set(cat)),'chain_status':'PARTIAL_CHAIN_VERIFIED'}

def admit(result,contract,claim_type):
    """Consumer-side check. The digest is recomputed from the consumer's own contract."""
    c=result.get('C') or {}; b=c.get('binding')
    if not c.get('authorized') or not b or contract is None:return False
    same_contract=b.get('contract_sha256')==contract_digest(contract)
    same_claim=b.get('claim_type')==claim_type==contract.get('claim_type')
    return same_contract and same_claim
