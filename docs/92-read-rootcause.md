# ROOT CAUSE: why the zone-2350 contour's extractcodes fail

> ПРИЧИНА НАЙДЕНА (FACT, по MTR реально исполняемого монитора): `э52`
> векторится не в `0o0522`, а в `0o0552` (`0500+052`). Решающая ветка —
> `0o5162 R`: бит привилегии в дескрипторе задачи `M[0o72451+0o41] &
> 0o100000 == 0`, поэтому берётся `по 5164` и печатается `ЗАПРЕЩ.ЭКСТРАКОД`.
> У задачи, созданной `*TRANS`, этого бита нет. `э60`/`э70` падают позже
> на проверках массива/таблицы описаний, которых задача тоже не имеет.
> Код обработчика грузится при загрузке ОС с носителя монитора, а не из
> зоны диска 2048. Легальная установка контекста из user mode циклична.
> Минимальные варианты патча на копии — §6; они не являются продуктом.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/read-rootcause/`.
Read-only w.r.t. the repository, all live disks, tmux 0 and dispak C sources.
No SIMH run, no live disk attached, no C patch, no repo edit. A byte copy of
the disk-2048 image was made in the workspace (SHA-256 unchanged,
`a98e8109...`) and analysed with `lindis.py`-style word decoding; all other
inputs were read in place. Git status on entry and exit is identical.

---

## 0. Executive answer

All three failures are **OS-handler decisions taken after the BESM-6 trap**,
not SIMH encoding problems. For `э52` the decisive branch is identified at the
instruction level: the supervisor tests a **privilege bit in the current task's
descriptor** (`M[0o72451+0o41] & 0o100000`). The bit is **0** for the
`*TRANS`-created contour task, so the handler takes the abort branch and prints
errtxt[36] `ЗАПРЕЩ.ЭКСТРАКОД`. `э60`/`э70` die later in the same supervisor
complex, on task-state (input-array / descriptor-table) checks that this
contour task also does not own.

A *TRANS-invoked contour cannot legally install that state from user mode: the
setup itself needs the privileges that are being refused (circular). The
minimum OS change is described in §5.

---

## 1. Correction to the stated premise (FACT)

| item | stated | actual |
|:--|:--|:--|
| vector for `э52` | `0o0522` | **`0o0552`** |

SIMH `besm6_cpu.c:1557-1558` executes `PC = 0500 + opcode` with `opcode` the
octal opcode (`052`). `0500+052 = 0552`. The on-machine MTR trace confirms the
first instruction lives at `00552`. `э60 -> 0560`, `э70 -> 0570` are correct.

Also (FACT, correction to the premise): **the handler machine code is not
stored literally in disk 2048.** I searched the copy of disk 2048 (33,024,000
bytes), the original `/usr/local/share/besm6/2048`, `2348`, `boot_dispak.b6`,
the drum images and the attached system MD images for the exact 48-bit words
of the executed handler instructions, in both 6-byte and 8-byte little-endian
encodings:

```
0o552   word = 0o0000221303070000  hex 0x00048b0c7000
0o70000 word = 0o0042001600120230  hex 0x02200e00a098
0o5156  word = 0o0042001600002217  hex 0x02200e00048f
```

Result: **no match in disk 2048** (only coincidental 6-byte hits of the very
common `счи 16`/`зп ...` pairs on other media). The resident monitor that owns
these vectors is loaded into RAM at boot (via `load boot_dispak.b6; run 2000`
in `OSZAGR/dispak.ini` and the system area of the monitor media), not read as
a verbatim RAM image from a zone of disk 2048. So the task's instruction to
"disassemble the handler from a copy of disk 2048" cannot be satisfied
literally; the decoded handler evidence below comes from the **raw SIMH MTR
trace of the actual executing OS code**, which is strictly stronger evidence
than a disk dump would be.

---

## 2. FACT: the trap mechanism (SIMH source)

`besm6_cpu.c:1509-1558`: opcodes `050..077` (and 0200/0210) go to
`stop_as_extracode`:

```
Aex = ADDR (addr + M[reg]);
M[ERET]  = nextpc;                       /* return address */
M[SPSW]  = (M[PSW] & (INTR|MMAP|PROT disable)) | IS_SUPERVISOR(RUU);
M[PSW]   = INTR|MMAP|PROT|INTR_HALT disable;
M[14]    = Aex;                          /* operand handed to OS in R16 */
RUU      = SET_SUPERVISOR (RUU, SPSW_EXTRACODE);
PC       = 0500 + opcode;                /* 0552 / 0560 / 0570 */
```

Therefore: user mode at the point of the trap is irrelevant to the `э` decode
itself; the task context (saved in supervisor cells) is what the handler
judges. `M[14]` is register 16 in the ACPU dump and is the effective operand.

---

## 3. FACT: `э52` handler path and the exact rejecting branch

Source: `/dev/shm/contour-read/logs/MTR_ec52_excerpt.txt` (raw per-halfword
SIMH trace, saved by the earlier session; no new SIMH run was made here).
Instruction encoding was re-verified with a local emulation of
`besm6_fprint_insn`/`besm6_fprint_cmd` (`besm6_sys.c:420-460`, `BBIT(n)=1<<(n-1)`),
so every halfword below reproduces the printed fields exactly.

```
30115 L: 00 052 0170  э52 170 = 30170   ; RUU=044, M16(Aex)=30170, M32=30116
00552 L: 00 000 2213  зп 2213           ; M[02213] = ACC
00552 R: 00 30 70000  пб 70000          ; -> supervisor entry
70000 L: 00 042 0016  счи 16            ; ACC = M[16] = Aex = 0o30170
70000 R: 00 012 0230  нтж 230           ; ACC ^= M[0o230]=0o7777 -> 0o37607
                                          ; RAU becomes LOGICAL
