# Claim-Aware Verification → Signed Verdict → Base Escrow

**Compatibility: PARTIALLY_COMPATIBLE. Demonstrated guarantee: LABORATORY_VERIFIED;
external chain: PARTIAL_CHAIN_VERIFIED. Recommendation: HOLD for production payment
integration; completed local experiment is ready for independent review.**

Branch: `experiment/claim-aware-verdict-escrow-v0`, based on unchanged PR7
`c93087f06bd14c45a1d12b0c068195e3bef05dae`. The exact local experiment commit and its
subsequent fresh-checkout results are supplied in the external closure report.
No push, PR, merge, network deployment, transaction broadcast or real funds were used.

## Sources and evidence discipline

| Source | Exact commit |
|---|---|
| PR7 baseline | c93087f06bd14c45a1d12b0c068195e3bef05dae |
| Observed VAGC main | 18a5916098addf6447700ed95441125bfa7079c3 |
| [invinoveritas source](https://github.com/babyblueviper1/invinoveritas/tree/ce8c504f2ae4d9b389b53823fe16afec7fcf3bb3/integrations/verdict-escrow) | ce8c504f2ae4d9b389b53823fe16afec7fcf3bb3 |
| [zkIE native source](https://github.com/trustless-ai/zkIE/tree/39d8df96877bc3bebf33c69b06907d792b3184b9) | 39d8df96877bc3bebf33c69b06907d792b3184b9 |
| [ERC-8404 Draft / PR1980](https://github.com/pipavlo82/ERCs/blob/7a9e63a80bce04db53c6550103c1d41eca35f3d1/ERCS/erc-8404.md) | 7a9e63a80bce04db53c6550103c1d41eca35f3d1 |
| forge-std | b013eff2ac4fce26f34d789e6f5c49021c5ee817 |

The entire current ERC draft was read and archived; SHA-256
`63f1ad56b6a8a5099a12afbacd511c1271f50b1af6ef674a12b7aeb28850ad85`.
ERC-8404 Core and existing receipts/conformance vectors remain unchanged. New payment
rules are external research policy, not normative ERC requirements. All 10,709
PR7 baseline files and 10 vendored escrow files are byte-identical.

## Demonstrated chain and its scope

Preserved native proof `87da845a2fe2c4768d0ec47926d6c5b6a88cf10149f0ac291033b034dc364530` is verified through the
unchanged native adapter. PR7 independently recomputes the authorization and refuses
tampered consumer records, missing obligations, unconsumed fields and prohibited
self-judgment. The payment adapter additionally recomputes scenario/evidence/profile
commitments and compares a separate payer grant with escrow state. It signs the
actual v2 ABI digest using a deterministic public laboratory BIP-340 key. The original
Solidity contract verifies the signature and performs an observed mock-token transfer.

The exact authorized claim is `LAB_REPLAY_AND_REVIEWED_PROOF_IDENTITY` under scenario
`preserved-proof-a-replay-and-review`, scope `local-output-replay-and-proof-byte-review`.
Scenario contract SHA-256: `60a98d797564268383a7bb6268b4e58659b77f978b20c2c1b80617b3573a2834`.
External profile SHA-256: `9916f0ee2862691b528fe4566e7c86f30003d64e7f6cc27aef99bb532d94ca5d`.
This authorizes the laboratory replay/review service only under the separately trusted
payer grant. It is not evidence of external task completion or permission to spend
arbitrary funds. The production signer differs from the lab signer.

## Independently observed Base deployment

Two read-only RPC providers returned chain 8453, address
`0xfC4Da1b7C56D46AB23c750c0890025F6335bCA3F`, block `0x326c500`,
block hash `0x59ac1688e0a2cf6390ae78550050134ba4334ff2ebaaa91e2b2b16e26303b5ea`.
The 4,370-byte runtime exactly matches the original pinned Solidity compiled with
solc 0.8.26, optimizer 200, viaIR false after substituting recorded immutable getters.
Full runtime SHA-256: `7e9f66bf43f8b6bc9f80e89c94788244770a81958c48fd5bed107660dbcc697c`.
Token and public verifier key are preserved in the raw RPC snapshots. No payment
transaction was sent or inferred from this code observation.

## Results and concrete boundaries

31 scenarios, 9 Python methods, 7 integration Foundry methods, original 7 escrow tests,
16 unchanged PR7 methods, 33 secondary digest/signature checks and deterministic
normal/repeat/-O output are recorded. New mutations: 17 adapter + 5 Solidity = 22
killed, zero surviving/crashed applied mutations. Six absent on-chain guards are
NOT_APPLIED. PR7's historical 22 mutation results remain separate.

On 28 authorization-negative scenarios, signed-only A permits 24 unsupported claims;
B and C each permit 2 lifecycle reuses after expiry/revocation. This comparison is
limited to the declared domain and trusted off-chain gateway assumption. A legitimate
signature is not a guarantee of verdict correctness. C does not add the missing
semantic guards to the unchanged escrow.

Confirmed boundaries: request text versus funded recipient/amount; post-signing
expiry/revocation; same nonce across separate payments; opaque scope/profile/evidence
commitments; honest signing-service assumption; token truthfulness. Chain/address/id
binding, immutable signer selection, signature rejection and same-escrow duplicate
prevention work in the tested domain.

## Deliverable map

- [Architecture and trust boundaries](ARCHITECTURE.md)
- [Exact compatibility matrix](COMPATIBILITY_MATRIX.md)
- [Nine guarantee layers](GUARANTEES.md)
- [Complete vectors, comparison and gas](EXPERIMENT_RESULTS.md)
- [Mutation evidence](MUTATION_REPORT.md)
- [Reproduction commands](REPRODUCTION.md)
- [Remaining guarantees and acquisition requirements](LIMITATIONS.md)
- [Independent review checklist](INDEPENDENT_REVIEW_CHECKLIST.md)
- Machine-readable reports and raw logs: `evidence/escrow-v0/validation/`
- Byte integrity: `evidence/escrow-v0/SHA256.json`

The experiment is complete within its authorized local scope. FULL_CHAIN_VERIFIED
is not claimed. No private relay service, real payer authorization, authenticated
public execution state or actual Base transfer closes the remaining external links.
