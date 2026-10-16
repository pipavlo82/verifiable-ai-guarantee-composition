"""Synthetic composition experiment. No cryptographic proof/signature adapters."""
import hashlib
import json

VERIFIED = "VERIFIED"
REFUTED = "REFUTED"
UNVERIFIABLE = "UNVERIFIABLE"
ROLES = ("provenance", "model", "proof", "judgment", "receipt")
GUARANTEES = tuple(f"G{i}" for i in range(1, 9))


def canonical(value):
    """Experiment JSON profile: ASCII keys/strings, integers, no floats. Not JCS."""
    def admit(x):
        if x is None or type(x) in (bool, int):
            return
        if type(x) is str and x.isascii():
            return
        if type(x) is list:
            for item in x:
                admit(item)
            return
        if type(x) is dict and all(type(k) is str and k.isascii() for k in x):
            for item in x.values():
                admit(item)
            return
        raise ValueError("Unsupported synthetic canonical value")
    admit(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def input_digest(value):
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def sealed(body):
    # Publicly recomputable checksum, NOT a signature or authenticity proof.
    return {"body": body, "fixture_checksum": digest(body)}


def load(path):
    def pairs(items):
        out = {}
        for key, val in items:
            if key in out:
                raise ValueError("Duplicate JSON key")
            out[key] = val
        return out
    with open(path, encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))
    canonical(value)
    return value


def verdict(condition, reason):
    return {"status": VERIFIED if condition else REFUTED,
            "reason": "CHECK_SATISFIED" if condition else reason}


def unknown(reason):
    return {"status": UNVERIFIABLE, "reason": reason}


def combine(results):
    statuses = [r["status"] for r in results]
    if REFUTED in statuses:
        return REFUTED
    if not statuses or UNVERIFIABLE in statuses:
        return UNVERIFIABLE
    return VERIFIED


def component(role, envelope):
    if envelope is None:
        return unknown("EVIDENCE_MISSING")
    if set(envelope) != {"body", "fixture_checksum"}:
        return unknown("UNSUPPORTED_ENVELOPE")
    b = envelope["body"]
    if b["mechanism"] != "synthetic-checksum-v0" or b["role"] != role:
        return unknown("UNSUPPORTED_COMPONENT")
    if digest(b) != envelope["fixture_checksum"]:
        return verdict(False, "CHECKSUM_MISMATCH")
    p = b["payload"]
    if role == "provenance":
        if type(p["input"]) is not int:
            return unknown("INPUT_TYPE_UNSUPPORTED")
        return verdict(p["raw"] == str(p["input"]) and p["transform"] == "identity-v0"
                       and p["input_digest"] == input_digest(p["input"]), "PROVENANCE_INTERNAL_MISMATCH")
    if role == "model":
        if type(p["version"]) is not int:
            return unknown("MODEL_VERSION_TYPE_UNSUPPORTED")
        return verdict(p == {"id": "square", "version": 1, "operation": "x*x"}, "MODEL_UNSUPPORTED")
    if role == "proof":
        if type(p["input"]) is not int or type(p["output"]) is not int or type(p["version"]) is not int:
            return unknown("WITNESS_TYPE_UNSUPPORTED")
        return verdict(p["input_digest"] == input_digest(p["input"])
                       and p["output"] == p["input"] * p["input"], "ARITHMETIC_MISMATCH")
    if role == "judgment":
        return verdict(p["verdict"] == "approve", "JUDGMENT_NOT_APPROVAL")
    if type(p["output"]) is not int:
        return unknown("RECEIPT_OUTPUT_TYPE_UNSUPPORTED")
    return verdict(p["completed"] == "recorded", "RECEIPT_NOT_RECORDED")


def g1(e, r, p):
    return verdict(e["provenance"]["payload"]["input_digest"] == r["input_digest"], "G1_REQUEST_INPUT_MISMATCH")  # MUTATE:G1


def g2(e, r, p):
    model = e["model"]["payload"]
    proof = e["proof"]["payload"]
    return verdict((model["id"], model["version"]) == (r["model"], r["version"]) == (proof["model"], proof["version"]), "G2_MODEL_VERSION_MISMATCH")  # MUTATE:G2


def g3(e, r, p):
    proof = e["proof"]["payload"]
    return verdict(proof["input_digest"] == e["provenance"]["payload"]["input_digest"] and proof["output"] == r["output"], "G3_PROOF_STATEMENT_MISMATCH")  # MUTATE:G3


def g4(e, r, p):
    return verdict(all(b["subject"] == r["subject"] for b in e.values()), "G4_SUBJECT_MISMATCH")  # MUTATE:G4


def g5(e, r, p):
    j = e["judgment"]
    # Pinned public fixture catalog models a trusted authenticity oracle. No signatures.
    return verdict(digest(j) in p["authentic_judgments"].get(j["issuer"], []), "G5_FIXTURE_AUTHENTICITY_MISMATCH")  # MUTATE:G5


