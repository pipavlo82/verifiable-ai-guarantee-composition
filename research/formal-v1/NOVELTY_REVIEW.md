# Bounded prior-art review and candidate contribution

**Conclusion: scientific novelty is not yet established.** The current contribution is a reproducible research instrument, a source-specific obligations map, and small executed examples. The literature sample below is targeted, not an exhaustive priority or patent search. Exact captured bytes, retrieval times and hashes are in [captures.json](evidence/captures.json); full papers remain local reference material rather than copied source in this repository.

| Primary source | Relevant established idea | Consequence for our claim |
| --- | --- | --- |
| [Chilton, Jonsson and Kwiatkowska, 2014](https://qav.cs.ox.ac.uk/papers/CJK14.pdf), assume-guarantee reasoning for compositional component theories | Formal reasoning about local contracts and their composition | We cannot claim the first theory of composing guarantees |
| [A Proof-Carrying Authorization System, Princeton TR-638-01](https://www.cs.princeton.edu/techreports/2001/638.pdf) | Authorization justified by proofs against policy | Proof validity and permission are already distinct obligations |
| [RFC 9334, RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html), especially appraisal and relying-party roles | Attestation evidence is appraised; a relying party makes decisions under its own policy | Authentic attestation alone is not a new theory of authorization |
| [AEX, arXiv:2603.14283v1](https://arxiv.org/html/2603.14283v1) | Signed AI exchange bindings and explicit transformation/binding modes | Portable request/output evidence and representation boundaries have close prior art |
| [Composable Attestation, arXiv:2603.02451v1](https://arxiv.org/html/2603.02451v1) | Attestation composition for AI/distributed workflows | A broad claim of first composable AI attestation would be unjustified |
| [Agent Action Capsule Provenance Binding, draft-00](https://www.ietf.org/archive/id/draft-rampalli-scitt-capsule-provenance-binding-00.txt) | Per-action authorization bound to provenance; separates permission, execution and justification | Combining these categories is not by itself a new contribution; this source is a draft, not an adopted RFC |
| [Pinned ERC-8299 draft](https://github.com/ethereum/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md) and [judgment interface](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IJudgmentExecutionAttestation.sol) | Judgment authenticity does not imply soundness or permission; proposal and execution binding are explicit concerns | These distinctions must be credited to upstream rather than presented as an omission we discovered |

## What could become a defensible contribution

For an exact, versioned combination of native verifiers and downstream policy, derive the additional cross-artifact obligations that remain after the native checks. Make representations and transformations explicit. Give conditional sufficiency arguments and a counterexample for each necessary obligation. Then exercise those obligations against a genuine coherent chain, using identical inputs for component-only and composition-aware consumers.

The proposed distinction is the **measured residual obligations for specific profiles**, not a new cryptographic primitive or generic statement that composition can fail. This stage does not establish that prior work lacks such a method. That requires a deeper comparison and independent review.

The graph model provides an inspectable method but its connectivity/minimality facts are elementary. The signed-event substitution control is a familiar authentication-versus-context example. The public event and local zkIE tests are unrelated and cannot jointly support a real end-to-end result.

## Acceptance gates

1. Define one real target claim and its exact authority/policy/representation profile.
2. Obtain one coherent tuple with proof, preimages, attestation, verdict, execution evidence and receipt.
3. Identify which relations native verification already establishes, with executable evidence.
4. Derive remaining obligations and test necessity without changing the native valid components.
5. Compare against a well-specified baseline on the same tuple; report unknowns and costs without generalizing from one case.
6. Seek independent reproduction and specialist review before broader novelty or security claims.

Recommendation: CONTINUE this narrow experiment; HOLD priority claims and upstream vulnerability claims.
