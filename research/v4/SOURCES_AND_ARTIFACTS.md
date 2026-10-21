# Sources, artifacts and trust boundaries

All pins were resolved from live public repositories on 2026-10-18. Exact source
responses and preparation commands are preserved in evidence/v4/phase1-commands;
fixtures/v4/source-lock.json is the machine-readable lock. Full SHA-256 inventory
is artifacts.sha256.json. A source pin identifies bytes, not trustworthiness.

| Source | Exact SHA | Role |
| --- | --- | --- |
| trustless-ai/zkIE | 39d8df96877bc3bebf33c69b06907d792b3184b9 | Actual native public arithmetic verifier |
| trustless-ai/recompute-kit | f7308cdd5ba55ac8229103e82ebc5fc14f81b88b | Existing external signature/CRC replay and conventions; no new external chain inferred |
| trustless-ai/agent-ercs | 01283ca57305f915afb560d23359a27fd748eb5a | Pinned Solidity interface implementation text |
| ethereum/ERCs PR1810, TMerlini/ERCs | c0e13d17940a6eabe4d842e623fd0f871550ef7b | WYRIWE draft Section 5, identity Appendix C and L4 |
| ethereum/ERCs PR1771, JimmyShi22/ERCs | 3f014d07a0ceac39fe6fb6dec0efdc30640a9653 | Current ERC-8274 draft interfaces and digest rules |
| pipavlo82/receiptos-verify | 396143120f787d2f5534e92c0cf896c029a05775 | Existing native receipt replay and bounded claim projection |

WYRIWE exact source SHA-256:
`5ea02730bdc94bd45983b3e5d22bafabf7e3aa6ca4dc1095d483b6776b7eccd3`.
ERC-8274 exact source SHA-256:
`186b84f7d6d8b063814860b0624400e1055ad548c40c16c81ff3a54f327f17cf`.
Preserved ERC source text retains its original CC0 notice. No additional upstream
implementation source is copied into the v4 verifier. Existing dependencies and
notices retain their licenses.

## Evidence inventory and interpretation

| Artifact | Producer and verifier authority | Subject, scope and procedure | Original bytes |
| --- | --- | --- | --- |
| Native proof A | Previous local experiment using pinned zkIE and original narrow Rust wrapper; verified by rebuilt same pinned native code | Public (4,8,8) MatMul, exact input/weights/output, actual native proof verification and explicit statement binding | evidence/v2/capture/a/proof.bin; SHA-256 87da845a2fe2c4768d0ec47926d6c5b6a88cf10149f0ac291033b034dc364530 |
| Model manifest | Laboratory model definition, allowed by explicit laboratory policy | Fixed public operator, field, encoding and weight digest; no trained model or external authorization | evidence/v2/capture/a/model.json; SHA-256 a8645f4c909745d4e90df6bac9c929960e665ef48f1379d7f689c42245604b8c |
| V4 provenance/judgment/receipt signatures | Ephemeral local role keys; laboratory policy is the authority, not an external registry | Actual EIP-712 signatures over baseline and controlled negative assertions, recovered with Node/noble and Python/eth-account | evidence/v4/lab/bundle.json and policy.json, full inventory pins |
| Raw/input/weights/output/result/observation bytes | Frozen previous local experiment | Exact digest and identity transform replay; current arithmetic recomputation; preserved observation integrity | evidence/v2/capture/a, unchanged |
| Identity transform | Normative fallback text from pinned draft Appendix C | Exact bytes pinned; no claim of fresh IPFS transport verification | evidence/v4/sources/identity.json; SHA-256 in source-lock.json |
| External Nostr/EIP-712 objects | Existing independently published producers from v3 | Newly repeated v3 signature and narrow binding verification, not the producer of the v4 local MatMul | evidence/v3/public and evidence/v4/prior-reproduction/v3 |
| Local execution of verification | This verifier process, current machine and later CI | Actual subprocess commands, outputs and exit codes, not historical external task execution | evidence/v4/validation/raw-execution.stdout.log and setup/replay logs |

The signed negative judgments are deliberately controlled laboratory assertions.
The underlying signatures are real; their content is not labeled an external
observation. No new real-chain proof, transaction or external execution receipt is
invented. Private signing keys are never written to repository or logs.

## What source inspection establishes

Normative requirements come from the pinned draft prose. Implementation behavior
comes from actual native calls and reviewed source (zkie-ops compose.rs,
research/chain-v2/native/src/main.rs, agent-ercs ERC8274 interfaces, recompute-kit
CONVENTIONS.md and existing signature verifier, ReceiptOS README and bounded replay
implementation already exercised by v3). A repository README's deployment status
is upstream-reported, not independently confirmed production behavior.

Research assumptions include laboratory authority, trusted scenario adequacy,
identity-transform-only support and verifier correctness. General cryptographic
soundness, complete natural-language requirement elicitation and scientific
novelty are unverified hypotheses. See the separate v4 prior-art comparison.
