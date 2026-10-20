// Optional fixture regeneration creates different signatures and requires new inventory.
// Fresh ephemeral laboratory keys are never stored. This is a controlled counterexample.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT,sign,address,secp256k1} from '../../src/v2/crypto.mjs';
const weak=process.argv.includes('--weak-authority');
const dest=path.join(ROOT,weak?'fixtures/integration/weak-review.json':'fixtures/integration/other-proof-review.json');
if(fs.existsSync(dest))throw Error('Preserved evidence exists; refusing overwrite');
const canonical=x=>x===null||typeof x!=='object'?JSON.stringify(x):Array.isArray(x)?'['+x.map(canonical).join(',')+']':'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const c=JSON.parse(fs.readFileSync(path.join(ROOT,'fixtures/erc8404/lab/independent.json')));
const keys={producer:secp256k1.utils.randomSecretKey(),judgment:secp256k1.utils.randomSecretKey()};
for(const r of Object.keys(keys))c.contract.authorized[r]=address(secp256k1.getPublicKey(keys[r]));
const source=weak?'evidence/v2/capture/a/proof.bin':'evidence/v2/capture/b/proof.bin';
const bytes=fs.readFileSync(path.join(ROOT,source));c.source_artifact=source;
c.claim.subject='lab:preserved-native-proof-b';c.claim.artifactSha256=sha(bytes);
c.contract.scenario='lab-other-proof-review';c.claim.scenario=c.contract.scenario;
if(weak){delete c.contract.requirements.S04;delete c.contract.requirements.O14;c.contract.separation=[];c.catalog=JSON.parse(JSON.stringify(c.contract.requirements));c.contract.scenario='lab-missing-authority-obligation';c.claim.scenario=c.contract.scenario;c.claim.subject='lab:proof-a-under-weakened-review';}
const raw=Buffer.from(canonical(c.contract));c.contract_bytes=raw.toString('base64');c.context.contract_sha256=sha(raw);c.documents={};delete c.variants;
for(const r of Object.keys(keys))c.documents[r]=sign('LabJudgment',{subject:c.claim.subject,inputHash:'0x'+'00'.repeat(32),outputHash:'0x'+'00'.repeat(32),modelHash:'0x'+'00'.repeat(32),proofHash:'0x'+sha(bytes),scope:c.claim.scope,executionId:'NOT_AN_EXECUTION_CLAIM',policyHash:'0x'+sha(raw),nonce:'integration-counterexample-only',action:c.contract.actions[r]},keys[r],c.contract.domain);
fs.writeFileSync(dest,JSON.stringify(c,null,2)+'\n');
console.log(JSON.stringify({fixture:dest,classification:'LABORATORY_CONTROLLED_COUNTEREXAMPLE',external_observation:false,artifact_sha256:sha(bytes),private_keys_persisted:false}));
