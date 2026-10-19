"""Offline consumer CLI; request contains receipt/profile/evidence and contract bytes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404.engine import decide
from src.erc8404.cases import base
p=argparse.ArgumentParser();p.add_argument('request',nargs='?');p.add_argument('--example',action='store_true');a=p.parse_args()
if a.example:print(json.dumps(base(),indent=2,sort_keys=True))
elif a.request:print(json.dumps(decide(json.loads(Path(a.request).read_bytes())),indent=2,sort_keys=True))
else:p.error('request path or --example required')
