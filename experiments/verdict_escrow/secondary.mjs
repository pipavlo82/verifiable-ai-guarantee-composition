import fs from 'node:fs';
import crypto from 'node:crypto';
import {schnorr} from '../../build/formal-v1/crypto/node_modules/@noble/curves/secp256k1.js';
const root=process.argv[2];const hash=b=>crypto.createHash('sha256').update(b).digest();const u=x=>Buffer.from(BigInt(x).toString(16).padStart(64,'0'),'hex');const addr=x=>Buffer.from(x.slice(2).padStart(64,'0'),'hex');let rows=[];
for(const file of fs.readdirSync(root).filter(x=>x.endsWith('-offchain.json')).sort()){
 const v=JSON.parse(fs.readFileSync(root+'/'+file));const r=v.request;const d=hash(Buffer.concat([hash(Buffer.from('invinoveritas/verdict-relay/v2')),u(r.chain_id),addr(r.escrow_contract),addr(r.escrow_contract),u(r.payment_id),u(r.nonce),u(1),hash(Buffer.from(v.request_bytes,'hex')),Buffer.from(v.snapshot.policy_sha256,'hex'),u(1),Buffer.from(v.decision_ref,'hex')]));
 let ok=false;try{ok=schnorr.verify(Buffer.from(v.verdict.signature,'hex'),Buffer.from(v.verdict.digest,'hex'),Buffer.from(v.verdict.signer,'hex'));}catch{}
 rows.push({name:v.name,digest_equal:d.toString('hex')===v.verdict.digest,python_schnorr:v.component_signature_valid,node_schnorr:ok,agreement:ok===v.component_signature_valid});
}
console.log(JSON.stringify({rows,passed:rows.length>=31&&rows.every(r=>r.digest_equal&&r.agreement)},null,2));if(!rows.every(r=>r.digest_equal&&r.agreement))process.exitCode=1;
