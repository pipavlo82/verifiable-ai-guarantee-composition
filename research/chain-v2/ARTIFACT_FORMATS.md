# V2 artifact formats and exact claim boundary

This is an independent laboratory profile, not an official Trustless AI specification.
The [source lock](../../evidence/v2/sources.lock.json) records the exact upstream files.

## Retained native zkIE proof

The original adapter calls `zkie_ops::compose::prove_shard`, serializes its actual
`OpShardProof`, and later deserializes those bytes in a separate process before calling
`verify_shard`. Replay never calls the prover. Two 380-byte proofs are retained with
their exact input, weights and output bytes. The Rust dependency source is unmodified.

The supported operator is one public `MatMul(a=0,b=1,c=2,m=4,k=8,n=8)` over Goldilocks,
modulus 18446744069414584321. Tensors contain canonical unsigned 64-bit little-endian
field values, with 32 input, 64 weight and 32 output entries. This is a small linear
model, not a trained neural network, private inference or an LLM.

`VAGCNP2` followed by a NUL is the 8-byte header. Each vector has a little-endian
u32 length then canonical u64 field elements. Vectors follow in this exact order:
claimed scalar (1), u (2), v (3), challenges (3), sumcheck round coefficients (9),
terminal evaluations (2). Three claims follow: u32 tensor id, point vector (5/6/5),
evaluation vector (1). Tensor ids must be 0,1,2. `bound` and `binds` must be empty.
Trailing bytes, other shapes and noncanonical fields are unsupported and yield
UNVERIFIABLE. Extracted values and tensor SHA-256 digests are in each capture's
`public-statement.json`; `statement.py` is an extractor, not a verifier.

The native implementation is a development prototype. Its public challenges are
generated with the pinned test-style XorShift64 path. Native acceptance is not a
claim of malicious-prover soundness, zero knowledge or succinct verification. Our
adapter additionally checks all tensor claims, the claimed output MLE and the full
recomputed output. A separately authored Python multiplication checks the captured
outputs. We rely on full recomputation for this narrow arithmetic relation.

## Signatures and provenance

`src/v2/crypto.mjs` declares exact EIP-712 schemas. Primitive operations use locked
`@noble/curves@2.0.1` and `@noble/hashes@2.0.1`; the inherited package-lock pins tarball
integrity. The encoder is checked against the published EIP-712 Ether Mail signature
and the empty Keccak-256 known answer. Signatures are genuine secp256k1 r||s||v bytes,
with low-s verification and v=27/28. Private keys were OS-random, kept in process
memory, never written or logged, and discarded after capture.

The provenance struct is the pinned eight-field `WyriweAttestation`. Raw bytes are
retained; identity sanitization is byte equality. Its pipeline commitment is
Keccak256(UTF8(full identity sentinel IPFS URI) || rawInputHash bytes32), following
the pinned draft. This verifies the declared identity operation and commitment;
it does not prove external admission of those bytes or IPFS availability.

The domain is explicitly **offline laboratory policy**, name
`ERC8004AttestationGateway`, version `1`, chainId `31337`. No network's `block.chainid`
was observed. Consequently these are genuine EIP-712 signatures using the draft
struct, **not a claim of full WYRIWE deployment conformance or a real chain origin**.
No on-chain transaction, ERC-8004 registration or external issuer is asserted.
Timestamp zero is an informational sentinel; chronology is not inferred.

`LabJudgment` and `LabReceipt` are original laboratory schemas. Their exact field
order and types are in `crypto.mjs`. They are not relabeled as the upstream nine-field
`JudgmentExecutionAttestation`, and are not a ReceiptOS production adapter. They bind
subject, input/output/model/proof hashes, action, scope, execution id, policy hash
and nonce. Receipt additionally binds result bytes and local observation bytes.
Ten authentic signed artifacts include explicitly labeled unrelated action,
execution, domain and unauthorized-key controls. All are laboratory artifacts.

## Execution and authorization

The capture actually creates, writes, fsyncs and reopens `delivered.bin`. The bytes,
commands and local observations are preserved. Signatures are generated after this
operation. No pre-execution judgment or trusted temporal ordering is claimed.
The observation author and signer are controlled by this experiment. A reviewer
can reproduce the operation and recompute the result, but these artifacts do not
independently prove that a historical external execution occurred.

The positive downstream claim is only `recompute-output` under the independently
selected `lab-recompute-policy-v2`. Every required relation is checked against the
caller claim and policy. An external historical execution or successful task
completion claim returns UNVERIFIABLE even when all signatures and native checks
pass. No full real external chain positive exists in v2; that acceptance gate is
explicitly NOT IMPLEMENTED. Nonce protection is an explicit caller snapshot, not
an atomic durable service. Policy trust and public-key authorization are laboratory
assumptions, not an external endorsement.
