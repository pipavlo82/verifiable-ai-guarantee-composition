# Prior-art analysis, accessed 2026-10-16

This is a targeted primary-source comparison, not an exhaustive systematic
literature review or a claim of priority. Preprints are identified as such. The
following summaries concern published proposals; their empirical/security claims
were not independently reproduced here.

| Work and primary source | Established or proposed overlap | Consequence for this experiment |
| --- | --- | --- |
| Chilton, Jonsson, Kwiatkowska, *Compositional Assume-Guarantee Reasoning for Input/Output Component Theories*, 2014, [author PDF](https://qav.cs.ox.ac.uk/papers/CJK14.pdf), DOI 10.1016/j.scico.2013.12.010 | Formal component contracts and assume-guarantee composition | Dependency reasoning and conditional guarantee preservation are established topics; our finite AND graph offers much less theory |
| Appel and Felten, *Proof-Carrying Authentication*, CCS 1999, [author paper](https://www.cs.princeton.edu/~appel/papers/says.pdf), DOI 10.1145/319709.319718 | Requests carry checkable logical justification rooted in authentication/authority | Separating signature validity from permission is not novel; this work supplies no comparable higher-order proof calculus. Review scope here: author-hosted indexed abstract and publication record; direct PDF fetch was blocked |
| IETF, [RFC 9334: RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html), 2023 | Distinct attester, evidence, verifier appraisal policy and relying-party decision | Evidence validity and authorization policy are distinct established roles; no hardware-rooted attestation is implemented here |
| W3C, [PROV-DM](https://www.w3.org/TR/prov-dm/), Recommendation 2013 | Entities, activities, agents, derivation and responsibility | Typed provenance relationships are established; a digest relationship does not independently establish an observed activity |
| Sun and Evans, [*Composable Attestation*, arXiv:2603.02451v1](https://arxiv.org/html/2603.02451v1), preprint 2026 | Proposed composition properties and constructions for attestations | Attestation composability is already explicit research; our mutation witnesses do not prove those cryptographic constructions |
| Guan, [AEX, arXiv:2603.14283v1](https://arxiv.org/html/2603.14283v1), preprint 2026 | Request/output binding and signed transformation receipt chains | Cross-stage evidence binding is overlapping prior art; issuer assertions must retain their stated scope |
| Wang, Poskitt and Sun, [*AgentSpec*, arXiv:2503.18666v3](https://arxiv.org/html/2503.18666v3) | Runtime constraints and enforcement for LLM agents | Workflow policy enforcement is established research; v3 is offline evidence appraisal, not an agent runtime guard |
| Zhang et al., [*FAVA*, arXiv:2607.27267v1](https://arxiv.org/html/2607.27267v1), preprint 2026 | Evidence-backed permission graphs, dependencies, context and deterministic authorization checks | Particularly close overlap: a typed authorization graph is not a defensible novelty claim for this repository |
| Rhodes and Kang, [*Proof of Execution*, arXiv:2607.05397v1](https://arxiv.org/abs/2607.05397v1), preprint 2026 | Contracts, execution history and replay with explicit deployment assumptions | Execution guarantees require assumptions about mediation and trace completeness; receipt hashing alone cannot supply them. Abstract reviewed; reported performance/theorems not adopted |

Potentially useful contribution, narrowly stated: an independently replayable
case study combining preserved external Nostr/EIP-712 objects, a retained native
zkIE laboratory proof and actual local verification records, with explicit
unsupported edges, tri-state admission and source-mutated isolated witnesses.
Whether this combination is scientifically novel remains **UNPROVEN**. An
artifact/experience report is presently more defensible than a new general
composition theorem or a claim of upstream vulnerability.

Upstream normative requirements, implementation behavior and our experimental
policy are separated in [the source audit](v3/SOURCE_AND_ARTIFACT_AUDIT.md).
This independent research is not an official Trustless AI specification or review.
