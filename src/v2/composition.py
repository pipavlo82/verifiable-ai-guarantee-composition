"""Explicit, fail-closed laboratory composition; no historical execution inference.

Caller supplies the trusted claim and policy independently of evidence. Never trust a
producer's 'verified' flag. Native zkIE and ECDSA verification are subprocess operations.
"""
import base64, hashlib, json, os, subprocess
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CAP=ROOT/'evidence/v2/capture'
PIN='39d8df96877bc3bebf33c69b06907d792b3184b9'
class Status(str,Enum):
    VERIFIED='VERIFIED'
    REFUTED='REFUTED'
    UNVERIFIABLE='UNVERIFIABLE'
@dataclass(frozen=True)
class Obligation:
    name:str
    status:Status
    reason:str
def combine(statuses):
    values=list(statuses)
    if Status.REFUTED in values:return Status.REFUTED
    if not values or Status.UNVERIFIABLE in values:return Status.UNVERIFIABLE
    return Status.VERIFIED
def check(value):
    return Status.UNVERIFIABLE if value is None else Status.VERIFIED if value else Status.REFUTED
def read_json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError,ValueError,TypeError):return None
def native_path():
    return ROOT/'build/chain-v2/cargo-target/debug'/('composition-native-capture.exe' if os.name=='nt' else 'composition-native-capture')
def base_case():
    files={k:str(CAP/'a'/v) for k,v in {'raw_input':'raw-input.bin','input':'input.bin','weights':'weights.bin','output':'output.bin','proof':'proof.bin','model':'model.json','result':'delivered.bin','observation':'execution-observation.json'}.items()}
    return {'files':files,'documents':{role:read_json(CAP/'a'/f'{role}.json') for role in ('provenance','judgment','receipt')},'claim':read_json(CAP/'a/claim.json'),'consumed_nonces':[]}
