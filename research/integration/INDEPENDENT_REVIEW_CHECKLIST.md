# Independent review procedure

Use a fresh checkout of the reported integration commit. Review the source lock,
dependency graph and original PR branches before trusting the report.

```sh
python -B tools/verify_artifacts.py
python -B tools/v3/prepare.py --online
python -B tools/integration/validate.py
python -B tools/verify_artifacts.py
git status --porcelain
```

Pinned tools: Python 3.12, Node 22.15.0, Bun 1.3.14, Rust 1.97.1. Dependency locks
and hashes are preserved. After dependencies are available, preparation supports
offline Cargo replay. Logs and command exit codes are written under
`build/integration/validation`; fixture generation is not part of replay.

- Recompute the joint contract and both original profile commitments independently.
- Inspect what each signature and native public statement actually says.
- Confirm both subject labels remain distinct and the proof-byte edge is checked.
- Reproduce forged flags, missing/changed scenario, scope/type/contract reuse.
- Reproduce O14 self-judgment, missing identities and explicit self-allowed policy.
- Exercise read-without-validation and unknown nested fields.
- Check missing preimages/profile/payload and REFUTED versus UNVERIFIABLE.
- Reproduce all source-copy mutations, restoration and positive controls.
- Verify original 16/1 versus additional fallback-carrier isolation separately.
- Verify Core byte identity and Python/TypeScript conformance outputs.
- Inspect native build/replay and independent signature recovery logs.
- Review the external contract adequacy assumption and exact missing real links.

Neither PR #5 nor #6 is merged by this work. Integration review readiness is a
bounded research verdict. Existing #5 fork CI remains an independent workflow
approval issue; the new integration CI cannot retroactively change that status.
