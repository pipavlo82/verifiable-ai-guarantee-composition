# Real evidence and exact authorized scope

Classification: **LABORATORY_VERIFIED / PARTIAL_CHAIN_VERIFIED**.

The positive chain reuses the original preserved `evidence/v2/capture/a` native
proof, exact input/weights/output/model bytes, v4 EIP-712 assertions, and the #6
identity receipt and review signatures. The RVR receipt already commits the proof
bytes actually replayed by the native verifier; no positive artifact is regenerated.
The two labels remain `lab-subject-a` and `lab:preserved-native-proof-a`.

The pinned native adapter is built again against clean zkIE
`39d8df96877bc3bebf33c69b06907d792b3184b9`, using Rust 1.97.1 and locked Cargo
dependencies. Two exact Rust roundtrip tests execute. Separately, actual retained
proof verification runs over the declared input/weights/output/proof files. The
native verifier's statement and output checks are recorded in raw subprocess logs.
Upstream test success alone is not treated as proof verification.

This is the pinned public MatMul research statement, not verification of an entire
deployed LLM or private-input inference service. Proof A SHA-256 is
`87da845a2fe2c4768d0ec47926d6c5b6a88cf10149f0ac291033b034dc364530`;
proof B SHA-256 is
`88a6e1949678eaeff228e60b598716f5a6acd2314f9b79bbfe69b354f0477dcf`.
The native profile's signed proof commitment uses its original Keccak convention;
the RVR edge separately recomputes SHA-256 of the exact bytes. These digests are not
silently treated as interchangeable.
The adapter executes `verify_shard` on the deserialized retained proof, then separately
recomputes the public 4x8x8 MatMul output and checks all statement evaluations. The
historical fixture's public XorShift seed is not production cryptographic randomness.
The reported guarantee is this pinned native verification plus exact public replay;
it is not a general proof-system soundness or zero-knowledge claim.

EIP-712 assertions are recovered by the Node/noble implementation and independently
by Python eth-account. These are real signatures with laboratory provenance; no
observed on-chain transaction or independent organization is implied.

The distinct-proof negative witness uses preserved proof B and two newly generated
laboratory signatures. Ephemeral private keys existed only in memory. The fixture
declares this producer and its non-external origin. Frozen Core creates a new
identity receipt for that counterexample; original receipts remain unchanged. Its
purpose is to make both component checks valid while the cross-proof edge fails.
A second explicitly laboratory control signs a review contract omitting its authority
obligation, using proof A. It checks that an unchanged claim-type name cannot conceal
a weakened semantic contract. This control creates no external execution observation.

The existing v3 externally published signatures and ReceiptOS records remain
preserved and undergo regression tests. They do not supply the missing bindings
to this particular proof/review pair. An external artifact cannot be repurposed as
an execution observation for an unrelated claim.

Missing links for FULL_CHAIN_VERIFIED:

- Externally observed WYRIWE admission of these exact original bytes and transform.
- Authorized deployed model identity and inference statement linked to that admission.
- An external authenticated judgment binding this particular inference and action.
- Independent evidence that the claimed external execution actually occurred.
- An authority policy establishing real-world controller independence, if requested.

Executable acquisition/replay plan: preserve each original byte artifact with its
producer/source commit and SHA-256; add a separate candidate fixture without editing
existing artifacts; specify the exact signed subject/domain/action and native public
statement; extend the independent scenario contract only with reviewed interfaces;
run `python -B tools/integration/validate.py` plus positive, substitution, missing and
single-check mutation controls for each new edge. A failing or missing edge continues
to refuse authorization. No remote capture, transaction or researcher contact is
performed by this integration task.
