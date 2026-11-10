# 3a alphabet sensitivity: prediction (written before any run)

Time: 2026-11-04 05:12 UTC. Code: ff3b76c plus uncommitted v3 task option and alphabet switches (README
"Alphabet-sensitivity switches"); git.exe still blocked. Reference: runs/v3 (12/16 delta,
median 168,628 candidates, 11 of 12 with a = 1.000).

Runs (same seeds, budget, task, threads as v3; add-node on):
- `python local_runner.py --seeds 1-16 --budget 1500000 --tag v3-nomatvec --task v3 --no-op MatVec --parallel 2 --threads 8`
- `python local_runner.py --seeds 1-16 --budget 1500000 --tag v3-extraops --task v3 --extra-ops --parallel 2 --threads 8`
Before them, a timing pilot per variant: seeds 1-2, budget 300k, tags v3a-pilot-nomatvec and
v3a-pilot-extraops.

Decision rule, fixed now: two-sided Fisher exact test of each variant's delta rate against
v3 (12/16). Significant at p < 0.05 only for 5/16 or fewer (scipy, computed before the run:
p = 0.032 at 5, 0.073 at 6, 0.149 at 7). Reading: delta rate stays (no significant drop) => the delta family comes from the
task, not from a short path in the alphabet. Delta rate drops significantly => the
alphabet's short path matters.

Predictions (subjective probabilities):
- No-MatVec: delta reached by at least 1 seed (p = 0.9); rate not significantly below v3
  (p = 0.6); median candidates to delta higher than v3's 168,628 (p = 0.7). Found delta rules
  use MatMul with an outer product of k (p = 0.85).
- Extra ops: delta reached by at least 1 seed (p = 0.9); rate not significantly below v3
  (p = 0.65); at least one best rule uses an extra op in its effective program (p = 0.8).
- In both variants every delta seed keeps T128 K8 at or above 0.75 (p = 0.6).
- No seed in either variant beats tuned DeltaNet on v3 on T128 K8 by more than 0.02 (p = 0.8).
- Pilot wall time per seed at 300k: 2 to 6 min for both variants (p = 0.6).

## Addendum (2026-11-04 07:19 UTC, post hoc)

Both 3a runs were stopped by the user's decision before completion: v3-extraops after
1 of 16 seeds, v3-nomatvec never started. Predictions above stay unchanged and untested.
Details: runs/v3-extraops/3a_ABBRUCH.md.

## Addendum 2 (2026-11-04 08:29 UTC, before any further result)

On the user's request the aborted v3-extraops run is resumed on the JupyterHub (jh.ide3.de, 16 vCPU EPYC 7763,
cargo 1.99.1) instead of being left aborted. Equality test before launch: hub and local give identical log rows
(fitness, accuracy, real evaluations at 628 / 50,036 / 100,084 candidates) for extra-ops seed 2 and v3 seed 4.
Same command and parameters as above; seed 2 (finished locally) is skipped, seeds 1 and 3-16 run from scratch.
v3-nomatvec stays held. Predictions unchanged.

## Addendum 3 (2026-11-04 15:37 UTC, before any no-MatVec result)

The user released the no-MatVec arm. It runs on the JupyterHub (same binary as the extra-ops arm, equality with
local checked there) with the command above; runs/v3-nomatvec/PAUSE removed. Predictions unchanged.
