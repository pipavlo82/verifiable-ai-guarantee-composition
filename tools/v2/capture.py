"""Generate genuine native proof artifacts and observe two actual local file actions.

Not an external service, on-chain action, trained model, or proof of historical execution.
The saved signatures are made only after the observed action; no pre-execution timestamp claim.
"""
import hashlib, json, os, shutil, struct, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CAP=ROOT/'evidence/v2/capture'
def dump(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def native():
    return ROOT/'build/chain-v2/cargo-target/debug'/('composition-native-capture.exe' if os.name=='nt' else 'composition-native-capture')
def main():
    resume='--resume-signatures' in sys.argv
    if CAP.exists() and not resume: raise RuntimeError('Capture directory exists; no overwrite of frozen artifacts')
    if resume and (CAP/'policy.json').exists(): raise RuntimeError('Signed capture is frozen')
    records=[]
    for variant in ('a','b'):
        out=CAP/variant
        if resume:
            records.append({'variant':variant,'prove_exit':0,'verify_exit':0,'proof_bytes':(out/'proof.bin').stat().st_size,'command':['composition-native-capture','prove','input.bin','weights.bin','output.bin','proof.bin','424242'],'verifier_command':['composition-native-capture','verify','input.bin','weights.bin','output.bin','proof.bin']})
            checked=subprocess.run([str(native()),'verify',*[str(out/name) for name in ('input.bin','weights.bin','output.bin','proof.bin')]],capture_output=True)
            if checked.returncode or (out/'delivered.bin').read_bytes()!=(out/'output.bin').read_bytes(): raise RuntimeError('Cannot resume invalid capture')
            continue
        out.mkdir(parents=True)
        values=[(i+1)*(1 if variant=='a' else 3) for i in range(32)]
        weights=[(i%9)+1 for i in range(64)]
        (out/'input.bin').write_bytes(struct.pack('<32Q',*values))
        shutil.copyfile(out/'input.bin',out/'raw-input.bin')
        (out/'weights.bin').write_bytes(struct.pack('<64Q',*weights))
        dump(out/'model.json',{'schema':'public-linear-model-v2','version':1,'operator':'MatMul','shape':[4,8,8],'field':18446744069414584321,'encoding':'canonical-u64-little-endian','weights_sha256':hashlib.sha256((out/'weights.bin').read_bytes()).hexdigest(),'zkie_commit':'39d8df96877bc3bebf33c69b06907d792b3184b9','circuit':'fixed public one-op MatMul, no trained neural model','proof_profile':'VAGCNP2'})
        command=[str(native()),'prove',*[str(out/name) for name in ('input.bin','weights.bin','output.bin','proof.bin')],'424242']
        result=subprocess.run(command,capture_output=True,timeout=120)
        (out/'prove.stdout.log').write_bytes(result.stdout);(out/'prove.stderr.log').write_bytes(result.stderr)
        if result.returncode: raise RuntimeError(result.stderr.decode())
        verify=subprocess.run([*command[:1],'verify',*command[2:6]],capture_output=True,timeout=120)
        (out/'verify.stdout.log').write_bytes(verify.stdout);(out/'verify.stderr.log').write_bytes(verify.stderr)
        if verify.returncode: raise RuntimeError(verify.stderr.decode())
        # Actual authorized local effect, with independently readable bytes and readback.
        with (out/'delivered.bin').open('xb') as target:
            target.write((out/'output.bin').read_bytes()); target.flush(); os.fsync(target.fileno())
        readback=(out/'delivered.bin').read_bytes()
        dump(out/'execution-observation.json',{'schema':'local-observation-v2','executionId':'lab-execution-'+variant,'action':'materialize-matmul-output','result_sha256':hashlib.sha256(readback).hexdigest(),'bytes':len(readback),'observer':'capture.py on the generating host','observation':'exclusive create, write, fsync, reopen and read bytes','independent_historical_execution_proof':False})
        records.append({'variant':variant,'prove_exit':result.returncode,'verify_exit':verify.returncode,'proof_bytes':(out/'proof.bin').stat().st_size,'command':['composition-native-capture','prove','input.bin','weights.bin','output.bin','proof.bin','424242'],'verifier_command':['composition-native-capture','verify','input.bin','weights.bin','output.bin','proof.bin']})
    signed=subprocess.run(['node','tools/v2/sign_capture.mjs'],cwd=ROOT,capture_output=True)
    (CAP/'sign.stdout.log').write_bytes(signed.stdout);(CAP/'sign.stderr.log').write_bytes(signed.stderr)
    if signed.returncode: raise RuntimeError(signed.stderr.decode())
    dump(CAP/'generation.json',{'schema':'actual-laboratory-capture-v2','python':sys.version.split()[0],'node':subprocess.check_output(['node','--version'],text=True).strip(),'rustc':subprocess.check_output(['rustc','--version'],text=True).strip(),'runs':records,'native_binary_sha256':hashlib.sha256(native().read_bytes()).hexdigest(),'external_issuer':False,'chain_observation':None,'historical_execution_independently_verified':False})
    print(json.dumps(records))
if __name__=='__main__':main()
