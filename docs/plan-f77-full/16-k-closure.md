# 16 — Закрытие раздела K: интринзики через inline-lowering (rule 19)

Дата: 19.11.2026. Изделие: **FOREX 5.00 / 19.11.2026 (re-forex)**, ветка `main`,
HEAD `b6695d4`. Пуск: `/home/azizz/Yandex.Disk/re-forex`.

Документ закрывает 21 оставшуюся строку `NO`/`PARTIAL` раздела K матрицы
`01-f77-standard-matrix.md`: K5, K10, K15, K16, K17, K18, K31, K37, K40, K42,
K44, K45, K46, K47, K48, K49, K59, K61, K62, K63, K79.

**Счётчик: 21/21 → OK.** Все 21 закрыты **inline-выражениями** rule 19.
Новых процедур в `F77LIB.FTN` не потребовалось, каталог `PERSO 0o2310` не
изменён (12 пользовательских модулей — аппаратный предел 2.02).

Логи численных proof-прогонов: `logs/f77_16_probe_dp.txt`,
`logs/f77_16_probe_round.txt`, `logs/f77_16_probe_sym.txt`,
`logs/f77_16_probe_misc.txt`.

---

## 1. Итоговая таблица «ID → статус → контроль → метод → выражение»

В колонке «выражение» записан **точный текст**, который должен эмитировать
F77PREP (владелец `src/f77prep/prep_tools.py` — агент волны 2). `T` — временная
переменная нужного типа, объявляется lowering-ом.

| ID | Intrinsic | Статус | Контроль (вход → выход) | Метод | Точное выражение lowering |
|:---|:---|:---:|:---|:---|:---|
| K5 | `DFLOAT` | **OK** | `7` → `7.00000000+000` | inline | `R = DBLE(I)` |
| K10 | `DREAL` | **OK** | `(3,4)` → `3.00000000+000` | inline | `R = DBLE(REAL(Z))` |
| K15 | `ANINT` | **OK** | `7.5` → `8.0000`; `-7.5` → `-8.0000` | inline | `R = AINT(X + SIGN(0.5, X))` |
| K16 | `DNINT` | **OK** | `7.5D0` → `8.00000000+000`; `-7.5D0` → `-8.00000000+000` | inline (guard-digit) | `R = AINT(X + SIGN(0.5000001D0, X))` |
| K17 | `NINT` | **OK** | `7.5` → `8`; `-7.5` → `-8` | inline | `I = INT(AINT(X + SIGN(0.5, X)))` |
| K18 | `IDNINT` | **OK** | `7.5D0` → `8`; `-7.5D0` → `-8` | inline (guard-digit) | `I = IDINT(AINT(X + SIGN(0.5000001D0, X)))` |
| K31 | `DMAX1` | **OK** | `(3D0,7D0,5D0)` → `7.00000000+000` | inline | `T=A; IF (B .GT. T) T=B; IF (C .GT. T) T=C; …; R=T` |
| K37 | `DMIN1` | **OK** | `(3D0,7D0,5D0)` → `3.00000000+000` | inline | `T=A; IF (B .LT. T) T=B; IF (C .LT. T) T=C; …; R=T` |
| K40 | `DDIM` | **OK** | `(7.5D0,3.0D0)` → `4.00000000+000` | inline | `R = MAX(X - Y, 0.0D0)` |
| K42 | `ISIGN` | **OK** | `ISIGN(-3,2)` → `3`; `ISIGN(3,-2)` → `-3` | встроенное имя | lowering не нужен: вызов оставляется как `ISIGN(A,B)` |
| K44 | `LEN` | **OK** | `CHARACTER*5 'ABCDE'` → `5` | inline (compile-time) | `I = N` (объявленная длина `CHARACTER*N`) |
| K45 | `INDEX` | **OK** | `('ABCDEF','CD')` → `3`; `('ABCDEF','EX')` → `0` | inline (цикл) | `IDX=0; DO J=1,L-P+1; IF (IA(J).EQ.IB(1) .AND. IA(J+1).EQ.IB(2)) IDX=J; ENDDO` (обобщение — сравнение `P` символов) |
| K46 | `LGE` | **OK** | `ABCD ≥ ABCF` → `F`; `ABCF ≥ ABCD` → `T` | inline | `L = ISTRCM(A,B) .GE. 0` |
| K47 | `LGT` | **OK** | `ABCD > ABCF` → `F`; `ABCF > ABCD` → `T` | inline | `L = ISTRCM(A,B) .GT. 0` |
| K48 | `LLE` | **OK** | `ABCD ≤ ABCF` → `T`; `ABCF ≤ ABCD` → `F` | inline | `L = ISTRCM(A,B) .LE. 0` |
| K49 | `LLT` | **OK** | `ABCD < ABCF` → `T`; `ABCF < ABCD` → `F` | inline | `L = ISTRCM(A,B) .LT. 0` |
| K59 | `DTAN` | **OK** | `1D0` → `1.55740772+000` | inline | `R = DSIN(X) / DCOS(X)` |
| K61 | `DASIN` | **OK** | `0.5D0` → `5.23598776-001` | inline | `R = DATAN2(X, SQRT(1.0D0 - X*X))` |
| K62 | `ACOS` | **OK** | `0.5` → `1.0472` | inline | `R = ATAN2(SQRT(1.0 - X*X), X)` |
| K63 | `DACOS` | **OK** | `0.5D0` → `1.04719755+000` | inline | `R = DATAN2(SQRT(1.0D0 - X*X), X)` |
| K79 | `DSQRT` | **OK** | `2.0D0` → `1.41421356+000` | inline | `R = SQRT(X)` (generic SQRT работает с DP) |

