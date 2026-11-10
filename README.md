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
