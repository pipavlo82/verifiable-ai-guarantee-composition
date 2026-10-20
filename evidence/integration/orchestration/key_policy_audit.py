import copy,json,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');sys.path.insert(0,str(ROOT))
from src.integration.engine import evaluate
from src.integration.cases import base,repin
from src.v4_1.scenarios import weak_output,CATALOG
c=base();c['inference']=weak_output();entry=copy.deepcopy(CATALOG['O14']);entry['verification_procedure']='attestation_signature';c['inference']['catalog']['O14']=entry
c['inference']['contract']['requirements']['O14']={k:entry[k] for k in ('applicable_policy','authority','dependencies','scope','verification_procedure')}
repin(c);r=evaluate(c);out=ROOT/'build/integration/development-key-policy';out.mkdir(parents=True,exist_ok=True)
for name,data in [('witness.json',c),('before.json',r)]: (out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
(out/'engine-before.py').write_bytes((ROOT/'src/integration/engine.py').read_bytes())
print(json.dumps({'status':r['status'],'authorized':r['authorized'],'finding':'O14 identifier present with substituted procedure is not evidence of actual key inequality'}))
