# autoplast: runbook for the executing agent

You run experiments for autoplast on the owner's machines. Read `CLAUDE.md` (goal and rules)
and `README.md` (method and every result) first. This file says which machine does what, in
which order, and what you hand back. Where this file and `CLAUDE.md` disagree, `CLAUDE.md` wins.

## Machines

| name | what it is | use it for |
|---|---|---|
| workstation | Ryzen 7 5700G (8 cores, 16 threads), GTX 1660 Super (6 GB) | searches, `sweep`, `verify`; the GPU only for stage 4 (small trained models) |
| epyc | university EPYC, 8 cores, reached over SSH with the owner's key | searches |
| modal | Modal; 30 USD of credits in total | GPU runs only, each with the owner's explicit approval; no CPU searches |

Never write host names, user names, key paths or tokens into the repository, a commit message
or a summary. Use the three names above.

The university machine is shared infrastructure. Check its load before you start (`uptime`),
run under `nice`, use at most its 8 physical cores, and stop if someone else needs it.

## Rules for running

1. No search code changes. You run what is committed. If a run needs a code change, stop and
   report; do not tune mutations, selection or hyperparameters yourself.
2. Commit first, run second. `local_runner.py` marks results `-dirty` if `src/` has
   uncommitted changes; dirty results do not go into the README.
3. One tag, one setting. All seeds of a tag share every flag except seed and task seed. A new
   setting gets a new tag. Never overwrite a tag; resume it (finished seeds are skipped).
4. Time before you spend. Before any tag, run 2 seeds of it, note minutes per seed, and write
   the expected total into your report. On Modal this is mandatory for anything above 8 seeds.
5. Modal. Not used for searches (decision of 3 Nov 2026). A GPU run needs the owner's
   explicit approval; look up the remaining credit before and after and report both numbers.
6. Report negatives. A seed that finds nothing, a failed job and a crashed machine all go
   into the report as they happened.
7. Results are tied to the machine. The search is deterministic for a given binary, seed,
   `--batch` and flags, but `tanh` and `exp` can differ in the last bit between machines, so
   do not expect the same rule for the same seed on workstation, epyc and modal. Record where
   each seed ran (see "Handing back").

## Setup, once per machine

```bash
git clone <repo> && cd autoplast && git checkout <branch given by the owner>
```

```bash
cargo build --release
```

```bash
pip install numpy jax
```

Self-check. The table must label the five reference rules as no write, linear attention,
delta rule, delta rule, gated delta rule:

```bash
./target/release/autoplast baselines | cut -c1-90
```

Determinism check. On Linux, linear attention first appears as best rule at 16,756 candidates
and the last log row reads `120052,22831,...,0.82164,0.8142,4,...`. The same values mean the
machine reproduces bit for bit; other values are not an error (rule 7), but report them:

```bash
./target/release/autoplast search --seed 2 --budget 120000 --threads 2 --out /tmp/chk > /dev/null && grep '^\* ' /tmp/chk/summary.md && tail -1 /tmp/chk/log.csv
```

## Status update, 10 Nov 2026 (read this first if you ran packages A and B)

The branch `exp/v2-rediscovery-rate` was merged into `claude/inspiring-pascal-2sa9s7`
(commit ae33301). Work from this branch from now on. What that means for you:

- One code base. It is the code of the experiment branch (task v3, `--no-op`, `--extra-ops`,
  `--evolve-readout`, stage-2 regimes, `dump`) plus the structural test, the state budget
  (`--persist-m`, `--persist-v`), `--recip`, the ridge ceiling and two-state references in
  `sweep`. All earlier results of both branches are in `runs/`.
- Your two package-B tags were renamed: `runs/v3` is now `runs/base-recip`, `runs/v3-noaddnode`
  is now `runs/base-recip-noaddnode`. `runs/v3` is the task-v3 run of 4 Nov. Nothing in your
  files was changed except the headings.
- `Recip` is off by default. Package B ran at commit 045ea3a, where it was on; the same runs
  now need `--recip`. `--no-recip` no longer exists.
