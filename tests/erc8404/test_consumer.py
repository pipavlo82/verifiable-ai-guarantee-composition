import base64,copy,json,unittest
from src.erc8404.engine import *
from src.erc8404.cases import base,cases

class ConsumerTests(unittest.TestCase):
    def test_scenarios(self):
        for w in cases():
            with self.subTest(w['name']):self.assertEqual(decide(w['case'])['status'],w['expected'])
    def test_independence_scenario_dependent(self):
        self.assertEqual(decide(base('self'))['checks']['O14'],R)
        self.assertTrue(decide(base('self_allowed'))['authorized'])
    def test_additional_roles(self):
        self.assertTrue(decide(base('author_bound_independent'))['authorized'])
        self.assertEqual(decide(base('author_bound_collision'))['checks']['O14'],R)
    def test_list_policy_does_not_authorize_output(self):
        c=base('list');c['claim']['outputHash']='false';d=decide(c)
        self.assertTrue(d['authorized']);self.assertEqual(d['unconsumed_claim_fields'],['outputHash'])
        self.assertNotIn('outputHash',d['authorization_scope']['verified_claim_scope'])
    def test_scope_always_named(self):
        for family in ('independent','self_allowed','list','author_bound_independent'):
            c=base(family);s=decide(c)['authorization_scope']
            self.assertEqual(s['contract_sha256'],sha(base64.b64decode(c['contract_bytes'])))
            self.assertEqual(s['scenario'],c['claim']['scenario']);self.assertEqual(s['claim_type'],c['claim']['claimType'])
    def test_authorization_reuse(self):
        c=base();record=decide(c)['authorization_scope']
        self.assertEqual(consume_authorization(record,c),V)
        self.assertEqual(consume_authorization(record,base('self_allowed')),R)
        other=copy.deepcopy(c);other['claim']['claimType']='OTHER'
        self.assertEqual(consume_authorization(record,other),R)
        forged=copy.deepcopy(record);forged['verified_claim_scope']['subject']='someone-else'
        self.assertEqual(consume_authorization(forged,c),R)
    def test_catalog_not_coverage_oracle(self):
        c=base('self');del c['catalog']['O14']
        self.assertEqual(decide(c,'B')['status'],V)
        self.assertEqual(decide(c)['missing_obligations'],['O14'])
    def test_no_broader_core_inference(self):
        c=base();c['claim']['claimType']='EXTERNAL_EXECUTION_SUCCEEDED'
        self.assertEqual(decide(c,'A')['rvr']['recomputationStatus'],'REPRODUCED')
        self.assertEqual(decide(c)['status'],R)
    def test_receipt_bytes_unchanged(self):
        c=base();original=c['receipt_bytes'];before=copy.deepcopy(c)
        decide(c);self.assertEqual(c,before);self.assertEqual(c['receipt_bytes'],original)
    def test_canonical_discrimination(self):
        samples=[{}, {'z':False,'a':True},'\u2028\u2029','\b\u0000/\\','e\u0301',['a','a','b'],{'\U00010000':'a','\ue000':'b'}]
        for s in samples:self.assertEqual(canonical(s),ADAPTER.canonical_bytes(s))
        self.assertNotEqual(canonical(['a','a','b']),canonical(['a','b','a']))
        self.assertNotEqual(canonical('é'),canonical('e\u0301'))
    def test_invalid_canonical_domain(self):
        for raw in (b'{"x":1}',b'{"x":null,"x":false}',b'"\\ud800"',b'NaN'):
            with self.assertRaises(ValueError):strict(raw)
    def test_contract_preimage_required(self):
        c=base();c['contract_bytes']=None;c['contract']=None
        self.assertEqual(decide(c)['status'],U)
    def test_profile_preimage_substitution(self):
        c=base();b=json.loads(base64.b64decode(c['bundle_bytes']));b['verificationProfile']['profileId']='other'
        c['bundle_bytes']=base64.b64encode(canonical(b)).decode()
        self.assertEqual(rvr(c)['gate'],'PROFILE_NOT_SUPPORTED')
    def test_missing_payload_preserves_core_axis(self):
        c=next(w['case'] for w in cases() if w['name']=='missing_committed_payload');d=decide(c)
        self.assertEqual(d['rvr']['recomputationStatus'],'CANNOT_RECOMPUTE')
        self.assertFalse(d['rvr']['evaluationPerformed']);self.assertNotIn('verificationOutcome',d['rvr'])
        self.assertEqual(d['status'],U)
    def test_unknown_obligation(self):
        c=base();c['catalog']['FUTURE']={'procedure':'unknown','dependencies':[]}
        self.assertEqual(decide(c)['status'],U)
    def test_mixed_failure_precedence(self):
        c=base();c['documents']['judgment']=None;c['claim']['scope']='excess'
        self.assertEqual(decide(c)['status'],R)
    def test_malformed_contract(self):
        for value in ([],{},'not-contract',{'schema':'claim-aware.external.v1'}):
            c=base();c['contract_bytes']=base64.b64encode(canonical(value)).decode()
            self.assertEqual(decide(c)['status'],R)

if __name__=='__main__':unittest.main()
