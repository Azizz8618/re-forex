#!/usr/bin/env python3
"""Reproducible build of the canonical FOREX 5.00 product contour.

Reuses the proven on-machine chain in final_sign.py verbatim (copied from
/tmp/.private/azizz/opencode/sign-opt/scripts). Only the workspace path was
adapted; no opcode, constant, word or deck-byte was re-derived.

Outputs (under ../images):
  2048_base                base zone-2350 contour (repo tool, SHA a98e8109...)
  2048_forex500_canonical  canonical product image (= docs/100 SIGN_A)
  2048_SIGN_B              SIGNBIT T8 1<<40 -> 0 (one machine-word patch)
  2048_SIGN_REST           byte-identical restore of the canonical image

Usage: python3 build/build_canonical.py
"""
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
sys.path.insert(0, str(HERE))

import final_sign as S  # noqa: E402


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    # 1. Base contour: exact repo tool, vendored read-only fixtures.
    base_cmd = [sys.executable, str(HERE / "build_zone2350_contour.py"),
                "base", "--out", str(WS / "images")]
    print("+", " ".join(base_cmd), flush=True)
    subprocess.run(base_cmd, check=True)
    base = WS / "images/2048_base"
    print("base sha:", sha(base), flush=True)
    assert sha(base) == ("a98e81090d4b254554a0cd3ff8611438615de84fc012e"
                         "8e2b70fbabc2ebdc796"), "base drift"

    # 2. Canonical image: 116 halfwords = 58/58 words, sign + both reclaims.
    S.build("forex500_canonical", sign="plain", drop_last_ati=True,
            floor_acc=True, ws=str(WS))
    # 3. B: one machine word (SIGNBIT in T[8] = RAM 0o2137) set to zero.
    S.build("SIGN_B", sign="plain", drop_last_ati=True, floor_acc=True,
            patch={"T8": 0}, ws=str(WS))
    # 4. C: byte-identical restore (no patch) -> same SHA as canonical.
    S.build("SIGN_REST", sign="plain", drop_last_ati=True, floor_acc=True,
            ws=str(WS))

    canon = WS / "images/2048_forex500_canonical"
    bimg = WS / "images/2048_SIGN_B"
    rest = WS / "images/2048_SIGN_REST"
    assert sha(canon) == ("f620c72a1febff771ff970cd325ffad19f4844148f02a4f"
                          "aca453127662541be"), "canonical image drift"
    assert sha(rest) == sha(canon), "restore not byte-identical"
    assert sha(bimg) == ("21325b509ed89cc79f85e29e931381fcc4e370b46a3e82e6"
                         "110dca8b0ee99f3a"), "B image drift"
    print("VERIFIED: canonical = restore = f620c72a..., B = 21325b50...",
          flush=True)


if __name__ == "__main__":
    main()
