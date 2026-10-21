# External joint consumer

Entry points: `src.integration.engine.evaluate(case)` and `admit(record, case)`.
The consumer supplies its current trusted contract bytes, requested claim and
evidence. A record is not a transferable bearer credential.

The authorized proposition is precisely:
`LAB_REPLAY_AND_REVIEWED_PROOF_IDENTITY`, with scope
`local-output-replay-and-proof-byte-review`. It means that the pinned inference
profile establishes local replay, the pinned review profile establishes authenticated
artifact identity/review, the same proof bytes connect them, and the displayed
claim fields equal the independently verified values. It does not say that the
reviewer's opinion is true or that an external task was executed.

The scenario contract and catalog are separate artifacts. Coverage compares the
catalog against the independently supplied contract. A separately published minimum
contract in `fixtures/integration/scenario-contract.json` limits this specific
supported claim type: a weaker contract cannot retain the broader authorization
name. Neither artifact's adequacy is established by the code or by its hash.

| Obligation | Procedure | Consumed guarantee |
|---|---|---|
| J01 | inference_profile | Native replay, original provenance/action/authority/scope bindings |
| J02 | review_profile | Frozen receipt replay and authentic authorized review |
| J03 | proof_byte_binding | Exact proof SHA-256 across both verified components |
| J04 | profile_commitments | Original canonicalization, subprofile digests and exact native authority/model/scope policy bytes |
| J05 | claim_values | Scenario, type, scope, both subjects, proof/input/model/output values |
| J06 | claim_fields | Explicit unknown-field rejection, including nested profile claims |
| J07 | key_policy | Scenario-dependent O14 requirements and actual recovered-key inequality |
| J08 | controller_scope | Refuse unestablished real-world controller independence |
| J09 | supported_scope | Only the implemented laboratory claim type and scope |

Dependencies and procedure names are in the contract. Unknown IDs do not inherit
authority merely by pointing to a known function. Missing catalog entries are
coverage refutations; absent evidence is UNVERIFIABLE; known contradictions remain
REFUTED even alongside unavailable evidence.

Every decision returns status, authorized, scenario, claim_type, contract_sha256,
verified_scope, missing_obligations, unconsumed_claim_fields, evidence_references,
assumptions, component statuses and research classification. Verified scope is
present only for authorization. Evidence references hash the bytes actually read
and the exact receipt/documents. Missing paths cannot be substituted with verified
flags, and the legacy file resolver is confined to the checkout.

Admission reruns both profiles, native verification and cross-artifact checks.
It requires a VERIFIED result and exact canonical equality of the presented
decision with the fresh result. Changes to flags, status, scope, evidence refs,
scenario, type, contract or assumptions therefore cannot become authority.

The distinct-key policy checks recovered identities directly. An obligation named
O14 can point to a different procedure in an independently supplied contract; the
label alone is insufficient. A preserved development counterexample constructs that
case with real self-judgment signatures. The final implementation refuses it and a
single-check key-identity mutation changes the refusal to incorrect authorization.
The same rule applies to profile names. The supported mapping requires the published
minimum v4 output procedures O01-O13 and review procedures S01-S06 with their exact
declared definitions. O14 remains conditional. An inference profile without native
verification or a review profile without authority cannot retain this joint claim type.

This is a reference experiment with local files, Python, Node and Rust. No service,
network trust protocol, Solidity ABI or normative ERC verification profile is added.
