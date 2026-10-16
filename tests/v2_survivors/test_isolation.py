"""Regression oracles for the two formerly masked source mutants."""
import copy,json,struct,unittest
from pathlib import Path
from tools.v2.audit_survivors import WITNESSES,evaluate,load_case
from src.v2.composition import CAP,verify
class IsolatedWitnesses(unittest.TestCase):
    def test_native_rejection_is_isolated(self):
        r=evaluate('native_isolated')
        self.assertEqual(r['status'],'REFUTED')
        self.assertEqual({o['name']:o['status'] for o in r['obligations'] if o['status']!='VERIFIED'},{'inference':'REFUTED'})
        self.assertEqual(r['native']['exit'],1)
        self.assertTrue(all(r['components'][role]=='VERIFIED' for role in ('provenance','judgment','receipt')))
    def test_type_rejection_is_isolated(self):
        r=evaluate('type_isolated')
        self.assertEqual(r['status'],'REFUTED')
        self.assertEqual({o['name']:o['status'] for o in r['obligations'] if o['status']!='VERIFIED'},{'artifact_types':'REFUTED'})
        self.assertTrue(all(v=='VERIFIED' for v in r['components'].values()))
    def test_positive_control(self):self.assertEqual(evaluate('positive')['status'],'VERIFIED')
    def test_corruption_is_only_one_scalar(self):
        old=(CAP/'a/proof.bin').read_bytes();new=(WITNESSES/'invalid-claimed-scalar.bin').read_bytes()
        self.assertEqual(old[:12],new[:12]);self.assertEqual(old[20:],new[20:]);self.assertNotEqual(old[12:20],new[12:20])
        self.assertEqual(struct.unpack_from('<Q',new,12)[0],(struct.unpack_from('<Q',old,12)[0]+1)%18446744069414584321)
    def test_type_witness_keeps_role_separation(self):
        c,p=load_case('type_isolated');policy=json.loads(p.read_text())
        self.assertEqual(len(set(policy['authorized'].values())),3)
        self.assertEqual(c['documents']['judgment']['type'],'LabReceipt')
        self.assertEqual(c['documents']['judgment']['signer'],policy['authorized']['judgment'])
    def test_signature_still_required(self):
        c,p=load_case('positive');c=copy.deepcopy(c);c['documents']['judgment']['signature']='0x'+'00'*65
        self.assertEqual(verify(c,p)['status'],'REFUTED')
    def test_stronger_claim_still_unknown(self):
        c,p=load_case('positive');c['claim']['claimKind']='historical-external-execution'
        self.assertEqual(verify(c,p)['status'],'UNVERIFIABLE')
if __name__=='__main__':unittest.main()
