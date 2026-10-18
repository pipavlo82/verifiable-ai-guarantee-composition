# Scenario-relative coverage, verification and composition

Independent research profile v4/1, not an upstream specification. The executable
claim is about a finite, explicitly trusted scenario contract. It does not discover
all requirements of an arbitrary real system.

Let S be a scenario revision, P a trusted policy, q the requested claim, T the
separately supplied contract, K the declared catalog, and E the evidence bytes.
T supplies a finite requirement set R(S,P,q), its semantic procedure identifiers
and dependency edges. K is supplied independently. The implementation's function
inventory is neither R nor its oracle. The four contracts in fixtures/v4/contracts
are literal reviewable specifications. They are not generated from K or reflection
over verifier functions. The same researcher authored both: structural separation
is not independent human elicitation, and adequacy of T is an explicit assumption.

Each obligation is a typed record (ID, claim type, subject, scope, authority,
evidence requirements, verification procedure, dependencies, applicable policy,
source/version, justification, failure classification). The machine catalog and
contract requirements are JSON records; tests check their field structure.

**Coverage** checks scenario revision, presence R subset K, procedure/dependency/
policy/authority/scope agreement with T, and dependency closure in T. Unknown
required procedures are UNVERIFIABLE. An observed missing required catalog entry
is REFUTED as a coverage assertion, not a refutation of the absent artifact.

**Verification** evaluates only procedures declared by K against actual E.
The common fact collector performs real native proof and EIP-712 operations.
Those facts do not authorize anything until the selected obligations consume them.
No producer-supplied boolean is evidence of cryptographic verification. Catalog
entries that cannot be evaluated remain UNVERIFIABLE.

**Composition** requires coverage, every selected evidence obligation and the exact
requested claim to agree with the contract. Broader requests are refused. Extra
declared checks also constrain this conservative implementation; adding an unknown
check can make the result UNVERIFIABLE. The graph is conjunctive, with no
disjunction, delegation calculus, temporal logic or theorem prover.

Decision algebra: any REFUTED dominates; otherwise any UNVERIFIABLE dominates;
otherwise the nonempty conjunction is VERIFIED. Empty evidence is UNVERIFIABLE.
Retain individual statuses even when the aggregate is REFUTED. Authorization
requires VERIFIED; refusal includes both REFUTED and UNVERIFIABLE.

## Conditional propositions and their status

1. **Relative omission detection (logical consequence of the definition).** With
   fixed trusted T and faithful coverage evaluation, deleting r in R from K makes
   the coverage assertion false. This is elementary set inclusion, not a new
   scientific theorem. Thirteen physical deletion witnesses exercise the code.
2. **Inventory insufficiency (counterexample, empirically exercised).** If r is
   absent from K and all other checks pass, conjunction over K cannot establish r.
   The same evidence is admitted by baseline B and refused by C. A self-reported
   complete inventory changes no evidence or trusted requirement.
3. **Conditional preservation (candidate sufficient conditions).** If T faithfully
   states all requirements of q; evidence verifiers are sound for their narrow
   statements; all authority, subject, context and dependency bindings are faithful;
   and composition implements those rules, VERIFIED supports q within those
   assumptions. General soundness and adequacy are **NOT PROVEN** here.
4. **World completeness is not inferable (open obligation).** A matching K and T
   cannot establish that T includes an omitted real-world requirement. Modifying
   both together or choosing the wrong trusted contract is outside the omission
   experiment's trust assumptions. Independent requirements review remains needed.

Necessary conditions are contract-relative: isolated witnesses establish that
each selected boundary matters for this corpus. They do not prove universal
minimality. No claim of formal verification of Python, Rust, cryptographic
primitives or operating-system execution is made.

## Threat model

The adversary substitutes evidence, claims, catalog entries or scenario contexts,
but does not redefine the trusted scenario contract or policy root. Compromise of
the verifier, contract approval process, build toolchain, issuer key or filesystem
lies outside this experiment. Trusted policy bytes must agree with their parsed
policy and signed policy commitment. No live revocation, durable replay database,
chain identity, external admission or external task completion is implemented.
