import datetime,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/claim-aware-integration-20261019/remote';OUT.mkdir(parents=True,exist_ok=True)
pub=json.loads((OUT.parent/'publication/published.json').read_bytes());REPO='pipavlo82/verifiable-ai-guarantee-composition';stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def api(label,path):
 p=subprocess.run(['gh','api','repos/'+REPO+'/'+path],capture_output=True,timeout=120);(OUT/(stamp+'-'+label+'.stdout.json')).write_bytes(p.stdout);(OUT/(stamp+'-'+label+'.stderr.log')).write_bytes(p.stderr)
 if p.returncode:raise RuntimeError(label+': '+p.stderr.decode())
 return json.loads(p.stdout)
runs=api('runs','actions/runs?head_sha='+pub['commit']+'&per_page=100');checks=api('checks','commits/'+pub['commit']+'/check-runs?per_page=100');pr=api('pr','pulls/'+pub['url'].rsplit('/',1)[1]);sources={str(n):api('pr'+str(n),'pulls/'+str(n)) for n in range(2,7)}
report={'commit':pub['commit'],'pr':{'url':pr['html_url'],'head':pr['head']['sha'],'base':pr['base']['sha'],'draft':pr['draft'],'merged':pr['merged'],'state':pr['state']},'runs':[{'id':r['id'],'name':r['name'],'event':r['event'],'status':r['status'],'conclusion':r['conclusion'],'url':r['html_url']} for r in runs['workflow_runs']],'checks':[{'name':r['name'],'status':r['status'],'conclusion':r['conclusion']} for r in checks['check_runs']],'source_prs':{n:{'head':p['head']['sha'],'base':p['base']['sha'],'draft':p['draft'],'state':p['state'],'merged':p['merged']} for n,p in sources.items()}}
report['ci_green']=bool(report['runs']) and all(r['status']=='completed' and r['conclusion']=='success' for r in report['runs']) and bool(report['checks']) and all(r['conclusion']=='success' for r in report['checks'])
(OUT/'latest.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps(report,indent=2))
