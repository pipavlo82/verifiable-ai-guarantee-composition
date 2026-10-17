import copy
from src.v3.evidence import base_case
from src.v3.model import policy
def cases():
    rows=[]
    def add(name,claim,expected,mutate=lambda c,p:None,boundary=None):
        c=base_case();p=policy();mutate(c,p);rows.append({'name':name,'claim':claim,'expected':expected,'case':c,'request':p,'boundary':boundary})
    for claim in ('judgment_publication','claim_agreement','native_recomputation','local_receipt_binding'):add('positive_'+claim,claim,'VERIFIED')
    def sig(role):
        def change(c,p):
            if role=='cell2':c['cell2']['signature']['signature']='0x'+'00'*65
            else:c[role]['proof_event' if role=='ledger' else 'event']['sig']='00'*64
        return change
    add('bad_judgment_signature','judgment_publication','REFUTED',sig('ledger'),'judgment_signature')
    add('wrong_judgment_authority','judgment_publication','REFUTED',lambda c,p:p.update(ledger_key='00'*32),'judgment_authority')
    add('valid_signature_wrong_artifact_profile','judgment_publication','REFUTED',lambda c,p:c['ledger'].update(proof_event=copy.deepcopy(c['cell1']['event'])))
    add('bad_cell1_signature','claim_agreement','REFUTED',sig('cell1'),'cell1_signature')
    add('bad_cell2_signature','claim_agreement','REFUTED',sig('cell2'),'cell2_signature')
    add('wrong_cell_authority','claim_agreement','REFUTED',lambda c,p:p.update(cell2_key='0x'+'00'*20),'cell_authority')
    add('cross_subject','claim_agreement','REFUTED',lambda c,p:p.update(decision_ref='sha256:'+'00'*32),'decision_binding')
    add('wrong_claim','claim_agreement','REFUTED',lambda c,p:p.update(claim_id='sha256:'+'00'*32),'claim_binding')
    add('valid_judgment_wrong_action','claim_agreement','REFUTED',lambda c,p:p.update(verdict='approve'),'judgment_scope')
    add('cross_domain','claim_agreement','REFUTED',lambda c,p:p['domain'].update(chainId=31337),'domain')
    add('replay_context','claim_agreement','REFUTED',lambda c,p:p.update(as_of='2026-10-16T00:00:00Z'),'as_of')
    add('invalid_native_proof','native_recomputation','REFUTED',lambda c,p:c.update(native='invalid'),'native_proof')
    add('wrong_model','native_recomputation','REFUTED',lambda c,p:p.update(model_sha256='00'*32),'native_model')
    add('invalid_receipt_root','local_receipt_binding','REFUTED',lambda c,p:c['receipt']['anchor'].update(receipt_root='0x'+'00'*32),'receipt_root')
    add('valid_receipt_wrong_execution_subject','local_receipt_binding','REFUTED',lambda c,p:p.update(proof_sha256='00'*32),'receipt_subject')
    for role,claim in [('ledger','judgment_publication'),('cell1','claim_agreement'),('cell2','claim_agreement'),('native','native_recomputation'),('receipt','local_receipt_binding')]:add('missing_'+role,claim,'UNVERIFIABLE',lambda c,p,role=role:c.update({role:None}))
    for key,claim in [('ledger_key','judgment_publication'),('cell2_key','claim_agreement'),('decision_ref','claim_agreement'),('claim_id','claim_agreement'),('verdict','claim_agreement'),('domain','claim_agreement'),('as_of','claim_agreement'),('model_sha256','native_recomputation'),('proof_sha256','local_receipt_binding')]:add('missing_binding_'+key,claim,'UNVERIFIABLE',lambda c,p,key=key:p.update({key:None}))
    add('historical_execution_unestablished','historical_cell_execution','UNVERIFIABLE')
    add('full_external_chain_missing','external_full_chain','UNVERIFIABLE')
    def mixed(c,p):c['cell1']=None;p['domain']['chainId']=31337
    add('mixed_refuted_and_missing','claim_agreement','REFUTED',mixed)
    return rows
