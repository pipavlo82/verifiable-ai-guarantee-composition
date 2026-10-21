# Existing interface compatibility

VerdictGatedEscrow is a non-upgradeable ERC20 escrow with immutable token and x-only
BIP-340 verifier key. `fund` stores a payer-derived id, payee, amount, request hash,
policy hash, version, refund deadline and state. `release` verifies eleven ABI words
under SHA-256, requires Funded, changes state before the token call, and transfers
the stored amount to the stored payee. There is no EIP-712 or ECDSA verdict interface.

| Required binding | External adapter | Existing on-chain semantics |
|---|---|---|
| Exact claim type / scope | Compare to PR7 result and payer grant | Opaque request hash only; no semantic comparison |
| Scenario contract digest | Recompute from canonical bytes through unchanged PR7 | Opaque request hash only |
| Evidence / proof digest | Recompute actual evidence references and bind native proof | Opaque request hash only; native proof not executed |
| Verification profile | Exact profile bytes and SHA-256; pinned underlying source | Opaque request hash only; no profile lookup |
| Authorization outcome | Independent recomputation and exact consumer-record equality | Signed approved word fixed to one; no recomputation of truth |
| Intended consumer | Exact equality with payer grant | In request hash; caller of release is unrestricted |
| Chain ID | Compare grant, request and supplied current context | Direct signed `block.chainid` |
| Escrow address | Compare all three contexts | Direct signed authority and task_contract = address(this) |
| Payment identifier | Match payer grant and escrow snapshot | Direct signed id; payer/salt-derived storage key |
| Job identifier | Exact external grant mapping | Opaque request hash; no separate job semantics |
| Recipient | Compare request, payer grant and stored payee | Transfers to immutable stored payee; does not compare it to request preimage |
| Amount | Compare request, payer grant and stored amount | Transfers stored amount; does not compare it to request preimage |
| Token | Exact address in grant/request/snapshot | Immutable token; generic IERC20 behavior is trusted |
| Nonce | Exact request/grant equality and local reservation journal | submissionId is signed but not globally consumed |
| Expiration | Check submission-time policy clock | Not enforced; refundAfter permits refund, not expiry of release |
| Revocation | Explicit external revoked-signer policy | No revoke/rotate interface; immutable signer persists |
| Replay / duplicate | Local nonce journal and current state | Released/Refunded state prevents repeated release of the same escrow |
| Actual payment | Observe local token balance changes separately | Relies on IERC20 transfer returning true; arbitrary lying tokens can return success without payment |

All manifest fields are cryptographically included in resultHash, but this is not
on-chain semantic enforcement of their values or correspondence with funded state.
The policy document is similarly committed by tdHash. The new `decision_ref` preimage
has an explicitly laboratory schema. Contract wire compatibility is demonstrated;
conformance to the private service's ledger/decision semantics is NOT established.

`services/verdict_relay.py` is referenced upstream but absent at the inspected commit.
The stock test's optional import skips the private-server comparison when unavailable.
Its digest result is compared independently with Solidity and our Python/Node ABI
encoding, not reported as execution of the absent server implementation.

Conclusion: PARTIALLY_COMPATIBLE. A native verified laboratory conjunction can feed
the existing wire format, but broad independent on-chain policy enforcement is absent.
