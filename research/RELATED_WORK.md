# Related work and provenance

This is independent experimental research, not official Trustless AI specification work. Ownership of the personal repository does not imply sole authorship of the referenced ecosystem. The new Python implementation uses only the standard library and does not vendor upstream source code.

1. [zkIE at 39d8df9](https://github.com/trustless-ai/zkIE/tree/39d8df96877bc3bebf33c69b06907d792b3184b9): inference proof primitives and shard composition. Relevant to inference-statement validity and internal tensor bindings; not treated here as an external authorization policy.
2. [recompute-kit at f7308cd](https://github.com/trustless-ai/recompute-kit/tree/f7308cdd5ba55ac8229103e82ebc5fc14f81b88b): primary-artifact recomputation and explicit unavailable outcomes. Informs the method, not a native dependency of this experiment.
3. [ERC-8299 draft at PR #1810 head c0e13d1](https://github.com/ethereum/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md): WYRIWE input provenance and judgment-execution composition; the source already distinguishes authentic judgment from authorization and soundness.
4. [agent-ercs at 01283ca](https://github.com/trustless-ai/agent-ercs/tree/01283ca57305f915afb560d23359a27fd748eb5a): interfaces separating proof verification, agent authorization and declaration; WYRIWE/judgment typed structures. Interfaces are not a deployed-system audit.
5. [ReceiptOS Verify at 3961431](https://github.com/pipavlo82/receiptos-verify/tree/396143120f787d2f5534e92c0cf896c029a05775): caller-selected claims, signed evidence surfaces, replay and explicit subject/scope/authority/dependency bindings. Its existing behavior is not the weak independent-only baseline.

The contribution attempted here is a small, reproducible, tri-state composition experiment with explicit source-removal controls and a same-input comparator. Novelty beyond this bounded experimental packaging is not established. A wider academic literature review, formal proof and independent implementation are future work; no unreviewed citation list is presented as evidence of novelty.

Selected source blobs and exact references are in `sources.lock.json`; [SOURCE_REVIEW.md](SOURCE_REVIEW.md) distinguishes draft requirements, observed code, upstream assertions and proposed hypotheses. Original code is MIT licensed. No upstream dependency has been copied or relicensed.
