# Scoped Authorization from Heterogeneous Verification Artifacts

**Research draft, v3. Independent work by pipavlo82. Not peer reviewed.**
Artifact study with a partial real evidence chain; no claim of an upstream
vulnerability, security certification or scientific priority.

## Abstract

Verification results authorize conclusions only within their checked statements
and assumptions. We study how downstream consumers can overextend individually
valid signatures, inference proofs and receipt roots when they omit subject,
authority, domain or dependency bindings. An executable typed AND graph selects
the obligations for a requested claim and preserves three-valued results. Our
case study preserves three externally published Nostr/EIP-712 signed objects,
replays a retained native zkIE laboratory proof, and records actual local
verification execution. In 36 declared scenarios, a deliberately weak
component-only baseline authorizes 21 of 32 negative or unsupported requests;
explicit composition authorizes none. Fourteen executed enforcement mutations
are killed by isolated witnesses. These finite results support the adequacy of
the selected controls, not general security. A complete external chain remains
unverified because admission, model authority, cross-system judgment linkage
and external execution evidence are unavailable.

## 1. Problem and scope

A signature can authenticate a judgment without making it factually correct or
applicable to a requested action. A valid proof can concern the wrong input or
an unauthorized model. A receipt root can preserve a statement about execution
without independently establishing the event. The research question is: under
which explicit conditions do individually verified guarantees justify a requested
downstream claim? Our object of study is a consumer's inference rule, not an
exploit in zkIE, WYRIWE, recompute-kit or ReceiptOS.

We separate eight obligations: input provenance, model/version binding, inference
validity, subject binding, judgment authenticity, judgment authorization,
execution receipt binding and downstream authorization. V3 implements bounded
instances of these obligations and leaves unsupported external links visible.
No evidence is manufactured to obtain a positive full-chain result.

## 2. Definitions and formal candidates

Let a guarantee be `(subject, scope, authority, evidence, assumptions,
dependencies, verification_contract, permitted_claims)`. A claim selects a finite
acyclic dependency graph with AND semantics. `VERIFIED` means evidence satisfies
the selected contract under declared assumptions; `REFUTED` means a known
contradiction; `UNVERIFIABLE` means evidence or a verifier is unavailable.
Aggregation retains refutation if present, otherwise uncertainty if present,
and verifies only a nonempty set of verified dependencies.

The claim planner expands the closure and reports additional bindings beyond
component validity. It does not synthesize missing evidence, resolve arbitrary
natural-language policy or infer authority from the artifact being checked.
Trusted request expectations are literal profile constants.

The no-authorization-from-a-missing-AND-leaf property follows directly from this
definition. The stronger candidate proposition is conditional: given sound
leaf verifiers, complete dependency contracts, correct authority policy and
scope-preserving edges, a verified root entails the conjunction of its declared
leaf guarantees. Structural induction is an intended proof strategy, not a
completed proof of real-world or cryptographic soundness. Necessity is tested
only relative to explicit contracts and witnesses. See
[the full typed model](FORMAL_COMPOSITION_MODEL.md).

## 3. Threat model

The adversary can substitute an artifact, supply a signature from an accepted
key on an unrelated statement, change request subject/action/domain/time context,
omit dependencies or alter proof/receipt bytes. We assume the local verifier
source and caller policy are selected honestly and their execution is not
compromised. Signature unforgeability and hash collision resistance are standard
assumptions, not experimental discoveries. Key compromise, malicious approved
policy, runtime compromise, censorship, model quality and a complete external
execution observer are outside demonstrated protection.

The baseline is intentionally constructed to accept when selected components
verify independently. It is not a replica or characterization of any upstream
authorization service. Expected outcomes are predeclared per scenario and do
not derive from the baseline's decisions.

## 4. Evidence and methods

We pin source commits and selected files, preserve raw HTTP responses before
normalization, and record original SHA-256 digests. The external objects are a
live signed ledger judgment and two published CRC cells concerning its decision.
We reconstruct Nostr event IDs, verify BIP-340 signatures, recompute the Cell
Keccak evidence digest and EIP-712 statement, and recover its signer. Noble in
Node is cross-checked against pinned Python BIP-340 reference code and
eth-account. No external private key is used and no v3 replacement signature is
generated.

The native proof remains a laboratory artifact from v2, verified through the
pinned Rust zkIE implementation and explicit public matrix recomputation. It is
not claimed as the inference behind the public judgment. A local observer receipt
preserves actual subprocess commands, streams and exits; ReceiptOS/Crystal and
Python independently recompute its root. This establishes local record integrity
under an honest-recorder assumption, not historical producer execution.

