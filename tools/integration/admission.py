"""Record-tampering controls kept separate from the same-claim A/B/C/D study."""
import base64,copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.integration import engine as e
from src.integration.cases import base,cases,contract,repin
from src.erc8404.cases import base as review_base
from src.v4_1.scenarios import cases as inference_cases
def main():
    rows=[];good=base();record=e.evaluate(good)
    def add(name,r,c,expected):
        got=e.admit(r,c);rows.append({'name':name,'expected':expected,'presented':r,'case':c,'result':got,'passed':got['status']==expected and got['authorized']==(expected==e.V)})
    add('positive',record,good,e.V)
    for k in ('scenario','claim_type','contract_sha256'):
        r=copy.deepcopy(record);r[k]='forged';add('changed_'+k,r,good,e.R)
        r=copy.deepcopy(record);r.pop(k);add('missing_'+k,r,good,e.R)
    r=copy.deepcopy(record);r['status']=e.R;r['authorized']=True;add('refuted_true',r,good,e.R)
    r=copy.deepcopy(record);r['authorized']=1;add('numeric_flag',r,good,e.R)
    r=copy.deepcopy(record);r['verified_scope']['outputHash']='false';add('forged_verified_output',r,good,e.R)
    r=copy.deepcopy(record);r['evidence_references']['rvr_receipt_sha256']='forged';add('forged_evidence_reference',r,good,e.R)
    r=copy.deepcopy(record);r['unchecked']='extra';add('extra_result_field',r,good,e.R)
    for label,changes in [('same_scenario_other_contract',{'adequacy':'different relying policy'}),('other_key_policy',{'checker_policy':'SCENARIO_PROFILES'})]:
        c=base();contract(c,**changes);add(label,record,c,e.R)
    c=next(x['case'] for x in cases() if x['name']=='self_judgment');r=e.evaluate(c);r['authorized']=True;add('forged_authorized_on_refutation',r,c,e.R)
    c=base();c['contract_bytes']=None;add('missing_contract_preimage',record,c,e.U)
    c=base();c['review']['documents']['judgment']=None;add('missing_signer',record,c,e.U)
    c=base();c['review']['documents']['judgment']['signature']='0x'+'00'*65;add('invalid_signature',record,c,e.R)
    # PR6 LIST policy may authorize its explicitly narrower scope. The joint REJECT
    # policy must expose and refuse the added unconsumed output claim.
    c=base();c['review']=review_base('list');c['review']['claim']['outputHash']='false';repin(c);add('listed_unconsumed_outputHash',e.evaluate(c),c,e.R)
    c=base();c['inference']=next(x['case'] for x in inference_cases() if x['name']=='unconsumed_output_under_replay');repin(c);add('false_output_under_replay_contract',e.evaluate(c),c,e.R)
    report={'controls':len(rows),'rows':rows,'passed':all(r['passed'] for r in rows),'scope':'Presented-result integrity under unchanged evidence or explicitly altered consumer context; not mixed into claim-truth baseline false-authorization counts.'}
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
