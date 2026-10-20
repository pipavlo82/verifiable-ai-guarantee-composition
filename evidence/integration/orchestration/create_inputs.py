import base64,hashlib,json,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');sys.path.insert(0,str(ROOT))
from src.v4_1.scenarios import upgrade
from src.v4.scenarios import base as ibase
from src.erc8404.cases import base as rbase
from src.integration.engine import canonical,contract_bytes
i=upgrade(ibase());r=rbase()
# A separately authored scenario contract. Its requirement set is not discovered by
# enumerating the engine's dispatch table. These are research policy obligations.
c={'schema':'claim-aware.integration.v1','scenario':'preserved-proof-a-replay-and-review',
 'claim_type':'LAB_REPLAY_AND_REVIEWED_PROOF_IDENTITY','scope':'local-output-replay-and-proof-byte-review',
 'profiles':{'inference':hashlib.sha256(json.dumps(i['contract'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),'inference_policy':hashlib.sha256((ROOT/i['files']['policy']).read_bytes()).hexdigest(),'review':hashlib.sha256(base64.b64decode(r['contract_bytes'])).hexdigest()},
 'checker_policy':'DISTINCT_KEYS_IN_EACH_PROFILE','controller_policy':'NOT_CLAIMED',
 'adequacy':'EXTERNAL_RESEARCH_ASSUMPTION; same investigators authored contract and engine',
 'requirements':{
 'J01':{'procedure':'inference_profile','dependencies':[]},
 'J02':{'procedure':'review_profile','dependencies':[]},
 'J03':{'procedure':'proof_byte_binding','dependencies':['J01','J02']},
 'J04':{'procedure':'profile_commitments','dependencies':[]},
 'J05':{'procedure':'claim_values','dependencies':['J01','J02','J03']},
 'J06':{'procedure':'claim_fields','dependencies':['J05']},
 'J07':{'procedure':'key_policy','dependencies':['J01','J02']},
 'J08':{'procedure':'controller_scope','dependencies':['J07']},
 'J09':{'procedure':'supported_scope','dependencies':['J01','J02']}}}
d=ROOT/'fixtures/integration';d.mkdir(parents=True,exist_ok=True)
(d/'scenario-contract.json').write_bytes(canonical(c))
(d/'catalog.json').write_bytes(canonical(c['requirements']))
(d/'PROVENANCE.json').write_text(json.dumps({'kind':'EXTERNAL_LABORATORY_COMPOSITION_POLICY','cryptographic_artifacts':'Original PR5 and PR6 bytes reused without changing signed assertions','subject_mapping':'Two distinct labels retained; equality applies only to actual proof bytes','contract_origin':'independently supplied fixture, not inferred from verifier inventory; external adequacy assumption'},indent=2)+'\n',encoding='utf8',newline='\n')
print(hashlib.sha256(canonical(c)).hexdigest())
