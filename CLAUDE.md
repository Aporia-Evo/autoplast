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
same day (README, "Merge"). State of the method claim: the add-node mutation and constant
tuning show no effect; parent selection by behaviour (`--select share`, `--select lexicase`)
removes the seeds that stop at linear attention on the base task (package H, 15 Nov), and
the plain search does not catch up with more wall time (package I, 17 Nov). Package J (19 Nov)
shows the same on collision3 in the space of D and E, wall-time control pending (package K).
Down-sampled tournaments do not explain it (package L, 19 Nov, base task).
Constant tuning is closed as a negative result (packages F and G).

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
   (Sep 2026, arXiv 2609.07816), Gated KalmaNet (arXiv 2511.21016), Kalman Linear Attention
   (Feb 2026), Momentum DeltaNet (May 2026), OSDN (May 2026), Kronecker Delta Rule (NXAI,
   Oct 2026), Dual DeltaNet (not found in a search on 19 Nov), Muir, RWKV-7, Longhorn,
   MesaNet, NTM erase/add, Titans, Modular TTT, Memory Mosaics. Method neighbours:
   AutoML-Zero, ASI-Arch (LLM-driven, starts from DeltaNet). Selection by behaviour is not
   new: fitness sharing (Goldberg and Richardson 1987; in GP: McKay 2000/2001), semantic GP,
   novelty search, MAP-Elites, lexicase (Spector 2012; Helmuth et al.), and down-sampled
   tournaments as its rival (Geiger et al. 2025), Dominated Novelty Search (Bahlous-Boldi
   et al. 2025, arXiv 2502.00593). Evolving learning rules is not new: Chalmers
   1990 evolved the delta rule; Bengio et al. 1994 used GP (README, "Literature check of the
   method components").
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

1. Method improvement. Decided with the owner on 14 Nov 2026: first component is constants
   tuned per structure (`--tune-consts`), second is speciation by behaviour, typed crossover
   is deferred. `--tune-consts`, random search (`--algo random`) and the validation log are
   implemented, off by default (README, "Search method, first change"). Package F (done
   15 Nov; README, "Package F: result and reading"): no detectable effect of tuning on the
   base task (7/16 and 8/16 against 14/32), no cost either; random search never gets past
   linear attention (0/16). Decided with the owner on 15 Nov: both. Second component built:
   parent selection by behaviour, `--select share` (fitness sharing over per-episode
   behaviour) and `--select lexicase` (README, "Search method, second change"). Released:
   package H (base task, 32 seeds, `h-base` / `h-share` / `h-lexicase`) and package G
   (`--tune-consts 8` on collision3 in the space of D and E, 32 seeds). Typed crossover stays
   deferred. Package H done 15 Nov (README, "Package H: result and reading"): with selection
   by behaviour no seed stops at linear attention on the base task (31/31 and 32/32 at the
   delta accuracy level against 12/32, p about 1e-8); not shown on the strict structural
   count; wall time 2 to 2.5 times higher. First component that supports the method claim,
   on one task. Released: package I (plain search at 4M candidates as wall-time control).
   Package G done 16 Nov (README, "Package G: result and reading"): no effect of constant
   tuning in the space of D and E either (rule 2 in 6/32 against 6/32); the component is
   closed. Released on 16 Nov as package J: `--select lexicase`, then `--select share`, on
   collision3 in the space of D and E, 32 seeds each, thresholds of package E (README,
   "Package J"). Package I done 17 Nov (README, "Package I: result and reading"): the plain
   search at 4M candidates and more wall time reaches the delta accuracy level in 24/32,
   against 32/32 for both arms at 1.5M (p = 0.0024); on the structural count it equals
   `share` (22 vs 20) and beats `lexicase` (22 vs 10). `share` is the variant to carry
   forward. A positive J needs a wall-time-matched plain arm in that space before it is
   claimed. Literature check 17 Nov: the method claim has to be framed as a component study,
   not a new algorithm; a down-sampling control (plain tournament on a random subset of train
   episodes per batch) is missing and is the first thing a reviewer asks. Still open: that
   control, and the same arms on task v3. A cache fault found by H is fixed.
   Direction decided by the owner on 17 Nov: aim for a new capability, a search that reaches
   Kalman delta (or its level) from the empty program where the present search never does
   (0/64 above 0.90). The path from delta to Kalman delta is nearly monotone but every step
   needs 3 to 5 specific instructions before it changes fitness (README, "Direction 2").
   Third component built for that barrier: `--residual-insert` (off by default). A package
   follows after J; any success needs a held-out target with the method frozen first.
   Package J arm `j-lexicase` done 18 Nov (README, "Package J, arm j-lexicase"): stuck 0/32
   against 12/32 (criterion met, p = 7e-5, not yet wall-time matched), rule 2 11/32, nothing
   counted above 0.85. Seed 6 (0.893) writes only through the 1e-6 in Normalize, a scale trick
   (rule 3), not counted; its epsilon-free rewrite reaches 0.898. Every arm in this space now
   gets `verify.py --x64 --norm-eps 1e-9` and `verify/eps_scale.py`. `j-share` done 19 Nov
   (README, "Package J, arm j-share"): stuck 0/32, rule 2 11/32, best seed 0.694, below
   lexicase on the median (p = 0.0007). Package J: behaviour selection removes the stuck seeds
   in this space too, raises nothing above 0.85; 0/128 seeds above 0.90 in this space.
   Released 19 Nov as package K (README, "Package K"): `k-ri-lex` (residual insertion with
   lexicase, against `j-lexicase`; main count 2/32 above 0.90) on epyc, and `k-plain2m` (plain
   search at 2.1M, the wall-time control of J; J's stuck effect stands if 5/32 or more stuck)
   on the workstation. A success of `k-ri-lex` needs testbed 2 as held-out target, method frozen.
   Outside review 19 Nov (README, "Outside review of 19 Nov 2026"): the residual insertion of
   17 Nov overwrote live registers (37% of insertions destroyed the rule); corrected before
   any K run (1.9%). Length penalty works against neutral blocks; left as is, noted. Lexicase
   here is lexicase inside a tournament of 10 (a limit of H and J). Down-sampling control built
   (`--select downsample`), released as package L on the base task, before `k-plain2m`.
   Package L done 19 Nov (README, "Package L: result and reading"): down-sampling reaches the
   delta level in 19/32 (h-base 12/32, p = 0.066; lexicase and share 32/32, p = 2.6e-5). The
   effect of H belongs to behaviour-based selection, not to random episode subsets (base task
   only). `k-ri-lex` done 20 Nov (README, "Package K, arm k-ri-lex: result and reading"): main
   count 0/32 above 0.90 (needed 2), 0/32 above 0.85, rule 2 11/32, median as `j-lexicase`
   (p = 0.75); the mutation inserts in 73% of attempts but no rule gains a normalised
   preconditioner. Residual insertion in the evolutionary search is closed as negative.
   `k-plain2m` done 21 Nov (README, "Package K, arm k-plain2m"): 9/32 stuck at 2.1M (criterion
   5/32 met, p = 0.001 against J): J's stuck effect stands at matched wall time.
   clustered8 check 19 Nov (README, "clustered8: a found rule..."): d-kalman seed 9, found on
   collision3, scores 0.860 on clustered8 fresh draws against 0.672 for tuned Kalman delta
   (12/12 draws); one rule of 128. An obvious hand-made fix (key centring + delta rule, one extra
   vector) reaches 0.805, so the regime's headroom is mostly a single key mean. No package yet.
   Owner decision 19 Nov: the method may be gradient-guided (no LLM, no prior rule). Adjoint
   feasibility test done (README, "Feasibility test: result and reading"): next step of the
   measured path ranked first in 3/5 transitions (T2 rank 10, T5 rank 31, whose top candidate
   reaches 0.898 of 0.932). Neither pre-set criterion met; promising, with a known gap (neutral
   pairs such as reading an unchanged P). Closed-loop growth test done 19 Nov (README,
   "Closed-loop growth test: result and reading"): with neutral taps (arm B) the loop reaches
   0.860 test on task seed 1 (partial success, all checks pass) in 2.8k Rust evaluations; without
   (arm A) 0.511. Replicates: B 0.527 / 0.645 / 0.771, A 0.64 to 0.65. Works, not yet reliable:
   greedy, length-bound. Second version (beam 4, compaction; README, "Growth loop, second
   version: result of B2"), task seeds 1 to 8: 0 of 8 at 0.85; the best rules grow P and diverge
   on long episodes (rule 3), 7 of 8. Third version (stability gate, identity kept, stop rule;
   README, "Growth loop, third version: result of B3"), unseen task seeds 10 to 17, done 20 Nov:
   0 of 8 at 0.85 (criterion 3 of 8 not met, not frozen); all eight bounded on long episodes,
   7 of 8 at 0.77 to 0.80 test with a two-state preconditioned erase/write rule (fresh draws 0.78
   to 0.81, DeltaNet 0.643, Kalman delta 0.934), about 8k Rust evaluations per seed. The length
   limit binds (21 to 24 of 24). Post hoc only: test ≥ 0.75 in 7/8 against 1/96 evolutionary
   seeds, on other task seeds. Remaining `A2` seeds run after B3. Next step open with the owner.
   Reference of 21 Nov (README, "A classical rule at the ridge ceiling"): RLS covariance with an
   unregularised write gain (recursive pseudo-inverse memory, 16 instructions, hand-written,
   `verify/probe_olam.py`) reaches the ridge ceiling on collision3 (1.000, every check passed)
   and on 8 more of the 11 regimes. Headroom above it is left only in overload (0.077) and
   overload48 (0.146). It is to be listed next to every number; on solved regimes a search can
   at most tie (method result, not discovery). The memetic MAP-Elites search on the owner's PC
   (`v2/memetic`, not yet in the repository) reached 1.000 on validation in development; its
   counted run (task seeds 1 and 501, 4 seeds each) is read as fixed in that README section.
   Memetic search v3.1 in the repository (`v2/`, merged 21 Nov; README, "Memetic search v3.1 in
   the repository"): deterministic, episode evaluations counted. Frozen default on unseen task
   seeds 601 to 616: 8/16 counted (recounted here, 4 at ≥ 0.99); ablation on 701 to 708 at 22M
   episode evaluations: no component shown at 8 seeds, post hoc the liveness-safe mutations
   carry the effect and constant tuning makes rules unstable. Evolution: 0/160 above 0.90, on task
   seed 1 only, at about 5 times the episode evaluations. Package M (RUNBOOK; plain and lexicase
   on task seeds 601 to 608) makes the comparison matched; awaiting the owner's go.
   v3.1 is deterministic on one machine and across thread counts, not across platforms (seed 601
   on Linux: 0.70 against 0.99): rates carry meaning, single seeds do not. Growth-loop A2 runs
   stopped 21 Nov (owner); the growth-loop line is closed.
   Confirmation 21 Nov (README, "Memetic search: confirmation on 16 fresh task seeds"): v3.1
   `--no-const-tune` on task seeds 801 to 816: 8/16 counted, both knockouts 0/16 (liveness-safe
   mutations, state-class archive; p = 0.0012 each, pre-registered). Method frozen (item 4) at
   71d7948 with these flags. Ties the classical reference (method result, not discovery).
   Package M released 21 Nov (owner). Testbed 2 specified in README before any implementation
   ("Testbed 2: optimizer update rules"); the research agent builds generator, dumps, evaluation,
   ladder and JAX in this repository, the memetic binary reads the dumps. Implemented 21 Nov
   (README, "Testbed 2: implementation in this repository"): `--task opt`, `--opt-ops`; strict
   ladder (Adam −3.073 on suite 1), numpy check within 4e-5, structural test; package N (plain
   and random search, task seeds 901 to 916) prepared in RUNBOOK.
   Results 24 Nov (README, "Packages M and N and testbed 2"): collision3 801 to 808, memetic 5/8
   against plain 0/8 and lexicase 0/8 (p = 0.013 each): method result on matched tasks. Testbed 2,
   901 to 916: memetic reaches suite 1 ≤ −3.023 in 15/16 (plain 0/16, random 0/16) but the counted
   Adam level (no divergence, gap) only in 4/16 under the corrected gap (5/16 literal; the written
   criterion had a sign error); against plain p = 0.051, so the transfer claim at the fixed bar is
   not met. Most found rules break on the gradient-scale and d = 32 suites; no structural rediscovery
   of momentum, RMSProp or Adam (0/16).
   Literature check 24 Nov (README): method claim is a component study of known devices (effective
   mutations of linear GP, MAP-Elites); found collision3 rules sit in the RLS/Kalman family (Kernel
   Ridge Attention, MesaNet, Kalman Delta Networks); nothing claimed as new. Experiment 2a fixed
   24 Nov (README): frozen method on overload (task seeds 1001-1016) and overload48 (1101-1116);
   discovery if 3+/16 seeds beat the best reference (0.878 / 0.603) by 0.02 on test and on fresh draws.
   Amended 24 Nov before any run (outside review): T128 K8 ≥ 0.838 dropped as an exclusion (no
   reference meets it; long probe, JAX and train − test stay); secondary count against references
   that pass T128 K8 (0.820 / 0.565). README also corrects: v2 starts from short random programs,
   has 5% one-point crossover, knockouts switch off bundles, a 0.02 skeleton filter throttles
   constant changes under --no-const-tune.
   Background:
   Decide with the owner what the method improvement is. Evidence to start from: failed seeds
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
