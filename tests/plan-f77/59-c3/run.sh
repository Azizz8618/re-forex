#!/usr/bin/env bash
# D2 reproducible test: C3 self-contained patched *TRANS runs OUR code.
#
# Everything writable lives in a private work directory below ${TMPDIR:-/var/tmp}.
# The live images in /usr/local/share/besm6 are only ever read/copied.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DISK_SHARE="${BESM6_DISK_SHARE:-/usr/local/share/besm6}"
KEEP=0
NO_BUILD=0
NO_DISKMARKER=0
VERBOSE=0
WORK=""
BIN="${DISPAK_C3_BIN:-}"

usage() {
    sed -n '2,8p' "$0"
    echo "Usage: $0 [--work DIR] [--keep] [--no-build] [--no-diskmarker]"
    echo "       DISPAK_C3_BIN=PATH  use a prebuilt patched dispak instead of building"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --work) WORK="$2"; shift 2 ;;
        --keep) KEEP=1; shift ;;
        --no-build) NO_BUILD=1; shift ;;
        --no-diskmarker) NO_DISKMARKER=1; shift ;;
        --verbose) VERBOSE=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    esac
done

for d in 2048 2053 2099 2148; do
    if [[ ! -f "$DISK_SHARE/$d" ]]; then
        echo "missing system disk: $DISK_SHARE/$d" >&2
        exit 2
    fi
done
command -v besmtool >/dev/null || { echo "besmtool not found in PATH" >&2; exit 2; }
command -v cmake >/dev/null || { echo "cmake not found in PATH" >&2; exit 2; }

if [[ -z "$WORK" ]]; then
    WORK="$(mktemp -d "${TMPDIR:-/var/tmp}/f77-59-c3.XXXXXX")"
else
    mkdir -p "$WORK"
fi
WORK="$(cd "$WORK" && pwd)"
if [[ "$KEEP" -eq 0 ]]; then
    trap 'python3 -c "import shutil,sys; shutil.rmtree(sys.argv[1], ignore_errors=True)" "$WORK"' EXIT
fi
echo "WORK=$WORK"

if [[ -n "$BIN" ]]; then
    NO_BUILD=1
fi
if [[ "$NO_BUILD" -eq 0 ]]; then
    cp -a "$HERE/src" "$WORK/src"
    cmake -S "$WORK/src" -B "$WORK/build" -DCMAKE_BUILD_TYPE=Release \
        > "$WORK/cmake.log" 2>&1 || { tail -40 "$WORK/cmake.log" >&2; exit 1; }
    cmake --build "$WORK/build" --target dispak -j4 \
        > "$WORK/build.log" 2>&1 || { tail -60 "$WORK/build.log" >&2; exit 1; }
    BIN="$WORK/build/dispak/dispak"
fi
echo "BIN=$BIN"

mkdir -p "$WORK/base-disks"
for d in 2048 2053 2099 2148; do
    cp "$DISK_SHARE/$d" "$WORK/base-disks/$d"
done

EXTRA=()
[[ "$NO_DISKMARKER" -eq 1 ]] && EXTRA+=(--no-diskmarker)
[[ "$VERBOSE" -eq 1 ]] && EXTRA+=(--verbose)
python3 "$HERE/run.py" --work "$WORK" --bin "$BIN" \
    --besmtool "$(command -v besmtool)" "${EXTRA[@]}"
