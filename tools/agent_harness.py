"""Thin, expectation-free transport to the pinned recompute-kit reporter grader.

This module does not verify ERC evidence or issue authorization credentials.
Commands/configuration are trusted local code, not a sandbox for hostile adapters.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'conformance/agent-harness-v0/source-lock.json'
DEFAULT = ROOT / 'conformance/agent-harness-v0/erc8404/suite.json'
CACHE = ROOT / 'build/agent-harness-v0/recompute-kit'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def prepare(source=None):
    lock = json.loads(LOCK.read_bytes())['recompute-kit']
    for name, digest in lock['runtime_files'].items():
        dest = CACHE / name
        if dest.is_file() and sha(dest.read_bytes()) == digest:
            continue
        if source:
            data = (Path(source) / name).read_bytes()
        else:
            url = f"https://raw.githubusercontent.com/{lock['repository']}/{lock['commit']}/{name}"
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
        if sha(data) != digest:
            raise ValueError('dependency digest mismatch: ' + name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)


def grader():
    lock = json.loads(LOCK.read_bytes())['recompute-kit']
    for name, digest in lock['runtime_files'].items():
        if sha((CACHE / name).read_bytes()) != digest:
            raise ValueError('dependency drift: ' + name)
    spec = importlib.util.spec_from_file_location('pinned_recompute_runner', CACHE / 'tools/run_conformance.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def detached_request(corpus):
    return {'schema': 'agent-harness.request.v0', 'profile': corpus['profile'],
            'cases': [{'id': v['name'], 'input': v['input']} for v in corpus['vectors']]}


def validate_observations(data):
    if not isinstance(data, dict) or set(data) != {'schema', 'observations'} or data['schema'] != 'agent-harness.observation.v0':
        raise ValueError('observation envelope')
    if not isinstance(data['observations'], dict):
        raise ValueError('observation map')
    for name, row in data['observations'].items():
        if not isinstance(row, dict) or set(row) != {'behavior', 'authorization', 'evidence'}:
            raise ValueError('observation row: ' + name)
        auth = row['authorization']
        if not isinstance(row['behavior'], dict) or not isinstance(row['evidence'], dict):
            raise ValueError('behavior/evidence maps')
        if not isinstance(auth, dict) or set(auth) != {'status', 'authorized', 'scope'}:
            raise ValueError('authorization shape')
        if auth['status'] not in ('VERIFIED', 'REFUTED', 'UNVERIFIABLE') or type(auth['authorized']) is not bool:
            raise ValueError('authorization types')
        if auth['scope'] is not None and not isinstance(auth['scope'], dict):
            raise ValueError('authorization scope type')
        # Inconsistent status/flag/scope is observable behavior to grade, not repaired here.


def execute(suite_path, adapter_path, out, target_root=None):
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {'schema': 'agent-harness.report.v0', 'backend_conformance': 'NOT_COVERED',
              'authorization_credential': False, 'rows': [], 'exit_code': 2}
    try:
        g = grader()
        suite_path = Path(suite_path).resolve()
        suite = g._strict_json(suite_path.read_bytes(), 'SUITE')
        def pinned(entry):
            path = (suite_path.parent / entry['path']).resolve()
            raw = path.read_bytes()
            if sha(raw) != entry['sha256']:
                raise ValueError('suite pin mismatch: ' + entry['path'])
            return g._strict_json(raw, entry['path'])
        corpus = pinned(suite['vectors'])
        obligations = pinned(suite['obligations'])
        g._reporter_corpus(encode(corpus))
        for v in corpus['vectors']:
            if not v['obligations'] or any(k not in obligations for k in v['obligations']):
                raise ValueError('undefined semantic obligation')
        config = g._strict_json(Path(adapter_path).read_bytes(), 'ADAPTER')
        substitutions = {'{python}': sys.executable, '{repo}': str(ROOT),
                         '{implementation}': str(Path(target_root or ROOT).resolve())}
        argv = config['argv']
        if not isinstance(argv, list) or not argv or any(not isinstance(a, str) for a in argv):
            raise ValueError('adapter argv must be nonempty strings')
        argv = [substitute(a, substitutions) for a in argv]
        if sys.flags.optimize and argv[0] == sys.executable:
            argv.insert(1, '-O')
        request = detached_request(corpus)
        raw_request = encode(request)
        (out / 'request.json').write_bytes(raw_request)
        report.update(suite_sha256=sha(suite_path.read_bytes()),
                      vectors_sha256=suite['vectors']['sha256'],
                      adapter_config_sha256=sha(Path(adapter_path).read_bytes()),
                      request_sha256=sha(raw_request), adapter_argv=argv)
        proc = subprocess.run(argv, input=raw_request, capture_output=True, cwd=ROOT, timeout=180, shell=False)
        (out / 'adapter.stdout').write_bytes(proc.stdout)
        (out / 'adapter.stderr').write_bytes(proc.stderr)
        report['adapter_exit_code'] = proc.returncode
        if proc.returncode:
            report['backend_conformance'] = 'UNVERIFIABLE'
            raise ValueError('adapter exited without a completed observation: ' + str(proc.returncode))
        data = g._strict_json(proc.stdout, 'ADAPTER_OUTPUT')
        validate_observations(data)
        projected = {name: {'behavior': row['behavior'], 'authorization': row['authorization']}
                     for name, row in data['observations'].items()}
        write(out / 'projected.json', projected)
        # The unchanged upstream runner grades this captured report, not another execution.
        cmd = [sys.executable, '-B', str(ROOT / 'tools/harness_v0/replay.py'), str(out / 'projected.json')]
        command = subprocess.list2cmdline(cmd) if os.name == 'nt' else shlex.join(cmd)
        result = g._run_reporter(ROOT, command, suite['id'], encode(corpus), suite['vectors']['path'])
        code = 0 if result.ok else 1 if result.kind in g.DETERMINATE else 2
        report.update(backend_conformance='PASS' if result.ok else 'FAIL' if code == 1 else 'UNVERIFIABLE',
                      exit_code=code, grader={'kind': result.kind, 'detail': result.detail},
                      observation_sha256=sha(proc.stdout))
        canon = g._grader_canon()
        for v in corpus['vectors']:
            observed = projected.get(v['name'])
            report['rows'].append({
                'id': v['name'],
                'requirements': {k: obligations[k] for k in v['obligations']},
                'expected_behavior': v['expected'], 'observed_behavior': observed,
                'backend_conformance': 'UNVERIFIABLE' if v['name'] not in projected else
                    'PASS' if canon(observed) == canon(v['expected']) else 'FAIL',
                'evidence_supported_authorization': observed['authorization'] if observed else None,
                'evidence': data['observations'].get(v['name'], {}).get('evidence', {})})
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['exit_code'] = 2
        if report['backend_conformance'] == 'PASS':
            report['backend_conformance'] = 'UNVERIFIABLE'
    write(out / 'report.json', report)
    return report


def substitute(value, replacements):
    for token, replacement in replacements.items():
        value = value.replace(token, replacement)
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('--source')
    run = sub.add_parser('run')
    run.add_argument('--suite', type=Path, default=DEFAULT)
    run.add_argument('--adapter', type=Path, default=DEFAULT.parent / 'adapter.json')
    run.add_argument('--out', type=Path, default=ROOT / 'build/agent-harness-v0/run')
    run.add_argument('--implementation-root', type=Path)
    args = p.parse_args()
    if args.command == 'prepare':
        prepare(args.source); grader(); print('Pinned recompute-kit ready'); return 0
    report = execute(args.suite, args.adapter, args.out, args.implementation_root)
    print(json.dumps({k: report[k] for k in ('backend_conformance', 'exit_code')}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
