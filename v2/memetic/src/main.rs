//! Zero-leak Memetic MAP-Elites + 3-Tier Continuous Constant Optimization
//! over the exact <= 24-instruction autoplast register space (NM=4, NV=6, NS=4, 20 ops).
//!
//! Reads ONLY exact Rust train and val dumps (`--train-dump`, `--val-dump`).
//! Test data is never loaded. Exports exact `best.json` for post-hoc audit via `v2/strict_eval.py`.

use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::PathBuf;
use std::time::Instant;

const NM: usize = 4;
const NV: usize = 6;
const NS: usize = 4;
const MAX_LEN: usize = 24;
const PM_MAX: usize = 3;
const N_BUCKETS: usize = 5; // (w1/l1, w1/l2+, w2/l2, w2/l3, w3/l3)
const CELL_K: usize = 4;
const LEN_PENALTY: f32 = 5e-4;

// --- Fast deterministic Xoshiro256** PRNG ---

#[derive(Clone)]
struct Rng([u64; 4]);

impl Rng {
    fn new(mut seed: u64) -> Self {
        let mut s = [0u64; 4];
        for slot in &mut s {
            seed = seed.wrapping_add(0x9e3779b97f4a7c15);
            let mut z = seed;
            z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
            *slot = z ^ (z >> 31);
        }
        Rng(s)
    }

    #[inline]
    fn next_u64(&mut self) -> u64 {
        let res = (self.0[1].wrapping_mul(5)).rotate_left(7).wrapping_mul(9);
        let t = self.0[1] << 17;
        self.0[2] ^= self.0[0];
        self.0[3] ^= self.0[1];
        self.0[1] ^= self.0[2];
        self.0[0] ^= self.0[3];
        self.0[2] ^= t;
        self.0[3] = self.0[3].rotate_left(45);
        res
    }

    #[inline]
    fn below(&mut self, n: usize) -> usize {
        (self.next_u64() as usize) % n
    }

    #[inline]
    fn uniform(&mut self) -> f32 {
        ((self.next_u64() >> 40) as f32) * (1.0 / (1u64 << 24) as f32)
    }

    fn normal(&mut self) -> f32 {
        let u1 = self.uniform().max(1e-7);
        let u2 = self.uniform();
        (-2.0 * u1.ln()).sqrt() * (std::f32::consts::TAU * u2).cos()
    }
}

// --- Exact 20-op autoplast D/E/K alphabet ---

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
enum Ty {
    M,
    V,
    S,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
#[repr(u8)]
enum Op {
    Outer = 0,
    MatAdd,
    MatSub,
    MatScale,
    Transpose,
    MatMul,
    MatVec,
    VecAdd,
    VecSub,
    VecScale,
    Hadamard,
    Normalize,
    Tanh,
    Dot,
    Const,
    SAdd,
    SMul,
    Sigmoid,
    Norm,
    Recip,
}

const OPS: [Op; 20] = [
    Op::Outer,
    Op::MatAdd,
    Op::MatSub,
    Op::MatScale,
    Op::Transpose,
    Op::MatMul,
    Op::MatVec,
    Op::VecAdd,
    Op::VecSub,
    Op::VecScale,
    Op::Hadamard,
    Op::Normalize,
    Op::Tanh,
    Op::Dot,
    Op::Const,
    Op::SAdd,
    Op::SMul,
    Op::Sigmoid,
    Op::Norm,
    Op::Recip,
];

impl Op {
    #[inline]
    fn sig(self) -> (Ty, &'static [Ty]) {
        use Ty::*;
        match self {
            Op::Outer => (M, &[V, V]),
            Op::MatAdd | Op::MatSub | Op::MatMul => (M, &[M, M]),
            Op::MatScale => (M, &[S, M]),
            Op::Transpose => (M, &[M]),
            Op::MatVec => (V, &[M, V]),
            Op::VecAdd | Op::VecSub | Op::Hadamard => (V, &[V, V]),
            Op::VecScale => (V, &[S, V]),
            Op::Normalize | Op::Tanh => (V, &[V]),
            Op::Dot => (S, &[V, V]),
            Op::Const => (S, &[]),
            Op::SAdd | Op::SMul => (S, &[S, S]),
            Op::Sigmoid | Op::Recip => (S, &[S]),
            Op::Norm => (S, &[V]),
        }
    }

    fn name(self) -> &'static str {
        match self {
            Op::Outer => "Outer",
            Op::MatAdd => "MatAdd",
            Op::MatSub => "MatSub",
            Op::MatScale => "MatScale",
            Op::Transpose => "Transpose",
            Op::MatMul => "MatMul",
            Op::MatVec => "MatVec",
            Op::VecAdd => "VecAdd",
            Op::VecSub => "VecSub",
            Op::VecScale => "VecScale",
            Op::Hadamard => "Hadamard",
            Op::Normalize => "Normalize",
            Op::Tanh => "Tanh",
            Op::Dot => "Dot",
            Op::Const => "Const",
            Op::SAdd => "SAdd",
            Op::SMul => "SMul",
            Op::Sigmoid => "Sigmoid",
            Op::Norm => "Norm",
            Op::Recip => "Recip",
        }
    }
}

#[inline]
fn n_regs(ty: Ty) -> usize {
    match ty {
        Ty::M => NM,
        Ty::V => NV,
        Ty::S => NS,
    }
}

#[derive(Clone, Debug)]
struct Instr {
    op: Op,
    out: u8,
    a: u8,
    b: u8,
    c: f32,
}

#[derive(Clone, Debug)]
struct Program {
    instrs: Vec<Instr>,
}

impl Program {
    fn compact(&self) -> (Program, [bool; PM_MAX], usize, usize) {
        let n = self.instrs.len();
        let mut persist_live = [false; PM_MAX];
        persist_live[0] = true;
        let mut keep = vec![false; n];

        loop {
            keep.fill(false);
            let mut nm = [false; NM];
            let mut nv = [false; NV];
            let mut ns = [false; NS];
            for p in 0..PM_MAX {
                nm[p] = persist_live[p];
            }
            for i in (0..n).rev() {
                let ins = &self.instrs[i];
                let (ot, ins_t) = ins.op.sig();
                let needed = match ot {
                    Ty::M => nm[ins.out as usize],
                    Ty::V => nv[ins.out as usize],
                    Ty::S => ns[ins.out as usize],
                };
                if !needed {
                    continue;
                }
                keep[i] = true;
                match ot {
                    Ty::M => nm[ins.out as usize] = false,
                    Ty::V => nv[ins.out as usize] = false,
                    Ty::S => ns[ins.out as usize] = false,
                }
                if let Some(&t0) = ins_t.first() {
                    match t0 {
                        Ty::M => nm[ins.a as usize] = true,
                        Ty::V => nv[ins.a as usize] = true,
                        Ty::S => ns[ins.a as usize] = true,
                    }
                }
                if let Some(&t1) = ins_t.get(1) {
                    match t1 {
                        Ty::M => nm[ins.b as usize] = true,
                        Ty::V => nv[ins.b as usize] = true,
                        Ty::S => ns[ins.b as usize] = true,
                    }
                }
            }
            let mut changed = false;
            for p in 1..PM_MAX {
                if nm[p] && !persist_live[p] {
                    persist_live[p] = true;
                    changed = true;
                }
            }
            if !changed {
                break;
            }
        }

        let instrs: Vec<Instr> = self
            .instrs
            .iter()
            .zip(&keep)
            .filter_map(|(ins, &k)| if k { Some(ins.clone()) } else { None })
            .collect();
        let n_live = persist_live.iter().filter(|&&b| b).count();
        let mut n_written = 0usize;
        for p in 0..PM_MAX {
            if persist_live[p]
                && instrs
                    .iter()
                    .any(|ins| ins.op.sig().0 == Ty::M && ins.out as usize == p)
            {
                n_written += 1;
            }
        }
        let state_bucket = match (n_written.clamp(1, 3), n_live.clamp(1, 3)) {
            (1, 1) => 0,
            (1, _) => 1,
            (2, 2) => 2,
            (2, _) => 3,
            _ => 4,
        };
        let export_pm = if persist_live[2] {
            3
        } else if persist_live[1] {
            2
        } else {
            1
        };
        (Program { instrs }, persist_live, state_bucket, export_pm)
    }

    fn struct_hash(&self) -> u64 {
        let mut h: u64 = 0xcbf29ce484222325;
        for ins in &self.instrs {
            let v = (ins.op as u64)
                | ((ins.out as u64) << 8)
                | ((ins.a as u64) << 16)
                | ((ins.b as u64) << 24);
            h ^= v;
            h = h.wrapping_mul(0x100000001b3);
        }
        h
    }

    fn op_multiset_hash(&self) -> u64 {
        let mut counts = [0u8; 20];
        for ins in &self.instrs {
            counts[ins.op as usize] = counts[ins.op as usize].saturating_add(1);
        }
        let mut h: u64 = 0x517cc1b727220a95;
        for &c in &counts {
            h ^= c as u64;
            h = h.wrapping_mul(0x100000001b3);
        }
        h
    }

