# Verifiable Execution & Claim Authorization

Research and executable experiments for determining **which downstream claims
verified evidence actually authorizes**.

The project separates three questions: **Coverage** — which obligations does the
scenario require? **Verification** — does the evidence establish each obligation?
**Composition** — do the established guarantees authorize this exact claim?
Consumers then recompute authorization before admitting a result.

**Current result: a narrow laboratory claim, with a partially verified evidence
chain.** The integration checks local output replay and review of exact proof
bytes. It does not authorize arbitrary execution or establish a complete external
provenance-to-execution chain. The escrow experiment is **PARTIALLY_COMPATIBLE**;
production payments remain **HOLD**.

## Start here

| Document | What it answers |
| --- | --- |
| [Roadmap P0–P5](../ROADMAP.md) | What exists, what is planned, and the evidence needed to accept each milestone |
| [Architecture](../docs/ARCHITECTURE.md) | Components, authorization boundaries and the exact laboratory claim |
| [Status and research history](../docs/STATUS.md) | Verified baseline, merged PRs, finite results and remaining gaps |
| [Reproducibility](../docs/REPRODUCIBILITY.md) | Pinned environments, commands, integrity checks and raw output locations |
| [Integrations](../docs/INTEGRATIONS.md) | Existing ecosystem components, current experiments and proposed adapters |
| [Contributing](../CONTRIBUTING.md) | Reviewable changes, evidence discipline, attribution and preservation |

## Evidence and limits

- **Claim-aware integration:** [report](../research/integration/EXPERIMENT_RESULTS.md),
  [mutation controls](../research/integration/MUTATION_REPORT.md),
  [limitations](../research/integration/LIMITATIONS.md).
- **Verdict-gated escrow:** [technical report](../research/escrow-v0/REPORT.md),
  [results](../research/escrow-v0/EXPERIMENT_RESULTS.md),
  [limitations](../research/escrow-v0/LIMITATIONS.md).
- **ERC-8404 external consumer:** [compatibility](../research/erc8404/COMPATIBILITY_MATRIX.md)
  and [frozen Core baseline](../research/erc8404/CORE_BASELINE.md).
- **Research:** [paper draft](../research/ACADEMIC_PAPER_DRAFT.md),
  [integration addendum](../research/integration/ACADEMIC_PAPER_DRAFT.md),
  [prior art](../research/PRIOR_ART_ANALYSIS.md) and
  [open proof obligations](../research/OPEN_PROOF_OBLIGATIONS.md).

The reusable community conformance harness is a planned generalization of existing
checks, vectors and runners. Semantic ABI, RSI and recompute-kit already exist as
separate projects; their code and responsibilities are not being absorbed here.
Research-policy checks are separate from normative ERC requirements. This work is
neither a security certification nor evidence of an upstream vulnerability.

Initiated by [Pavlo / pipavlo82](https://github.com/pipavlo82) as
`verifiable-ai-guarantee-composition`, the repository was transferred to
[Trustless AI](https://github.com/trustless-ai) with its Git and PR history intact.
Original project material remains [MIT licensed](../LICENSE); third-party material
retains its own licenses and attribution. Hosting does not imply an additional
maintainer or governance agreement.

This is the GitHub entry README. The [root README](../README.md) remains unchanged
because its exact bytes are integrity-pinned; it retains the detailed research and
replay guide. [GitHub selects `.github/README.md` first](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).
