import copy
import tempfile
import unittest
import sys
sys.stdout.reconfigure(newline="\n")
sys.stderr.reconfigure(newline="\n")
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
from composition import canonical, digest, evaluate, load, sealed, combine
import mutations
import experiment


class CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load(ROOT / "fixtures/policy.json")
        cls.base = load(ROOT / "fixtures/P00_valid.json")
        cls.cases = load(ROOT / "fixtures/cases.json")

    def test_fixture_inventory(self):
        self.assertEqual(len(self.cases), 21)
        self.assertEqual(sum(c["core_negative"] for c in self.cases), 9)
        self.assertEqual(len({c["id"] for c in self.cases}), len(self.cases))

    def test_all_fixtures_both_strategies(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                packet = load(ROOT / "fixtures" / case["file"])
                self.assertEqual(evaluate(packet, self.policy)["status"], case["expected"])
                self.assertEqual(evaluate(packet, self.policy, True)["status"], case["baseline_expected"])

    def test_no_real_crypto_claim_in_any_case(self):
        for case in self.cases:
            self.assertIs(evaluate(load(ROOT / "fixtures" / case["file"]), self.policy)["real_crypto_verified"], False)

    def test_unknown_mechanism_is_not_false_proof(self):
        packet = copy.deepcopy(self.base)
        packet["evidence"]["proof"]["body"]["mechanism"] = "zkIE"
        self.assertEqual(evaluate(packet, self.policy)["status"], "UNVERIFIABLE")

    def test_boolean_is_not_proof(self):
        packet = copy.deepcopy(self.base)
        packet["evidence"]["proof"] = {"verified": True}
        self.assertEqual(evaluate(packet, self.policy)["status"], "UNVERIFIABLE")

    def test_boolean_version_rejected(self):
        packet = copy.deepcopy(self.base)
        packet["request"]["version"] = True
        self.assertEqual(evaluate(packet, self.policy)["status"], "UNVERIFIABLE")

    def test_boolean_evidence_numbers_rejected(self):
        for role, field in (("model", "version"), ("proof", "version"), ("receipt", "output")):
            packet = copy.deepcopy(self.base)
            body = packet["evidence"][role]["body"]
            body["payload"][field] = True
            packet["evidence"][role] = sealed(body)
            self.assertEqual(evaluate(packet, self.policy)["status"], "UNVERIFIABLE")

    def test_nonobject_packet_unverifiable(self):
        self.assertEqual(evaluate([], self.policy)["status"], "UNVERIFIABLE")

    def test_checksum_does_not_authenticate(self):
        packet = copy.deepcopy(self.base)
        j = packet["evidence"]["judgment"]["body"]
        j["extra"] = "tampered"
        packet["evidence"]["judgment"] = sealed(j)
        report = evaluate(packet, self.policy)
        self.assertEqual(report["components"]["judgment"]["status"], "VERIFIED")
        self.assertEqual(report["guarantees"]["G5"]["status"], "REFUTED")

    def test_checksum_corruption(self):
        packet = copy.deepcopy(self.base)
        packet["evidence"]["receipt"]["fixture_checksum"] = "0" * 64
        self.assertEqual(evaluate(packet, self.policy)["status"], "REFUTED")

    def test_every_missing_component_unknown(self):
        for role in self.base["evidence"]:
            with self.subTest(role=role):
                packet = copy.deepcopy(self.base)
                packet["evidence"].pop(role)
                report = evaluate(packet, self.policy)
                self.assertEqual(report["status"], "UNVERIFIABLE")
                self.assertEqual(report["guarantees"]["G8"]["status"], "UNVERIFIABLE")

    def test_arbitrary_dependency_list_cannot_omit_check(self):
        packet = load(ROOT / "fixtures/N04_cross_subject.json")
        packet["request"]["required_guarantees"] = []
        self.assertEqual(evaluate(packet, self.policy)["status"], "REFUTED")

    def test_combine_three_values(self):
        self.assertEqual(combine([]), "UNVERIFIABLE")
        self.assertEqual(combine([{"status": "UNVERIFIABLE"}]), "UNVERIFIABLE")
        self.assertEqual(combine([{"status": "UNVERIFIABLE"}, {"status": "REFUTED"}]), "REFUTED")

    def test_missing_is_not_refutation(self):
        report = evaluate(load(ROOT / "fixtures/N09_missing_dependency.json"), self.policy)
        self.assertEqual(report["status"], "UNVERIFIABLE")
        self.assertNotIn("REFUTED", [v["status"] for v in report["guarantees"].values()])

    def test_real_mode_even_with_flags_is_unimplemented(self):
        packet = copy.deepcopy(self.base)
        packet.update(mode="real", proof_valid=True, signature_verified=True)
        report = evaluate(packet, self.policy)
        self.assertEqual(report["status"], "UNVERIFIABLE")
        self.assertEqual(report["reason"], "REAL_ARTIFACT_INTEGRATION_NOT_IMPLEMENTED")

    def test_duplicate_keys_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for data in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":1.5}'):
                path.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load(path)

    def test_repeat_deterministic_and_no_mutation(self):
        before = canonical(self.base)
        self.assertEqual(experiment.run(), experiment.run())
        evaluate(self.base, self.policy)
        self.assertEqual(before, canonical(self.base))

    def test_mutation_classifications(self):
        self.assertEqual(mutations.classify(False, False, None, None, None, None), "NOT_APPLIED")
        self.assertEqual(mutations.classify(True, True, "REFUTED", None, "REFUTED", "VERIFIED"), "CRASHED")
        self.assertEqual(mutations.classify(True, False, "REFUTED", "REFUTED", "REFUTED", "VERIFIED"), "SURVIVED")
        self.assertEqual(mutations.classify(True, False, "UNVERIFIABLE", "VERIFIED", "REFUTED", "VERIFIED"), "UNVERIFIABLE")
        self.assertEqual(mutations.classify(True, False, "REFUTED", "VERIFIED", "REFUTED", "VERIFIED"), "KILLED")

    def test_all_boundary_mutations_and_restore(self):
        report = mutations.run()
        self.assertEqual(report["counts"], {"KILLED": 8, "SURVIVED": 0, "CRASHED": 0, "NOT_APPLIED": 0, "UNVERIFIABLE": 0})
        self.assertTrue(report["original_bytes_unchanged"])


if __name__ == "__main__":
    unittest.main()
