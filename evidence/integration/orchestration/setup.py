import hashlib,json,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019'
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');CACHE=Path('C:/Users/msi/Documents/Codex/vagc-pr5-cold-review')
pins=json.loads((OUT/'phase1/pins.json').read_bytes())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
git('switch','-c','research/claim-aware-composition-integration',pins['prs']['6']['head'])
# Add the exact PR5-only paths. Never overwrite divergent shared files.
added=git('diff','--name-only','--diff-filter=A',pins['prs']['5']['base'],pins['prs']['5']['head']).decode().splitlines()
inventory={}
for rel in added:
    data=git('show',pins['prs']['5']['head']+':'+rel);p=ROOT/rel
    if p.exists() and p.read_bytes()!=data:raise RuntimeError('Import conflict '+rel)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);inventory[rel]=hashlib.sha256(data).hexdigest()
for target in (ROOT,Path(str(ROOT)+'-pr5'),Path(str(ROOT)+'-pr6')):
    for rel in ('build/formal-v1/crypto','build/v3/python-deps'):
        shutil.copytree(CACHE/rel,target/rel)
    rel='build/chain-v2/cargo-target/debug/composition-native-capture.exe'
    (target/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(CACHE/rel,target/rel)
runtime={p.relative_to(CACHE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for rel in ('build/formal-v1/crypto','build/v3/python-deps') for p in (CACHE/rel).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
runtime[rel]=hashlib.sha256((CACHE/rel).read_bytes()).hexdigest()
for name,data in [('pr5-import.json',{'head':pins['prs']['5']['head'],'files':inventory}),('runtime-reuse.json',{'files':runtime,'native_rebuilt':False,'description':'Verified cached runtime, actual verification reruns; separate rebuild recorded if performed'})]:
    (OUT/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'imported':len(inventory),'runtime_files':len(runtime)}))
