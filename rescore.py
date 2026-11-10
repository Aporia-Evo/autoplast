"""Apply the structural test (src/classify.rs) to the final rule of every seed of the given tags.

    python rescore.py > runs/structural-rescore.md

Each rule is evaluated with the task it was searched on, so the memory states of the fit come
from that task. Reads only committed best.json files; nothing is searched.
"""

import collections
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).parent
EXE = ROOT / "target/release/autoplast"
TAGS = [
    ("v1-noaddnode", "", "base task, 48 train episodes, add-node off (3 Nov)"),
    ("v2-local", "", "base task, add-node on (3 Nov)"),
    ("v2", "", "base task, add-node on"),
    ("v2-noaddnode", "", "base task, add-node off"),
    ("base-recip", "", "base task, add-node on, Recip in the alphabet (package B)"),
    ("base-recip-noaddnode", "", "base task, add-node off, Recip in the alphabet (package B)"),
    ("v3", "--task v3", "task v3 (long episodes), add-node on"),
    ("v3-extraops", "--task v3", "task v3, ten extra ops"),
    ("v3-nomatvec", "--task v3", "task v3, without MatVec"),
    ("5a-A", "--regime collision3", "collision3, fixed readout"),
    ("5a-B", "--regime collision3", "collision3, evolved readout, ten extra ops"),
    ("5a-C", "--regime collision3", "collision3, evolved readout"),
]
DELTA = ("delta rule", "gated delta rule")

print("# Structural test on the final rule of every committed seed\n")
print("Family by `src/classify.rs` (least-squares fit on real memory states, R² ≥ 0.99). \"old count\" is the")
print("number of seeds whose summary says the accuracy level of delta rule beta=0.5 was reached, the")
print("criterion used before 10 Nov 2026. For evolved-readout runs only the write rule is classified.\n")
print("| tag | setting | seeds | delta family (structural) | old count (accuracy level) | linear attention family | unclassified | other |")
print("|---|---|---|---|---|---|---|---|")
detail = []
for tag, flags, what in TAGS:
    fam = collections.Counter()
    old = n = 0
    rows = []
    for d in sorted((ROOT / "runs" / tag).glob("seed*"), key=lambda p: int(p.name[4:])):
        if not (d / "best.json").exists():
            continue
        out = subprocess.run([str(EXE), "eval", "--prog", str(d / "best.json")] + flags.split(), capture_output=True, text=True).stdout
        line = next(l for l in out.splitlines() if l.startswith("structure: "))
        f = line[len("structure: "):].split("  [")[0]
        r2 = re.search(r"R²=([0-9.]+)", line).group(1)
        a = re.search(r"a=([0-9.-]+)", line).group(1)
        e = re.search(r"c/a=([0-9.-]+)", line).group(1)
        train = next(l for l in out.splitlines() if l.startswith("train acc ")).split()[2]
        summ = (d / "summary.md").read_text(encoding="utf-8")
        hit = re.search(r"^- delta rule \(beta=0\.5\) \(acc [0-9.]+\): (\d+) candidates", summ, flags=re.M)
        old += bool(hit)
        fam[f] += 1
        n += 1
        rows.append(f"| {tag} | {d.name[4:]} | {f} | {a} | {e} | {r2} | {train} | {'yes' if hit else 'no'} |")
    la = fam["linear attention"] + fam["decayed linear attention"]
    dl = sum(fam[x] for x in DELTA)
    other = n - la - dl - fam["unclassified"]
    print(f"| {tag} | {what} | {n} | {dl} | {old} | {la} | {fam['unclassified']} | {other} |")
    detail += rows
print("\n## Per seed\n")
print("| tag | seed | family | a | erase c/a | R² | train acc | delta accuracy level reached |")
print("|---|---|---|---|---|---|---|---|")
print("\n".join(detail))
