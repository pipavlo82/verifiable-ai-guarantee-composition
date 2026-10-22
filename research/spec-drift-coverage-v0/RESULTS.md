# Executed results

Recommendation: **INTEGRATE** as an additive bounded source-monitoring and evidence
reporting layer, after independent review. This is not permission to merge.

## Current source observations

Live GitHub observation at 2026-10-22T18:11:54.836197+00:00:

- ERC-8004: UPSTREAM_MOVED_CONTENT_UNCHANGED. Pin
  `503591a6e80e6e1affdd6403341e25269141f046`; observed master
  `3c0f7076cf20d70bdd6142f012d8e03322f4518c`. Exact file SHA-256 remains
  `249dc3d96ad7bbe4afd25cacd14be942eb87751abcf1608bab19a610f3c3f8a9`.
- ERC-8404 draft: UNCHANGED at `7a9e63a80bce04db53c6550103c1d41eca35f3d1`
  on `pipavlo82/ERCs:feat/rvr-erc-draft`.
- RVR v0 specification: UNCHANGED at `9dd36e882dd372f264b77b179130948aa5adcbde`
  on `pipavlo82/recomputable-verification-receipts:main`.

No normative byte change was observed in these configured sources. No pin was
updated and no historical execution result was invalidated. This is a timestamped
source observation, not an ongoing freshness guarantee or conformance verdict.

## Coverage reconstructed from preserved execution evidence

| Profile | Matched cases | Obligations | Specific enforcement mappings | Execution evidence only |
| --- | ---: | ---: | ---: | ---: |
| ERC-8404 original harness | 18 | 16 | 12 | 4 |
| ERC-8004 deterministic pilot | 29 | 17 | 17 | 0 |
| ERC-8004 generated corpus | 300 | 13 | 6 | 7 |
| PR11 supplemental sibling | 5 | 5 | 4 | 1 |

These are distinct profiles. There is no summed mutation campaign. Each of the
four populations remains separately 12/12, 17/17, 6/6 and 4/4 KILLED. All are
historical outcomes rechecked against actual source changes, case inputs, grader
observations, positive controls and restoration reports. The reporter does not
claim to have re-executed those physical mutants in this experiment.

PR12 retains all six 29-case comparisons: each mutant escaped the original matrix
and was distinguished by its generated witness. PR11's archived comparison against
the original 18 cases remains separately 1 KILLED / 4 SURVIVED (`original_18` in
its frozen `validation/normal/report.json`); it is not combined with the four
supplemental kills or imported as integrated code.

All 51 obligation records have independent replay NOT_COVERED. The 39 explicit
guard mappings establish finite sensitivity at those sites, not complete enforcement
of 39 entire requirements. The other 12 records are not upgraded merely because
their tests pass. Normative, implementation and research-policy entries remain distinct.

## Newly executed checks

- 32/32 deterministic research controls, normal and Python -O.
- 13/13 existing harness transport controls, normal and Python -O.
- Coverage JSON, drift JSON and Markdown checklist byte-identical across normal,
  repeat and optimized runs, using the retained source snapshot.
- Existing local ERC-8404 profile: 18/18 PASS; existing local ERC-8004 pilot: 29/29
  PASS. Correct refusal remains conformance PASS and authorization REFUTED.
- All 12703 PR12 inventoried files preserved; original inventory retained exactly.
  Core/history, integration history, ERC-8004 dependencies/source pins, PR12 source
  and package integrity, PR12 historical report consistency, and 631 PR11 archive
  member hashes pass. Harness transport and pinned recompute-kit bytes unchanged.

Raw command receipts, stdout/stderr, new native-profile reports and exact runtimes
are retained in `evidence/spec-drift-coverage-v0/RAW.zip`. SUMMARY.json describes
the local uncommitted validation phase with its exact research source seal, not a
retroactive claim of testing a later commit. Fresh-checkout and CI closure will be
recorded separately before publication. No independent reviewer result is inferred.
