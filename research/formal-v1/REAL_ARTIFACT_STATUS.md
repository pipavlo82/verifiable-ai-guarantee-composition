# Real artifact status and evidence boundaries

## Executed independently

At zkIE commit `39d8df96877bc3bebf33c69b06907d792b3184b9`, both exact tests passed:

- `compose::tests::op_shard_matmul_roundtrip`
- `compose::tests::committed_projection_roundtrip`

They execute the upstream native proof/verification routines. Their test bodies include changed-input or changed-weight rejection controls. They use upstream test parameters and deterministic test randomness. We did not audit cryptographic soundness, run a full inference model, export a portable proof, or attach these proofs to a real external attestation.

The initial offline attempt failed because the isolated Cargo cache lacked dependencies. That failure is preserved in `evidence/native/offline-*`. Online dependency installation with `--locked` then succeeded, followed by offline replay. The original reports and raw logs are preserved, together with a replay using the portable runner. Upstream tracked files stayed clean.

The public event extracted from [ledger 19](https://api.babyblueviper.com/ledger/19) has ID `ff7227c605828f94457f450bc44b4c1dbc11e8f6df27f38f55a4aeb75d0b284a`. We independently recompute the [NIP-01](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md) event ID from the original content string and verify its [BIP-340](https://github.com/bitcoin/bips/blob/927b6de9915c9262615a6399de51b200f81e5aa4/bip-0340.mediawiki) signature using locked `@noble/curves@2.0.1`. No signing keys, new signatures or server-side verification endpoints are used.

The original verifies. Corrupting the signature, content, ID or key fails. Changed content with a recomputed event ID also fails under the original signature. Keeping the genuine signed event unchanged while substituting the consumer's requested proposal digest leaves authenticity VERIFIED and makes the digest binding REFUTED. This is a controlled consumer test, not evidence that the upstream service accepts the substitution.

## Scope of the verified public signature

The signature authenticates the event content under its embedded public key. It does not establish who controls that key, who authorized it, whether the judgment is correct, trusted issuance time, relay inclusion, chain execution, or downstream permission. The signed `artifact_hash` can be compared to a caller-supplied digest under an assumed common profile; the proposal preimage is not verified in this stage.

The API's surrounding execution, transaction, timestamp and outcome fields are producer-reported data. We did not verify them with chain/relay inclusion proofs, nor infer their authenticity from a signature over a different nested object. The signed content does not contain the surrounding `executed_action_hash`. The source already limits its timestamp/anchor claims; we do not upgrade them.

The extracted JSON is not advertised as raw HTTP bytes. Its provenance file records the complete response's SHA-256; raw response snapshots remain in the local evidence delivery. The capture manifest's `signature_verification: NOT_PERFORMED` describes capture-time behavior. `evidence/crypto.json` records the subsequent independent offline verification.

## Next coherent experiment

1. Obtain or generate an authorized real inference with retained input bytes, model manifest, native proof and public statement.
2. Obtain a real attestation covering the same input/model/output, including canonicalization and signature domain.
3. Obtain a judgment covering the exact proposed action, with an independently configured authority policy.
4. Retain real execution evidence and a receipt for that same execution; verify the transform from proposal to execution.
5. Publish only shareable artifacts, with source locks and exact byte commitments. Independently replay the native verifiers and composition rules.
6. Use valid but unrelated components for controlled substitutions; compare consumers on identical inputs and explicitly classify missing evidence.

End-to-end integration remains NOT IMPLEMENTED. No fabricated proof, signature, transaction, receipt or retrospective policy field fills a missing link. The local native tests and this public event must not be stitched together into a purported execution chain.
