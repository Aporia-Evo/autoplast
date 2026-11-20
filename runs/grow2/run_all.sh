#!/bin/bash
# Runs the pre-registered growth-loop v2 arms (README, "Growth loop, second version").
# With arguments: one lane over the given jobs (ARM:TASK). Without: the original two lanes.
# A job whose log already ends with the final report is skipped.
cd "$(dirname "$0")/../.."
lane() { for job in "$@"; do arm=${job%%:*}; t=${job##*:}; [ -f runs/grow2/arm${arm}2_task$t/log.md ] && grep -q '^```' runs/grow2/arm${arm}2_task$t/log.md && continue; python3 verify/grow.py --arm $arm --beam 4 --compact --task-seed $t > runs/grow2/${arm}2_task$t.stdout 2>&1; done; }
if [ $# -gt 0 ]; then lane "$@"; exit 0; fi
lane B:2 B:4 B:6 B:8 A:1 A:3 A:5 A:7 &
lane B:3 B:5 B:7 A:2 A:4 A:6 A:8 &
wait
echo ALL_DONE > runs/grow2/ALL_DONE
