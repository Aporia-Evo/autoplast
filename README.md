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
| main count (test > 0.85) | 1/32 | 7/32 or more |

Only a large change of the search shows up at this sample size. The main count is too rare
to serve as the primary measure; rule 2 and the stuck count are the usable ones, together
with candidates to the first rule-2 level, which the logs do not hold yet (they record train
accuracy every 50,000 candidates).

## Search method, first change: constants tuned per structure (14 Nov 2026, before any result)

Three additions to the search code, all off by default; with them off, committed runs
reproduce (v2 seed 3 to 100,000 candidates, d-kalman seed 9 to 50,000).

**`--tune-consts K`.** The present search changes either the structure of a rule or one
constant per mutation, so a new structure is judged with whatever constants it happens to
carry. With the option, a child whose structure (its effective code without the values of its
constants) has not occurred before in the run, and that contains a constant, is evaluated
together with K copies whose constants are perturbed: each constant is rescaled by a
log-normal factor (probability 0.5), shifted by a normal step (0.3) or redrawn from the
initial range (0.2). The best of the K + 1 enters the population. Every copy counts as a
candidate, so an arm with tuning and an arm without spend the same budget. No rule or
constant value is encoded.

Why this first:
- Seed 9 of d-kalman built its constants out of structure: a write gain of 6 from three
  vector additions, 0.25 from `σ(0)·σ(0)`. That spends instructions and search time.
- Measured on the collision3 train task (64 draws of the constants from the initial range
  each; scratch measurement, not in `runs/`): the seed-9 structure scores above the level of
  decayed linear attention in 0 of 64 draws (tuned: 0.863), so a search that hits it with the
  wrong constants discards it. The Kalman delta structure is different: it beats tuned
  DeltaNet in 35 of 64 draws (median 0.670, tuned 0.932). Kalman delta is therefore missed
  for want of the structure, and constant tuning is not expected to bring it within reach.
- The draw of the seed-9 structure used a raw decay; the rule as found passes it through a
  sigmoid, so the 0 of 64 overstates the difficulty somewhat.

Known limits: more tuning on the fixed train episodes can raise train accuracy without test
accuracy (rule 3); and tuning constants inside a structure search is standard in symbolic
regression, so it is a component to be ablated, not a contribution on its own.

**`--algo random`.** Baseline without selection: every candidate is a fresh program of 1 to
24 random instructions, the best is kept.

**`--val-log`, `--level-acc A`, `--level-long L`.** Logging only. At every log row the best
rule is scored on a validation draw of the train task and on 128-write episodes (seeds that
no suite uses); two columns are appended to `log.csv`, and the first row with validation
> A, long-episode accuracy ≥ L and train − validation ≤ 0.03 is written to the summary.
Nothing of it reaches the search.

A function test on the base task (2 seeds, 300,000 candidates, with and without
`--tune-consts 8`; random search 100,000) ran through. It is not a result.

### Package F: first measurement, on the base task

The base task is used first because a seed takes minutes there and the failure is the same
as elsewhere (seeds stop at decayed linear attention). Arms, 16 seeds, 1,500,000 candidates,
default 19-op alphabet, one state, add-node on:

| tag | flags |
|---|---|
| `f-tune8` | `--tune-consts 8 --val-log` |
| `f-tune3` | `--tune-consts 3 --val-log` |
| `f-random` | `--algo random --val-log` |

Baseline: the committed `runs/v2` and `runs/v2-noaddnode`, pooled (the add-node mutation made
no difference): final rule at the accuracy level of delta β = 0.5 in 14/32 seeds, in the
delta family by the structural test in 11/32. Fixed before the run:
- Primary count per arm: seeds whose best rule reaches the accuracy level of delta β = 0.5
  (the line `delta rule (beta=0.5)` under Milestones), and next to it the structural count.
- An arm of 16 seeds shows at one-sided p < 0.05 with 12/16 on the first count or 11/16 on
  the second. Anything less is reported as "no detectable effect at this sample size".
- Also reported: median candidates to that level among seeds that reach it, seeds ending at
  linear attention level, train minus test, and growth factors (the base task rewards a > 1).
- A positive result here is not a claim about the method; it decides whether the arm is
  worth 6-hour runs on collision3 in the space of packages D and E.
- Prediction of the research agent: `f-tune8` reaches 5 to 9 of 16 on the primary count with
  probability 0.6 and 12 or more with probability 0.1; `f-random` reaches it in 0 of 16
  with probability 0.9.

## Package F: result and reading (15 Nov 2026)

Run by the executing agent on the university machine, commit 6df6477, 2.3 h for the three
arms, predictions committed before the run (345dc58). Facts per seed: `runs/f-tune8/f_report.md`,
`runs/f-tune3/f_report.md`, `runs/f-random/f_report.md`. The counts below were recomputed from
the summaries and agree with the reports.

| base task, 16 seeds, 1.5M candidates | accuracy level of delta β = 0.5 | median candidates to it | delta family, structural | ends at linear attention level | mean train − test |
|---|---|---|---|---|---|
| `f-tune8` | 7/16 | 292,436 | 5/16 | 9/16 | +0.019 |
| `f-tune3` | 8/16 | 135,100 | 6/16 | 8/16 | +0.017 |
| `f-random` | 0/16 | – | 0/16 | 16/16 | +0.022 |
| baseline, `v2` + `v2-noaddnode` | 14/32 | 388,980 | 11/32 | 17/32 | +0.018 |

By the rule fixed before the run (12/16 on the first count or 11/16 on the second), neither
tuning arm shows an effect: **no detectable effect of constant tuning on the base task at
this sample size.** The rates are the baseline's. The lower medians are within the spread of
the baseline itself (86,000 in `v2`, 497,000 in `v2-noaddnode`). The research agent had
predicted this outcome (5 to 9 of 16 with probability 0.6).

What the run does show:
- Tuning does not cost anything at equal budget: the same rate although every new structure
  spends up to 9 or 4 candidates. It also does not raise train minus test.
- Random search finds plain linear attention (two instructions, train 0.772) in all 16 seeds
  and nothing beyond it. Selection is what gets the search past linear attention at all;
  that is the first measured baseline of the method claim.
- Three delta rules with growth factor 1.000 appeared (two in `f-tune8`, one in `f-tune3`);
  those hold on long episodes (T128 K8 0.83), the others have a ≈ 1.09 to 1.14 and do not.
  The baseline arms had none in 14 delta seeds on this task. Three of eleven against none of
  fourteen is suggestive, not established, and it was not a pre-set count.
- JAX agrees with Rust within 0.017 on test ow0.3 for all 48 rules.

Reading for the next step. The sentence fixed before the run was that a positive result
decides whether the arm goes to collision3. There is no positive result, so on this evidence
it does not. The base task was, however, a weak test of this component: the delta rule's
constants are uncritical there, while the measurement that motivated the change was made on
a structure whose constants are critical (seed 9 of d-kalman). Whether to test tuning where
that applies, despite the null here, is a decision for the owner and is not taken in this
file.

## Search method, second change: parent selection by behaviour (15 Nov 2026, before any result)

Decided with the owner on 15 Nov 2026: build the second component (niching by behaviour), and
in parallel test constant tuning where constants are critical, although package F showed no
effect on the base task (package G below; this departs from the sentence fixed before F and
is the owner's decision, for the reason given under "Package F: result and reading").

**What is added.** Every individual keeps its behaviour: the number of correct queries on
each train episode. `--select` chooses how the parent is picked among the 10 individuals
drawn for a tournament. All of it is off by default (`--select fitness`), and committed runs
reproduce with it off (v2 seed 3 to 100,000 candidates; f-tune8 seed 9 to 50,000).

- `--select share`, fitness sharing. An individual's fitness is divided by its niche count:
  the number of individuals in the population whose behaviour lies within a radius, each
  weighted by 1 − distance/radius, distance = summed absolute difference of the per-episode
  counts. `--share-radius` is that radius as a fraction of all train queries (default 0.05).
  This is the mechanism NEAT's speciation uses to protect new structure, with distance taken
  between behaviours instead of genomes.
- `--select lexicase`, lexicase selection inside the tournament. Train episodes are drawn at
  random one after another; after each, only the candidates with the most correct queries on
  that episode stay; when one is left, or after 32 episodes, the fittest of those left is the
  parent. It favours rules that are best on some episodes even if their overall accuracy is
  lower.

Neither option names a rule or an op; both act on which episodes a rule gets right.

**Why.** In every run the seeds split into the same two groups and a third to a half stop at
decayed linear attention (17/32 on the base task, 12/32 in the space of D and E); improvements
come late and rarely (seed 9 of d-kalman after 1.2M candidates). With 500 individuals and
tournaments of 10 the population is expected to sit on one behaviour; that was not measured
directly. Random search (package F) shows that selection is what carries the search past
linear attention, so selection is the place to change. Both options are standard (fitness
sharing: Goldberg and Richardson 1987, NEAT 2002; lexicase: Spector 2012); what is to be
measured is whether they change the rate here.

**Cost.** Fitness sharing compares all pairs of the population once per batch and, by keeping
the population spread, lowers the share of cached evaluations. In a function test on the base
task (2 seeds, 300,000 candidates, one thread) it took about four times the wall time of the
plain search; lexicase took the same time as the plain search. In that test both `share` seeds
ended on a delta rule and both `lexicase` seeds on linear attention. Two seeds at a fifth of
the budget are not a result.

### Package H: selection by behaviour on the base task

Base task (v2 setting), seeds 1 to 32, 1,500,000 candidates, batch 128, one machine for all
arms:

| tag | flags |
|---|---|
| `h-base` | `--val-log` (the plain search, as baseline on the same machine and seeds) |
| `h-share` | `--select share --val-log` |
| `h-lexicase` | `--select lexicase --val-log` |

Fixed before the run:
- Counts per arm: seeds reaching the accuracy level of delta β = 0.5; seeds whose final rule
  is in the delta family by the structural test; seeds ending at linear attention level
  (train < 0.84).
- An arm shows an effect if a one-sided Fisher test against `h-base` gives p < 0.05 on the
  first or the second count. With `h-base` near the earlier rate (14/32) that takes about
  21/32. The two tests per arm and two arms are four tests; a single p just under 0.05 is to
  be read with that in mind.
- Also reported: median candidates to the level, train − test, growth factor and T128 K8 of
  every delta rule (does the arm find more rules that only work on short episodes?),
  real evaluations and wall time (does the arm win per candidate but lose per second?).
- Prediction of the research agent: `h-share` shows an effect by the rule above with
  probability 0.4, `h-lexicase` with 0.15; `h-base` gives 11 to 17 of 32 on the first count
  with probability 0.7.

### Package G: constant tuning in the space of packages D and E

collision3, `--persist-m 3 --persist-init identity --recip`, seeds 1 to 32, 1,500,000
candidates, `--tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838` (`runs/g-tune8`),
on the machine of D and E. Baseline: the 32 seeds of `runs/d-kalman`.

Fixed before the run: the counts are those of E. The arm shows an effect with rule 2 in 13/32
or more (baseline 6/32), at most 5/32 seeds stuck below 0.53 (baseline 12/32), or test > 0.85
in 7/32 or more (baseline 1/32). Also reported: seeds whose rule has the shape of seed 9, and
train − test. Prediction of the research agent: rule 2 in 5 to 10 of 32 with probability 0.6,
13 or more with probability 0.12; at least one seed above 0.85 with probability 0.45.

## Package H: result and reading (15 Nov 2026)

Run by the executing agent on the university machine, commit ad31161, 7.2 h, predictions
committed before the run (fcb1b3c). Facts per seed: `runs/h-base/h_report.md`,
`runs/h-share/h_report.md`, `runs/h-lexicase/h_report.md`. Counts below recomputed from the
summaries; they agree with the reports.

| base task, 1.5M candidates | `h-base` | `h-share` | `h-lexicase` |
|---|---|---|---|
| seeds finished | 32 | 31 (seed 16 aborted, see below) | 32 |
| accuracy level of delta β = 0.5 reached | 12/32 | 31/31 | 32/32 |
| one-sided Fisher against `h-base` | – | p = 1.7e-8 | p = 1.2e-8 |
| delta family by the structural test | 12/32 | 19/31 | 10/32 |
| one-sided Fisher against `h-base` | – | p = 0.051 | p = 0.78 |
| ends at linear attention level (train < 0.84) | 19/32 | 0/31 | 0/32 |
| test ow0.3, median over seeds | 0.798 | 0.950 | 0.969 |
| test ow0.3, best seed | 0.971 | 0.970 | 0.975 |
| mean train − test | +0.019 | +0.005 | +0.007 |
| median candidates to the level | 140,340 | 90,100 | 74,548 |
| real evaluations per seed, mean | 457,000 | 940,000 | 747,000 |
| minutes per seed, mean | 4.9 | 12.2 | 9.2 |
| instructions of the final rule, median | 9 | 14 | 15 |
| delta-level rules with growth factor within 0.02 of 1 | 0 | 12 | 1 |
| final rules with T128 K8 ≥ 0.80 | 0 | 10 | 1 |

By the rule fixed before the run (p < 0.05 on the first or the second count), **both arms
show an effect**: with selection by behaviour no seed stops at linear attention, against 19
of 32 with the plain search. The effect is on the accuracy level. On the strict structural
count it is not shown (`h-share` p = 0.051, `h-lexicase` p = 0.78). Counting the aborted seed
of `h-share` as a failure gives p = 1.8e-7 and 0.066. The research agent had given `h-share`
a probability of 0.4 and `h-lexicase` 0.15; the second was a clear underestimate.

Checks and limits:
- **Not bought with more evaluations.** The arms run more real evaluations at the same
  candidate budget (fewer cache hits). But every `h-share` seed is at the level within 277,000
  real evaluations and every `h-lexicase` seed within 232,000; within those many real
  evaluations 11 and 10 of the 32 `h-base` seeds are, and `h-base` spends 457,000 on average.
- **Wall time is not matched.** The arms take 2.5 and 1.9 times as long per seed. The plain
  search with the same wall time (about 4M candidates) has not been run; package I does it.
- **What the rules are.** Most final rules of the two arms erase along the key (erase above
  0.3 in all but two) but are longer and carry nonlinear terms, so the structural test at
  R² ≥ 0.99 leaves 9 (`h-share`) and 18 (`h-lexicase`) unclassified. The result is "every seed
  gets past linear attention to delta-level accuracy", not "every seed rediscovers the delta
  rule". No rule is above tuned Gated DeltaNet (0.969) beyond noise.
- **Growth factors (rule 3).** The base task rewards a > 1, and most rules of all arms fail
  on 128-write episodes. `h-share` differs: 12 of its rules have a growth factor of 1 and 10
  hold on T128 K8 (≥ 0.80), against none in `h-base`. This was not a pre-set count.
- **Overfitting.** Train minus test is smaller in the two arms than in `h-base`.
- **One task.** The base task only. Task v3 and collision3 in the space of D and E are not
  run with these arms.
- JAX agrees with Rust for all rules (reports of the executing agent).

**A fault in the search code, found by this run.** With `--select share` or `lexicase` the
score cache was emptied at 1,000,000 entries after a batch had been evaluated but before its
programs looked up their scores, so a program that had been a cache hit in that batch was
missing and the run aborted (`h-share` seed 16, after 681 s). The same order existed for the
plain search at 3,000,000 entries, which no run has reached. Fixed on 15 Nov: the cache is
emptied at the start of a batch. Scores do not depend on the cache, so the fix changes the
count of real evaluations and nothing else; tested by forcing the limit down to 4,000 entries
in a scratch build, where all four modes (plain, `share`, `lexicase`, `--tune-consts`) ran to
the same log rows as with the normal limit. The 31 finished `h-share` seeds and all
`h-lexicase` seeds are valid as they are: a run either aborted or was unaffected.

Seed 16 was rerun with the fixed code on the review machine (`runs/h-share/seed16_local_rerun/`):
all 30 log rows of the aborted run are reproduced, and the run ends on a gated delta rule that
reached the accuracy level at 39,284 candidates (train 0.971, test 0.968). With it `h-share`
stands at 32/32 on the accuracy level and 20/32 on the structural count (one-sided Fisher
against `h-base`: p = 1.2e-8 and p = 0.040). The second value crosses 0.05 only with this seed
and is one of four tests, so the structural count stays "not shown". The rerun on the
university machine in package I is the one that enters `runs/h-share/seed16/`.

### Package I: the plain search at the wall time of the selection arms (released 15 Nov 2026, before any result)

`i-base4m`: base task, plain search, seeds 1 to 32, 4,000,000 candidates (about the wall time
of `h-share` at 1.5M), same machine. Also the rerun of `h-share` seed 16 with the fixed code.
Fixed before the run: the count is seeds at the accuracy level of delta β = 0.5 at 4M. If
`i-base4m` stays below 24/32, the selection arms beat the plain search at equal wall time by
the same test as in H (31/31 against 23/32 gives p < 0.01); at 28/32 or more the gain of the
arms is a saving of candidates, not something more budget cannot buy. Prediction of the
research agent: 13 to 20 of 32 with probability 0.65; 28 or more with probability 0.05.

## Package G: result and reading (16 Nov 2026)

Run by the executing agent on the university machine, commit ad31161, 12.0 h, predictions
committed before the run (f72bd0f). Facts per seed: `runs/g-tune8/g_report.md`. Counts
recomputed from the summaries; they agree with the report.

| collision3, space of D and E, 32 seeds, 1.5M candidates | `g-tune8` | `d-kalman` (plain search) | needed for an effect |
|---|---|---|---|
| rule 2 passed | 6/32 | 6/32 | 13/32 or more |
| stuck below 0.53 | 11/32 | 12/32 | 5/32 or fewer |
| test > 0.85 with rule 2's other conditions | 0/32 | 1/32 | 7/32 or more |
| above 0.695 with rule 2's other conditions | 3/32 | 2/32 | – |
| median test | 0.639 | 0.630 | – |

**No effect of constant tuning in the space where constants were measured to be critical.**
None of the three criteria fixed before the run is met; the distributions are the same
(Mann-Whitney p = 0.49). The best seeds reach 0.724 and 0.721 with rules that write along the
key; none has the shape of seed 9 of d-kalman. JAX agrees with Rust within 0.0005. The
research agent had predicted rule 2 in 5 to 10 seeds (it is 6) and had given a seed above
0.85 a probability of 0.45 (there is none).

The mean of train minus test is lower for `g-tune8` (−0.002 against +0.014), but the
baseline's value is carried by its seed 22, whose test suite is zeroed by the state guard;
without it the two are about equal. The first use of the validation log: 7 of 32 seeds reach
rule 2 on validation data, median at 450,000 candidates; the baseline was run before this
log existed.

Reading. Together with package F this closes the first component: tuning constants per
structure, as built (perturbed copies of every new structure), changes neither the rate nor
the tail, on a task where constants are uncritical and on one where they are critical. The
measurement that motivated it stands (the seed-9 structure is worthless with random
constants), so the likely reason is that a handful of perturbed copies around random
starting constants does not find a narrow band either; that reason was not tested. The
option stays in the code, off, as a negative result. The departure from the rule fixed before
F, taken on 15 Nov at the owner's decision, cost 12 hours and bought a clean negative.

## Package J: selection by behaviour in the space of packages D and E (released 16 Nov 2026, before any result)

Released by the owner on 16 Nov 2026. It asks whether the effect of package H carries over
from the base task to the benchmark: collision3, `--persist-m 3 --persist-init identity
--recip`, seeds 1 to 32, 1,500,000 candidates, batch 128, on the machine of D and E.

| tag | flags added to the setting of D and E |
|---|---|
| `j-lexicase` | `--select lexicase --val-log --level-acc 0.651 --level-long 0.838` |
| `j-share` | `--select share --val-log --level-acc 0.651 --level-long 0.838` |

`j-lexicase` runs first (it was cheaper in H and reached 32/32 there). Baseline: the 32 seeds
of `runs/d-kalman`. Commands: RUNBOOK.md, package J. A function test of both options in this
space (one seed, 30,000 candidates each) ran through; it is not a result.

Fixed before the run:
- Per arm, an effect is shown by rule 2 in 13/32 or more (baseline 6/32), by at most 5/32
  seeds stuck below 0.53 (baseline 12/32), or by test > 0.85 with rule 2's other conditions
  in 7/32 or more (baseline 1/32). These are the thresholds of package E. Three criteria and
  two arms are six looks; one criterion met narrowly in one arm is weak evidence.
- Also reported: seeds above 0.695; seeds above 0.90 (the level of Kalman delta is 0.93);
  rules with the shape of seed 9; train − test; candidates to rule 2 on validation data;
  real evaluations and minutes per seed. The comparison per real evaluation is made as in H.
  Wall time is not matched: the baseline at a larger budget does not exist in this space.
- A rule above 0.85 is checked on fresh task draws and with `--query-gap` before anything is
  said about it, as for seed 9.
- Prediction of the research agent for `j-lexicase`: at most 5/32 stuck with probability
  0.55; rule 2 in 13/32 or more with 0.40; at least one seed above 0.85 with 0.50; 7 or more
  above 0.85 with 0.08; a seed above 0.90 with 0.07. For `j-share` the same numbers minus
  0.05 each. On the base task the stuck seeds vanished entirely; here the step past decayed
  linear attention is the same step, the steps after it are not.

## Package I: result and reading (17 Nov 2026)

Run by the executing agent on the university machine, commit 50c2d10, 4.9 h, predictions
committed before the run (e7c41e0). Facts per seed: `runs/i-base4m/i_report.md`. Counts
recomputed from the summaries; they agree with the report.

| base task | `i-base4m`, plain, 4M | `h-base`, plain, 1.5M | `h-share`, 1.5M | `h-lexicase`, 1.5M |
|---|---|---|---|---|
| accuracy level of delta β = 0.5 | 24/32 | 12/32 | 32/32 | 32/32 |
| delta family by the structural test | 22/32 | 12/32 | 20/32 | 10/32 |
| ends at linear attention level (train < 0.84) | 7/32 | 19/32 | 0/32 | 0/32 |
| median test ow0.3 | 0.966 | 0.798 | 0.950 | 0.969 |
| minutes per seed | 17.6 | 4.9 | 12.2 | 9.1 |
| real evaluations per seed | 1,357,000 | 457,000 | 942,000 | 747,000 |
| wall time within which every seed of the arm reached the level | – | – | 215 s | 141 s |
| plain-search seeds at the level within that wall time | – | – | 13/32 | 10/32 |
| delta-level rules with growth factor within 0.02 of 1 | 2 | 0 | 12 | 1 |
| final rules with T128 K8 ≥ 0.80 | 2 | 0 | 10 | 1 |

The rule fixed before the run said "below 24/32: the arms beat the plain search at equal
wall time; 28/32 or more: their gain is a saving of candidates". The result is exactly 24,
which the rule does not decide: its two cases left 24 to 27 open. The test the rule names
still favours the arms (32/32 against 24/32, one-sided Fisher p = 0.0024), and the plain
search was given more wall time than either arm, not equal (17.6 minutes per seed against
12.2 and 9.1). Within the wall time in which every seed of `h-share` had reached the level,
13 of 32 plain-search seeds had; for `h-lexicase` it is 10 of 32 (seconds read from the log
rows, every 50,000 candidates; same machine). The research agent's prediction (13 to 20 of
32 with probability 0.65) was wrong; the plain search improves more with budget than
expected.

