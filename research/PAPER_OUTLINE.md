# Research paper outline — v2 working draft

1. **Abstract.** Describe a reproducible experiment on guarantee preservation;
   report native artifacts and genuine laboratory signatures, scoped results and
   the unavailable external execution link. Make no novelty or vulnerability claim.
2. **Problem statement.** Ask which explicit binding, authority and scope conditions
   permit component predicates to justify a downstream claim.
3. **Formal definitions.** Typed evidence, G1-G8 guarantees, representations,
   dependency graph, caller policy, tri-state aggregation and scope entailment.
4. **Threat model.** Reuse of valid unrelated components; missing bytes, wrong
   authority/domain, replay, mixed failures; trusted local verifier and lab keys.
5. **Composition proposition candidates.** State conditional sufficiency and
   profile-dependent necessity with all assumptions. Distinguish definition-level
   facts from unproved cryptographic and system propositions.
6. **Counterexamples.** Genuine signatures for other actions/executions/domains;
   valid native component from another input; receipt assertion versus occurrence.
7. **Experimental methodology.** Pinned sources, exact native wire format, real
   EIP-712 verification, same-evidence A/B comparison, normal/repeat/-O,
   independent arithmetic recomputation, source mutations and fresh-checkout replay.
8. **Results.** 26 scenarios, 20 test methods, 18/25 versus 0/25 negative
   authorizations, 18 killed/2 surviving executed mutants, missing evidence and
   exploratory paired timing. Link raw logs and exact commit, not screenshots alone.
9. **Prior art.** Assume-guarantee reasoning, proof-carrying authorization, RATS,
   AEX, composable attestation and upstream drafts. Novelty remains unestablished.
10. **Limitations.** Self-authorized laboratory keys, offline domain, public
    test-style native protocol, full recomputation, no independently evidenced
    historical execution or complete external chain, incomplete mutant isolation.
11. **Future work.** Externally issued coherent chain, reviewed proof profile,
    authority/key history, durable replay state, independent reproduction,
    mechanized preservation argument and specialist academic review.

Status: experimental manuscript outline, not a submitted or peer-reviewed paper.
Recommendation: CONTINUE research; HOLD broader claims until acceptance gates pass.
