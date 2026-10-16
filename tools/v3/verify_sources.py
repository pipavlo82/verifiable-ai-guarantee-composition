import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    sources=json.loads((ROOT/'evidence/v3/discovery/sources.json').read_text());sources+=[json.loads((ROOT/'evidence/v3/public/ccip-router-source.json').read_text())]
    checks=[]
    for source in sources:
        if source['repository']=='ethereum/ERCs':continue
        clone=ROOT/'build/v3/upstream'/source['repository'].split('/')[1]
        try:
            head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=clone).decode().strip();dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=clone)
            checks.append({'repository':source['repository'],'head':head,'passed':head==source['commit'] and not dirty})
        except (OSError,subprocess.CalledProcessError):checks.append({'repository':source['repository'],'passed':False})
    for file in json.loads((ROOT/'evidence/v3/upstream/selected-source-lock.json').read_text()):
        p=ROOT/(file['preserved_path'] or ('build/v3/upstream/'+file['repository'].split('/')[1]+'/'+file['path']))
        reference_only=file['repository'] in ('trustless-ai/agent-ercs','trustless-ai/ccip-router')
        raw=subprocess.check_output(['git','show',file['commit']+':'+file['path']],cwd=ROOT/'build/v3/upstream'/file['repository'].split('/')[1]) if reference_only else p.read_bytes() if p.exists() else b''
        checks.append({'file':file['path'],'verification':'exact Git blob (review-only text)' if reference_only else 'exact executed/preserved bytes','passed':hashlib.sha256(raw).hexdigest()==file['sha256']})
    print(json.dumps({'checks':checks,'passed':all(c['passed'] for c in checks)},indent=2,sort_keys=True));return 0 if all(c['passed'] for c in checks) else 1
if __name__=='__main__':raise SystemExit(main())
