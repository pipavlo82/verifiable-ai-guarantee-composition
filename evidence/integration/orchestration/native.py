import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');CACHE=Path('C:/Users/msi/Documents/Codex/vagc-erc8404/build/v3/upstream')
OUT=Path(__file__).resolve().parents[2]/'outputs/claim-aware-integration-20261019/native';OUT.mkdir(parents=True,exist_ok=True);rows=[]
def run(name,args):
 p=subprocess.run(list(map(str,args)),cwd=ROOT,capture_output=True,timeout=1800)
 for s in ('stdout','stderr'):(OUT/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
 rows.append({'name':name,'command':list(map(str,args)),'exit':p.returncode});(OUT/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n');print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(name)
for name in ('zkIE','recompute-kit','agent-ercs','receiptos-verify','ccip-router'):
 dest=ROOT/'build/v3/upstream'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():run('clone-'+name,['git','-c','core.autocrlf=false','clone','--no-hardlinks',CACHE/name,dest])
cargohome=ROOT/'build/cargo-home'
cache_registry=Path(__file__).resolve().parents[1]/'guarantee-composition-v1-20261016/cargo-home/registry'
shutil.copytree('\\\\?\\'+str(cache_registry),'\\\\?\\'+str(cargohome/'registry'),dirs_exist_ok=True)
run('native-prepare-complete-cache',[sys.executable,'-B','-X','utf8','tools/v3/prepare.py','--cargo-home',cargohome])
shutil.copytree(ROOT/'build/v2/native',OUT/'rust',dirs_exist_ok=True)
shutil.copytree(ROOT/'build/v3/setup-replay',OUT/'setup',dirs_exist_ok=True)
print('NATIVE_SOURCE_BUILD_COMPLETE')
