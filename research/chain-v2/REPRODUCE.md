# Reproduce v2 from a fresh checkout

Requirements: Python 3.12 (captured 3.12.14), Node 22.15.0, Rust/Cargo 1.97.1,
Git, a C/C++ linker supported by Rust. No API keys or signing keys are required.
Source and dependencies are downloaded only during setup. The proof and signature
artifacts are already public; replay never regenerates or signs them.

```sh
git clone --branch research/real-artifact-composition-v2 https://github.com/pipavlo82/verifiable-ai-guarantee-composition
cd verifiable-ai-guarantee-composition
python -B tools/verify_artifacts.py
python -B research/formal-v1/prepare_crypto.py
npm ci --ignore-scripts --no-audit --no-fund --prefix build/formal-v1/crypto
git clone https://github.com/trustless-ai/zkIE build/chain-v2/zkIE
git -C build/chain-v2/zkIE checkout --detach 39d8df96877bc3bebf33c69b06907d792b3184b9
python -B tools/v2/prepare.py --online
python -B tools/v2/prepare.py
python -B tools/v2/statement.py
python -B tools/validate.py --out build/v0-regression
python -B research/formal-v1/validate.py
python -B tools/v2/validate.py
python -B tools/v2/check_snapshot.py
python -B tools/verify_artifacts.py
git status --short
```

Use `--cargo-home PATH` with prepare.py only to select a cache; it does not change
the lockfile. All subsequent replay can run offline after setup. CI repeats the
same native verifier, actual signature checks and v2 mutations on Linux. V0 and
v1 workflows remain active. Sources are never modified by preparation.

The mutation runner temporarily edits exactly one check in `src/v2/composition.py`,
runs its witness in a fresh process with bytecode disabled, restores in `finally`,
then replays the negative and positive controls. Do not concurrently edit that file
or run another mutation process. Source restoration is checked by SHA-256. Raw
logs under ignored `build/` are safe to retain. A process crash is not a kill.

Determinism means byte-identical comparison and mutation reports across normal,
repeat and Python -O on one platform. Cross-platform comparisons parse native
JSON stdout to accommodate CRLF/LF. Timing, test durations, compiler paths and
binary hashes are platform dependent. Newly generated OS-random signatures are
not expected to repeat. `capture.py` refuses to overwrite the retained capture.

Technical source text uses LF. Raw subprocess logs preserve their original bytes
so their SHA-256 evidence remains truthful, including Windows line endings.
