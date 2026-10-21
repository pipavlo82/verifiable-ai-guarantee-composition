"""Check an externally supplied acquisition bundle. Never execute its commands.

Successful byte acquisition is not successful semantic integration.
Exit 2: missing/unsupported evidence; exit 1: contradictory supplied digest.
"""
import argparse,hashlib,json
from pathlib import Path
REQUIREMENTS={
 'raw-input.bin':'Original admitted bytes, not a normalized reconstruction',
 'sanitized-input.bin':'Exact transform output consumed by inference',
 'transform.json':'Versioned deterministic transform/CID and executable source pin',
 'wyriwe.json':'Complete signed EIP-712 schema and domain, timestamp, signer, commitments',
 'authority.json':'Independent gateway/model/judgment/action policy with chain and block context',
 'model.json':'Exact model, weights, circuit and native toolchain identifiers',
 'weights.bin':'Native verifier weights',
 'output.bin':'Native inference output',
 'proof.bin':'Genuine producer-generated proof, exact serialization and public statement',
 'judgment.json':'Signed subject, input, proof statement, action, policy and scope',
 'execution.json':'Action/result receipt plus independently verifiable effect or mediation evidence',
 'execution-witness.bin':'Raw external transaction/trace/admission witness, not an opaque hash only',
 'historical-ledger-236.raw':'Optional historical CRC reproduction bytes matching the signed 6cb8... hash',
}
def inspect(folder):
    root=Path(folder).resolve();manifest=root/'manifest.json';missing=[];refuted=[];present=[]
    try:declared=json.loads(manifest.read_bytes())['files']
    except (OSError,ValueError,KeyError,TypeError):declared={};missing.append('manifest.json with file -> SHA-256 mapping')
    for name in REQUIREMENTS:
        if name=='historical-ledger-236.raw':continue
        path=root/name
        if not path.is_file() or root not in path.resolve().parents or name not in declared:missing.append(name);continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=declared[name]:refuted.append(name)
        else:present.append(name)
    return {'status':'REFUTED' if refuted else 'UNVERIFIABLE','acquired_hash_checked':present,'missing':missing,'digest_mismatches':refuted,'integration':'NOT IMPLEMENTED for new external bundles; authority, provenance admission, native statement linkage and execution semantics require independent review','full_chain_authorized':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--bundle');a=p.parse_args()
    if not a.bundle:print(json.dumps({'requirements':REQUIREMENTS,'warning':'No credentials or private keys belong in the bundle.'},indent=2));return 0
    result=inspect(a.bundle);print(json.dumps(result,indent=2));return 1 if result['digest_mismatches'] else 2
if __name__=='__main__':raise SystemExit(main())
