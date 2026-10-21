import base64,copy,json,unittest
from src.integration import engine as e
from src.integration.cases import base,cases,contract

class IntegrationTests(unittest.TestCase):
    def test_predeclared_scenarios(self):
        for w in cases():
            with self.subTest(w['name']):
                r=e.evaluate(w['case']);self.assertEqual(w['expected'],r['status']);self.assertEqual(r['status']==e.V,r['authorized'])
    def test_forged_authorized(self):
        c=next(w['case'] for w in cases() if w['name']=='self_judgment');r=e.evaluate(c);r['authorized']=True
        self.assertFalse(e.admit(r,c)['authorized'])
    def test_refuted_true(self):
        c=base();r=e.evaluate(c);r.update(status=e.R,authorized=True);self.assertFalse(e.admit(r,c)['authorized'])
    def test_changed_scenario(self):
        c=base();r=e.evaluate(c);r['scenario']='other';self.assertFalse(e.admit(r,c)['authorized'])
    def test_missing_scenario(self):
        c=base();r=e.evaluate(c);r.pop('scenario');self.assertFalse(e.admit(r,c)['authorized'])
    def test_contract_replay(self):
        c=base();r=e.evaluate(c);contract(c,adequacy='Different consumer policy, same scenario');self.assertFalse(e.admit(r,c)['authorized'])
    def test_claim_type_replay(self):
        c=base();r=e.evaluate(c);r['claim_type']='TRANSFER_FUNDS';self.assertFalse(e.admit(r,c)['authorized'])
    def test_modified_verified_scope(self):
        c=base();r=e.evaluate(c);r['verified_scope']['outputHash']='false';self.assertFalse(e.admit(r,c)['authorized'])
    def test_numeric_flag(self):
        c=base();r=e.evaluate(c);r['authorized']=1;self.assertFalse(e.admit(r,c)['authorized'])
    def test_no_preimage(self):
        c=base();r=e.evaluate(c);c['contract_bytes']=None;self.assertEqual(e.U,e.admit(r,c)['status'])
    def test_canonical_order(self):
        c=json.loads(base64.b64decode(base()['contract_bytes']));self.assertEqual(e.canonical(c),e.canonical(dict(reversed(list(c.items())))))
    def test_no_original_branch_changes(self):
        lock=json.loads((e.ROOT/'fixtures/integration/source-lock.json').read_bytes())
        for p,h in lock['frozen_core'].items():self.assertEqual(h,e.sha((e.ROOT/p).read_bytes()),p)
    def test_semantic_validation_not_read_tracking(self):
        # Simulate a predicate that observes a false value but never validates it.
        c=base();c['claim']['outputHash']='false';_ = c['claim']['outputHash']
        self.assertEqual(e.R,e.evaluate(c)['status'])
    def test_nested_unconsumed_fields(self):
        c=base();c['inference']['claim']['unchecked']=True;r=e.evaluate(c)
        self.assertIn('inference.unchecked',r['unconsumed_claim_fields']);self.assertFalse(r['authorized'])
    def test_same_key_controller_is_not_inferred(self):
        c=base();contract(c,controller_policy='INDEPENDENT_REAL_WORLD_CONTROLLERS');self.assertEqual(e.U,e.evaluate(c)['status'])
    def test_positive_roundtrip(self):
        c=base();r=e.evaluate(c);self.assertEqual(e.V,e.admit(json.loads(json.dumps(r)),c)['status'])
if __name__=='__main__':unittest.main()
