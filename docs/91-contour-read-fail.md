# contour-read: attempt at an on-machine READ in the zone-2350 contour

> ВЕРДИКТ главного агента: formatted READ на контуре `0o2350` — **FAIL**,
> зафиксирован честно. Новые факты (15‑битная адресация, машинный
> float→GOST) решают размещение и вывод, но не **захват ввода**.
> SIMH‑доказательства: `э52` -> `ЗАПРЕЩ.ЭКСТРАКОД`, `э60` ->
> `МАССИВ НЕ СУЩ-Т.`, `э70` -> переполнение таблицы описаний; позитивный
> контроль `xta` печатает `01 1.00 3.00` и доходит до `КОНЕЦ ЗАДАЧИ`.
> A/B «литерал в деке `1`→`2` при том же образе» не получен и не заявлен.
> Отсутствующий примитив: пользовательский путь ввода карты с LUN/дескриптором.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/contour-read/`
(bulky copies under `/dev/shm/contour-read/` via symlinks, because the shared
`/tmp` tmpfs is 100% full). Repo, live disks, tmux session 0 and dispak C
sources were never edited; every attached SIMH image was a copy. C `dispak`
was read as a source oracle only and never used for a reported result.

## VERDICT: FAIL

The contour invoked by `*TRANS:OURMRK*,,412350` **cannot** read a numeric value
from the job's input stream (LUN 41 / vu0 / deck data card) with machine code.
The decisive A/B required by the task (deck INPUT `1` -> `2`, byte-identical
contour image, printed value changes) was therefore **not achievable** and is
not claimed. No host-side value was substituted.

The two new facts from the parent do not remove the blocker: 15-bit modifier
addressing (docs/65, docs/88, docs/89) only solves **where** a word can be
placed/reached in high RAM, and the proven machine float->GOST converter
(docs/89) only solves **how a binary float becomes a printable digit**. Neither
supplies the missing primitive, which is a **user-mode-callable card-input
path**: a way to move one character/digit from the vu0 card stream into a RAM
cell. On this contour that path is absent and is actively refused by the OS.

---

## 1. Documentary determination (FACT vs INFERENCE)

| # | statement | marker | citation |
|:--|:--|:--|:--|
| 1 | The contour implements formatted PRINT (GOST descriptor words at `0o2006..0o2011` + `*64`), A/B proven under SIMH | FACT | docs/83:59-63, docs/83:209-233 (A/B/A `21 1.00 3.00` / `01 ...` / restore, image SHAs `a98e8109...` / `1f4431d1...` / `a98e8109...`) |
| 2 | The contour has **no formatted READ path**: no input extract-code/LUN chain, no field-decoding loop, no input buffer in body/overlay | FACT (declared result) | docs/83:266-273 ("Formatted READ has no path in the contour ... I therefore do not claim contour READ"); docs/77:25 |
| 3 | The only confirmed on-machine "READ" is the **compile-time literal** `READ X/1.0/` -> word `777010` -> body cell; A/B `1.00 -> 7.00` changes the *source literal*, not a data card | FACT | docs/77:25; this is a literal embedded in the translated source, not a stream read |
| 4 | 15-bit `utc 30000` addressing reaches zone N+3 `0o30114..0o30205` (58 clean words); M32/M20 traces show no truncation | FACT | docs/65-high-ram-zone.md; docs/88:40-56, docs/88:134-146; docs/89:39-41, docs/89 §1 raw trace |
| 5 | Machine float->packed-decimal (GOST) conversion works entirely in BESM-6 code (`a/x`, `aex`, `e+x`, `aax`, `asx`, `arx`, `atx`) and the printed digit changes with one machine word | FACT | docs/89:17-33, docs/89:35-88, docs/89:108-125 |
| 6 | `FT*002` transfer cell `0o77776` is page-protected (`Число/Команда в чужом листе`) and reads as 0 in our contour; FTDISP never runs in this deck | FACT | docs/88:26-37, docs/88:83-117, docs/88:171-174 |
| 7 | All `*50` FPU extractcode type codes tried abort from the contour under SIMH; the OS handler at `0o574` diverts and never returns to M32 | FACT | docs/89:122-124, docs/89:131-132; docs/78:29 |
| 8 | `READ(u,fmt)` and OPEN/CLOSE/INQUIRE live only at OS job-control level; no LUN table/file binding is available in Fortran texts alone | FACT (text-level) | docs/83:244-245, docs/79:173-174; docs/plan-f77-full/24-file-card-monitor.md §4 |
| 9 | The contour deck invokes no `*FOREX`, `*FTN` or `*perso`, so no FOREX READ runtime (FT*002 / IOXXFMR* / INPUT*) is installed or callable | FACT (deck) | deck SHA `1d93c468...`, line `*TRANS:OURMRK*,,412350` only; docs/83:39-47 |

**INFERENCE / not proven here:** that some other, undocumented OS entry point
could read a card for a contour task. No such entry was found in the monitor80
sources that are present, and the OS refusals in §3 make it unlikely; this is
not claimed as proof of impossibility for every possible monitor patch.

---

## 2. Machine-level architecture of the blocker (from source, FACT)

* `besm6_cpu.c:1388-1392` - `увв`/EXT (opcode 033), the only instruction that
  reads the vu (card reader) register, is **privileged**:
  `Aex = ADDR (addr + M[reg]); if (! IS_SUPERVISOR (RUU)) longjmp (cpu_halt, STOP_BADCMD);`
  `vu_read()` is reachable only from inside `cmd_033()`
  (`besm6_cpu.c:865-867`, cases `04150`/`04154`). The contour executes in user
  mode (MTR shows `RUU = 040`/`044`, never supervisor), so direct VU access is
  impossible.
* `besm6_cpu.c:1509-1552` - extractcodes `э50..э77` are **not executed in the
  CPU**; they trap: `M[ERET] = nextpc; ... PC = 0500 + opcode`. Whether an
  extractcode works therefore depends on the OS handler in the task context.
  `*64` works (docs/89 trace: `30131 R: ... э64 2004` -> `00564 L: ...`).
* `src/lib21/INPUT_.mad:83,110` - the real card-read path uses `*60 INC` and
  `*52 R52021` (COS) with a 2-word descriptor (`Z00,INC / Z00,INC+27B`),
  inside the monitor INPUT* program. `INPUT*.mad:143` is the actual `*52` card
  read. This program is not installed by our contour-only deck.
* `monitor80-re/inputcal/takecrd.asm` and `permanent/monread%.asm` show that
  card intake is a monitor overlay (TAKECRD*, MONREAD*) using `*70` spool I/O
  and the `MONCARD*`/`КCOUNT*` structures, i.e. OS task state our contour does
  not own.

**Missing primitive, stated exactly:** a callable, user-mode card-input
extractcode (or an OS-provided routine plus its LUN/descriptor/array chain)
reachable from the zone-2350 contour body. The contour has the *placement*
mechanism (`utc` 15-bit addressing) and the *output conversion* mechanism
(docs/89) but no *input capture* mechanism.

---

## 3. New on-machine attempt (SIMH, copies only)

### 3.1 Method

Probe routine installed in the 58 clean words of zone N+3, entered by the
proven same-length substitution `body[0o11] (RAM 0o1770 L) = LONG uj 30114`.
Every high-RAM access is preceded by its own `UTC 30000` in the RIGHT halfword
(the one-instruction modifier rule from docs/88/89). Each probe issues exactly
one candidate input extractcode at `0o30115 L` and then prints the **untouched
baseline GOST word** with `*64 2004`. Thus no Python-computed value can appear
as a result; any change would have to come from on-machine execution.

Deck (SHA `1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2`):
`ШИФР 410300 ЗС5^ / ДИС 41(2048)^ / ОЗУ 32^АЦП 32^ / ЕЕВ1А3 / *NAME OURMRK /
*TRANS:OURMRK*,,412350 / PROGRAM MAIN / END / *EXECUTE / *END FILE / `````` / ЕКОНЕЦ`.
No `*FOREX`, `*FTN`, `*perso`.

Harness: isolated `TMUX_TMPDIR`, console only via `capture-pane -p -S -2000`,
all input via `send-keys`, boot marker `ДATA:`, `ДАЙ А0` / `ДАЙ А1` / `НОМВ`
before the deck, post-job-start `НОМВ` after the job-start line, stock
`attach -n prn0/prn1` untouched, md41 = workspace copy, `at vu0 <deck>`,
MTR via SIMH `set debug` + `set cpu debug`.

### 3.2 Results (raw ACPU, decisive device = prn1 / `output1.txt`)

| case | candidate primitive | ACPU decisive line at PC `30115` | printed value |
|:--|:--|:--|:--|
| `posctl` (positive control) | `xta 0o30170` instead of an extractcode | no error | `01 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` |
| `ec60` / `ec60zero` | `Э60` (I/O control, input) | `МАССИВ НЕ СУЩ-Т.  +284814860828⏨-19  0010320000200004`; dump `АП=30115` | none (routine aborted before `*64`) |
| `ec52zero` | `Э52` (COS/card read), operand 0 | `ЗАПРЕЩ.ЭКСТРАКОД  +000000000000⏨+00  0000200600002006`; dump `АП=30115` | none |
| `ec52desc` | `Э52` with the documented 2-word descriptor (`0o30174`, `0o30204`) | `ЗАПРЕЩ.ЭКСТРАКОД ...`; dump `АП=30115` | none |
| `ec70` | `Э70` (disk/drum read) | `ПЕРЕПОЛНЕНА ТАБЛИЦА ОПИСАНИЙ` / `ЕRRОR IN SТАNDАRТ АRRАУ` | `01 1.00 3.00` then error |

Raw ACPU excerpts (`runs/acpu1_ec60.txt`, `runs/acpu1_ec52desc.txt`,
`runs/acpu_posctl.txt`, `runs/acpu_ec70.txt`):

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350

 МАССИВ НЕ СУЩ-Т.    +284814860828⏨-19    0010320000200004
  АП   Э     РК    И1 ...  И15   И16   И17   КРА  ЗПСЧ
30115 30115 00006 02034 00000 ... 01764 30170 53401 00000 53400
...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0003011520000000
```

