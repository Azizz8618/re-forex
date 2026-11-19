#!/usr/bin/env python3
"""Парсер таблицы системных вызовов (экстракодов) из rukava.be и книги Тюрина.

КЛАССИФИКАЦИЯ КОДОВ (критическое правило): экстракоды — только 050..077.
Коды 020..047 (*20, *21, *33, *36, *46, *47 и др.) — обычные КОМАНДЫ БЭСМ-6;
они НЕ требуют расшифровки из rukava.be или книги Тюрина.
См. ``classify_opcode()``.

АВТОРИТЕТНОЕ УТОЧНЕНИЕ (2026-11-19): формат команды определяется 20-м разрядом
полуслова (в 0-based это бит 19), см. ``CmdSheet.md:17/96``.  Наши машинные
слова имеют «1-я структура ТО IX, 20-й разряд=0 (в 0-based это бит 19)» — это
первая структура (короткий формат), а не вторая.  ``besm6tape.py:84`` проверяет
тот же 20-й разряд (``(h >> 19) & 1``), поэтому его проверка корректна; прежняя
формулировка «off-by-one баг, проверяется бит 20» была неверной (смешение
1-based и 0-based нумерации разрядов).

Мнемоники в исходниках — латинские имена МАДЛЕН: 020 = APX (сбр, упаковка
битов по маске), 021 = AUX (рзб, разборка битов по маске), 033 = EXT (увв,
управление вводом-выводом), 036 = ASN (сда, сдвиг по адресу), 046/047 —
неиспользованные коды (имени в МАДЛЕН нет, остаются ``*46``/``*47``).  Имена
«э20/э21/счп/соп/э47/втбрз» — внутренние заглушки дизассемблеров
(LONG_BEMSH/SHORT_BEMSH; ``disbesm6.c`` строки 109–110 и 83–84 закомментированы);
«втбрз» — имя подпрограммы gens1.be, а не мнемоника opcode.  Источники:
``CmdSheet.md:48,49,40,52``, ``disbesm6.c:61,62,72,75,83,84``.

АРГУМЕНТ ASN (036), ФОРМУЛИРОВКА МОНИТОР-80: ``,ASN,64+N`` — сдвиг **вправо**
на N, ``,ASN,64−N`` — сдвиг **влево** на N.  Число в адресе — НЕ весь адрес, а
``N = EA[7:1]`` (младшие 7 разрядов адреса, ``Besm6_Instruction_Set.md §6``):
например ``4037B`` даёт ``N=0o37(31)=64−33`` ⇒ влево на 33.  См.
``asn_shift()`` / ``make_asn_comment()``.

ЭКСТРАКОДЫ 060/061/070/071: по ``Besm6_Instruction_Set.md §6`` (таблица
«Extracodes») 060 = I/O control (input), 061 = output, 070 = Memory/register
dump, 071 = Debug output.  Конкретные информационные слова наших вхождений в
``rukava.be``/Тюрине не описаны — сохраняется пометка «НЕ НАЙДЕНО ни в
rukava.be, ни в Тюрине-1985», к ней добавлен КЛАСС экстракода и контекстная
интерпретация информационного слова (адрес буфера/устройства либо
адрес/объём дампа).

033 В ПОЛЬЗОВАТЕЛЬСКОМ ГЕНЕРАТОРЕ КОДА: ``EXT`` (увв) — привилегированная
команда ОС (1-я структура); в ``LO*GEN`` то же число 033 — ``STOP`` (2-я
структура, Format 2), останов скомпилированной программы, выдаваемый в
объектный модуль [``Besm6_Instruction_Set.md §6; CmdSheet.md:41``].  В МАДЛЕН
STOP пишется сырым ``,33,`` — мнемоника ``EXT`` в ``LO*GEN`` заменена на ``33``.

Первичный источник: /home/azizz/Yandex.Disk/re-dispak/rukava.be,
раздел 1.4 «ПЕРЕЧЕНЬ СИСТЕМНЫХ ВЫЗВОВ (ЭКСТРАКОДОВ)».

Вторичный источник: /home/azizz/Yandex.Disk/re-dispak/docs/tyurin1985/extract-codes.json
(описания экстракодов из OCR книги В. Ф. Тюрина «Операционная система
ДИСПАК», 1985, Приложение П и §2.4).  Приоритет: rukava.be, затем Тюрин.

Выбор источника: ``--source rukava|tyurin|all`` (по умолчанию ``all``).

Строки таблицы имеют вид::

    *| Э50 0000     | SIN                          |   263|
    *| Э53 0041     | УСТАНОВКА ...                |   204|
    *|              | ПАКЕТЕ ОПЕРАЦИОННОЙ ...      |      |

Продолжения описаний (пустая колонка кода) приклеиваются к предыдущей
записи.  Ключ словаря — пара (код, информационное слово), например
``('Э50', '0131')``; значение — кортеж ``(описание, страница, номер_строки)``.

Примеры::

    python3 tools/extract_codes.py --list
    python3 tools/extract_codes.py --find Э57/1263
    python3 tools/extract_codes.py --find 'Э53 0041'
    python3 tools/extract_codes.py --find Э57/1263 --source tyurin
    python3 tools/extract_codes.py --json
    python3 tools/extract_codes.py --scan --source all
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_SOURCE = Path("/home/azizz/Yandex.Disk/re-dispak/rukava.be")
DEFAULT_TYURIN = Path("/home/azizz/Yandex.Disk/re-dispak/docs/tyurin1985/extract-codes.json")
SOURCES = ("rukava", "tyurin", "all")

# ── Классификация кодов: экстракоды (050–077) vs команды (020–047) ────────────
# КРИТИЧЕСКОЕ ПРАВИЛО: в ДИСПАКе экстракоды — только коды 050..077.
# Коды 020..047 — обычные КОМАНДЫ БЭСМ-6.  Формат определяется 20-м разрядом
# полуслова (в 0-based это бит 19): 0 → 1-я структура ТО IX (короткий адрес,
# CmdSheet.md:17); 1 → 2-я структура (полный адрес, CmdSheet.md:96).
# besm6tape.py:84 проверяет тот же 20-й разряд ((h >> 19) & 1) — корректно.
# Мнемоники: APX/AUX/EXT/ASN; *46/*47 остаются (в МАДЛЕН имени нет).
# Источники: CmdSheet.md:48,49,40,52; disbesm6.c:61,62,72,75,83,84.
# Значение: (MADLEN-мнемоника, имя/смысл, ссылка на источник).

# Латинские мнемоники МАДЛЕН, пришедшие на смену *NN.  Машинное слово НЕ меняется:
# opcode APX/AUX/EXT/ASN — это биты 0x010000/0x011000/0x01b000/0x01e000,
# те же, что у *20/*21/*33/*36 (disbesm6.c:61,62,72,75; маска 0x0bf000).
MNEMONIC_OPCODES: Dict[str, str] = {
    "APX": "20", "AUX": "21", "EXT": "33", "ASN": "36",
}
OPCODE_MNEMONICS: Dict[str, str] = {v: k for k, v in MNEMONIC_OPCODES.items()}

# Каноническая формулировка формата: 20-й разряд (1-based) = бит 19 (0-based).
FORMAT_LABEL = "1-я структура ТО IX, 20-й разряд=0 (в 0-based это бит 19)"

COMMAND_OPCODES: Dict[str, Tuple[str, str, str]] = {
    # 1-я структура ТО IX (20-й разряд=0; CmdSheet.md:48,49,40,52 / disbesm6.c)
    "20": ("APX", "сбр/APX", "CmdSheet.md:48; disbesm6.c:61"),
    "21": ("AUX", "рзб/AUX", "CmdSheet.md:49; disbesm6.c:62"),
    "22": ("utc", "мода", "besm6tape.py:44,48"),
    "23": ("wtc", "мод", "besm6tape.py:44,48"),
    "24": ("vtm", "уиа", "besm6tape.py:44,48"),
    "25": ("utm", "слиа", "besm6tape.py:44,48"),
    "26": ("uza", "по", "besm6tape.py:44,48"),
    "27": ("u1a", "пе", "besm6tape.py:44,48"),
    "30": ("uj", "пб", "besm6tape.py:45,49"),
    "31": ("vjm", "пв", "besm6tape.py:45,49"),
    "32": ("ij", "выпр", "besm6tape.py:45,49"),
    "33": ("EXT", "увв/EXT", "CmdSheet.md:40; disbesm6.c:72"),
    "34": ("vzm", "пио", "besm6tape.py:45,49"),
    "35": ("v1m", "пино", "besm6tape.py:45,49"),
    "36": ("ASN", "сда/ASN", "CmdSheet.md:52; disbesm6.c:75"),
    "37": ("vlm", "цикл", "besm6tape.py:45,49"),
    # 040–045 — обычные команды первой структуры
    "40": ("ati", "уи", "besm6tape.py:26,37"),
    "41": ("sti", "уим", "besm6tape.py:26,37"),
    "42": ("ita", "счи", "besm6tape.py:26,37"),
    "43": ("its", "счим", "besm6tape.py:26,37"),
    "44": ("mtj", "уии", "besm6tape.py:26,37"),
    "45": ("j+m", "сли", "besm6tape.py:26,37"),
    # 046/047 — неиспользованные коды (disbesm6.c:83–84 закомментировано)
    "46": ("*46", "неиспользованный код", "disbesm6.c:83 (закомментировано)"),
    "47": ("*47", "неиспользованный код", "disbesm6.c:84 (закомментировано)"),
}

# Пометка формата для канонических комментариев (все коды — 1-я структура).
COMMAND_LABELS: Dict[str, str] = {
    "20": FORMAT_LABEL,
    "21": FORMAT_LABEL,
    "33": FORMAT_LABEL,
    "36": FORMAT_LABEL,
    "46": FORMAT_LABEL,
    "47": FORMAT_LABEL,
}

# Значение команды и интерпретация её аргумента; источник — в ``command_ref()``.
COMMAND_STATEMENTS: Dict[str, str] = {
    "20": ("APX (сбр): упаковка битов по маске; аргумент — маска: TEXT/GOST слово, "
           "адрес слова-маски или immediate-код [monitor80-re/permanent/paramt%.masm:365; "
           "star%.masm:258,490] (НЕ адрес данных), пример «сборка, Л»"),
    "21": ("AUX (рзб): разборка битов по маске; аргумент — маска: TEXT/GOST слово, "
           "адрес слова-маски или immediate-код [monitor80-re/permanent/paramt%.masm:365; "
           "star%.masm:258,490] (НЕ адрес данных)"),
    "33": ("EXT (увв): привилегированная команда ОС 1-й структуры, управление "
           "вводом-выводом; в пользовательском генераторе кода (LO*GEN) 033 — "
           "STOP (2-я структура, Format 2), останов скомпилированной программы, "
           "выдаваемый в объектный модуль [Besm6_Instruction_Set.md §6; "
           "CmdSheet.md:41]"),
    "36": ("ASN (сда): сдвиг по адресу; N = EA[7:1] (младшие 7 разрядов адреса), "
           ",ASN,64+N — сдвиг вправо, ,ASN,64−N — влево "
           "[Besm6_Instruction_Set.md §6; monitor80-re/chekjob/mvstack.asm:17] "
           "(immediate, НЕ весь адрес), группа Л"),
    "46": "*46: неиспользованный код по ТО IX; аргумент не интерпретируется",
    "47": "*47: неиспользованный код по ТО IX; аргумент не интерпретируется",
}

# Интерпретация конкретного операнда (аргумента) в строке команды — для явной
# записи в комментарий вида «; GATAD = ...».  Для 036 используется явная
# формула Монитор-80 (см. ``make_asn_comment()``), а не общая заметка.
ARGUMENT_NOTES: Dict[str, str] = {
    "20": "адрес слова-маски (не адрес данных)",
    "21": "адрес слова-маски (не адрес данных)",
    "33": "код устройства (привилегированная операция, не адрес)",
    "36": ("N=EA[7:1] (младшие 7 разрядов адреса); ,ASN,64+N — вправо, "
           ",ASN,64−N — влево (не весь адрес)"),
}

# ── КЛАССЫ АРГУМЕНТОВ КОМАНД 020 (APX) / 021 (AUX) ──────────────────────────
# Запрос пользователя (2026-11-19): «аргументы команд 020 и 021 нередко
# работают с текстом».  Один и тот же формат «,APX,АРГ» / «,AUX,АРГ» несёт три
# разных по природе аргумента — классификация обязательна для каждого из
# 307 вхождений APX/AUX в src/*.mad и src/lib21/*.mad (см.
# logs/apx_aux_args_audit.txt):
#
#   * ``mask-word (text)`` — НЕ адрес: 8-символьное TEXT/ISO/GOST слово,
#     упакованное в машинное слово и используемое КАК МАСКА.  Примеры:
#     OCT-слово ``0160 3407 0160 34`` [monitor80-re/permanent/star%.masm:490],
#     то же слово по адресу ``*0353B`` [paramt%.masm:365], литералы
#     ``=6H'7''7''7''7''7'''`` [edit%%%.asm:996], ``=:0000 3703``, ``=1740``.
#   * ``immediate-code`` — код/счётчик в младших разрядах: AUX 25B, 43B, 44B
#     в DATAPR/OCTTDEC (формат даты DD MON 7Y); символические DV043=MONTHFI,
#     DV044=DATE2, DV025=PREPDAT (src/FOREX_DECODER_DISASM.mad:67,72,76).
#   * ``address`` — адрес слова-маски (5-значное восьмеричное либо символи-
#     ческая метка),content которого — маска; НЕ адрес данных.
#     Пример: ``APX,AC153D`` [src/LO_GEN.mad:631].
#
# Класс вычисляется по исходному токену и его разрешённому значению (EQU):
# литеральная форма `=...`, `6H...`, `:` или имя ETX*/TL*/*MSK*/*MAS* ⇒ текст;
# малое восьмеричное (≤0o7777) без литеральной формы ⇒ immediate-код;
# остальное ⇒ адрес.
#
# ПРОВЕРКА КОДИРОВОК ЧЕРЕЗ DTRAN (2026-11-19, см. docs/19-dtran-text-encodings.md):
# файл `-D` задаёт `iso:/gost:/itm:/text:<octal offsets>` (monitor80-re/*.dtr),
# но эти команды действуют только в Pascal-бэкендах.  Для DMS-модулей авторитетно
# auto-обнаруженное `,TEXT, 8H...`.  Полный кросс-чек ключевых констант делаёт
# `tools/dtran_text.py --audit`; он же показывает, что `gost:` dtran (8 бит/байт)
# на наших 6-битных TEXT-словах даёт «мусор», а настоящие GOST-константы DATAPR
# (S5:7712-7731) читаются только `-D gost:`.  Поэтому «GOST '…'» в наших
# комментариях — это 8 шестибитных группы по gost10859.h, а НЕ dtran -D gost.

APX_AUX_ARG_CLASSES: Tuple[str, ...] = (
    "mask-word (text)", "immediate-code", "address",
)

# Имена токенов, которые в исходниках явно объявлены TEXT/ISO/GOST-литералами
# (EQU `=6H...`, `=:...`, `=NNNN NNNN`; роль «литерал (TEXT/OCT/GOST/ISO)»).
TEXT_MASK_TOKENS: frozenset = frozenset({
    "OXMSK", "DYMSK", "YMASK", "TMASK", "MSK",
})

# Шаблоны явной интерпретации аргумента для каждого класса.  Формулировки
# совпадают с требованием задания: «маска = TEXT/GOST слово … [источник],
# НЕ адрес данных» и «аргумент = код DD из даты (младшие разряды), не адрес».
APX_AUX_ARG_NOTES: Dict[str, str] = {
    "mask-word (text)": (
        "маска = TEXT/GOST слово {value} "
        "[monitor80-re/permanent/star%.masm:490; "
        "monitor80-re/permanent/paramt%.masm:365; "
        "monitor80-re/permanent/edit%%%.asm:996], НЕ адрес данных"
    ),
    "immediate-code": (
        "аргумент = код DD из даты (младшие разряды) = {value}, не адрес "
        "[besmmons/system1.txt:7663,7682,7700; "
        "src/FOREX_DECODER_DISASM.mad:67,72,76,164,184,213]"
    ),
    "address": "адрес слова-маски (не адрес данных)",
}

_MASK_PREFIXES = ("ETX", "TL", "MAS", "MASC")
# Имена, которые в EQU объявлены АДРЕСОМ ячейки/константы (не кодом):
#   AC153D ,EQU, 53257B  . адрес ячейки/константы в резидентной памяти
#   AC2254 ,EQU, 2254B   . адрес ячейки/константы в резидентной памяти
#   CA7017 ,EQU, 7017B   . опк 20 — адрес слова-маски
ADDR_PREFIXES = ("AC", "CA", "C")
# Имена, которые в EQU объявлены кодом/индексом/аргументом экстракода:
#   DV043 ,EQU, 43B  . индекс MONTHFI;  DV025 ,EQU, 25B . AUX 25B в PREPDAT
#   AU121 ,EQU, 121B . операнд AUX (литерал); EX0326 ,EQU, 326B . аргумент экстракода
IMMEDIATE_PREFIXES = ("DV", "SC", "EX", "AU", "AA")


def classify_apx_aux_argument(token: str, info: str) -> str:
    """Класс аргумента команды 020 (APX) / 021 (AUX).

    См. ``APX_AUX_ARG_CLASSES``.  Решение принимается по двум признакам:
    исходное имя ``token`` (роль из EQU) и разрешённое значение ``info``.
    Ни один из них не является адресом данных: это либо текстовая маска,
    либо immediate-код, либо адрес слова-маски.
    """
    t = str(token).strip().upper().rstrip("-")
    i = str(info).strip()
    # 1. Явная литеральная форма или имя TEXT/GOST-литерала → текстовая маска.
    if i.startswith("=") or "6H" in i.upper() or i.startswith(":"):
        return "mask-word (text)"
    if t in TEXT_MASK_TOKENS or t.startswith(_MASK_PREFIXES):
        return "mask-word (text)"
    core = i[:-1] if i.endswith("B") else i
    small = core.isdigit() and int(core, 8) <= 0o7777
    # 2. Имена, явно объявленные адресом ячейки, — адрес слова-маски даже
    #    если значение 4-значное (AC2254=2254B, CA7017=7017B).
    if t.startswith(ADDR_PREFIXES):
        return "address"
    # 3. Код/индекс/счётчик в младших разрядах (DV043=43B, DV025=25B,
    #    AU121=121B, EX0326=326B и т.п.), не адрес.
    if small and t.startswith(IMMEDIATE_PREFIXES):
        return "immediate-code"
    # 4. Всё остальное (5-значный адрес или символическая метка) → адрес.
    return "address"


def apx_aux_argument_note(token: str, info: str) -> str:
    """Явная интерпретация аргумента APX/AUX для встроенного комментария.

    ``info`` может прийти как из EQU с суффиксом ``B`` (``326B``), так и
    разрешённым ``scan_sources()`` числом (``326``) — курс восьмеричной
    системы один и тот же, поэтому суффикс приводится к единой форме.
    """
    cls = classify_apx_aux_argument(token, info)
    value = str(info).strip() or str(token).strip()
    if value.endswith("B") and value[:-1].isdigit():
        value = value[:-1]
    return f"{token} = " + APX_AUX_ARG_NOTES[cls].format(value=value)


def asn_shift(info: str) -> Tuple[str, int, int, str, str]:
    """Разложить информационное слово ASN по правилам Монитор-80.

   Возвращает ``(формула, N, k, направление)`` где формула имеет вид
   ``N=0o37(31)=64−33 ⇒ ,ASN,64-33 — сдвиг ВЛЕВО на 33``.  ``N = EA[7:1]`` —
   младшие 7 разрядов адреса (``Besm6_Instruction_Set.md §6``), ``k`` — величина
   сдвига: ``,ASN,64+N`` ⇒ вправо, ``,ASN,64−N`` ⇒ влево.
   """
    n = int(str(info).strip(), 8) & 0o177
    if n >= 64:
        k, madlen, word = n - 64, f"64+{n - 64}", "ВПРАВО"
        decomp = f"64+{k}"
    else:
        k, madlen, word = 64 - n, f"64-{64 - n}", "ВЛЕВО"
        decomp = f"64\u2212{k}"  # U+2212 — минус в формулировке Монитор-80
    formula = (f"N=0o{format(n, 'o')}({n})={decomp} ⇒ ,ASN,{madlen} "
               f"— сдвиг {word} на {k}")
    return formula, n, k, madlen, word


def make_asn_comment(info: str) -> str:
    """Явный комментарий ASN с формулой Монитор-80 для конкретного адреса."""
    formula, *_ = asn_shift(info)
    return (f". ASN: {info}B → {formula} "
            f"[monitor80-re/chekjob/mvstack.asm:17; Besm6_Instruction_Set.md §6]")


# Класс экстракода по ``Besm6_Instruction_Set.md §6`` (таблица «Extracodes»)
# для кодов, конкретные информационные слова которых отсутствуют в справочниках.
EXTRACT_CLASSES: Dict[str, Tuple[str, str]] = {
    "Э60": ("I/O control (input)", "адрес буфера/устройство (контекст)"),
    "Э61": ("I/O control (output)", "адрес буфера/устройства вывода (контекст)"),
    "Э70": ("Memory/register dump", "адрес/объём дампа (контекст)"),
    "Э71": ("Debug output", "адрес/объём отладочных данных (контекст)"),
}


def make_extract_class_comment(code: str, info: str) -> str:
    """Комментарий экстракода 060/061/070/071: класс +Context + уточнение."""
    cls, context = EXTRACT_CLASSES.get(code, ("неописанный экстракод", "адрес/данные"))
    return (f". {code} {info} = {cls} [Besm6_Instruction_Set.md §6]; "
            f"информационное слово {info} — {context}; "
            "НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985 "
            "(конкретное информационное слово не описано в справочниках)")

def is_long_halfword(h: int) -> bool:
    """Формат 24-битного полуслова по 20-му разряду (бит 19 в 0-based).

    20-й разряд=0 → 1-я структура ТО IX (CmdSheet.md:17); =1 → 2-я структура
    (CmdSheet.md:96).  ``besm6tape.py:84`` проверяет тот же разряд
    (``(h >> 19) & 1``); прежняя формулировка «off-by-one, бит 20» была
    ошибкой 1-based/0-based нумерации.  Наши слова: 20-й разряд=0.
    """
    return bool((h >> 19) & 1)


def classify_opcode(code_octal: str,
                    halfword: Optional[int] = None) -> Tuple[str, str]:
    """Классифицировать восьмеричный код команды/экстракода.

    Формат определяется 20-м разрядом (битом 19 в 0-based, см.
    ``is_long_halfword()``).  Наши слова имеют 20-й разряд=0 → 1-я структура
    ТО IX; ``besm6tape.py:84`` проверяет тот же разряд корректно.

    Возвращает ``(категория, мнемоника)``:
      * ``('extract', 'Э50')``   — настоящий экстракод, код 050..077;
      * ``('command', 'сбр/APX')`` — команда БЭСМ-6, код 020..047
        (020=сбр/APX, 021=рзб/AUX, 033=увв/EXT, 036=сда/ASN,
        046/047=неиспользованные);
      * ``('unknown', '')``      — код вне диапазонов 020..077.

    >>> classify_opcode('36')
    ('command', 'сда/ASN')
    >>> classify_opcode('050')
    ('extract', 'Э50')
    """""
    raw = str(code_octal).strip().upper().lstrip("Э*")
    try:
        value = int(raw, 8)
    except ValueError:
        return ("unknown", "")
    if 0o20 <= value <= 0o47:
        norm = format(value, "02o")
        # 20-й разряд (бит 19 в 0-based), НЕ бит 20.  Без полуслова считаем
        # 1-ю структуру ТО IX; явная 2-я структура не меняет категорию, но
        # отключает подстановку имени команды.
        short = halfword is None or not is_long_halfword(halfword)
        mnemonic = (COMMAND_OPCODES.get(norm, (norm, norm, ""))[1]
                    if short else norm)
        return ("command", mnemonic)
    if 0o50 <= value <= 0o77:
        return ("extract", "Э" + format(value, "02o"))
    return ("unknown", "")


def command_ref(code_octal: str) -> str:
    """Ссылка на таблицу, подтверждающую, что код — команда, а не экстракод."""
    norm = format(int(str(code_octal).strip().lstrip("Э*"), 8), "02o")
    return COMMAND_OPCODES.get(norm, (norm, norm, "besm6tape.py"))[2]


def make_command_comment(code_octal: str, info: str = "") -> str:
    """Канонический комментарий для команды 020/021/033/036/046/047.

    Формулировка формата (1-я структура ТО IX, 20-й разряд=0 == бит 19 в
    0-based), значение команды, интерпретация аргумента и источник —
    обязательны:

      . опк 20 (1-я структура ТО IX, 20-й разряд=0 (в 0-based это бит 19)) = APX (сбр): упаковка битов по маске; аргумент — адрес слова-маски [monitor80-re/permanent/paramt%.masm:365; star%.masm:258,490] [CmdSheet.md:48; disbesm6.c:61]

    Имена «э20/э21/счп/соп/э47/втбрз» из дизассемблеров не используются:
    «втбрз» — имя подпрограммы gens1.be, а не мнемоника opcode.
    """
    kind, _mnemonic = classify_opcode(code_octal)
    if kind != "command":
        return ""
    norm = format(int(str(code_octal).strip().lstrip("Э*"), 8), "02o")
    # Для ASN с известным информационным словом — явная формула Монитор-80.
    if norm == "36" and info:
        return make_asn_comment(info)
    fmt = COMMAND_LABELS.get(norm, FORMAT_LABEL)
    statement = COMMAND_STATEMENTS.get(norm, "неизвестная команда")
    ref = command_ref(norm)
    if info:
        return f". опк {norm} ({fmt}) {info} = {statement} [{ref}]"
    return f". опк {norm} ({fmt}) = {statement} [{ref}]"

# Ключ: (Э50, 0131).  Значение: (описание, страница, строка файла).
Entry = Tuple[str, str, int]
CodeTable = Dict[Tuple[str, str], Entry]
TyurinData = Dict[str, Any]
# Унифицированная находка: (описание, страница, ссылка, имя_источника).
Found = Tuple[str, str, str, str]

ROW_RE = re.compile(
    r"^\*\|\s*(Э\d{2})(?:\s+([^\s|]+))?\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
CONT_RE = re.compile(r"^\*\|\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|\s*$")


def parse_table_rows(path: Path = DEFAULT_SOURCE) -> List[Tuple[str, str, str, str, int]]:
    """Все строки таблицы: (код, и.слово, описание, страница, линия).

    В таблице есть повторяющиеся ключи (например ``Э72 А`` встречается
    10 раз — разные операции выбираются другими параметрами), поэтому
    полный список строк хранится отдельно от словаря.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: List[Tuple[str, str, str, str, int]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = ROW_RE.match(line)
        if m:
            rows.append((
                m.group(1),
                m.group(2) or "",
                m.group(3).strip(),
                m.group(4).strip(),
                lineno,
            ))
            continue
        c = CONT_RE.match(line)
        if c and rows:
            extra = c.group(1).strip()
            if extra:
                code, info, desc, page, first = rows[-1]
                page2 = c.group(2).strip()
                rows[-1] = (code, info, (desc + " " + extra).strip(),
                            page or page2, first)
    return rows


def parse_table(path: Path = DEFAULT_SOURCE) -> CodeTable:
    """Словарь {(код, и.слово): (описание, страница, линия)}.

    Повторяющиеся строки с одним ключом объединяются: описания через
    « / », страницы через «, », линия берётся от первой строки.
    """
    table: CodeTable = {}
    for code, info, desc, page, lineno in parse_table_rows(path):
        key = (code, info)
        if key not in table:
            table[key] = (desc, page, lineno)
        else:
            old_desc, old_page, old_line = table[key]
            table[key] = (
                f"{old_desc} / {desc}" if desc not in old_desc else old_desc,
                f"{old_page}, {page}" if page and page not in old_page.split(", ") else old_page,
                old_line,
            )
    return table


def norm_info(info: str) -> str:
    """Нормализовать информационное слово: убрать суффикс B и ведущие нули.

    Числа в таблицы rukava.be записаны в восьмеричной системе (0000, 0131,
    1202, 7703), поэтому перевода в десятичную систему НЕ делаем: ``20`` и
    ``0020`` — одно и то же слово, а ``20B`` означает восьмеричное 20.
    """
    info = info.strip().rstrip("B").lstrip("0")
    return info or "0"


def lookup(table: CodeTable, code: str, info: str) -> Optional[Entry]:
    """Найти запись по коду/информационному слову (сравнение по восьмеричному значению)."""
    code = code.strip().upper()
    key = (code, norm_info(info))
    for (c, i), entry in table.items():
        if c == code and norm_info(i) == key[1]:
            return entry
    return None


def format_entry(code: str, info: str, entry: Optional[Entry]) -> str:
    if entry is None:
        return f"{code} {info} -> НЕ НАЙДЕНО в rukava.be"
    desc, page, lineno = entry
    return f"{code} {info} -> {desc} (стр.{page}) [rukava.be:{lineno}]"


# ---------------------------------------------------------------------------
# Второй источник: книга Тюрина (1985).
# ---------------------------------------------------------------------------

def load_tyurin(path: Path = DEFAULT_TYURIN) -> Optional[TyurinData]:
    """Загрузить JSON с описаниями экстракодов из книги Тюрина.

    Формат первого агента: ``{"Э057:0000": {"desc": ..., "page": 264,
    "confidence": ...}, ...}``.  Возвращает ``None``, если файл отсутствует
    или повреждён (тогда работает только rukava.be).
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return data


# Краткие названия экстракодов по указателю книги (используются как fallback
# по номеру кода, когда конкретное информационное слово в книге не найдено).
TYURIN_CODE_TITLES: Dict[str, str] = {
    "Э50": "СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A)",
    "Э51": "COS (ИР 051 A)",
    "Э52": "COS (ИР 052 A)",
    "Э53": "ARCTAN / СОБЫТИЯ И СВЯЗЬ МЕЖДУ ЗАДАЧАМИ (ИР 053 A)",
    "Э54": "ARCSIN (ИР 054 A)",
    "Э55": "LN (ИР 055 A)",
    "Э56": "EXP (ИР 056 A)",
    "Э57": "ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A)",
    "Э62": "СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A)",
    "Э63": "ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A)",
    "Э64": "УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A)",
    "Э73": "ВВОД МАССИВА С НОМЕРОМ N+1 В ПАМЯТЬ ЗАДАЧИ (ИР 073 A)",
    "Э76": "СВЯЗЬ БЭСМ-6 С ЭВМ М-6000 / Т-1600 (ИР 076 A)",
}


def _tyurin_entries(data: Optional[TyurinData]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Индекс записей Тюрина: (код, восьмеричное_слово) -> запись."""
    out: Dict[Tuple[str, str], Dict[str, Any]] = {}
    if not data:
        return out
    for key, val in data.items():
        if ":" not in key or not isinstance(val, dict):
            continue
        raw_code, raw_info = key.split(":", 1)
        code = "Э" + raw_code.lstrip("Э").lstrip("0")
        info = norm_info(raw_info)
        out[(code, info)] = val
    return out


def lookup_tyurin(data: Optional[TyurinData], code: str, info: str) -> Optional[Entry]:
    """Найти описание у Тюрина: сначала пара (код/слово), затем код целиком.

    Возвращает ``(описание, страница, 'tyurin1985')``.
    """
    if not data:
        return None
    code = code.strip().upper()
    entries = _tyurin_entries(data)
    hit = entries.get((code, norm_info(info)))
    if hit is not None:
        desc = str(hit.get("desc", "")).strip()
        page = str(hit.get("page", 264))
        if desc:
            return (desc, page, "tyurin1985")
    # Fallback по номеру экстракода: описание класса экстракодов из книги.
    title = TYURIN_CODE_TITLES.get(code)
    if title is not None:
        pages = [str(v.get("page", 264)) for (c, _), v in sorted(entries.items())
                 if c == code and v.get("page")]
        return (title, pages[0] if pages else "264", "tyurin1985")
    return None


def lookup_all(code: str, info: str, table: CodeTable,
               tyurin: Optional[TyurinData] = None,
               source: str = "all") -> Optional[Found]:
    """Унифицированный поиск с приоритетом rukava.be > Тюрин.

    ``source``: ``rukava`` — только rukava.be, ``tyurin`` — только Тюрин,
    ``all`` — оба (сначала rukava.be).
    """
    if source in ("rukava", "all"):
        entry = lookup(table, code, info)
        if entry is not None:
            return (entry[0], entry[1], f"rukava.be:{entry[2]}", "rukava.be")
    if source in ("tyurin", "all"):
        entry = lookup_tyurin(tyurin, code, info)
        if entry is not None:
            return (entry[0], entry[1], entry[2], "tyurin1985")
    return None


# ---------------------------------------------------------------------------
# Сканирование аннотированных МАДЛЕН-текстов.
# ---------------------------------------------------------------------------

EQU_RE = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9_#$]*)\s*,\s*EQU\s*,\s*(.*?)\s*(?:[.;].*)?$"
)
# Экстракод в мнемонике: *NN,ARG  (ARG — простой операнд, не метка/литерал).
OPCODE_RE = re.compile(
    r"(?<![A-Za-z0-9_*])\*([0-7]{2})(?![0-7])\s*,\s*([A-Za-z0-9_#$()+\-=:]+)"
)
# Латинская мнемоника МАДЛЕН: APX,AUX,EXT,ASN,ARG (вместо *NN,ARG).
LATIN_MNEMO_RE = re.compile(
    r"(?<![A-Za-z0-9_])(APX|AUX|EXT|ASN)(?![A-Za-z0-9_])\s*,\s*"
    r"([A-Za-z0-9_#$()+\-=:]+)"
)
# Экстракод в тексте: ЭNN ARG.
MNEMO_RE = re.compile(
    r"(?<![A-Za-z0-9_])Э([0-7]{2})(?![0-7])\s+([A-Za-z0-9_#$()+\-=:]+)"
)
NUMBER_RE = re.compile(r"^(?:0o)?([0-7]+)[bB]?$|^\d+$")


