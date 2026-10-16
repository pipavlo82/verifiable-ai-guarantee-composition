"""Stage lockfiles under ignored build/; install commands are explicit and separate."""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'build/formal-v1/crypto'
OUT.mkdir(parents=True, exist_ok=True)
for name in ('package.json', 'package-lock.json'):
    shutil.copyfile(HERE / 'crypto' / name, OUT / name)
print('Prepared build/formal-v1/crypto; run npm ci --ignore-scripts there.')
