import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');OUT=Path(__file__).resolve().parents[2]/'outputs/claim-aware-integration-20261019/admission';OUT.mkdir(parents=True,exist_ok=True);rows=[];values=[]
for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
 cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),'tools/integration/admission.py'];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=300)
 for s in ('stdout','stderr'):(OUT/(mode+'.'+s+'.log')).write_bytes(getattr(p,s))
 rows.append({'mode':mode,'command':cmd,'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()});values.append(p.stdout);print(mode,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(mode)
report={'commands':rows,'deterministic':len(set(values))==1,'controls':json.loads(values[0])['controls'],'passed':all(r['exit']==0 for r in rows) and len(set(values))==1}
(OUT/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
