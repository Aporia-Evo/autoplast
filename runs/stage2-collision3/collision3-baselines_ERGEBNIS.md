# collision3 baselines: result

Time: 2026-11-05 06:13 UTC. Code: 3bc77d0 plus the collision3 regime. Local, 159 s.
Raw: baselines_collision3.md, sweep_collision3.md, ceiling_collision3.txt.

| family / rule | a | e | train | test regime collision3 | T12 ow0.3 | T64 K8 | T128 K8 |
|---|---|---|---|---|---|---|---|
| linear attention | | | 0.362 | 0.385 | 0.750 | 0.104 | 0.062 |
| delta β=0.5 | | | 0.617 | 0.640 | 0.924 | 0.840 | 0.828 |
| tuned DeltaNet | 1 | 0.60 | 0.620 | 0.631 | 0.919 | 0.855 | 0.858 |
| tuned Gated DeltaNet | 1 | 0.60 | 0.620 | 0.631 | 0.919 | 0.855 | 0.858 |
| LS reference (offline) | | | 1.000 | 1.000 | | | |

Reading: with long episodes in the mix the a > 1 artefact is gone; tuned Gated DeltaNet
collapses onto DeltaNet (a = 1). The best tuned family reaches 0.631 on the collision3 test,
the offline least-squares reference 1.000: headroom 0.369. This is the stage-2 target regime.
(Delta β=0.5 untuned scores 0.640 on test, 0.009 above the tuned family, which was tuned on
the train set where it scores 0.620 vs 0.617: within noise.)

Predictions vs outcome: GDN optimum a <= 1.01 (p 0.7): yes, 1.00. DeltaNet test 0.60 to 0.72
(p 0.6): yes, 0.631. GDN at most 0.02 above DeltaNet (p 0.65): yes, 0. LS at least 0.95 (p 0.8):
yes, 1.000. Headroom at least 0.2 (p 0.65): yes, 0.369.
