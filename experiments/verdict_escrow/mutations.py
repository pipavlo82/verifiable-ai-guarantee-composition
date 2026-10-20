"""Exact source-copy controls. A crash or missing edit is never a kill."""
import copy,hashlib,json,sys,types
from pathlib import Path
import adapter as original
from vectors import make
HERE=Path(__file__).resolve().parent
PAIRS={'authorization':'B_missing_obligation','record':'Q_record_tamper','scope':'A_wrong_scope','scenario':'changed_scenario_digest','evidence':'K_evidence_digest','profile':'R_other_profile','chain':'D_other_chain','escrow':'C_other_escrow','recipient':'E_other_recipient','amount':'F_other_amount','payment':'G_other_payment','nonce':'nonce_reused_other_job','expiry':'I_expired','revocation':'J_revoked'}
def evaluate(module,v):return module.assess(v['case'],v['record'],bytes.fromhex(v['request_bytes']),v['grant'],v['snapshot'],v['now'],set(v['journal']),bytes.fromhex(v['profile_bytes']) if v['profile_bytes'] else None)['authorized']
def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);source=(HERE/'adapter.py').read_text(encoding='utf8');positive=make('positive');rows=[]
 specs=[]
 for guard,w in PAIRS.items():
  line=next(s for s in source.splitlines() if '# guard '+guard==s[s.find('# guard '):]);name=line.split("check('",1)[1].split("'",1)[0];specs.append((guard,w,line,"  check('"+name+"',True) # mutation "+guard))
 specs += [('trusted_signer','J_unauthorized'," if verdict['signer']!=grant['signer']:return R # guard trusted_signer"," if False:return R # mutant trusted signer"),('consumption','nonce_reused_other_job',' journal.add(nonce) # guard consumption',' pass # mutant nonce consumption'),('verdict_preimage','valid-unrelated-signature'," return V if verdict['digest']==d.hex() else R # guard verdict_preimage"," return V # mutant digest preimage")]
 for guard,w,old,new in specs:
  row={'id':guard,'witness':w,'old':old,'new':new}
  try:
   if source.count(old)!=1:row['classification']='NOT_APPLIED';rows.append(row);continue
   modified=source.replace(old,new);(out/(guard+'.py')).write_text(modified,encoding='utf8',newline='\n');m=types.ModuleType('mutant_'+guard);m.__file__=str(HERE/'adapter.py');exec(compile(modified,m.__file__,'exec'),m.__dict__)
   negative=make(w) if w!='valid-unrelated-signature' else positive
   def trial(mod,neg):
    if guard=='trusted_signer':return mod.verify_bound_verdict(neg['verdict'],bytes.fromhex(neg['request_bytes']),neg['grant'],neg['record'])==original.V
    if guard=='verdict_preimage':return mod.verify_bound_verdict(original.laboratory_sign(bytes(32)) if neg is negative else neg['verdict'],bytes.fromhex(neg['request_bytes']),neg['grant'],neg['record'])==original.V
    if guard=='consumption':
     j=set();first=mod.reserve(positive['adapter'],'7',j);second=mod.reserve(positive['adapter'],'7',j);return second if neg is negative else first
    return evaluate(mod,neg)
   # Separate object identity for positive versus negative even for custom controls.
   pos=copy.deepcopy(positive)
   b=trial(original,negative);p=trial(original,pos);v=trial(m,negative);pv=trial(m,pos);r=trial(original,negative);pr=trial(original,pos)
   row.update({'baseline':b,'positive':p,'mutant':v,'positive_mutant':pv,'restored':r,'positive_restored':pr,'mutant_sha256':hashlib.sha256(modified.encode()).hexdigest(),'classification':'KILLED' if b is False and v is True and r is False and p and pv and pr else 'SURVIVED'})
  except Exception as ex:row.update({'classification':'CRASHED','error':type(ex).__name__+': '+str(ex)})
  rows.append(row)
 report={'mutations':rows,'counts':{k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'source_unchanged':source==(HERE/'adapter.py').read_text(encoding='utf8')}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps(report['counts']));return 0 if all(r['classification']=='KILLED' for r in rows) else 1
if __name__=='__main__':raise SystemExit(main())
