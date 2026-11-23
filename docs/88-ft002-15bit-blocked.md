# FT*002 (0o77776) / LINK 0o74012 15-bit reachability from zone-2350 contour

> ФИНАЛЬНЫЙ ВЕРДИКТ главного агента: 15‑битная адресация **работает** (LONG
> `uj 77776` даёт M33 = 0o77776, без усечения до 0o776), но страницы
> `0o77776` и `0o74012` защищены MMU SIMH: `Число в чужом листе` /
> `Команда в чужом листе` (`STOP_OPERAND_PROT` / `STOP_INSN_PROT`).
> Позитивный контроль `utc 2000 / arx 6` читает `0o2006` без трапа.
> Значит `FT*002/INTPRT` из резидентного монитора Дубна **недоступен**
> из нашего контура — путь float→GOST через рантайм закрыт фактом.
> CORE C‑эмулятора показывает ячейку передачи `0o77776 = 0`, потому что
> FTDISP в нашем `*TRANS`‑деке не исполняется. Никаких packed‑decimal байтов
> и end‑to‑end A/B получено не было.

Experiment on COPIES only. Workspace: `/tmp/.private/azizz/opencode/ft002-15bit/`.
Repo, live disks, `/usr/local/share/besm6`, tmux session 0 and dispak C sources were
never edited. All attached images were workspace copies; base `dispak.ini` had
`attach -e md45 ~/.besm6/2348` (live) and it was rewritten to a workspace copy.
Stock `attach -n prn0/prn1` kept verbatim; ACPU copied after each run.
Boot marker `ДATA:` via `capture-pane` only; all input via `send-keys`;
`ДАЙ А0`/`ДАЙ А1`, `НОМВ` before deck and `НОМВ` after job start; isolated
`TMUX_TMPDIR`. Deck SHA-256
`1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2`;
its only translator line is `*TRANS:OURMRK*,,412350`, plus `ДИС 41(2048)^`;
no `*FOREX`, `*FTN`, `*perso`.

## VERDICT

| question | verdict |
|:--|:--|
| (a) executable code present at 0o77776 during our contour run? | **FAIL / NO** |
| (b) does modified-address read/jump reach 0o77776 (not truncated to 0o776)? | **FAIL in effect** — address arithmetic reaches it, but the access traps (split below) |
| (b1) did the 15-bit address resolve to 0o77776 / 0o74012, not 0o776 / 0o12? | **PASS** (address decode only) |
| (b2) did the read/jump actually succeed in touching the cell? | **FAIL** (SIMH page-protection trap) |
| (c) FT*002 callable with float in ACC, producing packed-decimal bytes? | **FAIL** — not invoked, no packed decimal produced |

The overall goal (on-machine float→packed-decimal conversion, no Python) was
**not achieved**. No end-to-end A/B was attempted because (a)/(b) failed.

## 1. Encoding used (FACT, derived from SIMH source + repo docs)

From `/home/azizz/Yandex.Disk/simh/BESM6/besm6_cpu.c:1049-1062,1090-1091,1554-1557`:

- halfword `RK`; `reg = RK >> 20` (top nibble, modifier register M0..M17).
- `RK & BBIT(20)` (= bit 19, 0-based) set → LONG form: `addr = RK & 0o77777`
  (full 15 bits), `opcode = (RK >> 12) & 0o370`. Long `utc`(мода)=0o220,
  `uj`(пб)=0o300, `vjm`(пв)=0o310.
- otherwise SHORT: `addr = RK & 0o7777`; if `RK & BBIT(19)` (bit 18, 0-based)
  then `addr |= 0o70000`; `opcode = (RK >> 12) & 0o077`.
- `Aex = ADDR(addr + M[reg])`, `ADDR` masking to 15 bits.
- `utc A` sets `M[MOD]` = M20 (octal 020) = Aex **for the next halfword only**
  (`next_mod` applied at `besm6_cpu.c:1740-1745`). This is the same mechanism
  proven in `docs/65-high-ram-zone.md:76-80` for `utc 30000 / arx 155 → 0o30155`.

