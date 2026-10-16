"""Paired same-evidence wall-time samples; descriptive, not performance certification."""
import json,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v3.model import evaluate
from src.v3.scenarios import cases
rows=[]
for name in ('positive_claim_agreement','cross_subject'):
    case=next(c for c in cases() if c['name']==name);samples={'component_only':[],'composition':[]};statuses={}
    for index in range(12):
        for mode in (('component_only','composition') if index%2==0 else ('composition','component_only')):
            start=time.perf_counter_ns();result=evaluate(case['case'],case['request'],case['claim'],mode=='component_only');samples[mode].append(time.perf_counter_ns()-start);statuses[mode]=result['status']
    medians={mode:statistics.median(values) for mode,values in samples.items()}
    rows.append({'case':name,'samples_ns':samples,'medians_ns':medians,'median_difference_ns':medians['composition']-medians['component_only'],'median_ratio':medians['composition']/medians['component_only'],'statuses':statuses})
print(json.dumps({'schema':'v3-paired-benchmark','includes':'fresh Node crypto subprocess startup and actual verification in both strategies','limitation':'single host, 12 paired samples, interleaved order; scheduling variance may exceed binding cost; no general performance claim','rows':rows},indent=2,sort_keys=True))
