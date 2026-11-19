# Дизассемблирование библиотеки lib21

## Метод

Данные: DMS-библиотека
`/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin`
(211968 слов, 601 запись в каталоге, **358 найденных объектов**).
Парсер — `~/Yandex.Disk/re-siprod/tools/siprod_lib.py`, дизассемблер —
`/home/azizz/Yandex.Disk/dtran/dtran -F dms` (по образцу
`re-siprod/tools/siprod_madlen.py:disassemble`).

Инструмент: `tools/lib21_disasm.py`. Для каждого модуля:

1. Извлекается объектный образ от заголовка до конца секции `debug`
   (секции `cmd`, `const`, `data`, `set`, `head`, `sym`, `long`, `debug`);
   секция `comment` (исходный текст) не включается.
2. Образ пишется во временный файл `build/_lib21_module.dms` (build/ в
   `.gitignore`) и разбирается `dtran -F dms`.
3. Служебные строки `C ...` (счётчики разделов, симтаблица) удаляются, чтобы
   листинг начинался с строки `<ИМЯ>  :,NAME, NEW DTRAN`.
4. Результат сохраняется в `disasm/lib21/<имя>.madlen`.

Преобразование имён файлов: `/` → `#`, `*` → `_`.
Например: `FOREX*` → `FOREX_.madlen`, `GIV/PG` → `GIV#PG.madlen`,
`A/OCTDEC` → `A#OCTDEC.madlen`, `*DISPAR1` → `_DISPAR1.madlen`.

Запуск:

```bash
python3 tools/lib21_disasm.py                       # все 358 модулей
python3 tools/lib21_disasm.py --module FOREX*       # один модуль
python3 tools/lib21_disasm.py --limit 10            # первые 10 по алфавиту
python3 tools/lib21_disasm.py --out DIR --dtran PATH --log FILE
```

Если `dtran` падает, таймаутит или даёт пустой вывод — в `disasm/lib21`
пишется пустой файл, а модуль с причиной заносится в лог
`logs/lib21_disasm.txt`.

## Результаты

| Показатель | Значение |
|---|---|
| Модулей обработано | 358 |
| С непустым листингом | 358 |
| С пустым выводом / ошибкой dtran | 0 |
| Суммарно строк МАДЛЕН | 55 168 |
| Средний размер листинга | 154.1 строки |
| Минимальный / максимальный | 3 / 2666 строк |

Лог полного прогона: `logs/lib21_disasm.txt` (построчно: модуль → файл →
число строк; в конце сводка).

Крупнейшие листинги: `TCATALOG.madlen` (2666), `DOS#IAE.madlen` (2608),
`VOБФOP.madlen` (1121), `XREF.madlen` (944), `REDACT1.madlen` (913).
Самые маленькие: `ERROR_P.madlen`, `LIBLIST.madlen`, `ЬTRUЬ.madlen`,
`ЬЦ0Ь.madlen` (по 3 строки) — модули без секции команд.

## Контрольные модули

Проверены модули `FOREX*`, `FORMAT`, `GIV/PG`, `BEMSH*`, `XREF`.
У всех первая строка имеет вид `<ИМЯ>  :,NAME, NEW DTRAN` (dtran выравнивает
имя влево до 8 символов, поэтому у коротких имён пробелов больше: например,
`XREF    :,NAME, NEW DTRAN`), и присутствуют мнемоники МАДЛЕН `XTA`, `ATX`,
`VTM`, `UJ`, `VJM`:

| Модуль | Файл | Строк | XTA | ATX | VTM | UJ | VJM |
|---|---|---:|---:|---:|---:|---:|---:|
| `FOREX*` | `FOREX_.madlen` | 88 | 5 | 13 | 4 | 2 | 5 |
| `FORMAT` | `FORMAT.madlen` | 58 | 2 | 11 | 1 | 13 | 0 |
| `GIV/PG` | `GIV#PG.madlen` | 57 | 8 | 9 | 3 | 3 | 0 |
| `BEMSH*` | `BEMSH_.madlen` | 108 | 10 | 24 | 3 | 3 | 1 |
| `XREF` | `XREF.madlen` | 944 | 156 | 91 | 123 | 66 | 135 |

### Пример: начало `FOREX_.madlen`

```madlen
FOREX*  :,NAME, NEW DTRAN
 ENTRY*  :,LC,40
 FLGEX*  :,LC,1
 NOLISFL*:,LC,1
 FULISFL*:,LC,1
 CHECKFL*:,LC,1
 *DUMON* :,LC,5
 A/I0    :,LC,1
 DATAPR* :,SUBP,
 TAK/PG  :,SUBP,
 GIV/PG  :,SUBP,
 OCTTDEC :,SUBP,
 FOREX   :,SUBP,
 CONST   :,SUBP,
 COMEQ   :,SUBP,
 OPRTR   :,SUBP,
 ПP      :,SUBP,
 *A*     :,LC,2048
 LOADANGO:,SUBP,
 GAM/5:,EQU,*DUMON* +3
 GAM/6:,EQU,*DUMON* +2
 GAM/7:,EQU,*DUMON* +1
 GAN/0:,EQU,*DUMON* +4
 ,ITA,13
 ,ATX,*0050B
 ,*57,6
  :,ATX,*0035B
 ,XTA,
 ,ATX,GAM/5
 14,VTM,ENTRY*
```

### Пример: начало `XREF.madlen`

```madlen
XREF    :,NAME, NEW DTRAN
 P/1D    :,LC,462
 *OUTPUT*:,LC,30
 *INPUT* :,LC,30
 P/CO    :,SUBP,
 P/IT    :,SUBP,
 P/2     :,SUBP,
 P/SC    :,SUBP,
```

## Связанные файлы

- `tools/lib21_disasm.py` — инструмент массового разбора.
- `disasm/lib21/*.madlen` — 358 листингов.
- `logs/lib21_disasm.txt` — полный лог прогона.
