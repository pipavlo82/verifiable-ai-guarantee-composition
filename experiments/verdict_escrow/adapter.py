"""External laboratory policy adapter. No network, production keys or transactions.

The payer supplies the grant and an authenticated state snapshot. The unchanged
escrow does NOT execute this code or establish the authenticity of that snapshot.
"""
import base64,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).parent/'vendor/invinoveritas/examples/decision-receipt'))
import bip340
from src.integration import engine
V,R,U='VERIFIED','REFUTED','UNVERIFIABLE'
LABEL=b'claim-aware escrow v0 public deterministic laboratory key -- NEVER FUND'
LAB_KEY=hashlib.sha256(LABEL).digest()
LAB_PUB=bip340.pubkey(LAB_KEY).hex()
PROFILE=Path(__file__).parent/'profile.json'
FIELDS={'schema','claim_type','scenario','scope','scenario_contract_sha256','evidence_sha256','proof_sha256','verification_profile_sha256','authorization','intended_consumer','chain_id','escrow_contract','token','payment_id','job_id','recipient','amount','nonce','expires_at'}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return engine.canonical(x)
def word(n):return int(n).to_bytes(32,'big')
def address(a):
 b=bytes.fromhex(a.removeprefix('0x'))
 if len(b)!=20:raise ValueError('Address length')
 return b'\0'*12+b
def digest(chain,escrow,payment,nonce,version,request_hash,policy_hash,approved,decision):
 return hashlib.sha256(hashlib.sha256(b'invinoveritas/verdict-relay/v2').digest()+word(chain)+address(escrow)+address(escrow)+word(payment)+word(nonce)+word(version)+bytes.fromhex(request_hash)+bytes.fromhex(policy_hash)+word(int(approved))+bytes.fromhex(decision)).digest()
def profile_bytes():return PROFILE.read_bytes()
def reference(case,grant):
 fresh=engine.evaluate(case)
 return {'schema':'claim-aware.escrow-request.v0','claim_type':fresh['claim_type'],'scenario':fresh['scenario'],'scope':engine.SCOPE,'scenario_contract_sha256':fresh['contract_sha256'],'evidence_sha256':sha(canonical(fresh['evidence_references'])),'proof_sha256':case['claim']['proof_sha256'],'verification_profile_sha256':sha(profile_bytes()),'authorization':{'status':V,'authorized':True},**{k:grant[k] for k in ('intended_consumer','chain_id','escrow_contract','token','payment_id','job_id','recipient','amount','nonce','expires_at')}}
def assess(case,record,request_raw,grant,snapshot,now,journal,profile_raw=None):
 checks={}
 def check(name,value):checks[name]=V if value else R
 def out():
  status=R if R in checks.values() else U if U in checks.values() else V
  return {'status':status,'authorized':status==V,'checks':checks,'missing_obligations':fresh.get('missing_obligations',[]) if 'fresh' in locals() else [],'enforcement':'OFF_CHAIN','assumptions':['payer-selected grant','authenticated fresh snapshot','honest policy signer','local nonce journal is not a global chain registry']}
 if case.get('contract_bytes') is None:checks['contract_preimage']=U;return out()
 if profile_raw is None:checks['profile_preimage']=U;return out()
 try:
  request=json.loads(request_raw)
  check('canonical_request',canonical(request)==request_raw and set(request)==FIELDS)
  fresh=engine.evaluate(case)
  check('authorization_recomputation',fresh['status']==V and fresh['authorized'] is True) # guard authorization
  check('consumer_record',canonical(record)==canonical(fresh)) # guard record
  check('scope',request['schema']=='claim-aware.escrow-request.v0' and request['claim_type']==fresh['claim_type']==grant['claim_type'] and request['scenario']==fresh['scenario']==grant['scenario'] and request['scope']==engine.SCOPE==grant['scope']) # guard scope
  check('scenario_digest',request['scenario_contract_sha256']==fresh['contract_sha256']==grant['scenario_contract_sha256']) # guard scenario
  check('evidence_digest',request['evidence_sha256']==sha(canonical(fresh['evidence_references'])) and request['proof_sha256']==case['claim']['proof_sha256']) # guard evidence
  check('profile',profile_raw==profile_bytes() and request['verification_profile_sha256']==sha(profile_raw)==grant['verification_profile_sha256']) # guard profile
  check('outcome',request['authorization']=={'status':V,'authorized':True})
  check('consumer',request['intended_consumer']==grant['intended_consumer'])
  check('chain',request['chain_id']==snapshot['chain_id']==grant['chain_id']) # guard chain
  check('escrow',request['escrow_contract'].lower()==snapshot['escrow_contract'].lower()==grant['escrow_contract'].lower()) # guard escrow
  check('recipient',request['recipient'].lower()==snapshot['recipient'].lower()==grant['recipient'].lower()) # guard recipient
  check('amount',request['amount']==snapshot['amount']==grant['amount']) # guard amount
  check('token',request['token'].lower()==snapshot['token'].lower()==grant['token'].lower())
  check('payment',request['payment_id']==snapshot['payment_id']==grant['payment_id'] and request['job_id']==grant['job_id']) # guard payment
  check('nonce',request['nonce']==grant['nonce'] and request['nonce'] not in journal) # guard nonce
  check('expiry',request['expires_at']==grant['expires_at'] and int(now)<int(request['expires_at'])) # guard expiry
  check('request_hash',snapshot['request_sha256']==sha(request_raw))
  check('policy_hash',snapshot['policy_sha256']==sha(canonical(grant)))
  check('funded',snapshot['state']=='Funded')
  check('signer_active',grant['signer']==LAB_PUB and grant['signer'] not in grant['revoked_signers']) # guard revocation
  result=out();result['missing_obligations']=fresh.get('missing_obligations',[]);return result
 except (ValueError,TypeError,KeyError):checks['malformed']=R;return out()
def reserve(result,nonce,journal):
 if result['authorized'] is not True:return False
 if nonce in journal:return False
 journal.add(nonce) # guard consumption
 return True
def verify_verdict(verdict,grant):
 if verdict['signer']!=grant['signer']:return R # guard trusted_signer
 return V if bip340.verify(bytes.fromhex(verdict['signer']),bytes.fromhex(verdict['digest']),bytes.fromhex(verdict['signature'])) else R
def laboratory_sign(d,key=LAB_KEY):
 return {'signer':bip340.pubkey(key).hex(),'digest':d.hex(),'signature':bip340.sign(key,d).hex(),'origin':'DETERMINISTIC_LABORATORY_ONLY'}
def decision_reference(request_raw,grant,record):
 return sha(canonical({'schema':'lab-decision-reference.v0','request_sha256':sha(request_raw),'policy_sha256':sha(canonical(grant)),'claim_result_sha256':sha(canonical(record))}))
def verify_bound_verdict(verdict,request_raw,grant,record):
 """Authenticate the exact supplied preimages, not a caller-supplied digest alone."""
 if verify_verdict(verdict,grant)!=V:return R
 r=json.loads(request_raw)
 d=digest(r['chain_id'],r['escrow_contract'],r['payment_id'],r['nonce'],1,sha(request_raw),sha(canonical(grant)),r['authorization']['authorized'],decision_reference(request_raw,grant,record))
 return V if verdict['digest']==d.hex() else R # guard verdict_preimage
