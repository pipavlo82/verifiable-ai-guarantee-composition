# Claim-aware result to verdict-gated escrow: laboratory architecture

```mermaid
flowchart TD
  P[Preserved native zkIE proof + exact public input/model/output] --> V[Unchanged PR7 independent consumer]
  E[Authentic laboratory attestations + RVR receipt] --> V
  K[Consumer-selected canonical scenario contract] --> V
  V --> A[Exact scoped authorization]
  G[Separate payer grant + trusted current escrow snapshot] --> X[External payment adapter]
  A --> X
  X --> S[Deterministic laboratory BIP-340 signer]
  S --> D[Verdict-relay v2 digest and signature]
  D --> C[Unchanged escrow in Foundry EVM]
  C --> T[Mock token transfer + observed balance delta]
  C -. does not recompute .-> V
```

The public Base deployment is inspected only through read-only RPC. Local test
instances are ephemeral in-process EVM objects; no Anvil RPC deployment, network
broadcast, real funds or production key is used. The production fixed verifier key
is different from the deterministic public laboratory key.

The deployed escrow does not call the adapter. Anyone holding an approving signature
can submit it directly. An honest signer/gateway is therefore a necessary off-chain
assumption. An expiry or revocation that changes after signing is not independently
enforced by the existing contract. A stronger mandatory on-chain policy requires a
new interface/contract or separately authorized gate; none is implemented upstream.

The adapter grants only payment for the verified laboratory replay/review service
under a separately supplied payer policy. Native inference verification does not
itself authorize spending. No assertion of completed external work is introduced.