```
 ЗАПРЕЩ.ЭКСТРАКОД    +000000000000⏨+00    0000200600002006
  АП   Э     РК    И1 ...  И15   И16   И17   КРА  ЗПСЧ
30115 30115 00006 02034 00000 ... 01764 30170 53401 00000 53400
```

Positive control:

```
 01 1.00 3.00
 ...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

### 3.3 Raw SIMH MTR excerpt (`logs/MTR_ec52_excerpt.txt`, case `ec52desc`)

```
00460 R: 00 30 00000 пб
01770 L: 00 30 30114 пб 30114
30114 L: 00 010 2004 сч 2004
      Memory Read [02004] = 0000 2006 0000 2006
30114 R: 00 22 30000 мода 30000
      M20 = 30000
30115 L: 00 052 0170 э52 170 = 30170
      M16 = 30170
      M21 = 02007
      M32 = 30116
      RUU = 044
00552 L: 00 000 2213 зп 2213
00552 R: 00 30 70000 пб 70000
70000 L: 00 042 0016 счи 16
      ACC = 0000 0000 0003 0170
70000 R: 00 012 0230 нтж 230
      Memory Read [00230] = 0000 0000 0000 7777
      ACC = 0000 0000 0003 7607
70001 L: 00 26 70002 по 70002
70001 R: 00 27 05156 пе 5156
...
```

FACT from this trace: the contour's `э52 170` resolves through `utc 30000` to
the **full 15-bit** address `0o30170` (M16 = 30170, M32 = 30116), traps to the
OS handler at `0o552`, and the handler enters the privileged region at
`0o70000`. The OS then rejects the request for this task
(`ЗАПРЕЩ.ЭКСТРАКОД` in ACPU). No card data reached `0o30170`.

### 3.4 Interpretation (FACT vs INFERENCE)

**FACT:** from the contour, `Э52` is refused as a forbidden extractcode;
`Э60` fails because the required array/descriptor does not exist in this
task context; `Э70` overflows the descriptor table. The positive control
shows the same image/harness still prints and reaches `КОНЕЦ ЗАДАЧИ`.

**INFERENCE:** the refusals are consistent with the documented fact that the
LUN/array/descriptor state for card input is owned by the monitor/Fortran
runtime (docs/83 §5, docs/79 §5, docs/plan-f77-full/24 §4), which this
contour-only deck never installs. I did not attempt a monitor patch, which is
outside the task scope (copies only, no dispak C edits).

**Not claimed:** that no FOREX/runtime READ exists at all. The system
compiler's `READ 10,X -> 3.50` (docs/83 §2, J04) is explicitly **not** evidence
for our contour.

---

## 4. Decisive A/B status

Required A/B: same contour image SHA, deck INPUT `1` -> `2`, printed value
changes. **Not performed / FAIL** because no on-machine input exists to change.
The only A/B available here is positive control vs extractcode cases with the
same builder, which shows the failure is specific to the input primitives,
not to the harness.

---

## 5. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (repo tool baseline; reproduces docs/87/89)
a8e63c41038a29d9297355ec7835beed01e7c3efdad4242d090ce01d169904b4  images/2048_posctl  (positive control)
6e87b88fb1cc6a622281d3f156f8cda0384dbe24d22533b43251b130caf9467f  images/2048_ec60
8d68ddb5daf1ff86104131c95c5b790e8999be84d94d2bbd72d467fca58b174b  images/2048_ec60zero
42b589a9d1c8d5450d5ac6d193466a0bad5f7e39c909a54deaea58e29a85df18  images/2048_ec52
fbad0f1f5a23dd3e33adb6bdfe0043fcef7dbfc34cc496acb8b5e42727c114f9  images/2048_ec52zero
9e924d2e8243d584f94874bcb29bb07a745623f40b80c2299110ef15126d4453  images/2048_ec52desc
cea262ca8f57886cc2fdbb54a8b21a9b601d7a111393652e0ea9bb3eebce5c34  images/2048_ec70
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  decks/deck_trans.b6
222152b14addae64b96fb68873701f16af05fe4c4b626a2946bdee3e121e594f  runs/acpu_posctl.txt
e2463274ad8721f80730ab195ecddce4d66f4da5ea8de13af0be9c1e2e429191  runs/acpu1_ec60.txt (decisive)
193b06b05f6e5895f85483fd939e79b4374f50d127faaf62309bf99ad81c028e  runs/acpu_ec60zero.txt
46ff724c263d98da435b737eb7ba23d1aeabe57da04a8e12d2756f23d6dc1cac  runs/acpu_ec52zero.txt
3897b9f9e8b03a071eb74a8223dff29bb4939f17462e6c1696c464af9f729abd  runs/acpu_ec52desc.txt
0e8d1613f03b493ea0f542605a81f7bec2172da04fe8ce7a41099131ab5f42cc  runs/acpu_ec70.txt
918a2fc56b4670792551ff4b6be65228a87f8428df5fc993c16521ef79d53ab7  logs/MTR_ec52_excerpt.txt
```

