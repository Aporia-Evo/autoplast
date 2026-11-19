Diagnostics of `--residual-insert` (README, "Outside review of 19 Nov 2026").

- `mutstat_legacy*.md`, `mutstat_fixed*.md`: `autoplast mutstat --regime collision3 --recip --n 250 [--legacy]`
  on the 32 best rules of `runs/j-lexicase` and `runs/d-kalman`; one row per rule.
- `function_test_ri_lex_seed1_60k.md`: summary of `search --seed 1 --budget 60000 --batch 128 --regime collision3
  --recip --persist-m 3 --persist-init identity --select lexicase --residual-insert` with the corrected mutation.
  Not a result; it shows the counter line.
