import copy,json
from adapter import *
from src.integration.cases import base
SCENARIOS=['positive','A_wrong_scope','B_missing_obligation','C_other_escrow','D_other_chain','E_other_recipient','F_other_amount','G_other_payment','H_replay','I_expired','J_unauthorized','J_revoked','K_evidence_digest','L_no_contract','M_unverified_field','N_self_judgment','O_duplicate','P_incorrect_authorization','Q_record_tamper','R_other_profile','nonce_reused_other_job','changed_scenario_digest','missing_profile','expired_after_signing','revoked_after_signing','false_returning_token','high_s','invalid_signature','refund_then_release','lying_token','negated_s']
def make(name,escrow='0x'+'11'*20,token='0x'+'22'*20,payment='1',other='0x'+'33'*20,target_payment=None):
 case=base();record=engine.evaluate(case)
 grant={'schema':'payer-lab-grant.v0','claim_type':engine.CLAIM_TYPE,'scenario':record['scenario'],'scope':engine.SCOPE,'scenario_contract_sha256':record['contract_sha256'],'verification_profile_sha256':sha(profile_bytes()),'intended_consumer':'claim-aware.escrow.consumer.v0','chain_id':'8453','escrow_contract':escrow.lower(),'token':token.lower(),'payment_id':str(payment),'job_id':'lab-proof-review-job-1','recipient':'0x0000000000000000000000000000000000000b0b','amount':'1000000','nonce':'7','expires_at':'2000','signer':LAB_PUB,'revoked_signers':[],'permission':'PAY_FOR_LOCAL_PROOF_REPLAY_AND_REVIEW_ONLY; no delivery assertion'}
 request=reference(case,grant);snapshot={k:request[k] for k in ('chain_id','escrow_contract','token','payment_id','recipient','amount')};snapshot['state']='Funded';now=1000;journal=set();profile=profile_bytes();signchain='8453';signescrow=escrow;signpayment=str(payment);approved=True;key=LAB_KEY
 if name=='A_wrong_scope':request['scope']='external-task-completed'
 elif name=='B_missing_obligation':case['catalog'].pop('J07');record=engine.evaluate(case)
 elif name=='C_other_escrow':snapshot['escrow_contract']=other
 elif name=='D_other_chain':snapshot['chain_id']='8454'
 elif name=='E_other_recipient':snapshot['recipient']='0x000000000000000000000000000000000000dead'
 elif name=='F_other_amount':snapshot['amount']='2000000'
 elif name=='G_other_payment':snapshot['payment_id']=str(target_payment or int(payment)+1)
 elif name=='H_replay':journal={'7'};snapshot['state']='Released'
 elif name=='nonce_reused_other_job':journal={'7'}
 elif name=='I_expired':now=2000
 elif name=='J_unauthorized':key=hashlib.sha256(b'other PUBLIC LAB key').digest()
 elif name=='J_revoked':grant['revoked_signers']=[LAB_PUB]
 elif name=='K_evidence_digest':request['evidence_sha256']='00'*32
 elif name=='L_no_contract':case['contract_bytes']=None;record=engine.evaluate(case)
 elif name=='M_unverified_field':case['inference']['claim']['unchecked']='not checked';record=engine.evaluate(case)
 elif name=='N_self_judgment':
  # Reuse genuine preserved self-judgment fixture from PR5, not an invalid forged signature.
  from src.v4_1.scenarios import cases
  chosen=next(x for x in cases() if x['name']=='negative_O14_self_judged')
  case['inference']=copy.deepcopy(chosen['case']);record=engine.evaluate(case);request['evidence_sha256']=sha(canonical(record['evidence_references']))
 elif name=='O_duplicate':snapshot['state']='Released'
 elif name=='P_incorrect_authorization':case['catalog'].pop('J01');record=engine.evaluate(case)
 elif name=='Q_record_tamper':record['scenario']='tampered'
 elif name=='R_other_profile':request['verification_profile_sha256']='11'*32
 elif name=='changed_scenario_digest':request['scenario_contract_sha256']='22'*32
 elif name=='missing_profile':profile=None
 elif name=='expired_after_signing':pass
 elif name=='revoked_after_signing':pass
 elif name=='false_returning_token':pass
 elif name=='refund_then_release':snapshot['state']='Refunded'
 raw=canonical(request);snapshot['request_sha256']=sha(raw);snapshot['policy_sha256']=sha(canonical(grant))
 result=assess(case,record,raw,grant,snapshot,now,journal,profile)
 decision=decision_reference(raw,grant,record)
 d=digest(signchain,signescrow,signpayment,request['nonce'],1,sha(raw),sha(canonical(grant)),approved,decision);verdict=laboratory_sign(d,key)
 if name=='high_s':verdict['signature']=verdict['signature'][:64]+bip340.N.to_bytes(32,'big').hex()
 if name=='negated_s':verdict['signature']=verdict['signature'][:64]+(bip340.N-int(verdict['signature'][64:],16)).to_bytes(32,'big').hex()
 if name=='invalid_signature':verdict['signature']='00'*64
 sigstatus=verify_bound_verdict(verdict,raw,grant,record)
 if sigstatus!=V:result['status']=R;result['authorized']=False;result['checks']['verdict_signature']=R
 # Direct-chain submission is deliberately exercised even when this adapter refuses.
 return {'name':name,'case':case,'record':record,'request':request,'request_bytes':raw.hex(),'grant':grant,'snapshot':snapshot,'now':now,'journal':sorted(journal),'profile_bytes':profile.hex() if profile is not None else None,'decision_ref':decision,'verdict':verdict,'adapter':result,'component_signature_valid':bip340.verify(bytes.fromhex(verdict['signer']),d,bytes.fromhex(verdict['signature']))}