**Accuracy level and structure part ways.** On the structural count the plain search with
more budget is level with `h-share` (22 against 20) and well ahead of `h-lexicase` (22 against
10; one-sided Fisher p = 0.003, a test chosen after seeing the data). `h-lexicase` reaches
delta-level accuracy faster than any other arm, but mostly with longer rules that erase along
the key and carry nonlinear terms the structural test does not accept. `h-share` reaches the
level in every seed and keeps the structural rate of the plain search at 2.7 times its budget;
it is also the only arm that finds many rules with growth factor 1 that hold on long episodes.

Other checks: up to 1.5M candidates `i-base4m` reaches the level in exactly the same 12 seeds
as `h-base` (the cache fix did not change the search). The rerun of `h-share` seed 16 on the
university machine is identical, row for row and in its final rule, to the research agent's
rerun on the review machine and to the 30 rows of the aborted run; `h-share` now has 32 seeds
of record (32/32 on the level, 20/32 structural).

Reading for the method claim, on the base task only:
- Selection by behaviour gets every seed to delta-level accuracy, in less wall time and fewer
  real evaluations than the plain search needs for three quarters of its seeds. That holds
  for both variants and survives the wall-time control.
- On rediscovering the delta rule itself, `share` matches the plain search at a fraction of
  the budget and `lexicase` is worse. If one variant is carried forward as "the method",
  the evidence points to `share`; `lexicase` buys speed to an accuracy level with less
  interpretable rules.
- Whether any of this carries over to a task where the plain search fails is the question of
  package J.

### Addition to package J, 17 Nov 2026, before any J result

Package I shows that the plain search gains a lot from a larger budget. If an arm of J shows an
effect, the comparison against `runs/d-kalman` is at equal candidates but not at equal wall
time, and the claim is held back until a plain-search arm in the same space with the arm's
wall time has been run. This adds a condition to the reading of J; the criteria of J are
unchanged.

## Literature check of the method components (17 Nov 2026)

Asked by the owner after package I. Question: is selection by behaviour (`--select share`,
`--select lexicase`) new, and how new is evolving a memory update rule from scratch? Sources
were read in full where an arXiv copy exists (marked "read"); others only from abstracts,
bibliographies or reference lists (marked "secondary"). Not exhaustive.

### Selection by behaviour: not new

- **Fitness sharing** goes back to Goldberg and Richardson (1987); NEAT (Stanley and
  Miikkulainen 2002) uses it inside species. Secondary.
- **Fitness sharing in genetic programming**, including behaviour (phenotype) based variants:
  McKay (2000, 2001) applied implicit fitness sharing to program populations and reports the
  results of raw fitness with populations two to three times smaller, attributed to preserved
  diversity. A GECCO 2002 study contrasts behaviour-based with tree-distance-based sharing in
  GP. Secondary (abstracts in the GP bibliography).
- **Semantic and behavioural methods in GP** are an established line (survey: Vanneschi,
  Castelli and Silva 2014; behavioural programming: Krawiec and O'Reilly 2014); novelty search
  (Lehman and Stanley 2011) and MAP-Elites (Mouret and Clune 2015) select on behaviour
  descriptors. Secondary.
- **Behaviour-based niching in GP is still being published**: Liu, Mei and Zhang (2026,
  arXiv 2609.24104) niche GP individuals by behaviour descriptors of the search they induce;
  the effect on solution quality is small, the effect on program size is clear. Read.
- **Lexicase selection** (Spector 2012; Helmuth, Spector and Matheson 2014, IEEE TEVC) selects
  on individual training cases and is known to keep diversity (Helmuth, McPhee and Spector
  2016). Secondary. **Geiger, Briesch, Sobania and Rothlauf (2025, arXiv 2502.18093)** show for
  symbolic regression that tournament selection with random or informed down-sampling of the
  training cases matches ε-lexicase in error and diversity and is faster. Read. This is the
  control a reviewer will ask for (see below).

### Evolving learning or memory update rules from scratch: not new either

- **Chalmers (1990)**, "The evolution of learning: an experiment in genetic connectionism",
  evolved learning rules for single-layer networks with a genetic algorithm, starting from a
  population that could not learn; the delta rule (or a rule very close to it) emerged. The
  rule space was a fixed parametric form over local quantities, not a program space.
  Secondary (abstract, and reference [6] of Baxter 1992).
- **Baxter (1992)**, read (arXiv 2512.01203): a GA over network architecture and a local binary
  rule; Hebb's rule evolved in all five runs.
- **Bengio, Bengio and Cloutier (1994, 1995)** used genetic programming to search the form of a
  synaptic learning rule. Secondary. Radi and Poli (2003) evolved less constrained rules with
  GP that resemble backpropagation; known only from a citation, not checked.
- **AutoML-Zero (Real, Liang, So and Le 2020)**, read: regularized evolution from empty
  programs over basic linear-algebra ops finds gradient descent and two-layer networks. The
  search upgrades that helped were migration between workers, functional-equivalence caching,
  dataset diversity (half the workers on another dataset) and hurdles; crossover and
  geographic structure did not. No fitness sharing, niching or lexicase. This project's search
  is that method, scaled down.
- Recent symbolic discovery of learning rules without evolution: Perin, Anselmi and Deny (2026,
  arXiv 2611.12248) regress local losses on a dictionary of monomials. Read. Jordan et al.
  (2021) evolve plasticity rules with Cartesian GP. Secondary.
- No paper was found that searches update rules of matrix-valued fast-weight or linear-attention
  memories with program evolution from an empty program, or that applies behaviour-based
  selection inside an AutoML-Zero-style search. The search for both was two queries in a paper
  index and one web query each; that is weak evidence of absence.

### What this means for the paper

1. **The method claim cannot be "a new search algorithm".** Fitness sharing, lexicase and
   behavioural niching are decades old. What the data of this project can support is an
   empirical finding: in an AutoML-Zero-style search for memory update rules, the component
   that decides whether seeds escape linear attention is parent selection by behaviour, while
   a NEAT-style add-node mutation and constant tuning do nothing measurable. That is a
   component study. Its value rises with the number of tasks and testbeds it holds on.
2. **"Rediscovery of the delta rule by evolution" is 36 years old** (Chalmers 1990). It stays a
   sanity check of the search; it is not a result. What is less covered: a program space with
   matrix state from an empty program, the structural test, and the 2026 rule families (Kalman
   delta, preconditioning) as held-out targets.
3. **A control is missing.** Geiger et al. (2025) found that most of lexicase's advantage
   comes back with down-sampled training cases under plain tournaments. The obvious control
   here: the plain search with a random subset of the train episodes per batch. If it closes
   most of the gap of package H, the finding becomes "any source of selection noise or
   diversity", not "behaviour-based selection". Not implemented; to be decided with the owner.
4. Related-work section to write, at least: Goldberg and Richardson 1987; Stanley and
   Miikkulainen 2002; McKay 2000/2001; Vanneschi et al. 2014; Lehman and Stanley 2011; Mouret
   and Clune 2015; Spector 2012; Helmuth et al. 2014, 2016; Geiger et al. 2025; Chalmers 1990;
   Baxter 1992; Bengio et al. 1994; Real et al. 2020; plus the memory-rule literature listed in
   CLAUDE.md. The secondary items must be read before they are cited.

## Direction 2: a search that reaches a known strong rule (17 Nov 2026)

Decided by the owner on 17 Nov 2026 after the literature check: the project aims at a new
capability rather than a new component. Target: a search that finds the Kalman delta rule, or
a rule at its level, from the empty program in the space of packages D and E, where the
present search never does (0 of 64 seeds above 0.90 in `d-kalman` and `g-tune8`; Kalman delta
written by hand reaches 0.933). Known components are acceptable if the capability is new.

### Why the present search does not get there (`python verify/probe_path_kalman.py`)

Hand-written programs between the delta rule and Kalman delta, each adding one piece, best
constants on a small grid, train accuracy as the search sees it (collision3, task seed 1):

| step from the delta rule | added instructions | train | test | T128 K8 |
|---|---|---|---|---|
| A delta rule | – | 0.617 | 0.640 | 0.828 |
| write key `P k` with P = I, P never updated | 1 | same as A | | |
| B normalised gain `g = Pk/(δ + kᵀPk)`, P fixed | +5 | 0.618 | 0.635 | 0.845 |
| D' unnormalised `P' = P − c·(Pk)(Pk)ᵀ`, best c = 0.1 | +4 to A | 0.646 | 0.668 | 0.765 |
| D B + `P' = P − c·g(Pk)ᵀ`, c = 0.05 / 0.2 / 0.5 / 1.0 | +4 to B | 0.658 / 0.782 / 0.826 / 0.624 | | |
| E D + `q·I`, c = 0.2 / 0.5 / 1.0 | +3 to D | 0.718 / 0.813 / 0.932 | | 0.950 at c = 1 |

Reading:
- There is a path along which fitness rises almost monotonically: delta → key `Pk` (neutral)
  → normalised gain (neutral) → partial update of P with a small factor c (rising to 0.826
  at c = 0.5) → add `q·I` (about neutral at c = 0.5) → raise c to 1 (0.932). No deep valley.
- But every step needs three to five specific instructions in place before it changes
  anything: the update of P is four (`Outer`, `Const`, `MatScale`, `MatSub`), the normalised
  gain five, the `q·I` term three. Until the last of them is inserted the others are dead code,
  invisible to selection. With 20 ops and 4 to 6 registers per type, a specific instruction
  is drawn about once in a few thousand insertions, so a specific four-instruction step is far
  out of reach of 1.5M candidates. This is the barrier, measured, not assumed.
- Seed 9 of `d-kalman` found a shorter route to a projector state (three to four
  instructions), which is why it, and nothing better, appeared.

### Search method, third change: residual branch insertion (logged before any result)

`--residual-insert`, off by default. With probability 1/6 per mutation, four instructions are
inserted at a random position:

    t = op(a, b)        random op producing the type of r, random inputs
    s = Const(ε)        ε = ±10^U(−3, −1)
    t = s · t
    r = r + t           r a random register of that type (matrix, vector or scalar)

The branch is live at once but nearly neutral, and its weight can grow by constant mutation.
A step that pays off only once complete is then reachable through a slope: for the update of
P, a single residual insertion with `op = Outer`, both inputs the register holding `Pk` and a
negative ε is the step D' at small c. Nothing in the mutation names a rule, an op or a
register; it is the zero-initialised residual branch of deep learning, or NEAT's new
connection with a small weight, applied to typed programs. When off, no random number is
drawn for it and committed runs reproduce (v2 seed 3 to 100,000 candidates, d-kalman seed 9
to 50,000).

Known risk, stated now: the mutation was chosen after measuring the path to one target. A
success on that target alone would be open to the charge that the method was fitted to it.
Any claim therefore needs a held-out target the method was not designed on (testbed 2,
item 5 of CLAUDE.md, or another known rule in another regime), with the method frozen first.

Status: implemented and smoke-tested. A pilot on this agent's container (collision3, space of
D and E, 300,000 candidates, seeds 1 to 4, `--residual-insert` with `--select fitness` and with
`--select share`) was stopped at the container's time limit with 7 of 8 seeds done; collision3
test 0.632 / 0.508 / 0.516 / 0.666 and 0.661 / 0.660 / 0.638; the committed seeds 1 to 4 of
`d-kalman` had train 0.517 / 0.669 / 0.510 / 0.624 at 300,000 candidates. Too small to read;
it is not a result. A package on the
university machine follows after package J.

