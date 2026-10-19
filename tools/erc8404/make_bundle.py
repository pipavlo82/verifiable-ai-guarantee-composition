import base64,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404.engine import ADAPTER,PROFILE,PROFILE_DIGEST,SCHEMA,canonical,sha
dest=ROOT/'fixtures/erc8404/rvr-bundle.json'
if dest.exists():raise RuntimeError('Refusing to overwrite frozen fixture')
raw=(ROOT/'evidence/v2/capture/a/proof.bin').read_bytes()
case={'claim':{'schema':'rvr.claim.sha256-equals.v0','operation':'SHA256_EQUALS','evidenceMember':'artifact','expectedDigest':sha(raw)},'evidenceSet':{'schema':'rvr.evidence-set.v0','members':[{'id':'artifact','status':'PRESENT','mediaType':'application/octet-stream','byteLength':str(len(raw)),'digest':sha(raw)}]},'payloadsBase64':{'artifact':base64.b64encode(raw).decode()}}
bundle=ADAPTER.make_bundle(case,PROFILE,PROFILE_DIGEST,SCHEMA)
dest.write_bytes(canonical(bundle));(dest.parent/'receipt.json').write_bytes(canonical(bundle['receipt']))
print(json.dumps({'profile_digest':PROFILE_DIGEST,'receipt_sha256':sha(canonical(bundle['receipt'])),'origin':'locally generated RVR identity receipt over preserved proof bytes; not external execution evidence'}))