70001 L: 00 26 70002  по 70002          ; UZA: logical && ACC!=0 -> not taken
70001 R: 00 27 05156  пе 5156          ; U1A: logical && ACC!=0 -> taken
05156 L: 00 042 0016  счи 16            ; ACC = Aex
05156 R: 00 000 2217  зп 2217           ; M[02217] = Aex
05157 L: 00 26 05164  по 5164
05157 R: 00 030 0077  счрж 77           ; ACC = 0o3000000...
05160 L: 00 015 0547  или 547           ; M[0o547] = 0o12 -> ACC = ...0012
05160 R: 00 000 2214  зп 2214           ; M[02214] = built word
05161 L: 00 23 00474  мод 474           ; M20 = M[0o474] = 0o72451, RUU=064
05161 R: 00 010 0041  сч 41             ; read M[0o72451+0o41] = M[72512]
                                          ; = 7774 2554 0000 0000
05162 L: 00 011 0143  и 143             ; AND M[0o143] = 0000 0000 0010 0000
                                          ; ACC = 0   <-- DECISIVE TEST
05162 R: 00 26 05164  по 5164          ; LOGICAL && ACC==0 -> BRANCH TAKEN
05164 L: 00 042 0016  счи 16
05164 R: 00 036 0102  сда 102
05165 L: 00 27 06616  пе 6616           ; -> error/abort subroutine
06616 L: 00 010 0145  сч 145            ; M[0o145] = 0o20000
06616 R: 16 31 16641  пв 16641(16)
16641 L: 00 100 3005  зп 73005
16641 R: 00 042 0016  счи 16
16642 L: 00 000 2204  зп 2204           ; M[02204] = return link
16644 L: 00 042 0015  счи 15            ; ACC = M[15] = 0o1764
16644 R: 00 000 2216  зп 2216           ; M[02216] = 0o1764
16645 L: 00 23 00474  мод 474 ; 16645 R: 15 24 00000 уиа (15) ; M15=0o72451
```

Cross-check against the ACPU dump for `ec52zero` / `ec52desc`:
`... И15=01764 И16=(30000 or 30170) И17=53401 КРА=00000 ЗПСЧ=53400` - the
`01764` written at `0o16644` is literally the dumped И15, and И16 is `Aex`
from `M[14]`. This is the standard DISPAK task-abort dump.

**Exact branch condition (FACT):**

```
(M[ M[0o474] + 0o41 ] & 0o100000) == 0   ->  по 5164 taken  ->  abort
```

with, in this run, `M[0o474] = 0o72451`, tested word `M[0o72512]`,
mask word `M[0o143] = 0o100000`.

The operand is irrelevant: `ec52zero` (operand 0, dumped Aex `0o30000`) and
`ec52desc` (2-word descriptor, dumped Aex `0o30170`) both produce the same
`ЗАПРЕЩ.ЭКСТРАКОД`. Therefore this is a **task-level permission refusal**,
not validation of the descriptor the probe supplied.

`errtxt.c:52` maps error number **36** to ` ЗАПРЕЩ.ЭКСТРАКОД`.

---

## 4. FACT: `э60` and `э70`

There is no surviving MTR trace for these cases, so only the ACPU dumps and
documentation are cited; the internal branch addresses are INFERENCE.

### 4.1 `э60 -> МАССИВ НЕ СУЩ-Т.` (error 59, `errtxt.c:75`)

ACPU (`runs/acpu1_ec60.txt`):

```
 МАССИВ НЕ СУЩ-Т.    +284814860828⏨-19  0010320000200004
 30115 30115 00006 02034 00000 00000 00000 00001 00000 00000
       03332 03015 01160 06010 06000 01764 30170 53401 00000 53400
