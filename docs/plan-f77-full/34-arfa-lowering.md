# 34 — P7c / ВОЛНА G: lowering файлового I/O F77 → PERSO 0o2320 (реализация)

**Дата:** 19.11.2026. **Изделие:** FOREX 5.00 / 19.11.2026 (re-forex).
**Статус:** rules 34–40 реализованы в host-движке `src/f77prep/prep_tools.py`,
исполняемо проверены двухпроходными тестами case23–case26,
`tests/run-f77-prep.sh` rc=0. `F77PREP.FTN` **не трогался** (лимит памяти 2.02).

**Владение.** `src/f77prep/prep_tools.py`, `tests/f77/prep-case23..26.f77`
(+ `-expected.f77` / `-expected.out`), `tests/run-f77-prep.sh`, этот документ,
`logs/f77_26_lower_*.txt`. `src/f77libr`, `src/lib21`, `REFERENCE`, эталоны,
`tests/plan-f77-full`, dispak — READ-ONLY.

**Предыдущие волны:** 30 (АРФА как ФС), 31 (Fortran→PERSO Э63/Э70),
32 (spec-контракт `/FILMAP/`), 26 (Level B блокирует `WRITE(41,…)`).

---

## 0. Что сделано и чего НЕ сделано (честно)

| Аспект | Статус | Комментарий |
|---|---|---|
| Правила 34–40 в host-движке | **OK (executable)** | чист текст. замена до ФОРЭКС 2.02, 0 слов в оверлеях |
| ENCODE/DECODE для formatted I/O | **OK (проба)** | FOREX 2.02 поддерживает, bufffer — настоящий (лог `f77_26_lower_probe.txt`) |
| OPEN/CLOSE/INQUIRE/WRITE/READ/EOF | **OK\* (stub/bridge)** | CALL-API + `/FILMAP/`; реальная АРФА — за G1 |
| `ИМЯ` с точными ГОСТ-байтами | **ОГОВОРКА** | FOREX `nH` даёт ASCII; ГОСТ-цифры = управляющие коды, картами не проходят. Host эмитит ASCII, ZFOPEN обязан транскодировать |
| `IOSTAT` X3.9 / настоящий EOF | **НЕТ** | эмуляция: `FM(1)=-1` из PERSO; `STATUS/ACCESS/FORM/RECL` кэшируются в `FM(4..7)` |
| Реальные Э63 01/02/07/12/30/31 + Э70 | **НЕ в этой волне** | агент G1, PERSO 0o2320; host лишь формирует вызовы и имена |
| Level B / `ERRLUN` | **НЕТ** | обмен внутри PERSO (31, 32 H11); без правки монитора `WRITE(41,…)` недоступен |

`OK*` = lowering + исполняемая проверка на тестовом stub-рантайме; это **не**
закрытая J24 в смысле X3.9. Завышения статуса нет.

---

## 1. Проба ENCODE/DECODE (результат зафиксирован)

Ответ: **ДА, FOREX 2.02 поддерживает `ENCODE`/`DECODE` (внутренний файл)**.
Пять дек подтвердили: значение действительно проходит через буфер, а не через
скрытый scratch: `DECODE` из неписанного буфера даёт `0`, из записанного —
`12345`; `ENCODE` INTEGER+REAL → `DECODE` в обнуленные переменные даёт
`12345` / `67.8900`. Полный протокол — `logs/f77_26_lower_probe.txt`.

Следствие — formatted lowering использует нативный механизм:

```
WRITE(u,fmt) list  ->  ENCODE(nw,fmt,IB<u>) list
                       CALL ZFWRIT(u,IB<u>,nw,IST)
READ(u,fmt) list   ->  CALL ZFREAD(u,IB<u>,nw,IST)
                       [k = IST]
                       [IF (IST .EQ. -1) GO TO Lend]
                       DECODE(nw,fmt,IB<u>) list
```

`nw = IOBUF_WORDS * 6 = 12 * 6 = 72` символа; буфер `INTEGER IB<u>(12)`.
Минимальный форматтер в хосте/PERSO для I/F/A/E **не потребовался**.

Дополнительные факты 2.02, найденные пробой:
* `nH` = 8-битные ASCII-байты, 6 на 48-битное слово (совпадает с
  `10-implementation-libr.md §3.1`);
* INTEGER ≤ 2²⁵−1 в литерале (`2^36` → `ПЕРЕПОЛ МАНТИССЫ`), поэтому 48-битное
  ГОСТ-слово нельзя записать десятичной константой;
