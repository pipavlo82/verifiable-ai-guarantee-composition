# Supplemental review controls for the first harness pilot

These controls follow the reviewer report forwarded by Pavlo on 2026-10-22.
They supplement the frozen 18-case profile at PR #9 commit
`0e17c97e896916b4d9505072cc9ebe2018329b01`. The original vectors, 12-mutation
report, consumer, adapter, grader and ERC-8404 Core remain unchanged.

## What is tested

Five vectors: the existing permitted review plus four isolated negative witnesses.
Each negative has one REFUTED check and all other checks VERIFIED. Physically
removing that one check produces an incorrect authorization; restoring the source
returns to refusal. These are external research-policy requirements, not new ERC
requirements or demonstrated upstream vulnerabilities.

| Guard | Isolated witness | Expected | After removing only this check |
| --- | --- | --- | --- |
| `scope` | Requested scope differs from the contract; signed documents stay unchanged | REFUTED | Incorrect authorization |
| `scenario` | Requested scenario differs from the contract | REFUTED | Incorrect authorization |
| `definitions` | Catalog changes S04 from authority verification to signature verification | REFUTED | Incorrect authorization |
| `supported_contract` | Authentic preserved signatures bind a contract and claim for EXTERNAL_TASK_SUCCESS | REFUTED | Incorrect authorization |

The supported-contract witness reuses `fixtures/erc8404/lab/unsupported_claim.json`;
it does not fabricate an external observation or require new signing keys.
`review_vectors.py` authors expectations without importing the consumer.

## Reproduce

Use a full clone, Python 3.12 and Node 22.15.0. The Git objects for the reviewed
head above and its research base `2e329fffbee103047d034b97056aea9e49cf1c58`
are required. For a shallow checkout, fetch them explicitly:

```sh
git fetch origin 0e17c97e896916b4d9505072cc9ebe2018329b01
git fetch origin 2e329fffbee103047d034b97056aea9e49cf1c58
python -B tools/agent_harness.py prepare
python -B research/formal-v1/prepare_crypto.py
cd build/formal-v1/crypto
npm ci --ignore-scripts --no-audit --no-fund
cd ../../..
python -B tools/harness_v0/validate.py
python -B tools/harness_v0/review_validate.py
python -B tools/verify_artifacts.py
```

The first validation preserves the original normal/repeat/-O, transport, Core and
12-mutation regression. The second reproduces the reviewer's five mutations
against the old suite and adds the four isolated mutations, in normal and optimized
Python. Both modes repeat the supplemental suite; semantic outputs and mutation
outcomes must match. Crashes, unavailable adapters, broken positives and failed
restorations cannot count as kills. Eight classification controls enforce this.

Run just the new vectors through the unchanged CLI:

```sh
python -B tools/agent_harness.py run --suite conformance/agent-harness-review-v0/suite.json --adapter conformance/agent-harness-v0/erc8404/adapter.json --out build/harness-review/run
```

The historical and supplemental reports remain separate. Do not describe the
original 12/12 as full guard coverage, or count the existing reuse/admission
mutation twice. These witnesses establish non-redundancy for these finite cases;
they do not cover every conjunct of `supported_contract`, all definition changes,
or every possible authorization boundary.

See [analysis and results](../../research/harness-v0/REVIEW_FOLLOWUP.md),
[preserved evidence](../../evidence/harness-review-v0/README.md), and
[original limitations](../../research/harness-v0/LIMITATIONS.md).
