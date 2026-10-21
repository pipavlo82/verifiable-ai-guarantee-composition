import unittest
from src.v4.observations import EXAMPLES,non_implications
class ExploratoryObservationTests(unittest.TestCase):
 def test_examples_are_not_crypto_results(self):self.assertTrue(all(e['kind']=='synthetic explanatory descriptor' for e in EXAMPLES))
 def test_not_a_total_order(self):
  rows=non_implications();self.assertTrue(next(x['witness'] for x in rows if x['from']=='DISCRIMINATING' and x['to']=='ATTRIBUTION'));self.assertTrue(next(x['witness'] for x in rows if x['from']=='ATTRIBUTION' and x['to']=='DISCRIMINATING'))
 def test_independence_not_authorship(self):self.assertTrue(next(x['witness'] for x in non_implications() if x['from']=='INDEPENDENT' and x['to']=='ATTRIBUTION'))
 def test_authentication_requires_a_statement_in_this_interpretation(self):self.assertFalse(any(e['ATTRIBUTION'] and not e['DECLARED'] for e in EXAMPLES))