def resolve_equ(name: str, equs: Dict[str, str], seen: Optional[set] = None) -> Optional[str]:
    """Разрешить символическое информационное слово в восьмеричную строку.

    Поддерживаются восьмеричные (``502B``, ``0o502``), десятичные (``47``),
    символические ссылки и простые выражения ``A+B`` / ``A-B``.
    Возвращает ``None``, если разрешить значение нельзя (например TEXT-литерал).
    """
    if seen is None:
        seen = set()
    name = name.strip()
    if name in seen:
        return None
    seen.add(name)
    if name.startswith('-'):
        val = resolve_equ(name[1:], equs, seen)
        return ('-' + val) if val is not None else None
    raw = equs.get(name)
    if raw is None:
        return None
    raw = raw.strip()

    def atom(tok: str) -> Optional[int]:
        tok = tok.strip()
        if not tok:
            return None
        m = re.fullmatch(r"([0-7]+)[bB]", tok)
        if m:
            return int(m.group(1), 8)
        m = re.fullmatch(r"0o([0-7]+)", tok)
        if m:
            return int(m.group(1), 8)
        if re.fullmatch(r"\d+", tok):
            return int(tok)
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_#$]*", tok):
            sub = resolve_equ(tok, equs, seen)
            return int(sub, 8) if sub is not None else None
        return None

    # Унарный минус: -EDC008.
    if raw.startswith('-'):
        val = atom(raw[1:])
        return ('-' + format(val, 'o')) if val is not None else None
    # Простое выражение из двух операндов и одного + или -.
    m = re.fullmatch(r"([^+\-]+)([+\-])(.+)", raw)
    if m:
        a, op, b = atom(m.group(1)), m.group(2), atom(m.group(3))
        if a is not None and b is not None:
            return format(a + b if op == "+" else a - b, "o")
    val = atom(raw)
    return format(val, "o") if val is not None else None