Same-length substitutions in the executed contour word at RAM 0o1773
(builder body index 14 octal = decimal 12; baseline word `uj 0(15)`):

| case | RAM 0o1773 word (hex) | decoded |
|:--|:--|:--|
| `read77776` | `0x097000008FFE` | `utc 70000` / `xta 7776` → Aex 0o70000+0o7776 = **0o77776** |
| `read74012` | `0x09780000800A` | `utc 74000` / `xta 12` → **0o74012** |
| `jump77776` | `0x0C7FFE000000` | LONG `uj 77776` |
| `jump74012` | `0x0C780A000000` | LONG `uj 74012` |
| `ctrl2006` | `0x09040000B006` | `utc 2000` / `arx 6` → 0o2006 (positive control) |
| baseline/noop | `0x00DC0000090000` | original `uj 0(15)`; noop patch reproduced base SHA exactly |

RAM 0o1774 received the original return word in every case (guarded fallthrough).

## 2. Tracing methodology and its deviation (FACT)

`BESM6_MTR_LO/HI/N` and `BESM6_DD_DEBUG` are **not compiled into the SIMH
binary** (`strings /home/azizz/Yandex.Disk/simh/BIN/besm6` has no such tokens;
also recorded in `docs/plan-f77-full/40-hang-repro.md:50-54`). They exist only in
the C emulator `/home/azizz/Yandex.Disk/dispak/build/dispak/dispak`. Therefore:

- Authoritative machine runs: SIMH with `set debug <workspace file>` +
  `set cpu debug` (`besm6_trace.c:179-195`, `besm6_cpu.c:1070-1073`), enabled
  from boot because the contour executes during the `*TRANS` phase **before**
  the `B075` job-start line.
- C emulator with `BESM6_MTR_LO=01770 HI=01770 N=60` was run as **ORACLE ONLY**
  (never success evidence), for a narrow windowed MTR view of the contour.

## 3. SIMH raw trace lines (authoritative, copies only)

Decisive excerpts are saved in `runs/simh_decisive_excerpts.txt`.

### 3.1 `read77776` — modifier armed, operand read traps

```
01773 L: 00 22 70000 мода 70000
      M20 = 70000
      RUU = 060
01773 R: 00 010 7776 сч 7776
----- 01774L: Число в чужом листе -----
00500 L: 00 000 2213 зп 2213
      M21 = 02003
      M27 = 01420
      M33 = 01774
```

`besm6_cpu.c:319-320`: "Число в чужом листе" = `STOP_OPERAND_PROT`, paging
error during load/store (`besm6_mmu.c:294-308`, `mmu_protection_check`).
No `Memory Read [077776]` line exists. The read never returns data.

### 3.2 `jump77776` — PC reaches 0o77776, instruction fetch traps

```
01773 L: 00 30 77776 пб -2
----- 77776L: Команда в чужом листе -----
00500 L: 00 000 2213 зп 2213
      M27 = 01400
      M33 = 77776
```

`Команда в чужом листе` = `STOP_INSN_PROT`, paging error during fetch
(`besm6_mmu.c:585-599`, `mmu_fetch_check`). This is direct proof that the LONG
jump resolves to the **full 15-bit** address 0o77776 and does **not** truncate
to 0o776 (M33 = 77776). Execution there is blocked.

### 3.3 `read74012` and `jump74012` — same result at the LINK cell

```
01773 L: 00 22 74000 мода 74000
      M20 = 74000
01773 R: 00 010 0012 сч 12
----- 01774L: Число в чужом листе -----
```

```
01773 L: 00 30 74012 пб 74012
----- 74012L: Команда в чужом листе -----
      M33 = 74012
```

### 3.4 Positive control `ctrl2006` — modifier mechanism itself is sound

```
01773 L: 00 22 02000 мода 2000
      M20 = 02000
01773 R: 00 013 0006 слц 6
      Memory Read [02006] = 0040 0417 0020 7000
      ACC = 0050 3617 0040 7004
01774 L: 15 30 00000 пб (15)
```

No trap. Therefore the failures above are specific to the protected high
pages, not a defect in the encoding or in arming M20.

## 4. C-emulator MTR oracle (NOT success evidence)

