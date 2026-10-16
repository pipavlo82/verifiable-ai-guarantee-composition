"""Deterministic finite-fixture report; timing is deliberately separate."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from composition import evaluate, load, digest


def run():
    policy = load(ROOT / "fixtures/policy.json")
    cases = load(ROOT / "fixtures/cases.json")
    totals = {m: {"false_authorizations": 0, "correct_refusals": 0, "unverifiable": 0, "verified": 0,
                  "refuted": 0, "oracle_matches": 0} for m in ("independent", "composition")}
    rows = []
    for case in cases:
        packet = load(ROOT / "fixtures" / case["file"])
        row = {"id": case["id"], "core_negative": case["core_negative"], "expected": case["expected"]}
        for name, baseline in (("independent", True), ("composition", False)):
            result = evaluate(packet, policy, baseline)
            row[name] = result
            status = result["status"]
            t = totals[name]
            t[status.lower()] += 1
            t["false_authorizations"] += int(status == "VERIFIED" and case["expected"] != "VERIFIED")
            t["correct_refusals"] += int(status != "VERIFIED" and case["expected"] != "VERIFIED")
            t["oracle_matches"] += int(status == case["expected"])
        rows.append(row)
    return {"schema": "composition-experiment-v0", "origin": "RECONSTRUCTION", "real_integration": "NOT IMPLEMENTED",
            "policy_sha256": digest(policy), "cases": len(cases), "core_negatives": sum(c["core_negative"] for c in cases),
            "totals": totals, "results": rows}


if __name__ == "__main__":
    sys.stdout.reconfigure(newline="\n")
    print(json.dumps(run(), sort_keys=True, indent=2))
