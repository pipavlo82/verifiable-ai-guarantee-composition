"""Actual native proof replay and independent eth-account signature implementation."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'build/v3/python-deps')]
from eth_account import Account
from eth_account.messages import encode_typed_data
from src.integration.cases import base
from src.v4.model import facts,V
def main():
    c=base();f=facts(c['inference']);other=json.loads((ROOT/'fixtures/integration/other-proof-review.json').read_bytes())
    schema=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {TYPES} from './src/v2/crypto.mjs'; console.log(JSON.stringify(TYPES));"],cwd=ROOT))
    docs=list(c['inference']['documents'].values())+list(c['review']['documents'].values())+list(other['documents'].values())
    docs+=list(json.loads((ROOT/'fixtures/integration/weak-review.json').read_bytes())['documents'].values())
    def recover(d):return Account.recover_message(encode_typed_data(d['domain'],{d['type']:[{'name':n,'type':t} for n,t in schema[d['type']]]},d['message']),signature=d['signature']).lower()
    rows=[{'signer':d['signer'],'recovered':recover(d),'passed':recover(d)==d['signer'].lower()} for d in docs]
    bad=copy.deepcopy(next(d for d in docs if d['type']=='LabJudgment'));bad['message']['subject']='substitution';negative=recover(bad)!=bad['signer'].lower()
    extra=copy.deepcopy(docs[0]);extra['message']['subject']='not-in-this-typed-preimage';unsigned_extra_ignored=recover(extra)==extra['signer'].lower()
    report={'native':f['native'],'commands':f['commands'],'signatures':rows,'signature_count':len(rows),'tampered_signed_judgment_subject_rejected':negative,'undeclared_subject_on_provenance_not_signed':unsigned_extra_ignored,'classification':'LABORATORY_VERIFIED; same machine, independent signature library','passed':f['native']['status']==V and all(r['passed'] for r in rows) and negative and unsigned_extra_ignored}
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