- `local_runner.py` is the runner of 3 Nov again (`--parallel`, `--threads`, `--task`, `--regime`,
  `--evolve-readout`, ...) with `--extra`, `--recip`, `--task-seed-from-seed` added. It writes
  `wall_seconds.txt` per seed and calls `aggregate.py`.
- Your results were checked: files complete, two seeds recomputed on Linux with identical logs
  to 350,000 candidates. The gap you reported (base-recip seed 4, clustered suite, Rust 0.034
  against JAX 0.091) is the draw of the embeddings: the same rule scores 0.034 to 0.120 in
  Rust over six task seeds. The ± next to accuracies counts queries only.
- Outcome of package B together with the 3 Nov ablation: delta family in 9/32 seeds with
  add-node and 11/32 without. The add-node mutation has no measurable effect.
- Platform: `runs/v3` seeds 1 and 2 (run on Windows) do not reproduce on Linux, four other
  seeds do. Treat a committed seed as reproducible on its own platform only (rule 7).
- Modal is not used for searches (decision of 3 Nov, restored).

Read README, "Merge of the two branches and package B" and "Package C", before you start.

## Work packages

A and B are done (`runs/base-recip/`, `runs/base-recip-noaddnode/`; README, "Merge").

### C. Second state on collision3 (released 10 Nov 2026)

Status 11 Nov 2026: arm C1 is done and checked (`runs/c-m2/`; README, "Package C, arm C1").
Arm C2 is withdrawn; package D below replaces it. Two notes from your run: set `PYTHONPATH` to the
repository if Python does not put the script directory on `sys.path`, and the summary line
"train episodes: 144" is 96 standard plus 48 long episodes, the same task as 5a-A.

Question: 48 searches with one state (5a-A, 5a-B, 5a-C) found no rule above tuned DeltaNet on
collision3. Does the same search find one when a rule may keep a second d×d state?

Everything is as in 5a-A (task collision3, task seed 1, 96 train episodes, 19 ops, fixed
readout, seeds 1 to 16, 1,500,000 candidates, batch 128) except the state budget. The control
is the committed `runs/5a-A`; do not rerun it.

Bars on the collision3 test suite (README, "Package C"): tuned DeltaNet 0.640, tuned Gated
DeltaNet 0.644, hand-written two-state probe 0.679 (T128 K8 0.857), Kalman delta 0.935,
ridge ceiling 1.000.

Before anything else, write your predictions into `runs/c-m2/C_VORHERSAGE.md`, as for B.

1. Timing, 2 seeds, not committed:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-c --parallel 2 --threads 8 --regime collision3 --extra="--persist-m 2"
```

Report minutes per seed and the projection to 1,500,000 candidates (times 2 as margin). If
the projection for 16 seeds is above 24 hours of wall time, stop and ask.

2. Arm C1, the main arm:

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag c-m2 --parallel 2 --threads 8 --regime collision3 --extra="--persist-m 2"
```

3. Arm C2, only after C1 is reported and the owner says go (adds the reciprocal):

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag c-m2-recip --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 2"
```

4. Check every best rule in JAX on the exact Rust test data:

```bash
./target/release/autoplast dump --regime collision3 --split test --out runs/c-m2/collision3_test.json
```

```bash
python verify/verify.py --task-json runs/c-m2/collision3_test.json runs/c-m2/seed*/best.json > runs/c-m2/verify_dump.txt
```

What to report, per arm:
- Per seed: collision3 test accuracy, train accuracy, T128 K8, structural family, and whether
  the rule uses the second state at all (a line `P1' = ...` under the formula in `summary.md`).
- Rule 1 (as in 5a): Mann-Whitney test of the 16 test accuracies against `runs/5a-A`.
- Rule 2 (as in 5a, unchanged): test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03.
  How many seeds pass, and for each passing seed the formula.
- How many seeds beat the hand-written probe (0.679) under rule 2's other two conditions.
- JAX against Rust on the dump: largest difference.

