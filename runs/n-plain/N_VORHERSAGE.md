# Package N (n-plain, n-random, testbed 2): predictions of the executing agent (written 2026-11-21 21:32 UTC, before the build, the self-checks, the timing and any run of N)

Build: commit dce11aa (branch claude/inspiring-pascal-2sa9s7, head at the time of writing; tree checked blob by blob, 4327/4327).
src/ differs from 6c2f60a only by the testbed-2 code (src/opt.rs, main.rs, program.rs, task.rs; RUNBOOK: memory search unchanged).
Machine: epyc, a fresh directory with this tree, cargo --release. Self-checks before any run: package F (seed 2, 120,000) and
d-kalman seed 9 to 50,000 (expected row 50036,19778,...,0.50570,0.5094,12,0.3803). The tree has no .git, so the commit is passed as
--extra="... --commit dce11aa". Keepalive kernel that prints a line every 60 s.

Design: RUNBOOK.md, package N. --task opt --opt-ops --persist-v 2, task seeds 901 to 916 (search seed = task seed), 300,000 candidates,
--parallel 2 --threads 8; n-random adds --algo random. Timing first (tag time-n-plain, seeds 901-902, 30,000, not committed); stop and ask if
the projection for an arm is above 30 h. Runs after package M on epyc. Report per seed: suite-1 objective, diverged fractions of all suites,
train - suite-1 gap, real evaluations, minutes, structural class (train dump per task seed, verify/opt_structure.py).
Reading of the research agent (README): Adam level = suite 1 at most -3.023, no divergence on any suite, gap at most 0.1.

Mine (subjective probabilities):
1. n-plain: at least one of 16 at the Adam level: P = 0.10.
2. n-random: at least one of 16 at the Adam level: P = 0.02.
3. n-plain: median suite-1 objective at or below SGD's -2.072: P = 0.45.
4. n-plain: the structural class SGD (or SGD-like) for 8 or more of 16 best rules: P = 0.50.
5. n-random: median suite-1 objective worse (higher) than that of n-plain: P = 0.90.
6. n-plain: at least one seed with a diverged fraction above 0 on some suite: P = 0.70.
7. Timing projection for each arm (x10 from 30,000 to 300,000, x2 margin, 8 pairs) at or below 30 h: P = 0.70.
8. Mean train - suite-1 gap of n-plain at or below 0.1: P = 0.75.