## Package J, arm j-lexicase: result and reading (18 Nov 2026)

Run: `runs/j-lexicase`, commit 50c2d10, seeds 1 to 32, 1,500,000 candidates, epyc, 16.1 h of
wall time. The executing agent's report is `runs/j-lexicase/j_report.md`. The baseline is
`runs/d-kalman`. On collision3 test: ridge ceiling 1.000, Kalman delta written in the space
0.933, tuned DeltaNet 0.640, tuned Gated DeltaNet 0.644.

### Outcome against what was fixed before the run

| | j-lexicase | d-kalman | fixed threshold | met |
|---|---|---|---|---|
| rule 2 | 12/32, **11/32 without seed 6** | 6/32 | ≥ 13/32 | no (p = 0.13 for 11 vs 6) |
| stuck below 0.53 | **0/32** | 12/32 | ≤ 5/32 | yes, Fisher one-sided p = 6.9e-5 |
| test > 0.85 with rule 2's other conditions | 1/32 (seed 6), **0/32 without** | 1/32 | ≥ 7/32 | no |
| above 0.695 under those conditions | 5/32, 4/32 without seed 6 | 2/32 | reported | |
| above 0.90 | 0/32 | 0/32 | reported | |
| median test | 0.682 | 0.630 | reported | Mann-Whitney p = 6.6e-6 |
| mean train − test | +0.000 | +0.014 | | |
| mean real evaluations per seed | 806,780 | 784,926 | | |
| mean minutes per seed | 59.5 | 42.2 | | |

Seed 6 is excluded under CLAUDE.md rule 3 (below). JAX against Rust on the dump: largest
difference 0.0006. Validation level reached in 20/32 seeds (`d-kalman` has no validation log).
The prediction (stuck ≤ 5 with 0.55, rule 2 ≥ 13 with 0.40, a seed above 0.85 with 0.50, a seed
above 0.90 with 0.07) came out as the likeliest case: only the stuck count moved.

### Seed 6: a strong rule written through the epsilon of Normalize

The executing agent read off that seed 6's write cancels in exact arithmetic,
S' = 1.011·(S + v rᵀ)(I − û ûᵀ) with r = k + P1·tanh(k) and û = r/|r|, so S stays zero, and
it took the accuracy (Rust 0.893) for float32 rounding residue. That mechanism is not right.
`verify/verify.py` now has a float64 mode (`--x64`) and a settable epsilon for Normalize
(`--norm-eps`, default 1e-6 as in `src/program.rs`); `verify/eps_scale.py` measures whether the
size of S follows that epsilon. JAX on the collision3 test dump (`runs/eps-check/`):

| program | float32, ε 1e-6 | float64, ε 1e-6 | float64, ε 1e-3 | float64, ε 1e-9 | max\|S\| at ε 1e-3 / at ε 1e-6 |
|---|---|---|---|---|---|
| j-lexicase seed 6 | 0.893 | 0.896 | 0.897 | **0.000** | **1000** |
| j-lexicase seed 7 | 0.711 | 0.714 | 0.713 | 0.502 | 0.99 |
| d-kalman seed 9 | 0.855 | 0.858 | 0.846 | 0.834 | 0.94 |
| j-lexicase seed 2 | 0.721 | 0.721 | | 0.721 | 1.00 |

Float64 keeps the accuracy, so it is not rounding. The write is the leak of the epsilon:
Normalize is x/(|x| + 1e-6), û is slightly shorter than a unit vector, and v rᵀ(I − û ûᵀ)
leaves about 1e-6·(1 + |r|)·v ûᵀ. To first order in ε the program is
S' = 1.011·[S(I − û ûᵀ) + ε(1 + |r|)·v ûᵀ]: a delta rule with step 1 on the key û, every write
scaled by ε. S starts at zero and the rule is linear in S and in the write, so S is ε times the
state of the same rule written at scale 1. Argmax decoding ignores that factor, and the readout
clears the 1e-6 norm threshold of `src/task.rs` only because of the factors 1.011 per step and
1 + |r|. At ε = 1e-9 every readout falls below the threshold. The program as found is a scale
trick under rule 3 and is not counted.

What the rule computes once the epsilon is taken out (reference probe only, rule 6;
`verify/probe_j6.py`, Rust `eval` in `runs/eps-check/j6_rust_eval.txt`):

| program | train | collision3 test | T64 K8 | T128 K8 |
|---|---|---|---|---|
| found (writes through ε) | 0.909 | 0.893 | 0.997 | 0.995 |
| b: S' = 1.011·[S(I − û ûᵀ) + (1 + \|r\|)·v ûᵀ] | 0.907 | 0.898 | 1.000 | 0.999 |
| a: S' = 1.011·[S(I − û ûᵀ) + v ûᵀ] | 0.874 | 0.881 | 1.000 | 0.999 |

with P' = 0.9935·P − 0.366·r rᵀ and P = I at the start, the constants as evolved. This is the
delta rule with step 1 on a key decorrelated by a second state that subtracts a decayed sum of
r rᵀ from the identity: a first-order estimate of the inverse key covariance. At 0.898 it lies
between `d-kalman` seed 9 (0.855) and Kalman delta (0.933). Neighbours: Preconditioned DeltaNet
(Tumma, Loo and Rus, ICML 2026, arXiv 2604.21100; the delta rule with the curvature of the
least-squares loss as preconditioner), OSDN (May 2026; a diagonal preconditioner on the write
key), decorrelation by anti-Hebbian learning (Földiák 1990) and Kohonen's novelty filter. The
rewrite is hand-written and no claim rests on it. What it shows is that lexicase reached the
region of strong rules once in 32 seeds, by a route that a scale check excludes.

### The same check on every arm in this space

All 96 best rules of `d-kalman`, `g-tune8` and `j-lexicase`, float32 at ε 1e-6 against float64
at ε 1e-9: 92 do not move (difference ≤ 0.0005). Four move: j-lexicase 6 (the scale trick),
j-lexicase 7 (0.711 to 0.502), `d-kalman` 9 (0.855 to 0.834) and `d-kalman` 20 (0.513 to 0.510).
In seeds 7 and 9 the epsilon is a numerical floor for normalising vectors that can come close to
zero, and S does not scale with it (ratio 0.99 and 0.94). Seed 7 is in no count (T128 K8 0.713).
Seed 9 stays above 0.695 and its count stands. Its 0.855 does depend a little on the constant,
and in float32 at ε 1e-9 it falls to 0.742.

From now on this is a verification step for every arm in this space, applied to all compared arms
alike: `verify.py --x64 --norm-eps 1e-9` on the dump, then `verify/eps_scale.py` for every seed
that moves by more than 0.02. A ratio near 1000 is a scale trick and the seed is not counted. The
fitness is unchanged, so the arms stay comparable. Closing the channel in the fitness itself
(counting a query only if |o| > 1e-3, as values have unit norm) would change the fitness and
make new arms incomparable with `d-kalman`, `g-tune8` and J. That is left to the owner.

### Reading

- In this space too, lexicase removes the seeds that stop at decayed linear attention: 0/32
  against 12/32 (p = 6.9e-5), at equal real evaluations and 1.4 times the wall time. This
  carries package H to a second task. It is one of three criteria, the one predicted most likely.
- It does not raise the top. Rule 2 is reached in 11/32, there is no counted seed above 0.85 and
  none above 0.90. The median moves because the bottom moves.
- The condition of 17 Nov applies: the stuck count is not claimed for this space until a plain
  arm at j-lexicase's wall time (about 2.1M candidates) has run. In package I, more wall time
  for the plain search removed part of the stuck seeds, not all of them (24/32 against 32/32).
- For Direction 2 the arm adds one hint: a rule at about 0.90 exists in this space at 24
  instructions, and the search assembled it once, in a form that writes through the epsilon.

## Package J, arm j-share, and package J as a whole: result and reading (19 Nov 2026)

Run: `runs/j-share`, commit 50c2d10, seeds 1 to 32, 1,500,000 candidates, epyc, 13.4 h, no seed
aborted. The executing agent's report is `runs/j-share/j_report.md`. The epsilon check of 18 Nov
was run by the research agent on the same dump (identical to the executing agent's, byte for
byte): no seed moves (`runs/eps-check/j-share.*.txt`).

| | j-share | j-lexicase (seed 6 excluded) | d-kalman | fixed threshold |
|---|---|---|---|---|
| stuck below 0.53 | **0/32** | **0/32** | 12/32 | ≤ 5/32: met by both, p = 6.9e-5 each |
| rule 2 | 11/32 | 11/32 | 6/32 | ≥ 13/32: met by neither |
| test > 0.85 with rule 2's other conditions | 0/32 | 0/32 | 1/32 | ≥ 7/32: met by neither |
| above 0.695 under those conditions | 0/32 | 4/32 | 2/32 | reported |
| above 0.90 | 0/32 | 0/32 | 0/32 | reported |
| test range | 0.617 to 0.694 | 0.564 to 0.721 | | |
| median test | 0.653 | 0.682 | 0.630 | MW: share vs d-kalman p = 0.0021, share vs lexicase p = 0.0007 (share lower) |
| final rule classified as delta rule | 5/32 (four at exactly 0.640, the tuned DeltaNet level) | 0/32 | | |
| mean real evaluations per seed | 962,443 | 806,780 | 784,926 | |
| mean minutes per seed | 49.4 | 59.5 | 42.2 | |
| mean pop_mean_acc of the last row | 0.349 | 0.446 | 0.418 | |

Reading of package J:
- Selection by behaviour removes the seeds that stop at decayed linear attention in this space,
  with both variants (0/64 against 12/32). With package H this is the same effect on a second
  task. Not yet at matched wall time: the selection arms take 1.17 (share) and 1.41 (lexicase)
  times as long per seed. In the plain arms the number of seeds with train accuracy below 0.53
  falls from 19 to 13 to 11 (`d-kalman`) and 20 to 14 to 11 (`g-tune8`) at 0.5M, 1.0M and 1.5M
  candidates, so more budget helps the plain search and the control is needed (package K).
- Neither variant raises the top. Rule 2 stays at 11/32, nothing counted is above 0.85 and
  nothing is above 0.90. 0 of 128 seeds in this space are above 0.90 now (`d-kalman`, `g-tune8`,
  `j-lexicase`, `j-share`).
- The two variants differ above the floor. Share keeps a diverse, weaker population (mean
  population accuracy 0.35) and parks five seeds on the plain delta rule; its best seed is 0.694.
  Lexicase reaches the 0.70 to 0.72 band in 5 seeds and gave the one strong (if degenerate) rule.
  On the base task (package I) share was the better variant on the structural count. Which is
  better depends on the task and the measure; neither is a general improvement.
- Predictions: the stuck criterion, the likeliest case in both arms, came out; nothing else did.

## Package K: residual insertion on collision3, and the wall-time control of J (released 19 Nov 2026, before any result)

Two arms, collision3, the space of D and E (`--persist-m 3 --persist-init identity --recip`),
seeds 1 to 32, batch 128, built at the commit that releases this package (it contains
`--residual-insert`, README "Search method, third change"). With the flag off the new binary
reproduces the committed runs: `d-kalman` seed 9 gives the same 50,036-candidate log row with and
without `--val-log` and with 4 or 8 threads.

| tag | flags added to the setting of D and E | budget | baseline | machine |
|---|---|---|---|---|
| `k-ri-lex` | `--select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838` | 1.5M | `j-lexicase` (only the new mutation differs) | epyc |
| `k-plain2m` | `--val-log --level-acc 0.651 --level-long 0.838` | 2.1M | `d-kalman`; wall-time control for both arms of J | workstation |

Lexicase rather than share is chosen for the residual arm because in this space it reached the
higher band and share did not (J above); the choice is made on J's data, so the comparison that
isolates the mutation is `k-ri-lex` against `j-lexicase`, same selection, seeds and budget.
2.1M candidates is 1.5M times the larger wall-time factor of J (1.41).

Fixed before the run:
- `k-ri-lex`, main count (Direction 2): seeds with collision3 test > 0.90 that meet rule 2's
  other conditions (T128 K8 ≥ 0.838, train − test ≤ 0.03) and pass the epsilon check. An effect
  is shown by 2/32 or more against 0/128 in this space (Fisher one-sided p = 0.039). One seed is
  reported as one seed. Secondary: test > 0.85 under the same conditions in 3/32 or more against
  1/128 (p = 0.026). Also reported against `j-lexicase`: rule 2, stuck, above 0.695, median with
  Mann-Whitney, real evaluations and minutes per seed.
- Any rule above 0.85 is checked on fresh task draws and with `--query-gap` before anything is
  said about it, as for `d-kalman` seed 9, and its formula is compared with Kalman delta.
- `k-plain2m`: the stuck effect of J stands at matched wall time if `k-plain2m` has 5/32 or more
  seeds below 0.53 on test (0/32 against 5/32: p = 0.027). With 4 or fewer the effect of J is
  a budget effect in this space. Its other counts are reported as for J.
- The fitness is unchanged (the epsilon channel of 18 Nov stays open; the epsilon check is
  applied to every arm alike).
- A success of `k-ri-lex` on the main count is not a claim on its own: the mutation was designed
  after measuring the path to this target. It must be followed by a held-out target with the
  method frozen first. The held-out target is testbed 2 (CLAUDE.md, item 5: reaching the level of
  RMSProp or Adam from `w' = w`), where the same kind of multi-instruction step is needed and the
  mutation was not designed. Its path is not measured before the method is frozen.
- Predictions of the research agent. `k-ri-lex`: main count met (2 or more above 0.90) with
  probability 0.12, at least one seed above 0.90 with 0.22, secondary count met with 0.20, median
  below that of `j-lexicase` with 0.35, stuck at most 5/32 with 0.85. `k-plain2m`: 5 or more stuck
  with 0.80, above 0.90 with 0.03. The pilot of 18 Nov gave no sign either way.

## Outside review of 19 Nov 2026, residual insertion corrected, down-sampling control (before any result of package K)

The owner had the project reviewed by a second model on 19 Nov. Each point was checked against
the code; what was confirmed is fixed or recorded here, before any run of package K.

### Residual insertion overwrote live registers (confirmed, fixed)

The block `t = op(a, b); s = Const(ε); t = s·t; r = r + t` drew its temporaries t and s among
all registers of their type. In the space of D and E three of the four matrix registers are S
or persistent, and V0, V1 hold k and v, so t or s often overwrote a value the rule still
needed. The block was not near-neutral, as README ("Search method, third change") claimed.
Since this commit t and s are drawn only among registers whose value is not needed at the
insertion point (backward liveness, persistent registers counted as needed when the next step
reads them); if there is none, no block is inserted. `MAX_LEN` = 24 counts dead code too, and
programs in the population sit at that limit: in a function test (seed 1, 60,000 candidates,
`--select lexicase --residual-insert`) 86% of attempts met a program at the limit. The first
version would have failed there. Now just enough dead instructions, chosen at random, are
removed first (no change in behaviour); 86% of attempts then insert a block. `MAX_LEN` is
unchanged. The summary counts attempts, inserted blocks and removals. With the flag off nothing
changed (`d-kalman` seed 9 gives the same 50,036-candidate row and the self-check of package F
the same 120,052-candidate row, after every change of this section).

A side observation: since an ordinary insertion at the limit turns into a deletion, every
search here runs with programs full of dead code at 24 instructions. Rules that need more than
about 20 live instructions are hard to reach for any arm; Kalman delta needs 15.

Measured with the new diagnostic `autoplast mutstat` (250 insertions into each of the 32 best
rules of `j-lexicase` and of `d-kalman`, collision3 train task; `runs/ri-diag/`):

| | version of 17 Nov, j-lexicase | corrected, j-lexicase | 17 Nov, d-kalman | corrected, d-kalman |
|---|---|---|---|---|
| rules that can take a block (length ≤ 20) | 28/32 | 28/32 | 27/32 | 27/32 |
| insertion drops train accuracy by more than 0.05 | **37%** | **1.9%** | **29%** | **1.0%** |
| block live (the effective program grows) | 48% | 33% | 48% | 32% |
| live block within ±0.005 of the parent's accuracy | 28% | 80% | 37% | 82% |
| insertion raises train accuracy | 0.1% | 0.5% | 0.1% | 0.1% |
| live block with fitness ≥ parent | 1% | 2% | 0% | 0% |

