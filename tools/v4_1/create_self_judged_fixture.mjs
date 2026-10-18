// One-time laboratory issuance for the v4.1 self-judged witness (O14).
// Same pattern as tools/v4/create_lab_fixture.mjs: ephemeral keys never leave process memory.
// One key signs BOTH provenance and judgment, and the policy authorizes that key for both roles,
// so every O01-O13 check passes and only checker independence (O14) can refuse it.
// Genuine crypto over controlled assertions, NOT external observations.
import fs from 'node:fs';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
import {ROOT,sign,hash,address,secp256k1} from '../../src/v2/crypto.mjs';
const out=path.join(ROOT,'evidence/v4_1/self-judged');
if(fs.existsSync(path.join(out,'bundle.json'))) throw Error('Frozen fixture already exists');
fs.mkdirSync(out,{recursive:true});
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const copy=x=>structuredClone(x);
const keys={producer:randomBytes(32),receipt:randomBytes(32)};
const role_key={provenance:'producer',judgment:'producer',receipt:'receipt'};
const policy=read('evidence/v4/lab/policy.json');
policy.schema='v4.1-lab-policy-self-judged';
policy.authorized=Object.fromEntries(Object.entries(role_key).map(([r,k])=>[r,address(secp256k1.getPublicKey(keys[k]))]));
const policyBytes=Buffer.from(JSON.stringify(policy,null,2)+'\n');
fs.writeFileSync(path.join(out,'policy.json'),policyBytes);
const v4=read('evidence/v4/lab/bundle.json');
const claim=copy(v4.claim); claim.policyHash=hash(policyBytes);
const documents=Object.fromEntries(Object.entries(v4.documents).map(([role,d])=>{const m=copy(d.message);if(role!=='provenance')m.policyHash=claim.policyHash;return [role,sign(d.type,m,keys[role_key[role]],policy.domain)];}));
const bundle={schema:'v4.1-laboratory-self-judged-capture',classification:'LAB_CRYPTOGRAPHIC_CONTROLLED_ASSERTIONS',producer:'local experiment; one ephemeral key for provenance and judgment, one for receipt',chain_origin:'UNVERIFIABLE: no observed chain',historical_execution:'NOT CLAIMED',policy,claim,documents};
fs.writeFileSync(path.join(out,'bundle.json'),JSON.stringify(bundle,null,2)+'\n');
console.log(JSON.stringify({created:'evidence/v4_1/self-judged/bundle.json',private_keys_saved:false,external_observation:false}));