The 405 MB full SIMH debug file was reduced to the cited excerpt and deleted,
to avoid filling the shared tmpfs.

---

## 6. Safety record

* No repo/live-disk/tmux-0/dispak-C edits. `git status` in
  `/home/azizz/Yandex.Disk/re-forex` is unchanged from entry
  (` M tools/run_besm6_deck.py`, `?? tests/plan-f77/64-monitor-patch/`).
* Only workspace copies attached to SIMH; stock `attach -n prn0/prn1` lines
  kept verbatim.
* Console via isolated `TMUX_TMPDIR` + `capture-pane`; input only `send-keys`.
* C `dispak` sources were read as an oracle only; no C run result is reported.

## 7. Evidence index

* `scripts/build_ec.py`, `scripts/build_probe.py` - image builders (copies).
* `scripts/setup_read.py`, `scripts/drive_read.py` - isolated SIMH harness.
* `decks/deck_trans.b6` - contour-only deck.
* `runs/acpu1_ec60.txt`, `runs/acpu_ec52desc.txt`, `runs/acpu_ec52zero.txt`,
  `runs/acpu_ec60zero.txt`, `runs/acpu_posctl.txt`, `runs/acpu_ec70.txt` - raw ACPU.
* `runs/console_*.txt`, `logs/drive_*.log` - boot/job-start/completion.
* `logs/MTR_ec52_excerpt.txt` - raw SIMH per-halfword trace of the `э52` trap.
* `images/2048_*` - all SIMH images (copies).

DONE
