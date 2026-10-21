import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');OUT=Path(__file__).resolve().parents[2]/('outputs/claim-aware-integration-20261019/legacy-unrestricted' if '--unrestricted' in sys.argv else 'outputs/claim-aware-integration-20261019/legacy');OUT.mkdir(parents=True,exist_ok=True);rows=[]
def run(name,args):
 cmd=[sys.executable,'-B','-X','utf8',*args];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=1200)
 for s in ('stdout','stderr'):(OUT/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
 rows.append({'name':name,'command':cmd,'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()});(OUT/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n');print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(name)
for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
 prefix=['-O'] if opt else []
 run('v0-tests-'+mode,prefix+['-m','unittest','discover','-s','tests','-p','test_composition.py','-v'])
 run('v0-mutations-'+mode,prefix+['tools/mutations.py'])
run('v1-complete',['research/formal-v1/validate.py','--out',str(OUT/'v1')])
