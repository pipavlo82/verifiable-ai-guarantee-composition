"""Physical PR5 source-copy mutation: reading a field is not validating it."""
import copy,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from src.v4_1 import model as original
from src.integration import engine as joint
from src.integration.cases import base
source=(ROOT/'src/v4_1/model.py').read_bytes();old="    funcs['checker_independence']=lambda:independence(f)"
new=old+"\n    funcs['attestation_signature']=lambda:(claim.get('unchecked'),f['signatures'].get('provenance',{}).get('status',U))[1]"
def main():
    if source.decode().count(old)!=1:raise RuntimeError('NOT_APPLIED')
    m=types.ModuleType('read_without_check');m.__file__=str(ROOT/'src/v4_1/model.py');mutated=source.decode().replace(old,new);exec(compile(mutated,m.__file__,'exec'),m.__dict__)
    c=base();c['inference']['claim']['unchecked']='unsupported statement';b=original.evaluate(c['inference']);v=m.evaluate(c['inference'])
    before=joint.evaluate(c);saved=joint.inference
    try:joint.inference=m;protected=joint.evaluate(c)
    finally:joint.inference=saved
    restored=joint.evaluate(c)
    report={'mutation':{'from':old,'to':new,'sha256':joint.sha(mutated.encode())},'pr5_before':b,'pr5_mutant':v,'integration_before':before,'integration_under_pr5_mutant':protected,'integration_restored':restored,
      'classification':'KILLED_BY_ISOLATED_NEGATIVE_WITNESS','result':'PR5 read tracking marks a discarded read consumed. External integration rejects the explicitly unconsumed nested claim field.',
      'passed':not b['C']['authorized'] and v['C']['authorized'] and not protected['authorized'] and before==restored and 'inference.unchecked' in protected['unconsumed_claim_fields'] and (ROOT/'src/v4_1/model.py').read_bytes()==source}
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
