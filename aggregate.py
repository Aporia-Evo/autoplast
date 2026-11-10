"""Build runs/<tag>/aggregate.md from the per-seed summaries. Shared by modal_runner.py and
local_runner.py, so a tag looks the same wherever it ran.

    python aggregate.py runs/v3
"""

import pathlib
import re
import sys


def parse_levels(summary: str) -> dict:
    """Accuracy levels (not rediscovery): reference rule -> candidate count or None."""
    hits = {}
    for name, val in re.findall(r"^- (.+?) \(acc [0-9.]+\): (.+)$", summary, flags=re.M):
        m = re.match(r"(\d+) candidates", val)
        hits[name] = int(m.group(1)) if m else None
    return hits


def parse_families(summary: str) -> dict:
    """Structural families that appeared as best rule -> candidate count of first appearance."""
    return {name: int(n) for name, n in re.findall(r"^\* (.+?): (\d+) candidates$", summary, flags=re.M)}


def field(summary: str, prefix: str, default: str = "?") -> str:
    return next((l[len(prefix):] for l in summary.splitlines() if l.startswith(prefix)), default)


def write(base: pathlib.Path) -> str:
    rows = []
    for d in sorted(base.glob("seed*"), key=lambda p: int(p.name[4:])):
        f = d / "summary.md"
        if not f.exists():
            continue
        s = f.read_text()
        rows.append(
            dict(
                seed=int(d.name[4:]),
                levels=parse_levels(s),
                fams=parse_families(s),
                final=field(s, "structure: ").split("  [")[0],
                formula=field(s, "S' =", ""),
                train=field(s, "train acc "),
                header=[l for l in s.splitlines()[2:5]],
            )
        )
    if not rows:
        return ""
    lines = [f"# {base.name}: {len(rows)} seeds", ""]
    lines += ["Settings of the first seed (all seeds of a tag must share them except seed and task seed):", ""]
    lines += [f"    {l}" for l in rows[0]["header"]] + [""]
    lines += ["## Structural rediscovery", ""]
    lines += ["| seed | family of final best rule | train acc | families seen as best rule (first candidate count) | best rule |", "|---|---|---|---|---|"]
    for r in rows:
        seen = ", ".join(f"{f} ({n:,})" for f, n in r["fams"].items())
        lines.append(f"| {r['seed']} | {r['final']} | {r['train']} | {seen} | `S' ={r['formula'][:110]}` |")
    lines.append("")
    for fam in sorted({f for r in rows for f in r["fams"]}):
        reached = sorted(r["fams"][fam] for r in rows if fam in r["fams"])
        ended = sum(r["final"] == fam for r in rows)
        lines.append(
            f"- {fam}: seen in {len(reached)}/{len(rows)} seeds (median {reached[len(reached) // 2]:,} candidates), "
            f"final rule in {ended}/{len(rows)}"
        )
    names = list(rows[0]["levels"])
    lines += ["", "## Accuracy levels (not rediscovery)", "", "| seed | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for r in rows:
        lines.append(f"| {r['seed']} | " + " | ".join(f"{r['levels'][n]:,}" if r["levels"].get(n) else "–" for n in names) + " |")
    text = "\n".join(lines) + "\n"
    (base / "aggregate.md").write_text(text)
    return text


if __name__ == "__main__":
    print(write(pathlib.Path(sys.argv[1])))
