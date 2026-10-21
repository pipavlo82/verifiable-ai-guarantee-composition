# Review findings: independent reconstruction

The user attributes two findings to Federico. The captured public PR4 issue,
review and inline-comment responses contain no review text. We preserve that
snapshot and do not invent a quotation, review date or independent reviewer
endorsement. The two technical behaviors are reconstructed and executed here.

1. At unchanged v4 head ee1143f2b8f669a88f36c736d20bb86c2ade950a,
   newly generated genuine laboratory signatures allow all three roles to use
   one authorized key. v4 C authorizes its declared laboratory claim. v4 has no
   scenario-dependent O14. The new independent scenario rejects self-judgment;
   the explicitly permissive scenario still accepts it.
2. v4's replay contract omits output binding O13. Changing outputHash to a false
   value leaves its declared replay checks green. That does not prove the replay
   implementation verified that outputHash. Its boolean output does not itself
   enumerate the excluded field or exact authorized scope. The external consumer
   either rejects the field or explicitly excludes it from the scoped decision.

`tools/erc8404/secondary.py` replays both against the unchanged v4 implementation
and independently recovers laboratory signatures with eth-account/eth-keys.
The evidence includes new signed witness bytes and exact contract/policy bytes.
These are controlled fixtures, not external production observations.

Controls cover independent checker, self-judgment, absent O14 coverage,
counterfeit O14 definition, missing producer, incomparable identities,
additional role separation, contract preimage absence, wrong contract digest,
wrong claim type, wider scope, wrong signed contract, false outputHash, unconsumed
payment field and cross-context authorization reuse. Physical source mutations
are run in isolated copies, with baseline/restore/positive controls. A crash is
never counted as a kill.

These are external consumer-policy obligations. They are not new normative
requirements for ERC-8404, WYRIWE or ERC-8274.
