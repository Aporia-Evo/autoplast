# autoplast: agent brief

You are the research agent on autoplast. Read README.md first; it holds the method and every
result so far. This file says what the project is after, the rules that keep results honest,
and what to do next.

## Goal

Find a memory update rule that is genuinely new and better than tuned Gated DeltaNet in a
clearly defined regime, discovered by gradient-free evolution from an empty program, with
no LLM-written or hand-designed rule in the loop. Target venue: a main ML conference
(NeurIPS / ICLR / ICML), so every claim must survive a hostile reviewer.

Stages:
1. Rediscovery (done once): the search assembles the delta family from nothing. Needs a rate.
2. Discovery: point the search at regimes where tuned Gated DeltaNet fails.
3. Transfer: put the best rule into a small language model (~125M params) vs Gated DeltaNet.

## Non-negotiable rules

1. No hardcoding. Do not add instructions or mutations that encode a known rule (no
   "delta op", no "gate op", no initial population seeded with known rules). Generic ops
   and generic graph mutations are fine. Every change to the search space, mutations or
   fitness goes into README with the reason, before results that depend on it.
2. No claim of "better" without all of:
   - `autoplast sweep` (or an extended sweep) tuning the known families on the same train
     task, compared on the held-out suites;
   - `verify/verify.py` reproducing the accuracy in JAX within noise;
   - a rate over at least 8 seeds, not a single lucky seed.
3. Check for degenerate wins: overfitting the fixed train episodes (train ≫ test),
   scale-invariance tricks (argmax decoding ignores global scale of S), and growth
   factors > 1 that only work because episodes are short.
4. Report negatives as faithfully as positives. A seed that finds nothing is data.
5. Literature check before calling anything new. Known neighbours: DeltaNet, Gated
   DeltaNet, Kronecker Delta Rule (NXAI, Oct 2026), Erase-then-Delta (Jun 2026), NTM
   erase/add, Titans (surprise-gated memory), Modular TTT, Memory Mosaics.

## Compute

Decision (3 Nov 2026): Modal is for GPU runs only. All CPU work, including multi-seed
search fan-outs, runs locally on the Ryzen 5700G (8 cores, 16 threads), because CPU
containers on Modal spend limited credits on work the local machine can do. Do not launch
`modal_runner.py` for CPU searches; it stays in the repo only as a reference.
Before any local launch larger than 8 seeds, run 2 seeds with a small budget, measure wall
time, and state the expected total hours on the local machine. Any GPU run on Modal needs
explicit approval first.

## Next experiments, in order

1. Rediscovery rate: seeds 1-16, `--budget 1500000`, tag `v2`, run locally with
   `autoplast search` (see Compute).
   Report how many seeds reach the delta milestones and the median candidates.
2. Ablation: same seeds locally with `--no-split-edge`, tag `v2-noaddnode`. Does the NEAT-style
   add-node mutation actually matter? (It looked decisive, but that was 1 vs 2 seeds.)
3. Task fixes before stage 2: long episodes (T = 64 and more) so growth factors > 1 are
   punished; resample or enlarge train episodes; keep the held-out suites.
4. Gate analysis: the 3-term least-squares decomposition in verify.py saturates on random
   S and cannot see state-dependent gates (seed 1 of v2). Add an analysis on realistic
   memory states taken from actual episodes.
5. Stage 2 regimes where tuned Gated DeltaNet is weak: high key collision (clustered keys,
   cos > 0.8), capacity overload (writes > d), noisy keys at query time, long gaps.
   First measure the tuned baselines there, then search.
6. Literature check of the occupancy-gated write found by v2 seed 1:
   `S' = S + σ(‖S k̃‖⁴)·v kᵀ`.

## Working style

Keep runs reproducible: seed, budget, flags and git commit in every summary. Commit small,
with results and the README update in the same commit. Write short, plain summaries of what
ran, what came out, and what it means.
