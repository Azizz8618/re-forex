#!/bin/bash
# 71 — FRONT.FTN BASE77 rules 30..37: compile with SYSTEM FOREX 2.02 and
# compare the emitted IR with the contract in docs/63 section 3.1.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
export FRONT1_WORK=${FRONT1_WORK:-$(mktemp -d "${TMPDIR:-/tmp}/front71.XXXXXX")}
export BESM6_DISK_SHARE=${BESM6_DISK_SHARE:-/usr/local/share/besm6}
echo "workspace: $FRONT1_WORK"
python3 "$HERE/inject.py" --mode spec10 || exit 1
python3 "$HERE/compile.py" --mode spec10 || exit 1
if diff -u "$HERE/expected_ir_spec10.txt" "$FRONT1_WORK/ir_spec10.txt"; then
    echo "IR: MATCHES docs/63 section 3.1 (spec10, corrected itype)"
else
    echo "VERDICT: FAIL (IR mismatch)"
    exit 1
fi
echo "VERDICT: PASS"
