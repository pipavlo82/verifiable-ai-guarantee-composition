"""Same retained genuine evidence, adversarial substitutions and explicit expectations."""
import copy
from pathlib import Path
from .composition import CAP, ROOT, base_case, read_json
def scenarios():
    rows=[]
    def put(name,expected,edit=lambda c:None,boundary=None):
        c=base_case();edit(c);rows.append({'name':name,'expected':expected,'boundary':boundary,'case':c})
    put('valid_recomputation','VERIFIED')
    put('complete_historical_chain_unavailable','UNVERIFIABLE',lambda c:c['claim'].update(claimKind='historical-external-execution'),'claim_strength')
    put('wrong_claim_input','REFUTED',lambda c:c['claim'].update(inputHash='0x'+'12'*32),'input_binding')
    put('cross_subject','REFUTED',lambda c:c['claim'].update(subject='unrelated-subject'),'subject_binding')
    put('wrong_model_version','REFUTED',lambda c:c['claim'].update(modelHash='0x'+'23'*32),'model_binding')
    put('wrong_proof_reference','REFUTED',lambda c:c['claim'].update(proofHash='0x'+'34'*32),'proof_binding')
    put('valid_judgment_wrong_action','REFUTED',lambda c:c['documents'].update(judgment=read_json(CAP/'a/wrong-action-judgment.json')),'action_binding')
    put('valid_receipt_wrong_execution','REFUTED',lambda c:c['documents'].update(receipt=read_json(CAP/'a/wrong-execution-receipt.json')),'execution_binding')
    put('invalid_authority_valid_signature','REFUTED',lambda c:c['documents'].update(judgment=read_json(CAP/'a/outsider-judgment.json')),'authority')
    put('cross_domain_valid_signature','REFUTED',lambda c:c['documents'].update(judgment=read_json(CAP/'a/other-domain-judgment.json')),'domain')
    put('replay','REFUTED',lambda c:c['consumed_nonces'].append(c['claim']['nonce']),'replay')
    put('scope_escalation','REFUTED',lambda c:c['claim'].update(scope='production-task-completion'),'scope')
    put('wrong_policy','REFUTED',lambda c:c['claim'].update(policyHash='0x'+'45'*32),'policy_binding')
    put('wrong_output_claim','REFUTED',lambda c:c['claim'].update(outputHash='0x'+'56'*32),'output_binding')
    put('raw_input_substitution','REFUTED',lambda c:c['files'].update(raw_input=str(CAP/'b/raw-input.bin')),'provenance_preimage')
    put('receipt_result_substitution','REFUTED',lambda c:c['files'].update(result=str(CAP/'b/delivered.bin')),'receipt_evidence')
    put('missing_judgment','UNVERIFIABLE',lambda c:c['documents'].update(judgment=None))
    put('missing_input_bytes','UNVERIFIABLE',lambda c:c['files'].update(input=str(ROOT/'build/v2/nonexistent-input')))
    def mixed(c):c['documents']['judgment']=None;c['claim']['modelHash']='0x'+'67'*32;c['consumed_nonces'].append(c['claim']['nonce'])
    put('mixed_refutation_missing','REFUTED',mixed)
    def bad_signature(c):c['documents']['judgment']['signature']='0x'+'00'*65
    put('invalid_signature','REFUTED',bad_signature)
    def bad_provenance(c):c['documents']['provenance']['signature']='0x'+'00'*65
    put('invalid_provenance_signature','REFUTED',bad_provenance)
    def bad_receipt(c):c['documents']['receipt']['signature']='0x'+'00'*65
    put('invalid_receipt_signature','REFUTED',bad_receipt)
    put('valid_receipt_used_as_judgment','REFUTED',lambda c:c['documents'].update(judgment=copy.deepcopy(c['documents']['receipt'])),'artifact_types')
    def wrong_native(c):
        c['files']['input']=str(CAP/'b/input.bin')
        c['files']['raw_input']=str(CAP/'b/raw-input.bin')
    put('native_proof_wrong_input','REFUTED',wrong_native)
    # A genuinely valid other execution's complete native component retains local validity.
    def other_native(c):
        for k,n in [('input','input.bin'),('weights','weights.bin'),('output','output.bin'),('proof','proof.bin'),('raw_input','raw-input.bin')]:c['files'][k]=str(CAP/'b'/n)
    put('valid_other_native_component','REFUTED',other_native)
    put('unknown_claim_kind','UNVERIFIABLE',lambda c:c['claim'].update(claimKind='unknown'))
    return rows
