"""Build a pinned adapter against an existing clean zkIE clone; source is never edited.

First run: git clone https://github.com/trustless-ai/zkIE build/chain-v2/zkIE
git -C build/chain-v2/zkIE checkout --detach 39d8df96877bc3bebf33c69b06907d792b3184b9
python tools/v2/prepare.py --online   # fetch pinned Cargo dependencies once
Subsequent replay uses the default --offline --locked Cargo build.
"""
import argparse, hashlib, json, os, platform, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PIN='39d8df96877bc3bebf33c69b06907d792b3184b9'
def main():
    p=argparse.ArgumentParser();p.add_argument('--online',action='store_true');p.add_argument('--cargo-home');args=p.parse_args()
    clone=ROOT/'build/chain-v2/zkIE';out=ROOT/'build/v2/native';out.mkdir(parents=True,exist_ok=True)
    def git(*a):return subprocess.check_output(['git',*a],cwd=clone).decode().strip()
    if git('rev-parse','HEAD')!=PIN or git('status','--porcelain'):raise RuntimeError('Native source must match the clean pin')
    env=dict(os.environ,CARGO_TARGET_DIR=str(ROOT/'build/chain-v2/cargo-target'),CARGO_TERM_COLOR='never')
    if args.cargo_home:env['CARGO_HOME']=str(Path(args.cargo_home).resolve())
    version=subprocess.check_output(['rustc','--version'],text=True).strip()
    if not version.startswith('rustc 1.97.1 '):raise RuntimeError('Pinned Rust 1.97.1 required; observed '+version)
    commands=[['cargo','build','--locked','--manifest-path',str(ROOT/'research/chain-v2/native/Cargo.toml')]]
    for target in ('compose::tests::op_shard_matmul_roundtrip','compose::tests::committed_projection_roundtrip'):
        commands.append(['cargo','test','--locked','--manifest-path',str(clone/'Cargo.toml'),'-p','zkie-ops',target])
    rows=[]
    for index,command in enumerate(commands):
        if not args.online:command+=['--offline']
        if index:command+=['--','--exact','--nocapture']
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,timeout=900)
        for stream in ('stdout','stderr'):(out/f'{index}.{stream}.log').write_bytes(getattr(result,stream))
        rows.append({'command':command,'exit':result.returncode,'executed':True if index==0 else b'1 passed; 0 failed' in result.stdout,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()})
    report={'schema':'native-v2-build','pin':PIN,'rustc':version,'cargo':subprocess.check_output(['cargo','--version'],text=True).strip(),'platform':platform.platform(),'python':sys.version.split()[0],'runs':rows,'source_clean':not git('status','--porcelain'),'adapter_lock_sha256':hashlib.sha256((ROOT/'research/chain-v2/native/Cargo.lock').read_bytes()).hexdigest()}
    report['passed']=report['source_clean'] and all(r['exit']==0 and r['executed'] for r in rows)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
