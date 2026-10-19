import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 pins=json.loads((ROOT/'fixtures/erc8404/core-lock.json').read_bytes())
 core={p:sha((ROOT/'evidence/erc8404/core'/p).read_bytes())==s for p,s in pins.items()}
 sources=json.loads((ROOT/'evidence/erc8404/sources/sources.json').read_bytes())
 specs={str(s['pr']):sha((ROOT/'evidence/erc8404/sources'/(str(s['path'].split('-')[-1]))).read_bytes())==s['sha256'] for s in sources if s['kind']=='proposal'}
 history=json.loads((ROOT/'fixtures/erc8404/history-lock.json').read_bytes())
 entries=history['files']
 historical={p:sha((ROOT/p).read_bytes())==digest for p,digest in entries.items() if p not in ('README.md','.gitattributes')}
 result={'core_files':len(core),'core_byte_identical':all(core.values()),'formal_source_pins':specs,'historical_files':len(historical),'history_byte_identical':all(historical.values()),'changed_core':[p for p,v in core.items() if not v],'changed_history':[p for p,v in historical.items() if not v]}
 result['passed']=all(core.values()) and all(specs.values()) and all(historical.values());print(json.dumps(result,sort_keys=True,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
