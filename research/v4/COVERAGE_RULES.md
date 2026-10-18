# Coverage rules and non-circular controls

The trusted contract is an input, not the output of verifier introspection. Review
fixtures/v4/contracts before fixtures/v4/catalog.json. Compare exact scenario
revision and claim type; check every required ID and its procedure, dependencies,
policy, authority and scope; require dependency closure; then evaluate evidence.
Source citations and coverage justifications are review metadata, not automatic
proofs that the contract is adequate or that the cited ERC mandates a research rule.

Two versions illustrate scenario dependence: lab-replay-v1 consumes O01–O12;
lab-output-v2 additionally consumes O13 because it asserts a requested output.
Keeping the former catalog after adopting the latter contract omits a necessary
binding. Changing the context without revising the contract is separately refused.

| Required negative family | Executable witness | Positive control | Mutation |
| --- | --- | --- | --- |
| All declared checks pass, omitted requirement | omitted_O05 (and all 13 omitted cases) | positive_output | O05-coverage |
| Silent catalog deletion | physical deletion of each O01–O13 | positive_output before/after restoration | 13 catalog mutants |
| Circular implementation inventory | circular_self_inventory | positive_output | O13-coverage, same isolated missing-output boundary |
| Genuine proof, wrong input claim | negative_O05 | positive_output | O05-verification |
| Valid judgment for another inference | negative_O07, signature over proof B while native proof A verifies | positive_output | O07-verification |
| Missing authority check | omitted_O08, valid unauthorized signature | positive_output | O08-coverage |
| Authentic receipt insufficient for claim | scope_overclaim | positive_output | composition |
| Unavailable required dependency | negative_O10, missing observation bytes | positive_output | O10-verification |
| New scenario with stale catalog/context | omitted_O13; stale_scenario | positive_replay; positive_output | O13-coverage; context |
| Claim stronger than evidence | negative_O12; scope_overclaim | positive_output | O12-verification; composition |

Each O01–O13 also has a fixed missing-evidence witness, missing_Oxx. Missing data
does not become a false cryptographic statement. Mixed refutation and missing
evidence preserves both statuses. All expected results are fixture literals, not
derived from current evaluator output.

## Mutation interpretation

For each obligation, mutate its physical catalog entry, its coverage enforcement
and its evidence enforcement separately. Fresh subprocesses prevent module-cache
effects. Preserve exact before/mutant/restored logs and positive controls.

Catalog deletion is KILLED by a specific coverage alarm and refusal, including on
the formerly positive input. It does **not** produce unsafe authorization. Coverage
and evidence enforcement removals are KILLED when their isolated negative witness
changes to authorization, while the positive control remains valid. These are
different detection effects and must not be conflated. Five additional guards
cover context, semantic definitions, composition scope, dependency closure and
unimplemented future requirements. Crashes are CRASHED, never KILLED.

No mutation result certifies universal requirement discovery. The missing-contract
branch has two conservative unknown results; it has functional tests, not an
isolated bypass mutation or a claimed killed control.
