"""Equality obligations under explicit assumptions; not an authorization verifier.

This module has no cryptographic verification API. Its finite model and typed
commitments are research objects, not zkIE/WYRIWE/ReceiptOS wire formats.
"""
import hashlib
import itertools
import json

GROUPS = {
    "input": ("requested_input", "provenance_input", "inference_input"),
    "model": ("requested_model", "provenance_model", "inference_model"),
    "action": ("requested_action", "judged_action", "executed_action"),
}
EDGES = {
    f"{dimension}.{pair}": (nodes[left], nodes[right])
    for dimension, nodes in GROUPS.items()
    for pair, left, right in (("RP", 0, 1), ("PI", 1, 2), ("RI", 0, 2))
}
NODES = tuple(node for group in GROUPS.values() for node in group)
TARGETS = tuple((nodes[0], other) for nodes in GROUPS.values() for other in nodes[1:])


def components(selected, native=()):
    chosen = set(selected) | set(native)
    if not chosen <= EDGES.keys():
        raise ValueError("Unknown obligation identifier")
    roots = {node: node for node in NODES}
    def root(node):
        while roots[node] != node:
            node = roots[node]
        return node
    for name in sorted(chosen):
        left, right = EDGES[name]
        roots[root(right)] = root(left)
    return {node: root(node) for node in NODES}


def entails(selected, native=()):
    groups = components(selected, native)
    return all(groups[left] == groups[right] for left, right in TARGETS)


def witness(selected, native=()):
    groups = components(selected, native)
    for left, right in TARGETS:
        if groups[left] != groups[right]:
            return {node: int(groups[node] == groups[right]) for node in NODES}
    return None


def satisfies_edges(assignment, selected):
    return all(assignment[EDGES[name][0]] == assignment[EDGES[name][1]] for name in selected)


def target_semantics(assignment):
    # Separate oracle: direct three-way equality, no use of graph closure.
    return all(assignment[a] == assignment[b] == assignment[c] for a, b, c in GROUPS.values())


def compare_commitments(left, right):
    """A narrow research relation. Algorithm+representation labels are mandatory.

    Caller-authenticated labels are an assumption; this does not authenticate them.
    A missing bridge between unlike representations is unknown, not a refutation.
    """
    if type(left) is not dict or type(right) is not dict:
        return "UNVERIFIABLE"
    required = {"algorithm", "representation", "digest"}
    if set(left) != required or set(right) != required:
        return "UNVERIFIABLE"
    for item in (left, right):
        if type(item["algorithm"]) is not str or item["algorithm"] not in {"sha256", "keccak256"} or type(item["representation"]) is not str or not item["representation"]:
            return "UNVERIFIABLE"
        if type(item["digest"]) is not str or len(item["digest"]) != 64 or any(c not in "0123456789abcdef" for c in item["digest"]):
            return "UNVERIFIABLE"
    if (left["algorithm"], left["representation"]) != (right["algorithm"], right["representation"]):
        return "UNVERIFIABLE"
    return "VERIFIED" if left["digest"] == right["digest"] else "REFUTED"


def analyze(native=()):
    native = frozenset(native)
    if not native <= EDGES.keys():
        raise ValueError("Unknown native premise")
    candidates = tuple(sorted(set(EDGES) - native))
    assignments = [dict(zip(NODES, values)) for values in itertools.product((0, 1), repeat=len(NODES))]
    compatible = [a for a in assignments if satisfies_edges(a, native)]
    # Compact bit masks for the independent exhaustive oracle.
    semantic_rows = [(sum(1 << i for i, e in enumerate(candidates) if satisfies_edges(a, [e])), target_semantics(a)) for a in compatible]
    sufficient = []
    certificates = []
    evaluations = 0
    for mask in range(1 << len(candidates)):
        chosen = frozenset(e for i, e in enumerate(candidates) if mask & (1 << i))
        graph_result = entails(chosen, native)
        oracle = True
        # Do not short-circuit: count every audited assignment/subset pair.
        for satisfied_mask, target in semantic_rows:
            if mask & satisfied_mask == mask and not target:
                oracle = False
            evaluations += 1
        if graph_result != oracle:
            raise RuntimeError("Graph closure disagrees with exhaustive semantics")
        if graph_result:
            sufficient.append(chosen)
        else:
            assignment = witness(chosen, native)
            if assignment is None or not satisfies_edges(assignment, chosen | native) or target_semantics(assignment):
                raise RuntimeError("Invalid necessity witness")
    minimal = [s for s in sufficient if not any(entails(s - {edge}, native) for edge in s)]
    for basis in minimal:
        for edge in sorted(basis):
            reduced = basis - {edge}
            assignment = witness(reduced, native)
            if not satisfies_edges(assignment, reduced | native) or target_semantics(assignment):
                raise RuntimeError("Removed obligation has no semantic counterexample")
            certificates.append({"basis": sorted(basis), "removed": edge, "countermodel": assignment})
    return {"native_premises": sorted(native), "candidate_edges": len(candidates), "subsets": 1 << len(candidates),
            "assignments": len(compatible), "oracle_evaluations": evaluations, "sufficient_sets": len(sufficient),
            "inclusion_minimal_bases": [sorted(s) for s in sorted(minimal, key=lambda s: tuple(sorted(s)))],
            "minimum_cardinality": min(map(len, sufficient)), "removal_countermodels": certificates,
            "all_observed_minimal_bases_are_minimum": len({len(s) for s in minimal}) == 1}


def run():
    # Equal normalized values cannot establish byte identity: normalization is not injective.
    left, right = b"3", b"003"
    return {"schema": "composition-obligation-analysis-v1", "mode": "ABSTRACT_EQUALITY_MODEL",
            "cryptographic_verification": "NOT_PERFORMED", "downstream_authorization": "NOT_ESTABLISHED",
            "hypotheses": ["sound native verifiers", "trusted caller policy and authority", "verified representation bridges", "applicable scope/time/replay checks", "authenticated subject and execution linkage"],
            "without_cross_component_native_equalities": analyze(),
            "conditional_on_one_additional_verified_equality": analyze(["model.PI"]),
            "noninjective_translation_counterexample": {"left_hex": left.hex(), "right_hex": right.hex(),
                "normalized_equal": int(left) == int(right), "raw_equal": left == right,
                "left_sha256": hashlib.sha256(left).hexdigest(), "right_sha256": hashlib.sha256(right).hexdigest()},
            "novelty": "Application-specific candidate; no priority claim for equality closure, graph minimality or assume-guarantee reasoning."}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(newline="\n")
    print(json.dumps(run(), sort_keys=True, indent=2))
