# autoplast: agent brief

You are the research agent on autoplast. Read README.md first; it holds the method and every
result so far. This file says what the project is after, the rules that keep results honest,
and what to do next.

## Goal

The contribution is the search method: an improved NEAT-style evolutionary search over typed
programs, used as a discovery tool. Starting from an empty program, with no LLM-written or
hand-designed solution in the loop, it should find a procedure that is better than or
different from what is known inside a stated search space. Memory update rules are the
testbed, not the product. Target venue: a main ML conference (NeurIPS / ICLR / ICML), so
every claim must survive a hostile reviewer.

Two claims carry the paper:
- Method: the search finds known rules and the best rule of a regime more often and with
  fewer evaluations than other search algorithms on the same space and budget (regularized
  evolution as in AutoML-Zero, random search, and each added component switched off).
- Discovery: in at least one regime with measured headroom it finds a rule that beats every
  tuned known family at the same state budget, or a different rule of equal accuracy.
  Gains are reported against the ridge ceiling (`verify/headroom.py`).

Scope history: corrected on 10 Nov 2026 (README, "Review and scope correction"), then
re-centred on the search method the same day at the owner's direction.

Stages:
1. Rediscovery: the search assembles the delta family from nothing. Needs a rate over seeds
   and a structural test; accuracy milestones do not count as rediscovery. Held-out part:
   does it also reassemble the 2026 rules (decoupled erase/write, preconditioning)?
2. Discovery: regimes with measured headroom (few keys rewritten over long episodes,
   clustered keys, full load), at a stated state budget (one d×d matrix, or two).
3. Transfer of the frozen search method to a second testbed (optimizer update rules).
4. Small trained models (MQAR, learned keys and gates) for the top structures. A language
   model stage is undecided: ask the owner before planning or spending on it.

## Non-negotiable rules

1. No hardcoding. Do not add instructions or mutations that encode a known rule (no
   "delta op", no "gate op", no initial population seeded with known rules). Generic ops
   and generic graph mutations are fine. Every change to the search space, mutations or
   fitness goes into README with the reason, before results that depend on it.
2. No claim of "better" without all of:
   - `autoplast sweep` (or an extended sweep) tuning the known families on the same train
     task, compared on the held-out suites; the families are linear attention, DeltaNet,
     Gated DeltaNet, decoupled erase/write, Kronecker Delta Rule, and at two states RLS and
     Kalman delta;
   - the ridge ceiling for the same regime next to every number;
   - `verify/verify.py` reproducing the accuracy in JAX within noise;
   - a rate over at least 8 seeds, not a single lucky seed.
3. Check for degenerate wins: overfitting the fixed train episodes (train ≫ test),
   scale-invariance tricks (argmax decoding ignores global scale of S), and growth
   factors > 1 that only work because episodes are short.
4. Report negatives as faithfully as positives. A seed that finds nothing is data.
5. Literature check before calling anything new; the field moves monthly, so search again
   each time. Known neighbours: DeltaNet, Gated DeltaNet, Gated DeltaNet-2 (May 2026),
   Erase-then-Delta (Jun 2026), Preconditioned DeltaNet (Apr 2026), Kalman Delta Networks
   (Sep 2026), Kronecker Delta Rule (NXAI, Oct 2026), Dual DeltaNet, Muir, RWKV-7, Longhorn,
   MesaNet, NTM erase/add, Titans, Modular TTT, Memory Mosaics. Method neighbours:
   AutoML-Zero, ASI-Arch (LLM-driven, starts from DeltaNet).
6. Hand-written rules may be used as reference points and headroom probes only. They never
   enter a population, a mutation or the fitness.

## Compute

Modal credits are limited. Use `modal_runner.py` (CPU containers only, 8 CPUs each).
Before any launch larger than 8 seeds, run 2 seeds with a small budget, measure wall time,
and state the expected total container-hours. The local machine is fine for single seeds
and for `sweep` / `verify`.

## Next experiments, in order

Agreed with the owner before launch; items 1 to 3 need no Modal credits. Every search run
from item 4 on is repeated with the baseline search algorithms on the same seeds and budget;
that comparison is the method result.

1. Structural rediscovery test replacing the accuracy milestones: fit a found rule to the
   known families on memory states taken from real episodes (this also fixes the saturating
   decomposition in verify.py). Re-score the three existing runs with it.
2. Task: regimes from `verify/headroom.py` in Rust (long episodes with few rewritten keys,
   clustered keys, full load), train episodes resampled or enlarged, held-out suites that
   shift the load. Extend `sweep` to all baseline families and print the ridge ceiling.
3. Search space, logged in README before any run: persistent registers under a state budget,
   scalar reciprocal.
4. Rediscovery rate on the base task: `modal run modal_runner.py --seeds 1-16 --budget 1500000
   --tag v3`, then the same with `--no-split-edge`. Time 2 seeds first.
5. Stage 2 search per regime and state budget, 8 seeds each.
6. Freeze the search method: commit it with a note in README. No change to mutations,
   selection or hyperparameters after this point may be tuned on testbed 2.
7. Testbed 2, optimizer update rules, as a transfer test of the frozen method. Program gets
   gradient `g` and parameters `w` as vectors and returns new parameters; start is the empty
   program (`w' = w`). Task: small ill-conditioned quadratics and linear regression with noisy
   gradients, about 50 steps per episode, fitness = final loss. Known ladder for the
   structural test: SGD, momentum, RMSProp, Adam. Ceiling: Newton step / conjugate gradients.
   Held-out: other condition numbers, dimensions and noise levels. Needs a new task file,
   the persistent registers from item 3, and two generic ops (element-wise reciprocal and
   square root), logged in README before any run. Report discovery rate and evaluations
   against the baseline search algorithms; do not promise a new optimizer.
8. Literature check of anything that survives, including the occupancy-gated write of v2
   seed 1: `S' = S + σ(‖S k̃‖⁴)·v kᵀ` (weak as a rule; its signal ‖S k‖² is the interesting part).

## Working style

Keep runs reproducible: seed, budget, flags and git commit in every summary. Commit small,
with results and the README update in the same commit. Write short, plain summaries of what
ran, what came out, and what it means.
