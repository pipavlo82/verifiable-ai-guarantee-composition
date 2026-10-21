# v4.1: checker independence (O14) and authorization-scope binding of C

An isolated increment on v4 (`ee1143f`). No v4 file is edited: `src/v4`, `fixtures/v4`,
`evidence/v4`, `tests/v4` and `tools/v4` are byte-identical, and v4's 44 mutants are unchanged.
v4.1 lives in `src/v4_1`, `fixtures/v4_1`, `evidence/v4_1`, `tests/v4_1`, `tools/v4_1`.
The only edit outside those directories is `artifacts.sha256.json`, which gains entries for
the new files; no existing entry changes.

## The two gaps v4 leaves open

1. **Checker independence is not an obligation.** `authority()` compares each role's signer
   with `policy.authorized[role]` and never compares roles with each other. A policy that
   authorizes one key for provenance and judgment passes O01-O13, so a producer that judges
   its own output is authorized.
2. **C does not say what it authorized.** `evaluate()` returns `C = {status, authorized}`.
   The negative_O13 claim (`outputHash = 0x55…55`) is REFUTED under the output contract and
   VERIFIED under the replay contract, because replay never reads `outputHash`. A holder of
   `{claim, authorized: true}` then holds an authorization over a false output claim, with
   nothing in the result saying it was replay-only.

## What v4.1 adds

- **O14 `checker_independence`** (catalog + output contract revision 3, scenario-dependent,
  so the replay, attestation and provenance contracts do not require it). The recovered
  judgment signer must differ from the recovered provenance signer. It is UNVERIFIABLE when
  either signature does not verify, which is why O14 depends on O01, O07 and O08.
- **`C.binding = {scenario, claim_type, contract_sha256}`**. `contract_sha256` is SHA-256 over
  the sorted-key compact JSON of the exact contract object the evaluation used. It is
  recomputed in `evaluate()` and never read from the claim or a result. A claim that carries
  its own `contract_sha256` is not believed: the field is unconsumed, so C refuses it.
- **`unconsumed_claim_fields`**. Consumption is observed, not declared: the claim is wrapped
  so every read during each required obligation's check is recorded. Fields that no required
  obligation read refuse C (`claim_fields = REFUTED`). If a catalogued required check ended
  UNVERIFIABLE, its reads are unknown and `claim_fields` is UNVERIFIABLE instead.
- **`admit(result, evidence, contract, claim_type)`**, the consumer side. A presented result
  is never trusted on its own flags: C is recomputed from the evidence and the presented C must
  equal it exactly (status, authorized, every binding field). The digest is then recomputed from
  the contract the consumer holds and the requested claim type must match. Because the binding
  is derived from the contract object, an equal digest also fixes `binding.scenario` and
  `binding.claim_type` to that contract.

## Witnesses (fixed expectations in `src/v4_1/scenarios.py`)

| Witness | v4 C | v4.1 C |
|---|---|---|
| `negative_O14_self_judged`: one key signs provenance and judgment, policy authorizes it for both (fresh lab fixture, `tools/v4_1/create_self_judged_fixture.mjs`, keys not saved) | VERIFIED, authorized (v4 output contract) | REFUTED, only O14 non-VERIFIED |
| `omitted_O14`: same evidence, O14 deleted from the catalog | n/a | REFUTED, coverage alarm, `missing_obligations = [O14]` |
| `unconsumed_output_under_replay`: the negative_O13 claim under the replay contract | VERIFIED, authorized | REFUTED, `unconsumed_claim_fields = [outputHash]` |
| `reused_under_other_contract`: the self-judged result authorized under the v4 output contract, presented to a consumer holding revision 3 (same scenario name and claim type) | n/a | not admitted (digest differs) |
| `reused_under_other_claim_type`: `positive_replay`'s result with `LAB_OUTPUT_REPLAY_ADMISSIBLE` requested | n/a | not admitted |
| `reused_tampered_authorized` (review F1): the self-judged result with only `C.authorized` edited to true; `C.status` and O14 stay REFUTED | n/a | not admitted (admitted by the first v4.1 `admit`) |
| `reused_tampered_scenario` (review F2): `positive_output`'s result with `binding.scenario` removed | n/a | not admitted (admitted by the first v4.1 `admit`) |
| `reused_forged_binding`: `positive_replay`'s result with the whole binding rewritten to revision 3's scenario, claim type and digest | n/a | not admitted (admitted by the first v4.1 `admit`; found while fixing F1/F2) |

Controls: `positive_replay` admitted under its own contract and `positive_output` under
revision 3. All 54 v4 rows are carried with their v4 expectations, with three declared
adjustments: the output contract becomes revision 3 (+O14); the narrow-profile positives present
only the claim fields their contract reads (listed in `PROFILE_FIELDS`); and `omitted_O01`
expects B = UNVERIFIABLE, because with the provenance signature invalid O14 cannot compare signers.

## Results (this checkout, Python 3.12, Node 22.15.0, pinned dependencies)

- 57 rows (54 carried + 3 new), 7 reuse cases: all fixed oracles hold. C false authorizations
  0/53, positive authorizations 4/4, false admissions 0/5. (The first revision of this README
  said 58 rows and 4 new; the correct count is 57 and 3.)
- 16 tests, normal and `-O`.
- 9 physical mutants, each with its own witness and positive control, before / mutant /
  restored, in normal and `-O` mode: 9/9 KILLED, 0 survived, 0 crashed; source and catalog
  restored byte-exact. Sites: O14 catalog deletion, O14 presence, O14 verification,
  the `claim_fields` guard, the `admit` recompute-equality check (three witnesses: edited
  `authorized`, removed `binding.scenario`, rewritten binding), the `admit` digest recompute,
  the `admit` claim-type check.
- CI: `.github/workflows/coverage-v4_1.yml` runs the comparison, the tests in both modes and
  the mutations in both modes.

```sh
python -B tools/v4_1/run.py
python -B -m unittest -v tests.v4_1.test_v4_1
python -B tools/v4_1/mutations.py --out build/v4_1/mutations
python -B -O tools/v4_1/mutations.py --out build/v4_1/mutations-optimized
```

Outputs from this run are in `evidence/v4_1/validation`.

## Limits

- The self-judged fixture is a laboratory issuance, like v4's: genuine signatures over
  controlled assertions, not an external observation.
- O14 compares keys. It does not show that two different keys belong to different parties.
  Separation of key holders needs identity evidence this model does not have.
- Consumption means observation, not semantic validation: a field is consumed when a required
  obligation's check read it, whatever the check then did with the value. A predicate that reads
  a field without checking it would count it as consumed (the review's isolated witness shows
  this). Mutation controls cover the guard, not every
  predicate's read discipline.
- The contract digest is over the parsed contract (sorted-key compact JSON), not the file
  bytes. It identifies the contract content the evaluation used.
- The same separation rule (checker key differs from producer key, refused when the keys
  cannot be compared) is in the work-acceptance record profile 1.3
  (maximusrufus/work-acceptance-record @ `270e9fe`). O14 here is the laboratory form of that
  rule. It makes no claim of conformance to that profile.
