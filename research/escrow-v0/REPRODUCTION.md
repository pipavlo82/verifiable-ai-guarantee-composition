# Reproduction

This experiment is committed locally only. No remote branch, pull request, network
deployment or transaction broadcast is part of the procedure. Clone the local Git
repository with `git clone --no-hardlinks <source> <fresh-directory>` and check out
the exact commit from the accompanying closure report. That report is outside the
commit so it can identify the commit and record its later fresh replay honestly.

Use Python 3.12.14, Node 22.15.0, Bun 1.3.14, Foundry 1.7.1 (commit
4072e48705af9d93e3c0f6e29e93b5e9a40caed8), solc 0.8.26, and the Rust toolchain
pinned by the existing native preparation script. Exact observed versions and
commands are preserved in the raw evidence; no faster-machine timing extrapolation
is justified. The initial checkout reused a verified native binary; the final fresh
replay builds the native adapter again from pinned source using a cached registry.

```text
python -B -X utf8 tools/v3/prepare.py --online
python -B -X utf8 tools/escrow_prepare.py --online
python -B -X utf8 tools/escrow_inventory.py
python -B -X utf8 experiments/verdict_escrow/validate.py --out build/escrow/replay
```

The first command prepares unchanged PR7 native and cryptographic dependencies.
For offline reproduction supply its `--cargo-home <cache>` and the pinned source
checkouts plus Node/Python dependency caches. `tools/escrow_prepare.py` also accepts
`--forge-std-cache <checkout>` and verifies every file against the 72-file lock.
The raw fresh-checkout transcript records the exact cache sources and commands used.
The proof verification itself runs again; cached results are not substituted.

Set `FORGE` if the executable is not at the documented default. Foundry FFI runs
the Python interpreter selected by the validator. The stock upstream harness copy
changes only interpreter selection from `python3` to `LAB_PYTHON`, with before/after
hashes recorded. The original vendored harness and contracts remain byte-identical.

The validator performs original seven escrow tests, a clean local integration
build, normal/repeated/optimized Python and EVM vectors, a separate Node Schnorr
and ABI-digest implementation, source mutations, PR7 regression tests/mutations,
source inventories and output determinism. `-O` affects the Python FFI and unit
tests; there is no fictitious Python optimization mode for Solidity itself.

Public runtime comparison can be repeated entirely offline:

```text
python -B -X utf8 tools/escrow_bytecode.py evidence/escrow-v0/public evidence/escrow-v0/compiler/VerdictGatedEscrow.json
```

That compiler artifact was produced from the original source at solc 0.8.26,
optimizer 200, without viaIR, and includes AST and immutable offsets. The recorded
immutable token/key values are substituted at those compiler offsets. The full
runtime, including metadata, is compared. The experimental test harness separately
uses viaIR to avoid stack-depth limits; it is not used to assert public-bytecode
identity. `evidence/escrow-v0/compiler` preserves the original compilation metadata.

Raw logs are immutable captures. The new SHA256 inventory covers the experiment
and its evidence; the original project inventory is deliberately not rewritten.
Development failures are labeled separately from the final successful matrix.

Fresh replay and local commit identifiers are recorded in the external closure
bundle. No GitHub CI run is claimed for an intentionally unpublished branch.
