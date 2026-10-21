import copy,json,os,unittest
from pathlib import Path
import adapter as a
from vectors import make,SCENARIOS
class AdapterTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  folder=os.environ.get('LAB_VECTOR_DIR');cls.v={n:json.loads((Path(folder)/(n+'-offchain.json')).read_bytes()) if folder else make(n) for n in SCENARIOS}
 def test_declared_expected_outcomes(self):
  accepted={'positive','expired_after_signing','revoked_after_signing','false_returning_token','lying_token'}
  unavailable={'L_no_contract','missing_profile'}
  for n,v in self.v.items():
   with self.subTest(n=n):self.assertEqual(v['adapter']['status'],a.V if n in accepted else a.U if n in unavailable else a.R)
 def test_nonce_reservation_is_load_bearing(self):
  v=self.v['positive'];j=set();self.assertTrue(a.reserve(v['adapter'],'7',j));self.assertFalse(a.reserve(v['adapter'],'7',j))
 def test_valid_signature_does_not_validate_scope(self):
  v=self.v['A_wrong_scope'];self.assertTrue(v['component_signature_valid']);self.assertFalse(v['adapter']['authorized'])
 def test_digest_preimage_is_recomputed(self):
  v=self.v['positive'];other=a.laboratory_sign(bytes(32));self.assertEqual(a.verify_verdict(other,v['grant']),a.V);self.assertEqual(a.verify_bound_verdict(other,bytes.fromhex(v['request_bytes']),v['grant'],v['record']),a.R)
 def test_o14_uses_real_self_signed_evidence(self):
  v=self.v['N_self_judgment'];f=a.engine.inference.facts(v['case']['inference']);self.assertEqual(f['signatures']['provenance']['status'],a.V);self.assertEqual(f['signatures']['judgment']['status'],a.V);self.assertEqual(f['signatures']['provenance']['signer'],f['signatures']['judgment']['signer']);self.assertEqual(a.engine.evaluate(v['case'])['checks']['J07'],a.R);self.assertFalse(v['adapter']['authorized'])
 def test_positive_replays_native_proof(self):
  v=self.v['positive'];self.assertTrue(v['adapter']['authorized']);self.assertEqual(a.engine.inference.facts(v['case']['inference'])['native']['status'],a.V)
 def test_canonical_request_and_amount_types(self):
  v=self.v['positive'];kw=[v['case'],v['record'],b' '+bytes.fromhex(v['request_bytes']),v['grant'],v['snapshot'],v['now'],set(),a.profile_bytes()];self.assertEqual(a.assess(*kw)['status'],a.R)
 def test_signature_scalar_controls(self):
  for n in ('high_s','negated_s','invalid_signature'):self.assertFalse(self.v[n]['component_signature_valid'])
 def test_expiry_is_not_part_of_the_onchain_tuple(self):
  v=self.v['positive'];r=v['request'];d=a.digest(r['chain_id'],r['escrow_contract'],r['payment_id'],r['nonce'],1,v['snapshot']['request_sha256'],v['snapshot']['policy_sha256'],True,v['decision_ref']);self.assertEqual(d.hex(),v['verdict']['digest'])
if __name__=='__main__':unittest.main()