def g6(e, r, p):
    j = e["judgment"]
    return verdict(j["issuer"] in p["authorized_judges"] and j["payload"]["action"] == r["action"] and j["payload"]["policy"] == p["id"], "G6_JUDGMENT_NOT_AUTHORIZED")  # MUTATE:G6


def g7(e, r, p):
    receipt = e["receipt"]["payload"]
    return verdict(receipt["execution"] == r["execution"] and receipt["action"] == r["action"] and receipt["output"] == r["output"] and receipt["proof_digest"] == digest(e["proof"]), "G7_EXECUTION_BINDING_MISMATCH")  # MUTATE:G7


def g8(e, r, p):
    # All eight guarantees are mandatory; producer-supplied dependency lists cannot remove them.
    scope_ok = bool(r["scope"]) and r["action"] in r["scope"] and all(set(r["scope"]) <= set(b["scope"]) for b in e.values())
    strength_ok = r["strength"] == "SYNTHETIC" and all(b["strength"] == "SYNTHETIC" for b in e.values())
    domain_ok = r["domain"] == p["domain"] and all(b["domain"] == r["domain"] for b in e.values())
    time_ok = type(r["time"]) is int and all(b["not_before"] <= r["time"] < b["not_after"] for b in e.values())
    return verdict(scope_ok and strength_ok and domain_ok and time_ok and r["nonce"] not in p["consumed_nonces"] and r["policy"] == p["id"], "G8_SCOPE_STRENGTH_REPLAY_OR_POLICY")  # MUTATE:G8


NEEDS = {"G1": ("provenance",), "G2": ("model", "proof"), "G3": ("proof", "provenance"),
         "G4": ROLES, "G5": ("judgment",), "G6": ("judgment",), "G7": ("receipt", "proof"), "G8": ROLES}


def evaluate(packet, policy, baseline=False):
    """The caller selects the request and trusted policy. Evidence is untrusted.

    baseline=True runs identical component checks (including the fixture authenticity
    oracle), but intentionally ignores composition edges. It is a weak research baseline,
    not a model of any named upstream verifier. This API never authorizes real actions.
    """
    mode = packet.get("mode") if type(packet) is dict else None
    report = {"schema": "composition-report-v0", "mode": mode,
              "method": "independent" if baseline else "composition", "real_crypto_verified": False,
              "components": {}, "guarantees": {}, "status": UNVERIFIABLE}
    if mode != "synthetic":
        report["reason"] = "REAL_ARTIFACT_INTEGRATION_NOT_IMPLEMENTED"
        return report
    try:
        canonical(packet)
        canonical(policy)
        if packet["schema"] != "composition-fixture-v0" or policy["id"] != "composition-policy-v0":
            raise ValueError("Unknown schema/policy")
        req, evidence = packet["request"], packet["evidence"]
        # Exact scalar types avoid Python's True == 1 and other ambiguous comparisons.
        if type(req["version"]) is not int or type(req["output"]) is not int:
            raise ValueError("Invalid scalar type")
        for key in ("subject", "input_digest", "model", "action", "execution", "strength", "domain", "nonce", "policy"):
            if type(req[key]) is not str or not req[key]:
                raise ValueError("Invalid request string")
        if type(req["scope"]) is not list or any(type(x) is not str for x in req["scope"]):
            raise ValueError("Invalid scope")
        for item in evidence.values():
            if item is not None:
                body = item["body"]
                if type(body["scope"]) is not list or any(type(x) is not str for x in body["scope"]):
                    raise ValueError("Invalid scope")
                if type(body["not_before"]) is not int or type(body["not_after"]) is not int:
                    raise ValueError("Invalid time")
        for role in ROLES:
            report["components"][role] = component(role, evidence.get(role))
        bodies = {role: item["body"] for role, item in evidence.items() if role in ROLES and item is not None}
        for gid in (("G5",) if baseline else GUARANTEES):
            deps = [report["components"][role] for role in NEEDS[gid]]
            dep_status = combine(deps)
            if dep_status != VERIFIED:
                report["guarantees"][gid] = {"status": dep_status, "reason": "COMPONENT_DEPENDENCY_" + dep_status}
            else:
                report["guarantees"][gid] = globals()[gid.lower()](bodies, req, policy)
        if not baseline:
            # G8 authorization also depends on every G1-G7 premise; local context is insufficient.
            overall_g8 = combine(report["guarantees"].values())
            if overall_g8 != report["guarantees"]["G8"]["status"]:
                report["guarantees"]["G8"] = {"status": overall_g8, "reason": "GUARANTEE_DEPENDENCY_" + overall_g8}
        # G5's fixture authenticity lookup is part of both strategies.
        required = list(report["components"].values()) + [report["guarantees"]["G5"]]
        if not baseline:
            required += list(report["guarantees"].values())
        report["status"] = combine(required)
        report["reason"] = "SYNTHETIC_POLICY_EVALUATION_ONLY"
    except (KeyError, TypeError, ValueError, AttributeError, OverflowError):
        report["status"] = UNVERIFIABLE
        report["reason"] = "MALFORMED_OR_UNSUPPORTED_EVIDENCE"
    return report
