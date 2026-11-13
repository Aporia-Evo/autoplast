# Package E (d-kalman seeds 17-32): predictions of the executing agent (written 2026-11-13 15:03 UTC, before the run)

Commit af0a992 (branch claude/inspiring-pascal-2sa9s7). The compare e979a8e...af0a992 shows no change under src/ and none to
local_runner.py, so the run uses the epyc binary built from e979a8e for package D, in the same directory, without a rebuild.
Machine: epyc. Command (RUNBOOK.md, package E), commit passed through --extra because the epyc tree has no .git:

    python local_runner.py --seeds 17-32 --budget 1500000 --tag d-kalman --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --commit e979a8e"

The summaries will carry commit e979a8e, the code they were built from. Seeds 1-16 are skipped by the runner and not touched.

Research agent's prediction (README, "Package E"): main count for seeds 17-32 is 0 with P = 0.45, 1 with 0.35, 2 or more with 0.20;
at least one seed above 0.695 with P = 0.85.

Mine for seeds 17-32 (subjective probabilities):
1. Main count (test > 0.85, T128 K8 >= 0.838, train - test <= 0.03): 0 with P = 0.45, exactly 1 with P = 0.33, 2 or more with P = 0.22.
2. At least one seed above 0.695 under rule 2's other two conditions. P = 0.75.
3. Rule 2 passed by 2 to 7 of the 16 new seeds. P = 0.65.
4. If a new seed is above 0.72, its formula has the shape of seed 9 (an address such as norm(P1ᵀ k) taken from a persistent register
   and a write along that address). P = 0.50, conditional on such a seed existing.
5. At least 3 of the new seeds end at decayed linear attention level (test 0.50 to 0.53). P = 0.70.
6. Wall time for the 16 new seeds 5 to 8 h. P = 0.70.
7. JAX on the dumped test data reproduces Rust within 0.002 for every new seed. P = 0.80.
8. Rule 1 over all 32 seeds: significant (p < 0.05) against 5a-A with P = 0.45; against c-m2 with P = 0.10.
