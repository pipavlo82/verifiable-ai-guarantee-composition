"""Fresh-process source-mutation audit; do not run concurrently with another mutation job.

Uses new genuine signatures, not mocked verification flags. Original corpus is retained.
The decisive oracle requires exactly one non-VERIFIED obligation before mutation.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
SOURCE=ROOT/'src/v2/composition.py'
PIN='ba889271bef7cb3d2eed00067a12064689bfb627'
WITNESSES=ROOT/'evidence/v2/survivor-audit/witnesses'
PLANS=[
 {'name':'native_enforcement','target':'inference','old_case':'native_proof_wrong_input','new_case':'native_isolated','old':"Obligation('inference',native_status,",'new':"Obligation('inference',Status.VERIFIED,"},
 {'name':'artifact_types','target':'artifact_types','old_case':'valid_receipt_used_as_judgment','new_case':'type_isolated','old':"add('artifact_types',profile_ok,",'new':"add('artifact_types',True,"},
]
def load_case(name):
    if name.startswith('legacy:'):
        from src.v2.scenarios import scenarios
        from src.v2.composition import CAP
        return next(r['case'] for r in scenarios() if r['name']==name[7:]),CAP/'policy.json'
    data=json.loads((WITNESSES/(name+'.json')).read_text(encoding='utf-8'))
    case={k:data[k] for k in ('documents','claim','consumed_nonces')}
    case['files']={k:str(ROOT/v) for k,v in data['files'].items()}
    return case,ROOT/data['policy']
def evaluate(name):
    from src.v2.composition import verify
    case,policy=load_case(name)
    return verify(case,policy)
def compact(result):
    return {'status':result.get('status'),'authorized':result.get('authorized'),
      'non_verified':{o['name']:o['status'] for o in result.get('obligations',[]) if o['status']!='VERIFIED'},
      'components':result.get('components',{}),'native_exit':result.get('native',{}).get('exit')}
def audit(out):
    out.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_bytes();original_hash=hashlib.sha256(original).hexdigest()
    pinned=subprocess.check_output(['git','show',PIN+':src/v2/composition.py'],cwd=ROOT)
    if original!=pinned:raise RuntimeError('This audit is for the unchanged published verifier only')
    published=json.loads((ROOT/'evidence/v2/validation/mutations-normal.stdout.log').read_bytes())
    old_mutants={r['boundary']:r for r in published['mutations']}
    results=[]
    def run(plan,phase,name):
        command=[sys.executable,'-B','-X','utf8',*(['-O'] if sys.flags.optimize else []),'tools/v2/audit_survivors.py','--case',name]
        r=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=90)
        label=plan+'.'+phase
        (out/(label+'.stdout.json')).write_bytes(r.stdout);(out/(label+'.stderr.log')).write_bytes(r.stderr)
        try:obj=json.loads(r.stdout)
        except ValueError:obj={}
        return {'exit':r.returncode,'result':obj,'command':['python','-B',*(['-O'] if sys.flags.optimize else []),'tools/v2/audit_survivors.py','--case',name]}
    def stable(run):return compact(run['result'])
    try:
        for plan in PLANS:
            text=original.decode('utf-8')
            if text.count(plan['old'])!=1:
                results.append({'boundary':plan['name'],'mutation':'NOT_APPLIED','passed':False});continue
            before={label:run(plan['name'],'before-'+label,name) for label,name in [('legacy','legacy:'+plan['old_case']),('isolated',plan['new_case']),('positive','positive')]}
            mutant=text.replace(plan['old'],plan['new'])
            mutant_hash=hashlib.sha256(mutant.encode()).hexdigest()
            if mutant_hash!=old_mutants[plan['name']]['mutant_source_sha256']:raise RuntimeError('Mutation differs from published survivor')
            (out/(plan['name']+'.mutant.py')).write_text(mutant,encoding='utf-8',newline='\n')
            SOURCE.write_text(mutant,encoding='utf-8',newline='\n')
            try:
                after={label:run(plan['name'],'mutant-'+label,name) for label,name in [('legacy','legacy:'+plan['old_case']),('isolated',plan['new_case']),('positive','positive')]}
            finally:SOURCE.write_bytes(original)
            restored={label:run(plan['name'],'restored-'+label,name) for label,name in [('isolated',plan['new_case']),('positive','positive')]}
            all_runs=[*before.values(),*after.values(),*restored.values()]
            no_crash=all(r['exit']==0 and 'status' in r['result'] for r in all_runs)
            isolated=stable(before['isolated'])['non_verified']=={plan['target']:'REFUTED'}
            crypto_live=all(before['isolated']['result'].get('components',{}).get(role)=='VERIFIED' for role in ('provenance','judgment','receipt'))
            positives=all(stable(r)['status']=='VERIFIED' for r in [before['positive'],after['positive'],restored['positive']])
            reset=SOURCE.read_bytes()==original and stable(before['isolated'])==stable(restored['isolated'])
            legacy_survives=stable(before['legacy'])['status']=='REFUTED' and stable(after['legacy'])['status']=='REFUTED'
            changed=stable(after['isolated'])['status']=='VERIFIED' and stable(after['isolated'])['authorized'] is True
            passed=no_crash and isolated and crypto_live and positives and reset and legacy_survives and changed
            verdict='CRASHED' if not no_crash else 'KILLED' if passed else 'SURVIVED' if isolated and not changed else 'UNVERIFIABLE'
            results.append({'boundary':plan['name'],'target_obligation':plan['target'],'mutation':verdict,'equivalent':False if passed else None,
              'diagnosis':'TEST_GAP_MASKED_WITNESS' if passed else 'UNRESOLVED','isolated':isolated,'actual_signatures_verified':crypto_live,'legacy_witness_survives':legacy_survives,
              'before':{k:stable(v) for k,v in before.items()},'after':{k:stable(v) for k,v in after.items()},'restored':{k:stable(v) for k,v in restored.items()},
              'replacement':{'from':plan['old'],'to':plan['new']},'mutant_source_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'source_restored':reset,'passed':passed})
    finally:SOURCE.write_bytes(original)
    report={'schema':'surviving-mutant-audit-v1','audited_commit':PIN,'source_sha256':original_hash,'source_unchanged':SOURCE.read_bytes()==original,
      'same_mutant_source_hashes_as_published':True,
      'scope':'same-assistant fresh-process experiment, not independent human review; no upstream or verifier logic fix',
      'mutation_counts':{k:sum(r['mutation']==k for r in results) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'boundaries':results,
      'passed':len(results)==2 and all(r['passed'] for r in results) and SOURCE.read_bytes()==original}
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument('--case');p.add_argument('--out',default='build/v2/survivor-audit');a=p.parse_args()
    if a.case:print(json.dumps(evaluate(a.case),sort_keys=True));return 0
    report=audit(ROOT/a.out);print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
