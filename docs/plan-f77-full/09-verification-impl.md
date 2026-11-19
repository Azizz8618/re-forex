# 09 — Реализация системы верификации полной FORTRAN 77 (этап P8)

Дата: 19.11.2026. Изделие: **FOREX 5.00 / 19.11.2026 (re-forex)**, ветка `main`.
Документ описывает созданную инфраструктуру по ТЗ `docs/plan-f77-full/04-verification.md`.

## 1. Как запускать

```sh
cd /tmp/.private/azizz/opencode/re-forex
bash tests/run-f77-full.sh
echo "rc=$?"
```

Оркестратор — `tests/run-f77-full.sh` (исполняемый, `set -uo pipefail`). Время
прогона на рабочей машине — около 7 с (около 60 запусков dispak, из них 32 unit-дека и 15 проб gate).

Переопределения окружения (как в E5/E2):

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `DISPAK_BIN` | `/home/azizz/Yandex.Disk/dispak/build/dispak/dispak` | эмулятор dispak |
| `BESMTOOL` | `besmtool` | утилита записи зоны диска 2348 |
| `ETALON` | `/usr/local/share/besm6/2348` | эталонный диск (только читается) |
| `IMAGE` | `build/FOREX_PERSO_2300.bin` | образ PERSO зоны `0o2300` |
| `TIMEOUT` | `180` | таймаут одного прогона dispak, с |
| `TMPDIR` / `TMPROOT` | `/tmp/.private/azizz/opencode` | рабочий каталог (`mktemp -d`, удаляется по `trap`) |
| `F77_FULL_EXTERNAL=1` | выключено | включить прогон внешних Dhrystone/Whetstone (`.dub` из `besm6.net/examples`) |

При отсутствии dispak / `besmtool` / эталона / образа сценарий печатает
`ОЖИДАЕТСЯ: …`, пишет уровни как `ОЖИДАЕТСЯ` в логи и возвращает **0**
(ветка prerequisites сохранена по образцу `tests/run-f77-suite.sh`).

## 2. Что создано (зона владения P8)

```
tests/plan-f77-full/
├── unit/<ID>_<name>/       32 каталога: <deck>.b6 + <ID>_<name>.gold + options.txt
├── gold/REGISTRY.txt       32 gold-пары: ID|DIR|DECK|GOLD|SOURCE|REF
├── gold/*.gold             32 эталонных блока результата
├── cross/cases.txt         X01..X04 → 4 деков × 2 компилятора = 8 кросс-прогонов
├── real/cases.txt          R01 Глиссада, R02 решето, R03 Dhrystone, R04 Whetstone
├── negative/cases.txt      NC01..NC09 (ожидаемая диагностика / control)
└── gate/                   4 положительных F77-дека + gold (LISTDIR/IMPLICIT/ENDREAD/SAVE)
tests/run-f77-full.sh       оркестратор всех уровней + gate 20/20
logs/f77_full_*.txt         8 логов уровней и сводки
logs/f77_full.sha256        манифест SHA256 деков, gold, образов
docs/plan-f77-full/09-verification-impl.md  этот документ
```

Не трогались: `src/`, `include/`, `reference/`, `docs/drakon`, существующие
`tests/*.sh` (кроме нового `tests/run-f77-full.sh`), `checklist/STATUS.md`.

## 3. Что проверяет каждый уровень

### L0 — 32 unit-пробы (матрица A–K)

`docs/plan-f77-full/01-f77-standard-matrix.md` содержит 11 разделов **A–K**
(лексика … интринзики). По ним распределены 32 слота, каждый — отдельная дека
в `unit/<ID>_<name>/`:

