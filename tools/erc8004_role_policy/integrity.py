"""Preserve every historical inventory entry; additions do not reseal old evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '80c91a09095eca362dbfb69d39d0c01fc31130cf'


def check():
    raw = subprocess.check_output(['git', 'show', BASE + ':artifacts.sha256.json'], cwd=ROOT)
    historical = json.loads(raw)['files']
    bad = []
    current = json.loads((ROOT / 'artifacts.sha256.json').read_bytes())['files']
    for name, expected in historical.items():
        p = ROOT / name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            bad.append('historical_bytes:' + name)
        if current.get(name) != expected: bad.append('historical_inventory_entry:' + name)
    lock = json.loads((ROOT / 'conformance/erc8004-pilot-v0/source-lock.json').read_bytes())
    reused = json.loads((ROOT / 'conformance/erc8004-role-policy-v1/source-lock.json').read_bytes())
    for name, expected in reused['reused_files'].items():
        p = ROOT / name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected: bad.append('reused:' + name)
    for kind in ('implementation', 'specification'):
        entry = lock[kind]
        for name, expected in entry.get('files', {entry.get('path'): entry.get('sha256')}).items():
            p = ROOT / 'build/erc8004' / kind / name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected: bad.append('pin:' + name)
    return {'schema': 'erc8004-role-policy.preservation.v1', 'passed': not bad, 'base': BASE,
            'historical_files': len(historical), 'historical_inventory_sha256': hashlib.sha256(raw).hexdigest(),
            'mismatches': sorted(bad)}


if __name__ == '__main__':
    result = check(); print(json.dumps(result, sort_keys=True)); raise SystemExit(not result['passed'])
