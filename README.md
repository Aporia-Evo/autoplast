# autoplast

Gradient-free discovery of associative-memory update rules, starting from an empty program.

## Question

Can an evolutionary search, given only elementary linear-algebra operations and a recall task,
assemble a working memory update rule on its own? And once it reliably rediscovers known rules
(linear attention, the delta rule), can it find rules that are not known yet?

Stage 1 (this repo, now) is the rediscovery test. It decides whether the search is a usable
discovery engine at all. Stage 2 points the same search at regimes where known rules are weak.
Stage 3 transfers the best rules into small language models.

## Search space

A rule is a straight-line program over typed registers, run once per write step:

| registers | on entry | meaning |
|---|---|---|
| `M0..M3` (d×d) | `M0 = S`, rest 0 | `M0` on exit is the new memory `S'` |
| `V0..V5` (d) | `V0 = k`, `V1 = v`, rest 0 | |
| `s0..s3` | 0 | |

19 operations: `Outer, MatAdd, MatSub, MatScale, Transpose, MatMul, MatVec, VecAdd, VecSub,
VecScale, Hadamard, Normalize, Tanh, Dot, Const, SAdd, SMul, Sigmoid, Norm`.

Readout is identical for every rule: `o = S q`, decoded to the closest value embedding.
No rule family is built in. Linear attention, the delta rule and gated variants are just
particular programs in this space (`program::baselines()`), the same as any other.

## Task

Multi-query associative recall with overwrites: 12 writes per episode into an empty memory,
d = 16, 64 keys and 64 values as fixed random unit vectors. With probability 0.3 a write
reuses an earlier key with a new value. Every key is queried at the end; the target is its
latest value. Fitness = accuracy + 0.05 · mean margin − 1e-4 · program length.

Held-out tests use fresh embeddings and episodes, other overwrite rates and other sizes
(d = 32 / T = 24, d = 8 / T = 6) the search never saw.

### Task v3 (added 3 Nov 2026, before any v3 result)

Reason: in v2 every tuned or found delta rule has a growth factor a > 1 (tuned Gated DeltaNet
a = 1.1, found rules 1.055 to 1.153, one rule with a = 1.48 that overflows on d32 T24). With
12 writes per episode the amplification a^12 does no harm, and argmax decoding ignores the
global scale of S. Such rules would not survive long sequences.

Change (`--task v3`, any command; without the flag everything is the v2 task, byte for byte):
the train set keeps the 96 standard episodes and adds 48 long episodes from the same RNG
stream, T = 64 writes each, at most 8 distinct keys per episode (load stays below d = 16, so
this is not capacity overload; once 8 keys are in use every further write is an overwrite).
Keys written early and not rewritten sit in memory for up to ~60 steps, so a > 1 amplifies
old entries relative to recent ones. Fitness formula unchanged (accuracy + 0.05 margin -
1e-4 length, over all 144 episodes). The existing guard still scores a rule 0 if any entry
of S exceeds 1e4 or is not finite.

New held-out suites, printed for every task: `test d16 T64 K8 ow0.3` (256 episodes, seed 7)
and `test d16 T128 K8 ow0.3` (128 episodes, seed 8), fresh embeddings and episodes.
`sweep` alpha grid refined around 1 (added 0.97, 0.99, 1.01, 1.03).

Success criterion for the task fix, fixed in advance: on v3, tuned Gated DeltaNet should have
its optimum at a <= 1, and v2 rules with a > 1 should lose accuracy on T128.

### Alphabet-sensitivity switches (added 4 Nov 2026, before any 3a result)

Reason: the delta rule is only about four instructions from the empty program in the
default alphabet (MatVec, VecSub, Outer, MatAdd). Queue item 3a asks whether the search
finds it because of the task or because of the alphabet.

- `--no-op A,B`: remove ops from the alphabet (random instructions and add-node candidates).
  `--no-op MatVec` keeps delta expressible, but only via `S (k kᵀ)` with Outer and MatMul
  (five instructions instead of four).
- `--extra-ops`: add ten generic ops that encode no known rule: VecAbs, VecRelu, VecMax,
  VecSigmoid (elementwise), MatHadamard, MatTanh (elementwise), RowSum (M·1), VecSum, SSub,
  SAbs. The alphabet grows from 19 to 29 ops, which dilutes the probability of drawing any
  given op by about a third. The whole fixed pool is used rather than a random subset, so
  the test is reproducible. verify.py implements the same ten ops.
- Without these flags the alphabet and the RNG sequence are unchanged (checked: v3 seed 4
  log rows identical up to 50,036 candidates).


Regularized (aging) evolution as in AutoML-Zero: population 500, tournament 10, the whole
population starts as the empty program (`S' = S`, accuracy 0). Mutations insert, delete,
replace or rewire one instruction or perturb a constant. Programs with identical effective
code share a cached score.

## Verification

