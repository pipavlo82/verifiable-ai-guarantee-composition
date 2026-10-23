# Source-pinned finite coverage

The executable [obligation catalog](../../conformance/agent-harness-v0/erc8404/obligations.json) contains 16 independently described obligations: three normative RVR-profile clauses and thirteen external research-policy requirements. The [vectors](../../conformance/agent-harness-v0/erc8404/vectors.json) contain 18 scenarios. Neither count establishes specification completeness.

| Witness | Requirement source | Expected admission |
| --- | --- | --- |
| permitted_review | RVR v0 section 8 + external reviewed-artifact contract | VERIFIED, exact artifact-review scope |
| separation_not_required | External conditional O14 policy | VERIFIED; self-signing permitted by this contract |
| unsupported_claim | External supported claim type | REFUTED |
| wrong_authority | External authorized recovered keys | REFUTED |
| wrong_subject | External exact signed/requested subject | REFUTED |
| wrong_signed_scope | External signed action/scope | REFUTED |
| missing_payload | RVR v0 sections 5 and 9 | UNVERIFIABLE; CANNOT_RECOMPUTE, no Core verification outcome |
| missing_judgment | External authentic review requirement | UNVERIFIABLE |
| mismatched_contract | External independently recomputed contract digest | REFUTED |
| wrong_signed_policy | External signature-to-policy binding | REFUTED |
| cross_component_loss | External receipt/claim/signature artifact alignment | REFUTED |
| downstream_promotion | External REJECT policy for unconsumed fields | REFUTED |
| missing_independence_coverage | External independently supplied O14 requirement | REFUTED |
| self_judgment | External required role separation | REFUTED |
| invalid_signature | External actual EIP-712 verification | REFUTED |
| missing_contract_preimage | External canonical contract evidence | UNVERIFIABLE |
| tampered_admission | External fresh admission, not a bearer scope record | REFUTED despite underlying valid decision |
| contradictory_receipt | RVR v0 section 7 | REFUTED admission; Core projection gate rejection, no semantic outcome |

The normative source is the frozen [RVR v0 specification](../../evidence/erc8404/core/docs/spec/RECOMPUTABLE_VERIFICATION_RECEIPTS_V0.md); the external policy source is the preserved [claim-aware profile](../erc8404/CLAIM_AWARE_PROFILE.md). The latter's authority, O14 and downstream restrictions are not ERC-8404 Core requirements.

Coverage extends only to the selected claim `REVIEWED_ARTIFACT_IDENTITY`, `artifact-byte-identity` scope, fixed laboratory EIP-712 schema and the selected policy families. The copied native proof is treated as exact bytes. This adapter does not execute the native zkIE verifier. Historical integration tests remain separately reproducible and are not counted as this pilot's proof verification.

ERC8274 execution verification, complete WYRIWE provenance, arbitrary Semantic ABI/RSI profiles, live transactions, native model authorization, independent controller ownership, and a second independently authored backend are **NOT_COVERED** here. Missing implementations are not simulated as external observations. The repository's prior real-chain status remains PARTIAL_CHAIN_VERIFIED.
