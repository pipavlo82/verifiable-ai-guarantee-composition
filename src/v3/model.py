"""Typed claim-specific obligations over actual verification and explicit caller policy.

The graph is an AND dependency graph, not a theorem prover or a deployment policy.
No caller-supplied status is admitted as cryptographic evidence.
"""
import json
from dataclasses import asdict,dataclass
from src.v3.evidence import ROOT,base_case,canonical,cryptography,native,receipt,sha
V='VERIFIED';R='REFUTED';U='UNVERIFIABLE'
@dataclass(frozen=True)
class Guarantee:
    id:str
    subject:str
    scope:str
    authority:str
    evidence:str
    assumptions:tuple
    dependencies:tuple
    verification_contract:str
    permitted_claims:tuple
CLAIMS={
 'judgment_publication':('judgment_signature','judgment_authority'),
 'claim_agreement':('judgment_signature','judgment_authority','cell1_signature','cell2_signature','cell_authority','decision_binding','claim_binding','judgment_scope','domain','as_of'),
 'native_recomputation':('native_proof','native_model'),
 'local_receipt_binding':('receipt_root','receipt_subject'),
 'historical_cell_execution':('claim_agreement','historical_input_bytes','historical_execution'),
 'external_full_chain':('claim_agreement','native_recomputation','local_receipt_binding','wyriwe_provenance','external_model_authority','inference_judgment_binding','external_execution'),
}
CONTRACTS={
 'judgment_signature':('NIP-01 event','authentic publication','BIP-340 public key','exact live ledger proof_event','recompute id and verify BIP-340'),
 'judgment_authority':('declared validator key','caller-selected acceptance','relying-party key policy','pinned expected issuer key','match the declared key; signature dependency authenticates it'),
 'cell1_signature':('Nostr CRC Cell','signed cell publication','BIP-340 public key','CC0 published node1 bytes','NIP-01 plus BIP-340'),
 'cell2_signature':('EIP-712 CRC Cell','signed cell publication','recovered secp256k1 key','CC0 published node2 bytes','recompute evidence hash and EIP-712 digest, recover signer'),
 'cell_authority':('two declared cell issuers','caller-selected acceptance','relying-party key policy','explicit expected keys','require both declared issuers match accepted keys'),
 'decision_binding':('judgment and requested decision','exact decision reference','signed source plus request','declared eight-field preimage','recompute decision reference and match both cells and request'),
 'claim_binding':('two cells and requested claim','same claim preimage','caller request','exact claim preimages','recompute both IDs and compare request'),
 'judgment_scope':('requested verdict','literal signed verdict only','caller request','signed source and cell claim bodies','match requested verdict and source policy/class; no judgment correctness'),
 'domain':('EIP-712 domain','declared off-chain domain','caller domain policy','signed domain name/version/chainId','exact domain equality; not live chain proof'),
 'as_of':('requested observation window','literal signed as_of equality','caller time context','cell and claim preimage as_of','exact match; no trusted clock or durable replay service'),
 'native_proof':('retained MatMul tuple','public arithmetic recomputation','pinned native verifier','v2 exact input/weights/output/proof','run Rust verifier and recompute output'),
 'native_model':('model manifest','explicit pinned model selection','caller model policy','v2 model.json bytes','SHA-256 equality; no external model approval'),
 'receipt_root':('local observer receipt','integrity only','ReceiptOS native root verifier','actual preserved subprocess receipt','run pinned ReceiptOS/Crystal plus independent Python root recomputation'),
 'receipt_subject':('requested replay subject','exact proof digest','caller request','receipt subject.proof_sha256','match requested proof digest; no historical truth inference'),
 'historical_input_bytes':('original #236 capture','historical exact-byte admission','external capture observer','6cb8... source bytes absent','UNVERIFIABLE until exact signed input commitment opens'),
 'historical_execution':('CRC producer execution','producer actually ran stated code','independent execution observer','only reference hashes are available','UNVERIFIABLE; a signed result is not execution evidence'),
 'wyriwe_provenance':('external input to native tuple','actual admitted bytes and transform','authorized external gateway','no compatible complete artifact','UNVERIFIABLE; bounded public search is not proof of global absence'),
 'external_model_authority':('model execution','authorized model/version','external policy owner','missing signed delegation/registry policy','UNVERIFIABLE; native mathematical validity is insufficient'),
 'inference_judgment_binding':('native proof and public judgment','same reviewed action/input','signed judgment contract','public judgment does not reference this native statement','UNVERIFIABLE; do not invent a linkage'),
 'external_execution':('action and resulting effect','actual external occurrence','independent mediation or settlement observer','outcome #236 HTTP404; no matching execution receipt','UNVERIFIABLE; absence is not refutation'),
}
GRAPH={name:Guarantee(name,*fields[:4],('verifier integrity','collision resistance','explicit scoped trust; no truth from signatures'),(),fields[4],tuple(c for c in CLAIMS if name in CLAIMS[c])) for name,fields in CONTRACTS.items()}
for name,deps in CLAIMS.items():GRAPH[name]=Guarantee(name,'caller requested subject',name,'caller policy','dependency closure',('all dependencies verified within their scopes',),deps,'conjunction with REFUTED precedence over UNVERIFIABLE',(name,))
def closure(claim):
    if claim not in CLAIMS:raise ValueError('Unknown claim; never infer a policy')
    found=[];visiting=set()
    def visit(name):
        if name in visiting:raise ValueError('dependency cycle')
        visiting.add(name)
        if GRAPH[name].dependencies:
            for dependency in GRAPH[name].dependencies:visit(dependency)
        elif name not in found:found.append(name)
        visiting.remove(name)
    visit(claim);return found
