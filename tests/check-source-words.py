#!/usr/bin/env python3
"""Побайтовая проверка аннотированных МАДЛЕН-текстов против дампов.

В каждом `src/LO_*.mad` агент оставил метку слова с его машинным значением:
  LO_SYN: `С--- слово 0000 (абс 241500), машинное слово 000000200003 ---`
  LO_GEN: `С слово 0000  @0o277500  = 0o0000000000200003`
Скрипт извлекает пары (номер слова, 48-битное слово) и сверяет их с
`build/LO_*.words`. Это проверка того, что реконструкция сохранила ВСЕ
1024 слова без искажений.

Возврат: 0 — все слова совпали; 1 — расхождения.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAT_SYN = re.compile(
    r"слово\s+([0-7]{3,4})\s+\(абс\s+[0-7]+\),\s*машинное слово\s+([0-7]{12,16})"
)
PAT_GEN = re.compile(r"слово\s+([0-7]{3,4})\s+@0o[0-7]+\s*=\s*0o?([0-7]{12,16})")


def check(name: str, src: Path, dump: Path, pattern: re.Pattern) -> bool:
    data = dump.read_bytes()
    words = [int.from_bytes(data[i:i + 6], "big") for i in range(0, len(data), 6)]
    got: dict[int, int] = {}
    for m in pattern.finditer(src.read_text(errors="replace")):
        idx = int(m.group(1), 8)
        val = int(m.group(2), 8)
        if idx in got and got[idx] != val:
            print(f"FAIL {name}: слово {idx:04o} имеет два разных значения")
            return False
        got[idx] = val
    if len(got) != 1024:
        print(f"FAIL {name}: найдено {len(got)} слов, ожидалось 1024")
        return False
    bad = [(i, words[i], got[i]) for i in range(1024) if words[i] != got[i]]
    if bad:
        print(f"FAIL {name}: {len(bad)} расхождений, первое: "
              f"слово {bad[0][0]:04o} дамп={bad[0][1]:016o} текст={bad[0][2]:016o}")
        return False
    print(f"OK {name}: все 1024 слова совпадают с дампом")
    return True


def main() -> int:
    ok = True
    ok &= check("LO*SYN", ROOT / "src/LO_SYN.mad", ROOT / "build/LO_SYN.words", PAT_SYN)
    ok &= check("LO*GEN", ROOT / "src/LO_GEN.mad", ROOT / "build/LO_GEN.words", PAT_GEN)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
