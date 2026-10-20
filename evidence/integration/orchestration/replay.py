import hashlib,json,platform,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019';number=sys.argv[1]
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019-pr'+number);dest=OUT/('pr'+number);dest.mkdir(parents=True,exist_ok=True);rows=[];outputs={}
def run(name,args,opt=False):
    cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*map(str,args)]
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=2400)
    for s in ('stdout','stderr'):(dest/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
    n=re.search(rb'Ran (\d+) tests',p.stderr)
    rows.append({'name':name,'command':cmd,'cwd':str(ROOT),'exit':p.returncode,'tests':int(n[1]) if n else None,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
    (dest/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n');outputs[name]=p.stdout
    print(name,p.returncode,flush=True)
    if p.returncode:raise RuntimeError(name)
run('inventory-before',['tools/verify_artifacts.py'])
suite='v4_1' if number=='5' else 'erc8404'
for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
    run('tests-'+mode,['-m','unittest','discover','-s','tests/'+suite,'-v'],opt)
    run('comparison-'+mode,['tools/'+suite+'/run.py'],opt)
    if number=='6':run('mutations-'+mode,['tools/erc8404/mutations.py','--out','build/review/mutations-'+mode],opt)
if number=='5':run('mutations-normal',['tools/v4_1/mutations.py','--out','build/review/mutations-normal'])
if number=='6':run('core-integrity',['tools/erc8404/integrity.py'])
run('inventory-after',['tools/verify_artifacts.py'])
report={'python':sys.version,'platform':platform.platform(),'comparison_deterministic':len({outputs['comparison-'+m] for m in ('normal','repeat','optimized')})==1,'commands':rows}
(dest/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(report))
