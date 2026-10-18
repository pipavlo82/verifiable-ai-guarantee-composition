import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v4.model import V,U
from src.v4 import model as v4model
from src.v4_1.model import evaluate,facts,admit
from src.v4_1.scenarios import cases,reuse_cases
def main():
    p=argparse.ArgumentParser();p.add_argument('--case');a=p.parse_args();rows=[];results={}
    for row in cases():
        if a.case and row['name']!=a.case and not a.case.startswith(('reused_','control_')):continue
        f=facts(row['case']);result=evaluate(row['case'],f);results[row['name']]=result
        extra={}
        if row.get('v4_expected_C') is not None:extra['v4_C']=v4model.evaluate(row['v4_case'])['C']
        rows.append({k:v for k,v in row.items() if k not in ('case','v4_case')}|{'result':result,**extra,'passed':result['C']['status']==row['expected'] and all(row.get('expected_'+m) is None or row['expected_'+m]==result[m]['status'] for m in ('A','B')) and (row.get('v4_expected_C') is None or extra['v4_C']['status']==row['v4_expected_C'])})
    reuse=[]
    for name,src,contract,claim_type,expected in reuse_cases():
        if a.case and a.case!=name and not (a.case in results and not a.case.startswith(('reused_','control_'))):
            if a.case!=name:continue
        res=results.get(src) if isinstance(src,str) else None
        if res is None:
            c=src if not isinstance(src,str) else next(r['case'] for r in cases() if r['name']==src)
            res=evaluate(c)
        got=admit(res,contract,claim_type)
        reuse.append({'name':name,'source_authorized':res['C']['authorized'],'binding':res['C']['binding'],'admitted':got,'expected':expected,'passed':got==expected and res['C']['authorized']})
    summary={m:{'false_authorizations':sum(r['expected']!=V and r['result'][m]['authorized'] for r in rows),'positive_authorizations':sum(r['expected']==V and r['result'][m]['authorized'] for r in rows)} for m in ('A','B','C')}
    summary['false_admissions']=sum(r['admitted'] and not r['expected'] for r in reuse)
    out={'schema':'v4.1-comparison','cases':rows,'reuse':reuse,'summary':summary,'passed':bool(rows or reuse) and all(r['passed'] for r in rows+reuse)}
    print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
