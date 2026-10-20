import hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019/fresh-public';OUT.mkdir(parents=True,exist_ok=True)
CACHE=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-public-20261019');REPO='pipavlo82/verifiable-ai-guarantee-composition'
published=json.loads((OUT.parent/'publication/published.json').read_bytes());rows=[]
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
def run(name,args,cwd=ROOT):
 p=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True,timeout=3600)
 for s in ('stdout','stderr'):(OUT/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
 rows.append({'name':name,'command':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()});dump(OUT/'commands.json',rows)
 print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(name+': '+p.stderr.decode(errors='replace')[-2000:])
 return p.stdout
if ROOT.exists():raise RuntimeError('Fresh target already exists; inspect before resuming')
run('clone',['git','-c','core.autocrlf=false','clone','--no-checkout','https://github.com/'+REPO+'.git',ROOT],CACHE)
run('checkout',['git','-c','core.autocrlf=false','checkout','--detach',published['commit']])
if run('head',['git','rev-parse','HEAD']).decode().strip()!=published['commit']:raise RuntimeError('Wrong HEAD')
for rel in ('build/formal-v1/crypto','build/v3/python-deps'):shutil.copytree(CACHE/rel,ROOT/rel)
for name in ('zkIE','recompute-kit','agent-ercs','receiptos-verify','ccip-router'):
 dest=ROOT/'build/v3/upstream'/name;dest.parent.mkdir(parents=True,exist_ok=True);run('source-'+name,['git','-c','core.autocrlf=false','clone','--no-hardlinks',CACHE/'build/v3/upstream'/name,dest])
run('prepare',[sys.executable,'-B','-X','utf8','tools/v3/prepare.py','--cargo-home',CACHE/'build/cargo-home'])
run('validation',[sys.executable,'-B','-X','utf8','tools/integration/validate.py'])
dirty=run('clean',['git','status','--porcelain']).decode().strip()
report=json.loads((ROOT/'build/integration/validation/report.json').read_bytes())
cross_checkout={name:(ROOT/'build/integration/validation'/(name+'-normal.stdout.log')).read_bytes()==(ROOT/'evidence/integration/validation'/(name+'-normal.stdout.log')).read_bytes() for name in ('comparison','mutations','pr5-targeted','fallback','read-tracking','admission')}
shutil.copytree(ROOT/'build/integration/validation',OUT/'validation');shutil.copytree(ROOT/'build/v2/native',OUT/'native')
dump(OUT/'report.json',{'commit':published['commit'],'branch':published['branch'],'root':str(ROOT),'fresh_clone_from_public_remote':True,'fresh_native_build':True,'clean':not dirty,'cross_checkout_determinism':cross_checkout,'validation':report,'passed':report['passed'] and not dirty and all(cross_checkout.values())})
print(json.dumps({'commit':published['commit'],'passed':report['passed'] and not dirty and all(cross_checkout.values())}))
