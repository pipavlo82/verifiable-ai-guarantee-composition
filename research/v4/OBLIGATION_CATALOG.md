# Typed obligation catalog v4/1

The authoritative machine records are [catalog.json](../../fixtures/v4/catalog.json).
Every entry carries all thirteen fields requested by the research protocol.
The independent requirement sets are [contracts](../../fixtures/v4/contracts).
All successful conclusions are scoped to the declared local laboratory policy.

| ID | Obligation / evidence procedure | What it does not establish |
| --- | --- | --- |
| O01 | EIP-712 provenance signature verification | Truth of the attestation or original input admission |
| O02 | Native pinned zkIE public MatMul verification, bound public statement and recomputed output | Authorized model, trained-model accuracy, ZK or general prover soundness |
| O03 | Exact raw bytes match signed rawInputHash | Historical admission by an external producer |
| O04 | Pinned identity transform bytes, byte equality and pipeline/input commitment replay | Safety of arbitrary sanitizers or verified IPFS transport |
| O05 | Requested input matches native input and all signed inputs | Other undeclared inputs or hidden context |
| O06 | Exact model manifest, weights and policy model binding | Global model authorization or training provenance |
| O07 | Judgment signature, proof identity, subject and action binding | Judgment correctness or WYRIWE L4 conformance |
| O08 | Laboratory signer allowlist for each role | Legal/organizational identity or on-chain agent registry |
| O09 | Receipt signature and execution identifier binding | External execution occurrence |
| O10 | Preserved result and observation bytes match signed hashes | Historical factual correctness of the observation |
| O11 | Policy bytes/content, declared domain and nonce snapshot | Observed chain domain, durable replay protection or timestamp ordering |
| O12 | Consistent signed/requested scope and narrow claim kind | Stronger task success |
| O13 | Requested output matches native output and signed outputs | Any broader model or workflow correctness |

Claim profiles: AUTHENTICATED_ATTESTATION consumes O01/O08/O11;
INPUT_PROVENANCE_ESTABLISHED adds O03/O04, meaning only available-byte replay under
this research policy. LAB_REPLAY_ADMISSIBLE consumes O01–O12;
LAB_OUTPUT_REPLAY_ADMISSIBLE adds O13. The first two profiles retain the laboratory
bundle's shared policy/domain context; they are not generic minimal ERC verifiers.
DOWNSTREAM_CLAIM_AUTHORIZED is a decision about one exact profile, never a universal
guarantee or an unqualified full-chain label.

All O01–O13 use REFUTED for observed mismatches and UNVERIFIABLE for missing
prerequisites. Dependency edges are named in both contract and catalog; equality
and closure are checked. Metadata descriptions supplement, rather than replace,
executable checks. The semantic adequacy of procedure identifiers needs review.
