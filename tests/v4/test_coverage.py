import copy,json,unittest
from src.v4.model import ROOT,load,evaluate,facts,V,R,U,combine
from src.v4.scenarios import cases,base

class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=cases();cls.results={r['name']:evaluate(r['case']) for r in cls.rows}
    def test_fixed_oracles(self):
        for r in self.rows:
            with self.subTest(r['name']):self.assertEqual(self.results[r['name']]['C']['status'],r['expected'])
    def test_positive_witnesses(self):
        self.assertEqual(sum(r['kind']=='positive' for r in self.rows),4)
        for r in self.rows:
            if r['kind']=='positive':self.assertTrue(self.results[r['name']]['C']['authorized'])
    def test_every_boundary_is_isolated(self):
        for i in range(1,14):
            k=f'O{i:02}';r=self.results['negative_'+k]
            self.assertEqual({o:s for o,s in r['verification'].items() if s!=V},{k:U if k=='O10' else R})
    def test_omission_all_declared_pass(self):
        for i in range(1,14):
            k=f'O{i:02}';r=self.results['omitted_'+k]
            self.assertTrue(r['all_declared_pass']);self.assertNotIn(k,r['executed']);self.assertEqual(r['missing_obligations'],[k]);self.assertEqual(r['C']['status'],R)
    def test_missing_evidence_never_verified(self):
        for r in self.rows:
            if r['kind']=='missing':self.assertEqual(self.results[r['name']]['C']['status'],U)
    def test_same_evidence_baseline_expected(self):
        for r in self.rows:
            for mode in ('A','B'):
                if r['expected_'+mode] is not None:self.assertEqual(self.results[r['name']][mode]['status'],r['expected_'+mode])
    def test_no_implementation_inventory_oracle(self):
        r=self.results['circular_self_inventory'];self.assertTrue(r['B']['authorized']);self.assertFalse(r['C']['authorized'])
    def test_no_scope_amplification(self):
        r=self.results['scope_overclaim'];self.assertTrue(r['all_declared_pass']);self.assertEqual(r['composition'],R)
    def test_definition_identity_is_not_name_only(self):
        r=self.results['counterfeit_definition'];self.assertTrue(r['all_declared_pass']);self.assertEqual(r['coverage']['definitions'],R)
    def test_scenario_revision_required(self):self.assertEqual(self.results['stale_scenario']['coverage']['context'],R)
    def test_raw_missing_authentication_survives_only_narrow_claim(self):
        self.assertEqual(self.results['positive_attestation']['C']['status'],V)
        self.assertEqual(self.results['missing_O03']['C']['status'],U)
    def test_mixed_preserves_refutation_and_unknown(self):
        r=self.results['mixed_refutation_missing'];self.assertEqual(r['C']['status'],R);self.assertIn(U,r['verification'].values())
    def test_signature_does_not_authorize_foreign_key(self):
        r=self.results['negative_O08'];self.assertTrue(r['A']['authorized']);self.assertEqual(r['verification']['O08'],R)
    def test_no_external_execution_claim(self):
        for r in self.results.values():self.assertEqual(r['chain_status'],'PARTIAL_CHAIN_VERIFIED')
    def test_catalog_typed_fields(self):
        expected={'obligation_id','claim_type','subject','scope','authority','evidence_requirements','verification_procedure','dependencies','applicable_policy','source_specification','source_version','coverage_justification','failure_classification'}
        for k,v in load(ROOT/'fixtures/v4/catalog.json').items():self.assertEqual(set(v),expected);self.assertEqual(v['obligation_id'],k);self.assertIsInstance(v['dependencies'],list)
    def test_contracts_do_not_read_implementation_inventory(self):
        c=base();f=facts(c);c['catalog'].clear();r=evaluate(c,f);self.assertEqual(len(r['required']),13);self.assertEqual(len(r['missing_obligations']),13)
    def test_undeclared_future_requirement(self):self.assertEqual(self.results['unknown_required_obligation']['C']['status'],U)
    def test_contract_dependency_closure(self):self.assertEqual(self.results['unclosed_dependencies']['coverage']['dependency_closure'],R)
    def test_repeat_evidence_evaluation(self):
        c=base();f=facts(c);self.assertEqual(evaluate(c,f),evaluate(c,f))
    def test_three_state_algebra(self):
        self.assertEqual(combine([R,U]),R);self.assertEqual(combine([V,U]),U);self.assertEqual(combine([]),U)
if __name__=='__main__':unittest.main()
