import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE='c93087f06bd14c45a1d12b0c068195e3bef05dae'

# One authorized documentation revision, not a general README exclusion. The
# original remains verifiable at its original digest in the archived snapshot.
README_ARCHIVE='research/history/README-3d55a845.md'
README_ORIGINAL='c545773112d834399de7fc6c765807c571ba0469562b64f776b52ad7142e0be9'
README_CURRENT='ca021c56b2ed76d2eeb5f940677ef15691f2d74e29e40e436b558b2cf030103f'

def documentation_refresh(path, original_digest, current):
 if path!='README.md' or original_digest!=README_ORIGINAL:return False
 try:
  return hashlib.sha256(current).hexdigest()==README_CURRENT and hashlib.sha256((ROOT/README_ARCHIVE).read_bytes()).hexdigest()==README_ORIGINAL
 except OSError:return False

def manifest_refresh(original, current):
 # Original entries remain binding, with only the exact documented README
 # revision accepted. The unchanged verifier checks the entire current set.
 try:
  old=json.loads(original);new=json.loads(current)
  metadata={k:v for k,v in old.items() if k!='files'}
  same_metadata={k:v for k,v in new.items() if k!='files'}==metadata
  preserved=all(new['files'].get(p)==h for p,h in old['files'].items())
  accounted=all(new['files'].get(p)==h or (p=='README.md' and new['files'].get(p)==README_CURRENT and documentation_refresh(p,h,(ROOT/p).read_bytes())) for p,h in old['files'].items())
  canonical=current==(json.dumps(new,indent=2,sort_keys=True)+'\n').encode('utf8')
  gate=subprocess.run([sys.executable,'-B','tools/verify_artifacts.py'],cwd=ROOT,capture_output=True)
  verified=json.loads(gate.stdout)
  passed=same_metadata and accounted and canonical and gate.returncode==0 and verified['passed'] is True
  return {'passed':passed,'original_sha256':hashlib.sha256(original).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),'old_entries_preserved':preserved,'old_entries_accounted_for':accounted,'canonical':canonical,'whole_repository_gate':verified}
 except (ValueError,KeyError,TypeError,OSError):return {'passed':False}
def check():
 entries=[]
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE],cwd=ROOT).split(b'\0'):
  if not row:continue
  meta,p=row.split(b'\t',1);_,kind,oid=meta.split()
  if kind==b'blob':entries.append((p.decode(),oid.decode()))
 data=subprocess.check_output(['git','cat-file','--batch'],cwd=ROOT,input=''.join(oid+'\n' for _,oid in entries).encode());offset=0;bad=[];refresh=None;docs=[]
 for p,oid in entries:
  end=data.index(b'\n',offset);size=int(data[offset:end].split()[2]);raw=data[end+1:end+1+size];offset=end+size+2
  if not (ROOT/p).is_file():bad.append(p);continue
  current=(ROOT/p).read_bytes()
  if current!=raw:
   if documentation_refresh(p,hashlib.sha256(raw).hexdigest(),current):
    docs.append({'path':p,'archive':README_ARCHIVE,'original_sha256':README_ORIGINAL,'current_sha256':README_CURRENT});continue
   if p=='artifacts.sha256.json':
    refresh=manifest_refresh(raw,current)
    if refresh['passed']:continue
   bad.append(p)
 lock=json.loads((ROOT/'experiments/verdict_escrow/source-lock.json').read_bytes());vendor=ROOT/'experiments/verdict_escrow/vendor/invinoveritas';vb=[p for p,h in lock['files'].items() if hashlib.sha256((vendor/p).read_bytes()).hexdigest()!=h]
 return {'baseline':BASE,'baseline_files':len(entries),'baseline_changed':bad,'documentation_refresh':docs,'manifest_refresh':refresh,'vendor_files':len(lock['files']),'vendor_changed':vb,'passed':not bad and not vb}
if __name__=='__main__':
 r=check();print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
