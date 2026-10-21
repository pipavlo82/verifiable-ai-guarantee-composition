# Limits and exact open obligations

Status of the external evidence chain remains **PARTIAL_CHAIN_VERIFIED**. v4 adds
contract-relative coverage experiments, not missing external artifacts.

1. Contract adequacy is assumed. Separate contract/catalog files prevent the tested
   circular inventory oracle but do not prove requirements were fully elicited.
   Both were authored in this experiment; independent human requirements review is
   pending. A maliciously replaced trusted contract is outside the threat model.
2. The corpus is deliberately finite and includes weak baselines. False
   authorizations are relative to explicit laboratory oracles, not deployed
   attacks or population rates. Controls are not independent statistical samples.
3. Real EIP-712 signatures over controlled laboratory assertions are newly issued
   with ephemeral keys. They are not external observations. Ten preserved signed
   documents are replayable; private keys were not preserved. Regeneration changes
   signatures, so reproducibility replays frozen bytes rather than reissuing them.
4. The retained native zkIE proof is genuine for the local public MatMul wrapper.
   No trained model, zero knowledge, general malicious-prover security, Ethereum
   verifier deployment or ERC-8274 compatibility is certified.
5. Identity transformation is replayed from the pinned Appendix C fallback. No
   arbitrary sanitizer, live IPFS availability or historical input admission is
   established. The chainId is laboratory context, not observed chain provenance.
6. Signed receipts and observation hashes support integrity, not external task
   execution. Missing external producer admission, model authority, exact external
   proof-to-judgment binding and execution occurrence remain blockers.
7. Same-host Node/Python checks provide implementation diversity only. Fresh
   checkouts and GitHub CI provide runtime reproduction, not independent human
   validation or organizationally independent source acquisition.
8. Mutation coverage is restricted to executed sites and witnesses. Catalog alarms
   are distinguished from unsafe-authorizing bypasses. The initial development
   generator crashes are retained as CRASHED; they are not retroactive kills.
9. Exact procedure/dependency/policy/authority/scope fields are enforced. Human
   descriptions, source citations and coverage justifications require review;
   matching them syntactically would still not prove semantic adequacy.
10. Runtime samples include raw measurements and disclosed shared crypto costs.
    No performance or general security improvement is inferred from this machine.

## Executable acquisition and review plan

First independently review contracts and propose a new scenario requirement that
was not derived from existing code. Preserve that revision, a positive witness,
an omitted-catalog witness and a targeted enforcement mutant. Re-run
`python -B tools/v4/validate.py` and the artifact inventory.

For an external chain, acquire exact raw bytes and admission records, the declared
transform/CID and model authorization, a genuine proof with its public statement,
an authentic authorized judgment committing that proof/action, and independent
execution occurrence evidence. Record source/commit/producer/authority/hash before
normalization. Verify the appropriate native and signature tools and bind every
edge. Missing inputs must remain UNVERIFIABLE. Do not relabel laboratory artifacts
or infer execution from issuer assertions. The v3 acquisition plan remains in
../OPEN_PROOF_OBLIGATIONS.md; no upstream changes or researcher contact are needed
to complete independent local coverage work.
