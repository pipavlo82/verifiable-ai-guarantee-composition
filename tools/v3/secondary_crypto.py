"""Different implementations: pinned recompute-kit BIP340 and eth-account EIP712."""
import hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'build/v3/python-deps'))
from src.v3.evidence import base_case,canonical,sha
from eth_account import Account
from eth_account.messages import encode_typed_data
from eth_hash.auto import keccak
from eth_keys.exceptions import BadSignature
source=ROOT/'evidence/v3/upstream/recompute-kit/bin/bip340.py'
spec=importlib.util.spec_from_file_location('pinned_bip340',source);bip=importlib.util.module_from_spec(spec);spec.loader.exec_module(bip)
def nostr(e):
    raw=json.dumps([0,e['pubkey'],e['created_at'],e['kind'],e['tags'],e['content']],separators=(',',':'),ensure_ascii=False).encode();identifier=sha(raw)
    return identifier==e['id'] and bip.verify_hex(identifier,e['pubkey'],e['sig'])
def eip(doc):
    p=doc['proof_payload'];s=doc['signature'];h='0x'+keccak(canonical(p['evidence'])).hex();message={k:p[k] for k in ('schema','claim_id','result','verifier','boundary','as_of','recomputed_at')};message['evidence_hash']=h
    recovered=Account.recover_message(encode_typed_data(s['domain'],s['types'],message),signature=s['signature']).lower()
    return h==s['evidence_hash'] and recovered==s['signer'].lower()==p['verifier'].lower()
def main():
    import copy
    c=base_case();bad=copy.deepcopy(c);bad['ledger']['proof_event']['sig']='00'*64;bad['cell2']['signature']['signature']='0x'+'00'*65
    out={'ledger_bip340':nostr(c['ledger']['proof_event']),'cell1_bip340':nostr(c['cell1']['event']),'cell2_eip712':eip(c['cell2']),'negative_bip340_rejected':not nostr(bad['ledger']['proof_event'])}
    try:out['negative_eip712_rejected']=not eip(bad['cell2'])
    except (ValueError,BadSignature):out['negative_eip712_rejected']=True
    # Missing input is deliberately not passed to a crypto primitive and never certified.
    out['missing']='UNVERIFIABLE';out['passed']=all(v for v in out.values() if isinstance(v,bool));print(json.dumps(out,sort_keys=True));return 0 if out['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
