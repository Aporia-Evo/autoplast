//! Search space: a memory update rule is a short straight-line program over typed registers.
//!
//! Registers per write step (all scratch registers start at zero every step):
//!   matrices  M0..M3   M0 = memory S on entry; M0 on exit becomes the new S
//!   vectors   V0..V5   V0 = key k, V1 = value v
//!   scalars   s0..s3
//!
//! Nothing about delta rules, linear attention or gating is built in. Those rules are only
//! *expressible* as particular instruction sequences (see `baselines()`), exactly like any
//! other program in the space. The readout is fixed for every rule: o = S q.

use crate::rng::Rng;

pub const NM: usize = 4;
pub const NV: usize = 6;
pub const NS: usize = 4;
pub const MAX_LEN: usize = 24;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Ty {
    M,
    V,
    S,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Op {
    // matrix result
    Outer,    // M = Va ⊗ Vb
    MatAdd,   // M = Ma + Mb
    MatSub,   // M = Ma - Mb
    MatScale, // M = sa * Mb
    Transpose,
    MatMul, // M = Ma @ Mb
    // vector result
    MatVec,   // V = Ma @ Vb
    VecAdd,   // V = Va + Vb
    VecSub,   // V = Va - Vb
    VecScale, // V = sa * Vb
    Hadamard, // V = Va ⊙ Vb
    Normalize,
    Tanh,
    // scalar result
    Dot, // s = Va · Vb
    Const,
    SAdd,
    SMul,
    Sigmoid,
    Norm, // s = |Va|
}

pub const ALL_OPS: [Op; 19] = [
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
];

impl Op {
    /// (output type, input types)
    pub fn sig(self) -> (Ty, &'static [Ty]) {
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
            Op::Sigmoid => (S, &[S]),
            Op::Norm => (S, &[V]),
        }
    }

    pub fn name(self) -> &'static str {
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
        }
    }

    pub fn from_name(s: &str) -> Option<Op> {
        ALL_OPS.iter().copied().find(|o| o.name() == s)
    }
}

pub fn n_regs(t: Ty) -> usize {
    match t {
        Ty::M => NM,
        Ty::V => NV,
        Ty::S => NS,
    }
}

fn reg_name(t: Ty, i: u8) -> String {
    match t {
        Ty::M => format!("M{i}"),
        Ty::V => format!("V{i}"),
        Ty::S => format!("s{i}"),
    }
}

#[derive(Clone, Debug)]
pub struct Instr {
    pub op: Op,
    pub out: u8,
    pub a: u8,
    pub b: u8,
    pub c: f32,
}

impl Instr {
    pub fn random(rng: &mut Rng) -> Instr {
        let op = ALL_OPS[rng.below(ALL_OPS.len())];
        let (ot, ins) = op.sig();
        let pick = |rng: &mut Rng, t: Ty| rng.below(n_regs(t)) as u8;
        Instr {
            op,
            out: pick(rng, ot),
            a: ins.first().map(|&t| pick(rng, t)).unwrap_or(0),
            b: ins.get(1).map(|&t| pick(rng, t)).unwrap_or(0),
            c: rng.uniform() * 4.0 - 2.0,
        }
    }

    pub fn inputs(&self) -> Vec<(Ty, u8)> {
        let (_, ins) = self.op.sig();
        ins.iter()
            .enumerate()
            .map(|(i, &t)| (t, if i == 0 { self.a } else { self.b }))
            .collect()
    }

    pub fn output(&self) -> (Ty, u8) {
        (self.op.sig().0, self.out)
    }

    pub fn render(&self) -> String {
        let (ot, _) = self.op.sig();
        let o = reg_name(ot, self.out);
        let ins: Vec<String> = self.inputs().iter().map(|&(t, i)| reg_name(t, i)).collect();
        match self.op {
            Op::Const => format!("{o} = {:.4}", self.c),
            _ => format!("{o} = {}({})", self.op.name(), ins.join(", ")),
        }
    }
}

