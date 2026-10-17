"""Actual one-check source replacements executed in fresh subprocesses; restore in finally.

Source mutations are NOT environment flags. A kill requires targeted classification change
to VERIFIED, valid unmutated witness, zero process exit, and restored positive control.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from src.v2.scenarios import scenarios
SOURCE=ROOT/'src/v2/composition.py'
def child(name):
    cmd=[sys.executable,'-B',*(['-O'] if sys.flags.optimize else []),'-c',"import json;from src.v2.scenarios import scenarios;from src.v2.composition import verify;r=next(r for r in scenarios() if r['name']=="+repr(name)+");print(json.dumps(verify(r['case']),sort_keys=True))"]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=60)
    try:obj=json.loads(r.stdout)
    except ValueError:obj={}
    return r,obj
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/v2/mutations');args=p.parse_args()
    out=ROOT/args.out;out.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_bytes();text=original.decode();rows=[]
    mapping={'provenance_preimage':'raw_ok','input_binding':'input_ok','model_binding':'model_ok','subject_binding':'subject_ok','proof_binding':'proof_ok','action_binding':'action_ok','authority':'authority_ok','execution_binding':'execution_ok','output_binding':'output_ok','receipt_evidence':'result_ok','domain':'domain_ok','scope':'scope_ok','policy_binding':'policy_ok','replay':'replay_ok','claim_strength':'historical_ok','artifact_types':'profile_ok'}
    plans=[]
    for boundary,var in mapping.items():
        row=next(r for r in scenarios() if r['boundary']==boundary)
        old=f"add('{boundary}',{var},";new=f"add('{boundary}',True,"
        plans.append((boundary,row['name'],row['expected'],old,new))
    for role,witness in [('judgment','invalid_signature'),('provenance','invalid_provenance_signature'),('receipt','invalid_receipt_signature')]:
        plans.append((role+'_signature',witness,'REFUTED',"Status(components[role]),'ECDSA",f"(Status.VERIFIED if role=='{role}' else Status(components[role])),'ECDSA"))
    plans += [('native_enforcement','native_proof_wrong_input','REFUTED',"Obligation('inference',native_status,", "Obligation('inference',Status.VERIFIED,")]
    try:
        for boundary,witness,expected,old,new in plans:
            before,before_obj=child(witness)
            if text.count(old)!=1:
                rows.append({'boundary':boundary,'status':'NOT_APPLIED','reason':'unique mutation site missing'});continue
            mutated=text.replace(old,new)
            SOURCE.write_text(mutated,encoding='utf-8',newline='\n')
            try:result,obj=child(witness)
            finally:SOURCE.write_bytes(original)
            restored,restored_obj=child(witness);positive,pos_obj=child('valid_recomputation')
            for label,r in [('original',before),('mutant',result),('restored',restored),('positive',positive)]:
                (out/f'{boundary}.{label}.stdout.json').write_bytes(r.stdout);(out/f'{boundary}.{label}.stderr.log').write_bytes(r.stderr)
            valid=before.returncode==0 and before_obj.get('status')==expected and restored.returncode==0 and restored_obj.get('status')==expected and positive.returncode==0 and pos_obj.get('status')=='VERIFIED'
            status='CRASHED' if result.returncode!=0 else 'UNVERIFIABLE' if not valid or 'status' not in obj else 'KILLED' if obj['status']=='VERIFIED' else 'SURVIVED'
            rows.append({'boundary':boundary,'witness':witness,'status':status,'before':before_obj.get('status'),'after':obj.get('status'),'restored':restored_obj.get('status'),'positive_restored':pos_obj.get('status'),'mutant_source_sha256':hashlib.sha256(mutated.encode()).hexdigest(),'replacement':{'from':old,'to':new}})
    finally:SOURCE.write_bytes(original)
    rows += [{'boundary':'historical_execution_verifier','status':'UNVERIFIABLE','executed':False,'reason':'no external execution artifact/verifier available; not implemented, not counted as an executed mutation'}]
    report={'source_restored':SOURCE.read_bytes()==original,'source_sha256':hashlib.sha256(original).hexdigest(),'counts':{k:sum(r['status']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'mutations':rows}
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['source_restored'] and report['counts']['CRASHED']==0 else 1
if __name__=='__main__':raise SystemExit(main())
