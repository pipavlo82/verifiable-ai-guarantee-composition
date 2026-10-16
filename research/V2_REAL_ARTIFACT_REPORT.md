# V2 real-artifact experiment report

## Outcome and acceptance boundary

The laboratory experiment is implemented and reproducible. **A complete external
real artifact chain is NOT IMPLEMENTED and is not reported as successful.** The
required full-chain positive cannot be supplied from the available artifacts; it
is an explicit UNVERIFIABLE case rather than a fabricated positive. The narrow
positive concerns public arithmetic recomputation and consistent signed references.

Verified starting main: `18a5916098addf6447700ed95441125bfa7079c3`. V1 `ea89871064e98a67b6ba01c836d498bee89aa437` is a merge parent and ancestor (git
merge-base --is-ancestor exit 0). Main CI runs 38930438758 and 38930438597 succeeded
at that exact main SHA. A fresh public clone reproduced v0/v1 before creating
`research/real-artifact-composition-v2`. The branch commit and draft PR are reported
in the publication record outside the self-referential commit; no merge is made.

## Real artifacts and missing links

Two genuine native `OpShardProof` instances were produced, serialized to 380-byte
files, and verified after deserialization in a separate process. Exact inputs,
weights, outputs, operator, public claims and toolchain are pinned. Ten actual
EIP-712 signatures were produced by OS-random laboratory keys, whose secret bytes
were never saved. Raw tensor bytes, identity transform commitments and signed
references are independently recomputed in replay. Two actual local file actions
have retained readback bytes and local observations.

This is a public one-op linear model, not a trained network. Native acceptance
is supplemented by full recomputation and does not establish a general cryptographic
soundness or privacy theorem. The chain id is a declared offline laboratory domain,
not an observed `block.chainid`. Consequently full WYRIWE deployment conformance,
external input admission, upstream judgment schema conformance, trusted chronology,
independent historical execution, ReceiptOS production integration and a full-chain
positive remain missing. A signature verifies an issuer's assertion, not its truth.
See [exact artifact formats](chain-v2/ARTIFACT_FORMATS.md).

## Test matrix

| Check | Normal | Repeat | Python -O / replay |
| --- | --- | --- | --- |
| v0 unittest suite from fresh main | 19 pass | 19 pass | 19 pass |
| v0 mutation controls | 8 killed | recorded deterministic comparison | 8 killed |
| v1 unittest suite from fresh main | 11 pass | 11 pass | 11 pass |
| v1 native probes | 2 exact tests pass | retained previous replay evidence | native Rust tests, not Python assertions |
| v1 genuine public signature controls | 11 cases pass | identical output | native JS unaffected by Python -O |
| v1 source mutations | 4 killed | deterministic | 4 killed |
| v2 unittest suite | 20 pass | 20 pass | 20 pass |
| v2 comparison | 26 declared outcomes match | byte identical | byte identical |
| v2 source mutations | 18 killed / 2 survived | source restored each time | same results and bytes |
| Saved native proofs | 2 pass | separate verifier processes | native verifier not a Python assert |
| Native upstream library probes | 2 tests pass at pinned source | locked offline build | original source clean |
| Exact public statement extraction | 2 match | deterministic | binary fields and artifact hashes checked |
| Source pins | 27 v0/v1 selected files rechecked | 12 v2 source-file locks added | immutable commit references |

Raw commands, exit codes, versions, stdout/stderr and SHA-256 are in
[`evidence/v2`](../evidence/v2). The SHA-256 inventory covers all tracked evidence
except its own manifest. V0/v1 protected files are byte-identical in the
[preservation record](../evidence/v2/preservation.json). Replay builds dependencies
once, then runs offline. Reproducing on the same computer in a fresh checkout is
independent of producer flags, but is not an independent human or hardware audit.

## Comparative experiment

Both consumers execute the same native and ECDSA component checks on the same
evidence. A grants a downstream claim when all four components verify individually.
B additionally evaluates the explicit bindings and claim-strength restriction.
This deliberately incomplete A is our research control, not an upstream product.

26 scenarios include 25 negative/unsupported claims. A falsely authorizes 18,
refuses 7, and classifies 3 as UNVERIFIABLE. B falsely authorizes 0, refuses all 25,
and classifies 4 as UNVERIFIABLE (the others are REFUTED). Missing evidence alone
is never a refutation; observed contradictions dominate aggregate status while
unknown obligations remain visible.