| Раздел стандарта | ID проб | Конструкции |
|---|---|---|
| A Лексика | A01, A02 | fixed form (комментарий, продолжение кол. 6, метки); имена >6 знаков |
| B Типы | B01–B03 | INTEGER/REAL; DOUBLE PRECISION + `D22.15`; COMPLEX + `2F10.4` |
| C Выражения | C01, C02 | `**`, унарный минус, смешанные типы; `.GT./.AND./.NOT.` |
| D Присваивание | D01, D02 | численное; логическое (`L1`) |
| E Управление | E01–E04 | `GO TO`; логический `IF … GO TO`; `BLOCK IF`; `DO` с шагом −2 |
| F Описания | F01–F04 | `DIMENSION`/`DATA`; `PARAMETER`; `EXTERNAL`/`INTRINSIC`; `IMPLICIT NONE` (lowered) |
| G Подпрограммы | G01, G02 | внешняя `FUNCTION`; `SUBROUTINE` + `CALL` (by reference) |
| H Массивы | H01, H02 | 2D-массив, column-major; `COMMON`/`BLOCK DATA` (glkern) |
| I Строки | I01, I02 | Hollerith `4HABCD` + `A4`; `CHARACTER*10` + подстрока |
| J Ввод-вывод | J01–J05 | `WRITE(54,…)`; `L1`; `/`; `READ 10,X` + карта данных; list-directed lowered |
| K Интринзики | K01–K04 | `SQRT`/`ABS`; `AMOD`; `CABS`; `SQRT(2.0D0)` |

Все деки грузят `*perso:602300` (зона `0o2300`), содержат `PROGRAM …` и
`*forex`, чтобы тот же исходник компилировался `*FTN`/`*FORTRAN`. Баннер
`ВЕРСИЯ 2.02 ОТ 15.07.80` не является версией изделия: `normalize()` заменяет
его на `<BANNER>` вместе с нормализацией даты `DD.DD.DD → ##.##.##`; в блок
результата (`extract_result`, строки перед `КОНЕЦ ЗАДАЧИ`) он не входит.
FATAL-фильтр — тот же, что в E5 (`БЫЛИ ОШИБКИ|НЕДОПУСТИМ|ОШИБКА|ERR n|ОШ.
ТРАНСЛЯТОРА|ТИП ОП-ДА|ОТСУТСТВУЕТ|ИСПОРЧЕН|АТТ `). «Просто отсутствие ошибки»
успехом не считается: требуется непустой блок и побайтовое совпадение с gold.

### L1 — 32 gold-пары

`gold/REGISTRY.txt` задаёт 32 записи. Происхождение эталонов:

* **8 переиспользованы** из `tests/f77/suite/*.gold` (`base`, `blockif`,
  `do2d`, `dataparam`, `dpcomplex`, `intrinsics_ext`, `charhollerith`,
  `listio`); оркестратор дополнительно проверяет, что копия в `gold/` байтово
  равна оригиналу (`REUSED OK/FAIL` в логе).
* **18 новых** — по слотам матрицы, у которых не было готового gold.
* **6 с контролями E1** — `e1/precision/double`, `e1/precision/complex`,
  `e1/units/read_nounit`, `e1/units/write_u54`, `tests/forex-glissade`,
  `e1/strings/hollerith_format`.

Сравнение — побайтовое после нормализации даты/баннера; `diff gold/fact`
пишется в лог.

### L2 — кросс-сверка (8 прогонов)

Набор `X01 base`, `X02 do2d`, `X03 intrinsics_ext`, `X04 dpcomplex` → по два
прогона. Исходник вырезается между `*forex` и `*execute`, собирается дек с
`*system`, `*full list`, `*ftn` (`*name F<case>`) или `*fortran`
(`*name D<case>`) на диске 2048. Числа сравниваются regex
`[-+]?(\d+(\.\d*)?|\.\d+)([EDed][-+]?\d+)?` с `D→E`.

| Компилятор | Допуск | Дополнительно |
|---|---|---|
| `*FTN` (Fortran-ГДР) | `max(1e-6, 1e-5·max(\|x\|,\|y\|))` | совпадение количества чисел |
| `*FORTRAN` (Дубна) | `max(1e-4, 1e-4·max(\|x\|,\|y\|))` | sliding window `W=3`, `score ≥ 0.95`, первая и последняя строки совпали |