#[derive(Clone, Debug, Default)]
pub struct Program {
    pub instrs: Vec<Instr>,
}

impl Program {
    /// Keep only instructions that can influence the final M0 (backward liveness).
    pub fn effective(&self) -> Program {
        let mut live_m = [false; NM];
        let mut live_v = [false; NV];
        let mut live_s = [false; NS];
        live_m[0] = true;
        let mut keep = vec![false; self.instrs.len()];
        for (idx, ins) in self.instrs.iter().enumerate().rev() {
            let (ot, o) = ins.output();
            let o = o as usize;
            let is_live = match ot {
                Ty::M => live_m[o],
                Ty::V => live_v[o],
                Ty::S => live_s[o],
            };
            if !is_live {
                continue;
            }
            keep[idx] = true;
            match ot {
                Ty::M => live_m[o] = false,
                Ty::V => live_v[o] = false,
                Ty::S => live_s[o] = false,
            }
            for (t, i) in ins.inputs() {
                let i = i as usize;
                match t {
                    Ty::M => live_m[i] = true,
                    Ty::V => live_v[i] = true,
                    Ty::S => live_s[i] = true,
                }
            }
        }
        Program {
            instrs: self
                .instrs
                .iter()
                .zip(keep)
                .filter(|(_, k)| *k)
                .map(|(i, _)| i.clone())
                .collect(),
        }
    }

    /// NEAT-style add-node: pick an input edge `r -> instr i`, insert a new instruction
    /// `t = op(r, x)` (or `op(x, r)`) right before i and rewire i to read `t`.
    /// When x is still a zero register this is often behaviour-preserving (r - 0, r + 0),
    /// so structure can grow through neutral steps instead of needing several lucky
    /// simultaneous mutations. It is generic graph surgery; no op or rule is favoured.
    fn split_edge(&mut self, rng: &mut Rng) -> bool {
        let len = self.instrs.len();
        if len == 0 || len >= MAX_LEN {
            return false;
        }
        let i = rng.below(len);
        let ins_types = self.instrs[i].op.sig().1;
        if ins_types.is_empty() {
            return false;
        }
        let slot = rng.below(ins_types.len());
        let ty = ins_types[slot];
        let r = if slot == 0 { self.instrs[i].a } else { self.instrs[i].b };
        let candidates: Vec<Op> = ALL_OPS
            .iter()
            .copied()
            .filter(|o| o.sig().0 == ty && o.sig().1.contains(&ty))
            .collect();
        let op = candidates[rng.below(candidates.len())];
        let (_, op_ins) = op.sig();
        let pos_r: Vec<usize> = (0..op_ins.len()).filter(|&j| op_ins[j] == ty).collect();
        let pr = pos_r[rng.below(pos_r.len())];
        let mut fields = [0u8; 2];
        for (j, &t) in op_ins.iter().enumerate() {
            fields[j] = if j == pr { r } else { rng.below(n_regs(t)) as u8 };
        }
        let out = rng.below(n_regs(ty)) as u8;
        let new = Instr {
            op,
            out,
            a: fields[0],
            b: fields[1],
            c: rng.uniform() * 4.0 - 2.0,
        };
        self.instrs.insert(i, new);
        let target = &mut self.instrs[i + 1];
        if slot == 0 {
            target.a = out;
        } else {
            target.b = out;
        }
        true
    }