def join(statuses):return R if R in statuses else U if not statuses or U in statuses else V
def eq(values):
    known=[v for v in values if v is not None]
    if known and any(v!=known[0] for v in known):return R
    return U if not known or len(known)!=len(values) else V
def both(statuses):return join(statuses)
def policy():
    # These literal caller keys are accepted only for scoped publication claims.
    # Request expectations are independent constants, never derived from submitted evidence.
    return {'ledger_key':'6786e18a864893a900bd9858e650f67ccc3513f248fed374b591e2ff6922fbb7','cell1_key':'6786e18a864893a900bd9858e650f67ccc3513f248fed374b591e2ff6922fbb7','cell2_key':'0x85fa13511d170fbe173761b63d7f8dd4a6f6bf1a','domain':{'name':'cross-reference-console','version':'1','chainId':1},'decision_ref':'sha256:5bca0bf044c8e1c8e16a01bf3ee44b12c305ce6a50dd9789ff73cbd13482b9b9','claim_id':'sha256:df1a6bfe3063186f8a8327b75a5bfddae12d3518f2cc16f8fddbc6c311de9512','verdict':'reject','as_of':'2026-08-04T00:11:24Z','model_sha256':'a8645f4c909745d4e90df6bac9c929960e665ef48f1379d7f689c42245604b8c','proof_sha256':'87da845a2fe2c4768d0ec47926d6c5b6a88cf10149f0ac291033b034dc364530'}
