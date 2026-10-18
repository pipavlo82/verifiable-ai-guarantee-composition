import copy,json,unittest
from src.v4.model import V,R,U
from src.v4 import model as v4model
from src.v4_1.model import evaluate,facts,admit,contract_digest
from src.v4_1.scenarios import cases,reuse_cases,weak_output,OUTPUT

class V41Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=cases();cls.by={r['name']:r for r in cls.rows};cls.results={r['name']:evaluate(r['case']) for r in cls.rows}
    def test_fixed_oracles(self):
        for r in self.rows:
            with self.subTest(r['name']):
                self.assertEqual(self.results[r['name']]['C']['status'],r['expected'])
                for m in ('A','B'):
                    if r['expected_'+m] is not None:self.assertEqual(self.results[r['name']][m]['status'],r['expected_'+m])
    def test_all_v4_rows_carried(self):
        self.assertEqual(sum(r['origin']=='v4' for r in self.rows),54)
    def test_self_judged_isolated_to_O14(self):
        r=self.results['negative_O14_self_judged']
        self.assertEqual({o:s for o,s in r['verification'].items() if s!=V},{'O14':R});self.assertTrue(r['A']['authorized'])
    def test_v4_authorizes_self_judged(self):
        self.assertTrue(v4model.evaluate(weak_output())['C']['authorized'])
    def test_omitted_O14_coverage_alarm(self):
        r=self.results['omitted_O14'];self.assertTrue(r['all_declared_pass']);self.assertEqual(r['missing_obligations'],['O14']);self.assertEqual(r['C']['status'],R)
    def test_unconsumed_output_under_replay(self):
        r=self.results['unconsumed_output_under_replay']
        self.assertTrue(r['all_declared_pass']);self.assertEqual(r['unconsumed_claim_fields'],['outputHash']);self.assertEqual(r['claim_fields'],R);self.assertFalse(r['C']['authorized'])
        self.assertTrue(v4model.evaluate(self.by['unconsumed_output_under_replay']['case'])['C']['authorized'])
    def test_positives_consume_every_claim_field(self):
        for r in self.rows:
            if r['kind']=='positive':
                with self.subTest(r['name']):self.assertEqual(self.results[r['name']]['unconsumed_claim_fields'],[])
    def test_binding_recomputed_from_contract(self):
        for r in self.rows:
            res=self.results[r['name']];c=r['case']['contract']
            with self.subTest(r['name']):
                if c is None:self.assertIsNone(res['C']['binding'])
                else:self.assertEqual(res['C']['binding'],{'scenario':c['scenario'],'claim_type':c['claim_type'],'contract_sha256':contract_digest(c)})
    def test_binding_not_taken_from_claim(self):
        c=copy.deepcopy(self.by['positive_output']['case']);c['claim']['contract_sha256']='00'*32
        r=evaluate(c);self.assertNotEqual(r['C']['binding']['contract_sha256'],'00'*32);self.assertIn('contract_sha256',r['unconsumed_claim_fields']);self.assertFalse(r['C']['authorized'])
    def test_reuse_admission(self):
        for name,src,contract,claim_type,expected in reuse_cases():
            res=self.results[src] if isinstance(src,str) else evaluate(src)
            with self.subTest(name):self.assertTrue(res['C']['authorized']);self.assertEqual(admit(res,contract,claim_type),expected)
    def test_forged_binding_not_admitted(self):
        # A result whose binding was edited to the consumer's claim type is still refused: the digest is recomputed.
        res=copy.deepcopy(self.results['positive_replay']);res['C']['binding']['claim_type']=OUTPUT['claim_type']
        self.assertFalse(admit(res,OUTPUT,OUTPUT['claim_type']))
    def test_unauthorized_never_admitted(self):
        r=self.results['negative_O14_self_judged'];self.assertFalse(admit(r,self.by['negative_O14_self_judged']['case']['contract'],OUTPUT['claim_type']))
    def test_repeat_evaluation(self):
        c=self.by['positive_output']['case'];f=facts(c);self.assertEqual(evaluate(c,f),evaluate(c,f))
if __name__=='__main__':unittest.main()
