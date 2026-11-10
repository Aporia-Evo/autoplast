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

## Work packages

A (timing) and B (base task with `--recip`, add-node on and off, 16 seeds each) are done; the
results are in `runs/base-recip/` and `runs/base-recip-noaddnode/` and in README, "Merge".
They were run at commit 045ea3a, where `Recip` was on by default; since the merge the same
runs need `--recip`.

No package is released at the moment. The next ones follow `CLAUDE.md`, "Next experiments",
and will be written here with tags and commands once the owner has decided on the method
change. Do not start searches on your own.

Command pattern for a released package (the runner skips finished seeds):

```bash
python local_runner.py --seeds 1-16 --budget 1500000 --tag <tag> --parallel 2 --threads 8 --task v3
```

```bash
python local_runner.py --seeds 1-8 --budget 1500000 --tag <tag> --parallel 2 --threads 8 --task-seed-from-seed --extra="--regime rewrite8 --train-episodes 192 --persist-m 2 --recip"
```

If `git` cannot be executed where the runner starts, pass the commit yourself with
`--extra="--commit <hash>"` and say so in `WHERE.md`.

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
