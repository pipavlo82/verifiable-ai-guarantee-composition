import copy,json,unittest
from pathlib import Path
from validate import comparison_semantics

class DeterminismContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[2]
  cls.report=json.loads((root/'evidence/escrow-v0/validation/comparison-normal.stdout.log').read_bytes())
 def test_measured_gas_is_retained_without_changing_claim_semantics(self):
  changed=copy.deepcopy(self.report);changed['rows'][0]['release_call_gas']+=1
  self.assertNotEqual(changed,self.report)
  self.assertEqual(comparison_semantics(changed),comparison_semantics(self.report))
 def test_authorization_change_is_detected(self):
  changed=copy.deepcopy(self.report);changed['rows'][0]['modes']['C']=False
  self.assertNotEqual(comparison_semantics(changed),comparison_semantics(self.report))
 def test_payment_delta_change_is_detected(self):
  changed=copy.deepcopy(self.report);changed['rows'][0]['observed_recipient_delta']=0
  self.assertNotEqual(comparison_semantics(changed),comparison_semantics(self.report))
 def test_counts_classifications_and_unknown_fields_remain_checked(self):
  for mutate in (lambda r:r['comparison']['C'].update(false_authorizations=999),lambda r:r['rows'][0].update(offchain='REFUTED'),lambda r:r['rows'][0].update(unexpected='must not disappear')):
   changed=copy.deepcopy(self.report);mutate(changed)
   self.assertNotEqual(comparison_semantics(changed),comparison_semantics(self.report))
if __name__=='__main__':unittest.main()
