import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT,sign,address,secp256k1,hash} from '../../src/v2/crypto.mjs';
const out=path.join(ROOT,'fixtures/erc8404/lab');
const canon=x=>x===null||typeof x!=='object'?JSON.stringify(x):Array.isArray(x)?'['+x.map(canon).join(',')+']':'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canon(x[k])).join(',')+'}';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const key=secp256k1.utils.randomSecretKey();const addr=address(secp256k1.getPublicKey(key));
const key2=secp256k1.utils.randomSecretKey();const addr2=address(secp256k1.getPublicKey(key2));
function write(name,data){let p=path.join(out,name);if(fs.existsSync(p))throw Error('already frozen '+name);fs.writeFileSync(p,data);}
for(const family of ['unsupported_claim','incomparable','missing_role']){
 const base=JSON.parse(fs.readFileSync(path.join(out,'independent.json')));const c=base.contract;
 c.authorized={producer:addr,judgment:addr2};
 if(family==='unsupported_claim')c.claim_type='EXTERNAL_TASK_SUCCESS';
 if(family==='incomparable')c.identity_namespace=null;
 if(family==='missing_role')c.separation.push(['judgment','unknown-role']);
 const raw=Buffer.from(canon(c)),digest=sha(raw);
 base.contract_bytes=raw.toString('base64');base.context.contract_sha256=digest;base.claim.claimType=c.claim_type;
 for(const role of ['producer','judgment'])base.documents[role]=sign('LabJudgment',{...base.documents[role].message,policyHash:'0x'+digest},role==='producer'?key:key2,c.domain);
 base.variants={};write(family+'.contract.json',raw);write(family+'.json',JSON.stringify(base,null,2)+'\n');
}
// Reproduce v4 gaps without editing its implementation or historical evidence.
const old=JSON.parse(fs.readFileSync(path.join(ROOT,'evidence/v4/lab/bundle.json')));
old.policy.authorized={provenance:addr,judgment:addr,receipt:addr};
const policy=Buffer.from(JSON.stringify(old.policy,null,2)+'\n');const ph=hash(policy);
old.claim.policyHash=ph;
for(const [role,doc] of Object.entries(old.documents))old.documents[role]=sign(doc.type,{...doc.message,...(role==='provenance'?{}:{policyHash:ph})},key,doc.domain);
write('v4-self-policy.json',policy);write('v4-self-witness.json',JSON.stringify({documents:old.documents,claim:old.claim,policy:old.policy},null,2)+'\n');
console.log(JSON.stringify({new_control_families:3,v4_self_signature_witness:true,keys_saved:false}));