* объявление после исполняемого оператора → `ERR 04441`; все объявления
  правил 34–40 выносятся сразу за заголовок PROGRAM/SUBROUTINE/FUNCTION;
* `F77PREP.FTN` имеет жёсткий потолок трансляции — правила 34–40 поэтому
  классифицируются **только в хосте** (как правила 25–32).

---

## 2. Контракт PERSO 0o2320 (согласован с G1)

```fortran
      INTEGER FM(20)
      COMMON /FILMAP/ FM
```

| Слот | Назначение |
|---|---|
| `FM(1)` | **ISTAT последней операции**. `0` = успех, `-1` = EOF, `>0` = профильный код M16 (таблица 32 §4.5) |
| `FM(2)` | `OPENED` (0/1) |
| `FM(3)` | `EXIST` (0/1) |
| `FM(4)` | STATUS: UNKNOWN=0, OLD=1, NEW=2, SCRATCH=3 |
| `FM(5)` | ACCESS: SEQUENTIAL=0, DIRECT=1 |
| `FM(6)` | FORM: FORMATTED=0, UNFORMATTED=1 |
| `FM(7)` | RECL (запрос; АРФА работает зонами) |
| `FM(8)` | длина/позиция текущей записи |
| `FM(9..20)` | 12-словный буфер данных stub-рантайма |

**Status returns through COMMON, not through the dummy argument.** FOREX 2.02
передаёт скалярные фактические аргументы по значению (`31 §2.3`): `IST` в
сигнатуре сохраняется для совместимости, но фактическое состояние PERSO
пишет в `FM(1)`, откуда его читает сгенерированный Fortran.

Entry points (не конфликтуют с lib21). `ZFCLOSE` — 7 знаков ровно по
согласованному с G1 API; ФОРЭКС 2.02 печатит безвредное
`АТТ: ZFCLOSE УКОРОЧЕН`, но разрешает символ (проверено сборкой stub-а и
case23). Остальные имена ≤6: `ZFOPEN`, `ZFINQ`, `ZFWRIT`, `ZFREAD`,
`FMN<u>`, `IB<u>`, `FM`.

```
ZFOPEN (NAME, LUN, IST)        NAME — INTEGER(2), NAME(1)/NAME(2)
ZFCLOSE(LUN, DEL, IST)         DEL=1 для STATUS='DELETE', иначе 0
ZFINQ (LUN, OPENED, EXIST, IST)
ZFWRIT(LUN, BUF, N, IST)
ZFREAD(LUN, BUF, N, IST)       IST=-1 при EOF
```

`INTEGER(2) NAME` host.materializuet как `DATA FMN<u> /12H<ASCII-name>/`.
FOREX 2.02 `nH` = ASCII, а АРФА ждёт ГОСТ-10859; точные ГОСТ-байты для
цифр (коды `000..011`) не вводятся картами. **Обязательство G1:** в ZFOPEN
выполнить ASCII→ГОСТ (DUBNA TEXT→GOST 10859, таблица
`tools/besm6_text_scan.py:TEXT_TO_GOST`) и сформировать имя с шифром
владельца (doc 32 H6/H7). Хвост `/419999` (шифр хозяина) — на стороне PERSO.

Все деки содержит `*perso:602300` **и** `*perso:602320,cont`
(`make_deck1()`, `make_deck2()`; проверено регрессией case1/2/8..26).

---

## 3. Таблица правил 34–40

