import concurrent.futures,datetime,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019/phase1'
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019')
REPO='pipavlo82/verifiable-ai-guarantee-composition';OUT.mkdir(parents=True,exist_ok=True)
def dump(p,obj):p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def run(name,args,cwd=None):
    p=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True,timeout=300)
    for s in ('stdout','stderr'):(OUT/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
    dump(OUT/(name+'.command.json'),{'command':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
    if p.returncode:raise RuntimeError(name+': '+p.stderr.decode(errors='replace'))
    return p.stdout
def api(name,path):return json.loads(run(name,['gh','api','repos/'+REPO+'/'+path]))
prs={}
for n in range(2,7):prs[str(n)]=api('pr'+str(n),'pulls/'+str(n))
jobs=[('main','commits/main')]
for n,p in prs.items():
    jobs.extend([(f'pr{n}-reviews',f'pulls/{n}/reviews?per_page=100'),(f'pr{n}-comments',f'issues/{n}/comments?per_page=100'),(f'pr{n}-runs',f'actions/runs?head_sha={p["head"]["sha"]}&per_page=100'),(f'pr{n}-checks',f'commits/{p["head"]["sha"]}/check-runs?per_page=100')])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=dict(zip((name for name,_ in jobs),ex.map(lambda item:api(*item),jobs)))
if ROOT.exists():raise RuntimeError('Integration workspace already exists; inspect it before reuse')
run('clone',['git','-c','core.autocrlf=false','clone','--no-checkout','https://github.com/'+REPO+'.git',ROOT])
run('fetch-main',['git','fetch','origin','main'],ROOT)
for n in prs:run('fetch-pr'+n,['git','fetch','origin',f'refs/pull/{n}/head:refs/review/pr{n}'],ROOT)
run('checkout-main',['git','-c','core.autocrlf=false','checkout','--detach',results['main']['sha']],ROOT)
for n,p in prs.items():
    if run('head-pr'+n,['git','rev-parse','refs/review/pr'+n],ROOT).decode().strip()!=p['head']['sha']:raise RuntimeError('PR head raced '+n)
ancestry=[]
for a in prs:
    for b in prs:
        if a==b:continue
        p=subprocess.run(['git','merge-base','--is-ancestor',prs[a]['head']['sha'],prs[b]['head']['sha']],cwd=ROOT,capture_output=True)
        if p.returncode not in (0,1):raise RuntimeError(p.stderr.decode())
        if p.returncode==0:ancestry.append({'ancestor_pr':a,'descendant_pr':b})
pins={'main':results['main']['sha'],'repository':REPO,'root':str(ROOT),'ancestry':ancestry,'prs':{n:{'head':p['head']['sha'],'base':p['base']['sha'],'base_ref':p['base']['ref'],'head_ref':p['head']['ref'],'author':p['user']['login'],'draft':p['draft'],'state':p['state'],'merged':p['merged'],'auto_merge':p['auto_merge'],'reviews':results[f'pr{n}-reviews'],'checks':results[f'pr{n}-checks']['total_count'],'runs':[{'id':r['id'],'status':r['status'],'conclusion':r['conclusion'],'url':r['html_url']} for r in results[f'pr{n}-runs']['workflow_runs']]} for n,p in prs.items()}}
for n in ('5','6'):
    target=Path(str(ROOT)+'-pr'+n)
    if target.exists():raise RuntimeError('Fresh replay target already exists')
    run('clone-pr'+n,['git','-c','core.autocrlf=false','clone','--no-checkout','https://github.com/'+REPO+'.git',target])
    run('replay-fetch-pr'+n,['git','fetch','origin','refs/pull/'+n+'/head'],target)
    run('replay-checkout-pr'+n,['git','-c','core.autocrlf=false','checkout','--detach',prs[n]['head']['sha']],target)
dump(OUT/'pins.json',pins)
print(json.dumps({k:v for k,v in pins.items() if k!='prs'},indent=2))
print(json.dumps({n:{k:v for k,v in p.items() if k not in ('reviews','runs')} for n,p in pins['prs'].items()},indent=2))
