import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
import adapter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FORGE=os.environ.get('FORGE','C:/Users/msi/.foundry/bin/forge.exe' if os.name=='nt' else 'forge')
def main():
 out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True);source=(HERE/'vendor/invinoveritas/integrations/verdict-escrow/src/VerdictGatedEscrow.sol').read_text();rows=[]
 def run(label,code,witness):
  p=out/label;(p/'src').mkdir(parents=True,exist_ok=True);(p/'test').mkdir(exist_ok=True)
  (p/'src/VerdictGatedEscrow.sol').write_text(code,encoding='utf8',newline='\n');shutil.copyfile(HERE/'vendor/invinoveritas/integrations/verdict-escrow/src/BIP340.sol',p/'src/BIP340.sol');shutil.copyfile(HERE/'mutation_harness.sol',p/'test/Boundary.t.sol')
  lib=(ROOT/'build/escrow/lib/forge-std/src').as_posix();permitted=out.as_posix()
  (p/'foundry.toml').write_text('[profile.default]\nsrc="src"\ntest="test"\nsolc="0.8.26"\noptimizer=true\noptimizer_runs=200\nvia_ir=true\nffi=true\nremappings=["forge-std/='+lib+'/"]\nallow_paths=["'+lib+'"]\nfs_permissions=[{access="read-write",path="'+permitted+'"}]\n',encoding='utf8',newline='\n')
  env=dict(os.environ,LAB_PYTHON=sys.executable,LAB_BRIDGE=str(HERE/'bridge.py'),LAB_EVIDENCE_DIR=str(p/'results'),LAB_MUTATION_WITNESS=witness)
  args=[FORGE,'test','--root',str(p),'--json'];r=subprocess.run(args,env=env,capture_output=True,timeout=300)
  for s in ('stdout','stderr'):(p/(s+'.log')).write_bytes(getattr(r,s))
  (p/'command.json').write_text(json.dumps({'command':args,'exit':r.returncode,'witness':witness},indent=2)+'\n',encoding='utf8',newline='\n')
  if r.returncode:raise RuntimeError(label+' infrastructure/test failure; not a kill')
  return json.loads((p/'results/boundary.json').read_bytes())
 baseline=run('baseline-address',source,'address');primary=baseline['primary_address'];attacker=adapter.bip340.pubkey(hashlib.sha256(b'other PUBLIC LAB key').digest()).hex()
 oldcall='BIP340.verify(verifierPubkey, bytes32(sig[0:32]), bytes32(sig[32:64]), releaseDigest(id, submissionId, decisionRef))'
 specs=[('chain','chain','DOMAIN_TAG, block.chainid,','DOMAIN_TAG, uint256(8453),'),('escrow_address','address','address(this), address(this), id,','address('+primary+'), address('+primary+'), id,'),('trusted_signer','signer',oldcall,'('+oldcall+' || BIP340.verify(bytes32(0x'+attacker+'), bytes32(sig[0:32]), bytes32(sig[32:64]), releaseDigest(id, submissionId, decisionRef)))'),('replay_guard','replay','if (e.state != State.Funded) revert NotFunded();','if (false) revert NotFunded();'),('state_consumption','replay','e.state = State.Released;','/* state consumption removed */')]
 for mid,w,old,new in specs:
  row={'id':mid,'witness':w,'old':old,'new':new}
  try:
   count=source.count(old);expected=2 if mid=='replay_guard' else 1
   if count!=expected:row['classification']='NOT_APPLIED';rows.append(row);continue
   # First state guard is release; refund's independent guard remains intact.
   changed=source.replace(old,new,1);b=run(mid+'-baseline',source,w);m=run(mid+'-mutant',changed,w);r=run(mid+'-restored',source,w)
   row.update({'baseline':b,'mutant':m,'restored':r,'mutant_sha256':hashlib.sha256(changed.encode()).hexdigest(),'classification':'KILLED' if not b['negative_authorized'] and m['negative_authorized'] and m['negative_delta']==1000000 and not r['negative_authorized'] and all(x['positive'] for x in (b,m,r)) else 'SURVIVED'})
  except Exception as ex:row.update({'classification':'CRASHED','error':str(ex)})
  rows.append(row);print(mid,row['classification'],flush=True)
 report={'mutations':rows,'counts':{k:sum(r['classification']==k for r in rows) for k in ('KILLED','SURVIVED','CRASHED','NOT_APPLIED','UNVERIFIABLE')},'absent_upstream_guards':{'recipient_preimage':'NOT_APPLIED','amount_preimage':'NOT_APPLIED','global_nonce_consumption':'NOT_APPLIED','expiration':'NOT_APPLIED','revocation':'NOT_APPLIED','claim_scope':'NOT_APPLIED'},'original_source_unchanged':source==(HERE/'vendor/invinoveritas/integrations/verdict-escrow/src/VerdictGatedEscrow.sol').read_text()}
 (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n');print(json.dumps(report['counts']));return 0 if all(r['classification']=='KILLED' for r in rows) else 1
if __name__=='__main__':raise SystemExit(main())
