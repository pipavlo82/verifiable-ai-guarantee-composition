"""Foundry FFI only. Deterministic test keys; no remote APIs or broadcast support."""
import json,os,sys
from pathlib import Path
from vectors import make
from adapter import LAB_PUB,word
if sys.argv[1]=='pubkey':print('0x'+LAB_PUB)
elif sys.argv[1]=='vector':
 name,escrow,token,payment,other,target=sys.argv[2:8];v=make(name,escrow,token,payment,other,target)
 out=Path(os.environ['LAB_EVIDENCE_DIR']);out.mkdir(parents=True,exist_ok=True)
 (out/(name+'-offchain.json')).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
 r=v['request'];s=v['verdict']['signature'];code={'VERIFIED':0,'REFUTED':1,'UNVERIFIABLE':2}[v['adapter']['status']]
 b=bytes.fromhex(v['snapshot']['request_sha256']+v['snapshot']['policy_sha256']+v['decision_ref']+s)+word(r['nonce'])+word(v['adapter']['authorized'])+word(code)
 print('0x'+b.hex())
