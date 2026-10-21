// New, explicitly adversarial LAB artifacts. Original v2 capture stays frozen.
// No proof is fabricated as valid; the corrupted proof is labeled an invalid witness.
// These signatures do not assert a new historical execution or third-party issuance.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {ROOT,hash,sign,address,secp256k1,knownAnswers} from '../../src/v2/crypto.mjs';
const dir=path.join(ROOT,'evidence/v2/survivor-audit/witnesses');
if(fs.existsSync(dir)) throw Error('Refusing to overwrite frozen survivor witnesses');
if(!Object.values(knownAnswers()).every(Boolean)) throw Error('Known answer failure');
fs.mkdirSync(dir,{recursive:true});
const original=path.join(ROOT,'evidence/v2/capture');
const read=name=>fs.readFileSync(path.join(original,name));
const obj=name=>JSON.parse(read(name));
const write=(name,value)=>fs.writeFileSync(path.join(dir,name),JSON.stringify(value,null,2)+'\n');
const keys=Object.fromEntries(['provenance','judgment','receipt'].map(role=>[role,secp256k1.utils.randomSecretKey()]));
try {
 const policy={...obj('policy.json'),authorized:Object.fromEntries(Object.entries(keys).map(([role,key])=>[role,address(secp256k1.getPublicKey(key))]))};
 write('policy.json',policy);
 const policyHash=hash(fs.readFileSync(path.join(dir,'policy.json')));
 const proof=Buffer.from(read('a/proof.bin'));
 // VAGCNP2 header + vector length: the first claimed scalar starts at offset 12.
 const originalClaimed=proof.readBigUInt64LE(12), invalidClaimed=(originalClaimed+1n)%18446744069414584321n;
 proof.writeBigUInt64LE(invalidClaimed,12);
 fs.writeFileSync(path.join(dir,'invalid-claimed-scalar.bin'),proof);
 const common={...obj('a/judgment.json').message,policyHash};
 const receipt={...obj('a/receipt.json').message,policyHash};
 const provenance=sign('WyriweAttestation',obj('a/provenance.json').message,keys.provenance,policy.domain);
 for(const name of ['positive','native_isolated','type_isolated']) {
  const badNative=name==='native_isolated';
  const message={...common,proofHash:badNative?hash(proof):common.proofHash};
  const receiptMessage={...receipt,proofHash:message.proofHash};
  const judgment=name==='type_isolated'
   ?sign('LabReceipt',receiptMessage,keys.judgment,policy.domain)
   :sign('LabJudgment',message,keys.judgment,policy.domain);
  write(name+'.json',{schema:'survivor-isolation-case-v1',purpose:'laboratory verifier input, no new execution claim',policy:'evidence/v2/survivor-audit/witnesses/policy.json',
   files:Object.fromEntries(Object.entries({raw_input:'raw-input.bin',input:'input.bin',weights:'weights.bin',output:'output.bin',proof:'proof.bin',model:'model.json',result:'delivered.bin',observation:'execution-observation.json'}).map(([k,v])=>[k,badNative && k==='proof'?'evidence/v2/survivor-audit/witnesses/invalid-claimed-scalar.bin':'evidence/v2/capture/a/'+v])),
   documents:{provenance,judgment,receipt:sign('LabReceipt',receiptMessage,keys.receipt,policy.domain)},
   claim:{...obj('a/claim.json'),policyHash,proofHash:message.proofHash},consumed_nonces:[]});
 }
 write('generation.json',{schema:'survivor-witness-generation-v1',base_commit:'ba889271bef7cb3d2eed00067a12064689bfb627',new_private_keys_persisted:false,
  policy_change:'only role public keys changed; same supported policy schema and semantics; claim policyHash recomputed',
  proof_change:{offset:12,field:'claimed scalar',from:originalClaimed.toString(),to:invalidClaimed.toString(),original_sha256:createHash('sha256').update(read('a/proof.bin')).digest('hex'),modified_sha256:createHash('sha256').update(proof).digest('hex')},
  unique_signatures_created:6,source_observations:'reuse retained original local observation bytes; no new operation or chronology is asserted',
  type_witness:'LabReceipt genuinely signed by the judgment-role key; the policy still has distinct role keys',
  native_witness:'all signed digest references updated to the explicitly invalid proof; native verification must reject'});
 console.log(JSON.stringify({created:true,cases:3,private_keys_persisted:false,proof_marked_invalid:true}));
} finally {for(const key of Object.values(keys)) key.fill(0);}
