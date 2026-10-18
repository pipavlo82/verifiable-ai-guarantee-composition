import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v4.model import evaluate,facts,V,U
from src.v4.scenarios import cases
def main():
    p=argparse.ArgumentParser();p.add_argument('--case');p.add_argument('--raw',action='store_true');a=p.parse_args();rows=[];raw=[]
    for row in cases():
        if a.case and row['name']!=a.case:continue
        f=facts(row['case']);result=evaluate(row['case'],f)
        rows.append({k:v for k,v in row.items() if k!='case'}|{'result':result,'passed':result['C']['status']==row['expected'] and all(row.get('expected_'+m) is None or row['expected_'+m]==result[m]['status'] for m in ('A','B'))})
        raw.append({'case':row['name'],'commands':f['commands']})
    summary={m:{'false_authorizations':sum(r['expected']!=V and r['result'][m]['authorized'] for r in rows),'correct_refusals':sum(r['expected']!=V and not r['result'][m]['authorized'] for r in rows),'unverifiable':sum(r['result'][m]['status']==U for r in rows),'positive_authorizations':sum(r['expected']==V and r['result'][m]['authorized'] for r in rows)} for m in ('A','B','C')}
    summary['missing_obligation_detection']={'detected':sum(r['kind']=='omission' and bool(r['result']['missing_obligations']) for r in rows),'total':sum(r['kind']=='omission' for r in rows)}
    out={'schema':'v4-comparison','cases':rows,'summary':summary,'passed':bool(rows) and all(r['passed'] for r in rows)}
    if a.raw:out['raw_execution']=raw
    print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
