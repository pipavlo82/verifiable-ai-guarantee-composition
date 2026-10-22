# Adapter contract and developer guide

This repository-specific v0 transport is experimental. It is not a new ERC interface, Semantic ABI definition, RSI relation format or recompute-kit standard.

## Request and response

The runner sends one UTF-8 JSON document to stdin:

```json
{"schema":"agent-harness.request.v0","profile":"rvr-reviewed-artifact-v0","cases":[{"id":"permitted_review","input":{"...":"complete case data"}}]}
```

The `input` object is opaque to the harness. The selected profile defines it. In this pilot it contains exact base64 receipt/bundle/contract bytes, signed documents, requested claim, catalog, and context. The runner sends no `expected`, obligation descriptions, or grading policy. IDs are stable locators, not promises about expected outcomes.

An adapter must execute its backend and emit only one stdout JSON document:

```json
{"schema":"agent-harness.observation.v0","observations":{"permitted_review":{"behavior":{"receipt_status":"VERIFIED","decision_status":"VERIFIED","core_gate":"ACCEPTED","recomputation_status":"REPRODUCED","verification_outcome":"VERIFIED"},"authorization":{"status":"VERIFIED","authorized":true,"scope":{"...":"exact established scope"}},"evidence":{"...":"raw verification reports and identities"}}}}
```

This is a shape illustration, not a passing fixture. Return raw observed behavior even if inconsistent. Do not repair `REFUTED` plus `authorized=true`, or replace a missing native result with VERIFIED. Diagnostics go to stderr. Exit zero means only that a report was produced. Nonzero exit, crash, malformed/duplicate JSON, missing or extra cases, unavailable dependencies and empty suites cannot produce a successful conformance result.

The **whole** `behavior` and `authorization` objects are compared by the pinned recompute-kit reporter grader. `evidence` retains supporting reports but is not independently certified by the transport. The pilot adapter executes real verification and independent admission; another adapter's mere assertion is insufficient to establish that it did so. A dishonest adapter can hardcode known vectors. Review, discriminating mutations, trusted execution and independent replay remain necessary.

## Six separate outputs

| Axis | Source / meaning |
| --- | --- |
| Normative specification requirement | A pinned specification clause, explicitly labeled `NORMATIVE_SPECIFICATION` |
| Research-policy requirement | An external scenario restriction, explicitly labeled `RESEARCH_POLICY` |
| Expected behavior | Independently authored vector, never obtained by calling the backend |
| Observed implementation behavior | Captured adapter execution, including raw receipt outcome/recomputation/gate axes |
| Backend conformance | Comparison against this exact finite profile; not universal conformance |
| Evidence-supported authorization | Backend's freshly recomputed tri-state and scope, kept separate from PASS/FAIL |

`agent-harness.report.v0` records each axis, command, input/config/suite/output hashes and raw evidence. The `authorization_credential` field is always false. Consumers must not promote this report into a bearer permission.

## Supply another implementation

1. Select the independently specified obligations in `erc8404/obligations.json`. Review their assumptions. An implementation that supports only the normative receipt layer can legitimately fail the external research-policy profile; that is not an ERC defect.
2. Write an executable adapter that reads the request, maps its exact input preimages to your real implementation, executes it and projects its outputs into the response above. Do not import `vectors.json`, `expected`, or the reference implementation to manufacture observations.
3. Supply an argv configuration, for example:

   ```json
   {"argv":["node","/absolute/path/to/your-erc8404-adapter.mjs"]}
   ```

4. Run the **same** suite:

   ```sh
   python -B tools/agent_harness.py run --adapter /path/to/adapter.json --out build/other-backend
   ```

5. Preserve the backend's source revision, exact dependencies, stdout/stderr and evidence; supply a positive witness and physical mutations in that backend. An adapter that is missing or cannot run is NOT_COVERED/UNVERIFIABLE, never PASS. A test double is not an independent ERC implementation.

For a different ERC/profile, author a separate obligations file and vectors object with `profile`, nonempty `vectors`, unique `name`, `input`, `obligations` and `expected` entries. Pin both files' exact SHA-256 in a `suite.json` with `id`, `vectors` and `obligations`, each file entry containing `path` and `sha256`. Invoke `--suite /path/to/suite.json`. Contract adequacy must come from the specification/scenario owner; do not derive requirements solely from the backend inventory.

Configuration and adapters are trusted executable code. Paths are not a sandbox. The runner uses argv without a shell for the target; the upstream grader uses its existing shell transport only to replay a local, safely quoted captured-report helper. Expectations are absent from stdin, but not hidden from the adapter's filesystem or its author.

The bridge consumes pinned private recompute-kit functions `_run_reporter`, `_reporter_corpus`, `_strict_json` and `_grader_canon`. These are not claimed stable public interfaces. Any upgrade requires source review, repinning and full transport/pilot/mutation replay. No upstream source is copied into the repository or modified.
