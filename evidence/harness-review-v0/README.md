# Supplemental review evidence

`replay.zip` preserves raw commands, exit codes, adapter requests/stdout/stderr,
projections, original/mutant/restored results, physical mutant source files and
GitHub state snapshots for this follow-up. `archive.json` records its SHA-256 and
every member's SHA-256. No member needs to be executed to verify its bytes.
The root repository inventory pins the archive and its manifest.

Contents:

- `original-validation/`: unchanged original 18-case / 12-mutation validation,
  including normal, repeat, Python `-O`, Core conformance and transport controls.
- `validation/`: supplemental normal and optimized execution, each with repeated
  scenarios, five original-suite physical mutations and four isolated witnesses.
- `prerequisites/`: tampered expectation refusal and exact missing-history/fetch
  recovery evidence; the temporary Git clone itself is excluded from the archive.
- `github/`: live PR #9/#10 refs, draft state and check snapshots. These green
  checks are for their original published SHAs, not the local follow-up commit.

The earlier `evidence/harness-v0/` bytes and all historical research reports are
preserved. The reviewer report is attributed in
[REVIEW_FOLLOWUP.md](../../research/harness-v0/REVIEW_FOLLOWUP.md); no raw macOS
replay artifact was supplied here. New execution in this archive is local Windows
Python 3.12.10 / Node 22.15.0. This is not a fresh external-chain verification or
a scientific novelty claim.

Reproduce using the [supplemental profile commands](../../conformance/agent-harness-review-v0/README.md).
Verify the complete repository with `python -B tools/verify_artifacts.py`.
Archive member hashes can be recomputed with Python's `zipfile` and `hashlib`;
there is no extraction requirement, private key or executable download step.
