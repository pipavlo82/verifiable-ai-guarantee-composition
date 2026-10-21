import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 lock=json.loads((ROOT/'fixtures/v4/source-lock.json').read_bytes());rows=[]
 for s in lock['sources']:
  if s['repository']=='ethereum/ERCs':
   path=ROOT/'evidence/v4/sources'/Path(s['path']).name;actual=hashlib.sha256(path.read_bytes()).hexdigest();rows.append({'repository':s['repository'],'commit':s['commit'],'sha256':actual,'passed':actual==s['sha256'],'verification':'preserved exact blob vs independently captured source pin'})
  else:
   clone=ROOT/'build/v3/upstream'/s['repository'].split('/')[1];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=clone).decode().strip();dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=clone)
   rows.append({'repository':s['repository'],'commit':head,'passed':head==s['commit'] and not dirty,'verification':'fresh checkout commit and tracked worktree cleanliness'})
 rows.append({'file':'identity.json','passed':hashlib.sha256((ROOT/'evidence/v4/sources/identity.json').read_bytes()).hexdigest()==lock['identity_spec_sha256']})
 report={'checks':rows,'passed':all(r['passed'] for r in rows)};print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
