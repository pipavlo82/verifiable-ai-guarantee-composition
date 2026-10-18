# Replay the preserved v4 experiment

Use a fresh checkout of the exact published v4 commit. The draft PR depends on
unmerged PR #3 at 98ffba16730030c797c47766e13a5314181ba2f6, itself descended from
PR #2 at 653b8e92e56afb99797c04b1c616a6d7fb3555e9. Main was
18a5916098addf6447700ed95441125bfa7079c3. Review the v4-only diff from the PR #3 SHA.
No historical evidence or old PR branch is rewritten.

Requirements: Python 3.12, Node 22.15.0, Bun 1.3.14, Rust 1.97.1, Git and the
published hash-locked dependencies. Network is needed once to prepare dependencies;
verification itself replays local frozen evidence. No private keys or provider API
tokens are required. Do not run the one-time laboratory issuance script on a replay.

```sh
python -B tools/verify_artifacts.py
python -B tools/v3/prepare.py --online
python -B tools/v4/verify_sources.py
python -B tools/v4/validate.py
python -B tools/verify_artifacts.py
git status --porcelain
```

validate.py runs normal, repeat and Python -O tests, scenario comparisons, a
different EIP-712 implementation, actual physical mutations and determinism
checks. It preserves commands, exits, stdout/stderr and hashes under
build/v4/validation. Native preparation rebuilds and tests the pinned Rust wrapper.
The comparison snapshot must match evidence/v4/validation. Timing is excluded
from deterministic equality. Raw command paths legitimately vary by host.

For a focused witness:

```sh
python -B tools/v4/run.py --case omitted_O05 --raw
python -B tools/v4/run.py --case positive_output --raw
python -B tools/v4/secondary.py
python -B tools/v4/mutations.py --out build/v4/manual-mutations
```

Mutation runners physically edit their own checkout and restore exact bytes in
finally blocks. Run them sequentially, never concurrently in the same checkout.
They intentionally record exit 1 from an oracle mismatch; this differs from a
crash. A killed mutation requires the specified behavioral witness and restored
positive/negative controls.

Historical reproduction commands:

```sh
python -B tools/validate.py --out build/v4/history/v0
python -B research/formal-v1/validate.py --out build/v4/history/v1
python -B tools/v2/validate.py --out build/v4/history/v2 --skip-benchmark
python -B tools/v2/check_snapshot.py --out build/v4/history/v2
python -B tools/v2/validate_survivors.py --out build/v4/history/v2-survivors
python -B tools/v3/validate.py --out build/v4/history/v3 --skip-benchmark
```

The immutable original v2 result is 18 killed / 2 surviving mutants. The subsequent
isolated controls are a separate 2 killed / 0 surviving result. Do not combine
them into a rewritten historical report. The v4 initial development run likewise
retains its 13 generator crashes, separately from the corrected final experiment.
