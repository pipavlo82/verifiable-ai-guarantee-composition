import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.integration.engine import evaluate,admit,V,U
from src.integration.cases import cases
def run(benchmark=False):
    rows=[];timing={m:[] for m in 'ABCD'}
    for w in cases():
        results={}
        for m in 'ABC':
            start=time.perf_counter();results[m]=evaluate(w['case'],m);timing[m].append(time.perf_counter()-start)
        start=time.perf_counter();results['D']=admit(results['C'],w['case']);timing['D'].append(time.perf_counter()-start)
        if results['C']['status']!=w['expected'] or results['D']['status']!=w['expected']:raise RuntimeError(w['name']+' expected '+w['expected']+' got '+json.dumps(results['C']))
        rows.append({k:v for k,v in w.items() if k!='case'}|{'results':results})
    summary={m:{'false_authorizations':sum(r['kind']=='negative' and r['results'][m]['authorized'] for r in rows),'correct_refusals':sum(r['kind']=='negative' and not r['results'][m]['authorized'] for r in rows),'positive_authorizations':sum(r['kind']=='positive' and r['results'][m]['authorized'] for r in rows),'unverifiable':sum(r['results'][m]['status']==U for r in rows),'missing_obligation_detection':sum(bool((r['results'][m].get('recomputed') or r['results'][m]).get('missing_obligations')) for r in rows)} for m in 'ABCD'}
    report={'scenarios':len(rows),'summary':summary,'cases':rows,'scope':'Finite laboratory controls. A and B are deliberately narrower guarantees; downstream lifting is an experimental consumer choice.'}
    if benchmark:report['timing_seconds']={m:{'total':sum(v),'mean':sum(v)/len(v),'samples':len(v)} for m,v in timing.items()}
    return report
if __name__=='__main__':print(json.dumps(run('--benchmark' in sys.argv),indent=2,sort_keys=True))