```

Same abort dump as э52 (И15=01764, И16=Aex=30170, И17=53401) but a different
error number, so the failure is a *later* task-state check in the same
supervisor group at vector `0o560`, not the permission bit at `0o5162`.

Documented semantics (`/home/azizz/Yandex.Disk/re-dispak/docs/Dispak-programmer-guide.md`,
§5.3.9 and §5.3.63), FACT:

> `МАССИВ НЕ СУЩ-Т.` = "Входной поток задачи не содержит массива с указанным
> номером" (the task's **input stream** contains no array with that number).

Arrays are defined by an "вводное слово" (introductory word) and terminated by
`E`; the task passport is array 0. The contour deck
(`*TRANS:OURMRK*,,412350`, no `вводное слово`/`E` structures) does not contain
such an array. So the OS correctly reports that the requested input array does
not exist in this task's input stream.

(Correction to the earlier wording: this message is about **input-stream
arrays**, not about a generic "array descriptor table" in RAM.)

### 4.2 `э70 -> ПЕРЕПОЛНЕНА ТАБЛИЦА ОПИСАНИЙ / ERROR IN STANDARD ARRAY`

ACPU (`runs/acpu_ec70.txt`), dump at `АП=02017`:

```
 01 1.00 3.00
ПЕРЕПОЛНЕНА ТАБЛИЦА ОПИСАНИЙ
ЕRRОR IN SТАNDАRТ АRRАУ
 02017 02017 00006 02034 00000 ... И10=02065 И11=03332 И12=03015
       И14=02020 И15=00000 И16=02017 И17=00000 ... ЗПСЧ=53400
