# Регрессионные сценарии

Сценарии не изменяют эталоны: временные файлы создаются в `$TMPDIR`
(по умолчанию `/tmp/.private/azizz/opencode`) и удаляются по завершении.
Каждый сценарий печатает `OK`/`FAIL` и возвращает 0/1.

## Запуск

```sh
cd /tmp/.private/azizz/opencode/re-forex
tests/run-forex.sh
tests/verify-dumps.sh
tests/check-annotations.sh
tests/check-disasm.sh
tests/check-dtran.sh
tests/check-word-coverage.sh
tests/check-labels.sh
tests/check-constants.sh
tests/check-runtime-disasm.sh
python3 tests/check-source-words.py
```

Прогнать все и сохранить логи:

```sh
mkdir -p logs
for s in run-forex verify-dumps check-annotations check-disasm check-dtran check-word-coverage check-labels check-constants check-runtime-disasm; do
    tests/$s.sh > logs/tests_$s.txt 2>&1
    printf '%-20s rc=%s\n' "$s" "$?"
done
python3 tests/check-source-words.py > logs/tests_check-source-words.txt 2>&1
printf '%-20s rc=%s\n' check-source-words "$?"
```

## Что проверяет каждый сценарий

| Сценарий | Проверка | Ожидаемый вывод |
|---|---|---|
| `run-forex.sh` | Прогон `reference/forex.b6` через dispak в отдельном каталоге; побайтовая сверка с `reference/output.gold.txt` после нормализации даты `DD.DD.DD` → `##.##.##` | `OK: FOREX 2.02 вывод совпадает с эталоном` |
| `verify-dumps.sh` | `dd bs=6 skip=$((8#241500/277500)) count=1024` из `monsys.9`; sha256 выгрузок = `83a7e962…` (LO_SYN) и `4f4d8e4c…` (LO_GEN); при наличии — `cmp` с `build/*.words` | `OK: оверлеи LO*SYN и LO*GEN выгружены и сверены` |
| `check-annotations.sh` | Наличие 19 обязательных символов чек-листа в `src/LO_SYN.mad`, `src/LO_GEN.mad`, `include/FOREX_ROOT.mad` и ≥50 строк комментариев (`С ` или `.`) в каждом `.mad`. Если файлы ещё не созданы — печатает «ОЖИДАЕТСЯ» и возвращает 0 | `OK (ожидается): …` до этапа 5, затем `OK: все обязательные символы и комментарии присутствуют` |
| `check-disasm.sh` | `disasm/LO_{SYN,GEN}.raw.lst` содержат `СТАРТ` и `ФИНИШ` и ≥900 строк; размеры `build/LO_{SYN,GEN}.words` кратны 6 байтам | `OK: листинги и дампы прошли проверку` |
| `check-dtran.sh` | `disasm/LO_{SYN,GEN}.dtran.madlen` exist, ≥1500 строк, заголовок `LO*SYN`/`LO*GEN`, присутствуют `VTM`/`VJM` | `OK …: N строк, заголовок …, VTM/VJM присутствуют` |
| `check-word-coverage.sh` | в `src/LO_{SYN,GEN}.mad` ровно 1024 уникальных строк-меток слов (формат `С--- слово NNNN`) | `OK …: 1024/1024 слов аннотировано` |
| `check-source-words.py` | каждое из 1024 машинных слов в аннотированном тексте совпадает с дампом `build/LO_*.words` | `OK …: все 1024 слова совпадают с дампом` |
| `check-labels.sh` | в `src/*.mad` нет автосгенерированных меток `W1777:`/`WT0533:`/`D00001:`; для каждого модуля есть таблица соответствий в `include/*.labels.md` | `OK …: авто-меток 0, в … N строк соответствий` |
| `check-constants.sh` | числовые литералы вынесены в `,EQU,`: для каждого файла печатает число EQU, голых литералов и уникальных | `OK …: EQU > 0, уник ≤ 20` |
| `check-runtime-disasm.sh` | новые рантайм-дизассемблы: наличие/непустота `src/FOREX_{RUNTIME,DECODER}_DISASM.mad`, `disasm/RUNTIME_*.{madlen,bemsh.lst}`; в `.mad` — >20 `,EQU,`, нет авто-меток `Wnnn:`/`Dnnnnn:`/`*000NN`, >100 строк комментариев; `build/RUNTIME_*.words` кратны 6 байтам; вызывает `check-source-words.py` и `check-constants.sh` с пробросом rc. Отсутствующие файлы → «ОЖИДАЕТСЯ», rc=0 | `ОЖИДАЕТСЯ …` до появления файлов, затем `OK: все проверки новых рантайм-модулей пройдены` |

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `DISPAK_BIN` | `/home/azizz/Yandex.Disk/dispak/build/dispak/dispak` | путь к эмулятору dispak |
| `MONSYS_TAPE` | `/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9` | путь к ленте с оверлеями |
| `TMPDIR` | `/tmp/.private/azizz/opencode` | каталог для временных файлов |

## Примечания

- Версия 2.02 (`output.gold.txt`) — эталон с подстановкой `##.##.##` в строке
  даты; реальный прогон даёт текущую дату, поэтому сравнивается только дата.
  Эталоны 4.13 и LIBREFER из `reference/expect_*.txt` используются на этапе 6
  для сверки баннеров и LIBREFER, но не как «золотой вывод» FOREX 2.02.
- `build/` и `reference/*.bin` исключены из git (`.gitignore`); дампы
  восстанавливаются `verify-dumps.sh`, а не хранятся в репозитории.
- Порядок запуска: сначала `verify-dumps.sh` и `check-disasm.sh` (этапы 2–4),
  затем `check-annotations.sh` (этап 5), затем `run-forex.sh` (этап 6).
