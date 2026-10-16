# Source and artifact audit

Inspected public heads and release metadata on 2026-10-16. These are source
versions, not evidence that a live service runs the same deployment commit.

| Source | Exact commit |
| --- | --- |
| trustless-ai/zkIE | `39d8df96877bc3bebf33c69b06907d792b3184b9` |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` |
| trustless-ai/recompute-kit | `f7308cdd5ba55ac8229103e82ebc5fc14f81b88b` |
| ethereum/ERCs PR #1810, head TMerlini/ERCs | `c0e13d17940a6eabe4d842e623fd0f871550ef7b` |
| pipavlo82/receiptos-verify | `396143120f787d2f5534e92c0cf896c029a05775` |
| linked implementation trustless-ai/ccip-router | `e667a4f78b8a0aa0239e32d1e0b827495e72ae0a` |

Repository links and metadata are in `evidence/v3/discovery/sources.json` and
`evidence/v3/public/ccip-router-source.json`. Exact relevant file hashes are in
`evidence/v3/upstream/selected-source-lock.json`. All source checkouts must match
their pins and have clean tracked files; executed and preserved files are checked
as bytes. Review-only agent-ercs/router files are checked as original Git blobs.

## Normative versus implemented versus experimental

The open ERC proposal defines an eight-field WYRIWE attestation including timestamp,
an ERC8004AttestationGateway version-1 EIP-712 domain and pipeline hash semantics.
The agent-ercs contracts supply Solidity interfaces. Neither the prose nor an
interface demonstrates that a particular gateway admitted particular bytes.
The inspected router implementation adds `commitmentHash` and a domain
`verifyingContract`; it has an `IDENTITY_SENTINEL` and different non-sentinel
input-hash construction. These profiles must be distinguished explicitly.

Two public gateway identity endpoints and bounded record queries were captured.
The later query returned 200 records from each service. Decoded attestation bodies
in those 400 records lack the current timestamp/commitmentHash/chainId shape;
the envelope timestamp does not retroactively fill a signed field. A legacy
agent identifier also differs from the current bytes32 profile. We did not recover
a compatible admitted-input preimage linked to the retained native proof. These
observations do not prove malformed signatures, an upstream vulnerability, or
global absence of suitable records. Current-profile verification is UNVERIFIABLE.

zkIE's pinned implementation permits a real native public matrix proof and
forward-output recomputation. The retained proof, binary serialization, adapter,
model manifest and Cargo lock come unchanged from v2. They establish the native
contract actually checked, not an external LLM task, private weights, authorized
model or WYRIWE provenance. No published matching complete chain was found in
the bounded source tree/release/fixture inspection.

recompute-kit supplies the two signed CRC Cell fixtures and reference code.
The Nostr cell authenticates a payload after NIP-01 event-ID reconstruction and
BIP-340 verification. The EIP-712 Cell signs schema, claim ID, result, verifier,
boundary, as_of, recomputed_at and evidence_hash. Its domain is
`cross-reference-console`, version `1`, chainId `1`. This is a CRC Cell format,
**not** a WYRIWE input-provenance attestation. The evidence hash uses real
Keccak-256. The implemented canonicalizer deliberately supports only the
integer/ASCII-key subset in these artifacts, not unrestricted RFC 8785.

The live ledger #236 Nostr event has ID
`ce953822d970b5786dd3474f43e159f80cdd08a81e254354449fb01c90a0c5a3`.
Its signed decision reference is
`sha256:5bca0bf044c8e1c8e16a01bf3ee44b12c305ce6a50dd9789ff73cbd13482b9b9`.
Both cells refer to that decision and claim ID
`sha256:df1a6bfe3063186f8a8327b75a5bfddae12d3518f2cc16f8fddbc6c311de9512`.
The exact decision preimage is reconstructed from the eight fields declared by
the signed event, including nulls for absent fields. The literal claim is reject.
Cell GREEN is agreement with a scoped claim, not authorization of the rejected
action. The `agent_reported` limitation remains part of the interpretation.

The signed historical input hash `6cb8...586c` does not match the new full ledger
capture or the partial fixture. We make no claim that new bytes were historically
admitted or that signing software actually executed its declared checks. Node1
has null execution metadata; node2 supplies an unresolved witness hash. Bitcoin/
OpenTimestamps fields are reported metadata; no independent OTS/chain verification
was executed. The outcome endpoint returned 404 in our preserved observation.

ReceiptOS's pinned native Crystal bridge verifies our local receipt's canonical
root. That invocation and an independent Python recomputation agree. The object
is a research observer record with actual command times, exits and stream hashes;
it is unsigned and does not assert full upstream issuance-schema conformity.
Execution evidence is local to replay, with the honest-recorder assumption.

## Preservation and licenses

The full artifact catalog lists exact bytes, provenance, producer, verification
authority, subject/scope and execution grade. Public HTTP captures retain original
bytes; technical notes use LF. Frozen v0/v1/v2 evidence is unchanged. Only selected
CC0 recompute-kit files/fixtures are copied, with their original LICENSE. Other
upstream sources are fetched at fixed commits and are not republished here.
This repository's existing permissive license covers its own additions; it does
not relicense third-party observations or source code.
