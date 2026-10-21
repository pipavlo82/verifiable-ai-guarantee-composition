# Claim-aware external consumer v1

Status: experimental external policy, not normative ERC-8404 requirements.
Implementation: `src/erc8404/engine.py`; executable inputs: `fixtures/erc8404`.

## Three layers

Let K be the independently supplied, relying-party-approved scenario contract,
C the requested claim, D the submitted catalog, E exact evidence and R the RVR
receipt. K is supplied separately; its requirements are not generated from the
consumer's procedure dispatch table. This separation prevents an implementation
inventory from certifying its own coverage. The experiment author created both
artifacts: organizational independence of the contract author is not claimed.

Coverage requires every obligation declared by K to occur in D with exactly the
same procedure and dependencies, and requires dependency closure. Verification
executes those procedures against actual bytes and signatures. Composition
requires the exact contract preimage/commitment, scenario, permitted claim type,
scope, signed contract binding and unconsumed-field policy.

REFUTED dominates UNVERIFIABLE when independent contradictions coexist with
missing evidence. Missing required evidence alone is UNVERIFIABLE. Authorization
requires VERIFIED. A Core CANNOT_RECOMPUTE remains a recomputation status with no
invented Core outcome; the separate consumer decision is UNVERIFIABLE and refused.

## Accepted claim and commitments

The only implemented claim type is REVIEWED_ARTIFACT_IDENTITY with scope
artifact-byte-identity. Consumed fields are exactly scenario, claimType, scope,
subject and artifactSha256. This is an authenticated laboratory statement about
artifact identity, not a claim that an inference, judgment or external task was
correct. Unknown broader claim types are refused even if a caller writes a
contract that requests them.

contract_sha256 = SHA256(exact canonical contract bytes).
The same explicit no-number canonical byte rules are implemented independently
and checked against the frozen adapter. Contract files must already be canonical;
pretty-printed aliases are rejected. The caller's digest is compared with the
recomputed digest; a parsed hint without the preimage is insufficient. The
contract digest is also carried in the actual EIP-712 LabJudgment policyHash.
The receipt bytes remain untouched and have a separate SHA-256 identifier.

The context contract digest must come from the relying party's trusted policy
selection. Letting an adversary choose both contract and expected digest does
not establish authorization under an honest party's policy. Contract adequacy,
selection authority and key custody remain external assumptions.

## Obligation catalog

| ID | Evidence and procedure | Dependencies | Failure |
|---|---|---|---|
| S01 | Actual EIP-712 producer and judgment signatures | none | invalid R; absent U |
| S02 | Request artifact SHA-256 = RVR claim expectedDigest = both signed proofHash values | S01 | mismatch R; missing U |
| S03 | Exact request subject = both signed subjects | S01 | mismatch R; missing U |
| S04 | Recovered signer identities match contract role allowlist | S01 | unauthorized R; missing U |
| S05 | Exact signed domain matches contract domain | S01 | mismatch R; missing U |
| S06 | Signed actions match declared producer/reviewer roles | S01 | mismatch R; missing U |
| O14 | Policy-selected role pairs have authenticated, comparable and distinct identities | S01, S04, S05 | same/wrong identity R; unavailable/incomparable U |

The frozen RVR gate/procedure is required independently of this catalog.
Core receipt checks, contract bindings and supported-policy restrictions are
structural consumer preconditions, not fields invented inside an old receipt.

O14 is omitted when the scenario does not require independent checking.
The positive self_allowed fixture demonstrates this. Additional role pairs use
the exact scenario policy and authorized identity. Namespace comparisons are
limited to eip155:31337:secp256k1 in this laboratory. Distinct keys do not prove
distinct persons, organizations, economic control or absence of collusion.

## Authorization and reuse

Every positive decision includes scenario, claim_type, recomputed
contract_sha256, verified_claim_scope, receipt_sha256, unconsumed_claim_fields
and explicit limits. REJECT refuses any unconsumed field. LIST permits the
narrow consumed claim only and lists every excluded field. A false outputHash
under LIST is explicitly outside the authorized scope; it never becomes a
verified output. The REJECT counterpart refuses it.

The result JSON is not a bearer credential. `consume_authorization` recomputes
the decision on the current evidence and compares the entire scoped record.
Cross-contract, cross-type and altered-record reuse are refused. This is offline
idempotent verification, not a live single-use nonce service or settlement API.

## Reproduction

```sh
python -B tools/v3/prepare.py --online
python -B tools/erc8404/consume.py --example > request.json
python -B tools/erc8404/consume.py request.json
python -B tools/erc8404/validate.py
bun evidence/erc8404/core/conformance/rvr-v0/adapter.ts --check
python -B tools/erc8404/integrity.py
python -B tools/verify_artifacts.py
```

Preparation downloads pinned dependencies and builds the historical native
wrapper. The consumer and replay make no network calls. Generators are provenance
tools, not replay steps: they use fresh ephemeral laboratory keys, save only
public signatures and refuse to overwrite existing fixtures.
