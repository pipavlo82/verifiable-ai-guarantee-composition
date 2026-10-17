# Open obligations and executable acquisition plan

Overall: **PARTIAL_CHAIN_VERIFIED; HOLD_WITH_EXACT_BLOCKERS**.

| Missing obligation | Exact evidence required | Current observation |
| --- | --- | --- |
| WYRIWE admission -> native input | Original bytes, committed sanitization code/CID, exact output bytes, complete signed type/domain, independently accepted gateway policy and admission witness | Two bounded gateway pages each yielded 200 legacy-shaped records; no compatible complete current profile or matching native input preimage was obtained |
| External model authorization | Versioned authority policy/delegation binding model, weights, circuit, input, action and validity context | Laboratory manifest pin exists; external authorization does not |
| Inference -> judgment | Signed judgment naming exact native public statement, input/model and requested action under an applicable policy | Published ledger/cells concern a different decision; no invented edge is added |
| Judgment -> external execution | Preserved receipt identifying the same action/result plus independent mediation, settlement or external effect evidence | Ledger #236 outcome GET returned 404; local replay receipt proves no historical external effect |
| Historical CRC exact input | Bytes opening `sha256:6cb8dc90bfa9709b1885310427eee6703c9273b2240b53d94316a2ba90cc586c` | Current live ledger and partial fixture are different bytes |
| Historical CRC producer execution | Resolvable execution witness with subject, code/runtime, input/output, authority and observation guarantees | Signed reference fields/opaque witness hashes are insufficient |

Absence in this bounded search is not a refutation, nor proof that an artifact
cannot exist. A local freshly generated proof is real mathematics but cannot be
presented as an observation of an external production workflow.

## Executable steps

From repository root, after the pinned setup in [REPRODUCE](v3/REPRODUCE.md):

```sh
python -B tools/v3/acquire.py --plan research/v3-acquisition-plan.json --out build/new-gateway-capture
python -B tools/v3/acquire.py --plan research/v3-gateway-followup.json --out build/new-recent-gateway-capture
python -B tools/v3/check_acquisition.py
python -B tools/v3/check_acquisition.py --bundle /path/to/external-bundle
python -B tools/v3/run.py --plan external_full_chain
```

GET capture saves original responses before parsing, timestamps, statuses and
SHA-256; destinations must be new. A non-200 response exits 2. No credentials,
signing request, on-chain transaction or outbound researcher message is sent.
The bundle check validates a `manifest.json` file-to-SHA-256 mapping and the exact
filenames printed by the command. A mismatch exits 1; missing or semantically
unintegrated evidence exits 2. Even a byte-complete bundle stays UNVERIFIABLE:
digest completeness is not evidence of authority or execution.

Once matching externally produced artifacts are available, pin their original
bytes in a new additive version. Implement the exact schema-specific WYRIWE
verifier (do not fill missing legacy fields), verify its authorized signer/domain,
run its declared transform, compare the native input and public statement,
resolve the judgment policy, and verify the execution witness's own trust model.
Only then add a complete positive chain, an isolated negative and a missing
witness for each new edge, physical mutations, and fresh replay. Authority and
execution adapters for arbitrary new bundles are **NOT IMPLEMENTED** in v3.

Open formal obligations: parser/canonicalization equivalence outside the supported
integer/ASCII-key subset; completeness of the graph for real application policy;
verifier soundness; trusted policy distribution/revocation; temporal freshness;
execution trace completeness and non-bypass; proof of model authorization;
judgment factual validity. None is discharged by the current finite test suite.
