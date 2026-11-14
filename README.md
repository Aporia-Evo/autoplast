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

Optional, off by default (added 10 Nov 2026, see "Steps 1 to 3" and "Merge"): `--recip` adds
the scalar op `Recip` (`x/(x²+1e-6)`) as a 20th op. `--persist-m N` keeps `M0..M{N-1}` from one
write step to the next and `--persist-v N` keeps `V2..V{1+N}` (state budget); without them
every scratch register is zeroed before every step and a rule is a function of (S, k, v) only.

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


### Stage-2 regimes (added 5 Nov 2026, before any regime result)

Reason: on v2/v3 the delta rule is near-optimal, so a found rule cannot beat tuned DeltaNet
there (CLAUDE.md item 5). `--regime NAME` (any command) replaces the train task by a regime
(96 episodes, train seed 1) and adds a held-out suite `test regime NAME` (512 episodes, seed 9);
the v2/v3 suites are still reported. Without the flag everything is unchanged (checked:
`sweep --task v3` output identical; `baselines` numbers identical).
- `collision`: the 64 keys are drawn around 8 random centres, k = normalize(√c·centre +
  √(1−c)·u) with c = 0.85, giving within-cluster cosine 0.854 (measured), across −0.08.
- `overload`: 32 writes per episode at overwrite rate 0.3, 22.4 distinct keys on average for
  d = 16 (more keys than dimensions).
- `noisyq`: queries use normalize(c·k + √(1−c²)·u) with c = 0.9 instead of k (measured mean
  cosine 0.902); writes use the exact keys.
- `longgap`: 48 episodes of 128 writes with at most 8 distinct keys.
- `collision3` (added after the first regime baselines, before any collision3 result): the
  collision keys with the v3 episode mix (96 standard plus 48 episodes of 64 writes with at
  most 8 keys; the test suite has 512 plus 256). Reason: on the short collision episodes the
  tuned Gated DeltaNet optimum was a = 1.15, which collapses on long episodes.
`autoplast dump --regime NAME [--split test]` writes the task as JSON. `verify/ceiling.py`
fits, per episode, the best linear memory for the final latest pairs by ridge least squares
and decodes like the evaluator. It is an offline in-sample oracle (it fits the very pairs it is
scored on, at most 12 keys at d = 16), not a rule, not reachable headroom and not an upper bound on
accuracy. Only M0 persists between write steps, so RLS/Mesa-type rules are not expressible in the
search space (wording corrected 5 Nov 2026 after review).

### Evolved readout (queue item 5a, added 5 Nov 2026, before any 5a result)

Reason: the readout o = S q was fixed for every rule, so the search could only change how S is
written. With correlated keys (collision3) a linear readout of a single matrix limits what any
write rule can reach. `--evolve-readout` gives every individual a second program, run once per
query with M0 = S, V0 = q, V1 = S q (all else zero); V1 on exit is the readout o. The empty
read program is exactly the fixed readout, and the search starts from it (a first version
that started from a one-instruction MatVec read program deadlocked: with the empty write
program every candidate scores 0, the length penalty then deletes the read instruction, and
the search never climbs; seen in a 60k-candidate smoke test, not a result). Mutations go to
the read or the write program with probability 1/2 each; the length penalty counts both.
Programs without a read program (all earlier runs) behave as before (checked: v3 seed 4 log
rows and an old best.json evaluate identically). verify.py runs the read program in JAX
(checked on a hand-written read program: Rust 0.210 vs JAX 0.211 on T12). verify.py does not
generate the stage-2 regimes itself; regime results are checked on the dumped Rust data (`--task-json`, see Verification).

## Search

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
Since 5 Nov 2026 it also has two collision suites (8 centres, within-cluster cosine 0.85; T12 and
T64 K8) for checking collision3 results. With only 8 random centres per embedding draw, these
suites vary more between draws than the plain ones: on one pilot rule JAX was about 0.03 below
the Rust collision3 test while the plain T12 suite matched within 0.003.

`verify.py --task-json FILE prog.json ...` (5 Nov 2026) instead reads the exact Rust data written by
`autoplast dump --regime <r> --split test|train`, so JAX and Rust see the same episodes. On the collision3
test (768 episodes, 6,503 queries) all 32 best programs of 5a-A and 5a-B, including evolved read programs,
matched the Rust accuracy to the 3-decimal rounding of the summaries (max |diff| 0.0005; runs/5a-A/verify-dump_ERGEBNIS.md).
The 0.03 gap above therefore comes from the separate embedding draw, not from the interpreter.

Since 10 Nov 2026 it also prints a 95% interval per accuracy (queries only, not the draw of
the embeddings) and repeats the structural test of `src/classify.rs`: a least-squares fit of
the update on `a·S + b·(v kᵀ) + c·((S k) kᵀ) + g·((vᵀS k)·v kᵀ)` on memory states the rule
produces on real episodes. Program files with a state budget are run with it.

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
python local_runner.py --seeds 1-16 --budget 1500000 --tag <tag> --parallel 2 --threads 8
python aggregate.py runs/<tag>          # structural families per seed, then accuracy levels
python rescore.py                       # structural test on every committed final rule
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

Stage-2 baselines (5 Nov 2026, runs/stage2-baselines): on the regime test suites tuned DeltaNet
reaches 0.658 (collision), 0.663 (overload), 0.901 (noisyq) and 0.875 (longgap), against an offline
least-squares reference of 1.000, 0.956, 0.971 and 1.000. Collision and overload show the largest gap to
that oracle (an in-sample oracle, not reachable headroom; see Task). Tuned Gated DeltaNet leads on the three short-episode regimes only with a > 1 and then
collapses on T128 K8, so those regimes need long episodes (as in v3) before a fair search.
Details: runs/stage2-baselines/stage2-baselines_ERGEBNIS.md.

Stage 2, queue item 5a on collision3 (5 Nov 2026, JupyterHub, 3 arms x 16 seeds x 1.5M, one binary):
A default alphabet with fixed readout, B evolved readout plus ten extra ops, C evolved readout only.
Delta reached in 7/16, 4/16 and 2/16 seeds; median collision3 test 0.517, 0.521, 0.517; best seeds
0.660, 0.640, 0.638. Pre-registered rule 1 (Mann-Whitney vs A): B p = 0.82, C p = 0.77, not
significant. Rule 2 (test > 0.651, T128 K8 >= 0.838, train - test <= 0.03): no seed passes; the only
seed above 0.651 (A seed 2, delta-like with a |S k| step and tanh terms) reaches only 0.777 on T128 K8.
All delta-reaching seeds sit around untuned delta beta = 0.5 (0.640) and tuned DeltaNet (0.631).
At equal budget neither a free readout nor extra ops help, and no evolved rule beats tuned DeltaNet
here. All 48 best programs reproduce in JAX on the exact Rust test data (max |diff| 0.0005).
Details: runs/5a-A/5a_ERGEBNIS.md, addendum runs/5a-A/5a_NACHTRAG_2026-11-05.md.

