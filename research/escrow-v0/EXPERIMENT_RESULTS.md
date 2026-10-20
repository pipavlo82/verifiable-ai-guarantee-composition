# Executed results

Initial isolated checkout: all commands in `evidence/escrow-v0/validation/commands.json`
completed with exit 0. This file reports those executions. The subsequent exact-commit
fresh checkout, fresh native build and cross-checkout comparison are captured in the
external closure bundle, not backdated into this commit.

| Suite | Normal | Repeat | Python -O / optimized FFI |
|---|---|---|---|
| New Python unit methods | 9/9 | 9/9 | 9/9 |
| New Foundry test methods | 7/7 | 7/7 | 7/7 |
| Main end-to-end vectors | 31/31 expected | 31/31 expected | 31/31 expected |
| Python/Node digest and Schnorr cross-check | 33/33 agree | 33/33 agree | 33/33 agree |
| Adapter source mutations | 17 killed | 17 killed | 17 killed |
| Original escrow tests | 7/7 | not separately repeated | not applicable |
| Isolated Solidity mutations | 5 killed, each baseline/mutant/restored | covered by fresh replay | Python mode does not change Solidity |
| Unchanged PR7 tests | 16/16 | baseline regressions run once here | unchanged historical evidence retained |
| Unchanged PR7 mutations | 22 killed | historical reports preserved | not counted as new mutations |

Normal/repeat/optimized semantic outputs, all off-chain vector bytes, Node comparison
results and adapter mutation reports are identical. All 10,709 baseline files and
10 vendored upstream files remain byte-identical. The inherited integrity check also
verifies 13 frozen Core files, 18 PR5 imported files and 9,251 preserved PR6 files.
No new GitHub CI is claimed: publication was prohibited.

## Finite comparative domain

31 vectors comprise one positive, 28 authorization-negative cases and two token
execution controls. The authorization comparison excludes the two execution-only
controls, so its denominator is 29 (one positive + 28 negatives), identical for A/B/C.
All configurations accept the positive.

A verifies a signature against the selected trusted signer; it does not recompute
claim semantics. B recomputes claim-aware policy and exact signed preimages at
issuance/admission. C additionally executes the unchanged escrow's on-chain checks.
The raw chain is deliberately exercised even for B refusals to distinguish off-chain
gating from mandatory on-chain enforcement.

| Mode | Incorrect downstream authorizations / 28 | Correct refusals / 28 | UNVERIFIABLE (included in refusals) | Cases detecting missing obligations |
|---|---:|---:|---:|---:|
| A | 24 | 4 | 0 | 0 |
| B | 2 | 26 | 2 | 2 |
| C | 2 | 26 | 2 | 2 |

The two residual cases in B and C are expiration and revocation **after signing**.
They are lifecycle counterexamples to reusing the earlier admission, not false
decisions at the original signing instant. No new B evaluation at execution time
is claimed. Revocation is a declared laboratory policy change; no external revocation
transaction or production signer revocation was observed. The immutable contract has
no revocation input. Expiration is directly exercised by advancing the EVM clock.
These two counterexamples are distinct from mutation survivors (there are none among
the 22 applied new mutations).

The raw contract accepts 19 rows marked NOT_COVERED for the broader requested policy.
That includes the lying-token execution control, not 19 demonstrated upstream bugs.
The narrower signature/escrow guarantee is not misrepresented as full claim coverage.

## Positive and negative vectors

VERIFIED means the stated layer established its own guarantee. REFUTED is a failed
enforced check. UNVERIFIABLE is unavailable evidence. NOT_COVERED means the existing
on-chain contract contains no corresponding semantic enforcement. No infrastructure
failure is mapped to REFUTED or KILLED.

| Vector | Off-chain | On-chain policy classification | Observed recipient delta (mock base units) | Warm release-call gas |
|---|---|---|---:|---:|
| positive | VERIFIED | VERIFIED | 1000000 | 36654 |
| A_wrong_scope | REFUTED | NOT_COVERED | 1000000 | 36651 |
| B_missing_obligation | REFUTED | NOT_COVERED | 1000000 | 36603 |
| C_other_escrow | REFUTED | REFUTED | 0 | 9991 |
| D_other_chain | REFUTED | REFUTED | 0 | 10004 |
| E_other_recipient | REFUTED | NOT_COVERED | 1000000 | 36715 |
| F_other_amount | REFUTED | NOT_COVERED | 2000000 | 36728 |
| G_other_payment | REFUTED | REFUTED | 0 | 10045 |
| H_replay | REFUTED | REFUTED | 0 | 1618 |
| I_expired | REFUTED | NOT_COVERED | 1000000 | 36650 |
| J_unauthorized | REFUTED | REFUTED | 0 | 10009 |
| J_revoked | REFUTED | NOT_COVERED | 1000000 | 36789 |
| K_evidence_digest | REFUTED | NOT_COVERED | 1000000 | 36801 |
| L_no_contract | UNVERIFIABLE | NOT_COVERED | 1000000 | 36738 |
| M_unverified_field | REFUTED | NOT_COVERED | 1000000 | 36826 |
| N_self_judgment | REFUTED | NOT_COVERED | 1000000 | 36763 |
| O_duplicate | REFUTED | REFUTED | 0 | 1717 |
| P_incorrect_authorization | REFUTED | NOT_COVERED | 1000000 | 36788 |
| Q_record_tamper | REFUTED | NOT_COVERED | 1000000 | 36800 |
| R_other_profile | REFUTED | NOT_COVERED | 1000000 | 36888 |
| nonce_reused_other_job | REFUTED | NOT_COVERED | 1000000 | 36901 |
| changed_scenario_digest | REFUTED | NOT_COVERED | 1000000 | 36914 |
| missing_profile | UNVERIFIABLE | NOT_COVERED | 1000000 | 36926 |
| expired_after_signing | VERIFIED | NOT_COVERED | 1000000 | 36939 |
| revoked_after_signing | VERIFIED | NOT_COVERED | 1000000 | 36951 |
| false_returning_token | VERIFIED | REFUTED | 0 | 11868 |
| high_s | REFUTED | REFUTED | 0 | 3953 |
| invalid_signature | REFUTED | REFUTED | 0 | 3937 |
| refund_then_release | REFUTED | REFUTED | 0 | 1910 |
| lying_token | VERIFIED | NOT_COVERED | 0 | 13901 |
| negated_s | REFUTED | REFUTED | 0 | 10363 |

A separate actual two-payment witness releases two escrows with submissionId 7,
observing 2,000,000 mock units. Same-escrow replay is rejected; global nonce uniqueness
is not provided. The false-return token reverts without payment. The lying token
returns success with zero recipient delta, illustrating the trusted-token assumption;
this is not a statement about the deployed Base token.

## Gas and cost

The positive warmed local release call costs 36,654 gas and moves 1,000,000 mock
base units. Per-vector gas is above and in the machine-readable report. This excludes
transaction intrinsic/calldata gas, Base L1 data fees and cold-state effects. At a
purely hypothetical 1 gwei, that call-only term is 36,654,000,000,000 wei; it is not
a Base transaction-fee estimate. Actual network execution cost and real funds used: 0.
Off-chain runtimes are raw local command measurements, not a performance benchmark.
