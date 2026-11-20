#!/bin/bash
# Growth loop v3, arm B3, one lane over the given task seeds (README, "Growth loop, third version").
# A seed whose log already ends with the final report is skipped; an interrupted seed resumes
# from its saved state.
cd "$(dirname "$0")/../.."
for t in "$@"; do
  f=runs/grow3/armB3_task$t/log.md
  [ -f $f ] && grep -q '^```' $f && continue
  python3 verify/grow.py --v3 --arm B --beam 4 --task-seed $t > runs/grow3/B3_task$t.stdout 2>&1
done
