# Scoped Authorization from Heterogeneous Verification Artifacts

**Integration addendum to the preserved v3-v4 research draft. Independent research;
not peer reviewed.** The earlier paper and historical results remain byte-identical.

## Abstract

We study an external consumer that joins native inference replay with a recomputable
artifact-identity receipt and authenticated review. The two component profiles retain
their original claim identifiers, canonicalization rules, subjects and evidence.
An independently supplied scenario contract identifies required obligations and exact
profile commitments. The consumer checks proof-byte identity, claim values, policy
scope and conditional role separation, then recomputes authorization at admission.
Controlled counterexamples and isolated mutations test whether these boundaries affect
the decision. Results concern this finite laboratory experiment; no complete external
AI execution chain or general security theorem is established.

## Method and definitions

Let I and R be the exact statements of the native and receipt/review profiles. The
joint claim is `(I, R, proofBytes(I)=proofBytes(R), requestedScope)` under a trusted
contract K. The claim is not an assertion that the component subject labels denote
the same real-world entity. Coverage checks the declared catalog against K and the
minimum published contract for the supported joint claim type. Verification executes
the selected component procedures. Composition consumes only their checked statements.
Admission reruns these steps rather than trusting the serialized authorization flag.

Candidate conditional proposition: if both component verifiers are sound for their
stated predicates, K is adequate, scope mapping preserves those predicates, and the
admission verifier executes the same bindings over identical bytes, then authorization
establishes their conjunction under those assumptions. This is a proposition requiring
formalization and proof, not a theorem derived from successful tests.

## Counterexamples and empirical findings

Two individually valid components can concern different proof artifacts. A predicate
can observe an unchecked claim field. A receipt can reproduce byte identity while an
external execution claim remains unsupported. Different signing keys can have the
same controller. A consumer that trusts a presented flag can accept an edited decision.
The executable witnesses, mutation classifications and comparison counts are linked
from `EXPERIMENT_RESULTS.md` and `MUTATION_REPORT.md`.

## Relationship to prior work

Assume-guarantee reasoning, proof-carrying authorization, remote attestation and
evidence provenance already address scoped guarantees and trusted dependencies.
The preserved `research/PRIOR_ART_ANALYSIS.md` and `research/v4/PRIOR_ART.md` document
that overlap. This addendum contributes an implementation-specific, reproducible
compatibility experiment; it does not establish scientific priority or novelty.

## Limitations and next stage

The complete external chain remains partial. Original input admission, deployed
model authority, a genuinely linked external judgment and independent execution
evidence must be obtained and checked before a broader claim can be considered.
Contract adequacy needs independent review. Organizational independence, revocation,
durable replay prevention, hostile-resource handling and formal soundness remain open.
