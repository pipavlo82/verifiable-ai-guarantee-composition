"""Capture complete local replay logs, real mutations, deterministic comparison and timings."""
import argparse, hashlib, json, platform, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/v2/validation');p.add_argument('--skip-benchmark',action='store_true');args=p.parse_args()
    out=ROOT/args.out;out.mkdir(parents=True,exist_ok=True);rows=[];outputs={}
    def run(name,arguments,opt=False):
        command=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*arguments]
        r=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=900)
        for stream in ('stdout','stderr'):(out/f'{name}.{stream}.log').write_bytes(getattr(r,stream))
        row={'name':name,'command':command,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
        match=re.search(rb'Ran (\d+) tests',r.stderr)
        if match:row['tests']=int(match.group(1))
        rows.append(row);outputs[name]=r.stdout
    for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
        run('tests-'+mode,['-m','unittest','discover','-s','tests/v2','-v'],opt)
        run('comparison-'+mode,['tools/v2/run.py'],opt)
    for mode,opt in [('normal',False),('optimized',True)]:run('mutations-'+mode,['tools/v2/mutations.py','--out',str(out/f'mutants-{mode}')],opt)
    if not args.skip_benchmark:run('benchmark',['tools/v2/benchmark.py'])
    deterministic=outputs['comparison-normal']==outputs['comparison-repeat']==outputs['comparison-optimized']
    mutations_deterministic=outputs['mutations-normal']==outputs['mutations-optimized']
    report={'schema':'complete-v2-validation','python':sys.version.split()[0],'platform':platform.platform(),'runs':rows,'comparison_deterministic':deterministic,'mutations_deterministic':mutations_deterministic,'passed':all(r['exit']==0 for r in rows) and deterministic and mutations_deterministic}
    for name,key in [('comparison-normal','comparison'),('mutations-normal','mutations')]:
        try:report[key]=json.loads(outputs[name])['summary' if key=='comparison' else 'counts']
        except (ValueError,KeyError):report['passed']=False
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2))
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
