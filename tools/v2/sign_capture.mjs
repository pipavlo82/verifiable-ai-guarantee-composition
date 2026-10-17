// Actual laboratory signatures. Fresh OS-random private keys live only in this process.
// This is not an upstream issuer or a transaction, and the domain is an OFFLINE lab policy.
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,hash,utf8,unhex,sign,address,secp256k1,IDENTITY,knownAnswers} from '../../src/v2/crypto.mjs';
const dir=path.join(ROOT,'evidence/v2/capture');
const read=(sub,name)=>fs.readFileSync(path.join(dir,sub,name));
const write=(name,obj)=>fs.writeFileSync(path.join(dir,name),JSON.stringify(obj,null,2)+'\n');
if(fs.existsSync(path.join(dir,'policy.json'))) throw Error('Capture is frozen: choose a new version explicitly');
if(!Object.values(knownAnswers()).every(Boolean)) throw Error('Known answer test failed');
const keys=Object.fromEntries(['provenance','judgment','receipt','outsider'].map(role=>[role,secp256k1.utils.randomSecretKey()]));
const domain={name:'ERC8004AttestationGateway',version:'1',chainId:31337};
const policy={schema:'lab-recompute-policy-v2',version:1,domain,domain_status:'DECLARED_OFFLINE_LAB_DOMAIN_NO_CHAIN_OBSERVATION',scope:'public-matmul-recomputation',action:'materialize-matmul-output',modelHash:hash(read('a','model.json')),authorized:Object.fromEntries(Object.entries(keys).filter(([k])=>k!=='outsider').map(([k,v])=>[k,address(secp256k1.getPublicKey(v))])),historicalExecutionAuthority:null};
write('policy.json',policy); const policyHash=hash(fs.readFileSync(path.join(dir,'policy.json')));
for(const id of ['a','b']) {
 const inputHash=hash(read(id,'input.bin')), outputHash=hash(read(id,'output.bin'));
 const common={subject:'lab-subject-'+id,inputHash,outputHash,modelHash:policy.modelHash,proofHash:hash(read(id,'proof.bin')),action:policy.action,scope:policy.scope,executionId:'lab-execution-'+id,policyHash,nonce:'lab-request-'+id};
 const provenance={agentId:'0x'+'00'.repeat(32),registry:'0x'+'00'.repeat(20),modelHash:policy.modelHash,rawInputHash:hash(read(id,'raw-input.bin')),sanitizationPipelineHash:hash(Buffer.concat([utf8(IDENTITY),unhex(inputHash)])),inputHash,outputHash,timestamp:0};
 write(id+'/provenance.json',sign('WyriweAttestation',provenance,keys.provenance,domain));
 write(id+'/judgment.json',sign('LabJudgment',common,keys.judgment,domain));
 const receipt={...common,resultHash:hash(read(id,'delivered.bin')),observationHash:hash(read(id,'execution-observation.json'))};
 write(id+'/receipt.json',sign('LabReceipt',receipt,keys.receipt,domain));
 write(id+'/claim.json',{...common,claimKind:'recompute-output'});
 if(id==='a') {
  write('a/outsider-judgment.json',sign('LabJudgment',common,keys.outsider,domain));
  write('a/other-domain-judgment.json',sign('LabJudgment',common,keys.judgment,{...domain,chainId:31338}));
  write('a/wrong-action-judgment.json',sign('LabJudgment',{...common,action:'unrelated-action'},keys.judgment,domain));
  write('a/wrong-execution-receipt.json',sign('LabReceipt',{...receipt,executionId:'unrelated-execution'},keys.receipt,domain));
 }
}
for(const key of Object.values(keys)) key.fill(0);
console.log(JSON.stringify({actual_signatures_created:10,private_keys_saved:false,domain_status:policy.domain_status,execution_truth:'signatures do not establish historical execution; local observations are separate'}));
