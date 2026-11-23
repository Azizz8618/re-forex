# Воспроизводимая сборка образа контура зоны 0o2350

Проверенный построитель перенесён из временного каталога в репозиторий:
`tools/build_zone2350_contour.py`. Это тот же код, что дал SIMH A/B/A в
`docs/83`, `docs/84`, `docs/86`; единственное изменение — явный `--out` вместо
жёстко заданного пути. Все входные фикстуры уже лежат в репозитории:

- `tests/plan-f77/84-wide-output/installer.py` (read-only импорт, генераторы O412C),
- `tests/plan-f77/69-full-emitted-body/o412d_words.hex` (хвост тела),
- `tests/plan-f77/65-m80-install/ovl_our.hex` (оверлей),
- `/usr/local/share/besm6/2048` (эталонная системная копия; только чтение).

Команда:

```
TMPDIR=/tmp/.private/azizz/opencode python3 tools/build_zone2350_contour.py base \
  --out /tmp/.private/azizz/opencode/zone2350-consolidated
```

Контрольная сумма получившегося образа (побайтово совпадает с этапом I/O и
baseline):

```
a98e81090d4b254554a0cd3f...  base (нормальный контур)
1f4431d177e02481aa70e22d...  zero body[0o41]   -> печать 01 вместо 21
a98e81090d4b254554a0cd3f...  restore
```

Заголовки зон SIMH: `w0=(phys<<36)|0x038ca3c918`,
`w1=0x000005f1c7800000`, `w2=0x0000410300000000`,
`w3` = end-around-carry checksum 1024 слов данных. Рецепт проверен на
заселённой зоне 4 (`docs/74-simh-verification.md` §3). Ошибка
`2048 НЕТ СОВП.КС … 02350` означает неверный `w3` — так падал FUNCTION‑этап,
пока не перешёл на этот построитель.

Целевая колода содержит только `*TRANS:OURMRK*,,412350`; карты тома пишут
`2048` (`docs/80-deck-2048.md`).
