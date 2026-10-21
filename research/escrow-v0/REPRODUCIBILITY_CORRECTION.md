# Gas measurement versus semantic determinism

The initial experiment commit bf40a1de626ee8e61afffac10243d1ba00610e42 passed its
initial checkout. A relocated fresh checkout completed every test/mutation command
successfully but the final validator returned 1: its full comparison JSON included
gas measurements sensitive to the harness's output-path length and cumulative EVM
memory allocation. Raw failure is preserved, not rewritten as a successful run.

The compiled contract runtime was identical. Nineteen cross-checkout gas rows differed
by 1-3 gas; authorization, statuses, token deltas, exact off-chain vectors and mutation
reports agreed. A separate actually executed 31-vector control using the reference
output-path length reproduced gas in all comparable call contexts. Five rows written
by separate test methods in the full suite were explicitly excluded from that causal
comparison. Its first selector matched zero tests and is labeled INVALID; the corrected
probe requires one successful test method and 31 vector records.

This follow-up changes only the experimental validation harness. It compares all
semantic report fields exactly, excluding two explicitly named gas measurement
fields. Per-mode gas values and their raw equality are still reported separately.
Four tests demonstrate sensitivity to changed authorization, payment delta,
classifications, aggregate counts and unexpected fields. They also require a changed
gas measurement to remain visible in raw data while preserving claim semantics.

The adapter, proof verifier, upstream escrow, PR7, ERC-8404 Core and historical test
evidence are unchanged. The original inventory is retained at
evidence/escrow-v0/history/SHA256-bf40a1de.json, identifying bytes in that Git commit.
Updated SHA256.json describes the current checkout. Fresh results for the final exact
commit are recorded in the external closure report. No additional security mutation
kill is claimed for these four validation-harness tests.
