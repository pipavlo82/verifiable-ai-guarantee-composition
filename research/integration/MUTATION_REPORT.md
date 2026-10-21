# Mutation evidence

Historical evidence is never overwritten. Raw current executions live under
`evidence/integration/` and fresh replay writes to `build/integration/validation`.

PR5's nine original controls are reproduced by its physical mutation CLI. They
represent seven distinct edits: three negative witnesses target the same admission
recomputation guard. Eight controls expose unsupported admission; catalog deletion
is detected by loss of the positive control. Targeted exact-edit replay additionally
runs in normal/repeated/optimized modes. Crashes are not counted as kills.

PR6's original report remains **16 KILLED / 1 SURVIVED**. Its exact fallback replaces
the required canonical byte-carrier with `case['contract']`. The preserved original
witness removes both carriers, so the mutant still refuses. The new isolated witness
removes only canonical bytes while retaining the complete parsed preimage: baseline
UNVERIFIABLE, mutant VERIFIED, restored UNVERIFIABLE. This is **KILLED for the canonical
carrier policy**, not evidence of authorization without a contract preimage. The
substituted parsed contract is also refused. Global equivalence is not established.

The joint implementation executes 22 source-copy mutations:

- J01-J09: force each individual joint obligation to VERIFIED under its negative witness.
- Coverage, definition equality, dependency closure and the independently published
  minimum scope contract: remove each enforcement check separately.
- Unknown obligation dispatch: permit an unknown ID to borrow a known procedure.
- Recovered-key inequality: trust an O14 label whose declared procedure has been replaced.
- Inference and review semantic floors: accept profiles that retain the name but omit native verification or authority.
- Native policy binding: accept a different valid signed authority/model/scope policy under the same consumer-selected policy commitment.
- Contract preimage: replace absence with the default scenario contract.
- Admission result status and canonical record equality: remove each independently.
- Canonical bytes: accept whitespace-altered contract bytes.

Each run preserves original, mutant and restored results, a positive control,
exact textual replacement and mutant SHA-256. Only incorrect authorization under
valid controls is a KILLED joint boundary. The score concerns these executed sites,
not every possible parser mutation or a general security guarantee.

A separate PR5 discarded-read mutation demonstrates the observation/validation
distinction. PR5's local field accounting accepts the added field under that mutation;
the joint field policy refuses it and explicitly reports `inference.unchecked`.

During development, an additional redundant unknown-requirement guard survived because
the unknown catalog dispatcher independently refused. The redundant guard was removed;
the final control mutates the actual dispatch boundary with an isolated unknown-ID /
known-procedure witness. This development result is preserved separately and is not
included in final mutation coverage.
