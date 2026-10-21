import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    lock=json.loads((ROOT/'fixtures/integration/source-lock.json').read_bytes());rows={}
    for section in ('frozen_core','pr5_import','pr6_preserved'):
        failed=[p for p,h in lock[section].items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
        rows[section]={'files':len(lock[section]),'mismatches':failed,'passed':not failed}
    report={'source_shas':lock['source_shas'],'checks':rows,'passed':all(r['passed'] for r in rows.values())};print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
