# Reproduce v3

Use a fresh checkout of the exact v3 commit, a short path on Windows, Python 3.12,
Node 22.15.0, Rust/Cargo 1.97.1 and Bun 1.3.14. The pinned ReceiptOS Windows bridge
currently expects `C:/Users/msi/.bun/bin/bun.exe`; Linux uses `bun` on PATH. This is
a portability limitation inherited from that adapter, not silently patched here.

```sh
git clone https://github.com/pipavlo82/verifiable-ai-guarantee-composition
cd verifiable-ai-guarantee-composition
git checkout --detach <exact-v3-commit>
python -B tools/verify_artifacts.py
python -B tools/v3/prepare.py --online
python -B tools/v3/validate.py
python -B tools/verify_artifacts.py
git status --porcelain
```

Setup fetches exact public source pins, uses the committed npm/Cargo locks and
hash-required Python package lock, then builds the native verifier and runs two
exact Rust tests. Subsequent setup can omit `--online` with dependencies cached.
`--cargo-home PATH` selects a local pinned dependency cache. The Crystal bridge
uses Bun built-ins; it does not require ReceiptOS npm packages at replay time.

Validation executes normal/repeat/Python `-O`, the 36 same-evidence scenarios,
19 test methods, two signature implementations, 14 physical mutations in each
mode, determinism and the committed comparison snapshot. Commands, exit codes,
stream hashes and raw streams go to `build/v3/validation`; mutation command
records are in each mutation directory. Never run two mutation jobs concurrently
in one checkout. Benchmark samples are observational and intentionally excluded
from deterministic snapshots.

The older validation scripts remain executable and unchanged. Their GitHub
workflows continue to run v0, v1, v2 and the separate survivor audit. Initial v3
phase-one replay of exact PR #2 is in `evidence/v3/phase1`. Do not overwrite older
evidence or count the original 18/2 mutants as 20/0.

Replay never re-signs data, generates replacement proofs, refetches live evidence
or manufactures receipts. New network observations belong in new directories.
The same assistant using a fresh checkout is not an independent human audit;
Node vs Python supplies an implementation cross-check for signatures. The native
proof uses the same pinned zkIE verifier, not a second proof implementation.
