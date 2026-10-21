import copy,itertools,json,unittest
from src.v3.evidence import ROOT,base_case,canonical,read,sha,strict
from src.v3.model import CLAIMS,GRAPH,closure,eq,evaluate,join,policy
from src.v3.scenarios import cases
class RealChainTests(unittest.TestCase):
    def test_policy_does_not_derive_expected_subject_from_evidence(self):
        from unittest.mock import patch
        with patch('src.v3.model.base_case',side_effect=RuntimeError('evidence must not define policy')):
            self.assertEqual(policy()['verdict'],'reject')
            self.assertTrue(policy()['decision_ref'].startswith('sha256:5bca0bf'))
    def test_all_declared_scenarios(self):
        for row in cases():
            with self.subTest(row['name']):
                result=evaluate(row['case'],row['request'],row['claim'])
                self.assertEqual(result['status'],row['expected']);self.assertEqual(result['authorized'],row['expected']=='VERIFIED')
    def test_required_counterexamples_are_isolated(self):
        for row in cases():
            if row['boundary']:
                with self.subTest(row['boundary']):
                    result=evaluate(row['case'],row['request'],row['claim'])
                    self.assertEqual({k:v for k,v in result['obligations'].items() if v!='VERIFIED'},{row['boundary']:'REFUTED'})
    def test_unrelated_native_and_public_judgment_do_not_complete_chain(self):
        r=evaluate(base_case(),policy(),'external_full_chain');self.assertEqual(r['status'],'UNVERIFIABLE')
        self.assertEqual(set(r['missing']),{'wyriwe_provenance','external_model_authority','inference_judgment_binding','external_execution'})
    def test_historical_hash_pointer_does_not_prove_capture_or_execution(self):
        r=evaluate(base_case(),policy(),'historical_cell_execution');self.assertEqual(r['status'],'UNVERIFIABLE');self.assertEqual(set(r['missing']),{'historical_input_bytes','historical_execution'})
    def test_valid_signature_wrong_requested_verdict(self):
        p=policy();p['verdict']='approve';r=evaluate(base_case(),p)
        self.assertTrue(all(v=='VERIFIED' for v in r['components'].values()));self.assertEqual(r['refuted'],['judgment_scope'])
    def test_receipt_integrity_does_not_supply_external_execution(self):
        c=base_case();self.assertEqual(evaluate(c,policy(),'local_receipt_binding')['status'],'VERIFIED');self.assertIn('external_execution',evaluate(c,policy(),'external_full_chain')['missing'])
    def test_missing_dependency_is_never_authorized(self):
        for role in ('ledger','cell1','cell2'):
            c=base_case();c[role]=None;self.assertFalse(evaluate(c,policy())['authorized'])
    def test_mixed_missing_and_known_refutation(self):
        c=base_case();c['cell1']=None;p=policy();p['domain']['chainId']=31337;r=evaluate(c,p)
        self.assertEqual(r['status'],'REFUTED');self.assertIn('cell1_signature',r['missing']);self.assertIn('domain',r['refuted'])
    def test_equality_retains_known_contradiction(self):
        self.assertEqual(eq(['a','b',None]),'REFUTED');self.assertEqual(eq(['a','a',None]),'UNVERIFIABLE');self.assertEqual(eq([None,None]),'UNVERIFIABLE')
    def test_aggregation_truth_table(self):
        for values in itertools.product(('VERIFIED','REFUTED','UNVERIFIABLE'),repeat=3):
            expected='REFUTED' if values.count('REFUTED') else 'UNVERIFIABLE' if values.count('UNVERIFIABLE') else 'VERIFIED';self.assertEqual(join(values),expected)
    def test_planner_requires_cross_artifact_bindings(self):
        needed=set(closure('claim_agreement'));self.assertTrue({'decision_binding','claim_binding','domain','judgment_scope','as_of'}<=needed);self.assertEqual(len(needed),10)
    def test_graph_contracts_and_dependency_closure(self):
        for claim in CLAIMS:self.assertEqual(len(closure(claim)),len(set(closure(claim))))
        for node in GRAPH.values():self.assertTrue(node.subject and node.scope and node.authority and node.evidence and node.assumptions and node.verification_contract)
    def test_unknown_claim_not_inferred(self):
        with self.assertRaises(ValueError):closure('payment_authorized')
    def test_canonicalization_rejects_unsupported_numbers(self):
        for value in (0.5,2**54):
            with self.assertRaises(ValueError):canonical({'n':value})
    def test_duplicate_members_rejected(self):
        with self.assertRaises(ValueError):strict('{"id":1,"id":2}')
    def test_signed_source_class_limit_is_preserved(self):
        j=json.loads(base_case()['ledger']['proof_event']['content']);self.assertEqual(j['source_class'],'agent_reported');self.assertIn('nothing external confirms',j['vantage_limitation'])
    def test_missing_outcome_is_observed_404_not_refutation(self):
        captures=read(ROOT/'evidence/v3/public/captures.json');row=next(r for r in captures if r['name']=='ledger-236-outcome');self.assertEqual(row['status'],404)
    def test_actual_external_input_digests_not_backfilled(self):
        c=base_case();signed=c['cell2']['proof_payload']['evidence']['independence']['inputs'][0]['content_hash'];observed='sha256:'+sha((ROOT/'evidence/v3/public/ledger-236.json').read_bytes());self.assertNotEqual(signed,observed)
if __name__=='__main__':unittest.main()
