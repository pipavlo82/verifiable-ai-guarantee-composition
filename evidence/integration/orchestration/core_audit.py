import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019';ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019')
UP=Path('C:/Users/msi/Documents/Codex/vagc-erc8404/build/erc8404/upstream/recomputable-verification-receipts');PIN='9dd36e882dd372f264b77b179130948aa5adcbde'
manifest=json.loads((ROOT/'evidence/erc8404/upstream-tree-baseline.json').read_bytes());rows=[]
for path,digest in manifest.items():
 raw=subprocess.check_output(['git','show',PIN+':'+path],cwd=UP)
 rows.append({'path':path,'expected':digest,'actual':hashlib.sha256(raw).hexdigest(),'passed':hashlib.sha256(raw).hexdigest()==digest})
specs=json.loads((ROOT/'evidence/erc8404/sources/sources.json').read_bytes())
formal=[{'commit':s['commit'],'path':s['path'],'passed':hashlib.sha256((ROOT/'evidence/erc8404/sources'/s['path'].split('-')[-1]).read_bytes()).hexdigest()==s['sha256']} for s in specs if s['kind']=='proposal']
report={'pin':PIN,'verification':'Exact Git objects at pinned commit, local read-only cache; not a claim about future upstream HEAD','upstream_files':rows,'formal_sources':formal,'passed':all(r['passed'] for r in rows+formal)}
(OUT/'core-audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps({'files':len(rows),'formal_sources':len(formal),'passed':report['passed']}))