The pilot of 18 Nov ran the faulty version; it says nothing about the mutation.

### Length penalty against near-neutral blocks (confirmed, left as is)

A live block costs 4 · 1e-4 of fitness, so a block that leaves accuracy unchanged is almost
never as fit as its parent (last row above). Along the measured path the penalty is smaller
than the signal once the block has some weight: a P update with weight c = 0.002 raises train
accuracy by 0.001 to 0.002, c = 0.01 by 0.008, c = 0.05 by 0.04 (delta rule with normalised
gain, `verify/probe_path_kalman.py` programs, β = 1, δ = 0.01 and 0.03). Under lexicase the
penalty only breaks ties between rules with the same per-episode counts. Changing it would
change the fitness of every arm and the comparison with `j-lexicase`; it stays, and is a
candidate explanation if `k-ri-lex` shows nothing.

### Points checked and not taken over

- "Individuals live only 3.9 batches." With 500 individuals and 128 children per batch an
  individual is replaced after 500 children, as in regularized evolution with one child per
  step, and it enters about as many tournaments (about 10). Not a defect; population size is
  an untested hyperparameter.
- "A smooth training loss (MSE) would give slopes." On the measured path accuracy already
  rises at small weights (above); the barrier is that a partial step is dead code. A loss
  change would also change the fitness of all 160 seeds in this space. Not adopted now. It
  would close the epsilon channel of 18 Nov by construction; recorded as an option.
