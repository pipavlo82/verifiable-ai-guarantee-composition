import fs from 'node:fs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const {verifyIntegrity}=await import(pathToFileURL(root+'/build/v3/upstream/receiptos-verify/src/adapters/crystal.mjs'));
console.log(JSON.stringify(await verifyIntegrity(JSON.parse(fs.readFileSync(0,'utf8')))));