    fn const_indices(&self) -> Vec<usize> {
        self.instrs
            .iter()
            .enumerate()
            .filter_map(|(i, ins)| if ins.op == Op::Const { Some(i) } else { None })
            .collect()
    }

    fn to_json(&self, export_pm: usize) -> String {
        let body: Vec<String> = self
            .instrs
            .iter()
            .map(|ins| {
                format!(
                    "{{\"op\":\"{}\",\"out\":{},\"a\":{},\"b\":{},\"c\":{}}}",
                    ins.op.name(),
                    ins.out,
                    ins.a,
                    ins.b,
                    ins.c
                )
            })
            .collect();
        format!(
            "{{\"persist_m\":{},\"persist_v\":0,\"persist_identity\":1,\"instrs\":[{}]}}",
            export_pm,
            body.join(",")
        )
    }

    fn format_lines(&self) -> String {
        let mut out = String::new();
        for (i, ins) in self.instrs.iter().enumerate() {
            if ins.op == Op::Const {
                out.push_str(&format!(
                    "  {:2}: {:9} out={} c={:.5}\n",
                    i,
                    ins.op.name(),
                    ins.out,
                    ins.c
                ));
            } else {
                out.push_str(&format!(
                    "  {:2}: {:9} out={} a={} b={}\n",
                    i,
                    ins.op.name(),
                    ins.out,
                    ins.a,
                    ins.b
                ));
            }
        }
        out
    }
}

struct Analysis {
    live_m: Vec<[bool; NM]>,
    live_v: Vec<[bool; NV]>,
    live_s: Vec<[bool; NS]>,
    def_m: Vec<[bool; NM]>,
    def_v: Vec<[bool; NV]>,
    def_s: Vec<[bool; NS]>,
}

fn analyze(prog: &Program, persist_live: [bool; PM_MAX]) -> Analysis {
    let n = prog.instrs.len();
    let mut live_m = vec![[false; NM]; n + 1];
    let mut live_v = vec![[false; NV]; n + 1];
    let mut live_s = vec![[false; NS]; n + 1];
    for p in 0..PM_MAX {
        live_m[n][p] = persist_live[p];
    }
    for i in (0..n).rev() {
        live_m[i] = live_m[i + 1];
        live_v[i] = live_v[i + 1];
        live_s[i] = live_s[i + 1];
        let ins = &prog.instrs[i];
        let (ot, ins_t) = ins.op.sig();
        match ot {
            Ty::M => live_m[i][ins.out as usize] = false,
            Ty::V => live_v[i][ins.out as usize] = false,
            Ty::S => live_s[i][ins.out as usize] = false,
        }
        if let Some(&t0) = ins_t.first() {
            match t0 {
                Ty::M => live_m[i][ins.a as usize] = true,
                Ty::V => live_v[i][ins.a as usize] = true,
                Ty::S => live_s[i][ins.a as usize] = true,
            }
        }
        if let Some(&t1) = ins_t.get(1) {
            match t1 {
                Ty::M => live_m[i][ins.b as usize] = true,
                Ty::V => live_v[i][ins.b as usize] = true,
                Ty::S => live_s[i][ins.b as usize] = true,
            }
        }
    }

    let mut def_m = vec![[false; NM]; n + 1];
    let mut def_v = vec![[false; NV]; n + 1];
    let mut def_s = vec![[false; NS]; n + 1];
    for p in 0..PM_MAX {
        def_m[0][p] = true;
    }
    def_v[0][0] = true;
    def_v[0][1] = true;
    for i in 0..n {
        def_m[i + 1] = def_m[i];
        def_v[i + 1] = def_v[i];
        def_s[i + 1] = def_s[i];
        let ins = &prog.instrs[i];
        let (ot, _) = ins.op.sig();
        match ot {
            Ty::M => def_m[i + 1][ins.out as usize] = true,
            Ty::V => def_v[i + 1][ins.out as usize] = true,
            Ty::S => def_s[i + 1][ins.out as usize] = true,
        }
    }
    Analysis {
        live_m,
        live_v,
        live_s,
        def_m,
        def_v,
        def_s,
    }
}

// --- Exact Rust JSON Task Dump Loader ---

struct Episode {
    writes: Vec<(usize, usize)>,
    queries: Vec<(usize, usize)>,
}

struct Task {
    d: usize,
    n_vals: usize,
    keys: Vec<f32>,
    vals: Vec<f32>,
    episodes: Vec<Episode>,
}

impl Task {
    #[inline]
    fn key(&self, i: usize) -> &[f32] {
        &self.keys[i * self.d..(i + 1) * self.d]
    }
    #[inline]
    fn val(&self, i: usize) -> &[f32] {
        &self.vals[i * self.d..(i + 1) * self.d]
    }

    fn load_json(path: &str) -> Self {
        let s = fs::read_to_string(path).expect("read task dump");
        let b = s.as_bytes();
        let mut i = 0usize;

        fn skip_ws(b: &[u8], i: &mut usize) {
            while *i < b.len() && matches!(b[*i], b' ' | b'\n' | b'\r' | b'\t') {
                *i += 1;
            }
        }
        fn parse_f32(b: &[u8], i: &mut usize) -> f32 {
            skip_ws(b, i);
            let st = *i;
            while *i < b.len()
                && (b[*i].is_ascii_digit()
                    || matches!(b[*i], b'-' | b'+' | b'.' | b'e' | b'E'))
            {
                *i += 1;
            }
            std::str::from_utf8(&b[st..*i]).unwrap().parse().unwrap()
        }
        fn parse_usize(b: &[u8], i: &mut usize) -> usize {
            skip_ws(b, i);
            let st = *i;
            while *i < b.len() && b[*i].is_ascii_digit() {
                *i += 1;
            }
            std::str::from_utf8(&b[st..*i]).unwrap().parse().unwrap()
        }
        fn parse_str<'a>(b: &'a [u8], i: &mut usize) -> &'a str {
            skip_ws(b, i);
            assert_eq!(b[*i], b'"');
            *i += 1;
            let st = *i;
            while b[*i] != b'"' {
                *i += 1;
            }
            let res = std::str::from_utf8(&b[st..*i]).unwrap();
            *i += 1;
            res
        }
        fn parse_f32_arr(b: &[u8], i: &mut usize) -> Vec<f32> {
            skip_ws(b, i);
            assert_eq!(b[*i], b'[');
            *i += 1;
            let mut out = Vec::new();
            loop {
                skip_ws(b, i);
                if b[*i] == b']' {
                    *i += 1;
                    return out;
                }
                out.push(parse_f32(b, i));
                skip_ws(b, i);
                if b[*i] == b',' {
                    *i += 1;
                }
            }
        }
        fn parse_pairs(b: &[u8], i: &mut usize) -> Vec<(usize, usize)> {
            skip_ws(b, i);
            assert_eq!(b[*i], b'[');
            *i += 1;
            let mut out = Vec::new();
            loop {
                skip_ws(b, i);
                if b[*i] == b']' {
                    *i += 1;
                    return out;
                }
                assert_eq!(b[*i], b'[');
                *i += 1;
                let k = parse_usize(b, i);
                skip_ws(b, i);
                assert_eq!(b[*i], b',');
                *i += 1;
                let v = parse_usize(b, i);
                skip_ws(b, i);
                assert_eq!(b[*i], b']');
                *i += 1;
                out.push((k, v));
                skip_ws(b, i);
                if b[*i] == b',' {
                    *i += 1;
                }
            }
        }

        let mut d = 0usize;
        let mut keys = Vec::new();
        let mut vals = Vec::new();
        let mut episodes = Vec::new();

        skip_ws(b, &mut i);
        assert_eq!(b[i], b'{');
        i += 1;
        loop {
            skip_ws(b, &mut i);
            if b[i] == b'}' {
                break;
            }
            let key = parse_str(b, &mut i);
            skip_ws(b, &mut i);
            assert_eq!(b[i], b':');
            i += 1;
            match key {
                "d" => d = parse_usize(b, &mut i),
                "keys" => keys = parse_f32_arr(b, &mut i),
                "vals" => vals = parse_f32_arr(b, &mut i),
                "episodes" => {
                    skip_ws(b, &mut i);
                    assert_eq!(b[i], b'[');
                    i += 1;
                    loop {
                        skip_ws(b, &mut i);
                        if b[i] == b']' {
                            i += 1;
                            break;
                        }
                        assert_eq!(b[i], b'{');
                        i += 1;
                        let mut writes = Vec::new();
                        let mut queries = Vec::new();
                        loop {
                            skip_ws(b, &mut i);
                            if b[i] == b'}' {
                                i += 1;
                                break;
                            }
                            let ek = parse_str(b, &mut i);
                            skip_ws(b, &mut i);
                            assert_eq!(b[i], b':');
                            i += 1;
                            match ek {
                                "w" => writes = parse_pairs(b, &mut i),
                                "q" => queries = parse_pairs(b, &mut i),
                                "qv" => {
                                    let _ = parse_f32_arr(b, &mut i);
                                }
                                _ => panic!("unexpected episode key {ek}"),
                            }
                            skip_ws(b, &mut i);
                            if b[i] == b',' {
                                i += 1;
                            }
                        }
                        episodes.push(Episode { writes, queries });
                        skip_ws(b, &mut i);
                        if b[i] == b',' {
                            i += 1;
                        }
                    }
                }
                _ => panic!("unexpected top key {key}"),
            }
            skip_ws(b, &mut i);
            if b[i] == b',' {
                i += 1;
            }
        }
        let n_vals = vals.len() / d;
        Task {
            d,
            n_vals,
            keys,
            vals,
            episodes,
        }
    }

    fn subset(&self, max_short: usize, max_long: usize) -> Vec<usize> {
        let mut idxs = Vec::new();
        let (mut ns, mut nl) = (0, 0);
        for (i, ep) in self.episodes.iter().enumerate() {
            if ep.writes.len() <= 24 {
                if ns < max_short {
                    idxs.push(i);
                    ns += 1;
                }
            } else if nl < max_long {
                idxs.push(i);
                nl += 1;
            }
        }
        if idxs.is_empty() {
            return (0..self.episodes.len().min(16)).collect();
        }
        idxs
    }
}

