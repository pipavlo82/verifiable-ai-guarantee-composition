# Primary-source review at 2026-10-16

All five public sources were fetched read-only into separate local clones. Each HEAD was compared to the captured GitHub commit. `sources.lock.json` records 19 selected Git blob identities, byte lengths and SHA-256 hashes; checkout line-ending conversion is not used for these hashes. This is bounded source inspection, not an upstream audit or an execution of upstream test suites. No upstream files were changed.

| Primary source | Exact observed commit | Status |
|---|---|---|
| trustless-ai/zkIE | `39d8df96877bc3bebf33c69b06907d792b3184b9` | main snapshot |
| trustless-ai/recompute-kit | `f7308cdd5ba55ac8229103e82ebc5fc14f81b88b` | main snapshot |
| ethereum/ERCs PR #1810 | `c0e13d17940a6eabe4d842e623fd0f871550ef7b` | OPEN PR head; ERC-8299 text says Draft; not a merged final standard |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | main snapshot |
| pipavlo82/receiptos-verify | `396143120f787d2f5534e92c0cf896c029a05775` | main snapshot |

## zkIE

**Implementation observed:** [`verify_shard` and `verify_shard_dag`](https://github.com/trustless-ai/zkIE/blob/39d8df96877bc3bebf33c69b06907d792b3184b9/crates/zkie-ops/src/compose.rs#L1387) recompute witness values through `forward_ops`; DAG verification checks shards and cross-tensor `same_poly` bindings. `ShardDagProof` is a Rust structure carrying shards, cross-tensor ids and binding proofs. These observations establish code paths at this pin, not that arbitrary external model/input claims are authenticated.

**Upstream reported:** the [README](https://github.com/trustless-ai/zkIE/blob/39d8df96877bc3bebf33c69b06907d792b3184b9/README.md) describes ongoing development and public weights/activations in the current route. We did not produce a proof, load weights or measure proof performance.

**Assumption to test later:** a real integration must bind exact input encoding, model manifest/version, circuit/config and output to the verifier's public statement. An enclosing claim envelope does not itself create those bindings. **Research hypothesis:** downstream authorization requires relations beyond the algebraic inference checks. This is not a claimed zkIE omission.

## WYRIWE / ERC-8299 PR #1810

**Normative within the draft, not an adopted standard:** the [pinned specification](https://github.com/ethereum/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md) defines raw input keccak256, sanitization pipeline commitment to exact CID URI bytes plus raw hash, and sanitized input hash. Its eight-field EIP-712 `WyriweAttestation` includes agentId, registry, modelHash, rawInputHash, sanitizationPipelineHash, inputHash, outputHash and timestamp. Signature verification is mandatory; applicable input/transform recomputation is required when inputs are available. Availability and signer trust remain separate assumptions. Timestamp alone is not replay protection.

The Composition section explicitly separates judgment authenticity, task authorization and accountability. It says a true judgment verification result does not establish judgment soundness or permission to proceed. Therefore the central distinction in this experiment is already recognized upstream; our weak baseline must not be attributed to this proposal.

For off-chain judgment verdicts the draft specifies SHA-256 over JCS and a producer-published preimage field list that pins the proposal. It distinguishes on-chain keccak256 encodings. `intended_verifier` and `policy_commitment` are recommendations, not unconditional required fields for all legacy artifacts. We do not backfill either field or silently assume an illustrative fixed preimage list. Legacy missing evidence remains unavailable.

**Open integration questions:** signing-time wording differs between the signature-role discussion (reveal) and later pointer rationale (verdict-time). The pinned Solidity interface comments describe an on-chain hashing form while draft prose also describes off-chain SHA-256/JCS. A real profile must explicitly choose a mechanism and resolve timing/encoding semantics with actual producer artifacts; v0 does not settle these questions. **Upstream reported** gateways, deployments and ledger examples were not independently queried or chain-verified here.

## agent-ercs

**Interface requirements observed:** [`IProofVerifier`](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8274/IProofVerifier.sol) accepts inputHash, outputHash, metadata and proof bytes, with mechanism/profile identifiers. [`IAgentVerifier`](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8274/IAgentVerifier.sol) adds taskId/agentId and describes stateful authorization. Interface declarations do not prove deployment correctness or a specific implementation's handling of metadata.

[`IWyriweAttestation`](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IWyriweAttestation.sol) retains the eight-field typed struct and signature interface. [`IJudgmentExecutionAttestation`](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IJudgmentExecutionAttestation.sol) defines agent/registry/validator identity, proposal/verdict/executed-action hashes, two timestamps and recordPointer. Its comments explicitly limit the judgment bool to authenticity/binding. We did not call these interfaces or implement their ECDSA/ABI path.

## recompute-kit

**Method and reported contract:** [RECOMPUTE.md](https://github.com/trustless-ai/recompute-kit/blob/f7308cdd5ba55ac8229103e82ebc5fc14f81b88b/RECOMPUTE.md) advocates exact references and re-execution of primary artifacts. The [README](https://github.com/trustless-ai/recompute-kit/blob/f7308cdd5ba55ac8229103e82ebc5fc14f81b88b/README.md) distinguishes verified good, verified bad and unavailable verification. V0 adopts a similarly explicit tri-state discipline as an original local implementation; no native recompute-kit runner or conformance claim is made. The inspected license text is CC0-1.0 despite GitHub's generic NOASSERTION metadata.

## ReceiptOS Verify

**Implementation observed:** v1 [`subject.mjs`](https://github.com/pipavlo82/receiptos-verify/blob/396143120f787d2f5534e92c0cf896c029a05775/src/core/subject.mjs) compares caller-selected subject, claim and policy. v2 [`verify-v2.mjs`](https://github.com/pipavlo82/receiptos-verify/blob/396143120f787d2f5534e92c0cf896c029a05775/src/core/verify-v2.mjs) separately evaluates authenticity, native binding, semantic compatibility, dependencies and projection. It explicitly limits supplied observations relative to external execution provenance.

The pinned v2 profile is `receiptos.verify.generic.v2`; its adapter dispatch lists rvr, semantic-abi, trustless and interpoll. No zkIE/WYRIWE bridge is inferred from this list. The [request schema](https://github.com/pipavlo82/receiptos-verify/blob/396143120f787d2f5534e92c0cf896c029a05775/schemas/request-v2.schema.json) and [bundle schema](https://github.com/pipavlo82/receiptos-verify/blob/396143120f787d2f5534e92c0cf896c029a05775/schemas/bundle-v2.schema.json) identify caller request versus signed statement/surface, evidence manifest, signature and payload. A toy `receipt` in this repository is not a ReceiptOS bundle and is never relabeled as one.

## Evidence classes

Independently verified here: captured repository pins, selected blob hashes, this repository's own executed tests and reports. Source-observed: the bounded implementations/interfaces above. Upstream reported: readiness, deployments and performance claims. Assumed: trusted fixture policy/catalog and local interpreter. Proposed: real bridge mappings and conditional composition propositions. These classes are not interchangeable.
