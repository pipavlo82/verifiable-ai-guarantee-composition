"""Fetch/build fixed public sources. Does not generate or replace any evidence."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--online',action='store_true');p.add_argument('--cargo-home');a=p.parse_args()
    out=ROOT/'build/v3/setup-replay';out.mkdir(parents=True,exist_ok=True);rows=[]
    def run(name,cmd,cwd=ROOT):
        r=subprocess.run([str(v) for v in cmd],cwd=cwd,capture_output=True,timeout=1200)
        for s in ('stdout','stderr'):(out/(name+'.'+s+'.log')).write_bytes(getattr(r,s))
        rows.append({'name':name,'command':[str(v) for v in cmd],'cwd':str(cwd),'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
        (out/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({'step':name,'exit':r.returncode}),flush=True)
        if r.returncode:raise RuntimeError(name+' failed')
        return r.stdout.decode().strip()
    if run('node-version',['node','--version'])!='v22.15.0':raise RuntimeError('Node 22.15.0 required')
    bun='C:/Users/msi/.bun/bin/bun.exe' if os.name=='nt' else 'bun'
    if run('bun-version',[bun,'--version'])!='1.3.14':raise RuntimeError('Bun 1.3.14 required')
    sources=json.loads((ROOT/'evidence/v3/discovery/sources.json').read_text())+[json.loads((ROOT/'evidence/v3/public/ccip-router-source.json').read_text())]
    for s in sources:
        if s['repository']=='ethereum/ERCs':continue
        name=s['repository'].split('/')[1];dest=ROOT/'build/v3/upstream'/name
        if not dest.exists():
            if not a.online:raise RuntimeError('Missing source; use --online once: '+name)
            dest.parent.mkdir(parents=True,exist_ok=True)
            run('clone-'+name,['git','-c','core.autocrlf=false','clone','https://github.com/'+s['repository'],dest])
            run('pin-'+name,['git','checkout','--detach',s['commit']],dest)
    native=ROOT/'build/chain-v2/zkIE'
    if not native.exists():
        native.parent.mkdir(parents=True,exist_ok=True)
        run('clone-native',['git','-c','core.autocrlf=false','clone','--no-hardlinks',ROOT/'build/v3/upstream/zkIE',native])
    run('node-manifest',[sys.executable,'-B','research/formal-v1/prepare_crypto.py'])
    npm='npm.cmd' if os.name=='nt' else 'npm'
    if a.online:run('node-install',[npm,'ci','--ignore-scripts','--no-audit','--no-fund','--prefix','build/formal-v1/crypto'])
    cmd=[sys.executable,'-B','tools/v2/prepare.py']
    if a.online:cmd+=['--online']
    if a.cargo_home:cmd+=['--cargo-home',a.cargo_home]
    run('native',cmd)
    if a.online:run('python-install',[sys.executable,'-m','pip','install','--disable-pip-version-check','--no-deps','--require-hashes','--target',ROOT/'build/v3/python-deps','--report',out/'pip-report.json','-r','research/v3/requirements.lock.txt'])
    run('sources',[sys.executable,'-B','tools/v3/verify_sources.py'])
    return 0
if __name__=='__main__':raise SystemExit(main())
