# Reproducibility

Use a fresh checkout with complete Git history: baseline checks read pinned ancestor
commits. The [status snapshot](STATUS.md) identifies the verified baseline. Run from
the repository root, record your exact HEAD and preserve outputs under ignored
`build/` or outside the repository. Existing `evidence/` is historical input, not an
output directory to overwrite.

## Baseline and synthetic experiment

```sh
git clone https://github.com/trustless-ai/verifiable-execution-claim-authorization.git
cd verifiable-execution-claim-authorization
git checkout --detach 2e329fffbee103047d034b97056aea9e49cf1c58
git rev-parse HEAD
python -B tools/verify_artifacts.py
python -B tools/validate.py
```

Use Python 3.12. To review a documentation or implementation candidate, check out its
exact commit instead and record that SHA. `tools/validate.py` reproduces the v0
synthetic experiment, normal/repeat/optimized tests, mutations and semantic
determinism; it does not verify the real external chain. Logs: `build/validation/`.

## Native proof and joint integration

Install Node 22.15.0, Bun 1.3.14 and Rust 1.97.1 in addition to Python 3.12:

```sh
rustup override set 1.97.1
python -B tools/v3/prepare.py --online
python -B tools/integration/validate.py
python -B tools/verify_artifacts.py
```

Preparation fetches pinned dependencies and builds the native verifier. It does not
generate a replacement proof. The runner preserves commands, exit codes, tests,
scenarios, cryptographic verification, mutations and deterministic semantic reports
under `build/integration/validation/`.

## Local verdict-escrow experiment

After native integration preparation, install Foundry 1.7.1. The harness uses solc
0.8.26. Reproduce the locked dependency representation in a fresh `build/`:

```sh
git -c core.autocrlf=true clone --no-checkout https://github.com/foundry-rs/forge-std.git build/escrow/forge-std-source
git -C build/escrow/forge-std-source -c core.autocrlf=true checkout --detach b013eff2ac4fce26f34d789e6f5c49021c5ee817
python -B tools/escrow_prepare.py --forge-std-cache build/escrow/forge-std-source
python -B -X utf8 tools/escrow_ci.py
python -B tools/verify_artifacts.py
```

The checkout setting reproduces the frozen forge-std bytes; newly authored technical
text in this repository uses LF. The runner exercises local EVM/mock-token release,
Python normal/repeat/-O, mutations, evidence integrity, determinism and baseline/CI
negative controls. It requires no production keys, broadcast or real funds. Logs:
`build/escrow/ci/`. Gas measurements describe that exact local environment.

## Documentation and preservation checks

```sh
git diff --check
python -B tools/verify_artifacts.py
python -B tools/integration/integrity.py
python -B tools/erc8404/integrity.py
python -B -c "import json; from experiments.verdict_escrow.integrity import check; r=check(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['passed'] else 1)"
```

For documentation changes, also resolve every added relative path/heading link,
check LF/no-BOM/final-newline formatting, and compare the complete Git diff against
the base. Only documentation and the canonical current inventory may change in a
documentation-only contribution; source locks, implementation, licenses and
historical evidence remain unchanged. Render Markdown to inspect tables/code blocks.

The complete current inventory is `artifacts.sha256.json`. An intentional addition
can be indexed with `python -B tools/verify_artifacts.py --write` **only after**
independently confirming the exact change set. Confirm all prior entries retain
their hashes. Never regenerate a manifest to conceal an unexplained mismatch.

The root README is pinned by the escrow baseline. This documentation branch adds
`.github/README.md` as the displayed entry point and preserves the pinned root
README and historical snapshots byte-for-byte. No implementation exception is added.

## CI and independent review

The nine unchanged [workflows](../.github/workflows/) cover v0, v1, v2, v3, v4,
v4.1, ERC-8404 compatibility, joint integration and escrow. Read exact-commit
outcomes; a green run on a parent commit is not evidence for its descendant.
CI infrastructure errors and unavailable tools are not successful verification.

An independent report should record OS/runtime versions, exact source and candidate
SHAs, command lines, exit codes, artifact SHA-256 values, scenario denominators,
mutation classifications and unresolved dependencies. Timing fields are not expected
to be byte-identical; semantic outputs must meet each runner's determinism contract.

Use the preserved [integration checklist](../research/integration/INDEPENDENT_REVIEW_CHECKLIST.md)
and [escrow checklist](../research/escrow-v0/INDEPENDENT_REVIEW_CHECKLIST.md), while
reading their old draft/publication statements as historical context. New review
findings belong in a new report, not edits to the original evidence.
