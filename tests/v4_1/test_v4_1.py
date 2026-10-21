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
    def _evidence(self,src):return self.by[src]['case'] if isinstance(src,str) else src
    def test_reuse_admission(self):
        for name,src,edit,contract,claim_type,expected in reuse_cases():
            evidence=self._evidence(src);res=copy.deepcopy(self.results[src] if isinstance(src,str) else evaluate(src))
            if edit is None:
                with self.subTest(name):self.assertTrue(res['C']['authorized'])
            presented=edit(res) if edit else res
            with self.subTest(name):self.assertEqual(admit(presented,evidence,contract,claim_type),expected)
    def test_forged_binding_not_admitted(self):
        # A result whose binding was edited to the consumer's claim type is still refused.
        res=copy.deepcopy(self.results['positive_replay']);res['C']['binding']['claim_type']=OUTPUT['claim_type']
        self.assertFalse(admit(res,self.by['positive_replay']['case'],OUTPUT,OUTPUT['claim_type']))
    def test_unauthorized_never_admitted(self):
        r=self.results['negative_O14_self_judged'];c=self.by['negative_O14_self_judged']['case']
        self.assertFalse(admit(r,c,c['contract'],OUTPUT['claim_type']))
    def test_F1_authorized_flag_alone_not_admitted(self):
        # Only C.authorized edited; C.status and O14 stay REFUTED. Before v4.1 review fixes this was admitted.
        r=copy.deepcopy(self.results['negative_O14_self_judged']);c=self.by['negative_O14_self_judged']['case']
        self.assertEqual(r['C']['status'],R);self.assertEqual(r['verification']['O14'],R);r['C']['authorized']=True
        self.assertFalse(admit(r,c,c['contract'],OUTPUT['claim_type']))
    def test_F2_scenario_edit_not_admitted(self):
        for edit in ('drop','other'):
            r=copy.deepcopy(self.results['positive_output']);c=self.by['positive_output']['case']
            if edit=='drop':r['C']['binding'].pop('scenario')
            else:r['C']['binding']['scenario']='LAB_SOME_OTHER_SCENARIO'
            with self.subTest(edit):self.assertFalse(admit(r,c,OUTPUT,OUTPUT['claim_type']))
    def test_scenario_count(self):
        self.assertEqual(len(self.rows),57);self.assertEqual(sum(r['origin']=='v4.1' for r in self.rows),3)
    def test_repeat_evaluation(self):
        c=self.by['positive_output']['case'];f=facts(c);self.assertEqual(evaluate(c,f),evaluate(c,f))
if __name__=='__main__':unittest.main()