`verify/verify.py` re-implements the interpreter in JAX with its own episodes and RNG, and
decomposes a rule's update by least squares into `a·S + b·(v kᵀ) + c·((S k) kᵀ)` with R².
Linear attention is (1, 1, 0); the delta rule with step β is (1, β, −β).
Since 3 Nov 2026 it also runs the T64 K8 and T128 K8 suites and marks a suite "diverged" when
some episode exceeds the Rust guard (|S| > 1e4 or non-finite), where Rust scores the whole
suite 0 while the JAX accuracy is computed without the guard.

## Usage

Repository: github.com/Aporia-Evo/autoplast. Agent instructions: CLAUDE.md.

```bash
cargo build --release
./target/release/autoplast baselines
./target/release/autoplast search --seed 1 --budget 3000000 --out runs/seed1
./target/release/autoplast eval --prog runs/seed1/best.json
python verify/verify.py runs/seed1/best.json     # needs jax, numpy
./target/release/autoplast sweep                 # tuned known families, fair baselines

# many seeds: run locally, one `search` per seed, results in runs/<tag>/seed<N>/
./target/release/autoplast search --seed 3 --budget 1500000 --threads 8 --out runs/v2/seed3
```

Compute policy (3 Nov 2026): CPU searches, including multi-seed fan-outs, run on the local
machine (Ryzen 5700G, 8 cores / 16 threads). Modal is reserved for GPU runs.
`modal_runner.py` (CPU fan-out on Modal) is kept for reference but is not used.

## Reference rules (from `baselines`)

Train column on the v2 train set (96 episodes); corrected 3 Nov 2026, it previously showed
v1 values (48 episodes). Test columns unchanged.

| rule | train | test ow0.3 | test ow0.0 | test ow0.6 | test d32 T24 | test d8 T6 |
|---|---|---|---|---|---|---|
| no write (start of search) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| linear attention | 0.772 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 |
| delta rule β=1 | 0.858 | 0.862 | 0.788 | 0.922 | 0.948 | 0.744 |
| delta rule β=0.5 | 0.932 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 |
| gated delta α=0.9 | 0.729 | 0.714 | 0.620 | 0.837 | 0.639 | 0.685 |

## Results so far (3 Nov 2026)

Run v1 (48 train episodes, no add-node mutation), seed 1, 3M candidates: linear attention
after 17k candidates, then decayed linear attention `S' = 0.936·(S + v⊗k)` (RetNet-style).
Best rule overfit the small train set (train 0.848, test 0.782). Delta rule not reached.

Run v2 (96 train episodes, NEAT-style add-node mutation), 1.5M candidates per seed:

| seed | what it found | train | test ow0.3 | test ow0.0 | test ow0.6 | test d32 T24 | test d8 T6 |
|---|---|---|---|---|---|---|---|
| 1 | occupancy-gated write `S + σ(‖S k̃‖⁴)·v⊗k` | 0.853 | 0.832 | 0.919 | 0.689 | 0.932 | 0.639 |
| 2 | Gated DeltaNet form `γ(S + v kᵀ)(I − η kkᵀ)`, γ=1.098, η=0.726 | 0.971 | 0.967 | 0.947 | 0.964 | 0.978 | 0.836 |

Seed 2 reached the β=0.5 delta level after 865k candidates. Simplified by hand
(unit v): `S' = γ·[S(I − η kkᵀ) + (1−η) v kᵀ]`, which is the DeltaNet transition form
`S(I − β kkᵀ) + β v kᵀ` with a gate γ.

Fair baselines (`autoplast sweep`: grid-tuned on the train task, reported on tests):

| family | a | e | w | train | test ow0.3 | test ow0.0 | test ow0.6 | test d32 T24 | test d8 T6 |
|---|---|---|---|---|---|---|---|---|---|
| DeltaNet (a=1, w=e) | 1 | 0.50 | 0.50 | 0.932 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 |
| Gated DeltaNet (w=e) | 1.1 | 0.65 | 0.65 | 0.970 | 0.968 | 0.957 | 0.964 | 0.957 | 0.841 |
| untied a, e, w | 1.1 | 0.65 | 0.05 | 0.970 | 0.968 | 0.957 | 0.964 | 0.957 | 0.841 |

Reading: seed 2 is a rediscovery of tuned Gated DeltaNet, not an improvement. The apparent
erase/write decoupling is not a real degree of freedom here: the rule is linear in (S, v),
so the write gain only rescales S and argmax decoding ignores it. The optimum a > 1
(amplification) is an artefact of short episodes and should vanish with long sequences.

