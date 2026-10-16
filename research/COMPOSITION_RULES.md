# Composition rules

Let R be the caller request, P the independently selected policy, E the supplied evidence, C_i the component checks and B_i the boundary predicates. Define `meet` on checked conjunctions: REFUTED if any premise is refuted; otherwise UNVERIFIABLE if any is unknown or the premise set is empty; otherwise VERIFIED. Missing evidence cannot by itself produce REFUTED.

1. Admit the synthetic schema and mechanism; unknown real modes return UNVERIFIABLE, NOT IMPLEMENTED. Public checksum equality is only integrity.
2. Recompute each present component's internal relation; no producer `verified` flag is accepted as proof.
3. Bind provenance to request input, model and version to witness and request, and witness to actual provenance input and output.
4. Bind every evidence subject to the caller subject. Bind judgment authenticity separately from permission for the action and policy.
5. Bind receipt execution/action/output to the request and its proof digest to the exact supplied witness body.
6. Require `scope(R) subseteq intersection(scope(E_i))`, matching domain, half-open time applicability `[not_before, not_after)`, exact policy, and an unconsumed nonce. Require the downstream assurance to be no stronger than each dependency; v0 only accepts SYNTHETIC.
7. All G1-G7 are mandatory. Evidence cannot erase dependencies by supplying an empty list. G8 is the meet of the local context rule and every prerequisite. A refusal is any result other than VERIFIED.

No edges may be inferred merely from equal output values, co-location in one JSON object, authentic issuer status, or a successful independent component check. Hash algorithms and encoding profiles must be explicit in any future cross-system bridge; SHA-256 here is not WYRIWE keccak256. A wrapper receipt must not upgrade the native conclusion.

## Candidate propositions (unproven generalizations)

C1, conditional scope preservation: for an acyclic dependency graph, sound premise verifiers, correct subject/statement translations, an authoritative scope order and explicit subset checks, successful composition should not amplify scope. A formal induction over that graph is future work. The implemented five-component graph and tests do not prove this generalization.

C2, conditional refusal monotonicity: removing necessary evidence should not turn a refused claim into a verified one. The finite missing-component tests exercise this property; no universal proof is offered. Malformed or unsupported admission may change REFUTED to UNVERIFIABLE while preserving refusal.

C3, separation of authenticity and authorization: authentic statements about unrelated actions need not authorize the selected action. V0 contains an executable counterexample to the implication from authenticity alone. A real cryptographic demonstration remains future work.

## Mutation experiment

`tools/mutations.py` replaces one marked enforcement return predicate with an unconditional successful local predicate in a compiled in-memory copy. It executes the designated negative, the positive and the complete matrix, then recompiles original bytes and checks the restored matrix. Original disk source is never changed. Each boundary is G1-G8; arithmetic component checks remain active.

KILLED requires original REFUTED -> mutated VERIFIED on the intended negative, positive still VERIFIED, and restored REFUTED plus a green full matrix. SURVIVED means the intended semantic counterexample did not authorize. CRASHED is execution failure, never a kill. NOT_APPLIED means no unique source site. UNVERIFIABLE means prerequisites/restoration/control validity did not establish a meaningful experiment. These eight removal mutants are a bounded control set, not a mutation-adequacy proof or exhaustive fault model.
