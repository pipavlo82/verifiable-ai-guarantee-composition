# Prior-art comparison, accessed 2026-10-18

Targeted primary-source review, not an exhaustive literature survey. Published
results are not reproduced merely by citing them. Preprints and abstract-only
access are labeled. No scientific novelty or upstream vulnerability is claimed.

| Primary work | Actual overlap | Difference / limit of v4 |
| --- | --- | --- |
| Chockler, Kupferman, Vardi, *Coverage Metrics for Formal Verification*, CHARME 2003, [author publication record and source](https://www.cs.rice.edu/~vardi/papers/) | Asking whether a passing specification covers the design is established formal-verification coverage research | Author record reviewed; compressed PostScript was not readable through the web parser. The accessible 2008 primary paper below also discusses this coverage distinction. No algorithm from the 2003 paper is claimed reproduced |
| Fisman, Kupferman, **Sarai** Sheinvald-Faragy, Vardi, *A Framework for Inherent Vacuity*, HVC 2008, [author PDF](https://www.cs.rice.edu/~vardi/papers/hvc08.pdf), abstract and Sections 1–3 reviewed | Specification-quality analysis and mutation can identify elements that do not affect satisfaction; the paper distinguishes specification vacuity from model coverage | v4 is a finite evidence-authorization harness, not an LTL vacuity decision procedure. Its central concern is not new in general |
| Alrajeh, Kramer, van Lamsweerde, Russo, Uchitel, *Generating obstacle conditions for requirements completeness*, ICSE 2012, [institutional primary record](https://research.dial.uclouvain.be/entities/publication/b3889570-0b30-4cfb-9f11-b1317c891277), abstract reviewed; PDF restricted | Missing requirements, goal obstacles, witness/counterexample traces and completeness relative to known domain properties | v4 manually supplies its contracts. It does not automatically elicit complete requirements or implement obstacle learning |
| *Proof-based coverage metrics for formal verification*, ASE 2017, DOI 10.1109/ASE.2017.8115632, [publisher abstract](https://ieeexplore.ieee.org/document/8115632/), indexed abstract reviewed; direct page blocked | Property adequacy, mutation coverage and inductive validity cores | v4 neither computes IVCs nor establishes proof-based coverage |
| Chilton, Jonsson, Kwiatkowska, *Compositional Assume-Guarantee Reasoning for Input/Output Component Theories*, 2014, [author PDF](https://qav.cs.ox.ac.uk/papers/CJK14.pdf), introduction and contract discussion reviewed | Explicit environment assumptions, guarantees, refinement and composition | v4's finite conjunction is substantially less expressive; conditional preservation is not a new general theorem |
| Appel, Felten, *Proof-Carrying Authentication*, CCS 1999, [author record](https://www.cs.princeton.edu/~appel/papers/says.pdf), inherited v3 indexed-abstract review; direct fetch unavailable | Authorization rooted in checkable justification and authority | v4 lacks its proof calculus. Signature validity versus permission is established prior art |
| IETF [RFC 9334 RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html), 2023 | Evidence, appraisal policy, attestation results and relying-party decisions are distinct | No hardware-rooted attestation or independent execution witness is added |
| W3C [PROV-DM](https://www.w3.org/TR/prov-dm/), 2013 Recommendation, core entity/activity/agent model reviewed | Typed provenance and responsibility relations | A matching digest does not establish an observed historical activity |
| Falcone, Havelund, Reger, *A Tutorial on Runtime Verification*, 2013, [author PDF](https://havelund.com/Publications/rv-tutorial-ios-2012.pdf), Sections 1–3 reviewed | Monitors evaluate observed executions against specified requirements; verdict domains can contain uncertainty | v4 performs offline evidence appraisal and does not instrument an agent runtime or prove trace completeness |
| Wang, Poskitt, Sun, [AgentSpec v3](https://arxiv.org/html/2503.18666v3), research manuscript | Explicit runtime policies for AI agents | Existing enforcement work; v4 does not provide an agent runtime controller |
| Zhang et al., [FAVA v1](https://arxiv.org/html/2607.27267v1), 2026 preprint, finite-graph soundness discussion reviewed | Evidence-backed permission graphs, obligations and policy-relative authorization | Particularly close overlap. FAVA explicitly does not claim completeness of natural-language extraction/implicit-flow discovery. v4 must not portray that distinction as newly discovered |
| Sun, Evans, [Composable Attestation v1](https://arxiv.org/html/2603.02451v1), 2026 preprint | Composition of attestation evidence and trust | v4 does not prove or reproduce its cryptographic constructions |

AI inference verification is grounded directly in the pinned zkIE implementation
and its actual public native statement; see ZKIE_ERC8274_MAPPING.md. An interface
label cannot supply privacy, soundness, provenance or agent authority. Earlier
research coverage and references remain unchanged in ../PRIOR_ART_ANALYSIS.md.

The defensible contribution candidate is an **artifact/experience study**: a
source-pinned, replayable example combining native inference artifacts and real
laboratory signatures with separately declared scenario contracts, catalog
omission controls and three baselines. Narrow integration usefulness may justify
review; scientific novelty remains UNPROVEN. Independent experts should assess
contract adequacy and the closest coverage/authorization literature before any
broader claim or award positioning.
