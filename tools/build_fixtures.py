"""Reconstruct named synthetic fixtures; no original archive was recovered."""
import copy
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from composition import digest, input_digest, sealed


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(output=None):
    output = Path(output) if output else ROOT / "fixtures"
    def body(role, payload, issuer="fixture-producer"):
        return {"role": role, "mechanism": "synthetic-checksum-v0", "subject": "subject-A",
                "issuer": issuer, "scope": ["release"], "strength": "SYNTHETIC",
                "domain": "local-experiment", "not_before": 100, "not_after": 200, "payload": payload}
    records = {
        "provenance": body("provenance", {"raw": "3", "input": 3, "transform": "identity-v0", "input_digest": input_digest(3)}),
        "model": body("model", {"id": "square", "version": 1, "operation": "x*x"}),
        "proof": body("proof", {"input": 3, "input_digest": input_digest(3), "output": 9, "model": "square", "version": 1}),
        "judgment": body("judgment", {"action": "release", "verdict": "approve", "policy": "composition-policy-v0"}, "judge-A")}
    records["receipt"] = body("receipt", {"execution": "run-A", "action": "release", "output": 9,
                                         "proof_digest": digest(records["proof"]), "completed": "recorded"})
    base = {"schema": "composition-fixture-v0", "mode": "synthetic", "request": {
        "subject": "subject-A", "input_digest": input_digest(3), "model": "square", "version": 1,
        "output": 9, "action": "release", "execution": "run-A", "scope": ["release"], "strength": "SYNTHETIC",
        "domain": "local-experiment", "time": 150, "nonce": "nonce-new", "policy": "composition-policy-v0"},
        "evidence": {k: sealed(v) for k, v in records.items()}}
    cases, packets = [], {}
    def add(name, boundary, status, baseline, edit=None, core=False):
        packet = copy.deepcopy(base)
        if edit:
            edit(packet)
        # Seals are freely recomputable. This does not make changed judgments authentic.
        for item in packet["evidence"].values():
            if item:
                item["fixture_checksum"] = digest(item["body"])
        packets[name] = packet
        cases.append({"id": name, "file": name + ".json", "boundary": boundary, "expected": status,
                      "baseline_expected": baseline, "core_negative": core})
    def payload(p, role):
        return p["evidence"][role]["body"]["payload"]
    add("P00_valid", None, "VERIFIED", "VERIFIED")
    add("N01_wrong_provenance", "G1", "REFUTED", "VERIFIED", lambda p: p["request"].update(input_digest=input_digest(8)), True)
    add("N02_wrong_model_version", "G2", "REFUTED", "VERIFIED", lambda p: p["request"].update(version=2), True)
    def wrong_input(p):
        # Square(3) == Square(-3): equal outputs do not establish equal inputs.
        payload(p, "proof").update(input=-3, input_digest=input_digest(-3))
        payload(p, "receipt")["proof_digest"] = digest(p["evidence"]["proof"]["body"])
    add("N03_valid_proof_wrong_input", "G3", "REFUTED", "VERIFIED", wrong_input, True)
    add("N04_cross_subject", "G4", "REFUTED", "VERIFIED", lambda p: p["evidence"]["receipt"]["body"].update(subject="subject-B"), True)
    add("N05_unauthentic_judgment", "G5", "REFUTED", "REFUTED", lambda p: p["evidence"]["judgment"]["body"].update(catalog_entry="unregistered-message"), True)
    add("N06_valid_judgment_wrong_action", "G6", "REFUTED", "VERIFIED", lambda p: payload(p, "judgment").update(action="delete"), True)
    add("N07_valid_receipt_wrong_execution", "G7", "REFUTED", "VERIFIED", lambda p: payload(p, "receipt").update(execution="run-B"), True)
    add("N08_replay", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(nonce="nonce-used"), True)
    add("N09_missing_dependency", "G7", "UNVERIFIABLE", "UNVERIFIABLE", lambda p: p["evidence"].pop("receipt"), True)
    add("N10_invalid_authority", "G6", "REFUTED", "VERIFIED", lambda p: p["evidence"]["judgment"]["body"].update(issuer="judge-B"))
    add("N11_scope_amplification", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(scope=["release", "delete"]))
    add("N12_strength_amplification", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(strength="REAL_CRYPTO"))
    add("N13_cross_domain", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(domain="foreign"))
    add("N14_expired", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(time=200))
    add("N15_invalid_arithmetic", "G3", "REFUTED", "REFUTED", lambda p: payload(p, "proof").update(output=10))
    add("N16_missing_proof", "G3", "UNVERIFIABLE", "UNVERIFIABLE", lambda p: p["evidence"].pop("proof"))
    add("N17_real_mode", None, "UNVERIFIABLE", "UNVERIFIABLE", lambda p: p.update(mode="real", verified=True))
    add("N18_policy_mismatch", "G8", "REFUTED", "VERIFIED", lambda p: p["request"].update(policy="other-policy"))
    add("N19_receipt_proof_substitution", "G7", "REFUTED", "VERIFIED", lambda p: payload(p, "receipt").update(proof_digest="0" * 64))
    add("N20_missing_plus_refuted", "G2", "REFUTED", "REFUTED", lambda p: (p["evidence"].pop("receipt"), payload(p, "proof").update(output=10)))
    # Catalog includes valid-but-wrong-action and authentic-but-unauthorized judge-B messages.
    catalog = {}
    for name in ("P00_valid", "N06_valid_judgment_wrong_action", "N10_invalid_authority"):
        j = packets[name]["evidence"]["judgment"]["body"]
        catalog.setdefault(j["issuer"], []).append(digest(j))
    policy = {"id": "composition-policy-v0", "domain": "local-experiment", "authorized_judges": ["judge-A"],
              "consumed_nonces": ["nonce-used"], "authentic_judgments": catalog}
    for name, packet in packets.items():
        write(output / (name + ".json"), packet)
    write(output / "cases.json", cases)
    write(output / "policy.json", policy)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    build(parser.parse_args().out)
