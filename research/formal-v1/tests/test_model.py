import importlib.util
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(newline="\n")
sys.stderr.reconfigure(newline="\n")
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("obligation_model", ROOT / "model.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class ObligationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = model.run()

    def test_exhaustive_oracle_and_minimal_bases(self):
        r = self.report["without_cross_component_native_equalities"]
        self.assertEqual((r["subsets"], r["assignments"], r["oracle_evaluations"]), (512, 512, 262144))
        self.assertEqual(r["sufficient_sets"], 64)
        self.assertEqual(len(r["inclusion_minimal_bases"]), 27)
        self.assertEqual(r["minimum_cardinality"], 6)
        self.assertEqual(len(r["removal_countermodels"]), 162)

    def test_native_premise_changes_minimum(self):
        r = self.report["conditional_on_one_additional_verified_equality"]
        self.assertEqual((r["subsets"], r["assignments"], r["oracle_evaluations"]), (256, 256, 65536))
        self.assertEqual(r["sufficient_sets"], 48)
        self.assertEqual(len(r["inclusion_minimal_bases"]), 18)
        self.assertEqual(r["minimum_cardinality"], 5)
        self.assertEqual(len(r["removal_countermodels"]), 90)

    def test_each_removal_satisfies_remaining_and_breaks_target(self):
        for key in ("without_cross_component_native_equalities", "conditional_on_one_additional_verified_equality"):
            r = self.report[key]
            for cert in r["removal_countermodels"]:
                selected = set(cert["basis"]) - {cert["removed"]}
                self.assertTrue(model.satisfies_edges(cert["countermodel"], selected | set(r["native_premises"])))
                self.assertFalse(model.target_semantics(cert["countermodel"]))
                self.assertTrue(model.entails(cert["basis"], r["native_premises"]))

    def test_empty_or_one_disconnected_group_cannot_entail(self):
        self.assertFalse(model.entails([]))
        self.assertFalse(model.entails([k for k in model.EDGES if not k.startswith("action.")]))
        self.assertTrue(model.entails(model.EDGES))

    def test_unknown_native_fact_rejected(self):
        with self.assertRaises(ValueError):
            model.entails([], ["producer_says_verified"])

    def test_algorithm_and_representation_cannot_be_erased(self):
        left = {"algorithm": "sha256", "representation": "raw-bytes-v1", "digest": "a" * 64}
        self.assertEqual(model.compare_commitments(left, left), "VERIFIED")
        for changed in ({"algorithm": "keccak256"}, {"representation": "canonical-value-v1"}):
            right = dict(left, **changed)
            self.assertEqual(model.compare_commitments(left, right), "UNVERIFIABLE")

    def test_missing_unsupported_or_boolean_evidence_cannot_verify(self):
        value = {"algorithm": "sha256", "representation": "raw", "digest": "a" * 64}
        for other in (None, True, [], "verified", {"verified": True}, dict(value, digest=True), dict(value, algorithm=[]), dict(value, algorithm="other")):
            self.assertEqual(model.compare_commitments(value, other), "UNVERIFIABLE")

    def test_same_type_digest_contradiction_refuted(self):
        value = {"algorithm": "sha256", "representation": "raw", "digest": "a" * 64}
        self.assertEqual(model.compare_commitments(value, dict(value, digest="b" * 64)), "REFUTED")

    def test_noninjective_translation_has_concrete_preimages(self):
        r = self.report["noninjective_translation_counterexample"]
        self.assertTrue(r["normalized_equal"])
        self.assertFalse(r["raw_equal"])
        self.assertNotEqual(r["left_sha256"], r["right_sha256"])

    def test_no_real_authorization_claim(self):
        self.assertEqual(self.report["downstream_authorization"], "NOT_ESTABLISHED")
        self.assertEqual(self.report["cryptographic_verification"], "NOT_PERFORMED")

    def test_source_removal_controls(self):
        original = (ROOT / "model.py").read_text(encoding="utf-8")
        sites = [
            ("return all(groups[left] == groups[right] for left, right in TARGETS)", "return True", "closure"),
            ('if (left["algorithm"], left["representation"]) != (right["algorithm"], right["representation"]):', 'if False:', "type")]
        for old, new, name in sites:
            self.assertEqual(original.count(old), 1)
            namespace = {"__name__": "mutant"}
            exec(compile(original.replace(old, new), "isolated-" + name, "exec"), namespace)
            if name == "closure":
                self.assertFalse(model.entails([]))
                self.assertTrue(namespace["entails"]([]))
                # The independent exhaustive oracle detects the mutant, not a crash-as-kill.
                with self.assertRaisesRegex(RuntimeError, "Graph closure disagrees"):
                    namespace["analyze"]()
            else:
                left = {"algorithm": "sha256", "representation": "raw", "digest": "a" * 64}
                right = dict(left, representation="normalized")
                self.assertEqual(model.compare_commitments(left, right), "UNVERIFIABLE")
                self.assertEqual(namespace["compare_commitments"](left, right), "VERIFIED")
            self.assertEqual((ROOT / "model.py").read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
