import json,sys
from pathlib import Path
from adapter import V,R,U,verify_verdict
from vectors import SCENARIOS
CHAIN_REJECT={'C_other_escrow','D_other_chain','G_other_payment','H_replay','O_duplicate','J_unauthorized','false_returning_token','high_s','invalid_signature','negated_s','refund_then_release'}
B_ACCEPT={'positive','expired_after_signing','revoked_after_signing','false_returning_token','lying_token'}
UNAVAILABLE={'L_no_contract','missing_profile'}
EXECUTION_ONLY={'false_returning_token','lying_token'}
def main(folder):
 folder=Path(folder);rows=[]
 for name in SCENARIOS:
  a=json.loads((folder/(name+'-offchain.json')).read_bytes());e=json.loads((folder/(name+'-evm.json')).read_bytes())
  expected=V if name in B_ACCEPT else U if name in UNAVAILABLE else R
  if a['adapter']['status']!=expected or e['onchain_success']!=(name not in CHAIN_REJECT):raise RuntimeError('Unexpected classification '+name)
  vals={'A':verify_verdict(a['verdict'],a['grant'])==V,'B':a['adapter']['authorized'],'C':a['adapter']['authorized'] and e['onchain_success']}
  rows.append({'name':name,'kind':'execution-only' if name in EXECUTION_ONLY else 'positive' if name=='positive' else 'negative','expected_offchain':expected,'offchain':a['adapter']['status'],'onchain':'REFUTED' if not e['onchain_success'] else 'VERIFIED' if name=='positive' else 'NOT_COVERED','release_succeeded':e['onchain_success'],'observed_recipient_delta':e['recipient_delta'],'release_call_gas':e['release_call_gas'],'missing_obligations':a['adapter']['missing_obligations'],'modes':vals})
 domain=[r for r in rows if r['kind']!='execution-only']
 summary={m:{'false_authorizations':sum(r['kind']=='negative' and r['modes'][m] for r in domain),'correct_refusals':sum(r['kind']=='negative' and not r['modes'][m] for r in domain),'positive_authorizations':sum(r['kind']=='positive' and r['modes'][m] for r in domain),'unverifiable':sum(r['offchain']==U for r in domain) if m!='A' else 0,'missing_obligations':sum(bool(r['missing_obligations']) for r in domain) if m!='A' else 0} for m in 'ABC'}
 report={'scenario_count':len(rows),'authorization_comparison_count':len(domain),'execution_only_count':len(EXECUTION_ONLY),'rows':rows,'comparison':summary,'conditional_on_honest_offchain_gate':True,'raw_chain_accepts_not_full_policy_coverage':sum(r['onchain']=='NOT_COVERED' for r in rows),'gas_scope':'Foundry in-process release call with warmed storage; excludes tx intrinsic/calldata, Base L1 data fee and real funds. No actual payment cost incurred.','hypothetical_1_gwei_positive_call_wei':next(r['release_call_gas'] for r in rows if r['name']=='positive')*10**9,'verdict':'PARTIALLY_COMPATIBLE','guarantee':'LABORATORY_VERIFIED / PARTIAL_CHAIN_VERIFIED','passed':True}
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main(sys.argv[1])