- "The additive block cannot build the normalised gain `P k / (δ + kᵀP k)`." Correct as a
  limit: the block offers the P update (step D') in one insertion, not the normalisation. Stated
  as a limit of the mutation, not a defect.

### Points that stand as limits of results already reported

- `--select lexicase` is lexicase inside a tournament of 10, with at most 32 episodes, as
  specified on 15 Nov. It is not lexicase over the whole population; a rule that is best on
  few episodes rarely enters the pool. Every lexicase result here (H, J) is for this variant.
- Constant tuning (F, G) is closed for the version tested: 8 random joint perturbations once
  per new structure. A stronger local optimiser of the constants was not tested.
- Scope: the reviewer reads the method claim as too thin for a main-track paper unless the
  search reaches Kalman delta and transfers to testbed 2; that is the reading of 17 Nov
  ("Literature check of the method components"). The venue is the owner's decision.

### The down-sampling control (built; package L)

`--select downsample` (off by default): once per batch a random subset of `--ds-rate` (default
0.1, not tuned) of the train episodes is drawn, and the parent is the candidate of the
tournament with the most correct queries on that subset, ties broken by fitness as in
lexicase. Every rule is still scored on all episodes; only selection uses the subset. This is
the rival Geiger et al. (2025) set against lexicase: selection on random subsets of cases also
keeps a population diverse. If it removes the stuck seeds as well as lexicase does, the effect
of H and J belongs to selection on random episode subsets, not to lexicase or sharing as such.

Package L, base task as in H, seeds 1 to 32, 1.5M candidates, `--select downsample --val-log`,
baseline `h-base`, `h-lexicase`, `h-share`. Fixed before the run: down-sampling alone gives an
effect if it reaches the accuracy level of delta β = 0.5 in 20/32 or more (against 12/32 of
`h-base`, p = 0.040); lexicase does more than down-sampling if `l-downsample` reaches it in
27/32 or fewer (against 32/32, p = 0.026). Both can hold. Prediction of the research agent:
20 or more with probability 0.6, 27 or fewer with probability 0.5.

### Package K after the correction

`k-ri-lex` runs with the corrected mutation, at the commit of this section; thresholds and
predictions of package K are unchanged. `k-plain2m` is not affected (flag off). If `k-ri-lex`
shows nothing, two explanations are open before the mutation is given up: the length penalty
above, and the length limit (4 of 32 final rules of `j-lexicase` are too long for a block).

## Package L: result and reading (19 Nov 2026)

Run: `runs/l-downsample`, commit 6c2f60a, workstation (Windows), seeds 1 to 32, 1.5M candidates,
base task, `--select downsample --val-log` (rate 0.1), 1.9 h. The executing agent's report is
`runs/l-downsample/l_report.md`. Counts recomputed from the summaries.

| base task, 1.5M candidates | `h-base` | `l-downsample` | `h-share` | `h-lexicase` |
|---|---|---|---|---|
| accuracy level of delta β = 0.5 reached | 12/32 | **19/32** | 32/32 | 32/32 |
| ends at linear attention level (train < 0.84) | 19/32 | 13/32 | 0/32 | 0/32 |
| delta family by the structural test | 12/32 | 13/32 | 20/32 | 10/32 |
| median test ow0.3 | 0.799 | 0.953 | 0.950 | 0.969 |
| delta-family rules with growth factor within 0.02 of 1 | 0 of 12 | 1 of 13 | 4 of 20 | 0 of 10 |
| final rules with T128 K8 ≥ 0.80 | 0 | 2 | 10 | 1 |

Against what was fixed before the run:
- Down-sampling alone gives an effect at 20/32 or more. It reached 19/32 (p = 0.066 against
  `h-base`): not shown, by one seed.
- Lexicase does more than down-sampling at 27/32 or fewer for `l-downsample`. Met: 19/32
  against 32/32 for both behaviour-based arms (p = 2.6e-5).

Reading:
- Selection on a random tenth of the episodes per batch frees some seeds from linear attention
  (19 against 12, not significant). It is far from what lexicase and fitness sharing do (32/32).
  The effect of package H is therefore not explained by selection on random subsets of
  episodes. It goes with selection that looks at the per-episode behaviour of each candidate.
  This is the reviewer's first question, answered on the base task. It is not answered on
  collision3 (not run there).
- Limits: one rate (0.1, not tuned), and the rival is our variant of lexicase (inside a
  tournament of 10, at most 32 episodes). Platform differs from H (workstation against epyc;
  rule 7), which does not bias rates. Minutes are not comparable across machines.
- The structural count does not move (13/32). Most delta-family rules of the arm grow by 1.09
  to 1.12 per step and fail on long episodes, as in `h-base` (rule 3). `h-share` stays the only
  arm with many rules at growth factor 1.
- Predictions of the research agent: 20 or more with 0.6 (no), 27 or fewer with 0.5 (yes).

### Package K, status 19 Nov

`k-ri-lex` stopped on epyc when the hub server there was restarted. The runner skips seeds with a
summary. A seed that was running restarts from the beginning. Seeds are deterministic for a given
binary, flags and machine, so a restarted seed gives the result it would have given anyway and
the restart does not bias the arm. Resumed with the same command (RUNBOOK, package K).

### Package K, arm k-ri-lex: result and reading (20 Nov 2026)

Run: `runs/k-ri-lex`, commit 6c2f60a, epyc, seeds 1 to 32, 1.5M candidates, collision3 in the space
of D and E, `--select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838`,
`--parallel 2 --threads 8`, 17.6 h for the arm. The executing agent's report is
`runs/k-ri-lex/k_report.md`, the run record `WHERE.md` (two starts killed by the hub after ten
minutes, kept in `aborted1/` and `aborted2/`; their log rows equal those of the complete run).
Counts recomputed from the summaries; they agree with the report.

| collision3, space of D and E | `d-kalman` | `j-share` | `j-lexicase` | `k-ri-lex` |
|---|---|---|---|---|
| rule 2 | 6/32 | 11/32 | 12/32 | 11/32 |
| stuck (test < 0.53) | 12/32 | 0/32 | 0/32 | 0/32 |
| above 0.695 under rule 2's other conditions | 2/32 | 0/32 | 5/32 | 7/32 |
| above 0.85 under the conditions | 1/32 | 0/32 | 1/32 (seed 6, scale trick, not counted) | **0/32** |
| above 0.90 under the conditions | 0/32 | 0/32 | 0/32 | **0/32** |
| median test | 0.630 | 0.653 | 0.682 | 0.677 |
| best test | 0.855 | 0.694 | 0.893 (trick) / 0.721 | 0.726 |
| real evaluations per seed, mean | 785k | | 807k | 939k |
| minutes per seed, mean | 42 | | 60 | 64 |

Against what was fixed before the run:
- Main count (2/32 or more above 0.90 under the conditions, ε check passed): **not met**, 0/32.
- Secondary count (3/32 or more above 0.85): not met, 0/32.
- Against `j-lexicase`: median 0.677 against 0.682, Mann-Whitney p = 0.75; rule 2 11 against 12;
  above 0.695 7 against 5 (Fisher p = 0.75). No difference.
- Checks: JAX on the dump within 0.0005 of Rust for all 32 seeds; the ε check (`--x64 --norm-eps
  1e-9`) moves no seed (on `j-lexicase` seed 6 the same command gives 0.0000, so it detects the
  known case).
- Predictions of the research agent: main count (0.12) no, a seed above 0.90 (0.22) no, secondary
  (0.20) no, median below `j-lexicase` (0.35) yes, stuck at most 5 (0.85) yes.

Reading:
- The mutation is active: 73% of the insertion attempts insert a block (31% to 84% per seed), about
  357k attempts per seed. It does not move the arm. The seven seeds above 0.695 sit at 0.72 to
  0.73; their rules (formulas in the report, collected forms checked numerically) are delta-type
  writes with a large erase (c/a 0.85 to 0.90) in which a persistent register is used as an
  offset or copy of S, not as a key preconditioner. No best rule contains a reciprocal, so none
  has a gain of the form P k / (c + kᵀP k).
- Of the two explanations noted before the run (length penalty, length limit), the length limit
  is consistent with the data: 26 of 32 final rules have 21 to 24 instructions. It was not tested.
- Residual insertion inside the evolutionary search is closed as a negative result in this space,
  as constant tuning was (packages F, G). The gradient-guided loop (growth loop, third version)
  reaches 0.77 to 0.80 in 7 of 8 task seeds with about 8k Rust evaluations each; that comparison
  is post hoc and on other task seeds (README, "Growth loop, third version: result of B3").
- `k-plain2m` (the wall-time control of J) runs on epyc, not on the workstation as RUNBOOK said:
  agreed with the research agent on 20 Nov, because J and `d-kalman` ran on epyc, so platform and
  minutes match the arms it controls. Command, budget (2.1M) and binary (6c2f60a) unchanged;
  timing projection 24.1 h.

### Package K, arm k-plain2m: result and reading (21 Nov 2026)

Run: `runs/k-plain2m`, commit 6c2f60a, epyc, seeds 1 to 32, 2.1M candidates, plain selection,
17.3 h for the arm; report `runs/k-plain2m/k_report.md`. Counts recomputed from the summaries;
they agree with the report. Up to 1.5M candidates every log row of every seed equals the row of
`d-kalman` (same binary and machine), so the arm is `d-kalman` continued by 600k candidates: a
reproduction check passed in passing.

| collision3, space of D and E | `d-kalman` (1.5M) | `k-plain2m` (2.1M) | `j-share` (1.5M) | `j-lexicase` (1.5M) |
|---|---|---|---|---|
| stuck (test < 0.53) | 12/32 | **9/32** | 0/32 | 0/32 |
| rule 2 | 6/32 | 8/32 | 11/32 | 12/32 |
| above 0.85 under the conditions | 1/32 | 1/32 (seed 9) | 0/32 | 1/32 (trick) |
| median test | 0.630 | 0.635 | 0.653 | 0.682 |
| minutes per seed, mean | 42 | 64 | 49 | 60 |

Against what was fixed before the run: the stuck effect of J stands at matched wall time if
`k-plain2m` has 5/32 or more stuck. **Met**: 9/32 (against 0/32 for both arms of J, Fisher
one-sided p = 0.001). Three of the 12 stuck seeds of `d-kalman` leave with the extra budget (18, 21,
23); the 11 seeds below 0.53 at 1.5M are the same 11 as in `d-kalman`. Median against `j-lexicase`:
Mann-Whitney p = 1.2e-4. Predictions of the research agent: 5 or more stuck (0.80) yes, a seed above
0.90 (0.03) no. Checks: JAX within 0.0005 on 31 seeds (seed 22 diverges in Rust's guard, as in
`d-kalman`); the ε check moves seed 9 by −0.0215 (0.855 to 0.834), with an ε-scale ratio of 0.94, so
not a scale trick, the same rule as `d-kalman` seed 9.

Reading: behaviour-based selection (J) removes the stuck seeds in the space of D and E, and the
plain search does not catch up with 40% more candidates and more wall time. With packages H, I and
L this is the one component with a supported effect, on two tasks. It does not raise the level:
no arm of this space reaches 0.90, and since 21 Nov the level that matters is the ridge ceiling,
which a classical reference reaches on collision3 (below, "A classical rule at the ridge ceiling").

## clustered8: a found rule against the tuned families and against an obvious fix (19 Nov 2026)

Prompted by the second outside review (owner, 19 Nov): `clustered8` (T48, 8 keys around one
centre, cos ≈ 0.8) is the regime with the largest measured gap between the best tuned family
and the ceiling (Kalman delta 0.680, ridge 1.000; `runs/sweeps/clustered8.md`), and no search
has been run on it. The 128 best rules of the space of D and E (`d-kalman`, `g-tune8`,
`j-lexicase`, `j-share`), all found on collision3, were evaluated on it unchanged.

| rule (state) | clustered8 test | 12 fresh draws, mean | gain over Kalman delta, draws won | T128 K8 |
|---|---|---|---|---|
| tuned DeltaNet (S) | 0.205 | 0.210 | −0.462, 0/12 | |
| Kalman delta (S, P), sweep, native | 0.680 | | | |
| Kalman delta in the space (S, P), δ and q tuned on clustered8 | 0.673 | 0.672 | – | |
| centred delta rule, hand-written reference (S, one vector) | 0.805 | | | 0.695 |
| `d-kalman` seed 9 as found on collision3 (P1, P2; S is recomputed each step) | **0.856** | **0.860** | **+0.188 ± 0.002, 12/12** | 0.885 |
| ridge ceiling | 1.000 | | | |

`verify/c8_checks.py` (fresh draws), `verify/probe_centering.py` (centring). JAX on the
clustered8 test dump reproduces seed 9 exactly (0.8564). Epsilon check: 0.804 at ε = 1e-9 in
float64, size of S independent of ε (ratio 0.87). The epsilon is a numerical floor there, as
described for seed 9 under package D, not a scale trick. Of the other 127 rules none is above
0.70 (best 0.603).

Reading:
- One rule found from the empty program on another regime beats every tuned family on
  clustered8 by 0.18 at a budget of two d×d states. It is one rule. A claim under rule 2 needs
  a rate over seeds from searches on clustered8 itself.
- The headroom is mostly structural and an obvious fix closes most of it. The keys share one
  centre. Subtracting a running mean of the keys before a delta write uses one extra vector
  and reaches 0.805. Centring does nothing on collision3 (best ρ = 1, i.e. no centring).
  Against "known families plus centring", seed 9 is ahead by 0.05, with more state. A discovery
  claim on clustered8 would have to include centred versions of the families as baselines, and
  a reviewer would read the regime as built around a single mean.
- Not released as a package. Searching here could still show whether the search finds rules
  above the centred delta rule at the same budget. That depends on the owner's choice of
  direction.

## Direction 2, fourth component considered: adjoint-guided growth (19 Nov 2026, feasibility test fixed before running)

Decided by the owner on 19 Nov 2026, on a proposal from the second outside review: the search
may use gradients to choose structure, as long as no LLM and no prior rule enters. The found
rules stay symbolic programs; the gradient only steers where the search adds code. Idea: run
the current program on the train episodes, backpropagate a smooth loss through all steps, and
read off for a register R the adjoint field G_t = ∂L/∂R_t at every step. A candidate
sub-expression e built from the registers then has a first-order effect proportional to
⟨G, e⟩ summed over steps and episodes. Candidates can be ranked from one forward and one
backward pass, without re-running episodes, and the best one is inserted as `R = R + ε·e`.
This addresses the measured barrier directly: a step of 3 to 5 instructions is scored as one
candidate before any of it is in the program. In a first search no direct precedent was
found; neighbours are semantic backpropagation in GP, gradient-based program repair (arXiv
2505.17703) and gradient-guided growth of neural networks.

Before anything is built into the search, a feasibility test (`verify/adjoint_probe.py`, JAX,
no search runs). The starting programs are hand-written points of the measured path (reference
probes, rule 6); the test asks only whether the ranking points to the next step.

| transition | start program | register | next step (target) |
|---|---|---|---|
| T1 | empty program | S | `v kᵀ` (linear attention write) |
| T2 | linear attention | S | `(S k) kᵀ` (erase along k; the delta family) |
| T3 | delta rule with write key `P k`, P fixed at I | P | `(P k)(P k)ᵀ` (step D') |
| T4 | normalised gain `g = P k/(δ + kᵀP k)`, P fixed | P | `g (P k)ᵀ` (step D) |
| T5 | D with c = 1, no `q·I` (train 0.62) | P | `I` (step E, train 0.93) |

- Candidates: every expression of one or two ops of the alphabet over the registers at the end
  of the step, of the register's type; zero and duplicate expressions (same values on the
  trace) removed. Score: |cos| between G and e over all steps and episodes. A candidate counts
  as the target when its values agree with the target's to |cos| > 0.999.
- Loss: cross-entropy over the 64 values with logits τ·cos(S q, v_j), τ = 10; scale-invariant
  in S, so candidates that only rescale S score zero. τ = 3 and 30 reported as sensitivity.
- Data: the collision3 train task (task seed 1), as the search sees it.
- Fixed before the run: the test supports building the component if the target is in the top
  5 of its register's candidates in at least 4 of 5 transitions. It speaks against it for this
  barrier if the target is outside the top 20 in 3 or more. Reported as well: the rank of the
  target, the five best candidates, and train accuracy after inserting the best candidate and
  the target with the best ε of ±{0.001, …, 1}.
- Prediction of the research agent: T1 and T2 in the top 5 with 0.8 each; T3 and T4 with 0.5
  each; T5 with 0.35. Criterion of 4 of 5 met with 0.35.

### Feasibility test: result and reading (19 Nov 2026)

`python verify/adjoint_probe.py TRAIN_DUMP.json [--tau T]`, collision3 train task (task seed 1),
all outputs in `runs/adjoint-probe/`. Candidates of one or two ops at the end of the step;
"rank" is among classes of the same direction (|cos| > 0.999, sign ignored, as for the target).

| transition | candidates | rank of the target, τ = 3 / 10 / 30 | best-ranked candidate (τ = 10) | train acc: start → best-ranked inserted → target inserted |
|---|---|---|---|---|
| T1 empty → `v kᵀ` | 30 | 1 / 1 / 1 | the target | 0.000 → 0.362 → 0.362 |
| T2 linear attention → erase `(S k) kᵀ` | 91 | 9 / 10 / 10 | `S_old` (decay of the old memory) | 0.362 → 0.500 → 0.598 |
| T3 key `P k`, P fixed → `−(P k)(P k)ᵀ` on P | 564 | 1 / 1 / 1 | the target, sign right | 0.617 → 0.623 → 0.626 |
| T4 normalised gain → `−g (P k)ᵀ` on P | 631 | 1 / 1 / 1 | the target, sign right | 0.578 → 0.618 → 0.767 |
| T5 D at c = 1 → `+q I` on P | 2439 | 30 / 31 / 31 | `P − ε s (P − I)`, a pull of P back to I | 0.607 → **0.898** → 0.932 |

(In T3 and T4 P is still the identity, so `P k = k` and the target is the direction `k kᵀ`.)

Against what was fixed before the run: the target is in the top 5 in 3 of 5 transitions (T1,
T3, T4), not 4; it is outside the top 20 in 1 of 5 (T5), not 3. Neither the criterion for
building nor the one against it is met. The prediction (top 5 in T1 and T2 with 0.8, T3 and
T4 with 0.5, T5 with 0.35) missed T2 and hit T3 and T4. The result is the same at τ = 3, 10
and 30.

Reading:
- One forward and one backward pass rank the next step of the path first in three of five
  transitions, among up to 631 candidates, including the steps on the second state that the
  search never takes (T3, T4).
- Where the target is not first, the first candidate is a different step that also helps.
  In T2 it is decay, the step every stuck seed takes; inserting the erase is better (0.598
  against 0.500). In T5 it is a pull of P back to the identity, a known form of forgetting in
  the covariance, which gets 0.898 of the 0.932 of `q I`. Inserting the best-ranked candidate
  raised train accuracy in all five transitions.
- A loop that ranks by the adjoint and then checks the best 10 candidates by real fitness
  would have taken the target step in 4 of 5; with the best 31, in all 5.
- What the test does not show: every start program here already reads P where it matters.
  Reading P while P is still the identity is a neutral step. Its first-order effect is zero
  and so is that of updating an unread P. That pair cannot be found by first-order ranking
  alone. It needs neutral drift (as in the evolutionary search) or a second-order term.
- Next test: a closed loop that grows a program from the empty one by rank-then-verify
  (below).

### Closed-loop growth test (fixed 19 Nov 2026, before running)

Owner's go on 19 Nov, with two points from the outside review taken over: constants are
polished by gradient after every accepted step, and residuals may target registers of any
type. A third point is tested as its own arm. That is the neutral tap: an unread persistent
matrix P that starts at I can be read through a tap `x ← P x`, which changes nothing while
P = I. Together with a write branch `P ← P + ε Δ` the pair has a first-order effect. Its
adjoint for P comes from the adjoints already computed:
G_P(t) = Σ_{τ>t} (∂L/∂x_τ) x_τᵀ. No extra pass is needed and no rule is named. The principle
(function-preserving growth, new part chosen by the gradient of its weights) is that of
GradMax (Evci et al., ICLR 2022, arXiv 2201.05125) and of Net2Net and network morphism. What
is new here is the use on typed recurrent programs, not the principle.

Loop (`verify/grow.py`, JAX for gradients, the Rust interpreter for every accuracy):
1. Sites are a register r at a position p of the program (before instruction p, or at the end
   of the step). For each site, the adjoint G = ∂L/∂r with the loss of the feasibility test
   (τ = 10). Candidates are expressions of one or two ops over the registers at p, as in the
   feasibility test, scored by the slope |⟨G, e⟩| / ‖e‖.
2. The best 60 (site, candidate) pairs over all sites, at most 3 per site, are inserted as
   `t = e; s = Const(ε); t = s·t; r = r + t`, with temporaries that are dead at p (as in
   `--residual-insert`), for ε in ±{0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3}. Each is scored by
   Rust train fitness (the search's fitness). The best is kept if it beats the current program.
3. Constant polish: 60 Adam steps on all `Const` values for the smooth loss. Kept if the Rust
   train fitness does not drop.
4. Stop when no candidate improves, when no candidate fits into `MAX_LEN` = 24, or after 20
   rounds.

Same space as packages D and E (`--persist-m 3 --persist-init identity --recip`, the 20 ops,
registers, `MAX_LEN` 24, collision3 train task); start is the empty program.

| arm | sites |
|---|---|
| A | every register of every type at every position, and S, P1, P2 at the end of the step |
| B | A, plus neutral taps `x ← P x` for every vector x at every position and every P not yet read |

Fixed before the run, on task seed 1 (the train task of all searches so far):
- Success of the loop: collision3 test ≥ 0.90 with rule 2's other conditions (T128 K8 ≥ 0.838,
  train − test ≤ 0.03) and the epsilon check. Partial success: ≥ 0.85 (the level of `d-kalman`
  seed 9).
- The taps matter if B reaches a level A does not reach (success or partial success for B
  only).
- Replicates: task seeds 2, 3 and 4, run after seed 1 and reported in full, whatever seed 1
  shows.
- Reported per round: the step taken, train and test accuracy, length, Rust evaluations and
  JAX passes. The cost is set against the 0.8M real evaluations of an evolutionary seed.
- Prediction of the research agent: A stops below 0.70 with probability 0.6. B reaches the
  partial level with 0.35 and success with 0.2. The main risks are the length limit (24) and
  the greedy loop taking decay at T2.

### Closed-loop growth test: result and reading (19 Nov 2026)

`python verify/grow.py --arm A|B --task-seed N`, design as fixed above, run once per arm and
task seed (the loop is deterministic). Logs and final programs: `runs/grow/arm{A,B}_task{N}/`.
Test is the fixed collision3 test suite; train is the train task of that task seed. The new
command `autoplast evalmany` scores a batch of programs with the search's own fitness. On two
committed rules it gives the summaries' train accuracies (0.732, 0.863).

| task seed | arm | train | collision3 test | T128 K8 | length | stopped by | taps taken | Rust evaluations | seconds |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A | 0.509 | 0.511 | 0.554 | 23 | length limit | – | 3,373 | 277 |
| 1 | B | 0.850 | **0.860** | 0.984 | 23 | length limit | 1 | 2,795 | 415 |
| 2 | A | 0.665 | 0.654 | 0.714 | 24 | length limit | – | 3,389 | 309 |
| 2 | B | 0.527 | 0.527 | 0.000 | 16 | no improvement | 1 | 2,295 | 158 |
| 3 | A | 0.654 | 0.644 | 0.778 | 17 | no improvement | – | 3,513 | 169 |
| 3 | B | 0.664 | 0.645 | 0.708 | 22 | length limit | 1 | 1,945 | 300 |
| 4 | A | 0.647 | 0.642 | 0.687 | 18 | no improvement | – | 3,241 | 186 |
| 4 | B | 0.799 | 0.771 | 0.895 | 21 | length limit | 1 | 2,137 | 356 |

Seconds are on this agent's 4-core container. On top of the Rust evaluations each round has
one forward-backward pass for the adjoints and 60 for the constant polish (about 300 per run).

Against what was fixed before the run (task seed 1):
- Success (≥ 0.90): not reached by either arm.
- Partial success (≥ 0.85 with rule 2's other conditions and the epsilon check): **arm B,
  0.860**, T128 K8 0.984, train − test −0.010. The JAX check reproduces 0.8602, also in float64
  at ε = 1e-9, and S does not scale with ε (ratio 1.0). Growth factor 0.975.
- The taps matter: B reaches a level A does not (0.860 against 0.511).
- Prediction: A below 0.70 (0.6) came true; B partial (0.35) came true; B success (0.2) did not.

Replicates (task seeds 2 to 4, reported as fixed):
- A ends between 0.64 and 0.65 every time (decay or delta rule, then nothing more).
- B is above A on seeds 1 and 4 (by 0.35 and 0.13), equal on 3, and below on 2 (by 0.13).
  On seed 2 the loop took a tap on v instead of k, a weak step it could not leave, and the
  rule fails on long episodes (T128 K8 0.000).
- B is above 0.85 in 1 of 4 and above 0.695 in 2 of 4. For the evolutionary search in this
  space the figures are 1 of 32 and 2 of 32 per seed (`d-kalman`). Four task seeds are too few
  for a rate under rule 2.

What the rule of task seed 1 is (`runs/grow/armB_task1/best.json`, 23 instructions):
P2' = P2 − 0.678·tanh(u) uᵀ with u = P2 k (an anti-Hebbian key preconditioner starting at I),
and S' = 0.973·[S − 0.243 (S k)kᵀ − 0.387 (S k)ûᵀ] + 0.013 v uᵀ, which is a delta-type rule
writing at the preconditioned key with an erase along k and along û. It is step D' of the
measured path plus erase terms. It is not new (Preconditioned DeltaNet, anti-Hebbian
decorrelation), and the claim here is not about the rule.

Reading:
- The mechanism works where it was meant to. In every B run a tap was taken in round 2 or 3,
  and the P update was entered in a single step, which the evolutionary search does in 1 of 32
  seeds at best. On task seed 1 that gives the level of `d-kalman` seed 9 in 2,795 Rust
  evaluations and about 300 gradient passes, against roughly 0.8M real evaluations per
  evolutionary seed.
- The loop is not reliable yet. It is greedy and runs one trajectory per task. One bad early
  choice (seed 2) cannot be undone. Three of four B runs stopped at the length limit of 24,
  because every step costs four or five instructions, including a `Const` and a scale.
- Next, before any claim: keep several programs per round instead of one (a beam). After
  each step, try deleting instructions and keep a deletion when fitness does not drop, to free
  length. Then run 8 or more task seeds against the evolutionary rates. These are changes to
  the loop and will be fixed in README before the run.

### Growth loop, second version (fixed 19 Nov 2026, before running)

Owner's go on 19 Nov, with three points of the outside review taken over. All changes are
generic; none names an op pattern of a known rule.

1. **Beam of 4, kept diverse.** Each round every beam member is expanded as in the first
   version (best 60 site-candidate pairs, at most 3 per site, all ε), and for every candidate
   the best ε gives one child. The next beam is the 4 best programs among the children and
   the current beam, by Rust fitness. At most one program is kept per skeleton (effective
   program without constant values). Among the children, at most one is kept per step
   signature (kind of step, target register, root op of the expression, tapped register).
   This prevents the beam from filling with variants of one path, the failure that behaviour
   selection removed in packages H and J. Stop when the beam does not change, or after 20
   rounds.
2. **Compaction** of every new beam member after the constant polish. The following steps
   are repeated until none applies. Each variant is scored by Rust fitness and kept only if
   fitness does not drop (the fitness carries the length penalty):
   - deletion of one instruction;
   - unit coefficient: `s = c; u = s·t; r = r + u` becomes `r = r + t` or `r = r − t`;
   - self residual: `s = c; u = s·r; r = r + u` becomes `s = 1 + c; r = s·r`;
   - common subexpressions: a repeated instruction whose inputs are unchanged is removed, and
     its readers read the first result.
   This addresses the length limit: every residual step costs a `Const` and a scale. Known
   rules mostly need neither (coefficients ±1).
3. **Reporting.** Per run: Rust evaluations, gradient passes (adjoints and polish) and wall
   time. The loop is deterministic, so its replicates are task seeds (train tasks 1 to 8).
   The replicates of the evolutionary search were search seeds on task seed 1. All rules are
   scored on the same fixed collision3 test suite and T128 K8. Any rule at 0.85 or above also
   gets 12 fresh draws, the epsilon check and JAX.

Arms: `B2` (with taps) on task seeds 1 to 8, then `A2` (without taps) on the same seeds.

Fixed before the run:
- An effect against the evolutionary search is shown if `B2` reaches ≥ 0.85 (with rule 2's
  other conditions and the epsilon check) in 3 or more of 8 task seeds. The evolutionary rate
  is 1 of 32 per seed (`d-kalman`); one-sided Fisher p = 0.020 for 3/8, 0.0035 for 4/8 (corrected
  from 0.023 the same day, before any result).
- The method is reliable enough to freeze and take to testbed 2 if `B2` does so in 5 or more
  of 8.
- A seed at ≥ 0.90 is reported as reaching the level of Kalman delta on that task seed; one
  seed is not a rate.
- The taps matter if `B2` has more seeds at ≥ 0.85 than `A2`.
- Prediction of the research agent: `B2` at ≥ 0.85 in 3 or more of 8 with probability 0.5,
  in 5 or more with 0.2; some seed ≥ 0.90 with 0.35; `A2` any seed ≥ 0.85 with 0.1.

Neighbours for the growth principle: GradMax (Evci et al., ICLR 2022, arXiv 2201.05125),
splitting steepest descent (Wu, Wang and Liu, NeurIPS 2019, arXiv 1910.02366; splitting
neurons to escape saddle points, a second-order criterion), Net2Net, network morphism.

Amendment of 20 Nov, before any result of the run: a crash, not a method change. The site
gradient was read with a dict literal that evaluated all three register types at once, so a
live `V4` or `V5` indexed the four-wide matrix array and stopped the run (`IndexError`). It hit
`B2` on task seeds 2, 3, 5, 7 and `A2` on 2, 4, 6, 8, after 2 to 6 rounds. Fixed in
`verify/grow.py` (the gradient of the site's own type is read). Every program that ran before
the fix gives the same scores after it, and the loop is deterministic, so the crashed seeds are
rerun from the start; the rerun has to repeat the rounds before the crash (checked, see the
result). Wall time is on a shared 4-core container with two runs in parallel.

Second amendment of 20 Nov, also before any result: a container restart stopped all runs.
`verify/grow.py` now saves the beam, the counters and the elapsed time after every round and
continues from that state when restarted. Test (B2, task seed 3, 3 rounds): a run killed after
round 2 and resumed gives the same rows, Rust evaluation and gradient-pass counts, final report
and `best.json` as an uninterrupted run. The rerun of B2 task seed 2 repeated the 5 rounds before
its crash exactly, Rust evaluation count included.

### Growth loop, second version: result of B2 and reading (20 Nov 2026)

`python verify/grow.py --arm B --beam 4 --compact --task-seed N`, logs in
`runs/grow2/armB2_taskN/`. Test is the fixed collision3 test suite.

| task seed | collision3 test | T64 K8 | T128 K8 | length | rounds | Rust evaluations | grad passes | hours |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.814 | 0.902 | **0.000** | 24 | 7 | 9,698 | 1,167 | 0.6 |
| 2 | 0.623 | 0.795 | 0.834 | 24 | 10 | 16,672 | 1,719 | 1.6 |
| 3 | 0.650 | 0.853 | 0.703 | 14 | 20 | 54,491 | 2,715 | 2.5 |
| 4 | 0.647 | 0.813 | 0.854 | 20 | 20 | 20,310 | 1,935 | 2.2 |
| 5 | 0.811 | 0.955 | **0.000** | 21 | 20 | 13,193 | 1,995 | 3.1 |
| 6 | 0.752 | **0.000** | **0.000** | 21 | 5 | 9,269 | 919 | 0.4 |
| 7 | 0.651 | 0.832 | **0.000** | 22 | 6 | 12,266 | 863 | 0.7 |
| 8 | 0.647 | 0.841 | **0.000** | 17 | 4 | 9,844 | 795 | 0.3 |

Against what was fixed before the run:
- Effect against the evolutionary search (≥ 0.85 in 3 or more of 8): **not met**, 0 of 8.
- Freeze (5 or more of 8): not met. No seed at 0.90.
- Prediction (3 or more of 8 with probability 0.5): wrong.

What fails: the loop exploits the short train episodes. The three best rules (seeds 1, 5, 6)
put a growth term into the key preconditioner P2: `P2 + 0.013·P2·P2`, `P2·(1 + 0.037·|S k|)`, a
cubic term. Under them sits the family of the first version's rule (a delta write at the
preconditioned key P2·k with an anti-Hebbian P2), but the growth makes it blow up on long
episodes. This is the mechanism of RLS with forgetting ρ > 1 in "A known target" (0.933 test,
T128 K8 0.000) and the degenerate win of CLAUDE.md rule 3. A probe on 64 episodes of 256 writes
(below, third version) is infinite for 7 of the 8 rules (all but seed 3), including seeds 2 and
4, which pass T128 K8 (0.834, 0.854) and diverge only later. Of the 32 best rules of `d-kalman`, 31 stay below
40 on the same probe; the one that diverges (seed 22, T128 K8 0.561) is in no count. This does
not show that evolution is more stable as a search: it reaches a working P update far less often
(1 of 32 above 0.85), so it rarely meets the choice.

Beam and compaction did not raise the level against the first version (task seeds 1 to 4: 0.814,
0.623, 0.650, 0.647 against 0.860, 0.527, 0.645, 0.771). The length limit still binds (21 to 24 in
six of eight). Cost per seed: 9k to 54k Rust evaluations, against about 0.8M per evolutionary seed.

#### Two checks asked by the owner (20 Nov, in the B2 logs and code)

1. *Was the identity available to the P update?* Yes while M1 was unwritten: M1 then holds I at
   every step, and candidates with it were taken, `M2 += ε·(M1 − M2)` with ε = −0.1 three times
   (P2' = 1.1·P2 − 0.1·I, growth away from I) and `M2 += ε·|V3|·M1` with ε = −0.003. On short
   episodes the gradient chose the growing sign. Later the loop used M1 as a temporary in every
   seed (all eight final programs write M1), and from then on I was not available. Under a gate
   that refuses growth, the bounded alternatives (+q·I, ε·(I − P)) need I, so this is fixed in
   the third version.
2. *Why did seeds 2, 3, 4 stay near 0.64: taps pushed out of the top 60, or two-state programs
   pushed out of the beam?* Neither. In all eight seeds a tap entered the beam in round 2 or 3,
   and from round 3 on every beam member descended from a tap program. In seeds 2, 4 and 8 the P
   branch is a scalar self-growth, P2' = P2·(1 + 0.01·|…|): P2 stays a multiple of I and acts as a
   growing step size, not as a preconditioner. In seed 3 it is a weak rank-one update (−0.01).
   A separate quota for taps or a niche per number of states would not have changed these seeds;
   they are not taken over.

### Growth loop, third version (fixed 20 Nov 2026, before running)

Owner's go of 20 Nov: a third version on unseen task seeds, with a stability gate and the fixes
the two checks call for. `python verify/grow.py --v3 --arm B --beam 4 --task-seed N`, logs in
`runs/grow3/armB3_taskN/`. All changes are generic and name no op pattern of a known rule.

1. **Stability gate.** A program enters the beam (a selected child, a polished version, each
   compaction step) only if every entry of S and of the persistent registers stays finite and
   below 100 in absolute value over 64 episodes of 256 writes on at most 8 keys, with the keys of
   the train distribution and its own draws (task seed + 1000). New Rust command:
   `autoplast evalmany --split long` (`task::max_state`); the train fitness is unchanged, the gate
   only refuses. Calibration on existing rules: stable rules give 0.3 to 40 (v1 seed 1: 1.0;
   `d-kalman` seeds 9 and 2: 4.9 and 4.7; Kalman delta written in the space: 2.1), the unstable
   B2 rules give infinity. The bound is not tuned; any value from 50 to 1e4 separates these.
   Gate evaluations and refusals are reported.
2. **Identity kept.** Persistent matrix registers the program never writes hold I at every step;
   they are not used as temporaries. Temporaries are written in place (a node writes into its
   child's temporary), so one matrix temporary (M3) is enough for every candidate expression.
3. **Compaction.** A unit fold that misses the acceptance by less than 0.01 in fitness gets 15
   polish steps on the remaining constants and is scored again (outside review).
4. **Stop rule.** Stop when the best program has not improved for 3 rounds, when the beam does not
   change, or after 20 rounds. In the second version the best never improved again after 3 rounds
   without improvement (0 of 8 seeds), so on that evidence the rule loses nothing; it saves the
   idle rounds of seeds 3, 4 and 5 (up to 2 hours each).
5. **Unseen task seeds 10 to 17.** Seeds 1 to 8 have been looked at through two versions. Seed 9 is
   excluded: it is the seed of the collision3 test suite (`regime_cfg(r, 9, 512)`), so a train
   task with seed 9 would share the key and value tables and its first episodes with the test.

Fixed before the run (as for the second version):
- An effect against the evolutionary search is shown if `B3` reaches ≥ 0.85 with rule 2's other
  conditions and the epsilon check in 3 or more of 8 task seeds (one-sided Fisher against 1 of 32,
  p = 0.020). Every such rule also gets 12 fresh draws and JAX (`verify/grow2_checks.py`).
- The method is frozen and taken to testbed 2 if `B3` does so in 5 or more of 8.
- A seed at ≥ 0.90 is reported as reaching the level of Kalman delta on that seed.
- Limit stated now: the evolutionary rate comes from 32 search seeds on task seed 1; the loop is
  measured over task seeds. This assumes that train draws of the same regime are of similar
  difficulty. The gate is applied to the loop only; on the evolutionary arm it would have refused
  one rule of 32, counted nowhere.
- Prediction of the research agent: `B3` at ≥ 0.85 in 3 or more of 8 with probability 0.3, in
  5 or more with 0.1; some seed ≥ 0.90 with 0.15; the gate refuses at least one child in every
  seed with 0.8.

Order of runs: `B3` on seeds 10 to 17 first, in two lanes; the remaining `A2` seeds of the second
version afterwards (they resume from their saved state).

### Growth loop, third version: result of B3 and reading (20 Nov 2026)

`python verify/grow.py --v3 --arm B --beam 4 --task-seed N`, task seeds 10 to 17, logs in
`runs/grow3/armB3_taskN/`, checks in `runs/grow3/checks_b3.md` and `checks_b3_16_17.md`. Test is
the fixed collision3 test suite; "fresh" is the mean over the 12 fresh draws of
`verify/grow2_checks.py` (tuned DeltaNet 0.643, hand-written Kalman delta 0.934 on the same draws);
"long" is the gate probe of the final rule (largest |entry| over 64 episodes of 256 writes).

| task seed | train | test | fresh | T64 K8 | T128 K8 | long | length | rounds | Rust evaluations | grad passes | gate evaluations | refused | minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.825 | 0.804 | 0.811 | 0.924 | 0.897 | 1.0 | 24 | 7 | 8,331 | 1,223 | 49 | 11 | 35 |
| 11 | 0.800 | 0.800 | 0.805 | 0.928 | 0.899 | 1.0 | 24 | 7 | 7,648 | 1,043 | 62 | 28 | 34 |
| 12 | 0.802 | 0.799 | 0.805 | 0.931 | 0.901 | 1.0 | 23 | 7 | 8,307 | 1,043 | 72 | 32 | 34 |
| 13 | 0.800 | 0.773 | 0.776 | 0.899 | 0.907 | 1.0 | 23 | 7 | 8,530 | 1,178 | 47 | 16 | 33 |
| 14 | 0.794 | 0.782 | 0.788 | 0.902 | 0.845 | 1.0 | 23 | 8 | 8,724 | 1,122 | 82 | 42 | 43 |
| 15 | 0.797 | 0.778 | 0.783 | 0.882 | 0.808 | 1.0 | 23 | 7 | 8,628 | 998 | 62 | 28 | 34 |
| 16 | 0.669 | 0.645 | 0.650 | 0.851 | 0.858 | 3.6 | 15 | 9 | 17,794 | 1,182 | 123 | 58 | 33 |
| 17 | 0.805 | 0.790 | 0.797 | 0.971 | 0.989 | 10.4 | 21 | 6 | 8,443 | 1,039 | 38 | 5 | 25 |

Every rule beats tuned DeltaNet on 12 of 12 fresh draws and loses to Kalman delta on 12 of 12.
JAX reproduces each test accuracy exactly in float32 at ε 1e-6 and in float64 at ε 1e-9; no rule
uses Normalize and the ε-scale ratio is 1 for all eight. Train − test is at most 0.027.

Against what was fixed before the run:
- Effect against the evolutionary search (≥ 0.85 in 3 or more of 8): **not met**, 0 of 8. The
  best rule reaches 0.804 test, 0.811 fresh.
- Freeze and testbed 2 (5 or more of 8): not met. No seed at 0.90.
- Predictions: 3 or more of 8 (probability 0.3) wrong; a seed ≥ 0.90 (0.15) no; the gate refuses
  at least one child in every seed (0.8) right, 5 to 58 children per seed.

What the gate changed. The failure of the second version is gone: all eight final rules stay
bounded on 256-write episodes (largest entry 1.0 to 10.4, against infinity for 7 of 8 B2 rules),
and T128 K8 is 0.81 to 0.99 (B2: 0.000 in 5 of 8). Seven of eight seeds reach 0.77 to 0.80 test
with a working two-state rule; the one B2 rule that stayed bounded (seed 3) was at 0.650. The
seeds are different, so this is no paired comparison of the versions.

What the loop finds. Five of the seven (seeds 10, 11, 12, 14, 15) assemble the same family,
with x = P2·k:

    S'  = (1 − c)·(S − η·(S k)⊗x) + v⊗(P1 x)            η ≈ 0.61 to 0.65, c ≈ 0.05
    P1' = P1 − η·(P1 x)⊗tanh(P1 x)
    P2' = P2 + α·|S k|·(P1' − P2)                      α ≈ 0.016 to 0.10

(seeds 14 and 15 decay S by S − c·S·P1 instead of a scalar; seed 14 writes tanh(v)). The
rule erases along a preconditioned key and writes along a doubly preconditioned key: decoupled
erase/write rather than the delta form (v − S k); P1 is updated anti-Hebbian, P − η·(P x)(P x)ᵀ,
the form of the RLS/Kalman covariance update with a fixed step in place of 1/(r + kᵀPk); P2 is a
lagged copy of P1 that moves at a rate set by the read |S k|. Seed 17 is a variant without the
lag (P2' = P2 − 0.036·(P2 k)⊗(P2 k) + 0.039·P1'ᵀ) and has the best long-episode accuracy (T128 K8
0.989). Seed 13 uses one preconditioner. None of these is new as a mechanism (anti-Hebbian
decorrelation, novelty filter, Preconditioned DeltaNet, Kalman delta, Erase-then-Delta are
neighbours), and all score below Kalman delta, so no discovery claim follows. Seed 16 is the
failure of B2 seeds 2, 4 and 8 again: P2' = P2 + 0.010·|e|·P1ᵀ with P1 = I unwritten, a step size
that grows linearly and stays below the gate bound; the rule is a delta rule at 0.645.

Why it stops at 0.80. The length limit binds: the best program has 23 or 24 instructions in six
seeds and 21 in seed 17, and every seed stops by "beam unchanged" (or, seed 16, three rounds
without improvement) one or two rounds after reaching it. What the family lacks against Kalman
delta is the normalisation 1/(r + kᵀPk) and the q·I term; with no free instructions left, no
residual block that could add them fits.

Cost: 7.6k to 8.7k Rust evaluations and 1.0k to 1.2k gradient passes per seed (seed 16: 17.8k),
25 to 43 minutes on one container core per seed. An evolutionary seed in this space evaluates about
0.98M candidates in about one hour.

Not fixed before the run, reported as observation only. Below the 0.85 bar the gap to the
evolutionary arms is large. Test ≥ 0.75: loop 7 of 8; evolutionary arms in this space (`d-kalman`,
`j-lexicase`, `j-share`, 96 seeds on task seed 1) 1 of 96 counted (`d-kalman` 9, 0.855;
`j-lexicase` 6 at 0.893 is the scale trick and not counted; the next best is 0.721). One-sided
Fisher p = 3e-9, but the threshold was chosen after seeing the data and the loop runs on other task
seeds than the evolutionary arms. Rule 2: loop 6 of 8 (seed 15 fails T128 K8, seed 16 the test
bar), evolutionary arms 28 of 96 (p = 0.014, same caveats). A claim needs both arms on the same
task seeds with the threshold fixed first.

## A classical rule at the ridge ceiling: the measured headroom was mostly not there (21 Nov 2026)

Prompted by a result of 1.000 on the collision3 validation split reported from the owner's PC
(below), a hand-written reference was added (`verify/probe_olam.py`; CLAUDE.md rule 6: reference
only, never a candidate, seed or mutation): the RLS covariance update with a separate, smaller
regulariser in the memory write,

    P' = P − (P k)(P k)ᵀ / (δ_P + kᵀP k)          P₀ = I
    S' = S + (v − S k)(P k)ᵀ / (ε + kᵀP k)

16 instructions, two states, `--persist-m 2 --persist-init identity --recip`. With ε = δ_P it is the
plain RLS of `verify/probe_rls.py` (ρ = 1), which averages a rewritten key with its old values
(collision3 test 0.62). With ε = 0 the write gain is P k / kᵀP k: for a new key the normalised
novelty vector of Greville's recursive pseudo-inverse (the recursive form of Kohonen's optimal
linear associative memory, S = V K⁺), and for a rewritten key, through the small δ_P left in P,
the dual vector of that key, so the old value is replaced and the other keys are kept. The
regulariser of the write was tied to that of P in both earlier probes; untying it is the whole
difference. Grid δ_P ∈ {0.01, …, 3}, ε ∈ {0, …, 0.3}, best by train (`runs/sweeps/probe_olam_*.md`).

| regime (test) | tuned Kalman delta | this reference | ridge ceiling | headroom left |
|---|---|---|---|---|
| collision3 | 0.935 | **1.000** (δ_P 0.03, ε 0) | 1.000 | 0 |
| collision | 0.991 | 1.000 | 1.000 | 0 |
| clustered | 0.958 | 1.000 | 1.000 | 0 |
| clustered8 | 0.680 | **1.000** | 1.000 | 0 |
| longgap | 0.956 | 1.000 | 1.000 | 0 |
| rewrite8 | 0.951 | 1.000 | 1.000 | 0 |
| rewrite14 | 0.854 | 0.999 | 1.000 | 0.001 |
| noisyq | 0.967 | 0.984 | 0.990 | 0.006 |
| full (T24) | 0.944 | 0.983 | 0.995 | 0.012 |
| overload (T32) | 0.805 | 0.878 | 0.955 | **0.077** |
| overload48 | 0.591 | 0.603 | 0.749 | **0.146** |

On collision3 the setting δ_P = 0.03, ε = 0 passes every check: train 1.000, test 1.000 (JAX
float32 and float64 at ε 1e-9: 6500/6503), T64 K8 and T128 K8 1.000, d32 1.000, query gap 4
0.993, long-episode probe 3.5 (bound 100), 12 fresh draws 0.9997 against 0.934 for Kalman delta
(12/12). The regimes with at most d distinct keys per episode are solved exactly by a pseudo-inverse
memory; the ridge ceiling is reachable online there.

What this changes:
- Kalman delta was the strongest reference so far, and it is not the strongest known rule in
  this space. Every "headroom" of stage 2 except overload and overload48 was measured against
  too weak a reference. From now on this reference sits next to every number, with the families
  of CLAUDE.md rule 2 (adding it to that list is the owner's decision).
- Earlier readings stand as measured but lose their weight: `d-kalman` seed 9 (collision3 0.864,
  clustered8 0.860) and the growth-loop rules (0.77 to 0.80) are all below a 16-instruction
  classical rule. "Reaching Kalman delta" (Direction 2) aimed below the ceiling.
- No rule can be better than known rules on collision3 or the other solved regimes; at most it
  ties. A search that finds a ceiling-level rule there is a method result (rediscovery of the best
  rule of the regime), not a discovery. A discovery claim needs a regime with headroom above this
  reference: overload (0.077) and overload48 (0.146), where an episode has more distinct keys
  than dimensions.
- Literature: the reference belongs to recursive least squares and recursive pseudo-inverse memory
  (Kohonen and Ruohonen 1973; Greville 1960). Recent neighbours of the same kind: MesaNet, Kernel
  Ridge Attention (arXiv 2611.23896, 18 Nov 2026), Kalman Delta Networks.

### The memetic MAP-Elites search on the owner's PC (recorded 21 Nov, before any counted result)

Recorded from the log of the agent on the owner's PC; the code (`v2/memetic`, a separate Rust
binary, the autoplast search unchanged) and its `PROTOCOL.md` are not yet in the repository.
After three dropped attempts at continuous relaxations (a dense typed supergraph with pruning, a
relaxed register machine, smooth L0 pruning; none reached the 24-instruction space at a useful
level), the agent built a search in the exact autoplast space: fitness MSE of S q against v plus
0.015·mean(state²) and a length tie-break, constants tuned by coordinate search and Nelder–Mead on
the best candidates, liveness-safe residual, chain and wrap mutations, and a MAP-Elites archive
over effective length × live states × written states × the 4 most frequent ops. Development used
only the train dump of task seed 1 and a validation dump (task seed 2001); the test suite was not
loaded. A development seed reached 1.000 on validation in 296k candidates (23 instructions), the
level of the reference above. The method was then frozen and a counted run started: 4 search seeds
on task seed 1 and 4 on the unseen task seed 501, 300k candidates each.

How the research agent will read it (fixed now, before any counted result is seen):
- A seed counts if its `best.json` (chosen on train and validation only) gives, in the Rust
  binary of this repository, collision3 test > 0.90, T128 K8 ≥ 0.838, train − test ≤ 0.03, the
  long-episode probe below 100, and no change above 0.02 under `verify.py --x64 --norm-eps 1e-9`.
- Task seed 1 is the development task, so its 4 seeds are reported but are not an independent
  measurement; task seed 501 is. Four seeds per arm is below the 8 of rule 2: a rate needs 8 or
  more unseen task seeds with the method unchanged.
- On collision3 the best possible outcome is a tie with the reference (1.000). Against the
  evolutionary arms in this space (0/160 seeds above 0.90: `d-kalman`, `g-tune8`, `j-lexicase`,
  `j-share`, `k-ri-lex`) it is a method result only after an ablation at equal cost, counted in
  episode evaluations: the MSE fitness, the constant tuning, the archive and the new mutations each
  switched off. Constant tuning alone had no effect under the accuracy fitness (packages F, G).
- Each counted rule is compared in formula with the reference (is it a recursive pseudo-inverse
  in substance?) before anything is said about its structure.

### The memetic MAP-Elites search: counted run as reported, and what was checked here (21 Nov 2026)

Reported by the agent on the owner's PC (Rust `eval` and its audit there; files not yet in the
repository). 300k candidates per seed, method frozen before the run.

| task seed | search seed | instructions | train | collision3 test | T128 K8 | long probe | counts (reading fixed above) |
|---|---|---|---|---|---|---|---|
| 1 (development task) | 10 | 24 | 0.992 | 0.995 | 1.000 | 3.0 | yes |
| 1 | 11 | 22 | 1.000 | 0.999 | 1.000 | 3.6 | yes |
| 1 | 12 | 19 | 1.000 | 1.000 | 1.000 | 3.9 | yes |
| 1 | 13 | 24 | 0.942 | 0.945 | 0.980 | 1.6 | yes |
| 501 (unseen) | 100 | 23 | 0.999 | 1.000 | 1.000 | 4.0 | yes |
| 501 | 101 | 23 | 0.834 | 0.839 | 0.965 | 1.7 | no (test ≤ 0.90) |
| 501 | 102 | 24 | 0.839 | 0.840 | 0.646 | 1.7e120 | no (unstable) |
| 501 | 103 | 22 | 0.721 | 0.729 | 0.958 | 1.0 | no (test ≤ 0.90) |

Reading, as fixed before the results:
- Unseen task: 1 of 4. Development task: 4 of 4, not an independent measurement. The gap between
  the two (Fisher p = 0.07 on 4 + 4) is a warning that the method may be tuned to task seed 1;
  four seeds settle nothing. No rate is established yet.
- Level: the counted rules tie the reference at the ceiling (1.000). On collision3 this is a
  method result at best, not a discovery. Against 0/160 evolutionary seeds above 0.90 (all on task
  seed 1), the comparison still lacks the ablation at equal cost and matched task seeds.
- The selection of the search does not look at long episodes: the best rule of seed 102 by train
  and validation diverges. A generic stability check inside the selection would be a method change,
  so a new version, measured on fresh task seeds.

Checked here: the rule of task seed 1, search seed 12, was rebuilt from the algebra the agent gave
(19 instructions, c₁ = 0.1676, c₂ = 6.764; not from its bytecode, which is not in the repository):

    p = P k,   u = p / ‖p‖,   e = v − S k
    P' = P − (2u − p)(p − c₁u)ᵀ
    S' = S + e uᵀ + c₂ (e uᵀ) P'³

In the Rust binary of this repository it gives 1.000 on the collision3 test from the train tasks of
seeds 1 and 501, T128 K8 1.000, d32 1.000, long probe 4.0. The description is consistent with the
reported numbers. In substance it is the family of the reference: along every direction it writes,
P is driven to the fixed point c₁ (a novelty filter with a floor, like the small δ_P left in P
above), and the write runs along the normalised P k with the unseen component amplified about
45-fold over the seen one through c₂·P'³, an approximate dual vector without a reciprocal. Not
claimed to be the same function. Post hoc, untuned on the regime: full 0.985 (reference tuned on
full 0.983), overload 0.864 (0.878), overload48 0.478 (0.603), noisyq 0.970 (0.984).

Five of the eight rules were then uploaded by the owner (`runs/memetic-pc/`; the rebuilt seed 12
is stored separately and labelled as such). Checked here in Rust and JAX:

| rule | collision3 test | train (own task seed) | T128 K8 | long probe, 9 draws | JAX f32 / f64 at ε 1e-9 | ε-scale ratio | 12 fresh draws |
|---|---|---|---|---|---|---|---|
| s501 seed 100 | 1.000 | 1.000 | 1.000 | 3.5 to 5.6, two draws 48 and 56 | 6500 / 6503 of 6503 | 1.00 | 1.000 (reference 0.9997) |
| s501 seed 101 | 0.839 | 0.842 | 0.965 | 1.3 to 1.6 | | | |
| s501 seed 102 | 0.840 | 0.850 | | infinite | | | |
| s501 seed 103 | 0.729 | 0.736 | 0.958 | 0.8 to 1.0 | | | |
| s1 seed 13 | 0.945 | 0.942 | 0.980 | 1.5 to 1.7 | 6148 / 6148 of 6503 | 1.00 | 0.946 |

The reported numbers are confirmed. One slip in the PC audit: the train accuracies of the task-501
rules were computed on task seed 1 (0.999, 0.834, 0.839, 0.721); on their own task they are those
above, and train − test stays within 0.03. The long probe of seed 100 is heavy-tailed (48 and 56 in
two of nine draws, bound 100), so its stability margin is thinner than the PC's 4.0 suggests.

Post hoc, not fixed before (`verify/long_probe_jax.py`, episodes of 1024 writes on at most 8
clustered keys): the reference with its collision3 setting (δ_P = 0.03) falls to 0.043, because
kᵀP k of a key rewritten about 128 times drops to where the 1e-6 in the Recip op dominates; with
δ_P = 0.3 to 3 it holds 1.000 at T = 1024 but drops to 0.91 to 0.71 on the collision3 test; a floor
q·I gives 0.99 on the test and 0.77 at T = 1024. Seed 100 holds 1.000 and the rebuilt seed 12 0.998
at T = 1024, with 1.000 on the test; neither uses Recip. So the found rules are of equal accuracy
on the suites and hold across horizons where the reference, in this space, needs a horizon-dependent
δ_P. This is a lead for "a different rule of equal accuracy", not a result: the 1024-step suite was
chosen after seeing the rules, and the gap comes from the epsilon of the reciprocal op, which a
reviewer can remove. Before it is used, a mixed regime with very long episodes is fixed in advance
and the reference families are tuned on it.

### The memetic search in the repository (`v2/`, merged 21 Nov from branch `v2`)

The owner's collaborator pushed the stack to branch `v2` (commits 5241a3e and ac3fe4a), merged here.
Checked:
- Rule 1: the search starts from 512 random programs of 1 to 6 instructions; the Kalman oracle
  appears only in `--self-test`; no known rule enters a population or a mutation. The search loads
  only the train and validation dumps.
- Data: `v2/data/` equals the dumps of this repository's binary up to the last float32 bit (at
  most 7e-8, Windows against Linux), with identical episodes. The validation dumps are train-split
  dumps of task seeds 2001 and 2501 (192 episodes).