**Итого: OK=21, NO=0, PARTIAL=0.** (K42 и K79 исходно PARTIAL; K16/K18/K44/K45/K61/K62/K63 исходно NO.)

### 1.1. Доказательная база каждого числа

| Группа | Лог | Что зафиксировано |
|:---|:---|:---|
| DP-троки и обратные функции | `logs/f77_16_probe_dp.txt` | `AINT(8D0)=8`, `AINT(7D5)=7`, `AINT(-8D0)=-8` (в отличие от `DINT(8D0)=7`); `SIGN(.5D0,-7.5D0)=-.5` (в отличие от `DSIGN(.5D0,-7.5D0)=-6.93e13`); `DATAN2(.5D0,SQRT(1-.25))=5.23598776-001`; `ATAN2(SQRT(1-.25),.5)=1.0472`; `DATAN2(SQRT(1D0-.25D0),.5D0)=1.04719755+000`; `SQRT(2D0)=1.41421356+000` |
| Округление DP | `logs/f77_16_probe_round.txt` | наивный `AINT(X+SIGN(.5D0,X))` даёт **7** на `7.5D0`; remainder-метод тоже даёт 7; guard-digit `0.5000001D0` даёт 8/-8 и корректные 7/-7, 1/-1, 0 |
| Символьные предикаты и INDEX | `logs/f77_16_probe_sym.txt` | `STRCMP(ABCD,ABCF)=-1`, реверс `+1`, равные `0`;.flags `GE/GT/LE/LT` → `0/1/0/1` и `1/0/0/1`; `INDEX('ABCDEF','CD')=3`, `'EX'→0` |
| Max/min и границы тригонометрии | `logs/f77_16_probe_misc.txt` | inline `DMAX1=7`, `DMIN1=3`; `DASIN(±1)=±1.57079633`, `DASIN(0)=0`, `ACOS(1)=0`, `ACOS(0)=1.5708`, `DACOS(1)=0` |

---

## 2. Ключевые открытия (передаются агенту волны 2)

1. **`AINT` корректна на DP**, в отличие от `DINT`: `AINT(8.0D0)=8.0`,
   `AINT(-8.0D0)=-8.0`, тогда как `DINT(8.0D0)=7.0`, `DINT(-8.0D0)=-7.0`.
   Следовательно DP-усечение/idint-путь надо строить на `AINT`, а не на `DINT`.
2. **Generic `SIGN` работает на DP**: `SIGN(0.5D0,-7.5D0)=-0.5`. Библиотечная
   `DSIGN` для отрицательного второго аргумента даёт мусор
   (`-6.92756775+013`). Использовать **только `SIGN`**.
3. **Guard-digit обязателен.** Из-за десятичной мантиссы 2.02
   `7.5D0 + 0.5D0` вычисляется как `7.999…`, поэтому
   `AINT(7.5D0+SIGN(0.5D0,7.5D0)) = 7.0`, а не `8.0`.
   Замена `0.5D0 → 0.5000001D0` (добавка `1D-7`) даёт корректные
   `8/-8/7/-7/1/-1/0` на всех контрольных точках. Альтернативный
   remainder-подход (`X-AINT(X)` vs `0.5`) **не работает** на `7.5` по той же
   причине.
4. **Обратные тригонометрические функции** выражаются через уже работающие
   `DATAN2`/`ATAN2` + generic `SQRT` (DP-ветка сохраняет точность):
   `asin(x)=atan2(x, sqrt(1-x²))`, `acos(x)=atan2(sqrt(1-x²), x)`.
   Порядок аргументов `ATAN2(Y,X)` — стандартный Fortran (проверено:
   `ATAN2(1,2)=0.4636`).
