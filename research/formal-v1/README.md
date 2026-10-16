# Typed composition obligations: research stage v1

This stage narrows the candidate contribution to **profile-specific, representation-aware binding obligations** across separately verified artifacts. Scientific novelty is **NOT ESTABLISHED**. Equality closure, assume-guarantee reasoning and the separation of authentication from authorization are established ideas.

This is independent research, not an official Trustless AI specification, security certification or upstream vulnerability report.

## What was actually executed

| Experiment | Observed result | What it establishes |
| --- | --- | --- |
| Abstract equality model, no native cross-component equalities | 27 inclusion-minimal bases, all size 6; 162 removal countermodels | Necessary and sufficient equality checks within the declared model |
| Same model, one **hypothetically established** native equality | 18 inclusion-minimal bases, all size 5; 90 removal countermodels | The minimum depends on native premises, not a universal checklist |
| Independent exhaustive oracle | 327,680 assignment/subset pairs, agreement with graph closure | Finite implementation cross-check; the general equality lemma has a separate proof |
| New Python suite | 11 tests in normal, repeat and `-O` modes | Research model and boundary controls |
| Public signed Nostr event | 11 checks, repeated; original BIP-340 signature verifies | Authenticity under the embedded public key and a narrow proposal-digest binding |
| New source mutations | 4 KILLED; 0 SURVIVED/CRASHED/NOT_APPLIED/UNVERIFIABLE; restoration passes | Four specific enforcement checks affect their intended negative controls |
| Pinned native zkIE tests | 2 exact tests pass online and in offline replay | Native proving/verification test routines execute, including their substitution checks |
| Unchanged v0 regression | 19 tests in normal/repeat/optimized modes; original results reproduce | Existing synthetic experiment preserved |

The 252 abstract countermodels are **not 252 implementation mutations**. The native tests and public event concern different subjects; they are not a composed real execution. Full WYRIWE EIP-712 verification, proof export, execution receipts and downstream authorization remain **NOT IMPLEMENTED** for a common tuple. The legacy v0 baseline numbers remain synthetic and are not generalized to real deployments.

An initial local v0 regression attempt encountered a Windows sandbox temporary-directory permission error. The unchanged suite passed when rerun with approved access. The failed attempt remains in the local delivery; `evidence/v0-regression/` records the successful run. CI repeats v0 separately and does not run the optional native zkIE Cargo tests.

Read [novelty review](NOVELTY_REVIEW.md), [formal model](FORMAL_MODEL.md), [bridge obligations](BRIDGE_OBLIGATIONS.md), [artifact status](REAL_ARTIFACT_STATUS.md), and [paper revision](PAPER_OUTLINE.md). Machine-readable deterministic evidence is in [evidence](evidence/); the validation reports distinguish executed checks from captured producer statements.

## Reproduce from the repository root

Python 3.12+ and Node 22.15+ are used. Python has no external dependencies. Node uses MIT-licensed `@noble/curves@2.0.1` and `@noble/hashes@2.0.1`, pinned with npm integrity digests. No upstream source is copied into our implementation.

```sh
python -B research/formal-v1/prepare_crypto.py
npm ci --ignore-scripts --no-audit --no-fund --prefix build/formal-v1/crypto
python -B research/formal-v1/validate.py
python -B tools/validate.py --out build/v0-regression
python -B tools/verify_artifacts.py
```

After the first dependency installation, the verifier itself is fully offline. A fresh install from a populated npm cache can add `--offline`. Determinism means byte equality of model, signature-check and mutation reports; timing-bearing unittest/native logs are not expected to be byte-identical.

Native zkIE replay is a separate, more expensive check:

```sh
git clone https://github.com/trustless-ai/zkIE.git build/zkIE
git -C build/zkIE checkout 39d8df96877bc3bebf33c69b06907d792b3184b9
python -B research/formal-v1/native_probe.py --zkie-clone build/zkIE --cache-dir build/native-cache --out build/native-online --online
python -B research/formal-v1/native_probe.py --zkie-clone build/zkIE --cache-dir build/native-cache --out build/native-offline
```

The runner requires a clean pinned checkout and `--locked` Cargo dependencies. It checks that exactly the intended test ran, not merely a zero exit from an empty test filter. Local evidence uses Rust/Cargo 1.97.1. Library tests use upstream testing parameters and deterministic test randomness; this is not a production cryptographic security assessment.

## Version boundary

Frozen v0 is commit `905767f8696afe4cee612c8248f9d5d76f81f81b`. This branch adds `research/formal-v1/` and its own workflow. Only the root SHA-256 inventory is intentionally expanded among existing files. Original v0 code, fixtures, documentation and evidence remain byte-identical; its `NOT IMPLEMENTED` statements describe that frozen version. New observations are recorded here without retroactively attributing them to v0. Main remains unchanged.

Recommendation: **CONTINUE**, with a coherent real artifact tuple and independent review as the next acceptance gate. Hold any claim of demonstrated scientific novelty, end-to-end verification or upstream vulnerability.
