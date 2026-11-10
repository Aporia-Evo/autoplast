"""Fan the Rust search out over many seeds on Modal, one container per seed.

    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3
    modal run modal_runner.py --seeds 1-16 --budget 1500000 --tag v3-noaddnode --no-split-edge
    modal run modal_runner.py --seeds 1-8 --tag r8-m2 --extra="--regime rewrite8 --train-episodes 192 --persist-m 2"

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
        ignore=["target", "runs", ".git", "**/__pycache__", "*.md", "verify"],
    )
    .run_commands("cd /src && /root/.cargo/bin/cargo build --release")
)

app = modal.App("autoplast-search", image=image)
runs_volume = modal.Volume.from_name("autoplast-runs", create_if_missing=True)


@app.function(cpu=float(CPUS), memory=4096, timeout=6 * 3600, volumes={"/runs": runs_volume})
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

    import aggregate  # local module; only needed on the launching machine

    base = ROOT / "runs" / tag
    for r in results:
        if isinstance(r, Exception):
            print("job failed:", r)
            continue
        d = base / f"seed{r['seed']}"
        d.mkdir(parents=True, exist_ok=True)
        for name in ("summary.md", "best.json", "log.csv"):
            (d / name).write_text(r[name])
    print(aggregate.write(base))
