"""Crashes/noncoverage cannot masquerade as a successful mutation witness."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/harness_v0'))
from review_controls import classify


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {'exit_code': 0}
        self.mutant = {'exit_code': 1, 'adapter_exit_code': 0, 'rows': [
            {'id': 'permitted_review', 'backend_conformance': 'PASS'},
            {'id': 'witness', 'backend_conformance': 'FAIL',
             'observed_behavior': {'authorization': {'authorized': True}}}]}

    def result(self):
        return classify(self.baseline, self.mutant, {'exit_code': 0}, 'witness')

    def test_distinguishing_authorization(self):
        self.assertEqual(self.result(), 'KILLED')

    def test_adapter_crash_is_not_killed(self):
        self.mutant['adapter_exit_code'] = 1
        self.assertEqual(self.result(), 'CRASHED')

    def test_unavailable_suite_is_not_killed(self):
        self.mutant['exit_code'] = 2
        self.assertEqual(self.result(), 'UNVERIFIABLE')

    def test_broken_positive_is_not_killed(self):
        self.mutant['rows'][0]['backend_conformance'] = 'FAIL'
        self.assertEqual(self.result(), 'SURVIVED')

    def test_failed_baseline_is_not_killed(self):
        self.baseline['exit_code'] = 1
        self.assertEqual(self.result(), 'UNVERIFIABLE')

    def test_restoration_failure_is_not_killed(self):
        self.assertEqual(classify(self.baseline, self.mutant, {'exit_code': 1}, 'witness'), 'UNVERIFIABLE')

    def test_missing_witness_is_not_killed(self):
        self.mutant['rows'].pop()
        self.assertEqual(self.result(), 'SURVIVED')

    def test_mismatch_without_authorization_is_not_killed(self):
        self.mutant['rows'][1]['observed_behavior']['authorization']['authorized'] = False
        self.assertEqual(self.result(), 'SURVIVED')


if __name__ == '__main__':
    unittest.main()
