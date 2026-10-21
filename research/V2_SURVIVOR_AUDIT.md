# V2 follow-up: audit of the two surviving mutants

## Result

Both survivors at `ba889271bef7cb3d2eed00067a12064689bfb627` are **non-equivalent mutations with inadequately isolated original witnesses**. This is an empirically verified result in the supported laboratory policy/input space, not a formal proof of general coverage or an independent human review.

The verifier did not need a logic change. New negative fixtures isolate one failed obligation each. Removing the exact original check changes each new negative from REFUTED to VERIFIED; restoring the source restores REFUTED. The positive remains VERIFIED throughout. Mutant source SHA-256 values match the original published mutants exactly.

| Boundary | Why the original witness survived | New isolated witness | Original / mutant / restored |
| --- | --- | --- | --- |
| `native_enforcement` | Wrong input also failed `input_binding` and `provenance_preimage` | Change one claimed scalar in the retained proof; sign consistent references to the explicitly invalid proof | REFUTED / VERIFIED / REFUTED |
| `artifact_types` | Receipt-as-judgment also failed signer `authority` | Genuine `LabReceipt` signature from the authorized judgment-role key, with otherwise matching fields | REFUTED / VERIFIED / REFUTED |

Only `inference` fails in the first unmutated case; only `artifact_types` fails in the second. All three signature checks succeed in both. Native verification actually exits 1 on the corrupted proof and succeeds on the type case. Even under the first mutant, the native component is still REFUTED: the removed check is enforcement of that result in composition.

## Evidence and provenance

The [machine-readable audit](../evidence/v2/survivor-audit/validation/normal/report.json) contains before, mutant and restored outcomes, original masking obligations, source hashes and classifications. The [validation matrix](../evidence/v2/survivor-audit/validation/report.json) records commands, runtime versions, stream hashes and exit codes; adjacent files retain raw outputs.

Original verifier SHA-256: `71ad471dcb2f322da56eea20060e9a5c8f0930bb87f7e0549b8cfaf2939ba69c`.

| Mutant | Source SHA-256 |
| --- | --- |
| `native_enforcement` | `c25ff4efd51b31cea502e60f296988553598aa33c484edef3347a9715d9fc306` |
| `artifact_types` | `96a62435250a26ae42fe91b9f468ad1ba21ae0bf9330b13d9a609b97cac9ff27` |

The invalid proof changes the first claimed scalar at byte offset 12 by one modulo the Goldilocks field. Every other byte, input, weight and output is retained. Its new digest is `2393d093f86b4428ab9ffee293b72e476fca5084cfb7c461dc82435a656a3fee`. This is a deliberately invalid negative artifact, never presented as a genuine valid proof.

Six unique EIP-712 signatures were actually generated using three fresh OS-random laboratory keys. Secret keys were held only in memory. The three cases reuse signatures when the exact signed statement is identical. The supported policy changes only the role public keys; the claim's policy digest is updated accordingly. Domain, model, scope, schema and three-role separation remain unchanged. A signed assertion does not establish occurrence, chronology or external authority.

The type witness is signed as `LabReceipt` from the outset; it is not a relabeled `LabJudgment` whose signature would fail. Reusing retained observation bytes asserts no new execution. Fixtures and the generation recipe are [preserved here](../evidence/v2/survivor-audit/witnesses/generation.json). Replay requires no private keys, signing, proof generation, QPU invocation or external service.

## Executed validation

| Check | Result |
| --- | --- |
| New regression tests, normal / repeat / Python `-O` | 7 / 7 / 7 pass |
| Exact source mutation audit, normal / repeat / Python `-O` | 2 KILLED in each run |
| Follow-up counts | 2 KILLED, 0 SURVIVED, 0 CRASHED, 0 NOT_APPLIED, 0 UNVERIFIABLE |
| Determinism | Compact audit reports identical across the three modes |
| Deliberately removed check, actual targeted unittest | Each of 2 tests fails by assertion, with no test error |
| Source restored, all new tests rerun | 7 pass; original source bytes restored |
| Original witnesses under the same mutants | Still REFUTED, reproducing the original masking |

Crashes do not count as kills. The deliberate red-test exit 1 is required to be an assertion failure, not an exception. Separate fresh Python processes prevent mutated imports from contaminating subsequent runs. The audit must not run concurrently with other source-mutation jobs in the same checkout.

The original 20-mutant run remains **18 KILLED / 2 SURVIVED** in its frozen evidence. This additive run covers just those two survivors with new witnesses. It is incorrect to rewrite the original run as 20 kills, claim two new mutation operators, or infer comprehensive security coverage from zero survivors in this follow-up.

## Reproduce

Follow the [v2 dependency preparation](chain-v2/REPRODUCE.md), including the pinned native source/toolchain and locked JavaScript dependencies. Use a full Git clone: the audit reads the original verifier from the exact published commit.

```sh
python -B tools/verify_artifacts.py
python -B tools/v2/validate_survivors.py
python -B tools/verify_artifacts.py
```

The driver executes all three Python modes, exact source mutations, positive controls, two red tests and restoration. `build/v2/survivor-validation/report.json` is the new host report; its deterministic audit subreport must match the committed snapshot. Freshly generating signatures would intentionally produce different bytes, so replay uses the preserved fixtures. The generator refuses to overwrite them.

## Interpretation and next step

A surviving mutant can be redundant on a finite corpus without being semantically equivalent. These two distinguishing inputs disprove equivalence over the verifier's supported caller-selected laboratory policies and artifacts. They do not establish behavior for arbitrary deployment policies or justify broader scientific priority.

The code and new tests share an author. Fresh processes, fresh checkout replay and GitHub CI provide reproducibility; they are not independent academic review. The appropriate next step is an external technical review of the isolated witnesses and the authority assumptions. PR #2 remains a draft, with no merge or researcher contact performed by this audit. The absent external WYRIWE admission and historical execution links remain UNVERIFIABLE; end-to-end success is not claimed.
