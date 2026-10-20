"""One textual change per physical module copy; restored controls, no crash-as-kill."""
import argparse,copy,hashlib,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.integration import engine as baseline
from src.integration.cases import cases,base
SOURCE=ROOT/'src/integration/engine.py'
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/integration/mutations');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_bytes();text=original.decode();by={w['name']:w['case'] for w in cases()};rows=[]
    specs=[]
    for oid,w in [('J01','altered_inference_claim'),('J02','wrong_review_artifact'),('J03','valid_components_different_proof'),('J04','altered_profile_contract'),('J05','read_without_validation'),('J06','unknown_claim_field'),('J07','independence_requirement_removed_from_profile'),('J08','same_controller_not_established'),('J09','receipt_valid_external_claim_unsupported')]:
        old="        if mode=='B':return output()";new="        checks['"+oid+"']=V\n"+old;specs.append((oid,old,new,w,'decision'))
    for guard,w in [('coverage','omitted_J01'),('definitions','counterfeit_definition'),('dependencies','missing_dependency'),('scope_floor','weakened_contract_keeps_broad_claim')]:
        old=next(x for x in text.splitlines() if '# GUARD '+guard in x);key=old.split("checks['")[1].split("']")[0];specs.append((guard,old,"        checks['"+key+"']=V",w,'decision'))
    specs.append(('unknown_dispatch','            checks[oid]=fn() if oid in KNOWN and fn else U','            checks[oid]=fn() if fn else U','unknown_id_known_procedure','decision'))
    old=next(x for x in text.splitlines() if '# GUARD key_identity' in x);specs.append(('key_identity',old,'                else:pairs.append(V)','O14_name_with_wrong_semantics','decision'))
    old=next(x for x in text.splitlines() if '# GUARD inference_semantics' in x);specs.append(('inference_semantics',old,'            native_floor=True','inference_name_without_native_obligation','decision'))
    old=next(x for x in text.splitlines() if '# GUARD review_semantics' in x);specs.append(('review_semantics',old,'            review_floor=True','review_name_without_authority_obligation','decision'))
    old=next(x for x in text.splitlines() if '# GUARD policy_binding' in x);specs.append(('policy_binding',old,'            policy_binding=V','authority_policy_substitution','decision'))
    old=next(x for x in text.splitlines() if '# GUARD preimage' in x)
    specs.append(('preimage',old,"    if contract is None:contract=json.loads((ROOT/'fixtures/integration/scenario-contract.json').read_bytes())",'missing_contract_preimage','decision'))
    old=next(x for x in text.splitlines() if '# GUARD admission_status' in x);specs.append(('admission_status',old,'    pass','self_judgment','admission_status'))
    old=next(x for x in text.splitlines() if '# GUARD admission_equality' in x);specs.append(('admission_equality',old,'    status=V','positive','admission_equality'))
    old="    if raw!=canonical(c):raise ValueError('Noncanonical joint contract')";specs.append(('canonical_bytes',old,'    pass','noncanonical_contract','decision'))
    for mid,old,new,w,kind in specs:
        if text.count(old)!=1:rows.append({'id':mid,'classification':'NOT_APPLIED'});continue
        mutant=text.replace(old,new);path=out/(mid+'.py');path.write_text(mutant,encoding='utf8',newline='\n')
        def load(raw,name):
            mod=types.ModuleType(name);mod.__file__=str(SOURCE);exec(compile(raw,str(SOURCE),'exec'),mod.__dict__);return mod
        def execute(mod):
            c=copy.deepcopy(by[w])
            if kind=='decision':return mod.evaluate(c)
            record=baseline.evaluate(c)
            if kind=='admission_equality':record['scenario']='forged-scenario'
            return mod.admit(record,c)
        try:
            b=execute(baseline);m=execute(load(path.read_bytes(),'mutant_'+mid));path.write_bytes(original);r=execute(load(path.read_bytes(),'restored_'+mid));positive=baseline.evaluate(base())
            controls=b==r and not b['authorized'] and positive['authorized']
            verdict='UNVERIFIABLE' if not controls else 'KILLED' if m['authorized'] else 'SURVIVED'
            row={'id':mid,'witness':w,'classification':verdict,'before':b,'mutant':m,'restored':r,'positive':positive,'source_restored':path.read_bytes()==original,'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'replacement':{'from':old,'to':new}}
        except Exception as e:row={'id':mid,'classification':'CRASHED','error':type(e).__name__+': '+str(e)}
        rows.append(row)
    counts={k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')}
    report={'mutations':rows,'counts':counts,'source_unchanged':SOURCE.read_bytes()==original,'survivors':[r['id'] for r in rows if r['classification']=='SURVIVED'],'passed':len(rows)==22 and counts['KILLED']==22,'scope':'22 executed authorization-boundary mutations; not an exhaustive mutation score over every defensive parser branch.'}
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
