"""Predeclared outcomes. Fixtures are evidence, not verification flags."""
import base64,copy,json
from src.v4.scenarios import base as original_inference
from src.v4_1.scenarios import upgrade,self_judged_base,weak_output,CATALOG
from src.erc8404.cases import base as review_base,cases as review_cases
from src.integration.engine import ROOT,V,R,U,sha,canonical,contract_bytes

def base():
    i=upgrade(original_inference());r=review_base();c=json.loads((ROOT/'fixtures/integration/scenario-contract.json').read_bytes())
    claim={'scenario':c['scenario'],'claim_type':c['claim_type'],'scope':c['scope'],'inference_subject':i['claim']['subject'],
      'review_subject':r['claim']['subject'],'proof_sha256':sha((ROOT/i['files']['proof']).read_bytes()),
      **{k:i['claim'][k] for k in ('inputHash','modelHash','outputHash')}}
    return {'contract_bytes':contract_bytes(c),'catalog':json.loads((ROOT/'fixtures/integration/catalog.json').read_bytes()),'claim':claim,'inference':i,'review':r}

def contract(case,**changes):
    c=json.loads(base64.b64decode(case['contract_bytes']));c.update(changes);case['contract_bytes']=contract_bytes(c);return c

def repin(case):
    i=case['inference']['contract'];r=json.loads(base64.b64decode(case['review']['contract_bytes']))
    contract(case,profiles={'inference':sha(json.dumps(i,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),'inference_policy':sha((ROOT/case['inference']['files']['policy']).read_bytes()),'review':sha(canonical(r))})

def cases():
    rows=[]
    def add(name,c,expected=R,kind='negative',target=None):rows.append({'name':name,'case':copy.deepcopy(c),'expected':expected,'kind':kind,'target':target})
    add('positive',base(),V,'positive')
    for k in sorted(base()['claim']):
        c=base();c['claim'][k]='unrelated';add('wrong_'+k,c,target='J05')
        c=base();c['claim'].pop(k);add('missing_'+k,c,U,target='J05')
    c=base();c['claim']['payment']='authorized';add('unknown_claim_field',c,target='J06')
    c=base();c['claim']['outputHash']='0x'+'99'*32;add('read_without_validation',c,target='J05')
    c=base();c['contract_bytes']=None;add('missing_contract_preimage',c,U,target='preimage')
    c=base();c['contract_bytes']=base64.b64encode(b'{"schema":').decode();add('malformed_contract',c)
    c=base();raw=base64.b64decode(c['contract_bytes']);c['contract_bytes']=base64.b64encode(raw+b' ').decode();add('noncanonical_contract',c)
    c=base();c['inference']['contract']['revision']=4;add('altered_profile_contract',c,target='J04')
    c=base();c['inference']['contract']['requirements'].pop('O02');c['inference']['catalog'].pop('O02')
    for entry in c['inference']['contract']['requirements'].values():entry['dependencies']=[d for d in entry['dependencies'] if d!='O02']
    for entry in c['inference']['catalog'].values():entry['dependencies']=[d for d in entry['dependencies'] if d!='O02']
    repin(c);add('inference_name_without_native_obligation',c,target='inference_semantics')
    c=base();c['inference']=self_judged_base();add('self_judgment',c,target='J01')
    c=base();c['inference']['catalog'].pop('O14');add('missing_O14',c,target='J01')
    c=base();c['inference']['documents']['judgment']=None;add('missing_identity_evidence',c,U,target='J01')
    c=base();c['review']['documents']['judgment']['signature']='0x'+'00'*65;add('invalid_review_signature',c,target='J02')
    c=base();c['review']['documents']['judgment']=c['review']['variants']['wrong_artifact'];add('wrong_review_artifact',c,target='J02')
    c=base();c['inference']['claim']['outputHash']='0x'+'99'*32;add('altered_inference_claim',c,target='J01')
    c=base();c['inference']['files']['proof']='evidence/v2/survivor-audit/witnesses/invalid-claimed-scalar.bin';add('altered_proof',c)
    c=base();c['inference']['files']['proof']=None;add('missing_proof',c,U)
    c=base();bundle=json.loads(base64.b64decode(c['review']['bundle_bytes']));bundle.pop('verificationProfile');c['review']['bundle_bytes']=base64.b64encode(canonical(bundle)).decode();add('missing_verification_profile',c,R,target='J02')
    c=base();c['inference']['files']['proof']='../outside.bin';add('path_escape',c)
    c=base();contract(c,controller_policy='INDEPENDENT_REAL_WORLD_CONTROLLERS');add('same_controller_not_established',c,U,target='J08')
    c=base();contract(c,scope='historical-external-task-success');c['claim']['scope']='historical-external-task-success';add('receipt_valid_external_claim_unsupported',c,target='J09')
    c=base();c['inference']=weak_output();repin(c);add('independence_requirement_removed_from_profile',c,target='J07')
    c=base();c['inference']=weak_output();entry=copy.deepcopy(CATALOG['O14']);entry['verification_procedure']='attestation_signature';c['inference']['catalog']['O14']=entry
    c['inference']['contract']['requirements']['O14']={k:entry[k] for k in ('applicable_policy','authority','dependencies','scope','verification_procedure')};repin(c);add('O14_name_with_wrong_semantics',c,target='key_identity')
    c=base();c['inference']=weak_output();repin(c);contract(c,checker_policy='SCENARIO_PROFILES');add('self_allowed_by_explicit_scenario',c,V,'positive')
    c=base();original_policy=json.loads(base64.b64decode(c['contract_bytes']))['profiles']['inference_policy'];c['inference']=weak_output();repin(c);ct=contract(c,checker_policy='SCENARIO_PROFILES');ct['profiles']['inference_policy']=original_policy;c['contract_bytes']=contract_bytes(ct);add('authority_policy_substitution',c,R,target='policy_binding')
    for oid in sorted(base()['catalog']):
        c=base();c['catalog'].pop(oid);add('omitted_'+oid,c,target='coverage')
    c=base();c['catalog']['J01']['dependencies']=[];c['catalog']['J01']['procedure']='claim_fields';add('counterfeit_definition',c,target='definitions')
    c=base();ct=json.loads(base64.b64decode(c['contract_bytes']));ct['requirements'].pop('J05');ct['requirements']['J06']['dependencies']=[];c['catalog']=copy.deepcopy(ct['requirements']);c['contract_bytes']=contract_bytes(ct);c['claim']['outputHash']='false';add('weakened_contract_keeps_broad_claim',c,target='scope_floor')
    c=base();ct=json.loads(base64.b64decode(c['contract_bytes']));ct['requirements']['J01']['dependencies']=['UNDECLARED'];c['catalog']['J01']['dependencies']=['UNDECLARED'];c['contract_bytes']=contract_bytes(ct);add('missing_dependency',c,target='dependencies')
    c=base();ct=json.loads(base64.b64decode(c['contract_bytes']));ct['requirements']['UNKNOWN']={'procedure':'unimplemented','dependencies':[]};c['contract_bytes']=contract_bytes(ct);add('unknown_missing_obligation',c,R)
    c['catalog']['UNKNOWN']={'procedure':'unimplemented','dependencies':[]};add('unknown_present_obligation',copy.deepcopy(c),U)
    c=base();ct=json.loads(base64.b64decode(c['contract_bytes']));ct['requirements']['UNKNOWN']={'procedure':'claim_fields','dependencies':[]};c['catalog']['UNKNOWN']=copy.deepcopy(ct['requirements']['UNKNOWN']);c['contract_bytes']=contract_bytes(ct);add('unknown_id_known_procedure',c,U,target='unknown_dispatch')
    c=base();c['review']=next(x['case'] for x in review_cases() if x['name']=='missing_committed_payload');add('missing_receipt_payload',c,U,target='J02')
    c['claim']['outputHash']='wrong';add('mixed_refutation_missing',copy.deepcopy(c),R)
    # Separate laboratory signatures over a distinct already preserved proof. Never an external observation.
    p=ROOT/'fixtures/integration/other-proof-review.json'
    if p.exists():
        c=base();c['review']=json.loads(p.read_bytes());repin(c);c['claim']['review_subject']=c['review']['claim']['subject'];add('valid_components_different_proof',c,R,target='J03')
    p=ROOT/'fixtures/integration/weak-review.json'
    if p.exists():
        c=base();c['review']=json.loads(p.read_bytes());repin(c);contract(c,checker_policy='SCENARIO_PROFILES');c['claim']['review_subject']=c['review']['claim']['subject'];add('review_name_without_authority_obligation',c,R,target='review_semantics')
    return rows
