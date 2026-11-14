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
re-centred on the search method the same day at the owner's direction. Branches merged the
same day (README, "Merge"). State of the method claim: the add-node mutation has no effect
in 64 runs, so no component supports it yet.

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

Decision of 3 Nov 2026, still valid: Modal is for GPU runs only and needs explicit approval
(30 USD of credits). All CPU work, including multi-seed searches, runs on the owner's
workstation (Ryzen 5700G, 8 cores, 16 threads; GTX 1660 Super) and, when reachable, on a
university 8-core EPYC. `modal_runner.py` stays in the repo as a reference and is not used.
Runs are carried out by an executing agent following `RUNBOOK.md`; keep that file current when
a work package is released. Before any launch larger than 8 seeds, run 2 seeds with a small
budget, measure wall time, and state the expected total. A committed seed reproduces on its
own platform; Windows and Linux can differ in the last bit of `tanh` / `exp`.

## Next experiments, in order

Done so far (details and numbers in README):
- Rediscovery rate on the base task (v2, base-recip) and add-node ablation: 5 to 6 of 16,
  no effect of add-node.
- Task v3 with long episodes: 11 to 12 of 16, growth factor 1.
- Alphabet sensitivity (3a): rate depends on the alphabet.
- Stage-2 regimes with tuned baselines, least-squares reference, ridge ceiling and two-state
  references (`runs/sweeps/`).
- Evolved readout and extra ops on collision3 (5a): no arm better, no rule above tuned DeltaNet.
- Structural rediscovery test, state budget (`--persist-m`, `--persist-v`), `--recip`.
- Package C arm C1: second state on collision3, rules above every one-state family in 3/16.
- Packages D and E: space containing Kalman delta, 32 seeds; one seed finds an orthogonalising
  memory at 0.86, Kalman delta is not reached, rule 2 in 6/32.

Open, in order. Items 2 to 4 are repeated with the baseline search algorithms on the same
seeds and budget; that comparison is the method result. Item 3 was released ahead of item 1
by the owner on 10 Nov 2026; it changes the search space, not the search algorithm.

1. Decide with the owner what the method improvement is. Evidence to start from: failed seeds
   stop at linear attention; candidates to the delta rule vary by a factor of 20 between seeds.
   Candidates discussed: tune constants per structure instead of mutating them one at a time,
   speciation by behaviour, typed crossover. Implement random search as a baseline.
   Every change goes into README before results (rule 1). The benchmark for it now exists
   (item 3). Controls any comparison needs: the present search with a larger budget (12 of 32
   seeds were still improving after 1.0M candidates) and random search. The search should
   also log when a rule first passes rule 2 on a held-out set, so candidates-to-level can be
   compared; that is a logging change, not a search change.
2. Measure the method on task v3 and the base task against regularized evolution, 16 seeds,
   with the structural test and the accuracy level side by side.
3. Search with a second state. Arm C1 done (README, "Package C, arm C1"): 3 of 16 seeds
   pass rule 2 on collision3 and use the second state; none is near Kalman delta, so the
   discovery claim is not met. Since 11 Nov the Kalman delta rule is expressible
   (`--persist-m 3 --persist-init identity --recip`, 15 instructions, collision3 test 0.933;
   README, "A known target"). Released on 11 Nov 2026 as package D (RUNBOOK.md; README,
   "Package D"). Done on 13 Nov (README, "Package D: result and reading"): main count 1/16.
   Seed 9 is a decayed Hebbian memory on keys orthogonalised by a projector state, 0.864 on
   fresh draws against 0.643 for tuned DeltaNet and 0.934 for Kalman delta; an old idea
   (novelty filter), found from the empty program. Kalman delta itself was not reached. The
   run is the baseline arm for item 1: 1/16 above 0.85, 2/16 above 0.695, 4/16 pass rule 2.
   Package E (seeds 17 to 32, done 14 Nov) found no second such rule. Baseline arm over
   32 seeds (README, "Package E"): rule 2 in 6/32, stuck at decayed linear attention in
   12/32, test > 0.85 in 1/32. A new search arm on the same 32 seeds needs about 13/32 on
   rule 2 or at most 5/32 stuck to show at p < 0.05. Arm C2 of package C is withdrawn.
4. Freeze the search method: commit it with a note in README. No change to mutations,
   selection or hyperparameters after this point may be tuned on testbed 2.
5. Testbed 2, optimizer update rules, as a transfer test of the frozen method. Program gets
   gradient `g` and parameters `w` as vectors and returns new parameters; start is the empty
   program (`w' = w`). Task: small ill-conditioned quadratics and linear regression with noisy
   gradients, about 50 steps per episode, fitness = final loss. Known ladder for the
   structural test: SGD, momentum, RMSProp, Adam. Ceiling: Newton step / conjugate gradients.
   Held-out: other condition numbers, dimensions and noise levels. Needs a new task file,
   the persistent registers, and two generic ops (element-wise reciprocal and square root),
   logged in README before any run. Report discovery rate and evaluations against the
   baseline search algorithms; do not promise a new optimizer.
6. Literature check of anything that survives, including the state-gated writes of v2 seed 1
   (`S' = S + σ(‖S k̃‖⁴)·v kᵀ`) and v2-noaddnode seed 4 (`S' = 1.111·S + σ(‖S k‖²)·(v − S k)⊗k`).

## Working style

Keep runs reproducible: seed, budget, flags and git commit in every summary. Commit small,
with results and the README update in the same commit. Write short, plain summaries of what
ran, what came out, and what it means.
