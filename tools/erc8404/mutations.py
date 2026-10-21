"""Source mutations in isolated copies; no production or frozen Core edits."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
SOURCE=ROOT/'src/erc8404/engine.py'

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='build/erc8404/mutations');p.add_argument('--worker');p.add_argument('--witness');a=p.parse_args()
 if a.worker:
  import types
  name='src.erc8404.engine';m=types.ModuleType(name);m.__file__=str(SOURCE);sys.modules[name]=m
  exec(compile(Path(a.worker).read_bytes(),str(SOURCE),'exec'),m.__dict__)
  from src.erc8404.cases import cases,base
  if a.witness=='reuse':
   c=base();record=m.decide(c)['authorization_scope'];record['contract_sha256']='ff'*32
   print(json.dumps({'status':m.consume_authorization(record,c),'authorized':m.consume_authorization(record,c)==m.V}));return 0
  c=base() if a.witness=='positive' else next(w['case'] for w in cases() if w['name']==a.witness)
  print(json.dumps(m.decide(c),sort_keys=True));return 0
 out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True);original=SOURCE.read_bytes();text=original.decode();mutations=[];rows=[];commands=[]
 witnesses={'coverage':'self_missing_O14','definitions':'self_counterfeit_O14','contract_commitment':'wrong_contract_context','scenario':'wrong_scenario','claim_type':'wrong_claim_type','scope':'wrong_scope','signed_contract':'wrong_contract','field_policy':'false_output_replay_only','supported_contract':'unsupported_contract_claim'}
 for key,witness in witnesses.items():
  old=next(line for line in text.splitlines() if '# MUTATE: '+key in line)
  mutations.append((key,old,"    statuses['"+key+"'] = V",witness))
 for key,witness in [('O14','self_judgment'),('S02','wrong_artifact'),('S03','wrong_subject'),('S04','unauthorized_without_separation'),('S06','wrong_action')]:
  old='    statuses.update(verification)';new=old+"\n    statuses['"+key+"'] = V"
  mutations.append((key,old,new,witness))
 mutations.append(('contract_preimage','    if raw is None: return None  # MUTATE: contract_preimage',"    if raw is None: return case['contract']",'missing_contract_preimage'))
 mutations.append(('receipt',"    statuses = {'receipt': core['consumer_status']}","    statuses = {'receipt': V}",'contradictory_receipt_projection'))
 mutations.append(('reuse','    return check(record == fresh[\'authorization_scope\'])  # MUTATE: reuse','    return V','reuse'))
 def run(mid,phase,path,witness):
  cmd=[sys.executable,'-B','-X','utf8',*(['-O'] if sys.flags.optimize else []),'tools/erc8404/mutations.py','--worker',str(path),'--witness',witness]
  try:r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:r=subprocess.CompletedProcess(cmd,124,e.stdout or b'',e.stderr or b'')
  for s in ('stdout','stderr'):(out/f'{mid}.{phase}.{s}.log').write_bytes(getattr(r,s))
  commands.append({'mutation':mid,'phase':phase,'command':cmd,'exit':r.returncode})
  try:return r.returncode,json.loads(r.stdout)
  except ValueError:return r.returncode,None
 baseline=out/'baseline.py';baseline.write_bytes(original)
 for mid,old,new,w in mutations:
  if text.count(old)!=1:rows.append({'id':mid,'classification':'NOT_APPLIED'});continue
  mutant=out/(mid+'.py');mutant.write_text(text.replace(old,new),encoding='utf-8',newline='\n')
  outputs=[run(mid,phase,path,wit) for phase,path,wit in [('before',baseline,w),('mutant',mutant,w),('restored',baseline,w),('positive',baseline,'positive')]]
  crashed=any(code!=0 or value is None for code,value in outputs)
  b,m,r,pv=[v for _,v in outputs]
  controls=not crashed and b==r and not b['authorized'] and pv['authorized']
  isolated=controls and (w=='reuse' or [k for k,v in b['checks'].items() if v!='VERIFIED']==[mid] or mid=='contract_preimage')
  status='CRASHED' if crashed else 'UNVERIFIABLE' if not controls or not isolated else 'KILLED' if m['authorized'] else 'SURVIVED'
  rows.append({'id':mid,'witness':w,'classification':status,'isolated':isolated,'before':b.get('status') if b else None,'mutant':m.get('status') if m else None,'restored':r.get('status') if r else None,'incorrect_authorization':m.get('authorized') if m else None,'source_sha256':hashlib.sha256(mutant.read_bytes()).hexdigest(),'replacement':{'from':old,'to':new}})
 counts={k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')}
 expected={r['id']:('SURVIVED' if r['id']=='contract_preimage' else 'KILLED') for r in rows}
 report={'mutations':rows,'counts':counts,'source_unchanged':SOURCE.read_bytes()==original,
         'uncovered':['contract-preimage absence enforcement is not isolated by the single fallback mutation; refusal remains, no global equivalence claim'],
         'passed':len(rows)==17 and all(r['classification']==expected[r['id']] for r in rows)}
 for path,data in [('report.json',report),('commands.json',commands)]: (out/path).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(report,sort_keys=True,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