- All 8 counted `best.json` reproduce their reported numbers in this repository's Rust binary
  (s1 seeds 10, 11, 12: 0.995, 0.999, 1.000). The bytecode of s1 seed 12 is the formula rebuilt
  above. The audit slip (train on the wrong task seed) is fixed in ac3fe4a; the verdicts do not
  change.
- **The search is not deterministic.** The same seed and flags twice on the same machine gave
  validation 0.942 and 0.630 at 30k candidates. Cause: the archive is a `HashMap` with a random
  hash seed per process, so the order of `all_elites()` among elites of equal objective (frequent:
  neutral variants of one function) changes from run to run, and parent selection by index follows
  it. With `BTreeMap` for `Archive.cells` (two lines, no change to the algorithm) the two runs are
  identical. The counted results stay valid as draws of the method, but no seed of them can be
  re-run exactly; a rerun of s501 seed 100 here gave a different rule (train 0.982, test 0.987,
  T128 1.000) after the same 300,544 candidates. Every counted run from now on uses the fixed
  binary, and the original 8 are reported as they are, not replaced by reruns.
- Cost is logged as candidates and wall time only (92 s on 16 threads for s501 seed 100); the
  comparison with the evolutionary arms needs episode evaluations, which the binary does not count.

### Ablation of the memetic search (`ablations_v31`, running on the owner's PC; recorded 21 Nov before its end)

