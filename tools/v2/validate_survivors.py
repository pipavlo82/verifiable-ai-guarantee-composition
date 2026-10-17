"""Normal/repeat/-O replay, deterministic reports and true red-test controls."""
import argparse,hashlib,json,platform,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.v2.audit_survivors import PLANS,SOURCE
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='build/v2/survivor-validation');a=p.parse_args();out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_bytes();runs=[];reports=[]
    def run(name,args,opt=False):
        command=[sys.executable,'-B','-X','utf8',*(['-O'] if opt else []),*args]
        r=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
        for stream in ('stdout','stderr'):(out/(name+'.'+stream+'.log')).write_bytes(getattr(r,stream))
        item={'name':name,'command':command,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
        n=re.search(rb'Ran (\d+) tests',r.stderr)
        if n:item['tests']=int(n.group(1))
        runs.append(item);return r
    for mode,opt in [('normal',False),('repeat',False),('optimized',True)]:
        r=run('tests-'+mode,['-m','unittest','discover','-s','tests/v2_survivors','-v'],opt)
        if r.returncode:raise RuntimeError('Unmutated tests failed')
        r=run('audit-'+mode,['tools/v2/audit_survivors.py','--out',str(out/mode)],opt)
        if r.returncode:raise RuntimeError('Audit failed')
        reports.append(json.loads(r.stdout))
    # These deliberately red regressions execute actual unittest assertions, not just exit flags.
    controls=[]
    try:
        for plan in PLANS:
            text=original.decode();SOURCE.write_text(text.replace(plan['old'],plan['new']),encoding='utf-8',newline='\n')
            try:
                target='test_native_rejection_is_isolated' if plan['name']=='native_enforcement' else 'test_type_rejection_is_isolated'
                r=run('red-'+plan['name'],['-m','unittest','discover','-s','tests/v2_survivors','-k',target,'-v'])
                red=r.returncode==1 and b'FAILED (failures=' in r.stderr and b'errors=' not in r.stderr
                controls.append({'boundary':plan['name'],'red_assertion_failure_without_error':red,'exit':r.returncode})
            finally:SOURCE.write_bytes(original)
        green=run('tests-restored',['-m','unittest','discover','-s','tests/v2_survivors','-v'])
    finally:SOURCE.write_bytes(original)
    deterministic=reports[0]==reports[1]==reports[2]
    committed=ROOT/'evidence/v2/survivor-audit/validation/normal/report.json'
    snapshot_match=reports[0]==json.loads(committed.read_text()) if committed.exists() else None
    result={'schema':'survivor-validation-v1','environment':{'python':sys.version,'platform':platform.platform(),'node':subprocess.check_output(['node','--version'],text=True).strip(),'rustc':subprocess.check_output(['rustc','--version'],text=True).strip()},'runs':runs,'red_controls':controls,'normal_repeat_optimized_equal':deterministic,'snapshot_match':snapshot_match,
      'source_restored':SOURCE.read_bytes()==original,'counts':reports[0]['mutation_counts'],'passed':deterministic and snapshot_match is not False and green.returncode==0 and all(c['red_assertion_failure_without_error'] for c in controls) and SOURCE.read_bytes()==original}
    (out/'report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2,sort_keys=True));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
