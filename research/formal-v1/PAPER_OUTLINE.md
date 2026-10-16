# Revised paper outline: candidate research, not a priority claim

1. **Abstract.** State the specific composition question, exact experimental scope and incomplete real integration. Report reproducible observations without claiming an upstream vulnerability.
2. **Problem statement.** Determine the additional obligations required to authorize a particular downstream claim after native components verify.
3. **Related work.** Assume-guarantee reasoning, proof-carrying authorization, RATS, AEX, composable attestation, action capsules and the pinned upstream drafts. Explain overlaps before proposing a distinction.
4. **Formal definitions.** Typed facts, evidence scopes, native premises, representation bridges, authority policy and tri-state results. Separate equality of identifiers from action conformance.
5. **Threat model.** A consumer receives authentic but unrelated objects, unavailable dependencies or incompatible representations; cryptographic primitives are assumed sound. Honest upstream rejection is not an attack result.
6. **Established lemma and theorem candidates.** Give the standard equality-closure proof. State the full application-specific composition rule conditionally; do not promote unmet premises to a theorem about deployed software.
7. **Counterexamples.** Every removed abstract equality has a witness; normalization is non-injective; a genuine signature survives a changed consumer request while binding fails.
8. **Methodology.** Pinned sources, independent finite oracle, source mutations with crash separation, native test execution, locked-library signature replay, deterministic outputs and fresh-checkout verification.
9. **Results.** Distinguish v0 synthetic baseline, v1 abstract enumeration, four implementation mutations, public event verification and two native library tests. No single combined end-to-end success rate.
10. **Limitations.** Toy graph, conditional authority, no coherent tuple, no portable zkIE proof capture, no EIP-712/receipt integration, bounded prior-art coverage and no cryptographic audit.
11. **Future work.** A real common-subject tuple, executable representation/conformance bridges, stronger baselines, broader case coverage and independent reproduction/review.

The scientific contribution remains a hypothesis until the profile-specific analysis and real coherent experiment distinguish it from prior work.
