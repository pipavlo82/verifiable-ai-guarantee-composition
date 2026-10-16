# Research question

Can individually valid proofs, attestations and receipts yield an unauthorized downstream claim when their subjects, inputs, scopes or dependencies do not align?

The cryptographic version of this question remains open in this repository. V0 tests a finite synthetic analogue: internally valid arithmetic witnesses and integrity envelopes can be combined incorrectly by a verifier that omits bindings. It does not exhibit a failure of any upstream cryptographic protocol.

Hypothesis H1: component validation alone is insufficient for a caller-selected composed claim in the reconstructed fixture model. H2: explicitly enforcing all specified bindings refuses the constructed counterexamples while preserving the positive control. H3: removing each boundary changes its designated negative control. These are experimentally testable hypotheses, not universal theorems.

Unit of evaluation: an independently selected request, a pinned trusted policy, and five supplied component envelopes. All result counts refer to the fixed corpus, not population-level false-positive rates. No claim is made about original archive contents, production workloads or adversary prevalence.

The principal counterexample uses a square model. An internally correct witness for -3 produces the same output as the requested input 3. A same-output check alone cannot establish the requested input relation. Other controls separate authentic judgment from permission and intact receipt from requested execution.
