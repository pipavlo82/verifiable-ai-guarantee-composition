# Semantic compatibility

| Boundary | PR #5 | PR #6 | Explicit integration rule |
|---|---|---|---|
| Claim type | LAB_OUTPUT_REPLAY_ADMISSIBLE and narrower lab profiles | REVIEWED_ARTIFACT_IDENTITY | A new external conjunction type; neither identifier is aliased |
| Contract | Parsed JSON, including numeric revision | Exact canonical bytes, numbers forbidden | Each original preimage rule is retained; joint contract separately uses number-free canonical bytes |
| SHA-256 | Compact sorted UTF-8 JSON object | Canonical bytes independently parsed and reserialized | Joint contract commits both distinct subprofile digests |
| Authority policy | Separate policy object/bytes, in addition to scenario contract | Authorized role keys are in contract preimage | Joint contract additionally commits exact PR5 policy bytes; policy substitution has its own isolated negative/mutation witness |
| Native proof | Actual Rust verification over input/weights/output/proof | RVR SHA256_EQUALS over proof bytes | Compare SHA-256 of the actually replayed proof bytes with the receipt claim |
| Subjects | lab-subject-a | lab:preserved-native-proof-a | Return both labels; no asserted entity equality |
| Judgment | Authenticated lab action/inference assertion | Authenticated artifact review assertion | Both remain within their signed statements |
| O14 | Recovered provenance/judgment keys differ if required | Policy-selected role pairs, namespace and authorities | DISTINCT_KEYS_IN_EACH_PROFILE requires O14 in each profile; SCENARIO_PROFILES delegates to each explicit policy |
| Controllers | Not established | Not established | Real-world controller independence returns UNVERIFIABLE |
| Unconsumed fields | Observed reads, not semantic proof | REJECT or LIST plus explicit field semantics | Joint semantic comparisons plus explicit rejection/listing of unknown nested fields; no read log is used as proof |
| Tri-state | REFUTED dominates UNVERIFIABLE | Same consumer aggregation; separate Core axes | Preserve each profile status; never promote missing evidence |
| Admission | Recompute C and compare | Recompute scoped record | Recompute whole joint decision; strict canonical comparison rejects bool/integer substitutions |

The profiles are composable for the narrow laboratory conjunction. They are not
interchangeable authorization credentials. A hash match only establishes identity
of bytes actually in the preimage. No signature authenticates the new joint contract;
the relying consumer selects it as local policy and recomputes its exact digest.

The PR5 documented read-tracking limitation is independently exercised by a
discarded-read source mutation in `tools/integration/read_tracking.py`. PR5 marks
the extra field consumed under that mutation. The joint consumer rejects and names
`inference.unchecked` even when that imported predicate has been mutated.

PR5 comparison equality treats Python `True` and `1` as equal. This does not create
authority for refuted evidence because its admission recomputes C. The joint
consumer nevertheless rejects numeric flags at its serialized boundary.

Malformed legacy contracts can raise exceptions in PR5. The external wrapper
classifies supported malformed evidence as REFUTED and never treats a crash as a
verified result. General hostile-resource limits and a production API are outside
this experiment.
