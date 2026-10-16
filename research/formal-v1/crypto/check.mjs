// Narrow offline replay of an existing public event, not an authorization service.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const dependencyRoot = process.argv[2];
if (!dependencyRoot) throw new Error('Pass the isolated npm install directory');
const { schnorr } = await import(pathToFileURL(resolve(dependencyRoot, 'node_modules/@noble/curves/secp256k1.js')));
const event = JSON.parse(readFileSync(new URL('./ledger-19-event.json', import.meta.url), 'utf8'));
const hex = (s, n) => typeof s === 'string' && new RegExp(`^[0-9a-f]{${n}}$`).test(s);
const sha256 = data => createHash('sha256').update(data).digest('hex');

function authenticate(e) {
  if (!e || !hex(e.pubkey, 64) || !hex(e.id, 64) || !hex(e.sig, 128)
      || !Number.isSafeInteger(e.created_at) || e.created_at < 0
      || !Number.isSafeInteger(e.kind) || e.kind < 0 || e.kind > 65535
      || typeof e.content !== 'string' || !Array.isArray(e.tags)
      || !e.tags.every(t => Array.isArray(t) && t.every(x => typeof x === 'string'))) return 'UNVERIFIABLE';
  const id = sha256(JSON.stringify([0, e.pubkey, e.created_at, e.kind, e.tags, e.content]));
  if (id !== e.id) return 'REFUTED';
  try {
    return schnorr.verify(Buffer.from(e.sig, 'hex'), Buffer.from(id, 'hex'), Buffer.from(e.pubkey, 'hex')) ? 'VERIFIED' : 'REFUTED';
  } catch { return 'REFUTED'; }
}

function proposalBinding(e, requestedDigest) {
  const authentic = authenticate(e);
  if (authentic !== 'VERIFIED') return authentic;
  if (!hex(requestedDigest, 64)) return 'UNVERIFIABLE';
  let content;
  try { content = JSON.parse(e.content); } catch { return 'UNVERIFIABLE'; }
  if (!content || content.schema !== 'invinoveritas.verdict_proof.v1'
      || !hex(content.artifact_hash, 64) || content.verifier_pubkey !== e.pubkey) return 'UNVERIFIABLE';
  // A same-profile digest comparison only. Caller must establish preimage and encoding.
  return content.artifact_hash === requestedDigest ? 'VERIFIED' : 'REFUTED';
}

const content = JSON.parse(event.content);
const originalBytes = JSON.stringify(event);
const flip = s => (s[0] === '0' ? '1' : '0') + s.slice(1);
const changedSignature = { ...event, sig: flip(event.sig) };
const changedContent = { ...event, content: event.content + ' ' };
const changedKey = { ...event, pubkey: flip(event.pubkey) };
const changedId = { ...event, id: flip(event.id) };
const changedContentWithId = { ...changedContent, id: sha256(JSON.stringify([0, changedContent.pubkey, changedContent.created_at, changedContent.kind, changedContent.tags, changedContent.content])) };
const cases = [
  ['original_signature', authenticate(event), 'VERIFIED'],
  ['changed_signature', authenticate(changedSignature), 'REFUTED'],
  ['changed_content_stale_id', authenticate(changedContent), 'REFUTED'],
  ['changed_content_recomputed_id_original_signature', authenticate(changedContentWithId), 'REFUTED'],
  ['changed_key', authenticate(changedKey), 'REFUTED'],
  ['changed_id', authenticate(changedId), 'REFUTED'],
  ['matching_proposal_digest', proposalBinding(event, content.artifact_hash), 'VERIFIED'],
  ['wrong_proposal_same_authentic_event', proposalBinding(event, flip(content.artifact_hash)), 'REFUTED'],
  ['missing_proposal', proposalBinding(event, undefined), 'UNVERIFIABLE'],
  ['boolean_is_not_evidence', authenticate({ verified: true }), 'UNVERIFIABLE'],
  ['original_event_still_authentic', authenticate(event), 'VERIFIED'],
];
const report = {
  schema: 'public-nostr-replay-v1', mode: 'REAL_PUBLIC_SIGNATURE_WITH_CONTROLLED_CONSUMER_SUBSTITUTIONS',
  event_id: event.id, pubkey: event.pubkey, signature_algorithm: 'BIP340/secp256k1',
  dependency: '@noble/curves@2.0.1',
  cases: cases.map(([name, actual, expected]) => ({ name, actual, expected, passed: actual === expected })),
  original_event_unchanged: originalBytes === JSON.stringify(event),
  wrong_subject_control: { component_authenticity: authenticate(event), request_binding: proposalBinding(event, flip(content.artifact_hash)) },
  boundaries: {
    signer_identity: 'UNVERIFIABLE', signer_authority: 'UNVERIFIABLE', proposal_preimage: 'NOT_CHECKED',
    trusted_time: 'UNVERIFIABLE', relay_or_chain_inclusion: 'NOT_CHECKED', execution: 'NOT_CHECKED',
    wyriwe_eip712_attestation: 'NOT_CHECKED', zkie_link: 'NOT_IMPLEMENTED', downstream_authorization: 'UNVERIFIABLE'
  }
};
report.passed = report.cases.every(c => c.passed) && report.original_event_unchanged;
process.stdout.write(JSON.stringify(report, null, 2) + '\n');
if (!report.passed) process.exitCode = 1;