Saved in `runs/c_mtr_oracle_excerpt.txt` and `cwork2/mtr_narrow.txt`:

```
MTR 01772L *64    2004(0) AU=40041700207000 ...
 21 1.00 3.00
MTR 01773L utc    70000(0) AU=40041700207000 ... 20=01770
MTR 01773R xta    77776(0) AU=40041700207000 ... 20=70000
MTR 01774L uj     0(15) AU=0000000000000 ...
```

The C disassembler resolves the modified address to `77776(0)` (FACT of
address computation) and AU after the read is 0. C CORE dump at PC 0o1770
(`cwork2/cases/oracle_narrow/core-pc.bin`) gives:

```
01770 = 0010200600132020   01771 = 0013202100002006
01772 = 0064200402200000   01773 = 0227000000107776
01774 = 6700000002200000
77774 = 0000000000000000   77775 = 0000000000000000
77776 = 0000000000000000   77777 = 0000000000000000
```

So 0o77776 holds zero in this contour run, consistent with the fact that
FTDISP (which writes FT* entry addresses into the 77xxx cells,
`src/FOREX_RUNTIME.mad:118-120,175-186`) is never invoked by our `*TRANS` deck.

## 5. Console / ACPU excerpts (SIMH)

Every case still printed the baseline line and ended normally, because the
`*64` print at RAM 0o1772 executes **before** the substituted word at 0o1773:

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350
 21 1.00 3.00
 ...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

Boot showed `2048 - 41` in all runs (md41 = contour copy). Because the patch
point is after the print, this ACPU line is **not** evidence that FT*002 ran;
no end-to-end float→packed-decimal value was ever produced.

## 6. Image SHAs (SHA-256, re-hashed after runs)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base
8be8a7196d974c1a3b7a1fe54e032b223c55875a9e970427f2d5a6fb04800fa1  2048_read77776
1bc35380c13e8adc8c707438e6e603c6e60c983e9ad1749397166c46bf06e427  2048_read74012
0a77da8664220a240437c6baaf2238126a1b3af880f64a057fecdaf4638f2f3f  2048_jump77776
b67c98ff5040fc6348cb4ea119dfdc9298dca3977d43ae741b2571bdc6e6a859  2048_jump74012
2d687ef8553cc246083216beaea6f87b360dcf357153dec0f4ab1775f92850e1  2048_ctrl2006
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_noop (restore)
```

Baseline reproduces the documented `a98e81090d4b2545…` exactly.

## 7. FACT vs inference

**FACT (observed in this experiment):**
- The 15-bit encoding and `utc` one-instruction arming are implemented as in §1;
  `M20 = 70000` / `M20 = 74000` were observed in the SIMH trace.
- LONG `uj 77776` / `uj 74012` set `PC` to those exact addresses (M33 = 77776 /
  74012); no truncation to 0o776 / 0o12 occurred.
- Both the operand read and the instruction fetch at 0o77776 and 0o74012
  terminate in SIMH paging-protection traps (`Число в чужом листе` /
  `Команда в чужом листе`); no data was read, no instruction executed there.
- The C-oracle CORE dump shows 0o77776 = 0; its MTR shows the read resolving to
  77776 and AU becoming 0.
- A modifier read of an accessible address (0o2006) works in SIMH.
- All jobs printed the baseline `21 1.00 3.00` and ended with `КОНЕЦ ЗАДАЧИ`.

**INFERENCE / not proven here:**
- That the protection bits belong to the job's page table and would require a
  privileged PSW/MMU change to clear. I did not attempt to disable protection;
  that would be a separate, privileged experiment.
- That FT*002's real entry address is unknown to the contour: 0o77776 is a
  transfer cell filled by FTDISP, which this deck never runs. I did not locate
  FT*002's actual code address.
- The per-module ambiguity of LINK 0o74012 (`docs/06:178-184`,
  `docs/13:85-90`) remains unresolved; the address is protected regardless.

**Not claimed:** no packed-decimal bytes were produced by FT*002; no
float→GOST conversion was demonstrated; the overall on-machine-intrinsics goal
remains blocked. C dispak results are oracle only.

DONE
