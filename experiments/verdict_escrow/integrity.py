import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE='c93087f06bd14c45a1d12b0c068195e3bef05dae'
def check():
 entries=[]
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE],cwd=ROOT).split(b'\0'):
  if not row:continue
  meta,p=row.split(b'\t',1);_,kind,oid=meta.split()
  if kind==b'blob':entries.append((p.decode(),oid.decode()))
 data=subprocess.check_output(['git','cat-file','--batch'],cwd=ROOT,input=''.join(oid+'\n' for _,oid in entries).encode());offset=0;bad=[]
 for p,oid in entries:
  end=data.index(b'\n',offset);size=int(data[offset:end].split()[2]);raw=data[end+1:end+1+size];offset=end+size+2
  if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).digest()!=hashlib.sha256(raw).digest():bad.append(p)
 lock=json.loads((ROOT/'experiments/verdict_escrow/source-lock.json').read_bytes());vendor=ROOT/'experiments/verdict_escrow/vendor/invinoveritas';vb=[p for p,h in lock['files'].items() if hashlib.sha256((vendor/p).read_bytes()).hexdigest()!=h]
 return {'baseline':BASE,'baseline_files':len(entries),'baseline_changed':bad,'vendor_files':len(lock['files']),'vendor_changed':vb,'passed':not bad and not vb}
if __name__=='__main__':
 r=check();print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
