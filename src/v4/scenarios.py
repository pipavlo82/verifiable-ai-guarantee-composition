"""Fixed expected classifications, independent of evaluator results."""
import copy
from src.v4.model import ROOT,load,V,R,U

def base():
    bundle=load(ROOT/'evidence/v4/lab/bundle.json')
    names={'raw_input':'raw-input.bin','input':'input.bin','weights':'weights.bin','output':'output.bin','proof':'proof.bin','model':'model.json','result':'delivered.bin','observation':'execution-observation.json'}
    c={'files':{k:'evidence/v2/capture/a/'+v for k,v in names.items()},'documents':bundle['documents'],'claim':bundle['claim'],'policy':bundle['policy'],'consumed_nonces':[],'catalog':load(ROOT/'fixtures/v4/catalog.json'),'contract':load(ROOT/'fixtures/v4/contracts/output.json'),'scenario':'lab-output-v2','requested_claim':'LAB_OUTPUT_REPLAY_ADMISSIBLE'}
    c['files'].update(policy='evidence/v4/lab/policy.json',transform='evidence/v4/sources/identity.json')
    return c

def cases():
    b=base(); variants=load(ROOT/'evidence/v4/lab/bundle.json')['variants']; rows=[]
    def add(name,c,expected,boundary=None,kind='negative',expected_a=None,expected_b=None):
        rows.append({'name':name,'case':c,'expected':expected,'boundary':boundary,'kind':kind,'expected_A':expected_a,'expected_B':expected_b})
    add('positive_output',copy.deepcopy(b),V,kind='positive',expected_a=V,expected_b=V)
    for profile in ('replay','attestation','provenance'):
        c=copy.deepcopy(b);c['contract']=load(ROOT/f'fixtures/v4/contracts/{profile}.json');c['scenario']=c['contract']['scenario'];c['requested_claim']=c['contract']['claim_type'];c['catalog']={k:v for k,v in c['catalog'].items() if k in c['contract']['requirements']}
        if profile=='attestation':c['files']['raw_input']=None;c['files']['transform']=None
        add('positive_'+profile,c,V,kind='positive',expected_a=V,expected_b=V)
    for i in range(1,14):
        oid=f'O{i:02}';c=copy.deepcopy(b)
        if oid in variants:c['documents'].update(copy.deepcopy(variants[oid]))
        if oid=='O01':c['documents']['provenance']['signature']='0x'+'00'*65
        elif oid=='O02':c['files']['proof']='evidence/v2/survivor-audit/witnesses/invalid-claimed-scalar.bin';c['claim']['proofHash']=load(ROOT/'evidence/v4/lab/bundle.json')['badProofHash']
        elif oid=='O04':c['files']['transform']='fixtures/v4/invalid-transform.json'
        elif oid=='O05':c['claim']['inputHash']='0x'+'22'*32
        elif oid=='O06':c['claim']['modelHash']='0x'+'33'*32
        elif oid=='O10':c['files']['observation']=None
        elif oid=='O11':c['claim']['policyHash']='0x'+'44'*32
        elif oid=='O13':c['claim']['outputHash']='0x'+'55'*32
        status=U if oid=='O10' else R
        add('negative_'+oid,c,status,oid,expected_a=R if oid in ('O01','O02') else V,expected_b=status)
        omitted=copy.deepcopy(c);omitted['catalog'].pop(oid,None)
        add('omitted_'+oid,omitted,R,oid,'omission',expected_a=R if oid in ('O01','O02') else V,expected_b=V)
    missing={'O01':('document','provenance'),'O02':('file','proof'),'O03':('file','raw_input'),'O04':('file','transform'),'O05':('claim','inputHash'),'O06':('file','model'),'O07':('document','judgment'),'O08':('policy',None),'O09':('document','receipt'),'O10':('file','observation'),'O11':('file','policy'),'O12':('claim','scope'),'O13':('file','output')}
    for oid,(kind,key) in missing.items():
        c=copy.deepcopy(b)
        if kind=='policy':c['policy']=None
        else:c[{'document':'documents','file':'files','claim':'claim'}[kind]][key]=None
        add('missing_'+oid,c,U,oid,'missing')
    c=copy.deepcopy(b);c['scenario']='lab-output-v3-new-context';add('stale_scenario',c,R,'context',expected_a=V,expected_b=V)
    c=copy.deepcopy(b);c['catalog'].get('O05',{})['verification_procedure']='attestation_signature';c['claim']['inputHash']='0x'+'22'*32;add('counterfeit_definition',c,R,'definitions',expected_a=V,expected_b=V)
    c=copy.deepcopy(b);c['requested_claim']='EXTERNAL_TASK_SUCCESS';add('scope_overclaim',c,R,'composition',expected_a=V,expected_b=V)
    c=copy.deepcopy(b);c['contract']=None;add('missing_contract',c,U)
    c=copy.deepcopy(b);c['consumed_nonces']=[c['claim']['nonce']];add('replay',c,R)
    c=copy.deepcopy(b);c['policy']['domain']['chainId']=1;add('cross_domain',c,R)
    c=copy.deepcopy(b);c['files']['raw_input']=None;c['claim']['inputHash']='0x'+'22'*32;add('mixed_refutation_missing',c,R)
    c=copy.deepcopy(b);c['catalog'].pop('O13',None);c['claim']['outputHash']='0x'+'55'*32;c['self_reported_coverage']='COMPLETE';add('circular_self_inventory',c,R,expected_a=V,expected_b=V)
    c=copy.deepcopy(b);c['catalog'].get('O07',{})['dependencies']=[];add('removed_dependency_declaration',c,R)
    c=copy.deepcopy(b);c['contract']['requirements']['FUTURE_OBLIGATION']={'dependencies':[]};add('unknown_required_obligation',c,U)
    c=copy.deepcopy(b);c['contract']['requirements']['O07']['dependencies']=['UNAVAILABLE'];c['catalog'].get('O07',{})['dependencies']=['UNAVAILABLE'];add('unclosed_dependencies',c,R,'dependency_closure',expected_a=V,expected_b=V)
    return rows