def make_comment(code: str, info: str, table: CodeTable,
                 tyurin: Optional[TyurinData] = None,
                 source: str = "all") -> str:
    """Построить встроенный комментарий для одного кода.

    Для команд (020..047) расшифровка из rukava.be/Тюрина НЕ требуется —
    возвращается комментарий с пометкой «1-я структура ТО IX, 20-й разряд=0
    (в 0-based это бит 19)», значением команды и интерпретацией аргумента
    (CmdSheet/disbesm6).  Для экстракодов (050..077) — расшифровка по источникам.
    """
    kind, _mnemonic = classify_opcode(code)
    if kind == "command":
        return make_command_comment(code, info)
    entry = lookup_all(code, info, table, tyurin, source)
    if entry is None:
        norm = "Э" + format(int(str(code).lstrip("Э*"), 8), "02o")
        if norm in EXTRACT_CLASSES:
            return make_extract_class_comment(norm, info)
        return (f". {code} {info} = НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985 "
                "(информационное слово — адрес/данные)")
    desc, page, ref, _src = entry
    return f". {code} {info} = {desc}, стр.{page} [{ref}]"


def scan_line(line: str, equs: Dict[str, str]
              ) -> List[Tuple[str, str, str, str, str, str]]:
    """Коды с информационным словом в одной строке.

    Возвращает список ``(код, информационное_слово, исходный_токен,
    категория, мнемоника, найденная_мнёмоника)``.  ``найденная_мнёмоника`` —
    буквальный текст в исходнике: ``*36``, ``ASN`` и т.п.  Категория —
    ``extract`` (050..077), ``command`` (020..047) или ``unknown``.
    """
    out: List[Tuple[str, str, str, str, str, str]] = []
    # Не сканируем собственные комментарии вида ". Э57 6 = ...",
    # ". опк 36 (...)" или ". ASN: 4037B → ..." (иначе текст ",ASN,64-33"
    # внутри явной формулы выглядит как ещё одно вхождение команды).
    line = re.split(r"\s+\.\s+(?:Э[0-7]{2}|опк|ASN:)\s+", line, maxsplit=1)[0]
    for rx in (OPCODE_RE, LATIN_MNEMO_RE, MNEMO_RE):
        for m in rx.finditer(line):
            raw = m.group(2).strip()
            if not raw or "=" in raw or ":" in raw or "*" in raw:
                continue  # метка/литерал, а не информационное слово
            resolved = resolve_equ(raw, equs)
            if m.re is LATIN_MNEMO_RE:
                code = MNEMONIC_OPCODES[m.group(1)]
                found_mnem = m.group(1)
            else:
                code = m.group(1)
                found_mnem = "*" + code
            kind, mnemonic = classify_opcode(code)
            out.append(("Э" + code, resolved or raw, raw, kind, mnemonic, found_mnem))
    return out


