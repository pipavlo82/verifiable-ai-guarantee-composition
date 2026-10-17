// Verification only. Preserved external signatures are never generated or relabeled.
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {ROOT,hash,hex,unhex,digest,address,secp256k1,knownAnswers} from '../v2/crypto.mjs';
const {schnorr}=await import(pathToFileURL(ROOT+'/build/formal-v1/crypto/node_modules/@noble/curves/secp256k1.js'));
const sha=b=>createHash('sha256').update(b).digest('hex');
// This profile supports only the integer/ASCII-key subset present in these captures.
function canon(x){
 if(x===null || typeof x==='boolean' || typeof x==='string')return JSON.stringify(x);
 if(typeof x==='number'){if(!Number.isSafeInteger(x))throw Error('non-integer canonical input');return JSON.stringify(x);}
 if(Array.isArray(x))return '['+x.map(canon).join(',')+']';
 if(typeof x==='object' && Object.keys(x).every(k=>/^[\x20-\x7e]+$/.test(k)))return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canon(x[k])).join(',')+'}';
 throw Error('unsupported canonical value');
}
function nostr(event){
 if(!event)return {status:'UNVERIFIABLE',reason:'missing event'};
 try{
  if(!Number.isSafeInteger(event.created_at)||!Number.isSafeInteger(event.kind)||!Array.isArray(event.tags)||typeof event.content!=='string')throw Error('shape');
  const id=sha(JSON.stringify([0,event.pubkey,event.created_at,event.kind,event.tags,event.content]));
  const valid=id===event.id && schnorr.verify(Buffer.from(event.sig,'hex'),Buffer.from(id,'hex'),Buffer.from(event.pubkey,'hex'));
  return {status:valid?'VERIFIED':'REFUTED',id,signer:event.pubkey,payload:JSON.parse(event.content)};
 }catch{return {status:'REFUTED',reason:'invalid NIP-01/BIP-340 artifact'};}
}
const CELL=[['schema','string'],['claim_id','string'],['result','string'],['verifier','address'],['boundary','string'],['as_of','string'],['recomputed_at','string'],['evidence_hash','bytes32']];
function cell(doc){
 if(!doc)return {status:'UNVERIFIABLE',reason:'missing cell'};
 try{
  const p=doc.proof_payload,s=doc.signature;
  if(s.scheme!=='eip712'||s.primaryType!=='Cell'||canon(s.types.Cell)!==canon(CELL.map(([name,type])=>({name,type}))))return {status:'UNVERIFIABLE',reason:'unsupported signed type'};
  const evidenceHash=hash(Buffer.from(canon(p.evidence))),message={};
  for(const [key] of CELL)message[key]=key==='evidence_hash'?evidenceHash:p[key];
  const types={EIP712Domain:[['name','string'],['version','string'],['chainId','uint256']],Cell:CELL};
  const d=digest({type:'Cell',domain:s.domain,message},types),sig=unhex(s.signature);
  if(sig.length!==65||![27,28].includes(sig[64]))throw Error('signature shape');
  const pk=secp256k1.recoverPublicKey(Buffer.concat([Buffer.from([sig[64]-27]),sig.slice(0,64)]),d,{prehash:false});
  const recovered=address(pk),valid=evidenceHash===s.evidence_hash && recovered===s.signer.toLowerCase() && recovered===p.verifier.toLowerCase() && secp256k1.verify(sig.slice(0,64),d,pk,{prehash:false,lowS:true});
  return {status:valid?'VERIFIED':'REFUTED',signer:recovered,digest:hex(d),evidence_hash:evidenceHash,payload:p,domain:s.domain};
 }catch{return {status:'REFUTED',reason:'invalid EIP-712 cell'};}
}
const request=JSON.parse(fs.readFileSync(0,'utf8'));
if(!Object.values(knownAnswers()).every(Boolean))throw Error('v2 known-answer gate failed');
console.log(JSON.stringify({ledger:nostr(request.ledger?.proof_event),cell1:nostr(request.cell1?.event),cell2:cell(request.cell2)}));