As reported from the PC (protocol `v2/runs/ablations_v31/PROTOCOL.md`, not yet in the repository):
5 arms (`full`, `no_const_tune`, `acc_fitness`, `no_archive`, and a fifth, presumably the new
mutations off) × 8 unseen task seeds 701 to 708, each run stopped at 22M episode evaluations, binary
v3.1 (said to contain the deterministic archive and the episode counter). Validation accuracies
reported so far: `full` 5/8 above 0.94 and 4/8 above 0.99; `no_const_tune` 5/8 above 0.97;
`acc_fitness` 3/8 above 0.99; `no_archive` 1/4 above 0.90 on the first four seeds.

How the research agent will read it (fixed now, before the audited results are seen):
- Per arm, the count of the reading above (Rust test > 0.90, T128 K8 ≥ 0.838, train − test ≤ 0.03,
  long probe < 100 on its own task seed, ε shift ≤ 0.02), and separately the count at test ≥ 0.99.
  Validation numbers do not count.
- Each arm against `full` by one-sided Fisher on the first count. With 8 seeds per arm only large
  gaps show (6/8 against 1/8 gives p = 0.02; 5/8 against 3/8 gives p = 0.31), so "no difference"
  here means "not shown at this size". A component is called necessary only if its arm differs at
  p < 0.05; otherwise the comparison goes to 16 seeds before anything is said.
- Constant tuning alone had no effect in the evolutionary search either (packages F, G); the
  archive is a structural diversity mechanism of the kind behaviour selection was (packages H, J).
- Cost: an evolutionary seed of this space spends about 0.8M real evaluations of 144 episodes each,
  about 113M episode evaluations (`d-kalman` 785k, `j-lexicase` 807k real evaluations), 5 times the
  22M of an ablation arm, and reached 0.90 in 0 of 160 seeds, all on task seed 1. The matched
  comparison on task seeds 701 to 708 is package M (RUNBOOK), proposed to the owner.

### Ablation of the memetic search: audited result as reported, read as fixed (21 Nov 2026)

As reported from the PC after its audit (files not yet in the repository; the numbers below are
recomputed here once they are). Count = audited valid and collision3 test > 0.90.

| arm (task seeds 701 to 708, 22M episode evaluations) | valid | count | test ≥ 0.99 | median candidates |
|---|---|---|---|---|
| `full` (v3.1 default) | 3/8 (5 unstable on the long probe) | 2/8 | 2/8 | 396k |
| `no_const_tune` | 8/8 | **5/8** | 3/8 | 2,295k |
| `acc_fitness` | 8/8 | 3/8 | 3/8 | 252k |
| `no_archive` | 4/8 (4 unstable, 1 ε trick) | 1/8 | 0/8 | 492k |
| `basic_mut` | 8/8 | 0/8 | 0/8 | 1,202k |

Against the reading fixed before (each arm against `full`, one-sided Fisher, a component called
necessary only at p < 0.05): **no component is shown necessary at 8 seeds.** `no_const_tune` above
`full` p = 0.16, `basic_mut` below `full` p = 0.23, `no_archive` p = 0.50, `acc_fitness` p = 0.50.
The reference arm `full` is itself weakened by unstable rules, which is why the planned contrasts
carry little.

Post hoc, not fixed before and not a result: against `no_const_tune`, `basic_mut` 0/8 (p = 0.013)
and `no_archive` 1/8 (p = 0.059). The pattern says: constant tuning in the inner loop moves rules
across the stability bound (rule 3: tuned on 64-step episodes, diverging at 256), and the
liveness-safe structural mutations carry most of the effect; the archive may help. This choice of
reference arm was made after seeing the results, so task seeds 701 to 708 are spent for it. A
claim needs the variant fixed first (`no_const_tune`), its ablations taken from that variant
(mutations off, archive off), 16 fresh task seeds, and package M on the same seeds.
Descriptive: every audited rule above 0.90 uses Normalize and none uses Recip (24 of 24, PC count).

### Memetic search v3.1 in the repository: 16 unseen task seeds and the ablation, recounted here (21 Nov 2026)

Pushed to branch `v2` (71d7948) and merged: binary v3.1 (deterministic `BTreeMap` archive,
episode-evaluation counter, ablation flags), the run `v2/runs/frozen_16seeds` (task seeds 601 to
616, default flags, 300k candidates, about 21.7M episode evaluations and 450 s on 16 threads per
seed) and `v2/runs/ablations_v31`. Both have a `PROTOCOL.md` written on the PC before the runs; they
reached the repository in one commit after the results, so the time of writing is the PC's word.
A partial v3.0 run on 601 to 610 was discarded untested when v3.1 was built.

Recount here, with this repository's Rust binary: collision3 test > 0.90, T128 K8 ≥ 0.838,
train − test ≤ 0.03 on the rule's own task seed, the long probe below 100 in all of nine draws
(own task seed and 1 to 8), JAX float32 and float64 at ε 1e-9 within 0.02.

| run | count | test ≥ 0.99 among them | PC audit | difference |
|---|---|---|---|---|
| `frozen_16seeds` (v3.1 default) | **8/16** | 4 | 8/16 | none |
| ablation `full` | 2/8 | 2 | 2/8 | none |
| ablation `no_const_tune` | 4/8 | 3 | 5/8 | seed 704: T128 K8 0.676, not checked on the PC |
| ablation `acc_fitness` | 3/8 | 3 | 3/8 | none |
| ablation `no_archive` | 1/8 | 0 | 1/8 | none |
| ablation `basic_mut` | 0/8 | 0 | 0/8 | none |

All 18 counted rules agree between JAX float32 and float64 at ε 1e-9 to the fourth digit (no
ε trick). One rule of `frozen_16seeds` (seed 607, test 0.985) passes the long probe on its own task
seed (20.9) and diverges in five of the other eight draws; it is not counted, which is why a single
draw is not enough. Seed 614 (test 0.994) diverges on every draw.

Reading:
- The frozen v3.1 default finds a rule at the ceiling level on unseen task seeds in 8 of 16 (4 at
  ≥ 0.99), and 2 of 8 on 701 to 708; pooled 10 of 24. The evolutionary arms of this space reached
  0.90 in 0 of 160 seeds, at about 5 times the episode evaluations, but on task seed 1 only. The
  method comparison becomes a result with package M on the same task seeds (RUNBOOK; moved to
  601 to 608, where the frozen default was counted).
- The ablation recount does not change its reading above: no component shown at 8 seeds against
  `full`; post hoc, `basic_mut` 0/8 against `no_const_tune` 4/8 (p = 0.04).
- Literature to check before the method claim: liveness-safe ("effective") mutations are a known
  device of linear GP (Brameier and Banzhaf 2007, effective mutations and intron detection);
  memetic constant tuning in GP (e.g. Topchy and Punch 2001; Kommenda et al. 2020); MAP-Elites
  (Mouret and Clune 2015). The contribution is their combination and its measured effect here,
  not any of them alone.

Reproducibility of v3.1, checked here: the same seed twice on one machine, and with 16 against 4
threads, gives an identical `best.json` (30k candidates). Across platforms it does not: seed 601
rerun on Linux, with dumps made by this repository's binary (equal to the PC's up to the last float32
bit), ends at validation 0.699 against 0.994 on the PC, after 30.1M against 21.7M episode
evaluations. The search is chaotic in last-bit differences (input dumps or `tanh`/`exp`), so a
single seed's outcome is a draw and only rates carry meaning; a committed seed reproduces on its own
platform, as CLAUDE.md allows, once its dumps are committed (the per-seed dumps of 601 to 616 and
701 to 708 are not in the repository yet).