FIELDS=('artifact_hash','artifact_type','policy_version','verdict','source_class','vantage_limitation','related_decision_ref','intended_audience')
def evaluate(case,request,claim='claim_agreement',component_only=False):
    required=closure(claim);raw={};details={}
    crypto_needed=any(x in required for x in ('judgment_signature','cell1_signature','cell2_signature'))
    crypto,execution=cryptography(case) if crypto_needed else ({},{})
    if component_only:
        components={k:crypto[v]['status'] for k,v in [('judgment_signature','ledger'),('cell1_signature','cell1'),('cell2_signature','cell2')] if k in required}
        if 'native_proof' in required:details['native']=native(case);components['native_proof']=details['native']['status']
        if 'receipt_root' in required:details['receipt']=receipt(case);components['receipt_root']=details['receipt']['status']
        status=join(list(components.values()))
        return {'claim':claim,'status':status,'authorized':status==V,'mode':'component_only','required':required,'components':components,'details':details,'guarantee_scope':'individual components only'}
    def event_content(doc,key):
        try:return json.loads(doc[key]['content'])
        except (TypeError,KeyError,ValueError):return {}
    j=event_content(case.get('ledger'),'proof_event');a=event_content(case.get('cell1'),'event');b=(case.get('cell2') or {}).get('proof_payload',{})
    ap=a.get('evidence',{}).get('claim_preimage');bp=b.get('evidence',{}).get('claim_preimage')
    for key in ('judgment_signature','cell1_signature','cell2_signature'):
        component={'judgment_signature':'ledger','cell1_signature':'cell1','cell2_signature':'cell2'}[key];raw[key]=crypto.get(component,{}).get('status',U)
    raw['judgment_authority']=both([eq([(case.get('ledger') or {}).get('proof_event',{}).get('pubkey'),request.get('ledger_key')]),eq([j.get('schema'),'invinoveritas.verdict_proof.v1'])])
    raw['cell_authority']=both([eq([(case.get('cell1') or {}).get('event',{}).get('pubkey'),request.get('cell1_key')]),eq([b.get('verifier','').lower() or None,request.get('cell2_key')]),eq([a.get('schema'),b.get('schema'),'crc.cell.v1'])])
    derived='sha256:'+sha(canonical({k:j.get(k) for k in FIELDS})) if j and j.get('decision_ref_preimage_fields')==list(FIELDS) else None
    raw['decision_binding']=eq([derived,j.get('decision_ref'),request.get('decision_ref'),('sha256:'+ap['artifact_hash']) if ap else None,('sha256:'+bp['artifact_hash']) if bp else None])
    raw['claim_binding']=eq([a.get('claim_id'),b.get('claim_id'),request.get('claim_id'),'sha256:'+sha(canonical(ap)) if ap else None,'sha256:'+sha(canonical(bp)) if bp else None])
    raw['judgment_scope']=both([eq([j.get('verdict'),ap.get('claim_body') if ap else None,bp.get('claim_body') if bp else None,request.get('verdict')]),eq([j.get('policy_version'),ap.get('policy_version') if ap else None,bp.get('policy_version') if bp else None]),eq([j.get('source_class'),ap.get('source_class') if ap else None,bp.get('source_class') if bp else None])])
    raw['domain']=eq([(case.get('cell2') or {}).get('signature',{}).get('domain'),request.get('domain')])
    raw['as_of']=eq([a.get('as_of'),b.get('as_of'),ap.get('as_of') if ap else None,bp.get('as_of') if bp else None,request.get('as_of')])
    if 'native_proof' in required:details['native']=native(case);raw['native_proof']=details['native']['status']
    raw['native_model']=eq([sha((ROOT/'evidence/v2/capture/a/model.json').read_bytes()),request.get('model_sha256')])
    if 'receipt_root' in required:details['receipt']=receipt(case);raw['receipt_root']=details['receipt']['status']
    raw['receipt_subject']=eq([(case.get('receipt') or {}).get('subject',{}).get('proof_sha256'),request.get('proof_sha256')])
    for key in CONTRACTS:raw.setdefault(key,U)
    # Individual enforcement sites are intentionally explicit for source-mutation controls.
    checks={}
    def enforce(name,value):checks[name]=value
    enforce('judgment_signature',raw['judgment_signature'])
    enforce('judgment_authority',raw['judgment_authority'])
    enforce('cell1_signature',raw['cell1_signature'])
    enforce('cell2_signature',raw['cell2_signature'])
    enforce('cell_authority',raw['cell_authority'])
    enforce('decision_binding',raw['decision_binding'])
    enforce('claim_binding',raw['claim_binding'])
    enforce('judgment_scope',raw['judgment_scope'])
    enforce('domain',raw['domain'])
    enforce('as_of',raw['as_of'])
    enforce('native_proof',raw['native_proof'])
    enforce('native_model',raw['native_model'])
    enforce('receipt_root',raw['receipt_root'])
    enforce('receipt_subject',raw['receipt_subject'])
    for key in required:checks.setdefault(key,U)
    components=[key for key in required if key in ('judgment_signature','cell1_signature','cell2_signature','native_proof','receipt_root')]
    selected=components if component_only else required
    status=join([checks[key] for key in selected])
    return {'claim':claim,'status':status,'authorized':status==V,'mode':'component_only' if component_only else 'explicit_composition','required':required,'components':{k:raw[k] for k in components},'obligations':{k:checks[k] for k in required},'additional_bindings':[k for k in required if k not in components],'missing':[k for k in required if checks[k]==U],'refuted':[k for k in required if checks[k]==R],'details':details,'crypto_execution':execution,'guarantee_scope':GRAPH[claim].scope}
def graph():return {k:asdict(v) for k,v in GRAPH.items()}
