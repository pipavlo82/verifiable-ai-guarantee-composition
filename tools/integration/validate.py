"""Independent execution logs. Never regenerate historical evidence or fixtures."""
import argparse,hashlib,json,os,platform,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/integration/validation');p.add_argument('--skip-inventory',action='store_true');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True);commands=[];values={}
    def source_inventory():return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('src/integration','tools/integration','tests/integration','fixtures/integration') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    source_before=source_inventory()
    def run(name,args,opt=False,external=False):
        cmd=list(map(str,args)) if external else [sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*map(str,args)]
        start=time.perf_counter();r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=2400)
        for s in ('stdout','stderr'):(out/(name+'.'+s+'.log')).write_bytes(getattr(r,s))
        count=re.search(rb'Ran (\d+) tests',r.stderr)
        commands.append({'name':name,'command':cmd,'cwd':str(ROOT),'exit':r.returncode,'elapsed_seconds':time.perf_counter()-start,'tests':int(count[1]) if count else None,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
        (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n',encoding='utf8',newline='\n');values[name]=r.stdout;print(name,r.returncode,flush=True)
        if r.returncode:raise RuntimeError(name+'; inspect raw logs')
    if not a.skip_inventory:run('inventory-before',['tools/verify_artifacts.py'])
    run('integrity-before',['tools/integration/integrity.py'])
    run('source-pins',['tools/v3/verify_sources.py'])
    run('core-python',['evidence/erc8404/core/conformance/rvr-v0/adapter.py','--check'])
    bun='C:/Users/msi/.bun/bin/bun.exe' if os.name=='nt' else 'bun'
    run('core-typescript',[bun,'evidence/erc8404/core/conformance/rvr-v0/adapter.ts','--check'],external=True)
    for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
        run('tests-'+mode,['-m','unittest','discover','-s','tests/integration','-v'],opt)
        run('comparison-'+mode,['tools/integration/run.py'],opt)
        run('mutations-'+mode,['tools/integration/mutations.py','--out',out/('mutations-'+mode)],opt)
        run('pr5-targeted-'+mode,['tools/integration/pr5_controls.py'],opt)
        run('fallback-'+mode,['tools/integration/survivor.py'],opt)
        run('read-tracking-'+mode,['tools/integration/read_tracking.py'],opt)
        run('admission-'+mode,['tools/integration/admission.py'],opt)
    run('secondary-crypto-native',['tools/integration/secondary.py'])
    run('secondary-pr6',['tools/erc8404/secondary.py'])
    for suite in ('v2','v3','v4','v4_1','erc8404'):
        run('regression-'+suite,['-m','unittest','discover','-s','tests/'+suite,'-v'])
    run('benchmark',['tools/integration/run.py','--benchmark'])
    run('integrity-after',['tools/integration/integrity.py'])
    if not a.skip_inventory:run('inventory-after',['tools/verify_artifacts.py'])
    det={k:len({values[k+'-'+m] for m in ('normal','repeat','optimized')})==1 for k in ('comparison','mutations','pr5-targeted','fallback','read-tracking','admission')}
    comparison=json.loads(values['comparison-normal']);report={'environment':{'python':sys.version,'platform':platform.platform(),'node':subprocess.check_output(['node','--version'],text=True).strip()},'commands':commands,'source_inventory':source_before,'source_unchanged':source_before==source_inventory(),'determinism':det,'scenarios':comparison['scenarios'],'comparison':comparison['summary'],'mutations':json.loads(values['mutations-normal'])['counts'],'passed':all(det.values()) and source_before==source_inventory()}
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
