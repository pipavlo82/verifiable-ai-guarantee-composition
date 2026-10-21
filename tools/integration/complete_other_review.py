import base64,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404.engine import ADAPTER,PROFILE,PROFILE_DIGEST,SCHEMA,canonical,sha
p=ROOT/('fixtures/integration/weak-review.json' if '--weak-authority' in sys.argv else 'fixtures/integration/other-proof-review.json');c=json.loads(p.read_bytes())
if 'bundle_bytes' in c:raise RuntimeError('Preserved fixture already completed')
source=c.get('source_artifact','evidence/v2/capture/b/proof.bin');raw=(ROOT/source).read_bytes()
case={'claim':{'schema':'rvr.claim.sha256-equals.v0','operation':'SHA256_EQUALS','evidenceMember':'artifact','expectedDigest':sha(raw)},'evidenceSet':{'schema':'rvr.evidence-set.v0','members':[{'id':'artifact','status':'PRESENT','mediaType':'application/octet-stream','byteLength':str(len(raw)),'digest':sha(raw)}]},'payloadsBase64':{'artifact':base64.b64encode(raw).decode()}}
b=ADAPTER.make_bundle(case,PROFILE,PROFILE_DIGEST,SCHEMA);c['bundle_bytes']=base64.b64encode(canonical(b)).decode();c['receipt_bytes']=base64.b64encode(canonical(b['receipt'])).decode()
c['laboratory_origin']={'producer':'local integration fixture generator','external_observation':False,'keys_persisted':False,'source_artifact':source}
p.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'proof_sha256':sha(raw),'receipt_sha256':sha(canonical(b['receipt']))}))
