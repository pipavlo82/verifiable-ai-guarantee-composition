# Trust boundaries

1. The consumer chooses an adequate policy. Contract adequacy and source selection
   are external assumptions; the same investigators authored the contract and code.
2. Original profile semantics and signed bytes are immutable. Their two subject
   labels and contract canonicalization rules remain distinct.
3. Actual native proof verification, EIP-712 recovery and RVR recomputation establish
   only their respective predicates. Neither a boolean supplied by a fixture nor a
   test-success record is accepted as cryptographic evidence.
4. The cross-artifact edge compares bytes consumed by both verifiers. Distinct
   valid proofs cannot be combined merely because both component statuses are green.
5. O14 establishes role-key separation only when the scenario requires it. It does
   not prove that the key holders have different legal or operational controllers.
6. The downstream admission boundary independently recomputes the decision. It does
   not authenticate a mutable flag, a caller-supplied digest or a cached assertion.

All authorization additions are external to ERC-8404. Its receipt remains the same
six-field object. Gate rejection, recomputation status and semantic outcome are not
reinterpreted; the consumer maps unavailable replay to its own refusal semantics.
The exact Core inventory and both language conformance suites are replayed.

Local tools, dependency packages, filesystem stability during a call and the
cryptographic assumptions of the selected proof/signature systems are trusted.
No hostile concurrent filesystem writer, sandbox isolation, resource exhaustion,
revocation service, global replay database or durable transaction admission protocol
is implemented. The consumer must provide current nonce policy; the experiment
does not establish global freshness from an in-memory list.

REFUTED denotes a failed verification/admissibility obligation under the selected
policy. Rejecting an out-of-scope external-execution request does not prove that the
external event did not happen. Missing evidence without a contradiction remains
UNVERIFIABLE. The result's evidence_level and chain_status labels describe this
laboratory research dataset; only status/authorized/verified_scope describe the
particular row's authorization, and no refused row has a verified_scope.
