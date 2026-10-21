# Status and preserved research history

Snapshot independently checked on **2026-10-21** against repository
`trustless-ai/verifiable-execution-claim-authorization` (GitHub repository ID `1422280233`).
The verified main HEAD is
[`2e329fffbee103047d034b97056aea9e49cf1c58`](https://github.com/trustless-ai/verifiable-execution-claim-authorization/commit/2e329fffbee103047d034b97056aea9e49cf1c58),
tree `a0eee6da5c85f52c0276f0a049d9689a2b26ebe4`.
This documentation proposal is on `docs/project-roadmap-p0-p5`. It does not advance main or
assert that its own review/CI is complete; see the branch's exact-commit Actions.

## Status vocabulary and supported scope

Use the [five roadmap labels](../ROADMAP.md) separately from runtime decisions.

| Area | Status | Evidence or outstanding boundary |
| --- | --- | --- |
| Coverage, composition, O14 and admission research code | IMPLEMENTED | Inspectable implementations and preserved reports linked below |
| Joint integration and local escrow experiments | EXPERIMENTALLY VERIFIED | Finite scenarios, native proof/signature checks, mutations and fresh CI replay |
| External provenance-to-execution chain | PARTIALLY VERIFIED | Genuine components exist; required admission, authority and external execution bindings remain missing |
| Stable reusable engine, general community harness and additional adapters | PLANNED | P1–P3 acceptance criteria are not completed by existing experiment-specific runners |
| Arbitrary execution authorization, controller independence from key inequality, full external-chain success | UNSUPPORTED | These guarantees are not established by the current profile |

The exact current integration claim is `LAB_REPLAY_AND_REVIEWED_PROOF_IDENTITY`
with scope `local-output-replay-and-proof-byte-review`. It combines local-output
replay and authenticated review of exact proof bytes; it is not a general execution
permission. **LABORATORY_VERIFIED / PARTIAL_CHAIN_VERIFIED** remains the guarantee
level. Escrow compatibility is **PARTIALLY_COMPATIBLE**; production payments are
**HOLD**. [Architecture](ARCHITECTURE.md) explains the boundaries.

## Merged PRs and ancestry

All eight PRs returned MERGED in the GitHub API. Their head and recorded merge
commits are ancestors of the verified main, independently checked with
`git merge-base --is-ancestor`. These are historical integration facts, not proof
of academic approval, product readiness or completion of the roadmap.

| PR | Recorded head SHA | Recorded merge commit SHA |
| --- | --- | --- |
| [#1](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/1) | `ea89871064e98a67b6ba01c836d498bee89aa437` | `18a5916098addf6447700ed95441125bfa7079c3` |
| [#2](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/2) | `653b8e92e56afb99797c04b1c616a6d7fb3555e9` | `653b8e92e56afb99797c04b1c616a6d7fb3555e9` |
| [#3](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/3) | `98ffba16730030c797c47766e13a5314181ba2f6` | `98ffba16730030c797c47766e13a5314181ba2f6` |
| [#4](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/4) | `ee1143f2b8f669a88f36c736d20bb86c2ade950a` | `ee1143f2b8f669a88f36c736d20bb86c2ade950a` |
| [#5](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/5) | `c14d96b0a63fceba02b2cb4469d5b3228ae46612` | `ed298cc6a3d0215343be04b490b8f6343b05c098` |
| [#6](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/6) | `b0e894db53d58370df0d9959e070a1302f4a5787` | `b0e894db53d58370df0d9959e070a1302f4a5787` |
| [#7](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/7) | `c93087f06bd14c45a1d12b0c068195e3bef05dae` | `c93087f06bd14c45a1d12b0c068195e3bef05dae` |
| [#8](https://github.com/trustless-ai/verifiable-execution-claim-authorization/pull/8) | `ed298cc6a3d0215343be04b490b8f6343b05c098` | `3d55a8456dddb3cb981c91b143761e87e31d7531` |

PR #1 merged on 2026-10-16; PR #2–#8 merged on 2026-10-21. GitHub recognizes
several stacked ancestors as merged; their `merge_commit_sha` can equal the PR
head. #5's recorded merge is #8's final branch head. The combined main merge was
`3d55a8456dddb3cb981c91b143761e87e31d7531`; the later documentation refresh is
the verified HEAD above. Transfer preserved repository identity, Git history and PRs.

## Exact-HEAD baseline CI

All **9 workflow runs** below completed successfully with `head_sha` equal to
`2e329fffbee103047d034b97056aea9e49cf1c58`. The v0 workflow has two jobs; workflow and job counts are different.
These links identify this baseline, not an evergreen claim about future main.

| Workflow/run | Observed conclusion |
| --- | --- |
| [Reproduce research](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758727) | SUCCESS |
| [Typed composition research v1](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758832) | SUCCESS |
| [Real artifact composition v2](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758582) | SUCCESS |
| [Real evidence chain v3](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758828) | SUCCESS |
| [ERC8404 external consumer compatibility](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758623) | SUCCESS |
| [Verification obligation coverage v4](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758519) | SUCCESS |
| [Checker independence and C binding v4.1](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758388) | SUCCESS |
| [Claim-aware integration independent replay](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758361) | SUCCESS |
| [Claim-aware verdict escrow independent replay](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions/runs/39683758691) | SUCCESS |

For a new candidate, inspect its exact SHA through
[Actions](https://github.com/trustless-ai/verifiable-execution-claim-authorization/actions) and the
[reproduction guide](REPRODUCIBILITY.md). CI demonstrates executed checks under
their configured environments; it does not constitute independent human review.

## Finite experimental results

The following are preserved results whose replay workflows are green at the
baseline. They are separate experiments with different denominators, not a pooled
security score or an estimate of real-world exploit frequency.

| Experiment | Scenarios | Applied mutations | Unsupported downstream authorizations |
| --- | --- | --- | --- |
| [Joint integration](../research/integration/EXPERIMENT_RESULTS.md) | 61: 2 positive, 59 negative/unsupported | 22 KILLED / 0 SURVIVED / 0 CRASHED | A component-only: 51/59; B declared: 13/59; C scenario-complete: 0/59; D independently recomputed admission: 0/59 |
| [Verdict escrow](../research/escrow-v0/EXPERIMENT_RESULTS.md) | 31 expected outcomes: 1 positive, 28 authorization-negative, 2 token-execution controls | 22 KILLED / 0 SURVIVED / 0 CRASHED; 6 absent on-chain checks NOT_APPLIED | A signature only: 24/28; B claim-aware issuance: 2/28; C issuance plus existing on-chain enforcement: 2/28 |

Escrow's two remaining cases are expiration and signer revocation **after signing**.
They are observed gaps relative to the selected research policy, not surviving
mutants or automatically violations of the upstream contract's narrower documented
guarantees. Its positive execution transfers a local mock token; it proves no
external payment. The adapter is not mandatory at the existing contract boundary.

See the [integration mutation report](../research/integration/MUTATION_REPORT.md),
[escrow mutation report](../research/escrow-v0/MUTATION_REPORT.md),
[integration machine-readable report](../evidence/integration/validation/report.json)
and [escrow evidence](../evidence/escrow-v0/).

## Historical record

| Stage | Preserved reference and interpretation |
| --- | --- |
| v0 | [Research question](../research/RESEARCH_QUESTION.md) and [paper outline](../research/PAPER_OUTLINE.md). The missing original ZIP was not verified; the fixture was explicitly reconstructed. |
| v1 / PR #1 | [Guarantee model](../research/GUARANTEE_MODEL.md) and [composition rules](../research/COMPOSITION_RULES.md): typed obligations and scoped claims. |
| v2 / PR #2 | [Real-artifact report](../research/V2_REAL_ARTIFACT_REPORT.md): original 18 KILLED / 2 SURVIVED remains historical; the [survivor audit](../research/V2_SURVIVOR_AUDIT.md) records a separate isolated 2/0 result. |
| v3 / PR #3 | [Real-chain report](../research/V3_REAL_CHAIN_REPORT.md): genuine components and explicit missing links. |
| v4 / PR #4 | [Coverage results](../research/v4/RESULTS.md): scenario-relative obligation coverage; not proof of universally adequate contracts. |
| v4.1 / PR #5 | [O14 and scope](../research/v4_1/README.md): scenario-dependent independence and consumer admission fixes. |
| ERC-8404 / PR #6 | [Compatibility report](../research/erc8404/EXPERIMENT_RESULTS.md): original 16 KILLED / 1 SURVIVED; later [fallback isolation](../research/integration/MUTATION_REPORT.md) remains a distinct experiment. |
| Integration / PR #7 | [Engine report](../research/integration/CLAIM_AWARE_ENGINE.md) and [academic addendum](../research/integration/ACADEMIC_PAPER_DRAFT.md). |
| Escrow / PR #8 | [Technical report](../research/escrow-v0/REPORT.md), preserved failures, inventory repair and local enforcement evidence. |

Historical text saying Draft, unmerged or awaiting publication describes its own
snapshot. It is retained rather than rewritten after merge. No original report,
raw evidence, conformance vector, source lock, license or implementation is changed
by this documentation branch. The current whole-tree inventory is extended only
for the new documentation; existing entries remain identical.

## Remaining limits

Contract adequacy, original input admission, authorized model identity, judgment
truth, real-world controller separation and authoritative external execution require
additional evidence. An authentic signature or digest match does not establish them.
No full-chain verification, production readiness or scientific novelty is claimed.

Read [integration limitations](../research/integration/LIMITATIONS.md),
[escrow limitations](../research/escrow-v0/LIMITATIONS.md),
[open proof obligations](../research/OPEN_PROOF_OBLIGATIONS.md) and
[prior art](../research/PRIOR_ART_ANALYSIS.md). The [roadmap](../ROADMAP.md)
defines what must be demonstrated before expanding the supported scope.
