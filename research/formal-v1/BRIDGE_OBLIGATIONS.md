# Native interfaces and missing composition bridges

Source versions are frozen in the root [source lock](../../sources.lock.json) and the [additional lock](evidence/additional-sources.json). A normative draft requirement, an implementation observation, a trusted assumption and a proposed research obligation are different evidence categories.

| Boundary | Primary interface / source observation | Required additional evidence | Current status |
| --- | --- | --- | --- |
| Request → WYRIWE | `WyriweAttestation`: agentId, registry, modelHash, rawInputHash, sanitizationPipelineHash, inputHash, outputHash, timestamp | Raw input bytes, sanitization specification/preimages, EIP-712 signature, chain/domain and trusted attestor | NOT IMPLEMENTED for a common tuple |
| WYRIWE → tensor input | `rawInputHash` / `inputHash` describe byte commitments; zkIE Store/operation APIs operate on encoded values | Versioned tokenizer/normalizer, tensor layout, quantization and an authenticated transformation relation | NOT IMPLEMENTED |
| Model manifest → proof | WYRIWE `modelHash` can identify weights or a manifest; zkIE committed projection uses weight commitments | An explicit manifest-to-tensor/commitment mapping including shapes, operator graph and encoding | NOT IMPLEMENTED |
| Proof → inference claim | zkIE `OpShardProof`, `ShardDagProof`, `verify_shard`, `verify_shard_dag` | A serialized proof/statement interface and exact public statement for the target claim | Two native library tests executed; portable export not implemented |
| Inference output → proposal | Native output values and a judgment's `rawProposalHash` are different objects | Deterministic versioned action construction or another verified conformance relation | NOT IMPLEMENTED |
| Verdict → proposal | Public Nostr content carries `artifact_hash`; the draft also defines `verdictHash` constructions | Correct signature, exact signed bytes, proposal preimage/encoding, declared hash profile | Signature and same-profile digest relation checked; preimage unchecked |
| Signer → authority | A public key identifies a signing key, not policy entitlement | Caller-trusted key/identity mapping and policy granting this signer authority for this action | UNVERIFIABLE |
| Judgment → execution | Nine-field `JudgmentExecutionAttestation` includes validator, proposal/verdict/action hashes, two timestamps and recordPointer | Executing-agent signature, validator artifact, and proposal/execution conformance evidence | NOT IMPLEMENTED |
| Execution → receipt | ReceiptOS request/bundle schemas and `receiptos.verify.generic.v2` are source-observed interfaces | A genuine receipt for that execution, exact subject, profile, trust configuration and dependencies | NOT IMPLEMENTED |
| Receipt → downstream claim | A receipt attests to its declared verification result and subject | An explicit policy rule whose predicates follow from those exact facts | NOT IMPLEMENTED |
| Context / replay | Chain, verifier, policy and timing can constrain applicability | Authenticated context, pinned policy content and an actual freshness/replay mechanism | NOT IMPLEMENTED; a signed timestamp alone is insufficient |
| Algorithm / representation | Off-chain SHA-256/JCS and on-chain Keccak/ABI are distinct profiles | Declared algorithms, canonical bytes and a verifiable cross-profile relation | Research type checks only; no automatic bridge |

Primary references: [zkIE compose.rs](https://github.com/trustless-ai/zkIE/blob/39d8df96877bc3bebf33c69b06907d792b3184b9/crates/zkie-ops/src/compose.rs), [WYRIWE interface](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IWyriweAttestation.sol), [judgment interface](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IJudgmentExecutionAttestation.sol), [ReceiptOS schema](https://github.com/pipavlo82/receiptos-verify/blob/396143120f787d2f5534e92c0cf896c029a05775/schemas/request-v2.schema.json).

The draft's optional verifier/policy commitments must not be retroactively inserted into the semantics of older signed artifacts. A legacy object can authenticate its original content while leaving a newer consumer's obligation UNVERIFIABLE. The draft and interface also contain different wording about verdict-time freezing versus reveal-time signing; a future profile must resolve the precise signing event rather than silently choosing a favorable interpretation.

No adapters or source changes were made to upstream repositories. The present Node replay is our narrow consumer of a public Nostr event, not a WYRIWE EIP-712 verifier or a ReceiptOS adapter.
