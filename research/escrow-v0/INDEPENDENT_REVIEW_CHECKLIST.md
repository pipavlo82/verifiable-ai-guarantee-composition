# Independent reproduction checklist

Use the exact locally delivered experimental commit; do not merge it into PR7.
Prepare Python 3.12, Node 22.15, Foundry 1.7.1 and solc 0.8.26. The escrow stock
compiler uses optimizer 200; the larger experimental harness additionally uses viaIR.
This harness choice is separate from the exact no-viaIR public-bytecode comparison.

```sh
python -B tools/v3/prepare.py --online
python -B tools/escrow_prepare.py --online
python -B experiments/verdict_escrow/validate.py
python -B experiments/verdict_escrow/integrity.py
```

- Verify every original PR7 tracked byte and vendored upstream source hash.
- Check actual native proof execution, exact request/contract/profile preimages and all payer grant fields.
- Verify BIP-340 signatures independently with Python, Node and unchanged Solidity.
- Reproduce each A-R witness and inspect off-chain refusal versus direct on-chain outcome.
- Inspect the late expiry/revocation controls: an earlier approval is not perpetual current authorization.
- Confirm mismatched document recipient/amount really changes observed mock-token balances.
- Confirm same-id replay and duplicate release fail, while distinct payments may share submissionId.
- Reproduce all adapter and Solidity mutations with positive, baseline and restored controls.
- Keep absent upstream guards NOT_APPLIED; never promote these to killed mutations.
- Compare normal/repeated/Python-O outputs, exact source inventories and fresh checkout.
- Read the observed bytecode comparison and its RPC trust assumptions. No network transaction is required.
- Review the laboratory decision_ref semantics separately from the unavailable private service.
- Review token behavior, global nonce scope, revocation, expiry and caller/gateway bypass before any broader use.

Review recommendation is research-only. Production payment use and FULL_CHAIN_VERIFIED
remain blocked by the documented missing enforcement and external evidence.
