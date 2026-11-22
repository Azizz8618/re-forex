#!/bin/bash
# 75 — FRONT.FTN emits structured postfix RHS tokens 777005 in addition to
# the legacy ASCII stream. Compare them with the contract for the canonical
# 10-card BASE77 deck (X=1.0, Y=X+2.0).
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
export FRONT1_WORK=${FRONT1_WORK:-$(mktemp -d "${TMPDIR:-/tmp}/front75.XXXXXX")}
export BESM6_DISK_SHARE=${BESM6_DISK_SHARE:-/usr/local/share/besm6}
echo "workspace: $FRONT1_WORK"
python3 "$ROOT/tests/plan-f77/71-front-base77/inject.py" --mode spec10 || exit 1
python3 "$ROOT/tests/plan-f77/71-front-base77/compile.py" --mode spec10 || exit 1
grep '^ *777005' "$FRONT1_WORK/work/spec10/call.out" > "$FRONT1_WORK/got_777005.txt"
if diff -u "$HERE/expected_777005.txt" "$FRONT1_WORK/got_777005.txt"; then
    echo "777005: MATCHES structured RHS contract"
    echo "VERDICT: PASS"
else
    echo "VERDICT: FAIL"
    exit 1
fi
