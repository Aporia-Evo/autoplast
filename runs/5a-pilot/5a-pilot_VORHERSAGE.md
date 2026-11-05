# 5a pilot on collision3: prediction (written before the run)

Time: 2026-11-05 06:13 UTC. Code: 3bc77d0 plus collision3 and --evolve-readout (README "Evolved readout").
Purpose: timing pilot and first look before a 16-seed comparison. Arms, seeds 1-2, 300k each,
two processes with 8 threads in parallel, locally:
- A: `local_runner.py --seeds 1-2 --budget 300000 --tag 5a-pilot-A --regime collision3`
  (default alphabet, fixed readout)
- B: `... --tag 5a-pilot-B --regime collision3 --evolve-readout --extra-ops`
- C: `... --tag 5a-pilot-C --regime collision3 --evolve-readout` (readout only, for attribution)
Reference on the collision3 test: tuned DeltaNet 0.631, LS reference 1.000.

Predictions (subjective probabilities):
- Wall time per seed at 300k: A 2-6 min (p 0.6); B and C 1.5x to 4x slower than A (p 0.6).
- At 300k no arm exceeds 0.70 on the collision3 test (p 0.75).
- At least one B or C seed uses a non-empty effective read program (p 0.6).
