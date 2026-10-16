import copy, json, os, struct, subprocess, unittest
from pathlib import Path
from src.v2.composition import CAP,ROOT,Status,base_case,combine,native_path,verify
from src.v2.scenarios import scenarios
class RealArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.results={r['name']:verify(r['case']) for r in scenarios()}
    def test_declared_scenarios(self):
        for row in scenarios():
            with self.subTest(case=row['name']):self.assertEqual(self.results[row['name']]['status'],row['expected'])
    def test_real_native_invocation(self):
        result=self.results['valid_recomputation']
        self.assertEqual(result['native']['exit'],0)
        self.assertTrue(all(json.loads(result['native']['stdout']).values()))
    def test_external_signature_known_answer(self):self.assertTrue(all(self.results['valid_recomputation']['crypto']['known_answers'].values()))
    def test_authentic_wrong_authority(self):
        r=self.results['invalid_authority_valid_signature'];self.assertEqual(r['components']['judgment'],'VERIFIED');self.assertFalse(r['authorized'])
    def test_authentic_cross_domain(self):
        r=self.results['cross_domain_valid_signature'];self.assertEqual(r['components']['judgment'],'VERIFIED');self.assertFalse(r['authorized'])
    def test_authentic_wrong_action(self):
        r=self.results['valid_judgment_wrong_action'];self.assertEqual(r['components']['judgment'],'VERIFIED');self.assertFalse(r['authorized'])
    def test_authentic_wrong_execution(self):
        r=self.results['valid_receipt_wrong_execution'];self.assertEqual(r['components']['receipt'],'VERIFIED');self.assertFalse(r['authorized'])
    def test_actual_other_native_component(self):self.assertEqual(self.results['valid_other_native_component']['components']['inference'],'VERIFIED')
    def test_native_proof_wrong_input(self):self.assertEqual(self.results['native_proof_wrong_input']['components']['inference'],'REFUTED')
    def test_no_historical_execution_inference(self):self.assertEqual(self.results['complete_historical_chain_unavailable']['status'],'UNVERIFIABLE')
    def test_mixed_refutation_keeps_unknowns(self):
        r=self.results['mixed_refutation_missing'];self.assertEqual(r['status'],'REFUTED');self.assertIn('UNVERIFIABLE',[o['status'] for o in r['obligations']])
    def test_missing_is_not_refuted(self):self.assertEqual(self.results['missing_input_bytes']['status'],'UNVERIFIABLE')
    def test_no_producer_boolean_evidence(self):
        c=base_case();c['documents']['judgment']['verified']=True;c['documents']['judgment']['signature']='0x'+'00'*65
        self.assertEqual(verify(c)['status'],'REFUTED')
    def test_independent_python_output_recomputation(self):
        for v in ('a','b'):
            p=CAP/v;a=struct.unpack('<32Q',(p/'input.bin').read_bytes());b=struct.unpack('<64Q',(p/'weights.bin').read_bytes())
            expected=[sum(a[i*8+k]*b[k*8+j] for k in range(8))%18446744069414584321 for i in range(4) for j in range(8)]
            self.assertEqual(list(struct.unpack('<32Q',(p/'output.bin').read_bytes())),expected)
    def test_native_wire_rejects_trailing_bytes(self):
        out=ROOT/'build/v2';out.mkdir(parents=True,exist_ok=True);bad=out/'trailing-proof.bin';bad.write_bytes((CAP/'a/proof.bin').read_bytes()+b'\0')
        run=subprocess.run([str(native_path()),'verify',str(CAP/'a/input.bin'),str(CAP/'a/weights.bin'),str(CAP/'a/output.bin'),str(bad)],capture_output=True)
        self.assertEqual(run.returncode,2);self.assertIn(b'UNVERIFIABLE',run.stderr)
    def test_tri_state_refutation_precedence(self):
        self.assertEqual(combine([Status.UNVERIFIABLE,Status.REFUTED]),Status.REFUTED);self.assertEqual(combine([]),Status.UNVERIFIABLE)
    def test_fixture_mode_honesty(self):
        meta=json.loads((CAP/'generation.json').read_text());self.assertFalse(meta['external_issuer']);self.assertIsNone(meta['chain_observation']);self.assertFalse(meta['historical_execution_independently_verified'])
    def test_type_and_authority_are_independent(self):
        r=self.results['valid_receipt_used_as_judgment'];self.assertEqual(r['components']['judgment'],'VERIFIED');self.assertEqual(r['status'],'REFUTED')
    def test_public_statement_extraction(self):
        from tools.v2.statement import extract
        for variant in ('a','b'):self.assertEqual(extract(CAP/variant),json.loads((CAP/variant/'public-statement.json').read_text()))
    def test_trusted_policy_is_required(self):self.assertEqual(verify(base_case(),ROOT/'build/v2/no-policy')['status'],'UNVERIFIABLE')
if __name__=='__main__':unittest.main()
