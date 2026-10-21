"""Exact PR5 edits with targeted witnesses, avoiding unrelated case evaluations."""
import copy,importlib.util,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v4_1 import model as baseline
from src.v4_1 import scenarios
def main():
    s=importlib.util.spec_from_file_location('specs',ROOT/'tools/v4_1/mutations.py');specs=importlib.util.module_from_spec(s);s.loader.exec_module(specs)
    source=(ROOT/'src/v4_1/model.py').read_bytes();catalog=(ROOT/'fixtures/v4_1/catalog.json').read_bytes();rows=[]
    def trial(m,name,deleted=False):
        saved=scenarios.CATALOG
        try:
            if deleted:scenarios.CATALOG={k:v for k,v in saved.items() if k!='O14'}
            by={r['name']:r['case'] for r in scenarios.cases()}
            if name in by:return m.evaluate(by[name])['C']['authorized']
            row=next(r for r in scenarios.reuse_cases() if r[0]==name);_,src,edit,ct,kind,_=row;c=by[src] if isinstance(src,str) else src
            r=m.evaluate(c);r=edit(copy.deepcopy(r)) if edit else r;return m.admit(r,c,ct,kind)
        finally:scenarios.CATALOG=saved
    for mid,kind,old,new,w,positive in specs.MUTATIONS:
        try:
            if kind=='catalog':m=baseline;deleted=True
            else:
                if source.decode().count(old)!=1:rows.append({'id':mid,'classification':'NOT_APPLIED'});continue
                m=types.ModuleType('targeted_'+mid);m.__file__=str(ROOT/'src/v4_1/model.py');exec(compile(source.decode().replace(old,new),m.__file__,'exec'),m.__dict__);deleted=False
            b=trial(baseline,w);pb=trial(baseline,positive);v=trial(m,w,deleted);pv=trial(m,positive,deleted);r=trial(baseline,w);pr=trial(baseline,positive)
            controls=b is False and r is False and pb is True and pr is True
            killed=controls and (v is False and pv is False if deleted else v is True and pv is True)
            rows.append({'id':mid,'kind':kind,'witness':w,'before':b,'positive_before':pb,'mutant':v,'positive_mutant':pv,'restored':r,'positive_restored':pr,'classification':'KILLED' if killed else 'SURVIVED' if controls else 'UNVERIFIABLE'})
        except Exception as ex:rows.append({'id':mid,'classification':'CRASHED','error':type(ex).__name__+': '+str(ex)})
    report={'mutations':rows,'counts':{k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'unique_edits':len({(x[1],x[2],x[3]) for x in specs.MUTATIONS}),'unchanged':(ROOT/'src/v4_1/model.py').read_bytes()==source and (ROOT/'fixtures/v4_1/catalog.json').read_bytes()==catalog,'passed':len(rows)==9 and all(r['classification']=='KILLED' for r in rows)}
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
