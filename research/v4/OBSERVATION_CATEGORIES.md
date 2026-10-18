# Exploratory observation categories

These are provisional research interpretations, not a published formal model or
definitions/theorems attributed to Echo. They are not used as cryptographic
acceptance flags. Their unit is an observation with an explicitly stated context
and independence dimension, not a universal ranking of systems.

| Category | Provisional interpretation and required evidence | Positive example | Negative example / limit |
| --- | --- | --- | --- |
| DECLARED | A preserved explicit assertion with its claimed issuer/context | Preserved laboratory signed message bytes, regardless of truth | No statement supplied; declaration does not prove its content |
| DISCRIMINATING | A controlled intervention separates a stated alternative explanation or violated boundary | A physical enforcement removal changes the isolated negative decision, then restoration reverses it | Repeated identical output without an intervention; a crash is not discrimination of the intended authorization boundary |
| ATTRIBUTION | Authenticity and exact-statement binding under a specified key authority | Node and eth-account recover the declared laboratory signer, then policy checks its role | A valid signature from the wrong allowed-role key; key attribution is not causal execution attribution |
| INDEPENDENT | A specified verification dimension differs and its procedure/results are disclosed | Different Node/noble and Python/eth-account paths verify the same bytes | Re-running the same code is repeatability, not implementation independence; same machine/operator is not organizational independence |

src/v4/observations.py contains explicitly synthetic explanatory descriptors and
tests for non-implications. They are not fabricated empirical observations.
The corresponding empirical evidence is the raw signature, mutation and secondary
verification logs. Each category has positive and negative examples; no category
implicitly proves full provenance or task success.

A declaration can lack intervention, attribution and independent checking.
An anonymous experiment can discriminate without authenticating its producer.
An authenticated statement can lack causal discrimination. Independent arithmetic
recomputation can lack issuer attribution. Thus discrimination and attribution
are incomparable under these interpretations. In the chosen examples attribution
presupposes a statement, but that local implication is not a universal hierarchy.

Still undefined: the intervention/counterfactual semantics for complex workflows;
criteria for causal rather than key attribution; independence between libraries
with shared algorithms or trust roots; adversarial evidence acquisition; and how
these categories compose quantitatively. No numerical assurance score or total
order is assigned. Independent human review and independent contract elicitation
have not occurred.
