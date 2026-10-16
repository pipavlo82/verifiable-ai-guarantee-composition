# Current v2 status

The current typed G1-G8 model, assumptions, failure classifications and dependency graph are in [v2 formal model](chain-v2/FORMAL_MODEL.md). Its positive scope is public MatMul recomputation under a laboratory policy. External admission and historical execution remain UNVERIFIABLE. The earlier synthetic model below remains historical context.

---

# Guarantee model

A guarantee descriptor is `(subject, scope, authority, evidence, dependencies, assumptions, verifier, failure)`. The table defines the research model and its limited v0 realization. These are not invented upstream promises. Every row inherits the trusted caller policy, correct local implementation/runtime, and synthetic-only assurance ceiling.

| ID | Subject and scope | Authority | Evidence and verification | Dependencies | Assumptions | Failure classification |
|---|---|---|---|---|---|---|
| G1 Input provenance | Requested input bytes under identity-v0 | Caller-selected input digest; fixture producer | Recompute raw/input identity and SHA-256; compare provenance input to request | Provenance envelope | Input is canonical decimal integer text; source origin is simulated | Contradictory digest/transform: REFUTED; missing bytes/unsupported representation: UNVERIFIABLE |
| G2 Model/version binding | Exact square model id and integer version | Caller-selected model/version | Compare model record and witness metadata to request; require known toy operation | Model and proof components | Toy version identifies x*x; no weights or zkIE model are loaded | Known mismatch: REFUTED; missing/unsupported: UNVERIFIABLE |
| G3 Inference validity and statement | Claimed output for the bound input/model | Local arithmetic evaluator | Recompute x*x, input digest and requested output; join witness input to provenance | G1, G2 plus witness | Arithmetic recomputation substitutes only a toy relation, not a succinct/ZK proof | Arithmetic or binding contradiction: REFUTED; unavailable witness: UNVERIFIABLE |
| G4 Subject binding | Caller subject-A across all records | Caller-selected subject | Compare every component subject exactly | All five components | Subject strings are fixture identities, not registry identities | Any distinct subject: REFUTED; unavailable subject: UNVERIFIABLE |
| G5 Judgment authenticity | Exact judgment body, including issuer and scope | Trusted public fixture catalog | Recompute judgment body digest and look it up under issuer | Judgment component and external catalog | Catalog stands in for authenticity; not cryptography and trivially writable outside the model | Known nonmember: REFUTED in catalog model; missing/unsupported evidence: UNVERIFIABLE |
| G6 Judgment authorization | Approval for exact action and policy | Caller policy authorized_judges | Check authentic issuer is allowed, action and policy match | G5 and judgment | Authentic approval does not establish soundness or suitability | Wrong issuer/action/policy: REFUTED; unavailable judgment: UNVERIFIABLE |
| G7 Execution receipt binding | Exact requested execution, action, output and proof body | Caller-selected execution id; fixture recorder | Recompute proof digest, compare receipt fields to request and actual witness | G3, G4 plus receipt/proof components | Fixture recorded completion is not observation of external execution | Wrong execution, proof digest, action or output: REFUTED; missing receipt: UNVERIFIABLE |
| G8 Downstream authorization | Caller claim with scope, assurance, domain, time, nonce and policy | Caller policy-v0 | Require all G1-G7, scope subset of every dependency, SYNTHETIC ceiling, domain equality, validity interval and unused nonce | G1-G7 and all envelopes | Static policy snapshot; scope sets have literal action semantics; no concurrent consumption | Any demonstrated violation: REFUTED; any unestablished dependency without contradiction: UNVERIFIABLE |

The implementation reports local predicate results for G1-G7 and their direct component prerequisites. The dependency graph above is closed at G8; it does not misleadingly promote a locally satisfied G6 into an independently authenticated judgment. G8 and overall status include every required premise. Explicit refutation dominates unknown for this conjunction; it refutes the composed claim, not every component.

Strength is a deliberately tiny partial order: v0 can establish only SYNTHETIC. REAL_CRYPTO is not reachable. Unknown schemes are not silently mapped into this order. Scope is a finite set of literal actions; no general policy entailment solver is claimed. Model, subject, execution and domain bindings use equality, not fuzzy equivalence.
