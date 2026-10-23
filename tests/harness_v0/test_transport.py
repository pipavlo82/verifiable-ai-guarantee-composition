"""Transport controls are infrastructure probes, not another ERC implementation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import agent_harness as h


class Transport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'build')
        self.folder = Path(self.temp.name)
        self.g = h.grader()

    def tearDown(self):
        self.temp.cleanup()

    def grade(self, stdout, code=0, corpus=None):
        script = self.folder / 'probe.py'
        script.write_text('import sys\nsys.stdout.write(' + repr(stdout) + ')\nsys.exit(' + str(code) + ')\n', encoding='utf8', newline='\n')
        import os, shlex
        cmd = [sys.executable, '-B', str(script)]
        command = subprocess.list2cmdline(cmd) if os.name == 'nt' else shlex.join(cmd)
        corpus = corpus if corpus is not None else {'vectors': [{'name': 'probe', 'expected': {'allowed': False}}]}
        return self.g._run_reporter(ROOT, command, 'transport-probe', h.encode(corpus), 'declared.json')

    def test_expectations_are_not_sent(self):
        corpus = {'profile': 'x', 'vectors': [{'name': 'n', 'input': {'claim': 'x'}, 'expected': True, 'obligations': ['secret-oracle']}]}
        before = copy.deepcopy(corpus)
        request = h.detached_request(corpus)
        self.assertEqual(request, {'schema': 'agent-harness.request.v0', 'profile': 'x', 'cases': [{'id': 'n', 'input': {'claim': 'x'}}]})
        self.assertEqual(corpus, before)

    def test_correct_negative_is_conformant(self):
        self.assertTrue(self.grade('{"probe":{"allowed":false}}').ok)

    def test_wrong_value_fails(self):
        r = self.grade('{"probe":{"allowed":true}}'); self.assertFalse(r.ok); self.assertEqual(r.kind, 'SUITE')

    def test_missing_row_never_passes(self):
        self.assertFalse(self.grade('{}').ok)

    def test_extra_row_never_passes(self):
        self.assertFalse(self.grade('{"probe":{"allowed":false},"extra":{}}').ok)

    def test_duplicate_member_never_passes(self):
        self.assertFalse(self.grade('{"probe":{"allowed":false},"probe":{"allowed":false}}').ok)

    def test_crash_is_not_refutation_or_pass(self):
        r = self.grade('crash', 7); self.assertFalse(r.ok); self.assertNotIn(r.kind, self.g.DETERMINATE)

    def test_empty_corpus_never_passes(self):
        self.assertFalse(self.grade('{}', corpus={'vectors': []}).ok)

    def test_empty_output_never_passes(self):
        self.assertFalse(self.grade('').ok)

    def test_missing_adapter_fails_closed(self):
        config = self.folder / 'adapter.json'; h.write(config, {'argv': ['nonexistent-harness-executable-89417']})
        r = h.execute(h.DEFAULT, config, self.folder / 'run')
        self.assertEqual(r['exit_code'], 2); self.assertEqual(r['backend_conformance'], 'NOT_COVERED')

    def test_stale_suite_pin_fails_closed(self):
        h.write(self.folder / 'vectors.json', {'vectors': []})
        h.write(self.folder / 'suite.json', {'vectors': {'path': 'vectors.json', 'sha256': '00' * 32}})
        r = h.execute(self.folder / 'suite.json', h.DEFAULT.parent / 'adapter.json', self.folder / 'run')
        self.assertEqual(r['exit_code'], 2); self.assertIn('pin mismatch', r['error'])

    def test_dependency_tamper_fails_closed(self):
        target = h.CACHE / 'bin/conformance-suite'; original = target.read_bytes()
        try:
            target.write_bytes(original + b'\n# tamper\n')
            with self.assertRaisesRegex(ValueError, 'dependency drift'):
                h.grader()
        finally:
            target.write_bytes(original)

    def test_inconsistent_authorization_is_observable(self):
        row = {'behavior': {}, 'authorization': {'status': 'REFUTED', 'authorized': True, 'scope': None}, 'evidence': {}}
        h.validate_observations({'schema': 'agent-harness.observation.v0', 'observations': {'bad': row}})
        self.assertTrue(row['authorization']['authorized'])


if __name__ == '__main__':
    unittest.main()
