import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404.engine import decide,V,U
from src.erc8404.cases import cases

def run():
    rows=[]
    for w in cases():
        results={m:decide(w['case'],m) for m in 'ABC'}
        if results['C']['status']!=w['expected']:raise RuntimeError(w['name']+' expected '+w['expected']+' got '+json.dumps(results['C']))
        rows.append({k:v for k,v in w.items() if k!='case'}|{'results':results})
    summary={}
    for m in 'ABC':
        negative=[r for r in rows if r['kind']=='negative'];positive=[r for r in rows if r['kind']=='positive']
        summary[m]={'incorrect_downstream_authorizations':sum(r['results'][m]['authorized'] for r in negative),'correct_refusals':sum(not r['results'][m]['authorized'] for r in negative),'unverifiable':sum(r['results'][m]['status']==U for r in rows),'positive_authorizations':sum(r['results'][m]['authorized'] for r in positive),'missing_obligation_detected':sum(bool(r['results'][m]['missing_obligations']) for r in rows)}
    return {'schema':'claim-aware-experiment-v1','scope':'finite controlled research fixtures; A/B downstream lifts are deliberately incomplete consumer policies, not ERC-8404 defects','scenarios':len(rows),'summary':summary,'cases':rows}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
