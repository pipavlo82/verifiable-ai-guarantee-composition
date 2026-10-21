# Source and dependency graph

The live API captures and fetched Git refs are preserved in `evidence/integration/phase1/`.
Git ancestry is `main -> #2 -> #3 -> #4 -> {#5, #6}`. PR #3 and #4 target main
in GitHub even though their commits include the earlier research. API target branches
and commit ancestry are different facts.

| Ref | Exact HEAD | API base |
|---|---|---|
| main | 18a5916098addf6447700ed95441125bfa7079c3 | n/a |
| #2 | 653b8e92e56afb99797c04b1c616a6d7fb3555e9 | main |
| #3 | 98ffba16730030c797c47766e13a5314181ba2f6 | main |
| #4 | ee1143f2b8f669a88f36c736d20bb86c2ade950a | main |
| #5 | c14d96b0a63fceba02b2cb4469d5b3228ae46612 | #4 |
| #6 | b0e894db53d58370df0d9959e070a1302f4a5787 | #4 |

The integration branch starts from #6. Eighteen additive #5 files are imported
byte-for-byte from its exact Git tree. This is a content dependency, not a claim
that #5 is a Git ancestor. No merge operation or existing-branch update is used.
The new draft PR targets `research/erc8404-claim-aware-compatibility`.

#5 is open and ready for review, with an APPROVED review pinned to c14d96b0.
Its six fork workflows are `action_required`, with zero completed check runs.
The existing approval is explicitly bounded to the two admission fixes. #2, #3,
#4 and #6 remain drafts. Source code and review assertions are checked separately;
the new execution logs, not these descriptions, support reproduction claims.

`fixtures/integration/source-lock.json` pins 9,251 preserved #6 files, all 18
imported #5 files and 13 executable Core files. README and the new complete
repository manifest are intentionally versioned outside the historical lock.

Upstream implementation pins: zkIE `39d8df96877bc3bebf33c69b06907d792b3184b9`;
recompute-kit `f7308cdd5ba55ac8229103e82ebc5fc14f81b88b`;
agent-ercs `01283ca57305f915afb560d23359a27fd748eb5a`;
receiptos-verify `396143120f787d2f5534e92c0cf896c029a05775`;
RVR `9dd36e882dd372f264b77b179130948aa5adcbde`.
Proposal versions and exact preserved text hashes are in
`evidence/erc8404/sources/sources.json`. These are the selected research versions,
not an assertion that upstream interfaces will remain unchanged.
