# Exact unresolved guarantees

1. The existing escrow cannot make the external adapter mandatory. Any approving
   signature under its immutable key can reach release directly. No public production
   signing-service integration or guarantee that it executes PR7 was established.
2. A signed request hash does not prove correspondence between the text's recipient/
   amount and funded storage. The contract transfers the immutable stored terms; the
   external adapter is responsible for the cross-representation comparison.
3. Expiration and revocation after signing are not enforced. refundAfter permits refund
   but does not make release expire. No key rotation/revocation API exists.
4. submissionId is signed, but no global nonce registry exists. Per-escrow state rejects
   duplicate payment, while different escrows can use the same submissionId.
5. Payer grant authorization, authentic/fresh state snapshots, contract adequacy,
   policy clock and journal persistence are trusted external assumptions. They are not
   provided by the native proof or by an RVR receipt.
6. The laboratory decision_ref schema is explicit. The upstream private relay module
   is absent, and no conformance to its unpublished ledger semantics is asserted.
7. Native proof verification, real EIP-712 laboratory signatures, RVR recomputation,
   real Schnorr signature math, local Solidity checks and local mock transfers are
   executed. Original real-world input admission, model authorization, independent
   controller ownership, external task completion and public payment are not proven.
8. A genuine signature authenticates its signer, not factual judgment correctness.
   Different keys do not establish different people or organizations. O14 here proves
   the scenario's key-separation rule only.
9. Two RPC providers and matching compiled bytecode establish a read-only deployment
   observation, not independent Base consensus/finality or historical payment execution.
10. Arbitrary token semantics can violate the assumption that true transfer implies
    payment. The adversarial mock is not evidence of a USDC defect. Fee-on-transfer,
    reentrancy, liveness, MEV and economic analysis are outside this finite experiment.
11. No scientific novelty, production readiness, general cryptographic soundness or
    vulnerability in zkIE/ERC-8404 is claimed. No upstream semantics were changed.

Recommendation: HOLD for production/payment integration. The completed local research
is suitable for independent review. A next authorized stage needs a documented signer
service contract, authenticated payer grants/state snapshots and mandatory execution-time
policy enforcement if expiry/revocation/scope are required. Since upstream modification
was prohibited, those gaps are documented, not silently fixed through altered contracts.