// --- Ultra-fast stack-allocated fixed-size D=16 register file (LLVM auto-vectorized) ---

const D16: usize = 16;
const D16SQ: usize = 256;

struct Regs16 {
    m: [[f32; D16SQ]; NM],
    v: [[f32; D16]; NV],
    s: [f32; NS],
    tm: [f32; D16SQ],
    tv: [f32; D16],
}

impl Regs16 {
    fn new() -> Self {
        Regs16 {
            m: [[0.0; D16SQ]; NM],
            v: [[0.0; D16]; NV],
            s: [0.0; NS],
            tm: [0.0; D16SQ],
            tv: [0.0; D16],
        }
    }

    #[inline(always)]
    fn reset_episode(&mut self, pm: usize) {
        self.m[0] = [0.0; D16SQ];
        for p in 1..NM {
            self.m[p] = [0.0; D16SQ];
            if p < pm {
                for i in 0..D16 {
                    self.m[p][i * D16 + i] = 1.0;
                }
            }
        }
    }

    #[inline(always)]
    fn step(&mut self, prog: &Program, k: &[f32], v: &[f32], pm: usize) -> bool {
        for r in pm..NM {
            self.m[r] = [0.0; D16SQ];
        }
        self.v[0].copy_from_slice(k);
        self.v[1].copy_from_slice(v);
        for r in 2..NV {
            self.v[r] = [0.0; D16];
        }
        self.s = [0.0; NS];

        for ins in &prog.instrs {
            let (o, a, b) = (ins.out as usize, ins.a as usize, ins.b as usize);
            match ins.op {
                Op::Outer => {
                    let va = self.v[a];
                    let vb = self.v[b];
                    for i in 0..D16 {
                        let vai = va[i];
                        let base = i * D16;
                        for j in 0..D16 {
                            self.m[o][base + j] = vai * vb[j];
                        }
                    }
                }
                Op::MatAdd => {
                    for idx in 0..D16SQ {
                        self.tm[idx] = self.m[a][idx] + self.m[b][idx];
                    }
                    self.m[o] = self.tm;
                }
                Op::MatSub => {
                    for idx in 0..D16SQ {
                        self.tm[idx] = self.m[a][idx] - self.m[b][idx];
                    }
                    self.m[o] = self.tm;
                }
                Op::MatScale => {
                    let sc = self.s[a];
                    for idx in 0..D16SQ {
                        self.tm[idx] = sc * self.m[b][idx];
                    }
                    self.m[o] = self.tm;
                }
                Op::Transpose => {
                    for i in 0..D16 {
                        for j in 0..D16 {
                            self.tm[i * D16 + j] = self.m[a][j * D16 + i];
                        }
                    }
                    self.m[o] = self.tm;
                }
                Op::MatMul => {
                    self.tm = [0.0; D16SQ];
                    for i in 0..D16 {
                        let ib = i * D16;
                        for kk in 0..D16 {
                            let aik = self.m[a][ib + kk];
                            let kb = kk * D16;
                            for j in 0..D16 {
                                self.tm[ib + j] += aik * self.m[b][kb + j];
                            }
                        }
                    }
                    self.m[o] = self.tm;
                }
                Op::MatVec => {
                    let vb = self.v[b];
                    for i in 0..D16 {
                        let ib = i * D16;
                        let mut sum = 0.0f32;
                        for j in 0..D16 {
                            sum += self.m[a][ib + j] * vb[j];
                        }
                        self.tv[i] = sum;
                    }
                    self.v[o] = self.tv;
                }
                Op::VecAdd => {
                    for i in 0..D16 {
                        self.tv[i] = self.v[a][i] + self.v[b][i];
                    }
                    self.v[o] = self.tv;
                }
                Op::VecSub => {
                    for i in 0..D16 {
                        self.tv[i] = self.v[a][i] - self.v[b][i];
                    }
                    self.v[o] = self.tv;
                }
                Op::VecScale => {
                    let sc = self.s[a];
                    for i in 0..D16 {
                        self.tv[i] = sc * self.v[b][i];
                    }
                    self.v[o] = self.tv;
                }
                Op::Hadamard => {
                    for i in 0..D16 {
                        self.tv[i] = self.v[a][i] * self.v[b][i];
                    }
                    self.v[o] = self.tv;
                }
                Op::Normalize => {
                    let mut ss = 0.0f32;
                    for i in 0..D16 {
                        ss += self.v[a][i] * self.v[a][i];
                    }
                    let inv = 1.0 / (ss.sqrt() + 1e-6);
                    for i in 0..D16 {
                        self.tv[i] = self.v[a][i] * inv;
                    }
                    self.v[o] = self.tv;
                }
                Op::Tanh => {
                    for i in 0..D16 {
                        self.tv[i] = self.v[a][i].tanh();
                    }
                    self.v[o] = self.tv;
                }
                Op::Dot => {
                    let mut sum = 0.0f32;
                    for i in 0..D16 {
                        sum += self.v[a][i] * self.v[b][i];
                    }
                    self.s[o] = sum;
                }
                Op::Const => {
                    self.s[o] = ins.c;
                }
                Op::SAdd => {
                    self.s[o] = self.s[a] + self.s[b];
                }
                Op::SMul => {
                    self.s[o] = self.s[a] * self.s[b];
                }
                Op::Sigmoid => {
                    let x = self.s[a].clamp(-40.0, 40.0);
                    self.s[o] = 1.0 / (1.0 + (-x).exp());
                }
                Op::Norm => {
                    let mut ss = 0.0f32;
                    for i in 0..D16 {
                        ss += self.v[a][i] * self.v[a][i];
                    }
                    self.s[o] = ss.sqrt();
                }
                Op::Recip => {
                    let x = self.s[a];
                    self.s[o] = x / (x * x + 1e-6);
                }
            }
        }

        for p in 0..pm {
            for &x in &self.m[p] {
                if !x.is_finite() || x.abs() > 1e3 {
                    return false;
                }
            }
        }
        true
    }
}

#[derive(Clone, Copy, Debug)]
struct EvalMetrics {
    obj: f32, // mse + st_l2 * mean(st^2) + LEN_PENALTY * len
    mse: f32,
    acc: f32,
    max_st: f32,
}

impl EvalMetrics {
    fn inf() -> Self {
        EvalMetrics {
            obj: f32::INFINITY,
            mse: f32::INFINITY,
            acc: 0.0,
            max_st: f32::INFINITY,
        }
    }
}

fn eval_program(
    prog: &Program,
    pm: usize,
    task: &Task,
    ep_indices: Option<&[usize]>,
    regs: &mut Regs16,
    st_l2: f32,
    compute_acc: bool,
) -> EvalMetrics {
    assert_eq!(task.d, D16, "Regs16 expects d=16");
    let mut o = [0.0f32; D16];
    let mut mse_sum = 0.0f32;
    let mut tot_q = 0usize;
    let mut cor_q = 0usize;
    let mut l2_ep_sum = 0.0f32;
    let mut max_st = 0.0f32;
    let n_eps = ep_indices.map(|s| s.len()).unwrap_or(task.episodes.len());
    let inv_pm_d2 = 1.0 / (pm * D16SQ) as f32;

    for idx_pos in 0..n_eps {
        let ei = ep_indices.map(|s| s[idx_pos]).unwrap_or(idx_pos);
        let ep = &task.episodes[ei];
        regs.reset_episode(pm);
        let mut ep_l2 = 0.0f32;
        for &(kid, vid) in &ep.writes {
            if !regs.step(prog, task.key(kid), task.val(vid), pm) {
                return EvalMetrics::inf();
            }
            let mut step_sq = 0.0f32;
            for p in 0..pm {
                for &x in &regs.m[p] {
                    let ax = x.abs();
                    if ax > max_st {
                        max_st = ax;
                    }
                    step_sq += x * x;
                }
            }
            ep_l2 += step_sq * inv_pm_d2;
        }
        l2_ep_sum += ep_l2 / ep.writes.len().max(1) as f32;

        let s_mem = &regs.m[0];
        for &(kid, target) in &ep.queries {
            let q = task.key(kid);
            let tv = task.val(target);
            let mut sq = 0.0f32;
            let mut onorm2 = 0.0f32;
            for i in 0..D16 {
                let ib = i * D16;
                let mut sum = 0.0f32;
                for j in 0..D16 {
                    sum += s_mem[ib + j] * q[j];
                }
                o[i] = sum;
                let diff = sum - tv[i];
                sq += diff * diff;
                onorm2 += sum * sum;
            }
            if !sq.is_finite() {
                return EvalMetrics::inf();
            }
            mse_sum += sq;
            tot_q += 1;

            if compute_acc && onorm2 > 1e-12 {
                let mut best = f32::NEG_INFINITY;
                let mut best_id = usize::MAX;
                for j in 0..task.n_vals {
                    let vj = task.val(j);
                    let mut sc = 0.0f32;
                    for i in 0..D16 {
                        sc += vj[i] * o[i];
                    }
                    if sc > best {
                        best = sc;
                        best_id = j;
                    }
                }
                if best_id == target {
                    cor_q += 1;
                }
            }
        }
    }

    let mse = mse_sum / tot_q.max(1) as f32;
    let l2_mean = l2_ep_sum / n_eps.max(1) as f32;
    let obj = mse + st_l2 * l2_mean + LEN_PENALTY * prog.instrs.len() as f32;
    if !obj.is_finite() {
        return EvalMetrics::inf();
    }
    EvalMetrics {
        obj,
        mse,
        acc: cor_q as f32 / tot_q.max(1) as f32,
        max_st,
    }
}

