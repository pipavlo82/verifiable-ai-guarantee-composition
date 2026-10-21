# zkIE / ERC-8274 semantic mapping assessment

**Result: exact deployed semantic compatibility NOT ESTABLISHED. No new
ERC-8274-conformant adapter is implemented.** An offline native verifier remains
usable for its exact statement. Similar argument names do not prove compatibility.

Sources: [zkIE 39d8df9](https://github.com/trustless-ai/zkIE/tree/39d8df96877bc3bebf33c69b06907d792b3184b9),
[agent-ercs 01283ca](https://github.com/trustless-ai/agent-ercs/tree/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8274),
[ERC-8274 draft 3f014d0](https://github.com/JimmyShi22/ERCs/blob/3f014d07a0ceac39fe6fb6dec0efdc30640a9653/ERCS/erc-8274.md).

| Dimension | Actual native experiment | ERC-8274 requirement / unresolved mapping |
| --- | --- | --- |
| Statement | Fixed public MatMul shape (4,8,8), Goldilocks field, exact canonical u64 little-endian tensors | A documented input/output hash scheme and proof-specific semantics are required |
| Proof artifact | Retained VAGCNP2 bytes around native zkIE APIs; sums/challenges and empty bounds bindings in this profile | No standardized ERC encoding of these witnesses is established |
| Public inputs | input.bin, weights.bin, output.bin, fixed operation graph and model manifest | Hashes alone cannot supply absent native tensors or define their meaning |
| Model identity | Keccak of exact model manifest, weight SHA-256, pinned zkIE source and wrapper | Model/version/toolchain invariants would need a fixed metadata profile |
| Authority | Local compiled Rust verifier at pinned source, runtime and lockfiles | Ethereum deployment address/code/upgrade authority are unavailable |
| Proof system | Public arithmetic verification and explicit recomputation | No ZK/privacy or general malicious-prover soundness claim; do not label it a zkML deployment by name alone |
| Scope | Exact local arithmetic relation | No automatic agent authorization, input provenance, judgment truth or execution success |

The native wrapper actually invokes verify_shard and checks its public statement;
it does not equate passing native unit tests with verification of the retained
artifact. Native build/test logs, proof subprocess output and a Python arithmetic
cross-check are preserved. Python recomputation is not a second native proof
verifier. Full statement and digests remain in evidence/v2/capture/a and its
source lock; v4 preserves them without changing their semantics.

## Version drift matters

The inner four-argument verify ABI is similar in both drafts and agent-ercs, but
the current ERC permits documented backend hash schemes, requires invariant
deployment metadata, and treats proofProfile as address-scoped self-description.
Matching profile values across addresses do not establish behavioral equivalence.
An outer profile binds verifier address, profile and metadata hash; multi-verifier
profiles also bind routing/aggregation policy.

The current outer verification digest binds nine items: taskId, agentId, inputHash,
outputHash, valid, agentProofProfile, timestamp, instanceId and chainId. Ethereum
instance and chain encoding are specified. Its event carries the corresponding
information. The pinned agent-ercs interface comments still describe a six-item
digest and an event without the new profile/time/domain preimage fields. This is
observed source-version divergence, not a claim about a deployed vulnerability.
The digest is not a unique occurrence receipt; transaction/log inclusion is a
separate obligation.

## Executable next-stage requirements

Before an adapter can claim conformance, acquire a pinned actual deployment and
code/profile/metadata policy; specify deterministic witness/public-input encoding;
execute identical positive and negative native and interface calls; check current
outer digest preimages and chain inclusion; separately verify agent authority.
Run `python -B tools/v4/verify_sources.py` to check this study's exact source pins
and `python -B tools/v4/secondary.py` for its independent crypto/arithmetic scope.
Until those deployment artifacts exist the ERC integration status is
**NOT IMPLEMENTED**, with no inferred agent-execution authorization.
