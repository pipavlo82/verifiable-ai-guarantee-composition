# Verifiable AI Guarantee Composition

Independent experimental research by **pipavlo82** on whether individually valid components can support an unauthorized downstream claim when their subjects, inputs, scopes or dependencies differ.

**This v0 is a reconstruction using synthetic evidence. It does not verify zkIE proofs, WYRIWE signatures, on-chain transactions, or real execution receipts. Real-artifact integration: NOT IMPLEMENTED. No upstream vulnerability or security certification is claimed. This is not an official Trustless AI specification.**

The requested `guarantee-composition-v0.zip` was not located in available local searches. Its bytes, original nine cases, mutation controls and SHA-256 were not verified. See [recovery record](evidence/recovery.json). The nine core negative cases here are newly constructed; eleven supplementary controls make the limits explicit.

## Reproduce offline

Python 3.12+ standard library; no pip packages or network needed for the experiment.

```sh
git clone https://github.com/pipavlo82/verifiable-ai-guarantee-composition.git
cd verifiable-ai-guarantee-composition
python -B tools/verify_artifacts.py
python -B tools/validate.py --out build/replay
```

`validate.py` runs the complete normal/repeat/`-O` test matrix, deterministic normal/repeat/optimized experiment reports, eight real source mutations and restoration, fixture regeneration comparison, and a separate local timing sample. It saves raw stdout/stderr, return codes and a machine-readable report. It exits nonzero for failed checks or surviving/crashed/unapplied/unverifiable mutations. It compares deterministic results to committed evidence when present. Timing and unittest elapsed times are not deterministic artifacts.

Individual commands:

```sh
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
python -B tools/experiment.py
python -B tools/mutations.py
python -B tools/benchmark.py
```

## What the experiment checks

The toy inference is `y = x*x`. A publicly recomputable SHA-256 checksum detects byte changes; it is **not a signature**. A pinned public catalog stands in for judgment authenticity. Policy is separately selected by the verifier, not supplied by the evidence producer. All accepted conclusions are limited to `SYNTHETIC` under `composition-policy-v0`.

G1 input provenance; G2 model/version; G3 inference statement; G4 subject; G5 judgment authenticity; G6 judgment authorization; G7 execution receipt; G8 downstream authorization. `VERIFIED` means satisfied in this synthetic model. `REFUTED` means a checked relation contradicts the selected claim. `UNVERIFIABLE` means missing, unsupported or unusable evidence. No non-VERIFIED result authorizes anything.

Strategy A checks components independently, including toy arithmetic and the fixture authenticity catalog. Strategy B adds explicit bindings and policy context over the **same input objects**. A is an intentionally weak experimental comparator, not a reconstruction of zkIE, WYRIWE or ReceiptOS behavior. B's finite-fixture results cannot establish production security.

## Research and evidence

- [Research question](research/RESEARCH_QUESTION.md), [threat model](research/THREAT_MODEL.md)
- [Guarantee model](research/GUARANTEE_MODEL.md), [composition rules](research/COMPOSITION_RULES.md)
- [Source review](research/SOURCE_REVIEW.md), [source lock](sources.lock.json), [related work](research/RELATED_WORK.md)
- [Results](research/RESULTS.md), [machine results](evidence/validation/experiment-normal.stdout.json), [mutations](evidence/validation/mutations-normal.stdout.json)
- [Validation matrix and raw logs](evidence/validation/report.json), [artifact SHA-256 inventory](artifacts.sha256.json)
- [Limitations](research/LIMITATIONS.md), [real-artifact roadmap](research/REAL_ARTIFACT_INTEGRATION.md), [paper outline](research/PAPER_OUTLINE.md)

MIT licensed original research implementation. Upstream sources are pinned references, not vendored dependencies. Existing upstream repositories and deployed systems are unchanged.
