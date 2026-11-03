# v2-localpilot: result

Time: 2026-11-03 15:02 UTC. Commit e75904a, branch exp/v2-rediscovery-rate. Ryzen 5700G, two processes in
parallel, `--threads 8 --batch 128 --budget 300000`, add-node on. Prediction file:
v2-localpilot_VORHERSAGE.md (written before the run).

| seed | wall s | real evals | linear attention at | delta beta=1 | delta beta=0.5 | best rule (300k) | train | test ow0.3 | test d32 T24 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 57.5 | 92,195 | 71,156 | not reached | not reached | `S' = 0.962·S + v⊗k` (printed as `(0.481·S + 0.481·S) - v⊗(-k)`) | 0.814 | 0.786 | 0.875 |
| 2 | 57.3 | 82,057 | 65,012 | not reached | not reached | `S' = <v, tanh v>·S + tanh(tanh v)⊗k` | 0.817 | 0.789 | 0.878 |

Both best rules at 300k are decayed linear attention (seed 2 with a value-dependent decay).

Extrapolation to 1.5M candidates per seed, using the superlinear factor from runs/v2-local
(t(1.5M)/t(300k) = 11.5 and 24.4): 660 to 1,401 s per seed. 16 seeds, two at a time:
1.5 to 3.1 hours on this machine. The same again for the ablation (queue item 2).

Check against predictions: wall time per seed in 20 to 90 s (yes); both reach linear
attention (yes); neither reaches delta beta=0.5 (yes); 16-seed estimate in 1 to 6 h (yes);
trajectories differ from runs/v2-local for the same seeds (yes: local v2 seed 2 reached
linear attention at 16,756 candidates, here at 65,012).
