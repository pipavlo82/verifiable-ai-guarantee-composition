# Experimental results

Recommendation: **COMPATIBLE_WITH_FROZEN_CORE**, limited to the external consumer.
No full real execution-chain claim is made.

## Verified starting state

Main: 18a5916098addf6447700ed95441125bfa7079c3.
PR2: 653b8e92e56afb99797c04b1c616a6d7fb3555e9.
PR3: 98ffba16730030c797c47766e13a5314181ba2f6.
PR4: ee1143f2b8f669a88f36c736d20bb86c2ade950a.
The ancestry checks establish main -> PR2 -> PR3 -> PR4. Their published
workflow results were captured in starting-state.json. The new branch starts
at PR4 and preserves all prior implementation/evidence bytes, apart from README
navigation and .gitattributes additions plus the regenerated aggregate inventory.

## New experiment

45 scenarios; four positive controls. The Python suite has
17 tests
in each normal/repeat/optimized run. All pass. Comparison, secondary signature
results and physical mutation reports are byte-deterministic across all three.

| Mode | Incorrect downstream authorizations | Correct refusals | UNVERIFIABLE | Missing-obligation detections |
|---|---:|---:|---:|---:|
| A | 38 | 3 | 1 | 0 |
| B | 18 | 23 | 7 | 0 |
| C | 0 | 41 | 6 | 8 |

All modes receive identical inputs. A executes the exact RVR procedure; B adds
declared obligations; C adds independent contract coverage and scoped composition.
A and B are deliberately incomplete *downstream consumer policies*. No result
here says that a narrower RVR receipt is defective or falsely verified.
All four positive controls authorize their explicitly restricted scope.

Mutation counts: {"CRASHED": 0, "KILLED": 17, "NOT_APPLIED": 0, "SURVIVED": 0, "UNVERIFIABLE": 0}.
Every claimed kill has an isolated baseline refusal, incorrect authorization
under a physically modified source copy, restored refusal and restored positive
control. Frozen Core is never mutated. No surviving mutant is hidden; no crash
is counted as killed. This is the listed consumer-boundary inventory, not
exhaustive crypto/Core coverage.

64 preserved genuine laboratory signatures were recovered
by the second eth-account implementation; a changed-message control is rejected.
Historical native proof verification is separate from RVR byte identity.
The source bytes and the 13 vendored Core files remain identical; all 75 tracked
upstream files match the initial inventory. The formal draft SHA-256 matches.

## Historical reproduction

Normal/repeat/-O historical suites: v0 19 tests, v1 11, v2 20,
v2 survivor isolation 7, v3 19, v4 24. Historical mutations retain their meaning:
v0 8 killed; v1 4 killed; original v2 18 killed/2 survived; subsequent isolated
v2 controls 2 killed/0 survived; v3 14 killed; v4 44 killed/0 survived.
Raw replay logs are in evidence/erc8404/history-replay. Existing historical
evidence is preserved separately and never rewritten with the new counts.

The preliminary repository-wide inventory check at the end of discovery saw new
research files added concurrently. This was an inventory-update mismatch, not
historical artifact drift. The original-file inventory is independently rechecked;
the new aggregate inventory is regenerated and verified before publication.

## Timing

Local medians in milliseconds, 12 positive runs per mode:
{"A": 8.90845, "B": 216.3979, "C": 208.7679}.
C minus B: -7.630000 ms;
C minus A: 199.859450 ms.
This includes Node subprocess startup for B/C, excludes warmed Python import,
and is a finite local observation, not a portable performance claim or advantage.
Raw nanosecond samples and environment are preserved.

## Development observations and final reproduction

The first exploratory mutation run had 15 killed and one UNVERIFIABLE receipt
control because an independent artifact-binding check also failed. It is retained
under development; subsequent isolation preserves the candidate claim diagnostic
without accepting the rejected receipt. An exploratory validation also detected
secondary-output drift while new signature fixtures were added. It is retained
as failed development evidence. The final frozen-fixture normal/repeat/-O run
passes all deterministic comparisons. These events do not change v0-v4 history.
An intermediate authority mutant was UNVERIFIABLE as an isolation experiment
because O14 independently rejected the same unauthorized signer. Its raw result
is retained. The final authority witness uses the scenario where separation is
not required; it isolates authority enforcement without weakening O14.

Fresh published-checkout replay and exact-head GitHub CI evidence are added to
the delivery report after the publication commit exists; they cannot truthfully
be predeclared inside that same commit. No end-to-end external-chain completion,
scientific novelty or upstream vulnerability is claimed.