| rule | Вход | Lowering (host, `prep_tools.py`) |
|---:|---|---|
| **34** | `OPEN(u,FILE='N',STATUS='S',ACCESS='A',FORM='F',RECL=r,IOSTAT=k,ERR=L)` | decl `INTEGER FM(20)`+`COMMON /FILMAP/ FM`; `FM(4..7)` = коды S/A/F/r; `INTEGER FMN<u>(2)`+`DATA` с ASCII-именем; `CALL ZFOPEN(FMN<u>,u,FM(1))`; `k=FM(1)`; `IF(k.NE.0) GO TO L` |
| **35** | `CLOSE(u[,STATUS='DELETE'][,IOSTAT=k][,ERR=L])` | `CALL ZFCLOSE(u,del,FM(1))`, `del=1` только для DELETE; status/ERR как в 34 |
| **36** | `INQUIRE(UNIT=u,OPENED=v[,EXIST=e][,IOSTAT=k][,ERR=L])` | `CALL ZFINQ(u,v,e,FM(1))`; `EXIST=.FALSE.` **не** ошибка; status/ERR |
| **37** | `WRITE(u,fmt) list` (в т.ч. `fmt=*`) | `ENCODE(72,fmt,IB<u>) list` + `CALL ZFWRIT(u,IB<u>,12,FM(1))`; для `fmt=*` host синтезирует FORMAT из типов (`_descriptor`) |
| **38** | `READ(u,fmt) list [,END=L,IOSTAT=k,ERR=E]` | `CALL ZFREAD(u,IB<u>,12,FM(1))` → `k=FM(1)` → `IF(FM(1).EQ.-1) GO TO L` → `DECODE(72,fmt,IB<u>) list` → `IF(k.NE.0) GO TO E` |
| **39** | `WRITE(u) list` (неформатированный) | упаковка `IB<u>(i)=v_i` + `CALL ZFWRIT(u,IB<u>,n,FM(1))`, **один** CALL на запись |
| **40** | `READ(u) list [,END=L,IOSTAT=k]` | `CALL ZFREAD(u,IB<u>,n,FM(1))` → `k=FM(1)` → END-ветвь → `v_i=IB<u>(i)` |

Общее для всех правил: `C@ F77A … -> ZF bridge` якорь; сохранение метки
оператора (`lab CONTINUE`); объявления выносятся в начало unit-а; правило 20
не считает `OPEN/CLOSE/INQUIRE` длинными именами (добавлены в `KEYWORDS`).

Ограничения: список неформатированного I/O ≤ 12 слов; строка формата ≤ 72
символов; `INQUIRE(FILE=…)` не поддерживается (API только по UNIT);
`ACCESS='DIRECT'`, `RECL`, `SCRATCH` — profile-оговорки (32 §5.1–5.2).

---

## 4. Тесты и контрольные значения

| Кейс | Что проверяет | CONTROL (`*-expected.out`) |
|---|---|---|
| case23 | OPEN + INQUIRE(OPENED/EXIST) + CLOSE(DELETE), IOSTAT/ERR | ` OP  1 EX  1 K  0` / ` K  0` |
| case24 | formatted WRITE→READ (ENCODE/ZFWRIT/ZFREAD/DECODE) | ` C   12 D   34 K   0` |
| case25 | unformatted WRITE→READ (пакетная упаковка) | ` C  111 D  222 K   0` |
| case26 | EOF: второй READ → `FM(1)=-1` → `END=80`, `IOSTAT=-1` | ` EOF K  -1` |

`tests/run-f77-prep.sh` собирает тестовый ZF-stub в 0o2320 (или берёт
`ZF_IMAGE` G1), прогоняет 21 кейс (1, 2, 8–26) — **rc=0**; старые эталоны
побайтово не изменились.  Логи: `logs/f77_prep_v2_case23..26.txt`,
`logs/f77_prep_v2_pass{1,2}_case23..26.txt`.

---

## 5. Оговорки профиля FOREX 5.00

1. `IOSTAT` — профильный код из `FM(1)`, не системный X3.9; `-1` = EOF —
   синтетический сигнал PERSO, не аппаратный `Э60`.
2. `WRITE/READ` formatted идут через ENCODE/DECODE и 72-символьный буфер;
   запись длиннее 72 символов усекается (документированное ограничение).
3. unformatted I/O проходит через INTEGER-слова; REAL/COMPLEX преобразуются
   присваиванием, побитовая идентичность не гарантирована.
4. Имя файла — ASCII в `INTEGER(2)`; транскодировка в ГОСТ и шифр хозяина —
   обязанность PERSO ZFOPEN (G1). Без неё АРФА отклонит имя.
5. Реальная семантика АРФА (зоны, отсутствие record/RECL/EOF) — 32 §5;
   Level B по-прежнему блокирует прямой `WRITE(41,…)` (26, 31).

---

## 6. Источники

* `src/f77prep/prep_tools.py` (rules 34–40, `_io_control`, `_gost_name_words`,
  `_classify_file_io`, hoisted declarations).
* `tests/run-f77-prep.sh`, `tests/f77/prep-case23..26*`,
  `logs/f77_26_lower_probe.txt`.
* `docs/plan-f77-full/32-f77-on-arfa.md` §2–4 (контракт, FILMAP, M16),
  `31-fortran-arfa-bridge.md` §2.3 (скаляры по значению),
  `26-file-runtime.md` (Level B), `20-open-close.md §1.2` (COMMON-канал),
  `10-implementation-libr.md §3.1` (nH = ASCII).
