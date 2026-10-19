import argparse,hashlib,json,platform,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/erc8404/validation');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True);rows=[];values={}
 def run(name,args,opt=False):
  cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*args];start=time.perf_counter();r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=1200)
  for s in ('stdout','stderr'):(out/(name+'.'+s+'.log')).write_bytes(getattr(r,s))
  row={'name':name,'command':cmd,'exit':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()};n=re.search(rb'Ran (\d+) tests',r.stderr)
  if n:row['tests']=int(n.group(1))
  rows.append(row);values[name]=r.stdout;(out/'commands.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8',newline='\n');print(name,r.returncode,flush=True)
  if r.returncode:raise RuntimeError(name+'; inspect preserved logs')
 run('integrity-before',['tools/erc8404/integrity.py'])
 run('core-python',['evidence/erc8404/core/conformance/rvr-v0/adapter.py','--check'])
 for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
  run('tests-'+mode,['-m','unittest','discover','-s','tests/erc8404','-v'],opt)
  run('comparison-'+mode,['tools/erc8404/run.py'],opt)
  run('secondary-'+mode,['tools/erc8404/secondary.py'],opt)
  run('mutations-'+mode,['tools/erc8404/mutations.py','--out',str(out/('mutations-'+mode))],opt)
 run('integrity-after',['tools/erc8404/integrity.py'])
 determinism={k:values[k+'-normal']==values[k+'-repeat']==values[k+'-optimized'] for k in ('comparison','secondary','mutations')}
 comparison=json.loads(values['comparison-normal']);mut=json.loads(values['mutations-normal'])
 report={'environment':{'python':sys.version,'platform':platform.platform(),'node':subprocess.check_output(['node','--version'],text=True).strip()},'commands':rows,'scenarios':comparison['scenarios'],'comparison':comparison['summary'],'mutations':mut['counts'],'determinism':determinism,'passed':all(determinism.values())}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
