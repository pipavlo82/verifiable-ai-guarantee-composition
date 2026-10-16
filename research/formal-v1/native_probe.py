"""Run two pinned native zkIE library tests; no portable proof or authorization claim."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

PIN = '39d8df96877bc3bebf33c69b06907d792b3184b9'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--zkie-clone', required=True)
    p.add_argument('--cache-dir', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--online', action='store_true', help='Allow Cargo to fetch pinned dependencies; default offline')
    args = p.parse_args()
    clone, cache, out = (Path(v).resolve() for v in (args.zkie_clone, args.cache_dir, args.out))
    out.mkdir(parents=True, exist_ok=True)
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=clone, text=True).strip() != PIN:
        raise RuntimeError('Unexpected zkIE commit')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=clone):
        raise RuntimeError('Use a clean upstream checkout')
    env = dict(os.environ, CARGO_TARGET_DIR=str(cache / 'cargo-target'), CARGO_HOME=str(cache / 'cargo-home'), CARGO_TERM_COLOR='never')
    rows = []
    for target in ('compose::tests::op_shard_matmul_roundtrip', 'compose::tests::committed_projection_roundtrip'):
        command = ['cargo', 'test', '--locked', '-p', 'zkie-ops', target]
        if not args.online:
            command.append('--offline')
        command += ['--', '--exact', '--nocapture']
        result = subprocess.run(command, cwd=clone, env=env, capture_output=True, timeout=900)
        name = target.split('::')[-1]
        for stream in ('stdout', 'stderr'):
            (out / (name + '.' + stream + '.log')).write_bytes(getattr(result, stream))
        rows.append({'target': target, 'exit': result.returncode, 'executed': b'1 passed; 0 failed' in result.stdout,
                     'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()})
    clean = not subprocess.check_output(['git', 'status', '--porcelain'], cwd=clone)
    report = {'pin': PIN, 'cargo_lock_sha256': hashlib.sha256((clone / 'Cargo.lock').read_bytes()).hexdigest(),
              'rustc': subprocess.check_output(['rustc', '--version'], text=True).strip(),
              'cargo': subprocess.check_output(['cargo', '--version'], text=True).strip(),
              'runs': rows, 'clean_upstream': clean, 'passed': clean and all(r['exit'] == 0 and r['executed'] for r in rows),
              'portable_proof_capture': 'NOT_IMPLEMENTED', 'end_to_end_authorization': 'NOT_IMPLEMENTED'}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
