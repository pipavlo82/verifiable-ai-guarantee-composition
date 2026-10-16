# A conditional model of binding obligations

## Typed facts, rather than a scalar assurance score

Represent a verified fact as `(predicate, subjects, representation, scope, authority, evidence, dependencies, assumptions)`. Examples are `Authentic(signer, bytes)`, `Proves(verifier_profile, statement, proof)`, `Derived(transform, raw, normalized)`, `Conforms(policy, proposal, execution)` and `Permitted(policy, requester, action, context)`.

These predicates are not ordered by one generic strength number. A signature, an inference proof and a judgment establish different facts. In particular, authentication does not entail truth, permission or physical execution. A rule may use a fact only with its declared type and assumptions.

The G1-G8 obligations in [v0](../GUARANTEE_MODEL.md) remain separate. V1 studies the equality/representation part of their composition. It does not implement all eight guarantees for real artifacts.

For each applicable obligation use `VERIFIED`, `REFUTED` or `UNVERIFIABLE`. A checked contradiction is REFUTED. Missing evidence, unsupported representation or an unavailable native verifier is UNVERIFIABLE. Refuse authorization unless every required obligation is VERIFIED. A refusal does not establish maliciousness or falsehood. For an overall conjunction, a verified contradiction can refute the conjunction even if other dependencies are unknown.

## Exact abstract scope

There are nine subject variables in three groups:

| Dimension | Variables | Target |
| --- | --- | --- |
| input | requested_input, provenance_input, inference_input | All three equal |
| model | requested_model, provenance_model, inference_model | All three equal |
| action | requested_action, judged_action, executed_action | All three equal |

Each group offers its three pairwise equality checks: RP (first/second), PI (second/third), RI (first/third). These are **abstract identifiers in a common representation**, not literal upstream bytes. In particular, a proposed action and an execution record normally differ. Applying the action equality model requires an independently justified projection/conformance relation; no such bridge is supplied by the toy graph.

Let E be the nine candidate edges, N a set of trusted native equalities, S a subset of E minus N, and T the six requested-to-other target equalities. Native facts are explicit hypotheses. A producer's `verified=true` is not a fact in N. All node domains contain at least two elements.

## Equality-closure proposition (standard result, no novelty claim)

`N ∪ S` entails every equality in T if and only if both endpoints of each target are connected in the undirected graph `(variables, N ∪ S)`.

Proof: a connecting path entails equality by transitivity. Conversely, if a target's endpoints are disconnected, assign value 1 to the component of one endpoint and 0 to all other components. Every selected/native equality holds, while that target fails. This supplies a concrete two-valued countermodel. The argument works over any domain with at least two distinct values; finite enumeration checks our implementation, not the general proof.

In this particular target graph, after contracting N, inclusion-minimal sufficient sets form trees connecting each required group. The implementation independently checks all binary assignments using direct three-way equality rather than graph traversal.

Without native cross-component equalities, each triangle has three spanning trees with two edges. Therefore there are `3^3 = 27` bases of six edges. Adding the hypothetical native equality `model.PI` leaves two choices to connect the requested model: `3 × 2 × 3 = 18` bases of five added edges. In these instances all inclusion-minimal bases also have minimum cardinality; this coincidence must not be generalized to arbitrary policies or weighted checks.

Every single-edge removal from every basis has a saved countermodel: 162 and 90 respectively. The exhaustive comparisons examine 512 × 512 and 256 × 256 compatible assignment/subset pairs. No claim is made that six checks suffice for a real AI system. Sound native verification, authority, policy, representation, freshness and receipt semantics are outside this graph and are necessary additional premises.

## Representation boundary

A commitment is identified by `(algorithm, representation, digest)`, not digest bytes alone. Unlike representations are UNVERIFIABLE without a verified bridge. The reference comparator only compares these research records; it neither computes Keccak nor authenticates their labels.

The concrete preimages `b"3"` and `b"003"` both normalize to integer 3 but have different raw hashes. Thus equality of normalized model inputs cannot prove equality of submitted byte strings. A downstream claim must specify whether it concerns raw bytes, normalized values, tensors or action conformance. This is a standard non-injectivity argument, not a hash collision.

## Full composition rule: candidate profile, not an implemented theorem about upstreams

For a fixed policy P and claim C, require: sound native verification of each typed predicate; authenticated and available subjects; verified representation/transform/conformance bridges; applicable authority and scope; time/replay constraints; and a derivation of C from those exact premises under P. Only then may C be marked VERIFIED.

The proposition above handles the equality subproblem. Proving that real profiles discharge the remaining premises, and that their concrete verifier implementations implement this rule, is future work. No end-to-end composition theorem for zkIE/WYRIWE/ReceiptOS is asserted here.