    pub fn mutate(&mut self, rng: &mut Rng) {
        if rng.below(6) == 5 && self.split_edge(rng) {
            return;
        }
        let len = self.instrs.len();
        let choice = rng.below(5);
        match choice {
            0 if len < MAX_LEN => {
                let pos = rng.below(len + 1);
                self.instrs.insert(pos, Instr::random(rng));
            }
            1 if len > 0 => {
                self.instrs.remove(rng.below(len));
            }
            2 if len > 0 => {
                let pos = rng.below(len);
                self.instrs[pos] = Instr::random(rng);
            }
            3 if len > 0 => {
                // rewire one field, keeping the op
                let pos = rng.below(len);
                let ins = &mut self.instrs[pos];
                let (ot, ints) = ins.op.sig();
                match rng.below(3) {
                    0 => ins.out = rng.below(n_regs(ot)) as u8,
                    1 if !ints.is_empty() => ins.a = rng.below(n_regs(ints[0])) as u8,
                    2 if ints.len() > 1 => ins.b = rng.below(n_regs(ints[1])) as u8,
                    _ => ins.c += rng.normal() * 0.2,
                }
            }
            4 if len > 0 => {
                let pos = rng.below(len);
                let ins = &mut self.instrs[pos];
                if rng.uniform() < 0.5 {
                    ins.c += rng.normal() * 0.1;
                } else {
                    ins.c *= 1.0 + rng.normal() * 0.2;
                }
            }
            _ => {
                // fallback when the chosen mutation is not applicable (e.g. empty program)
                if len < MAX_LEN {
                    let pos = rng.below(len + 1);
                    self.instrs.insert(pos, Instr::random(rng));
                }
            }
        }
    }

    pub fn listing(&self) -> String {
        self.instrs
            .iter()
            .map(|i| format!("  {}", i.render()))
            .collect::<Vec<_>>()
            .join("\n")
    }

    /// Symbolic formula for the new S, by forward substitution over the effective program.
    pub fn formula(&self) -> String {
        let eff = self.effective();
        let mut m: Vec<String> = (0..NM).map(|i| if i == 0 { "S".into() } else { "0".into() }).collect();
        let mut v: Vec<String> = (0..NV)
            .map(|i| match i {
                0 => "k".into(),
                1 => "v".into(),
                _ => "0".into(),
            })
            .collect();
        let mut s: Vec<String> = (0..NS).map(|_| "0".into()).collect();
        for ins in &eff.instrs {
            let a = ins.a as usize;
            let b = ins.b as usize;
            let e = match ins.op {
                Op::Outer => format!("({})⊗({})", v[a], v[b]),
                Op::MatAdd => format!("({} + {})", m[a], m[b]),
                Op::MatSub => format!("({} - {})", m[a], m[b]),
                Op::MatScale => format!("{}·{}", s[a], m[b]),
                Op::Transpose => format!("({})ᵀ", m[a]),
                Op::MatMul => format!("({})({})", m[a], m[b]),
                Op::MatVec => format!("{}·{}", m[a], v[b]),
                Op::VecAdd => format!("({} + {})", v[a], v[b]),
                Op::VecSub => format!("({} - {})", v[a], v[b]),
                Op::VecScale => format!("{}·{}", s[a], v[b]),
                Op::Hadamard => format!("({} ⊙ {})", v[a], v[b]),
                Op::Normalize => format!("norm({})", v[a]),
                Op::Tanh => format!("tanh({})", v[a]),
                Op::Dot => format!("<{}, {}>", v[a], v[b]),
                Op::Const => format!("{:.3}", ins.c),
                Op::SAdd => format!("({} + {})", s[a], s[b]),
                Op::SMul => format!("{}·{}", s[a], s[b]),
                Op::Sigmoid => format!("σ({})", s[a]),
                Op::Norm => format!("|{}|", v[a]),
            };
            let e = if e.len() > 400 { "…".to_string() } else { e };
            let o = ins.out as usize;
            match ins.op.sig().0 {
                Ty::M => m[o] = e,
                Ty::V => v[o] = e,
                Ty::S => s[o] = e,
            }
        }
        format!("S' = {}", m[0])
    }

    pub fn to_json(&self) -> String {
        let items: Vec<String> = self
            .instrs
            .iter()
            .map(|i| {
                format!(
                    "{{\"op\":\"{}\",\"out\":{},\"a\":{},\"b\":{},\"c\":{}}}",
                    i.op.name(),
                    i.out,
                    i.a,
                    i.b,
                    i.c
                )
            })
            .collect();
        format!("{{\"instrs\":[{}]}}", items.join(","))
    }

