# Load-bearing mutation results

New applied mutations: **22 KILLED, 0 SURVIVED, 0 CRASHED, 0 NOT_APPLIED, 0 UNVERIFIABLE**.
17 adapter mutations reproduce under normal/repeat/-O; five actual Solidity source-copy
mutations reproduce against the unchanged BIP340 library. Historical PR7's 22 kills
are reported separately and not added to this new count.

Each adapter kill requires a rejected baseline negative witness becoming authorized,
then rejection after restoration, plus positive controls in all three configurations.
Each Solidity kill additionally requires actual 1,000,000-unit token movement in the
mutant and no movement for the baseline/restored negative. A crash cannot satisfy it.
The precise old/new source strings and all command/log hashes are preserved.

| Layer | Mutation | Classification | Distinguishing witness |
|---|---|---|---|
| adapter | authorization | KILLED | B_missing_obligation |
| adapter | record | KILLED | Q_record_tamper |
| adapter | scope | KILLED | A_wrong_scope |
| adapter | scenario | KILLED | changed_scenario_digest |
| adapter | evidence | KILLED | K_evidence_digest |
| adapter | profile | KILLED | R_other_profile |
| adapter | chain | KILLED | D_other_chain |
| adapter | escrow | KILLED | C_other_escrow |
| adapter | recipient | KILLED | E_other_recipient |
| adapter | amount | KILLED | F_other_amount |
| adapter | payment | KILLED | G_other_payment |
| adapter | nonce | KILLED | nonce_reused_other_job |
| adapter | expiry | KILLED | I_expired |
| adapter | revocation | KILLED | J_revoked |
| adapter | trusted_signer | KILLED | J_unauthorized |
| adapter | consumption | KILLED | nonce_reused_other_job |
| adapter | verdict_preimage | KILLED | valid-unrelated-signature |
| Solidity copy | chain | KILLED | chain |
| Solidity copy | escrow_address | KILLED | address |
| Solidity copy | trusted_signer | KILLED | signer |
| Solidity copy | replay_guard | KILLED | replay |
| Solidity copy | state_consumption | KILLED | replay |

Six requested on-chain semantic guards do not exist upstream and therefore cannot be
removed: recipient-preimage comparison, amount-preimage comparison, global nonce
consumption, expiration, revocation and claim-scope verification. These are separately
**NOT_APPLIED (6)**, not kills or evidence of mutation coverage. Recipient/amount and
nonce guards are tested where they actually exist in the external adapter.

Zero surviving applied mutants is a finite suite result, not full coverage. Token
behavior, identity/controller ownership, private-server correctness and all possible
malformed inputs have not received exhaustive mutation analysis.