```

FACT: `ERROR IN STANDARD ARRAY` is emitted by the FOREX `FORTLIBR` runtime:
`re-forex/src/FOREX_RUNTIME.mad:318-322` (diagnostic words `TL0013="ERROR"`,
`TL0014="IN STA"`, `TL0015="NDART"`, `TL0011="ARRAY"`). This text is **not** in
`errtxt.c`; it belongs to the standard-array library. `ПЕРЕПОЛНЕНА ТАБЛИЦА
ОПИСАНИЙ` is likewise not in `errtxt.c`. So the `э70` trap reaches the
standard-array/descriptor machinery, which has no free descriptor entry for a
task that never opened a file/LUN. (The contour still printed `01 1.00 3.00`
and reached `КОНЕЦ ЗАДАЧИ`; this is not a total abort.)

---

## 5. What setup is required, and can a *TRANS contour do it?

### FACT (from the real card-read path)

`re-forex/src/lib21/INPUT_.mad` (monitor overlay INPUT*, lines 17405-17479):

```
XTA,PROC R          ; card reader status
...
*60,INC             ; I/O control (input) - obtain card image into INC
...
XTA,R52021          ; 2-word descriptor:
R52021: LOG
        Z00,INC          ; word 1 -> input buffer INC
        Z00,INC+27B      ; word 2 -> +27 bytes