    /// Minimal parser for the format written by `to_json`.
    pub fn from_json(s: &str) -> Result<Program, String> {
        let mut instrs = Vec::new();
        for chunk in s.split('{').skip(2) {
            let field = |name: &str| -> Result<String, String> {
                let key = format!("\"{name}\":");
                let start = chunk.find(&key).ok_or(format!("missing {name}"))? + key.len();
                let rest = &chunk[start..];
                let end = rest.find([',', '}']).unwrap_or(rest.len());
                Ok(rest[..end].trim().trim_matches('"').to_string())
            };
            let op = Op::from_name(&field("op")?).ok_or("bad op")?;
            instrs.push(Instr {
                op,
                out: field("out")?.parse().map_err(|e| format!("{e}"))?,
                a: field("a")?.parse().map_err(|e| format!("{e}"))?,
                b: field("b")?.parse().map_err(|e| format!("{e}"))?,
                c: field("c")?.parse().map_err(|e| format!("{e}"))?,
            });
        }
        Ok(Program { instrs })
    }
}

/// Register file + scratch buffers for the interpreter.
pub struct Regs {
    pub d: usize,
    pub m: [Vec<f32>; NM],
    pub v: [Vec<f32>; NV],
    pub s: [f32; NS],
    tm: Vec<f32>,
    tv: Vec<f32>,
}

impl Regs {
    pub fn new(d: usize) -> Regs {
        Regs {
            d,
            m: std::array::from_fn(|_| vec![0.0; d * d]),
            v: std::array::from_fn(|_| vec![0.0; d]),
            s: [0.0; NS],
            tm: vec![0.0; d * d],
            tv: vec![0.0; d],
        }
    }

    /// Load inputs for one write step: M0 = S, V0 = k, V1 = v, everything else zero.
    pub fn load(&mut self, s_mem: &[f32], k: &[f32], v: &[f32]) {
        self.m[0].copy_from_slice(s_mem);
        for i in 1..NM {
            self.m[i].fill(0.0);
        }
        self.v[0].copy_from_slice(k);
        self.v[1].copy_from_slice(v);
        for i in 2..NV {
            self.v[i].fill(0.0);
        }
        self.s = [0.0; NS];
    }

