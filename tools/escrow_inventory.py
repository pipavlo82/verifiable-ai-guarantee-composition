"""Verify the separate experiment inventory; preserve all historical manifests."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    inventory=json.loads((ROOT/'evidence/escrow-v0/SHA256.json').read_bytes())
    bad=[rel for rel,digest in inventory.items() if not (ROOT/rel).is_file() or hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest]
    print(json.dumps({'files':len(inventory),'mismatches':bad,'passed':not bad},indent=2))
    return bool(bad)
if __name__=='__main__':raise SystemExit(main())
