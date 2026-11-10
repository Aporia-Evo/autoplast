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

20 operations: `Outer, MatAdd, MatSub, MatScale, Transpose, MatMul, MatVec, VecAdd, VecSub,
VecScale, Hadamard, Normalize, Tanh, Dot, Const, SAdd, SMul, Sigmoid, Norm, Recip`.
`Recip` (scalar `x/(x²+1e-6)`) was added on 10 Nov 2026; `--no-recip` gives the 19-op space of
runs v1 and v2. State budget: `--persist-m N` keeps `M0..M{N-1}` from one write step to the
next, `--persist-v N` keeps `V2..V{1+N}`; all other registers are zeroed before every step.
The default (1, 0) is the v1/v2 space, where a rule is a function of (S, k, v) only.

Readout is identical for every rule: `o = S q`, decoded to the closest value embedding.
No rule family is built in. Linear attention, the delta rule and gated variants are just
particular programs in this space (`program::baselines()`), the same as any other.

## Task

Multi-query associative recall with overwrites: 12 writes per episode into an empty memory,
d = 16, 64 keys and 64 values as fixed random unit vectors. With probability 0.3 a write
reuses an earlier key with a new value. Every key is queried at the end; the target is its
latest value. Fitness = accuracy + 0.05 · mean margin − 1e-4 · program length.

Held-out tests use fresh embeddings and episodes, other overwrite rates and other sizes
(d = 32 / T = 24, d = 8 / T = 6) the search never saw, plus six regime suites that shift
load, episode length, rewrite pressure and key similarity (`--regime`, see "Steps 1 to 3").

## Search

Regularized (aging) evolution as in AutoML-Zero: population 500, tournament 10, the whole
population starts as the empty program (`S' = S`, accuracy 0). Mutations insert, delete,
replace or rewire one instruction or perturb a constant. Programs with identical effective
code share a cached score.

## Verification

`verify/verify.py` re-implements the interpreter in JAX with its own episodes and RNG and
prints every accuracy with its 95% interval. It repeats the structural test of
`src/classify.rs`: least squares of the update on four terms,
`a·S + b·(v kᵀ) + c·((S k) kᵀ) + g·((vᵀS k)·v kᵀ)`, on memory states from real episodes.
Linear attention is (1, b, 0, 0); the delta rule with step e is (1, w, −e, 0).

## Usage

Repository: github.com/Aporia-Evo/autoplast. Agent instructions: CLAUDE.md.

```bash
cargo build --release
./target/release/autoplast baselines
./target/release/autoplast search --seed 1 --budget 3000000 --out runs/seed1
./target/release/autoplast eval --prog runs/seed1/best.json
python verify/verify.py runs/seed1/best.json     # needs jax, numpy
./target/release/autoplast sweep --regime rewrite8 --train-episodes 192   # tuned families + ceiling
./target/release/autoplast search --seed 1 --regime clustered --train-episodes 192 --persist-m 2

# many seeds on one machine; RUNBOOK.md says which machine runs what
python local_runner.py --seeds 1-8 --budget 1500000 --tag v3 --jobs 2 --threads 4
python aggregate.py runs/v3

# many seeds on Modal (CPU containers), results copied to runs/<tag>/
modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3
modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3-noaddnode --no-split-edge
```

## Reference rules (from `baselines`)

| rule | train | test ow0.3 | test ow0.0 | test ow0.6 | test d32 T24 | test d8 T6 |
|---|---|---|---|---|---|---|
| no write (start of search) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| linear attention | 0.778 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 |
| delta rule β=1 | 0.872 | 0.862 | 0.788 | 0.922 | 0.948 | 0.744 |
| delta rule β=0.5 | 0.935 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 |
| gated delta α=0.9 | 0.751 | 0.714 | 0.620 | 0.837 | 0.639 | 0.685 |

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

## Review and scope correction (10 Nov 2026)

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

### Tuned baselines per regime (`runs/sweeps/*.md`)

Each row: families tuned on 192 train episodes of that regime, accuracy on that regime's
held-out suite. Parameters are in the sweep files. Standard error about 0.005 to 0.01.

| regime | lin. att. | decayed LA | DeltaNet | Gated DeltaNet | Kronecker | gated Kronecker | RLS (2 states) | Kalman delta (2 states) | ridge ceiling |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.750 | 0.790 | 0.924 | 0.969 | 0.765 | 0.808 | 0.835 | 0.999 | 1.000 |
| full | 0.553 | 0.588 | 0.751 | 0.820 | 0.598 | 0.623 | 0.825 | 0.946 | 0.997 |
| overload | 0.342 | 0.381 | 0.502 | 0.530 | 0.342 | 0.387 | 0.549 | 0.591 | 0.750 |
| rewrite8 | 0.080 | 0.574 | 0.869 | 0.869 | 0.077 | 0.598 | 0.079 | 0.952 | 1.000 |
| rewrite14 | 0.107 | 0.462 | 0.701 | 0.701 | 0.103 | 0.476 | 0.165 | 0.840 | 1.000 |
| clustered | 0.141 | 0.172 | 0.224 | 0.402 | 0.140 | 0.185 | 0.844 | 0.960 | 1.000 |
| clustered8 | 0.045 | 0.165 | 0.201 | 0.201 | 0.045 | 0.182 | 0.202 | 0.689 | 1.000 |

Reading: the Rust numbers agree with the NumPy probe above. Best one-state family against the
ceiling: 0.87 vs 1.00 (`rewrite8`), 0.70 vs 1.00 (`rewrite14`), 0.82 vs 1.00 (`full`), 0.40 vs
1.00 (`clustered`). These are the bars a one-state search result has to clear; Kalman delta is
the bar for two states. The Kronecker delta rule is weak here, which is expected: it stores a
scalar score per pair and is not built for the vector readout `S q` this task fixes. Limits:
λ for Kalman delta and ridge sits at the lower grid edge (1e-4), and the clustered optimum for
Gated DeltaNet has a = 1.25, which will not survive longer episodes.
