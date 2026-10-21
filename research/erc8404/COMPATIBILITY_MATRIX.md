# Compatibility matrix

| Requested property | Existing Core support | External consumer binding | Classification |
|---|---|---|---|
| Exact RVR claim | claimDigest over canonical claim | Recompute exact preimage | Directly supported |
| Evidence set | evidenceSetDigest over normalized descriptor, raw member pins | Resolve exact bytes and lengths | Directly supported |
| Verification profile | verificationProfileDigest over canonical profile and closure | Select the exact supported profile | Directly supported |
| Verification result | resultDigest and checked outcome/reason projections | Re-execute procedure; preserve both axes | Directly supported |
| Broader requested claim | Only fields actually in the selected claim preimage | Bind artifact hash, subject, claim type and scope separately | External binding |
| Scenario contract | No universal scenario-contract member | Canonical contract bytes, SHA-256, trusted relying context and signed policyHash | External binding |
| Authorized scope | Profile defines its proposition; no universal action permission | Exact scenario/type/contract/consumed fields in local decision | External binding |
| Checker role separation | No universal independent-checker requirement | Scenario-dependent O14, authenticated identities, explicit role policy | External binding |
| Unconsumed fields | No general application claim-field policy | REJECT or LIST with exact excluded fields | External binding |
| Adequacy/completeness of the scenario contract | Not established by hashing/reproduction | Explicit external assumption, independent policy review required | Unsupported by this experiment |
| Real organizational independence | Distinct signing keys do not establish it | Would require additional authority/evidence policy | Unsupported |
| External execution / judgment truth / inference correctness | Not established by this SHA256_EQUALS profile | Separate genuine evidence and verification relations required | Unsupported |
| New scope/contract field inside the old receipt | Receipt forbids additional fields | Keep an external decision object instead | Core change would be incompatible |
| Reinterpret resultDigest as receipt digest | resultDigest addresses canonical result | Separately hash exact receipt bytes for the external record | Core change would be incompatible |
| Treat CANNOT_RECOMPUTE as a Core semantic outcome | Explicitly forbidden | Consumer may refuse authorization, leaving Core output untouched | Core reinterpretation incompatible |

The supported route is an **external consumer**, not a newly certified RVR
Verification Profile. The consumer's source and fixtures are pinned by the
research artifact inventory. No new normative manifest, profile identifier or
old-profile conformance claim is fabricated. A future first-class RVR profile
would need its own specification, schema, canonical result, complete closure
and conformance suite with new content identities.

The preserved laboratory receipt establishes SHA-256 identity of the 380-byte
native proof artifact. It does not execute zkIE. Native proof verification is
reproduced separately in the historical v2-v4 suites; it is not implied by this
receipt's narrow proposition.
