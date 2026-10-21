# Typed, scoped evidence composition (v3)

Status: executable finite model and conditional proposition candidates, not a mechanized security proof.

A guarantee is a tuple `G = (subject, scope, authority, evidence, assumptions,
dependencies, contract, permitted_claims)`. The concrete declarations live in
`src/v3/model.py:GRAPH`; `python -B tools/v3/run.py --plan external_full_chain`
exports the graph and the exact dependency closure. A requested claim selects an
AND graph. The planner returns its required leaf contracts and the additional
bindings beyond component validity. It does not discover new policies or prove
that the declared contracts are complete.

| Type | Evidence/contract | Permitted conclusion |
| --- | --- | --- |
| SignedPublication | Exact NIP-01 bytes/event ID and BIP-340 verification | The selected key authenticated this event |
| SignedCell | Exact Nostr or EIP-712 Cell and evidence digest | The selected key authenticated this scoped cell |
| AcceptedIssuer | Key equality under a separate caller policy | Accepted for this publication profile only |
| DecisionBinding | Eight-field decision preimage, both cell artifact references, requested reference | Same decision reference |
| ClaimBinding | Both claim preimages/IDs and request | Same claim preimage |
| JudgmentScope | Verdict, policy, source class and signed claim bodies | Literal agreement with a requested verdict |
| DomainContext | Exact signed EIP-712 domain vs requested domain | Domain equality, not chain deployment |
| ObservationContext | Signed `as_of` vs requested `as_of` | Context equality, not a trusted timestamp or replay database |
| NativeArithmetic | Pinned Rust verifier and recomputation on retained tuple | This public matrix operation verifies |
| ModelSelection | SHA-256 of exact manifest vs explicit caller pin | Caller selected this laboratory model |
| ReceiptIntegrity | ReceiptOS/Crystal and separate Python root computation | These receipt bytes have the stated root |
| ReceiptSubject | Proof digest in receipt vs requested digest | Receipt names that proof |

All nodes additionally declare verification authority, explicit assumptions,
dependencies and permitted claims in the executable graph. Compound authority is
the caller policy; it cannot strengthen a child scope. Trust in the key policy,
verifier implementation, hash collision resistance and signature unforgeability
is assumed, not established by a test. Caller constants are not inferred from
submitted artifact fields.

## Three-valued contracts

`VERIFIED` means the specific contract has sufficient checked evidence under its
assumptions. `REFUTED` means a known contradiction to that contract. `UNVERIFIABLE`
means a required value or verification procedure is unavailable. Aggregate:
any REFUTED -> REFUTED; otherwise any UNVERIFIABLE (or empty set) -> UNVERIFIABLE;
otherwise VERIFIED. Known inequality retains REFUTED even when another operand
is missing. Reports preserve both the missing and refuted obligations.

Authorization is the predicate `aggregate(required(claim)) == VERIFIED`, never a
claim about more than that graph's scope. Invalid runtime execution yields no
authorization. Test success is not substituted for a cryptographic primitive.

## Conditions and proof status

1. **Definition-level derivation:** if a nonempty AND closure contains U and no R,
   authorization is false. This follows directly from the aggregate definition;
   it is not a cryptographic soundness theorem. All 27 length-three status tuples
   are also checked empirically.
2. **EMPIRICALLY VERIFIED, relative necessity:** for each of 14 implemented
   enforcement sites, an isolated witness has exactly that required leaf R.
   Replacing that one enforcement result with V authorizes the negative request;
   restoring the source rejects it and restores its positive control. This
   establishes necessity for that witness and configured claim, not all possible
   verifiers or equivalent formulations.
3. **HYPOTHESIS, sufficient conditions:** if every leaf verifier is sound for its
   declared semantics, the requested closure is complete, authority policy is
   correct, encodings are unambiguous, and each binding preserves subject/scope,
   then authorization entails the conjunction of those scoped leaf guarantees.
   An induction over a finite acyclic AND graph is a candidate proof strategy.
   Soundness and completeness of the real-world leaf semantics are open.
4. **NOT IMPLEMENTED:** sound inference of original admission, model delegation,
   judgment truth, external effect, or freshness from these signed objects.

Counterexamples are executable in `src/v3/scenarios.py` and individually mapped
to source mutations in `evidence/v3/validation/mutations-normal/report.json`.
Missing-evidence controls cover every implemented stage and required binding
family. Six unavailable integration contracts are explicitly outside mutation
coverage. No positive complete external chain is claimed.

The planner is a fixed dependency expansion. It is not an SMT solver, a general
minimal-binding synthesis algorithm, a proof-carrying authorization calculus or
an upstream Trustless AI specification.
