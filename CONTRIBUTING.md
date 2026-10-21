# Contributing

Contributions should make a specific claim easier to verify independently. Start
with the [roadmap](ROADMAP.md), [architecture](docs/ARCHITECTURE.md),
[current status](docs/STATUS.md) and [integration boundaries](docs/INTEGRATIONS.md).
The research is experimental; passing a finite suite is not production certification.

## Prepare a reviewable change

1. Create an isolated branch from an identified base commit. State the problem,
   affected claim/profile and intended behavior; keep unrelated changes separate.
2. Distinguish normative source requirements, observed implementation behavior,
   research-policy restrictions and hypotheses. Pin exact source versions.
3. For new verification behavior, include a positive witness, isolated negative
   witness, missing-evidence case and mutation control at the affected boundary.
4. Run the applicable [reproduction commands](docs/REPRODUCIBILITY.md), preserve
   commands/logs/exit codes, and inspect CI on the exact proposed commit.
5. Submit the evidence and limitations for review. A merge, CI success or hosting
   under Trustless AI must not be described as independent academic approval.

Documentation-only changes need link/rendering, formatting, diff and integrity
checks; do not add implementation changes or new behavioral tests just to restate
prose. The existing workflows remain the regression gates.

## Preserve evidence and semantic boundaries

- Keep original v0–v4.1, PR #5–#8, ERC-8404 and escrow reports, source pins,
  conformance vectors and raw evidence unchanged. Corrections and later replays
  are additive, dated and pinned; do not rewrite an old failure as a pass.
- ERC-8404 Core and upstream escrow are frozen inputs to these experiments.
  Additional authorization policy belongs in an explicitly scoped external profile.
- Distinguish VERIFIED, REFUTED and UNVERIFIABLE. Refuse authorization when a
  required fact is missing; do not label that absence a demonstrated refutation.
- Report mutation KILLED, SURVIVED, CRASHED, NOT_APPLIED and UNVERIFIABLE separately.
  A kill requires an executed distinguishing witness and a working positive control.
- State what the evidence does not establish. Signature validity, proof validity,
  key inequality and receipt matching do not automatically prove truth, authority,
  controller independence or external execution.
- Use deterministic canonical bytes and LF technical text. Preserve exact imported
  bytes when a historical digest requires them; never normalize frozen inputs.
- Keep generated replay outputs in ignored `build/` or a separately identified
  evidence location. Never commit secrets, production signing keys or credentials.

`artifacts.sha256.json` is the current whole-tree inventory. Regenerate it only for
an intentional, independently reviewed file change set; retain all unaffected
entries and run the stricter source/history checks afterward. The pinned root README
is preserved; the concise GitHub entry point lives in `.github/README.md`.

## Attribution, licenses and collaboration

Preserve Git authorship, original notices and the existing [MIT license](LICENSE).
Vendored/imported material keeps its own license; adding a link does not relicense
or transfer ownership of an ecosystem project. Semantic ABI, RSI and recompute-kit
remain separate components with their own histories and responsibilities.

This guide does not appoint maintainers, grant merge rights or establish a new
governance agreement. Repository permissions and any future responsibility or release
agreements must be recorded explicitly by the people involved. Use issues and pull
requests for concrete proposals; no response time or review commitment is implied.

Keep experiments local unless separately authorized. This roadmap and contribution
guide do not authorize production deployment, real-fund transactions or changes to
upstream standards. Report unsupported guarantees as limitations rather than
claiming an upstream vulnerability from a research-only policy mismatch.
