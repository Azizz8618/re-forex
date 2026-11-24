#!/usr/bin/env python3
"""Full SIMH suite for the integrated variant-B + DO + ABS image.
Sequential, isolated tmux socket, workspace copies only.  The private prn0
capture is the authoritative observable; ACPU device copies are shared/stale.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
H = WS / "harness"
IMG = WS / "images"
RES = H / "runs"
CASES = [
    ("T1_A",      "T1_lit_A.b6",    None,      " 21 -0012.34  3000.00"),
    ("T1_B",      "T1_lit_B.b6",    None,      " 21 -0056.78  3000.00"),
    ("T2_A",      "T2_expr_A.b6",   None,      " 21 -0011.50  3000.00"),
    ("T2_B",      "T2_expr_B.b6",   None,      " 21 -0006.50  3000.00"),
    ("T2_PARENS", "T2_parens.b6",   None,      " 21 -0016.00  3000.00"),
    ("T3_W4",     "T3_w4.b6",       None,      " 21 -0034.50  3000.00"),
    ("T3_W2",     "T3_w2.b6",       None,      " 21 -  34.50  3000.00"),
    ("T4_SQRT_A", "T4_sqrt_A.b6",   None,      " 21 -0004.00  3000.00"),
    ("T4_SQRT_B", "T4_sqrt_B.b6",   None,      " 21 -0003.00  3000.00"),
    ("T4_ABS_A",  "T4_abs_A.b6",    None,      " 21 -0016.00  3000.00"),
    ("T4_ABS_B",  "T4_abs_B.b6",    None,      " 21 -0009.00  3000.00"),
    ("T5_DO_2",   "T5_do_2.b6",     None,      " 21 -0040.00  3000.00"),
    ("T5_DO_3",   "T5_do_3.b6",     None,      " 21 -0060.00  3000.00"),
    ("T6_NEG",    "T6_negative.b6", None,      None),
    ("PATCH",     "T2_expr_A.b6",   "patch",   " 21 -0011.60  3000.00"),
    ("RESTORE",   "T2_expr_A.b6",   "restore", " 21 -0011.50  3000.00"),
]

def clean_md41():
    for p in (H / "images").glob("md41_*"):
        p.unlink()

def main():
    preferred = sys.argv[1] if len(sys.argv) > 1 else "2048_FULL_A2"
    base = IMG / preferred
    if not base.is_file():
        raise SystemExit(f"missing {base}")
    for case, deck, img_kind, expected in CASES:
        image = base
        if img_kind == "patch":
            image = IMG / "2048_FULL_PATCH"
        elif img_kind == "restore":
            image = IMG / "2048_FULL_RESTORE"
            if not image.exists():
                shutil.copy2(base, image)
        tag = "FINAL2_" + case
        clean_md41()
        r = subprocess.run([sys.executable, str(H / "drive_b.py"), "--case", tag,
                            "--deck", str(WS / "decks" / deck),
                            "--image", str(image), "--timeout", "240"],
                           cwd=H, text=True, capture_output=True)
        vpath = RES / f"verdict_{tag}.json"
        verdict = json.loads(vpath.read_text()) if vpath.exists() else {}
        prn = (RES / f"localprn_{tag}.txt")
        prn_text = prn.read_text(encoding="utf-8", errors="replace") if prn.exists() else ""
        line = next((l for l in prn_text.splitlines() if l.startswith(" 21 ")), "")
        done = "КОНЕЦ ЗАДАЧИ" in prn_text
        if expected is None:
            ok = (verdict.get("product_gate") in ("PASS", "N/A")
                  and verdict.get("plumbing") == "PASS" and done
                  and ("ОТСУТСТВУЕТ" in prn_text))
        else:
            ok = (verdict.get("product_gate") == "PASS"
                  and verdict.get("plumbing") == "PASS" and done
                  and line == expected)
        print(f"{case:11s} rc={r.returncode} product={verdict.get('product_gate')} "
              f"plumbing={verdict.get('plumbing')} done={done} "
              f"line={line!r} expected={expected!r} -> {'PASS' if ok else 'FAIL'}",
              flush=True)
    clean_md41()

if __name__ == "__main__":
    main()
