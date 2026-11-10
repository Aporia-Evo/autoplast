# autoplast: runbook for the executing agent

You run experiments for autoplast on the owner's machines. Read `CLAUDE.md` (goal and rules)
and `README.md` (method and every result) first. This file says which machine does what, in
which order, and what you hand back. Where this file and `CLAUDE.md` disagree, `CLAUDE.md` wins.

## Machines

| name | what it is | use it for |
|---|---|---|
| workstation | Ryzen 7 5700G (8 cores, 16 threads), GTX 1660 Super (6 GB) | searches, `sweep`, `verify`; the GPU only for stage 4 (small trained models) |
| epyc | university EPYC, 8 cores, reached over SSH with the owner's key | searches |
| modal | Modal, CPU containers with 8 CPUs; 30 USD of credits in total | overflow only, see budget rule |

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
5. Modal budget. Look up the remaining credit before and after every launch and report both
   numbers. Do not launch if the estimate for the launch exceeds 5 USD without the owner's
   go-ahead, and never go below 10 USD remaining. Prices are not recorded here; read them
   from the Modal dashboard.
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

Determinism check. On the machine this file was written on, the checksum of `best.json` is
`7e0c2197a77e256e63f643baf773bd7b` and linear attention first appears at 16,756 candidates. The
same values mean the machine reproduces bit for bit; other values are not an error (rule 7),
but report them:

```bash
./target/release/autoplast search --seed 2 --budget 120000 --threads 2 --no-recip --out /tmp/chk > /dev/null && md5sum /tmp/chk/best.json && grep '^\* ' /tmp/chk/summary.md
```

## Work packages, in order

### A. Timing (no credits)

On workstation and on epyc, 2 seeds each of the base task and of the most expensive regime:

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-base --jobs 2 --threads 4
```

```bash
python local_runner.py --seeds 1-2 --budget 150000 --tag time-r8 --jobs 2 --threads 4 --task-seed-from-seed --extra="--regime rewrite8 --train-episodes 192"
```

Report minutes per seed for both, per machine, and the projection to 1,500,000 candidates.
Cost per candidate rises during a search (programs get longer), so multiply the projection by
2 as a safety margin. `time-*` tags are not results; do not commit them.

### B. Rediscovery rate on the base task (item 4 in `CLAUDE.md`)

Two tags, 16 seeds each, 1,500,000 candidates. Split by seed range across the two machines:

```bash
python local_runner.py --seeds 1-8 --budget 1500000 --tag v3 --jobs 2 --threads 4
```

```bash
python local_runner.py --seeds 9-16 --budget 1500000 --tag v3 --jobs 2 --threads 4
```

```bash
python local_runner.py --seeds 1-8 --budget 1500000 --tag v3-noaddnode --jobs 2 --threads 4 --extra="--no-split-edge"
```

```bash
python local_runner.py --seeds 9-16 --budget 1500000 --tag v3-noaddnode --jobs 2 --threads 4 --extra="--no-split-edge"
```

Then copy `runs/v3*/seed*/` from epyc to workstation and rebuild the tables:

```bash
python aggregate.py runs/v3 && python aggregate.py runs/v3-noaddnode
```

What to report: for each tag, in how many of 16 seeds the final best rule is a delta rule or
gated delta rule, the median candidate count of its first appearance, and the same for linear
attention. "Seen as best rule" early in a run can be a weak rule that merely has the family's
shape; the headline number is the family of the final rule together with its train accuracy.
Verify every final rule of the delta family in JAX:

```bash
python verify/verify.py runs/v3/seed*/best.json > runs/v3/verify.txt
```

Modal is not needed for B. If one machine is unavailable, run the missing seed range on the
other one rather than on Modal.

### C. Search per regime (item 5 in `CLAUDE.md`): blocked

Do not start C. It waits for two things from the owner and the research agent:
the decision which improvements the search method gets, and the baseline search algorithms
(random search is not implemented yet). When C is released it will come with its own tags and
commands in this file.

### D. Modal check (only when the owner asks for it)

The Modal runner was changed on 10 Nov 2026 and has not run since. Its first use is a
2-seed test, which also measures cost:

```bash
modal run modal_runner.py --seeds 1-2 --budget 150000 --tag modal-test
```

Report wall time per seed, credit before and after, and whether `runs/modal-test/aggregate.md`
was written.

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
- Any Modal launch above the limits in rule 5.
- The university machine is busy or its use is questioned.