## Review and scope correction (10 Nov 2026)

Note added at the merge: this review was written on a branch that did not contain the work
of 3 to 5 Nov reported above (16-seed rates, task v3, alphabet sensitivity, stage-2 regimes,
evolved readout). Findings 1, 4, 5 and 6 stand as written. Findings 2, 3 and 7 had already
been addressed in part: task v3 and the T64 / T128 suites punish growth factors, and the
stage-2 regimes shift the load. The text is kept as it was written.

Code, runs and the current literature were reviewed before any stage-2 compute is spent.
Nothing below is a search result; it changes what the project should claim and measure.

### Findings

1. **The milestones measure accuracy, not rediscovery.** A milestone fires when the best train
   accuracy passes a reference rule's accuracy. v2 seed 1 "reached delta rule β=1" with a rule
   that has no erase term at all. The "gated delta α=0.9" milestone (0.729) lies below linear
   attention (0.772) and fires together with it. A rediscovery rate built on these counts
   would not survive review. Rediscovery needs a structural test (fit to the family on real
   memory states, or algebraic canonicalisation).
2. **The base task has almost no headroom.** Tuned Gated DeltaNet 0.968, ceiling of a linear
   readout 1.000 (table below). All held-out suites keep the same load T/d = 0.75, so they
   test fresh samples, not a shifted regime.
3. **Train noise.** 96 episodes are about 840 queries: ±1.2 points standard error at 0.85. The
   train task is the same for every search seed, so seeds vary the search only, not the data.
4. **The search space cannot express the 2026 rules.** Scratch registers are zeroed every
   step, so a rule is a function of (S, k, v) only: no second state, hence no preconditioner,
   Kalman gain or momentum. There is no reciprocal, so normalised steps (NLMS, Longhorn, RLS)
   are out too.
5. **Constants versus learned gates.** A rule here carries fixed scalars; in a language model
   α_t, β_t, keys and values are learned per token. A win with fixed constants on random unit
   vectors is evidence about the functional form only.
6. **"Tuned Gated DeltaNet" is no longer the bar.** Since May 2026: Gated DeltaNet-2 (NVIDIA,
   NeurIPS 2026; channel-wise erase and write gates, 1.3B / 100B tokens), Erase-then-Delta,
   Preconditioned DeltaNet (diagonal key-Gram preconditioner, 340M / 1B), Kalman Delta
   Networks, Kronecker Delta Rule (scalar bilinear read-out vᵀSk, xLSTM family), Dual DeltaNet,
   Muir. ASI-Arch (COLM 2026) is the LLM-driven counterpart of this project: 1,773 experiments,
   about 20,000 GPU hours, starting from DeltaNet code. None of these was reproduced here;
   they are read from the papers.
7. Confirmed from the README's own reading: the growth factor a > 1 disappears on long episodes
   (optimum a = 1.0 at T = 96). `verify.py` had no d = 8 suite and no noise band (fixed and
   run in "Steps 1 to 3" below).

### Headroom per regime (`python verify/headroom.py`, NumPy, d = 16)

Families tuned on 200 train episodes, reported on 1000 fresh episodes with fresh embeddings.
"Ridge" is batch least squares on the latest (key, value) pairs: the ceiling for the fixed
readout `o = S q`. "Kalman delta" is the delta error with a Kalman gain and keeps a second
d×d state. Both are reference points written by hand, never candidates or seeds.

| regime | lin. att. | DeltaNet | Gated DeltaNet | RLS (2 states) | Kalman delta (2 states) | ridge ceiling |
|---|---|---|---|---|---|---|
| base T12, ow 0.3 | 0.757 | 0.933 | 0.968 | 0.836 | 0.998 | 1.000 |
| full load T24 | 0.576 | 0.763 | 0.835 | 0.824 | 0.949 | 0.997 |
| overload T48 | 0.344 | 0.499 | 0.532 | 0.556 | 0.599 | 0.757 |
| 8 keys rewritten, T96 | 0.078 | 0.871 | 0.871 | 0.098 | 0.958 | 1.000 |
| 14 keys rewritten, T96 | 0.105 | 0.715 | 0.715 | 0.162 | 0.839 | 1.000 |
| clustered keys cos≈0.8, T12 | 0.127 | 0.199 | 0.314 | 0.838 | 0.962 | 1.000 |
| clustered, 8 keys, T48 | 0.042 | 0.206 | 0.205 | 0.181 | 0.686 | 1.000 |

