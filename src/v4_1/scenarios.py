"""Fixed expected classifications for v4.1, independent of evaluator results.

Every v4 row is carried with its v4 expectation, with two declared adjustments:
the output contract is the v4.1 revision (adds O14) and the catalog carries O14 wherever
that contract applies; the narrow-profile positives present only the claim fields their
contract consumes (declared below, not derived from the evaluator).
"""
import copy
from src.v4.model import ROOT,load,V,R,U
from src.v4 import scenarios as v4

CATALOG=load(ROOT/'fixtures/v4_1/catalog.json')
OUTPUT=load(ROOT/'fixtures/v4_1/contracts/output.json')
OUTPUT_V4=load(ROOT/'fixtures/v4/contracts/output.json')
# Claim fields each narrow contract's obligations read (O01/O02/O03/O04/O08/O10 read none).
PROFILE_FIELDS={
 'replay':['subject','inputHash','modelHash','proofHash','action','scope','executionId','policyHash','nonce','claimKind'],
 'attestation':['policyHash','nonce'],
 'provenance':['policyHash','nonce'],
}
def upgrade(c):
    if c['contract'] is None or c['contract'].get('scenario')==OUTPUT['scenario']:
        if c['contract'] is not None:
            extra={k:v for k,v in c['contract']['requirements'].items() if k not in OUTPUT_V4['requirements'] or v!=OUTPUT_V4['requirements'][k]}
            c['contract']={**copy.deepcopy(OUTPUT),**{k:v for k,v in c['contract'].items() if k not in ('requirements','revision','schema')}}
            c['contract']['requirements'].update(copy.deepcopy(extra))
        if 'O14' not in c['catalog'] and 'O14' in CATALOG:c['catalog']['O14']=copy.deepcopy(CATALOG['O14'])
    return c
def narrow(c,profile):
    c['claim']={k:v for k,v in c['claim'].items() if k in PROFILE_FIELDS[profile]};return c

def self_judged_base():
    b=load(ROOT/'evidence/v4_1/self-judged/bundle.json');c=upgrade(v4.base())
    c['documents']=b['documents'];c['claim']=b['claim'];c['policy']=b['policy'];c['files']['policy']='evidence/v4_1/self-judged/policy.json'
    return c

def weak_output():
    """The self-judged evidence under the v4 output contract (no O14): what v4 authorizes."""
    c=self_judged_base();c['contract']=copy.deepcopy(OUTPUT_V4);c['catalog'].pop('O14',None);return c

def cases():
    rows=[]
    for r in v4.cases():
        r=copy.deepcopy(r);r['origin']='v4';upgrade(r['case'])
        if r['name'].startswith('positive_') and r['name']!='positive_output':narrow(r['case'],r['name'][9:])
        # O14 depends on O01: with the provenance signature invalid, signers cannot be compared.
        if r['name']=='omitted_O01':r['expected_B']=U
        rows.append(r)
    def add(name,c,expected,boundary=None,kind='negative',expected_a=None,expected_b=None,v4_expected=None,v4_case=None):
        rows.append({'name':name,'case':c,'expected':expected,'boundary':boundary,'kind':kind,'expected_A':expected_a,'expected_B':expected_b,'origin':'v4.1','v4_expected_C':v4_expected,'v4_case':v4_case or c})
    # O14: producer key also signs the judgment; policy authorizes it for both roles.
    add('negative_O14_self_judged',self_judged_base(),R,'O14',expected_a=V,expected_b=R,v4_expected=V,v4_case=weak_output())
    c=self_judged_base();c['catalog'].pop('O14',None);add('omitted_O14',c,R,'O14','omission',expected_a=V,expected_b=V)
    # C binding: the negative_O13 claim (false outputHash) presented under the replay contract.
    c=copy.deepcopy(v4.base());c['claim']['outputHash']='0x'+'55'*32
    c['contract']=load(ROOT/'fixtures/v4/contracts/replay.json');c['scenario']=c['contract']['scenario'];c['requested_claim']=c['contract']['claim_type']
    c['catalog']={k:v for k,v in c['catalog'].items() if k in c['contract']['requirements']}
    add('unconsumed_output_under_replay',c,R,'claim_fields',expected_a=V,expected_b=V,v4_expected=V)
    return rows

def reuse_cases():
    """Consumer-side admission of an authorized result. Fixed expectations."""
    replay=load(ROOT/'fixtures/v4/contracts/replay.json')
    weak=weak_output()
    return [
     # (name, row producing the result, contract the consumer holds, claim type requested, expected admit)
     ('control_replay_same_contract','positive_replay',replay,replay['claim_type'],True),
     ('control_output_same_contract','positive_output',OUTPUT,OUTPUT['claim_type'],True),
     ('reused_under_other_claim_type','positive_replay',replay,OUTPUT['claim_type'],False),
     ('reused_under_other_contract',weak,OUTPUT,OUTPUT['claim_type'],False),
    ]
