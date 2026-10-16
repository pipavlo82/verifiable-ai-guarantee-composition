"""Descriptive local timings, same resident objects, alternating strategy order."""
import json
import platform
import statistics
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from composition import evaluate, load


def run(rounds=11, repeats=20):
    policy = load(ROOT / "fixtures/policy.json")
    packets = [load(ROOT / "fixtures" / c["file"]) for c in load(ROOT / "fixtures/cases.json")]
    samples = {"independent": [], "composition": []}
    def batch(baseline):
        start = time.perf_counter_ns()
        for _ in range(repeats):
            for packet in packets:
                evaluate(packet, policy, baseline)
        return (time.perf_counter_ns() - start) / (repeats * len(packets))
    batch(True)
    batch(False)
    for r in range(rounds):
        for name in (("independent", "composition") if r % 2 == 0 else ("composition", "independent")):
            samples[name].append(batch(name == "independent"))
    medians = {name: statistics.median(values) for name, values in samples.items()}
    return {"schema": "composition-benchmark-v0", "python": platform.python_version(), "system": platform.system(),
            "machine": platform.machine(), "rounds": rounds, "repeats": repeats, "cases": len(packets),
            "unit": "ns per packet", "samples": samples, "medians": medians,
            "composition_minus_independent_ns": medians["composition"] - medians["independent"],
            "median_ratio": medians["composition"] / medians["independent"],
            "limitation": "One local Python host, tiny synthetic fixtures, no cryptographic/runtime/network costs; not a security or upstream performance result."}


if __name__ == "__main__":
    sys.stdout.reconfigure(newline="\n")
    print(json.dumps(run(), sort_keys=True, indent=2))
