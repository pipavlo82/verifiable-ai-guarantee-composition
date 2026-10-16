# Paper outline

## Abstract
Study guarantee preservation when inference, provenance, judgments and execution evidence cross verifier boundaries. Report a reconstructed synthetic experiment with explicit limits. Present real-artifact integration as future work.

## Problem statement
Individually valid components may refer to different inputs, subjects, actions or scopes. Ask which explicit relations are necessary for a downstream authorization claim. Distinguish this research question from a claim that upstream systems omit these relations.

## Formal definitions
Define evidence subjects, authority, scope, assurance order, dependencies and caller policy. Define G1-G8, tri-state evaluation and conjunction/refusal semantics. Separate cryptographic validity, authenticity, semantic correctness and authorization.

## Threat model
Evidence substitution, omission, authentic wrong-action judgments, invalid authority, unrelated receipts and scope/replay mismatch. State trusted policy, synthetic authenticity oracle and runtime assumptions.

## Composition theorem candidates
Conditional scope preservation on acyclic graphs; refusal preservation under unavailable dependencies; authenticity/authorization separation. Label each candidate unproven beyond the implemented finite model. Specify proof obligations for translations and authority resolution.

## Counterexamples
Equal-output/different-input square witnesses; cross-subject substitution; wrong model/version; valid judgment about another action; intact receipt for another execution; unknown dependency and replay/scope cases.

## Experimental methodology
Publish exact fixture bytes and policy, fixed oracle labels, source pins, identical-input A/B comparison, normal/repeat/optimized runs, deterministic reports and source-removal mutants with restoration. Separate timing from deterministic artifacts.

## Results
Populate from `evidence/validation/experiment-normal.stdout.json` and mutation output. Report numerator and denominator for each metric, unknown outcomes separately, all mutation classifications and raw timing distribution. Do not substitute upstream performance or real cryptographic claims.

## Limitations
Unrecovered archive, synthetic modes, weak comparator selection, shared implementation authorship, finite graph/mutant set, no real proof/signature/receipt adapters, no durable replay state or deployment audit.

## Future work
Obtain genuine artifacts; implement pinned verifiers and exact statement translation; test real substitutions without forging cryptography; independently reproduce in another implementation; formalize candidates; broaden corpus and mutation operators.