The growth loop's remaining `A2` runs (second version, without taps) were stopped on the owner's
decision of 21 Nov; finished: task seed 1 only, the others partial (logs in `runs/grow2/`). The
comparison "taps matter" of the second version stays unmeasured; the line is closed.

### Memetic search: confirmation on 16 fresh task seeds, recounted here (21 Nov 2026)

Design as fixed in this README before the run ("Ablation ... audited result"): the variant
`--no-const-tune` of v3.1, its two single-component knockouts, 16 fresh task seeds (801 to 816),
22M episode evaluations per run, one-sided Fisher at α = 0.05. Protocol and audits from the PC in
`v2/runs/confirm_801_816/` (commit 159132b, merged); binary source unchanged since 71d7948.
Recount here with this repository's Rust binary and JAX, by the reading fixed before (test > 0.90,
T128 K8 ≥ 0.838, train − test ≤ 0.03, long probe below 100 in all nine draws, ε within 0.02):

| arm (task seeds 801 to 816) | count | test ≥ 0.99 | on 801 to 808 | PC audit |
|---|---|---|---|---|
| `frozen` (`--no-const-tune`) | **8/16** | 5 | 5/8 | 8/16 |
| `frozen_basic_mut` (liveness-safe mutations off) | **0/16** | 0 | 0/8 | 0/16 |
| `frozen_no_archive` (state-class archive off) | **0/16** | 0 | 0/8 | 0/16 |

- Both pre-registered tests are met: `frozen` above `frozen_basic_mut`, p = 0.0012, and above
  `frozen_no_archive`, p = 0.0012 (Bonferroni over the two, 0.0024). On fresh task seeds, with the
  variant fixed first, the liveness-safe structural mutations and the state-class archive are each
  necessary for the effect. This is the first component result of the project shown on held-out
  task seeds at the level of the best rule.
- The 8 counted rules reach 0.960 to 0.999 on the collision3 test; JAX float32 and float64 at ε 1e-9
  agree to the fourth digit for all 8; 7 of 8 use no Recip. Seed 805 holds the long probe at 50.5
  (thin margin); seeds 809 and 814 (test 0.998, 0.989) diverge on it and are not counted.
- The level: the classical reference reaches 1.000 here, so the found rules tie it at best. This is
  a method result (finding the best rule of the regime from the empty program), not a discovery.
- Against the evolutionary search the comparison is still unmatched (0/160 above 0.90, task seed 1
  only). Package M (RUNBOOK) is moved to task seeds 801 to 808, where `frozen` counted 5 of 8.

**Freeze (CLAUDE.md item 4).** The search method is frozen as memetic MAP-Elites v3.1 with
`--no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015`, source `v2/memetic/src/main.rs`
at commit 71d7948. No change to mutations, selection or hyperparameters may be tuned on testbed 2.
The task, ops and reading of testbed 2 go into README before any run on it.

## Testbed 2: optimizer update rules (fixed 21 Nov 2026, before any implementation or run)

Purpose (CLAUDE.md item 5): a held-out target for the frozen method. Nothing of the search method
changes; what changes is the task, its objective, two generic ops and the register convention.
Owner's go of 21 Nov. The research agent writes the task generator, dump, evaluation and the
hand-written ladder in this repository's Rust binary and JAX; the memetic binary reads the dumps,
as for collision3, so both implementations see the same data and the counted numbers come from an
implementation the search did not use.

**Program interface.** One step of an optimizer: on entry V0 = w (parameters, dimension d) and
V1 = g (a stochastic gradient at w); the program's output is V0 at the end of the step. State
budget: persistent vectors V2 and V3 (zero at the start of an episode) and the persistent matrix M0
(zero at the start); everything else is temporary. 24 instructions, NM 4, NV 6, NS 4, the 20 ops of
the collision3 space plus two generic element-wise ops, logged here before use:
`VecRecip` (x / (x² + 1e-6), element-wise, the vector form of `Recip`) and `VecSqrt` (√|x|,
element-wise). The empty program is w' = w. No op or mutation knows of momentum, second moments,
bias correction or any optimizer.

**Task family (train).** d = 16, T = 50 steps per episode, w₀ and the optimum w* drawn so that
‖w₀ − w*‖ = 1. Two kinds of problem, half of the episodes each:
- quadratic: f(w) = ½ (w − w*)ᵀ A (w − w*), A = Q diag(λ) Qᵀ with eigenvalues log-uniform in [1/κ, 1];
  Q = I in half of these episodes (axis-aligned) and a random rotation in the other half; gradient
  g = A (w − w*) + σ ξ, ξ ~ N(0, I/d);
- linear regression: n = 64 rows, features with covariance of the same spectrum, targets
  y = X w* + 0.1 noise, f the full-batch mean squared error over 2, g the gradient on a minibatch
  of 8 rows drawn per step.
κ ∈ {10, 100} and σ ∈ {0, 0.1}, balanced over episodes; 128 train episodes per task seed; validation
dumps from task seed 2000 + t as for collision3. Episode objective: log₁₀(f(w_T) / f(w₀)), clipped to
[−10, 3], and 3 for an episode whose w leaves |wᵢ| < 1e4 or becomes non-finite. The search
minimises the mean over episodes (in place of the MSE of collision3), plus the frozen 0.015 ·
mean(state²) and the length tie-break.

**Held-out suites** (fixed seed 99, 512 episodes each, never loaded by a search): (1) the train
distribution; (2) κ = 1000; (3) d = 32; (4) d = 8; (5) σ = 0.3; (6) T = 200; (7) the gradient and the
loss scaled by 10 and by 0.1 (half each). Reported per suite: mean objective and the fraction of
diverged episodes.

**References, hand-written, tuned on the train task by grid** (rule 6: references only): SGD (η),
momentum (η, β), RMSProp (η, β, ε), Adam (η, β₁, β₂, ε; without bias correction, which needs a step
counter the program does not get), and for the ceiling, not expressible in the space: exact Newton
w' = w − A⁻¹ g on the quadratics and the least-squares solution on regression, plus conjugate
gradients on noise-free quadratics. Every number is reported next to tuned Adam and the ceiling.

**Structural test.** A found rule is run on train episodes; each ladder member, with its constants
fitted by least squares to the rule's own per-step updates Δw on the same gradient sequences, is
scored by R². The rule is assigned to the simplest member with R² ≥ 0.95 (SGD < momentum < RMSProp <
Adam), otherwise "unclassified". Accuracy levels alone do not count as rediscovery.

**What is counted** (task seeds 901 to 916, one search seed each, the frozen method unchanged at
22M episode evaluations):
- Level: a seed reaches the Adam level if its rule's mean objective on suite (1) is at most that of
  tuned Adam plus 0.05, no episode diverges on any suite including T = 200, and train − suite (1) is
  at most 0.1.
- Rediscovery: the structural class of each rule; counted separately for momentum, RMSProp and
  Adam.
- Baseline searches on the same task seeds and episode-evaluation budget: the plain evolutionary
  search of this repository (regularized evolution as in AutoML-Zero; the executing agent, epyc) and
  random search. Method result: memetic against plain evolution on the level count, one-sided
  Fisher, α = 0.05.
- Degenerate wins (rule 3): divergence at T = 200, dependence on the scale suite (7), train ≫ test.
  A rule better than tuned Adam is a candidate only; it needs the full rule-2 analogue (ladder
  retuned per suite, ceiling, JAX, a rate over 8 or more seeds) and a literature check before
  anything is claimed.

**Neighbours to cite and check** (search again before any claim): symbolic optimizer discovery by
program search, Lion (Chen et al. 2023, "Symbolic Discovery of Optimization Algorithms"); Neural
Optimizer Search (Bello et al. 2017; PowerSign, AddSign); learned optimizers (VeLO and others).
Lion was found by evolutionary program search with a funnel of proxy tasks, the closest precedent
of this testbed; the claim here can only be about the search method on a fixed space and budget.

**Predictions of the research agent:** the frozen method reaches the Adam level in 8 or more of 16
with probability 0.35; plain evolution does so with 0.15; the method result (p < 0.05) with 0.35;
momentum is rediscovered in 8 or more of 16 with 0.6.

### Testbed 2: implementation in this repository (21 Nov 2026, before any counted run)

Built by the research agent, as fixed above. Changes to the space and the code (rule 1):
- Two generic ops, only with `--opt-ops`: `VecRecip` (x / (x² + 1e-6) element-wise) and `VecSqrt`
  (√|x| element-wise). Without the flag the alphabet is unchanged.
- `--task opt` (`src/opt.rs`): generator, loss, gradients, objective, held-out suites, ceiling.
  Under it the output of a step is V0, so dead-code removal (`effective()`) keeps what reaches V0;
  M0 is then state like any persistent register. `--persist-v 2` gives V2 and V3.
- The memory search is unchanged: the self-check of `d-kalman` seed 9 gives the same 50,036-
  candidate row as before (`50036,19778,…,0.50570,0.5094,12,0.3803`).

Commands: `autoplast dump --task opt --split train --task-seed N [--train-episodes 192]`,
`dump --task opt --split test --suite 1..7`, `eval --task opt --opt-ops --prog rule.json` (train and
the seven suites), `evalmany --task opt --opt-ops --persist-v 2 [--split test --suite N]`,
`ceiling --task opt`, and `search --task opt --opt-ops --persist-v 2` (the plain evolutionary search
on testbed 2; the validation log, the memory-rule milestones and the memory classifier are off).

The ladder, tuned by grid on the train task of task seed 1 (`verify/probe_opt.py`,
`runs/sweeps/probe_opt.md`; no best value on the edge of its grid; mean log₁₀(f_T / f₀), lower is
better):

| rule | parameters | train | suite 1 | κ 1000 | d 32 | d 8 | σ 0.3 | T 200 | scale ×10 / ×0.1 |
|---|---|---|---|---|---|---|---|---|---|
| SGD | η 1 | −2.013 | −2.072 | −1.437 | −1.018 (4% div.) | −2.206 | −0.957 | −2.762 | 0.927 (50% div.) |
| momentum | η 0.5, β 0.6 | −2.614 | −2.638 | −1.485 | −2.012 | −2.694 | −1.009 | −2.910 | 0.869 (50% div.) |
| RMSProp | η 0.02, β₂ 0.99 | −2.717 | −2.679 | −1.588 | −2.376 | −2.726 | −1.279 | −2.634 | −2.512 |
| Adam | η 0.03, β₁ 0.6, β₂ 0.99 | −3.130 | −3.073 | −1.621 | −2.980 | −3.129 | −1.208 | −3.406 | −2.814 |
| optimum (ceiling) | | −5.79 | −5.81 | −5.67 | −5.90 | −5.77 | −5.81 | −5.81 | −5.81 |

The ladder is strictly ordered on the train task, and SGD and momentum diverge under the ×10
gradient scale where RMSProp and Adam do not, as they should. Adam (17 instructions) fits the 24.
One deviation from the plan above: Newton steps with the exact Hessian on the stochastic gradients
are no ceiling (−1.13 on train, worse than SGD: the inverse Hessian amplifies the gradient noise),
so the ceiling reported is the optimum itself (w* on the quadratics, the least-squares solution on
regression); Newton is kept in the probe output for reference. The Adam level of the counted
criterion is −3.073 on suite 1 (so a rule must reach −3.023 or lower).

Checks: `verify/verify_opt.py` re-implements machine and episodes in numpy and reads the Rust dumps;
on suites 1 and 7 the four ladder rules agree with Rust within 4e-5 (float64) and 1e-4 (float32).
`verify/opt_structure.py` (structural test) assigns each ladder rule to its own family with R² =
1.000. Smoke test, not counted: the plain search, 20k candidates on task seed 1, finds an SGD-like
rule (w − tanh²¹(g), structural class SGD, R² 0.961) at −2.106 on train.

For the memetic binary (owner's PC): read the dumps (`dump --task opt`, keys `task, d, t, seed,
episodes[{kind, kappa, sigma, rotated, scale, f0, w0, wstar, a, noise | x, y, batch}]`), apply the
register convention and the two ops exactly as `src/opt.rs` and `verify/verify_opt.py`, minimise
the mean episode objective in place of the MSE (state penalty and length tie-break as frozen),
and nothing else. Counted runs: task seeds 901 to 916, train dumps of task seed t, validation dumps
of task seed 2000 + t with 192 episodes, one search seed per task seed, 22M episode evaluations,
`--no-const-tune`. The counted numbers are taken from this repository's binary
(`eval --task opt`) and the structural test.

## Packages M and N and testbed 2: results and reading (24 Nov 2026)

Merged: the executing agent's packages M (`runs/m-plain`, `runs/m-lexicase`, commit dce11aa, epyc)
and N (`runs/n-plain`, `runs/n-random`), and the memetic search on testbed 2 from the owner's
collaborator (`v2/runs/testbed2_901_916`, commits ec5c13f adapter, b0dac36 protocol, 5774c44
checkpointing, bea07f2 results). Recounted here with this repository's binary; the memetic rules
were evaluated afresh (`eval --task opt` on each task seed) and agree with the PC's numbers to the
printed digit; the counted ones agree with the numpy re-implementation on suite 1.

### Collision3, matched task seeds 801 to 808 (package M)

| arm (1.5M candidates, or 22M episode evaluations) | count (test > 0.90 with the conditions) | best test |
|---|---|---|
| frozen memetic search (confirmation run) | **5/8** | 0.999 |
| plain evolution (`m-plain`) | 0/8 | 0.643 |
| lexicase (`m-lexicase`) | 0/8 | 0.693 |

The method result on matched tasks: 5/8 against 0/8 for each evolutionary arm, one-sided Fisher
p = 0.013 each (0.0013 against both pooled, not fixed before). The evolutionary arms spent about
0.78M real evaluations × 144 episodes (about 110M episode evaluations), 5 times the memetic arm.
Five of eight `m-plain` seeds end below 0.53 (stuck), as on task seed 1. Predictions: the research
agent's (0/8 with 0.85, 0/8 with 0.8) right.

### Testbed 2, task seeds 901 to 916 (memetic search and package N)

Adam level as fixed: suite 1 at most −3.023, no divergence on train or any of the seven suites,
and the train/test gap at most 0.1.

| arm | suite 1 ≤ −3.023 | no divergence anywhere | Adam level, gap read as test worse than train (S1 − train ≤ 0.1) | Adam level, gap as literally written (train − S1 ≤ 0.1) | structural class |
|---|---|---|---|---|---|
| frozen memetic search (22.1M episode evaluations) | **15/16** | 5/16 | **4/16** (905, 910, 913, 915) | 5/16 (+ 908, gap 0.114) | SGD 2, unclassified 14 |
| plain evolution (`n-plain`, 26.3M) | 0/16 | 16/16 | 0/16 | 0/16 | SGD 8, momentum 1, unclassified 7 |
| random search (`n-random`, 21.1M) | 0/16 | 16/16 | 0/16 | 0/16 | SGD 14, unclassified 2 |

**A defect in the criterion, the research agent's.** The text fixed before the run reads "train −
suite (1) is at most 0.1", copied from the accuracy criterion where higher is better. Here lower is
better, so the written condition only fails when train is worse than test and does not check
overfitting at all; the intended check is S1 − train ≤ 0.1. Seed 908 (train −3.412, suite 1 −3.298)
separates the two readings. Both are reported, and the stricter one is the one used for claims:
- strict reading: 4/16 against 0/16 for plain evolution, one-sided Fisher **p = 0.051**: the fixed
  method result (α = 0.05) is **not met**, by the smallest margin;
- literal reading: 5/16 against 0/16, p = 0.022, met;
- against plain evolution and random search pooled (0/32, not fixed before): p = 0.009 (strict).

Reading:
- The frozen method transfers in level: 15 of 16 rules beat tuned Adam on the train distribution
  (median −3.30 against −3.07), where plain evolution and random search reach at most the level of
  momentum (best −2.647). It does not transfer in robustness: 10 of the 15 diverge on a held-out
  suite, mostly the gradient scale ×10 (10 of 16) and d = 32 (8 of 16). Rules that adapt to the train
  distribution's gradient scale instead of normalising it are the failure (rule 3, scale dependence).
- Even the four counted rules are below Adam on the scale suite (−0.41 to −1.26 against −2.81) and
  three of them on d = 32. They are better in distribution and worse under shift; no "better than
  Adam" can be said, and none is a different rule of equal accuracy across the suites.
- No rule of the memetic search is structurally momentum, RMSProp or Adam (0/16); 14 are unclassified.
  Rediscovery of the ladder is not shown on testbed 2; plain evolution rediscovered momentum once.
- Predictions of the research agent: Adam level in 8 or more of 16 (0.35) no; plain evolution 8 or
  more (0.15) no; method result at p < 0.05 (0.35) no under the strict reading; momentum rediscovered
  in 8 or more (0.6) no.

What the two testbeds together support: the frozen memetic search reaches the best rule of
collision3 where evolution does not (5/8 against 0/8 on matched tasks, 8/16 confirmed with both
components necessary), and on a held-out testbed it reaches a level no baseline reaches (15/16
against 0/32 on suite 1) but mostly with rules that break under distribution shift. A transfer
claim at the fixed bar is not shown (p = 0.051).
