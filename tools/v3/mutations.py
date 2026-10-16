"""Physical one-site source mutations, fresh processes, negative/positive/restoration.
Never run concurrently with another mutation task in the same checkout.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v3.scenarios import cases
SOURCE=ROOT/'src/v3/model.py'
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/v3/mutations');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
 original=SOURCE.read_bytes();text=original.decode();rows=[];executions=[]
 def run(boundary,phase,name):
  cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if sys.flags.optimize else []),'tools/v3/run.py','--case',name]
  try:r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:r=subprocess.CompletedProcess(cmd,124,e.stdout or b'',e.stderr or b'')
  for stream in ('stdout','stderr'):(out/(boundary+'.'+phase+'.'+stream+'.log')).write_bytes(getattr(r,stream))
  executions.append({'boundary':boundary,'phase':phase,'command':cmd,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
  try:result=json.loads(r.stdout)['cases'][0]['result']
  except (ValueError,KeyError,IndexError):result=None
  return r.returncode,result
 try:
  for case in cases():
   boundary=case['boundary']
   if not boundary:continue
   old=f"enforce('{boundary}',raw['{boundary}'])";new=f"enforce('{boundary}',V)";positive='positive_'+case['claim']
   if text.count(old)!=1:rows.append({'boundary':boundary,'classification':'NOT_APPLIED'});continue
   before,b=run(boundary,'before',case['name']);p0,positive_before=run(boundary,'positive-before',positive)
   mutant=text.replace(old,new);SOURCE.write_text(mutant,encoding='utf-8',newline='\n')
   try:after,m=run(boundary,'mutant',case['name'])
   finally:SOURCE.write_bytes(original)
   restored,r=run(boundary,'restored',case['name']);p1,positive_after=run(boundary,'positive-restored',positive)
   # run.py exits 1 when the deliberately mutated result violates the fixed oracle.
   crashed=any(x is None for x in (b,m,r,positive_before,positive_after)) or any(code not in (0,1) for code in (before,after,restored,p0,p1))
   isolated=b is not None and {k:v for k,v in b['obligations'].items() if v!='VERIFIED'}=={boundary:'REFUTED'}
   controls=not crashed and before==restored==p0==p1==0 and positive_before['status']==positive_after['status']=='VERIFIED' and b['status']==r['status']=='REFUTED'
   killed=controls and isolated and after==1 and m['status']=='VERIFIED' and m['authorized']
   verdict='CRASHED' if crashed else 'UNVERIFIABLE' if not controls or not isolated else 'KILLED' if killed else 'SURVIVED'
   rows.append({'boundary':boundary,'witness':case['name'],'classification':verdict,'isolated':isolated,'before':b['status'] if b else None,'after':m['status'] if m else None,'restored':r['status'] if r else None,'positive_restored':positive_after['status'] if positive_after else None,'mutant_source_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'oracle_mismatch_exit_expected':after==1,'replacement':{'from':old,'to':new}})
 finally:
  SOURCE.write_bytes(original)
  (out/'executions.json').write_text(json.dumps(executions,indent=2)+'\n',encoding='utf-8',newline='\n')
 report={'schema':'v3-source-mutations','source_sha256':hashlib.sha256(original).hexdigest(),'source_restored':SOURCE.read_bytes()==original,'mutations':rows,'counts':{k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'unexecuted_integration_boundaries':['wyriwe_provenance','external_model_authority','inference_judgment_binding','external_execution','historical_input_bytes','historical_execution']}
 report['passed']=bool(rows) and all(r['classification']=='KILLED' for r in rows) and report['source_restored'];(out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
