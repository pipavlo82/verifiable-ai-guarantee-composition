"""Prepare only isolated build dependencies. Never broadcast or deploy."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PIN='b013eff2ac4fce26f34d789e6f5c49021c5ee817'
def main():
 p=argparse.ArgumentParser();p.add_argument('--online',action='store_true');p.add_argument('--forge-std-cache');a=p.parse_args();B=ROOT/'build/escrow';B.mkdir(parents=True,exist_ok=True)
 src=Path(a.forge_std_cache).resolve() if a.forge_std_cache else B/'forge-std-source'
 if not src.exists():
  if not a.online:raise RuntimeError('Supply --online or verified --forge-std-cache')
  subprocess.run(['git','clone','--no-checkout','https://github.com/foundry-rs/forge-std.git',str(src)],check=True)
  subprocess.run(['git','-c','core.autocrlf=false','checkout','--detach',PIN],cwd=src,check=True)
 lock=json.loads((ROOT/'fixtures/escrow-v0/runtime-lock.json').read_bytes())
 bad=[p for p,h in lock['forge_std_files'].items() if not (src/p).is_file() or hashlib.sha256((src/p).read_bytes()).hexdigest()!=h]
 if bad:raise RuntimeError('forge-std bytes differ: '+str(bad[:5]))
 lib=B/'lib/forge-std'
 for rel in lock['forge_std_files']:
  dest=lib/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/rel,dest)
 vendor=ROOT/'experiments/verdict_escrow/vendor/invinoveritas';stock=B/'stock';shutil.copytree(vendor,stock,dirs_exist_ok=True)
 test=stock/'integrations/verdict-escrow/test/VerdictGatedEscrow.t.sol';before=test.read_bytes();adapted=before.decode().replace('c[0] = "python3";','c[0] = vm.envString("LAB_PYTHON");').encode();test.write_bytes(adapted)
 report={'forge_std_commit':PIN,'forge_std_files':len(lock['forge_std_files']),'stock_harness_adaptation':'python3 -> vm.envString(LAB_PYTHON), interpreter selection only','before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(adapted).hexdigest()}
 (B/'setup.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(report))
if __name__=='__main__':main()
