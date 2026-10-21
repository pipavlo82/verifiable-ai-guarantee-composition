"""Isolate PR6 fallback without rewriting its preserved 16/1 report."""
import copy,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.erc8404 import engine as original
from src.erc8404.cases import base
source=(ROOT/'src/erc8404/engine.py').read_bytes();old='    if raw is None: return None  # MUTATE: contract_preimage';new="    if raw is None: return case['contract']"
def main():
    if source.decode().count(old)!=1:raise RuntimeError('NOT_APPLIED')
    mutated=source.decode().replace(old,new);m=types.ModuleType('isolated_fallback');m.__file__=str(ROOT/'src/erc8404/engine.py');exec(compile(mutated,m.__file__,'exec'),m.__dict__)
    variants=[]
    c=base();variants.append(('complete',c,'VERIFIED','VERIFIED'))
    c=base();c['contract_bytes']=None;variants.append(('canonical_carrier_absent_parsed_preimage_retained',c,'UNVERIFIABLE','VERIFIED'))
    c=base();c['contract_bytes']=None;c['contract']=None;variants.append(('all_preimages_absent',c,'UNVERIFIABLE','UNVERIFIABLE'))
    c=base();c['contract_bytes']=None;c['contract']['scenario']='other';variants.append(('fallback_parsed_preimage_substituted',c,'UNVERIFIABLE','REFUTED'))
    rows=[]
    for name,c,b,mv in variants:
        before=original.decide(c);changed=m.decide(c);restored=original.decide(c)
        rows.append({'name':name,'input':c,'before':before,'mutant':changed,'restored':restored,'passed':before==restored and before['status']==b and changed['status']==mv})
    out={'original_report':'16 KILLED / 1 SURVIVED remains unchanged','isolated_classification':'KILLED','killed_boundary':'Requirement for exact canonical contract byte carrier. A parsed preimage remains in this witness.','all_preimages_absent':'SURVIVED on preserved original witness; no incorrect authorization','equivalence':'NOT ESTABLISHED. No global equivalence claim.','mutation':{'from':old,'to':new,'sha256':original.sha(mutated.encode())},'rows':rows,'passed':all(r['passed'] for r in rows),'core_unchanged':True}
    print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
