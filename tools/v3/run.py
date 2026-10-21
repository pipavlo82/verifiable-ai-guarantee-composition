import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v3.model import evaluate,graph,closure
from src.v3.scenarios import cases
def main():
    p=argparse.ArgumentParser();p.add_argument('--case');p.add_argument('--plan');a=p.parse_args()
    if a.plan:print(json.dumps({'claim':a.plan,'required':closure(a.plan),'contracts':graph()},indent=2,sort_keys=True));return 0
    rows=[]
    for row in cases():
        if a.case and row['name']!=a.case:continue
        result=evaluate(row['case'],row['request'],row['claim']);baseline=evaluate(row['case'],row['request'],row['claim'],True)
        # Runtime stdout hashes are not portable semantic identity.
        for r in (result,baseline):r.pop('crypto_execution',None)
        rows.append({'name':row['name'],'expected':row['expected'],'result':result,'baseline':baseline,'passed':result['status']==row['expected']})
    if not rows:raise ValueError('Unknown or empty case selection')
    summary={'scenarios':len(rows),'negative_cases':sum(r['expected']!='VERIFIED' for r in rows),'baseline_false_authorizations':sum(r['expected']!='VERIFIED' and r['baseline']['authorized'] for r in rows),'composition_false_authorizations':sum(r['expected']!='VERIFIED' and r['result']['authorized'] for r in rows),'baseline_correct_refusals':sum(r['expected']!='VERIFIED' and not r['baseline']['authorized'] for r in rows),'composition_correct_refusals':sum(r['expected']!='VERIFIED' and not r['result']['authorized'] for r in rows),'baseline_unverifiable':sum(r['baseline']['status']=='UNVERIFIABLE' for r in rows),'composition_unverifiable':sum(r['result']['status']=='UNVERIFIABLE' for r in rows),'passed':all(r['passed'] for r in rows)}
    print(json.dumps({'schema':'composition-v3-results','cases':rows,'summary':summary},indent=2,sort_keys=True));return 0 if summary['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
