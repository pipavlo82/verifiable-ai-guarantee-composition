"""Compare semantic replay evidence across hosts; timings and stdout newline differ."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def portable(report):
    for row in report['cases']:
        native=row['result']['native']
        if native.get('stdout'):native['stdout']=json.loads(native['stdout'])
        if native.get('stderr'):native['stderr']=native['stderr'].replace('\r\n','\n')
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/v2/validation');args=p.parse_args()
    actual=json.loads((ROOT/args.out/'comparison-normal.stdout.log').read_bytes())
    saved=json.loads((ROOT/'evidence/v2/validation/comparison-normal.stdout.log').read_bytes())
    mutations=json.loads((ROOT/args.out/'mutations-normal.stdout.log').read_bytes())
    expected=json.loads((ROOT/'evidence/v2/validation/mutations-normal.stdout.log').read_bytes())
    checks={'comparison':portable(actual)==portable(saved),'mutations':mutations==expected}
    print(json.dumps(checks));return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
