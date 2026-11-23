# VARIANT B harness preparation - plumbing report

> СТАТУС: инфраструктура готова. 6 шаблонов деков с **настоящим Fortran**
> (колонки 7..72, без `777005`), `setup_b.py` (копии образов, stock `-n prn`),
> `drive_b.py` (изолированный tmux, `ДATA:`, `ДАЙ A0/A1`, `НОМВ`, post‑job‑start,
> JSON‑вердикт). Проба: boot‑маркер, задание дошло до ОС, `КОНЕЦ ЗАДАЧИ`,
> фатальных ошибок нет. Строки `21` на этом этапе не ожидаются — парсер
> ещё не готов. Harness находится в `/tmp/.private/azizz/opencode/b-harness/`.

**Result: PASS (harness plumbing).** No product gate was run or claimed.

## What was built

- `decks/deck_b_{x1234,x5678,expr,sqrt,print,two}.b6` - six deck templates with
  real Fortran source in columns 7..72, `FRX5XX` / `*TRANS:FRX5*,,412350`
  preserved, and **no `777005` IR cards**. Verified by script.
- `setup_b.py` - ini builder: copies all attached images into
  `b-harness/images/` (28 images, 307 MB), keeps stock `attach -n prn0/prn1`
  and redirects only their paths to `runs/`, comments out `vu0` and the
  oversized console log, rewrites every other attach/load to a workspace copy.
  A missing stock image (`mg57` -> `ML/204`) is commented out instead of
  attached from a dead path. An uncommented-path grep confirmed there are no
  live SIMH paths left in the generated ini.
- `drive_b.py` - single-deck driver with CLI `--case --deck --image [--timeout
  --session --trace --skip-setup]`; checks emulator SHA, uses an isolated tmux
  socket, `capture-pane`/`send-keys` only, `ДATA:` boot marker, `ДАЙ А0` /
  `ДАЙ А1` / `НОМВ` before deck, post-deck `НОМВ` only after confirmed
  job-start, writes console/prn0/prn1/ACPU captures plus a JSON/text verdict.
- `PROBE.md` - usage guide and PASS criteria.

## Probe execution

```
python3 setup_b.py PROBE /home/azizz/Yandex.Disk/simh/BESM6/MD/2048
python3 drive_b.py --case PROBE --deck decks/deck_b_x1234.b6 \
    --image /home/azizz/Yandex.Disk/simh/BESM6/MD/2048 --skip-setup --timeout 180
```

Observed, from `runs/console_PROBE.txt` and `runs/localprn_PROBE.txt`:

- emulator SHA `9ef71b260e8a780d` (matches `9ef71b26...`)
- `ДATA:23.11.26 BPEMЯ:22.37.00` boot marker in captured pane
- `ДАЙ А0` -> `ECTЬ`, `ДАЙ А1` -> `ECTЬ`, `НОМВ` before deck
- `sim> at vu0 .../decks/deck_b_x1234.b6`, `d 6 1`, `d 5 10`, `set cpu req`, `go`
- `B075-1 410300000000` and `КЗ(075) 410300000000 22.37 M=021` job lines;
  post-deck `НОМВ` sent only after those lines
- printer capture shows the deck header `БОБ:2048 :30(41)-0004,2048 :41(41)` and
  `410300000000 ЗС5` (from the deck's `ДИС` / `ШИФР` lines) and
  `КОНЕЦ ЗАДАЧИ`
- no fatal SIMH/tmux error; exit code 0

`runs/verdict_PROBE.json`:

```
plumbing: PASS
product_gate: FAIL        (expected at this stage: no 21 ... line)
boot_marker: true
sim_prompt_reached: true
deck_attached_and_go: true
job_start_line: true
post_deck_nomv: true
completion_marker: true
result_21_line: false
absence_marker: false
fatal_error: false
```

The deck reached the OS and the job terminated normally. The Fortran text was
not compiled (printer shows `МОNIТОR* SТОР**` / `ИСПОРЧЕНА ПОДПРОГРАММА`),
which is fine for this stage: no machine-code Fortran compiler is under test.
The expected later product PASS signature (`21 <number>` plus `КОНЕЦ ЗАДАЧИ`)
is documented in `PROBE.md`.

## Unverified / out of scope

The harness was not run against a disk containing new machine code, and no
product gate, C patch, repository write, live-disk write, or tmux-0 use was
performed.
