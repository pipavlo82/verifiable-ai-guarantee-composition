"""Optional verification of pinned upstream Git blobs in already available clones."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clones", required=True, help="Directory containing zkIE, recompute-kit, agent-ercs, receiptos-verify, ERCs-1810")
    args = parser.parse_args()
    lock = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))
    if len(lock["sources"]) != 5 or not all(s["files"] for s in lock["sources"]):
        raise ValueError("Source inventory incomplete")
    rows = []
    for source in lock["sources"]:
        clone = Path(args.clones) / source["clone_name"]
        for entry in source["files"]:
            p = subprocess.run(["git", "-C", str(clone), "show", source["commit"] + ":" + entry["path"]], capture_output=True)
            passed = p.returncode == 0 and hashlib.sha256(p.stdout).hexdigest() == entry["sha256"]
            rows.append({"repository": source["repository"], "path": entry["path"], "passed": passed})
    print(json.dumps({"passed": all(r["passed"] for r in rows), "files": rows}, indent=2))
    return 0 if all(r["passed"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
