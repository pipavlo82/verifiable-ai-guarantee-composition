"""Independent extraction of the narrow native wire format, never a proof verifier."""
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=18446744069414584321
def extract(directory):
    data=(directory/'proof.bin').read_bytes();offset=8
    if data[:8]!=b'VAGCNP2\0':raise ValueError('wire profile')
    def number():
        nonlocal offset
        n=struct.unpack_from('<I',data,offset)[0];offset+=4;return n
    def vector(count):
        nonlocal offset
        if number()!=count:raise ValueError('shape')
        values=list(struct.unpack_from('<'+'Q'*count,data,offset));offset+=8*count
        if any(x>=P for x in values):raise ValueError('noncanonical field')
        return values
    claimed=vector(1)[0];u=vector(2);v=vector(3);ch=vector(3);rounds=vector(9);evals=vector(2);claims=[]
    for tid,length in [(0,5),(1,6),(2,5)]:
        if number()!=tid:raise ValueError('tensor id')
        claims.append({'tensor_id':tid,'point':vector(length),'evaluation':vector(1)[0]})
    if offset!=len(data):raise ValueError('trailing bytes')
    return {'schema':'native-public-statement-v2','not_a_verifier':True,'operator':{'MatMul':{'a':0,'b':1,'c':2,'m':4,'k':8,'n':8}},'field_modulus':P,'encoding':'canonical-u64-little-endian','artifact_sha256':{name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in ('input.bin','weights.bin','output.bin','proof.bin','model.json')},'claimed':claimed,'u':u,'v':v,'ch':ch,'sumcheck_round_coefficients':rounds,'sumcheck_terminal_evaluations':evals,'tensor_claims':claims,'bound':[],'binds':[],'security_scope':'public tensors; native verification plus full deterministic output recomputation; no zero-knowledge, succinctness or malicious-prover soundness claim'}
if __name__=='__main__':
    for variant in ('a','b'):
        directory=ROOT/'evidence/v2/capture'/variant
        obj=extract(directory);target=directory/'public-statement.json'
        content=json.dumps(obj,indent=2,sort_keys=True)+'\n'
        if '--write' in sys.argv:target.write_text(content,encoding='utf-8',newline='\n')
        elif target.read_text(encoding='utf-8')!=content:raise RuntimeError('Statement mismatch')
    print(json.dumps({'statements':2,'matched':True}))
