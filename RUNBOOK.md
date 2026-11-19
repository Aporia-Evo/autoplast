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
reading"). Package E below extends it.

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

### E. Seeds 17 to 32 of package D (released 13 Nov 2026)

Status 14 Nov 2026: done and checked (README, "Package E: result, and the base rate over 32
seeds"). Package F below is the next one.

Purpose: package D found one seed above 0.85 in 16. Before any search algorithm is compared
against this setting, the base rate needs more seeds. E is D with seeds 17 to 32 and nothing
else changed.

Conditions that keep the 32 seeds one sample:
- Same machine as D (epyc) and the same binary: the search code has not changed since
  e979a8e (`git diff e979a8e HEAD -- src` is empty at the commit that adds this section). If
  you rebuild, check that first; if `src/` differs, stop and ask.
- Same tag, `d-kalman`. The runner skips seeds that have a summary, so seeds 1 to 16 are not
  touched. Do not edit their files or `d-kalman_report.md`.
- If epyc is not reachable, stop and ask; do not move the run to the workstation.

Write your predictions into `runs/d-kalman/E_VORHERSAGE.md` and commit them before the run.
No timing step: D measured 17 to 107 minutes per seed, 6.1 h for 16 seeds.

```bash
python local_runner.py --seeds 17-32 --budget 1500000 --tag d-kalman --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity"
```

Then the JAX check on the exact Rust test data for the new seeds, and delete the dump:

```bash
./target/release/autoplast dump --regime collision3 --split test --out runs/d-kalman/collision3_test.json
```

```bash
python verify/verify.py --task-json runs/d-kalman/collision3_test.json runs/d-kalman/seed1[7-9]/best.json runs/d-kalman/seed2[0-9]/best.json runs/d-kalman/seed3[0-2]/best.json > runs/d-kalman/verify_dump_17-32.txt
```

Report in `runs/d-kalman/e_report.md`, with the same columns and counts as in D, three times:
for seeds 17 to 32 alone, for seeds 1 to 16 as already reported, and for all 32. Also the full
formula of every new seed with test above 0.72, and for every such seed whether its formula
has the shape of seed 9 (README, "What seed 9 is": an address `norm(P1ᵀ k)` or similar taken
from a persistent register, and a write along that address); say only what the formula shows.
Rule 1 for all 32 seeds against `runs/c-m2` and `runs/5a-A` (16 seeds each). `aggregate.md`
is rewritten by the runner for all 32 seeds; that is intended. Add the new seeds to `WHERE.md`.

### F. Constants tuned per structure, base task (released 14 Nov 2026)

Status 15 Nov 2026: done and checked (README, "Package F: result and reading"). Packages H
and G below are released; run H first.

Read README, "Search method, first change", first. Three arms on the base task (the v2
setting: no `--task`, no `--regime`, default alphabet, one state), seeds 1 to 16, 1,500,000
candidates, batch 128. The baseline is the committed `runs/v2` and `runs/v2-noaddnode`; do not
rerun them. Any one machine; say which in `WHERE.md`.

Build the code at the commit that contains this section. Self-check before the runs: the
default search must still give `120052,22831,...,0.82164,0.8142,4,...` as last log row of

```bash
./target/release/autoplast search --seed 2 --budget 120000 --threads 2 --out /tmp/chk > /dev/null && tail -1 /tmp/chk/log.csv
```

on Linux (other values on Windows are possible, see rule 7; report them).

Write predictions into `runs/f-tune8/F_VORHERSAGE.md` and commit them before the first run.
Timing first, 2 seeds, not committed (tuning costs more real evaluations per candidate):

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-f --parallel 2 --threads 8 --extra="--tune-consts 8 --val-log"
```

Then the three arms:

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag f-tune8 --parallel 2 --threads 8 --extra="--tune-consts 8 --val-log"
```

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag f-tune3 --parallel 2 --threads 8 --extra="--tune-consts 3 --val-log"
```

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag f-random --parallel 2 --threads 8 --extra="--algo random --val-log"
```

JAX check of every best rule of the three arms (no dump needed on the base task):

```bash
python verify/verify.py runs/f-tune8/seed*/best.json > runs/f-tune8/verify.txt
```

and the same for `f-tune3` and `f-random`.

What to report, per arm, in `runs/<tag>/f_report.md`, next to the same numbers for `runs/v2`
and `runs/v2-noaddnode` taken from their committed summaries:
- Primary count: seeds whose summary shows `delta rule (beta=0.5)` reached under Milestones,
  with the candidate count; median of those counts.
- Structural count: seeds whose final rule is `delta rule` or `gated delta rule`
  (`structure:` line), and seeds that are `unclassified` with erase c/a above 0.3.
- Seeds ending at linear attention level (train accuracy below 0.84).
- Per seed: train, test ow0.3, T64 K8, T128 K8, the growth factor `a` of the structure line,
  number of instructions, real evaluations, minutes.
- Train minus test ow0.3 per seed and its mean per arm, against the baseline's mean.
- The `val_acc` and `long_acc` columns of the last log row per seed.
- Largest difference JAX against Rust on test ow0.3.

### H. Parent selection by behaviour, base task (released 15 Nov 2026) — run this first

Status 15 Nov 2026: done and checked (README, "Package H: result and reading"). The abort of
`h-share` seed 16 was a fault in the search code (cache emptied before the lookups); it is
fixed in the commit that adds this note. Thank you for not patching it and for reporting the
cause. Package I below follows after G.

Read README, "Search method, second change", first. The search code changed: build at the
commit that contains this section and repeat the self-check of package F (same expected last
log row). Base task (no `--task`, no `--regime`), seeds 1 to 32, 1,500,000 candidates, batch
128, all three arms on the same machine (epyc, as in F). Predictions into
`runs/h-base/H_VORHERSAGE.md`, committed before the first run.

Timing, 2 seeds each, not committed (`share` is expected to take several times as long as the
plain search):

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-h-share --parallel 2 --threads 8 --extra="--select share --val-log"
```

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-h-lex --parallel 2 --threads 8 --extra="--select lexicase --val-log"
```

If the projection for all three arms is above 30 hours of wall time, stop and ask. The arms:

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag h-base --parallel 2 --threads 8 --extra="--val-log"
```

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag h-share --parallel 2 --threads 8 --extra="--select share --val-log"
```

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag h-lexicase --parallel 2 --threads 8 --extra="--select lexicase --val-log"
```

JAX check of every best rule, per arm:

```bash
python verify/verify.py runs/h-share/seed*/best.json > runs/h-share/verify.txt
```

Report per arm in `runs/<tag>/h_report.md`, with `h-base` next to it, the columns and counts
of package F, and in addition:
- one-sided Fisher test of the arm against `h-base` on the accuracy-level count and on the
  structural count (state the four p values plainly; do not pick one);
- for every delta rule: growth factor `a` and T128 K8; per arm the number of delta rules with
  `a` within 0.02 of 1;
- real evaluations and minutes per seed, and their arm means;
- the `pop_mean_acc` column of the last log row per seed, arm mean.

### G. Constant tuning in the space of D and E (released 15 Nov 2026) — after H

Status 16 Nov 2026: done and checked (README, "Package G: result and reading"). Next is
package I, then package J.

Read README, "Package G". collision3, same space, machine and counts as D and E; the baseline
is the committed `runs/d-kalman` (32 seeds); do not rerun it. Predictions into
`runs/g-tune8/G_VORHERSAGE.md`, committed before the first run. Timing first, not committed:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-g --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838"
```

If the projection for 32 seeds is above 30 hours of wall time, stop and ask. The run:

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag g-tune8 --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838"
```

Then dump, JAX check on the dump for all 32 seeds, delete the dump, as in D. Report in
`runs/g-tune8/g_report.md` with the columns and counts of `e_report.md`, the 32 seeds of
`runs/d-kalman` next to them, and in addition: the `validation level` line of every summary
(candidates to rule 2 on validation data), train − test per seed, real evaluations and
minutes per seed, the full formula of every seed with test above 0.72, and for each of those
whether it has the shape of seed 9.

### I. Plain search with the wall time of the selection arms (released 15 Nov 2026) — after G

Status 17 Nov 2026: done and checked (README, "Package I: result and reading"), including
the rerun of `h-share` seed 16 and the rewritten `runs/h-share/aggregate.md`. Package J is
released and unchanged; its reading got one added condition (README, "Addition to package
J"), which does not change what you run or report.

Purpose: `h-share` and `h-lexicase` take 2.5 and 1.9 times as long per seed as `h-base`. I
gives the plain search that time. Build at the commit that contains this section (it holds
the cache fix) and repeat the self-check of package F. Base task, same machine as H.
Predictions into `runs/i-base4m/I_VORHERSAGE.md`, committed before the run. No timing step
(`h-base` took 4.9 minutes per seed at 1.5M).

```bash
python local_runner.py --seeds 1-32 --budget 4000000 --tag i-base4m --parallel 2 --threads 8 --extra="--val-log"
```

Also rerun the one aborted seed of H with the fixed code (the runner skips the 31 finished
seeds; first delete the directory of the aborted run, after copying its `log.csv` and
`stderr.txt` to `runs/h-share/seed16_aborted/`):

```bash
python local_runner.py --seeds 16-16 --budget 1500000 --tag h-share --parallel 1 --threads 8 --extra="--select share --val-log"
```

Report in `runs/i-base4m/i_report.md`: the counts of package H for `i-base4m` next to
`h-base`, `h-share`, `h-lexicase`; for `i-base4m` also the number of seeds at the accuracy
level by 1.5M candidates (from the Milestones line) and by 4M; minutes per seed. For seed 16:
its row as in `h_report.md`, whether the first rows of its log equal those of the aborted
run (all columns but `real_evals` and `seconds`), and the counts of `h-share` with 32 seeds.

Note of 16 Nov 2026: `aggregate.py` failed on `runs/h-share` because of the side folder
`seed16_local_rerun` (it read every `seed*` folder as a seed number). Fixed in the commit that
adds this note; it now takes only folders named `seed<number>`. The search binary is not
affected, no rebuild is needed. After fetching the rerun of seed 16, write the table with
`python aggregate.py runs/h-share` from a checkout that has the fix.

### J. Selection by behaviour in the space of D and E (released 16 Nov 2026) — after I

Status 19 Nov 2026: both arms done and checked (README, "Package J, arm j-lexicase" and
"Package J, arm j-share"). The epsilon check of `j-share` was run by the research agent
(`runs/eps-check/`). Package K below is released.

Read README, "Package J". Same build as package I (the commit with the cache fix or later;
`git diff 2f49b69 HEAD -- src` must be empty, otherwise rebuild and repeat the self-check).
collision3, same space and machine as D and E; baseline is the committed `runs/d-kalman`
(32 seeds), do not rerun it. Predictions into `runs/j-lexicase/J_VORHERSAGE.md`, committed
before the first run of J.

Timing, 2 seeds each, not committed:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-j-lex --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --val-log --level-acc 0.651 --level-long 0.838"
```

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-j-share --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select share --val-log --level-acc 0.651 --level-long 0.838"
```

If the projection for one arm of 32 seeds is above 40 hours of wall time, stop and ask
before starting that arm. First arm:

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag j-lexicase --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --val-log --level-acc 0.651 --level-long 0.838"
```

Report `j-lexicase` (below) before starting the second arm; it may run on while you report:

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag j-share --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select share --val-log --level-acc 0.651 --level-long 0.838"
```

Per arm: dump, JAX check on the dump for all 32 seeds, delete the dump, as in D. A seed that
aborts is reported with its `stderr.txt` and partial log and is not restarted without word
from the research agent.

Added 18 Nov 2026 after `j-lexicase` (README, "Package J, arm j-lexicase"), for `j-share` and
every later arm in this space. On the same dump, before deleting it, from a checkout that has
`verify/eps_scale.py`:

```bash
python verify/verify.py --x64 --norm-eps 1e-9 --task-json runs/<tag>/collision3_test.json runs/<tag>/seed*/best.json > runs/<tag>/verify_x64_eps1e-9.txt
```

For every seed whose accuracy there differs from `verify_dump.txt` by more than 0.02:

```bash
python verify/eps_scale.py --task-json runs/<tag>/collision3_test.json runs/<tag>/seed<N>/best.json >> runs/<tag>/eps_scale.txt
```

Report both files and list those seeds with their ratio. Do not exclude a seed yourself; the
research agent applies rule 3.

Report in `runs/<tag>/j_report.md`, with the 32 seeds of `runs/d-kalman` next to the arm:
- the three counts of package E (rule 2; stuck below 0.53; test > 0.85 with rule 2's other
  conditions), seeds above 0.695 and above 0.90, median test, Mann-Whitney against
  `runs/d-kalman`;
- per seed: train, collision3 test, T64 K8, T128 K8, train − test, structural family, which
  of `P1` and `P2` the `S'` formula reads, reciprocal in `S'` or not, the `validation level`
  line, instructions, real evaluations, minutes, `pop_mean_acc` of the last log row;
- the full formula of every seed with test above 0.72 and, for each, whether it has the shape
  of seed 9 (an address taken from a persistent register and a write along it) or contains
  a gain of the form `P k / (c + kᵀP k)`; say only what the formula shows;
- real evaluations at the `validation level` row per seed (column 2 of that log row).

### K. Residual insertion on collision3, and the wall-time control of J (released 19 Nov 2026)

Read README, "Package K" and "Outside review of 19 Nov 2026". The search code changed since
50c2d10 (`--residual-insert`, off by default; corrected on 19 Nov): build at the commit that
contains the note "Corrected 19 Nov" below, or later, on both machines.

Corrected 19 Nov 2026: the residual insertion of the first release overwrote live registers.
If `k-ri-lex` (or its timing run) was started with an earlier build, stop it, move its folder
to `runs/k-ri-lex-faulty/` without committing it, and report how far it got. `k-plain2m` does
not use the flag; a run started with the earlier build may continue. The summary of
`k-ri-lex` now has a line `residual insert: ... attempts, ... blocks inserted, ... compacted`;
report those three numbers per seed.

Self-checks after the build, on each machine:

1. The self-check of package F (last log row of seed 2 at 120,000 candidates).
2. The flag-off reproduction of `d-kalman` seed 9. On Linux the row must read
   `50036,19778,<seconds>,0.50570,0.5094,12,0.3803`; on Windows report what you get (rule 7):

```bash
./target/release/autoplast search --seed 9 --budget 50000 --batch 128 --threads 8 --regime collision3 --recip --persist-m 3 --persist-init identity --out /tmp/chk9 > /dev/null && grep '^50036' /tmp/chk9/log.csv
```

Predictions into `runs/k-ri-lex/K_VORHERSAGE.md`, committed before the first run of K.

Timing, 2 seeds each, not committed; `k-ri-lex` on epyc, `k-plain2m` on the workstation:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-k-ri-lex --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838"
```

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-k-plain2m --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --val-log --level-acc 0.651 --level-long 0.838"
```

If the projection for an arm is above 30 hours of wall time, stop and ask before starting it.
The two arms run at the same time, one per machine (on the workstation after package L):

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag k-ri-lex --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838"
```

```bash
python local_runner.py --seeds 1-32 --budget 2100000 --tag k-plain2m --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --val-log --level-acc 0.651 --level-long 0.838"
```

Note of 19 Nov 2026: `k-ri-lex` stopped when the hub server on epyc restarted. Resume it with the
same command. Before that, delete the folders of seeds without `summary.md` (copy their
`log.csv` to `runs/k-ri-lex/aborted/seed<N>_log.csv` first). The runner restarts those seeds
from the beginning; seeds are deterministic, so this is safe. To survive a restart of the
notebook kernel, start the runner from a terminal of the hub, detached
(`nohup setsid python local_runner.py ... > runs/k-ri-lex/runner_log_epyc.txt 2>&1 &`). A restart
of the whole server still stops it; then resume the same way and record each stop in `WHERE.md`.

Per arm, as in J: dump, JAX check on the dump for all 32 seeds, the epsilon check of 18 Nov
(`verify.py --x64 --norm-eps 1e-9`, then `verify/eps_scale.py` for every seed that moves by more
than 0.02), delete the dump. A seed that aborts is reported with its `stderr.txt` and partial
log and is not restarted without word from the research agent. If one arm finishes first,
report it without waiting for the other.

Report in `runs/<tag>/k_report.md`:
- `k-ri-lex`, with `j-lexicase` and `d-kalman` next to it: the counts of J (rule 2; stuck below
  0.53; test > 0.85 with rule 2's other conditions; above 0.695 under those conditions; above
  0.90 under those conditions), median test, Mann-Whitney against `j-lexicase`, the seeds the
  epsilon check moved with their ratio, and the per-seed table of J. The full formula of every
  seed with test above 0.72; for each, say only what the formula shows: whether `S'` reads `P1`
  or `P2`, whether a persistent register is updated by subtracting an outer product, whether a
  gain of the form `P k / (c + kᵀP k)` appears.
- `k-plain2m`, with `d-kalman`, `j-lexicase` and `j-share` next to it: the same counts; per seed
  also the train accuracy of the last log row at or below 1,500,100 candidates (to compare with
  `d-kalman`, where 11 of 32 seeds were below 0.53 at that point); minutes per seed.

### L. Down-sampling control, base task (released 19 Nov 2026) — on the workstation, before `k-plain2m`

Status 19 Nov 2026: done and checked (README, "Package L: result and reading").

Read README, "The down-sampling control". Same build as K (corrected). Base task as in H (no
`--task`, no `--regime`), seeds 1 to 32, 1.5M candidates. Baseline: the committed `h-base`,
`h-share`, `h-lexicase`; do not rerun them. Predictions into `runs/l-downsample/L_VORHERSAGE.md`,
committed before the run. No timing step: `h-lexicase` took 9.2 minutes per seed, expect about
2.5 to 3 h in total. Self-check of package F first.

```bash
python local_runner.py --seeds 1-32 --budget 1500000 --tag l-downsample --parallel 2 --threads 8 --extra="--select downsample --val-log"
```

```bash
python verify/verify.py runs/l-downsample/seed*/best.json > runs/l-downsample/verify.txt
```

Report in `runs/l-downsample/l_report.md`, with `h-base`, `h-share` and `h-lexicase` next to it,
the counts and columns of package H (accuracy level of delta β = 0.5; one-sided Fisher against
`h-base` and against `h-lexicase`; structural count; ends at linear attention level; median and
best test; train − test; candidates and real evaluations to the level; minutes per seed;
growth factors; T128 K8 ≥ 0.80). Then start `k-plain2m`.

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
