# Integrations and ecosystem boundaries

The repository studies claim authorization across evidence boundaries. Existing
ecosystem projects remain independently maintained components. This roadmap neither
absorbs their code nor presents their existing work as a new feature of this repository.
The source observations below were made on 2026-10-21; they are documentation
references, not new runtime dependency pins or fresh tests of those projects.

## Existing ecosystem components

| Component and inspected source | Existing role | Proposed relationship here |
| --- | --- | --- |
| [Semantic ABI](https://github.com/trustless-ai/semantic-abi/tree/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee) — `d15c666dfccff17f7350fe97d2fc7b71cb2cbaee` | Typed evidence declarations and semantic linking across claim, authority, scope and temporal boundaries; expected/observed outcomes remain separate. | PLANNED explicit mapping to scenario/profile requirements; do not replace its linker or treat declaration compatibility as evidence truth. |
| [Relational Security Invariants (RSI)](https://github.com/pipavlo82/relational-security-invariants/tree/3d3038f90c3dd98e79f948398167c5cc3ef2fdd8) — `3d3038f90c3dd98e79f948398167c5cc3ef2fdd8` | Relation profiles, expectation admission, adapters and conformance comparison with mutation controls and stated independence limits. | PLANNED interoperability with its existing relation/expectation contracts; no automatic equivalence of its outcomes and this engine's authorizations. |
| [recompute-kit](https://github.com/trustless-ai/recompute-kit/tree/f7308cdd5ba55ac8229103e82ebc5fc14f81b88b) — `f7308cdd5ba55ac8229103e82ebc5fc14f81b88b` | Existing recomputation primitives, ERC-specific recipes and pinned conformance suites with explicit inability-to-verify outcomes. | Use exact recipe/suite semantics as external evidence or replay interfaces where a mapping is established; no duplication of the toolchain. A new general engine connector remains PLANNED. |

These descriptions come from the linked source READMEs. We have not claimed a
fresh ecosystem-wide conformance run, stable cross-project API, shared maintainer
agreement or complete interoperability. The projects' existing licenses, attribution
and version boundaries continue to apply.

## Current research integrations

| Integration | Established within the experiment | What is not established |
| --- | --- | --- |
| Native zkIE | Actual native verification of preserved proof bytes under the pinned toolchain/statement | WYRIWE admission of the original external input; general model authorization or task completion |
| WYRIWE-related and judgment evidence | Commitment/signature checks and selected laboratory cross-artifact bindings | A signature alone does not establish input provenance or judgment truth; Section 5 semantics remain distinct from extra research policy |
| ERC-8404 consumer | Receipt/commitment verification and an external claim-aware profile | Receipt validity alone does not imply downstream authorization; frozen Core is not extended or reinterpreted |
| ReceiptOS records | Preserved records and explicitly checked identity/binding relationships | Historical external execution does not follow from a signed assertion or matching digest |
| Verdict-gated escrow | Laboratory verdict issuance, unchanged contract checks and mock-token release | Mandatory use of the adapter, execution-time expiration/revocation and arbitrary payment authorization |

Authoritative experimental pins remain in the unchanged
[integration source lock](../fixtures/integration/source-lock.json),
[escrow source lock](../experiments/verdict_escrow/source-lock.json) and
[ERC-8404 Core baseline](../research/erc8404/CORE_BASELINE.md).
Examples include zkIE `39d8df96877bc3bebf33c69b06907d792b3184b9`, upstream escrow
`ce8c504f2ae4d9b389b53823fe16afec7fcf3bb3`, and the ERC-8404 research source
`7a9e63a80bce04db53c6550103c1d41eca35f3d1`. These are historical experiment pins,
not assertions about current upstream HEADs or accepted standard status.

## Admission criteria for a new adapter

A proposed adapter must document exact inputs/outputs, canonical preimages, source
and policy versions, identity namespaces, verification authority, required evidence,
unsupported fields and the permitted downstream claim. Preserve original bytes and
map expected versus observed behavior independently. Provide positive, substitution,
missing-evidence and mutation controls, with raw commands and outputs.

Cross-project result vocabularies require an explicit semantic mapping. Do not
translate a conformance PASS, authentic signature or recomputation success directly
into permission to execute. Unknown profiles, unavailable dependencies and missing
preimages retain explicit refusal/inability-to-establish outcomes.

Where an interface cannot express the required binding, report incompatibility.
Do not silently change a frozen receipt schema, upstream implementation or historical
artifact. See [P2–P4](../ROADMAP.md) and [contribution rules](../CONTRIBUTING.md).