Each positive bounded stage has negative and missing-evidence controls. For each
of 14 implemented enforcement sites we physically replace one check, run its
isolated negative witness, restore original source bytes, and rerun the negative
and positive controls. A parsed semantic authorization change kills a mutant;
crashes and unavailable runs have different classifications. Six unsupported
integration boundaries are excluded from coverage.

## 5. Results

The 36 scenarios comprise four narrow positive claims and 32 negative or
unsupported requests. Component-only validation falsely authorizes 21/32,
correctly refuses 11/32 and reports six unknown outcomes. Explicit composition
falsely authorizes 0/32, refuses 32/32 and preserves 16 unknown outcomes. Nineteen
unittest methods pass in normal, repeated and optimized Python. Semantic
comparison, signature and mutation outputs are deterministic across those modes.
All 14 executed v3 mutations are killed with zero surviving or crashed mutants.
Original v2 evidence remains 18 killed and two surviving; a separate subsequent
isolation study kills those two. Historical reports are not retroactively changed.

For example, the same genuinely signed reject judgment and valid cells pass
component checks when a consumer requests approval. The scope contract rejects
that request. A preserved valid receipt also remains cryptographically intact
when the requested proof subject changes; the explicit subject check rejects it.
Missing artifacts yield uncertainty, including a complete external-chain request
assembled from individually valid but unrelated native and public evidence.

Twelve paired interleaved samples for a positive claim and a cross-subject case
measure actual verification on the same evidence. Raw measurements and exact
medians appear in [the technical report](V3_REAL_CHAIN_REPORT.md). Fresh process
startup and scheduling variance limit interpretation; we claim no portable
overhead bound or speed advantage. The observed false-authorization difference
is restricted to these deliberately chosen witnesses.

## 6. Related work and possible contribution

Assume-guarantee verification, proof-carrying authentication, remote attestation
appraisal and provenance modeling already address central parts of this question.
Recent attestation and agent-workflow work overlaps directly with binding chains,
permission graphs and execution policies. The [primary-source comparison](PRIOR_ART_ANALYSIS.md)
includes both established publications/standards and clearly identified preprints.
In particular, graph-based authorization and the distinction between authenticity
and authority cannot be claimed as new here.

The potential contribution is a reproducible artifact study: concrete preserved
cross-format objects, explicit limits on permitted conclusions, a claim-driven
obligation planner and load-bearing mutation witnesses. Scientific novelty of
that package is unproven. It may be useful for independent empirical review
without asserting a new general theory.

## 7. Limitations and open obligations

There is no complete external positive chain. Public gateway captures do not
provide a compatible admitted-input artifact linked to this native tuple.
External model delegation and inference-to-judgment linkage are missing. The
signed CRC historical input hash does not open to the newly captured ledger bytes;
historical execution witness hashes are unresolved. The observed outcome endpoint
returns 404, which cannot refute execution. Signing and hash equality do not
repair those missing links.

The fixed canonicalization subset, selected-key policy, limited graph language,
small fixture set, single native implementation and local recorder constrain
generalization. Fresh checkout and another runtime do not provide an independent
human audit. No chain settlement, OpenTimestamps verification, trusted execution
environment, deployed agent authorization or factual judgment verification was
performed. Our receipt object is not claimed as a complete upstream issuance
schema. No formal soundness theorem or complete policy synthesis is delivered.

## 8. Next experimental stage

Acquire exact admitted raw/transformed bytes, a complete profile-specific signed
commitment, independent authority policy, matching native proof statement,
judgment tied to that statement/action and an independently verifiable external
effect witness. The [executable acquisition plan](OPEN_PROOF_OBLIGATIONS.md)
captures bytes and checks bundle completeness without promoting it to semantic
success. New adapters and isolated witnesses must discharge each missing edge
before a new version can claim FULL_CHAIN_VERIFIED. Independent technical and
academic review of the bounded results is useful now; full-chain acceptance
remains on hold.

## References and artifact availability

Full primary-source references are in [PRIOR_ART_ANALYSIS](PRIOR_ART_ANALYSIS.md).
Exact upstream commits, interface differences, artifact formats and licensing are
in [SOURCE_AND_ARTIFACT_AUDIT](v3/SOURCE_AND_ARTIFACT_AUDIT.md). Reproduction commands
are in [REPRODUCE](v3/REPRODUCE.md); raw evidence, command records and machine-readable
reports are under `evidence/v3/`. This draft is for review, not a published
peer-reviewed result or an official upstream specification.
