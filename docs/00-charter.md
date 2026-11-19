# Устав и происхождение (этап 0)

**Версия изделия: FOREX 5.00** (`re-forex`). Это номер версии нашей
реконструкции. Он фиксируется в заголовках `src/*.mad`, `src/f77*/`,
в PERSO-образе `build/FOREX_PERSO_2300.bin` (TEXT-метка `FOREX 5.00` в хвосте)
и в ДРАКОН-схемах `docs/drakon/`.

**Важно (баннер).** Строка `F О R Е Х … ВЕРСИЯ 2.02 ОТ 15.07.80` в эталонных
прогонах печатается **системным ФОРЭКСОМ на диске 2048**, а не нашей
реконструкцией. Проверено: один и тот же дек с `*perso:602300` и без него даёт
одинаковый баннер 2.02; константы 2.02 нет ни в одном реконструируемом модуле
(`CORE_ROOT.words`, `LO_*.words`, рантайм) и на ленте `monsys.9`. Поэтому
"патчить негде": системный баннер 2.02 остаётся, а версия **нашего изделия —
5.00**. См. `docs/16-glissade-run.md` §6.

## Цель

Получить аннотированные МАДЛЕН-исходники оверлеев `LO*SYN` и `LO*GEN`
компилятора ФОРЭКС с побайтовой проверкой и эталонным прогоном.
Детальный план — [PLAN.md](PLAN.md).

## Происхождение эталонов

| Объект | Путь | SHA256 / примечание |
|---|---|---|
| `monsys.9` | `/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9` | `e26a2036011bc33a2671b052ea63eaa60b6f577235cfe7080837978d1df1118b` |
| исходник `FOREX*` | `besm6.github.io/sources/dubna/besml21/libra211.l21:15448-15528` | только чтение |
| LIBREFER | `besm6-new/dubna/tests/expect_library21.txt` | только чтение |
| эталон прогона | `dispak/tests/forex/output.txt` | Фортран-решето, FOREX 2.02 |
| эталон Дубны | `besm6-new/dubna/tests/expect_forex.txt` | FOREX 4.13 |

Образ `monsys.9` — уже исправленная версия: 18 байт в зоне `0137`
(адреса `0o277775-0o277777`) восстановлены по upstream-образу. Не изменять.
Контрольную сумму симулятор проверяет.

## Инструменты

| Инструмент | Путь | Версия |
|---|---|---|
| `disbesm6` | `/usr/local/bin/disbesm6` | `Usage: disbesm6 [-r] [-b] [-aN] [-eN] [-nSymtab] file...` |
| `besmtool` | `/usr/local/bin/besmtool` | `2.6.458-9b5cabe` |
| `besm6tape.py` | `besm6.net/tools/besm6tape.py` | `info/dis/text/strings/zones`, смещения восьмеричные |
| `dtran` (Linux) | `~/Yandex.Disk/dtran/dtran` | `Usage: dtran [options] objfile`, `-F dms|pa|pb`, `-e -l` |
| `dispak` | `~/Yandex.Disk/dispak/build/dispak/dispak` | DTRAN в мониторе, прогон `forex.b6` |

Симуляторы `dubna` (C++) и `besm6.net` (C#) в этой среде не собраны —
дамп памяти выполняется только через `dispak`.