*52,R52021          ; actual CARD READ  (COS, Tyurin-1985 ИР 052 A)
...
*52,REF022          ; release/refuse card
```

So a successful card read needs: (a) the right to issue `э52`/`э60` at all,
(b) a LUN bound to `vu0`/deck input, (c) a 2-word COS descriptor whose first
word points at a buffer that the **monitor** owns or that the task is allowed
to hand over. `INPUT*` is a monitor overlay: it runs as monitor code with the
task descriptor's privilege bit set and with the input-stream/LUN tables
already built by the job-control reader (`КCOUNT*`, `MONCARD*`, `TAKECRD*`,
`MONREAD*` - `monitor80-re/inputcal/takecrd.asm`,
`permanent/monread%.asm`, as cited in docs/91 §2).

Tyurin-1985 (via `docs/lib21/04-extract-codes.md:224-225`) identifies
`Э52 R52021` as `COS (ИР 052 A)`.

### FACT (the contour's state)

* Deck contains only `*NAME OURMRK / *TRANS:OURMRK*,,412350`; no `*FOREX`,
  `*FTN`, `*perso`, no Fortran `READ`, no monitor overlay (docs/91 item 9).
* MTR shows `RUU=040/044`, i.e. user mode, except inside the trap.
* The tested privilege bit in the task descriptor is 0 (§3).
* The input stream has no `E`-terminated arrays (§4.1).
* A positive control (`xta` instead of an extractcode, same image/harness)
  prints `01 1.00 3.00` and reaches `КОНЕЦ ЗАДАЧИ`: the harness and contour
  itself are sound.

### INFERENCE (well-supported, not directly traced)

The contour task cannot establish the required state, because:

1. Setting the privilege bit, binding a LUN, and allocating a descriptor are
   themselves monitor operations reachable only through extractcodes/COS or
   through job-control directives that replace the executing program.
2. When the contour tries the first such extractcode, the same supervisor
   refuses it (the `M[0o72451+0o41] & 0o100000 == 0` branch).
3. `*TRANS` only transfers control to the named module in the fixed zone
   (`*TRANS:OURMRK*,,412350`), it does not install INPUT*/FOREX runtime into
   the *contour's* task context. Loading FOREX3* via `*TRANS:FOREX3*,,411550`
   (logs in `docs/plan-f77-full/`) makes FOREX the executing program, so the
   contour no longer runs.

So: **impossible from user mode in this configuration**; the prerequisite is
circular. Not claimed as a proof for every conceivable monitor patch.

---

## 6. MINIMUM OS/monitor change (on a copy) to make `э52` read a card into RAM

Two options, in increasing order of certainty. Neither was applied or run
here; both are specifications derived from the decoded path.

**A. Sufficient, self-contained (INFERENCE, but smallest provable change).**
Patch the supervisor code reached from vector `0o552`, not SIMH and not the
contour image:

1. At `0o5162 R` replace the branch `по 5164` (taken when the privilege bit is
   clear) with a branch to a small routine placed in a free supervisor word
   range (e.g. unused words near `0o70000`, after verifying they are free in a
   RAM dump). Do **not** touch the `счи 16`/`нтж 230` prologue at `0o70000`:
   `M[14]` already holds the caller's target address `Aex`.
2. The routine issues the privileged `увв`/EXT (opcode 033) with
   `Aex = 04150` (or `04154`) - `besm6_cpu.c:865-867` routes those to
   `vu_read()`, which returns one punched-card line in ACC. `Aex` must be
   formed as a long-format address (`0o3070000`-style encoding), as verified
   above against `besm6_fprint_insn`.
3. Store ACC to `M[ M[14] ]` with `зп 16`-style addressing (or load `M[14]`
   into an index register first), then return through the standard
   extractcode exit that restores `RUU` from `M[SPSW]` and `PC` from
   `M[ERET]` (the same exit `*64` uses successfully).

That is ~10-20 new machine words plus one rewired branch. It bypasses the
LUN/descriptor tables entirely and writes exactly one card word into the RAM
cell named by the contour's operand. The patch must be applied to whatever
medium actually supplies the monitor image to RAM (§1: *not* a zone of disk
2048), on a copy.

**B. Smaller patch to existing state, needs verification (INFERENCE).**
Set the task-descriptor privilege bit `M[0o72451+0o41] |= 0o100000` for the
contour task (e.g. from a monitor directive on a copy) and keep the existing
2-word descriptor (`Z00,buffer / Z00,buffer+27B`). Then `по 5164` is not taken
and the normal COS/INPUT* path may service the read. This is *not proven*
here: the remaining supervisor code after `0o5163` was not traced, and a LUN
binding may still be required. Option A is the recommended minimum because it
exercises the same real `vu_read()` path the monitor itself uses and does not
depend on unverified descriptor handling.

---

## 7. FACT / INFERENCE index

| # | statement | marker | evidence |
|:--|:--|:--|:--|
| 1 | handler vectors are 0552/0560/0570, not 0522 | FACT | `besm6_cpu.c:1557-1558`; MTR `00552` |
| 2 | handler words absent from disk 2048 | FACT | byte search of SHA-identical copy, 6/8-byte LE |
| 3 | trap saves Aex in M[14], PC=nextpc in M[ERET], supervisor set | FACT | `besm6_cpu.c:1547-1555` |
| 4 | э52 abort branch is `(M[72451+41] & 100000)==0` at `05162` | FACT | decoded MTR, `по 5164` taken |
| 5 | ACPU dump И15=01764 comes from `счи 15` at `16644` | FACT | MTR + ACPU cross-check |
| 6 | operand does not change the refusal | FACT | `ec52zero` vs `ec52desc` dumps |
| 7 | `МАССИВ НЕ СУЩ-Т.` = missing input-stream array | FACT | Programmer guide §5.3.9/§5.3.63 |
| 8 | `ERROR IN STANDARD ARRAY` from FORTLIBR runtime | FACT | `FOREX_RUNTIME.mad:318-322` |
| 9 | real read path = `*60 INC` + `*52` 2-word descriptor | FACT | `INPUT_.mad:17405-17479` |
| 10 | contour has no FOREX/INPUT* context, user mode | FACT | deck SHA in docs/91; MTR RUU=044 |
| 11 | privilege bit absence is due to *TRANS user task | INFERENCE | consistent with 4+10 |
| 12 | `э60`/`э70` fail at later task-state checks | INFERENCE | dumps differ from э52; no trace kept |
| 13 | setup impossible from user mode here | INFERENCE | circular dependency |
| 14 | option A patch is sufficient | INFERENCE | based on `vu_read()` source and trap return path |

---

## 8. Safety record

* Workspace copies/scripts only under `/tmp/.private/azizz/opencode/read-rootcause/`.
  Disk copy SHA-256 equals the parent's `2048_base` (`a98e8109...`).
* No SIMH invocation, no tmux 0, no live disk attached/written, no C patch,
  no repo edit. `git status --short` unchanged (` M tools/run_besm6_deck.py`,
  `?? tests/plan-f77/64-monitor-patch/`).
* Read of `/home/azizz` by broad grep was aborted/finished without writes.

DONE
