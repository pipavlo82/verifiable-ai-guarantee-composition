# CI inventory repair for the published escrow experiment

The original published commit is `ac30419dd5a2e72fe9e359bbbb538f58fc5f40c0`.
All 16 inherited workflow entrypoints failed at the same whole-repository inventory
gate. A new exact-head checkout independently reproduced those exits: the root
manifest had 10,708 entries and the Git tree had 11,862 non-manifest files. The
1,154 mismatches were exactly the experimental additions. No original hash changed,
no original file disappeared, and no unexpected generated file was included.

## Manifest procedure and preserved guarantees

`tools/verify_artifacts.py` is unchanged. Its canonical maintainer procedure remains:

```sh
python -B -X utf8 tools/verify_artifacts.py --write
python -B -X utf8 tools/verify_artifacts.py
```

Only use `--write` after independently reviewing the actual Git tree and expected
changes. CI never uses `--write`. It still rejects changed bytes, missing files and
unlisted files. The original root manifest and experiment manifest are preserved
byte-for-byte in `evidence/escrow-v0/history/*ac30419d.json`; old captures and reports
are not regenerated. The current experiment manifest is refreshed before the root
manifest, excluding the root manifest to avoid a commitment cycle.

The experimental baseline checker previously compared the root manifest itself
byte-for-byte with PR #7. Its only allowed refresh now requires all of the following:

- The original schema and exclusion metadata are identical.
- Every original manifest entry and its digest remain present and unchanged.
- The current manifest uses the canonical existing serialization.
- The unchanged whole-repository verifier accepts the complete current file set.
- Every other PR #7 file remains byte-identical, and all vendored escrow hashes pass.

This is not a general baseline exclusion. A changed original artifact that is
rehashed into the new manifest is independently rejected by the baseline checker.
Only the root manifest, the experimental baseline checker and the current
experiment index intentionally change in this repair. PR #7's branch, all inherited
verifier code, frozen ERC-8404 Core and upstream escrow sources remain untouched.

## Dedicated escrow CI

`.github/workflows/verdict-escrow.yml` pins its actions and tool versions and runs
on Ubuntu 24.04. It builds the native verifier from pinned sources, prepares the
unchanged upstream escrow dependencies and runs:

```sh
python -B -X utf8 tools/escrow_ci.py
```

The entrypoint checks both inventories and frozen sources, then executes the full
escrow validator: normal/repeat/Python-O, seven original Foundry tests, seven new
Foundry methods, 31 scenarios, signature/native proof replay, cross-implementation
checks, 17 adapter plus five Solidity mutations, semantic determinism and PR #7
regression. It additionally requires the exact mutation-ID sets, distinguishing
negative outcomes, positive controls, restoration and zero survivors/crashes.
Missing/empty or partially executed mutation reports cannot pass this gate.

Five executable CI negative controls use disposable copies:

1. Modify the pinned `evidence/v2/capture/b/proof.bin`.
2. Remove that expected file.
3. Add an unlisted file.
4. Modify and rehash the old proof, demonstrating that the baseline refresh rule
   still rejects it even when the whole-repository index is internally consistent.
5. Add a redundant scope guard only in a disposable adapter copy, then execute the
   unchanged mutation harness. Removing the original scope guard actually survives:
   16 KILLED / 1 SURVIVED / 0 CRASHED. Both the harness and strict CI report gate
   must exit 1. Positive/negative probes and exact source restoration must succeed.

The fifth result is deliberately constructed to test CI failure propagation. It
is not a survivor in the stock experiment and is not counted among its 22 kills.
Inventory failures must produce the exact expected mismatch set; exceptions and
infrastructure failures do not certify a successful control. Raw commands, exit
codes and reports are uploaded even when CI fails.

The inherited workflows are also retained unchanged. Historical failed runs remain
failed at their original SHA. New CI status and the final repair SHA must be taken
from actual GitHub execution, not this procedure document.

## Research limits remain unchanged

PARTIALLY_COMPATIBLE; LABORATORY_VERIFIED / PARTIAL_CHAIN_VERIFIED; HOLD for production
payments. Expiration, signer revocation, global nonce scope, private relay semantics
and missing external-chain evidence are not repaired by an inventory/CI change.
No merge, network deployment, transaction broadcast or real funds are involved.
