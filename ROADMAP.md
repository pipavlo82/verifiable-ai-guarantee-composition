# Roadmap P0–P5

The goal is to determine which claims evidence can authorize and test whether
implementations preserve those boundaries. The starting point is a set of finite,
reproducible research experiments, not a general execution-authorization service.
The [status snapshot](docs/STATUS.md) fixes the baseline and evidence behind this
roadmap. Milestones are acceptance gates, not release dates or assigned commitments.

## How to read status

| Label | Meaning |
| --- | --- |
| IMPLEMENTED | Inspectable code or documentation exists at the referenced version; this alone says nothing about successful verification. |
| EXPERIMENTALLY VERIFIED | The named procedure ran with preserved inputs, expected results and execution evidence, within a stated finite scope. |
| PARTIALLY VERIFIED | Some required evidence or cross-component bindings are established; the remaining gaps are explicit. |
| PLANNED | Proposed work or acceptance criteria; no implementation or verification is implied. |
| UNSUPPORTED | The current profile does not establish this guarantee. It must not be inferred from another successful check. |

These labels describe different properties, not a total order. `VERIFIED`,
`REFUTED` and `UNVERIFIABLE` are runtime decision states; they are not roadmap
completion labels. Every milestone below remains **open** until all of its criteria
have recorded evidence and review. Existing results satisfy only the cited parts.

## P0 — Repository Foundation

**Current:** IMPLEMENTED repository and preserved history; EXPERIMENTALLY VERIFIED
baseline integrity and exact-HEAD CI; this documentation organization is proposed
on an isolated branch. **Milestone: open.**

Acceptance criteria:

- [ ] Review and merge a concise entry README, architecture, status, integration map,
  reproducibility guide and contribution guide, with resolving links.
- [ ] Record the accepted commit, all merged research PR heads and merge commits,
  and successful CI on that exact commit; distinguish later CI from old reports.
- [ ] Recompute the full file inventory, confirm every historical evidence/source
  pin and license is unchanged, and retain raw commands and exit codes.
- [ ] Demonstrate the documented fresh-checkout commands in CI; clearly name
  external dependencies, non-executed checks and the narrow claim scope.

Existing evidence: [baseline and CI](docs/STATUS.md),
[preservation rules](CONTRIBUTING.md), [replay guide](docs/REPRODUCIBILITY.md).
No new governance agreement is a prerequisite invented by this roadmap.

## P1 — Reusable Claim-Aware Verification Engine

**Current:** IMPLEMENTED bounded research engine; EXPERIMENTALLY VERIFIED integration
fixtures. A stable reusable engine interface is PLANNED. **Milestone: open.**

Acceptance criteria:

- [ ] Publish a versioned input/output contract for claims, scenario bytes,
  evidence references, profile identity, decisions and exact authorization scope.
- [ ] Obtain required obligations from an independently supplied scenario contract;
  reject stale, missing or unknown requirements and document contract-adequacy assumptions.
- [ ] Recompute contract/evidence commitments from exact preimages; preserve
  REFUTED versus UNVERIFIABLE and disclose unconsumed fields.
- [ ] Preserve scenario-dependent O14 and identity namespaces; do not treat distinct
  keys as proof of different controllers. Admission must independently recompute results.
- [ ] Reproduce all historical integration outcomes unchanged, plus positive,
  negative, missing-evidence and load-bearing mutation controls for each new boundary.
- [ ] Demonstrate a second claim profile through the same versioned interface without
  copying the core decision logic; publish its different assumptions and unsupported fields.

Existing evidence: [engine contract](research/integration/CLAIM_AWARE_ENGINE.md),
[61-scenario experiment](research/integration/EXPERIMENT_RESULTS.md).

## P2 — Community Agent Conformance Harness

**Current:** IMPLEMENTED experiment-specific vectors, runners and mutation tools;
general cross-implementation harness PLANNED. **Milestone: open.**

Acceptance criteria:

- [ ] Define a versioned adapter protocol with explicit setup, execution, evidence,
  timeout and failure classifications; an unavailable adapter must not pass.
- [ ] Keep normative ERC requirements, selected research policies, independent
  expected outcomes and observed implementation outcomes separately identifiable.
- [ ] Evaluate at least two independently implemented targets through the same
  harness; disclose shared code, authorship and oracle assumptions rather than
  inferring independence from different languages or processes.
