# V3 real evidence chain report

**PARTIAL_CHAIN_VERIFIED. Recommendation: HOLD_WITH_EXACT_BLOCKERS.**
This report establishes bounded real-artifact verification, not a complete
external WYRIWE -> zkIE -> judgment -> execution chain or an upstream vulnerability.

## Starting state and frozen history

Main observed: `18a5916098addf6447700ed95441125bfa7079c3`.
PR #2 observed head: `653b8e92e56afb99797c04b1c616a6d7fb3555e9`, open draft.
`ea89871064e98a67b6ba01c836d498bee89aa437` is an ancestor of main;
`git merge-base --is-ancestor` exited 0. A clean checkout of PR #2 independently
replayed the native build/tests, 26 scenarios, EIP-712 checks, normal/repeat/-O,
determinism, snapshot and 755-file inventory before/after.
Six GitHub CI runs at the exact PR #2 head were successful in the captured API
response. Raw phase-one commands and results are in `evidence/v3/phase1`, CI in
`evidence/v3/discovery/v2-ci.json`.

Original v2: **18 KILLED / 2 SURVIVED**. Subsequent survivor isolation:
**2 KILLED / 0 SURVIVED**, seven added tests per mode. These are separate
experiments; neither original evidence nor original production verifier is rewritten.

## Verified artifacts and exact scope

Three externally published signatures are independently checked by Node and
Python implementations: live ledger #236 Nostr event, upstream node1 Nostr CRC
cell, upstream node2 EIP-712 CRC cell. Event IDs, signatures, cell evidence hash,
decision preimage and claim preimages are recomputed. Accepted keys are explicit
caller policy, not an independently verified chain registry identity.
The signed judgment is **reject**, with source class **agent_reported** and an
explicit external-observation limitation. Agreement does not authorize the action.

The retained v2 laboratory zkIE proof is genuinely deserialized and verified by
the pinned native Rust verifier with public-output recomputation. Its native
statement is a public matrix tuple; this is not a private LLM inference claim.
The new unsigned local receipt preserves actual replay commands/results and has
a root checked through pinned ReceiptOS/Crystal and separate Python computation.
It is our receipt schema, not a claim of complete ReceiptOS issuance-schema
conformance. Root validity and subject equality do not attest historical truth.

Each artifact's original-byte SHA-256, source commit or live URL, producer,
authority, subject, scope, procedure, assumptions and execution grade is recorded
in `evidence/v3/artifact-catalog.json`. Exact source pins are in the linked audit.

## Results

| Check | Normal | Repeat | Python -O |
| --- | --- | --- | --- |
| v3 unittest methods | 19 pass | 19 pass | 19 pass |
| Same-evidence scenarios | 36/36 | 36/36 | 36/36 |
| Secondary signature checks | 3 valid + 2 invalid controls pass | same | same |
| Physical one-site mutations | 14 killed, 0 survived/crashed | same | same |
| Deterministic comparison/signature/mutation output | identical | identical | identical |

There are four narrow positive claims and 32 negative/unsupported requests.
The baseline falsely authorizes **21/32**, correctly refuses 11/32, and reports
6 UNVERIFIABLE. Explicit composition falsely authorizes **0/32**, correctly
refuses 32/32, and preserves **16 UNVERIFIABLE**. All declared classifications
match. Six unimplemented integration boundaries are **unexecuted**, not mutation
kills or coverage. Four positives do not combine into a positive external chain.

Mutation scripts physically replace one enforcement site, execute an isolated
negative, restore exact source bytes and re-run both negative/positive controls.
Crashes, missing executions and semantic nonchanges have separate classifications.
All command streams, exits and replacement hashes are retained.

## Runtime observation

Twelve paired, interleaved samples per case, milliseconds; both strategies
actually verify the same signatures and include fresh Node process startup.

| Case | Baseline median ms | Composition median ms | Difference ms |
| --- | --- | --- | --- |
| positive_claim_agreement | 159.448 | 160.468 | +1.020 |
| cross_subject | 161.576 | 160.402 | -1.174 |

This single-host measurement is dominated by startup and scheduling noise. It
does not establish a stable overhead bound, speed advantage or deployment security
rate. Raw samples are in `evidence/v3/validation/benchmark.stdout.log`.

## Missing links and reproducibility limits

The four full-chain blockers are WYRIWE admission to this input, external model
authorization, inference-to-judgment binding, and external execution evidence.
Historical CRC reproduction additionally lacks the signed original input bytes
and a resolvable historical execution witness. Outcome #236 returned HTTP404;
that is missing evidence, not a refutation of execution.

Setup failures are preserved separately: an initial local noble API integration
used hex strings where byte arrays were required; it was corrected before final
verification. Review-only Git text can have checkout line endings; its locks use
original Git blob bytes, while executed/preserved source locks use exact bytes.
No failed setup is counted as a successful verifier or mutant kill.

The published workflows reproduce v0/v1/v2 and v3; exact publication SHA, CI run
IDs and fresh-checkout evidence are recorded in the delivery report after push,
avoiding a self-referential commit identifier. Local replay by this same assistant
is not independent human review. Signature cross-checking uses different
implementations; native zkIE uses the same pinned implementation.

See [formal model](FORMAL_COMPOSITION_MODEL.md), [prior art](PRIOR_ART_ANALYSIS.md),
[paper draft](ACADEMIC_PAPER_DRAFT.md), [exact blockers/acquisition](OPEN_PROOF_OBLIGATIONS.md),
[source audit](v3/SOURCE_AND_ARTIFACT_AUDIT.md), [reproduction](v3/REPRODUCE.md).
