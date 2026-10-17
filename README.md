# Verifiable AI Guarantee Composition

Independent experimental research by **pipavlo82** on the conditions under which
component guarantees can justify a downstream authorization claim.

## V3: public artifacts and explicit missing links

**PARTIAL_CHAIN_VERIFIED — full external chain remains unestablished.** V3 adds
three preserved externally published signatures checked by two implementations,
retained native zkIE replay, an actual unsigned local replay receipt, typed claim
dependency planning, 36 scenarios and 14 isolated killed mutations. The controlled
baseline authorizes 21/32 negative or unsupported requests; composition authorizes
0/32 and preserves 16 UNVERIFIABLE results. There are 19 v3 test methods per mode.

Read the [v3 report](research/V3_REAL_CHAIN_REPORT.md),
[paper draft](research/ACADEMIC_PAPER_DRAFT.md),
[prior-art comparison](research/PRIOR_ART_ANALYSIS.md), and
[exact blockers and acquisition plan](research/OPEN_PROOF_OBLIGATIONS.md).
V3 is based on unmerged draft PR #2; its historical results below remain intact.
No full-chain success, upstream vulnerability, general security guarantee or
scientific novelty is claimed.

## Preserved v2 report

**V2 verifies genuine laboratory signatures and retained native zkIE proof artifacts.
It does not establish a complete external WYRIWE -> zkIE -> judgment -> execution
chain. Historical execution remains UNVERIFIABLE. No upstream vulnerability,
security certification or scientific priority is claimed.**

The positive claim is deliberately narrow: a pinned public matrix operation's
output can be recomputed and is consistently referenced by laboratory attestations
under an explicit caller policy. The source-controlled profile uses exact bytes,
Keccak-256, real EIP-712/secp256k1 verification and a separate native proof verifier
process. The generated keys are laboratory authorities, not external issuer keys.

## Current results

**Survivor follow-up:** both original survivors are non-equivalent mutations masked
by additional failures in their original witnesses. Isolated cases now kill both;
7 additional tests pass in normal/repeat/`-O`. The production verifier is unchanged.
See the [audit and reproduction evidence](research/V2_SURVIVOR_AUDIT.md).
The table below preserves the original v2 experiment's results.

| Experiment | Observed result |
| --- | --- |
| Same-evidence v2 comparison | 26 scenarios: one narrow positive and 25 negative/unsupported claims |
| Independent component baseline | 18/25 negative cases falsely authorized |
| Explicit composition | 0/25 negative cases authorized; 4 UNVERIFIABLE classifications retained |
| Python v2 tests | 20 pass in normal, repeated and optimized runs |
| Executed source mutations | 18 KILLED, 2 SURVIVED, 0 CRASHED, 0 NOT_APPLIED |
| Unavailable integration check | 1 UNVERIFIABLE, unexecuted; not counted as a mutation |
| Native artifacts | Two retained 380-byte proofs; deserialized native verification and full output recomputation |
| Signatures | Ten genuine laboratory artifacts; external EIP-712 known-answer recovery also checked |

These numbers describe a controlled experiment against our deliberately incomplete
component-only baseline. They do not estimate real deployment exploit rates or
compare against upstream authorization software. The two surviving mutants are
retained in that original run, not retroactively counted as kills. The separate
follow-up reports 2 KILLED and 0 SURVIVED. No security advantage is generalized beyond these
specific witnesses. Full evidence is linked below.

- [Completed v2 experimental report](research/V2_REAL_ARTIFACT_REPORT.md)
- [Fresh-checkout reproduction](research/chain-v2/REPRODUCE.md)
- [Exact formats and trust boundaries](research/chain-v2/ARTIFACT_FORMATS.md)
- [Typed model and candidate propositions](research/chain-v2/FORMAL_MODEL.md)
- [Machine-readable results](evidence/v2/validation/report.json), [mutation evidence](evidence/v2/validation/mutations-normal.stdout.log), [integration status](evidence/v2/status.json)
- [Prior-art comparison](research/RELATED_WORK.md) and [paper outline](research/PAPER_OUTLINE.md)

## Version history and provenance

V0 (`905767f8696afe4cee612c8248f9d5d76f81f81b`) was an explicitly labeled synthetic
reconstruction: the requested original ZIP was unavailable and was never verified.
Its 21 scenarios, 19 tests and 8 killed controls remain preserved.

V1 (`ea89871064e98a67b6ba01c836d498bee89aa437`) added typed obligations, native library probes and an unrelated genuine
public signature. It did not provide a coherent real chain. V1 is an ancestor of
verified main `18a5916098addf6447700ed95441125bfa7079c3` (merge parents include the exact v1 SHA). Both main CI runs
passed; a fresh public clone reproduced v0/v1 before v2 began. See the
[phase-1 record](evidence/v2/phase1/report.json).

V2 is developed on `research/real-artifact-composition-v2` from that main. Its
experimental status is distinct from the frozen v0/v1 evidence. MIT covers our
original code; upstream source is fetched at pinned commits, not copied into the
repository. Dependency licenses remain applicable. No upstream repositories were
modified, no external researchers were contacted, and no merge is authorized.