Reading: outside the base task Gated DeltaNet sits 13 to 80 points under the ceiling, and a
known two-state rule closes most of that gap. One hand-written one-state probe
(`S' = aS + b(v − Sk)(k − c·SᵀSk)ᵀ`, the matrix version of seed 1's occupancy signal) gains
0.06 on clustered keys and nothing elsewhere. So the open question is not "beat Gated
DeltaNet" but "how much of the gap is reachable at a given state budget". Single run, one
embedding seed per split; standard error about 0.01.

### Corrected scope

Owner's direction (10 Nov 2026): the paper is about the search method, an improved NEAT-style
evolutionary search as a discovery tool; memory rules are its testbed. The points below then
define the benchmark the method is judged on. The method result itself is a comparison of
search algorithms on the same space, seeds and budget: discovery rate and evaluations needed,
against regularized evolution (AutoML-Zero), random search and each added component removed.
So far the only added component is the add-node mutation, with evidence from 1 versus 2 seeds.

- **Claim to aim for:** a rule found by evolution from the empty program that beats every
  tuned known family *with the same state budget* in a named regime, reported as the fraction
  of the gap to the ridge ceiling it closes. State budget (one d×d matrix, two matrices) is an
  explicit axis.
- **Baselines:** linear attention, DeltaNet, Gated DeltaNet, decoupled erase/write (Gated
  DeltaNet-2, Erase-then-Delta), Kronecker Delta Rule, and for two states RLS and Kalman delta.
- **Target regimes:** rewriting few keys over long episodes, clustered keys, full load.
  The base task stays as the rediscovery test only.
- **Rediscovery, strengthened:** the 2026 rules were published after the op set was fixed.
  Whether the search reassembles them is a held-out test of the method.
- **Search-space changes this needs (both generic, to be logged before results):** registers
  that persist across steps under a stated budget, and a scalar reciprocal.
- **Before any "better" claim:** refit the top structures with learned per-step gates and
  learned keys in a small trained model (MQAR, 2 layers), so the fixed-constant objection is
  answered before a language model is trained.
- **Stage 3 is open.** Published comparisons run at 340M to 1.3B parameters and 15 to 100
  billion tokens on multi-GPU nodes. Whether and how a language-model stage is affordable is
  a decision for the project owner, not settled here.

### Second testbed (planned, 10 Nov 2026)

To show the search is a tool and not a single case, the method is developed on memory rules,
frozen by a commit, and then run unchanged on optimizer update rules (ladder SGD, momentum,
RMSProp, Adam; ceiling Newton / conjugate gradients on quadratics). Details and order are in
CLAUDE.md, "Next experiments". Nothing is implemented yet.

## Steps 1 to 3: structural test, regimes, state budget (10 Nov 2026)

Note added at the merge: flags and regime definitions in this section describe commits
142e94d to 045ea3a. The merged state differs in three points, listed under "Merge": `Recip` is
off by default (`--recip`), the regimes are generated by the stage-2 generator (`overload` is
the 32-write regime, the 48-write one is `overload48`), and summaries print the base suites
plus the suite of the chosen regime. The baseline table of this section was replaced by the
one under "Merge".

Changes to measurement, task and search space, logged here before any search result that
depends on them. No search result is reported in this section.

### What changed and why

- **Structural rediscovery test** (`src/classify.rs`, repeated independently in
  `verify/verify.py`). The rule is run on 32 held-out episodes of the search regime; every write
  step gives a sample (S, k, v, S'). The update is fitted with the four terms listed under
  Verification. R² is taken over the part of the update that is not the carry `a·S`. A rule
  belongs to a family only if R² ≥ 0.99; a coefficient counts as present above 5% of `a`.
  Families: no write, (decayed) linear attention, (gated) delta rule, (gated) Kronecker delta
  rule, mix. "Decayed" and "gated" mean a ≠ 1, including a > 1. The search records the first
  candidate count at which the best rule belongs to each family. Reason: the accuracy
  milestones are not rediscovery (review finding 1). They are still printed, labelled as
  accuracy levels.
- **Regimes** (`--regime`, d = 16): `base` (T12), `full` (T24), `overload` (T48), `rewrite8` and
  `rewrite14` (T96, at most 8 / 14 distinct keys, every further write rewrites one),
  `clustered` (T12, keys around one centre, cos ≈ 0.8), `clustered8` (T48, 8 keys, clustered).
  Each has a held-out suite. `--train-episodes` and `--task-seed` set size and sample of the
  train task. Reason: the base task has no headroom and one fixed, small train set.
- **`sweep`** now tunes linear attention, decayed linear attention, DeltaNet, Gated DeltaNet
  and the Kronecker delta rule (with and without decay) on the train task of a regime and
  prints RLS, Kalman delta (both with a second d×d state, written natively in
  `src/reference.rs`, never part of the search) and the ridge ceiling. Not included: channel-wise
  erase/write gates (Gated DeltaNet-2), which need learned per-channel parameters; their
  scalar version is the old "untied" row, which is redundant because of scale invariance.
- **Search space**: `Recip` and persistent registers (see Search space). Reason: without a
  second state and a reciprocal the space cannot contain preconditioned or normalised rules.
  Both are generic; no rule is encoded. Program files record their state budget.
- Every summary now carries commit, regime, task seed, train episodes and space flags;
  accuracies carry their binomial standard error.

### Checks

- Old seeds reproduce bit for bit with `--no-recip`: best rule and log of two 120k-candidate
  runs (seed 2; seed 5 with `--no-split-edge`) are identical between the old and new binary.
- The structural test labels the five reference rules correctly (`autoplast baselines`).
- Old runs re-scored (`runs/rescore-v1-v2.md`): v2 seed 2 is a gated delta rule (a = 1.098,
  erase 0.725, R² = 1.0000); v2 seed 1 and v1 seed 1 are unclassified (R² = 0.94 and 0.96).
  So by the structural test the delta family was found by 1 of 2 v2 seeds and by 0 of 1 v1
  seeds, the same count as before, now on a criterion that cannot be passed by accuracy alone.
- JAX verification of the three old rules (`runs/verify-v1-v2.txt`): accuracies agree with
  Rust within the 95% interval on all eleven suites (seed 2, base test: 0.967 ±0.003 Rust,
  0.961 ±0.006 JAX), coefficients agree to three digits.
- v2 seed 2 fails on long episodes: 0.03 on `rewrite8` and `rewrite14`, because its growth
  factor 1.098 overflows the state bound after 96 steps. This confirms the degenerate-win
  suspicion about a > 1.
- Smoke test of the second state: one 150k-candidate search on `clustered` with `--persist-m 2`
  runs (95 s on 3 threads, 192 train episodes). It found nothing useful (train 0.164); the
  budget was a tenth of a real run, so this says nothing about the regime.
- `modal_runner.py` passes the new flags through `--extra` and aggregates structural families.
  It was not run here (no Modal access in this session); only its parsing was checked.

## Merge of the two branches and package B (10 Nov 2026)

`exp/v2-rediscovery-rate` (work of 3 to 5 Nov) and the review branch (10 Nov) were merged.
The code of the experiment branch is the basis; the structural test, the state budget, `Recip`,
the two-state references, the ridge ceiling and the extended `sweep` were ported onto it.

### What changed for the user of the binary

- `Recip` is off by default and switched on with `--recip` (it was on by default in commits
  142e94d to 045ea3a; `--no-recip` no longer exists). Every run before 10 Nov reproduces with
  its original command line.
- Regimes are generated by the stage-2 generator. `overload` is the 32-write regime of 5 Nov;
  the 48-write regime is `overload48`. `rewrite8`, `rewrite14` and `clustered8` are made of long
  episodes only; `clustered` is one key centre with cosine 0.8. `--task-seed` and
  `--train-episodes` work for every task.
- `sweep` tunes linear attention, decayed linear attention, DeltaNet, Gated DeltaNet and the
  Kronecker delta rule and prints RLS, Kalman delta and the ridge ceiling. The "untied" row is
  gone (redundant, see 3 Nov). `verify/ceiling.py` (offline least squares) is kept.
- Summaries carry a structure line, the structural families seen during the search, commit,
  task seed and state budget. Program files carry the state budget only when it is not (1, 0).
- `local_runner.py` is the runner of 3 Nov with `--extra`, `--recip`, `--task-seed-from-seed`
  and the new `aggregate.py`. The two package-B tags were run as `v3` and `v3-noaddnode` and
  renamed to `base-recip` and `base-recip-noaddnode`, because `runs/v3` is the task-v3 run.

### Does the merged binary reproduce the committed runs?

Log rows up to 100,000 candidates, merged binary on Linux against the committed `log.csv`:

| run | flags | identical |
|---|---|---|
| v2 seed 3, v2-noaddnode seed 5 | default, `--no-split-edge` | yes |
| v3 seeds 3, 4, 5, 6 | `--task v3` | yes (to 50,000) |
| v3 seeds 1, 2 | `--task v3` | no |
| v3-extraops seed 2, v3-nomatvec seed 4 | `--task v3 --extra-ops`, `--no-op MatVec` | yes |
| 5a-A seed 2, 5a-B seed 3, 5a-C seed 1 | `--regime collision3`, with `--evolve-readout` (`--extra-ops`) | yes |
| base-recip seed 15, base-recip-noaddnode seed 8 | `--recip`, `--no-split-edge` | yes (to 350,000 before the merge) |

v3 seeds 1 and 2 also differ when run with the unmerged experiment branch (commits e90d6d3,
689142e and its head give the same log as the merged binary), so the merge is not the cause.
The v3 tag was run on Windows; the likely cause is a last-bit difference in `tanh` or `exp`
between platforms, which changes a run only when it flips a comparison. Not proven. It means
a committed seed is reproducible on its own platform, not everywhere.

### Package B: base task with `Recip`, add-node on and off

16 seeds each, 1,500,000 candidates, commit 045ea3a, all on the workstation (`runs/base-recip`,
`runs/base-recip-noaddnode`; predictions written before the run in `B_VORHERSAGE.md`).

| | add-node on | add-node off |
|---|---|---|
| final rule in the delta family (structural test) | 4/16 | 5/16 |
| final rule linear attention or decayed linear attention | 11/16 | 10/16 |
| unclassified | 1/16 | 1/16 |
| median candidates to the first gated delta rule, seeds that reach it | 951,796 | 425,460 |

No effect of the add-node mutation (Fisher p = 1.0). The unclassified seed with add-node
(seed 3) is a delta rule with `tanh` on the key, R² = 0.9895, just under the threshold. Every
delta rule found has a growth factor of 1.10 to 1.14 and scores about 0.02 on 96-write
episodes, as on 3 Nov. No rule is above tuned Gated DeltaNet (test 0.959 to 0.967 against
0.969). All 32 rules were run in JAX by the executing agent (`verify.txt`, `rust_vs_jax.md`).
Two seeds were recomputed on a second machine and gave identical logs to 350,000 candidates.

One reported gap was checked: seed 4 on a clustered suite, Rust 0.034 against JAX 0.091. The
same rule scores 0.034 to 0.120 in Rust over six draws of the task, so the gap is the draw of
the embeddings. The ± printed next to accuracies counts queries only and is too small on
clustered regimes.

### Add-node mutation, all evidence

| base task, 1.5M candidates | add-node on | add-node off | Fisher p |
|---|---|---|---|
| structural test (v2 + base-recip) | 9/32 | 11/32 | 0.79 |
| accuracy level of delta β=0.5 | 11/32 | 13/32 | 0.80 |

The add-node mutation, the only component that sets this search apart from regularized
evolution as in AutoML-Zero, has no measurable effect on the rediscovery rate in 64 runs.

### Structural test on every committed final rule (`python rescore.py`)

| tag | setting | seeds | delta family (structural) | accuracy level reached | linear attention family | unclassified |
|---|---|---|---|---|---|---|
| v2 | base task, add-node on | 16 | 5 | 6 | 8 | 3 |
| v2-noaddnode | base task, add-node off | 16 | 6 | 8 | 8 | 2 |
| base-recip | base task, add-node on, `Recip` | 16 | 4 | 5 | 11 | 1 |
| base-recip-noaddnode | base task, add-node off, `Recip` | 16 | 5 | 5 | 10 | 1 |
| v3 | task v3, add-node on | 16 | 11 | 12 | 4 | 1 |
| v3-extraops | task v3, ten extra ops | 16 | 6 | 9 | 1 | 9 |
| v3-nomatvec | task v3, without MatVec | 16 | 4 | 5 | 10 | 2 |
| 5a-A | collision3, fixed readout | 16 | 1 | 7 | 4 | 10 |
| 5a-B | collision3, evolved readout, extra ops | 16 | 2 | 4 | 2 | 12 |
| 5a-C | collision3, evolved readout | 16 | 1 | 2 | 11 | 4 |

Per seed with coefficients: `runs/structural-rescore.md`. Reading: on the base task and on
task v3 the structural count is the accuracy count minus zero to three seeds. Those seeds are
delta rules with a nonlinear gate or key (erase 0.57 to 0.72, R² 0.96 to 0.99). On collision3
the strict test passes far fewer seeds (1 against 7 in 5a-A): the rules there erase by 0.45 to
0.53 but sit at R² 0.94 to 0.99, because clustered keys make `tanh` terms matter more. So the
threshold of 0.99 is a strict lower count, and a rate should be given with both numbers.
The conclusions of 3 to 5 Nov do not change.

### Tuned baselines per task (`runs/sweeps/*.md`)

Families tuned on 192 train episodes of the task, accuracy on that task's held-out suite
(base: T12 ow0.3; v3: T64 K8). Last column: the tuned Gated DeltaNet of that row on T128 K8.
Parameters are in the sweep files. One draw per suite; see the note on ± above.

| task | lin. att. | decayed LA | DeltaNet | Gated DeltaNet | Kronecker | gated Kronecker | RLS (2 states) | Kalman delta (2 states) | ridge ceiling | T128 K8 of tuned Gated DeltaNet |
|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.750 | 0.790 | 0.924 | 0.969 | 0.765 | 0.808 | 0.835 | 0.999 | 1.000 | 0.021 (a=1.1, e=0.70) |
| v3 | 0.104 | 0.446 | 0.840 | 0.833 | 0.085 | 0.499 | 0.140 | 0.959 | 1.000 | 0.809 (a=1.01, e=0.55) |
| full | 0.584 | 0.620 | 0.765 | 0.835 | 0.614 | 0.646 | 0.823 | 0.944 | 0.995 | 0.085 (a=1.05, e=0.55) |
| overload | 0.477 | 0.520 | 0.663 | 0.723 | 0.493 | 0.538 | 0.766 | 0.805 | 0.955 | 0.400 (a=1.03, e=0.50) |
| overload48 | 0.353 | 0.400 | 0.505 | 0.534 | 0.353 | 0.414 | 0.545 | 0.591 | 0.749 | 0.635 (a=1.02, e=0.50) |
| rewrite8 | 0.068 | 0.584 | 0.874 | 0.874 | 0.068 | 0.607 | 0.089 | 0.951 | 1.000 | 0.861 (a=1, e=0.65) |
| rewrite14 | 0.106 | 0.460 | 0.718 | 0.718 | 0.103 | 0.470 | 0.156 | 0.854 | 1.000 | 0.858 (a=1, e=0.60) |
| clustered | 0.120 | 0.162 | 0.205 | 0.410 | 0.120 | 0.177 | 0.845 | 0.958 | 1.000 | 0.000 (a=1.25, e=0.55) |
| clustered8 | 0.040 | 0.165 | 0.205 | 0.206 | 0.039 | 0.181 | 0.195 | 0.680 | 1.000 | 0.683 (a=0.99, e=0.30) |
| collision | 0.524 | 0.553 | 0.658 | 0.725 | 0.530 | 0.571 | 0.839 | 0.991 | 1.000 | 0.000 (a=1.15, e=0.60) |
| collision3 | 0.385 | 0.519 | 0.640 | 0.644 | 0.384 | 0.530 | 0.620 | 0.935 | 1.000 | 0.771 (a=1.01, e=0.50) |
| noisyq | 0.724 | 0.750 | 0.899 | 0.934 | 0.738 | 0.773 | 0.812 | 0.967 | 0.990 | 0.021 (a=1.1, e=0.70) |
| longgap | 0.049 | 0.575 | 0.875 | 0.875 | 0.050 | 0.605 | 0.071 | 0.956 | 1.000 | 0.863 (a=1, e=0.75) |

Reading: the DeltaNet values agree with those of 5 Nov within 0.002 (collision 0.658,
overload 0.663, noisyq 0.901 there). New is the Kalman delta column: a known rule with a second
d×d state reaches 0.94 on collision3, where tuned DeltaNet and every evolved rule of 5a stay
near 0.64, and 0.95 to 0.96 on the long-episode tasks, where DeltaNet reaches 0.84 to 0.88.
The gap that 5 Nov called "an in-sample oracle, not reachable headroom" is therefore
reachable online with two states. Whether one state can reach any of it is open; the 48
searches of 5a did not. Gated DeltaNet's lead on the short tasks (`clustered`, `collision`,
`full`, `noisyq`) comes with a > 1 and collapses on T128 K8, as noted on 5 Nov.

### What this leaves open

The rediscovery rate depends on the task (base 5 to 6 of 16, task v3 11 to 12 of 16) and on
the alphabet (3a), not on the add-node mutation. The method claim in `CLAUDE.md` therefore has
no supporting component yet. The seeds that fail stop at linear attention; a method change
has to show up as fewer such seeds or fewer candidates on the same tasks and seeds.

## Package C: second state on collision3 (released 10 Nov 2026, before any result)

Question: the 48 one-state searches of 5a found no rule above tuned DeltaNet on collision3.
Does the same search find one when a rule may keep a second d×d state?

Design: arm C1 (`runs/c-m2`) is 5a-A with `--persist-m 2` and nothing else changed: task
collision3, task seed 1, 96 train episodes, 19 ops, fixed readout, seeds 1 to 16, 1,500,000
candidates, batch 128. The control is the committed `runs/5a-A`. Arm C2 (`runs/c-m2-recip`)
adds `--recip` and runs only after C1 is reported. The decision rules are those of 5a,
unchanged: rule 1, Mann-Whitney on the test accuracies against 5a-A; rule 2, test > 0.651 and
T128 K8 ≥ 0.838 and train − test ≤ 0.03. Commands: RUNBOOK.md, package C.

Is there anything to find? One hand-written probe says yes (`python verify/probe_two_state.py`,
`runs/sweeps/probe_two_state_collision3.md`). It is a reference only and never enters a search:

    S' = S + β·(v − S k)(k − c·G k)ᵀ        G' = ρ·(G + k kᵀ)

with G in the persistent register, 14 instructions of the default alphabet, no reciprocal.

| rule on collision3 | train | test | T128 K8 |
|---|---|---|---|
| plain delta rule (c = 0), best β by train | 0.617 | 0.640 | 0.828 |
| probe, β = 0.9, c = 0.3, ρ = 0.85 | 0.662 | 0.679 | 0.857 |
| probe, β = 0.7, c = 0.2, ρ = 0.85 | 0.663 | 0.674 | 0.872 |
| Kalman delta (two states, not in the search space) | – | 0.935 | – |

The probe passes rule 2 and reproduces in JAX on the exact Rust test data (0.6789 against
0.679). So the two-state space contains at least one rule about 0.04 above every one-state
family, on one task draw and a grid of 72 settings; a first attempt without decay of G was
worse than the plain delta rule. The exact Kalman rule is not expressible (a persistent
register starts at zero and there is no matrix inverse), so 0.935 is a reference, not a target
the search is known to be able to reach. What C can show: whether the search finds the probe's
level or better (discovery claim), or does not find it although it exists (which would be
evidence about the search method, the open point above). Limits: the probe was written by
hand after seeing the Kalman reference, so it says nothing about how easy the rule is to
find; and C changes the search space, not the search algorithm.

## Package C, arm C1: result and reading (11 Nov 2026)

Run by the executing agent: `runs/c-m2`, 16 seeds, 1,500,000 candidates, commit 21e513a,
4.56 h on the workstation, predictions committed before the run (1b82762). Facts per seed:
`runs/c-m2/c-m2_report.md`. Checks below: `runs/c-m2/checks_2026-11-11.md`,
`python verify/c1_checks.py`.

Task option added for these checks, after the run and not used in any search: `--query-gap N`
writes N extra pairs with fresh keys after the last regular write of an episode and never
queries them. Default 0 leaves every task unchanged (5a-A seed 2 reproduces to 50,000).

### Outcome against the pre-set rules

| | c-m2 (two states) | 5a-A (one state, control) |
|---|---|---|
| median collision3 test | 0.634 | 0.517 |
| rule 1, Mann-Whitney on test accuracy | p = 0.33, not significant | |
| rule 2 passed (test > 0.651, T128 K8 ≥ 0.838, train − test ≤ 0.03) | 3/16 (seeds 2, 6, 9) | 0/16 |
| above the hand-written probe (0.679) with rule 2's other conditions | 1/16 (seed 2, 0.695) | 0/16 |
| JAX against Rust on the dumped test data, largest difference | 0.0005 | |

Rule 1 fails because both arms split into the same two groups: seeds stuck at decayed linear
attention (7 of 16 here, test 0.51) and seeds at delta level or above (9 of 16, 0.63 to 0.70).

### Do the gains hold on other draws of the task?

Yes. Twelve fresh task draws, gain paired per draw against tuned DeltaNet (mean 0.643):

| rule | mean | gain | draws won |
|---|---|---|---|
| tuned Gated DeltaNet | 0.646 | +0.003 ± 0.001 | 10/12 |
| hand-written probe | 0.685 | +0.041 ± 0.002 | 12/12 |
| c-m2 seed 2 | 0.697 | +0.054 ± 0.001 | 12/12 |
| c-m2 seed 9 | 0.686 | +0.043 ± 0.001 | 12/12 |
| c-m2 seed 6 | 0.658 | +0.015 ± 0.001 | 12/12 |
| c-m2 seed 1 (second state unused) | 0.669 | +0.026 ± 0.001 | 12/12 |
| 5a-A seed 2 (one state) | 0.665 | +0.022 ± 0.001 | 12/12 |

Two one-state rules are also above tuned DeltaNet on every draw; they fail rule 2 on T128 K8
(0.799 and 0.777), which is why 5a reported no rule above the baseline.

### What the two best rules do

Seed 2, in closed form (constants collected by hand, checked: 0.696 against 0.697 as found):

    P' = 0.990·(P + v kᵀ)(I − 0.490·kkᵀ)        S' = c·(P + v kᵀ)(I − 0.956·kkᵀ)

The memory is P, a delta rule with a soft erase. S, which the fixed readout uses, does not
depend on the old S at all: it is P plus the newest pair with a near-complete erase along
the newest key. Ablation of that read-side erase r: r = 0.49 makes S a copy of P, a one-state
rule, and scores 0.639 (tuned DeltaNet 0.643); r = 0.85 gives 0.688, r = 0.956 gives 0.696,
r = 1.0 collapses to 0.574. So the whole gain comes from erasing harder for reading than for
storing, which one state cannot do. Because `S q = c·(P + v kᵀ)(q − r·(k·q)·k)`, the same rule
can be read as a query projected against the most recent key before reading P.

Seed 9, read from its formula with unit values:

    S' = (S + 1.677·v kᵀ + 0.888·v₋ k₋ᵀ)(I − 0.789·kkᵀ)        P' holds the previous pair (v₋, k₋)

A delta rule that writes every pair a second time one step later.

Is the gain an artefact of every query following directly on the last write? Partly tested
with `--query-gap` on the same twelve draws, DeltaNet retuned per row:

| extra unqueried writes | DeltaNet | seed 2 | seed 9 | probe |
|---|---|---|---|---|
| 0 | 0.643 | +0.053 | +0.042 | +0.041 |
| 1 | 0.571 | +0.054 | +0.044 | +0.045 |
| 2 | 0.507 | +0.041 | +0.028 | +0.036 |
| 4 | 0.399 | +0.020 | −0.002 | +0.017 |

The gain of seed 2 survives one and two intervening writes and shrinks to +0.020 at four,
where every rule is near 0.40. Seed 9 loses its gain at four. So the rules are not only
exploiting the position of the queries, but their benefit is tied to recent writes.

### What can be claimed

- Not claimed: "better than every tuned known family at the same state budget". The project's
  own rule 2 puts Kalman delta in the comparison at two states, and it reaches 0.935 on this
  test. Seed 2 at 0.695 is above every one-state family and above RLS (0.620) and far below
  Kalman delta. Measured against the ridge ceiling it closes about 15% of the gap that tuned
  DeltaNet leaves; Kalman delta closes about 82%.
- Supported: with a second state the search finds, from the empty program, rules that use it
  and that beat every one-state family on collision3 under the unchanged rule 2, in 3 of 16
  seeds, robustly over task draws. One of them is above a rule written by hand for the purpose.
- Rate: 3 of 16 seeds pass rule 2, 1 of 16 beats the probe. Rule 1 is not met.
- Literature, checked 11 Nov 2026 by search and abstract or method section, not exhaustively:
  nothing found that states seed 2's rule. Its neighbours are query-side corrections of the
  readout: Muir (per-channel gain on the query, Nov 2026), MesaNet and Gated KalmaNet (query
  preconditioned by a key-covariance state), the query transform in Preconditioned DeltaNet.
  Seed 9's second write of the previous pair resembles the previous-token term of Mamba-3.
  Both are best described as small members of known ideas, not as new rules.
- Limits: one task family, fixed constants on random embeddings (review finding 5), one run of
  16 seeds, and a search space change rather than a search method change. The seven stuck
  seeds are the same failure as before.

### Why Kalman delta cannot be found yet

A persistent register starts at zero and there is no matrix inverse or identity, so neither
`P₀ = I/λ` nor `+ q·I` can be written. Recursive least squares with a forgetting factor
(`P' = (P − g (P k)ᵀ)/λ`, about 13 instructions with `Recip`) would be expressible if a
persistent register could start at the identity. That is a generic change, not made here;
see CLAUDE.md, next experiments.

## A known target inside the search space: Kalman delta (11 Nov 2026, before any search)

Search-space option added: `--persist-init identity` starts the persistent matrix registers
M1.. of every episode as the identity instead of zero (M0, the memory, always starts empty).
Reason: without an identity neither `P₀ = I/λ` nor `+ q·I` can be written, so recursive least
squares and the Kalman delta rule were outside the space. The option is generic (the identity
is the neutral element of the matrix product) and encodes no rule. Off by default; program
files record it; `verify.py` follows it; c-m2 seed 2 still reproduces to 50,000 candidates.

Two known rules were then written by hand in the space as references (`python
verify/probe_rls.py`, `runs/sweeps/probe_rls_collision3.md`). They never enter a search.

    g = P k / (δ + kᵀP k)        S' = S + (v − S k) gᵀ

    RLS with forgetting:   P' = ρ·(P − g (P k)ᵀ)          2 states, 14 instructions
    Kalman delta:          P' = P − g (P k)ᵀ + q·I        3 states, 15 instructions

Kalman delta needs the identity at every step; it sits in a third persistent register that
the rule never writes, so the nominal budget is three matrices and the effective one two.
Both need `--recip`.

| rule on collision3, best setting by train | train | test | T64 K8 | T128 K8 | rule 2 |
|---|---|---|---|---|---|
| tuned DeltaNet (one state) | 0.617 | 0.640 | – | 0.828 | no |
| c-m2 seed 2 (found by the search, two states) | 0.683 | 0.695 | – | 0.861 | pass |
| RLS with forgetting, δ = 0.01, ρ = 1.1 | 0.940 | 0.933 | 0.871 | 0.000 | no |
| RLS with forgetting, δ = 0.01, ρ = 1.05 | 0.867 | 0.856 | 0.666 | 0.662 | no |
| Kalman delta, δ = 0.01, q = 0.003 | 0.932 | 0.933 | 0.944 | 0.950 | pass |
| Kalman delta, native reference (`sweep`) | – | 0.935 | – | – | – |
| ridge ceiling | – | 1.000 | – | – | – |

Reading: RLS with forgetting reaches 0.93 on the test but fails long episodes, because P
grows by ρ per step in directions that are never written and passes the state bound after
128 steps (score 0), or forgets too little (ρ = 1.05). No setting of the grid passes rule 2.
Kalman delta written in the space matches the native reference (0.933 against 0.935), holds
on T128 K8 (0.950) and passes rule 2 by a wide margin. One setting was checked in JAX on the
exact Rust test data (δ = 0.1, q = 0.01: 0.8887 against 0.889).

What this gives the project: in the space `--persist-m 3 --persist-init identity --recip`
there is a known rule of 15 instructions at 0.93 on collision3, where the best rule the search
has found is at 0.70 and every one-state family at 0.64. The delta rule takes 4 to 6
instructions and is found in a third to three quarters of seeds, so the present search is
not expected to reach a 15-instruction rule in 1.5M candidates. That is a prediction, not a
result. If it holds, this is a fixed target for the method claim: how often and after how
many candidates does a search algorithm reach rule 2 with test above, say, 0.85. If the
present search does reach it, that is a rediscovery of a 2026 rule family (Kalman Delta
Networks, MesaNet) from the empty program. No search has been run in this space.

## Package D: search in the space that contains Kalman delta (released 11 Nov 2026, before any result)

Design: the present search, unchanged, on collision3 with `--persist-m 3 --persist-init
identity --recip`; task seed 1, 96 + 48 train episodes, fixed readout, seeds 1 to 16,
1,500,000 candidates, batch 128 (`runs/d-kalman`). Controls: `runs/5a-A` (one state) and
`runs/c-m2` (two states, zero start, no reciprocal). Commands: RUNBOOK.md, package D.

The space differs from c-m2 in three things at once (third register, identity start,
reciprocal), so a difference to c-m2 cannot be assigned to one of them. That is accepted:
the run asks one question, whether the search reaches a rule that is known to exist.

Decided before the run:
- Main count: seeds with collision3 test > 0.85 that also meet T128 K8 ≥ 0.838 and
  train − test ≤ 0.03. The hand-written Kalman delta rule is at 0.933 / 0.950.
- Also reported: rule 1 (Mann-Whitney on test accuracy) against c-m2 and against 5a-A, rule 2
  of 5a unchanged, seeds above the best rule of C1 (0.695).
- Reading. Main count 0: the space holds a rule the search does not reach at this budget;
  the run then becomes the baseline arm for every later search algorithm on the same seeds.
  Main count ≥ 1: check whether the rule is Kalman delta or RLS in substance (gain
  `P k/(c + kᵀP k)`, error-correcting write, update of P), on fresh task draws and with
  `--query-gap`, before calling it a rediscovery.
- Prediction of the research agent: main count 0 with probability 0.85; at least one seed
  above 0.695 with probability 0.6. Reason: 15 instructions against 4 to 6 for the delta
  rule, which is found in a third to three quarters of seeds.
- A smoke test of the runner in this space (2 seeds, 40,000 candidates) ran through on the
  review machine. It is not a result.

## Package D: result and reading (13 Nov 2026)

Run by the executing agent: `runs/d-kalman`, 16 seeds, 1,500,000 candidates, commit e979a8e,
6.13 h on the university machine, predictions committed before the run (1a4dd1b). Facts per
seed: `runs/d-kalman/d-kalman_report.md`. Checks below: `runs/d-kalman/checks_2026-11-13.md`,
`python verify/d_checks.py`.

### Outcome against what was fixed before the run

| | d-kalman | c-m2 | 5a-A |
|---|---|---|---|
| main count: test > 0.85, T128 K8 ≥ 0.838, train − test ≤ 0.03 | 1/16 (seed 9: 0.855 / 0.885 / +0.008) | 0/16 | 0/16 |
| above the best rule of C1 (0.695) | 2/16 (seeds 7, 9) | – | – |
| rule 2 passed | 4/16 (seeds 2, 7, 9, 15) | 3/16 | 0/16 |
| median test | 0.638 | 0.634 | 0.517 |
| rule 1, Mann-Whitney against d-kalman | – | p = 0.44 | p = 0.097 |
| JAX against Rust on the dumped test data, largest difference | 0.0005 | | |

The research agent predicted a main count of 0 with probability 0.85, and so did the
executing agent. Both were wrong. Rule 1 is again not met: 4 seeds stop at decayed linear
attention (test 0.51 to 0.52) and most of the rest sit at delta level.

### Does seed 9 hold up?

Yes, on every check made. Twelve fresh task draws, paired against tuned DeltaNet (0.643):
seed 9 scores 0.864 (+0.221 ± 0.003, 12/12 draws), seed 7 0.721 (+0.078), the best rule of C1
0.697, hand-written Kalman delta 0.934. With extra unqueried writes before the queries the
lead of seed 9 over retuned DeltaNet grows (+0.221, +0.274, +0.312, +0.345 at 0, 1, 2, 4
writes), so it does not depend on the queries following the last write. It keeps its level on
the suites it was not searched on: T12 0.954, T64 K8 0.940, T128 K8 0.885, d = 32 0.918,
d = 8 0.799. Train and test agree (0.863 / 0.855).

### What seed 9 is

In closed form, checked to reproduce the rule exactly (0.864 on the same draws); P1 and P2
are the two persistent registers and start as the identity:

    r   = P1ᵀ k                              the part of k not covered by earlier keys
    u   = r / |r|                            (as found: 0.25·r / (0.25·|r| + 1e-6))
    P1' = P1 − <u,u>·(P1 k) uᵀ               remove that direction from P1, incompletely
    P2' = 0.80·(P2 + 6·norm(tanh v) uᵀ)      decayed Hebbian write, addressed by u instead of k
    S'  = P2 + 6·norm(tanh v) uᵀ − P1'       the −P1' term changes nothing (0.865 without it)

It is linear attention with decay, written at an address u that is the key made orthogonal to
the keys written before. P1 is the running projector that produces this address. There is no
error term `v − S k`, no reciprocal and no gain of the form `P k/(c + kᵀP k)`; overwriting
works through the decay alone. Ablations: without the decay 0.345; with an exact projector
update `P1' = P1 − u uᵀ` 0.369, because a key that is removed completely cannot be rewritten;
the odd `0.25` and `<u,u>` factors are worth 0.026 (they silence the write when the residual is
numerically zero); `norm(tanh v)` instead of `v` changes nothing.

### What can be claimed

- It is not a rediscovery of Kalman delta or RLS. It shares their second state: P1 plays the
  role of RLS's P for a vanishing regulariser, the projector onto the directions not yet
  written. It lacks their error-correcting write. Under the reading fixed before the run this
  is "not Kalman delta or RLS in substance".
- It is a rediscovery of an old idea: an associative memory that orthogonalises its inputs
  with a novelty filter (Kohonen and Oja, 1976, "Fast adaptive formation of orthogonalizing
  filters and associative memory"; orthogonal-projection memories in Kohonen's work of the
  1970s). Checked on 13 Nov 2026 with two web searches; the paper index used earlier was not
  reachable. In the 2023 to 2026 linear-attention literature the searches found no rule of
  this form; the nearest named neighbour is linear attention via orthogonal memory (LAVO,
  2023), which orthogonalises for compression, not per write. This is not an exhaustive check
  and no novelty is claimed.
- Not claimed: "better than every tuned known family at the same state budget". Kalman delta
  is at 0.934 on the same draws. Seed 9 closes about 62% of the gap between tuned DeltaNet and
  the ridge ceiling, Kalman delta about 82%, the best rule of C1 about 15%.
- Supported: from the empty program, with no rule in the loop, the search assembled in 1 of 16
  seeds a 22-instruction rule that keeps a projector state, beats every one-state family by
  0.22 on collision3 and holds on long episodes. The step came late: train accuracy stood at
  0.711 from 600,000 to 1,200,000 candidates and rose to 0.863 by 1,250,000.
- Rate: 1 of 16. With a base rate this low the result says the rule can be found, not how
  often. Limits as before: one task family, fixed constants on random embeddings, three
  changes of the search space at once against c-m2.

### The benchmark this gives

Space `--persist-m 3 --persist-init identity --recip` on collision3, 1.5M candidates, present
search: test > 0.85 under rule 2's other conditions in 1/16 seeds, above 0.695 in 2/16, rule 2
in 4/16. A known rule at 0.93 is in the space and was not reached. These are the numbers a
changed search algorithm has to beat on the same seeds.

## Package E: seeds 17 to 32 of package D (released 13 Nov 2026, before any result)

Package D gave 1 seed in 16 above 0.85. A method comparison against a base rate estimated
from one success is not informative, so the same setting is run on seeds 17 to 32: same
space, task, budget and batch, same machine and unchanged search code, same tag
(`runs/d-kalman`). Commands: RUNBOOK.md, package E.

Fixed before the run: the counts are those of D (main count: test > 0.85, T128 K8 ≥ 0.838,
train − test ≤ 0.03; seeds above 0.695; rule 2), reported for the new 16 seeds alone and for
all 32. The base rate for later comparisons is the count over all 32, whatever the new seeds
show; seeds 1 to 16 are not dropped or reweighted. Prediction of the research agent for the
new 16 seeds: main count 0 with probability 0.45, 1 with 0.35, 2 or more with 0.20; at
least one seed above 0.695 with probability 0.85. (The last prediction of this kind, a main
count of 0 with 0.85 for D, was wrong.)

## Package E: result, and the base rate over 32 seeds (14 Nov 2026)

Run by the executing agent: seeds 17 to 32 of `runs/d-kalman`, same machine and binary as D
(commit e979a8e in every summary), 5.37 h, predictions committed before the run (107f920).
Facts per seed: `runs/d-kalman/e_report.md`. The counts below were recomputed from the 32
summaries and agree with the report.

| collision3, space of package D, 1.5M candidates | seeds 17–32 | seeds 1–16 | all 32 |
|---|---|---|---|
| main count: test > 0.85, T128 K8 ≥ 0.838, train − test ≤ 0.03 | 0 | 1 (seed 9) | 1/32 |
| above 0.695 (best rule of C1) | 0 | 2 (7, 9) | 2/32 |
| rule 2 passed | 2 (24, 25) | 4 (2, 7, 9, 15) | 6/32 |
| stuck at decayed linear attention level (test < 0.53) | 8 | 4 | 12/32 |
| median test | 0.553 | 0.638 | 0.630 |
| rule 1 against c-m2 / against 5a-A (Mann-Whitney p) | 0.72 / 0.52 | 0.44 / 0.097 | 0.82 / 0.18 |

Best new seed: 27 with test 0.687. No new seed is above 0.72, so there is no second rule of
the kind of seed 9. Seed 22 scores 0.000 on the test in Rust because one of the 768 test
episodes passes the state bound and the guard zeroes the suite; JAX without the guard
measures 0.515; with train 0.519 it fails rule 2 either way. For the other 31 seeds JAX and
Rust differ by at most 0.0005.

Prediction check: the research agent gave a main count of 0 a probability of 0.45 (it
happened) and "at least one new seed above 0.695" a probability of 0.85 (it did not).

### Reading

- Seed 9 stays a single event: 1 in 32, with a 95% interval from about 0.5% to 16%. The claim
  remains "the search can find it", not a rate. Nothing about the rule itself changes; it
  was checked on fresh task draws on 13 Nov.
- The first 16 seeds looked better than the second 16 on every count. That is what a small
  sample does; as fixed before the run, the base rate is the count over all 32.
- Rule 1 is not met against either control over 32 seeds. The larger space does not shift
  the distribution of outcomes; it adds a thin upper tail.
- Twelve of 32 seeds made their last gain in train accuracy after 1,000,000 candidates, five
  after 1,300,000. The search has not converged at this budget, so "more candidates" is a
  control every method comparison needs.

### The baseline arm for method comparisons

Setting: collision3, `--persist-m 3 --persist-init identity --recip`, seeds 1 to 32, 1.5M
candidates, present search. Numbers to beat on the same seeds, with the size of effect that
32 against 32 seeds can show (one-sided Fisher test, p < 0.05):

| measure | present search | needed in a new arm |
|---|---|---|
| rule 2 passed | 6/32 | 13/32 or more |
| stuck at decayed linear attention level | 12/32 | 5/32 or fewer |
| main count (test > 0.85) | 1/32 | 6/32 or more |

Only a large change of the search shows up at this sample size. The main count is too rare
to serve as the primary measure; rule 2 and the stuck count are the usable ones, together
with candidates to the first rule-2 level, which the logs do not hold yet (they record train
accuracy every 50,000 candidates).

