// One-time laboratory issuance. Ephemeral private keys never leave process memory.
// These signatures are genuine crypto over controlled assertions, NOT external observations.
import fs from 'node:fs';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
import {ROOT,sign,hash,address,secp256k1} from '../../src/v2/crypto.mjs';
const out=path.join(ROOT,'evidence/v4/lab');
if(fs.existsSync(path.join(out,'bundle.json'))) throw Error('Frozen fixture already exists');
fs.mkdirSync(out,{recursive:true});
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const copy=x=>structuredClone(x);
const keys=Object.fromEntries(['provenance','judgment','receipt','unauthorized'].map(r=>[r,randomBytes(32)]));
const policy=read('evidence/v2/capture/policy.json');
policy.schema='v4-lab-policy'; policy.version=4;
policy.authorized=Object.fromEntries(['provenance','judgment','receipt'].map(r=>[r,address(secp256k1.getPublicKey(keys[r]))]));
const policyBytes=Buffer.from(JSON.stringify(policy,null,2)+'\n');
fs.writeFileSync(path.join(out,'policy.json'),policyBytes);
const claim=read('evidence/v2/capture/a/claim.json'); claim.policyHash=hash(policyBytes);
const originals=Object.fromEntries(['provenance','judgment','receipt'].map(r=>[r,read('evidence/v2/capture/a/'+r+'.json')]));
const issue=(role,message,key=role)=>sign(originals[role].type,message,keys[key],policy.domain);
const documents=Object.fromEntries(Object.entries(originals).map(([role,d])=>{const m=copy(d.message);if(role!=='provenance')m.policyHash=claim.policyHash;return [role,issue(role,m)];}));
const variants={};
function variant(id,role,edit,key=role){const m=copy(documents[role].message);edit(m);variants[id]={[role]:issue(role,m,key)};}
const badProof=hash(fs.readFileSync(path.join(ROOT,'evidence/v2/survivor-audit/witnesses/invalid-claimed-scalar.bin')));
variants.O02={};
for(const role of ['judgment','receipt']){const m=copy(documents[role].message);m.proofHash=badProof;variants.O02[role]=issue(role,m);}
variant('O03','provenance',m=>m.rawInputHash='0x'+'11'.repeat(32));
variant('O07','judgment',m=>m.proofHash=hash(fs.readFileSync(path.join(ROOT,'evidence/v2/capture/b/proof.bin'))));
variant('O08','provenance',()=>{},'unauthorized');
variant('O09','receipt',m=>m.executionId='unrelated-execution');
variant('O12','receipt',m=>m.scope='unrelated-scope');
const bundle={schema:'v4-laboratory-crypto-capture',classification:'LAB_CRYPTOGRAPHIC_CONTROLLED_ASSERTIONS',producer:'local experiment; ephemeral role keys',chain_origin:'UNVERIFIABLE: no observed chain',historical_execution:'NOT CLAIMED',policy,claim,documents,variants,badProofHash:badProof};
fs.writeFileSync(path.join(out,'bundle.json'),JSON.stringify(bundle,null,2)+'\n');
console.log(JSON.stringify({created:'evidence/v4/lab/bundle.json',private_keys_saved:false,external_observation:false}));
