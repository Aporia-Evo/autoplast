"""Fan the Rust search out over many seeds on Modal, one container per seed.

    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3
    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3-noaddnode --no-split-edge
    modal run modal_runner.py --seeds 1-8 --tag r8-m2 --extra "--regime rewrite8 --train-episodes 192 --persist-m 2"

`--extra` is passed to `autoplast search` unchanged (regime, task seed, state budget, --no-recip).

Each container builds nothing at run time: the binary is compiled once into the image.
Results land in the Modal volume `autoplast-runs` and are copied to ./runs/<tag>/seed<N>/.
./runs/<tag>/aggregate.md then lists, per seed, the structural family of the best rule and when
each family first appeared as best rule (the rediscovery test), plus the rate across seeds.
Accuracy levels are listed separately; they are not rediscovery.

Cost control: every container uses CPU only (no GPU). Start with a few seeds and a small
budget to check timing before launching large fan-outs.
"""

import pathlib
import re
import subprocess

import modal

ROOT = pathlib.Path(__file__).parent
CPUS = 8

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("curl", "build-essential")
    .run_commands("curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal")
    .add_local_dir(
        str(ROOT),
        "/src",
        copy=True,
        ignore=["target", "runs", ".git", "**/__pycache__"],
    )
    .run_commands("cd /src && /root/.cargo/bin/cargo build --release")
)

app = modal.App("autoplast-search", image=image)
runs_volume = modal.Volume.from_name("autoplast-runs", create_if_missing=True)


@app.function(cpu=float(CPUS), timeout=6 * 3600, volumes={"/runs": runs_volume})
def search(seed: int, budget: int, tag: str, no_split_edge: bool, extra: str = "", commit: str = "unknown") -> dict:
    out = f"/runs/{tag}/seed{seed}"
    cmd = [
        "/src/target/release/autoplast", "search",
        "--seed", str(seed),
        "--budget", str(budget),
        "--threads", str(CPUS),
        "--batch", str(16 * CPUS),
        "--log-every", "50000",
        "--out", out,
        "--commit", commit,
    ] + extra.split()
    if no_split_edge:
        cmd.append("--no-split-edge")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    runs_volume.commit()
    files = {name: open(f"{out}/{name}").read() for name in ("summary.md", "best.json", "log.csv")}
    return {"seed": seed, **files}


def parse_milestones(summary: str) -> dict:
    hits = {}
    for name, val in re.findall(r"^- (.+?) \(acc [0-9.]+\): (.+)$", summary, flags=re.M):
        m = re.match(r"(\d+) candidates", val)
        hits[name] = int(m.group(1)) if m else None
    return hits


def parse_families(summary: str) -> dict:
    """Structural families that appeared as best rule -> candidate count of first appearance."""
    return {name: int(n) for name, n in re.findall(r"^\* (.+?): (\d+) candidates$", summary, flags=re.M)}


@app.local_entrypoint()
def main(seeds: str = "1-4", budget: int = 1_500_000, tag: str = "v3", no_split_edge: bool = False, extra: str = ""):
    lo, hi = (int(x) for x in seeds.split("-"))
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "unknown"
    except OSError:
        commit = "unknown"
    jobs = [(s, budget, tag, no_split_edge, extra, commit) for s in range(lo, hi + 1)]
    print(f"launching {len(jobs)} containers x {CPUS} CPUs, budget {budget} candidates each")
    results = list(search.starmap(jobs, return_exceptions=True))

    base = ROOT / "runs" / tag
    rows, names = [], None
    for r in results:
        if isinstance(r, Exception):
            print("job failed:", r)
            continue
        d = base / f"seed{r['seed']}"
        d.mkdir(parents=True, exist_ok=True)
        for name in ("summary.md", "best.json", "log.csv"):
            (d / name).write_text(r[name])
        hits = parse_milestones(r["summary.md"])
        names = names or list(hits)
        formula = next((l for l in r["summary.md"].splitlines() if l.startswith("S' =")), "")
        final = next((l[len("structure: "):].split("  [")[0] for l in r["summary.md"].splitlines() if l.startswith("structure: ")), "?")
        rows.append((r["seed"], hits, formula, final, parse_families(r["summary.md"])))

    if not rows:
        return
    rows.sort()
    lines = [f"# {tag}: {len(rows)} seeds, budget {budget}, add-node {'off' if no_split_edge else 'on'}, extra '{extra}', commit {commit}", ""]
    lines += ["## Structural rediscovery", "", "| seed | family of final best rule | families seen as best rule (first candidate count) | best rule |", "|---|---|---|---|"]
    for seed, _, formula, final, fams in rows:
        seen = ", ".join(f"{f} ({n:,})" for f, n in fams.items())
        lines.append(f"| {seed} | {final} | {seen} | `{formula[:120]}` |")
    lines.append("")
    for fam in sorted({f for r in rows for f in r[4]}):
        reached = sorted(r[4][fam] for r in rows if fam in r[4])
        ended = sum(r[3] == fam for r in rows)
        lines.append(f"- {fam}: seen in {len(reached)}/{len(rows)} seeds (median {reached[len(reached) // 2]:,} candidates), final rule in {ended}/{len(rows)}")
    lines += ["", "## Accuracy levels (not rediscovery)", "", "| seed | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for seed, hits, *_ in rows:
        lines.append(f"| {seed} | " + " | ".join(f"{hits[n]:,}" if hits[n] else "–" for n in names) + " |")
    (base / "aggregate.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
