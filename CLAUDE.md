# autoplast: agent brief

You are the research agent on autoplast. Read README.md first; it holds the method and every
result so far. This file says what the project is after, the rules that keep results honest,
and what to do next.

## Goal

Find, by gradient-free evolution from an empty program, a memory update rule that beats every
tuned known rule family with the same state budget in a clearly defined regime, with no
LLM-written or hand-designed rule in the loop. Report gains as the share of the gap to the
ridge ceiling (`verify/headroom.py`), not only against one baseline. Target venue: a main ML
conference (NeurIPS / ICLR / ICML), so every claim must survive a hostile reviewer.

Scope was corrected on 10 Nov 2026 (README, "Review and scope correction"): tuned Gated
DeltaNet alone is no longer the bar, and the base task has almost no headroom.

Stages:
1. Rediscovery: the search assembles the delta family from nothing. Needs a rate over seeds
   and a structural test; accuracy milestones do not count as rediscovery. Held-out part:
   does it also reassemble the 2026 rules (decoupled erase/write, preconditioning)?
2. Discovery: regimes with measured headroom (few keys rewritten over long episodes,
   clustered keys, full load), at a stated state budget (one d×d matrix, or two).
3. Small trained models (MQAR, learned keys and gates) for the top structures. A language
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

Agreed with the owner before launch; items 1 to 3 need no Modal credits.

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
6. Literature check of anything that survives, including the occupancy-gated write of v2
   seed 1: `S' = S + σ(‖S k̃‖⁴)·v kᵀ` (weak as a rule; its signal ‖S k‖² is the interesting part).

## Working style

Keep runs reproducible: seed, budget, flags and git commit in every summary. Commit small,
with results and the README update in the same commit. Write short, plain summaries of what
ran, what came out, and what it means.
