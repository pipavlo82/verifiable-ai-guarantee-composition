"""Finite wall-clock samples: shared crypto collection and separate decision cost."""
import json,platform,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v4.model import evaluate,facts
from src.v4.scenarios import cases
rows=cases();samples=[];crypto=[]
for row in rows:
 start=time.perf_counter_ns();f=facts(row['case']);crypto.append(time.perf_counter_ns()-start)
 for repeat in range(7):
  order=('A','B','C') if repeat%2==0 else ('C','B','A')
  for mode in order:
   start=time.perf_counter_ns();evaluate(row['case'],f,mode=mode);samples.append({'case':row['name'],'repeat':repeat,'mode':mode,'ns':time.perf_counter_ns()-start})
medians={m:statistics.median(x['ns'] for x in samples if x['mode']==m) for m in ('A','B','C')}
print(json.dumps({'schema':'v4-finite-runtime','platform':platform.platform(),'python':sys.version,'cases':len(rows),'decision_repeats':7,'shared_crypto_ns':crypto,'shared_crypto_median_ns':statistics.median(crypto),'decision_median_ns':medians,'C_minus_B_median_ns':medians['C']-medians['B'],'raw_samples':samples,'limitations':'same machine, uncontrolled load; crypto computed once per case; decision-only costs plus shared crypto separately; no general speed/security claim'},indent=2,sort_keys=True))
