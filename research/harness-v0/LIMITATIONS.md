# Limitations and independent review checklist

- This is one actual off-chain RVR implementation plus an existing external research consumer. Independent authorship of a second implementation is NOT_COVERED. Reusability is demonstrated by the configurable transport/profile and executable negative controls, not by pretending a second backend exists.
- The 18-case profile is finite. Passing it does not establish universal ERC conformance, complete requirements, soundness against all inputs, or production execution authorization.
- Genuine signatures are deterministic laboratory artifacts already preserved in the repository. They establish authenticity under the declared keys, not judgment truth. Different keys do not prove different controllers.
- A SHA-256 match establishes the identity of proof bytes. This adapter does not independently establish native proof validity, original input admission, model authorization, complete WYRIWE provenance or external execution.
- The normative RVR verifier and the external policy consumer have different jobs. Failure of an external policy requirement is not an ERC-8404 defect. No upstream vulnerability claim follows from these vectors.
- The harness trusts local executable code, its runtime, filesystem, supplied adapter configuration and adequacy of the independently selected scenario contract. It is not a sandbox, a remote-attestation protocol, or a defense against an adapter author hardcoding public expectations.
- The dependency uses pinned **private** recompute-kit functions; compatibility beyond that exact revision is unverified. No change to its upstream API is requested or assumed.
- Twelve physical consumer mutations target explicit policy boundaries. They do not cover every normative Core rule, every transport branch or every possible mutant. The unchanged Core's own semantic mutant/witness audit is separate and is not added to this physical mutation count.
- No benchmark or general performance/security improvement is claimed. Command timings are reproduction diagnostics, not comparative performance results.

## Independent review

- [ ] Confirm the baseline/main and four ecosystem commit pins from source objects.
- [ ] Confirm all previous inventoried bytes, including frozen Core and historical evidence, remain unchanged.
- [ ] Review normative-versus-policy labels against the pinned specification and scenario contracts.
- [ ] Verify expected outcomes were authored independently; `build_vectors.py` does not import/call the verifier.
- [ ] Inspect actual stdin and ensure it contains no expectation/obligation metadata.
- [ ] Inspect positive scope and negative raw Core/crypto/admission evidence; do not treat PASS as permission.
- [ ] Reproduce all 18 cases and 13 transport controls on normal/repeated/optimized Python.
- [ ] Inspect each physical mutation, baseline witness, incorrect authorization, positive control, restoration and exit code.
- [ ] Reproduce the unchanged Core conformance suite and semantic determinism from a fresh checkout.
- [ ] Supply a genuinely independent implementation before claiming cross-implementation validation.

Recommendation: **READY_FOR_INDEPENDENT_REVIEW** as a narrow reusable pilot. **HOLD** for universal conformance claims, arbitrary execution authorization or production payments.
