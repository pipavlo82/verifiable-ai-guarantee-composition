import json,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');sys.path.insert(0,str(ROOT))
from src.integration.engine import evaluate
d=ROOT/'build/integration/development-key-policy';case=json.loads((d/'witness.json').read_bytes());r=evaluate(case)
(d/'after.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'status':r['status'],'failed_checks':{k:v for k,v in r['checks'].items() if v!='VERIFIED'}}))
if r['status']!='REFUTED' or r['authorized']:raise RuntimeError('Counterexample remains')