Stage 1 criterion ("rediscover the delta family from an empty program") is met by 1 of 2
seeds. Open: more seeds for a rate, long-sequence tasks that punish a > 1, a gate analysis
that does not saturate (the linear decomposition in `verify.py` cannot see state-dependent
gates such as seed 1's), and whether seed 1's occupancy gate is known in the literature.

Local timing pilot (3 Nov 2026, runs/v2-localpilot): seeds 1 and 2, 300k candidates, two
processes with 8 threads each on a Ryzen 5700G: 57 s per seed. Both found decayed linear
attention, neither the delta rule (as expected at this budget). Extrapolated cost of the
16-seed v2 run at 1.5M: 1.5 to 3.1 hours locally.

Run v2 at scale (3 Nov 2026, runs/v2, local, commit 62cbf63): 16 seeds, 1.5M candidates,
add-node on. 6 of 16 seeds reach the delta rule (beta=0.5 level), Wilson 95 % interval
18 % to 61 %, median 86k candidates when reached. All six are the Gated DeltaNet form
`a·S + b·v kᵀ - c·(S k) kᵀ` with a = 1.055 to 1.153 and test ow0.3 0.961 to 0.967, the level
of tuned Gated DeltaNet (0.968), not above it. The other 10 seeds stay at decayed linear
attention (test ow0.3 about 0.79). No seed found a state-dependent gate. All 16 rules
reproduce in JAX within 0.018. Details: runs/v2/v2_ERGEBNIS.md.

Stage 1 rate: the search rediscovers the delta family from an empty program in about one
third of seeds at this budget. The remaining seeds get stuck at decayed linear attention.

Ablation of the add-node mutation (3 Nov 2026, runs/v2-noaddnode, same 16 seeds and budget,
`--no-split-edge`): 8/16 seeds reach the delta rule, against 6/16 with add-node (Fisher
p = 0.72). The earlier impression that add-node is decisive (1 vs 2 seeds) does not hold;
at this sample size there is no detectable effect. One of the eight (seed 11) diverges on
d32 T24 because its state grows each step. Seed 4 found a delta write gated by the state,
`S' = 1.111·S + σ(‖S k‖²)·(v − S k)⊗k`, at tuned-Gated-DeltaNet level (test ow0.3 0.971 Rust,
0.966 JAX). Details: runs/v2-noaddnode/v2-noaddnode_ERGEBNIS.md.

Long-sequence check (3 Nov 2026, runs/v3-baselines): on the new held-out suites with 64 and
128 writes (at most 8 keys), all 14 delta rules found on v2 and tuned v2 Gated DeltaNet
(a = 1.1) collapse (T128 K8 at most 0.081; GDN 0.020), below decayed linear attention
(0.38 to 0.52) and far below DeltaNet with a = 1 (0.828). The v2 rediscovery therefore holds
only for short episodes. Tuned on the v3 train task, Gated DeltaNet moves to a = 1.01 and
DeltaNet (a = 1) is best on T128 (0.850). Timing pilot on v3 (runs/v3-localpilot): 166 s per
seed at 300k; seed 2 already found a delta rule with a = 1 (T128 K8 0.853).

Run v3 (4 Nov 2026, runs/v3, task v3, 16 seeds, 1.5M, add-node on, local, 3.5 h): 12/16 seeds
reach the delta rule (v2: 6/16), median 168,628 candidates. 11 of 12 have growth factor
a = 1.000 (seed 16: 1.015), so the v3 task removed the a > 1 artefact. Delta seeds score
T12 0.918 to 0.937, T64 K8 0.841 to 0.854, T128 K8 0.812 to 0.854, the level of tuned
DeltaNet on v3 (0.923 / 0.852 / 0.850); no seed is better beyond noise. Four seeds use a
nonlinear state-dependent erase or write gate at the same level. All rules reproduce in JAX
within 0.022. Details: runs/v3/v3_ERGEBNIS.md.

Alphabet sensitivity 3a (4 Nov 2026): stopped by decision before completion (extra ops: 1 of
16 seeds finished, no MatVec: not started). No conclusion is drawn. The one finished seed
(extra ops, seed 2) found a delta rule using VecMax at tuned-DeltaNet level (T128 K8 0.845).
Details: runs/v3-extraops/3a_ABBRUCH.md.

Alphabet sensitivity 3a, extra-ops arm completed (4 Nov 2026, resumed on the JupyterHub after the
abort, equality with local checked): with ten generic extra ops the search still finds the delta
family in 9/16 seeds (v3 default alphabet 12/16, Fisher p = 0.46, not significant), but about six
times later (median 998,644 vs 168,628 candidates). All 7 failed seeds use MatTanh, a saturating
memory that stays near linear-attention level on long episodes. Delta seeds: T128 K8 0.841 to
0.855, the level of tuned DeltaNet. The no-MatVec arm is held. Details:
runs/v3-extraops/v3-extraops_ERGEBNIS.md.

Alphabet sensitivity 3a, no-MatVec arm (4 Nov 2026, JupyterHub): without MatVec the delta family is
found in 5/16 seeds (default 12/16, Fisher p = 0.032, significant by the pre-set rule, exactly at
the threshold), always via MatMul with k kᵀ, median 384,372 candidates. The other 11 seeds stay at
decayed linear attention (0.907·S + v kᵀ). Delta seeds reach T128 K8 0.842 to 0.857, tuned-DeltaNet
level. Summary of 3a: the task makes the search find delta (it appears in every alphabet), but the
rate within the budget depends strongly on how short the rule is in the alphabet; any rediscovery
rate must be reported together with the alphabet. Details: runs/v3-nomatvec/v3-nomatvec_ERGEBNIS.md.

