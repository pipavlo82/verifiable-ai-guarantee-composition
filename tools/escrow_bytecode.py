"""Offline comparison of captured RPC runtime and an original-settings compiler artifact."""
import argparse, hashlib, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('snapshot');p.add_argument('artifact');a=p.parse_args()
    snap=Path(a.snapshot)
    def result(name):return json.loads((snap/(name+'.json')).read_bytes())['result']
    artifact=json.loads(Path(a.artifact).read_bytes());names={}
    def visit(o):
        if isinstance(o,dict):
            if o.get('nodeType')=='VariableDeclaration' and o.get('mutability')=='immutable':names[str(o['id'])]=o['name']
            for v in o.values():visit(v)
        elif isinstance(o,list):
            for v in o:visit(v)
    visit(artifact['ast'])
    code=bytearray.fromhex(artifact['deployedBytecode']['object'].removeprefix('0x'))
    for key,locations in artifact['deployedBytecode']['immutableReferences'].items():
        value=bytes.fromhex(result('provider0-'+names[key]).removeprefix('0x'))
        for loc in locations:
            if len(value)!=loc['length']:raise ValueError('Immutable word length')
            code[loc['start']:loc['start']+loc['length']]=value
    actual=bytes.fromhex(result('provider0-code').removeprefix('0x'))
    checks={'full_bytecode_match':bytes(code)==actual,
            'two_provider_code_agreement':result('provider0-code')==result('provider1-code'),
            'two_provider_block_agreement':result('provider0-block')['hash']==result('provider1-block')['hash']}
    print(json.dumps({'checks':checks,'runtime_sha256':hashlib.sha256(actual).hexdigest(),
                     'compiled_sha256':hashlib.sha256(code).hexdigest(),'runtime_bytes':len(actual),
                     'limitations':'Offline consistency of captured public RPC observations; no independent consensus or payment proof.'},indent=2))
    return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
