"""Behavioral source mutants. Exceptions are CRASHED, never automatically KILLED."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(dependency_root, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    original = (ROOT / 'model.py').read_text(encoding='utf-8')
    baseline = {'__name__': 'baseline'}
    exec(compile(original, 'baseline', 'exec'), baseline)
    left = {'algorithm': 'sha256', 'representation': 'raw', 'digest': 'a' * 64}
    right = dict(left, representation='normalized')
    rows = []
    changes = [
        ('closure', 'return all(groups[left] == groups[right] for left, right in TARGETS)', 'return True'),
        ('representation', 'if (left["algorithm"], left["representation"]) != (right["algorithm"], right["representation"]):', 'if False:')]
    for name, old, new in changes:
        row = {'name': name, 'classification': 'NOT_APPLIED'}
        if original.count(old) == 1:
            try:
                ns = {'__name__': 'mutant'}
                exec(compile(original.replace(old, new), 'mutant-' + name, 'exec'), ns)
                if name == 'closure':
                    before, after = baseline['entails']([]), ns['entails']([])
                    positive = ns['entails'](ns['EDGES'])
                    killed = before is False and after is True and positive is True
                else:
                    before, after = baseline['compare_commitments'](left, right), ns['compare_commitments'](left, right)
                    positive = ns['compare_commitments'](left, left)
                    killed = before == 'UNVERIFIABLE' and after == positive == 'VERIFIED'
                row.update(before=before, after=after, positive_control=positive, classification='KILLED' if killed else 'SURVIVED')
            except Exception as error:
                row.update(classification='CRASHED', error=type(error).__name__)
        rows.append(row)
    script = (ROOT / 'crypto/check.mjs').read_text(encoding='utf-8')
    (scratch / 'ledger-19-event.json').write_bytes((ROOT / 'crypto/ledger-19-event.json').read_bytes())
    replacements = [
        ('signature_verification', "return schnorr.verify(Buffer.from(e.sig, 'hex'), Buffer.from(id, 'hex'), Buffer.from(e.pubkey, 'hex')) ? 'VERIFIED' : 'REFUTED';", "return 'VERIFIED';", 'changed_signature'),
        ('proposal_binding', "return content.artifact_hash === requestedDigest ? 'VERIFIED' : 'REFUTED';", "return 'VERIFIED';", 'wrong_proposal_same_authentic_event')]
    for name, old, new, target in replacements:
        row = {'name': name, 'classification': 'NOT_APPLIED', 'target': target}
        if script.count(old) == 1:
            try:
                path = scratch / (name + '.mjs')
                path.write_text(script.replace(old, new), encoding='utf-8', newline='\n')
                proc = subprocess.run(['node', str(path), str(Path(dependency_root).resolve())], capture_output=True, timeout=30)
                (scratch / (name + '.stdout.json')).write_bytes(proc.stdout)
                (scratch / (name + '.stderr.log')).write_bytes(proc.stderr)
                if proc.returncode not in (0, 1):
                    raise RuntimeError('Mutation process failed')
                report = json.loads(proc.stdout)
                observed = {r['name']: r for r in report['cases']}
                killed = observed[target]['actual'] == 'VERIFIED' and not observed[target]['passed'] and observed['original_signature']['passed']
                row.update(before='REFUTED', after=observed[target]['actual'], positive_control=observed['original_signature']['actual'],
                           classification='KILLED' if killed else 'SURVIVED', exit=proc.returncode,
                           output_sha256=hashlib.sha256(proc.stdout).hexdigest())
            except Exception as error:
                row.update(classification='CRASHED', error=type(error).__name__)
        rows.append(row)
    # Restore is literal: originals were never changed. Confirm behavior once more.
    restored = (ROOT / 'model.py').read_text(encoding='utf-8') == original and (ROOT / 'crypto/check.mjs').read_text(encoding='utf-8') == script
    restored = restored and baseline['entails']([]) is False and baseline['compare_commitments'](left, right) == 'UNVERIFIABLE'
    p = subprocess.run(['node', str(ROOT / 'crypto/check.mjs'), str(Path(dependency_root).resolve())], capture_output=True, timeout=30)
    restored = restored and p.returncode == 0 and json.loads(p.stdout)['passed']
    counts = {key: sum(r['classification'] == key for r in rows) for key in ('KILLED', 'SURVIVED', 'CRASHED', 'NOT_APPLIED', 'UNVERIFIABLE')}
    return {'schema': 'formal-v1-mutations', 'controls': rows, 'counts': counts, 'restored': restored,
            'passed': restored and counts['KILLED'] == 4,
            'scope': 'Four implementation controls; 252 abstract removal countermodels are separate, not counted as source mutants.'}
