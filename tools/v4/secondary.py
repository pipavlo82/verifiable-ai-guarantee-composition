"""Independent EIP712 implementation and arithmetic recomputation, not a second zk proof system."""
import copy,json,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'build/v3/python-deps')]
from eth_account import Account
from eth_account.messages import encode_typed_data
from eth_hash.auto import keccak
from src.v4.scenarios import base
def main():
    c=base();bundle=json.loads((ROOT/'evidence/v4/lab/bundle.json').read_bytes())
    schema=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {TYPES} from './src/v2/crypto.mjs'; console.log(JSON.stringify(TYPES));"],cwd=ROOT))
    def recover(d):
        types={d['type']:[{'name':n,'type':t} for n,t in schema[d['type']]]}
        return Account.recover_message(encode_typed_data(d['domain'],types,d['message']),signature=d['signature']).lower()
    docs=list(bundle['documents'].values())+[d for v in bundle['variants'].values() for d in v.values()]
    signatures=[recover(d)==d['signer'].lower() for d in docs]
    bad=copy.deepcopy(docs[0]);bad['message']['timestamp']+=1
    altered_rejected=recover(bad)!=bad['signer'].lower()
    invalid=copy.deepcopy(docs[0]);invalid['signature']='0x'+'00'*65
    try:invalid_rejected=recover(invalid)!=invalid['signer'].lower()
    except (ValueError,Exception) as e:invalid_rejected=type(e).__name__ in ('BadSignature','ValueError')
    raw=(ROOT/c['files']['raw_input']).read_bytes();p=c['documents']['provenance']['message']
    def fields(name):
        b=(ROOT/c['files'][name]).read_bytes();return struct.unpack('<'+'Q'*(len(b)//8),b)
    x=fields('input');w=fields('weights');y=fields('output');mod=18446744069414584321
    expected=tuple(sum(x[i*8+k]*w[k*8+j] for k in range(8))%mod for i in range(4) for j in range(8))
    out={'schema':'v4-second-implementation','signature_count':len(docs),'all_signatures_recovered':all(signatures),'altered_message_rejected':altered_rejected,'invalid_signature_rejected':invalid_rejected,'keccak_raw_matches':'0x'+keccak(raw).hex()==p['rawInputHash'],'python_matmul_recomputed':expected==y,'missing_evidence':'UNVERIFIABLE','scope':'eth-account/eth-keys signatures and Python arithmetic; same machine and artifacts; no independent human review or second native proof verifier'}
    out['passed']=all(v for v in out.values() if type(v)is bool);print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