// --- 3-Tier Multi-Scale Continuous Constant Optimizer ---

/// Tier 0: 1 micro-eval (12 eps), plus 5-point 1D probe ONLY when a constant was added/changed or eval diverged.
fn quick_screen_1d(
    prog: &mut Program,
    pm: usize,
    task: &Task,
    sub: &[usize],
    regs: &mut Regs16,
    st_l2: f32,
    focus_const: Option<usize>,
) -> EvalMetrics {
    let mut best = eval_program(prog, pm, task, Some(sub), regs, st_l2, false);
    let cidx = prog.const_indices();
    if cidx.is_empty() || (focus_const.is_none() && best.obj.is_finite()) {
        return best;
    }
    let ci = focus_const
        .filter(|&i| i < prog.instrs.len() && prog.instrs[i].op == Op::Const)
        .unwrap_or(*cidx.last().unwrap());
    let mut best_c = prog.instrs[ci].c;
    for &probe in &[0.005f32, 0.05, 0.5, -0.05, -0.5] {
        prog.instrs[ci].c = probe;
        let m = eval_program(prog, pm, task, Some(sub), regs, st_l2, false);
        if m.obj + 1e-6 < best.obj {
            best = m;
            best_c = probe;
        }
    }
    prog.instrs[ci].c = best_c;
    best
}

/// Tier 1 (fast=true) & Tier 2 (full_polish=true): Multi-scale coordinate + Nelder-Mead.
fn tune_constants(
    prog: &mut Program,
    pm: usize,
    task: &Task,
    ep_indices: Option<&[usize]>,
    regs: &mut Regs16,
    st_l2: f32,
    full_polish: bool,
) -> EvalMetrics {
    let cidx = prog.const_indices();
    let mut best = eval_program(prog, pm, task, ep_indices, regs, st_l2, false);
    if cidx.is_empty() {
        return best;
    }

    if !best.obj.is_finite() || best.obj > 1.2 {
        let orig: Vec<f32> = cidx.iter().map(|&i| prog.instrs[i].c).collect();
        for &scale in &[0.1f32, 0.01, -0.1, 0.5] {
            for (&ci, &ov) in cidx.iter().zip(&orig) {
                prog.instrs[ci].c = ov * scale;
            }
            let m = eval_program(prog, pm, task, ep_indices, regs, st_l2, false);
            if m.obj < best.obj {
                best = m;
            }
        }
        if !best.obj.is_finite() {
            return best;
        }
    }

    let sweeps = if full_polish { 3 } else { 1 };
    let steps: &[f32] = if full_polish {
        &[0.4, 0.12, 0.035, 0.01, 0.0025]
    } else {
        &[0.3, 0.07, 0.015]
    };

    for sw in 0..sweeps {
        let mut improved_sweep = false;
        for &ci in &cidx {
            let mut c0 = prog.instrs[ci].c;
            if sw == 0 {
                let probes = if c0.abs() < 0.05 {
                    [0.002, 0.01, 0.05, 0.3, -0.01, -0.3]
                } else {
                    [c0 * 0.1, c0 * 0.35, c0 * 0.7, c0 * 1.5, c0 * 2.5, -c0]
                };
                for p in probes {
                    prog.instrs[ci].c = p;
                    let m = eval_program(prog, pm, task, ep_indices, regs, st_l2, false);
                    if m.obj + 1e-6 < best.obj {
                        best = m;
                        c0 = p;
                        improved_sweep = true;
                    }
                }
                prog.instrs[ci].c = c0;
            }
            for &st in steps {
                let mut moved = false;
                for &dir in &[1.0f32, -1.0f32] {
                    let cand = c0 + dir * st;
                    prog.instrs[ci].c = cand;
                    let m = eval_program(prog, pm, task, ep_indices, regs, st_l2, false);
                    if m.obj + 1e-6 < best.obj {
                        best = m;
                        c0 = cand;
                        moved = true;
                        improved_sweep = true;
                        break;
                    }
                }
                if !moved {
                    prog.instrs[ci].c = c0;
                }
            }
        }
        if !improved_sweep {
            break;
        }
    }

    // Joint Nelder-Mead polish on full_polish (or small k in Tier 1).
    let k = cidx.len();
    if full_polish && k >= 2 && k <= 8 {
        let max_iter = 22 * k;
        let mut x0: Vec<f32> = cidx.iter().map(|&i| prog.instrs[i].c).collect();
        let mut eval_vec = |xs: &[f32]| -> EvalMetrics {
            for (&ci, &xv) in cidx.iter().zip(xs) {
                prog.instrs[ci].c = xv;
            }
            eval_program(prog, pm, task, ep_indices, regs, st_l2, false)
        };

        let mut simplex: Vec<(Vec<f32>, EvalMetrics)> = Vec::with_capacity(k + 1);
        simplex.push((x0.clone(), best));
        for j in 0..k {
            let mut xj = x0.clone();
            let delta = (0.15 * xj[j].abs()).max(0.008);
            xj[j] += delta;
            let mj = eval_vec(&xj);
            simplex.push((xj, mj));
        }

        for _ in 0..max_iter {
            simplex.sort_by(|a, b| a.1.obj.total_cmp(&b.1.obj));
            if simplex[k].1.obj - simplex[0].1.obj < 1e-5 {
                break;
            }
            let mut cen = vec![0.0f32; k];
            for v in &simplex[..k] {
                for j in 0..k {
                    cen[j] += v.0[j];
                }
            }
            for j in 0..k {
                cen[j] /= k as f32;
            }

            let xr: Vec<f32> = (0..k).map(|j| cen[j] + (cen[j] - simplex[k].0[j])).collect();
            let fr = eval_vec(&xr);
            if fr.obj < simplex[0].1.obj {
                let xe: Vec<f32> = (0..k).map(|j| cen[j] + 2.0 * (xr[j] - cen[j])).collect();
                let fe = eval_vec(&xe);
                if fe.obj < fr.obj {
                    simplex[k] = (xe, fe);
                } else {
                    simplex[k] = (xr, fr);
                }
            } else if fr.obj < simplex[k - 1].1.obj {
                simplex[k] = (xr, fr);
            } else {
                let xc: Vec<f32> = if fr.obj < simplex[k].1.obj {
                    (0..k).map(|j| cen[j] + 0.5 * (xr[j] - cen[j])).collect()
                } else {
                    (0..k).map(|j| cen[j] + 0.5 * (simplex[k].0[j] - cen[j])).collect()
                };
                let fc = eval_vec(&xc);
                if fc.obj < fr.obj.min(simplex[k].1.obj) {
                    simplex[k] = (xc, fc);
                } else {
                    let best_v = simplex[0].0.clone();
                    for v in &mut simplex[1..] {
                        for j in 0..k {
                            v.0[j] = best_v[j] + 0.5 * (v.0[j] - best_v[j]);
                        }
                        v.1 = eval_vec(&v.0);
                    }
                }
            }
        }
        simplex.sort_by(|a, b| a.1.obj.total_cmp(&b.1.obj));
        if simplex[0].1.obj < best.obj {
            best = simplex[0].1;
            x0 = simplex[0].0.clone();
        }
        for (&ci, &xv) in cidx.iter().zip(&x0) {
            prog.instrs[ci].c = xv;
        }
    }
    best
}

// --- Generic, Liveness-Aware Program Mutations ---

