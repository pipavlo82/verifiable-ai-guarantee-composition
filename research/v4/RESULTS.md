# V4 results: scenario-relative verification obligation coverage

Recommendation: **READY_FOR_INDEPENDENT_REVIEW** of this bounded experiment.
External-chain status: **PARTIAL_CHAIN_VERIFIED**. Contract adequacy, scientific
novelty and complete external execution remain unestablished.

## Verified starting state

Main: `18a5916098addf6447700ed95441125bfa7079c3`.
PR #2: `653b8e92e56afb99797c04b1c616a6d7fb3555e9`.
PR #3 / v4 base: `98ffba16730030c797c47766e13a5314181ba2f6`.
Git ancestry main -> PR2 -> PR3 passed; v1
`ea89871064e98a67b6ba01c836d498bee89aa437` is an ancestor of main.
The prior exact-head CI was successful. Isolated fresh baseline replay preserved
every historical file. V4 is additive except README navigation, the paper addendum,
raw-evidence Git attributes and the aggregate hash inventory.

## Test matrix

| Suite | Normal | Repeat | Python -O | Mutation result |
| --- | ---: | ---: | ---: | --- |
| v0 | 19 pass | 19 pass | 19 pass | 8 killed |
| v1 | 11 pass | 11 pass | 11 pass | 4 killed |
| v2 original | 20 pass | 20 pass | 20 pass | 18 killed / 2 survived, unchanged |
| v2 survivor isolation | 7 pass | 7 pass | 7 pass | separate 2 killed / 0 survived |
| v3 | 19 pass | 19 pass | 19 pass | 14 killed |
| v4 | 24 pass | 24 pass | 24 pass | 44 killed / 0 survived in each mode |

Native preparation rebuilds the pinned Rust verifier and runs two exact native
tests. The retained proof is separately verified in actual scenario subprocesses.
V4 has 54 fixed-oracle scenarios: 4 positive and 50 negative/unsupported. All pass.
Comparison, mutation and secondary-crypto outputs are byte-identical across the
three modes; timing and host-specific command logs are excluded from equality.
Ten laboratory signed documents pass the separate eth-account implementation;
altered-message and invalid-signature controls fail, and Python independently
recomputes the public MatMul output and raw keccak commitment.

## Same-evidence comparison

| Baseline | False authorizations / 50 | Correct refusals / 50 | UNVERIFIABLE | Positive authorizations / 4 |
| --- | ---: | ---: | ---: | ---: |
| A: components only | 41 | 9 | 5 | 4 |
| B: declared obligations | 21 | 29 | 14 | 4 |
| C: independent scenario contract + obligations + composition | 0 | 50 | 16 | 4 |

Missing-obligation detection: **13/13**. In every omission case all remaining
declared checks pass. Known absence from the required inventory refutes the
coverage claim; missing actual evidence remains unknown. These are deliberately
constructed finite controls, not real-world vulnerability or security-rate estimates.

## Mutation survival

Final: KILLED 44, SURVIVED 0, CRASHED 0, NOT_APPLIED 0, UNVERIFIABLE 0.
Thirteen physical catalog deletions are detected through coverage alarms and
refusal; they do not cause unsafe authorization. Thirteen coverage-enforcement
removals, thirteen evidence-enforcement removals and five guard removals make
their intended unsupported request authorized and are killed by their fixed
oracle. Exact restoration and positive controls pass. Crashes are never kills.

The initial development run is preserved in evidence/v4/development-run1:
31 killed and 13 CRASHED. The generator initially attempted to delete already
missing catalog entries while constructing unrelated cases. It was corrected to
allow physical deletion witnesses to reach the evaluator. The final evidence is
a new run, not a rewrite of those crashes or the historical v2 survivors.

## Finite timing observation

Windows Python 3.12.14, 54 inputs, 7 alternating-order decision samples per input. Shared actual crypto/native collection median: 185.041700 ms. Decision-only medians: A 0.006100 ms; B 0.422250 ms; C 0.448000 ms. C minus B median difference: 0.025750 ms. Shared crypto is collected once per input and reported separately, so these are not end-to-end independent benchmark timings. Raw samples are preserved. No performance extrapolation is made.

## Evidence and reproduction

[Machine report](../../evidence/v4/validation/report.json),
[comparison](../../evidence/v4/validation/comparison-normal.stdout.log),
[mutations](../../evidence/v4/validation/mutations-normal/report.json),
[secondary crypto](../../evidence/v4/validation/secondary-normal.stdout.log),
[prior replay](../../evidence/v4/prior-reproduction), and
[reproduction commands](REPRODUCE.md).

The initial capture's snapshot_match field compares its just-written capture and
is not independent reproduction evidence. The required subsequent fresh public
checkout and GitHub CI compare against these frozen committed bytes. Exact-head
postpublication results and raw logs are recorded separately to avoid a
self-referential commit. The pinned CI workflow executes v4 alongside unchanged
v0–v3 workflows. The final delivery identifies the exact verified head and runs.

Scientific scope: no full-chain success, official ERC/Trustless AI endorsement,
upstream vulnerability, global requirements-completeness theorem, organizational
independence or scientific novelty claim. Review the formal assumptions and prior
art before interpreting the finite outcomes more broadly.