    pub fn run(&mut self, prog: &Program) {
        let d = self.d;
        for ins in &prog.instrs {
            let (a, b, o) = (ins.a as usize, ins.b as usize, ins.out as usize);
            match ins.op {
                Op::Outer => {
                    for i in 0..d {
                        for j in 0..d {
                            self.tm[i * d + j] = self.v[a][i] * self.v[b][j];
                        }
                    }
                    self.m[o].copy_from_slice(&self.tm);
                }
                Op::MatAdd | Op::MatSub => {
                    let sign = if ins.op == Op::MatAdd { 1.0 } else { -1.0 };
                    for i in 0..d * d {
                        self.tm[i] = self.m[a][i] + sign * self.m[b][i];
                    }
                    self.m[o].copy_from_slice(&self.tm);
                }
                Op::MatScale => {
                    let c = self.s[a];
                    for i in 0..d * d {
                        self.tm[i] = c * self.m[b][i];
                    }
                    self.m[o].copy_from_slice(&self.tm);
                }
                Op::Transpose => {
                    for i in 0..d {
                        for j in 0..d {
                            self.tm[i * d + j] = self.m[a][j * d + i];
                        }
                    }
                    self.m[o].copy_from_slice(&self.tm);
                }
                Op::MatMul => {
                    self.tm.fill(0.0);
                    for i in 0..d {
                        for k in 0..d {
                            let x = self.m[a][i * d + k];
                            if x == 0.0 {
                                continue;
                            }
                            for j in 0..d {
                                self.tm[i * d + j] += x * self.m[b][k * d + j];
                            }
                        }
                    }
                    self.m[o].copy_from_slice(&self.tm);
                }
                Op::MatVec => {
                    for i in 0..d {
                        let mut acc = 0.0;
                        for j in 0..d {
                            acc += self.m[a][i * d + j] * self.v[b][j];
                        }
                        self.tv[i] = acc;
                    }
                    self.v[o].copy_from_slice(&self.tv);
                }
                Op::VecAdd | Op::VecSub | Op::Hadamard => {
                    for i in 0..d {
                        let (x, y) = (self.v[a][i], self.v[b][i]);
                        self.tv[i] = match ins.op {
                            Op::VecAdd => x + y,
                            Op::VecSub => x - y,
                            _ => x * y,
                        };
                    }
                    self.v[o].copy_from_slice(&self.tv);
                }
                Op::VecScale => {
                    let c = self.s[a];
                    for i in 0..d {
                        self.tv[i] = c * self.v[b][i];
                    }
                    self.v[o].copy_from_slice(&self.tv);
                }
                Op::Normalize => {
                    let n = self.v[a].iter().map(|x| x * x).sum::<f32>().sqrt() + 1e-6;
                    for i in 0..d {
                        self.tv[i] = self.v[a][i] / n;
                    }
                    self.v[o].copy_from_slice(&self.tv);
                }
                Op::Tanh => {
                    for i in 0..d {
                        self.tv[i] = self.v[a][i].tanh();
                    }
                    self.v[o].copy_from_slice(&self.tv);
                }
                Op::Dot => {
                    self.s[o] = (0..d).map(|i| self.v[a][i] * self.v[b][i]).sum();
                }
                Op::Const => self.s[o] = ins.c,
                Op::SAdd => self.s[o] = self.s[a] + self.s[b],
                Op::SMul => self.s[o] = self.s[a] * self.s[b],
                Op::Sigmoid => self.s[o] = 1.0 / (1.0 + (-self.s[a]).exp()),
                Op::Norm => self.s[o] = self.v[a].iter().map(|x| x * x).sum::<f32>().sqrt(),
            }
        }
    }
}

fn parse_line(line: &str) -> Instr {
    // helper for writing baselines readably: "OP out a b c"
    let p: Vec<&str> = line.split_whitespace().collect();
    Instr {
        op: Op::from_name(p[0]).expect("op"),
        out: p[1].parse().unwrap(),
        a: p.get(2).map(|x| x.parse().unwrap()).unwrap_or(0),
        b: p.get(3).map(|x| x.parse().unwrap()).unwrap_or(0),
        c: p.get(4).map(|x| x.parse().unwrap()).unwrap_or(0.0),
    }
}

pub fn prog(lines: &[&str]) -> Program {
    Program {
        instrs: lines.iter().map(|l| parse_line(l)).collect(),
    }
}

/// Hand-written reference rules, expressed in the same instruction set the search uses.
pub fn baselines() -> Vec<(&'static str, Program)> {
    vec![
        ("no-write (start of search)", Program::default()),
        (
            // S' = S + v kᵀ
            "linear attention",
            prog(&["Outer 1 1 0", "MatAdd 0 0 1"]),
        ),
        (
            // S' = S + (v - S k) kᵀ
            "delta rule (beta=1)",
            prog(&["MatVec 2 0 0", "VecSub 3 1 2", "Outer 1 3 0", "MatAdd 0 0 1"]),
        ),
        (
            "delta rule (beta=0.5)",
            prog(&[
                "MatVec 2 0 0",
                "VecSub 3 1 2",
                "Outer 1 3 0",
                "Const 0 0 0 0.5",
                "MatScale 1 0 1",
                "MatAdd 0 0 1",
            ]),
        ),
        (
            // S' = 0.9 S + (v - 0.9 S k) kᵀ   (gated delta, fixed gate)
            "gated delta (alpha=0.9)",
            prog(&[
                "Const 0 0 0 0.9",
                "MatScale 0 0 0",
                "MatVec 2 0 0",
                "VecSub 3 1 2",
                "Outer 1 3 0",
                "MatAdd 0 0 1",
            ]),
        ),
    ]
}