`runs/c-m2/collision3_test.json` is large; do not commit it (delete it after step 4).
If `git` cannot be executed where the runner starts, pass the commit with
`--extra="--persist-m 2 --commit <hash>"` and say so in `WHERE.md`.

### D. Search in the space that contains Kalman delta (released 11 Nov 2026)

Status 13 Nov 2026: done and checked (`runs/d-kalman/`; README, "Package D: result and
reading"). No further package is released; wait for the owner.

Question: since commit c12f791 the Kalman delta rule can be written in the search space
(15 instructions, collision3 test 0.933, T128 K8 0.950; README, "A known target inside the
search space"). Does the present search find it, or anything near it?

Setting: collision3, task seed 1, the usual 96 + 48 train episodes, fixed readout, seeds 1 to 16,
1,500,000 candidates, batch 128, with three changes against arm C1: a third persistent matrix
register, persistent registers start at the identity, and the reciprocal op. Controls are the
committed `runs/5a-A` (one state) and `runs/c-m2` (two states); do not rerun them.

Bars on the collision3 test suite: tuned DeltaNet 0.640, best rule found so far 0.695 (c-m2
seed 2), Kalman delta written by hand in this space 0.933, ridge ceiling 1.000.

Use the code at the commit that contains this section or later, and build it first. Write
your predictions into `runs/d-kalman/D_VORHERSAGE.md` and commit them before the first run.

1. Timing, 2 seeds, not committed:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-d --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity"
```

Report minutes per seed and the projection to 1,500,000 candidates (times 2 as margin). On
the review machine this space ran slower per candidate than C1. If the projection for 16
seeds is above 24 hours of wall time, stop and ask.

2. The run:

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag d-kalman --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity"
```

3. Check every best rule in JAX on the exact Rust test data, then delete the dump:

```bash
./target/release/autoplast dump --regime collision3 --split test --out runs/d-kalman/collision3_test.json
```

```bash
python verify/verify.py --task-json runs/d-kalman/collision3_test.json runs/d-kalman/seed*/best.json > runs/d-kalman/verify_dump.txt
```

What to report:
- Per seed: train, collision3 test, T64 K8, T128 K8, structural family, which of `P1` and `P2`
  the printed `S'` formula reads, and whether the formula contains a reciprocal (`1/(`).
- Rule 1 (as in 5a): Mann-Whitney on the 16 test accuracies, once against `runs/c-m2` and once
  against `runs/5a-A`.
- Rule 2 (unchanged): test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03. Seeds passing.
- New count: seeds with test > 0.85 under rule 2's other two conditions. This is the number
  the run is about. Also the seeds above 0.695 (the best rule of C1).
- The full formula (`S'`, `P1'`, `P2'`) of every seed with test above 0.72.
- Candidate count at which each seed's best rule first passed test-level 0.70 is not in the
  logs (they hold train accuracy); report instead the candidate count of the last improvement
  of `best_acc` in `log.csv`.
- JAX against Rust on the dump: largest difference.

As in C: if Python does not find `aggregate`, set `PYTHONPATH` to the repository; if `git`
cannot be executed, add `--commit <hash>` inside `--extra` and say so in `WHERE.md`.

## Handing back

For every finished tag:

1. `runs/<tag>/aggregate.md` exists and lists all seeds.
2. Add `runs/<tag>/WHERE.md`: which seeds ran on workstation, epyc or modal, minutes per seed,
   and any seed that failed or was rerun.
3. Commit `runs/<tag>/` (summaries, logs, best rules, aggregate, WHERE, verify output) with a
   message that names tag, seeds and budget. Do not edit `README.md` or `CLAUDE.md`; the
   research agent writes the interpretation.
4. Write a short report: what ran, on which machine, how long, the numbers asked for in the
   work package, and anything that went wrong.

## When to stop and ask

- A command in this file fails or its output looks different from what is described here.
- The self-check does not label the reference rules as listed.
- Timing says a work package would take more than 24 hours of wall time.
- Any use of Modal.
- The university machine is busy or its use is questioned.
