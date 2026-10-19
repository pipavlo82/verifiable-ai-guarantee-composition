"""Physical mutations of the v4.1 sites only (v4's 44 are unchanged in tools/v4/mutations.py).

Same procedure as v4: witness and positive control run before, under the mutant, and after
exact-byte restoration. KILLED requires the witness to be refused before and restored, the
mutant to admit it, and the positive control to stay authorized throughout.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/v4_1/model.py';CATALOG=ROOT/'fixtures/v4_1/catalog.json'
MUTATIONS=[
 # (id, kind, old, new, witness, positive control)
 ('O14-catalog','catalog',None,None,'negative_O14_self_judged','positive_output'),
 ('O14-coverage','source',"    presence('O14')","    pass # omitted presence enforcement",'omitted_O14','positive_output'),
 ('O14-verification','source',"    verify('O14')","    force('O14')",'negative_O14_self_judged','positive_output'),
 ('claim-fields','source',"claim_fields=check(not unconsumed) if determinate else U","claim_fields=V",'unconsumed_output_under_replay','positive_replay'),
 ('admit-recompute-authorized','source',"    if c!=recomputed:return False","    pass # presented result trusted",'reused_tampered_authorized','control_output_same_contract'),
 ('admit-recompute-scenario','source',"    if c!=recomputed:return False","    pass # presented result trusted",'reused_tampered_scenario','control_output_same_contract'),
 ('admit-recompute-binding','source',"    if c!=recomputed:return False","    pass # presented result trusted",'reused_forged_binding','control_output_same_contract'),
 ('admit-digest','source',"same_contract=b.get('contract_sha256')==contract_digest(contract)","same_contract=True",'reused_under_other_contract','control_output_same_contract'),
 ('admit-claim-type','source',"same_claim=b.get('claim_type')==claim_type==contract.get('claim_type')","same_claim=True",'reused_under_other_claim_type','control_replay_same_contract'),
]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/v4_1/mutations');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
 original=SOURCE.read_bytes();catalog=CATALOG.read_bytes();text=original.decode();rows=[];executions=[]
 def run(mid,phase,name):
  cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if sys.flags.optimize else []),'tools/v4_1/run.py','--case',name]
  try:r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=120)
  except subprocess.TimeoutExpired as e:r=subprocess.CompletedProcess(cmd,124,e.stdout or b'',e.stderr or b'')
  for stream in ('stdout','stderr'):(out/f'{mid}.{phase}.{stream}.log').write_bytes(getattr(r,stream))
  executions.append({'mutation':mid,'phase':phase,'command':cmd,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
  try:
   d=json.loads(r.stdout)
   hit=[x for x in d['cases'] if x['name']==name] or [x for x in d['reuse'] if x['name']==name]
   x=hit[0];ok=x['admitted'] if 'admitted' in x else x['result']['C']['authorized']
  except (ValueError,KeyError,IndexError):ok=None
  return r.returncode,ok
 try:
  for mid,kind,old,new,witness,positive in MUTATIONS:
   if kind=='source' and text.count(old)!=1:rows.append({'id':mid,'classification':'NOT_APPLIED'});continue
   _,b=run(mid,'before',witness);_,pb=run(mid,'positive-before',positive)
   if kind=='catalog':
    cat=json.loads(catalog);del cat['O14'];mutant=(json.dumps(cat,indent=2,sort_keys=True)+'\n').encode();CATALOG.write_bytes(mutant)
   else:mutant=text.replace(old,new).encode();SOURCE.write_bytes(mutant)
   try:_,m=run(mid,'mutant',witness);_,pm=run(mid,'positive-mutant',positive)
   finally:SOURCE.write_bytes(original);CATALOG.write_bytes(catalog)
   _,r=run(mid,'restored',witness);_,pr=run(mid,'positive-restored',positive)
   crashed=any(v is None for v in (b,pb,m,pm,r,pr))
   controls=not crashed and b is False and r is False and pb is True and pr is True
   if kind=='catalog':killed=controls and m is False and pm is False;effect='CATALOG_DELETION_DETECTED'
   else:killed=controls and m is True and pm is True;effect='UNSUPPORTED_AUTHORIZATION'
   status='CRASHED' if crashed else 'UNVERIFIABLE' if not controls else 'KILLED' if killed else 'SURVIVED'
   rows.append({'id':mid,'kind':kind,'witness':witness,'positive':positive,'classification':status,'effect':effect,'before':b,'mutant':m,'restored':r,'positive_before':pb,'positive_mutant':pm,'positive_restored':pr,'mutant_sha256':hashlib.sha256(mutant).hexdigest(),'replacement':None if kind=='catalog' else {'from':old,'to':new}})
 finally:
  SOURCE.write_bytes(original);CATALOG.write_bytes(catalog)
  (out/'executions.json').write_text(json.dumps(executions,indent=2)+'\n',encoding='utf-8',newline='\n')
 counts={k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')}
 report={'schema':'v4.1-physical-mutations','mutations':rows,'counts':counts,'source_restored':SOURCE.read_bytes()==original,'catalog_restored':CATALOG.read_bytes()==catalog,'source_sha256':hashlib.sha256(original).hexdigest(),'catalog_sha256':hashlib.sha256(catalog).hexdigest(),'passed':len(rows)==len(MUTATIONS) and counts['KILLED']==len(MUTATIONS)}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
