"""Actual verifier adapters. Caller reports/booleans never stand in for cryptography."""
import copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/'evidence/v3/upstream/recompute-kit/conformance/crc-claim-v0/fixtures'
def strict(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON member')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs)
def read(path):return strict(Path(path).read_bytes())
def canonical(obj):
    def check(x):
        if isinstance(x,float):raise ValueError('non-integer canonical value')
        if isinstance(x,int) and not isinstance(x,bool) and abs(x)>2**53-1:raise ValueError('unsafe integer')
        if isinstance(x,dict):
            if any(not k.isascii() for k in x):raise ValueError('non-ASCII key')
            for v in x.values():check(v)
        elif isinstance(x,list):
            for v in x:check(v)
    check(obj);return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(value):return hashlib.sha256(value).hexdigest()
def base_case():
    return {'ledger':read(ROOT/'evidence/v3/public/ledger-236.json'),'cell1':read(UP/'node1-nostr.cell.json'),'cell2':read(UP/'node2-eip712.cell.json'),'native':'original','receipt':read(ROOT/'evidence/v3/local-replay/receipt.json') if (ROOT/'evidence/v3/local-replay/receipt.json').exists() else None}
def cryptography(case):
    try:
        run=subprocess.run(['node',str(ROOT/'src/v3/public_crypto.mjs')],input=json.dumps({k:case.get(k) for k in ('ledger','cell1','cell2')}).encode(),capture_output=True,timeout=40)
        if run.returncode==0:return strict(run.stdout),{'exit':0,'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr)}
    except (OSError,ValueError,subprocess.TimeoutExpired):pass
    return {k:{'status':'UNVERIFIABLE','reason':'crypto runtime unavailable'} for k in ('ledger','cell1','cell2')},{'exit':None}
def native(case):
    from src.v2.composition import native_path
    if case.get('native') is None:return {'status':'UNVERIFIABLE','reason':'missing native tuple'}
    cap=ROOT/'evidence/v2/capture/a';paths=[cap/n for n in ('input.bin','weights.bin','output.bin','proof.bin')]
    if case['native']=='invalid':paths[-1]=ROOT/'evidence/v2/survivor-audit/witnesses/invalid-claimed-scalar.bin'
    try:
        r=subprocess.run([str(native_path()),'verify',*map(str,paths)],capture_output=True,timeout=60)
        value=strict(r.stdout)
        if r.returncode not in (0,1) or set(value)!={'native_verified','output_recomputed','statement_bound'} or any(type(v)!=bool for v in value.values()):raise ValueError('native contract')
        return {'status':'VERIFIED' if r.returncode==0 and all(value.values()) else 'REFUTED','exit':r.returncode,'result':value,'proof_sha256':sha(paths[-1].read_bytes())}
    except (OSError,ValueError,subprocess.TimeoutExpired):return {'status':'UNVERIFIABLE','reason':'native verifier unavailable'}
def receipt(case):
    value=case.get('receipt')
    if value is None:return {'status':'UNVERIFIABLE','reason':'missing replay receipt'}
    try:
        r=subprocess.run(['node',str(ROOT/'tools/v3/receipt_bridge.mjs')],input=json.dumps(value).encode(),capture_output=True,timeout=30)
        if r.returncode:raise ValueError('receipt runtime failed')
        native=strict(r.stdout);body={k:v for k,v in value.items() if k!='anchor'}
        root=value.get('anchor',{}).get('receipt_root');recomputed='0x'+sha(canonical(body))
        if root is None:return {'status':'UNVERIFIABLE','reason':'missing receipt root','native':native.get('status')}
        if native.get('status') not in ('VERIFIED','REJECTED_MALFORMED'):return {'status':'UNVERIFIABLE','reason':'receipt native result unavailable'}
        return {'status':'VERIFIED' if root==recomputed and native['status']=='VERIFIED' else 'REFUTED','root':root,'recomputed':recomputed,'native':native['status']}
    except (OSError,ValueError,subprocess.TimeoutExpired):return {'status':'UNVERIFIABLE','reason':'receipt verification unavailable'}
