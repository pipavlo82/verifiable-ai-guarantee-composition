"""Remove one actual enforcement predicate in an isolated compiled source copy."""
import json
import sys
import types
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from composition import evaluate, load

TARGETS = {f"G{i}": name for i, name in enumerate([
    "N01_wrong_provenance", "N02_wrong_model_version", "N03_valid_proof_wrong_input", "N04_cross_subject",
    "N05_unauthentic_judgment", "N06_valid_judgment_wrong_action", "N07_valid_receipt_wrong_execution", "N08_replay"], 1)}


def classify(applied, crashed, before, after, restored, positive):
    if not applied:
        return "NOT_APPLIED"
    if crashed:
        return "CRASHED"
    if before != "REFUTED" or restored != "REFUTED" or positive != "VERIFIED":
        return "UNVERIFIABLE"
    return "KILLED" if after == "VERIFIED" else "SURVIVED"


def run():
    path = ROOT / "src/composition.py"
    original = path.read_bytes()
    source = original.decode("utf-8")
    policy = load(ROOT / "fixtures/policy.json")
    positive = load(ROOT / "fixtures/P00_valid.json")
    cases = load(ROOT / "fixtures/cases.json")
    rows = []
    for gid, case_id in TARGETS.items():
        packet = load(ROOT / "fixtures" / (case_id + ".json"))
        before = evaluate(packet, policy)["status"]
        lines = [line for line in source.splitlines() if line.endswith("# MUTATE:" + gid)]
        applied = len(lines) == 1
        crashed, after, positive_status, error = False, None, None, None
        killed_by = []
        if applied:
            old = lines[0]
            replacement = '    return verdict(True, "MUTATED_REMOVED_' + gid + '")  # MUTATE:' + gid
            changed = source.replace(old, replacement)
            module = types.ModuleType("isolated_mutant_" + gid)
            try:
                exec(compile(changed, "isolated-mutant-" + gid + ".py", "exec"), module.__dict__)
                after = module.evaluate(packet, policy)["status"]
                positive_status = module.evaluate(positive, policy)["status"]
                for case in cases:
                    observed = module.evaluate(load(ROOT / "fixtures" / case["file"]), policy)["status"]
                    if observed != case["expected"]:
                        killed_by.append(case["id"])
            except Exception as exc:
                crashed, error = True, type(exc).__name__
        restored_module = types.ModuleType("restored_" + gid)
        exec(compile(source, "restored-source.py", "exec"), restored_module.__dict__)
        restored = restored_module.evaluate(packet, policy)["status"]
        restored_green = all(restored_module.evaluate(load(ROOT / "fixtures" / c["file"]), policy)["status"] == c["expected"] for c in cases)
        label = classify(applied, crashed, before, after, restored, positive_status)
        if not restored_green:
            label = "UNVERIFIABLE"
        rows.append({"guarantee": gid, "target": case_id, "classification": label, "before": before,
                     "after": after, "restored": restored, "restored_full_matrix_green": restored_green,
                     "positive_after": positive_status, "killed_by": killed_by, "error": error,
                     "removed_source": lines[0].strip() if applied else None})
    if original != path.read_bytes():
        raise RuntimeError("Original source changed during mutations")
    counts = {name: sum(r["classification"] == name for r in rows)
              for name in ("KILLED", "SURVIVED", "CRASHED", "NOT_APPLIED", "UNVERIFIABLE")}
    return {"schema": "composition-mutations-v0", "method": "one predicate removed per compiled isolated copy",
            "original_bytes_unchanged": True, "counts": counts, "mutants": rows}


if __name__ == "__main__":
    sys.stdout.reconfigure(newline="\n")
    result = run()
    print(json.dumps(result, sort_keys=True, indent=2))
    sys.exit(0 if result["counts"]["KILLED"] == 8 else 1)
