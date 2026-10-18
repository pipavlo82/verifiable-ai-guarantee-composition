"""Physical catalog/source mutations. Separate alarm detection from unsafe admission."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/v4/model.py';CATALOG=ROOT/'fixtures/v4/catalog.json'
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/v4/mutations');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
 original=SOURCE.read_bytes();catalog=CATALOG.read_bytes();text=original.decode();rows=[];executions=[]
 def run(mid,phase,name):
  cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if sys.flags.optimize else []),'tools/v4/run.py','--case',name]
  try:r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:r=subprocess.CompletedProcess(cmd,124,e.stdout or b'',e.stderr or b'')
  for stream in ('stdout','stderr'):(out/f'{mid}.{phase}.{stream}.log').write_bytes(getattr(r,stream))
  executions.append({'mutation':mid,'phase':phase,'command':cmd,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
  try:d=json.loads(r.stdout)['cases'][0]['result']
  except (ValueError,KeyError,IndexError):d=None
  return r.returncode,d
 mutations=[]
 for i in range(1,14):
  oid=f'O{i:02}'
  mutations.extend([(oid+'-catalog','catalog',oid,None,None,'negative_'+oid),(oid+'-coverage','coverage',oid,f"    presence('{oid}')",'    pass # omitted presence enforcement','omitted_'+oid),(oid+'-verification','verification',oid,f"    verify('{oid}')",f"    force('{oid}')",'negative_'+oid)])
 mutations.extend([
 ('context','guard','context',"coverage['context']=check(case['scenario']==contract['scenario'])","coverage['context']=V",'stale_scenario'),
 ('definitions','guard','definitions',"coverage['definitions']=combine(definitions)","coverage['definitions']=V",'counterfeit_definition'),
 ('composition','guard','composition',"composition=check(case['requested_claim']==contract['claim_type'])","composition=V",'scope_overclaim'),
 ('closure','guard','dependency_closure',"coverage['dependency_closure']=check(all(dep in requirements for req in requirements.values() for dep in req['dependencies']))","coverage['dependency_closure']=V",'unclosed_dependencies'),
 ('future','guard','unknown_requirement',"coverage[oid]=U","coverage[oid]=V",'unknown_required_obligation')])
 try:
  for mid,kind,oid,old,new,witness in mutations:
   if kind!='catalog' and text.count(old)!=1:rows.append({'id':mid,'classification':'NOT_APPLIED'});continue
   before,b=run(mid,'before',witness);p0,pb=run(mid,'positive-before','positive_output')
   if kind=='catalog':
    cat=json.loads(catalog);del cat[oid];mutant=(json.dumps(cat,indent=2,sort_keys=True)+'\n').encode();CATALOG.write_bytes(mutant)
   else:mutant=text.replace(old,new).encode();SOURCE.write_bytes(mutant)
   try:after,m=run(mid,'mutant',witness);mp,pm=run(mid,'positive-mutant','positive_output')
   finally:SOURCE.write_bytes(original);CATALOG.write_bytes(catalog)
   restored,r=run(mid,'restored',witness);p1,pr=run(mid,'positive-restored','positive_output')
   crashed=any(v is None for v in (b,pb,m,pm,r,pr)) or any(x not in (0,1) for x in (before,p0,after,mp,restored,p1))
   controls=not crashed and before==p0==restored==p1==0 and b==r and pb['C']['authorized'] and pr['C']['authorized']
   isolated=controls and (kind not in ('verification','coverage') or (len([v for v in (b['verification'] if kind=='verification' else b['coverage']).values() if v!='VERIFIED'])==1))
   if kind=='catalog':killed=controls and m['C']['status']=='REFUTED' and m['all_declared_pass'] and m['missing_obligations']==[oid] and pm['C']['status']=='REFUTED' and pm['missing_obligations']==[oid];effect='CATALOG_DELETION_DETECTED'
   else:killed=controls and isolated and m['C']['authorized'] and not b['C']['authorized'] and pm['C']['authorized'];effect='UNSUPPORTED_AUTHORIZATION'
   status='CRASHED' if crashed else 'UNVERIFIABLE' if not controls or not isolated else 'KILLED' if killed else 'SURVIVED'
   rows.append({'id':mid,'kind':kind,'boundary':oid,'witness':witness,'classification':status,'effect':effect,'isolated':isolated,'before':b['C']['status'] if b else None,'after':m['C']['status'] if m else None,'restored':r['C']['status'] if r else None,'unsupported_authorized':m['C']['authorized'] if m else None,'positive_mutant':pm['C']['status'] if pm else None,'mutant_sha256':hashlib.sha256(mutant).hexdigest(),'replacement':None if kind=='catalog' else {'from':old,'to':new}})
 finally:
  SOURCE.write_bytes(original);CATALOG.write_bytes(catalog)
  (out/'executions.json').write_text(json.dumps(executions,indent=2)+'\n',encoding='utf-8',newline='\n')
 counts={k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')}
 report={'schema':'v4-physical-mutations','mutations':rows,'counts':counts,'source_restored':SOURCE.read_bytes()==original,'catalog_restored':CATALOG.read_bytes()==catalog,'source_sha256':hashlib.sha256(original).hexdigest(),'catalog_sha256':hashlib.sha256(catalog).hexdigest(),'uncovered':['universal contract adequacy','external artifact acquisition','missing contract double fail-closed branch'],'passed':len(rows)==44 and counts['KILLED']==44}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
