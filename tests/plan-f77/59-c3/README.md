# Тест 59-C3: самодостаточный патч `*TRANS` исполняет наш код

Этот каталог превращает доказательство C3 (`docs/plan-f77-full/logs/f77_30_59_c3_selfcontained.txt`)
в воспроизводимый репозиторный тест. Проверяется, что пропатченный C-симулятор
`dispak` **без единой `BESM6_REDIRECT_*`-переменной** исполняет наши слова через
путь `*TRANS` монитора-80 и печатает `OUR-CODE-RAN-7391`.

Подробный рецепт, точные слова и адреса, границы доказанного:
`docs/plan-f77-full/60-patched-trans-recipe.md`.

## Запуск

```sh
tests/plan-f77/59-c3/run.sh
```

Полный прогон (сборка симулятора и три варианта) занимает около минуты.
Ожидаемый хвост вывода:

```
  [PASS] main: rc=0 marker=True banner=False patch_hooks=True (...)
  [PASS] zero9: rc=0 marker=False banner=False patch_hooks=True (...)
  [PASS] diskmarker: rc=0 marker=False banner=True patch_hooks=True (...)
  [PASS] system disk 2148 unchanged (sha256 75617c04fee7d90d...)
RESULT: PASS (3/3 checks)
```

Для отладки: `run.sh --keep --verbose` (рабочий каталог не удаляется, видны строки
консоли и trace-хуки). Чтобы не собирать симулятор: `DISPAK_C3_BIN=/path/to/dispak-c3 run.sh`
или `run.sh --no-build`. Опция `--no-diskmarker` отключает третий вариант.

## Что внутри

| путь | назначение |
|:--|:--|
| `run.sh` | главный runner: рабочий каталог, сборка, копирование дисков, вызов `run.py` |
| `run.py` | харнесс: пишет зоны диска 2148, запускает deck, проверяет консоль и trace |
| `deck.b6` | deck с `*TRANS:OURMRK*,,411744` |
| `data/*.hex` | слова каталога, тела и зоны N+2 текстом (по одному 6-байтному слову на строку) |
| `patches/{defs.h,cu.c}.patch` | эталонные diff C2 -> C3 для справки |
| `src/` | уже пропатченный исходник `dispak` плюс `besmtool`, `disbesm6` (GPL-2, см. `src/COPYING`) |

Бинарники и образы дисков в репозиторий **не** кладутся: `run.sh` собирает `dispak`
из `src/` и копирует диски 2048/2053/2099/2148 из `/usr/local/share/besm6`
(или из `$BESM6_DISK_SHARE`) в приватный рабочий каталог под `${TMPDIR:-/var/tmp}`.
Хеш системного диска 2148 проверяется до и после прогона.

## Варианты

1. `main`: пишем `body.hex`, ждём маркер `OUR-CODE-RAN-7391`, баннера нет.
2. `zero9`: слово 9 тела обнулено, маркера нет (A/B: печать идёт именно из нашего кода).
3. `diskmarker`: в теле на диске другой GOST-маркер `BANNER-DISK-7391`, он и печатается
   (доказательство, что слова приходят с диска, а не из константы в исходнике).

Все три варианта дополнительно требуют в stderr оба trace-хука `C3PATCH pc=...` и
`C3: loaded 11 body words from disk 2148 zone 01745 ...`.
