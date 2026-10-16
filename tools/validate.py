"""Run reproducibility gates and save raw process output without shell interpolation."""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="build/validation")
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    runs = []
    outputs = {}
    def run(label, command, json_output=False, seed="0"):
        process = subprocess.run([sys.executable, "-B", "-X", "utf8"] + command, cwd=ROOT,
                                 env=dict(env, PYTHONHASHSEED=seed), capture_output=True)
        suffix = ".stdout.json" if json_output else ".stdout.log"
        # Preserve raw bytes. Child runners explicitly emit LF on every platform.
        (out / (label + suffix)).write_bytes(process.stdout)
        (out / (label + ".stderr.log")).write_bytes(process.stderr)
        runs.append({"id": label, "command": ["python", "-B", "-X", "utf8"] + command,
                     "pythonhashseed": seed, "returncode": process.returncode,
                     "stdout_sha256": sha(process.stdout), "stderr_sha256": sha(process.stderr)})
        outputs[label] = process.stdout
    for label, flags in (("tests-normal", []), ("tests-repeat", []), ("tests-optimized", ["-O"])):
        run(label, flags + ["-m", "unittest", "discover", "-s", "tests", "-v"])
    for label, flags, seed in (("experiment-normal", [], "0"), ("experiment-repeat", [], "29"), ("experiment-optimized", ["-O"], "71")):
        run(label, flags + ["tools/experiment.py"], True, seed)
    for label, flags in (("mutations-normal", []), ("mutations-optimized", ["-O"])):
        run(label, flags + ["tools/mutations.py"], True)
    before = {p.name: sha(p.read_bytes()) for p in (ROOT / "fixtures").glob("*.json")}
    run("fixtures-regenerate", ["tools/build_fixtures.py", "--out", "build/regenerated-fixtures"])
    after = {p.name: sha(p.read_bytes()) for p in (ROOT / "build/regenerated-fixtures").glob("*.json")}
    run("benchmark", ["tools/benchmark.py"], True)
    deterministic = outputs["experiment-normal"] == outputs["experiment-repeat"] == outputs["experiment-optimized"]
    mutations_equal = outputs["mutations-normal"] == outputs["mutations-optimized"]
    saved = ROOT / "evidence/validation"
    committed_match = {}
    for label in ("experiment-normal", "mutations-normal"):
        path = saved / (label + ".stdout.json")
        if path.exists() and path.parent != out:
            # Compare JSON values across platforms; within-host byte determinism above.
            committed_match[label] = json.loads(path.read_bytes()) == json.loads(outputs[label])
    ok = all(r["returncode"] == 0 for r in runs) and deterministic and mutations_equal and before == after and all(committed_match.values())
    report = {"schema": "composition-validation-v0", "passed": ok, "python": platform.python_version(),
              "system": platform.system(), "optimized_parent": not __debug__, "commands": runs,
              "deterministic_experiment_bytes": deterministic, "deterministic_mutation_bytes": mutations_equal,
              "fixture_regeneration_identical": before == after, "committed_results_match": committed_match}
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k != "commands"}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
