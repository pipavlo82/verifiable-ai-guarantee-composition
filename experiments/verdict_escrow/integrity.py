import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE='c93087f06bd14c45a1d12b0c068195e3bef05dae'

def manifest_refresh(original, current):
 # Only this intentionally regenerated index may differ from PR7. All its old
 # entries remain binding; the unchanged verifier checks the entire current set.
 try:
  old=json.loads(original);new=json.loads(current)
  metadata={k:v for k,v in old.items() if k!='files'}
  same_metadata={k:v for k,v in new.items() if k!='files'}==metadata
  preserved=all(new['files'].get(p)==h for p,h in old['files'].items())
  canonical=current==(json.dumps(new,indent=2,sort_keys=True)+'\n').encode('utf8')
  gate=subprocess.run([sys.executable,'-B','tools/verify_artifacts.py'],cwd=ROOT,capture_output=True)
  verified=json.loads(gate.stdout)
  passed=same_metadata and preserved and canonical and gate.returncode==0 and verified['passed'] is True
  return {'passed':passed,'original_sha256':hashlib.sha256(original).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),'old_entries_preserved':preserved,'canonical':canonical,'whole_repository_gate':verified}
 except (ValueError,KeyError,TypeError,OSError):return {'passed':False}
def check():
 entries=[]
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE],cwd=ROOT).split(b'\0'):
  if not row:continue
  meta,p=row.split(b'\t',1);_,kind,oid=meta.split()
  if kind==b'blob':entries.append((p.decode(),oid.decode()))
 data=subprocess.check_output(['git','cat-file','--batch'],cwd=ROOT,input=''.join(oid+'\n' for _,oid in entries).encode());offset=0;bad=[];refresh=None
 for p,oid in entries:
  end=data.index(b'\n',offset);size=int(data[offset:end].split()[2]);raw=data[end+1:end+1+size];offset=end+size+2
  if not (ROOT/p).is_file():bad.append(p);continue
  current=(ROOT/p).read_bytes()
  if current!=raw:
   if p=='artifacts.sha256.json':
    refresh=manifest_refresh(raw,current)
    if refresh['passed']:continue
   bad.append(p)
 lock=json.loads((ROOT/'experiments/verdict_escrow/source-lock.json').read_bytes());vendor=ROOT/'experiments/verdict_escrow/vendor/invinoveritas';vb=[p for p,h in lock['files'].items() if hashlib.sha256((vendor/p).read_bytes()).hexdigest()!=h]
 return {'baseline':BASE,'baseline_files':len(entries),'baseline_changed':bad,'manifest_refresh':refresh,'vendor_files':len(lock['files']),'vendor_changed':vb,'passed':not bad and not vb}
if __name__=='__main__':
 r=check();print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
