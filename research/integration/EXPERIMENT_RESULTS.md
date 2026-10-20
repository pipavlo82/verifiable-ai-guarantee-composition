# Finite integration experiment

The predeclared claim experiment contains **61 scenarios: 2 positives and 59
negative/unsupported requests**. Expectations are stated independently in
`src/integration/cases.py`, not generated from actual verdicts.

| Mode | False authorizations / 59 | Correct refusals | UNVERIFIABLE / 61 | Positives accepted / 2 | Missing-obligation detections |
|---|---:|---:|---:|---:|---:|
| A: component result lifting | 51 | 8 | 4 | 2 | 0 |
| B: declared joint checks | 13 | 46 | 16 | 2 | 0 |
| C: scenario-complete composition | 0 | 59 | 16 | 2 | 10 |
| D: independently recomputed admission | 0 | 59 | 16 | 2 | 10 |

The same evidence and requested claim are used for each row. A and B intentionally
lift narrower component/declared guarantees to the requested downstream claim. This
is not an allegation that either upstream implementation violates its own scope.
Mode A actually checks native proof validity, all five role signatures and the RVR
receipt independently; it does not require the joint contract carrier. It consumes
no cross-artifact or authority/scope relationship. It is not implemented as a trusted
boolean flag or as receipt verification with signature checks silently omitted.
REFUTED and UNVERIFIABLE both refuse authorization but remain distinct outcomes.

The D path here receives the corresponding C record. Record tampering is measured
separately by `tools/integration/admission.py`; otherwise a correct claim decision
could be mislabeled as a false authorization merely because an unrelated presented
record was edited. The separate controls cover flags/status, scenario/type/contract
reuse, policy changes, evidence refs, numeric flags, missing identities and unconsumed
output claims under narrower contracts.

The joint suite has 16 unittest methods, including subtests over all 61 scenarios.
Normal/repeated/optimized executions compare deterministic machine-readable outputs.
Source-copy mutation results, exact commands, exit codes, crypto/native output and
Core conformance output accompany the report. Timings in `benchmark.stdout.log`
measure this unoptimized implementation, including shared verification work and
subprocess startup; they are not an estimate of an optimized baseline's overhead.

See `evidence/integration/validation/report.json` for the executed matrix and
`evidence/integration/pr5/` / `pr6/` for independent source-branch replays. Final
public-commit replay and GitHub CI are additionally checked after publication; those
results identify the exact commit and do not retroactively change historical evidence.

Research verdict: the explicit laboratory conjunction is suitable for independent
review once the published commit's replay and CI succeed. The complete external chain
remains PARTIAL_CHAIN_VERIFIED. No production-readiness or novelty claim follows.

Measured local timing (one pass; not a universal performance claim):

- A: 21.899 s total, 0.359000 s/fixture, n=61.
- B: 29.900 s total, 0.490163 s/fixture, n=61.
- C: 30.106 s total, 0.493535 s/fixture, n=61.
- D: 29.984 s total, 0.491548 s/fixture, n=61.

The first secondary-signature negative control incorrectly altered an undeclared provenance field. Its failed run is preserved; the corrected control alters signed LabJudgment.subject and passes. This correction changed the test premise, not the verifier.
