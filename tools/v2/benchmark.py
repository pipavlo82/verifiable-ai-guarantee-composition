"""Small paired wall-clock measurement, including identical verifier process startup."""
import json, statistics, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v2.composition import verify
from src.v2.scenarios import scenarios
def main():
    cases=scenarios();verify(cases[0]['case'])
    rows=[]
    for rep in range(3):
        times={}
        for mode in (['A','B'] if rep%2==0 else ['B','A']):
            start=time.perf_counter_ns()
            answers=[verify(r['case'],component_only=mode=='A')['authorized'] for r in cases]
            times[mode]=time.perf_counter_ns()-start
            if mode=='B' and sum(answers)!=1:raise RuntimeError('Benchmark did not execute expected verifier')
        rows.append({'repeat':rep,'A_ns':times['A'],'B_ns':times['B'],'difference_ns':times['B']-times['A']})
    print(json.dumps({'schema':'paired-local-timing-v2','cases_per_pass':len(cases),'repeats':3,'includes':'Python-to-Node and native process startup, real crypto, same evidence','warning':'exploratory local timing; no statistical or portable performance advantage claimed','pairs':rows,'median_A_ns':statistics.median(r['A_ns'] for r in rows),'median_B_ns':statistics.median(r['B_ns'] for r in rows),'median_paired_difference_ns':statistics.median(r['difference_ns'] for r in rows)},indent=2))
if __name__=='__main__':main()