def scan_sources(root: Path = Path("src"), table: Optional[CodeTable] = None,
                 tyurin: Optional[TyurinData] = None,
                 source: str = "all") -> List[Dict[str, object]]:
    """Просканировать ``src/*.mad`` и ``src/lib21/*.mad``."""
    if table is None:
        table = parse_table()
    found: List[Dict[str, object]] = []
    files = sorted(root.glob("*.mad")) + sorted((root / "lib21").glob("*.mad"))
    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        equs: Dict[str, str] = {}
        for line in lines:
            m = EQU_RE.match(line)
            if m:
                equs[m.group(1)] = m.group(2)
        for lineno, line in enumerate(lines, 1):
            for code, info, raw, kind, mnemonic, found_mnem in scan_line(line, equs):
                # Строки, где латинская мнёмоника уже была до правки и нет
                # аннотации «. опк NN ...», НЕ являются объектом проверки
                # комментариев (как и до замены *NN → APX/AUX/EXT/ASN).
                # Явная формула Монитор-80 (". ASN: ... → ...") — тоже
                # объект проверки, наравне с каноническим ". опк 36 ...".
                if kind == "command" and ". опк " not in line and ". ASN: " not in line:
                    continue
                entry = (None if kind == "command"
                         else lookup_all(code, info, table, tyurin, source))
                arg_cls = (classify_apx_aux_argument(raw, info)
                           if code in ("Э20", "Э21") else None)
                found.append({
                    "file": str(path), "line": lineno, "code": code,
                    "info": info, "token": raw,
                    "argument_class": arg_cls,
                    "argument_note": (apx_aux_argument_note(raw, info)
                                      if arg_cls else None),
                    "kind": kind, "mnemonic": mnemonic,
                    "opcode_mnemonic": found_mnem,
                    "command_ref": command_ref(code) if kind == "command" else None,
                    "description": entry[0] if entry else None,
                    "page": entry[1] if entry else None,
                    "source_line": entry[2] if entry else None,
                    "source": entry[3] if entry else None,
                    "comment": make_comment(code, info, table, tyurin, source),
                })
    return found


