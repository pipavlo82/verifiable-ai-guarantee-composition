# V2 bounded prior-art comparison

Scientific novelty is **NOT ESTABLISHED**. This is independent research, not an
official Trustless AI specification. We credit upstream for explicitly separating
authenticity, correctness, authorization and execution binding. Tests here do not
demonstrate an upstream vulnerability.

| Primary work | Established overlap | Difference evaluated in v2 / remaining uncertainty |
| --- | --- | --- |
| [Chilton, Jonsson, Kwiatkowska (2014)](https://qav.cs.ox.ac.uk/papers/CJK14.pdf) | Compositional assume-guarantee contracts and sound reasoning rules | Our small typed binding model is an application, not a new composition theory |
| [Proof-Carrying Authorization System, TR-638-01](https://www.cs.princeton.edu/techreports/2001/638.pdf) | Authorization follows policy-supported evidence | We instantiate narrow cross-artifact witnesses; firstness is not claimed |
| [RFC 9334 RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html) | Evidence appraisal and relying-party policy are distinct | Our G5/G6/G8 split follows this established distinction; our lab authority is not a trusted external attester |
| [AEX, 2603.14283v1](https://arxiv.org/html/2603.14283v1) | Explicit request-output and transformation receipt bindings for LLM APIs | Our matrix-native profile and mutation witnesses differ operationally; no claim AEX lacks equivalent checks |
| [Composable Attestation, 2603.02451v1](https://arxiv.org/html/2603.02451v1) | Generalized attestation composition, inclusion and incremental verification | Our profile measures refusal of mismatched authorization context; attestation composition itself is not new |
| [EIP-712](https://eips.ethereum.org/EIPS/eip-712) | Typed-data encoding and domain separation; replay state remains external | V2 uses real signatures and a published known answer; its chain domain is explicitly offline |
| [Pinned WYRIWE draft](https://github.com/ethereum/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md) | Provenance fields, exact transform commitment and judgment/authorization distinctions | We implement only the declared lab subset and do not claim full on-chain/deployment conformance |

The contribution candidate is a reproducible, source-pinned map of the additional
bindings required after actual native and signature acceptance, including tri-state
counterexamples and source mutation survival. This bounded reading does not
establish that no prior system provides that method. An exhaustive literature
review, stronger real artifacts and independent academic review remain necessary.
Primary-source capture hashes from the earlier review are preserved in
[v1 captures](formal-v1/evidence/captures.json). EIP-712's public Ether Mail vector
is verified by the v2 implementation; no upstream source is copied unnecessarily.

---

## Earlier v0 references

# Related work and provenance

This is independent experimental research, not official Trustless AI specification work. Ownership of the personal repository does not imply sole authorship of the referenced ecosystem. The new Python implementation uses only the standard library and does not vendor upstream source code.

1. [zkIE at 39d8df9](https://github.com/trustless-ai/zkIE/tree/39d8df96877bc3bebf33c69b06907d792b3184b9): inference proof primitives and shard composition. Relevant to inference-statement validity and internal tensor bindings; not treated here as an external authorization policy.
2. [recompute-kit at f7308cd](https://github.com/trustless-ai/recompute-kit/tree/f7308cdd5ba55ac8229103e82ebc5fc14f81b88b): primary-artifact recomputation and explicit unavailable outcomes. Informs the method, not a native dependency of this experiment.
3. [ERC-8299 draft at PR #1810 head c0e13d1](https://github.com/ethereum/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md): WYRIWE input provenance and judgment-execution composition; the source already distinguishes authentic judgment from authorization and soundness.
4. [agent-ercs at 01283ca](https://github.com/trustless-ai/agent-ercs/tree/01283ca57305f915afb560d23359a27fd748eb5a): interfaces separating proof verification, agent authorization and declaration; WYRIWE/judgment typed structures. Interfaces are not a deployed-system audit.
5. [ReceiptOS Verify at 3961431](https://github.com/pipavlo82/receiptos-verify/tree/396143120f787d2f5534e92c0cf896c029a05775): caller-selected claims, signed evidence surfaces, replay and explicit subject/scope/authority/dependency bindings. Its existing behavior is not the weak independent-only baseline.

The contribution attempted here is a small, reproducible, tri-state composition experiment with explicit source-removal controls and a same-input comparator. Novelty beyond this bounded experimental packaging is not established. A wider academic literature review, formal proof and independent implementation are future work; no unreviewed citation list is presented as evidence of novelty.

Selected source blobs and exact references are in `sources.lock.json`; [SOURCE_REVIEW.md](SOURCE_REVIEW.md) distinguishes draft requirements, observed code, upstream assertions and proposed hypotheses. Original code is MIT licensed. No upstream dependency has been copied or relicensed.