Если эталон недоступен (rc≠0 или нет результата) — `SKIP (нет эталона)` и
уровень не блокирует приёмку. Логи: `logs/f77_full_cross_ftn.txt`,
`logs/f77_full_cross_fortran.txt`.

### L3 — реальные программы

| ID | Программа | Контроль | Статус по умолчанию |
|---|---|---|---|
| R01 | `tests/forex-glissade/glkern.b6` (полная PERSO 9 модулей) | 14/14 строк | обязателен, запускается `tests/run-glissade-forex.sh` |
| R02 | `reference/forex.b6`, решето Эратосфена | SHA256 нормализованного вывода (`tests/run-forex.sh`) | обязателен |
| R03 | `dhrystone-forex.dub` (FOREX 4.13, 18+4 control, 48/48 прогонов) | внешний эталон | `SKIP` без `F77_FULL_EXTERNAL=1` |
| R04 | `whetstone-longbottom-forex.dub` (8 секций, `0.809 MWIPS ±5 %`) | внешний эталон | `SKIP` без `F77_FULL_EXTERNAL=1` |

R03/R04 имеют внешние `.dub`-исходники, но используют `CHARACTER*30` и
рантайм 4.13; на системном 2.02 их вывод не является gold-эталоном, поэтому
по умолчанию помечаются `SKIP` (в документе 04 это «SKIP, формально не
увеличивает R»). При `F77_FULL_EXTERNAL=1` оркестратор оборачивает `.dub` в
деку и запускает её.

### L4 — negative cases (9/9)

NC01–NC07 сверяют ожидаемую диагностику с уже зафиксированными
`tests/plan-f77/work/**/out.txt` и `tests/plan-f77/e1/**/out.txt` (поиск —
строго литеральный `grep -F`, так как диагностики содержат `*`). Дополнительно
проверяется, что диагностический текст **не** попал ни в один gold как успех.
NC08 проверяет каталог PERSO в свежем glissade-выводе: токен `ОСТТDЕС` есть,
`ИСПОРЧЕН` нет (переход FAIL→OK для дубля `OCTTDEC`). NC09 — positively
контролируемая порча: во временной копии `check-source-words.py` +
`src/LO_*.mad` + `build/LO_*.words` меняется одно машинное слово; сценарий
обязан вернуть rc=1, а неисправленная копия — rc=0. Репозиторий при этом не
изменяется.

### Gate G — обязательные 20/20

Состав фиксирован `docs/plan-f77/04-assembler-path.md` §5.1–5.2:

* **G01–G15** — 15 сценариев `tests/plan-f77/probe.sh` (вызывается как есть).
  Gate — это проверка **отсутствия регрессии относительно baseline 2.02**:
  для 10 сценариев ожидается `OK`, для 5 (`CHARSTAR`, `LISTDIR`, `IMPLICIT`,
  `ENDREAD`, `SAVE`) — baseline-диагностика; переход последних в `OK` после
  P1–P7 засчитывается как `IMPROVED`, а не как FAIL. Любая иная диагностика
  или пропажа строки — FAIL.
* **G16** — Глиссада 14/14 (результат L3 переиспользуется, без второго прогона).
* **G17–G20** — четыре положительных F77-дека в `gate/` с lowered-формой
 (list-directed `PRINT`, `IMPLICIT NONE`→удаление, `READ`-понижение, `SAVE`
  →удаление). После P1–P7 они заменяются нативными аналогами.

Gate проверяется с тем же прогоном, что и L0–L4; при `FAIL > 0` или `OK < 20`
оркестратор печатает `FAIL: gate … — риск регрессии` и возвращает **1**,
независимо от PENDING на остальных уровнях.

## 4. Политика PENDING

Пока P1–P7 (правки E4/MADLEN) не выполнены, любая непройденная проба L0–L4
помечается `PENDING (E4/MADLEN)` с причиной (диагностика ФОРЭКСа или
`gold/fact`) и **не** увеличивает rc сценария. После завершения P1–P7
остатки PENDING должны быть переведены в FAIL и разобраны: критерий приёмки
`04-verification.md` §4.1 — `32/32, 32 gold, 0 FAIL, cross 8/8, real 4/4,
neg 9/9, gate 20/20`. Gate — единственная часть, которая уже сейчас обязательна
и всегда влияет на rc.