def parse_query(q: str) -> Tuple[str, str]:
    q = q.strip().replace("/", " ").replace(",", " ")
    parts = q.split()
    code = parts[0].upper() if parts else ""
    info = parts[1] if len(parts) > 1 else ""
    return code, info


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", choices=SOURCES, default="all",
                    help="источник расшифровок: rukava, tyurin или all "
                         "(по умолчанию all: rukava.be, затем Тюрин)")
    ap.add_argument("--rukava", type=Path, default=DEFAULT_SOURCE,
                    help="путь к rukava.be (по умолчанию %(default)s)")
    ap.add_argument("--tyurin", type=Path, default=DEFAULT_TYURIN,
                    help="путь к JSON Тюрина (по умолчанию %(default)s)")
    ap.add_argument("--list", action="store_true", help="вывести всю таблицу")
    ap.add_argument("--find", metavar="Э57/1263",
                    help="найти код (формы: Э57/1263, 'Э53 0041', Э50)")
    ap.add_argument("--json", action="store_true", help="вывести таблицу в JSON")
    ap.add_argument("--scan", action="store_true",
                    help="просканировать src/*.mad и src/lib21/*.mad")
    ap.add_argument("--root", type=Path, default=Path("src"),
                    help="корень исходников для --scan (по умолчанию %(default)s)")
    args = ap.parse_args(argv)

    try:
        table = parse_table(args.rukava)
    except OSError as exc:
        print(f"ОШИБКА: не удалось прочитать {args.rukava}: {exc}", file=sys.stderr)
        return 2
    tyurin = load_tyurin(args.tyurin) if args.source in ("tyurin", "all") else None

    if args.scan:
        rows = scan_sources(args.root, table, tyurin, args.source)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            return 0
        extracts = [r for r in rows if r["kind"] == "extract"]
        commands = [r for r in rows if r["kind"] == "command"]
        hits = sum(1 for r in extracts if r["description"] is not None)
        for r in rows:
            if r["kind"] == "command":
                print(f"{r['file']}:{r['line']}: {r['code']} {r['info']} "
                      f"[{r['token']}] -> команда опк {r['code'].lstrip('Э*')} "
                      f"[{r['command_ref']}]")
                continue
            mark = "НАЙДЕНО" if r["description"] is not None else "не найдено"
            src = r["source"] or "-"
            print(f"{r['file']}:{r['line']}: {r['code']} {r['info']} "
                  f"[{r['token']}] -> {mark} [{src}]")
        print(f"\nВсего вхождений: {len(rows)}; экстракоды (050..077): "
              f"{len(extracts)} (расшифровано: {hits}, не найдено: "
              f"{len(extracts) - hits}); команды 1-й структуры (020..047): "
              f"{len(commands)} (источник: {args.source})", file=sys.stderr)
        return 0

    if args.json and not args.find:
        out = [
            {"code": code, "info": info, "description": desc,
             "page": page, "source_line": lineno, "source": "rukava.be"}
            for (code, info), (desc, page, lineno) in sorted(table.items())
        ]
        if tyurin:
            for (code, info), val in sorted(_tyurin_entries(tyurin).items()):
                out.append({"code": code, "info": info,
                            "description": val.get("desc", ""),
                            "page": val.get("page", 264),
                            "source_line": None, "source": "tyurin1985"})
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.find:
        code, info = parse_query(args.find)
        found = []
        for (c, i), entry in sorted(table.items()):
            if c == code and (not info or i == info or
                              (info.lstrip("0") and i.lstrip("0") == info.lstrip("0"))):
                found.append((c, i, f"{entry[0]} (стр.{entry[1]}) [rukava.be:{entry[2]}]"))
        # Добавляем результат из Тюрина, если пара ещё не найдена в rukava.be.
        if not found and tyurin:
            entry = lookup_tyurin(tyurin, code, info)
            if entry is not None:
                found.append((code, info,
                              f"{entry[0]} (стр.{entry[1]}) [{entry[2]}]"))
        if not found:
            print(f"Экстракод {args.find}: не найдено ни в rukava.be, ни у Тюрина")
            return 1
        for c, i, text in found:
            print(f"{c} {i} -> {text}")
        return 0

    if args.list or not args.json:
        for (code, info), entry in sorted(table.items()):
            print(format_entry(code, info, entry))
        print(f"\nВсего записей rukava.be: {len(table)}", file=sys.stderr)
        if tyurin:
            print(f"Записей у Тюрина: {len(_tyurin_entries(tyurin))} пар",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
