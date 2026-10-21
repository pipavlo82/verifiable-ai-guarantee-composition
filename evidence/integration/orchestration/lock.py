import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019';ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019')
pins=json.loads((OUT/'phase1/pins.json').read_bytes());core=json.loads((ROOT/'fixtures/erc8404/core-lock.json').read_bytes());imports=json.loads((OUT/'pr5-import.json').read_bytes())
files=subprocess.check_output(['git','ls-tree','-r','--name-only',pins['prs']['6']['head']],cwd=ROOT).decode().splitlines()
preserved={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files if p not in ('README.md','artifacts.sha256.json')}
data={'source_shas':{'main':pins['main'],**{'pr'+n:p['head'] for n,p in pins['prs'].items()}},'frozen_core':{'evidence/erc8404/core/'+p:h for p,h in core.items()},'pr5_import':imports['files'],'pr6_preserved':preserved}
(ROOT/'fixtures/integration/source-lock.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:len(data[k]) for k in ('frozen_core','pr5_import','pr6_preserved')}))