## 5. Текущий результат (прогон 19.11.2026, rc=0)

| Уровень | OK | PENDING | SKIP | Комментарий |
|---|---:|---:|---:|---|
| L0 | 29/32 | 3 | — | F03, I02, K03 |
| L1 | 29/32 | 3 | — | те же 3 пары; 8 suite-пар байтово равны оригиналам |
| L2 | 8/8 | 0 | 0 | `*FTN` 4/4, `*FORTRAN` 4/4 (1e-5 / 1e-4 + sliding) |
| L3 | 2/4 | 0 | 2 | Глиссада 14/14, решето SHA; Dhrystone/Whetstone — внешние эталоны |
| L4 | 9/9 | 0 | — | включая NC09 tamper-control |
| **G** | **20/20** | — | — | 15 проб + Глиссада + 4 lowered F77-дека |

PENDING-пробы:

| ID | Конструкция | Диагностика / причина |
|---|---|---|
| F03 | `EXTERNAL FOO` / `INTRINSIC SQRT` как операторы описания | `НЕДОПУСТИМ КЛЮЧ СЛОВО` |
| I02 | `CHARACTER*10 S`, `S='ABCDE'`, `S(2:4)` | `ТИП ОП-ДА НЕ СООТВЕТ ОПЕРАЦ` |
| K03 | `CABS(WC)`, `WC=(3.0,4.0)` | число `*3184.0000` вместо `5.0000` (нет корректной реализации) |

Итоговая строка (текущая, с оговоркой P1–P7):
`F77 full = 29/32 constructs, 29/32 gold pairs, cross 8/8, real 2/4 (2 SKIP),
neg 9/9, gate 20/20, rc=0`.

## 6. Логи

| Файл | Содержимое |
|---|---|
| `logs/f77_full_run.txt` | общий протокол и итоговая таблица |
| `logs/f77_full_matrix.txt` | 32 строки `OK/PENDING <id> <конструкция> <диагностика>` |
| `logs/f77_full_gold.txt` | `ID/DECK/GOLD/SOURCE/STATUS`, `gold/fact`, `REUSED OK/FAIL` |
| `logs/f77_full_cross_ftn.txt`, `logs/f77_full_cross_fortran.txt` | `CROSS OK/FAIL/SKIP`, числа, допуск, sliding score |
| `logs/f77_full_real.txt` | 14/14, SHA решета, SKIP внешних бенчмарков |
| `logs/f77_full_negative.txt` | ожидаемая диагностика, факт, классификация |
| `logs/f77_full_gate.txt` | 20 строк gate + итог 20/20 |
| `logs/f77_full_summary.txt` | сводная таблица + `RC=0/1` |
| `logs/f77_full.sha256` | SHA256 всех деков/gold/registry и образов диска |

Имена логов сохранены с префиксом `f77_full_` (в проекте 04 предлагались
`f77_cross_ftn.txt`, `f77_cross_fortran.txt`; префикс здесь единообразен и
попадает в зону владения P8).

## 7. Что делать после P1–P7

1. Устранить три PENDING: нативная поддержка `EXTERNAL`/`INTRINSIC` (F03),
   `CHARACTER` + подстроки (I02), численная реализация `CABS` в `F77LIBR` (K03).
2. Обновить соответствующие `gold/*.gold` только если меняется **эталонная**
   семантика (не ради снятия PENDING).
3. Заменить 4 lowered-дека в `gate/` на нативные конструкции и убрать
   `IMPROVED`-ветку для LISTDIR/IMPLICIT/ENDREAD/SAVE из gate.
4. Включить `F77_FULL_EXTERNAL=1` и зафиксировать control-векторы Dhrystone
   (18+4, 48/48) и Whetstone (8/8, `0.809 MWIPS ±5 %`).
5. Переписать итоговую строку §5 на целевую из `04-verification.md` §4.1.
