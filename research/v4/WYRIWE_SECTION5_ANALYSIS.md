# WYRIWE Section 5 and L4: preserve conditional semantics

Primary source: [ERC PR #1810 at c0e13d1](https://github.com/TMerlini/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md).
This is an open draft, not a final ERC. Exact source bytes and SHA-256 are in
evidence/v4/sources and fixtures/v4/source-lock.json.

## Normative requirements at this version

Section 5 always requires signature/digest checking against a known attestor.
Its raw-input and transformation checks are conditional on corresponding inputs
being available; all applicable checks must pass. It does not unconditionally
require consumers to possess every preimage. Therefore absent raw bytes alone
must not be described as ERC nonconformance or a refuted signature.

Section 1 distinguishes keccak256 of exact raw bytes, the commitment to the full
UTF-8 pipeline CID followed by the raw hash bytes, and keccak256 of exact sanitized
bytes. Section 2's identity sentinel is fixed, with raw/input equality. Section 3
specifies the eight ordered EIP-712 fields. Section 4 binds the chain domain to
the actual chain; this experiment's 31337 domain is declared laboratory context,
with no observed chain origin. We do not certify full ERC conformance.

## Stronger research policy, separately identified

AUTHENTICATED_ATTESTATION means the preserved statement has a valid signature
under the declared allowlist/domain. It is not evidence that hidden bytes were
admitted or transformed. INPUT_PROVENANCE_ESTABLISHED in this experiment requires
available raw bytes and replayable identity transformation evidence. This is a
stronger **research-policy availability requirement**, not a rewrite of Section 5.
Even that label establishes a byte relationship, not external historical admission.

positive_attestation succeeds with raw and transform evidence absent. missing_O03
and missing_O04 are UNVERIFIABLE for the stronger replay request. Negative O03/O04
exercise available but inconsistent data; actual signatures alone do not override
them. The Appendix C identity JSON is preserved from the pinned source, rather
than falsely reported as a successful IPFS retrieval. O04 checks its exact digest.

## Composition / L4

The pinned L4 prose distinguishes off-chain exact-proposal SHA-256 and SHA-256
over a declared JCS preimage from deployment-specific on-chain keccak/ABI profiles.
The producer publishes the committed field list including the proposal pin;
consumers must use that actual list. A suggested example list is not universal.
Optional intended-verifier and policy-commitment fields may be required by a
consumer research policy without becoming unconditional ERC conformance rules.

L4 distinguishes authentic, task-bound judgment from judgment soundness, permission
to proceed and independent endorsement. It separates inner proof authenticity,
outer authority and the accountability record pointer. Timestamp conditions for
on-chain records cannot be backfilled onto historical off-chain records with
missing fields. The draft's illustrative code/comments and cross-references
include profiles older than its current off-chain prose; a consumer must select
and pin the actual declared profile instead of silently unifying incompatible
commitment recipes.

The v4 LabJudgment and LabReceipt EIP-712 schemas remain explicitly laboratory
schemas. They are not relabeled as L4 artifacts. No external proposal/commitment/
judgment/execution chain was acquired. Section 5 timestamp is informational;
our nonce snapshot is an additional laboratory replay policy, not ERC-provided
replay prevention. A signature establishes authenticity, not factual correctness.
