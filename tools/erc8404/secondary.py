"""Second signature implementation and unchanged v4 counterexamples."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'build/v3/python-deps')]
from eth_account import Account
from eth_account.messages import encode_typed_data
from src.v4.scenarios import base as v4base
from src.v4.model import evaluate as v4evaluate

def main():
 schema=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {TYPES} from './src/v2/crypto.mjs'; console.log(JSON.stringify(TYPES));"],cwd=ROOT))
 docs=[]
 for p in sorted((ROOT/'fixtures/erc8404/lab').glob('*.json')):
  data=json.loads(p.read_bytes())
  if 'documents' in data:docs.extend(data['documents'].values());docs.extend(data.get('variants',{}).values())
 def recover(d):
  types={d['type']:[{'name':n,'type':t} for n,t in schema[d['type']]]}
  return Account.recover_message(encode_typed_data(d['domain'],types,d['message']),signature=d['signature']).lower()
 results=[recover(d)==d['signer'].lower() for d in docs]
 bad=copy.deepcopy(docs[0]);bad['message']['subject']='substituted';reject=recover(bad)!=bad['signer'].lower()
 c=v4base();w=json.loads((ROOT/'fixtures/erc8404/lab/v4-self-witness.json').read_bytes());c.update(w);c['files']['policy']='fixtures/erc8404/lab/v4-self-policy.json'
 self_result=v4evaluate(c)
 c=v4base();contract=json.loads((ROOT/'fixtures/v4/contracts/replay.json').read_bytes());c.update(contract=contract,scenario=contract['scenario'],requested_claim=contract['claim_type']);c['catalog']={k:v for k,v in c['catalog'].items() if k in contract['requirements']};c['claim']['outputHash']='0x'+'ff'*32
 replay_result=v4evaluate(c)
 report={'signature_count':len(docs),'all_recovered':all(results),'tampered_message_rejected':reject,'v4_self_judgment':self_result,'v4_false_output_under_replay':replay_result,'attribution':'User-reported Federico findings independently reconstructed; no review text present in public PR4 comments snapshot','scope':'genuine laboratory signatures, same machine second crypto implementation; v4 authorizes its narrow declared replay, not outputHash correctness','passed':all(results) and reject and self_result['C']['authorized'] and replay_result['C']['authorized']}
 print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
