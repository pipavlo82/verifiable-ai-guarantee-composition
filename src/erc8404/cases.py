"""Predeclared witness classifications; no verdict-derived expectations."""
import base64
import copy
import json
from src.erc8404.engine import ROOT, canonical, sha, V, R, U

def base(family='independent'):
    c=json.loads((ROOT/f'fixtures/erc8404/lab/{family}.json').read_bytes())
    c['bundle_bytes']=base64.b64encode((ROOT/'fixtures/erc8404/rvr-bundle.json').read_bytes()).decode()
    c['receipt_bytes']=base64.b64encode((ROOT/'fixtures/erc8404/receipt.json').read_bytes()).decode()
    return c

def changed_contract(c, **updates):
    d=copy.deepcopy(c['contract']);d.update(updates)
    c['contract_bytes']=base64.b64encode(canonical(d)).decode()
    c['contract']=d

def cases():
    rows=[]
    def add(name,c,expected=R,kind='negative',target=None):
        rows.append(dict(name=name,case=c,expected=expected,kind=kind,target=target))
    add('independent',base(),V,'positive')
    add('self_allowed',base('self_allowed'),V,'positive')
    add('additional_role_independent',base('author_bound_independent'),V,'positive')
    c=base('list');c['claim']['outputHash']='0x'+'ff'*32
    add('list_false_output_excluded',c,V,'positive')
    add('self_judgment',base('self'),target='O14')
    add('additional_role_collision',base('author_bound_collision'),target='O14')
    c=base('author_bound_independent');c['documents']['author']=c['variants']['unbound_author'];add('additional_role_substitution',c,target='O14')
    add('unsupported_contract_claim',base('unsupported_claim'),target='supported_contract')
    add('incomparable_identities',base('incomparable'),U,target='O14')
    add('missing_required_role_identity',base('missing_role'),U,target='O14')
    c=base('statement_scope');c['documents']['judgment']=c['variants']['wrong_scope'];add('signed_scope_mismatch',c,target='S06')
    c=base('self_allowed');c['documents']['judgment']=c['variants']['unauthorized'];add('unauthorized_without_separation',c,target='S04')
    for oid in base()['catalog']:
        c=base();c['catalog'].pop(oid)
        add('omitted_'+oid,c,target='coverage')
    c=base('self');c['catalog'].pop('O14');add('self_missing_O14',c,target='coverage')
    c=base();c['context']['contract_sha256']='ff'*32;add('wrong_contract_context',c,target='contract_commitment')
    c=base();c['contract_bytes']=None;add('missing_contract_preimage',c,U,target='contract_preimage')
    for field,target,value in [('scenario','scenario','other-scenario'),('claimType','claim_type','EXTERNAL_TASK_SUCCESS'),('scope','scope','successful-execution')]:
        c=base();c['claim'][field]=value;add('wrong_'+target,c,target=target)
    c=base();c['claim']['outputHash']='0x'+'ff'*32;add('false_output_replay_only',c,target='field_policy')
    c=base();c['claim']['paymentAuthorized']=True;add('unconsumed_payment',c,target='field_policy')
    for variant,target in [('wrong_artifact','S02'),('wrong_subject','S03'),('wrong_action','S06'),('wrong_contract','signed_contract'),('unauthorized','S04')]:
        c=base();c['documents']['judgment']=c['variants'][variant];add(variant,c,target=target)
    c=base();c['catalog']['O14']={'procedure':'signature','dependencies':[]};add('counterfeit_O14',c,target='definitions')
    c=base('self');c['catalog']['O14']={'procedure':'signature','dependencies':[]};add('self_counterfeit_O14',c,target='definitions')
    c=base();c['documents']['judgment']=None;add('missing_judgment',c,U)
    c=base();c['documents']['producer']=None;add('missing_producer_identity',c,U)
    c=base();c['documents']['judgment']['signature']='0x'+'00'*65;add('invalid_signature',c)
    c=base();c['documents']['judgment']['domain']['chainId']='1';add('cross_domain',c)
    c=base();bundle=json.loads(base64.b64decode(c['bundle_bytes']));bundle['payloadsBase64']={};c['bundle_bytes']=base64.b64encode(canonical(bundle)).decode();add('missing_committed_payload',c,U)
    c=base();receipt=json.loads(base64.b64decode(c['receipt_bytes']));receipt['outcome']='REFUTED';c['receipt_bytes']=base64.b64encode(canonical(receipt)).decode();add('contradictory_receipt_projection',c,target='receipt')
    c=base();c['receipt_bytes']=base64.b64encode(b'{}').decode();add('malformed_receipt',c)
    c=base();c['contract_bytes']=base64.b64encode(b'{"schema":"a","schema":"b"}').decode();add('duplicate_contract_key',c)
    c=base();c['contract_bytes']=base64.b64encode(b'{"number":1}').decode();add('forbidden_contract_number',c)
    c=base();c['contract_bytes']=base64.b64encode(b' '+base64.b64decode(c['contract_bytes'])).decode();add('noncanonical_contract',c)
    c=base();c['documents']['producer']=None;c['claim']['scope']='excess';add('mixed_missing_and_refuted',c)
    return rows
