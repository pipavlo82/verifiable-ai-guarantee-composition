# Executed pilot results

These are finite laboratory observations, not universal conformance or production guarantees. Original v0-v4.1, PR5-8, ERC-8404 and escrow evidence remains unchanged.

| Check | Result |
| --- | --- |
| Actual RVR verifier + external consumer | 18/18 expected scenario outcomes |
| Scoped authorization | 2 VERIFIED; 13 REFUTED; 3 UNVERIFIABLE |
| Transport/runner negative controls | 13/13, normal/repeat/Python `-O` |
| Pilot modes | normal/repeat/`-O`; identical projected semantic bytes |
| Frozen Core conformance | unchanged Python suite, normal and `-O` |
| Physical external-consumer mutations | 12 KILLED; 0 SURVIVED; 0 CRASHED; 0 NOT_APPLIED; 0 UNVERIFIABLE |
| Historical baseline | 11,872 inventoried file hashes unchanged |
| Second independently authored implementation | NOT_COVERED |

The positive claims authorize only the exact reviewed artifact identity. Negative cases that correctly refuse authorization are **conformant**, not failed tests. `missing_payload` preserves Core `CANNOT_RECOMPUTE` without a verification outcome. `contradictory_receipt` records `rvr.gate.result_projection_mismatch`, not a fabricated REFUTED Core outcome. `tampered_admission` keeps the valid internal decision but refuses the altered presented scope.

## Physical mutation evidence

Each row physically edits exactly one check in a disposable copy of the existing consumer, re-runs an isolated negative and positive witness through the harness, restores the exact original bytes and repeats both controls. The frozen Core is never mutated. A kill requires the intended negative to become an incorrect authorization, a valid positive, a determinate conformance failure and successful restoration. Crashes are classified separately.

| Removed check | Isolated negative | Classification |
| --- | --- | --- |
| Authorized recovered identity | wrong_authority | KILLED |
| Signed/requested subject equality | wrong_subject | KILLED |
| Signed scope/action | wrong_signed_scope | KILLED |
| Cross-component artifact equality | cross_component_loss | KILLED |
| Required key separation | self_judgment | KILLED |
| Requested claim type | unsupported_claim | KILLED |
| Recomputed contract/context commitment | mismatched_contract | KILLED |
| Signed policy commitment | wrong_signed_policy | KILLED |
| Unconsumed-field rejection | downstream_promotion | KILLED |
| Independently required O14 coverage | missing_independence_coverage | KILLED |
| Missing contract preimage refusal | missing_contract_preimage | KILLED |
| Fresh admission scope equality | tampered_admission | KILLED |

These are fresh executions against this transport and profile. They are not summed with any historical mutation report and do not establish coverage of every Core or transport branch.

## Reproduction

Use the [CLI commands](../../conformance/agent-harness-v0/README.md). `tools/harness_v0/validate.py` preserves exact argv, exit codes, runtime versions, raw stdout/stderr, raw requests/observations, deterministic projections, baseline/restored/mutated sources and evidence digests under its `--out` directory. Python `-O` is propagated into the Python pilot adapter; optimization is not merely applied to the outer command.

Committed [local validation evidence](../../evidence/harness-v0/validation/summary.json) records the local run. [The new CI workflow](../../.github/workflows/agent-harness-v0.yml) reproduces it on a fresh GitHub checkout and publishes raw results as an Actions artifact. A workflow definition is not itself evidence of a successful run; exact commit CI status must be checked separately. Existing nine research workflows are unchanged.

Development evidence preserves an incorrectly constructed missing-payload vector detected before final validation. It removed an unused field, leaving the committed payload available. The vector was corrected; no verifier semantics or expected normative requirement was weakened. The receipt projection witness was also narrowed to the actual `outcome` field and its exact gate reason. Neither event is an upstream finding.

Recommendation: **READY_FOR_INDEPENDENT_REVIEW** for this narrow pilot. Complete external-chain verification, broad ERC coverage and production execution authorization remain unsupported.
