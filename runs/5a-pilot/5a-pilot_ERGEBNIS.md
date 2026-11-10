# 5a pilot on collision3: result

Time: 2026-11-05 06:33 UTC. Code 38511a2 (local, Ryzen 5700G), seeds 1-2, 300k candidates, two in parallel.
Arms: A default alphabet + fixed readout; B evolved readout + extra ops; C evolved readout only.

| arm | seed | wall s | train | test regime collision3 | T12 ow0.3 | T128 K8 | readout |
|---|---|---|---|---|---|---|---|
| A | 1 | 220 | 0.510 | 0.509 | 0.716 | 0.542 | `(fixed)` |
| A | 2 | 261 | 0.510 | 0.517 | 0.746 | 0.541 | `(fixed)` |
| B | 1 | 225 | 0.513 | 0.523 | 0.790 | 0.556 | `o = S·q` |
| B | 2 | 638 | 0.519 | 0.527 | 0.765 | 0.574 | `o = S·q` |
| C | 1 | 86 | 0.509 | 0.517 | 0.765 | 0.554 | `o = S·q` |
| C | 2 | 178 | 0.513 | 0.517 | 0.727 | 0.560 | `o = (((σ(0.955)·S·q ⊙ tanh(S·q)) ⊙ tanh(S·q)) + tanh(S·q))` |

Reference on the collision3 test: tuned DeltaNet 0.631, LS reference 1.000. At 300k every arm
is at decayed-linear-attention level (0.51 to 0.53); no seed reached the delta milestone. One
C seed uses a nonlinear evolved readout, `o = tanh(Sq) + σ(0.955)·Sq ⊙ tanh(Sq)²`.

Cost of 16 seeds x 1.5M per arm (mean wall at 300k times the v3 factor 9.6, upper bound with
the v2 factor 16.6, two seeds in parallel on 16 threads):
A 5.1 h (up to 8.9 h), B 9.2 h (up to 15.9 h), C 2.8 h (up to 4.9 h);
together 17.1 h (up to 29.7 h) on one machine.

Predictions vs outcome: A 2 to 6 min per seed (p 0.6): yes, 3.7 and 4.4 min. B and C 1.5x to 4x
slower than A (p 0.6): B yes (1.8x), C no (0.55x, faster). No arm above 0.70 (p 0.75): yes.
At least one B or C seed with a non-empty effective read program (p 0.6): yes, C seed 2.
