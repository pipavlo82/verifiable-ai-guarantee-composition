import argparse,hashlib,json,platform,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/v4/validation');p.add_argument('--skip-benchmark',action='store_true');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True);rows=[];values={}
 def run(name,args,opt=False):
  command=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*args];r=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=1200)
  for stream in ('stdout','stderr'):(out/(name+'.'+stream+'.log')).write_bytes(getattr(r,stream))
  row={'name':name,'command':command,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()};n=re.search(rb'Ran (\d+) tests',r.stderr)
  if n:row['tests']=int(n.group(1))
  rows.append(row);values[name]=r.stdout;print(json.dumps({'step':name,'exit':r.returncode}),flush=True)
  if r.returncode:raise RuntimeError(name+' failed; inspect raw logs')
 run('source-pins',['tools/v4/verify_sources.py'])
 for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
  run('tests-'+mode,['-m','unittest','discover','-s','tests/v4','-v'],opt)
  run('comparison-'+mode,['tools/v4/run.py'],opt)
  run('secondary-'+mode,['tools/v4/secondary.py'],opt)
  run('mutations-'+mode,['tools/v4/mutations.py','--out',str(out/('mutations-'+mode))],opt)
 run('raw-execution',['tools/v4/run.py','--raw'])
 if not a.skip_benchmark:run('benchmark',['tools/v4/benchmark.py'])
 checks={group:values[group+'-normal']==values[group+'-repeat']==values[group+'-optimized'] for group in ('comparison','secondary','mutations')}
 expected=ROOT/'evidence/v4/validation/comparison-normal.stdout.log';snapshot=None if not expected.exists() else json.loads(values['comparison-normal'])==json.loads(expected.read_bytes())
 result={'schema':'v4-validation','environment':{'python':sys.version,'platform':platform.platform(),'node':subprocess.check_output(['node','--version'],text=True).strip(),'rustc':subprocess.check_output(['rustc','--version'],text=True).strip()},'runs':rows,'determinism':checks,'snapshot_match':snapshot,'comparison':json.loads(values['comparison-normal'])['summary'],'scenarios':len(json.loads(values['comparison-normal'])['cases']),'mutations':json.loads(values['mutations-normal'])['counts'],'passed':all(checks.values()) and snapshot is not False}
 (out/'report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,indent=2,sort_keys=True));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
