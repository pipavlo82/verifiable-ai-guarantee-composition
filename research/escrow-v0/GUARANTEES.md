# Nine distinct guarantees and trust boundaries

| Layer | Established by this experiment | Does not establish |
|---|---|---|
| Native proof verification | Pinned verify_shard and exact public MatMul replay | Deployed LLM, input admission, approved model or general proof-system soundness |
| Evidence authenticity | Actual EIP-712 and BIP-340 verification | Factual truth or independent human/organizational control |
| Evidence completeness | Required declared evidence is available under the selected contract | Universal completeness of the contract |
| Scenario coverage | PR7 catalog compared with independent scenario requirements and minimum scope | Adequacy for arbitrary payment policies |
| Scoped authorization | Exact PR7 claim plus separate payer-selected grant | Permission to release arbitrary funds |
| Signed verdict authenticity | Exact v2 ABI digest, real deterministic laboratory Schnorr signatures, Python/Node agreement | Correctness of signed approval or production signing-service integration |
| On-chain signature verification | Actual unchanged BIP340 Solidity verification in local EVM | Claim scope, raw-byte admission, expiration or revocation |
| Payment authorization | Stored escrow terms plus trusted key approval; adapter adds external policy | Mandatory enforcement of all adapter checks on-chain |
| Payment execution | Actual mock-token balance changes observed separately | Public Base payment, token correctness generally, or external task completion |

Missing evidence stays UNVERIFIABLE. Refutation is a demonstrated failed obligation.
NOT_COVERED means the existing layer contains no enforcement for the requested
guarantee; it is not a successful check. A build/runtime failure is infrastructure,
not REFUTED evidence and not a mutation kill.

The payer grant and escrow snapshot are trusted inputs in this experiment. No RPC
state proof, payer signature over the grant, global replay registry, controller
ownership oracle, Base finality proof or production signing-key custody is supplied.
PR7's original contract adequacy and stable-toolchain assumptions remain explicit.

The BIP-340 library uses ecrecover and modexp and compares Ethereum addresses of
reconstructed points. This is not a new proof of the library's cryptographic soundness.
Its explicit domain restrictions include px in (0,n), nonzero scalar/rx/challenge.
Tests reject s=n, negated s and invalid signatures; no ECDSA low-s rule is silently
applied to Schnorr. Deterministic lab signing is not constant-time production signing.
