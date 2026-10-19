# Frozen Core baseline

This is an external consumer experiment. No upstream repository, PR, release,
normative file, interface, schema, receipt, commitment or conformance vector is
modified. The independently supplied scenario contract is an application policy,
not an amendment to ERC-8404.

The complete current formal draft was read from ethereum/ERCs PR #1980,
head repository `pipavlo82/ERCs`, commit
`7a9e63a80bce04db53c6550103c1d41eca35f3d1`, path `ERCS/erc-8404.md`.
Status: Draft; created 2026-08-29; no numbered final specification version.
Exact file SHA-256:
`63f1ad56b6a8a5099a12afbacd511c1271f50b1af6ef674a12b7aeb28850ad85`.

Executable source: `pipavlo82/recomputable-verification-receipts` at
`9dd36e882dd372f264b77b179130948aa5adcbde`.
The byte inventory covers all 75 tracked upstream files. Thirteen exact files
(the current thin-slice package, specification and Apache-2.0 license) are
vendored under `evidence/erc8404/core`; `fixtures/erc8404/core-lock.json` pins each.
The original paths and byte contents are preserved. The upstream author remains
the copyright holder; the vendored license applies to these files.

Current executable profile canonical digest:
`51f79442e96339ca45e9e6cc0c8232833efbee20e7480df00987dbc97da72948`.
Current executable package digest:
`c56fa659590247b302cf670245523ed3b02902157c27b0d710bad653cb3a0eee`.

## Historical version distinction

RC2 tag `v0.0.1-rc.2` points to
`f4476754c92e0bea549474722108ec60ded1385a`, profile
`ac16ba13abe00d8b7fac14bf5c35ee3175de3dbd7d70a296be27a094a99ef29c`,
package `e2c7712e4ce5551628cf2d1b65b0ae4458d5d2f7aaed7ffd3c969505ee29d63c`.
Eight package/specification files differ between that tag and the observed main.
Those differences predate this experiment and are recorded in
`evidence/erc8404/historical-rc2-difference.json`. We neither overwrite them nor
backfill current semantics onto RC2. The present consumer selects the current
exact profile above, not the old digest.

## Interface and byte rules

The Core is an off-chain JSON contract; it defines no mandatory Solidity ABI.
The receipt has exactly `claimDigest`, `evidenceSetDigest`,
`verificationProfileDigest`, `outcome`, `reasonCode`, `resultDigest`.
The recomputation status is a separate output, never a seventh receipt field.
All four digests are SHA-256, lowercase hexadecimal without a prefix.

Claim, profile and canonical result digests hash their exact
`rvr-canonical-json-v0` bytes. Evidence-set hashing sorts the unique member IDs,
then hashes the canonical descriptor; present members separately pin raw bytes
and decimal-string length. The serializer forbids numbers, decoded duplicate
keys and lone surrogates; preserves array order/duplicates and Unicode; sorts
keys by scalar value; uses literal U+2028/U+2029 and exact escaping. It is not JCS.

Profile identity closes specification, schemas, byte contracts, result
projections, reasons, vector identities and outcome-relevant immutable context.
Required dependencies must be hash-checked before the same bytes are used.
Unavailable dependencies do not become semantic refutations. Gate rejection,
semantic outcome and recomputation status remain distinct.

The formal draft's conformance requirements include reproduced success,
semantic divergence, reproduced indeterminacy, missing and substituted required
dependencies, missing present payloads, payload mismatch, non-semantic dependency
invariance, projection contradictions, hidden state and hash-before-parse
controls. The unchanged Python/TypeScript suite is replayed. This is evidence
about this exact executable profile, not certification that every detail of a
pre-standard implementation conforms to the later formal draft. In particular,
the draft and thin-slice text order some gates differently and define the
generality of UNVERIFIABLE differently. Neither is silently rewritten.

Any proposal to add receipt fields, change an existing preimage, reinterpret a
published profile or alter a Core status is INCOMPATIBLE_WITH_FROZEN_CORE.

Run `python -B tools/erc8404/integrity.py` for the preserved Core, source and
historical research inventory. Full upstream before/after hashes are retained
in the evidence package.
