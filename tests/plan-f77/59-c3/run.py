#!/usr/bin/env python3
"""D2 harness for the F77 stage-59 C3 self-contained patched-*TRANS proof.

This script is deliberately self-contained: all BESM-6 words it writes are
stored as hexadecimal text fixtures next to it.  Disk images are always copied
from the system share into a private work directory; the live images under
/usr/local/share/besm6 are never written.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DECK = HERE / "deck.b6"
N = 0o1744                      # catalog zone on disk 2148
BODY_ZONE = N + 1               # 0o1745
Z2_ZONE = N + 2                 # 0o1746
DISK_SHARE = Path("/usr/local/share/besm6")
DISKS = ("2048", "2053", "2099", "2148")
MARKER = "OUR-CODE-RAN-7391"
BANNER = "BANNER-DISK-7391"


def hexwords(path):
    words = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if len(line) != 12:
            raise SystemExit(f"{path}: bad word length {len(line)}: {line!r}")
        words.append(bytes.fromhex(line))
    return words


def wb(words):
    return b"".join(words)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_env():
    env = dict(os.environ)
    for k in list(env):
        if (k.startswith("BESM6_REDIRECT") or k.startswith("BESM6_MTR")
                or k in ("BESM6_CORE_ON_PC", "BESM6_CORE_SKIP", "BESM6_DD_DEBUG")):
            env.pop(k, None)
    return env


def write_zone(besmtool, disks, zone, words, tag, case_dir, env):
    payload = case_dir / f".{tag}.words"
    payload.write_bytes(wb(words))
    r = subprocess.run(
        [besmtool, "write", "2148", f"--from-file={payload}",
         f"--start=0{zone:o}"],
        env=env, capture_output=True, text=True, timeout=60)
    if "Written" not in r.stdout:
        raise SystemExit(f"{tag}: besmtool write failed: {r.stdout!r} {r.stderr!r}")


def run_case(name, body, expect_marker, expect_banner, work, base_disks,
             besmtool, binary, timeout, verbose):
    case_dir = work / name
    case_dir.mkdir(parents=True)
    disks = case_dir / "disks"
    shutil.copytree(base_disks, disks)
    env = clean_env()
    env["BESM6_PATH"] = str(disks)

    cat = hexwords(DATA / "cat.hex")
    z2 = hexwords(DATA / "z2.hex")
    zero = [b"\0" * 6] * 1024
    write_zone(besmtool, disks, N, cat, "cat", case_dir, env)
    write_zone(besmtool, disks, BODY_ZONE, body, "body", case_dir, env)
    write_zone(besmtool, disks, Z2_ZONE, z2, "z2", case_dir, env)
    for z in range(3, 41):
        write_zone(besmtool, disks, N + z, zero, f"z{z:03o}", case_dir, env)

    shutil.copy(DECK, case_dir / "deck.b6")
    out = case_dir / "out.txt"
    err = case_dir / "err.txt"
    with out.open("wb") as fo, err.open("wb") as fe:
        try:
            rc = subprocess.run([str(binary), "-l", "deck.b6"], cwd=case_dir,
                                env=env, stdout=fo, stderr=fe,
                                timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            rc = "TIMEOUT"
    out_text = out.read_text(encoding="utf-8", errors="replace")
    err_text = err.read_text(encoding="utf-8", errors="replace")
    (case_dir / "rc.txt").write_text(str(rc))

    got_marker = MARKER in out_text
    got_banner = BANNER in out_text
    got_patch = ("C3PATCH pc=" in err_text
                 and "C3: loaded 11 body words from disk 2148 zone 01745" in err_text)
    ok = (rc == 0 and got_marker == expect_marker and got_banner == expect_banner
          and got_patch)
    if verbose:
        for line in out_text.splitlines():
            if any(k in line for k in (MARKER, BANNER, "КОНЕЦ")):
                print(f"    | {line.strip()}")
        for line in err_text.splitlines():
            if "C3PATCH" in line or "C3: loaded" in line:
                print(f"    | {line.strip()}")
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: rc={rc} marker={got_marker} "
          f"banner={got_banner} patch_hooks={got_patch} "
          f"(expect marker={expect_marker}, banner={expect_banner})")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="private work directory")
    ap.add_argument("--bin", required=True, help="patched dispak binary")
    ap.add_argument("--besmtool", default="besmtool")
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--no-diskmarker", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    work = Path(args.work).resolve()
    base_disks = work / "base-disks"
    if not base_disks.is_dir():
        raise SystemExit(f"missing prepared base disks: {base_disks}")
    binary = Path(args.bin).resolve()
    if not binary.is_file():
        raise SystemExit(f"missing dispak binary: {binary}")

    body = hexwords(DATA / "body.hex")
    if len(body) != 1024:
        raise SystemExit(f"body.hex: expected 1024 words, got {len(body)}")
    body_banner = hexwords(DATA / "body_banner.hex") if not args.no_diskmarker else None

    zero9 = list(body)
    zero9[9] = b"\0" * 6

    before = sha256(DISK_SHARE / "2148")
    results = []
    results.append(run_case("main", body, True, False, work, base_disks,
                            args.besmtool, binary, args.timeout, args.verbose))
    results.append(run_case("zero9", zero9, False, False, work, base_disks,
                            args.besmtool, binary, args.timeout, args.verbose))
    if body_banner is not None:
        results.append(run_case("diskmarker", body_banner, False, True, work,
                                base_disks, args.besmtool, binary,
                                args.timeout, args.verbose))
    after = sha256(DISK_SHARE / "2148")
    if before != after:
        print(f"  [FAIL] system disk 2148 changed: {before} -> {after}")
        results.append(False)
    else:
        print(f"  [PASS] system disk 2148 unchanged (sha256 {before[:16]}...)")

    print(f"RESULT: {'PASS' if all(results) else 'FAIL'} "
          f"({sum(results)}/{len(results)} checks)")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
