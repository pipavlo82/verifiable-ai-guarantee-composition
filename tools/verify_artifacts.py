"""Verify complete file inventory against SHA-256; no self-referential manifest hash."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts.sha256.json"
EXCLUDED_DIRS = {".git", "build", "__pycache__", ".venv"}


def inventory():
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.rglob("*")) if p.is_file() and p != MANIFEST
            and not set(p.relative_to(ROOT).parts) & EXCLUDED_DIRS and p.suffix != ".pyc"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Maintainer-only: regenerate after intentional changes")
    args = parser.parse_args()
    actual = inventory()
    if args.write:
        MANIFEST.write_text(json.dumps({"schema": "sha256-inventory-v0", "excludes": ["self", "git", "build", "pycache", "venv"], "files": actual}, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    saved = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    mismatch = sorted(k for k in set(saved) | set(actual) if saved.get(k) != actual.get(k))
    passed = bool(saved) and not mismatch
    print(json.dumps({"passed": passed, "files": len(saved), "mismatches": mismatch}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