5. **`LEN` — compile-time inquiry.** После rule 12 (`CHARACTER*N` → `INTEGER`
   массив) длина известна статически; lowering подставляет константу `N`.
6. **`INDEX` — цикл, не вызов.** Демонстрация на INTEGER-массиве ASCII-кодов
   (одна буква = один элемент, соглашение F77LIBR v3) даёт `3` и `0`.
   Для строк правила 12 (6-символьные слова в `INTEGER`-массиве) обобщение —
   сравнить `P` символов через `SUBSTR`+`ISTRCM`.
7. **`ISIGN` и `CONJG` — системные имена.** `ISIGN` распознаётся встроенной
   функцией (пытаться определить `FUNCTION ISIGN` нельзя), но **численно
   проверена**: `ISIGN(A,B)=sign(B)*ABS(A)`. Lowering для K42 не нужен.
8. **Символьные предикаты** нуждаются в `ISTRCM`/`STRCMP` из `0o2310` — оба
   уже catalogue-ized; новых модулей не требуется.

---

## 3. Процедуры в F77LIB.FTN и каталог PERSO

**Новых/заменённых процедур нет.** `src/f77libr/F77LIB.FTN` оставлен побайтово
равным HEAD (`b6695d4`): 13 процедур в исходнике, 12 каталогизируемых.

Причина: все 21 элемент выражаются inline через уже доступные нативные функции
и уже каталогизированные `STRCMP`/`ISTRCM`. Каталог `0o2310` находится на
жёстком пределе 12 пользовательских модулей (`08-runtime.md` §5.7: попытка
добавить 13-й `CNJG0` не дала записи). Замена `STRCAT`/`SUBSTR`/`ISTRCM`
недопустима: на них опирается lowering правил 13/14 агента волны 2
(`07-implementation-prep.md` §2). Замена `FMTLNK`/`ISGN0` etc. не потребовалась.

Каталог после пересборки (`tests/run-f77-runtime.sh`, rc=0):

```
PERSO 0o2310 catalog: DINT2 DMOD2 ISTRCM SUBSTR STRCAT STRCMP IDIV ISGN0 IMAX0 FMTLNK MYMAX MYABS FOREX* LO*SYN
```

12 пользовательских модулей + 2 безвредных дубля системных (`FOREX*`, `LO*SYN`),
все с ненулевым transfer vector; базовая зона `0o2300` побайтово неизменна.

---

## 4. Результаты проверок (rc)

| Проверка | rc | Детали |
|:---|:---:|:---|
| `tests/run-f77-runtime.sh` | **0** | каталог 12 модулей; gold == fact (4 строки) |
| `tests/run-glissade-forex.sh` | **0** | 14/14 строк результата совпадают |
| `tests/check-source-words.py` | **0** | `LO*SYN`/`LO*GEN`: 1024/1024 слов |
| `tests/check-label-semantics.sh` | **0** | 0 коллизий |
| `tests/check-constants.sh` | **0** | все литералы вынесены в `,EQU` |
| `tests/check-text-decoded.sh` | **0** | все текстовые константы расшифрованы |
| `tests/run-f77-full.sh` | **0** | gate **20/20**; L0 51/51, L1 51/51, L2 8/8, L3 2 OK/2 SKIP, L4 9/9 |

Все проверки запускались из `/home/azizz/Yandex.Disk/re-forex` при пустом
`~/.besm6/input_queue` (переполнение очереди даёт ложный `БУФ ПЕРЕП`).

---

## 5. Воспроизведение численных proof-прогонов

Временный инструмент `/tmp/.private/azizz/opencode/f77intr/exprprobe.py`
(в репозиторий не входит) собирает декану с `*perso:602300` (и, при нужде,
`*perso:602310,cont`) и печатает каждое выражение отдельной строкой.
Payload-файлы: `p1.txt` (DP/ATAN2), `p2.txt` (наивное округление),
`p4.txt`/`p5.txt` (guard-digit), `p6.txt` (предикаты),
`p7.txt` (INDEX), `p10.txt` (max/min, границы).

```sh
cd /tmp/.private/azizz/opencode/f77intr
rm -f ~/.besm6/input_queue/*
TAG=P5 python3 exprprobe.py p5.txt    # DNINT/IDNINT с guard-digit
TAG=P1 python3 exprprobe.py p1.txt    # DASIN/ACOS/DACOS/DSQRT
TAG=P6 LIBR=1 python3 exprprobe.py p6.txt  # LGE/LGT/LLE/LLT
TAG=P7 python3 exprprobe.py p7.txt    # INDEX
```
