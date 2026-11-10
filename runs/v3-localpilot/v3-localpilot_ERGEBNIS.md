# v3-localpilot: result

Time: 2026-11-03 21:10 UTC. Command as in the prediction file. Wall 132 s (seed 1) and 200 s (seed 2), two
in parallel, 8 threads each.

| seed | linear attention at | delta beta=0.5 at | best rule (300k) | train | T12 ow0.3 | d32 T24 | T64 K8 | T128 K8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 74,740 | no | `S' = σ(2.278)·S + v⊗k` (decay 0.907) | 0.725 | 0.769 | 0.734 | 0.571 | 0.555 |
| 2 | 13,172 | 18,420 | `S' = S + (tanh³(v) − 0.595·(S − 0.595·k⊗tanh²(v))·k)⊗k` | 0.913 | 0.915 | 0.984 | 0.853 | 0.853 |

Seed 2 found a delta rule with a = 1 (no amplification) at 18k candidates. On T128 K8 it is
at the level of tuned DeltaNet on v3 (0.850). One seed at 300k candidates; not a claim.

Extrapolation: mean 166 s per seed at 300k. With the v2 factor t(1.5M)/t(300k) (11.5 to 24.4
from v2-local, 16.6 measured as v2 mean over v2-localpilot), 1.5M takes about 1,900 to 4,050 s
per seed, so 16 seeds two at a time take 4.2 to 9.0 h, central estimate 6.1 h.

Predictions vs outcome: wall 2 to 6 min per seed (yes); both reach linear attention (yes);
neither reaches delta (no, seed 2 did at 18k); 16-seed estimate 4 to 12 h (yes, 4.2 to 9.0).
