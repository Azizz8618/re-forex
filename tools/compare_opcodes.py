#!/usr/bin/env python3
"""Прототип opcode-сверки (02-madlen-extension.md §3.3).

Сравнивает 6-битное поле КОП (и 3-бит ИР) каждой 24-битной половины слова,
игнорируя 15-бит поле АДР.  Это устойчиво к перенумерации меток и ловит
реальную семантическую поломку (замену операции).

В репозитории re-forex этого инструмента НЕТ — он описан в плане как
"новый tools/compare_opcodes.py".  Здесь он создан ТОЛЬКО в прототипе.
"""
import sys
from pathlib import Path

def load(path):
    d = Path(path).read_bytes()
    return [int.from_bytes(d[i:i+6], 'big') for i in range(0, len(d), 6)]

def halves(w):
    hi, lo = w >> 24, w & 0xFFFFFF
    return ((hi >> 15) & 0x3F, (lo >> 15) & 0x3F)  # (КОП_hi, КОП_lo)

def compare(gold, patch, ignore=()):
    diffs = []
    n = min(len(gold), len(patch))
    for i in range(n):
        if i in ignore:
            continue
        a, b = halves(gold[i]), halves(patch[i])
        if a != b:
            diffs.append((i, a, b))
    if len(gold) != len(patch):
        diffs.append(('LEN', len(gold), len(patch)))
    return diffs

def main():
    g = load('build/LO_GEN.words')
    # A: эталон vs эталон — ожидаем 0 различий
    d0 = compare(g, g)
    print(f"A gold-vs-gold: opcode diffs = {len(d0)}")
    # B: одно изменение КОП — должно быть найдено
    p = list(g); w = p[100]; p[100] = (w & ~(0x3F << 15)) | (0o12 << 15)
    d1 = compare(g, p)
    print(f"B one-opcode-change at 0144: diffs = {len(d1)} first = {d1[0] if d1 else None}")
    # C: вставка N слов в таблицу 0532..0623 сдвигает всё после неё
    for n in (10, 20, 60):
        ins = list(g[:0o532]) + [0]*n + list(g[0o532:1024-n])
        d2 = compare(g, ins)
        shifted = sum(1 for i, _, _ in d2 if isinstance(i, int))
        print(f"C insert {n} words @0532: len={len(ins)} opcode diffs={len(d2)} (shifted={shifted})")
    # D: вставка в автомат LO_SYN 1517..1777
    s = load('build/LO_SYN.words')
    for n in (10, 20, 60):
        ins = list(s[:0o1517]) + [0]*n + list(s[0o1517:1024-n])
        d3 = compare(s, ins)
        print(f"D insert {n} words @1517 (LO_SYN): opcode diffs={len(d3)}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
