"""Offline same-evidence comparison. Only verifier stdout is deterministic; timing is separate."""
import argparse, json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from src.v2.composition import verify
from src.v2.scenarios import scenarios
def run():
    rows=[]
    for item in scenarios():
        result=verify(item['case'])
        rows.append({k:item[k] for k in ('name','expected','boundary')} | {'result':result,'passed':result['status']==item['expected']})
    negatives=[r for r in rows if r['expected']!='VERIFIED']
    summary={'scenarios':len(rows),'negative_cases':len(negatives),'baseline_false_authorizations':sum(r['result']['baseline_authorized'] for r in negatives),'composition_false_authorizations':sum(r['result']['authorized'] for r in negatives),'baseline_refusals':sum(not r['result']['baseline_authorized'] for r in negatives),'composition_refusals':sum(not r['result']['authorized'] for r in negatives),'baseline_unverifiable':sum(r['result']['baseline_status']=='UNVERIFIABLE' for r in rows),'composition_unverifiable':sum(r['result']['status']=='UNVERIFIABLE' for r in rows),'passed':all(r['passed'] for r in rows)}
    return {'schema':'real-artifact-comparison-v2','scope':'genuine laboratory crypto and public MatMul; historical external chain remains unavailable','summary':summary,'cases':rows}
if __name__=='__main__':
    report=run();print(json.dumps(report,sort_keys=True,indent=2));raise SystemExit(0 if report['summary']['passed'] else 1)