fn pick_defined_reg(rng: &mut Rng, an: &Analysis, pos: usize, ty: Ty) -> u8 {
    let mut cands = [0u8; 6];
    let mut n = 0usize;
    match ty {
        Ty::M => {
            for r in 0..NM {
                if an.def_m[pos][r] {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
        Ty::V => {
            for r in 0..NV {
                if an.def_v[pos][r] {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
        Ty::S => {
            for r in 0..NS {
                if an.def_s[pos][r] {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
    }
    if n == 0 {
        rng.below(n_regs(ty)) as u8
    } else {
        cands[rng.below(n)]
    }
}

fn pick_dead_reg(rng: &mut Rng, an: &Analysis, pos: usize, ty: Ty, exclude: Option<u8>) -> Option<u8> {
    let mut cands = [0u8; 6];
    let mut n = 0usize;
    match ty {
        Ty::M => {
            for r in 0..NM {
                if !an.live_m[pos][r] && exclude != Some(r as u8) {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
        Ty::V => {
            for r in 0..NV {
                if !an.live_v[pos][r] && exclude != Some(r as u8) {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
        Ty::S => {
            for r in 0..NS {
                if !an.live_s[pos][r] && exclude != Some(r as u8) {
                    cands[n] = r as u8;
                    n += 1;
                }
            }
        }
    }
    if n == 0 {
        None
    } else {
        Some(cands[rng.below(n)])
    }
}

fn random_const(rng: &mut Rng) -> f32 {
    let u = rng.uniform();
    let sign = if rng.below(2) == 0 { 1.0 } else { -1.0 };
    if u < 0.4 {
        sign * 10.0f32.powf(-3.0 + 2.0 * rng.uniform())
    } else {
        rng.uniform() * 3.0 - 1.5
    }
}

fn random_instr_at(rng: &mut Rng, an: &Analysis, pos: usize, force_ty: Option<Ty>, force_out: Option<u8>) -> Instr {
    let ops: Vec<Op> = match force_ty {
        Some(t) => OPS.iter().copied().filter(|o| o.sig().0 == t).collect(),
        None => OPS.to_vec(),
    };
    let op = ops[rng.below(ops.len())];
    let (ot, ins_t) = op.sig();
    let out = force_out.unwrap_or_else(|| {
        if rng.uniform() < 0.6 {
            pick_dead_reg(rng, an, pos, ot, None).unwrap_or_else(|| rng.below(n_regs(ot)) as u8)
        } else {
            rng.below(n_regs(ot)) as u8
        }
    });
    let a = ins_t.first().map(|&t| pick_defined_reg(rng, an, pos, t)).unwrap_or(0);
    let b = ins_t.get(1).map(|&t| pick_defined_reg(rng, an, pos, t)).unwrap_or(0);
    Instr {
        op,
        out,
        a,
        b,
        c: random_const(rng),
    }
}

fn residual_insert_once(prog: &mut Program, rng: &mut Rng, persist_live: [bool; PM_MAX]) -> Option<usize> {
    let n = prog.instrs.len();
    if n + 2 > MAX_LEN {
        return None;
    }
    let an = analyze(prog, persist_live);
    let pos = rng.below(n + 1);

    let mut targets: Vec<(Ty, u8)> = Vec::new();
    for r in 0..NM {
        if an.def_m[pos][r] && (an.live_m[pos][r] || r < PM_MAX) {
            targets.push((Ty::M, r as u8));
        }
    }
    for r in 0..NV {
        if an.def_v[pos][r] && an.live_v[pos][r] {
            targets.push((Ty::V, r as u8));
        }
    }
    for r in 0..NS {
        if an.def_s[pos][r] && an.live_s[pos][r] {
            targets.push((Ty::S, r as u8));
        }
    }
    if targets.is_empty() {
        return None;
    }
    let (ty, target) = targets[rng.below(targets.len())];
    let tmp = pick_dead_reg(rng, &an, pos, ty, Some(target))?;

    let op_ins = random_instr_at(rng, &an, pos, Some(ty), Some(tmp));
    let use_scale = n + 4 <= MAX_LEN && rng.uniform() < 0.75;
    let sc_reg = if use_scale {
        pick_dead_reg(rng, &an, pos, Ty::S, if ty == Ty::S { Some(tmp) } else { None })
    } else {
        None
    };

    let mut block = Vec::with_capacity(4);
    block.push(op_ins);
    let mut focus = None;
    if let Some(sc) = sc_reg {
        let sign = if rng.below(2) == 0 { 1.0 } else { -1.0 };
        let c0 = sign * (0.02 + 0.08 * rng.uniform());
        focus = Some(pos + block.len());
        block.push(Instr { op: Op::Const, out: sc, a: 0, b: 0, c: c0 });
        let scale_op = match ty {
            Ty::M => Op::MatScale,
            Ty::V => Op::VecScale,
            Ty::S => Op::SMul,
        };
        block.push(Instr { op: scale_op, out: tmp, a: sc, b: tmp, c: 0.0 });
    }
    let add_op = match (ty, rng.below(2) == 0) {
        (Ty::M, true) => Op::MatAdd,
        (Ty::M, false) => Op::MatSub,
        (Ty::V, true) => Op::VecAdd,
        (Ty::V, false) => Op::VecSub,
        (Ty::S, _) => Op::SAdd,
    };
    block.push(Instr { op: add_op, out: target, a: target, b: tmp, c: 0.0 });
    prog.instrs.splice(pos..pos, block);
    Some(focus.unwrap_or(pos))
}

fn chain_residual_insert(prog: &mut Program, rng: &mut Rng, persist_live: [bool; PM_MAX]) -> Option<usize> {
    let n = prog.instrs.len();
    if n + 3 > MAX_LEN {
        return None;
    }
    let an = analyze(prog, persist_live);
    let pos = rng.below(n + 1);

    let h_ty = if rng.below(2) == 0 { Ty::V } else { Ty::S };
    let h_reg = pick_dead_reg(rng, &an, pos, h_ty, None)?;
    let helper_ins = random_instr_at(rng, &an, pos, Some(h_ty), Some(h_reg));

    let mut targets: Vec<(Ty, u8)> = Vec::new();
    for r in 0..NM {
        if an.def_m[pos][r] && (an.live_m[pos][r] || r < PM_MAX) {
            targets.push((Ty::M, r as u8));
        }
    }
    for r in 0..NV {
        if an.def_v[pos][r] && an.live_v[pos][r] {
            targets.push((Ty::V, r as u8));
        }
    }
    for r in 0..NS {
        if an.def_s[pos][r] && an.live_s[pos][r] {
            targets.push((Ty::S, r as u8));
        }
    }
    if targets.is_empty() {
        return None;
    }
    let (ty, target) = targets[rng.below(targets.len())];
    let tmp = pick_dead_reg(
        rng,
        &an,
        pos,
        ty,
        if ty == h_ty { Some(h_reg) } else { Some(target) },
    )?;
    if tmp == target || (ty == h_ty && tmp == h_reg) {
        return None;
    }

    let compat_ops: Vec<Op> = OPS
        .iter()
        .copied()
        .filter(|o| {
            let (ot, ins) = o.sig();
            ot == ty && ins.contains(&h_ty)
        })
        .collect();
    if compat_ops.is_empty() {
        return None;
    }
    let op2 = compat_ops[rng.below(compat_ops.len())];
    let (_, ins2) = op2.sig();
    let mut a2 = ins2.first().map(|&t| pick_defined_reg(rng, &an, pos, t)).unwrap_or(0);
    let mut b2 = ins2.get(1).map(|&t| pick_defined_reg(rng, &an, pos, t)).unwrap_or(0);
    if ins2.len() == 1 {
        a2 = h_reg;
    } else if ins2[0] == h_ty && ins2[1] == h_ty {
        match rng.below(3) {
            0 => a2 = h_reg,
            1 => b2 = h_reg,
            _ => {
                a2 = h_reg;
                b2 = h_reg;
            }
        }
    } else if ins2[0] == h_ty {
        a2 = h_reg;
    } else {
        b2 = h_reg;
    }

    let mut block = Vec::with_capacity(5);
    block.push(helper_ins);
    block.push(Instr { op: op2, out: tmp, a: a2, b: b2, c: 0.0 });

    let use_scale = n + 5 <= MAX_LEN && rng.uniform() < 0.7;
    let sc_reg = if use_scale {
        pick_dead_reg(
            rng,
            &an,
            pos,
            Ty::S,
            if h_ty == Ty::S { Some(h_reg) } else if ty == Ty::S { Some(tmp) } else { None },
        )
    } else {
        None
    };
    let mut focus = None;
    if let Some(sc) = sc_reg {
        let sign = if rng.below(2) == 0 { 1.0 } else { -1.0 };
        let c0 = sign * (0.02 + 0.08 * rng.uniform());
        focus = Some(pos + block.len());
        block.push(Instr { op: Op::Const, out: sc, a: 0, b: 0, c: c0 });
        let scale_op = match ty {
            Ty::M => Op::MatScale,
            Ty::V => Op::VecScale,
            Ty::S => Op::SMul,
        };
        block.push(Instr { op: scale_op, out: tmp, a: sc, b: tmp, c: 0.0 });
    }
    let add_op = match (ty, rng.below(2) == 0) {
        (Ty::M, true) => Op::MatAdd,
        (Ty::M, false) => Op::MatSub,
        (Ty::V, true) => Op::VecAdd,
        (Ty::V, false) => Op::VecSub,
        (Ty::S, _) => Op::SAdd,
    };
    block.push(Instr { op: add_op, out: target, a: target, b: tmp, c: 0.0 });
    prog.instrs.splice(pos..pos, block);
    Some(focus.unwrap_or(pos))
}

fn wrap_input_mutate(prog: &mut Program, rng: &mut Rng, persist_live: [bool; PM_MAX]) -> Option<usize> {
    let n = prog.instrs.len();
    if n == 0 || n + 1 > MAX_LEN {
        return None;
    }
    let an = analyze(prog, persist_live);
    let pos = rng.below(n);
    let (_, ins_t) = prog.instrs[pos].op.sig();
    if ins_t.is_empty() {
        return None;
    }
    let use_b = ins_t.len() == 2 && rng.below(2) == 1;
    let in_ty = if use_b { ins_t[1] } else { ins_t[0] };
    let old_r = if use_b { prog.instrs[pos].b } else { prog.instrs[pos].a };

    let new_r = pick_dead_reg(rng, &an, pos, in_ty, Some(old_r))?;
    let compat: Vec<Op> = OPS
        .iter()
        .copied()
        .filter(|o| {
            let (ot, it) = o.sig();
            ot == in_ty && it.contains(&in_ty)
        })
        .collect();
    if compat.is_empty() {
        return None;
    }
    let op = compat[rng.below(compat.len())];
    let (_, it) = op.sig();
    let mut a = it.first().map(|&t| pick_defined_reg(rng, &an, pos, t)).unwrap_or(0);
    let mut b = it.get(1).map(|&t| pick_defined_reg(rng, &an, pos, t)).unwrap_or(0);
    if it.len() == 1 {
        a = old_r;
    } else if it[0] == in_ty && it[1] == in_ty {
        if rng.below(2) == 0 {
            a = old_r;
        } else {
            b = old_r;
        }
    } else if it[0] == in_ty {
        a = old_r;
    } else {
        b = old_r;
    }

    let mut inserted = Vec::with_capacity(2);
    let mut focus = None;
    if matches!(op, Op::SAdd | Op::SMul | Op::VecScale | Op::MatScale)
        && n + 2 <= MAX_LEN
        && rng.uniform() < 0.6
    {
        if let Some(sc) = pick_dead_reg(rng, &an, pos, Ty::S, Some(new_r)) {
            let cval = if op == Op::SAdd {
                0.01 * (1.0 + 4.0 * rng.uniform())
            } else {
                0.5 + rng.uniform()
            };
            focus = Some(pos);
            inserted.push(Instr { op: Op::Const, out: sc, a: 0, b: 0, c: cval });
            if it[0] == Ty::S && !(in_ty == Ty::S && a == old_r) {
                a = sc;
            } else if it.len() == 2 && it[1] == Ty::S {
                b = sc;
            }
        }
    }
    inserted.push(Instr { op, out: new_r, a, b, c: 0.0 });
    let shift = inserted.len();
    prog.instrs.splice(pos..pos, inserted);

    let rewire_all = rng.below(2) == 0;
    if use_b {
        prog.instrs[pos + shift].b = new_r;
    } else {
        prog.instrs[pos + shift].a = new_r;
    }
    if rewire_all {
        for j in (pos + shift + 1)..prog.instrs.len() {
            let (ot_j, it_j) = prog.instrs[j].op.sig();
            if it_j.first() == Some(&in_ty) && prog.instrs[j].a == old_r {
                prog.instrs[j].a = new_r;
            }
            if it_j.get(1) == Some(&in_ty) && prog.instrs[j].b == old_r {
                prog.instrs[j].b = new_r;
            }
            if ot_j == in_ty && (prog.instrs[j].out == old_r || prog.instrs[j].out == new_r) {
                break;
            }
        }
    }
    Some(focus.unwrap_or(pos))
}

fn mutate_program(parent: &Program, partner: Option<&Program>, rng: &mut Rng) -> (Program, Option<usize>) {
    let (mut p, plive, _, _) = parent.compact();
    let n_edits = if rng.uniform() < 0.75 { 1 } else { 2 };
    let mut focus: Option<usize> = None;

    for _ in 0..n_edits {
        let n = p.instrs.len();
        let roll = rng.uniform();
        if n == 0 {
            let an = analyze(&p, plive);
            p.instrs.push(random_instr_at(rng, &an, 0, Some(Ty::M), Some(0)));
        } else if n >= 18 && roll < 0.16 {
            // Active bloat shedding on long programs so room stays open for new blocks.
            let idx = rng.below(n);
            p.instrs.remove(idx);
        } else if roll < 0.24 {
            if let Some(f) = residual_insert_once(&mut p, rng, plive) {
                focus = Some(f);
            } else if n < MAX_LEN {
                let an = analyze(&p, plive);
                let pos = rng.below(n + 1);
                p.instrs.insert(pos, random_instr_at(rng, &an, pos, None, None));
            }
        } else if roll < 0.42 {
            if let Some(f) = chain_residual_insert(&mut p, rng, plive) {
                focus = Some(f);
            } else if let Some(f) = residual_insert_once(&mut p, rng, plive) {
                focus = Some(f);
            }
        } else if roll < 0.62 {
            if let Some(f) = wrap_input_mutate(&mut p, rng, plive) {
                focus = Some(f);
            } else {
                let an = analyze(&p, plive);
                let idx = rng.below(n);
                p.instrs[idx] = random_instr_at(rng, &an, idx, None, None);
            }
        } else if roll < 0.80 {
            let idx = rng.below(n);
            let an = analyze(&p, plive);
            match rng.below(4) {
                0 => {
                    let (ot, _) = p.instrs[idx].op.sig();
                    let out_r = p.instrs[idx].out;
                    p.instrs[idx] = random_instr_at(rng, &an, idx, Some(ot), Some(out_r));
                }
                1 => {
                    let (_, it) = p.instrs[idx].op.sig();
                    if !it.is_empty() {
                        if it.len() == 2 && rng.below(2) == 1 {
                            p.instrs[idx].b = pick_defined_reg(rng, &an, idx, it[1]);
                        } else {
                            p.instrs[idx].a = pick_defined_reg(rng, &an, idx, it[0]);
                        }
                    } else {
                        p.instrs[idx].c += rng.normal() * 0.2;
                        focus = Some(idx);
                    }
                }
                2 => {
                    let (ot, _) = p.instrs[idx].op.sig();
                    p.instrs[idx].out = rng.below(n_regs(ot)) as u8;
                }
                _ => {
                    let cis = p.const_indices();
                    if !cis.is_empty() {
                        let ci = cis[rng.below(cis.len())];
                        if rng.below(2) == 0 {
                            p.instrs[ci].c *= 10.0f32.powf(rng.normal() * 0.4);
                        } else {
                            p.instrs[ci].c += rng.normal() * 0.25;
                        }
                        focus = Some(ci);
                    } else {
                        p.instrs[idx] = random_instr_at(rng, &an, idx, None, None);
                    }
                }
            }
        } else if roll < 0.89 && n > 1 {
            let idx = rng.below(n);
            p.instrs.remove(idx);
        } else if roll < 0.95 && n < MAX_LEN {
            let an = analyze(&p, plive);
            let pos = rng.below(n + 1);
            p.instrs.insert(pos, random_instr_at(rng, &an, pos, None, None));
        } else if let Some(b) = partner {
            let (bc, _, _, _) = b.compact();
            if !bc.instrs.is_empty() {
                let cut_a = rng.below(n + 1);
                let cut_b = rng.below(bc.instrs.len() + 1);
                let mut child = Vec::with_capacity(MAX_LEN);
                child.extend_from_slice(&p.instrs[..cut_a]);
                child.extend_from_slice(&bc.instrs[cut_b..]);
                if child.len() > MAX_LEN {
                    child.truncate(MAX_LEN);
                }
                p.instrs = child;
            }
        }
    }
    (p, focus)
}

// --- MAP-Elites Archive ---

#[derive(Clone)]
struct Elite {
    prog: Program,
    export_pm: usize,
    n_live_states: usize,
    metrics: EvalMetrics,
    op_sig: u64,
}

struct Archive {
    cells: HashMap<(usize, usize), Vec<Elite>>,
}

impl Archive {
    fn new() -> Self {
        Archive { cells: HashMap::new() }
    }

    fn cell_threshold(&self, len: usize, n_live: usize) -> f32 {
        match self.cells.get(&(len, n_live)) {
            None => f32::INFINITY,
            Some(v) if v.len() < CELL_K => f32::INFINITY,
            Some(v) => v.last().unwrap().metrics.obj,
        }
    }

    fn insert(&mut self, e: Elite) -> bool {
        let len = e.prog.instrs.len();
        if len == 0 || len > MAX_LEN || !e.metrics.obj.is_finite() {
            return false;
        }
        let key = (len, e.n_live_states);
        let bucket = self.cells.entry(key).or_default();
        if let Some(pos) = bucket.iter().position(|x| x.op_sig == e.op_sig) {
            if e.metrics.obj + 1e-6 < bucket[pos].metrics.obj {
                bucket[pos] = e;
                bucket.sort_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj));
                return true;
            }
            return false;
        }
        if bucket.len() < CELL_K || e.metrics.obj + 1e-6 < bucket.last().unwrap().metrics.obj {
            bucket.push(e);
            bucket.sort_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj));
            bucket.truncate(CELL_K);
            return true;
        }
        false
    }

    fn all_elites(&self) -> Vec<Elite> {
        let mut out: Vec<Elite> = self.cells.values().flat_map(|v| v.iter().cloned()).collect();
        out.sort_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj));
        out
    }

    fn best(&self) -> Option<&Elite> {
        self.cells
            .values()
            .flat_map(|v| v.iter())
            .min_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj))
    }
}

fn run_self_test(train_path: &str, st_l2: f32) {
    let task = Task::load_json(train_path);
    let mut regs = Regs16::new();
    println!(
        "Loaded train dump: {} (d={}, eps={}, vals={})",
        train_path, task.d, task.episodes.len(), task.n_vals
    );

    let mut kalman = Program {
        instrs: vec![
            Instr { op: Op::MatVec, out: 2, a: 1, b: 0, c: 0.0 },
            Instr { op: Op::Dot, out: 0, a: 0, b: 2, c: 0.0 },
            Instr { op: Op::Const, out: 1, a: 0, b: 0, c: 0.00184 },
            Instr { op: Op::SAdd, out: 0, a: 0, b: 1, c: 0.0 },
            Instr { op: Op::Recip, out: 0, a: 0, b: 0, c: 0.0 },
            Instr { op: Op::VecScale, out: 3, a: 0, b: 2, c: 0.0 },
            Instr { op: Op::MatVec, out: 4, a: 0, b: 0, c: 0.0 },
            Instr { op: Op::VecSub, out: 5, a: 1, b: 4, c: 0.0 },
            Instr { op: Op::Outer, out: 3, a: 5, b: 3, c: 0.0 },
            Instr { op: Op::MatAdd, out: 0, a: 0, b: 3, c: 0.0 },
            Instr { op: Op::Outer, out: 3, a: 3, b: 2, c: 0.0 },
            Instr { op: Op::MatSub, out: 1, a: 1, b: 3, c: 0.0 },
            Instr { op: Op::Const, out: 2, a: 0, b: 0, c: 0.00126 },
            Instr { op: Op::MatScale, out: 3, a: 2, b: 2, c: 0.0 },
            Instr { op: Op::MatAdd, out: 1, a: 1, b: 3, c: 0.0 },
        ],
    };
    let (kc, _, _, pm) = kalman.compact();
    let m_ref = eval_program(&kc, pm, &task, None, &mut regs, st_l2, true);
    println!(
        "1. Exact Kalman-2p check: tr_acc={:.4} mse={:.4} obj={:.4} max_st={:.2}",
        m_ref.acc, m_ref.mse, m_ref.obj, m_ref.max_st
    );

    kalman.instrs[2].c = 1.0;
    kalman.instrs[12].c = 0.5;
    let t0 = Instant::now();
    let _ = tune_constants(&mut kalman, 3, &task, None, &mut regs, st_l2, true);
    let dt = t0.elapsed().as_secs_f64();
    let m_rec = eval_program(&kalman, 3, &task, None, &mut regs, st_l2, true);
    println!(
        "2. Scrambled Kalman [1.0, 0.5] -> [{:.5}, {:.5}] acc={:.4} mse={:.4} in {:.3}s",
        kalman.instrs[2].c, kalman.instrs[12].c, m_rec.acc, m_rec.mse, dt
    );
    assert!(m_rec.acc >= 0.92);

    let sub = task.subset(8, 4);
    let t1 = Instant::now();
    let n_it = 5000;
    for _ in 0..n_it {
        std::hint::black_box(eval_program(&kc, 3, &task, Some(&sub), &mut regs, st_l2, false));
    }
    let dt1 = t1.elapsed().as_secs_f64();
    println!(
        "3. Micro-subset ({} eps) single-thread speed: {:.0} evals/sec ({:.3} ms/eval)",
        sub.len(),
        n_it as f64 / dt1,
        1000.0 * dt1 / n_it as f64
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let arg_str = |flag: &str, def: &str| -> String {
        args.windows(2)
            .find(|w| w[0] == flag)
            .map(|w| w[1].clone())
            .unwrap_or_else(|| def.to_string())
    };
    let arg_usize = |flag: &str, def: usize| -> usize { arg_str(flag, &def.to_string()).parse().unwrap() };
    let arg_u64 = |flag: &str, def: u64| -> u64 { arg_str(flag, &def.to_string()).parse().unwrap() };
    let arg_f32 = |flag: &str, def: f32| -> f32 { arg_str(flag, &def.to_string()).parse().unwrap() };

    let train_path = arg_str("--train-dump", "v2/data/collision3_train_s1.json");
    let val_path = arg_str("--val-dump", "v2/data/collision3_val_s2001.json");
    let st_l2 = arg_f32("--st-l2", 0.015);

    if args.iter().any(|a| a == "--self-test") {
        run_self_test(&train_path, st_l2);
        return;
    }

    let seed = arg_u64("--seed", 0);
    let seconds = arg_f32("--seconds", 120.0) as f64;
    let max_cands = arg_usize("--max-cands", 0);
    let threads = arg_usize("--threads", 16).max(1);
    let batch_size = arg_usize("--batch", 512).max(threads);
    let out_dir = PathBuf::from(arg_str("--out", &format!("v2/runs/memetic_dev/seed{seed}")));
    fs::create_dir_all(&out_dir).expect("mkdir out_dir");

    let train_task = Task::load_json(&train_path);
    let val_task = Task::load_json(&val_path);
    let micro_sub = train_task.subset(4, 4); // 8 eps: ultra-fast Tier 0/1 screen

    println!(
        "Memetic MAP-Elites v3 | seed={} max_cands={} seconds={:.0} threads={} batch={} st_l2={} | train={} ({} eps) val={} ({} eps)",
        seed, max_cands, seconds, threads, batch_size, st_l2, train_path, train_task.episodes.len(), val_path, val_task.episodes.len()
    );

    let t_start = Instant::now();
    let mut master_rng = Rng::new(seed ^ 0xA5A5_5A5A_1234_5678);
    let mut archive = Archive::new();
    let mut seen_structs: HashSet<u64> = HashSet::new();
    let mut polished_leaders: HashSet<u64> = HashSet::new();

    let mut init_progs: Vec<(Program, Option<usize>)> = Vec::with_capacity(512);
    for _ in 0..512 {
        let mut p = Program { instrs: Vec::new() };
        let len = 1 + master_rng.below(6);
        for _ in 0..len {
            let an = analyze(&p, [true, false, false]);
            let pos = p.instrs.len();
            p.instrs.push(random_instr_at(&mut master_rng, &an, pos, None, None));
        }
        init_progs.push((p, None));
    }

    let eval_batch = |cands: Vec<(Program, Option<usize>)>,
                      cell_thresh: &HashMap<(usize, usize), f32>,
                      best_by_bkt_obj: [f32; N_BUCKETS],
                      seen_snapshot: &HashSet<u64>,
                      batch_seed: u64|
     -> (Vec<Elite>, usize, usize) {
        let chunk = (cands.len() + threads - 1) / threads;
        std::thread::scope(|sc| {
            let mut handles = Vec::new();
            for (ti, slice) in cands.chunks(chunk.max(1)).enumerate() {
                let train_ref = &train_task;
                let sub_ref = &micro_sub;
                handles.push(sc.spawn(move || {
                    let mut regs = Regs16::new();
                    let mut lrng = Rng::new(batch_seed.wrapping_add((ti as u64 + 1) * 0x9e3779b9));
                    let mut winners = Vec::new();
                    let mut t1_cnt = 0usize;
                    let mut t2_cnt = 0usize;
                    for (raw, focus) in slice {
                        let (mut prog, _, bucket, pm) = raw.compact();
                        if prog.instrs.is_empty() || prog.instrs.len() > MAX_LEN {
                            continue;
                        }
                        let sh = prog.struct_hash();
                        if seen_snapshot.contains(&sh) && lrng.uniform() > 0.02 {
                            continue;
                        }
                        // Tier 0: 1..6 micro-evals (8 eps)
                        let m0 = quick_screen_1d(&mut prog, pm, train_ref, sub_ref, &mut regs, st_l2, *focus);
                        if !m0.obj.is_finite() {
                            continue;
                        }
                        let c_thr = cell_thresh
                            .get(&(prog.instrs.len(), bucket))
                            .copied()
                            .unwrap_or(f32::INFINITY);
                        let b_best = best_by_bkt_obj[bucket];
                        let gate_t1 = c_thr.min(b_best + 0.10) + 0.025;
                        if m0.obj > gate_t1 {
                            continue;
                        }
                        t1_cnt += 1;
                        // Tier 1: 1-sweep multi-scale coordinate tune on 8-ep micro-subset.
                        let m1 = tune_constants(&mut prog, pm, train_ref, Some(sub_ref), &mut regs, st_l2, false);
                        if !m1.obj.is_finite() || m1.obj > c_thr.min(b_best + 0.09) + 0.015 {
                            continue;
                        }
                        t2_cnt += 1;
                        // Tier 2: exact 144-ep evaluation (fast, NO Nelder-Mead in inner loop).
                        let full_m = eval_program(&prog, pm, train_ref, None, &mut regs, st_l2, true);
                        if full_m.obj.is_finite() && full_m.obj < c_thr + 1e-4 {
                            let op_sig = prog.op_multiset_hash();
                            winners.push(Elite {
                                prog,
                                export_pm: pm,
                                n_live_states: bucket,
                                metrics: full_m,
                                op_sig,
                            });
                        }
                    }
                    (winners, t1_cnt, t2_cnt)
                }));
            }
            let mut all = Vec::new();
            let (mut tot_t1, mut tot_t2) = (0, 0);
            for h in handles {
                let (w, a, b) = h.join().unwrap();
                all.extend(w);
                tot_t1 += a;
                tot_t2 += b;
            }
            (all, tot_t1, tot_t2)
        })
    };

    let empty_thresh = HashMap::new();
    let (init_w, _, _) = eval_batch(init_progs, &empty_thresh, [f32::INFINITY; N_BUCKETS], &seen_structs, seed);
    for e in init_w {
        seen_structs.insert(e.prog.struct_hash());
        archive.insert(e);
    }

    let mut total_cands = 512usize;
    let mut total_t1 = 0usize;
    let mut total_t2 = 0usize;
    let mut batch_idx = 0u64;
    let mut last_log = Instant::now();
    let mut val_regs = Regs16::new();

    while if max_cands > 0 { total_cands < max_cands } else { t_start.elapsed().as_secs_f64() < seconds } {
        batch_idx += 1;
        let elites = archive.all_elites();
        let mut cands = Vec::with_capacity(batch_size);

        let mut cell_thresh = HashMap::new();
        for len in 1..=MAX_LEN {
            for b in 0..N_BUCKETS {
                cell_thresh.insert((len, b), archive.cell_threshold(len, b));
            }
        }

        let mut by_bkt: [Vec<&Elite>; N_BUCKETS] = std::array::from_fn(|_| Vec::new());
        let mut best_by_bkt_obj = [f32::INFINITY; N_BUCKETS];
        for e in &elites {
            let bi = e.n_live_states;
            if e.metrics.obj < best_by_bkt_obj[bi] {
                best_by_bkt_obj[bi] = e.metrics.obj;
            }
            by_bkt[bi].push(e);
        }
        let compact_elites: Vec<&Elite> = elites.iter().filter(|e| e.prog.instrs.len() <= 18).collect();

        for _ in 0..batch_size {
            if elites.is_empty() || master_rng.uniform() < 0.02 {
                let mut p = Program { instrs: Vec::new() };
                let len = 1 + master_rng.below(6);
                for _ in 0..len {
                    let an = analyze(&p, [true, false, false]);
                    let pos = p.instrs.len();
                    p.instrs.push(random_instr_at(&mut master_rng, &an, pos, None, None));
                }
                cands.push((p, None));
                continue;
            }
            let r = master_rng.uniform();
            let parent = if r < 0.25 {
                let top_k = elites.len().min(10);
                &elites[master_rng.below(top_k)].prog
            } else if r < 0.40 && !compact_elites.is_empty() {
                let top_k = compact_elites.len().min(10);
                &compact_elites[master_rng.below(top_k)].prog
            } else if r < 0.88 {
                // Equal attention across all 5 genuine (written, live) state buckets!
                let bi = master_rng.below(N_BUCKETS);
                let pool = &by_bkt[bi];
                if !pool.is_empty() {
                    let top_k = pool.len().min(6);
                    &pool[master_rng.below(top_k)].prog
                } else {
                    &elites[master_rng.below(elites.len())].prog
                }
            } else {
                &elites[master_rng.below(elites.len())].prog
            };
            let partner = if elites.len() >= 2 {
                Some(&elites[master_rng.below(elites.len().min(24))].prog)
            } else {
                None
            };
            cands.push(mutate_program(parent, partner, &mut master_rng));
        }

        total_cands += cands.len();
        let bseed = seed.wrapping_mul(1_000_003).wrapping_add(batch_idx * 97);
        let (winners, t1, t2) = eval_batch(cands, &cell_thresh, best_by_bkt_obj, &seen_structs, bseed);
        total_t1 += t1;
        total_t2 += t2;
        for e in winners {
            seen_structs.insert(e.prog.struct_hash());
            archive.insert(e);
        }

        // Periodic/on-new-leader full 144-ep Nelder-Mead polish for the 5 bucket leaders (parallel, <= 5 progs).
        let mut to_polish: Vec<Elite> = Vec::new();
        for b in 0..N_BUCKETS {
            if let Some(leader) = archive
                .cells
                .iter()
                .filter(|&(&(_, bk), _)| bk == b)
                .flat_map(|(_, v)| v.iter())
                .min_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj))
            {
                let sh = leader.prog.struct_hash();
                if !polished_leaders.contains(&sh) {
                    polished_leaders.insert(sh);
                    to_polish.push(leader.clone());
                }
            }
        }
        if !to_polish.is_empty() {
            let polished: Vec<Elite> = std::thread::scope(|sc| {
                let mut hs = Vec::new();
                for mut e in to_polish {
                    let train_ref = &train_task;
                    hs.push(sc.spawn(move || {
                        let mut regs = Regs16::new();
                        let _ = tune_constants(&mut e.prog, e.export_pm, train_ref, None, &mut regs, st_l2, true);
                        e.metrics = eval_program(&e.prog, e.export_pm, train_ref, None, &mut regs, st_l2, true);
                        e
                    }));
                }
                hs.into_iter().map(|h| h.join().unwrap()).collect()
            });
            for e in polished {
                archive.insert(e);
            }
        }

        if last_log.elapsed().as_secs_f64() >= 5.0 {
            last_log = Instant::now();
            if let Some(best) = archive.best() {
                let vm = eval_program(&best.prog, best.export_pm, &val_task, None, &mut val_regs, st_l2, true);
                let labels = ["w1l1", "w1l+", "w2l2", "w2l3", "w3l3"];
                let best_by_st: Vec<String> = (0..N_BUCKETS)
                    .map(|b| {
                        archive
                            .cells
                            .iter()
                            .filter(|&(&(_, bk), _)| bk == b)
                            .flat_map(|(_, v)| v.iter())
                            .min_by(|a, b| a.metrics.obj.total_cmp(&b.metrics.obj))
                            .map(|e| format!("{}:{:.3}({:.3},L{})", labels[b], e.metrics.obj, e.metrics.acc, e.prog.instrs.len()))
                            .unwrap_or_else(|| format!("{}:-", labels[b]))
                    })
                    .collect();
                println!(
                    "  [{:5.1}s | cands={:7} t1={:5} t2={:4} cells={:3}/120] best tr={:.4}({:.3},L{},pm{}) val={:.4}({:.3},mx={:.2}) | {}",
                    t_start.elapsed().as_secs_f64(),
                    total_cands,
                    total_t1,
                    total_t2,
                    archive.cells.len(),
                    best.metrics.obj,
                    best.metrics.acc,
                    best.prog.instrs.len(),
                    best.export_pm,
                    vm.obj,
                    vm.acc,
                    vm.max_st,
                    best_by_st.join(" ")
                );
            }
        }
    }

    // Final validation-only selection across ALL archive elites.
    let elites = archive.all_elites();
    let mut best_val_elite: Option<(Elite, EvalMetrics)> = None;
    for e in elites {
        let vm = eval_program(&e.prog, e.export_pm, &val_task, None, &mut val_regs, st_l2, true);
        if vm.obj.is_finite() {
            if best_val_elite.as_ref().map(|b| vm.obj < b.1.obj).unwrap_or(true) {
                best_val_elite = Some((e, vm));
            }
        }
    }

    let (win, vm) = best_val_elite.expect("no valid elite found");
    let wall = t_start.elapsed().as_secs_f64();
    fs::write(out_dir.join("best.json"), win.prog.to_json(win.export_pm)).expect("write best.json");
    let summary = format!(
        "{{\n  \"seed\": {},\n  \"wall_seconds\": {:.2},\n  \"total_cands\": {},\n  \"n_instrs\": {},\n  \"persist_m\": {},\n  \"train_obj\": {:.5},\n  \"train_mse\": {:.5},\n  \"train_acc\": {:.4},\n  \"val_obj\": {:.5},\n  \"val_mse\": {:.5},\n  \"val_acc\": {:.4},\n  \"max_abs_state_val\": {:.3}\n}}\n",
        seed,
        wall,
        total_cands,
        win.prog.instrs.len(),
        win.export_pm,
        win.metrics.obj,
        win.metrics.mse,
        win.metrics.acc,
        vm.obj,
        vm.mse,
        vm.acc,
        vm.max_st
    );
    fs::write(out_dir.join("summary.json"), summary).expect("write summary.json");

    println!(
        "\n[FINAL seed {}] time={:.1}s cands={} (t1={}, t2={}) | len={} pm={} | tr_acc={:.4} (mse={:.4}) | val_acc={:.4} (mse={:.4}, obj={:.4}, max={:.2})",
        seed,
        wall,
        total_cands,
        total_t1,
        total_t2,
        win.prog.instrs.len(),
        win.export_pm,
        win.metrics.acc,
        win.metrics.mse,
        vm.acc,
        vm.mse,
        vm.obj,
        vm.max_st
    );
    print!("Program:\n{}", win.prog.format_lines());
}
