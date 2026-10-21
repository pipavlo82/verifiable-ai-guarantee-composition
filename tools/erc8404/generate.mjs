// Controlled laboratory signatures; fresh private keys remain only in memory.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT,sign,address,secp256k1} from '../../src/v2/crypto.mjs';
const out=path.join(ROOT,'fixtures/erc8404/lab');
if(fs.existsSync(out)) throw Error('Frozen generated laboratory artifacts already exist');
fs.mkdirSync(out,{recursive:true});
const canonical=x=>x===null||typeof x!=='object'?JSON.stringify(x):Array.isArray(x)?'['+x.map(canonical).join(',')+']':'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const keys=Object.fromEntries(['p','j','a'].map(k=>[k,secp256k1.utils.randomSecretKey()]));
const addr=k=>address(secp256k1.getPublicKey(keys[k]));
const artifact=fs.readFileSync(path.join(ROOT,'evidence/v2/capture/a/proof.bin'));
const digest=sha(artifact);
const requirements={S01:{procedure:'signature',dependencies:[]},S02:{procedure:'artifact',dependencies:['S01']},S03:{procedure:'subject',dependencies:['S01']},S04:{procedure:'authority',dependencies:['S01']},S05:{procedure:'domain',dependencies:['S01']},S06:{procedure:'judgment',dependencies:['S01']},O14:{procedure:'independence',dependencies:['S01','S04','S05']}};
const domain={name:'Claim-Aware External Lab',version:'1',chainId:'31337'};
const families=[['independent','p',true,'REJECT'],['self','j',true,'REJECT'],['self_allowed','j',false,'REJECT'],['list','p',true,'LIST'],['author_collision','p',true,'REJECT'],['author_independent','p',true,'REJECT']];
for(const [name,producer,independent,policy] of families){
 const contract={schema:'claim-aware.external.v1',scenario:'lab-artifact-review-v1',claim_type:'REVIEWED_ARTIFACT_IDENTITY',scope:'artifact-byte-identity',domain,
 authorized:{producer:addr(producer),judgment:addr('j')},identity_namespace:'eip155:31337:secp256k1',actions:{producer:'declare-artifact',judgment:'review-artifact'},
 separation:independent?[['producer','judgment']]:[],requirements:JSON.parse(JSON.stringify(requirements)),
 consumed_fields:['scenario','claimType','scope','subject','artifactSha256'],unconsumed_policy:policy,adequacy:'EXTERNAL_ASSUMPTION'};
 if(!independent) delete contract.requirements.O14;
 if(name.startsWith('author_'))contract.separation.push(['judgment','author']);
 const raw=Buffer.from(canonical(contract));const ch=sha(raw);
 const claim={scenario:contract.scenario,claimType:contract.claim_type,scope:contract.scope,subject:'lab:preserved-native-proof-a',artifactSha256:digest};
 const msg={subject:claim.subject,inputHash:'0x'+'00'.repeat(32),outputHash:'0x'+'00'.repeat(32),modelHash:'0x'+'00'.repeat(32),proofHash:'0x'+digest,scope:claim.scope,executionId:'NOT_AN_EXECUTION_CLAIM',policyHash:'0x'+ch,nonce:'lab-fixture-v1'};
 const documents={producer:sign('LabJudgment',{...msg,action:'declare-artifact'},keys[producer],domain),judgment:sign('LabJudgment',{...msg,action:'review-artifact'},keys.j,domain)};
 if(name.startsWith('author_'))documents.author=sign('LabJudgment',{...msg,action:'author-contract'},keys[name==='author_collision'?'j':'a'],domain);
 const variants={wrong_artifact:sign('LabJudgment',{...msg,action:'review-artifact',proofHash:'0x'+'12'.repeat(32)},keys.j,domain),wrong_subject:sign('LabJudgment',{...msg,action:'review-artifact',subject:'other-subject'},keys.j,domain),wrong_action:sign('LabJudgment',{...msg,action:'release-funds'},keys.j,domain),wrong_contract:sign('LabJudgment',{...msg,action:'review-artifact',policyHash:'0x'+'34'.repeat(32)},keys.j,domain),unauthorized:sign('LabJudgment',{...msg,action:'review-artifact'},keys.a,domain)};
 fs.writeFileSync(path.join(out,name+'.contract.json'),raw);
 fs.writeFileSync(path.join(out,name+'.json'),JSON.stringify({contract,contract_bytes:raw.toString('base64'),claim,context:{contract_sha256:ch},catalog:contract.requirements,documents,variants},null,2)+'\n');
}
fs.writeFileSync(path.join(out,'PROVENANCE.json'),JSON.stringify({kind:'CONTROLLED_LABORATORY_SIGNATURES',producer:'local experimental fixture generator',external_observation:false,private_keys_persisted:false,artifact_source:'evidence/v2/capture/a/proof.bin',artifact_sha256:digest,signed_statement:'byte identity and declared review only; no inference verification or execution assertion',schema:'LabJudgment reused as explicitly declared lab carrier; not WYRIWE L4'},null,2)+'\n');
console.log(JSON.stringify({generated:families.length,private_keys_persisted:false,artifact_sha256:digest}));