| Scenario | Declared expectation | A: component-only | B: composition |
| --- | --- | --- | --- |
| valid_recomputation | VERIFIED | VERIFIED | VERIFIED |
| complete_historical_chain_unavailable | UNVERIFIABLE | VERIFIED | UNVERIFIABLE |
| wrong_claim_input | REFUTED | VERIFIED | REFUTED |
| cross_subject | REFUTED | VERIFIED | REFUTED |
| wrong_model_version | REFUTED | VERIFIED | REFUTED |
| wrong_proof_reference | REFUTED | VERIFIED | REFUTED |
| valid_judgment_wrong_action | REFUTED | VERIFIED | REFUTED |
| valid_receipt_wrong_execution | REFUTED | VERIFIED | REFUTED |
| invalid_authority_valid_signature | REFUTED | VERIFIED | REFUTED |
| cross_domain_valid_signature | REFUTED | VERIFIED | REFUTED |
| replay | REFUTED | VERIFIED | REFUTED |
| scope_escalation | REFUTED | VERIFIED | REFUTED |
| wrong_policy | REFUTED | VERIFIED | REFUTED |
| wrong_output_claim | REFUTED | VERIFIED | REFUTED |
| raw_input_substitution | REFUTED | VERIFIED | REFUTED |
| receipt_result_substitution | REFUTED | VERIFIED | REFUTED |
| missing_judgment | UNVERIFIABLE | UNVERIFIABLE | UNVERIFIABLE |
| missing_input_bytes | UNVERIFIABLE | UNVERIFIABLE | UNVERIFIABLE |
| mixed_refutation_missing | REFUTED | UNVERIFIABLE | REFUTED |
| invalid_signature | REFUTED | REFUTED | REFUTED |
| invalid_provenance_signature | REFUTED | REFUTED | REFUTED |
| invalid_receipt_signature | REFUTED | REFUTED | REFUTED |
| valid_receipt_used_as_judgment | REFUTED | VERIFIED | REFUTED |
| native_proof_wrong_input | REFUTED | REFUTED | REFUTED |
| valid_other_native_component | REFUTED | VERIFIED | REFUTED |
| unknown_claim_kind | UNVERIFIABLE | VERIFIED | UNVERIFIABLE |

Timing is an exploratory paired three-repeat run over all 26 cases, including
process startup: median A 4.739205 seconds, median B
4.751762 seconds; median paired B-A difference
46.036 ms per 26-case pass. Raw pairs are
[retained](../evidence/v2/validation/benchmark.stdout.log). This is not a portable
overhead estimate, statistical significance claim or performance advantage.

## Mutation survival report

Twenty named implementation guards were each removed in source, executed against
their targeted witness in a fresh process, then restored. Restoration and the
positive control pass. Eighteen changes authorize the targeted negative and are
KILLED. Two remain refused and SURVIVE: `native_enforcement` is masked by input
bindings; `artifact_types` is masked by role-specific authority. These are incomplete
isolation witnesses, not proof that the guards are unnecessary. No crash counts as
a kill. The absent historical-execution verifier is UNVERIFIABLE and unexecuted,
explicitly outside the denominator of 20 executed mutations.

| Boundary | Classification | Witness |
| --- | --- | --- |
| provenance_preimage | KILLED | raw_input_substitution |
| input_binding | KILLED | wrong_claim_input |
| model_binding | KILLED | wrong_model_version |
| subject_binding | KILLED | cross_subject |
| proof_binding | KILLED | wrong_proof_reference |
| action_binding | KILLED | valid_judgment_wrong_action |
| authority | KILLED | invalid_authority_valid_signature |
| execution_binding | KILLED | valid_receipt_wrong_execution |
| output_binding | KILLED | wrong_output_claim |
| receipt_evidence | KILLED | receipt_result_substitution |
| domain | KILLED | cross_domain_valid_signature |
| scope | KILLED | scope_escalation |
| policy_binding | KILLED | wrong_policy |
| replay | KILLED | replay |
| claim_strength | KILLED | complete_historical_chain_unavailable |
| artifact_types | SURVIVED | valid_receipt_used_as_judgment |
| judgment_signature | KILLED | invalid_signature |
| provenance_signature | KILLED | invalid_provenance_signature |
| receipt_signature | KILLED | invalid_receipt_signature |
| native_enforcement | SURVIVED | native_proof_wrong_input |
| historical_execution_verifier | UNVERIFIABLE | not executed |

## Formal and prior-art findings

The [typed model](chain-v2/FORMAL_MODEL.md) separates an elementary definition-level
aggregation proof, finite empirical evidence, candidate preservation hypotheses,
and unimplemented integration. Its candidate sufficiency statement requires sound
native predicates, correct representation maps, authenticated applicable authority,
complete bindings and downstream entailment. Those premises are not all proved.

Assume-guarantee reasoning, proof-carrying authorization, RATS appraisal, AEX request
and transformation bindings, and composable attestation all substantially precede
or overlap this research. The proposed contribution is a version-specific executable
map of residual obligations and real-crypto substitution witnesses. **Novelty is not
established.** See the bounded [prior-art comparison](RELATED_WORK.md).

## Next acceptance gates and recommendation

1. Obtain a consensually redistributable externally issued WYRIWE artifact with exact
   admitted preimages, observed chain domain and authorized signer history.
2. Use an upstream proof profile with an established public statement and reviewed
   soundness properties; retain model, weights, circuit and toolchain.
3. Capture an authentic upstream judgment with exact policy and action binding,
   and independently evidenced commitment-before-execution where required.
4. Integrate an actual ReceiptOS-compatible receipt plus independent evidence of
   the exact external execution and result; never fill this gap with a signature.
5. Reproduce one full-chain positive and all substitutions, isolate surviving
   mutants, implement durable replay state, then seek independent specialist review.

Recommendation: **CONTINUE** the bounded experiment and acquisition of missing
artifacts; **HOLD** full-chain, security-certification, novelty and award claims.
