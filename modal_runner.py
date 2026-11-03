"""Fan the Rust search out over many seeds on Modal, one container per seed.

    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v2
    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v2-noaddnode --no-split-edge

Each container builds nothing at run time: the binary is compiled once into the image.
Results land in the Modal volume `autoplast-runs` and are copied to ./runs/<tag>/seed<N>/.
./runs/<tag>/aggregate.md then lists, per seed, whether and when each reference rule was
reached, plus the rediscovery rate across seeds.

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
def search(seed: int, budget: int, tag: str, no_split_edge: bool) -> dict:
    out = f"/runs/{tag}/seed{seed}"
    cmd = [
        "/src/target/release/autoplast", "search",
        "--seed", str(seed),
        "--budget", str(budget),
        "--threads", str(CPUS),
        "--batch", str(16 * CPUS),
        "--log-every", "50000",
        "--out", out,
    ]
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


@app.local_entrypoint()
def main(seeds: str = "1-4", budget: int = 1_500_000, tag: str = "v2", no_split_edge: bool = False):
    lo, hi = (int(x) for x in seeds.split("-"))
    jobs = [(s, budget, tag, no_split_edge) for s in range(lo, hi + 1)]
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
        rows.append((r["seed"], hits, formula))

    if not rows:
        return
    rows.sort()
    lines = [f"# {tag}: {len(rows)} seeds, budget {budget}, add-node {'off' if no_split_edge else 'on'}", ""]
    lines.append("| seed | " + " | ".join(names) + " | best rule |")
    lines.append("|---|" + "---|" * (len(names) + 1))
    for seed, hits, formula in rows:
        cells = [f"{hits[n]:,}" if hits[n] else "–" for n in names]
        lines.append(f"| {seed} | " + " | ".join(cells) + f" | `{formula[:120]}` |")
    lines.append("")
    for n in names:
        reached = [h[n] for _, h, _ in rows if h[n]]
        med = sorted(reached)[len(reached) // 2] if reached else None
        lines.append(f"- {n}: reached by {len(reached)}/{len(rows)} seeds" + (f", median {med:,} candidates" if med else ""))
    (base / "aggregate.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
