"""Continue unchanged engine replay after correcting an invalid secondary test premise."""
import hashlib,json,platform,re,subprocess,sys,time
from pathlib import Path
ROOT=Path('C:/Users/msi/Documents/Codex/vagc-integration-20261019');OUT=ROOT/'build/integration/prepublication';commands=json.loads((OUT/'commands.json').read_bytes())
def run(name,args):
 cmd=[sys.executable,'-B','-X','utf8',*args];start=time.perf_counter();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=2400)
 for s in ('stdout','stderr'):(OUT/(name+'.'+s+'.log')).write_bytes(getattr(p,s))
 n=re.search(rb'Ran (\d+) tests',p.stderr);commands.append({'name':name,'command':cmd,'exit':p.returncode,'elapsed_seconds':time.perf_counter()-start,'tests':int(n[1]) if n else None,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
 (OUT/'commands-complete.json').write_text(json.dumps(commands,indent=2)+'\n',encoding='utf8',newline='\n');print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(name)
run('secondary-crypto-native-corrected',['tools/integration/secondary.py'])
run('secondary-pr6',['tools/erc8404/secondary.py'])
for suite in ('v2','v3','v4','v4_1','erc8404'):run('regression-'+suite,['-m','unittest','discover','-s','tests/'+suite,'-v'])
run('benchmark',['tools/integration/run.py','--benchmark'])
run('integrity-after',['tools/integration/integrity.py'])
det={k:len({(OUT/(k+'-'+m+'.stdout.log')).read_bytes() for m in ('normal','repeat','optimized')})==1 for k in ('comparison','mutations','pr5-targeted','fallback','read-tracking')}
comparison=json.loads((OUT/'comparison-normal.stdout.log').read_bytes())
report={'environment':{'python':sys.version,'platform':platform.platform()},'commands':commands,'determinism':det,'scenarios':comparison['scenarios'],'comparison':comparison['summary'],'mutations':json.loads((OUT/'mutations-normal.stdout.log').read_bytes())['counts'],'resolved_failure':'Initial secondary negative added subject to LabProvenance, whose typed schema does not sign that field. Corrected control mutates signed LabJudgment.subject. Original failure retained; no verifier code changed.','admission_supplement':'evidence/integration/admission/report.json','passed':all(det.values()) and all(r['exit']==0 for r in commands if r['name']!='secondary-crypto-native')}
(OUT/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps({'passed':report['passed']}))
