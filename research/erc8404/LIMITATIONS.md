# Limits and unsupported guarantees

- Contract adequacy and trusted selection are assumptions, not mechanically
  established completeness for an open world. A hash authenticates bytes only
  relative to a trusted identity/selection channel.
- The implementation supports one narrow external claim type and one exact RVR
  SHA256_EQUALS profile. It is not a generic ERC-8404 conformance certification,
  a registered standard profile or a deployed settlement integration.
- Laboratory EIP-712 signatures are genuine but researcher-generated, clearly
  labeled and signed with ephemeral keys. They do not establish external admission,
  execution, organizational independence, judgment truth or preregistration time.
- RVR byte identity of a proof artifact is not native proof validity. Historical
  native verification remains separately scoped. No new full WYRIWE→zkIE→judgment
  →execution chain has been acquired: full-chain status remains partial.
- The local decision is not signed or persisted as a transferable capability;
  consumers must re-evaluate the evidence and trusted context. No online replay
  database, revocation service, chain canonicality or finality is implemented.
- S01/S05 cryptographic/domain checks are reused and tested, including a second
  signature implementation. The new mutation claims concern explicitly listed
  consumer boundaries, not exhaustive mutation coverage of cryptography or Core.
- One contract-preimage mutation survives: when both raw carrier and parsed hint
  are absent, changing the resolver to use the hint still yields no contract and
  the consumer refuses. This is not certified mutation coverage of that boundary
  or a proof of global equivalence. The initial published witness retained the
  full parsed contract and measured mandatory-carrier policy instead of actual
  preimage absence; its 17-kill report is preserved and superseded by 16/1.
- Catalog completeness is relative to the independently supplied contract.
  Implementation and contract authorship are not institutionally independent.
- A/B comparative modes intentionally lift narrower results into a broader
  downstream decision. Their false authorizations are consumer-policy outcomes,
  not incorrect ERC-8404 implementations or upstream vulnerabilities.
- Finite fixtures and local timings do not establish general security, proof
  soundness, performance advantages or scientific novelty.
- The executable accepts the documented typed request envelope; it is a research
  CLI, not a hardened public network service. The enumerated malformed-input
  controls do not claim exhaustive parser fuzzing or resource-exhaustion coverage.

## Neighboring primary sources

Exact sources are in `evidence/erc8404/sources/sources.json`. WYRIWE §5 always
requires signature verification; raw-byte/transform checks are conditional on
availability. A stronger provenance policy is separate. Its L4 commitment fields
are producer-declared; authentic judgment does not mean soundness, permission or
independent endorsement. This experiment's LabJudgment is not relabeled as L4.

ERC-8274 separates inner proof verification from outer agent authorization. Its
deployment metadata, hash scheme, address-scoped profiles and current outer
digest must be pinned before claiming ABI/semantic compatibility. No deployment
adapter or on-chain conformance claim is made here; the v4 mapping still applies.

ERC-8412 PR2002 at ff9fbc7e2de497d3dec2595a90b262aecd576f5d already specifies
preregistered criteria, typed/itemized obligations, on-chain consistency and
off-chain O1–O5 including document/chain binding. Its criteria digest uses
keccak256(JCS), which is not this consumer's SHA256(rvr-canonical-json-v0).
Its E14 author/verifier distinction and waiver-authority discussion overlap role
separation. No equivalent preregistration ordering or chain attestation is claimed
by this offline consumer. We preserve the draft's own claims separately: its
motivation's broad characterization of judged outcomes is not adopted as RVR
semantics; the current ERC-8404 explicitly supports deterministic verification
of authenticated judgment artifacts without replaying the judgment process.

Guarantee composition, explicit obligations, digest commitments and authority
separation have substantial prior art (see historical v4 PRIOR_ART.md).
The contribution claimed here is a reproducible compatibility experiment with
explicit counterexamples and scope-preserving outputs, not a new cryptographic
primitive or proven scientific novelty.
