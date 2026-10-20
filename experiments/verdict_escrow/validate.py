import argparse,hashlib,json,os,platform,re,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/escrow/validation');p.add_argument('--skip-onchain-mutations',action='store_true');a=p.parse_args();out=(ROOT/a.out).resolve();out.mkdir(parents=True,exist_ok=True);rows=[]
 forge=os.environ.get('FORGE','C:/Users/msi/.foundry/bin/forge.exe' if os.name=='nt' else 'forge')
 def inv():return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.rglob('*') if p.is_file() and not any(q in p.parts for q in ('__pycache__','out','cache'))}
 before=inv()
 def run(name,args,env=None):
  start=time.perf_counter();r=subprocess.run(list(map(str,args)),cwd=ROOT,env=env,capture_output=True,timeout=1800)
  for stream in ('stdout','stderr'):(out/(name+'.'+stream+'.log')).write_bytes(getattr(r,stream))
  rows.append({'name':name,'command':list(map(str,args)),'cwd':str(ROOT),'exit':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()});(out/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n');print(name,r.returncode,flush=True)
  if r.returncode:raise RuntimeError(name+' failed; inspect logs. Not a mutation kill.')
  return r.stdout
 py=[sys.executable,'-B','-X','utf8'];prefix='experiments/verdict_escrow/'
 run('baseline-integrity',[*py,prefix+'integrity.py']);run('forge-version',[forge,'--version']);run('core-integrity',[*py,'tools/integration/integrity.py'])
 baseenv=dict(os.environ,LAB_PYTHON=sys.executable)
 stock=ROOT/'build/escrow/stock/integrations/verdict-escrow';lib=ROOT/'build/escrow/lib/forge-std/src'
 run('stock-clean-build',[forge,'build','--force','--root',stock,'--remappings','forge-std/='+lib.as_posix()+'/','--lib-paths',lib.parent],baseenv)
 run('stock-seven-tests',[forge,'test','--root',stock,'--remappings','forge-std/='+lib.as_posix()+'/','--lib-paths',lib.parent,'--json'],baseenv)
 run('joint-clean-build',[forge,'build','--force','--root',HERE],baseenv)
 for mode in ('normal','repeat','optimized'):
  folder=out/mode;env=dict(baseenv,LAB_EVIDENCE_DIR=str(folder),LAB_VECTOR_DIR=str(folder),PYTHONOPTIMIZE='1' if mode=='optimized' else '0')
  run('evm-'+mode,[forge,'test','--root',HERE,'--threads','1','--json'],env)
  run('unit-'+mode,[*py,*(['-O'] if mode=='optimized' else []),'-m','unittest','discover','-s',HERE,'-p','test_adapter.py','-v'],env)
  run('comparison-'+mode,[*py,prefix+'analyze.py',folder],env)
  run('secondary-'+mode,['node',prefix+'secondary.mjs',folder],env)
  run('mutations-'+mode,[*py,prefix+'mutations.py',out/('mutations-'+mode)],env)
 if not a.skip_onchain_mutations:run('onchain-mutations',[*py,prefix+'onchain_mutations.py',out/'onchain-mutations'],baseenv)
 run('pr7-tests',[*py,'-m','unittest','discover','-s','tests/integration','-v'])
 run('pr7-mutations',[*py,'tools/integration/mutations.py','--out',out/'pr7-mutations'])
 run('baseline-integrity-after',[*py,prefix+'integrity.py'])
 deterministic={}
 for name in ('comparison','secondary'):
  values=[json.loads((out/(name+'-'+m+'.stdout.log')).read_bytes()) for m in ('normal','repeat','optimized')];deterministic[name]=values[0]==values[1]==values[2]
 deterministic['vectors']=all((out/'normal'/f.name).read_bytes()==(out/'repeat'/f.name).read_bytes()==(out/'optimized'/f.name).read_bytes() for f in (out/'normal').glob('*-offchain.json'))
 deterministic['mutations']=len({hashlib.sha256((out/('mutations-'+m)/'report.json').read_bytes()).hexdigest() for m in ('normal','repeat','optimized')})==1
 report={'commands':rows,'python':sys.version,'platform':platform.platform(),'source_inventory':before,'source_unchanged':before==inv(),'determinism':deterministic,'comparison':json.loads((out/'comparison-normal.stdout.log').read_bytes()),'adapter_mutations':json.loads((out/'mutations-normal/report.json').read_bytes())['counts'],'onchain_mutations':json.loads((out/'onchain-mutations/report.json').read_bytes())['counts'] if not a.skip_onchain_mutations else None,'passed':before==inv() and all(deterministic.values())}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps({k:report[k] for k in ('passed','determinism','adapter_mutations','onchain_mutations')}));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
