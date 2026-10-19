"""Finite local timing experiment; subprocess startup is included."""
import json,platform,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404.engine import decide
from src.erc8404.cases import base
c=base();samples={m:[] for m in 'ABC'}
for m in 'ABC':decide(c,m)
for i in range(12):
 for m in ('ABC','BCA','CAB')[i%3]:
  start=time.perf_counter_ns();d=decide(c,m);elapsed=time.perf_counter_ns()-start
  if not d['authorized']:raise RuntimeError('positive benchmark control failed')
  samples[m].append(elapsed)
med={m:statistics.median(v)/1e6 for m,v in samples.items()}
print(json.dumps({'scope':'12 repeated positive laboratory fixture runs per mode on this host; warmed Python import, fresh Node signature subprocess per B/C call; no general performance claim','python':sys.version,'platform':platform.platform(),'samples_ns':samples,'median_ms':med,'median_C_minus_B_ms':med['C']-med['B'],'median_C_minus_A_ms':med['C']-med['A']},indent=2,sort_keys=True))
