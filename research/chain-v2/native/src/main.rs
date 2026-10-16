//! Original narrow wire adapter around pinned zkIE APIs; no upstream source edits.
//! Fixed public MatMul shape (4,8,8), not a general model or a zero-knowledge claim.
use std::{env, fs, process};
use zkie_core::common::field::{Goldilocks as F, PrimeField64, XorShift64, P};
use zkie_core::common::matmul::MatmulProof;
use zkie_core::common::sumcheck::{RoundPoly, SumcheckProof};
use zkie_core::common::mle;
use zkie_ops::compose::{Store, Op, OpProof, OpShardProof, prove_shard, verify_shard, forward_shard};

const MAGIC: &[u8; 8] = b"VAGCNP2\0";

fn field_bytes(values: &[F]) -> Vec<u8> {
    values.iter().flat_map(|x| x.as_canonical_u64().to_le_bytes()).collect()
}
fn read_fields(bytes: &[u8], count: usize) -> Result<Vec<F>, String> {
    if bytes.len() != count * 8 { return Err("wrong fixed tensor size".into()); }
    bytes.chunks_exact(8).map(|b| {
        let n = u64::from_le_bytes(b.try_into().unwrap());
        if n >= P { Err("noncanonical field element".into()) } else { Ok(F::new(n)) }
    }).collect()
}
fn push_vec(out: &mut Vec<u8>, values: &[F]) {
    out.extend_from_slice(&(values.len() as u32).to_le_bytes());
    out.extend_from_slice(&field_bytes(values));
}
struct Reader<'a> { bytes: &'a [u8], offset: usize }
impl<'a> Reader<'a> {
    fn take(&mut self, n: usize) -> Result<&'a [u8], String> {
        let end = self.offset.checked_add(n).ok_or("length overflow")?;
        if end > self.bytes.len() { return Err("truncated proof".into()); }
        let result = &self.bytes[self.offset..end]; self.offset = end; Ok(result)
    }
    fn number(&mut self) -> Result<u32, String> { Ok(u32::from_le_bytes(self.take(4)?.try_into().unwrap())) }
    fn vec(&mut self, expected: usize) -> Result<Vec<F>, String> {
        if self.number()? as usize != expected { return Err("unsupported proof shape".into()); }
        read_fields(self.take(expected * 8)?, expected)
    }
}
fn encode(p: &OpShardProof) -> Result<Vec<u8>, String> {
    if p.ops.len() != 1 || !p.bound.is_empty() || !p.binds.is_empty() || p.claims.len() != 3 {
        return Err("only the fixed one-op proof is supported".into());
    }
    let OpProof::MatMul(mp, u, v, ch) = &p.ops[0] else { return Err("wrong op".into()); };
    let mut out = MAGIC.to_vec();
    push_vec(&mut out, &[*&mp.claimed]);
    push_vec(&mut out, u); push_vec(&mut out, v); push_vec(&mut out, ch);
    let rounds: Vec<F> = mp.sumcheck.rounds.iter().flat_map(|r| [r.c0, r.c1, r.c2]).collect();
    push_vec(&mut out, &rounds);
    push_vec(&mut out, &[mp.sumcheck.f_eval, mp.sumcheck.h_eval]);
    for (id, pt, ev) in &p.claims {
        out.extend_from_slice(&(*id as u32).to_le_bytes());
        push_vec(&mut out, pt); push_vec(&mut out, &[*ev]);
    }
    Ok(out)
}
fn decode(bytes: &[u8]) -> Result<OpShardProof, String> {
    let mut r = Reader { bytes, offset: 0 };
    if r.take(8)? != MAGIC { return Err("unsupported proof profile".into()); }
    let claimed = r.vec(1)?[0];
    let u = r.vec(2)?; let v = r.vec(3)?; let ch = r.vec(3)?;
    let flat = r.vec(9)?;
    let rounds = flat.chunks_exact(3).map(|x| RoundPoly { c0: x[0], c1: x[1], c2: x[2] }).collect();
    let evals = r.vec(2)?;
    let mut claims = Vec::new();
    for (id, length) in [(0, 5), (1, 6), (2, 5)] {
        if r.number()? != id { return Err("claim order differs from pinned profile".into()); }
        claims.push((id as usize, r.vec(length)?, r.vec(1)?[0]));
    }
    if r.offset != bytes.len() { return Err("trailing proof bytes".into()); }
    Ok(OpShardProof { ops: vec![OpProof::MatMul(MatmulProof { claimed,
        sumcheck: SumcheckProof { rounds, f_eval: evals[0], h_eval: evals[1] } }, u, v, ch)],
        bound: vec![], binds: vec![], claims })
}
fn execute(args: &[String]) -> Result<bool, String> {
    if args.len() < 6 { return Err("usage: prove|verify input.bin weights.bin output.bin proof.bin [public_seed]".into()); }
    let input = read_fields(&fs::read(&args[2]).map_err(|_| "input unavailable")?, 32)?;
    let weights = read_fields(&fs::read(&args[3]).map_err(|_| "weights unavailable")?, 64)?;
    let mut store = Store::new();
    let a = store.push(input); let b = store.push(weights); let c = store.push(vec![]);
    let ops = vec![Op::MatMul { a, b, c, m: 4, k: 8, n: 8 }];
    if args[1] == "prove" {
        let seed: u64 = args.get(6).ok_or("missing public seed")?.parse().map_err(|_| "invalid seed")?;
        let proof = prove_shard(&mut store, &ops, &[c], &mut XorShift64::new(seed));
        let bytes = encode(&proof)?;
        if !verify_shard(&store, &ops, &decode(&bytes)?) { return Err("generated proof did not verify".into()); }
        fs::write(&args[4], field_bytes(store.get(c))).map_err(|_| "output write failed")?;
        fs::write(&args[5], bytes).map_err(|_| "proof write failed")?;
        return Ok(true);
    }
    if args[1] != "verify" { return Err("unknown operation".into()); }
    let output = read_fields(&fs::read(&args[4]).map_err(|_| "output unavailable")?, 32)?;
    let proof = decode(&fs::read(&args[5]).map_err(|_| "proof unavailable")?)?;
    // Native verification is executed on the deserialized proof, never regenerated.
    let native = verify_shard(&store, &ops, &proof);
    forward_shard(&mut store, &ops, 0..1);
    // The declared output bytes are a separate adapter obligation: bind all values.
    let output_matches = store.get(c) == output;
    let OpProof::MatMul(mp, u, v, ch) = &proof.ops[0] else { return Err("wrong op".into()); };
    let mut ap = ch.clone(); ap.extend_from_slice(u);
    let mut bp = v.clone(); bp.extend_from_slice(ch);
    let mut cp = v.clone(); cp.extend_from_slice(u);
    let claims = vec![(a, ap.clone(), mle::eval(store.get(a), &ap)),
                      (b, bp.clone(), mle::eval(store.get(b), &bp)),
                      (c, cp.clone(), mle::eval(store.get(c), &cp))];
    let statement_matches = proof.claims == claims && mp.claimed == mle::eval(&output, &cp);
    println!("{{\"native_verified\":{native},\"output_recomputed\":{output_matches},\"statement_bound\":{statement_matches}}}");
    Ok(native && output_matches && statement_matches)
}
fn main() {
    // Panics from the pinned library indicate an unsupported/failed check, not refutation.
    let args: Vec<String> = env::args().collect();
    match std::panic::catch_unwind(|| execute(&args)) {
        Ok(Ok(true)) => process::exit(0),
        Ok(Ok(false)) => process::exit(1),
        Ok(Err(reason)) => { eprintln!("UNVERIFIABLE: {reason}"); process::exit(2); },
        Err(_) => { eprintln!("UNVERIFIABLE: native library panic"); process::exit(2); }
    }
}