def verify(case,policy_path=CAP/'policy.json',component_only=False):
    policy=read_json(policy_path)
    if policy is None:return {'status':'UNVERIFIABLE','authorized':False,'reason':'trusted policy unavailable'}
    files=case['files']; docs=case['documents']; claim=case['claim']
    payload={}
    for key,p in {**files,'policy':str(policy_path)}.items():
        try:payload[key]=Path(p).read_bytes()
        except (OSError,TypeError):pass
    request={'documents':docs,'bytes':{k:base64.b64encode(v).decode() for k,v in payload.items()}}
    try:
        crypto_run=subprocess.run(['node',str(ROOT/'src/v2/crypto.mjs')],input=json.dumps(request).encode(),capture_output=True,timeout=30)
        crypto=json.loads(crypto_run.stdout) if crypto_run.returncode==0 else {}
        if not all(crypto.get('known_answers',{}).values()) or len(crypto.get('known_answers',{}))!=2:crypto={}
    except (OSError,ValueError,subprocess.TimeoutExpired):crypto={}
    hashes=crypto.get('hashes',{})
    obligations=[]
    def add(name,value,reason):obligations.append(Obligation(name,check(value),reason))
    components={}
    for role in ('provenance','judgment','receipt'):
        components[role]=crypto.get('signatures',{}).get(role,{'status':'UNVERIFIABLE'})['status']
        obligations.append(Obligation(role+'_signature',Status(components[role]),'ECDSA verification of this artifact, not truth or authorization'))
    native_status=Status.UNVERIFIABLE
    native_detail={}
    if all(k in payload for k in ('input','weights','output','proof')):
        try:
            run=subprocess.run([str(native_path()),'verify',*[str(files[k]) for k in ('input','weights','output','proof')]],capture_output=True,timeout=60)
            native_detail={'exit':run.returncode,'stdout':run.stdout.decode(errors='replace'),'stderr':run.stderr.decode(errors='replace')}
            if run.returncode in (0,1):
                value=json.loads(run.stdout)
                expected={'native_verified','output_recomputed','statement_bound'}
                if set(value)==expected and all(type(v) is bool for v in value.values()):native_status=check(run.returncode==0 and all(value.values()))
        except (OSError,ValueError,subprocess.TimeoutExpired):pass
    components['inference']=native_status.value
    obligations.append(Obligation('inference',native_status,'deserialized proof passed native verifier and full output recomputation'))
    if component_only:
        baseline=combine(Status(v) for v in components.values())
        return {'status':baseline.value,'authorized':baseline==Status.VERIFIED,'components':components}
    # Each named assignment below is an independent, source-mutated enforcement boundary.
    # Missing operands yield UNVERIFIABLE; never equate two missing digest values.
    def equal(values):
        known=[v for v in values if v is not None]
        if len(set(known))>1:return False
        return None if len(known)!=len(values) else True
    def msg(role,key):return (docs.get(role) or {}).get('message',{}).get(key)
    def all_present(values):
        if False in values:return False
        return None if any(v is None for v in values) else all(values)
    raw_ok=all_present([equal([hashes.get('raw_input'),msg('provenance','rawInputHash')]),equal([hashes.get('raw_input'),hashes.get('input')]),equal([hashes.get('identity_pipeline'),msg('provenance','sanitizationPipelineHash')])])
    add('provenance_preimage',raw_ok,'exact retained raw bytes and identity transform commitment')
    input_ok=equal([claim.get('inputHash'),hashes.get('input'),msg('provenance','inputHash'),msg('judgment','inputHash'),msg('receipt','inputHash')])
    add('input_binding',input_ok,'claim, provenance, native tensor, judgment and receipt consume identical bytes')
    model=read_json(files.get('model'))
    model_ok=all_present([equal([claim.get('modelHash'),hashes.get('model'),policy.get('modelHash'),msg('provenance','modelHash'),msg('judgment','modelHash'),msg('receipt','modelHash')]),None if model is None or 'weights' not in payload else model.get('zkie_commit')==PIN and model.get('shape')==[4,8,8] and model.get('operator')=='MatMul' and model.get('field')==18446744069414584321 and model.get('encoding')=='canonical-u64-little-endian' and model.get('weights_sha256')==hashlib.sha256(payload['weights']).hexdigest()])
    add('model_binding',model_ok,'pinned model bytes, weights, operator and upstream revision')
    subject_ok=equal([claim.get('subject'),msg('judgment','subject'),msg('receipt','subject')])
    add('subject_binding',subject_ok,'declared local subject; no external identity registry claim')
    proof_ok=equal([claim.get('proofHash'),hashes.get('proof'),msg('judgment','proofHash'),msg('receipt','proofHash')])
    add('proof_binding',proof_ok,'judgment and receipt reference the exact native proof bytes')
    action_ok=equal([claim.get('action'),policy.get('action'),msg('judgment','action'),msg('receipt','action')])
    add('action_binding',action_ok,'valid judgment must concern the authorized action')
    authority_ok=all_present([None if docs.get(role) is None else docs[role].get('signer')==policy['authorized'].get(role) for role in ('provenance','judgment','receipt')])
    add('authority',authority_ok,'role-specific keys supplied by the relying party lab policy')
    execution_ok=equal([claim.get('executionId'),msg('judgment','executionId'),msg('receipt','executionId')])
    add('execution_binding',execution_ok,'receipt must name the requested execution; identity equality does not prove occurrence')
    output_ok=equal([claim.get('outputHash'),hashes.get('output'),msg('provenance','outputHash'),msg('judgment','outputHash'),msg('receipt','outputHash')])
    add('output_binding',output_ok,'exact recomputed output statement across artifacts')
    result_ok=all_present([equal([hashes.get('result'),hashes.get('output'),msg('receipt','resultHash')]),equal([hashes.get('observation'),msg('receipt','observationHash')])])
    add('receipt_evidence',result_ok,'preserved result and observation bytes, not a proof of historical execution')
    domain_ok=all_present([None if docs.get(role) is None else docs[role].get('domain')==policy.get('domain') for role in ('provenance','judgment','receipt')])
    add('domain',domain_ok,'offline chain domain equality; no RPC or on-chain event is inferred')
    scope_ok=equal([claim.get('scope'),policy.get('scope'),msg('judgment','scope'),msg('receipt','scope')])
    add('scope',scope_ok,'only the public MatMul recomputation claim is permitted')
    policy_ok=equal([claim.get('policyHash'),hashes.get('policy'),msg('judgment','policyHash'),msg('receipt','policyHash')])
    add('policy_binding',policy_ok,'signed policy hash must match the independently selected policy bytes')
    replay_ok=all_present([equal([claim.get('nonce'),msg('judgment','nonce'),msg('receipt','nonce')]),None if 'consumed_nonces' not in case else claim.get('nonce') not in case['consumed_nonces']])
    add('replay',replay_ok,'caller-provided consumed-nonce snapshot; not durable on-chain replay protection')
    profile_ok=all_present([None if docs.get(role) is None else docs[role].get('type')==expected for role,expected in [('provenance','WyriweAttestation'),('judgment','LabJudgment'),('receipt','LabReceipt')]])
    add('artifact_types',profile_ok,'laboratory schemas are explicit; no upstream judgment or ReceiptOS conformance claim')
    historical_ok=True if claim.get('claimKind')=='recompute-output' else None
    add('claim_strength',historical_ok,'external admission, historical execution, chain origin and task completion lack independent evidence')
    status=combine(o.status for o in obligations)
    baseline=combine(Status(v) for v in components.values())
    return {'status':status.value,'authorized':status==Status.VERIFIED,'baseline_status':baseline.value,'baseline_authorized':baseline==Status.VERIFIED,'components':components,'obligations':[asdict(o) for o in obligations],'native':native_detail,'crypto':crypto,'claim_kind':claim.get('claimKind')}