- [ ] Pin scenario contracts and expected vectors independently of target output.
  Include omission, stale-policy, scope-upgrade and unverified-field witnesses.
- [ ] Show that each supported boundary can fail using a mapped mutation and valid
  positive control; report SURVIVED, CRASHED, NOT_APPLIED and UNVERIFIABLE explicitly.
- [ ] Publish a fresh replay by a reviewer outside the implementation workflow,
  including commands, exact commits and disagreements or unavailable checks.

Coordinate through documented external interfaces with
[Semantic ABI, RSI and recompute-kit](docs/INTEGRATIONS.md). This milestone does
not propose rebuilding or absorbing their existing semantic and conformance work.

## P3 — Real Implementation Adapters

**Current:** PARTIALLY VERIFIED native-proof, signature, receipt and escrow research
integrations. General interoperable adapters are PLANNED. **Milestone: open.**

Acceptance criteria:

- [ ] For each admitted adapter, pin source/toolchain versions, formats, licenses,
  original artifact bytes and digests, producer identity and verification authority.
- [ ] Verify actual artifacts using their native verification procedures; a test
  flag or invented external observation cannot substitute for a proof or signature.
- [ ] Map subject, input, model, action, scope, authority and temporal bindings;
  explicitly refuse mappings that require unsupported semantic upgrades.
- [ ] Preserve positive, substitution and missing-artifact witnesses plus mutation
  evidence and an independently executed replay for every claimed mapping.
- [ ] Integrate at least two independent target implementations through the P2
  protocol, with external source repositories and frozen ERC cores unchanged.

Existing laboratory evidence remains useful even if an external artifact is absent.
A genuine component does not by itself complete an external chain.

## P4 — Verifiable Execution Enforcement

**Current:** EXPERIMENTALLY VERIFIED local escrow release and refusal behavior;
external execution guarantees PARTIALLY VERIFIED, arbitrary execution authorization
UNSUPPORTED. Stronger enforcement is PLANNED. **Milestone: open.**

Acceptance criteria:

- [ ] Define a versioned execution policy binding the exact claim, contract,
  profile, evidence, consumer, chain, instance, job, recipient, amount and validity period.
- [ ] Demonstrate that the execution boundary enforces that policy and cannot be
  bypassed by directly submitting a signature that satisfies a narrower contract.
- [ ] Exercise replay, duplicate consumption, cross-domain substitution,
  consumption-time expiration, signer revocation and stale authorization controls.
- [ ] Independently verify actual execution evidence and state transitions under
  declared state-authority/finality assumptions; a signed assertion is insufficient.
- [ ] Publish compatibility results for unchanged target interfaces. Required target
  changes belong in a separately authorized/versioned integration, never a silent patch.
- [ ] Retain local mock-token tests, gas-measurement scope and surviving/absent-check
  reports; demonstrate the required controls before reconsidering production HOLD.

The current escrow still admits two unsupported research-policy cases after signing
(expiration and revocation); its six absent on-chain checks remain NOT_APPLIED.
This roadmap authorizes no deployment, real-fund transfer or change to frozen Core.

## P5 — Independent Review and Release

**Current:** IMPLEMENTED reproducibility infrastructure and EXPERIMENTALLY VERIFIED
CI; a reviewed release meeting these gates is PLANNED. **Milestone: open.**

Acceptance criteria:

- [ ] An independent reviewer reproduces the exact candidate from a clean checkout,
  including native verification, signatures, conformance and mutation controls.
- [ ] Resolve findings with new versioned evidence; keep original failures and
  survivor reports. Explicitly document accepted limitations and scope exclusions.
- [ ] Verify candidate-HEAD CI, artifact/source inventories, deterministic semantic
  outputs and all documented commands; runtime measurements retain environment context.
- [ ] Publish a reviewed compatibility matrix, supported claims, known limitations,
  dependency/license inventory and reproducibility archive with SHA-256.
- [ ] Identify release ownership and review responsibilities through actual recorded
  agreement. This document does not appoint maintainers or establish governance.
- [ ] Create a versioned release only after those gates; state its precise guarantee
  level. FULL_CHAIN_VERIFIED requires every external link, authority and execution
  fact, not just passing CI or a merged PR.

P0 provides the reviewable baseline; P1 and P2 define reuse; P3 supplies real adapters;
P4 addresses execution; P5 evaluates the declared release scope. A bounded research
release may retain unsupported capabilities if explicitly excluded; it must not
claim completion of the broader execution or external-chain objectives.
