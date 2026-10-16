# Threat model

The synthetic adversary selects, substitutes, omits or changes evidence envelopes, including records that are internally correct. It can recompute all public checksums. It can attach authentic cataloged judgments about another action, or judgments by a known but unauthorized issuer. It can ask for broader scope, unsupported assurance, another domain, an expired time or a consumed nonce.

The verifier independently selects the request and the trusted policy file. The adversary does not replace policy, the catalog, source code or the fixed oracle labels. If the caller lets a producer select policy, this model's assumptions fail. Catalog entries are a synthetic oracle, not secret signing keys or proof of authorship.

Trust boundaries: raw input to provenance; provenance/model to inference; component subjects to requested subject; judgment body to authentic issuer; authentic judgment to authorized action; receipt to proof and execution; all dependencies to the downstream request. Replay state is a supplied snapshot in policy, not a durable transactional database.

The verifier has no protected external effect. Authorization in measurements means returning VERIFIED under the synthetic policy. It never sends a transaction, moves assets or executes a requested action.

Out of scope: cryptanalysis, key custody, live chain consensus/finality, execution-host compromise, malicious Python runtime, denial of service, concurrent replay races, unobserved external actions, model quality, judgment soundness, and proof-system security. Source review is bounded inspection; upstream test suites and deployments were not audited or executed.
