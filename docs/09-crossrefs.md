# 09 — Глобальный свод перекрёстных ссылок компилятора ФОРЭКС

> **Автоматически сгенерировано** `tools/xref_all.py`. Не редактировать вручную —
> перегенерируйте командой из раздела «Воспроизводимость».

## 1. Метод и источники

Инструмент сканирует все MAD-источники и извлекает объявления символов,
все применения, переходы/вызовы и внешние абсолютные адреса. Операнды,
вынесенные в `,EQU,`, разрешаются по цепочке при подсчёте адресов.

- MAD-файлов: **7**; строк: **9696**.
- Файлов `*.labels.md`: **3**: `include/FOREX.labels.md`, `include/LO_GEN.labels.md`, `include/LO_SYN.labels.md`
- Различных символов с определением: **3957**.
- Команд управления/перехода: **1347**.
- Внешних абсолютных адресов (переходы ≥ `0o020000`): **384**.
- Именованных констант `EQU`: **1489**.
- Файлов `include/*.xref.md` (новые рантайм-своды): **2**: `include/RUNTIME_DECODER.xref.md`, `include/RUNTIME_DISASM.xref.md`

Входные файлы:

- `include/FOREX.labels.md`
- `include/FOREX_ROOT.mad`
- `include/LO_GEN.labels.md`
- `include/LO_SYN.labels.md`
- `include/RUNTIME_DECODER.xref.md`
- `include/RUNTIME_DISASM.xref.md`
- `src/FOREX_CORE.mad`
- `src/FOREX_DECODER_DISASM.mad`
- `src/FOREX_RUNTIME.mad`
- `src/FOREX_RUNTIME_DISASM.mad`
- `src/LO_GEN.mad`
- `src/LO_SYN.mad`
- `include/*.xref.md`, `include/catalog.md`, `docs/03-symbols.md`, `docs/06-address-map.md` (для раздела 5)
- `include/RUNTIME_*.xref.md` — подробные xref-своды по дизассемблированному рантайму

## 2. Глобальная таблица символов

### 2.1 Метки, точки входа и внешние имена

«Определение» — файл:строка объявления; «Применения» — все операнды,
где символ встречается (полный список — в `logs/xref_all.txt`).

| Символ | Тип | Определение | Значение / примечание | Применения (всего) |
|---|---|---|---|---:|
| `MV0040` | EQU/LABEL(md) | `src/LO_SYN.mad:83`, `include/LO_SYN.labels.md:424` | 40B | 85 |
| `JT1NIW` | EQU/LABEL(md) | `src/LO_GEN.mad:489`, `include/LO_GEN.labels.md:1541` | 77144B | 69 |
| `AC0001` | EQU/LABEL(md) | `src/LO_GEN.mad:46`, `include/LO_GEN.labels.md:1096` | 1B | 65 |
| `JT18CK` | EQU/LABEL(md) | `src/LO_GEN.mad:326`, `include/LO_GEN.labels.md:1378` | 57476B | 45 |
| `AC0024` | EQU/LABEL(md) | `src/LO_GEN.mad:110`, `include/LO_GEN.labels.md:1160` | 24B | 40 |
| `FLCON` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:301`, `include/FOREX.labels.md:57`, `include/FOREX.labels.md:483` | — | 40 |
| `SC0400` | EQU/LABEL(md) | `src/LO_SYN.mad:591`, `include/LO_SYN.labels.md:450` | 400B | 38 |
| `SC0500` | EQU/LABEL(md) | `src/LO_SYN.mad:593`, `include/LO_SYN.labels.md:452` | 500B | 36 |
| `ME1040` | EQU/LABEL(md) | `src/LO_SYN.mad:78`, `include/LO_SYN.labels.md:603` | 1040B | 30 |
| `NMLN5D` | EQU/LABEL(md) | `src/LO_GEN.mad:243`, `include/LO_GEN.labels.md:1297` | 0000000000020005 | 29 |
| `AC0005` | EQU/LABEL(md) | `src/LO_GEN.mad:168`, `include/LO_GEN.labels.md:1218` | 5B | 27 |
| `AC0013` | EQU/LABEL(md) | `src/LO_GEN.mad:65`, `include/LO_GEN.labels.md:1115` | 13B | 27 |
| `SC0300` | EQU/LABEL(md) | `src/LO_SYN.mad:598`, `include/LO_SYN.labels.md:453` | 300B | 27 |
| `RG5501` | EQU/LABEL(md) | `src/LO_SYN.mad:77`, `include/LO_SYN.labels.md:500` | 5501B | 26 |
| `EX7555` | EQU/LABEL(md) | `src/LO_SYN.mad:76`, `include/LO_SYN.labels.md:60` | 75551B | 24 |
| `ME7404` | EQU/LABEL(md) | `src/LO_SYN.mad:186`, `include/LO_SYN.labels.md:647` | 74040B | 24 |
| `EX4244` | EQU/LABEL(md) | `src/LO_SYN.mad:127`, `include/LO_SYN.labels.md:259` | 42440B | 20 |
| `ME1171` | EQU/LABEL(md) | `src/LO_SYN.mad:185`, `include/LO_SYN.labels.md:646` | 1171B | 20 |
| `ONEW` | EQU/LABEL(md) | `src/FOREX_CORE.mad:130`, `src/FOREX_RUNTIME.mad:71`, `include/FOREX_ROOT.mad:36`, `include/FOREX.labels.md:201`, `include/FOREX.labels.md:263`, `include/FOREX.labels.md:324` … (+1) | 1 | 20 |
| `EX2151` | EQU/LABEL(md) | `src/LO_SYN.mad:102`, `include/LO_SYN.labels.md:67` | 2151B | 19 |
| `EX2440` | EQU/LABEL(md) | `src/LO_SYN.mad:298`, `include/LO_SYN.labels.md:110` | 42440B | 19 |
| `ME2101` | EQU/LABEL(md) | `src/LO_SYN.mad:182`, `include/LO_SYN.labels.md:644` | 2101B | 19 |
| `ME2520` | EQU/LABEL(md) | `src/LO_SYN.mad:121`, `include/LO_SYN.labels.md:614` | 2520B | 19 |
| `NG0004` | EQU/LABEL(md) | `src/LO_GEN.mad:270`, `include/LO_GEN.labels.md:1324` | -4 | 19 |
| `EX4254` | EQU/LABEL(md) | `src/LO_SYN.mad:100`, `include/LO_SYN.labels.md:65` | 42544B | 18 |
| `EX7013` | EQU/LABEL(md) | `src/LO_SYN.mad:101`, `include/LO_SYN.labels.md:66` | 70131B | 18 |
| `AC0026` | EQU/LABEL(md) | `src/LO_GEN.mad:112`, `include/LO_GEN.labels.md:1162` | 26B | 17 |
| `AC0141` | EQU/LABEL(md) | `src/LO_GEN.mad:88`, `include/LO_GEN.labels.md:1138` | 141B | 17 |
| `AP5210` | EQU/LABEL(md) | `src/LO_SYN.mad:108`, `include/LO_SYN.labels.md:360` | 52103B | 17 |
| `EX5210` | EQU/LABEL(md) | `src/LO_SYN.mad:107`, `include/LO_SYN.labels.md:69` | 52103B | 17 |
| `ME0040` | EQU/LABEL(md) | `src/LO_SYN.mad:148`, `include/LO_SYN.labels.md:626` | 40B | 17 |
| `ME7755` | EQU/LABEL(md) | `src/LO_SYN.mad:183`, `include/LO_SYN.labels.md:645` | 77554B | 17 |
| `MV0J42` | EQU/LABEL(md) | `src/LO_GEN.mad:250`, `include/LO_GEN.labels.md:1304` | 24770 | 17 |
| `NG0007` | EQU/LABEL(md) | `src/LO_GEN.mad:273`, `include/LO_GEN.labels.md:1327` | -7 | 17 |
| `ME7104` | EQU/LABEL(md) | `src/LO_SYN.mad:109`, `include/LO_SYN.labels.md:611` | 71040B | 16 |
| `SC0700` | EQU/LABEL(md) | `src/LO_SYN.mad:613`, `include/LO_SYN.labels.md:458` | 700B | 15 |
| `AC0006` | EQU/LABEL(md) | `src/LO_GEN.mad:213`, `include/LO_GEN.labels.md:1263` | 6B | 14 |
| `AC0051` | EQU/LABEL(md) | `src/LO_GEN.mad:172`, `include/LO_GEN.labels.md:1222` | 51B | 14 |
| `AC0007` | EQU/LABEL(md) | `src/LO_GEN.mad:225`, `include/LO_GEN.labels.md:1275` | 7B | 13 |
| `AC0014` | EQU/LABEL(md) | `src/LO_GEN.mad:86`, `include/LO_GEN.labels.md:1136` | 14B | 13 |
| `AC0030` | EQU/LABEL(md) | `src/LO_GEN.mad:115`, `include/LO_GEN.labels.md:1165` | 30B | 13 |
| `EX4044` | EQU/LABEL(md) | `src/LO_SYN.mad:85`, `include/LO_SYN.labels.md:249` | 40440B | 13 |
| `ME4503` | EQU/LABEL(md) | `src/LO_SYN.mad:216`, `include/LO_SYN.labels.md:662` | 4503B | 13 |
| `AC0134` | EQU/LABEL(md) | `src/LO_GEN.mad:75`, `include/LO_GEN.labels.md:1125` | 134B | 12 |
| `EX4251` | EQU/LABEL(md) | `src/LO_SYN.mad:274`, `include/LO_SYN.labels.md:280` | 42510B | 12 |
| `JT188D` | EQU/LABEL(md) | `src/LO_GEN.mad:325`, `include/LO_GEN.labels.md:1377` | 57325B | 12 |
| `ME1551` | EQU/LABEL(md) | `src/LO_SYN.mad:180`, `include/LO_SYN.labels.md:643` | 1551B | 12 |
| `OCTBAS` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:433`, `include/FOREX.labels.md:68`, `include/FOREX.labels.md:556` | — | 12 |
| `RETLR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:137`, `src/FOREX_RUNTIME.mad:74`, `include/FOREX_ROOT.mad:47`, `include/FOREX.labels.md:208`, `include/FOREX.labels.md:266`, `include/FOREX.labels.md:335` … (+2) | 13 | 12 |
| `ZERO` | EQU/TEXT | `src/FOREX_RUNTIME.mad:478`, `src/FOREX_RUNTIME.mad:516`, `src/FOREX_RUNTIME_DISASM.mad:63` | TL0000 | 12 |
| `AC0032` | EQU/LABEL(md) | `src/LO_GEN.mad:120`, `include/LO_GEN.labels.md:1170` | 32B | 11 |
| `AC0136` | EQU/LABEL(md) | `src/LO_GEN.mad:81`, `include/LO_GEN.labels.md:1131` | 136B | 11 |
| `AP2004` | EQU/LABEL(md) | `src/LO_SYN.mad:82`, `include/LO_SYN.labels.md:357` | 20040B | 11 |
| `EX4751` | EQU/LABEL(md) | `src/LO_SYN.mad:131`, `include/LO_SYN.labels.md:260` | 47510B | 11 |
| `RG0103` | EQU/LABEL(md) | `src/LO_SYN.mad:195`, `include/LO_SYN.labels.md:511` | 103B | 11 |
| `DW0001` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:30`, `include/FOREX.labels.md:222`, `include/FOREX.labels.md:443` | 00000000 00000000 | 10 |
| `JT1BCS` | EQU/LABEL(md) | `src/LO_GEN.mad:332`, `include/LO_GEN.labels.md:1384` | 61372B | 10 |
| `JT1NII` | EQU/LABEL(md) | `src/LO_GEN.mad:488`, `include/LO_GEN.labels.md:1540` | 77130B | 10 |
| `ME1513` | EQU/LABEL(md) | `src/LO_SYN.mad:114`, `include/LO_SYN.labels.md:612` | 1513B | 10 |
| `ME4105` | EQU/LABEL(md) | `src/LO_SYN.mad:240`, `include/LO_SYN.labels.md:674` | 4105B | 10 |
| `AC0046` | EQU/LABEL(md) | `src/LO_GEN.mad:163`, `include/LO_GEN.labels.md:1213` | 46B | 9 |
| `AC0132` | EQU/LABEL(md) | `src/LO_GEN.mad:66`, `include/LO_GEN.labels.md:1116` | 132B | 9 |
| `BS14R` | EQU/LABEL(md) | `src/FOREX_CORE.mad:37`, `src/FOREX_RUNTIME.mad:28`, `include/FOREX_ROOT.mad:24`, `include/FOREX.labels.md:108`, `include/FOREX.labels.md:220`, `include/FOREX.labels.md:312` … (+2) | 14 | 9 |
| `EX2040` | EQU/LABEL(md) | `src/LO_SYN.mad:132`, `include/LO_SYN.labels.md:76` | 2040B | 9 |
| `EX6444` | EQU/LABEL(md) | `src/LO_SYN.mad:97`, `include/LO_SYN.labels.md:254` | 64440B | 9 |
| `JT1CVN` | EQU/LABEL(md) | `src/LO_GEN.mad:340`, `include/LO_GEN.labels.md:1392` | 63347B | 9 |
| `ME0105` | EQU/LABEL(md) | `src/LO_SYN.mad:270`, `include/LO_SYN.labels.md:687` | 105B | 9 |
| `ME0117` | EQU/LABEL(md) | `src/LO_SYN.mad:212`, `include/LO_SYN.labels.md:660` | 117B | 9 |
| `ME0151` | EQU/LABEL(md) | `src/LO_SYN.mad:156`, `include/LO_SYN.labels.md:630` | 151B | 9 |
| `ME7010` | EQU/LABEL(md) | `src/LO_SYN.mad:200`, `include/LO_SYN.labels.md:652` | 70105B | 9 |
| `ME7503` | EQU/LABEL(md) | `src/LO_SYN.mad:203`, `include/LO_SYN.labels.md:654` | 7503B | 9 |
| `RS0012` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:256`, `src/LO_GEN.mad:584`, `src/LO_GEN.mad:587`, `src/LO_GEN.mad:1108`, `src/LO_GEN.mad:2113`, `src/LO_GEN.mad:2116` … (+13) | 12 | 9 |
| `SC0401` | EQU/LABEL(md) | `src/LO_SYN.mad:715`, `include/LO_SYN.labels.md:475` | 401B | 9 |
| `SC0701` | EQU/LABEL(md) | `src/LO_SYN.mad:682`, `include/LO_SYN.labels.md:468` | 701B | 9 |
| `*DUMON` | COMMON | `src/FOREX_CORE.mad:154`, `src/LO_SYN.mad:22`, `include/FOREX_ROOT.mad:67` | DUMMYL | 8 |
| `AC0011` | EQU/LABEL(md) | `src/LO_GEN.mad:60`, `include/LO_GEN.labels.md:1110` | 11B | 8 |
| `EX4252` | EQU/LABEL(md) | `src/LO_SYN.mad:84`, `include/LO_SYN.labels.md:248` | 42524B | 8 |
| `EX4520` | EQU/LABEL(md) | `src/LO_SYN.mad:376`, `include/LO_SYN.labels.md:134` | 4520B | 8 |
| `GATAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:114`, `include/FOREX.labels.md:185`, `include/FOREX.labels.md:516` | 7417B | 8 |
| `JT0WMA` | EQU/LABEL(md) | `src/LO_GEN.mad:302`, `include/LO_GEN.labels.md:1354` | 42274B | 8 |
| `JT0WWD` | EQU/LABEL(md) | `src/LO_GEN.mad:308`, `include/LO_GEN.labels.md:1360` | 42637B | 8 |
| `ME4502` | EQU/LABEL(md) | `src/LO_SYN.mad:168`, `include/LO_SYN.labels.md:637` | 4502B | 8 |
| `ME7044` | EQU/LABEL(md) | `src/LO_SYN.mad:237`, `include/LO_SYN.labels.md:672` | 70440B | 8 |
| `RG4056` | EQU/LABEL(md) | `src/LO_SYN.mad:229`, `include/LO_SYN.labels.md:516` | 40560B | 8 |
| `SC0501` | EQU/LABEL(md) | `src/LO_SYN.mad:687`, `include/LO_SYN.labels.md:469` | 501B | 8 |
| `SC0600` | EQU/LABEL(md) | `src/LO_SYN.mad:606`, `include/LO_SYN.labels.md:456` | 600B | 8 |
| `AC0035` | EQU/LABEL(md) | `src/LO_GEN.mad:123`, `include/LO_GEN.labels.md:1173` | 35B | 7 |
| `AC17OS` | EQU/LABEL(md) | `src/LO_GEN.mad:206`, `include/LO_GEN.labels.md:1256` | 56620B | 7 |
| `AP7704` | EQU/LABEL(md) | `src/LO_SYN.mad:348`, `include/LO_SYN.labels.md:382` | 77040B | 7 |
| `CW001` | LABEL(md) | `include/FOREX.labels.md:165`, `include/FOREX.labels.md:437` | — | 7 |
| `EX0010` | EQU/LABEL(md) | `src/LO_SYN.mad:116`, `include/LO_SYN.labels.md:257` | 20040B | 7 |
| `EX2010` | EQU/LABEL(md) | `src/LO_SYN.mad:94`, `include/LO_SYN.labels.md:252` | 20103B | 7 |
| `EX3661` | EQU/LABEL(md) | `src/LO_SYN.mad:169`, `include/LO_SYN.labels.md:84` | 61113B | 7 |
| `JT0WLS` | EQU/LABEL(md) | `src/LO_GEN.mad:301`, `include/LO_GEN.labels.md:1353` | 42256B | 7 |
| `JT1N2U` | EQU/LABEL(md) | `src/LO_GEN.mad:452`, `include/LO_GEN.labels.md:1504` | 76566B | 7 |
| `ME0440` | EQU/LABEL(md) | `src/LO_SYN.mad:154`, `include/LO_SYN.labels.md:629` | 440B | 7 |
| `ME2515` | EQU/LABEL(md) | `src/LO_SYN.mad:271`, `include/LO_SYN.labels.md:688` | 2515B | 7 |
| `ME3040` | EQU/LABEL(md) | `src/LO_SYN.mad:377`, `include/LO_SYN.labels.md:721` | 3040B | 7 |
| `ME4510` | EQU/LABEL(md) | `src/LO_SYN.mad:343`, `include/LO_SYN.labels.md:709` | 4510B | 7 |
| `ME7204` | EQU/LABEL(md) | `src/LO_SYN.mad:252`, `include/LO_SYN.labels.md:681` | 72040B | 7 |
| `ME7255` | EQU/LABEL(md) | `src/LO_SYN.mad:189`, `include/LO_SYN.labels.md:649` | 72554B | 7 |
| `ME7644` | EQU/LABEL(md) | `src/LO_SYN.mad:351`, `include/LO_SYN.labels.md:712` | 76440B | 7 |
| `MV7004` | EQU/LABEL(md) | `src/LO_SYN.mad:349`, `include/LO_SYN.labels.md:427` | 70040B | 7 |
| `NG0006` | EQU/LABEL(md) | `src/LO_GEN.mad:272`, `include/LO_GEN.labels.md:1326` | -6 | 7 |
| `RG4051` | EQU/LABEL(md) | `src/LO_SYN.mad:204`, `include/LO_SYN.labels.md:513` | 40513B | 7 |
| `SC0601` | EQU/LABEL(md) | `src/LO_SYN.mad:679`, `include/LO_SYN.labels.md:467` | 601B | 7 |
| `*00072` | LABEL | `src/FOREX_RUNTIME.mad:310` | — | 6 |
| `*00077` | LABEL | `src/FOREX_RUNTIME.mad:315` | — | 6 |
| `AC0002` | EQU/LABEL(md) | `src/LO_GEN.mad:101`, `include/LO_GEN.labels.md:1151` | 2B | 6 |
| `AC0027` | EQU/LABEL(md) | `src/LO_GEN.mad:113`, `include/LO_GEN.labels.md:1163` | 27B | 6 |
| `AC0142` | EQU/LABEL(md) | `src/LO_GEN.mad:89`, `include/LO_GEN.labels.md:1139` | 142B | 6 |
| `AC17OP` | EQU/LABEL(md) | `src/LO_GEN.mad:205`, `include/LO_GEN.labels.md:1255` | 56617B | 6 |
| `C072` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:380` | — | 6 |
| `EX0151` | EQU/LABEL(md) | `src/LO_SYN.mad:381`, `include/LO_SYN.labels.md:135` | 151B | 6 |
| `EX2120` | EQU/LABEL(md) | `src/LO_SYN.mad:406`, `include/LO_SYN.labels.md:142` | 2120B | 6 |
| `EX4055` | EQU/LABEL(md) | `src/LO_SYN.mad:215`, `include/LO_SYN.labels.md:269` | 40554B | 6 |
| `EX6610` | EQU/LABEL(md) | `src/LO_SYN.mad:233`, `include/LO_SYN.labels.md:272` | 66101B | 6 |
| `JT0WVD` | EQU/LABEL(md) | `src/LO_GEN.mad:306`, `include/LO_GEN.labels.md:1358` | 42601B | 6 |
| `ME0000` | EQU/LABEL(md) | `src/LO_SYN.mad:149`, `include/LO_SYN.labels.md:627` | 70117B | 6 |
| `ME0001` | EQU/LABEL(md) | `src/LO_SYN.mad:387`, `include/LO_SYN.labels.md:724` | 70110B | 6 |
| `ME0101` | EQU/LABEL(md) | `src/LO_SYN.mad:146`, `include/LO_SYN.labels.md:625` | 101B | 6 |
| `ME2511` | EQU/LABEL(md) | `src/LO_SYN.mad:278`, `include/LO_SYN.labels.md:691` | 2511B | 6 |
| `ME6501` | EQU/LABEL(md) | `src/LO_SYN.mad:158`, `include/LO_SYN.labels.md:632` | 6501B | 6 |
| `ME7456` | EQU/LABEL(md) | `src/LO_SYN.mad:247`, `include/LO_SYN.labels.md:677` | 74560B | 6 |
| `ME7650` | EQU/LABEL(md) | `src/LO_SYN.mad:415`, `include/LO_SYN.labels.md:733` | 76505B | 6 |
| `NG0005` | EQU/LABEL(md) | `src/LO_GEN.mad:271`, `include/LO_GEN.labels.md:1325` | -5 | 6 |
| `RG0105` | EQU/LABEL(md) | `src/LO_SYN.mad:277`, `include/LO_SYN.labels.md:520` | 105B | 6 |
| `RG7411` | EQU/LABEL(md) | `src/LO_SYN.mad:311`, `include/LO_SYN.labels.md:526` | 74117B | 6 |
| `RS0014` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:258`, `src/LO_GEN.mad:575`, `src/LO_GEN.mad:578`, `src/LO_GEN.mad:748`, `src/LO_GEN.mad:763`, `src/LO_GEN.mad:766` … (+295) | 14 | 6 |
| `SC1000` | EQU/LABEL(md) | `src/LO_SYN.mad:620`, `include/LO_SYN.labels.md:459` | 1000B | 6 |
| `AC0010` | EQU/LABEL(md) | `src/LO_GEN.mad:47`, `include/LO_GEN.labels.md:1097` | 10B | 5 |
| `AC0016` | EQU/LABEL(md) | `src/LO_GEN.mad:96`, `include/LO_GEN.labels.md:1146` | 16B | 5 |
| `AC0045` | EQU/LABEL(md) | `src/LO_GEN.mad:162`, `include/LO_GEN.labels.md:1212` | 45B | 5 |
| `AC0143` | EQU/LABEL(md) | `src/LO_GEN.mad:90`, `include/LO_GEN.labels.md:1140` | 143B | 5 |
| `AC17N7` | EQU/LABEL(md) | `src/LO_GEN.mad:186`, `include/LO_GEN.labels.md:1236` | 56563B | 5 |
| `AP4414` | EQU/LABEL(md) | `src/LO_SYN.mad:289`, `include/LO_SYN.labels.md:372` | 44144B | 5 |
| `C077` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:385`, `include/RUNTIME_DISASM.xref.md:87` | — | 5 |
| `ENTTA` | EQU/LABEL(md) | `src/FOREX_CORE.mad:107`, `include/FOREX.labels.md:178`, `include/FOREX.labels.md:474` | 4006B | 5 |
| `EX0005` | EQU/LABEL(md) | `src/LO_SYN.mad:442`, `include/LO_SYN.labels.md:156` | 40440B | 5 |
| `EX0021` | EQU/LABEL(md) | `src/LO_SYN.mad:412`, `include/LO_SYN.labels.md:296` | 20160B | 5 |
| `EX0440` | EQU/LABEL(md) | `src/LO_SYN.mad:202`, `include/LO_SYN.labels.md:90` | 440B | 5 |
| `EX2062` | EQU/LABEL(md) | `src/LO_SYN.mad:294`, `include/LO_SYN.labels.md:108` | 62113B | 5 |
| `EX3642` | EQU/LABEL(md) | `src/LO_SYN.mad:312`, `include/LO_SYN.labels.md:114` | 42440B | 5 |
| `EX4144` | EQU/LABEL(md) | `src/LO_SYN.mad:291`, `include/LO_SYN.labels.md:281` | 41440B | 5 |
| `EX4513` | EQU/LABEL(md) | `src/LO_SYN.mad:445`, `include/LO_SYN.labels.md:159` | 4513B | 5 |
| `EX4524` | EQU/LABEL(md) | `src/LO_SYN.mad:429`, `include/LO_SYN.labels.md:150` | 4524B | 5 |
| `EX4755` | EQU/LABEL(md) | `src/LO_SYN.mad:347`, `include/LO_SYN.labels.md:289` | 47554B | 5 |
| `EX5505` | EQU/LABEL(md) | `src/LO_SYN.mad:382`, `include/LO_SYN.labels.md:136` | 5505B | 5 |
| `EX6616` | EQU/LABEL(md) | `src/LO_SYN.mad:441`, `include/LO_SYN.labels.md:155` | 66166B | 5 |
| `EX6617` | EQU/LABEL(md) | `src/LO_SYN.mad:126`, `include/LO_SYN.labels.md:75` | 66170B | 5 |
| `JT0WHV` | EQU/LABEL(md) | `src/LO_GEN.mad:295`, `include/LO_GEN.labels.md:1347` | 42115B | 5 |
| `JT0WLG` | EQU/LABEL(md) | `src/LO_GEN.mad:300`, `include/LO_GEN.labels.md:1352` | 42244B | 5 |
| `JT0WW2` | EQU/LABEL(md) | `src/LO_GEN.mad:307`, `include/LO_GEN.labels.md:1359` | 42626B | 5 |
| `JT0Z1P` | EQU/LABEL(md) | `src/LO_GEN.mad:317`, `include/LO_GEN.labels.md:1369` | 45421B | 5 |
| `JT1N11` | EQU/LABEL(md) | `src/LO_GEN.mad:442`, `include/LO_GEN.labels.md:1494` | 76501B | 5 |
| `ME0520` | EQU/LABEL(md) | `src/LO_SYN.mad:219`, `include/LO_SYN.labels.md:663` | 520B | 5 |
| `ME0572` | EQU/LABEL(md) | `src/LO_SYN.mad:188`, `include/LO_SYN.labels.md:648` | 572B | 5 |
| `ME2117` | EQU/LABEL(md) | `src/LO_SYN.mad:241`, `include/LO_SYN.labels.md:675` | 2117B | 5 |
| `ME5440` | EQU/LABEL(md) | `src/LO_SYN.mad:163`, `include/LO_SYN.labels.md:635` | 5440B | 5 |
| `ME7013` | EQU/LABEL(md) | `src/LO_SYN.mad:411`, `include/LO_SYN.labels.md:732` | 70131B | 5 |
| `ME7211` | EQU/LABEL(md) | `src/LO_SYN.mad:81`, `include/LO_SYN.labels.md:606` | 72113B | 5 |
| `ME7244` | EQU/LABEL(md) | `src/LO_SYN.mad:159`, `include/LO_SYN.labels.md:633` | 72440B | 5 |
| `ME7502` | EQU/LABEL(md) | `src/LO_SYN.mad:205`, `include/LO_SYN.labels.md:655` | 7502B | 5 |
| `ME7560` | EQU/LABEL(md) | `src/LO_SYN.mad:207`, `include/LO_SYN.labels.md:657` | 7560B | 5 |
| `RE0010` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:254`, `src/LO_GEN.mad:635`, `src/LO_GEN.mad:661`, `src/LO_GEN.mad:670`, `src/LO_GEN.mad:709`, `src/LO_GEN.mad:3105` … (+2) | 10 | 5 |
| `RG7410` | EQU/LABEL(md) | `src/LO_SYN.mad:184`, `include/LO_SYN.labels.md:510` | 74101B | 5 |
| `RG7417` | EQU/LABEL(md) | `src/LO_SYN.mad:275`, `include/LO_SYN.labels.md:519` | 74171B | 5 |
| `SC0301` | EQU/LABEL(md) | `src/LO_SYN.mad:702`, `include/LO_SYN.labels.md:472` | 301B | 5 |
| `*00063` | LABEL | `src/FOREX_RUNTIME.mad:303` | — | 4 |
| `*00064` | LABEL | `src/FOREX_RUNTIME.mad:304` | — | 4 |
| `*00071` | LABEL | `src/FOREX_RUNTIME.mad:309` | — | 4 |
| `*00074` | LABEL | `src/FOREX_RUNTIME.mad:312` | — | 4 |
| `AC0021` | EQU/LABEL(md) | `src/LO_GEN.mad:103`, `include/LO_GEN.labels.md:1153` | 21B | 4 |
| `AC0031` | EQU/LABEL(md) | `src/LO_GEN.mad:119`, `include/LO_GEN.labels.md:1169` | 31B | 4 |
| `AC0137` | EQU/LABEL(md) | `src/LO_GEN.mad:84`, `include/LO_GEN.labels.md:1134` | 137B | 4 |
| `AC0140` | EQU/LABEL(md) | `src/LO_GEN.mad:87`, `include/LO_GEN.labels.md:1137` | 140B | 4 |
| `AC17N5` | EQU/LABEL(md) | `src/LO_GEN.mad:185`, `include/LO_GEN.labels.md:1235` | 56561B | 4 |
| `AC17N8` | EQU/LABEL(md) | `src/LO_GEN.mad:187`, `include/LO_GEN.labels.md:1237` | 56564B | 4 |
| `AC17NJ` | EQU/LABEL(md) | `src/LO_GEN.mad:194`, `include/LO_GEN.labels.md:1244` | 56575B | 4 |
| `AC17ON` | EQU/LABEL(md) | `src/LO_GEN.mad:203`, `include/LO_GEN.labels.md:1253` | 56615B | 4 |
| `AP4410` | EQU/LABEL(md) | `src/LO_SYN.mad:410`, `include/LO_SYN.labels.md:389` | 44103B | 4 |
| `AP4555` | EQU/LABEL(md) | `src/LO_SYN.mad:417`, `include/LO_SYN.labels.md:390` | 45554B | 4 |
| `AP4656` | EQU/LABEL(md) | `src/LO_SYN.mad:211`, `include/LO_SYN.labels.md:366` | 46561B | 4 |
| `AP6210` | EQU/LABEL(md) | `src/LO_SYN.mad:98`, `include/LO_SYN.labels.md:359` | 62105B | 4 |
| `AP6615` | EQU/LABEL(md) | `src/LO_SYN.mad:192`, `include/LO_SYN.labels.md:365` | 66151B | 4 |
| `C063` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:373` | — | 4 |
| `C064` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:374` | — | 4 |
| `C071` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:379` | — | 4 |
| `C074` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:382` | — | 4 |
| `DATAPR` | COMMON/LABEL(md)/NAME/SUBP/XREF(md) | `src/FOREX_CORE.mad:161`, `src/FOREX_RUNTIME.mad:329`, `src/FOREX_RUNTIME.mad:331`, `src/LO_GEN.mad:29`, `src/LO_SYN.mad:28`, `include/FOREX_ROOT.mad:69` … (+12) | — | 4 |
| `DEC_7` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:43`, `include/FOREX.labels.md:235` | 7 | 4 |
| `EX0000` | EQU/LABEL(md) | `src/LO_SYN.mad:120`, `include/LO_SYN.labels.md:258` | 20117B | 4 |
| `EX2004` | EQU/LABEL(md) | `src/LO_SYN.mad:110`, `include/LO_SYN.labels.md:70` | 20040B | 4 |
| `EX2015` | EQU/LABEL(md) | `src/LO_SYN.mad:234`, `include/LO_SYN.labels.md:273` | 20151B | 4 |
| `EX2554` | EQU/LABEL(md) | `src/LO_SYN.mad:153`, `include/LO_SYN.labels.md:79` | 2554B | 4 |
| `EX4152` | EQU/LABEL(md) | `src/LO_SYN.mad:135`, `include/LO_SYN.labels.md:77` | 41524B | 4 |
| `EX4505` | EQU/LABEL(md) | `src/LO_SYN.mad:329`, `include/LO_SYN.labels.md:120` | 64505B | 4 |
| `EX5011` | EQU/LABEL(md) | `src/LO_SYN.mad:165`, `include/LO_SYN.labels.md:82` | 50115B | 4 |
| `EX5204` | EQU/LABEL(md) | `src/LO_SYN.mad:99`, `include/LO_SYN.labels.md:64` | 52040B | 4 |
| `EX6351` | EQU/LABEL(md) | `src/LO_SYN.mad:454`, `include/LO_SYN.labels.md:162` | 63517B | 4 |
| `EX7012` | EQU/LABEL(md) | `src/LO_SYN.mad:272`, `include/LO_SYN.labels.md:103` | 70120B | 4 |
| `EX7044` | EQU/LABEL(md) | `src/LO_SYN.mad:235`, `include/LO_SYN.labels.md:274` | 70440B | 4 |
| `JT0W2U` | EQU/LABEL(md) | `src/LO_GEN.mad:287`, `include/LO_GEN.labels.md:1339` | 41574B | 4 |
| `JT1M7P` | EQU/LABEL(md) | `src/LO_GEN.mad:360`, `include/LO_GEN.labels.md:1412` | 75445B | 4 |
| `JT1MQL` | EQU/LABEL(md) | `src/LO_GEN.mad:395`, `include/LO_GEN.labels.md:1447` | 76125B | 4 |
| `JT1MWX` | EQU/LABEL(md) | `src/LO_GEN.mad:414`, `include/LO_GEN.labels.md:1466` | 76353B | 4 |
| `ME2151` | EQU/LABEL(md) | `src/LO_SYN.mad:145`, `include/LO_SYN.labels.md:624` | 2151B | 4 |
| `ME3117` | EQU/LABEL(md) | `src/LO_SYN.mad:157`, `include/LO_SYN.labels.md:631` | 3117B | 4 |
| `ME5517` | EQU/LABEL(md) | `src/LO_SYN.mad:326`, `include/LO_SYN.labels.md:705` | 5517B | 4 |
| `ME6440` | EQU/LABEL(md) | `src/LO_SYN.mad:220`, `include/LO_SYN.labels.md:664` | 6440B | 4 |
| `ME6505` | EQU/LABEL(md) | `src/LO_SYN.mad:423`, `include/LO_SYN.labels.md:734` | 6505B | 4 |
| `ME7004` | EQU/LABEL(md) | `src/LO_SYN.mad:140`, `include/LO_SYN.labels.md:621` | 70040B | 4 |
| `ME7015` | EQU/LABEL(md) | `src/LO_SYN.mad:96`, `include/LO_SYN.labels.md:609` | 70151B | 4 |
| `ME7210` | EQU/LABEL(md) | `src/LO_SYN.mad:273`, `include/LO_SYN.labels.md:689` | 72105B | 4 |
| `ME7550` | EQU/LABEL(md) | `src/LO_SYN.mad:290`, `include/LO_SYN.labels.md:695` | 75503B | 4 |
| `ME7744` | EQU/LABEL(md) | `src/LO_SYN.mad:428`, `include/LO_SYN.labels.md:737` | 77440B | 4 |
| `ME7752` | EQU/LABEL(md) | `src/LO_SYN.mad:206`, `include/LO_SYN.labels.md:656` | 77520B | 4 |
| `MODE_6` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:68`, `include/FOREX_ROOT.mad:34`, `include/FOREX.labels.md:260`, `include/FOREX.labels.md:322` | 6 | 4 |
| `MV0102` | EQU/LABEL(md) | `src/LO_SYN.mad:365`, `include/LO_SYN.labels.md:429` | 70102B | 4 |
| `MV0144` | EQU/LABEL(md) | `src/LO_SYN.mad:440`, `include/LO_SYN.labels.md:434` | 70144B | 4 |
| `NG0003` | EQU/LABEL(md) | `src/LO_GEN.mad:269`, `include/LO_GEN.labels.md:1323` | -3 | 4 |
| `OCT` | DATA/LABEL(md) | `src/FOREX_RUNTIME.mad:468`, `include/FOREX.labels.md:357` | — | 4 |
| `PG17AD` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:37`, `include/FOREX.labels.md:325`, `include/FOREX.labels.md:568` | 17B | 4 |
| `RG0040` | EQU/LABEL(md) | `src/LO_SYN.mad:414`, `include/LO_SYN.labels.md:533` | 40B | 4 |
| `RG0440` | EQU/LABEL(md) | `src/LO_SYN.mad:257`, `include/LO_SYN.labels.md:518` | 440B | 4 |
| `RG2524` | EQU/LABEL(md) | `src/LO_SYN.mad:113`, `include/LO_SYN.labels.md:501` | 2524B | 4 |
| `RS0011` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:255`, `src/LO_GEN.mad:862`, `src/LO_GEN.mad:877`, `src/LO_GEN.mad:895`, `include/LO_GEN.labels.md:1309` | 11 | 4 |
| `RZPAG` | EQU/LABEL(md) | `src/FOREX_CORE.mad:135`, `include/FOREX.labels.md:206`, `include/FOREX.labels.md:604` | 70000B | 4 |
| `*00062` | LABEL | `src/FOREX_RUNTIME.mad:302` | — | 3 |
| `*00070` | LABEL | `src/FOREX_RUNTIME.mad:308` | — | 3 |
| `*00100` | LABEL | `src/FOREX_RUNTIME.mad:316` | — | 3 |
| `AC0003` | EQU/LABEL(md) | `src/LO_GEN.mad:114`, `include/LO_GEN.labels.md:1164` | 3B | 3 |
| `AC0012` | EQU/LABEL(md) | `src/LO_GEN.mad:62`, `include/LO_GEN.labels.md:1112` | 12B | 3 |
| `AC0017` | EQU/LABEL(md) | `src/LO_GEN.mad:99`, `include/LO_GEN.labels.md:1149` | 17B | 3 |
| `AC0023` | EQU/LABEL(md) | `src/LO_GEN.mad:109`, `include/LO_GEN.labels.md:1159` | 23B | 3 |
| `AC0044` | EQU/LABEL(md) | `src/LO_GEN.mad:161`, `include/LO_GEN.labels.md:1211` | 44B | 3 |
| `AC0050` | EQU/LABEL(md) | `src/LO_GEN.mad:169`, `include/LO_GEN.labels.md:1219` | 50B | 3 |
| `AC0055` | EQU/LABEL(md) | `src/LO_GEN.mad:182`, `include/LO_GEN.labels.md:1232` | 55B | 3 |
| `AC0062` | EQU/LABEL(md) | `src/LO_GEN.mad:218`, `include/LO_GEN.labels.md:1268` | 62B | 3 |
| `AC0100` | EQU/LABEL(md) | `src/LO_GEN.mad:48`, `include/LO_GEN.labels.md:1098` | 100B | 3 |
| `AC0153` | EQU/LABEL(md) | `src/LO_GEN.mad:94`, `include/LO_GEN.labels.md:1144` | 153B | 3 |
| `AC0WQ5` | EQU/LABEL(md) | `src/LO_GEN.mad:157`, `include/LO_GEN.labels.md:1207` | 42413B | 3 |
| `AC0WTZ` | EQU/LABEL(md) | `src/LO_GEN.mad:158`, `include/LO_GEN.labels.md:1208` | 42551B | 3 |
| `AC17NA` | EQU/LABEL(md) | `src/LO_GEN.mad:189`, `include/LO_GEN.labels.md:1239` | 56566B | 3 |
| `AC17NE` | EQU/LABEL(md) | `src/LO_GEN.mad:190`, `include/LO_GEN.labels.md:1240` | 56570B | 3 |
| `AC17NG` | EQU/LABEL(md) | `src/LO_GEN.mad:192`, `include/LO_GEN.labels.md:1242` | 56572B | 3 |
| `AP4152` | EQU/LABEL(md) | `src/LO_SYN.mad:320`, `include/LO_SYN.labels.md:377` | 41524B | 3 |
| `AP4304` | EQU/LABEL(md) | `src/LO_SYN.mad:437`, `include/LO_SYN.labels.md:391` | 43040B | 3 |
| `AP4351` | EQU/LABEL(md) | `src/LO_SYN.mad:399`, `include/LO_SYN.labels.md:386` | 43516B | 3 |
| `AP4544` | EQU/LABEL(md) | `src/LO_SYN.mad:407`, `include/LO_SYN.labels.md:387` | 45440B | 3 |
| `AP4650` | EQU/LABEL(md) | `src/LO_SYN.mad:317`, `include/LO_SYN.labels.md:376` | 46502B | 3 |
| `AP5010` | EQU/LABEL(md) | `src/LO_SYN.mad:379`, `include/LO_SYN.labels.md:383` | 50101B | 3 |
| `AP5217` | EQU/LABEL(md) | `src/LO_SYN.mad:244`, `include/LO_SYN.labels.md:368` | 52170B | 3 |
| `BAS61` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:371`, `include/RUNTIME_DISASM.xref.md:86` | — | 3 |
| `C062` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:372`, `include/RUNTIME_DISASM.xref.md:87` | — | 3 |
| `C070` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:378` | — | 3 |
| `C100` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:386`, `include/RUNTIME_DISASM.xref.md:87` | — | 3 |
| `DMTIM` | EQU/LABEL(md) | `src/FOREX_CORE.mad:106`, `include/FOREX.labels.md:177`, `include/FOREX.labels.md:473` | 4025B | 3 |
| `EX0011` | EQU/LABEL(md) | `src/LO_SYN.mad:224`, `include/LO_SYN.labels.md:93` | 20040B | 3 |
| `EX0113` | EQU/LABEL(md) | `src/LO_SYN.mad:103`, `include/LO_SYN.labels.md:255` | 20113B | 3 |
| `EX0124` | EQU/LABEL(md) | `src/LO_SYN.mad:313`, `include/LO_SYN.labels.md:282` | 20124B | 3 |
| `EX0561` | EQU/LABEL(md) | `src/LO_SYN.mad:537`, `include/LO_SYN.labels.md:312` | 40561B | 3 |
| `EX2012` | EQU/LABEL(md) | `src/LO_SYN.mad:221`, `include/LO_SYN.labels.md:270` | 20120B | 3 |
| `EX2043` | EQU/LABEL(md) | `src/LO_SYN.mad:416`, `include/LO_SYN.labels.md:144` | 20143B | 3 |
| `EX2502` | EQU/LABEL(md) | `src/LO_SYN.mad:564`, `include/LO_SYN.labels.md:188` | 42502B | 3 |
| `EX3652` | EQU/LABEL(md) | `src/LO_SYN.mad:251`, `include/LO_SYN.labels.md:96` | 52102B | 3 |
| `EX4250` | EQU/LABEL(md) | `src/LO_SYN.mad:111`, `include/LO_SYN.labels.md:71` | 42503B | 3 |
| `EX4404` | EQU/LABEL(md) | `src/LO_SYN.mad:218`, `include/LO_SYN.labels.md:92` | 44040B | 3 |
| `EX4551` | EQU/LABEL(md) | `src/LO_SYN.mad:134`, `include/LO_SYN.labels.md:261` | 45517B | 3 |
| `EX4644` | EQU/LABEL(md) | `src/LO_SYN.mad:308`, `include/LO_SYN.labels.md:113` | 46440B | 3 |
| `EX4750` | EQU/LABEL(md) | `src/LO_SYN.mad:95`, `include/LO_SYN.labels.md:253` | 47502B | 3 |
| `EX4752` | EQU/LABEL(md) | `src/LO_SYN.mad:112`, `include/LO_SYN.labels.md:72` | 47524B | 3 |
| `EX4756` | EQU/LABEL(md) | `src/LO_SYN.mad:173`, `include/LO_SYN.labels.md:265` | 47566B | 3 |
| `EX6504` | EQU/LABEL(md) | `src/LO_SYN.mad:360`, `include/LO_SYN.labels.md:127` | 65040B | 3 |
| `EX6604` | EQU/LABEL(md) | `src/LO_SYN.mad:318`, `include/LO_SYN.labels.md:116` | 66040B | 3 |
| `EX6614` | EQU/LABEL(md) | `src/LO_SYN.mad:93`, `include/LO_SYN.labels.md:251` | 66140B | 3 |
| `ISOWSH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:62`, `include/FOREX.labels.md:254`, `include/FOREX.labels.md:528` | 64 | 3 |
| `JT0WNK` | EQU/LABEL(md) | `src/LO_GEN.mad:303`, `include/LO_GEN.labels.md:1355` | 42320B | 3 |
| `JT0WOO` | EQU/LABEL(md) | `src/LO_GEN.mad:305`, `include/LO_GEN.labels.md:1357` | 42360B | 3 |
| `JT0YGV` | EQU/LABEL(md) | `src/LO_GEN.mad:316`, `include/LO_GEN.labels.md:1368` | 44671B | 3 |
| `JT1AEA` | EQU/LABEL(md) | `src/LO_GEN.mad:329`, `include/LO_GEN.labels.md:1381` | 60130B | 3 |
| `JT1M2O` | EQU/LABEL(md) | `src/LO_GEN.mad:347`, `include/LO_GEN.labels.md:1399` | 75264B | 3 |
| `JT1M3O` | EQU/LABEL(md) | `src/LO_GEN.mad:348`, `include/LO_GEN.labels.md:1400` | 75300B | 3 |
| `JT1MAZ` | EQU/LABEL(md) | `src/LO_GEN.mad:379`, `include/LO_GEN.labels.md:1431` | 75563B | 3 |
| `JT1N2R` | EQU/LABEL(md) | `src/LO_GEN.mad:451`, `include/LO_GEN.labels.md:1503` | 76563B | 3 |
| `JT1NI2` | EQU/LABEL(md) | `src/LO_GEN.mad:479`, `include/LO_GEN.labels.md:1531` | 77114B | 3 |
| `LNK15` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:56`, `include/FOREX.labels.md:344`, `include/FOREX.labels.md:351`, `include/FOREX.labels.md:537` | 15 | 3 |
| `LOADAN` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:165`, `src/LO_GEN.mad:38`, `src/LO_SYN.mad:37`, `include/FOREX.labels.md:7`, `include/FOREX.labels.md:25`, `include/FOREX.labels.md:358` … (+2) | — | 3 |
| `ME0110` | EQU/LABEL(md) | `src/LO_SYN.mad:505`, `include/LO_SYN.labels.md:767` | 110B | 3 |
| `ME0566` | EQU/LABEL(md) | `src/LO_SYN.mad:344`, `include/LO_SYN.labels.md:710` | 566B | 3 |
| `ME1103` | EQU/LABEL(md) | `src/LO_SYN.mad:199`, `include/LO_SYN.labels.md:651` | 1103B | 3 |
| `ME1517` | EQU/LABEL(md) | `src/LO_SYN.mad:250`, `include/LO_SYN.labels.md:680` | 1517B | 3 |
| `ME1523` | EQU/LABEL(md) | `src/LO_SYN.mad:398`, `include/LO_SYN.labels.md:727` | 1523B | 3 |
| `ME2110` | EQU/LABEL(md) | `src/LO_SYN.mad:166`, `include/LO_SYN.labels.md:636` | 2110B | 3 |
| `ME2516` | EQU/LABEL(md) | `src/LO_SYN.mad:248`, `include/LO_SYN.labels.md:678` | 2516B | 3 |
| `ME2544` | EQU/LABEL(md) | `src/LO_SYN.mad:208`, `include/LO_SYN.labels.md:658` | 2544B | 3 |
| `ME4117` | EQU/LABEL(md) | `src/LO_SYN.mad:236`, `include/LO_SYN.labels.md:671` | 4117B | 3 |
| `ME4440` | EQU/LABEL(md) | `src/LO_SYN.mad:231`, `include/LO_SYN.labels.md:670` | 4440B | 3 |
| `ME7011` | EQU/LABEL(md) | `src/LO_SYN.mad:80`, `include/LO_SYN.labels.md:605` | 70115B | 3 |
| `ME7012` | EQU/LABEL(md) | `src/LO_SYN.mad:213`, `include/LO_SYN.labels.md:661` | 70120B | 3 |
| `ME7052` | EQU/LABEL(md) | `src/LO_SYN.mad:503`, `include/LO_SYN.labels.md:766` | 70524B | 3 |
| `ME7111` | EQU/LABEL(md) | `src/LO_SYN.mad:228`, `include/LO_SYN.labels.md:668` | 71116B | 3 |
| `ME7113` | EQU/LABEL(md) | `src/LO_SYN.mad:249`, `include/LO_SYN.labels.md:679` | 71131B | 3 |
| `ME7151` | EQU/LABEL(md) | `src/LO_SYN.mad:346`, `include/LO_SYN.labels.md:711` | 71517B | 3 |
| `ME7415` | EQU/LABEL(md) | `src/LO_SYN.mad:174`, `include/LO_SYN.labels.md:639` | 74151B | 3 |
| `ME7611` | EQU/LABEL(md) | `src/LO_SYN.mad:297`, `include/LO_SYN.labels.md:697` | 76117B | 3 |
| `MV7014` | EQU/LABEL(md) | `src/LO_SYN.mad:125`, `include/LO_SYN.labels.md:425` | 70142B | 3 |
| `ONE` | EQU/LABEL/LABEL(md) | `src/FOREX_RUNTIME_DISASM.mad:64`, `src/LO_GEN.mad:274`, `src/LO_GEN.mad:682`, `src/LO_GEN.mad:1711`, `src/LO_GEN.mad:1723`, `src/LO_GEN.mad:1732` … (+4) | 1 | 3 |
| `RG0104` | EQU/LABEL(md) | `src/LO_SYN.mad:519`, `include/LO_SYN.labels.md:544` | 104B | 3 |
| `RG1117` | EQU/LABEL(md) | `src/LO_SYN.mad:478`, `include/LO_SYN.labels.md:538` | 1117B | 3 |
| `RG7011` | EQU/LABEL(md) | `src/LO_SYN.mad:345`, `include/LO_SYN.labels.md:528` | 70110B | 3 |
| `RG7752` | EQU/LABEL(md) | `src/LO_SYN.mad:217`, `include/LO_SYN.labels.md:514` | 77520B | 3 |
| `RM*` | COMMON | `include/FOREX_ROOT.mad:241` | RMWD4 | 3 |
| `RMOD3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:73`, `include/FOREX_ROOT.mad:46`, `include/FOREX.labels.md:265`, `include/FOREX.labels.md:334`, `include/FOREX.labels.md:603` | 3 | 3 |
| `SC1001` | EQU/LABEL(md) | `src/LO_SYN.mad:705`, `include/LO_SYN.labels.md:473` | 1001B | 3 |
| `SC1101` | EQU/LABEL(md) | `src/LO_SYN.mad:736`, `include/LO_SYN.labels.md:480` | 1101B | 3 |
| `STKOF2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:76`, `include/FOREX_ROOT.mad:49`, `include/FOREX.labels.md:268`, `include/FOREX.labels.md:337`, `include/FOREX.labels.md:610` | -2 | 3 |
| `STKOF3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:77`, `include/FOREX.labels.md:269`, `include/FOREX.labels.md:611` | -3 | 3 |
| `STKOF4` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:78`, `include/FOREX.labels.md:270`, `include/FOREX.labels.md:612` | -4 | 3 |
| `SYMTG` | EQU/LABEL(md) | `src/FOREX_CORE.mad:139`, `include/FOREX.labels.md:210`, `include/FOREX.labels.md:617` | 65412B | 3 |
| `TIMCL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:140`, `include/FOREX.labels.md:211`, `include/FOREX.labels.md:645` | 4024B | 3 |
| `X57M6` | EQU/LABEL(md) | `src/FOREX_CORE.mad:109`, `include/FOREX.labels.md:180`, `include/FOREX.labels.md:478` | 6B | 3 |
| `*00065` | LABEL | `src/FOREX_RUNTIME.mad:305` | — | 2 |
| `A/I0` | COMMON | `src/FOREX_CORE.mad:155`, `src/LO_SYN.mad:27`, `include/FOREX_ROOT.mad:68` | ONEW | 2 |
| `AC0015` | EQU/LABEL(md) | `src/LO_GEN.mad:92`, `include/LO_GEN.labels.md:1142` | 15B | 2 |
| `AC0020` | EQU/LABEL(md) | `src/LO_GEN.mad:102`, `include/LO_GEN.labels.md:1152` | 20B | 2 |
| `AC0022` | EQU/LABEL(md) | `src/LO_GEN.mad:105`, `include/LO_GEN.labels.md:1155` | 22B | 2 |
| `AC0033` | EQU/LABEL(md) | `src/LO_GEN.mad:121`, `include/LO_GEN.labels.md:1171` | 33B | 2 |
| `AC0034` | EQU/LABEL(md) | `src/LO_GEN.mad:122`, `include/LO_GEN.labels.md:1172` | 34B | 2 |
| `AC0036` | EQU/LABEL(md) | `src/LO_GEN.mad:124`, `include/LO_GEN.labels.md:1174` | 36B | 2 |
| `AC0037` | EQU/LABEL(md) | `src/LO_GEN.mad:125`, `include/LO_GEN.labels.md:1175` | 37B | 2 |
| `AC0043` | EQU/LABEL(md) | `src/LO_GEN.mad:160`, `include/LO_GEN.labels.md:1210` | 43B | 2 |
| `AC0053` | EQU/LABEL(md) | `src/LO_GEN.mad:178`, `include/LO_GEN.labels.md:1228` | 53B | 2 |
| `AC0056` | EQU/LABEL(md) | `src/LO_GEN.mad:183`, `include/LO_GEN.labels.md:1233` | 56B | 2 |
| `AC0067` | EQU/LABEL(md) | `src/LO_GEN.mad:224`, `include/LO_GEN.labels.md:1274` | 67B | 2 |
| `AC0101` | EQU/LABEL(md) | `src/LO_GEN.mad:49`, `include/LO_GEN.labels.md:1099` | 101B | 2 |
| `AC0133` | EQU/LABEL(md) | `src/LO_GEN.mad:70`, `include/LO_GEN.labels.md:1120` | 133B | 2 |
| `AC0135` | EQU/LABEL(md) | `src/LO_GEN.mad:78`, `include/LO_GEN.labels.md:1128` | 135B | 2 |
| `AC0176` | EQU/LABEL(md) | `src/LO_GEN.mad:100`, `include/LO_GEN.labels.md:1150` | 176B | 2 |
| `AC0747` | EQU/LABEL(md) | `src/LO_GEN.mad:235`, `include/LO_GEN.labels.md:1285` | 747B | 2 |
| `AC0NCY` | EQU/LABEL(md) | `src/LO_GEN.mad:116`, `include/LO_GEN.labels.md:1166` | 30274B | 2 |
| `AC0V6J` | EQU/LABEL(md) | `src/LO_GEN.mad:136`, `include/LO_GEN.labels.md:1186` | 40411B | 2 |
| `AC0V6X` | EQU/LABEL(md) | `src/LO_GEN.mad:140`, `include/LO_GEN.labels.md:1190` | 40425B | 2 |
| `AC0V79` | EQU/LABEL(md) | `src/LO_GEN.mad:143`, `include/LO_GEN.labels.md:1193` | 40437B | 2 |
| `AC0WU4` | EQU/LABEL(md) | `src/LO_GEN.mad:159`, `include/LO_GEN.labels.md:1209` | 42556B | 2 |
| `AC12ZM` | EQU/LABEL(md) | `src/LO_GEN.mad:171`, `include/LO_GEN.labels.md:1221` | 50530B | 2 |
| `AC1351` | EQU/LABEL(md) | `src/LO_GEN.mad:79`, `include/LO_GEN.labels.md:1129` | 1351B | 2 |
| `AC1360` | EQU/LABEL(md) | `src/LO_GEN.mad:82`, `include/LO_GEN.labels.md:1132` | 1360B | 2 |
| `AC1362` | EQU/LABEL(md) | `src/LO_GEN.mad:83`, `include/LO_GEN.labels.md:1133` | 1362B | 2 |
| `AC17NF` | EQU/LABEL(md) | `src/LO_GEN.mad:191`, `include/LO_GEN.labels.md:1241` | 56571B | 2 |
| `AC17NI` | EQU/LABEL(md) | `src/LO_GEN.mad:193`, `include/LO_GEN.labels.md:1243` | 56574B | 2 |
| `AC17OC` | EQU/LABEL(md) | `src/LO_GEN.mad:199`, `include/LO_GEN.labels.md:1249` | 56604B | 2 |
| `AC17OT` | EQU/LABEL(md) | `src/LO_GEN.mad:207`, `include/LO_GEN.labels.md:1257` | 56621B | 2 |
| `AC17OW` | EQU/LABEL(md) | `src/LO_GEN.mad:209`, `include/LO_GEN.labels.md:1259` | 56624B | 2 |
| `AC1AJ7` | EQU/LABEL(md) | `src/LO_GEN.mad:216`, `include/LO_GEN.labels.md:1266` | 60307B | 2 |
| `AC4114` | EQU/LABEL(md) | `src/LO_GEN.mad:155`, `include/LO_GEN.labels.md:1205` | 4114B | 2 |
| `AI0AD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:35`, `include/FOREX.labels.md:106`, `include/FOREX.labels.md:377` | 4007B | 2 |
| `AP0110` | EQU/LABEL(md) | `src/LO_SYN.mad:489`, `include/LO_SYN.labels.md:394` | 20110B | 2 |
| `AP2014` | EQU/LABEL(md) | `src/LO_SYN.mad:181`, `include/LO_SYN.labels.md:363` | 20146B | 2 |
| `AP2105` | EQU/LABEL(md) | `src/LO_SYN.mad:190`, `include/LO_SYN.labels.md:364` | 52105B | 2 |
| `AP4104` | EQU/LABEL(md) | `src/LO_SYN.mad:409`, `include/LO_SYN.labels.md:388` | 41040B | 2 |
| `AP4150` | EQU/LABEL(md) | `src/LO_SYN.mad:152`, `include/LO_SYN.labels.md:361` | 41503B | 2 |
| `AP4156` | EQU/LABEL(md) | `src/LO_SYN.mad:161`, `include/LO_SYN.labels.md:362` | 41560B | 2 |
| `AP4244` | EQU/LABEL(md) | `src/LO_SYN.mad:266`, `include/LO_SYN.labels.md:370` | 42440B | 2 |
| `AP4554` | EQU/LABEL(md) | `src/LO_SYN.mad:568`, `include/LO_SYN.labels.md:401` | 45543B | 2 |
| `AP4644` | EQU/LABEL(md) | `src/LO_SYN.mad:293`, `include/LO_SYN.labels.md:373` | 46440B | 2 |
| `AP6444` | EQU/LABEL(md) | `src/LO_SYN.mad:500`, `include/LO_SYN.labels.md:396` | 64440B | 2 |
| `AP6505` | EQU/LABEL(md) | `src/LO_SYN.mad:551`, `include/LO_SYN.labels.md:399` | 46505B | 2 |
| `AP6617` | EQU/LABEL(md) | `src/LO_SYN.mad:285`, `include/LO_SYN.labels.md:371` | 66170B | 2 |
| `AP7004` | EQU/LABEL(md) | `src/LO_SYN.mad:314`, `include/LO_SYN.labels.md:375` | 70040B | 2 |
| `BUFALN` | EQU/LABEL(md) | `src/FOREX_CORE.mad:38`, `include/FOREX_ROOT.mad:25`, `include/FOREX.labels.md:109`, `include/FOREX.labels.md:313`, `include/FOREX.labels.md:380` | 4000B | 2 |
| `C065` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:375` | — | 2 |
| `C101` | TEXT/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:387`, `include/RUNTIME_DISASM.xref.md:87` | 'ERROR  ' | 2 |
| `C76245` | LABEL(md) | `include/FOREX.labels.md:162`, `include/FOREX.labels.md:434` | 0o076245 | 2 |
| `CMOD3` | LABEL(md) | `include/FOREX.labels.md:164`, `include/FOREX.labels.md:436` | — | 2 |
| `DATA*` | COMMON | `src/FOREX_RUNTIME.mad:330` | DBFLN | 2 |
| `DP001` | ENTRY/XREF(md) | `src/FOREX_DECODER_DISASM.mad:153`, `include/RUNTIME_DECODER.xref.md:14` | — | 2 |
| `DPDAT` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:144`, `include/RUNTIME_DECODER.xref.md:13` | 2 | 2 |
| `DTMISH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:39`, `include/FOREX.labels.md:231`, `include/FOREX.labels.md:456` | 64-24 | 2 |
| `DTYRSH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:42`, `include/FOREX.labels.md:234`, `include/FOREX.labels.md:466` | 64-14 | 2 |
| `DUMMYL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:105`, `include/FOREX_ROOT.mad:27`, `include/FOREX.labels.md:176`, `include/FOREX.labels.md:315`, `include/FOREX.labels.md:472` | 5 | 2 |
| `ENTRY*` | COMMON | `src/FOREX_CORE.mad:149`, `src/LO_GEN.mad:498`, `src/LO_SYN.mad:20`, `include/FOREX_ROOT.mad:62` | AOC50 | 2 |
| `ENTTLN` | EQU/LABEL(md) | `src/FOREX_CORE.mad:108`, `include/FOREX_ROOT.mad:28`, `include/FOREX.labels.md:179`, `include/FOREX.labels.md:316`, `include/FOREX.labels.md:475` | 50B | 2 |
| `EX0001` | EQU/LABEL(md) | `src/LO_SYN.mad:150`, `include/LO_SYN.labels.md:264` | 20115B | 2 |
| `EX0002` | EQU/LABEL(md) | `src/LO_SYN.mad:443`, `include/LO_SYN.labels.md:157` | 20117B | 2 |
| `EX0007` | EQU/LABEL(md) | `src/LO_SYN.mad:226`, `include/LO_SYN.labels.md:271` | 52040B | 2 |
| `EX0017` | EQU/LABEL(md) | `src/LO_SYN.mad:536`, `include/LO_SYN.labels.md:311` | 20142B | 2 |
| `EX0102` | EQU/LABEL(md) | `src/LO_SYN.mad:353`, `include/LO_SYN.labels.md:124` | 102B | 2 |
| `EX0117` | EQU/LABEL(md) | `src/LO_SYN.mad:396`, `include/LO_SYN.labels.md:141` | 117B | 2 |
| `EX0510` | EQU/LABEL(md) | `src/LO_SYN.mad:265`, `include/LO_SYN.labels.md:101` | 510B | 2 |
| `EX1101` | EQU/LABEL(md) | `src/LO_SYN.mad:408`, `include/LO_SYN.labels.md:143` | 1101B | 2 |
| `EX1551` | EQU/LABEL(md) | `src/LO_SYN.mad:256`, `include/LO_SYN.labels.md:97` | 1551B | 2 |
| `EX2002` | EQU/LABEL(md) | `src/LO_SYN.mad:430`, `include/LO_SYN.labels.md:151` | 20102B | 2 |
| `EX2003` | EQU/LABEL(md) | `src/LO_SYN.mad:446`, `include/LO_SYN.labels.md:160` | 20103B | 2 |
| `EX2020` | EQU/LABEL(md) | `src/LO_SYN.mad:210`, `include/LO_SYN.labels.md:91` | 20115B | 2 |
| `EX3603` | EQU/LABEL(md) | `src/LO_SYN.mad:540`, `include/LO_SYN.labels.md:184` | 44103B | 2 |
| `EX3641` | EQU/LABEL(md) | `src/LO_SYN.mad:388`, `include/LO_SYN.labels.md:138` | 41524B | 2 |
| `EX3643` | EQU/LABEL(md) | `src/LO_SYN.mad:323`, `include/LO_SYN.labels.md:117` | 20143B | 2 |
| `EX3650` | EQU/LABEL(md) | `src/LO_SYN.mad:370`, `include/LO_SYN.labels.md:130` | 50110B | 2 |
| `EX3651` | EQU/LABEL(md) | `src/LO_SYN.mad:299`, `include/LO_SYN.labels.md:111` | 20151B | 2 |
| `EX3673` | EQU/LABEL(md) | `src/LO_SYN.mad:436`, `include/LO_SYN.labels.md:153` | 73105B | 2 |
| `EX4050` | EQU/LABEL(md) | `src/LO_SYN.mad:315`, `include/LO_SYN.labels.md:283` | 40503B | 2 |
| `EX4056` | EQU/LABEL(md) | `src/LO_SYN.mad:325`, `include/LO_SYN.labels.md:118` | 40561B | 2 |
| `EX4111` | EQU/LABEL(md) | `src/LO_SYN.mad:106`, `include/LO_SYN.labels.md:68` | 41117B | 2 |
| `EX4112` | EQU/LABEL(md) | `src/LO_SYN.mad:369`, `include/LO_SYN.labels.md:129` | 41124B | 2 |
| `EX4155` | EQU/LABEL(md) | `src/LO_SYN.mad:268`, `include/LO_SYN.labels.md:102` | 41554B | 2 |
| `EX4172` | EQU/LABEL(md) | `src/LO_SYN.mad:397`, `include/LO_SYN.labels.md:293` | 74172B | 2 |
| `EX4502` | EQU/LABEL(md) | `src/LO_SYN.mad:316`, `include/LO_SYN.labels.md:115` | 4502B | 2 |
| `EX4515` | EQU/LABEL(md) | `src/LO_SYN.mad:197`, `include/LO_SYN.labels.md:89` | 4515B | 2 |
| `EX4576` | EQU/LABEL(md) | `src/LO_SYN.mad:142`, `include/LO_SYN.labels.md:78` | 4576B | 2 |
| `EX4754` | EQU/LABEL(md) | `src/LO_SYN.mad:196`, `include/LO_SYN.labels.md:268` | 47542B | 2 |
| `EX5211` | EQU/LABEL(md) | `src/LO_SYN.mad:167`, `include/LO_SYN.labels.md:83` | 52113B | 2 |
| `EX5517` | EQU/LABEL(md) | `src/LO_SYN.mad:282`, `include/LO_SYN.labels.md:105` | 5517B | 2 |
| `EX6017` | EQU/LABEL(md) | `src/LO_SYN.mad:104`, `include/LO_SYN.labels.md:256` | 60176B | 2 |
| `EX6040` | EQU/LABEL(md) | `src/LO_SYN.mad:461`, `include/LO_SYN.labels.md:300` | 66040B | 2 |
| `EX6111` | EQU/LABEL(md) | `src/LO_SYN.mad:115`, `include/LO_SYN.labels.md:73` | 61117B | 2 |
| `EX6151` | EQU/LABEL(md) | `src/LO_SYN.mad:535`, `include/LO_SYN.labels.md:182` | 6151B | 2 |
| `EX6454` | EQU/LABEL(md) | `src/LO_SYN.mad:419`, `include/LO_SYN.labels.md:146` | 64543B | 2 |
| `EX6570` | EQU/LABEL(md) | `src/LO_SYN.mad:418`, `include/LO_SYN.labels.md:145` | 70101B | 2 |
| `EX7010` | EQU/LABEL(md) | `src/LO_SYN.mad:392`, `include/LO_SYN.labels.md:139` | 70105B | 2 |
| `EX7015` | EQU/LABEL(md) | `src/LO_SYN.mad:264`, `include/LO_SYN.labels.md:100` | 70151B | 2 |
| `EX7310` | EQU/LABEL(md) | `src/LO_SYN.mad:91`, `include/LO_SYN.labels.md:250` | 73105B | 2 |
| `EX7404` | EQU/LABEL(md) | `src/LO_SYN.mad:191`, `include/LO_SYN.labels.md:266` | 74040B | 2 |
| `EX7411` | EQU/LABEL(md) | `src/LO_SYN.mad:245`, `include/LO_SYN.labels.md:276` | 74110B | 2 |
| `EX7417` | EQU/LABEL(md) | `src/LO_SYN.mad:137`, `include/LO_SYN.labels.md:262` | 74173B | 2 |
| `EX7451` | EQU/LABEL(md) | `src/LO_SYN.mad:179`, `include/LO_SYN.labels.md:87` | 74513B | 2 |
| `EX7504` | EQU/LABEL(md) | `src/LO_SYN.mad:496`, `include/LO_SYN.labels.md:171` | 7504B | 2 |
| `EX7515` | EQU/LABEL(md) | `src/LO_SYN.mad:258`, `include/LO_SYN.labels.md:98` | 7515B | 2 |
| `EX7516` | EQU/LABEL(md) | `src/LO_SYN.mad:259`, `include/LO_SYN.labels.md:277` | 47516B | 2 |
| `EX7547` | EQU/LABEL(md) | `src/LO_SYN.mad:434`, `include/LO_SYN.labels.md:298` | 47547B | 2 |
| `EX7744` | EQU/LABEL(md) | `src/LO_SYN.mad:513`, `include/LO_SYN.labels.md:176` | 77440B | 2 |
| `EX7752` | EQU/LABEL(md) | `src/LO_SYN.mad:438`, `include/LO_SYN.labels.md:154` | 77524B | 2 |
| `F541AD` | EQU/LABEL(md) | `src/LO_GEN.mad:44`, `include/LO_GEN.labels.md:1094` | 77237B | 2 |
| `FLGEX*` | COMMON | `src/FOREX_CORE.mad:150`, `src/LO_SYN.mad:23`, `include/FOREX_ROOT.mad:63` | ONEW | 2 |
| `FMT026` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:187`, `include/RUNTIME_DISASM.xref.md:62` | — | 2 |
| `FTDCNS` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:186`, `include/FOREX.labels.md:44`, `include/FOREX.labels.md:500` | — | 2 |
| `FTDTE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:183`, `include/FOREX.labels.md:43`, `include/FOREX.labels.md:507` | — | 2 |
| `FTLOG` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:37`, `include/RUNTIME_DISASM.xref.md:74` | 10000000 00000000 | 2 |
| `FULISF` | COMMON/LABEL(md) | `src/FOREX_CORE.mad:152`, `src/LO_SYN.mad:25`, `include/FOREX_ROOT.mad:65`, `include/FOREX.labels.md:513`, `include/FOREX.labels.md:696` | ONEW | 2 |
| `JT0W3P` | EQU/LABEL(md) | `src/LO_GEN.mad:288`, `include/LO_GEN.labels.md:1340` | 41605B | 2 |
| `JT0W44` | EQU/LABEL(md) | `src/LO_GEN.mad:289`, `include/LO_GEN.labels.md:1341` | 41620B | 2 |
| `JT0W4F` | EQU/LABEL(md) | `src/LO_GEN.mad:290`, `include/LO_GEN.labels.md:1342` | 41631B | 2 |
| `JT0WFS` | EQU/LABEL(md) | `src/LO_GEN.mad:293`, `include/LO_GEN.labels.md:1345` | 42040B | 2 |
| `JT0Y46` | EQU/LABEL(md) | `src/LO_GEN.mad:314`, `include/LO_GEN.labels.md:1366` | 44214B | 2 |
| `JT1554` | EQU/LABEL(md) | `src/LO_GEN.mad:320`, `include/LO_GEN.labels.md:1372` | 53320B | 2 |
| `JT1672` | EQU/LABEL(md) | `src/LO_GEN.mad:277`, `include/LO_GEN.labels.md:1329` | 1672B | 2 |
| `JT1BXM` | EQU/LABEL(md) | `src/LO_GEN.mad:333`, `include/LO_GEN.labels.md:1385` | 62122B | 2 |
| `JT1C6B` | EQU/LABEL(md) | `src/LO_GEN.mad:334`, `include/LO_GEN.labels.md:1386` | 62435B | 2 |
| `JT1CBU` | EQU/LABEL(md) | `src/LO_GEN.mad:336`, `include/LO_GEN.labels.md:1388` | 62634B | 2 |
| `JT1CTN` | EQU/LABEL(md) | `src/LO_GEN.mad:339`, `include/LO_GEN.labels.md:1391` | 63275B | 2 |
| `JT1D2T` | EQU/LABEL(md) | `src/LO_GEN.mad:342`, `include/LO_GEN.labels.md:1394` | 63605B | 2 |
| `JT1M4E` | EQU/LABEL(md) | `src/LO_GEN.mad:349`, `include/LO_GEN.labels.md:1401` | 75326B | 2 |
| `JT1M7C` | EQU/LABEL(md) | `src/LO_GEN.mad:359`, `include/LO_GEN.labels.md:1411` | 75432B | 2 |
| `JT1M9X` | EQU/LABEL(md) | `src/LO_GEN.mad:370`, `include/LO_GEN.labels.md:1422` | 75525B | 2 |
| `JT1MA6` | EQU/LABEL(md) | `src/LO_GEN.mad:372`, `include/LO_GEN.labels.md:1424` | 75534B | 2 |
| `JT1MAD` | EQU/LABEL(md) | `src/LO_GEN.mad:373`, `include/LO_GEN.labels.md:1425` | 75541B | 2 |
| `JT1MWD` | EQU/LABEL(md) | `src/LO_GEN.mad:410`, `include/LO_GEN.labels.md:1462` | 76333B | 2 |
| `JT1MWE` | EQU/LABEL(md) | `src/LO_GEN.mad:411`, `include/LO_GEN.labels.md:1463` | 76334B | 2 |
| `JT1MWR` | EQU/LABEL(md) | `src/LO_GEN.mad:413`, `include/LO_GEN.labels.md:1465` | 76347B | 2 |
| `JT1MZO` | EQU/LABEL(md) | `src/LO_GEN.mad:437`, `include/LO_GEN.labels.md:1489` | 76452B | 2 |
| `JT1N1F` | EQU/LABEL(md) | `src/LO_GEN.mad:446`, `include/LO_GEN.labels.md:1498` | 76515B | 2 |
| `JT1N2I` | EQU/LABEL(md) | `src/LO_GEN.mad:448`, `include/LO_GEN.labels.md:1500` | 76554B | 2 |
| `JT1N2V` | EQU/LABEL(md) | `src/LO_GEN.mad:453`, `include/LO_GEN.labels.md:1505` | 76567B | 2 |
| `JT1N2Z` | EQU/LABEL(md) | `src/LO_GEN.mad:454`, `include/LO_GEN.labels.md:1506` | 76571B | 2 |
| `JT1N7G` | EQU/LABEL(md) | `src/LO_GEN.mad:462`, `include/LO_GEN.labels.md:1514` | 76732B | 2 |
| `JT1N7V` | EQU/LABEL(md) | `src/LO_GEN.mad:463`, `include/LO_GEN.labels.md:1515` | 76747B | 2 |
| `JT1NGD` | EQU/LABEL(md) | `src/LO_GEN.mad:469`, `include/LO_GEN.labels.md:1521` | 77053B | 2 |
| `JT1NHO` | EQU/LABEL(md) | `src/LO_GEN.mad:473`, `include/LO_GEN.labels.md:1525` | 77100B | 2 |
| `JT1NHP` | EQU/LABEL(md) | `src/LO_GEN.mad:474`, `include/LO_GEN.labels.md:1526` | 77101B | 2 |
| `JT1NIB` | EQU/LABEL(md) | `src/LO_GEN.mad:484`, `include/LO_GEN.labels.md:1536` | 77123B | 2 |
| `LDADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:119`, `include/FOREX.labels.md:190`, `include/FOREX.labels.md:539` | 74022B | 2 |
| `LIBA27` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:318`, `include/RUNTIME_DISASM.xref.md:79` | — | 2 |
| `LIBA45` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:346`, `include/RUNTIME_DISASM.xref.md:83` | — | 2 |
| `ME0005` | EQU/LABEL(md) | `src/LO_SYN.mad:269`, `include/LO_SYN.labels.md:686` | 70104B | 2 |
| `ME0010` | EQU/LABEL(md) | `src/LO_SYN.mad:571`, `include/LO_SYN.labels.md:785` | 77104B | 2 |
| `ME0102` | EQU/LABEL(md) | `src/LO_SYN.mad:172`, `include/LO_SYN.labels.md:638` | 102B | 2 |
| `ME0120` | EQU/LABEL(md) | `src/LO_SYN.mad:89`, `include/LO_SYN.labels.md:608` | 120B | 2 |
| `ME0147` | EQU/LABEL(md) | `src/LO_SYN.mad:403`, `include/LO_SYN.labels.md:730` | 147B | 2 |
| `ME0160` | EQU/LABEL(md) | `src/LO_SYN.mad:267`, `include/LO_SYN.labels.md:685` | 160B | 2 |
| `ME0510` | EQU/LABEL(md) | `src/LO_SYN.mad:160`, `include/LO_SYN.labels.md:634` | 510B | 2 |
| `ME0524` | EQU/LABEL(md) | `src/LO_SYN.mad:393`, `include/LO_SYN.labels.md:726` | 524B | 2 |
| `ME1057` | EQU/LABEL(md) | `src/LO_SYN.mad:472`, `include/LO_SYN.labels.md:752` | 1057B | 2 |
| `ME1110` | EQU/LABEL(md) | `src/LO_SYN.mad:518`, `include/LO_SYN.labels.md:771` | 1110B | 2 |
| `ME1117` | EQU/LABEL(md) | `src/LO_SYN.mad:136`, `include/LO_SYN.labels.md:619` | 1117B | 2 |
| `ME1154` | EQU/LABEL(md) | `src/LO_SYN.mad:260`, `include/LO_SYN.labels.md:684` | 1154B | 2 |
| `ME1440` | EQU/LABEL(md) | `src/LO_SYN.mad:122`, `include/LO_SYN.labels.md:615` | 1440B | 2 |
| `ME1554` | EQU/LABEL(md) | `src/LO_SYN.mad:105`, `include/LO_SYN.labels.md:610` | 1554B | 2 |
| `ME1560` | EQU/LABEL(md) | `src/LO_SYN.mad:177`, `include/LO_SYN.labels.md:641` | 1560B | 2 |
| `ME2170` | EQU/LABEL(md) | `src/LO_SYN.mad:460`, `include/LO_SYN.labels.md:747` | 2170B | 2 |
| `ME2200` | EQU/LABEL(md) | `src/LO_SYN.mad:47`, `include/LO_SYN.labels.md:590` | 2200B | 2 |
| `ME2524` | EQU/LABEL(md) | `src/LO_SYN.mad:533`, `include/LO_SYN.labels.md:774` | 2524B | 2 |
| `ME4124` | EQU/LABEL(md) | `src/LO_SYN.mad:151`, `include/LO_SYN.labels.md:628` | 4124B | 2 |
| `ME4506` | EQU/LABEL(md) | `src/LO_SYN.mad:433`, `include/LO_SYN.labels.md:739` | 4506B | 2 |
| `ME4513` | EQU/LABEL(md) | `src/LO_SYN.mad:300`, `include/LO_SYN.labels.md:698` | 4513B | 2 |
| `ME4572` | EQU/LABEL(md) | `src/LO_SYN.mad:87`, `include/LO_SYN.labels.md:607` | 4572B | 2 |
| `ME5101` | EQU/LABEL(md) | `src/LO_SYN.mad:193`, `include/LO_SYN.labels.md:650` | 5101B | 2 |
| `ME5110` | EQU/LABEL(md) | `src/LO_SYN.mad:361`, `include/LO_SYN.labels.md:717` | 5110B | 2 |
| `ME5377` | EQU/LABEL(md) | `src/LO_SYN.mad:48`, `include/LO_SYN.labels.md:591` | 5377B | 2 |
| `ME6104` | EQU/LABEL(md) | `src/LO_SYN.mad:497`, `include/LO_SYN.labels.md:763` | 76104B | 2 |
| `ME7155` | EQU/LABEL(md) | `src/LO_SYN.mad:178`, `include/LO_SYN.labels.md:642` | 71551B | 2 |
| `ME7412` | EQU/LABEL(md) | `src/LO_SYN.mad:227`, `include/LO_SYN.labels.md:667` | 74124B | 2 |
| `ME7444` | EQU/LABEL(md) | `src/LO_SYN.mad:527`, `include/LO_SYN.labels.md:773` | 74440B | 2 |
| `ME7450` | EQU/LABEL(md) | `src/LO_SYN.mad:301`, `include/LO_SYN.labels.md:699` | 74501B | 2 |
| `ME7455` | EQU/LABEL(md) | `src/LO_SYN.mad:201`, `include/LO_SYN.labels.md:653` | 74554B | 2 |
| `ME7610` | EQU/LABEL(md) | `src/LO_SYN.mad:209`, `include/LO_SYN.labels.md:659` | 76105B | 2 |
| `ME7711` | EQU/LABEL(md) | `src/LO_SYN.mad:453`, `include/LO_SYN.labels.md:744` | 77110B | 2 |
| `ME7756` | EQU/LABEL(md) | `src/LO_SYN.mad:319`, `include/LO_SYN.labels.md:704` | 77560B | 2 |
| `MK761` | EQU/LABEL(md) | `src/FOREX_CORE.mad:123`, `include/FOREX.labels.md:194`, `include/FOREX.labels.md:544` | 7761B | 2 |
| `MK763` | EQU/LABEL(md) | `src/FOREX_CORE.mad:124`, `include/FOREX.labels.md:195`, `include/FOREX.labels.md:545` | 7763B | 2 |
| `MV08R7` | EQU/LABEL(md) | `src/LO_GEN.mad:244`, `include/LO_GEN.labels.md:1298` | 11347 | 2 |
| `MV09NO` | EQU/LABEL(md) | `src/LO_GEN.mad:247`, `include/LO_GEN.labels.md:1301` | 12516 | 2 |
| `MV0COW` | EQU/LABEL(md) | `src/LO_GEN.mad:248`, `include/LO_GEN.labels.md:1302` | 16448 | 2 |
| `MV7010` | EQU/LABEL(md) | `src/LO_SYN.mad:342`, `include/LO_SYN.labels.md:426` | 70103B | 2 |
| `MV7012` | EQU/LABEL(md) | `src/LO_SYN.mad:385`, `include/LO_SYN.labels.md:432` | 70120B | 2 |
| `MV7015` | EQU/LABEL(md) | `src/LO_SYN.mad:352`, `include/LO_SYN.labels.md:428` | 70151B | 2 |
| `MV7016` | EQU/LABEL(md) | `src/LO_SYN.mad:368`, `include/LO_SYN.labels.md:430` | 70160B | 2 |
| `NG0002` | EQU/LABEL(md) | `src/LO_GEN.mad:268`, `include/LO_GEN.labels.md:1322` | -2 | 2 |
| `NOLISF` | COMMON/LABEL(md) | `src/FOREX_CORE.mad:151`, `src/LO_SYN.mad:24`, `include/FOREX_ROOT.mad:64`, `include/FOREX.labels.md:554`, `include/FOREX.labels.md:695` | ONEW | 2 |
| `OCTTDE` | LABEL(md)/NAME/SUBP | `src/FOREX_CORE.mad:164`, `src/FOREX_RUNTIME.mad:432`, `src/LO_GEN.mad:32`, `src/LO_SYN.mad:31`, `include/FOREX_ROOT.mad:72`, `include/FOREX.labels.md:7` … (+6) | — | 2 |
| `PG67SA` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:289`, `include/FOREX.labels.md:580` | ONEW | 2 |
| `PGFLSA` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:288`, `include/FOREX.labels.md:88`, `include/FOREX.labels.md:581` | ONEW | 2 |
| `PGMD73` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:38`, `include/FOREX.labels.md:326`, `include/FOREX.labels.md:571` | =73401 | 2 |
| `PGSHWD` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:287`, `include/FOREX.labels.md:588` | ONEW | 2 |
| `PGSTP2` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:57`, `include/FOREX.labels.md:345`, `include/FOREX.labels.md:589` | 2 | 2 |
| `PGWRKB` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:242`, `include/FOREX.labels.md:87`, `include/FOREX.labels.md:591` | — | 2 |
| `RET` | COMMON/XREF(md) | `src/FOREX_CORE.mad:157`, `include/RUNTIME_DECODER.xref.md:26` | ONEW | 2 |
| `RG0016` | EQU/LABEL(md) | `src/LO_SYN.mad:67`, `include/LO_SYN.labels.md:497` | 16B | 2 |
| `RG0017` | EQU/LABEL(md) | `src/LO_SYN.mad:57`, `include/LO_SYN.labels.md:494` | 17B | 2 |
| `RG0102` | EQU/LABEL(md) | `src/LO_SYN.mad:528`, `include/LO_SYN.labels.md:546` | 102B | 2 |
| `RG0151` | EQU/LABEL(md) | `src/LO_SYN.mad:123`, `include/LO_SYN.labels.md:503` | 151B | 2 |
| `RG3027` | EQU/LABEL(md) | `src/LO_SYN.mad:56`, `include/LO_SYN.labels.md:493` | 30274B | 2 |
| `RG4044` | EQU/LABEL(md) | `src/LO_SYN.mad:467`, `include/LO_SYN.labels.md:536` | 40440B | 2 |
| `RG4054` | EQU/LABEL(md) | `src/LO_SYN.mad:287`, `include/LO_SYN.labels.md:522` | 40544B | 2 |
| `RG4105` | EQU/LABEL(md) | `src/LO_SYN.mad:144`, `include/LO_SYN.labels.md:506` | 4105B | 2 |
| `RG4410` | EQU/LABEL(md) | `src/LO_SYN.mad:514`, `include/LO_SYN.labels.md:542` | 44101B | 2 |
| `RG4751` | EQU/LABEL(md) | `src/LO_SYN.mad:147`, `include/LO_SYN.labels.md:507` | 47510B | 2 |
| `RG6105` | EQU/LABEL(md) | `src/LO_SYN.mad:225`, `include/LO_SYN.labels.md:515` | 6105B | 2 |
| `RG7004` | EQU/LABEL(md) | `src/LO_SYN.mad:380`, `include/LO_SYN.labels.md:531` | 70040B | 2 |
| `RG7010` | EQU/LABEL(md) | `src/LO_SYN.mad:525`, `include/LO_SYN.labels.md:545` | 70102B | 2 |
| `RG7016` | EQU/LABEL(md) | `src/LO_SYN.mad:350`, `include/LO_SYN.labels.md:529` | 70160B | 2 |
| `RG7554` | EQU/LABEL(md) | `src/LO_SYN.mad:198`, `include/LO_SYN.labels.md:512` | 7554B | 2 |
| `RG7655` | EQU/LABEL(md) | `src/LO_SYN.mad:128`, `include/LO_SYN.labels.md:504` | 76551B | 2 |
| `RS0007` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:264`, `src/LO_GEN.mad:554`, `src/LO_GEN.mad:691`, `src/LO_GEN.mad:697`, `src/LO_GEN.mad:706`, `src/LO_GEN.mad:712` … (+210) | 7 | 2 |
| `SC0001` | EQU/LABEL(md) | `src/LO_SYN.mad:51`, `include/LO_SYN.labels.md:5`, `include/LO_SYN.labels.md:445` | 1B | 2 |
| `STKOF5` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:79`, `include/FOREX.labels.md:271`, `include/FOREX.labels.md:613` | -5 | 2 |
| `X01` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:51`, `include/RUNTIME_DISASM.xref.md:25` | 74001B | 2 |
| `*00014` | LABEL | `src/FOREX_RUNTIME.mad:224` | — | 1 |
| `*00066` | LABEL | `src/FOREX_RUNTIME.mad:306` | — | 1 |
| `*00067` | LABEL | `src/FOREX_RUNTIME.mad:307` | — | 1 |
| `*00073` | LABEL | `src/FOREX_RUNTIME.mad:311` | — | 1 |
| `*00075` | LABEL | `src/FOREX_RUNTIME.mad:313` | — | 1 |
| `*00101` | TEXT | `src/FOREX_RUNTIME.mad:318` | TL0013 | 1 |
| `AB1005` | LABEL/LABEL(md) | `src/LO_SYN.mad:2320`, `include/LO_SYN.labels.md:20` | — | 1 |
| `AC0004` | EQU/LABEL(md) | `src/LO_GEN.mad:127`, `include/LO_GEN.labels.md:1177` | 4B | 1 |
| `AC0025` | EQU/LABEL(md) | `src/LO_GEN.mad:111`, `include/LO_GEN.labels.md:1161` | 25B | 1 |
| `AC0040` | EQU/LABEL(md) | `src/LO_GEN.mad:128`, `include/LO_GEN.labels.md:1178` | 40B | 1 |
| `AC0041` | EQU/LABEL(md) | `src/LO_GEN.mad:154`, `include/LO_GEN.labels.md:1204` | 41B | 1 |
| `AC0042` | EQU/LABEL(md) | `src/LO_GEN.mad:156`, `include/LO_GEN.labels.md:1206` | 42B | 1 |
| `AC0047` | EQU/LABEL(md) | `src/LO_GEN.mad:165`, `include/LO_GEN.labels.md:1215` | 47B | 1 |
| `AC0052` | EQU/LABEL(md) | `src/LO_GEN.mad:173`, `include/LO_GEN.labels.md:1223` | 52B | 1 |
| `AC0054` | EQU/LABEL(md) | `src/LO_GEN.mad:181`, `include/LO_GEN.labels.md:1231` | 54B | 1 |
| `AC0057` | EQU/LABEL(md) | `src/LO_GEN.mad:211`, `include/LO_GEN.labels.md:1261` | 57B | 1 |
| `AC0060` | EQU/LABEL(md) | `src/LO_GEN.mad:214`, `include/LO_GEN.labels.md:1264` | 60B | 1 |
| `AC0061` | EQU/LABEL(md) | `src/LO_GEN.mad:217`, `include/LO_GEN.labels.md:1267` | 61B | 1 |
| `AC0063` | EQU/LABEL(md) | `src/LO_GEN.mad:219`, `include/LO_GEN.labels.md:1269` | 63B | 1 |
| `AC0064` | EQU/LABEL(md) | `src/LO_GEN.mad:220`, `include/LO_GEN.labels.md:1270` | 64B | 1 |
| `AC0065` | EQU/LABEL(md) | `src/LO_GEN.mad:221`, `include/LO_GEN.labels.md:1271` | 65B | 1 |
| `AC0066` | EQU/LABEL(md) | `src/LO_GEN.mad:223`, `include/LO_GEN.labels.md:1273` | 66B | 1 |
| `AC0070` | EQU/LABEL(md) | `src/LO_GEN.mad:226`, `include/LO_GEN.labels.md:1276` | 70B | 1 |
| `AC0071` | EQU/LABEL(md) | `src/LO_GEN.mad:230`, `include/LO_GEN.labels.md:1280` | 71B | 1 |
| `AC0072` | EQU/LABEL(md) | `src/LO_GEN.mad:231`, `include/LO_GEN.labels.md:1281` | 72B | 1 |
| `AC0073` | EQU/LABEL(md) | `src/LO_GEN.mad:232`, `include/LO_GEN.labels.md:1282` | 73B | 1 |
| `AC0074` | EQU/LABEL(md) | `src/LO_GEN.mad:233`, `include/LO_GEN.labels.md:1283` | 74B | 1 |
| `AC0075` | EQU/LABEL(md) | `src/LO_GEN.mad:236`, `include/LO_GEN.labels.md:1286` | 75B | 1 |
| `AC0076` | EQU/LABEL(md) | `src/LO_GEN.mad:239`, `include/LO_GEN.labels.md:1289` | 76B | 1 |
| `AC0077` | EQU/LABEL(md) | `src/LO_GEN.mad:241`, `include/LO_GEN.labels.md:1291` | 77B | 1 |
| `AC0102` | EQU/LABEL(md) | `src/LO_GEN.mad:52`, `include/LO_GEN.labels.md:1102` | 102B | 1 |
| `AC0103` | EQU/LABEL(md) | `src/LO_GEN.mad:54`, `include/LO_GEN.labels.md:1104` | 103B | 1 |
| `AC0104` | EQU/LABEL(md) | `src/LO_GEN.mad:57`, `include/LO_GEN.labels.md:1107` | 104B | 1 |
| `AC0105` | EQU/LABEL(md) | `src/LO_GEN.mad:59`, `include/LO_GEN.labels.md:1109` | 105B | 1 |
| `AC0127` | EQU/LABEL(md) | `src/LO_GEN.mad:64`, `include/LO_GEN.labels.md:1114` | 127B | 1 |
| `AC0151` | EQU/LABEL(md) | `src/LO_GEN.mad:93`, `include/LO_GEN.labels.md:1143` | 151B | 1 |
| `AC0211` | EQU/LABEL(md) | `src/LO_GEN.mad:104`, `include/LO_GEN.labels.md:1154` | 211B | 1 |
| `AC0370` | EQU/LABEL(md) | `src/LO_GEN.mad:126`, `include/LO_GEN.labels.md:1176` | 370B | 1 |
| `AC0471` | EQU/LABEL(md) | `src/LO_GEN.mad:166`, `include/LO_GEN.labels.md:1216` | 471B | 1 |
| `AC0523` | EQU/LABEL(md) | `src/LO_GEN.mad:175`, `include/LO_GEN.labels.md:1225` | 523B | 1 |
| `AC0565` | EQU/LABEL(md) | `src/LO_GEN.mad:184`, `include/LO_GEN.labels.md:1234` | 565B | 1 |
| `AC0567` | EQU/LABEL(md) | `src/LO_GEN.mad:210`, `include/LO_GEN.labels.md:1260` | 567B | 1 |
| `AC0577` | EQU/LABEL(md) | `src/LO_GEN.mad:212`, `include/LO_GEN.labels.md:1262` | 577B | 1 |
| `AC0601` | EQU/LABEL(md) | `src/LO_GEN.mad:215`, `include/LO_GEN.labels.md:1265` | 601B | 1 |
| `AC0656` | EQU/LABEL(md) | `src/LO_GEN.mad:222`, `include/LO_GEN.labels.md:1272` | 656B | 1 |
| `AC0746` | EQU/LABEL(md) | `src/LO_GEN.mad:234`, `include/LO_GEN.labels.md:1284` | 746B | 1 |
| `AC0777` | EQU/LABEL(md) | `src/LO_GEN.mad:242`, `include/LO_GEN.labels.md:1292` | 777B | 1 |
| `AC0HHI` | EQU/LABEL(md) | `src/LO_GEN.mad:108`, `include/LO_GEN.labels.md:1158` | 22662B | 1 |
| `AC0NE0` | EQU/LABEL(md) | `src/LO_GEN.mad:117`, `include/LO_GEN.labels.md:1167` | 30312B | 1 |
| `AC0V1F` | EQU/LABEL(md) | `src/LO_GEN.mad:130`, `include/LO_GEN.labels.md:1180` | 40227B | 1 |
| `AC0V5L` | EQU/LABEL(md) | `src/LO_GEN.mad:131`, `include/LO_GEN.labels.md:1181` | 40377B | 1 |
| `AC0V69` | EQU/LABEL(md) | `src/LO_GEN.mad:132`, `include/LO_GEN.labels.md:1182` | 40401B | 1 |
| `AC0V6B` | EQU/LABEL(md) | `src/LO_GEN.mad:133`, `include/LO_GEN.labels.md:1183` | 40403B | 1 |
| `AC0V6D` | EQU/LABEL(md) | `src/LO_GEN.mad:134`, `include/LO_GEN.labels.md:1184` | 40405B | 1 |
| `AC0V6F` | EQU/LABEL(md) | `src/LO_GEN.mad:135`, `include/LO_GEN.labels.md:1185` | 40407B | 1 |
| `AC0V6P` | EQU/LABEL(md) | `src/LO_GEN.mad:137`, `include/LO_GEN.labels.md:1187` | 40417B | 1 |
| `AC0V6T` | EQU/LABEL(md) | `src/LO_GEN.mad:138`, `include/LO_GEN.labels.md:1188` | 40421B | 1 |
| `AC0V6V` | EQU/LABEL(md) | `src/LO_GEN.mad:139`, `include/LO_GEN.labels.md:1189` | 40423B | 1 |
| `AC0V75` | EQU/LABEL(md) | `src/LO_GEN.mad:141`, `include/LO_GEN.labels.md:1191` | 40433B | 1 |
| `AC0V77` | EQU/LABEL(md) | `src/LO_GEN.mad:142`, `include/LO_GEN.labels.md:1192` | 40435B | 1 |
| `AC0V7H` | EQU/LABEL(md) | `src/LO_GEN.mad:144`, `include/LO_GEN.labels.md:1194` | 40445B | 1 |
| `AC0V7J` | EQU/LABEL(md) | `src/LO_GEN.mad:145`, `include/LO_GEN.labels.md:1195` | 40447B | 1 |
| `AC0V7N` | EQU/LABEL(md) | `src/LO_GEN.mad:146`, `include/LO_GEN.labels.md:1196` | 40451B | 1 |
| `AC0V7P` | EQU/LABEL(md) | `src/LO_GEN.mad:147`, `include/LO_GEN.labels.md:1197` | 40453B | 1 |
| `AC0V7R` | EQU/LABEL(md) | `src/LO_GEN.mad:148`, `include/LO_GEN.labels.md:1198` | 40455B | 1 |
| `AC0V7T` | EQU/LABEL(md) | `src/LO_GEN.mad:149`, `include/LO_GEN.labels.md:1199` | 40457B | 1 |
| `AC0V7X` | EQU/LABEL(md) | `src/LO_GEN.mad:150`, `include/LO_GEN.labels.md:1200` | 40461B | 1 |
| `AC0V7Z` | EQU/LABEL(md) | `src/LO_GEN.mad:151`, `include/LO_GEN.labels.md:1201` | 40463B | 1 |
| `AC0V81` | EQU/LABEL(md) | `src/LO_GEN.mad:152`, `include/LO_GEN.labels.md:1202` | 40465B | 1 |
| `AC0V83` | EQU/LABEL(md) | `src/LO_GEN.mad:153`, `include/LO_GEN.labels.md:1203` | 40467B | 1 |
| `AC0ZLA` | EQU/LABEL(md) | `src/LO_GEN.mad:164`, `include/LO_GEN.labels.md:1214` | 46126B | 1 |
| `AC1010` | EQU/LABEL(md) | `src/LO_GEN.mad:50`, `include/LO_GEN.labels.md:1100` | 1010B | 1 |
| `AC1017` | EQU/LABEL(md) | `src/LO_GEN.mad:51`, `include/LO_GEN.labels.md:1101` | 1017B | 1 |
| `AC1021` | EQU/LABEL(md) | `src/LO_GEN.mad:53`, `include/LO_GEN.labels.md:1103` | 1021B | 1 |
| `AC1031` | EQU/LABEL(md) | `src/LO_GEN.mad:55`, `include/LO_GEN.labels.md:1105` | 1031B | 1 |
| `AC1035` | EQU/LABEL(md) | `src/LO_GEN.mad:56`, `include/LO_GEN.labels.md:1106` | 1035B | 1 |
| `AC1044` | EQU/LABEL(md) | `src/LO_GEN.mad:58`, `include/LO_GEN.labels.md:1108` | 1044B | 1 |
| `AC10UH` | EQU/LABEL(md) | `src/LO_GEN.mad:167`, `include/LO_GEN.labels.md:1217` | 47753B | 1 |
| `AC1210` | EQU/LABEL(md) | `src/LO_GEN.mad:63`, `include/LO_GEN.labels.md:1113` | 1210B | 1 |
| `AC12ZC` | EQU/LABEL(md) | `src/LO_GEN.mad:170`, `include/LO_GEN.labels.md:1220` | 50520B | 1 |
| `AC1322` | EQU/LABEL(md) | `src/LO_GEN.mad:67`, `include/LO_GEN.labels.md:1117` | 1322B | 1 |
| `AC1324` | EQU/LABEL(md) | `src/LO_GEN.mad:68`, `include/LO_GEN.labels.md:1118` | 1324B | 1 |
| `AC1326` | EQU/LABEL(md) | `src/LO_GEN.mad:69`, `include/LO_GEN.labels.md:1119` | 1326B | 1 |
| `AC1330` | EQU/LABEL(md) | `src/LO_GEN.mad:71`, `include/LO_GEN.labels.md:1121` | 1330B | 1 |
| `AC1332` | EQU/LABEL(md) | `src/LO_GEN.mad:72`, `include/LO_GEN.labels.md:1122` | 1332B | 1 |
| `AC1334` | EQU/LABEL(md) | `src/LO_GEN.mad:73`, `include/LO_GEN.labels.md:1123` | 1334B | 1 |
| `AC1336` | EQU/LABEL(md) | `src/LO_GEN.mad:74`, `include/LO_GEN.labels.md:1124` | 1336B | 1 |
| `AC1343` | EQU/LABEL(md) | `src/LO_GEN.mad:76`, `include/LO_GEN.labels.md:1126` | 1343B | 1 |
| `AC1347` | EQU/LABEL(md) | `src/LO_GEN.mad:77`, `include/LO_GEN.labels.md:1127` | 1347B | 1 |
| `AC1355` | EQU/LABEL(md) | `src/LO_GEN.mad:80`, `include/LO_GEN.labels.md:1130` | 1355B | 1 |
| `AC1374` | EQU/LABEL(md) | `src/LO_GEN.mad:85`, `include/LO_GEN.labels.md:1135` | 1374B | 1 |
| `AC1437` | EQU/LABEL(md) | `src/LO_GEN.mad:91`, `include/LO_GEN.labels.md:1141` | 1437B | 1 |
| `AC147P` | EQU/LABEL(md) | `src/LO_GEN.mad:174`, `include/LO_GEN.labels.md:1224` | 52117B | 1 |
| `AC14IQ` | EQU/LABEL(md) | `src/LO_GEN.mad:176`, `include/LO_GEN.labels.md:1226` | 52514B | 1 |
| `AC153D` | EQU/LABEL(md) | `src/LO_GEN.mad:179`, `include/LO_GEN.labels.md:1229` | 53257B | 1 |
| `AC1543` | EQU/LABEL(md) | `src/LO_GEN.mad:95`, `include/LO_GEN.labels.md:1145` | 1543B | 1 |
| `AC1641` | EQU/LABEL(md) | `src/LO_GEN.mad:97`, `include/LO_GEN.labels.md:1147` | 1641B | 1 |
| `AC1647` | EQU/LABEL(md) | `src/LO_GEN.mad:98`, `include/LO_GEN.labels.md:1148` | 1647B | 1 |
| `AC17N9` | EQU/LABEL(md) | `src/LO_GEN.mad:188`, `include/LO_GEN.labels.md:1238` | 56565B | 1 |
| `AC17NK` | EQU/LABEL(md) | `src/LO_GEN.mad:195`, `include/LO_GEN.labels.md:1245` | 56576B | 1 |
| `AC17NL` | EQU/LABEL(md) | `src/LO_GEN.mad:196`, `include/LO_GEN.labels.md:1246` | 56577B | 1 |
| `AC17O9` | EQU/LABEL(md) | `src/LO_GEN.mad:197`, `include/LO_GEN.labels.md:1247` | 56601B | 1 |
| `AC17OA` | EQU/LABEL(md) | `src/LO_GEN.mad:198`, `include/LO_GEN.labels.md:1248` | 56602B | 1 |
| `AC17OI` | EQU/LABEL(md) | `src/LO_GEN.mad:200`, `include/LO_GEN.labels.md:1250` | 56610B | 1 |
| `AC17OK` | EQU/LABEL(md) | `src/LO_GEN.mad:201`, `include/LO_GEN.labels.md:1251` | 56612B | 1 |
| `AC17OL` | EQU/LABEL(md) | `src/LO_GEN.mad:202`, `include/LO_GEN.labels.md:1252` | 56613B | 1 |
| `AC17OO` | EQU/LABEL(md) | `src/LO_GEN.mad:204`, `include/LO_GEN.labels.md:1254` | 56616B | 1 |
| `AC17OV` | EQU/LABEL(md) | `src/LO_GEN.mad:208`, `include/LO_GEN.labels.md:1258` | 56623B | 1 |
| `AC1I12` | EQU/LABEL(md) | `src/LO_GEN.mad:227`, `include/LO_GEN.labels.md:1277` | 70022B | 1 |
| `AC1I82` | EQU/LABEL(md) | `src/LO_GEN.mad:229`, `include/LO_GEN.labels.md:1279` | 70274B | 1 |
| `AC1LYB` | EQU/LABEL(md) | `src/LO_GEN.mad:237`, `include/LO_GEN.labels.md:1287` | 75107B | 1 |
| `AC1LYF` | EQU/LABEL(md) | `src/LO_GEN.mad:238`, `include/LO_GEN.labels.md:1288` | 75111B | 1 |
| `AC2254` | EQU/LABEL(md) | `src/LO_GEN.mad:107`, `include/LO_GEN.labels.md:1157` | 2254B | 1 |
| `AC5257` | EQU/LABEL(md) | `src/LO_GEN.mad:177`, `include/LO_GEN.labels.md:1227` | 5257B | 1 |
| `AC5377` | EQU/LABEL(md) | `src/LO_GEN.mad:180`, `include/LO_GEN.labels.md:1230` | 5377B | 1 |
| `ALL1` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:73`, `include/RUNTIME_DISASM.xref.md:96` | 77777B | 1 |
| `ALLMS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:27`, `include/FOREX.labels.md:219`, `include/FOREX.labels.md:376` | 77777B | 1 |
| `AOC4K` | EQU/LABEL(md) | `src/FOREX_CORE.mad:33`, `include/FOREX.labels.md:104`, `include/FOREX.labels.md:374` | 0o4000 | 1 |
| `AOC50` | EQU/LABEL(md) | `src/FOREX_CORE.mad:34`, `include/FOREX.labels.md:105`, `include/FOREX.labels.md:375` | 0o50 | 1 |
| `AP0000` | EQU/LABEL(md) | `src/LO_SYN.mad:664`, `include/LO_SYN.labels.md:412` | 2004B | 1 |
| `AP0111` | EQU/LABEL(md) | `src/LO_SYN.mad:580`, `include/LO_SYN.labels.md:405` | 20111B | 1 |
| `AP0314` | EQU/LABEL(md) | `src/LO_SYN.mad:597`, `include/LO_SYN.labels.md:407` | 314B | 1 |
| `AP0505` | EQU/LABEL(md) | `src/LO_SYN.mad:611`, `include/LO_SYN.labels.md:408` | 505B | 1 |
| `AP1111` | EQU/LABEL(md) | `src/LO_SYN.mad:632`, `include/LO_SYN.labels.md:409` | 1111B | 1 |
| `AP1314` | EQU/LABEL(md) | `src/LO_SYN.mad:648`, `include/LO_SYN.labels.md:410` | 1314B | 1 |
| `AP1501` | EQU/LABEL(md) | `src/LO_SYN.mad:328`, `include/LO_SYN.labels.md:379` | 41501B | 1 |
| `AP2003` | EQU/LABEL(md) | `src/LO_SYN.mad:663`, `include/LO_SYN.labels.md:411` | 2003B | 1 |
| `AP2010` | EQU/LABEL(md) | `src/LO_SYN.mad:253`, `include/LO_SYN.labels.md:369` | 20106B | 1 |
| `AP2011` | EQU/LABEL(md) | `src/LO_SYN.mad:389`, `include/LO_SYN.labels.md:384` | 20115B | 1 |
| `AP2016` | EQU/LABEL(md) | `src/LO_SYN.mad:86`, `include/LO_SYN.labels.md:358` | 20160B | 1 |
| `AP3001` | EQU/LABEL(md) | `src/LO_SYN.mad:669`, `include/LO_SYN.labels.md:413` | 3001B | 1 |
| `AP3031` | EQU/LABEL(md) | `src/LO_SYN.mad:71`, `include/LO_SYN.labels.md:356` | 30312B | 1 |
| `AP3101` | EQU/LABEL(md) | `src/LO_SYN.mad:675`, `include/LO_SYN.labels.md:414` | 3101B | 1 |
| `AP4011` | EQU/LABEL(md) | `src/LO_SYN.mad:689`, `include/LO_SYN.labels.md:415` | 4011B | 1 |
| `AP4022` | EQU/LABEL(md) | `src/LO_SYN.mad:699`, `include/LO_SYN.labels.md:416` | 4022B | 1 |
| `AP4056` | EQU/LABEL(md) | `src/LO_SYN.mad:331`, `include/LO_SYN.labels.md:380` | 40560B | 1 |
| `AP4101` | EQU/LABEL(md) | `src/LO_SYN.mad:557`, `include/LO_SYN.labels.md:400` | 44101B | 1 |
| `AP4110` | EQU/LABEL(md) | `src/LO_SYN.mad:391`, `include/LO_SYN.labels.md:385` | 41101B | 1 |
| `AP4155` | EQU/LABEL(md) | `src/LO_SYN.mad:439`, `include/LO_SYN.labels.md:392` | 41554B | 1 |
| `AP4201` | EQU/LABEL(md) | `src/LO_SYN.mad:728`, `include/LO_SYN.labels.md:417` | 4201B | 1 |
| `AP4305` | EQU/LABEL(md) | `src/LO_SYN.mad:570`, `include/LO_SYN.labels.md:403` | 43055B | 1 |
| `AP4416` | EQU/LABEL(md) | `src/LO_SYN.mad:755`, `include/LO_SYN.labels.md:418` | 4416B | 1 |
| `AP4550` | EQU/LABEL(md) | `src/LO_SYN.mad:498`, `include/LO_SYN.labels.md:395` | 45501B | 1 |
| `AP5211` | EQU/LABEL(md) | `src/LO_SYN.mad:307`, `include/LO_SYN.labels.md:374` | 52110B | 1 |
| `AP5404` | EQU/LABEL(md) | `src/LO_SYN.mad:550`, `include/LO_SYN.labels.md:398` | 54040B | 1 |
| `AP6144` | EQU/LABEL(md) | `src/LO_SYN.mad:336`, `include/LO_SYN.labels.md:381` | 61440B | 1 |
| `AP6501` | EQU/LABEL(md) | `src/LO_SYN.mad:321`, `include/LO_SYN.labels.md:378` | 46501B | 1 |
| `AP6616` | EQU/LABEL(md) | `src/LO_SYN.mad:531`, `include/LO_SYN.labels.md:397` | 66161B | 1 |
| `AP7010` | EQU/LABEL(md) | `src/LO_SYN.mad:448`, `include/LO_SYN.labels.md:393` | 70101B | 1 |
| `AP7044` | EQU/LABEL(md) | `src/LO_SYN.mad:569`, `include/LO_SYN.labels.md:402` | 70440B | 1 |
| `AP7310` | EQU/LABEL(md) | `src/LO_SYN.mad:214`, `include/LO_SYN.labels.md:367` | 73105B | 1 |
| `AP7550` | EQU/LABEL(md) | `src/LO_SYN.mad:584`, `include/LO_SYN.labels.md:406` | 75505B | 1 |
| `AP7710` | EQU/LABEL(md) | `src/LO_SYN.mad:574`, `include/LO_SYN.labels.md:404` | 77105B | 1 |
| `B` | LABEL(md) | `include/FOREX.labels.md:62`, `include/LO_SYN.labels.md:50` | — | 1 |
| `BS16A` | EQU/LABEL(md) | `src/FOREX_CORE.mad:36`, `include/FOREX.labels.md:107`, `include/FOREX.labels.md:378` | 74001B | 1 |
| `C` | LABEL(md) | `include/FOREX.labels.md:68`, `include/FOREX.labels.md:87` | — | 1 |
| `C066` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:376` | — | 1 |
| `C067` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:377` | — | 1 |
| `C073` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:381` | — | 1 |
| `C075` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:383` | — | 1 |
| `C10` | LABEL | `src/FOREX_RUNTIME.mad:513` | — | 1 |
| `C11200` | LABEL(md) | `include/FOREX.labels.md:111`, `include/FOREX.labels.md:383` | — | 1 |
| `C16617` | LABEL(md) | `include/FOREX.labels.md:115`, `include/FOREX.labels.md:387` | — | 1 |
| `C30453` | LABEL(md) | `include/FOREX.labels.md:117`, `include/FOREX.labels.md:389` | — | 1 |
| `C31056` | LABEL(md) | `include/FOREX.labels.md:118`, `include/FOREX.labels.md:390` | — | 1 |
| `C36464` | LABEL(md) | `include/FOREX.labels.md:119`, `include/FOREX.labels.md:391` | — | 1 |
| `C37013` | LABEL(md) | `include/FOREX.labels.md:120`, `include/FOREX.labels.md:392` | — | 1 |
| `C44000` | LABEL(md) | `include/FOREX.labels.md:137`, `include/FOREX.labels.md:409` | 0o044000 | 1 |
| `C44745` | LABEL(md) | `include/FOREX.labels.md:138`, `include/FOREX.labels.md:410` | 0o044745 | 1 |
| `C46555` | LABEL(md) | `include/FOREX.labels.md:140`, `include/FOREX.labels.md:412` | 0o046555 | 1 |
| `C55451` | LABEL(md) | `include/FOREX.labels.md:142`, `include/FOREX.labels.md:414` | 0o055451 | 1 |
| `C61200` | LABEL(md) | `include/FOREX.labels.md:144`, `include/FOREX.labels.md:416` | 0o061200 | 1 |
| `C70031` | LABEL(md) | `include/FOREX.labels.md:147`, `include/FOREX.labels.md:419` | 0o070031 | 1 |
| `C70035` | LABEL(md) | `include/FOREX.labels.md:148`, `include/FOREX.labels.md:420` | 0o070035 | 1 |
| `C70042` | LABEL(md) | `include/FOREX.labels.md:149`, `include/FOREX.labels.md:421` | 0o070042 | 1 |
| `C70043` | LABEL(md) | `include/FOREX.labels.md:150`, `include/FOREX.labels.md:422` | 0o070043 | 1 |
| `C70044` | LABEL(md) | `include/FOREX.labels.md:151`, `include/FOREX.labels.md:423` | 0o070044 | 1 |
| `C70045` | LABEL(md) | `include/FOREX.labels.md:152`, `include/FOREX.labels.md:424` | 0o070045 | 1 |
| `C70046` | LABEL(md) | `include/FOREX.labels.md:153`, `include/FOREX.labels.md:425` | 0o070046 | 1 |
| `C70047` | LABEL(md) | `include/FOREX.labels.md:154`, `include/FOREX.labels.md:426` | 0o070047 | 1 |
| `C70050` | LABEL(md) | `include/FOREX.labels.md:155`, `include/FOREX.labels.md:427` | 0o070050 | 1 |
| `C74757` | LABEL(md) | `include/FOREX.labels.md:157`, `include/FOREX.labels.md:429` | 0o074757 | 1 |
| `C75120` | LABEL(md) | `include/FOREX.labels.md:158`, `include/FOREX.labels.md:430` | 0o075120 | 1 |
| `C75451` | LABEL(md) | `include/FOREX.labels.md:159`, `include/FOREX.labels.md:431` | 0o075451 | 1 |
| `C75545` | LABEL(md) | `include/FOREX.labels.md:160`, `include/FOREX.labels.md:432` | 0o075545 | 1 |
| `C75663` | LABEL(md) | `include/FOREX.labels.md:161`, `include/FOREX.labels.md:433` | 0o075663 | 1 |
| `C76462` | LABEL(md) | `include/FOREX.labels.md:163`, `include/FOREX.labels.md:435` | 0o076462 | 1 |
| `CA1200` | LABEL(md) | `include/FOREX.labels.md:112`, `include/FOREX.labels.md:384` | — | 1 |
| `CA1247` | LABEL(md) | `include/FOREX.labels.md:113`, `include/FOREX.labels.md:385` | — | 1 |
| `CA1263` | LABEL(md) | `include/FOREX.labels.md:114`, `include/FOREX.labels.md:386` | — | 1 |
| `CA231` | LABEL(md) | `include/FOREX.labels.md:116`, `include/FOREX.labels.md:388` | — | 1 |
| `CA4040` | LABEL(md) | `include/FOREX.labels.md:121`, `include/FOREX.labels.md:393` | — | 1 |
| `CA4041` | LABEL(md) | `include/FOREX.labels.md:122`, `include/FOREX.labels.md:394` | — | 1 |
| `CA4042` | LABEL(md) | `include/FOREX.labels.md:123`, `include/FOREX.labels.md:395` | — | 1 |
| `CA4043` | LABEL(md) | `include/FOREX.labels.md:124`, `include/FOREX.labels.md:396` | — | 1 |
| `CA4044` | LABEL(md) | `include/FOREX.labels.md:125`, `include/FOREX.labels.md:397` | — | 1 |
| `CA4045` | LABEL(md) | `include/FOREX.labels.md:126`, `include/FOREX.labels.md:398` | — | 1 |
| `CA4046` | LABEL(md) | `include/FOREX.labels.md:127`, `include/FOREX.labels.md:399` | — | 1 |
| `CA4047` | LABEL(md) | `include/FOREX.labels.md:128`, `include/FOREX.labels.md:400` | — | 1 |
| `CA4050` | LABEL(md) | `include/FOREX.labels.md:129`, `include/FOREX.labels.md:401` | — | 1 |
| `CA4051` | LABEL(md) | `include/FOREX.labels.md:130`, `include/FOREX.labels.md:402` | — | 1 |
| `CA4052` | LABEL(md) | `include/FOREX.labels.md:131`, `include/FOREX.labels.md:403` | — | 1 |
| `CA4053` | LABEL(md) | `include/FOREX.labels.md:132`, `include/FOREX.labels.md:404` | — | 1 |
| `CA4054` | LABEL(md) | `include/FOREX.labels.md:133`, `include/FOREX.labels.md:405` | — | 1 |
| `CA4055` | LABEL(md) | `include/FOREX.labels.md:134`, `include/FOREX.labels.md:406` | — | 1 |
| `CA4056` | LABEL(md) | `include/FOREX.labels.md:135`, `include/FOREX.labels.md:407` | — | 1 |
| `CA4144` | LABEL(md) | `include/FOREX.labels.md:136`, `include/FOREX.labels.md:408` | — | 1 |
| `CA4543` | LABEL(md) | `include/FOREX.labels.md:139`, `include/FOREX.labels.md:411` | — | 1 |
| `CA5317` | LABEL(md) | `include/FOREX.labels.md:141`, `include/FOREX.labels.md:413` | — | 1 |
| `CA56` | LABEL(md) | `include/FOREX.labels.md:143`, `include/FOREX.labels.md:415` | — | 1 |
| `CA6264` | LABEL(md) | `include/FOREX.labels.md:145`, `include/FOREX.labels.md:417` | — | 1 |
| `CA6441` | LABEL(md) | `include/FOREX.labels.md:146`, `include/FOREX.labels.md:418` | — | 1 |
| `CA7017` | LABEL(md) | `include/FOREX.labels.md:156`, `include/FOREX.labels.md:428` | — | 1 |
| `CHECKF` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:66`, `include/FOREX.labels.md:381`, `include/FOREX.labels.md:697` | 1 | 1 |
| `CHKAD` | LABEL(md) | `include/FOREX.labels.md:110`, `include/FOREX.labels.md:382` | — | 1 |
| `CW002` | LABEL(md) | `include/FOREX.labels.md:166`, `include/FOREX.labels.md:438` | — | 1 |
| `CW004` | LABEL(md) | `include/FOREX.labels.md:167`, `include/FOREX.labels.md:439` | — | 1 |
| `CW005` | LABEL(md) | `include/FOREX.labels.md:168`, `include/FOREX.labels.md:440` | — | 1 |
| `D002DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:48`, `include/RUNTIME_DISASM.xref.md:34` | 77776B | 1 |
| `D003DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:49`, `include/RUNTIME_DISASM.xref.md:35` | 77775B | 1 |
| `D521DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:45`, `include/RUNTIME_DISASM.xref.md:31` | 77257B | 1 |
| `D531DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:42`, `include/RUNTIME_DISASM.xref.md:28` | 77247B | 1 |
| `D541DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:40`, `include/RUNTIME_DISASM.xref.md:26` | 77237B | 1 |
| `D561DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:43`, `include/RUNTIME_DISASM.xref.md:29` | 77217B | 1 |
| `D571DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:39`, `include/RUNTIME_DISASM.xref.md:25` | 77207B | 1 |
| `D611DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:41`, `include/RUNTIME_DISASM.xref.md:27` | 77167B | 1 |
| `D621DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:44`, `include/RUNTIME_DISASM.xref.md:30` | 77157B | 1 |
| `D641DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:47`, `include/RUNTIME_DISASM.xref.md:33` | 77137B | 1 |
| `D721DS` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:46`, `include/RUNTIME_DISASM.xref.md:32` | 77057B | 1 |
| `DATE0` | TEXT | `src/FOREX_RUNTIME.mad:406` | TL0019 | 1 |
| `DATE1` | TEXT | `src/FOREX_RUNTIME.mad:407` | TL0002 | 1 |
| `DATE2` | TEXT | `src/FOREX_RUNTIME.mad:411` | TL0007 | 1 |
| `DATE3` | TEXT | `src/FOREX_RUNTIME.mad:418` | TL0017 | 1 |
| `DATE4` | COMMON | `src/FOREX_RUNTIME.mad:412` | — | 1 |
| `DBFLN` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:108`, `include/FOREX.labels.md:300`, `include/FOREX.labels.md:451` | 2 | 1 |
| `DEC_38` | EQU/LABEL(md) | `src/FOREX_CORE.mad:99`, `include/FOREX.labels.md:170` | 38 | 1 |
| `DEC_43` | EQU/LABEL(md) | `src/FOREX_CORE.mad:100`, `include/FOREX.labels.md:171` | 43 | 1 |
| `DGET` | COMMON/ENTRY/LABEL(md) | `src/FOREX_RUNTIME.mad:341`, `src/FOREX_RUNTIME.mad:342`, `include/FOREX.labels.md:59`, `include/FOREX.labels.md:455` | — | 1 |
| `DMB07` | EQU/LABEL(md) | `src/FOREX_CORE.mad:101`, `include/FOREX.labels.md:172`, `include/FOREX.labels.md:468` | 40007B | 1 |
| `DMC04` | EQU/LABEL(md) | `src/FOREX_CORE.mad:102`, `include/FOREX.labels.md:173`, `include/FOREX.labels.md:469` | 4026B | 1 |
| `DMC05` | EQU/LABEL(md) | `src/FOREX_CORE.mad:103`, `include/FOREX.labels.md:174`, `include/FOREX.labels.md:470` | 4027B | 1 |
| `DMC06` | EQU/LABEL(md) | `src/FOREX_CORE.mad:104`, `include/FOREX.labels.md:175`, `include/FOREX.labels.md:471` | 4030B | 1 |
| `DP000` | COMMON | `src/FOREX_DECODER_DISASM.mad:149` | — | 1 |
| `DP003` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:160`, `include/RUNTIME_DECODER.xref.md:15` | — | 1 |
| `DP012` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:176`, `include/RUNTIME_DECODER.xref.md:16` | — | 1 |
| `DP023` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:197`, `include/RUNTIME_DECODER.xref.md:17` | — | 1 |
| `DP034` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:219`, `include/RUNTIME_DECODER.xref.md:19` | — | 1 |
| `DPARSE` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:348`, `include/FOREX.labels.md:60`, `include/FOREX.labels.md:458` | — | 1 |
| `DPRAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:98`, `include/FOREX.labels.md:169`, `include/FOREX.labels.md:441` | 74010B | 1 |
| `DPREPB` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:392`, `include/FOREX.labels.md:62`, `include/FOREX.labels.md:460` | — | 1 |
| `DPRNT` | NAME/XREF(md) | `src/FOREX_DECODER_DISASM.mad:143`, `include/RUNTIME_DECODER.xref.md:12` | — | 1 |
| `DPRTN` | LABEL/LABEL(md) | `src/FOREX_CORE.mad:222`, `include/FOREX_ROOT.mad:93`, `include/FOREX.labels.md:27`, `include/FOREX.labels.md:78`, `include/FOREX.labels.md:462` | — | 1 |
| `DTDAYS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:38`, `include/FOREX.labels.md:230`, `include/FOREX.labels.md:452` | 64+16 | 1 |
| `DTENDC` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:381`, `include/FOREX.labels.md:453` | — | 1 |
| `DTMOSH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:40`, `include/FOREX.labels.md:232`, `include/FOREX.labels.md:457` | 64+35 | 1 |
| `DTSTAD` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:403`, `include/FOREX.labels.md:463` | — | 1 |
| `DTTMSH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:41`, `include/FOREX.labels.md:233`, `include/FOREX.labels.md:464` | 64-22 | 1 |
| `DTWTCS` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:362`, `include/FOREX.labels.md:465` | — | 1 |
| `DW0000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:29`, `include/FOREX.labels.md:221`, `include/FOREX.labels.md:442` | 0000000000077777 | 1 |
| `DW0002` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:31`, `include/FOREX.labels.md:223`, `include/FOREX.labels.md:444` | 00000000 00000001 | 1 |
| `DW0003` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:32`, `include/FOREX.labels.md:224`, `include/FOREX.labels.md:445` | 00000000 00000002 | 1 |
| `DW0004` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:33`, `include/FOREX.labels.md:225`, `include/FOREX.labels.md:446` | 00000000 00001777 | 1 |
| `DW0005` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:34`, `include/FOREX.labels.md:226`, `include/FOREX.labels.md:447` | 00100000 00000000 | 1 |
| `DW0006` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:35`, `include/FOREX.labels.md:227`, `include/FOREX.labels.md:448` | 17 7777 7777 7777 | 1 |
| `DW0007` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:36`, `include/FOREX.labels.md:228`, `include/FOREX.labels.md:449` | 37777774 77777477 | 1 |
| `DW0008` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:37`, `include/FOREX.labels.md:229`, `include/FOREX.labels.md:450` | 77270707 00000000 | 1 |
| `DYMSK` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:419`, `include/FOREX.labels.md:467` | — | 1 |
| `ERRTRT` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:29`, `include/FOREX.labels.md:317`, `include/FOREX.labels.md:477` | 18H'200'0OШ | 1 |
| `EX0003` | EQU/LABEL(md) | `src/LO_SYN.mad:508`, `include/LO_SYN.labels.md:174` | 20110B | 1 |
| `EX0004` | EQU/LABEL(md) | `src/LO_SYN.mad:573`, `include/LO_SYN.labels.md:317` | 20110B | 1 |
| `EX0006` | EQU/LABEL(md) | `src/LO_SYN.mad:524`, `include/LO_SYN.labels.md:308` | 20102B | 1 |
| `EX0012` | EQU/LABEL(md) | `src/LO_SYN.mad:491`, `include/LO_SYN.labels.md:169` | 47515B | 1 |
| `EX0013` | EQU/LABEL(md) | `src/LO_SYN.mad:363`, `include/LO_SYN.labels.md:290` | 64520B | 1 |
| `EX0014` | EQU/LABEL(md) | `src/LO_SYN.mad:65`, `include/LO_SYN.labels.md:59` | 14B | 1 |
| `EX0015` | EQU/LABEL(md) | `src/LO_SYN.mad:510`, `include/LO_SYN.labels.md:175` | 47547B | 1 |
| `EX0016` | EQU/LABEL(md) | `src/LO_SYN.mad:404`, `include/LO_SYN.labels.md:295` | 62101B | 1 |
| `EX0020` | EQU/LABEL(md) | `src/LO_SYN.mad:494`, `include/LO_SYN.labels.md:305` | 45505B | 1 |
| `EX0022` | EQU/LABEL(md) | `src/LO_SYN.mad:720`, `include/LO_SYN.labels.md:340` | 4053B | 1 |
| `EX0023` | EQU/LABEL(md) | `src/LO_SYN.mad:719`, `include/LO_SYN.labels.md:339` | 4052B | 1 |
| `EX0024` | EQU/LABEL(md) | `src/LO_SYN.mad:554`, `include/LO_SYN.labels.md:315` | 74440B | 1 |
| `EX0040` | EQU/LABEL(md) | `src/LO_SYN.mad:334`, `include/LO_SYN.labels.md:122` | 40B | 1 |
| `EX0110` | EQU/LABEL(md) | `src/LO_SYN.mad:295`, `include/LO_SYN.labels.md:109` | 110B | 1 |
| `EX0111` | EQU/LABEL(md) | `src/LO_SYN.mad:435`, `include/LO_SYN.labels.md:299` | 20111B | 1 |
| `EX0115` | EQU/LABEL(md) | `src/LO_SYN.mad:463`, `include/LO_SYN.labels.md:164` | 115B | 1 |
| `EX0142` | EQU/LABEL(md) | `src/LO_SYN.mad:530`, `include/LO_SYN.labels.md:180` | 20142B | 1 |
| `EX0143` | EQU/LABEL(md) | `src/LO_SYN.mad:512`, `include/LO_SYN.labels.md:306` | 20143B | 1 |
| `EX0144` | EQU/LABEL(md) | `src/LO_SYN.mad:330`, `include/LO_SYN.labels.md:286` | 20144B | 1 |
| `EX0147` | EQU/LABEL(md) | `src/LO_SYN.mad:335`, `include/LO_SYN.labels.md:287` | 20147B | 1 |
| `EX0160` | EQU/LABEL(md) | `src/LO_SYN.mad:504`, `include/LO_SYN.labels.md:172` | 160B | 1 |
| `EX0274` | EQU/LABEL(md) | `src/LO_SYN.mad:55`, `include/LO_SYN.labels.md:58` | 274B | 1 |
| `EX0317` | EQU/LABEL(md) | `src/LO_SYN.mad:599`, `include/LO_SYN.labels.md:198` | 317B | 1 |
| `EX0323` | EQU/LABEL(md) | `src/LO_SYN.mad:601`, `include/LO_SYN.labels.md:199` | 323B | 1 |
| `EX0326` | EQU/LABEL(md) | `src/LO_SYN.mad:604`, `include/LO_SYN.labels.md:201` | 326B | 1 |
| `EX0501` | EQU/LABEL(md) | `src/LO_SYN.mad:607`, `include/LO_SYN.labels.md:202` | 501B | 1 |
| `EX0505` | EQU/LABEL(md) | `src/LO_SYN.mad:521`, `include/LO_SYN.labels.md:307` | 40505B | 1 |
| `EX0512` | EQU/LABEL(md) | `src/LO_SYN.mad:615`, `include/LO_SYN.labels.md:204` | 512B | 1 |
| `EX0514` | EQU/LABEL(md) | `src/LO_SYN.mad:617`, `include/LO_SYN.labels.md:205` | 514B | 1 |
| `EX0520` | EQU/LABEL(md) | `src/LO_SYN.mad:583`, `include/LO_SYN.labels.md:194` | 40520B | 1 |
| `EX1016` | EQU/LABEL(md) | `src/LO_SYN.mad:624`, `include/LO_SYN.labels.md:208` | 1016B | 1 |
| `EX1202` | EQU/LABEL(md) | `src/LO_SYN.mad:635`, `include/LO_SYN.labels.md:211` | 1202B | 1 |
| `EX1263` | EQU/LABEL(md) | `src/LO_SYN.mad:45`, `include/LO_SYN.labels.md:56` | 1263B | 1 |
| `EX1302` | EQU/LABEL(md) | `src/LO_SYN.mad:642`, `include/LO_SYN.labels.md:213` | 1302B | 1 |
| `EX1310` | EQU/LABEL(md) | `src/LO_SYN.mad:644`, `include/LO_SYN.labels.md:214` | 1310B | 1 |
| `EX1311` | EQU/LABEL(md) | `src/LO_SYN.mad:645`, `include/LO_SYN.labels.md:215` | 1311B | 1 |
| `EX1323` | EQU/LABEL(md) | `src/LO_SYN.mad:651`, `include/LO_SYN.labels.md:217` | 1323B | 1 |
| `EX1324` | EQU/LABEL(md) | `src/LO_SYN.mad:652`, `include/LO_SYN.labels.md:218` | 1324B | 1 |
| `EX1571` | EQU/LABEL(md) | `src/LO_SYN.mad:493`, `include/LO_SYN.labels.md:170` | 1571B | 1 |
| `EX2001` | EQU/LABEL(md) | `src/LO_SYN.mad:567`, `include/LO_SYN.labels.md:191` | 62101B | 1 |
| `EX2005` | EQU/LABEL(md) | `src/LO_SYN.mad:665`, `include/LO_SYN.labels.md:323` | 2005B | 1 |
| `EX2011` | EQU/LABEL(md) | `src/LO_SYN.mad:69`, `include/LO_SYN.labels.md:247` | 20116B | 1 |
| `EX2013` | EQU/LABEL(md) | `src/LO_SYN.mad:539`, `include/LO_SYN.labels.md:183` | 20113B | 1 |
| `EX2014` | EQU/LABEL(md) | `src/LO_SYN.mad:243`, `include/LO_SYN.labels.md:95` | 20142B | 1 |
| `EX2016` | EQU/LABEL(md) | `src/LO_SYN.mad:281`, `include/LO_SYN.labels.md:104` | 20160B | 1 |
| `EX2017` | EQU/LABEL(md) | `src/LO_SYN.mad:475`, `include/LO_SYN.labels.md:303` | 20173B | 1 |
| `EX2024` | EQU/LABEL(md) | `src/LO_SYN.mad:447`, `include/LO_SYN.labels.md:161` | 20124B | 1 |
| `EX2042` | EQU/LABEL(md) | `src/LO_SYN.mad:164`, `include/LO_SYN.labels.md:81` | 42546B | 1 |
| `EX2047` | EQU/LABEL(md) | `src/LO_SYN.mad:327`, `include/LO_SYN.labels.md:119` | 47505B | 1 |
| `EX2051` | EQU/LABEL(md) | `src/LO_SYN.mad:333`, `include/LO_SYN.labels.md:121` | 20151B | 1 |
| `EX2064` | EQU/LABEL(md) | `src/LO_SYN.mad:444`, `include/LO_SYN.labels.md:158` | 64566B | 1 |
| `EX2101` | EQU/LABEL(md) | `src/LO_SYN.mad:566`, `include/LO_SYN.labels.md:190` | 2101B | 1 |
| `EX2110` | EQU/LABEL(md) | `src/LO_SYN.mad:507`, `include/LO_SYN.labels.md:173` | 2110B | 1 |
| `EX2117` | EQU/LABEL(md) | `src/LO_SYN.mad:366`, `include/LO_SYN.labels.md:128` | 2117B | 1 |
| `EX2516` | EQU/LABEL(md) | `src/LO_SYN.mad:586`, `include/LO_SYN.labels.md:320` | 42516B | 1 |
| `EX2520` | EQU/LABEL(md) | `src/LO_SYN.mad:263`, `include/LO_SYN.labels.md:279` | 42520B | 1 |
| `EX3002` | EQU/LABEL(md) | `src/LO_SYN.mad:670`, `include/LO_SYN.labels.md:325` | 3002B | 1 |
| `EX3003` | EQU/LABEL(md) | `src/LO_SYN.mad:671`, `include/LO_SYN.labels.md:326` | 3003B | 1 |
| `EX3106` | EQU/LABEL(md) | `src/LO_SYN.mad:678`, `include/LO_SYN.labels.md:327` | 3106B | 1 |
| `EX3110` | EQU/LABEL(md) | `src/LO_SYN.mad:681`, `include/LO_SYN.labels.md:222` | 3110B | 1 |
| `EX3601` | EQU/LABEL(md) | `src/LO_SYN.mad:486`, `include/LO_SYN.labels.md:168` | 50101B | 1 |
| `EX3620` | EQU/LABEL(md) | `src/LO_SYN.mad:371`, `include/LO_SYN.labels.md:131` | 20102B | 1 |
| `EX3640` | EQU/LABEL(md) | `src/LO_SYN.mad:721`, `include/LO_SYN.labels.md:234` | 4054B | 1 |
| `EX3644` | EQU/LABEL(md) | `src/LO_SYN.mad:302`, `include/LO_SYN.labels.md:112` | 44040B | 1 |
| `EX3645` | EQU/LABEL(md) | `src/LO_SYN.mad:575`, `include/LO_SYN.labels.md:192` | 45517B | 1 |
| `EX3666` | EQU/LABEL(md) | `src/LO_SYN.mad:549`, `include/LO_SYN.labels.md:186` | 66110B | 1 |
| `EX4001` | EQU/LABEL(md) | `src/LO_SYN.mad:684`, `include/LO_SYN.labels.md:328` | 4001B | 1 |
| `EX4002` | EQU/LABEL(md) | `src/LO_SYN.mad:685`, `include/LO_SYN.labels.md:224` | 4002B | 1 |
| `EX4012` | EQU/LABEL(md) | `src/LO_SYN.mad:691`, `include/LO_SYN.labels.md:330` | 4012B | 1 |
| `EX4013` | EQU/LABEL(md) | `src/LO_SYN.mad:692`, `include/LO_SYN.labels.md:331` | 4013B | 1 |
| `EX4014` | EQU/LABEL(md) | `src/LO_SYN.mad:693`, `include/LO_SYN.labels.md:332` | 4014B | 1 |
| `EX4016` | EQU/LABEL(md) | `src/LO_SYN.mad:695`, `include/LO_SYN.labels.md:225` | 4016B | 1 |
| `EX4020` | EQU/LABEL(md) | `src/LO_SYN.mad:697`, `include/LO_SYN.labels.md:333` | 4020B | 1 |
| `EX4024` | EQU/LABEL(md) | `src/LO_SYN.mad:701`, `include/LO_SYN.labels.md:334` | 4024B | 1 |
| `EX4026` | EQU/LABEL(md) | `src/LO_SYN.mad:704`, `include/LO_SYN.labels.md:227` | 4026B | 1 |
| `EX4031` | EQU/LABEL(md) | `src/LO_SYN.mad:707`, `include/LO_SYN.labels.md:335` | 4031B | 1 |
| `EX4032` | EQU/LABEL(md) | `src/LO_SYN.mad:708`, `include/LO_SYN.labels.md:336` | 4032B | 1 |
| `EX4033` | EQU/LABEL(md) | `src/LO_SYN.mad:709`, `include/LO_SYN.labels.md:337` | 4033B | 1 |
| `EX4036` | EQU/LABEL(md) | `src/LO_SYN.mad:712`, `include/LO_SYN.labels.md:338` | 4036B | 1 |
| `EX4037` | EQU/LABEL(md) | `src/LO_SYN.mad:713`, `include/LO_SYN.labels.md:230` | 4037B | 1 |
| `EX4041` | EQU/LABEL(md) | `src/LO_SYN.mad:716`, `include/LO_SYN.labels.md:232` | 4041B | 1 |
| `EX4043` | EQU/LABEL(md) | `src/LO_SYN.mad:718`, `include/LO_SYN.labels.md:233` | 4043B | 1 |
| `EX4051` | EQU/LABEL(md) | `src/LO_SYN.mad:88`, `include/LO_SYN.labels.md:61` | 40513B | 1 |
| `EX4052` | EQU/LABEL(md) | `src/LO_SYN.mad:544`, `include/LO_SYN.labels.md:314` | 40520B | 1 |
| `EX4053` | EQU/LABEL(md) | `src/LO_SYN.mad:420`, `include/LO_SYN.labels.md:297` | 40530B | 1 |
| `EX4054` | EQU/LABEL(md) | `src/LO_SYN.mad:529`, `include/LO_SYN.labels.md:309` | 40547B | 1 |
| `EX4072` | EQU/LABEL(md) | `src/LO_SYN.mad:725`, `include/LO_SYN.labels.md:235` | 4072B | 1 |
| `EX4113` | EQU/LABEL(md) | `src/LO_SYN.mad:322`, `include/LO_SYN.labels.md:284` | 74113B | 1 |
| `EX4211` | EQU/LABEL(md) | `src/LO_SYN.mad:582`, `include/LO_SYN.labels.md:319` | 42111B | 1 |
| `EX4256` | EQU/LABEL(md) | `src/LO_SYN.mad:283`, `include/LO_SYN.labels.md:106` | 42560B | 1 |
| `EX4257` | EQU/LABEL(md) | `src/LO_SYN.mad:541`, `include/LO_SYN.labels.md:313` | 42575B | 1 |
| `EX4301` | EQU/LABEL(md) | `src/LO_SYN.mad:729`, `include/LO_SYN.labels.md:342` | 4301B | 1 |
| `EX4302` | EQU/LABEL(md) | `src/LO_SYN.mad:730`, `include/LO_SYN.labels.md:343` | 4302B | 1 |
| `EX4311` | EQU/LABEL(md) | `src/LO_SYN.mad:732`, `include/LO_SYN.labels.md:237` | 4311B | 1 |
| `EX4314` | EQU/LABEL(md) | `src/LO_SYN.mad:735`, `include/LO_SYN.labels.md:344` | 4314B | 1 |
| `EX4323` | EQU/LABEL(md) | `src/LO_SYN.mad:741`, `include/LO_SYN.labels.md:239` | 4323B | 1 |
| `EX4324` | EQU/LABEL(md) | `src/LO_SYN.mad:742`, `include/LO_SYN.labels.md:346` | 4324B | 1 |
| `EX4326` | EQU/LABEL(md) | `src/LO_SYN.mad:744`, `include/LO_SYN.labels.md:347` | 4326B | 1 |
| `EX4327` | EQU/LABEL(md) | `src/LO_SYN.mad:745`, `include/LO_SYN.labels.md:348` | 4327B | 1 |
| `EX4405` | EQU/LABEL(md) | `src/LO_SYN.mad:749`, `include/LO_SYN.labels.md:240` | 4405B | 1 |
| `EX4407` | EQU/LABEL(md) | `src/LO_SYN.mad:751`, `include/LO_SYN.labels.md:349` | 4407B | 1 |
| `EX4410` | EQU/LABEL(md) | `src/LO_SYN.mad:354`, `include/LO_SYN.labels.md:125` | 44101B | 1 |
| `EX4411` | EQU/LABEL(md) | `src/LO_SYN.mad:585`, `include/LO_SYN.labels.md:195` | 44117B | 1 |
| `EX4414` | EQU/LABEL(md) | `src/LO_SYN.mad:337`, `include/LO_SYN.labels.md:123` | 44144B | 1 |
| `EX4421` | EQU/LABEL(md) | `src/LO_SYN.mad:756`, `include/LO_SYN.labels.md:350` | 4421B | 1 |
| `EX4423` | EQU/LABEL(md) | `src/LO_SYN.mad:758`, `include/LO_SYN.labels.md:241` | 4423B | 1 |
| `EX4440` | EQU/LABEL(md) | `src/LO_SYN.mad:552`, `include/LO_SYN.labels.md:187` | 64440B | 1 |
| `EX4510` | EQU/LABEL(md) | `src/LO_SYN.mad:171`, `include/LO_SYN.labels.md:86` | 4510B | 1 |
| `EX4544` | EQU/LABEL(md) | `src/LO_SYN.mad:425`, `include/LO_SYN.labels.md:148` | 45440B | 1 |
| `EX4546` | EQU/LABEL(md) | `src/LO_SYN.mad:187`, `include/LO_SYN.labels.md:88` | 4546B | 1 |
| `EX4550` | EQU/LABEL(md) | `src/LO_SYN.mad:261`, `include/LO_SYN.labels.md:99` | 45501B | 1 |
| `EX4554` | EQU/LABEL(md) | `src/LO_SYN.mad:395`, `include/LO_SYN.labels.md:140` | 45543B | 1 |
| `EX4555` | EQU/LABEL(md) | `src/LO_SYN.mad:560`, `include/LO_SYN.labels.md:316` | 45551B | 1 |
| `EX4573` | EQU/LABEL(md) | `src/LO_SYN.mad:532`, `include/LO_SYN.labels.md:181` | 4573B | 1 |
| `EX4651` | EQU/LABEL(md) | `src/LO_SYN.mad:364`, `include/LO_SYN.labels.md:291` | 46517B | 1 |
| `EX4744` | EQU/LABEL(md) | `src/LO_SYN.mad:286`, `include/LO_SYN.labels.md:107` | 47440B | 1 |
| `EX5010` | EQU/LABEL(md) | `src/LO_SYN.mad:481`, `include/LO_SYN.labels.md:304` | 50101B | 1 |
| `EX5017` | EQU/LABEL(md) | `src/LO_SYN.mad:194`, `include/LO_SYN.labels.md:267` | 50171B | 1 |
| `EX5070` | EQU/LABEL(md) | `src/LO_SYN.mad:610`, `include/LO_SYN.labels.md:203` | 70504B | 1 |
| `EX5073` | EQU/LABEL(md) | `src/LO_SYN.mad:683`, `include/LO_SYN.labels.md:223` | 73111B | 1 |
| `EX5110` | EQU/LABEL(md) | `src/LO_SYN.mad:374`, `include/LO_SYN.labels.md:132` | 51105B | 1 |
| `EX5212` | EQU/LABEL(md) | `src/LO_SYN.mad:358`, `include/LO_SYN.labels.md:126` | 52120B | 1 |
| `EX5501` | EQU/LABEL(md) | `src/LO_SYN.mad:471`, `include/LO_SYN.labels.md:166` | 5501B | 1 |
| `EX6035` | EQU/LABEL(md) | `src/LO_SYN.mad:711`, `include/LO_SYN.labels.md:229` | 74035B | 1 |
| `EX6070` | EQU/LABEL(md) | `src/LO_SYN.mad:596`, `include/LO_SYN.labels.md:197` | 70313B | 1 |
| `EX6071` | EQU/LABEL(md) | `src/LO_SYN.mad:631`, `include/LO_SYN.labels.md:210` | 71105B | 1 |
| `EX6074` | EQU/LABEL(md) | `src/LO_SYN.mad:714`, `include/LO_SYN.labels.md:231` | 74040B | 1 |
| `EX6105` | EQU/LABEL(md) | `src/LO_SYN.mad:470`, `include/LO_SYN.labels.md:302` | 66105B | 1 |
| `EX6112` | EQU/LABEL(md) | `src/LO_SYN.mad:565`, `include/LO_SYN.labels.md:189` | 61120B | 1 |
| `EX6115` | EQU/LABEL(md) | `src/LO_SYN.mad:479`, `include/LO_SYN.labels.md:167` | 61154B | 1 |
| `EX6117` | EQU/LABEL(md) | `src/LO_SYN.mad:589`, `include/LO_SYN.labels.md:321` | 66117B | 1 |
| `EX6144` | EQU/LABEL(md) | `src/LO_SYN.mad:401`, `include/LO_SYN.labels.md:294` | 61440B | 1 |
| `EX6155` | EQU/LABEL(md) | `src/LO_SYN.mad:579`, `include/LO_SYN.labels.md:318` | 61551B | 1 |
| `EX6210` | EQU/LABEL(md) | `src/LO_SYN.mad:239`, `include/LO_SYN.labels.md:94` | 62101B | 1 |
| `EX6211` | EQU/LABEL(md) | `src/LO_SYN.mad:90`, `include/LO_SYN.labels.md:62` | 62117B | 1 |
| `EX6313` | EQU/LABEL(md) | `src/LO_SYN.mad:394`, `include/LO_SYN.labels.md:292` | 63131B | 1 |
| `EX6355` | EQU/LABEL(md) | `src/LO_SYN.mad:119`, `include/LO_SYN.labels.md:74` | 63551B | 1 |
| `EX6450` | EQU/LABEL(md) | `src/LO_SYN.mad:324`, `include/LO_SYN.labels.md:285` | 64503B | 1 |
| `EX6451` | EQU/LABEL(md) | `src/LO_SYN.mad:469`, `include/LO_SYN.labels.md:301` | 64510B | 1 |
| `EX6452` | EQU/LABEL(md) | `src/LO_SYN.mad:139`, `include/LO_SYN.labels.md:263` | 64524B | 1 |
| `EX6455` | EQU/LABEL(md) | `src/LO_SYN.mad:517`, `include/LO_SYN.labels.md:177` | 64551B | 1 |
| `EX6456` | EQU/LABEL(md) | `src/LO_SYN.mad:92`, `include/LO_SYN.labels.md:63` | 64561B | 1 |
| `EX6457` | EQU/LABEL(md) | `src/LO_SYN.mad:534`, `include/LO_SYN.labels.md:310` | 64576B | 1 |
| `EX6466` | EQU/LABEL(md) | `src/LO_SYN.mad:155`, `include/LO_SYN.labels.md:80` | 6466B | 1 |
| `EX6552` | EQU/LABEL(md) | `src/LO_SYN.mad:422`, `include/LO_SYN.labels.md:147` | 6552B | 1 |
| `EX6611` | EQU/LABEL(md) | `src/LO_SYN.mad:457`, `include/LO_SYN.labels.md:163` | 66117B | 1 |
| `EX6615` | EQU/LABEL(md) | `src/LO_SYN.mad:523`, `include/LO_SYN.labels.md:178` | 66151B | 1 |
| `EX7000` | EQU/LABEL(md) | `src/LO_SYN.mad:46`, `include/LO_SYN.labels.md:57` | 70000B | 1 |
| `EX7004` | EQU/LABEL(md) | `src/LO_SYN.mad:464`, `include/LO_SYN.labels.md:165` | 70040B | 1 |
| `EX7005` | EQU/LABEL(md) | `src/LO_SYN.mad:526`, `include/LO_SYN.labels.md:179` | 70055B | 1 |
| `EX7031` | EQU/LABEL(md) | `src/LO_SYN.mad:595`, `include/LO_SYN.labels.md:196` | 70312B | 1 |
| `EX7032` | EQU/LABEL(md) | `src/LO_SYN.mad:603`, `include/LO_SYN.labels.md:200` | 70325B | 1 |
| `EX7050` | EQU/LABEL(md) | `src/LO_SYN.mad:338`, `include/LO_SYN.labels.md:288` | 70505B | 1 |
| `EX7051` | EQU/LABEL(md) | `src/LO_SYN.mad:616`, `include/LO_SYN.labels.md:322` | 70513B | 1 |
| `EX7074` | EQU/LABEL(md) | `src/LO_SYN.mad:727`, `include/LO_SYN.labels.md:236` | 74075B | 1 |
| `EX7100` | EQU/LABEL(md) | `src/LO_SYN.mad:618`, `include/LO_SYN.labels.md:206` | 71000B | 1 |
| `EX7101` | EQU/LABEL(md) | `src/LO_SYN.mad:623`, `include/LO_SYN.labels.md:207` | 71015B | 1 |
| `EX7110` | EQU/LABEL(md) | `src/LO_SYN.mad:629`, `include/LO_SYN.labels.md:209` | 71101B | 1 |
| `EX7121` | EQU/LABEL(md) | `src/LO_SYN.mad:639`, `include/LO_SYN.labels.md:212` | 71215B | 1 |
| `EX7131` | EQU/LABEL(md) | `src/LO_SYN.mad:647`, `include/LO_SYN.labels.md:216` | 71313B | 1 |
| `EX7132` | EQU/LABEL(md) | `src/LO_SYN.mad:654`, `include/LO_SYN.labels.md:219` | 71326B | 1 |
| `EX7140` | EQU/LABEL(md) | `src/LO_SYN.mad:659`, `include/LO_SYN.labels.md:220` | 71405B | 1 |
| `EX7201` | EQU/LABEL(md) | `src/LO_SYN.mad:668`, `include/LO_SYN.labels.md:324` | 72011B | 1 |
| `EX7301` | EQU/LABEL(md) | `src/LO_SYN.mad:674`, `include/LO_SYN.labels.md:221` | 73010B | 1 |
| `EX7311` | EQU/LABEL(md) | `src/LO_SYN.mad:242`, `include/LO_SYN.labels.md:275` | 73110B | 1 |
| `EX7400` | EQU/LABEL(md) | `src/LO_SYN.mad:686`, `include/LO_SYN.labels.md:329` | 74003B | 1 |
| `EX7402` | EQU/LABEL(md) | `src/LO_SYN.mad:698`, `include/LO_SYN.labels.md:226` | 74021B | 1 |
| `EX7403` | EQU/LABEL(md) | `src/LO_SYN.mad:706`, `include/LO_SYN.labels.md:228` | 74030B | 1 |
| `EX7407` | EQU/LABEL(md) | `src/LO_SYN.mad:726`, `include/LO_SYN.labels.md:341` | 74073B | 1 |
| `EX7431` | EQU/LABEL(md) | `src/LO_SYN.mad:733`, `include/LO_SYN.labels.md:238` | 74312B | 1 |
| `EX7432` | EQU/LABEL(md) | `src/LO_SYN.mad:740`, `include/LO_SYN.labels.md:345` | 74322B | 1 |
| `EX7444` | EQU/LABEL(md) | `src/LO_SYN.mad:546`, `include/LO_SYN.labels.md:185` | 74440B | 1 |
| `EX7457` | EQU/LABEL(md) | `src/LO_SYN.mad:432`, `include/LO_SYN.labels.md:152` | 74576B | 1 |
| `EX7503` | EQU/LABEL(md) | `src/LO_SYN.mad:262`, `include/LO_SYN.labels.md:278` | 47503B | 1 |
| `EX7517` | EQU/LABEL(md) | `src/LO_SYN.mad:383`, `include/LO_SYN.labels.md:137` | 7517B | 1 |
| `EX7522` | EQU/LABEL(md) | `src/LO_SYN.mad:375`, `include/LO_SYN.labels.md:133` | 7522B | 1 |
| `EX7550` | EQU/LABEL(md) | `src/LO_SYN.mad:426`, `include/LO_SYN.labels.md:149` | 75505B | 1 |
| `EX7613` | EQU/LABEL(md) | `src/LO_SYN.mad:170`, `include/LO_SYN.labels.md:85` | 76131B | 1 |
| `EX7710` | EQU/LABEL(md) | `src/LO_SYN.mad:576`, `include/LO_SYN.labels.md:193` | 77101B | 1 |
| `F002DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:45`, `include/FOREX.labels.md:237`, `include/FOREX.labels.md:489` | 77776B | 1 |
| `F003DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:46`, `include/FOREX.labels.md:238`, `include/FOREX.labels.md:490` | 77775B | 1 |
| `F521DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:47`, `include/FOREX.labels.md:239`, `include/FOREX.labels.md:491` | 77257B | 1 |
| `F531DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:48`, `include/FOREX.labels.md:240`, `include/FOREX.labels.md:492` | 77247B | 1 |
| `F541DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:49`, `include/FOREX.labels.md:241`, `include/FOREX.labels.md:493` | 77237B | 1 |
| `F561DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:50`, `include/FOREX.labels.md:242`, `include/FOREX.labels.md:494` | 77217B | 1 |
| `F571DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:51`, `include/FOREX.labels.md:243`, `include/FOREX.labels.md:495` | 77207B | 1 |
| `F611DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:52`, `include/FOREX.labels.md:244`, `include/FOREX.labels.md:496` | 77167B | 1 |
| `F621DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:53`, `include/FOREX.labels.md:245`, `include/FOREX.labels.md:497` | 77157B | 1 |
| `F641DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:54`, `include/FOREX.labels.md:246`, `include/FOREX.labels.md:498` | 77137B | 1 |
| `F721AD` | EQU/LABEL(md) | `src/LO_GEN.mad:45`, `include/LO_GEN.labels.md:1095` | 77057B | 1 |
| `F721DS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:55`, `include/FOREX.labels.md:247`, `include/FOREX.labels.md:499` | 77057B | 1 |
| `FIXM2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:44`, `include/FOREX_ROOT.mad:30`, `include/FOREX.labels.md:236`, `include/FOREX.labels.md:318`, `include/FOREX.labels.md:479` | 2 | 1 |
| `FLAFT` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:215`, `include/FOREX.labels.md:48`, `include/FOREX.labels.md:481` | — | 1 |
| `FLALT` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:262`, `include/FOREX.labels.md:52`, `include/FOREX.labels.md:482` | — | 1 |
| `FLGAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:110`, `include/FOREX.labels.md:181`, `include/FOREX.labels.md:480` | 4002B | 1 |
| `FLWTC` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:254`, `include/FOREX.labels.md:51`, `include/FOREX.labels.md:484` | — | 1 |
| `FMRZB` | EQU/LABEL(md) | `src/FOREX_CORE.mad:111`, `include/FOREX.labels.md:182`, `include/FOREX.labels.md:485` | 4035B | 1 |
| `FMSBR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:112`, `include/FOREX.labels.md:183`, `include/FOREX.labels.md:486` | 4034B | 1 |
| `FMT004` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:152`, `include/RUNTIME_DISASM.xref.md:58` | — | 1 |
| `FMT005` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:153`, `include/RUNTIME_DISASM.xref.md:59` | — | 1 |
| `FMT010` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:159`, `include/RUNTIME_DISASM.xref.md:60` | — | 1 |
| `FMT012` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:163`, `include/RUNTIME_DISASM.xref.md:61` | — | 1 |
| `FT*002` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:131`, `include/RUNTIME_DISASM.xref.md:34` | — | 1 |
| `FT*003` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:132`, `include/RUNTIME_DISASM.xref.md:35` | — | 1 |
| `FT*521` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:128`, `include/RUNTIME_DISASM.xref.md:31` | — | 1 |
| `FT*531` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:125`, `include/RUNTIME_DISASM.xref.md:28` | — | 1 |
| `FT*541` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:123`, `include/RUNTIME_DISASM.xref.md:26` | — | 1 |
| `FT*561` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:126`, `include/RUNTIME_DISASM.xref.md:29` | — | 1 |
| `FT*571` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:122`, `include/RUNTIME_DISASM.xref.md:25` | — | 1 |
| `FT*611` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:124`, `include/RUNTIME_DISASM.xref.md:27` | — | 1 |
| `FT*621` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:127`, `include/RUNTIME_DISASM.xref.md:30` | — | 1 |
| `FT*641` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:130`, `include/RUNTIME_DISASM.xref.md:33` | — | 1 |
| `FT*721` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:129`, `include/RUNTIME_DISASM.xref.md:32` | — | 1 |
| `FTADFL` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:57`, `include/FOREX.labels.md:249`, `include/FOREX.labels.md:508` | 103B | 1 |
| `FTADR` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:34`, `include/RUNTIME_DISASM.xref.md:71` | 103B | 1 |
| `FTBTAB` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:36`, `include/RUNTIME_DISASM.xref.md:73` | 77766B | 1 |
| `FTDLOP` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:145`, `include/FOREX.labels.md:40`, `include/FOREX.labels.md:501` | — | 1 |
| `FTDOFS` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:152`, `include/FOREX.labels.md:41`, `include/FOREX.labels.md:502` | — | 1 |
| `FTDSTO` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:157`, `include/FOREX.labels.md:42`, `include/FOREX.labels.md:503` | — | 1 |
| `FTDTBA` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:56`, `include/FOREX.labels.md:248`, `include/FOREX.labels.md:506` | 77766B | 1 |
| `FTDTSB` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:143`, `include/FOREX.labels.md:39`, `include/FOREX.labels.md:505` | — | 1 |
| `FTLBFR` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:194`, `include/FOREX.labels.md:46`, `include/FOREX.labels.md:511` | — | 1 |
| `FTOFMK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:58`, `include/FOREX.labels.md:250`, `include/FOREX.labels.md:512` | 155B | 1 |
| `FTOFSM` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:35`, `include/RUNTIME_DISASM.xref.md:72` | 155B | 1 |
| `FULAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:113`, `include/FOREX.labels.md:184`, `include/FOREX.labels.md:514` | 4004B | 1 |
| `FUNDTM` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:107`, `include/FOREX.labels.md:299`, `include/FOREX.labels.md:515` | 67B | 1 |
| `GIV/PG` | SUBP | `src/LO_SYN.mad:30` | — | 1 |
| `GOSTBL` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:59`, `include/FOREX.labels.md:251`, `include/FOREX.labels.md:517` | 6H | 1 |
| `GOSTVR` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:32`, `include/FOREX.labels.md:320`, `include/FOREX.labels.md:518` | 6HBPEMЯ- | 1 |
| `GOSTYA` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:33`, `include/FOREX.labels.md:321`, `include/FOREX.labels.md:519` | 1H'231' | 1 |
| `GOST_V` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:31`, `include/FOREX.labels.md:319` | 1H'212' | 1 |
| `HDMARK` | EQU/LABEL(md) | `src/LO_GEN.mad:275`, `include/LO_GEN.labels.md:1293` | 0000000000200003 | 1 |
| `HDNMWD` | EQU/LABEL(md) | `src/LO_GEN.mad:276`, `include/LO_GEN.labels.md:1294` | 5457124745560000 | 1 |
| `IC033` | EQU/LABEL(md) | `src/FOREX_CORE.mad:116`, `include/FOREX.labels.md:187`, `include/FOREX.labels.md:522` | 33B | 1 |
| `IM150` | EQU/LABEL(md) | `src/FOREX_CORE.mad:117`, `include/FOREX.labels.md:188`, `include/FOREX.labels.md:524` | 1500B | 1 |
| `IM170` | EQU/LABEL(md) | `src/FOREX_CORE.mad:118`, `include/FOREX.labels.md:189`, `include/FOREX.labels.md:525` | 1700B | 1 |
| `INFAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:115`, `include/FOREX.labels.md:186`, `include/FOREX.labels.md:521` | 4036B | 1 |
| `INTZ` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:60`, `include/FOREX.labels.md:252`, `include/FOREX.labels.md:526` | 0 | 1 |
| `ISOCSH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:61`, `include/FOREX.labels.md:253`, `include/FOREX.labels.md:527` | 54B | 1 |
| `ISOHI` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:69`, `include/RUNTIME_DISASM.xref.md:92` | 10000000 00000000 | 1 |
| `ISOSHF` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:72`, `include/RUNTIME_DISASM.xref.md:95` | 54B | 1 |
| `JT0FIS` | EQU/LABEL(md) | `src/LO_GEN.mad:278`, `include/LO_GEN.labels.md:1330` | 20116B | 1 |
| `JT0FU1` | EQU/LABEL(md) | `src/LO_GEN.mad:279`, `include/LO_GEN.labels.md:1331` | 20521B | 1 |
| `JT0KEA` | EQU/LABEL(md) | `src/LO_GEN.mad:280`, `include/LO_GEN.labels.md:1332` | 26434B | 1 |
| `JT0NDY` | EQU/LABEL(md) | `src/LO_GEN.mad:281`, `include/LO_GEN.labels.md:1333` | 30310B | 1 |
| `JT0VOW` | EQU/LABEL(md) | `src/LO_GEN.mad:282`, `include/LO_GEN.labels.md:1334` | 41072B | 1 |
| `JT0VPS` | EQU/LABEL(md) | `src/LO_GEN.mad:283`, `include/LO_GEN.labels.md:1335` | 41104B | 1 |
| `JT0VU4` | EQU/LABEL(md) | `src/LO_GEN.mad:284`, `include/LO_GEN.labels.md:1336` | 41260B | 1 |
| `JT0VUF` | EQU/LABEL(md) | `src/LO_GEN.mad:285`, `include/LO_GEN.labels.md:1337` | 41271B | 1 |
| `JT0W2J` | EQU/LABEL(md) | `src/LO_GEN.mad:286`, `include/LO_GEN.labels.md:1338` | 41563B | 1 |
| `JT0W58` | EQU/LABEL(md) | `src/LO_GEN.mad:291`, `include/LO_GEN.labels.md:1343` | 41660B | 1 |
| `JT0W6I` | EQU/LABEL(md) | `src/LO_GEN.mad:292`, `include/LO_GEN.labels.md:1344` | 41706B | 1 |
| `JT0WG6` | EQU/LABEL(md) | `src/LO_GEN.mad:294`, `include/LO_GEN.labels.md:1346` | 42054B | 1 |
| `JT0WIA` | EQU/LABEL(md) | `src/LO_GEN.mad:296`, `include/LO_GEN.labels.md:1348` | 42130B | 1 |
| `JT0WID` | EQU/LABEL(md) | `src/LO_GEN.mad:297`, `include/LO_GEN.labels.md:1349` | 42133B | 1 |
| `JT0WIY` | EQU/LABEL(md) | `src/LO_GEN.mad:298`, `include/LO_GEN.labels.md:1350` | 42154B | 1 |
| `JT0WJE` | EQU/LABEL(md) | `src/LO_GEN.mad:299`, `include/LO_GEN.labels.md:1351` | 42170B | 1 |
| `JT0WNW` | EQU/LABEL(md) | `src/LO_GEN.mad:304`, `include/LO_GEN.labels.md:1356` | 42332B | 1 |
| `JT0WX3` | EQU/LABEL(md) | `src/LO_GEN.mad:309`, `include/LO_GEN.labels.md:1361` | 42663B | 1 |
| `JT0WZO` | EQU/LABEL(md) | `src/LO_GEN.mad:310`, `include/LO_GEN.labels.md:1362` | 42756B | 1 |
| `JT0XET` | EQU/LABEL(md) | `src/LO_GEN.mad:311`, `include/LO_GEN.labels.md:1363` | 43301B | 1 |
| `JT0XHM` | EQU/LABEL(md) | `src/LO_GEN.mad:312`, `include/LO_GEN.labels.md:1364` | 43402B | 1 |
| `JT0XJ8` | EQU/LABEL(md) | `src/LO_GEN.mad:313`, `include/LO_GEN.labels.md:1365` | 43460B | 1 |
| `JT0Y9H` | EQU/LABEL(md) | `src/LO_GEN.mad:315`, `include/LO_GEN.labels.md:1367` | 44405B | 1 |
| `JT10GL` | EQU/LABEL(md) | `src/LO_GEN.mad:318`, `include/LO_GEN.labels.md:1370` | 47253B | 1 |
| `JT12O2` | EQU/LABEL(md) | `src/LO_GEN.mad:319`, `include/LO_GEN.labels.md:1371` | 50114B | 1 |
| `JT155H` | EQU/LABEL(md) | `src/LO_GEN.mad:321`, `include/LO_GEN.labels.md:1373` | 53333B | 1 |
| `JT15PV` | EQU/LABEL(md) | `src/LO_GEN.mad:322`, `include/LO_GEN.labels.md:1374` | 54067B | 1 |
| `JT15WF` | EQU/LABEL(md) | `src/LO_GEN.mad:323`, `include/LO_GEN.labels.md:1375` | 54303B | 1 |
| `JT1864` | EQU/LABEL(md) | `src/LO_GEN.mad:324`, `include/LO_GEN.labels.md:1376` | 57244B | 1 |
| `JT18GG` | EQU/LABEL(md) | `src/LO_GEN.mad:327`, `include/LO_GEN.labels.md:1379` | 57616B | 1 |
| `JT1AAP` | EQU/LABEL(md) | `src/LO_GEN.mad:328`, `include/LO_GEN.labels.md:1380` | 60001B | 1 |
| `JT1AQA` | EQU/LABEL(md) | `src/LO_GEN.mad:330`, `include/LO_GEN.labels.md:1382` | 60562B | 1 |
| `JT1BA5` | EQU/LABEL(md) | `src/LO_GEN.mad:331`, `include/LO_GEN.labels.md:1383` | 61277B | 1 |
| `JT1CA2` | EQU/LABEL(md) | `src/LO_GEN.mad:335`, `include/LO_GEN.labels.md:1387` | 62570B | 1 |
| `JT1COS` | EQU/LABEL(md) | `src/LO_GEN.mad:337`, `include/LO_GEN.labels.md:1389` | 63100B | 1 |
| `JT1CSJ` | EQU/LABEL(md) | `src/LO_GEN.mad:338`, `include/LO_GEN.labels.md:1390` | 63235B | 1 |
| `JT1D1D` | EQU/LABEL(md) | `src/LO_GEN.mad:341`, `include/LO_GEN.labels.md:1393` | 63553B | 1 |
| `JT1D3O` | EQU/LABEL(md) | `src/LO_GEN.mad:343`, `include/LO_GEN.labels.md:1395` | 63636B | 1 |
| `JT1DM9` | EQU/LABEL(md) | `src/LO_GEN.mad:344`, `include/LO_GEN.labels.md:1396` | 64305B | 1 |
| `JT1E9S` | EQU/LABEL(md) | `src/LO_GEN.mad:345`, `include/LO_GEN.labels.md:1397` | 65152B | 1 |
| `JT1F24` | EQU/LABEL(md) | `src/LO_GEN.mad:346`, `include/LO_GEN.labels.md:1398` | 66172B | 1 |
| `JT1M4I` | EQU/LABEL(md) | `src/LO_GEN.mad:350`, `include/LO_GEN.labels.md:1402` | 75330B | 1 |
| `JT1M4N` | EQU/LABEL(md) | `src/LO_GEN.mad:351`, `include/LO_GEN.labels.md:1403` | 75335B | 1 |
| `JT1M4U` | EQU/LABEL(md) | `src/LO_GEN.mad:352`, `include/LO_GEN.labels.md:1404` | 75342B | 1 |
| `JT1M53` | EQU/LABEL(md) | `src/LO_GEN.mad:353`, `include/LO_GEN.labels.md:1405` | 75351B | 1 |
| `JT1M5C` | EQU/LABEL(md) | `src/LO_GEN.mad:354`, `include/LO_GEN.labels.md:1406` | 75360B | 1 |
| `JT1M6T` | EQU/LABEL(md) | `src/LO_GEN.mad:355`, `include/LO_GEN.labels.md:1407` | 75413B | 1 |
| `JT1M6V` | EQU/LABEL(md) | `src/LO_GEN.mad:356`, `include/LO_GEN.labels.md:1408` | 75415B | 1 |
| `JT1M70` | EQU/LABEL(md) | `src/LO_GEN.mad:357`, `include/LO_GEN.labels.md:1409` | 75420B | 1 |
| `JT1M73` | EQU/LABEL(md) | `src/LO_GEN.mad:358`, `include/LO_GEN.labels.md:1410` | 75423B | 1 |
| `JT1M7V` | EQU/LABEL(md) | `src/LO_GEN.mad:361`, `include/LO_GEN.labels.md:1413` | 75451B | 1 |
| `JT1M80` | EQU/LABEL(md) | `src/LO_GEN.mad:362`, `include/LO_GEN.labels.md:1414` | 75456B | 1 |
| `JT1M86` | EQU/LABEL(md) | `src/LO_GEN.mad:363`, `include/LO_GEN.labels.md:1415` | 75462B | 1 |
| `JT1M8F` | EQU/LABEL(md) | `src/LO_GEN.mad:364`, `include/LO_GEN.labels.md:1416` | 75471B | 1 |
| `JT1M8K` | EQU/LABEL(md) | `src/LO_GEN.mad:365`, `include/LO_GEN.labels.md:1417` | 75476B | 1 |
| `JT1M98` | EQU/LABEL(md) | `src/LO_GEN.mad:366`, `include/LO_GEN.labels.md:1418` | 75500B | 1 |
| `JT1M9E` | EQU/LABEL(md) | `src/LO_GEN.mad:367`, `include/LO_GEN.labels.md:1419` | 75506B | 1 |
| `JT1M9F` | EQU/LABEL(md) | `src/LO_GEN.mad:368`, `include/LO_GEN.labels.md:1420` | 75507B | 1 |
| `JT1M9O` | EQU/LABEL(md) | `src/LO_GEN.mad:369`, `include/LO_GEN.labels.md:1421` | 75516B | 1 |
| `JT1M9Y` | EQU/LABEL(md) | `src/LO_GEN.mad:371`, `include/LO_GEN.labels.md:1423` | 75526B | 1 |
| `JT1MAI` | EQU/LABEL(md) | `src/LO_GEN.mad:374`, `include/LO_GEN.labels.md:1426` | 75546B | 1 |
| `JT1MAJ` | EQU/LABEL(md) | `src/LO_GEN.mad:375`, `include/LO_GEN.labels.md:1427` | 75547B | 1 |
| `JT1MAN` | EQU/LABEL(md) | `src/LO_GEN.mad:376`, `include/LO_GEN.labels.md:1428` | 75551B | 1 |
| `JT1MAR` | EQU/LABEL(md) | `src/LO_GEN.mad:377`, `include/LO_GEN.labels.md:1429` | 75555B | 1 |
| `JT1MAT` | EQU/LABEL(md) | `src/LO_GEN.mad:378`, `include/LO_GEN.labels.md:1430` | 75557B | 1 |
| `JT1MB1` | EQU/LABEL(md) | `src/LO_GEN.mad:380`, `include/LO_GEN.labels.md:1432` | 75565B | 1 |
| `JT1MB3` | EQU/LABEL(md) | `src/LO_GEN.mad:381`, `include/LO_GEN.labels.md:1433` | 75567B | 1 |
| `JT1MB6` | EQU/LABEL(md) | `src/LO_GEN.mad:382`, `include/LO_GEN.labels.md:1434` | 75570B | 1 |
| `JT1MB9` | EQU/LABEL(md) | `src/LO_GEN.mad:383`, `include/LO_GEN.labels.md:1435` | 75573B | 1 |
| `JT1MBB` | EQU/LABEL(md) | `src/LO_GEN.mad:384`, `include/LO_GEN.labels.md:1436` | 75575B | 1 |
| `JT1MC1` | EQU/LABEL(md) | `src/LO_GEN.mad:385`, `include/LO_GEN.labels.md:1437` | 75601B | 1 |
| `JT1MC5` | EQU/LABEL(md) | `src/LO_GEN.mad:386`, `include/LO_GEN.labels.md:1438` | 75605B | 1 |
| `JT1MC6` | EQU/LABEL(md) | `src/LO_GEN.mad:387`, `include/LO_GEN.labels.md:1439` | 75606B | 1 |
| `JT1MOO` | EQU/LABEL(md) | `src/LO_GEN.mad:388`, `include/LO_GEN.labels.md:1440` | 76056B | 1 |
| `JT1MP7` | EQU/LABEL(md) | `src/LO_GEN.mad:389`, `include/LO_GEN.labels.md:1441` | 76075B | 1 |
| `JT1MPY` | EQU/LABEL(md) | `src/LO_GEN.mad:390`, `include/LO_GEN.labels.md:1442` | 76102B | 1 |
| `JT1MQ6` | EQU/LABEL(md) | `src/LO_GEN.mad:391`, `include/LO_GEN.labels.md:1443` | 76110B | 1 |
| `JT1MQ8` | EQU/LABEL(md) | `src/LO_GEN.mad:392`, `include/LO_GEN.labels.md:1444` | 76112B | 1 |
| `JT1MQH` | EQU/LABEL(md) | `src/LO_GEN.mad:393`, `include/LO_GEN.labels.md:1445` | 76121B | 1 |
| `JT1MQJ` | EQU/LABEL(md) | `src/LO_GEN.mad:394`, `include/LO_GEN.labels.md:1446` | 76123B | 1 |
| `JT1MQW` | EQU/LABEL(md) | `src/LO_GEN.mad:396`, `include/LO_GEN.labels.md:1448` | 76136B | 1 |
| `JT1MR0` | EQU/LABEL(md) | `src/LO_GEN.mad:397`, `include/LO_GEN.labels.md:1449` | 76140B | 1 |
| `JT1MR4` | EQU/LABEL(md) | `src/LO_GEN.mad:398`, `include/LO_GEN.labels.md:1450` | 76144B | 1 |
| `JT1MR6` | EQU/LABEL(md) | `src/LO_GEN.mad:399`, `include/LO_GEN.labels.md:1451` | 76146B | 1 |
| `JT1MRC` | EQU/LABEL(md) | `src/LO_GEN.mad:400`, `include/LO_GEN.labels.md:1452` | 76152B | 1 |
| `JT1MRE` | EQU/LABEL(md) | `src/LO_GEN.mad:401`, `include/LO_GEN.labels.md:1453` | 76154B | 1 |
| `JT1MRK` | EQU/LABEL(md) | `src/LO_GEN.mad:402`, `include/LO_GEN.labels.md:1454` | 76160B | 1 |
| `JT1MRO` | EQU/LABEL(md) | `src/LO_GEN.mad:403`, `include/LO_GEN.labels.md:1455` | 76164B | 1 |
| `JT1MRQ` | EQU/LABEL(md) | `src/LO_GEN.mad:404`, `include/LO_GEN.labels.md:1456` | 76166B | 1 |
| `JT1MSS` | EQU/LABEL(md) | `src/LO_GEN.mad:405`, `include/LO_GEN.labels.md:1457` | 76204B | 1 |
| `JT1MTJ` | EQU/LABEL(md) | `src/LO_GEN.mad:406`, `include/LO_GEN.labels.md:1458` | 76231B | 1 |
| `JT1MVK` | EQU/LABEL(md) | `src/LO_GEN.mad:407`, `include/LO_GEN.labels.md:1459` | 76304B | 1 |
| `JT1MVU` | EQU/LABEL(md) | `src/LO_GEN.mad:408`, `include/LO_GEN.labels.md:1460` | 76314B | 1 |
| `JT1MW4` | EQU/LABEL(md) | `src/LO_GEN.mad:409`, `include/LO_GEN.labels.md:1461` | 76324B | 1 |
| `JT1MWF` | EQU/LABEL(md) | `src/LO_GEN.mad:412`, `include/LO_GEN.labels.md:1464` | 76335B | 1 |
| `JT1MX5` | EQU/LABEL(md) | `src/LO_GEN.mad:415`, `include/LO_GEN.labels.md:1467` | 76361B | 1 |
| `JT1MX7` | EQU/LABEL(md) | `src/LO_GEN.mad:416`, `include/LO_GEN.labels.md:1468` | 76363B | 1 |
| `JT1MX8` | EQU/LABEL(md) | `src/LO_GEN.mad:417`, `include/LO_GEN.labels.md:1469` | 76364B | 1 |
| `JT1MX9` | EQU/LABEL(md) | `src/LO_GEN.mad:418`, `include/LO_GEN.labels.md:1470` | 76365B | 1 |
| `JT1MXI` | EQU/LABEL(md) | `src/LO_GEN.mad:419`, `include/LO_GEN.labels.md:1471` | 76374B | 1 |
| `JT1MXJ` | EQU/LABEL(md) | `src/LO_GEN.mad:420`, `include/LO_GEN.labels.md:1472` | 76375B | 1 |
| `JT1MXK` | EQU/LABEL(md) | `src/LO_GEN.mad:421`, `include/LO_GEN.labels.md:1473` | 76376B | 1 |
| `JT1MYA` | EQU/LABEL(md) | `src/LO_GEN.mad:422`, `include/LO_GEN.labels.md:1474` | 76402B | 1 |
| `JT1MYC` | EQU/LABEL(md) | `src/LO_GEN.mad:423`, `include/LO_GEN.labels.md:1475` | 76404B | 1 |
| `JT1MYE` | EQU/LABEL(md) | `src/LO_GEN.mad:424`, `include/LO_GEN.labels.md:1476` | 76406B | 1 |
| `JT1MYJ` | EQU/LABEL(md) | `src/LO_GEN.mad:425`, `include/LO_GEN.labels.md:1477` | 76411B | 1 |
| `JT1MYL` | EQU/LABEL(md) | `src/LO_GEN.mad:426`, `include/LO_GEN.labels.md:1478` | 76413B | 1 |
| `JT1MYO` | EQU/LABEL(md) | `src/LO_GEN.mad:427`, `include/LO_GEN.labels.md:1479` | 76416B | 1 |
| `JT1MYP` | EQU/LABEL(md) | `src/LO_GEN.mad:428`, `include/LO_GEN.labels.md:1480` | 76417B | 1 |
| `JT1MYU` | EQU/LABEL(md) | `src/LO_GEN.mad:429`, `include/LO_GEN.labels.md:1481` | 76422B | 1 |
| `JT1MYW` | EQU/LABEL(md) | `src/LO_GEN.mad:430`, `include/LO_GEN.labels.md:1482` | 76424B | 1 |
| `JT1MYX` | EQU/LABEL(md) | `src/LO_GEN.mad:431`, `include/LO_GEN.labels.md:1483` | 76425B | 1 |
| `JT1MYZ` | EQU/LABEL(md) | `src/LO_GEN.mad:432`, `include/LO_GEN.labels.md:1484` | 76427B | 1 |
| `JT1MZ3` | EQU/LABEL(md) | `src/LO_GEN.mad:433`, `include/LO_GEN.labels.md:1485` | 76431B | 1 |
| `JT1MZH` | EQU/LABEL(md) | `src/LO_GEN.mad:434`, `include/LO_GEN.labels.md:1486` | 76445B | 1 |
| `JT1MZJ` | EQU/LABEL(md) | `src/LO_GEN.mad:435`, `include/LO_GEN.labels.md:1487` | 76447B | 1 |
| `JT1MZN` | EQU/LABEL(md) | `src/LO_GEN.mad:436`, `include/LO_GEN.labels.md:1488` | 76451B | 1 |
| `JT1N01` | EQU/LABEL(md) | `src/LO_GEN.mad:438`, `include/LO_GEN.labels.md:1490` | 76465B | 1 |
| `JT1N06` | EQU/LABEL(md) | `src/LO_GEN.mad:439`, `include/LO_GEN.labels.md:1491` | 76470B | 1 |
| `JT1N0B` | EQU/LABEL(md) | `src/LO_GEN.mad:440`, `include/LO_GEN.labels.md:1492` | 76475B | 1 |
| `JT1N10` | EQU/LABEL(md) | `src/LO_GEN.mad:441`, `include/LO_GEN.labels.md:1493` | 76500B | 1 |
| `JT1N14` | EQU/LABEL(md) | `src/LO_GEN.mad:443`, `include/LO_GEN.labels.md:1495` | 76504B | 1 |
| `JT1N1B` | EQU/LABEL(md) | `src/LO_GEN.mad:444`, `include/LO_GEN.labels.md:1496` | 76511B | 1 |
| `JT1N1E` | EQU/LABEL(md) | `src/LO_GEN.mad:445`, `include/LO_GEN.labels.md:1497` | 76514B | 1 |
| `JT1N1Y` | EQU/LABEL(md) | `src/LO_GEN.mad:447`, `include/LO_GEN.labels.md:1499` | 76534B | 1 |
| `JT1N2L` | EQU/LABEL(md) | `src/LO_GEN.mad:449`, `include/LO_GEN.labels.md:1501` | 76557B | 1 |
| `JT1N2P` | EQU/LABEL(md) | `src/LO_GEN.mad:450`, `include/LO_GEN.labels.md:1502` | 76561B | 1 |
| `JT1N31` | EQU/LABEL(md) | `src/LO_GEN.mad:455`, `include/LO_GEN.labels.md:1507` | 76573B | 1 |
| `JT1N33` | EQU/LABEL(md) | `src/LO_GEN.mad:456`, `include/LO_GEN.labels.md:1508` | 76575B | 1 |
| `JT1N35` | EQU/LABEL(md) | `src/LO_GEN.mad:457`, `include/LO_GEN.labels.md:1509` | 76577B | 1 |
| `JT1N44` | EQU/LABEL(md) | `src/LO_GEN.mad:458`, `include/LO_GEN.labels.md:1510` | 76612B | 1 |
| `JT1N57` | EQU/LABEL(md) | `src/LO_GEN.mad:459`, `include/LO_GEN.labels.md:1511` | 76651B | 1 |
| `JT1N5G` | EQU/LABEL(md) | `src/LO_GEN.mad:460`, `include/LO_GEN.labels.md:1512` | 76660B | 1 |
| `JT1N5J` | EQU/LABEL(md) | `src/LO_GEN.mad:461`, `include/LO_GEN.labels.md:1513` | 76663B | 1 |
| `JT1N88` | EQU/LABEL(md) | `src/LO_GEN.mad:464`, `include/LO_GEN.labels.md:1516` | 76760B | 1 |
| `JT1N89` | EQU/LABEL(md) | `src/LO_GEN.mad:465`, `include/LO_GEN.labels.md:1517` | 76761B | 1 |
| `JT1NFK` | EQU/LABEL(md) | `src/LO_GEN.mad:466`, `include/LO_GEN.labels.md:1518` | 77024B | 1 |
| `JT1NG3` | EQU/LABEL(md) | `src/LO_GEN.mad:467`, `include/LO_GEN.labels.md:1519` | 77043B | 1 |
| `JT1NGC` | EQU/LABEL(md) | `src/LO_GEN.mad:468`, `include/LO_GEN.labels.md:1520` | 77052B | 1 |
| `JT1NGV` | EQU/LABEL(md) | `src/LO_GEN.mad:470`, `include/LO_GEN.labels.md:1522` | 77071B | 1 |
| `JT1NGY` | EQU/LABEL(md) | `src/LO_GEN.mad:471`, `include/LO_GEN.labels.md:1523` | 77074B | 1 |
| `JT1NH0` | EQU/LABEL(md) | `src/LO_GEN.mad:472`, `include/LO_GEN.labels.md:1524` | 77076B | 1 |
| `JT1NHR` | EQU/LABEL(md) | `src/LO_GEN.mad:475`, `include/LO_GEN.labels.md:1527` | 77103B | 1 |
| `JT1NHS` | EQU/LABEL(md) | `src/LO_GEN.mad:476`, `include/LO_GEN.labels.md:1528` | 77104B | 1 |
| `JT1NHZ` | EQU/LABEL(md) | `src/LO_GEN.mad:477`, `include/LO_GEN.labels.md:1529` | 77111B | 1 |
| `JT1NI1` | EQU/LABEL(md) | `src/LO_GEN.mad:478`, `include/LO_GEN.labels.md:1530` | 77113B | 1 |
| `JT1NI3` | EQU/LABEL(md) | `src/LO_GEN.mad:480`, `include/LO_GEN.labels.md:1532` | 77115B | 1 |
| `JT1NI8` | EQU/LABEL(md) | `src/LO_GEN.mad:481`, `include/LO_GEN.labels.md:1533` | 77120B | 1 |
| `JT1NI9` | EQU/LABEL(md) | `src/LO_GEN.mad:482`, `include/LO_GEN.labels.md:1534` | 77121B | 1 |
| `JT1NIA` | EQU/LABEL(md) | `src/LO_GEN.mad:483`, `include/LO_GEN.labels.md:1535` | 77122B | 1 |
| `JT1NID` | EQU/LABEL(md) | `src/LO_GEN.mad:485`, `include/LO_GEN.labels.md:1537` | 77125B | 1 |
| `JT1NIE` | EQU/LABEL(md) | `src/LO_GEN.mad:486`, `include/LO_GEN.labels.md:1538` | 77126B | 1 |
| `JT1NIF` | EQU/LABEL(md) | `src/LO_GEN.mad:487`, `include/LO_GEN.labels.md:1539` | 77127B | 1 |
| `JT1NL4` | EQU/LABEL(md) | `src/LO_GEN.mad:490`, `include/LO_GEN.labels.md:1542` | 77224B | 1 |
| `JT1NL7` | EQU/LABEL(md) | `src/LO_GEN.mad:491`, `include/LO_GEN.labels.md:1543` | 77227B | 1 |
| `JT1NLM` | EQU/LABEL(md) | `src/LO_GEN.mad:492`, `include/LO_GEN.labels.md:1544` | 77242B | 1 |
| `LGTAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:120`, `include/FOREX.labels.md:191`, `include/FOREX.labels.md:541` | 4032B | 1 |
| `LIBA10` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:288`, `include/RUNTIME_DISASM.xref.md:77` | — | 1 |
| `LIBA14` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:296`, `include/RUNTIME_DISASM.xref.md:76` | — | 1 |
| `LIBA23` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:310`, `include/RUNTIME_DISASM.xref.md:78` | — | 1 |
| `LIBA32` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:324`, `include/RUNTIME_DISASM.xref.md:80` | — | 1 |
| `LIBA36` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:332`, `include/RUNTIME_DISASM.xref.md:81` | — | 1 |
| `LIBA42` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:340`, `include/RUNTIME_DISASM.xref.md:82` | — | 1 |
| `LIBA50` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:352`, `include/RUNTIME_DISASM.xref.md:84` | — | 1 |
| `LIBA53` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:358`, `include/RUNTIME_DISASM.xref.md:85` | — | 1 |
| `LIBBLN` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:63`, `include/FOREX.labels.md:255`, `include/FOREX.labels.md:536` | 2000B | 1 |
| `LIBENT` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:272`, `include/RUNTIME_DISASM.xref.md:75` | — | 1 |
| `LIT10M` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:65`, `include/FOREX.labels.md:257`, `include/FOREX.labels.md:538` | 10000000 00000000 | 1 |
| `LIT_10` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:64`, `include/FOREX.labels.md:256` | 10 | 1 |
| `LIT_2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:66`, `include/FOREX.labels.md:258` | 2 | 1 |
| `LIT_3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:67`, `include/FOREX.labels.md:259` | 3 | 1 |
| `LO*GEN` | LABEL(md)/NAME | `src/LO_GEN.mad:18`, `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704`, `include/LO_GEN.labels.md:31` | NEW DTRAN | 1 |
| `LO*SYN` | LABEL(md)/NAME | `src/LO_SYN.mad:19`, `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | NEW DTRAN | 1 |
| `LSTAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:121`, `include/FOREX.labels.md:192`, `include/FOREX.labels.md:542` | 4031B | 1 |
| `M1777` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:68`, `include/RUNTIME_DISASM.xref.md:91` | 1777B | 1 |
| `ME0002` | EQU/LABEL(md) | `src/LO_SYN.mad:355`, `include/LO_SYN.labels.md:713` | 72117B | 1 |
| `ME0003` | EQU/LABEL(md) | `src/LO_SYN.mad:73`, `include/LO_SYN.labels.md:602` | 3B | 1 |
| `ME0004` | EQU/LABEL(md) | `src/LO_SYN.mad:561`, `include/LO_SYN.labels.md:783` | 7544B | 1 |
| `ME0006` | EQU/LABEL(md) | `src/LO_SYN.mad:304`, `include/LO_SYN.labels.md:700` | 70102B | 1 |
| `ME0007` | EQU/LABEL(md) | `src/LO_SYN.mad:502`, `include/LO_SYN.labels.md:765` | 70101B | 1 |
| `ME0011` | EQU/LABEL(md) | `src/LO_SYN.mad:400`, `include/LO_SYN.labels.md:728` | 74510B | 1 |
| `ME0012` | EQU/LABEL(md) | `src/LO_SYN.mad:468`, `include/LO_SYN.labels.md:751` | 75501B | 1 |
| `ME0013` | EQU/LABEL(md) | `src/LO_SYN.mad:61`, `include/LO_SYN.labels.md:597` | 13B | 1 |
| `ME0014` | EQU/LABEL(md) | `src/LO_SYN.mad:63`, `include/LO_SYN.labels.md:599` | 14B | 1 |
| `ME0015` | EQU/LABEL(md) | `src/LO_SYN.mad:545`, `include/LO_SYN.labels.md:777` | 70144B | 1 |
| `ME0016` | EQU/LABEL(md) | `src/LO_SYN.mad:587`, `include/LO_SYN.labels.md:788` | 74506B | 1 |
| `ME0017` | EQU/LABEL(md) | `src/LO_SYN.mad:70`, `include/LO_SYN.labels.md:600` | 17B | 1 |
| `ME0020` | EQU/LABEL(md) | `src/LO_SYN.mad:515`, `include/LO_SYN.labels.md:770` | 74117B | 1 |
| `ME0021` | EQU/LABEL(md) | `src/LO_SYN.mad:572`, `include/LO_SYN.labels.md:786` | 74105B | 1 |
| `ME0055` | EQU/LABEL(md) | `src/LO_SYN.mad:553`, `include/LO_SYN.labels.md:779` | 55B | 1 |
| `ME0104` | EQU/LABEL(md) | `src/LO_SYN.mad:62`, `include/LO_SYN.labels.md:598` | 104B | 1 |
| `ME0144` | EQU/LABEL(md) | `src/LO_SYN.mad:511`, `include/LO_SYN.labels.md:769` | 144B | 1 |
| `ME0264` | EQU/LABEL(md) | `src/LO_SYN.mad:50`, `include/LO_SYN.labels.md:593` | 264B | 1 |
| `ME0400` | EQU/LABEL(md) | `src/LO_SYN.mad:54`, `include/LO_SYN.labels.md:596` | 400B | 1 |
| `ME0502` | EQU/LABEL(md) | `src/LO_SYN.mad:284`, `include/LO_SYN.labels.md:693` | 502B | 1 |
| `ME0503` | EQU/LABEL(md) | `src/LO_SYN.mad:362`, `include/LO_SYN.labels.md:718` | 503B | 1 |
| `ME0515` | EQU/LABEL(md) | `src/LO_SYN.mad:246`, `include/LO_SYN.labels.md:676` | 515B | 1 |
| `ME0543` | EQU/LABEL(md) | `src/LO_SYN.mad:405`, `include/LO_SYN.labels.md:731` | 543B | 1 |
| `ME0554` | EQU/LABEL(md) | `src/LO_SYN.mad:305`, `include/LO_SYN.labels.md:701` | 554B | 1 |
| `ME1101` | EQU/LABEL(md) | `src/LO_SYN.mad:563`, `include/LO_SYN.labels.md:784` | 1101B | 1 |
| `ME1105` | EQU/LABEL(md) | `src/LO_SYN.mad:451`, `include/LO_SYN.labels.md:742` | 1105B | 1 |
| `ME1111` | EQU/LABEL(md) | `src/LO_SYN.mad:558`, `include/LO_SYN.labels.md:782` | 1111B | 1 |
| `ME1124` | EQU/LABEL(md) | `src/LO_SYN.mad:485`, `include/LO_SYN.labels.md:759` | 1124B | 1 |
| `ME1130` | EQU/LABEL(md) | `src/LO_SYN.mad:238`, `include/LO_SYN.labels.md:673` | 1130B | 1 |
| `ME1200` | EQU/LABEL(md) | `src/LO_SYN.mad:634`, `include/LO_SYN.labels.md:793` | 1200B | 1 |
| `ME1401` | EQU/LABEL(md) | `src/LO_SYN.mad:655`, `include/LO_SYN.labels.md:795` | 1401B | 1 |
| `ME1455` | EQU/LABEL(md) | `src/LO_SYN.mad:427`, `include/LO_SYN.labels.md:736` | 1455B | 1 |
| `ME1503` | EQU/LABEL(md) | `src/LO_SYN.mad:390`, `include/LO_SYN.labels.md:725` | 1503B | 1 |
| `ME2000` | EQU/LABEL(md) | `src/LO_SYN.mad:72`, `include/LO_SYN.labels.md:601` | 2000B | 1 |
| `ME2113` | EQU/LABEL(md) | `src/LO_SYN.mad:310`, `include/LO_SYN.labels.md:703` | 2113B | 1 |
| `ME2120` | EQU/LABEL(md) | `src/LO_SYN.mad:480`, `include/LO_SYN.labels.md:756` | 2120B | 1 |
| `ME2154` | EQU/LABEL(md) | `src/LO_SYN.mad:556`, `include/LO_SYN.labels.md:781` | 2154B | 1 |
| `ME2377` | EQU/LABEL(md) | `src/LO_SYN.mad:53`, `include/LO_SYN.labels.md:595` | 2377B | 1 |
| `ME2513` | EQU/LABEL(md) | `src/LO_SYN.mad:543`, `include/LO_SYN.labels.md:776` | 72513B | 1 |
| `ME2576` | EQU/LABEL(md) | `src/LO_SYN.mad:548`, `include/LO_SYN.labels.md:778` | 2576B | 1 |
| `ME3000` | EQU/LABEL(md) | `src/LO_SYN.mad:52`, `include/LO_SYN.labels.md:594` | 3000B | 1 |
| `ME3005` | EQU/LABEL(md) | `src/LO_SYN.mad:672`, `include/LO_SYN.labels.md:796` | 3005B | 1 |
| `ME3054` | EQU/LABEL(md) | `src/LO_SYN.mad:473`, `include/LO_SYN.labels.md:753` | 3054B | 1 |
| `ME3055` | EQU/LABEL(md) | `src/LO_SYN.mad:176`, `include/LO_SYN.labels.md:640` | 3055B | 1 |
| `ME3107` | EQU/LABEL(md) | `src/LO_SYN.mad:680`, `include/LO_SYN.labels.md:798` | 3107B | 1 |
| `ME3440` | EQU/LABEL(md) | `src/LO_SYN.mad:476`, `include/LO_SYN.labels.md:755` | 3440B | 1 |
| `ME4040` | EQU/LABEL(md) | `src/LO_SYN.mad:288`, `include/LO_SYN.labels.md:694` | 4040B | 1 |
| `ME4101` | EQU/LABEL(md) | `src/LO_SYN.mad:495`, `include/LO_SYN.labels.md:762` | 4101B | 1 |
| `ME4111` | EQU/LABEL(md) | `src/LO_SYN.mad:577`, `include/LO_SYN.labels.md:787` | 74111B | 1 |
| `ME4151` | EQU/LABEL(md) | `src/LO_SYN.mad:488`, `include/LO_SYN.labels.md:760` | 4151B | 1 |
| `ME4457` | EQU/LABEL(md) | `src/LO_SYN.mad:588`, `include/LO_SYN.labels.md:789` | 4457B | 1 |
| `ME4515` | EQU/LABEL(md) | `src/LO_SYN.mad:356`, `include/LO_SYN.labels.md:714` | 74515B | 1 |
| `ME4516` | EQU/LABEL(md) | `src/LO_SYN.mad:449`, `include/LO_SYN.labels.md:740` | 4516B | 1 |
| `ME4524` | EQU/LABEL(md) | `src/LO_SYN.mad:462`, `include/LO_SYN.labels.md:748` | 4524B | 1 |
| `ME4546` | EQU/LABEL(md) | `src/LO_SYN.mad:501`, `include/LO_SYN.labels.md:764` | 4546B | 1 |
| `ME4547` | EQU/LABEL(md) | `src/LO_SYN.mad:465`, `include/LO_SYN.labels.md:749` | 4547B | 1 |
| `ME4560` | EQU/LABEL(md) | `src/LO_SYN.mad:357`, `include/LO_SYN.labels.md:715` | 4560B | 1 |
| `ME5000` | EQU/LABEL(md) | `src/LO_SYN.mad:49`, `include/LO_SYN.labels.md:592` | 5000B | 1 |
| `ME5115` | EQU/LABEL(md) | `src/LO_SYN.mad:386`, `include/LO_SYN.labels.md:723` | 5115B | 1 |
| `ME5117` | EQU/LABEL(md) | `src/LO_SYN.mad:332`, `include/LO_SYN.labels.md:706` | 5117B | 1 |
| `ME5144` | EQU/LABEL(md) | `src/LO_SYN.mad:222`, `include/LO_SYN.labels.md:665` | 5144B | 1 |
| `ME5501` | EQU/LABEL(md) | `src/LO_SYN.mad:141`, `include/LO_SYN.labels.md:622` | 5501B | 1 |
| `ME5520` | EQU/LABEL(md) | `src/LO_SYN.mad:538`, `include/LO_SYN.labels.md:775` | 5520B | 1 |
| `ME6040` | EQU/LABEL(md) | `src/LO_SYN.mad:452`, `include/LO_SYN.labels.md:743` | 6040B | 1 |
| `ME6114` | EQU/LABEL(md) | `src/LO_SYN.mad:466`, `include/LO_SYN.labels.md:750` | 6114B | 1 |
| `ME6117` | EQU/LABEL(md) | `src/LO_SYN.mad:431`, `include/LO_SYN.labels.md:738` | 6117B | 1 |
| `ME6151` | EQU/LABEL(md) | `src/LO_SYN.mad:129`, `include/LO_SYN.labels.md:617` | 6151B | 1 |
| `ME6161` | EQU/LABEL(md) | `src/LO_SYN.mad:341`, `include/LO_SYN.labels.md:708` | 6161B | 1 |
| `ME6170` | EQU/LABEL(md) | `src/LO_SYN.mad:280`, `include/LO_SYN.labels.md:692` | 6170B | 1 |
| `ME6561` | EQU/LABEL(md) | `src/LO_SYN.mad:555`, `include/LO_SYN.labels.md:780` | 6561B | 1 |
| `ME7005` | EQU/LABEL(md) | `src/LO_SYN.mad:492`, `include/LO_SYN.labels.md:761` | 70055B | 1 |
| `ME7006` | EQU/LABEL(md) | `src/LO_SYN.mad:138`, `include/LO_SYN.labels.md:620` | 70066B | 1 |
| `ME7014` | EQU/LABEL(md) | `src/LO_SYN.mad:296`, `include/LO_SYN.labels.md:696` | 70143B | 1 |
| `ME7031` | EQU/LABEL(md) | `src/LO_SYN.mad:594`, `include/LO_SYN.labels.md:791` | 70311B | 1 |
| `ME7040` | EQU/LABEL(md) | `src/LO_SYN.mad:455`, `include/LO_SYN.labels.md:745` | 7040B | 1 |
| `ME7050` | EQU/LABEL(md) | `src/LO_SYN.mad:509`, `include/LO_SYN.labels.md:768` | 70502B | 1 |
| `ME7051` | EQU/LABEL(md) | `src/LO_SYN.mad:459`, `include/LO_SYN.labels.md:746` | 70510B | 1 |
| `ME7056` | EQU/LABEL(md) | `src/LO_SYN.mad:590`, `include/LO_SYN.labels.md:790` | 70561B | 1 |
| `ME7103` | EQU/LABEL(md) | `src/LO_SYN.mad:628`, `include/LO_SYN.labels.md:792` | 71037B | 1 |
| `ME7110` | EQU/LABEL(md) | `src/LO_SYN.mad:384`, `include/LO_SYN.labels.md:722` | 71105B | 1 |
| `ME7117` | EQU/LABEL(md) | `src/LO_SYN.mad:520`, `include/LO_SYN.labels.md:772` | 71171B | 1 |
| `ME7131` | EQU/LABEL(md) | `src/LO_SYN.mad:646`, `include/LO_SYN.labels.md:794` | 71312B | 1 |
| `ME7156` | EQU/LABEL(md) | `src/LO_SYN.mad:339`, `include/LO_SYN.labels.md:707` | 71561B | 1 |
| `ME7157` | EQU/LABEL(md) | `src/LO_SYN.mad:484`, `include/LO_SYN.labels.md:758` | 71570B | 1 |
| `ME7250` | EQU/LABEL(md) | `src/LO_SYN.mad:450`, `include/LO_SYN.labels.md:741` | 72507B | 1 |
| `ME7251` | EQU/LABEL(md) | `src/LO_SYN.mad:124`, `include/LO_SYN.labels.md:616` | 72510B | 1 |
| `ME7252` | EQU/LABEL(md) | `src/LO_SYN.mad:130`, `include/LO_SYN.labels.md:618` | 72520B | 1 |
| `ME7300` | EQU/LABEL(md) | `src/LO_SYN.mad:673`, `include/LO_SYN.labels.md:797` | 73007B | 1 |
| `ME7401` | EQU/LABEL(md) | `src/LO_SYN.mad:696`, `include/LO_SYN.labels.md:799` | 74017B | 1 |
| `ME7410` | EQU/LABEL(md) | `src/LO_SYN.mad:373`, `include/LO_SYN.labels.md:720` | 74101B | 1 |
| `ME7411` | EQU/LABEL(md) | `src/LO_SYN.mad:359`, `include/LO_SYN.labels.md:716` | 74110B | 1 |
| `ME7440` | EQU/LABEL(md) | `src/LO_SYN.mad:747`, `include/LO_SYN.labels.md:800` | 74401B | 1 |
| `ME7451` | EQU/LABEL(md) | `src/LO_SYN.mad:255`, `include/LO_SYN.labels.md:683` | 74517B | 1 |
| `ME7452` | EQU/LABEL(md) | `src/LO_SYN.mad:483`, `include/LO_SYN.labels.md:757` | 74524B | 1 |
| `ME7504` | EQU/LABEL(md) | `src/LO_SYN.mad:402`, `include/LO_SYN.labels.md:729` | 75040B | 1 |
| `ME7510` | EQU/LABEL(md) | `src/LO_SYN.mad:367`, `include/LO_SYN.labels.md:719` | 7510B | 1 |
| `ME7520` | EQU/LABEL(md) | `src/LO_SYN.mad:309`, `include/LO_SYN.labels.md:702` | 7520B | 1 |
| `ME7523` | EQU/LABEL(md) | `src/LO_SYN.mad:276`, `include/LO_SYN.labels.md:690` | 77523B | 1 |
| `ME7544` | EQU/LABEL(md) | `src/LO_SYN.mad:143`, `include/LO_SYN.labels.md:623` | 75440B | 1 |
| `ME7554` | EQU/LABEL(md) | `src/LO_SYN.mad:79`, `include/LO_SYN.labels.md:604` | 7554B | 1 |
| `ME7555` | EQU/LABEL(md) | `src/LO_SYN.mad:424`, `include/LO_SYN.labels.md:735` | 75551B | 1 |
| `ME7615` | EQU/LABEL(md) | `src/LO_SYN.mad:223`, `include/LO_SYN.labels.md:666` | 76151B | 1 |
| `ME7616` | EQU/LABEL(md) | `src/LO_SYN.mad:474`, `include/LO_SYN.labels.md:754` | 76161B | 1 |
| `ME7710` | EQU/LABEL(md) | `src/LO_SYN.mad:254`, `include/LO_SYN.labels.md:682` | 77103B | 1 |
| `ME7712` | EQU/LABEL(md) | `src/LO_SYN.mad:230`, `include/LO_SYN.labels.md:669` | 77124B | 1 |
| `ME7757` | EQU/LABEL(md) | `src/LO_SYN.mad:117`, `include/LO_SYN.labels.md:613` | 77576B | 1 |
| `MISAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:125`, `include/FOREX.labels.md:196`, `include/FOREX.labels.md:546` | 40037B | 1 |
| `MK760` | EQU/LABEL(md) | `src/FOREX_CORE.mad:122`, `include/FOREX.labels.md:193`, `include/FOREX.labels.md:543` | 7760B | 1 |
| `ML771` | EQU/LABEL(md) | `src/FOREX_CORE.mad:127`, `include/FOREX.labels.md:198`, `include/FOREX.labels.md:553` | 7771B | 1 |
| `MNTHIB` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:69`, `include/FOREX.labels.md:261`, `include/FOREX.labels.md:551` | 24 | 1 |
| `MNTHNM` | LABEL(md)/TEXT | `src/FOREX_RUNTIME.mad:413`, `include/FOREX.labels.md:64`, `include/FOREX.labels.md:552` | — | 1 |
| `MRT22` | EQU/LABEL(md) | `src/FOREX_CORE.mad:126`, `include/FOREX.labels.md:197`, `include/FOREX.labels.md:547` | 22B | 1 |
| `MRT22D` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:35`, `include/FOREX.labels.md:323`, `include/FOREX.labels.md:548` | 18 | 1 |
| `MSK` | TEXT | `src/FOREX_RUNTIME.mad:515` | GOSTBL | 1 |
| `MSK73` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:70`, `include/RUNTIME_DISASM.xref.md:93` | 37777774 77777477 | 1 |
| `MSK76` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:71`, `include/RUNTIME_DISASM.xref.md:94` | 77270707 00000000 | 1 |
| `MV0113` | EQU/LABEL(md) | `src/LO_SYN.mad:522`, `include/LO_SYN.labels.md:437` | 70113B | 1 |
| `MV0151` | EQU/LABEL(md) | `src/LO_SYN.mad:378`, `include/LO_SYN.labels.md:431` | 151B | 1 |
| `MV09N9` | EQU/LABEL(md) | `src/LO_GEN.mad:246`, `include/LO_GEN.labels.md:1300` | 12501 | 1 |
| `MV0J3V` | EQU/LABEL(md) | `src/LO_GEN.mad:249`, `include/LO_GEN.labels.md:1303` | 24763 | 1 |
| `MV0J46` | EQU/LABEL(md) | `src/LO_GEN.mad:251`, `include/LO_GEN.labels.md:1305` | 24774 | 1 |
| `MV0J47` | EQU/LABEL(md) | `src/LO_GEN.mad:252`, `include/LO_GEN.labels.md:1306` | 24775 | 1 |
| `MV0JSR` | EQU/LABEL(md) | `src/LO_GEN.mad:253`, `include/LO_GEN.labels.md:1307` | 25659 | 1 |
| `MV6502` | EQU/LABEL(md) | `src/LO_SYN.mad:490`, `include/LO_SYN.labels.md:436` | 6502B | 1 |
| `MV6520` | EQU/LABEL(md) | `src/LO_SYN.mad:487`, `include/LO_SYN.labels.md:435` | 6520B | 1 |
| `MV7011` | EQU/LABEL(md) | `src/LO_SYN.mad:421`, `include/LO_SYN.labels.md:433` | 70110B | 1 |
| `MV7654` | EQU/LABEL(md) | `src/LO_SYN.mad:559`, `include/LO_SYN.labels.md:438` | 76543B | 1 |
| `NG0012` | EQU/LABEL(md) | `src/LO_GEN.mad:267`, `include/LO_GEN.labels.md:1321` | -12 | 1 |
| `NOLAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:128`, `include/FOREX.labels.md:199`, `include/FOREX.labels.md:555` | 4003B | 1 |
| `NPR` | LABEL(md) | `include/FOREX.labels.md:27`, `include/FOREX.labels.md:78` | — | 1 |
| `OCDAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:129`, `include/FOREX.labels.md:200`, `include/FOREX.labels.md:560` | 74013B | 1 |
| `OCTCYC` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:443`, `include/FOREX.labels.md:558` | — | 1 |
| `OCTEDL` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:492`, `include/FOREX.labels.md:562` | — | 1 |
| `OCTERT` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:504`, `include/FOREX.labels.md:563` | — | 1 |
| `OCTISS` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:110`, `include/FOREX.labels.md:302`, `include/FOREX.labels.md:564` | 64-8 | 1 |
| `OCTSDM` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:70`, `include/FOREX.labels.md:262`, `include/FOREX.labels.md:565` | =777 7777-C | 1 |
| `OCTSYM` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:462`, `include/FOREX.labels.md:566` | — | 1 |
| `OS000` | COMMON | `src/FOREX_DECODER_DISASM.mad:249` | — | 1 |
| `OS003` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:257`, `include/RUNTIME_DECODER.xref.md:22` | — | 1 |
| `OS6SY` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:276`, `include/RUNTIME_DECODER.xref.md:23` | — | 1 |
| `OX003` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:305`, `include/RUNTIME_DECODER.xref.md:25` | — | 1 |
| `OXRET` | COMMON/XREF(md) | `src/FOREX_DECODER_DISASM.mad:318`, `include/RUNTIME_DECODER.xref.md:26` | — | 1 |
| `P1` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:114`, `include/FOREX.labels.md:306`, `include/FOREX.labels.md:592` | 10.0 | 1 |
| `P2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:113`, `include/FOREX.labels.md:305`, `include/FOREX.labels.md:593` | 100.0 | 1 |
| `P3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:112`, `include/FOREX.labels.md:304`, `include/FOREX.labels.md:594` | 1000.0 | 1 |
| `P4` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:111`, `include/FOREX.labels.md:303`, `include/FOREX.labels.md:595` | 10000.0 | 1 |
| `P5` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:72`, `include/FOREX.labels.md:264`, `include/FOREX.labels.md:596` | 100000.0 | 1 |
| `PAGEGV` | LABEL(md)/NAME/SUBP | `src/FOREX_CORE.mad:163`, `src/LO_GEN.mad:31`, `include/FOREX_ROOT.mad:71`, `include/FOREX_ROOT.mad:235`, `include/FOREX.labels.md:23`, `include/FOREX.labels.md:85` … (+2) | — | 1 |
| `PAGETK` | ENTRY/LABEL(md)/SUBP | `src/FOREX_CORE.mad:162`, `src/LO_GEN.mad:30`, `include/FOREX_ROOT.mad:70`, `include/FOREX_ROOT.mad:276`, `include/FOREX.labels.md:22`, `include/FOREX.labels.md:86` … (+2) | — | 1 |
| `PG0021` | LABEL/LABEL(md) | `src/LO_SYN.mad:817`, `include/LO_SYN.labels.md:12` | — | 1 |
| `PG67CD` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:40`, `include/FOREX.labels.md:328`, `include/FOREX.labels.md:578` | =:11 4037 77 | 1 |
| `PG67CN` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:275`, `include/FOREX.labels.md:579` | — | 1 |
| `PGBLKM` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:39`, `include/FOREX.labels.md:327`, `include/FOREX.labels.md:574` | =4000 | 1 |
| `PGCOMM` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:255`, `include/FOREX.labels.md:575` | — | 1 |
| `PGCOPL` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:256`, `include/FOREX.labels.md:576` | — | 1 |
| `PGFLGS` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:41`, `include/FOREX.labels.md:329`, `include/FOREX.labels.md:582` | 64+12 | 1 |
| `PGGO1` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:42`, `include/FOREX.labels.md:330`, `include/FOREX.labels.md:583` | =:00 2677 | 1 |
| `PGGO2` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:43`, `include/FOREX.labels.md:331`, `include/FOREX.labels.md:584` | =:00 6736 77 | 1 |
| `PGRST7` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:270`, `include/FOREX.labels.md:586` | — | 1 |
| `PGSAVS` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:290`, `include/FOREX.labels.md:587` | ONEW | 1 |
| `PGVAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:131`, `include/FOREX.labels.md:202`, `include/FOREX.labels.md:570` | 74012B | 1 |
| `PGWDSH` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:44`, `include/FOREX.labels.md:332`, `include/FOREX.labels.md:590` | 64-20 | 1 |
| `PGX67` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:273`, `include/FOREX.labels.md:577` | — | 1 |
| `PRIN` | LABEL(md) | `include/FOREX.labels.md:30`, `include/FOREX.labels.md:81` | 0o510327 | 1 |
| `PRINT8` | SUBP/XREF(md) | `src/FOREX_RUNTIME.mad:196`, `include/RUNTIME_DECODER.xref.md:20` | — | 1 |
| `PRMSAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:133`, `include/FOREX.labels.md:204`, `include/FOREX.labels.md:600` | 40023B | 1 |
| `PRTMSG` | LABEL/LABEL(md) | `src/FOREX_CORE.mad:295`, `include/FOREX_ROOT.mad:125`, `include/FOREX.labels.md:30`, `include/FOREX.labels.md:81`, `include/FOREX.labels.md:599` | — | 1 |
| `PTKAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:132`, `include/FOREX.labels.md:203`, `include/FOREX.labels.md:573` | 74011B | 1 |
| `R100A` | EQU/LABEL(md) | `src/FOREX_CORE.mad:134`, `include/FOREX.labels.md:205`, `include/FOREX.labels.md:602` | 4033B | 1 |
| `RETCL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:136`, `include/FOREX.labels.md:207`, `include/FOREX.labels.md:605` | 4023B | 1 |
| `RETMA` | EQU/LABEL(md) | `src/FOREX_CORE.mad:138`, `include/FOREX.labels.md:209`, `include/FOREX.labels.md:607` | 40050B | 1 |
| `RG0000` | EQU/LABEL(md) | `src/LO_SYN.mad:499`, `include/LO_SYN.labels.md:540` | 40510B | 1 |
| `RG0015` | EQU/LABEL(md) | `src/LO_SYN.mad:59`, `include/LO_SYN.labels.md:495` | 15B | 1 |
| `RG0110` | EQU/LABEL(md) | `src/LO_SYN.mad:303`, `include/LO_SYN.labels.md:524` | 110B | 1 |
| `RG0113` | EQU/LABEL(md) | `src/LO_SYN.mad:578`, `include/LO_SYN.labels.md:550` | 113B | 1 |
| `RG0117` | EQU/LABEL(md) | `src/LO_SYN.mad:482`, `include/LO_SYN.labels.md:539` | 20117B | 1 |
| `RG0122` | EQU/LABEL(md) | `src/LO_SYN.mad:133`, `include/LO_SYN.labels.md:505` | 122B | 1 |
| `RG0154` | EQU/LABEL(md) | `src/LO_SYN.mad:118`, `include/LO_SYN.labels.md:502` | 154B | 1 |
| `RG0160` | EQU/LABEL(md) | `src/LO_SYN.mad:542`, `include/LO_SYN.labels.md:547` | 160B | 1 |
| `RG0172` | EQU/LABEL(md) | `src/LO_SYN.mad:516`, `include/LO_SYN.labels.md:543` | 172B | 1 |
| `RG0327` | EQU/LABEL(md) | `src/LO_SYN.mad:605`, `include/LO_SYN.labels.md:552` | 327B | 1 |
| `RG0502` | EQU/LABEL(md) | `src/LO_SYN.mad:608`, `include/LO_SYN.labels.md:553` | 502B | 1 |
| `RG0505` | EQU/LABEL(md) | `src/LO_SYN.mad:562`, `include/LO_SYN.labels.md:549` | 505B | 1 |
| `RG0506` | EQU/LABEL(md) | `src/LO_SYN.mad:612`, `include/LO_SYN.labels.md:554` | 506B | 1 |
| `RG0510` | EQU/LABEL(md) | `src/LO_SYN.mad:614`, `include/LO_SYN.labels.md:555` | 510B | 1 |
| `RG0547` | EQU/LABEL(md) | `src/LO_SYN.mad:456`, `include/LO_SYN.labels.md:534` | 40547B | 1 |
| `RG0551` | EQU/LABEL(md) | `src/LO_SYN.mad:413`, `include/LO_SYN.labels.md:532` | 551B | 1 |
| `RG1002` | EQU/LABEL(md) | `src/LO_SYN.mad:619`, `include/LO_SYN.labels.md:556` | 1002B | 1 |
| `RG1006` | EQU/LABEL(md) | `src/LO_SYN.mad:621`, `include/LO_SYN.labels.md:557` | 1006B | 1 |
| `RG1033` | EQU/LABEL(md) | `src/LO_SYN.mad:625`, `include/LO_SYN.labels.md:558` | 1033B | 1 |
| `RG1034` | EQU/LABEL(md) | `src/LO_SYN.mad:626`, `include/LO_SYN.labels.md:559` | 1034B | 1 |
| `RG1035` | EQU/LABEL(md) | `src/LO_SYN.mad:627`, `include/LO_SYN.labels.md:560` | 1035B | 1 |
| `RG1102` | EQU/LABEL(md) | `src/LO_SYN.mad:630`, `include/LO_SYN.labels.md:561` | 1102B | 1 |
| `RG1115` | EQU/LABEL(md) | `src/LO_SYN.mad:633`, `include/LO_SYN.labels.md:562` | 1115B | 1 |
| `RG1204` | EQU/LABEL(md) | `src/LO_SYN.mad:636`, `include/LO_SYN.labels.md:563` | 1204B | 1 |
| `RG1214` | EQU/LABEL(md) | `src/LO_SYN.mad:638`, `include/LO_SYN.labels.md:564` | 1214B | 1 |
| `RG1217` | EQU/LABEL(md) | `src/LO_SYN.mad:640`, `include/LO_SYN.labels.md:565` | 1217B | 1 |
| `RG1301` | EQU/LABEL(md) | `src/LO_SYN.mad:641`, `include/LO_SYN.labels.md:566` | 1301B | 1 |
| `RG1303` | EQU/LABEL(md) | `src/LO_SYN.mad:643`, `include/LO_SYN.labels.md:567` | 1303B | 1 |
| `RG1315` | EQU/LABEL(md) | `src/LO_SYN.mad:649`, `include/LO_SYN.labels.md:568` | 1315B | 1 |
| `RG1402` | EQU/LABEL(md) | `src/LO_SYN.mad:656`, `include/LO_SYN.labels.md:569` | 1402B | 1 |
| `RG1403` | EQU/LABEL(md) | `src/LO_SYN.mad:657`, `include/LO_SYN.labels.md:570` | 1403B | 1 |
| `RG1407` | EQU/LABEL(md) | `src/LO_SYN.mad:660`, `include/LO_SYN.labels.md:571` | 1407B | 1 |
| `RG1524` | EQU/LABEL(md) | `src/LO_SYN.mad:547`, `include/LO_SYN.labels.md:548` | 1524B | 1 |
| `RG2001` | EQU/LABEL(md) | `src/LO_SYN.mad:661`, `include/LO_SYN.labels.md:572` | 2001B | 1 |
| `RG2010` | EQU/LABEL(md) | `src/LO_SYN.mad:667`, `include/LO_SYN.labels.md:573` | 2010B | 1 |
| `RG2011` | EQU/LABEL(md) | `src/LO_SYN.mad:162`, `include/LO_SYN.labels.md:508` | 20113B | 1 |
| `RG2014` | EQU/LABEL(md) | `src/LO_SYN.mad:175`, `include/LO_SYN.labels.md:509` | 20142B | 1 |
| `RG2174` | EQU/LABEL(md) | `src/LO_SYN.mad:75`, `include/LO_SYN.labels.md:499` | 2174B | 1 |
| `RG2544` | EQU/LABEL(md) | `src/LO_SYN.mad:372`, `include/LO_SYN.labels.md:530` | 2544B | 1 |
| `RG3031` | EQU/LABEL(md) | `src/LO_SYN.mad:68`, `include/LO_SYN.labels.md:498` | 30311B | 1 |
| `RG3102` | EQU/LABEL(md) | `src/LO_SYN.mad:676`, `include/LO_SYN.labels.md:574` | 3102B | 1 |
| `RG3103` | EQU/LABEL(md) | `src/LO_SYN.mad:677`, `include/LO_SYN.labels.md:575` | 3103B | 1 |
| `RG3601` | EQU/LABEL(md) | `src/LO_SYN.mad:66`, `include/LO_SYN.labels.md:496` | 36017B | 1 |
| `RG4010` | EQU/LABEL(md) | `src/LO_SYN.mad:688`, `include/LO_SYN.labels.md:576` | 4010B | 1 |
| `RG4023` | EQU/LABEL(md) | `src/LO_SYN.mad:700`, `include/LO_SYN.labels.md:577` | 4023B | 1 |
| `RG4025` | EQU/LABEL(md) | `src/LO_SYN.mad:703`, `include/LO_SYN.labels.md:578` | 4025B | 1 |
| `RG4071` | EQU/LABEL(md) | `src/LO_SYN.mad:724`, `include/LO_SYN.labels.md:579` | 4071B | 1 |
| `RG4110` | EQU/LABEL(md) | `src/LO_SYN.mad:506`, `include/LO_SYN.labels.md:541` | 41105B | 1 |
| `RG4131` | EQU/LABEL(md) | `src/LO_SYN.mad:232`, `include/LO_SYN.labels.md:517` | 4131B | 1 |
| `RG4313` | EQU/LABEL(md) | `src/LO_SYN.mad:734`, `include/LO_SYN.labels.md:580` | 4313B | 1 |
| `RG4321` | EQU/LABEL(md) | `src/LO_SYN.mad:739`, `include/LO_SYN.labels.md:581` | 4321B | 1 |
| `RG4325` | EQU/LABEL(md) | `src/LO_SYN.mad:743`, `include/LO_SYN.labels.md:582` | 4325B | 1 |
| `RG4406` | EQU/LABEL(md) | `src/LO_SYN.mad:750`, `include/LO_SYN.labels.md:584` | 4406B | 1 |
| `RG5505` | EQU/LABEL(md) | `src/LO_SYN.mad:458`, `include/LO_SYN.labels.md:535` | 5505B | 1 |
| `RG7014` | EQU/LABEL(md) | `src/LO_SYN.mad:279`, `include/LO_SYN.labels.md:521` | 70146B | 1 |
| `RG7050` | EQU/LABEL(md) | `src/LO_SYN.mad:306`, `include/LO_SYN.labels.md:525` | 70502B | 1 |
| `RG7051` | EQU/LABEL(md) | `src/LO_SYN.mad:340`, `include/LO_SYN.labels.md:527` | 70514B | 1 |
| `RG7251` | EQU/LABEL(md) | `src/LO_SYN.mad:292`, `include/LO_SYN.labels.md:523` | 72510B | 1 |
| `RG7440` | EQU/LABEL(md) | `src/LO_SYN.mad:748`, `include/LO_SYN.labels.md:583` | 74404B | 1 |
| `RG7502` | EQU/LABEL(md) | `src/LO_SYN.mad:477`, `include/LO_SYN.labels.md:537` | 7502B | 1 |
| `RG7650` | EQU/LABEL(md) | `src/LO_SYN.mad:581`, `include/LO_SYN.labels.md:551` | 76505B | 1 |
| `RMWD4` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:48`, `include/FOREX.labels.md:336`, `include/FOREX.labels.md:608` | 4 | 1 |
| `RS0002` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:260`, `src/LO_GEN.mad:557`, `src/LO_GEN.mad:3507`, `src/LO_GEN.mad:3510`, `include/LO_GEN.labels.md:1314` | 2 | 1 |
| `RS0003` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:261`, `src/LO_GEN.mad:626`, `src/LO_GEN.mad:1033`, `src/LO_GEN.mad:1081`, `src/LO_GEN.mad:1939`, `src/LO_GEN.mad:1975` … (+11) | 3 | 1 |
| `RS0005` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:263`, `src/LO_GEN.mad:632`, `src/LO_GEN.mad:667`, `src/LO_GEN.mad:3330`, `src/LO_GEN.mad:3351`, `include/LO_GEN.labels.md:1317` | 5 | 1 |
| `RS0009` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:266`, `src/LO_GEN.mad:703`, `src/LO_GEN.mad:835`, `src/LO_GEN.mad:928`, `src/LO_GEN.mad:1117`, `src/LO_GEN.mad:1120` … (+10) | 9 | 1 |
| `RS0013` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:257`, `src/LO_GEN.mad:581`, `src/LO_GEN.mad:599`, `src/LO_GEN.mad:664`, `include/LO_GEN.labels.md:1311` | 13 | 1 |
| `RS0015` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:259`, `src/LO_GEN.mad:688`, `src/LO_GEN.mad:718`, `src/LO_GEN.mad:724`, `src/LO_GEN.mad:808`, `src/LO_GEN.mad:889` … (+39) | 15 | 1 |
| `SC0002` | EQU/LABEL(md) | `src/LO_SYN.mad:74`, `include/LO_SYN.labels.md:449` | 2B | 1 |
| `SC0003` | EQU/LABEL(md) | `src/LO_SYN.mad:44`, `include/LO_SYN.labels.md:444` | 3B | 1 |
| `SC0014` | EQU/LABEL(md) | `src/LO_SYN.mad:64`, `include/LO_SYN.labels.md:448` | 14B | 1 |
| `SC0016` | EQU/LABEL(md) | `src/LO_SYN.mad:60`, `include/LO_SYN.labels.md:447` | 16B | 1 |
| `SC0017` | EQU/LABEL(md) | `src/LO_SYN.mad:58`, `include/LO_SYN.labels.md:446` | 17B | 1 |
| `SC0101` | EQU/LABEL(md) | `src/LO_SYN.mad:592`, `include/LO_SYN.labels.md:451` | 101B | 1 |
| `SC0200` | EQU/LABEL(md) | `src/LO_SYN.mad:690`, `include/LO_SYN.labels.md:470` | 200B | 1 |
| `SC0201` | EQU/LABEL(md) | `src/LO_SYN.mad:722`, `include/LO_SYN.labels.md:477` | 201B | 1 |
| `SC0322` | EQU/LABEL(md) | `src/LO_SYN.mad:600`, `include/LO_SYN.labels.md:454` | 322B | 1 |
| `SC1201` | EQU/LABEL(md) | `src/LO_SYN.mad:752`, `include/LO_SYN.labels.md:484` | 1201B | 1 |
| `SC1322` | EQU/LABEL(md) | `src/LO_SYN.mad:650`, `include/LO_SYN.labels.md:462` | 1322B | 1 |
| `SC2006` | EQU/LABEL(md) | `src/LO_SYN.mad:666`, `include/LO_SYN.labels.md:466` | 2006B | 1 |
| `SC4015` | EQU/LABEL(md) | `src/LO_SYN.mad:694`, `include/LO_SYN.labels.md:471` | 4015B | 1 |
| `SC4061` | EQU/LABEL(md) | `src/LO_SYN.mad:723`, `include/LO_SYN.labels.md:478` | 4061B | 1 |
| `SC4303` | EQU/LABEL(md) | `src/LO_SYN.mad:731`, `include/LO_SYN.labels.md:479` | 4303B | 1 |
| `SC4315` | EQU/LABEL(md) | `src/LO_SYN.mad:737`, `include/LO_SYN.labels.md:481` | 4315B | 1 |
| `SC4317` | EQU/LABEL(md) | `src/LO_SYN.mad:738`, `include/LO_SYN.labels.md:482` | 4317B | 1 |
| `SC4330` | EQU/LABEL(md) | `src/LO_SYN.mad:746`, `include/LO_SYN.labels.md:483` | 4330B | 1 |
| `SC4412` | EQU/LABEL(md) | `src/LO_SYN.mad:753`, `include/LO_SYN.labels.md:485` | 4412B | 1 |
| `SC4422` | EQU/LABEL(md) | `src/LO_SYN.mad:757`, `include/LO_SYN.labels.md:487` | 4422B | 1 |
| `SC7032` | EQU/LABEL(md) | `src/LO_SYN.mad:602`, `include/LO_SYN.labels.md:455` | 70324B | 1 |
| `SC7050` | EQU/LABEL(md) | `src/LO_SYN.mad:609`, `include/LO_SYN.labels.md:457` | 70503B | 1 |
| `SC7101` | EQU/LABEL(md) | `src/LO_SYN.mad:622`, `include/LO_SYN.labels.md:460` | 71013B | 1 |
| `SC7121` | EQU/LABEL(md) | `src/LO_SYN.mad:637`, `include/LO_SYN.labels.md:461` | 71213B | 1 |
| `SC7132` | EQU/LABEL(md) | `src/LO_SYN.mad:653`, `include/LO_SYN.labels.md:463` | 71325B | 1 |
| `SC7140` | EQU/LABEL(md) | `src/LO_SYN.mad:658`, `include/LO_SYN.labels.md:464` | 71404B | 1 |
| `SC7200` | EQU/LABEL(md) | `src/LO_SYN.mad:662`, `include/LO_SYN.labels.md:465` | 72002B | 1 |
| `SC7403` | EQU/LABEL(md) | `src/LO_SYN.mad:710`, `include/LO_SYN.labels.md:474` | 74034B | 1 |
| `SC7404` | EQU/LABEL(md) | `src/LO_SYN.mad:717`, `include/LO_SYN.labels.md:476` | 74042B | 1 |
| `SC7441` | EQU/LABEL(md) | `src/LO_SYN.mad:754`, `include/LO_SYN.labels.md:486` | 74413B | 1 |
| `SOM` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:81`, `include/FOREX.labels.md:273`, `include/FOREX.labels.md:616` | -8 | 1 |
| `STKOF1` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:75`, `include/FOREX.labels.md:267`, `include/FOREX.labels.md:609` | -1 | 1 |
| `STKOF6` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:80`, `include/FOREX.labels.md:272`, `include/FOREX.labels.md:614` | -6 | 1 |
| `TIMSCL` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:52`, `include/FOREX.labels.md:340`, `include/FOREX.labels.md:647` | =R100.0 | 1 |
| `TIMSEA` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:53`, `include/FOREX.labels.md:341`, `include/FOREX.labels.md:648` | =6H'''17''17''17''17''17' | 1 |
| `TIMSEB` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:54`, `include/FOREX.labels.md:342`, `include/FOREX.labels.md:649` | =6H'17''17''17''''17''17' | 1 |
| `TIMSEC` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:55`, `include/FOREX.labels.md:343`, `include/FOREX.labels.md:650` | =6H'''''''16''''' | 1 |
| `TL0000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:82`, `include/FOREX.labels.md:274`, `include/FOREX.labels.md:618` | ''000000'' | 1 |
| `TL0001` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:83`, `include/FOREX.labels.md:275`, `include/FOREX.labels.md:619` | 1H'055' | 1 |
| `TL0002` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:84`, `include/FOREX.labels.md:276`, `include/FOREX.labels.md:620` | 2H '200' | 1 |
| `TL0003` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:85`, `include/FOREX.labels.md:277`, `include/FOREX.labels.md:621` | 3H00 | 1 |
| `TL0004` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:86`, `include/FOREX.labels.md:278`, `include/FOREX.labels.md:622` | =6H00 | 1 |
| `TL0006` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:88`, `include/FOREX.labels.md:280`, `include/FOREX.labels.md:624` | 6H000000 | 1 |
| `TL0007` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:89`, `include/FOREX.labels.md:281`, `include/FOREX.labels.md:625` | 6H000 00 | 1 |
| `TL0008` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:90`, `include/FOREX.labels.md:282`, `include/FOREX.labels.md:626` | =6H00/00/ | 1 |
| `TL0010` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:92`, `include/FOREX.labels.md:284`, `include/FOREX.labels.md:628` | 6HABГCEH | 1 |
| `TL0011` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:93`, `include/FOREX.labels.md:285`, `include/FOREX.labels.md:629` | 6HARRAY | 1 |
| `TL0012` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:94`, `include/FOREX.labels.md:286`, `include/FOREX.labels.md:630` | 6HAПPMAЯ | 1 |
| `TL0013` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:95`, `include/FOREX.labels.md:287`, `include/FOREX.labels.md:631` | 6HERROR | 1 |
| `TL0014` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:96`, `include/FOREX.labels.md:288`, `include/FOREX.labels.md:632` | 6HIN STA | 1 |
| `TL0015` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:97`, `include/FOREX.labels.md:289`, `include/FOREX.labels.md:633` | 6HNDART | 1 |
| `TL0016` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:98`, `include/FOREX.labels.md:290`, `include/FOREX.labels.md:634` | 6HOKTHOЯ | 1 |
| `TL0017` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:99`, `include/FOREX.labels.md:291`, `include/FOREX.labels.md:635` | 6H 00.00 | 1 |
| `TL0018` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:100`, `include/FOREX.labels.md:292`, `include/FOREX.labels.md:636` | =6H'17''17''''''''' | 1 |
| `TL0019` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:101`, `include/FOREX.labels.md:293`, `include/FOREX.labels.md:637` | 6H'201'  '200'7 | 1 |
| `TL0021` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:103`, `include/FOREX.labels.md:295`, `include/FOREX.labels.md:639` | =6H'3''17''''17''17''' | 1 |
| `TL0022` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:104`, `include/FOREX.labels.md:296`, `include/FOREX.labels.md:640` | 6HФEBMAP | 1 |
| `TL0023` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:105`, `include/FOREX.labels.md:297`, `include/FOREX.labels.md:641` | 6HДEK | 1 |
| `TL0024` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:106`, `include/FOREX.labels.md:298`, `include/FOREX.labels.md:642` | 6HИЮHИЮЛ | 1 |
| `TTXAD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:141`, `include/FOREX.labels.md:212`, `include/FOREX.labels.md:651` | 4037B | 1 |
| `TTXBA` | EQU/LABEL(md) | `src/FOREX_CORE.mad:142`, `include/FOREX.labels.md:213`, `include/FOREX.labels.md:652` | 40033B | 1 |
| `TXLGEN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:50`, `include/FOREX.labels.md:338`, `include/FOREX.labels.md:643` | 8HLO*GEN | 1 |
| `TXLSYN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:51`, `include/FOREX.labels.md:339`, `include/FOREX.labels.md:644` | 8HLO*SYN | 1 |
| `WRTLBR` | LABEL(md)/SUBP | `src/FOREX_RUNTIME.mad:195`, `include/FOREX.labels.md:653` | — | 1 |
| `WV0350` | EQU/LABEL(md) | `src/LO_GEN.mad:493`, `include/LO_GEN.labels.md:1295` | 0003500000030264 | 1 |
| `WV0422` | EQU/LABEL(md) | `src/LO_GEN.mad:494`, `include/LO_GEN.labels.md:1296` | 0004220010075377 | 1 |
| `X02` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:52`, `include/RUNTIME_DISASM.xref.md:26` | 74002B | 1 |
| `X03` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:53`, `include/RUNTIME_DISASM.xref.md:27` | 74003B | 1 |
| `X04` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:54`, `include/RUNTIME_DISASM.xref.md:28` | 74004B | 1 |
| `X05` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:55`, `include/RUNTIME_DISASM.xref.md:29` | 74005B | 1 |
| `X06` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:56`, `include/RUNTIME_DISASM.xref.md:30` | 74006B | 1 |
| `X07` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:57`, `include/RUNTIME_DISASM.xref.md:31` | 74007B | 1 |
| `X10` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:58`, `include/RUNTIME_DISASM.xref.md:32` | 74010B | 1 |
| `X11` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:59`, `include/RUNTIME_DISASM.xref.md:33` | 74011B | 1 |
| `X12` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:60`, `include/RUNTIME_DISASM.xref.md:34` | 74012B | 1 |
| `X13` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:61`, `include/RUNTIME_DISASM.xref.md:35` | 74013B | 1 |
| `*A*` | COMMON | `src/FOREX_CORE.mad:156`, `src/LO_GEN.mad:497`, `src/LO_SYN.mad:21`, `include/FOREX_ROOT.mad:78` | AOC4K | 0 |
| `*DMON*` | COMMON | `src/LO_GEN.mad:499` | 5 | 0 |
| `A` | LABEL(md) | `include/FOREX.labels.md:8`, `include/FOREX.labels.md:703`, `include/LO_GEN.labels.md:28`, `include/LO_GEN.labels.md:28` | — | 0 |
| `AC0117` | EQU/LABEL(md) | `src/LO_GEN.mad:61`, `include/LO_GEN.labels.md:1111` | 117B | 0 |
| `AC0400` | EQU/LABEL(md) | `src/LO_GEN.mad:129`, `include/LO_GEN.labels.md:1179` | 400B | 0 |
| `AC0702` | EQU/LABEL(md) | `src/LO_GEN.mad:228`, `include/LO_GEN.labels.md:1278` | 702B | 0 |
| `AC0NE2` | EQU/LABEL(md) | `src/LO_GEN.mad:118`, `include/LO_GEN.labels.md:1168` | 30314B | 0 |
| `AC2200` | EQU/LABEL(md) | `src/LO_GEN.mad:106`, `include/LO_GEN.labels.md:1156` | 2200B | 0 |
| `AC7600` | EQU/LABEL(md) | `src/LO_GEN.mad:240`, `include/LO_GEN.labels.md:1290` | 7600B | 0 |
| `AD0005` | LABEL(md) | `include/LO_GEN.labels.md:66`, `include/LO_GEN.labels.md:1156` | 0o277505 | 0 |
| `AD0072` | LABEL(md) | `include/LO_GEN.labels.md:119`, `include/LO_GEN.labels.md:1325` | 0o277572 | 0 |
| `AD0702` | LABEL(md) | `include/LO_GEN.labels.md:511` | 0o300402 | 0 |
| `AD1710` | LABEL(md) | `include/LO_GEN.labels.md:1029` | 0o301410 | 0 |
| `ADDR_1` | LABEL(md) | `include/LO_GEN.labels.md:1096` | — | 0 |
| `ADDR_2` | LABEL(md) | `include/LO_GEN.labels.md:1151` | — | 0 |
| `ADDR_3` | LABEL(md) | `include/LO_GEN.labels.md:1164` | — | 0 |
| `ADDR_4` | LABEL(md) | `include/LO_GEN.labels.md:1177` | — | 0 |
| `ADDR_5` | LABEL(md) | `include/LO_GEN.labels.md:1218` | — | 0 |
| `ADDR_6` | LABEL(md) | `include/LO_GEN.labels.md:1263` | — | 0 |
| `ADDR_7` | LABEL(md) | `include/LO_GEN.labels.md:1275` | — | 0 |
| `AM0023` | LABEL(md) | `include/LO_GEN.labels.md:80`, `include/LO_GEN.labels.md:1328` | 0o277523 | 0 |
| `AM0037` | LABEL(md) | `include/LO_GEN.labels.md:92`, `include/LO_GEN.labels.md:1302`, `include/LO_GEN.labels.md:1316` | 0o277537 | 0 |
| `AM0053` | LABEL(md) | `include/LO_GEN.labels.md:104`, `include/LO_GEN.labels.md:1302` | 0o277553 | 0 |
| `AM0104` | LABEL(md) | `include/LO_GEN.labels.md:129` | 0o277604 | 0 |
| `AM0105` | LABEL(md) | `include/LO_GEN.labels.md:130`, `include/LO_GEN.labels.md:1303` | 0o277605 | 0 |
| `AM0111` | LABEL(md) | `include/LO_GEN.labels.md:134` | 0o277611 | 0 |
| `AM0112` | LABEL(md) | `include/LO_GEN.labels.md:135` | 0o277612 | 0 |
| `AM0113` | LABEL(md) | `include/LO_GEN.labels.md:136` | 0o277613 | 0 |
| `AM0116` | LABEL(md) | `include/LO_GEN.labels.md:139` | 0o277616 | 0 |
| `AM0117` | LABEL(md) | `include/LO_GEN.labels.md:140` | 0o277617 | 0 |
| `AM0120` | LABEL(md) | `include/LO_GEN.labels.md:141` | 0o277620 | 0 |
| `AM0125` | LABEL(md) | `include/LO_GEN.labels.md:146` | 0o277625 | 0 |
| `AM0134` | LABEL(md) | `include/LO_GEN.labels.md:153` | 0o277634 | 0 |
| `AM0137` | LABEL(md) | `include/LO_GEN.labels.md:156` | 0o277637 | 0 |
| `AM0142` | LABEL(md) | `include/LO_GEN.labels.md:159` | 0o277642 | 0 |
| `AM0144` | LABEL(md) | `include/LO_GEN.labels.md:161` | 0o277644 | 0 |
| `AM0204` | LABEL(md) | `include/LO_GEN.labels.md:193` | 0o277704 | 0 |
| `AM0206` | LABEL(md) | `include/LO_GEN.labels.md:195` | 0o277706 | 0 |
| `AM0207` | LABEL(md) | `include/LO_GEN.labels.md:196` | 0o277707 | 0 |
| `AM0213` | LABEL(md) | `include/LO_GEN.labels.md:200`, `include/LO_GEN.labels.md:1304` | 0o277713 | 0 |
| `AM0222` | LABEL(md) | `include/LO_GEN.labels.md:207` | 0o277722 | 0 |
| `AM0225` | LABEL(md) | `include/LO_GEN.labels.md:210` | 0o277725 | 0 |
| `AM0226` | LABEL(md) | `include/LO_GEN.labels.md:211` | 0o277726 | 0 |
| `AM0227` | LABEL(md) | `include/LO_GEN.labels.md:212` | 0o277727 | 0 |
| `AM0260` | LABEL(md) | `include/LO_GEN.labels.md:237` | 0o277760 | 0 |
| `AM0262` | LABEL(md) | `include/LO_GEN.labels.md:239` | 0o277762 | 0 |
| `AM0264` | LABEL(md) | `include/LO_GEN.labels.md:241`, `include/LO_GEN.labels.md:1303` | 0o277764 | 0 |
| `AM0266` | LABEL(md) | `include/LO_GEN.labels.md:243` | 0o277766 | 0 |
| `AM0267` | LABEL(md) | `include/LO_GEN.labels.md:244`, `include/LO_GEN.labels.md:1303` | 0o277767 | 0 |
| `AM0271` | LABEL(md) | `include/LO_GEN.labels.md:246` | 0o277771 | 0 |
| `AM0306` | LABEL(md) | `include/LO_GEN.labels.md:259` | 0o300006 | 0 |
| `AM0314` | LABEL(md) | `include/LO_GEN.labels.md:265` | 0o300014 | 0 |
| `AM0317` | LABEL(md) | `include/LO_GEN.labels.md:268` | 0o300017 | 0 |
| `AM0322` | LABEL(md) | `include/LO_GEN.labels.md:271` | 0o300022 | 0 |
| `AM0323` | LABEL(md) | `include/LO_GEN.labels.md:272` | 0o300023 | 0 |
| `AM0331` | LABEL(md) | `include/LO_GEN.labels.md:278`, `include/LO_GEN.labels.md:1305` | 0o300031 | 0 |
| `AM0337` | LABEL(md) | `include/LO_GEN.labels.md:284` | 0o300037 | 0 |
| `AM0341` | LABEL(md) | `include/LO_GEN.labels.md:286` | 0o300041 | 0 |
| `AM0343` | LABEL(md) | `include/LO_GEN.labels.md:288` | 0o300043 | 0 |
| `AM0351` | LABEL(md) | `include/LO_GEN.labels.md:294` | 0o300051 | 0 |
| `AM0352` | LABEL(md) | `include/LO_GEN.labels.md:295` | 0o300052 | 0 |
| `AM0355` | LABEL(md) | `include/LO_GEN.labels.md:298` | 0o300055 | 0 |
| `AM0362` | LABEL(md) | `include/LO_GEN.labels.md:303` | 0o300062 | 0 |
| `AM0363` | LABEL(md) | `include/LO_GEN.labels.md:304` | 0o300063 | 0 |
| `AM0636` | LABEL(md) | `include/LO_GEN.labels.md:475` | 0o300336 | 0 |
| `AM0641` | LABEL(md) | `include/LO_GEN.labels.md:478` | 0o300341 | 0 |
| `AM0643` | LABEL(md) | `include/LO_GEN.labels.md:480`, `include/LO_GEN.labels.md:1305` | 0o300343 | 0 |
| `AM0645` | LABEL(md) | `include/LO_GEN.labels.md:482`, `include/LO_GEN.labels.md:1305` | 0o300345 | 0 |
| `AM0667` | LABEL(md) | `include/LO_GEN.labels.md:500` | 0o300367 | 0 |
| `AM0671` | LABEL(md) | `include/LO_GEN.labels.md:502` | 0o300371 | 0 |
| `AM0710` | LABEL(md) | `include/LO_GEN.labels.md:517`, `include/LO_GEN.labels.md:1304` | 0o300410 | 0 |
| `AM0714` | LABEL(md) | `include/LO_GEN.labels.md:521` | 0o300414 | 0 |
| `AM0715` | LABEL(md) | `include/LO_GEN.labels.md:522` | 0o300415 | 0 |
| `AM0720` | LABEL(md) | `include/LO_GEN.labels.md:525` | 0o300420 | 0 |
| `AM0726` | LABEL(md) | `include/LO_GEN.labels.md:531` | 0o300426 | 0 |
| `AM0730` | LABEL(md) | `include/LO_GEN.labels.md:533` | 0o300430 | 0 |
| `AM0732` | LABEL(md) | `include/LO_GEN.labels.md:535` | 0o300432 | 0 |
| `AM0734` | LABEL(md) | `include/LO_GEN.labels.md:537` | 0o300434 | 0 |
| `AM0736` | LABEL(md) | `include/LO_GEN.labels.md:539` | 0o300436 | 0 |
| `AM0743` | LABEL(md) | `include/LO_GEN.labels.md:544`, `include/LO_GEN.labels.md:1304` | 0o300443 | 0 |
| `AM0752` | LABEL(md) | `include/LO_GEN.labels.md:551` | 0o300452 | 0 |
| `AM0753` | LABEL(md) | `include/LO_GEN.labels.md:552` | 0o300453 | 0 |
| `AM0757` | LABEL(md) | `include/LO_GEN.labels.md:556` | 0o300457 | 0 |
| `AM0761` | LABEL(md) | `include/LO_GEN.labels.md:558`, `include/LO_GEN.labels.md:1298` | 0o300461 | 0 |
| `AM0765` | LABEL(md) | `include/LO_GEN.labels.md:562` | 0o300465 | 0 |
| `AM0770` | LABEL(md) | `include/LO_GEN.labels.md:565` | 0o300470 | 0 |
| `AM0774` | LABEL(md) | `include/LO_GEN.labels.md:569` | 0o300474 | 0 |
| `AM0777` | LABEL(md) | `include/LO_GEN.labels.md:572` | 0o300477 | 0 |
| `AM1011` | LABEL(md) | `include/LO_GEN.labels.md:582` | 0o300511 | 0 |
| `AM1022` | LABEL(md) | `include/LO_GEN.labels.md:591` | 0o300522 | 0 |
| `AM1023` | LABEL(md) | `include/LO_GEN.labels.md:592` | 0o300523 | 0 |
| `AM1030` | LABEL(md) | `include/LO_GEN.labels.md:597` | 0o300530 | 0 |
| `AM1044` | LABEL(md) | `include/LO_GEN.labels.md:609`, `include/LO_GEN.labels.md:1298` | 0o300544 | 0 |
| `AM1062` | LABEL(md) | `include/LO_GEN.labels.md:623` | 0o300562 | 0 |
| `AM1075` | LABEL(md) | `include/LO_GEN.labels.md:634`, `include/LO_GEN.labels.md:1298` | 0o300575 | 0 |
| `AM1104` | LABEL(md) | `include/LO_GEN.labels.md:641` | 0o300604 | 0 |
| `AM1115` | LABEL(md) | `include/LO_GEN.labels.md:650` | 0o300615 | 0 |
| `AM1116` | LABEL(md) | `include/LO_GEN.labels.md:651` | 0o300616 | 0 |
| `AM1124` | LABEL(md) | `include/LO_GEN.labels.md:657` | 0o300624 | 0 |
| `AM1127` | LABEL(md) | `include/LO_GEN.labels.md:660` | 0o300627 | 0 |
| `AM1134` | LABEL(md) | `include/LO_GEN.labels.md:665` | 0o300634 | 0 |
| `AM1135` | LABEL(md) | `include/LO_GEN.labels.md:666` | 0o300635 | 0 |
| `AM1136` | LABEL(md) | `include/LO_GEN.labels.md:667` | 0o300636 | 0 |
| `AM1145` | LABEL(md) | `include/LO_GEN.labels.md:674` | 0o300645 | 0 |
| `AM1152` | LABEL(md) | `include/LO_GEN.labels.md:679` | 0o300652 | 0 |
| `AM1157` | LABEL(md) | `include/LO_GEN.labels.md:684` | 0o300657 | 0 |
| `AM1161` | LABEL(md) | `include/LO_GEN.labels.md:686` | 0o300661 | 0 |
| `AM1162` | LABEL(md) | `include/LO_GEN.labels.md:687` | 0o300662 | 0 |
| `AM1166` | LABEL(md) | `include/LO_GEN.labels.md:691` | 0o300666 | 0 |
| `AM1170` | LABEL(md) | `include/LO_GEN.labels.md:693` | 0o300670 | 0 |
| `AM1173` | LABEL(md) | `include/LO_GEN.labels.md:696` | 0o300673 | 0 |
| `AM1175` | LABEL(md) | `include/LO_GEN.labels.md:698` | 0o300675 | 0 |
| `AM1207` | LABEL(md) | `include/LO_GEN.labels.md:708` | 0o300707 | 0 |
| `AM1210` | LABEL(md) | `include/LO_GEN.labels.md:709` | 0o300710 | 0 |
| `AM1213` | LABEL(md) | `include/LO_GEN.labels.md:712` | 0o300713 | 0 |
| `AM1215` | LABEL(md) | `include/LO_GEN.labels.md:714` | 0o300715 | 0 |
| `AM1227` | LABEL(md) | `include/LO_GEN.labels.md:724` | 0o300727 | 0 |
| `AM1237` | LABEL(md) | `include/LO_GEN.labels.md:732` | 0o300737 | 0 |
| `AM1265` | LABEL(md) | `include/LO_GEN.labels.md:754` | 0o300765 | 0 |
| `AM1273` | LABEL(md) | `include/LO_GEN.labels.md:760`, `include/LO_GEN.labels.md:1300` | 0o300773 | 0 |
| `AM1274` | LABEL(md) | `include/LO_GEN.labels.md:761` | 0o300774 | 0 |
| `AM1300` | LABEL(md) | `include/LO_GEN.labels.md:765` | 0o301000 | 0 |
| `AM1302` | LABEL(md) | `include/LO_GEN.labels.md:767`, `include/LO_GEN.labels.md:1299` | 0o301002 | 0 |
| `AM1303` | LABEL(md) | `include/LO_GEN.labels.md:768` | 0o301003 | 0 |
| `AM1306` | LABEL(md) | `include/LO_GEN.labels.md:771` | 0o301006 | 0 |
| `AM1316` | LABEL(md) | `include/LO_GEN.labels.md:779` | 0o301016 | 0 |
| `AM1317` | LABEL(md) | `include/LO_GEN.labels.md:780`, `include/LO_GEN.labels.md:1300` | 0o301017 | 0 |
| `AM1321` | LABEL(md) | `include/LO_GEN.labels.md:782` | 0o301021 | 0 |
| `AM1331` | LABEL(md) | `include/LO_GEN.labels.md:790` | 0o301031 | 0 |
| `AM1335` | LABEL(md) | `include/LO_GEN.labels.md:794` | 0o301035 | 0 |
| `AM1343` | LABEL(md) | `include/LO_GEN.labels.md:800` | 0o301043 | 0 |
| `AM1345` | LABEL(md) | `include/LO_GEN.labels.md:802` | 0o301045 | 0 |
| `AM1346` | LABEL(md) | `include/LO_GEN.labels.md:803` | 0o301046 | 0 |
| `AM1356` | LABEL(md) | `include/LO_GEN.labels.md:811` | 0o301056 | 0 |
| `AM1357` | LABEL(md) | `include/LO_GEN.labels.md:812` | 0o301057 | 0 |
| `AM1366` | LABEL(md) | `include/LO_GEN.labels.md:819` | 0o301066 | 0 |
| `AM1367` | LABEL(md) | `include/LO_GEN.labels.md:820` | 0o301067 | 0 |
| `AM1371` | LABEL(md) | `include/LO_GEN.labels.md:822` | 0o301071 | 0 |
| `AM1374` | LABEL(md) | `include/LO_GEN.labels.md:825` | 0o301074 | 0 |
| `AM1400` | LABEL(md) | `include/LO_GEN.labels.md:829` | 0o301100 | 0 |
| `AM1401` | LABEL(md) | `include/LO_GEN.labels.md:830` | 0o301101 | 0 |
| `AM1406` | LABEL(md) | `include/LO_GEN.labels.md:835` | 0o301106 | 0 |
| `AM1415` | LABEL(md) | `include/LO_GEN.labels.md:842` | 0o301115 | 0 |
| `AM1424` | LABEL(md) | `include/LO_GEN.labels.md:849` | 0o301124 | 0 |
| `AM1435` | LABEL(md) | `include/LO_GEN.labels.md:858` | 0o301135 | 0 |
| `AM1442` | LABEL(md) | `include/LO_GEN.labels.md:863` | 0o301142 | 0 |
| `AM1452` | LABEL(md) | `include/LO_GEN.labels.md:871`, `include/LO_GEN.labels.md:1301` | 0o301152 | 0 |
| `AM1453` | LABEL(md) | `include/LO_GEN.labels.md:872` | 0o301153 | 0 |
| `AM1504` | LABEL(md) | `include/LO_GEN.labels.md:897` | 0o301204 | 0 |
| `AM1505` | LABEL(md) | `include/LO_GEN.labels.md:898` | 0o301205 | 0 |
| `AM1506` | LABEL(md) | `include/LO_GEN.labels.md:899` | 0o301206 | 0 |
| `AM1523` | LABEL(md) | `include/LO_GEN.labels.md:912` | 0o301223 | 0 |
| `AM1531` | LABEL(md) | `include/LO_GEN.labels.md:918` | 0o301231 | 0 |
| `AM1540` | LABEL(md) | `include/LO_GEN.labels.md:925` | 0o301240 | 0 |
| `AM1544` | LABEL(md) | `include/LO_GEN.labels.md:929` | 0o301244 | 0 |
| `AM1550` | LABEL(md) | `include/LO_GEN.labels.md:933` | 0o301250 | 0 |
| `AM1553` | LABEL(md) | `include/LO_GEN.labels.md:936` | 0o301253 | 0 |
| `AM1562` | LABEL(md) | `include/LO_GEN.labels.md:943` | 0o301262 | 0 |
| `AM1565` | LABEL(md) | `include/LO_GEN.labels.md:946` | 0o301265 | 0 |
| `AM1572` | LABEL(md) | `include/LO_GEN.labels.md:951` | 0o301272 | 0 |
| `AM1574` | LABEL(md) | `include/LO_GEN.labels.md:953` | 0o301274 | 0 |
| `AM1601` | LABEL(md) | `include/LO_GEN.labels.md:958` | 0o301301 | 0 |
| `AM1611` | LABEL(md) | `include/LO_GEN.labels.md:966` | 0o301311 | 0 |
| `AM1621` | LABEL(md) | `include/LO_GEN.labels.md:974` | 0o301321 | 0 |
| `AM1625` | LABEL(md) | `include/LO_GEN.labels.md:978` | 0o301325 | 0 |
| `AM1644` | LABEL(md) | `include/LO_GEN.labels.md:993` | 0o301344 | 0 |
| `AM1655` | LABEL(md) | `include/LO_GEN.labels.md:1002` | 0o301355 | 0 |
| `AM1657` | LABEL(md) | `include/LO_GEN.labels.md:1004` | 0o301357 | 0 |
| `AM1706` | LABEL(md) | `include/LO_GEN.labels.md:1027` | 0o301406 | 0 |
| `AM1707` | LABEL(md) | `include/LO_GEN.labels.md:1028` | 0o301407 | 0 |
| `AM1743` | LABEL(md) | `include/LO_GEN.labels.md:1056` | 0o301443 | 0 |
| `AM1747` | LABEL(md) | `include/LO_GEN.labels.md:1060` | 0o301447 | 0 |
| `AN0022` | LABEL(md) | `include/LO_GEN.labels.md:79`, `include/LO_GEN.labels.md:1142` | 0o277522 | 0 |
| `AN0150` | LABEL(md) | `include/LO_GEN.labels.md:165`, `include/LO_GEN.labels.md:1142` | 0o277650 | 0 |
| `AN0160` | LABEL(md) | `include/LO_GEN.labels.md:173`, `include/LO_GEN.labels.md:1275` | 0o277660 | 0 |
| `AN0175` | LABEL(md) | `include/LO_GEN.labels.md:186`, `include/LO_GEN.labels.md:1275` | 0o277675 | 0 |
| `AN0201` | LABEL(md) | `include/LO_GEN.labels.md:190`, `include/LO_GEN.labels.md:1160` | 0o277701 | 0 |
| `AN0246` | LABEL(md) | `include/LO_GEN.labels.md:227` | 0o277746 | 0 |
| `AN0275` | LABEL(md) | `include/LO_GEN.labels.md:250`, `include/LO_GEN.labels.md:1171` | 0o277775 | 0 |
| `AN0305` | LABEL(md) | `include/LO_GEN.labels.md:258`, `include/LO_GEN.labels.md:1173` | 0o300005 | 0 |
| `AN0313` | LABEL(md) | `include/LO_GEN.labels.md:264`, `include/LO_GEN.labels.md:1160` | 0o300013 | 0 |
| `AN0326` | LABEL(md) | `include/LO_GEN.labels.md:275` | 0o300026 | 0 |
| `AN0644` | LABEL(md) | `include/LO_GEN.labels.md:481`, `include/LO_GEN.labels.md:1263` | 0o300344 | 0 |
| `AN0646` | LABEL(md) | `include/LO_GEN.labels.md:483`, `include/LO_GEN.labels.md:1212` | 0o300346 | 0 |
| `AN0741` | LABEL(md) | `include/LO_GEN.labels.md:542`, `include/LO_GEN.labels.md:1160` | 0o300441 | 0 |
| `AN0745` | LABEL(md) | `include/LO_GEN.labels.md:546`, `include/LO_GEN.labels.md:1213` | 0o300445 | 0 |
| `AN0755` | LABEL(md) | `include/LO_GEN.labels.md:554` | 0o300455 | 0 |
| `AN0762` | LABEL(md) | `include/LO_GEN.labels.md:559`, `include/LO_GEN.labels.md:1215` | 0o300462 | 0 |
| `AN0772` | LABEL(md) | `include/LO_GEN.labels.md:567`, `include/LO_GEN.labels.md:1222` | 0o300472 | 0 |
| `AN1002` | LABEL(md) | `include/LO_GEN.labels.md:575` | 0o300502 | 0 |
| `AN1007` | LABEL(md) | `include/LO_GEN.labels.md:580` | 0o300507 | 0 |
| `AN1013` | LABEL(md) | `include/LO_GEN.labels.md:584`, `include/LO_GEN.labels.md:1213` | 0o300513 | 0 |
| `AN1016` | LABEL(md) | `include/LO_GEN.labels.md:587` | 0o300516 | 0 |
| `AN1025` | LABEL(md) | `include/LO_GEN.labels.md:594` | 0o300525 | 0 |
| `AN1032` | LABEL(md) | `include/LO_GEN.labels.md:599`, `include/LO_GEN.labels.md:1213` | 0o300532 | 0 |
| `AN1035` | LABEL(md) | `include/LO_GEN.labels.md:602`, `include/LO_GEN.labels.md:1228` | 0o300535 | 0 |
| `AN1053` | LABEL(md) | `include/LO_GEN.labels.md:616` | 0o300553 | 0 |
| `AN1056` | LABEL(md) | `include/LO_GEN.labels.md:619`, `include/LO_GEN.labels.md:1155` | 0o300556 | 0 |
| `AN1064` | LABEL(md) | `include/LO_GEN.labels.md:625`, `include/LO_GEN.labels.md:1233` | 0o300564 | 0 |
| `AN1066` | LABEL(md) | `include/LO_GEN.labels.md:627` | 0o300566 | 0 |
| `AN1076` | LABEL(md) | `include/LO_GEN.labels.md:635` | 0o300576 | 0 |
| `AN1107` | LABEL(md) | `include/LO_GEN.labels.md:644`, `include/LO_GEN.labels.md:1261` | 0o300607 | 0 |
| `AN1113` | LABEL(md) | `include/LO_GEN.labels.md:648` | 0o300613 | 0 |
| `AN1117` | LABEL(md) | `include/LO_GEN.labels.md:652` | 0o300617 | 0 |
| `AN1125` | LABEL(md) | `include/LO_GEN.labels.md:658` | 0o300625 | 0 |
| `AN1137` | LABEL(md) | `include/LO_GEN.labels.md:668`, `include/LO_GEN.labels.md:1212` | 0o300637 | 0 |
| `AN1200` | LABEL(md) | `include/LO_GEN.labels.md:701`, `include/LO_GEN.labels.md:1151` | 0o300700 | 0 |
| `AN1205` | LABEL(md) | `include/LO_GEN.labels.md:706` | 0o300705 | 0 |
| `AN1276` | LABEL(md) | `include/LO_GEN.labels.md:763`, `include/LO_GEN.labels.md:1222` | 0o300776 | 0 |
| `AN1310` | LABEL(md) | `include/LO_GEN.labels.md:773`, `include/LO_GEN.labels.md:1213` | 0o301010 | 0 |
| `AN1364` | LABEL(md) | `include/LO_GEN.labels.md:817` | 0o301064 | 0 |
| `AN1376` | LABEL(md) | `include/LO_GEN.labels.md:827` | 0o301076 | 0 |
| `AN1410` | LABEL(md) | `include/LO_GEN.labels.md:837` | 0o301110 | 0 |
| `AN1422` | LABEL(md) | `include/LO_GEN.labels.md:847` | 0o301122 | 0 |
| `AN1433` | LABEL(md) | `include/LO_GEN.labels.md:856` | 0o301133 | 0 |
| `AN1437` | LABEL(md) | `include/LO_GEN.labels.md:860` | 0o301137 | 0 |
| `AN1444` | LABEL(md) | `include/LO_GEN.labels.md:865` | 0o301144 | 0 |
| `AN1446` | LABEL(md) | `include/LO_GEN.labels.md:867`, `include/LO_GEN.labels.md:1274` | 0o301146 | 0 |
| `AN1511` | LABEL(md) | `include/LO_GEN.labels.md:902` | 0o301211 | 0 |
| `AN1542` | LABEL(md) | `include/LO_GEN.labels.md:927` | 0o301242 | 0 |
| `AN1555` | LABEL(md) | `include/LO_GEN.labels.md:938` | 0o301255 | 0 |
| `AN1567` | LABEL(md) | `include/LO_GEN.labels.md:948` | 0o301267 | 0 |
| `AN1575` | LABEL(md) | `include/LO_GEN.labels.md:954` | 0o301275 | 0 |
| `AN1603` | LABEL(md) | `include/LO_GEN.labels.md:960` | 0o301303 | 0 |
| `AN1612` | LABEL(md) | `include/LO_GEN.labels.md:967` | 0o301312 | 0 |
| `AN1623` | LABEL(md) | `include/LO_GEN.labels.md:976` | 0o301323 | 0 |
| `AN1704` | LABEL(md) | `include/LO_GEN.labels.md:1025` | 0o301404 | 0 |
| `AN1745` | LABEL(md) | `include/LO_GEN.labels.md:1058` | 0o301445 | 0 |
| `AN1756` | LABEL(md) | `include/LO_GEN.labels.md:1067`, `include/LO_GEN.labels.md:1274` | 0o301456 | 0 |
| `B40/1` | LABEL | `src/FOREX_RUNTIME.mad:512` | — | 0 |
| `BN0136` | LABEL(md) | `include/LO_GEN.labels.md:155`, `include/LO_GEN.labels.md:1541` | 0o277636 | 0 |
| `BN0147` | LABEL(md) | `include/LO_GEN.labels.md:164` | 0o277647 | 0 |
| `BN0151` | LABEL(md) | `include/LO_GEN.labels.md:166`, `include/LO_GEN.labels.md:1412` | 0o277651 | 0 |
| `BN0165` | LABEL(md) | `include/LO_GEN.labels.md:178`, `include/LO_GEN.labels.md:1407` | 0o277665 | 0 |
| `BN0173` | LABEL(md) | `include/LO_GEN.labels.md:184`, `include/LO_GEN.labels.md:1412` | 0o277673 | 0 |
| `BN0200` | LABEL(md) | `include/LO_GEN.labels.md:189`, `include/LO_GEN.labels.md:1411` | 0o277700 | 0 |
| `BN0220` | LABEL(md) | `include/LO_GEN.labels.md:205` | 0o277720 | 0 |
| `BN0234` | LABEL(md) | `include/LO_GEN.labels.md:217`, `include/LO_GEN.labels.md:1416` | 0o277734 | 0 |
| `BN0273` | LABEL(md) | `include/LO_GEN.labels.md:248`, `include/LO_GEN.labels.md:1422` | 0o277773 | 0 |
| `BN0312` | LABEL(md) | `include/LO_GEN.labels.md:263`, `include/LO_GEN.labels.md:1425` | 0o300012 | 0 |
| `BN0316` | LABEL(md) | `include/LO_GEN.labels.md:267`, `include/LO_GEN.labels.md:1426` | 0o300016 | 0 |
| `BN0357` | LABEL(md) | `include/LO_GEN.labels.md:300`, `include/LO_GEN.labels.md:1438` | 0o300057 | 0 |
| `BN0640` | LABEL(md) | `include/LO_GEN.labels.md:477`, `include/LO_GEN.labels.md:1441` | 0o300340 | 0 |
| `BN0701` | LABEL(md) | `include/LO_GEN.labels.md:510`, `include/LO_GEN.labels.md:1450` | 0o300401 | 0 |
| `BN1077` | LABEL(md) | `include/LO_GEN.labels.md:636` | 0o300577 | 0 |
| `BN1106` | LABEL(md) | `include/LO_GEN.labels.md:643`, `include/LO_GEN.labels.md:1465` | 0o300606 | 0 |
| `BN1126` | LABEL(md) | `include/LO_GEN.labels.md:659`, `include/LO_GEN.labels.md:1467` | 0o300626 | 0 |
| `BN1147` | LABEL(md) | `include/LO_GEN.labels.md:676`, `include/LO_GEN.labels.md:1474` | 0o300647 | 0 |
| `BN1156` | LABEL(md) | `include/LO_GEN.labels.md:683`, `include/LO_GEN.labels.md:1478` | 0o300656 | 0 |
| `BN1224` | LABEL(md) | `include/LO_GEN.labels.md:721`, `include/LO_GEN.labels.md:1495` | 0o300724 | 0 |
| `BN1525` | LABEL(md) | `include/LO_GEN.labels.md:914`, `include/LO_GEN.labels.md:1516` | 0o301225 | 0 |
| `BSS` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:187`, `src/FOREX_RUNTIME.mad:323`, `include/FOREX.labels.md:357`, `include/LO_GEN.labels.md:1552` | — | 0 |
| `BUFFER` | LABEL(md) | `include/FOREX.labels.md:46` | — | 0 |
| `BW0004` | LABEL(md) | `include/LO_GEN.labels.md:65`, `include/LO_GEN.labels.md:1275` | 0o277504 | 0 |
| `BW0011` | LABEL(md) | `include/LO_GEN.labels.md:70`, `include/LO_GEN.labels.md:1152`, `include/LO_GEN.labels.md:1310` | 0o277511 | 0 |
| `BW0012` | LABEL(md) | `include/LO_GEN.labels.md:71`, `include/LO_GEN.labels.md:1149`, `include/LO_GEN.labels.md:1310` | 0o277512 | 0 |
| `BW0013` | LABEL(md) | `include/LO_GEN.labels.md:72`, `include/LO_GEN.labels.md:1153` | 0o277513 | 0 |
| `BW0020` | LABEL(md) | `include/LO_GEN.labels.md:77`, `include/LO_GEN.labels.md:1146` | 0o277520 | 0 |
| `BW0021` | LABEL(md) | `include/LO_GEN.labels.md:78`, `include/LO_GEN.labels.md:1278` | 0o277521 | 0 |
| `BW0025` | LABEL(md) | `include/LO_GEN.labels.md:82`, `include/LO_GEN.labels.md:1319` | 0o277525 | 0 |
| `BW0026` | LABEL(md) | `include/LO_GEN.labels.md:83`, `include/LO_GEN.labels.md:1311` | 0o277526 | 0 |
| `BW0027` | LABEL(md) | `include/LO_GEN.labels.md:84`, `include/LO_GEN.labels.md:1319` | 0o277527 | 0 |
| `BW0032` | LABEL(md) | `include/LO_GEN.labels.md:87`, `include/LO_GEN.labels.md:1096` | 0o277532 | 0 |
| `BW0033` | LABEL(md) | `include/LO_GEN.labels.md:88` | 0o277533 | 0 |
| `BW0040` | LABEL(md) | `include/LO_GEN.labels.md:93`, `include/LO_GEN.labels.md:1314` | 0o277540 | 0 |
| `BW0042` | LABEL(md) | `include/LO_GEN.labels.md:95` | 0o277542 | 0 |
| `BW0044` | LABEL(md) | `include/LO_GEN.labels.md:97` | 0o277544 | 0 |
| `BW0054` | LABEL(md) | `include/LO_GEN.labels.md:105` | 0o277554 | 0 |
| `BW0055` | LABEL(md) | `include/LO_GEN.labels.md:106`, `include/LO_GEN.labels.md:1328` | 0o277555 | 0 |
| `BW0062` | LABEL(md) | `include/LO_GEN.labels.md:111`, `include/LO_GEN.labels.md:1120` | 0o277562 | 0 |
| `BW0064` | LABEL(md) | `include/LO_GEN.labels.md:113`, `include/LO_GEN.labels.md:1313`, `include/LO_GEN.labels.md:1324` | 0o277564 | 0 |
| `BW0065` | LABEL(md) | `include/LO_GEN.labels.md:114` | 0o277565 | 0 |
| `BW0067` | LABEL(md) | `include/LO_GEN.labels.md:116`, `include/LO_GEN.labels.md:1138` | 0o277567 | 0 |
| `BW0071` | LABEL(md) | `include/LO_GEN.labels.md:118`, `include/LO_GEN.labels.md:1325` | 0o277571 | 0 |
| `BW0110` | LABEL(md) | `include/LO_GEN.labels.md:133` | 0o277610 | 0 |
| `BW0122` | LABEL(md) | `include/LO_GEN.labels.md:143`, `include/LO_GEN.labels.md:1096` | 0o277622 | 0 |
| `BW0176` | LABEL(md) | `include/LO_GEN.labels.md:187` | 0o277676 | 0 |
| `BW0235` | LABEL(md) | `include/LO_GEN.labels.md:218` | 0o277735 | 0 |
| `BW0243` | LABEL(md) | `include/LO_GEN.labels.md:224` | 0o277743 | 0 |
| `BW0255` | LABEL(md) | `include/LO_GEN.labels.md:234` | 0o277755 | 0 |
| `BW0300` | LABEL(md) | `include/LO_GEN.labels.md:253` | 0o300000 | 0 |
| `BW0346` | LABEL(md) | `include/LO_GEN.labels.md:291` | 0o300046 | 0 |
| `BW0370` | LABEL(md) | `include/LO_GEN.labels.md:309` | 0o300070 | 0 |
| `BW0421` | LABEL(md) | `include/LO_GEN.labels.md:334` | 0o300121 | 0 |
| `BW0502` | LABEL(md) | `include/LO_GEN.labels.md:383` | 0o300202 | 0 |
| `BW0503` | LABEL(md) | `include/LO_GEN.labels.md:384` | 0o300203 | 0 |
| `BW0504` | LABEL(md) | `include/LO_GEN.labels.md:385` | 0o300204 | 0 |
| `BW0505` | LABEL(md) | `include/LO_GEN.labels.md:386` | 0o300205 | 0 |
| `BW0510` | LABEL(md) | `include/LO_GEN.labels.md:389` | 0o300210 | 0 |
| `BW0513` | LABEL(md) | `include/LO_GEN.labels.md:392` | 0o300213 | 0 |
| `BW0626` | LABEL(md) | `include/LO_GEN.labels.md:467`, `include/LO_GEN.labels.md:1131` | 0o300326 | 0 |
| `BW0632` | LABEL(md) | `include/LO_GEN.labels.md:471` | 0o300332 | 0 |
| `BW0635` | LABEL(md) | `include/LO_GEN.labels.md:474`, `include/LO_GEN.labels.md:1140` | 0o300335 | 0 |
| `BW0673` | LABEL(md) | `include/LO_GEN.labels.md:504`, `include/LO_GEN.labels.md:1125` | 0o300373 | 0 |
| `BW0705` | LABEL(md) | `include/LO_GEN.labels.md:514`, `include/LO_GEN.labels.md:1327` | 0o300405 | 0 |
| `BW0742` | LABEL(md) | `include/LO_GEN.labels.md:543` | 0o300442 | 0 |
| `BW0746` | LABEL(md) | `include/LO_GEN.labels.md:547` | 0o300446 | 0 |
| `BW0756` | LABEL(md) | `include/LO_GEN.labels.md:555` | 0o300456 | 0 |
| `BW0773` | LABEL(md) | `include/LO_GEN.labels.md:568` | 0o300473 | 0 |
| `BW1010` | LABEL(md) | `include/LO_GEN.labels.md:581` | 0o300510 | 0 |
| `BW1014` | LABEL(md) | `include/LO_GEN.labels.md:585` | 0o300514 | 0 |
| `BW1026` | LABEL(md) | `include/LO_GEN.labels.md:595` | 0o300526 | 0 |
| `BW1027` | LABEL(md) | `include/LO_GEN.labels.md:596` | 0o300527 | 0 |
| `BW1033` | LABEL(md) | `include/LO_GEN.labels.md:600` | 0o300533 | 0 |
| `BW1036` | LABEL(md) | `include/LO_GEN.labels.md:603` | 0o300536 | 0 |
| `BW1054` | LABEL(md) | `include/LO_GEN.labels.md:617` | 0o300554 | 0 |
| `BW1057` | LABEL(md) | `include/LO_GEN.labels.md:620` | 0o300557 | 0 |
| `BW1065` | LABEL(md) | `include/LO_GEN.labels.md:626` | 0o300565 | 0 |
| `BW1073` | LABEL(md) | `include/LO_GEN.labels.md:632` | 0o300573 | 0 |
| `BW1114` | LABEL(md) | `include/LO_GEN.labels.md:649` | 0o300614 | 0 |
| `BW1206` | LABEL(md) | `include/LO_GEN.labels.md:707` | 0o300706 | 0 |
| `BW1212` | LABEL(md) | `include/LO_GEN.labels.md:711` | 0o300712 | 0 |
| `BW1221` | LABEL(md) | `include/LO_GEN.labels.md:718` | 0o300721 | 0 |
| `BW1251` | LABEL(md) | `include/LO_GEN.labels.md:742`, `include/LO_GEN.labels.md:1139` | 0o300751 | 0 |
| `BW1277` | LABEL(md) | `include/LO_GEN.labels.md:764` | 0o300777 | 0 |
| `BW1311` | LABEL(md) | `include/LO_GEN.labels.md:774` | 0o301011 | 0 |
| `BW1323` | LABEL(md) | `include/LO_GEN.labels.md:784` | 0o301023 | 0 |
| `BW1333` | LABEL(md) | `include/LO_GEN.labels.md:792` | 0o301033 | 0 |
| `BW1351` | LABEL(md) | `include/LO_GEN.labels.md:806` | 0o301051 | 0 |
| `BW1353` | LABEL(md) | `include/LO_GEN.labels.md:808` | 0o301053 | 0 |
| `BW1365` | LABEL(md) | `include/LO_GEN.labels.md:818` | 0o301065 | 0 |
| `BW1377` | LABEL(md) | `include/LO_GEN.labels.md:828` | 0o301077 | 0 |
| `BW1411` | LABEL(md) | `include/LO_GEN.labels.md:838` | 0o301111 | 0 |
| `BW1423` | LABEL(md) | `include/LO_GEN.labels.md:848` | 0o301123 | 0 |
| `BW1434` | LABEL(md) | `include/LO_GEN.labels.md:857` | 0o301134 | 0 |
| `BW1440` | LABEL(md) | `include/LO_GEN.labels.md:861` | 0o301140 | 0 |
| `BW1445` | LABEL(md) | `include/LO_GEN.labels.md:866` | 0o301145 | 0 |
| `BW1450` | LABEL(md) | `include/LO_GEN.labels.md:869` | 0o301150 | 0 |
| `BW1512` | LABEL(md) | `include/LO_GEN.labels.md:903` | 0o301212 | 0 |
| `BW1520` | LABEL(md) | `include/LO_GEN.labels.md:909` | 0o301220 | 0 |
| `BW1533` | LABEL(md) | `include/LO_GEN.labels.md:920` | 0o301233 | 0 |
| `BW1543` | LABEL(md) | `include/LO_GEN.labels.md:928` | 0o301243 | 0 |
| `BW1547` | LABEL(md) | `include/LO_GEN.labels.md:932` | 0o301247 | 0 |
| `BW1556` | LABEL(md) | `include/LO_GEN.labels.md:939` | 0o301256 | 0 |
| `BW1561` | LABEL(md) | `include/LO_GEN.labels.md:942` | 0o301261 | 0 |
| `BW1570` | LABEL(md) | `include/LO_GEN.labels.md:949` | 0o301270 | 0 |
| `BW1604` | LABEL(md) | `include/LO_GEN.labels.md:961` | 0o301304 | 0 |
| `BW1624` | LABEL(md) | `include/LO_GEN.labels.md:977` | 0o301324 | 0 |
| `BW1636` | LABEL(md) | `include/LO_GEN.labels.md:987`, `include/LO_GEN.labels.md:1139` | 0o301336 | 0 |
| `BW1650` | LABEL(md) | `include/LO_GEN.labels.md:997` | 0o301350 | 0 |
| `BW1653` | LABEL(md) | `include/LO_GEN.labels.md:1000` | 0o301353 | 0 |
| `BW1654` | LABEL(md) | `include/LO_GEN.labels.md:1001` | 0o301354 | 0 |
| `BW1662` | LABEL(md) | `include/LO_GEN.labels.md:1007` | 0o301362 | 0 |
| `BW1671` | LABEL(md) | `include/LO_GEN.labels.md:1014` | 0o301371 | 0 |
| `BW1676` | LABEL(md) | `include/LO_GEN.labels.md:1019` | 0o301376 | 0 |
| `BW1677` | LABEL(md) | `include/LO_GEN.labels.md:1020` | 0o301377 | 0 |
| `BW1700` | LABEL(md) | `include/LO_GEN.labels.md:1021` | 0o301400 | 0 |
| `BW1701` | LABEL(md) | `include/LO_GEN.labels.md:1022`, `include/LO_GEN.labels.md:1097` | 0o301401 | 0 |
| `BW1702` | LABEL(md) | `include/LO_GEN.labels.md:1023` | 0o301402 | 0 |
| `BW1711` | LABEL(md) | `include/LO_GEN.labels.md:1030` | 0o301411 | 0 |
| `BW1721` | LABEL(md) | `include/LO_GEN.labels.md:1038`, `include/LO_GEN.labels.md:1134` | 0o301421 | 0 |
| `BW1727` | LABEL(md) | `include/LO_GEN.labels.md:1044` | 0o301427 | 0 |
| `BW1741` | LABEL(md) | `include/LO_GEN.labels.md:1054` | 0o301441 | 0 |
| `BW1746` | LABEL(md) | `include/LO_GEN.labels.md:1059` | 0o301446 | 0 |
| `BW1765` | LABEL(md) | `include/LO_GEN.labels.md:1074` | 0o301465 | 0 |
| `BW1766` | LABEL(md) | `include/LO_GEN.labels.md:1075` | 0o301466 | 0 |
| `BZ0074` | LABEL(md) | `include/LO_GEN.labels.md:121`, `include/LO_GEN.labels.md:1540` | 0o277574 | 0 |
| `BZ0077` | LABEL(md) | `include/LO_GEN.labels.md:124`, `include/LO_GEN.labels.md:1401` | 0o277577 | 0 |
| `BZ0106` | LABEL(md) | `include/LO_GEN.labels.md:131`, `include/LO_GEN.labels.md:1403` | 0o277606 | 0 |
| `BZ0157` | LABEL(md) | `include/LO_GEN.labels.md:172`, `include/LO_GEN.labels.md:1412` | 0o277657 | 0 |
| `BZ0250` | LABEL(md) | `include/LO_GEN.labels.md:229`, `include/LO_GEN.labels.md:1417` | 0o277750 | 0 |
| `BZ0276` | LABEL(md) | `include/LO_GEN.labels.md:251`, `include/LO_GEN.labels.md:1422` | 0o277776 | 0 |
| `BZ0304` | LABEL(md) | `include/LO_GEN.labels.md:257`, `include/LO_GEN.labels.md:1424` | 0o300004 | 0 |
| `BZ0336` | LABEL(md) | `include/LO_GEN.labels.md:283`, `include/LO_GEN.labels.md:1412` | 0o300036 | 0 |
| `BZ0675` | LABEL(md) | `include/LO_GEN.labels.md:506`, `include/LO_GEN.labels.md:1514` | 0o300375 | 0 |
| `BZ0711` | LABEL(md) | `include/LO_GEN.labels.md:518` | 0o300411 | 0 |
| `BZ0724` | LABEL(md) | `include/LO_GEN.labels.md:529`, `include/LO_GEN.labels.md:1525` | 0o300424 | 0 |
| `BZ1202` | LABEL(md) | `include/LO_GEN.labels.md:703`, `include/LO_GEN.labels.md:1486` | 0o300702 | 0 |
| `BZ1231` | LABEL(md) | `include/LO_GEN.labels.md:726`, `include/LO_GEN.labels.md:1490` | 0o300731 | 0 |
| `BZ1234` | LABEL(md) | `include/LO_GEN.labels.md:729`, `include/LO_GEN.labels.md:1491` | 0o300734 | 0 |
| `BZ1241` | LABEL(md) | `include/LO_GEN.labels.md:734`, `include/LO_GEN.labels.md:1492` | 0o300741 | 0 |
| `BZ1244` | LABEL(md) | `include/LO_GEN.labels.md:737`, `include/LO_GEN.labels.md:1493` | 0o300744 | 0 |
| `BZ1255` | LABEL(md) | `include/LO_GEN.labels.md:746`, `include/LO_GEN.labels.md:1496` | 0o300755 | 0 |
| `BZ1260` | LABEL(md) | `include/LO_GEN.labels.md:749`, `include/LO_GEN.labels.md:1497` | 0o300760 | 0 |
| `BZ1267` | LABEL(md) | `include/LO_GEN.labels.md:756`, `include/LO_GEN.labels.md:1499` | 0o300767 | 0 |
| `BZ1600` | LABEL(md) | `include/LO_GEN.labels.md:957`, `include/LO_GEN.labels.md:1519` | 0o301300 | 0 |
| `BZ1627` | LABEL(md) | `include/LO_GEN.labels.md:980`, `include/LO_GEN.labels.md:1522` | 0o301327 | 0 |
| `BZ1767` | LABEL(md) | `include/LO_GEN.labels.md:1076`, `include/LO_GEN.labels.md:1542` | 0o301467 | 0 |
| `BZ1776` | LABEL(md) | `include/LO_GEN.labels.md:1083`, `include/LO_GEN.labels.md:1094` | 0o301476 | 0 |
| `C076` | LABEL | `src/FOREX_RUNTIME_DISASM.mad:384` | — | 0 |
| `C1/10` | LABEL | `src/FOREX_RUNTIME.mad:514` | — | 0 |
| `COMEQ` | LABEL(md)/SUBP | `include/FOREX_ROOT.mad:75`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | — | 0 |
| `COMMON` | LABEL(md) | `include/LO_GEN.labels.md:1552` | 0o4000 | 0 |
| `CONST` | LABEL(md)/SUBP | `include/FOREX_ROOT.mad:74`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | — | 0 |
| `CYCL` | XREF(md) | `include/RUNTIME_DECODER.xref.md:22` | — | 0 |
| `DARET` | LABEL(md)/XREF(md) | `include/FOREX.labels.md:60`, `include/RUNTIME_DECODER.xref.md:15` | — | 0 |
| `DATA` | XREF(md) | `include/RUNTIME_DECODER.xref.md:13` | — | 0 |
| `DATE` | LABEL(md)/XREF(md) | `include/FOREX.labels.md:59`, `include/RUNTIME_DECODER.xref.md:14` | — | 0 |
| `DATEFM` | LABEL(md) | `include/FOREX.labels.md:454` | — | 0 |
| `DATE_BLOCK` | XREF(md) | `include/RUNTIME_DECODER.xref.md:13` | — | 0 |
| `DATE_EXIT` | XREF(md) | `include/RUNTIME_DECODER.xref.md:19` | — | 0 |
| `DATE_GET` | XREF(md) | `include/RUNTIME_DECODER.xref.md:14` | — | 0 |
| `DATE_LOOP1` | XREF(md) | `include/RUNTIME_DECODER.xref.md:16` | — | 0 |
| `DATE_LOOP2` | XREF(md) | `include/RUNTIME_DECODER.xref.md:17` | — | 0 |
| `DATE_PARSE` | XREF(md) | `include/RUNTIME_DECODER.xref.md:15` | — | 0 |
| `DATE_PREPARE` | XREF(md) | `include/RUNTIME_DECODER.xref.md:18` | — | 0 |
| `DATE_PRINT` | XREF(md) | `include/RUNTIME_DECODER.xref.md:12` | — | 0 |
| `DEC_15` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:26`, `include/FOREX.labels.md:314` | 15 | 0 |
| `DMON` | LABEL(md) | `include/LO_GEN.labels.md:30`, `include/LO_GEN.labels.md:30`, `include/LO_GEN.labels.md:1553` | — | 0 |
| `DP026` | ENTRY/XREF(md) | `src/FOREX_DECODER_DISASM.mad:205`, `include/RUNTIME_DECODER.xref.md:18` | — | 0 |
| `DPP8` | SUBP/XREF(md) | `src/FOREX_DECODER_DISASM.mad:145`, `include/RUNTIME_DECODER.xref.md:20` | — | 0 |
| `DPREPA` | ENTRY/LABEL(md) | `src/FOREX_RUNTIME.mad:389`, `include/FOREX.labels.md:63`, `include/FOREX.labels.md:459` | — | 0 |
| `DT0035` | LABEL(md) | `include/LO_GEN.labels.md:90`, `include/LO_GEN.labels.md:1229`, `include/LO_GEN.labels.md:1316` | 0o277535 | 0 |
| `DT0036` | LABEL(md) | `include/LO_GEN.labels.md:91`, `include/LO_GEN.labels.md:1214`, `include/LO_GEN.labels.md:1316` | 0o277536 | 0 |
| `DT0041` | LABEL(md) | `include/LO_GEN.labels.md:94`, `include/LO_GEN.labels.md:1315` | 0o277541 | 0 |
| `DT0043` | LABEL(md) | `include/LO_GEN.labels.md:96`, `include/LO_GEN.labels.md:1288`, `include/LO_GEN.labels.md:1317` | 0o277543 | 0 |
| `DT0045` | LABEL(md) | `include/LO_GEN.labels.md:98`, `include/LO_GEN.labels.md:1287`, `include/LO_GEN.labels.md:1317` | 0o277545 | 0 |
| `DT0047` | LABEL(md) | `include/LO_GEN.labels.md:100`, `include/LO_GEN.labels.md:1220` | 0o277547 | 0 |
| `DT0050` | LABEL(md) | `include/LO_GEN.labels.md:101`, `include/LO_GEN.labels.md:1227`, `include/LO_GEN.labels.md:1309` | 0o277550 | 0 |
| `DT0052` | LABEL(md) | `include/LO_GEN.labels.md:103`, `include/LO_GEN.labels.md:1226`, `include/LO_GEN.labels.md:1308` | 0o277552 | 0 |
| `DT0056` | LABEL(md) | `include/LO_GEN.labels.md:107`, `include/LO_GEN.labels.md:1218` | 0o277556 | 0 |
| `DT0140` | LABEL(md) | `include/LO_GEN.labels.md:157`, `include/LO_GEN.labels.md:1115`, `include/LO_GEN.labels.md:1319` | 0o277640 | 0 |
| `DT0141` | LABEL(md) | `include/LO_GEN.labels.md:158`, `include/LO_GEN.labels.md:1097`, `include/LO_GEN.labels.md:1309` | 0o277641 | 0 |
| `DT0143` | LABEL(md) | `include/LO_GEN.labels.md:160`, `include/LO_GEN.labels.md:1110`, `include/LO_GEN.labels.md:1309` | 0o277643 | 0 |
| `DT0203` | LABEL(md) | `include/LO_GEN.labels.md:192`, `include/LO_GEN.labels.md:1161` | 0o277703 | 0 |
| `DT0254` | LABEL(md) | `include/LO_GEN.labels.md:233`, `include/LO_GEN.labels.md:1115` | 0o277754 | 0 |
| `DT0263` | LABEL(md) | `include/LO_GEN.labels.md:240`, `include/LO_GEN.labels.md:1115`, `include/LO_GEN.labels.md:1320` | 0o277763 | 0 |
| `DT0320` | LABEL(md) | `include/LO_GEN.labels.md:269`, `include/LO_GEN.labels.md:1110` | 0o300020 | 0 |
| `DT0747` | LABEL(md) | `include/LO_GEN.labels.md:548` | 0o300447 | 0 |
| `DT1060` | LABEL(md) | `include/LO_GEN.labels.md:621` | 0o300560 | 0 |
| `DT1121` | LABEL(md) | `include/LO_GEN.labels.md:654` | 0o300621 | 0 |
| `DT1336` | LABEL(md) | `include/LO_GEN.labels.md:795`, `include/LO_GEN.labels.md:1136` | 0o301036 | 0 |
| `DT1420` | LABEL(md) | `include/LO_GEN.labels.md:845` | 0o301120 | 0 |
| `DT1513` | LABEL(md) | `include/LO_GEN.labels.md:904`, `include/LO_GEN.labels.md:1097` | 0o301213 | 0 |
| `DT1526` | LABEL(md) | `include/LO_GEN.labels.md:915`, `include/LO_GEN.labels.md:1151` | 0o301226 | 0 |
| `DT1573` | LABEL(md) | `include/LO_GEN.labels.md:952` | 0o301273 | 0 |
| `DT1646` | LABEL(md) | `include/LO_GEN.labels.md:995` | 0o301346 | 0 |
| `DT1737` | LABEL(md) | `include/LO_GEN.labels.md:1052` | 0o301437 | 0 |
| `DT1763` | LABEL(md) | `include/LO_GEN.labels.md:1072` | 0o301463 | 0 |
| `DUMON` | LABEL(md) | `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:373`, `include/FOREX.labels.md:698`, `include/FOREX.labels.md:698`, `include/LO_GEN.labels.md:30` | — | 0 |
| `DV0007` | LABEL(md) | `include/LO_GEN.labels.md:68`, `include/LO_GEN.labels.md:1179` | 0o277507 | 0 |
| `ENTOVL` | LABEL/LABEL(md) | `src/LO_SYN.mad:765`, `include/LO_SYN.labels.md:11` | — | 0 |
| `EQU` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `ERRTRL` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:311`, `include/FOREX_ROOT.mad:134`, `include/FOREX.labels.md:31`, `include/FOREX.labels.md:82`, `include/FOREX.labels.md:476` | — | 0 |
| `ERR_TRANSLATOR` | XREF(md) | `include/RUNTIME_DECODER.xref.md:36` | 0o074011 | 0 |
| `EXT_` | LABEL(md) | `include/LO_SYN.labels.md:45` | — | 0 |
| `FL*SAV` | LABEL(md) | `include/FOREX.labels.md:88` | — | 0 |
| `FLASMB` | LABEL(md) | `include/FOREX.labels.md:56` | — | 0 |
| `FLCMPR` | LABEL(md) | `include/FOREX.labels.md:54` | — | 0 |
| `FLGEX` | LABEL(md) | `include/FOREX.labels.md:703` | — | 0 |
| `FLMASK` | LABEL(md) | `include/FOREX.labels.md:55` | — | 0 |
| `FLSHIN` | LABEL(md) | `include/FOREX.labels.md:53` | — | 0 |
| `FLSIGC` | LABEL(md) | `include/FOREX.labels.md:49` | — | 0 |
| `FLXORL` | LABEL(md) | `include/FOREX.labels.md:50` | — | 0 |
| `FMT027` | XREF(md) | `include/RUNTIME_DISASM.xref.md:63` | — | 0 |
| `FMTCST` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:193`, `include/RUNTIME_DISASM.xref.md:68` | — | 0 |
| `FMTEND` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:195`, `include/RUNTIME_DISASM.xref.md:70` | — | 0 |
| `FMTENT` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:144`, `include/RUNTIME_DISASM.xref.md:57` | — | 0 |
| `FMTLST` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:189`, `include/RUNTIME_DISASM.xref.md:65` | — | 0 |
| `FMTNAM` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:191`, `include/RUNTIME_DISASM.xref.md:66` | — | 0 |
| `FMTTAB` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:167`, `include/RUNTIME_DISASM.xref.md:64` | — | 0 |
| `FMTXLT` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:192`, `include/RUNTIME_DISASM.xref.md:67` | — | 0 |
| `FMTXNM` | LABEL/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:194`, `include/RUNTIME_DISASM.xref.md:69` | — | 0 |
| `FOREX` | LABEL(md)/SUBP | `src/LO_SYN.mad:32`, `include/FOREX_ROOT.mad:73`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:700`, `include/FOREX.labels.md:704` | — | 0 |
| `FOREX*` | NAME/SUBP | `src/LO_GEN.mad:33`, `include/FOREX_ROOT.mad:61` | — | 0 |
| `FORMAT` | LABEL(md)/XREF(md) | `include/FOREX.labels.md:38`, `include/RUNTIME_DISASM.xref.md:10` | — | 0 |
| `FORTLIBR` | XREF(md) | `include/RUNTIME_DISASM.xref.md:11` | 0o510543 | 0 |
| `FT` | XREF(md) | `include/RUNTIME_DISASM.xref.md:10` | 0o510443 | 0 |
| `FTDISP` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:120`, `include/FOREX.labels.md:38`, `include/FOREX.labels.md:509` | — | 0 |
| `FTDTEN` | LABEL(md) | `include/FOREX.labels.md:504` | — | 0 |
| `FTLIO` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:193`, `include/FOREX.labels.md:45`, `include/FOREX.labels.md:510` | — | 0 |
| `FXCOR` | LABEL(md)/NAME | `src/FOREX_CORE.mad:145`, `include/FOREX.labels.md:19`, `include/FOREX.labels.md:19`, `include/FOREX.labels.md:487` | NEW DTRAN | 0 |
| `FXSTR` | ENTRY/LABEL(md) | `src/FOREX_CORE.mad:146`, `include/FOREX.labels.md:20`, `include/FOREX.labels.md:488` | — | 0 |
| `GOST` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `HD0000` | LABEL/LABEL(md) | `src/LO_GEN.mad:541`, `include/LO_GEN.labels.md:61`, `include/LO_GEN.labels.md:1293` | — | 0 |
| `HD0001` | LABEL/LABEL(md) | `src/LO_GEN.mad:543`, `include/LO_GEN.labels.md:31`, `include/LO_GEN.labels.md:62`, `include/LO_GEN.labels.md:1294` | — | 0 |
| `HD0002` | LABEL/LABEL(md) | `src/LO_GEN.mad:545`, `include/LO_GEN.labels.md:63`, `include/LO_GEN.labels.md:1296` | — | 0 |
| `HD0003` | LABEL/LABEL(md) | `src/LO_GEN.mad:547`, `include/LO_GEN.labels.md:64`, `include/LO_GEN.labels.md:1295` | — | 0 |
| `IFLOD` | LABEL(md) | `include/FOREX.labels.md:520` | — | 0 |
| `INITFO` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:191`, `include/FOREX_ROOT.mad:79`, `include/FOREX.labels.md:26`, `include/FOREX.labels.md:77`, `include/FOREX.labels.md:523`, `include/FOREX.labels.md:699` | — | 0 |
| `INIT_FOREX` | XREF(md) | `include/RUNTIME_DECODER.xref.md:34`, `include/RUNTIME_DECODER.xref.md:37` | 0o074010 | 0 |
| `ISO` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `JP0030` | LABEL(md) | `include/LO_GEN.labels.md:85`, `include/LO_GEN.labels.md:1318`, `include/LO_GEN.labels.md:1540` | 0o277530 | 0 |
| `JP0034` | LABEL(md) | `include/LO_GEN.labels.md:89`, `include/LO_GEN.labels.md:1318`, `include/LO_GEN.labels.md:1399` | 0o277534 | 0 |
| `JP0046` | LABEL(md) | `include/LO_GEN.labels.md:99`, `include/LO_GEN.labels.md:1400` | 0o277546 | 0 |
| `JP0101` | LABEL(md) | `include/LO_GEN.labels.md:126` | 0o277601 | 0 |
| `JP0115` | LABEL(md) | `include/LO_GEN.labels.md:138`, `include/LO_GEN.labels.md:1541` | 0o277615 | 0 |
| `JP0133` | LABEL(md) | `include/LO_GEN.labels.md:152`, `include/LO_GEN.labels.md:1541` | 0o277633 | 0 |
| `JP0205` | LABEL(md) | `include/LO_GEN.labels.md:194` | 0o277705 | 0 |
| `JP0224` | LABEL(md) | `include/LO_GEN.labels.md:209` | 0o277724 | 0 |
| `JP0231` | LABEL(md) | `include/LO_GEN.labels.md:214` | 0o277731 | 0 |
| `JP0244` | LABEL(md) | `include/LO_GEN.labels.md:225` | 0o277744 | 0 |
| `JP0253` | LABEL(md) | `include/LO_GEN.labels.md:232`, `include/LO_GEN.labels.md:1421` | 0o277753 | 0 |
| `JP0261` | LABEL(md) | `include/LO_GEN.labels.md:238`, `include/LO_GEN.labels.md:1420` | 0o277761 | 0 |
| `JP0301` | LABEL(md) | `include/LO_GEN.labels.md:254` | 0o300001 | 0 |
| `JP0307` | LABEL(md) | `include/LO_GEN.labels.md:260`, `include/LO_GEN.labels.md:1428` | 0o300007 | 0 |
| `JP0321` | LABEL(md) | `include/LO_GEN.labels.md:270`, `include/LO_GEN.labels.md:1427` | 0o300021 | 0 |
| `JP0340` | LABEL(md) | `include/LO_GEN.labels.md:285` | 0o300040 | 0 |
| `JP0342` | LABEL(md) | `include/LO_GEN.labels.md:287` | 0o300042 | 0 |
| `JP0350` | LABEL(md) | `include/LO_GEN.labels.md:293` | 0o300050 | 0 |
| `JP0354` | LABEL(md) | `include/LO_GEN.labels.md:297` | 0o300054 | 0 |
| `JP0367` | LABEL(md) | `include/LO_GEN.labels.md:308` | 0o300067 | 0 |
| `JP0371` | LABEL(md) | `include/LO_GEN.labels.md:310`, `include/LO_GEN.labels.md:1402` | 0o300071 | 0 |
| `JP0372` | LABEL(md) | `include/LO_GEN.labels.md:311`, `include/LO_GEN.labels.md:1404` | 0o300072 | 0 |
| `JP0373` | LABEL(md) | `include/LO_GEN.labels.md:312`, `include/LO_GEN.labels.md:1406` | 0o300073 | 0 |
| `JP0374` | LABEL(md) | `include/LO_GEN.labels.md:313`, `include/LO_GEN.labels.md:1410` | 0o300074 | 0 |
| `JP0375` | LABEL(md) | `include/LO_GEN.labels.md:314`, `include/LO_GEN.labels.md:1413` | 0o300075 | 0 |
| `JP0376` | LABEL(md) | `include/LO_GEN.labels.md:315`, `include/LO_GEN.labels.md:1423` | 0o300076 | 0 |
| `JP0377` | LABEL(md) | `include/LO_GEN.labels.md:316`, `include/LO_GEN.labels.md:1540` | 0o300077 | 0 |
| `JP0400` | LABEL(md) | `include/LO_GEN.labels.md:317`, `include/LO_GEN.labels.md:1540` | 0o300100 | 0 |
| `JP0401` | LABEL(md) | `include/LO_GEN.labels.md:318`, `include/LO_GEN.labels.md:1414` | 0o300101 | 0 |
| `JP0402` | LABEL(md) | `include/LO_GEN.labels.md:319`, `include/LO_GEN.labels.md:1431` | 0o300102 | 0 |
| `JP0403` | LABEL(md) | `include/LO_GEN.labels.md:320`, `include/LO_GEN.labels.md:1432` | 0o300103 | 0 |
| `JP0404` | LABEL(md) | `include/LO_GEN.labels.md:321` | 0o300104 | 0 |
| `JP0405` | LABEL(md) | `include/LO_GEN.labels.md:322` | 0o300105 | 0 |
| `JP0406` | LABEL(md) | `include/LO_GEN.labels.md:323`, `include/LO_GEN.labels.md:1439` | 0o300106 | 0 |
| `JP0407` | LABEL(md) | `include/LO_GEN.labels.md:324`, `include/LO_GEN.labels.md:1445` | 0o300107 | 0 |
| `JP0410` | LABEL(md) | `include/LO_GEN.labels.md:325`, `include/LO_GEN.labels.md:1446` | 0o300110 | 0 |
| `JP0415` | LABEL(md) | `include/LO_GEN.labels.md:330`, `include/LO_GEN.labels.md:1433` | 0o300115 | 0 |
| `JP0416` | LABEL(md) | `include/LO_GEN.labels.md:331`, `include/LO_GEN.labels.md:1437` | 0o300116 | 0 |
| `JP0417` | LABEL(md) | `include/LO_GEN.labels.md:332`, `include/LO_GEN.labels.md:1436` | 0o300117 | 0 |
| `JP0420` | LABEL(md) | `include/LO_GEN.labels.md:333`, `include/LO_GEN.labels.md:1451` | 0o300120 | 0 |
| `JP0422` | LABEL(md) | `include/LO_GEN.labels.md:335`, `include/LO_GEN.labels.md:1452` | 0o300122 | 0 |
| `JP0423` | LABEL(md) | `include/LO_GEN.labels.md:336`, `include/LO_GEN.labels.md:1453` | 0o300123 | 0 |
| `JP0424` | LABEL(md) | `include/LO_GEN.labels.md:337`, `include/LO_GEN.labels.md:1454` | 0o300124 | 0 |
| `JP0425` | LABEL(md) | `include/LO_GEN.labels.md:338`, `include/LO_GEN.labels.md:1475` | 0o300125 | 0 |
| `JP0426` | LABEL(md) | `include/LO_GEN.labels.md:339`, `include/LO_GEN.labels.md:1476` | 0o300126 | 0 |
| `JP0427` | LABEL(md) | `include/LO_GEN.labels.md:340`, `include/LO_GEN.labels.md:1455` | 0o300127 | 0 |
| `JP0430` | LABEL(md) | `include/LO_GEN.labels.md:341`, `include/LO_GEN.labels.md:1461` | 0o300130 | 0 |
| `JP0431` | LABEL(md) | `include/LO_GEN.labels.md:342`, `include/LO_GEN.labels.md:1456` | 0o300131 | 0 |
| `JP0432` | LABEL(md) | `include/LO_GEN.labels.md:343`, `include/LO_GEN.labels.md:1457` | 0o300132 | 0 |
| `JP0433` | LABEL(md) | `include/LO_GEN.labels.md:344`, `include/LO_GEN.labels.md:1459` | 0o300133 | 0 |
| `JP0434` | LABEL(md) | `include/LO_GEN.labels.md:345`, `include/LO_GEN.labels.md:1440` | 0o300134 | 0 |
| `JP0435` | LABEL(md) | `include/LO_GEN.labels.md:346`, `include/LO_GEN.labels.md:1471` | 0o300135 | 0 |
| `JP0436` | LABEL(md) | `include/LO_GEN.labels.md:347`, `include/LO_GEN.labels.md:1468` | 0o300136 | 0 |
| `JP0437` | LABEL(md) | `include/LO_GEN.labels.md:348`, `include/LO_GEN.labels.md:1462` | 0o300137 | 0 |
| `JP0440` | LABEL(md) | `include/LO_GEN.labels.md:349`, `include/LO_GEN.labels.md:1472` | 0o300140 | 0 |
| `JP0441` | LABEL(md) | `include/LO_GEN.labels.md:350`, `include/LO_GEN.labels.md:1469` | 0o300141 | 0 |
| `JP0442` | LABEL(md) | `include/LO_GEN.labels.md:351`, `include/LO_GEN.labels.md:1463` | 0o300142 | 0 |
| `JP0443` | LABEL(md) | `include/LO_GEN.labels.md:352`, `include/LO_GEN.labels.md:1463` | 0o300143 | 0 |
| `JP0444` | LABEL(md) | `include/LO_GEN.labels.md:353`, `include/LO_GEN.labels.md:1462` | 0o300144 | 0 |
| `JP0445` | LABEL(md) | `include/LO_GEN.labels.md:354`, `include/LO_GEN.labels.md:1479` | 0o300145 | 0 |
| `JP0446` | LABEL(md) | `include/LO_GEN.labels.md:355`, `include/LO_GEN.labels.md:1485` | 0o300146 | 0 |
| `JP0447` | LABEL(md) | `include/LO_GEN.labels.md:356`, `include/LO_GEN.labels.md:1487` | 0o300147 | 0 |
| `JP0450` | LABEL(md) | `include/LO_GEN.labels.md:357`, `include/LO_GEN.labels.md:1481` | 0o300150 | 0 |
| `JP0451` | LABEL(md) | `include/LO_GEN.labels.md:358`, `include/LO_GEN.labels.md:1488` | 0o300151 | 0 |
| `JP0463` | LABEL(md) | `include/LO_GEN.labels.md:368`, `include/LO_GEN.labels.md:1507` | 0o300163 | 0 |
| `JP0464` | LABEL(md) | `include/LO_GEN.labels.md:369`, `include/LO_GEN.labels.md:1460` | 0o300164 | 0 |
| `JP0465` | LABEL(md) | `include/LO_GEN.labels.md:370` | 0o300165 | 0 |
| `JP0466` | LABEL(md) | `include/LO_GEN.labels.md:371` | 0o300166 | 0 |
| `JP0467` | LABEL(md) | `include/LO_GEN.labels.md:372`, `include/LO_GEN.labels.md:1508` | 0o300167 | 0 |
| `JP0470` | LABEL(md) | `include/LO_GEN.labels.md:373`, `include/LO_GEN.labels.md:1509` | 0o300170 | 0 |
| `JP0471` | LABEL(md) | `include/LO_GEN.labels.md:374`, `include/LO_GEN.labels.md:1512` | 0o300171 | 0 |
| `JP0472` | LABEL(md) | `include/LO_GEN.labels.md:375` | 0o300172 | 0 |
| `JP0473` | LABEL(md) | `include/LO_GEN.labels.md:376` | 0o300173 | 0 |
| `JP0500` | LABEL(md) | `include/LO_GEN.labels.md:381`, `include/LO_GEN.labels.md:1523` | 0o300200 | 0 |
| `JP0501` | LABEL(md) | `include/LO_GEN.labels.md:382`, `include/LO_GEN.labels.md:1524` | 0o300201 | 0 |
| `JP0506` | LABEL(md) | `include/LO_GEN.labels.md:387`, `include/LO_GEN.labels.md:1431` | 0o300206 | 0 |
| `JP0507` | LABEL(md) | `include/LO_GEN.labels.md:388`, `include/LO_GEN.labels.md:1515` | 0o300207 | 0 |
| `JP0511` | LABEL(md) | `include/LO_GEN.labels.md:390`, `include/LO_GEN.labels.md:1431` | 0o300211 | 0 |
| `JP0512` | LABEL(md) | `include/LO_GEN.labels.md:391`, `include/LO_GEN.labels.md:1515` | 0o300212 | 0 |
| `JP0514` | LABEL(md) | `include/LO_GEN.labels.md:393`, `include/LO_GEN.labels.md:1517` | 0o300214 | 0 |
| `JP0515` | LABEL(md) | `include/LO_GEN.labels.md:394`, `include/LO_GEN.labels.md:1518` | 0o300215 | 0 |
| `JP0516` | LABEL(md) | `include/LO_GEN.labels.md:395`, `include/LO_GEN.labels.md:1529` | 0o300216 | 0 |
| `JP0517` | LABEL(md) | `include/LO_GEN.labels.md:396`, `include/LO_GEN.labels.md:1527` | 0o300217 | 0 |
| `JP0520` | LABEL(md) | `include/LO_GEN.labels.md:397`, `include/LO_GEN.labels.md:1528` | 0o300220 | 0 |
| `JP0530` | LABEL(md) | `include/LO_GEN.labels.md:405`, `include/LO_GEN.labels.md:1482` | 0o300230 | 0 |
| `JP0531` | LABEL(md) | `include/LO_GEN.labels.md:406`, `include/LO_GEN.labels.md:1484` | 0o300231 | 0 |
| `JP0657` | LABEL(md) | `include/LO_GEN.labels.md:492` | 0o300357 | 0 |
| `JP0666` | LABEL(md) | `include/LO_GEN.labels.md:499`, `include/LO_GEN.labels.md:1443` | 0o300366 | 0 |
| `JP0670` | LABEL(md) | `include/LO_GEN.labels.md:501`, `include/LO_GEN.labels.md:1434` | 0o300370 | 0 |
| `JP0703` | LABEL(md) | `include/LO_GEN.labels.md:512`, `include/LO_GEN.labels.md:1449` | 0o300403 | 0 |
| `JP0713` | LABEL(md) | `include/LO_GEN.labels.md:520` | 0o300413 | 0 |
| `JP0717` | LABEL(md) | `include/LO_GEN.labels.md:524` | 0o300417 | 0 |
| `JP0721` | LABEL(md) | `include/LO_GEN.labels.md:526` | 0o300421 | 0 |
| `JP0725` | LABEL(md) | `include/LO_GEN.labels.md:530` | 0o300425 | 0 |
| `JP0731` | LABEL(md) | `include/LO_GEN.labels.md:534` | 0o300431 | 0 |
| `JP0733` | LABEL(md) | `include/LO_GEN.labels.md:536` | 0o300433 | 0 |
| `JP0751` | LABEL(md) | `include/LO_GEN.labels.md:550` | 0o300451 | 0 |
| `JP1051` | LABEL(md) | `include/LO_GEN.labels.md:614` | 0o300551 | 0 |
| `JP1061` | LABEL(md) | `include/LO_GEN.labels.md:622` | 0o300561 | 0 |
| `JP1071` | LABEL(md) | `include/LO_GEN.labels.md:630` | 0o300571 | 0 |
| `JP1100` | LABEL(md) | `include/LO_GEN.labels.md:637` | 0o300600 | 0 |
| `JP1130` | LABEL(md) | `include/LO_GEN.labels.md:661` | 0o300630 | 0 |
| `JP1141` | LABEL(md) | `include/LO_GEN.labels.md:670`, `include/LO_GEN.labels.md:1466` | 0o300641 | 0 |
| `JP1151` | LABEL(md) | `include/LO_GEN.labels.md:678`, `include/LO_GEN.labels.md:1466` | 0o300651 | 0 |
| `JP1153` | LABEL(md) | `include/LO_GEN.labels.md:680` | 0o300653 | 0 |
| `JP1160` | LABEL(md) | `include/LO_GEN.labels.md:685` | 0o300660 | 0 |
| `JP1163` | LABEL(md) | `include/LO_GEN.labels.md:688` | 0o300663 | 0 |
| `JP1167` | LABEL(md) | `include/LO_GEN.labels.md:692` | 0o300667 | 0 |
| `JP1171` | LABEL(md) | `include/LO_GEN.labels.md:694`, `include/LO_GEN.labels.md:1480` | 0o300671 | 0 |
| `JP1174` | LABEL(md) | `include/LO_GEN.labels.md:697` | 0o300674 | 0 |
| `JP1176` | LABEL(md) | `include/LO_GEN.labels.md:699`, `include/LO_GEN.labels.md:1483` | 0o300676 | 0 |
| `JP1214` | LABEL(md) | `include/LO_GEN.labels.md:713` | 0o300714 | 0 |
| `JP1216` | LABEL(md) | `include/LO_GEN.labels.md:715` | 0o300716 | 0 |
| `JP1232` | LABEL(md) | `include/LO_GEN.labels.md:727`, `include/LO_GEN.labels.md:1494` | 0o300732 | 0 |
| `JP1235` | LABEL(md) | `include/LO_GEN.labels.md:730`, `include/LO_GEN.labels.md:1494` | 0o300735 | 0 |
| `JP1242` | LABEL(md) | `include/LO_GEN.labels.md:735`, `include/LO_GEN.labels.md:1494` | 0o300742 | 0 |
| `JP1245` | LABEL(md) | `include/LO_GEN.labels.md:738` | 0o300745 | 0 |
| `JP1256` | LABEL(md) | `include/LO_GEN.labels.md:747`, `include/LO_GEN.labels.md:1498` | 0o300756 | 0 |
| `JP1261` | LABEL(md) | `include/LO_GEN.labels.md:750`, `include/LO_GEN.labels.md:1498` | 0o300761 | 0 |
| `JP1324` | LABEL(md) | `include/LO_GEN.labels.md:785` | 0o301024 | 0 |
| `JP1326` | LABEL(md) | `include/LO_GEN.labels.md:787`, `include/LO_GEN.labels.md:1505` | 0o301026 | 0 |
| `JP1330` | LABEL(md) | `include/LO_GEN.labels.md:789`, `include/LO_GEN.labels.md:1505` | 0o301030 | 0 |
| `JP1340` | LABEL(md) | `include/LO_GEN.labels.md:797`, `include/LO_GEN.labels.md:1500` | 0o301040 | 0 |
| `JP1342` | LABEL(md) | `include/LO_GEN.labels.md:799` | 0o301042 | 0 |
| `JP1344` | LABEL(md) | `include/LO_GEN.labels.md:801` | 0o301044 | 0 |
| `JP1412` | LABEL(md) | `include/LO_GEN.labels.md:839` | 0o301112 | 0 |
| `JP1416` | LABEL(md) | `include/LO_GEN.labels.md:843`, `include/LO_GEN.labels.md:1510` | 0o301116 | 0 |
| `JP1425` | LABEL(md) | `include/LO_GEN.labels.md:850` | 0o301125 | 0 |
| `JP1454` | LABEL(md) | `include/LO_GEN.labels.md:873` | 0o301154 | 0 |
| `JP1456` | LABEL(md) | `include/LO_GEN.labels.md:875` | 0o301156 | 0 |
| `JP1460` | LABEL(md) | `include/LO_GEN.labels.md:877` | 0o301160 | 0 |
| `JP1462` | LABEL(md) | `include/LO_GEN.labels.md:879` | 0o301162 | 0 |
| `JP1464` | LABEL(md) | `include/LO_GEN.labels.md:881` | 0o301164 | 0 |
| `JP1466` | LABEL(md) | `include/LO_GEN.labels.md:883` | 0o301166 | 0 |
| `JP1470` | LABEL(md) | `include/LO_GEN.labels.md:885` | 0o301170 | 0 |
| `JP1475` | LABEL(md) | `include/LO_GEN.labels.md:890`, `include/LO_GEN.labels.md:1489` | 0o301175 | 0 |
| `JP1477` | LABEL(md) | `include/LO_GEN.labels.md:892` | 0o301177 | 0 |
| `JP1501` | LABEL(md) | `include/LO_GEN.labels.md:894` | 0o301201 | 0 |
| `JP1503` | LABEL(md) | `include/LO_GEN.labels.md:896` | 0o301203 | 0 |
| `JP1514` | LABEL(md) | `include/LO_GEN.labels.md:905` | 0o301214 | 0 |
| `JP1571` | LABEL(md) | `include/LO_GEN.labels.md:950` | 0o301271 | 0 |
| `JP1610` | LABEL(md) | `include/LO_GEN.labels.md:965`, `include/LO_GEN.labels.md:1521` | 0o301310 | 0 |
| `JP1617` | LABEL(md) | `include/LO_GEN.labels.md:972`, `include/LO_GEN.labels.md:1095` | 0o301317 | 0 |
| `JP1641` | LABEL(md) | `include/LO_GEN.labels.md:990` | 0o301341 | 0 |
| `JP1643` | LABEL(md) | `include/LO_GEN.labels.md:992`, `include/LO_GEN.labels.md:1526` | 0o301343 | 0 |
| `JP1645` | LABEL(md) | `include/LO_GEN.labels.md:994`, `include/LO_GEN.labels.md:1526` | 0o301345 | 0 |
| `JP1656` | LABEL(md) | `include/LO_GEN.labels.md:1003` | 0o301356 | 0 |
| `JP1660` | LABEL(md) | `include/LO_GEN.labels.md:1005` | 0o301360 | 0 |
| `JP1665` | LABEL(md) | `include/LO_GEN.labels.md:1010` | 0o301365 | 0 |
| `JP1672` | LABEL(md) | `include/LO_GEN.labels.md:1015`, `include/LO_GEN.labels.md:1532` | 0o301372 | 0 |
| `JP1714` | LABEL(md) | `include/LO_GEN.labels.md:1033` | 0o301414 | 0 |
| `JP1725` | LABEL(md) | `include/LO_GEN.labels.md:1042` | 0o301425 | 0 |
| `JP1762` | LABEL(md) | `include/LO_GEN.labels.md:1071` | 0o301462 | 0 |
| `JP1774` | LABEL(md) | `include/LO_GEN.labels.md:1081`, `include/LO_GEN.labels.md:1544` | 0o301474 | 0 |
| `KCNT` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:240`, `include/FOREX.labels.md:529` | ONEW | 0 |
| `L` | LABEL | `src/FOREX_RUNTIME.mad:199`, `src/FOREX_RUNTIME.mad:203`, `src/FOREX_RUNTIME.mad:204`, `src/FOREX_RUNTIME.mad:208`, `src/FOREX_RUNTIME.mad:230`, `src/FOREX_RUNTIME.mad:234` … (+26) | — | 0 |
| `L00023` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:239`, `include/FOREX.labels.md:530` | — | 0 |
| `L00027` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:248`, `include/FOREX.labels.md:531` | — | 0 |
| `L00042` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:270`, `include/FOREX.labels.md:532` | — | 0 |
| `L00045` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:276`, `include/FOREX.labels.md:533` | — | 0 |
| `L00050` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:282`, `include/FOREX.labels.md:534` | — | 0 |
| `L00053` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:288`, `include/FOREX.labels.md:535` | — | 0 |
| `L0021` | LABEL(md) | `include/LO_SYN.labels.md:12` | — | 0 |
| `L0315` | LABEL(md) | `include/LO_SYN.labels.md:13` | — | 0 |
| `L0316` | LABEL(md) | `include/LO_SYN.labels.md:14` | — | 0 |
| `L0500` | LABEL(md) | `include/LO_SYN.labels.md:15` | — | 0 |
| `L0507` | LABEL(md) | `include/LO_SYN.labels.md:16` | — | 0 |
| `L0511` | LABEL(md) | `include/LO_SYN.labels.md:17` | — | 0 |
| `L1` | XREF(md) | `include/RUNTIME_DECODER.xref.md:16`, `include/RUNTIME_DECODER.xref.md:25` | — | 0 |
| `L1001` | LABEL(md) | `include/LO_SYN.labels.md:18` | — | 0 |
| `L1003` | LABEL(md) | `include/LO_SYN.labels.md:19` | — | 0 |
| `L1005` | LABEL(md) | `include/LO_SYN.labels.md:20` | — | 0 |
| `L1030` | LABEL(md) | `include/LO_SYN.labels.md:21` | — | 0 |
| `L1031` | LABEL(md) | `include/LO_SYN.labels.md:22` | — | 0 |
| `L1032` | LABEL(md) | `include/LO_SYN.labels.md:23` | — | 0 |
| `L1112` | LABEL(md) | `include/LO_SYN.labels.md:24` | — | 0 |
| `L1113` | LABEL(md) | `include/LO_SYN.labels.md:25` | — | 0 |
| `L1201` | LABEL(md) | `include/LO_SYN.labels.md:26` | — | 0 |
| `L1304` | LABEL(md) | `include/LO_SYN.labels.md:27` | — | 0 |
| `L1317` | LABEL(md) | `include/LO_SYN.labels.md:28` | — | 0 |
| `L1321` | LABEL(md) | `include/LO_SYN.labels.md:29` | — | 0 |
| `L1327` | LABEL(md) | `include/LO_SYN.labels.md:30` | — | 0 |
| `L1330` | LABEL(md) | `include/LO_SYN.labels.md:31` | — | 0 |
| `L1331` | LABEL(md) | `include/LO_SYN.labels.md:32` | — | 0 |
| `L1400` | LABEL(md) | `include/LO_SYN.labels.md:33` | — | 0 |
| `L1410` | LABEL(md) | `include/LO_SYN.labels.md:34` | — | 0 |
| `L1427` | LABEL(md) | `include/LO_SYN.labels.md:35` | — | 0 |
| `L1430` | LABEL(md) | `include/LO_SYN.labels.md:36` | — | 0 |
| `L2` | XREF(md) | `include/RUNTIME_DECODER.xref.md:17` | — | 0 |
| `L3` | XREF(md) | `include/RUNTIME_DECODER.xref.md:19` | — | 0 |
| `LC` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `LD0006` | LABEL(md) | `include/LO_GEN.labels.md:67`, `include/LO_GEN.labels.md:1290` | 0o277506 | 0 |
| `LD0073` | LABEL(md) | `include/LO_GEN.labels.md:120`, `include/LO_GEN.labels.md:1327` | 0o277573 | 0 |
| `LD0076` | LABEL(md) | `include/LO_GEN.labels.md:123`, `include/LO_GEN.labels.md:1324` | 0o277576 | 0 |
| `LD0100` | LABEL(md) | `include/LO_GEN.labels.md:125`, `include/LO_GEN.labels.md:1327` | 0o277600 | 0 |
| `LD0102` | LABEL(md) | `include/LO_GEN.labels.md:127`, `include/LO_GEN.labels.md:1325` | 0o277602 | 0 |
| `LD0126` | LABEL(md) | `include/LO_GEN.labels.md:147`, `include/LO_GEN.labels.md:1320` | 0o277626 | 0 |
| `LD0130` | LABEL(md) | `include/LO_GEN.labels.md:149`, `include/LO_GEN.labels.md:1110` | 0o277630 | 0 |
| `LD0131` | LABEL(md) | `include/LO_GEN.labels.md:150`, `include/LO_GEN.labels.md:1400` | 0o277631 | 0 |
| `LD0135` | LABEL(md) | `include/LO_GEN.labels.md:154` | 0o277635 | 0 |
| `LD0146` | LABEL(md) | `include/LO_GEN.labels.md:163`, `include/LO_GEN.labels.md:1324` | 0o277646 | 0 |
| `LD0154` | LABEL(md) | `include/LO_GEN.labels.md:169`, `include/LO_GEN.labels.md:1308` | 0o277654 | 0 |
| `LD0156` | LABEL(md) | `include/LO_GEN.labels.md:171` | 0o277656 | 0 |
| `LD0162` | LABEL(md) | `include/LO_GEN.labels.md:175` | 0o277662 | 0 |
| `LD0167` | LABEL(md) | `include/LO_GEN.labels.md:180` | 0o277667 | 0 |
| `LD0171` | LABEL(md) | `include/LO_GEN.labels.md:182` | 0o277671 | 0 |
| `LD0174` | LABEL(md) | `include/LO_GEN.labels.md:185`, `include/LO_GEN.labels.md:1159` | 0o277674 | 0 |
| `LD0177` | LABEL(md) | `include/LO_GEN.labels.md:188` | 0o277677 | 0 |
| `LD0202` | LABEL(md) | `include/LO_GEN.labels.md:191` | 0o277702 | 0 |
| `LD0210` | LABEL(md) | `include/LO_GEN.labels.md:197`, `include/LO_GEN.labels.md:1320` | 0o277710 | 0 |
| `LD0217` | LABEL(md) | `include/LO_GEN.labels.md:204` | 0o277717 | 0 |
| `LD0221` | LABEL(md) | `include/LO_GEN.labels.md:206`, `include/LO_GEN.labels.md:1218` | 0o277721 | 0 |
| `LD0232` | LABEL(md) | `include/LO_GEN.labels.md:215` | 0o277732 | 0 |
| `LD0233` | LABEL(md) | `include/LO_GEN.labels.md:216` | 0o277733 | 0 |
| `LD0236` | LABEL(md) | `include/LO_GEN.labels.md:219` | 0o277736 | 0 |
| `LD0237` | LABEL(md) | `include/LO_GEN.labels.md:220` | 0o277737 | 0 |
| `LD0240` | LABEL(md) | `include/LO_GEN.labels.md:221` | 0o277740 | 0 |
| `LD0241` | LABEL(md) | `include/LO_GEN.labels.md:222` | 0o277741 | 0 |
| `LD0242` | LABEL(md) | `include/LO_GEN.labels.md:223`, `include/LO_GEN.labels.md:1165` | 0o277742 | 0 |
| `LD0245` | LABEL(md) | `include/LO_GEN.labels.md:226` | 0o277745 | 0 |
| `LD0247` | LABEL(md) | `include/LO_GEN.labels.md:228`, `include/LO_GEN.labels.md:1323` | 0o277747 | 0 |
| `LD0252` | LABEL(md) | `include/LO_GEN.labels.md:231`, `include/LO_GEN.labels.md:1169` | 0o277752 | 0 |
| `LD0265` | LABEL(md) | `include/LO_GEN.labels.md:242`, `include/LO_GEN.labels.md:1162` | 0o277765 | 0 |
| `LD0270` | LABEL(md) | `include/LO_GEN.labels.md:245` | 0o277770 | 0 |
| `LD0272` | LABEL(md) | `include/LO_GEN.labels.md:247` | 0o277772 | 0 |
| `LD0277` | LABEL(md) | `include/LO_GEN.labels.md:252`, `include/LO_GEN.labels.md:1165` | 0o277777 | 0 |
| `LD0302` | LABEL(md) | `include/LO_GEN.labels.md:255` | 0o300002 | 0 |
| `LD0303` | LABEL(md) | `include/LO_GEN.labels.md:256`, `include/LO_GEN.labels.md:1138` | 0o300003 | 0 |
| `LD0315` | LABEL(md) | `include/LO_GEN.labels.md:266`, `include/LO_GEN.labels.md:1138` | 0o300015 | 0 |
| `LD0332` | LABEL(md) | `include/LO_GEN.labels.md:279` | 0o300032 | 0 |
| `LD0333` | LABEL(md) | `include/LO_GEN.labels.md:280`, `include/LO_GEN.labels.md:1162` | 0o300033 | 0 |
| `LD0334` | LABEL(md) | `include/LO_GEN.labels.md:281`, `include/LO_GEN.labels.md:1169` | 0o300034 | 0 |
| `LD0335` | LABEL(md) | `include/LO_GEN.labels.md:282` | 0o300035 | 0 |
| `LD0347` | LABEL(md) | `include/LO_GEN.labels.md:292`, `include/LO_GEN.labels.md:1175` | 0o300047 | 0 |
| `LD0356` | LABEL(md) | `include/LO_GEN.labels.md:299` | 0o300056 | 0 |
| `LD0364` | LABEL(md) | `include/LO_GEN.labels.md:305`, `include/LO_GEN.labels.md:1178` | 0o300064 | 0 |
| `LD0365` | LABEL(md) | `include/LO_GEN.labels.md:306`, `include/LO_GEN.labels.md:1400` | 0o300065 | 0 |
| `LD0411` | LABEL(md) | `include/LO_GEN.labels.md:326`, `include/LO_GEN.labels.md:1204` | 0o300111 | 0 |
| `LD0412` | LABEL(md) | `include/LO_GEN.labels.md:327`, `include/LO_GEN.labels.md:1206` | 0o300112 | 0 |
| `LD0413` | LABEL(md) | `include/LO_GEN.labels.md:328`, `include/LO_GEN.labels.md:1210` | 0o300113 | 0 |
| `LD0414` | LABEL(md) | `include/LO_GEN.labels.md:329`, `include/LO_GEN.labels.md:1211` | 0o300114 | 0 |
| `LD0624` | LABEL(md) | `include/LO_GEN.labels.md:465`, `include/LO_GEN.labels.md:1328` | 0o300324 | 0 |
| `LD0625` | LABEL(md) | `include/LO_GEN.labels.md:466` | 0o300325 | 0 |
| `LD0627` | LABEL(md) | `include/LO_GEN.labels.md:468` | 0o300327 | 0 |
| `LD0630` | LABEL(md) | `include/LO_GEN.labels.md:469` | 0o300330 | 0 |
| `LD0633` | LABEL(md) | `include/LO_GEN.labels.md:472` | 0o300333 | 0 |
| `LD0634` | LABEL(md) | `include/LO_GEN.labels.md:473` | 0o300334 | 0 |
| `LD0637` | LABEL(md) | `include/LO_GEN.labels.md:476` | 0o300337 | 0 |
| `LD0647` | LABEL(md) | `include/LO_GEN.labels.md:484`, `include/LO_GEN.labels.md:1263` | 0o300347 | 0 |
| `LD0652` | LABEL(md) | `include/LO_GEN.labels.md:487` | 0o300352 | 0 |
| `LD0653` | LABEL(md) | `include/LO_GEN.labels.md:488`, `include/LO_GEN.labels.md:1162` | 0o300353 | 0 |
| `LD0656` | LABEL(md) | `include/LO_GEN.labels.md:491` | 0o300356 | 0 |
| `LD0662` | LABEL(md) | `include/LO_GEN.labels.md:495` | 0o300362 | 0 |
| `LD0665` | LABEL(md) | `include/LO_GEN.labels.md:498` | 0o300365 | 0 |
| `LD0674` | LABEL(md) | `include/LO_GEN.labels.md:505` | 0o300374 | 0 |
| `LD0677` | LABEL(md) | `include/LO_GEN.labels.md:508` | 0o300377 | 0 |
| `LD0700` | LABEL(md) | `include/LO_GEN.labels.md:509` | 0o300400 | 0 |
| `LD0704` | LABEL(md) | `include/LO_GEN.labels.md:513`, `include/LO_GEN.labels.md:1125` | 0o300404 | 0 |
| `LD0706` | LABEL(md) | `include/LO_GEN.labels.md:515` | 0o300406 | 0 |
| `LD0707` | LABEL(md) | `include/LO_GEN.labels.md:516` | 0o300407 | 0 |
| `LD0712` | LABEL(md) | `include/LO_GEN.labels.md:519`, `include/LO_GEN.labels.md:1125` | 0o300412 | 0 |
| `LD0722` | LABEL(md) | `include/LO_GEN.labels.md:527` | 0o300422 | 0 |
| `LD0723` | LABEL(md) | `include/LO_GEN.labels.md:528` | 0o300423 | 0 |
| `LD0737` | LABEL(md) | `include/LO_GEN.labels.md:540`, `include/LO_GEN.labels.md:1134` | 0o300437 | 0 |
| `LD0744` | LABEL(md) | `include/LO_GEN.labels.md:545`, `include/LO_GEN.labels.md:1170` | 0o300444 | 0 |
| `LD0754` | LABEL(md) | `include/LO_GEN.labels.md:553`, `include/LO_GEN.labels.md:1175` | 0o300454 | 0 |
| `LD0760` | LABEL(md) | `include/LO_GEN.labels.md:557` | 0o300460 | 0 |
| `LD0763` | LABEL(md) | `include/LO_GEN.labels.md:560` | 0o300463 | 0 |
| `LD0764` | LABEL(md) | `include/LO_GEN.labels.md:561` | 0o300464 | 0 |
| `LD0771` | LABEL(md) | `include/LO_GEN.labels.md:566`, `include/LO_GEN.labels.md:1219` | 0o300471 | 0 |
| `LD0775` | LABEL(md) | `include/LO_GEN.labels.md:570`, `include/LO_GEN.labels.md:1223` | 0o300475 | 0 |
| `LD0776` | LABEL(md) | `include/LO_GEN.labels.md:571`, `include/LO_GEN.labels.md:1211` | 0o300476 | 0 |
| `LD1001` | LABEL(md) | `include/LO_GEN.labels.md:574` | 0o300501 | 0 |
| `LD1005` | LABEL(md) | `include/LO_GEN.labels.md:578` | 0o300505 | 0 |
| `LD1012` | LABEL(md) | `include/LO_GEN.labels.md:583`, `include/LO_GEN.labels.md:1170` | 0o300512 | 0 |
| `LD1015` | LABEL(md) | `include/LO_GEN.labels.md:586` | 0o300515 | 0 |
| `LD1021` | LABEL(md) | `include/LO_GEN.labels.md:590` | 0o300521 | 0 |
| `LD1031` | LABEL(md) | `include/LO_GEN.labels.md:598`, `include/LO_GEN.labels.md:1170` | 0o300531 | 0 |
| `LD1043` | LABEL(md) | `include/LO_GEN.labels.md:608` | 0o300543 | 0 |
| `LD1052` | LABEL(md) | `include/LO_GEN.labels.md:615` | 0o300552 | 0 |
| `LD1063` | LABEL(md) | `include/LO_GEN.labels.md:624`, `include/LO_GEN.labels.md:1232` | 0o300563 | 0 |
| `LD1072` | LABEL(md) | `include/LO_GEN.labels.md:631` | 0o300572 | 0 |
| `LD1074` | LABEL(md) | `include/LO_GEN.labels.md:633`, `include/LO_GEN.labels.md:1140` | 0o300574 | 0 |
| `LD1105` | LABEL(md) | `include/LO_GEN.labels.md:642` | 0o300605 | 0 |
| `LD1120` | LABEL(md) | `include/LO_GEN.labels.md:653` | 0o300620 | 0 |
| `LD1140` | LABEL(md) | `include/LO_GEN.labels.md:669` | 0o300640 | 0 |
| `LD1146` | LABEL(md) | `include/LO_GEN.labels.md:675` | 0o300646 | 0 |
| `LD1154` | LABEL(md) | `include/LO_GEN.labels.md:681` | 0o300654 | 0 |
| `LD1155` | LABEL(md) | `include/LO_GEN.labels.md:682` | 0o300655 | 0 |
| `LD1177` | LABEL(md) | `include/LO_GEN.labels.md:700` | 0o300677 | 0 |
| `LD1201` | LABEL(md) | `include/LO_GEN.labels.md:702` | 0o300701 | 0 |
| `LD1203` | LABEL(md) | `include/LO_GEN.labels.md:704` | 0o300703 | 0 |
| `LD1211` | LABEL(md) | `include/LO_GEN.labels.md:710` | 0o300711 | 0 |
| `LD1217` | LABEL(md) | `include/LO_GEN.labels.md:716` | 0o300717 | 0 |
| `LD1220` | LABEL(md) | `include/LO_GEN.labels.md:717`, `include/LO_GEN.labels.md:1165` | 0o300720 | 0 |
| `LD1222` | LABEL(md) | `include/LO_GEN.labels.md:719` | 0o300722 | 0 |
| `LD1223` | LABEL(md) | `include/LO_GEN.labels.md:720` | 0o300723 | 0 |
| `LD1225` | LABEL(md) | `include/LO_GEN.labels.md:722` | 0o300725 | 0 |
| `LD1230` | LABEL(md) | `include/LO_GEN.labels.md:725`, `include/LO_GEN.labels.md:1116` | 0o300730 | 0 |
| `LD1233` | LABEL(md) | `include/LO_GEN.labels.md:728`, `include/LO_GEN.labels.md:1116` | 0o300733 | 0 |
| `LD1240` | LABEL(md) | `include/LO_GEN.labels.md:733`, `include/LO_GEN.labels.md:1116` | 0o300740 | 0 |
| `LD1243` | LABEL(md) | `include/LO_GEN.labels.md:736` | 0o300743 | 0 |
| `LD1252` | LABEL(md) | `include/LO_GEN.labels.md:743`, `include/LO_GEN.labels.md:1326` | 0o300752 | 0 |
| `LD1253` | LABEL(md) | `include/LO_GEN.labels.md:744` | 0o300753 | 0 |
| `LD1254` | LABEL(md) | `include/LO_GEN.labels.md:745` | 0o300754 | 0 |
| `LD1257` | LABEL(md) | `include/LO_GEN.labels.md:748` | 0o300757 | 0 |
| `LD1307` | LABEL(md) | `include/LO_GEN.labels.md:772` | 0o301007 | 0 |
| `LD1312` | LABEL(md) | `include/LO_GEN.labels.md:775` | 0o301012 | 0 |
| `LD1322` | LABEL(md) | `include/LO_GEN.labels.md:783` | 0o301022 | 0 |
| `LD1325` | LABEL(md) | `include/LO_GEN.labels.md:786`, `include/LO_GEN.labels.md:1173` | 0o301025 | 0 |
| `LD1327` | LABEL(md) | `include/LO_GEN.labels.md:788` | 0o301027 | 0 |
| `LD1332` | LABEL(md) | `include/LO_GEN.labels.md:791` | 0o301032 | 0 |
| `LD1334` | LABEL(md) | `include/LO_GEN.labels.md:793` | 0o301034 | 0 |
| `LD1337` | LABEL(md) | `include/LO_GEN.labels.md:796`, `include/LO_GEN.labels.md:1169` | 0o301037 | 0 |
| `LD1341` | LABEL(md) | `include/LO_GEN.labels.md:798` | 0o301041 | 0 |
| `LD1350` | LABEL(md) | `include/LO_GEN.labels.md:805` | 0o301050 | 0 |
| `LD1354` | LABEL(md) | `include/LO_GEN.labels.md:809` | 0o301054 | 0 |
| `LD1360` | LABEL(md) | `include/LO_GEN.labels.md:813`, `include/LO_GEN.labels.md:1137` | 0o301060 | 0 |
| `LD1361` | LABEL(md) | `include/LO_GEN.labels.md:814` | 0o301061 | 0 |
| `LD1375` | LABEL(md) | `include/LO_GEN.labels.md:826` | 0o301075 | 0 |
| `LD1402` | LABEL(md) | `include/LO_GEN.labels.md:831` | 0o301102 | 0 |
| `LD1407` | LABEL(md) | `include/LO_GEN.labels.md:836` | 0o301107 | 0 |
| `LD1413` | LABEL(md) | `include/LO_GEN.labels.md:840` | 0o301113 | 0 |
| `LD1417` | LABEL(md) | `include/LO_GEN.labels.md:844` | 0o301117 | 0 |
| `LD1426` | LABEL(md) | `include/LO_GEN.labels.md:851`, `include/LO_GEN.labels.md:1128` | 0o301126 | 0 |
| `LD1427` | LABEL(md) | `include/LO_GEN.labels.md:852` | 0o301127 | 0 |
| `LD1430` | LABEL(md) | `include/LO_GEN.labels.md:853` | 0o301130 | 0 |
| `LD1431` | LABEL(md) | `include/LO_GEN.labels.md:854` | 0o301131 | 0 |
| `LD1436` | LABEL(md) | `include/LO_GEN.labels.md:859` | 0o301136 | 0 |
| `LD1447` | LABEL(md) | `include/LO_GEN.labels.md:868` | 0o301147 | 0 |
| `LD1451` | LABEL(md) | `include/LO_GEN.labels.md:870` | 0o301151 | 0 |
| `LD1455` | LABEL(md) | `include/LO_GEN.labels.md:874` | 0o301155 | 0 |
| `LD1457` | LABEL(md) | `include/LO_GEN.labels.md:876` | 0o301157 | 0 |
| `LD1461` | LABEL(md) | `include/LO_GEN.labels.md:878` | 0o301161 | 0 |
| `LD1463` | LABEL(md) | `include/LO_GEN.labels.md:880` | 0o301163 | 0 |
| `LD1465` | LABEL(md) | `include/LO_GEN.labels.md:882`, `include/LO_GEN.labels.md:1268` | 0o301165 | 0 |
| `LD1467` | LABEL(md) | `include/LO_GEN.labels.md:884` | 0o301167 | 0 |
| `LD1471` | LABEL(md) | `include/LO_GEN.labels.md:886` | 0o301171 | 0 |
| `LD1472` | LABEL(md) | `include/LO_GEN.labels.md:887` | 0o301172 | 0 |
| `LD1474` | LABEL(md) | `include/LO_GEN.labels.md:889` | 0o301174 | 0 |
| `LD1476` | LABEL(md) | `include/LO_GEN.labels.md:891`, `include/LO_GEN.labels.md:1174` | 0o301176 | 0 |
| `LD1500` | LABEL(md) | `include/LO_GEN.labels.md:893` | 0o301200 | 0 |
| `LD1502` | LABEL(md) | `include/LO_GEN.labels.md:895`, `include/LO_GEN.labels.md:1281` | 0o301202 | 0 |
| `LD1510` | LABEL(md) | `include/LO_GEN.labels.md:901`, `include/LO_GEN.labels.md:1159` | 0o301210 | 0 |
| `LD1515` | LABEL(md) | `include/LO_GEN.labels.md:906` | 0o301215 | 0 |
| `LD1516` | LABEL(md) | `include/LO_GEN.labels.md:907` | 0o301216 | 0 |
| `LD1517` | LABEL(md) | `include/LO_GEN.labels.md:908` | 0o301217 | 0 |
| `LD1524` | LABEL(md) | `include/LO_GEN.labels.md:913` | 0o301224 | 0 |
| `LD1527` | LABEL(md) | `include/LO_GEN.labels.md:916` | 0o301227 | 0 |
| `LD1530` | LABEL(md) | `include/LO_GEN.labels.md:917`, `include/LO_GEN.labels.md:1164` | 0o301230 | 0 |
| `LD1532` | LABEL(md) | `include/LO_GEN.labels.md:919` | 0o301232 | 0 |
| `LD1534` | LABEL(md) | `include/LO_GEN.labels.md:921` | 0o301234 | 0 |
| `LD1541` | LABEL(md) | `include/LO_GEN.labels.md:926`, `include/LO_GEN.labels.md:1282` | 0o301241 | 0 |
| `LD1545` | LABEL(md) | `include/LO_GEN.labels.md:930` | 0o301245 | 0 |
| `LD1546` | LABEL(md) | `include/LO_GEN.labels.md:931`, `include/LO_GEN.labels.md:1399` | 0o301246 | 0 |
| `LD1554` | LABEL(md) | `include/LO_GEN.labels.md:937`, `include/LO_GEN.labels.md:1283` | 0o301254 | 0 |
| `LD1557` | LABEL(md) | `include/LO_GEN.labels.md:940` | 0o301257 | 0 |
| `LD1560` | LABEL(md) | `include/LO_GEN.labels.md:941`, `include/LO_GEN.labels.md:1399` | 0o301260 | 0 |
| `LD1566` | LABEL(md) | `include/LO_GEN.labels.md:947`, `include/LO_GEN.labels.md:1286` | 0o301266 | 0 |
| `LD1576` | LABEL(md) | `include/LO_GEN.labels.md:955` | 0o301276 | 0 |
| `LD1577` | LABEL(md) | `include/LO_GEN.labels.md:956` | 0o301277 | 0 |
| `LD1622` | LABEL(md) | `include/LO_GEN.labels.md:975`, `include/LO_GEN.labels.md:1219` | 0o301322 | 0 |
| `LD1626` | LABEL(md) | `include/LO_GEN.labels.md:979`, `include/LO_GEN.labels.md:1139` | 0o301326 | 0 |
| `LD1634` | LABEL(md) | `include/LO_GEN.labels.md:985` | 0o301334 | 0 |
| `LD1635` | LABEL(md) | `include/LO_GEN.labels.md:986` | 0o301335 | 0 |
| `LD1637` | LABEL(md) | `include/LO_GEN.labels.md:988`, `include/LO_GEN.labels.md:1289` | 0o301337 | 0 |
| `LD1640` | LABEL(md) | `include/LO_GEN.labels.md:989`, `include/LO_GEN.labels.md:1211` | 0o301340 | 0 |
| `LD1642` | LABEL(md) | `include/LO_GEN.labels.md:991` | 0o301342 | 0 |
| `LD1647` | LABEL(md) | `include/LO_GEN.labels.md:996` | 0o301347 | 0 |
| `LD1651` | LABEL(md) | `include/LO_GEN.labels.md:998` | 0o301351 | 0 |
| `LD1652` | LABEL(md) | `include/LO_GEN.labels.md:999` | 0o301352 | 0 |
| `LD1661` | LABEL(md) | `include/LO_GEN.labels.md:1006`, `include/LO_GEN.labels.md:1212` | 0o301361 | 0 |
| `LD1663` | LABEL(md) | `include/LO_GEN.labels.md:1008` | 0o301363 | 0 |
| `LD1664` | LABEL(md) | `include/LO_GEN.labels.md:1009` | 0o301364 | 0 |
| `LD1666` | LABEL(md) | `include/LO_GEN.labels.md:1011`, `include/LO_GEN.labels.md:1291` | 0o301366 | 0 |
| `LD1667` | LABEL(md) | `include/LO_GEN.labels.md:1012`, `include/LO_GEN.labels.md:1098` | 0o301367 | 0 |
| `LD1670` | LABEL(md) | `include/LO_GEN.labels.md:1013`, `include/LO_GEN.labels.md:1099` | 0o301370 | 0 |
| `LD1673` | LABEL(md) | `include/LO_GEN.labels.md:1016`, `include/LO_GEN.labels.md:1102` | 0o301373 | 0 |
| `LD1674` | LABEL(md) | `include/LO_GEN.labels.md:1017`, `include/LO_GEN.labels.md:1104` | 0o301374 | 0 |
| `LD1675` | LABEL(md) | `include/LO_GEN.labels.md:1018`, `include/LO_GEN.labels.md:1107` | 0o301375 | 0 |
| `LD1703` | LABEL(md) | `include/LO_GEN.labels.md:1024` | 0o301403 | 0 |
| `LD1705` | LABEL(md) | `include/LO_GEN.labels.md:1026` | 0o301405 | 0 |
| `LD1712` | LABEL(md) | `include/LO_GEN.labels.md:1031` | 0o301412 | 0 |
| `LD1722` | LABEL(md) | `include/LO_GEN.labels.md:1039` | 0o301422 | 0 |
| `LD1723` | LABEL(md) | `include/LO_GEN.labels.md:1040` | 0o301423 | 0 |
| `LD1726` | LABEL(md) | `include/LO_GEN.labels.md:1043` | 0o301426 | 0 |
| `LD1732` | LABEL(md) | `include/LO_GEN.labels.md:1047` | 0o301432 | 0 |
| `LD1733` | LABEL(md) | `include/LO_GEN.labels.md:1048`, `include/LO_GEN.labels.md:1322` | 0o301433 | 0 |
| `LD1734` | LABEL(md) | `include/LO_GEN.labels.md:1049`, `include/LO_GEN.labels.md:1323` | 0o301434 | 0 |
| `LD1735` | LABEL(md) | `include/LO_GEN.labels.md:1050` | 0o301435 | 0 |
| `LD1750` | LABEL(md) | `include/LO_GEN.labels.md:1061` | 0o301450 | 0 |
| `LD1760` | LABEL(md) | `include/LO_GEN.labels.md:1069` | 0o301460 | 0 |
| `LD1771` | LABEL(md) | `include/LO_GEN.labels.md:1078`, `include/LO_GEN.labels.md:1163` | 0o301471 | 0 |
| `LD1772` | LABEL(md) | `include/LO_GEN.labels.md:1079` | 0o301472 | 0 |
| `LD1773` | LABEL(md) | `include/LO_GEN.labels.md:1080` | 0o301473 | 0 |
| `LD1775` | LABEL(md) | `include/LO_GEN.labels.md:1082` | 0o301475 | 0 |
| `LIBBUF` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:74`, `include/RUNTIME_DISASM.xref.md:89` | 2000B | 0 |
| `LIBISO` | EQU/XREF(md) | `src/FOREX_RUNTIME_DISASM.mad:388`, `include/RUNTIME_DISASM.xref.md:88` | C101 | 0 |
| `LODOVL` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:243`, `include/FOREX_ROOT.mad:104`, `include/FOREX.labels.md:28`, `include/FOREX.labels.md:79`, `include/FOREX.labels.md:540` | — | 0 |
| `LOG` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `LOGTXT` | LABEL(md) | `include/LO_GEN.labels.md:31` | 0o277501 | 0 |
| `LOREX` | LABEL(md) | `include/FOREX.labels.md:7`, `include/FOREX.labels.md:28`, `include/FOREX.labels.md:79` | — | 0 |
| `MARR` | LABEL(md) | `include/FOREX.labels.md:64` | — | 0 |
| `MNTHFD` | DATA/LABEL(md) | `src/FOREX_RUNTIME.mad:424`, `include/FOREX.labels.md:66`, `include/FOREX.labels.md:549` | — | 0 |
| `MNTHFO` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:109`, `include/FOREX.labels.md:301`, `include/FOREX.labels.md:550` | 00 776 | 0 |
| `MNTXT` | LABEL(md)/TEXT | `src/LO_GEN.mad:502`, `include/LO_GEN.labels.md:31` | 8HLO*GEN | 0 |
| `MS0024` | LABEL(md) | `include/LO_GEN.labels.md:81`, `include/LO_GEN.labels.md:1168` | 0o277524 | 0 |
| `MS0103` | LABEL(md) | `include/LO_GEN.labels.md:128`, `include/LO_GEN.labels.md:1180`, `include/LO_GEN.labels.md:1317` | 0o277603 | 0 |
| `MU1715` | LABEL(md) | `include/LO_GEN.labels.md:1034` | 0o301415 | 0 |
| `MU1752` | LABEL(md) | `include/LO_GEN.labels.md:1063` | 0o301452 | 0 |
| `MV09N8` | EQU/LABEL(md) | `src/LO_GEN.mad:245`, `include/LO_GEN.labels.md:1299` | 12500 | 0 |
| `ND0532` | LABEL/LABEL(md) | `src/LO_GEN.mad:1584`, `include/LO_GEN.labels.md:407`, `include/LO_GEN.labels.md:1297` | — | 0 |
| `ND0534` | LABEL/LABEL(md) | `src/LO_GEN.mad:1588`, `include/LO_GEN.labels.md:409`, `include/LO_GEN.labels.md:1297` | — | 0 |
| `ND0536` | LABEL/LABEL(md) | `src/LO_GEN.mad:1592`, `include/LO_GEN.labels.md:411`, `include/LO_GEN.labels.md:1297` | — | 0 |
| `ND0540` | LABEL/LABEL(md) | `src/LO_GEN.mad:1596`, `include/LO_GEN.labels.md:413`, `include/LO_GEN.labels.md:1297` | — | 0 |
| `ND0542` | LABEL/LABEL(md) | `src/LO_GEN.mad:1600`, `include/LO_GEN.labels.md:415` | — | 0 |
| `ND0544` | LABEL/LABEL(md) | `src/LO_GEN.mad:1604`, `include/LO_GEN.labels.md:417` | — | 0 |
| `ND0546` | LABEL/LABEL(md) | `src/LO_GEN.mad:1608`, `include/LO_GEN.labels.md:419` | — | 0 |
| `ND0550` | LABEL/LABEL(md) | `src/LO_GEN.mad:1612`, `include/LO_GEN.labels.md:421` | — | 0 |
| `ND0552` | LABEL/LABEL(md) | `src/LO_GEN.mad:1616`, `include/LO_GEN.labels.md:423` | — | 0 |
| `ND0554` | LABEL/LABEL(md) | `src/LO_GEN.mad:1620`, `include/LO_GEN.labels.md:425` | — | 0 |
| `ND0556` | LABEL/LABEL(md) | `src/LO_GEN.mad:1624`, `include/LO_GEN.labels.md:427` | — | 0 |
| `ND0560` | LABEL/LABEL(md) | `src/LO_GEN.mad:1628`, `include/LO_GEN.labels.md:429` | — | 0 |
| `ND0562` | LABEL/LABEL(md) | `src/LO_GEN.mad:1632`, `include/LO_GEN.labels.md:431` | — | 0 |
| `ND0564` | LABEL/LABEL(md) | `src/LO_GEN.mad:1636`, `include/LO_GEN.labels.md:433` | — | 0 |
| `ND0566` | LABEL/LABEL(md) | `src/LO_GEN.mad:1640`, `include/LO_GEN.labels.md:435` | — | 0 |
| `ND0570` | LABEL/LABEL(md) | `src/LO_GEN.mad:1644`, `include/LO_GEN.labels.md:437` | — | 0 |
| `ND0572` | LABEL/LABEL(md) | `src/LO_GEN.mad:1648`, `include/LO_GEN.labels.md:439` | — | 0 |
| `ND0574` | LABEL/LABEL(md) | `src/LO_GEN.mad:1652`, `include/LO_GEN.labels.md:441` | — | 0 |
| `ND0576` | LABEL/LABEL(md) | `src/LO_GEN.mad:1656`, `include/LO_GEN.labels.md:443` | — | 0 |
| `ND0600` | LABEL/LABEL(md) | `src/LO_GEN.mad:1660`, `include/LO_GEN.labels.md:445` | — | 0 |
| `ND0602` | LABEL/LABEL(md) | `src/LO_GEN.mad:1664`, `include/LO_GEN.labels.md:447` | — | 0 |
| `ND0604` | LABEL/LABEL(md) | `src/LO_GEN.mad:1668`, `include/LO_GEN.labels.md:449` | — | 0 |
| `ND0606` | LABEL/LABEL(md) | `src/LO_GEN.mad:1672`, `include/LO_GEN.labels.md:451` | — | 0 |
| `ND0610` | LABEL/LABEL(md) | `src/LO_GEN.mad:1676`, `include/LO_GEN.labels.md:453` | — | 0 |
| `ND0612` | LABEL/LABEL(md) | `src/LO_GEN.mad:1680`, `include/LO_GEN.labels.md:455` | — | 0 |
| `ND0614` | LABEL/LABEL(md) | `src/LO_GEN.mad:1684`, `include/LO_GEN.labels.md:457` | — | 0 |
| `ND0616` | LABEL/LABEL(md) | `src/LO_GEN.mad:1688`, `include/LO_GEN.labels.md:459` | — | 0 |
| `ND0620` | LABEL/LABEL(md) | `src/LO_GEN.mad:1692`, `include/LO_GEN.labels.md:461` | — | 0 |
| `ND0622` | LABEL/LABEL(md) | `src/LO_GEN.mad:1696`, `include/LO_GEN.labels.md:463` | — | 0 |
| `NEG_12` | LABEL(md) | `include/LO_GEN.labels.md:1321` | — | 0 |
| `NEG_2` | LABEL(md) | `include/LO_GEN.labels.md:1322` | — | 0 |
| `NEG_3` | LABEL(md) | `include/LO_GEN.labels.md:1323` | — | 0 |
| `NEG_4` | LABEL(md) | `include/LO_GEN.labels.md:1324` | — | 0 |
| `NEG_5` | LABEL(md) | `include/LO_GEN.labels.md:1325` | — | 0 |
| `NEG_6` | LABEL(md) | `include/LO_GEN.labels.md:1326` | — | 0 |
| `NEG_7` | LABEL(md) | `include/LO_GEN.labels.md:1327` | — | 0 |
| `NMCHK` | EQU/LABEL(md) | `src/FOREX_CORE.mad:618`, `include/FOREX.labels.md:664` | CHECKF | 0 |
| `NMCOM` | EQU/LABEL(md) | `src/FOREX_CORE.mad:626`, `include/FOREX.labels.md:665` | COMEQ | 0 |
| `NMCON` | EQU/LABEL(md) | `src/FOREX_CORE.mad:625`, `include/FOREX.labels.md:666` | CONST | 0 |
| `NMDPR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:620`, `include/FOREX.labels.md:667` | DATAPR | 0 |
| `NMDUM` | EQU/LABEL(md) | `src/FOREX_CORE.mad:619`, `include/FOREX.labels.md:668` | *DUMON | 0 |
| `NMENT` | EQU/LABEL(md) | `src/FOREX_CORE.mad:614`, `include/FOREX.labels.md:669` | ENTRY* | 0 |
| `NMFEX` | EQU/LABEL(md) | `src/FOREX_CORE.mad:615`, `include/FOREX.labels.md:670` | FLGEX* | 0 |
| `NMFOR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:624`, `include/FOREX.labels.md:671` | FOREX | 0 |
| `NMFUL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:617`, `include/FOREX.labels.md:672` | FULISF | 0 |
| `NMGIV` | EQU/LABEL(md) | `src/FOREX_CORE.mad:622`, `include/FOREX.labels.md:673` | GIV/PG | 0 |
| `NMLDG` | EQU/LABEL(md) | `src/FOREX_CORE.mad:628`, `include/FOREX.labels.md:674` | LOADAN | 0 |
| `NMNOL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:616`, `include/FOREX.labels.md:675` | NOLISF | 0 |
| `NMOCT` | EQU/LABEL(md) | `src/FOREX_CORE.mad:623`, `include/FOREX.labels.md:676` | OCTTDE | 0 |
| `NMOPR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:627`, `include/FOREX.labels.md:677` | OPRTR | 0 |
| `NMTAK` | EQU/LABEL(md) | `src/FOREX_CORE.mad:621`, `include/FOREX.labels.md:678` | TAK/PG | 0 |
| `NN` | LABEL(md) | `include/LO_GEN.labels.md:1551` | — | 0 |
| `NNNNB` | LABEL(md) | `include/LO_GEN.labels.md:1090` | — | 0 |
| `NT0533` | LABEL(md)/TEXT | `src/LO_GEN.mad:1586`, `include/LO_GEN.labels.md:408` | 8HPOWER | 0 |
| `NT0535` | LABEL(md)/TEXT | `src/LO_GEN.mad:1590`, `include/LO_GEN.labels.md:410` | 8HA/RHOCHI | 0 |
| `NT0537` | LABEL(md)/TEXT | `src/LO_GEN.mad:1594`, `include/LO_GEN.labels.md:412` | 8HA/NOT | 0 |
| `NT0541` | LABEL(md)/TEXT | `src/LO_GEN.mad:1598`, `include/LO_GEN.labels.md:414` | 8HA/AND | 0 |
| `NT0543` | LABEL(md)/TEXT | `src/LO_GEN.mad:1602`, `include/LO_GEN.labels.md:416` | 8HFT*621 | 0 |
| `NT0545` | LABEL(md)/TEXT | `src/LO_GEN.mad:1606`, `include/LO_GEN.labels.md:418` | 8HFT*002 | 0 |
| `NT0547` | LABEL(md)/TEXT | `src/LO_GEN.mad:1610`, `include/LO_GEN.labels.md:420` | 8HFD*002 | 0 |
| `NT0551` | LABEL(md)/TEXT | `src/LO_GEN.mad:1614`, `include/LO_GEN.labels.md:422` | 8HFC*002 | 0 |
| `NT0553` | LABEL(md)/TEXT | `src/LO_GEN.mad:1618`, `include/LO_GEN.labels.md:424` | 8HFT*003 | 0 |
| `NT0555` | LABEL(md)/TEXT | `src/LO_GEN.mad:1622`, `include/LO_GEN.labels.md:426` | 8HFT*521 | 0 |
| `NT0557` | LABEL(md)/TEXT | `src/LO_GEN.mad:1626`, `include/LO_GEN.labels.md:428` | 8HFT*721 | 0 |
| `NT0561` | LABEL(md)/TEXT | `src/LO_GEN.mad:1630`, `include/LO_GEN.labels.md:430` | 8HFT*722 | 0 |
| `NT0563` | LABEL(md)/TEXT | `src/LO_GEN.mad:1634`, `include/LO_GEN.labels.md:432` | 8HFD*722 | 0 |
| `NT0565` | LABEL(md)/TEXT | `src/LO_GEN.mad:1638`, `include/LO_GEN.labels.md:434` | 8HFC*722 | 0 |
| `NT0567` | LABEL(md)/TEXT | `src/LO_GEN.mad:1642`, `include/LO_GEN.labels.md:436` | 8HFT*723 | 0 |
| `NT0571` | LABEL(md)/TEXT | `src/LO_GEN.mad:1646`, `include/LO_GEN.labels.md:438` | 8HFT*641 | 0 |
| `NT0573` | LABEL(md)/TEXT | `src/LO_GEN.mad:1650`, `include/LO_GEN.labels.md:440` | 8HFT*642 | 0 |
| `NT0575` | LABEL(md)/TEXT | `src/LO_GEN.mad:1654`, `include/LO_GEN.labels.md:442` | 8HFD*642 | 0 |
| `NT0577` | LABEL(md)/TEXT | `src/LO_GEN.mad:1658`, `include/LO_GEN.labels.md:444` | 8HFC*642 | 0 |
| `NT0601` | LABEL(md)/TEXT | `src/LO_GEN.mad:1662`, `include/LO_GEN.labels.md:446` | 8HFT*643 | 0 |
| `NT0603` | LABEL(md)/TEXT | `src/LO_GEN.mad:1666`, `include/LO_GEN.labels.md:448` | 8HFT*541 | 0 |
| `NT0605` | LABEL(md)/TEXT | `src/LO_GEN.mad:1670`, `include/LO_GEN.labels.md:450` | 8HFT*561 | 0 |
| `NT0607` | LABEL(md)/TEXT | `src/LO_GEN.mad:1674`, `include/LO_GEN.labels.md:452` | 8HFT*571 | 0 |
| `NT0611` | LABEL(md)/TEXT | `src/LO_GEN.mad:1678`, `include/LO_GEN.labels.md:454` | 8HFT*531 | 0 |
| `NT0613` | LABEL(md)/TEXT | `src/LO_GEN.mad:1682`, `include/LO_GEN.labels.md:456` | 8HFT*611 | 0 |
| `NT0615` | LABEL(md)/TEXT | `src/LO_GEN.mad:1686`, `include/LO_GEN.labels.md:458` | 8H*REWIN | 0 |
| `NT0617` | LABEL(md)/TEXT | `src/LO_GEN.mad:1690`, `include/LO_GEN.labels.md:460` | 8H*BACKS | 0 |
| `NT0621` | LABEL(md)/TEXT | `src/LO_GEN.mad:1694`, `include/LO_GEN.labels.md:462` | 8H*ENDFI | 0 |
| `NT0623` | LABEL(md)/TEXT | `src/LO_GEN.mad:1698`, `include/LO_GEN.labels.md:464` | 8HSTOP* | 0 |
| `OCTBGN` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:435`, `include/FOREX.labels.md:557` | — | 0 |
| `OCTDC` | NAME/XREF(md) | `src/FOREX_DECODER_DISASM.mad:248`, `include/RUNTIME_DECODER.xref.md:21` | — | 0 |
| `OCTEX` | NAME/XREF(md) | `src/FOREX_DECODER_DISASM.mad:297`, `include/RUNTIME_DECODER.xref.md:24` | — | 0 |
| `OCTEXF` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:485`, `include/FOREX.labels.md:70`, `include/FOREX.labels.md:561` | — | 0 |
| `OCTTDEC` | XREF(md) | `include/RUNTIME_DECODER.xref.md:21`, `include/RUNTIME_DECODER.xref.md:24`, `include/RUNTIME_DECODER.xref.md:74` | — | 0 |
| `OCT_6SYMB` | XREF(md) | `include/RUNTIME_DECODER.xref.md:23` | — | 0 |
| `OCT_CYCLE` | XREF(md) | `include/RUNTIME_DECODER.xref.md:22` | — | 0 |
| `OCT_DEC` | XREF(md) | `include/RUNTIME_DECODER.xref.md:21` | — | 0 |
| `OCT_DEC_EXFOR` | XREF(md) | `include/RUNTIME_DECODER.xref.md:24` | — | 0 |
| `OCT_EXFOR_LOOP` | XREF(md) | `include/RUNTIME_DECODER.xref.md:25` | — | 0 |
| `OCT_EXFOR_RETURN` | XREF(md) | `include/RUNTIME_DECODER.xref.md:26` | — | 0 |
| `OPRTR` | LABEL(md)/SUBP | `src/LO_GEN.mad:36`, `src/LO_SYN.mad:35`, `include/FOREX_ROOT.mad:76`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | — | 0 |
| `OX000` | COMMON | `src/FOREX_DECODER_DISASM.mad:298` | — | 0 |
| `P10_06` | LABEL(md) | `include/FOREX.labels.md:597` | — | 0 |
| `PGPGGO` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:285`, `include/FOREX.labels.md:585` | — | 0 |
| `PRBKLN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:45`, `include/FOREX.labels.md:333`, `include/FOREX.labels.md:598` | 002 | 0 |
| `PREPDAT` | XREF(md) | `include/RUNTIME_DECODER.xref.md:18` | — | 0 |
| `PRINT_TIME` | XREF(md) | `include/RUNTIME_DECODER.xref.md:35` | 0o074013 | 0 |
| `PRTIME` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:254`, `include/FOREX_ROOT.mad:111`, `include/FOREX.labels.md:29`, `include/FOREX.labels.md:80`, `include/FOREX.labels.md:601` | — | 0 |
| `PU` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `REAL` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `RI0057` | LABEL(md) | `include/LO_GEN.labels.md:108`, `include/LO_GEN.labels.md:1112`, `include/LO_GEN.labels.md:1313` | 0o277557 | 0 |
| `RI1716` | LABEL(md) | `include/LO_GEN.labels.md:1035` | 0o301416 | 0 |
| `RI1736` | LABEL(md) | `include/LO_GEN.labels.md:1051` | 0o301436 | 0 |
| `RI1740` | LABEL(md) | `include/LO_GEN.labels.md:1053` | 0o301440 | 0 |
| `RI1751` | LABEL(md) | `include/LO_GEN.labels.md:1062` | 0o301451 | 0 |
| `RI1753` | LABEL(md) | `include/LO_GEN.labels.md:1064` | 0o301453 | 0 |
| `RI1764` | LABEL(md) | `include/LO_GEN.labels.md:1073` | 0o301464 | 0 |
| `RMON` | LABEL(md) | `include/FOREX.labels.md:29`, `include/FOREX.labels.md:80` | 0o510317 | 0 |
| `RR0014` | LABEL(md) | `include/LO_GEN.labels.md:73`, `include/LO_GEN.labels.md:1312` | 0o277514 | 0 |
| `RR0015` | LABEL(md) | `include/LO_GEN.labels.md:74`, `include/LO_GEN.labels.md:1312` | 0o277515 | 0 |
| `RR0060` | LABEL(md) | `include/LO_GEN.labels.md:109`, `include/LO_GEN.labels.md:1312` | 0o277560 | 0 |
| `RR0164` | LABEL(md) | `include/LO_GEN.labels.md:177` | 0o277664 | 0 |
| `RR0310` | LABEL(md) | `include/LO_GEN.labels.md:261`, `include/LO_GEN.labels.md:1314` | 0o300010 | 0 |
| `RR0311` | LABEL(md) | `include/LO_GEN.labels.md:262` | 0o300011 | 0 |
| `RR0735` | LABEL(md) | `include/LO_GEN.labels.md:538` | 0o300435 | 0 |
| `RR1024` | LABEL(md) | `include/LO_GEN.labels.md:593` | 0o300524 | 0 |
| `RR1103` | LABEL(md) | `include/LO_GEN.labels.md:640` | 0o300603 | 0 |
| `RR1123` | LABEL(md) | `include/LO_GEN.labels.md:656` | 0o300623 | 0 |
| `RR1133` | LABEL(md) | `include/LO_GEN.labels.md:664` | 0o300633 | 0 |
| `RR1144` | LABEL(md) | `include/LO_GEN.labels.md:673` | 0o300644 | 0 |
| `RR1165` | LABEL(md) | `include/LO_GEN.labels.md:690` | 0o300665 | 0 |
| `RR1247` | LABEL(md) | `include/LO_GEN.labels.md:740` | 0o300747 | 0 |
| `RR1263` | LABEL(md) | `include/LO_GEN.labels.md:752` | 0o300763 | 0 |
| `RR1347` | LABEL(md) | `include/LO_GEN.labels.md:804` | 0o301047 | 0 |
| `RR1370` | LABEL(md) | `include/LO_GEN.labels.md:821` | 0o301070 | 0 |
| `RR1717` | LABEL(md) | `include/LO_GEN.labels.md:1036` | 0o301417 | 0 |
| `RR1730` | LABEL(md) | `include/LO_GEN.labels.md:1045` | 0o301430 | 0 |
| `RR1731` | LABEL(md) | `include/LO_GEN.labels.md:1046` | 0o301431 | 0 |
| `RR1754` | LABEL(md) | `include/LO_GEN.labels.md:1065` | 0o301454 | 0 |
| `RS0004` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:262`, `src/LO_GEN.mad:638`, `src/LO_GEN.mad:649`, `src/LO_GEN.mad:655`, `src/LO_GEN.mad:673`, `src/LO_GEN.mad:694` … (+22) | 4 | 0 |
| `RS0008` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:265`, `src/LO_GEN.mad:1105`, `src/LO_GEN.mad:1150`, `src/LO_GEN.mad:1183`, `src/LO_GEN.mad:2161`, `src/LO_GEN.mad:3180` … (+1) | 8 | 0 |
| `RS0010` | LABEL(md) | `include/LO_GEN.labels.md:69`, `include/LO_GEN.labels.md:1166`, `include/LO_GEN.labels.md:1310` | 0o277510 | 0 |
| `RS0016` | LABEL(md) | `include/LO_GEN.labels.md:75`, `include/LO_GEN.labels.md:1166` | 0o277516 | 0 |
| `RS0017` | LABEL(md) | `include/LO_GEN.labels.md:76`, `include/LO_GEN.labels.md:1313` | 0o277517 | 0 |
| `RS0031` | LABEL(md) | `include/LO_GEN.labels.md:86`, `include/LO_GEN.labels.md:1207`, `include/LO_GEN.labels.md:1318` | 0o277531 | 0 |
| `RS0061` | LABEL(md) | `include/LO_GEN.labels.md:110`, `include/LO_GEN.labels.md:1207` | 0o277561 | 0 |
| `RS0107` | LABEL(md) | `include/LO_GEN.labels.md:132` | 0o277607 | 0 |
| `RS0114` | LABEL(md) | `include/LO_GEN.labels.md:137`, `include/LO_GEN.labels.md:1237`, `include/LO_GEN.labels.md:1315` | 0o277614 | 0 |
| `RS0121` | LABEL(md) | `include/LO_GEN.labels.md:142`, `include/LO_GEN.labels.md:1238`, `include/LO_GEN.labels.md:1315` | 0o277621 | 0 |
| `RS0124` | LABEL(md) | `include/LO_GEN.labels.md:145`, `include/LO_GEN.labels.md:1239` | 0o277624 | 0 |
| `RS0132` | LABEL(md) | `include/LO_GEN.labels.md:151`, `include/LO_GEN.labels.md:1244` | 0o277632 | 0 |
| `RS0145` | LABEL(md) | `include/LO_GEN.labels.md:162`, `include/LO_GEN.labels.md:1246` | 0o277645 | 0 |
| `RS0152` | LABEL(md) | `include/LO_GEN.labels.md:167` | 0o277652 | 0 |
| `RS0166` | LABEL(md) | `include/LO_GEN.labels.md:179` | 0o277666 | 0 |
| `RS0170` | LABEL(md) | `include/LO_GEN.labels.md:181` | 0o277670 | 0 |
| `RS0211` | LABEL(md) | `include/LO_GEN.labels.md:198` | 0o277711 | 0 |
| `RS0216` | LABEL(md) | `include/LO_GEN.labels.md:203`, `include/LO_GEN.labels.md:1247` | 0o277716 | 0 |
| `RS0223` | LABEL(md) | `include/LO_GEN.labels.md:208`, `include/LO_GEN.labels.md:1237` | 0o277723 | 0 |
| `RS0230` | LABEL(md) | `include/LO_GEN.labels.md:213`, `include/LO_GEN.labels.md:1245` | 0o277730 | 0 |
| `RS0274` | LABEL(md) | `include/LO_GEN.labels.md:249` | 0o277774 | 0 |
| `RS0324` | LABEL(md) | `include/LO_GEN.labels.md:273`, `include/LO_GEN.labels.md:1236` | 0o300024 | 0 |
| `RS0325` | LABEL(md) | `include/LO_GEN.labels.md:274`, `include/LO_GEN.labels.md:1181` | 0o300025 | 0 |
| `RS0330` | LABEL(md) | `include/LO_GEN.labels.md:277`, `include/LO_GEN.labels.md:1182` | 0o300030 | 0 |
| `RS0344` | LABEL(md) | `include/LO_GEN.labels.md:289`, `include/LO_GEN.labels.md:1183` | 0o300044 | 0 |
| `RS0345` | LABEL(md) | `include/LO_GEN.labels.md:290` | 0o300045 | 0 |
| `RS0353` | LABEL(md) | `include/LO_GEN.labels.md:296`, `include/LO_GEN.labels.md:1244` | 0o300053 | 0 |
| `RS0360` | LABEL(md) | `include/LO_GEN.labels.md:301`, `include/LO_GEN.labels.md:1236` | 0o300060 | 0 |
| `RS0361` | LABEL(md) | `include/LO_GEN.labels.md:302`, `include/LO_GEN.labels.md:1184` | 0o300061 | 0 |
| `RS0366` | LABEL(md) | `include/LO_GEN.labels.md:307`, `include/LO_GEN.labels.md:1243` | 0o300066 | 0 |
| `RS0452` | LABEL(md) | `include/LO_GEN.labels.md:359`, `include/LO_GEN.labels.md:1188` | 0o300152 | 0 |
| `RS0453` | LABEL(md) | `include/LO_GEN.labels.md:360`, `include/LO_GEN.labels.md:1185` | 0o300153 | 0 |
| `RS0454` | LABEL(md) | `include/LO_GEN.labels.md:361`, `include/LO_GEN.labels.md:1200` | 0o300154 | 0 |
| `RS0455` | LABEL(md) | `include/LO_GEN.labels.md:362`, `include/LO_GEN.labels.md:1201` | 0o300155 | 0 |
| `RS0456` | LABEL(md) | `include/LO_GEN.labels.md:363`, `include/LO_GEN.labels.md:1202` | 0o300156 | 0 |
| `RS0457` | LABEL(md) | `include/LO_GEN.labels.md:364`, `include/LO_GEN.labels.md:1197` | 0o300157 | 0 |
| `RS0460` | LABEL(md) | `include/LO_GEN.labels.md:365`, `include/LO_GEN.labels.md:1196` | 0o300160 | 0 |
| `RS0461` | LABEL(md) | `include/LO_GEN.labels.md:366`, `include/LO_GEN.labels.md:1195` | 0o300161 | 0 |
| `RS0462` | LABEL(md) | `include/LO_GEN.labels.md:367`, `include/LO_GEN.labels.md:1203` | 0o300162 | 0 |
| `RS0474` | LABEL(md) | `include/LO_GEN.labels.md:377`, `include/LO_GEN.labels.md:1199` | 0o300174 | 0 |
| `RS0475` | LABEL(md) | `include/LO_GEN.labels.md:378`, `include/LO_GEN.labels.md:1198` | 0o300175 | 0 |
| `RS0476` | LABEL(md) | `include/LO_GEN.labels.md:379`, `include/LO_GEN.labels.md:1192` | 0o300176 | 0 |
| `RS0477` | LABEL(md) | `include/LO_GEN.labels.md:380`, `include/LO_GEN.labels.md:1189` | 0o300177 | 0 |
| `RS0521` | LABEL(md) | `include/LO_GEN.labels.md:398` | 0o300221 | 0 |
| `RS0522` | LABEL(md) | `include/LO_GEN.labels.md:399`, `include/LO_GEN.labels.md:1241` | 0o300222 | 0 |
| `RS0523` | LABEL(md) | `include/LO_GEN.labels.md:400`, `include/LO_GEN.labels.md:1244` | 0o300223 | 0 |
| `RS0524` | LABEL(md) | `include/LO_GEN.labels.md:401`, `include/LO_GEN.labels.md:1242` | 0o300224 | 0 |
| `RS0525` | LABEL(md) | `include/LO_GEN.labels.md:402`, `include/LO_GEN.labels.md:1241` | 0o300225 | 0 |
| `RS0526` | LABEL(md) | `include/LO_GEN.labels.md:403`, `include/LO_GEN.labels.md:1244` | 0o300226 | 0 |
| `RS0527` | LABEL(md) | `include/LO_GEN.labels.md:404`, `include/LO_GEN.labels.md:1242` | 0o300227 | 0 |
| `RS0631` | LABEL(md) | `include/LO_GEN.labels.md:470` | 0o300331 | 0 |
| `RS0642` | LABEL(md) | `include/LO_GEN.labels.md:479`, `include/LO_GEN.labels.md:1237` | 0o300342 | 0 |
| `RS0650` | LABEL(md) | `include/LO_GEN.labels.md:485`, `include/LO_GEN.labels.md:1208` | 0o300350 | 0 |
| `RS0651` | LABEL(md) | `include/LO_GEN.labels.md:486`, `include/LO_GEN.labels.md:1256` | 0o300351 | 0 |
| `RS0654` | LABEL(md) | `include/LO_GEN.labels.md:489`, `include/LO_GEN.labels.md:1266` | 0o300354 | 0 |
| `RS0655` | LABEL(md) | `include/LO_GEN.labels.md:490`, `include/LO_GEN.labels.md:1255` | 0o300355 | 0 |
| `RS0660` | LABEL(md) | `include/LO_GEN.labels.md:493`, `include/LO_GEN.labels.md:1266` | 0o300360 | 0 |
| `RS0661` | LABEL(md) | `include/LO_GEN.labels.md:494`, `include/LO_GEN.labels.md:1255` | 0o300361 | 0 |
| `RS0663` | LABEL(md) | `include/LO_GEN.labels.md:496`, `include/LO_GEN.labels.md:1208` | 0o300363 | 0 |
| `RS0664` | LABEL(md) | `include/LO_GEN.labels.md:497`, `include/LO_GEN.labels.md:1256` | 0o300364 | 0 |
| `RS0672` | LABEL(md) | `include/LO_GEN.labels.md:503`, `include/LO_GEN.labels.md:1240` | 0o300372 | 0 |
| `RS0716` | LABEL(md) | `include/LO_GEN.labels.md:523`, `include/LO_GEN.labels.md:1242` | 0o300416 | 0 |
| `RS0727` | LABEL(md) | `include/LO_GEN.labels.md:532`, `include/LO_GEN.labels.md:1243` | 0o300427 | 0 |
| `RS0740` | LABEL(md) | `include/LO_GEN.labels.md:541` | 0o300440 | 0 |
| `RS0750` | LABEL(md) | `include/LO_GEN.labels.md:549`, `include/LO_GEN.labels.md:1235` | 0o300450 | 0 |
| `RS1000` | LABEL(md) | `include/LO_GEN.labels.md:573`, `include/LO_GEN.labels.md:1239` | 0o300500 | 0 |
| `RS1003` | LABEL(md) | `include/LO_GEN.labels.md:576`, `include/LO_GEN.labels.md:1209` | 0o300503 | 0 |
| `RS1004` | LABEL(md) | `include/LO_GEN.labels.md:577`, `include/LO_GEN.labels.md:1255` | 0o300504 | 0 |
| `RS1006` | LABEL(md) | `include/LO_GEN.labels.md:579` | 0o300506 | 0 |
| `RS1017` | LABEL(md) | `include/LO_GEN.labels.md:588`, `include/LO_GEN.labels.md:1208` | 0o300517 | 0 |
| `RS1020` | LABEL(md) | `include/LO_GEN.labels.md:589`, `include/LO_GEN.labels.md:1256` | 0o300520 | 0 |
| `RS1037` | LABEL(md) | `include/LO_GEN.labels.md:604` | 0o300537 | 0 |
| `RS1042` | LABEL(md) | `include/LO_GEN.labels.md:607`, `include/LO_GEN.labels.md:1257` | 0o300542 | 0 |
| `RS1067` | LABEL(md) | `include/LO_GEN.labels.md:628`, `include/LO_GEN.labels.md:1209` | 0o300567 | 0 |
| `RS1070` | LABEL(md) | `include/LO_GEN.labels.md:629`, `include/LO_GEN.labels.md:1257` | 0o300570 | 0 |
| `RS1101` | LABEL(md) | `include/LO_GEN.labels.md:638`, `include/LO_GEN.labels.md:1255` | 0o300601 | 0 |
| `RS1102` | LABEL(md) | `include/LO_GEN.labels.md:639`, `include/LO_GEN.labels.md:1256` | 0o300602 | 0 |
| `RS1110` | LABEL(md) | `include/LO_GEN.labels.md:645`, `include/LO_GEN.labels.md:1248` | 0o300610 | 0 |
| `RS1112` | LABEL(md) | `include/LO_GEN.labels.md:647` | 0o300612 | 0 |
| `RS1122` | LABEL(md) | `include/LO_GEN.labels.md:655` | 0o300622 | 0 |
| `RS1131` | LABEL(md) | `include/LO_GEN.labels.md:662` | 0o300631 | 0 |
| `RS1132` | LABEL(md) | `include/LO_GEN.labels.md:663` | 0o300632 | 0 |
| `RS1142` | LABEL(md) | `include/LO_GEN.labels.md:671` | 0o300642 | 0 |
| `RS1143` | LABEL(md) | `include/LO_GEN.labels.md:672` | 0o300643 | 0 |
| `RS1150` | LABEL(md) | `include/LO_GEN.labels.md:677`, `include/LO_GEN.labels.md:1239` | 0o300650 | 0 |
| `RS1164` | LABEL(md) | `include/LO_GEN.labels.md:689`, `include/LO_GEN.labels.md:1236` | 0o300664 | 0 |
| `RS1172` | LABEL(md) | `include/LO_GEN.labels.md:695`, `include/LO_GEN.labels.md:1236` | 0o300672 | 0 |
| `RS1204` | LABEL(md) | `include/LO_GEN.labels.md:705` | 0o300704 | 0 |
| `RS1236` | LABEL(md) | `include/LO_GEN.labels.md:731`, `include/LO_GEN.labels.md:1190` | 0o300736 | 0 |
| `RS1246` | LABEL(md) | `include/LO_GEN.labels.md:739`, `include/LO_GEN.labels.md:1191` | 0o300746 | 0 |
| `RS1250` | LABEL(md) | `include/LO_GEN.labels.md:741` | 0o300750 | 0 |
| `RS1262` | LABEL(md) | `include/LO_GEN.labels.md:751`, `include/LO_GEN.labels.md:1190` | 0o300762 | 0 |
| `RS1264` | LABEL(md) | `include/LO_GEN.labels.md:753` | 0o300764 | 0 |
| `RS1266` | LABEL(md) | `include/LO_GEN.labels.md:755`, `include/LO_GEN.labels.md:1259` | 0o300766 | 0 |
| `RS1270` | LABEL(md) | `include/LO_GEN.labels.md:757` | 0o300770 | 0 |
| `RS1301` | LABEL(md) | `include/LO_GEN.labels.md:766`, `include/LO_GEN.labels.md:1258` | 0o301001 | 0 |
| `RS1313` | LABEL(md) | `include/LO_GEN.labels.md:776` | 0o301013 | 0 |
| `RS1352` | LABEL(md) | `include/LO_GEN.labels.md:807` | 0o301052 | 0 |
| `RS1362` | LABEL(md) | `include/LO_GEN.labels.md:815` | 0o301062 | 0 |
| `RS1403` | LABEL(md) | `include/LO_GEN.labels.md:832` | 0o301103 | 0 |
| `RS1421` | LABEL(md) | `include/LO_GEN.labels.md:846` | 0o301121 | 0 |
| `RS1432` | LABEL(md) | `include/LO_GEN.labels.md:855` | 0o301132 | 0 |
| `RS1441` | LABEL(md) | `include/LO_GEN.labels.md:862` | 0o301141 | 0 |
| `RS1507` | LABEL(md) | `include/LO_GEN.labels.md:900`, `include/LO_GEN.labels.md:1240` | 0o301207 | 0 |
| `RS1535` | LABEL(md) | `include/LO_GEN.labels.md:922` | 0o301235 | 0 |
| `RS1605` | LABEL(md) | `include/LO_GEN.labels.md:962` | 0o301305 | 0 |
| `RS1613` | LABEL(md) | `include/LO_GEN.labels.md:968`, `include/LO_GEN.labels.md:1250` | 0o301313 | 0 |
| `RS1614` | LABEL(md) | `include/LO_GEN.labels.md:969` | 0o301314 | 0 |
| `RS1620` | LABEL(md) | `include/LO_GEN.labels.md:973`, `include/LO_GEN.labels.md:1252` | 0o301320 | 0 |
| `RS1630` | LABEL(md) | `include/LO_GEN.labels.md:981` | 0o301330 | 0 |
| `RS1633` | LABEL(md) | `include/LO_GEN.labels.md:984`, `include/LO_GEN.labels.md:1235` | 0o301333 | 0 |
| `RS1713` | LABEL(md) | `include/LO_GEN.labels.md:1032` | 0o301413 | 0 |
| `RS1720` | LABEL(md) | `include/LO_GEN.labels.md:1037` | 0o301420 | 0 |
| `RS1724` | LABEL(md) | `include/LO_GEN.labels.md:1041` | 0o301424 | 0 |
| `RS1742` | LABEL(md) | `include/LO_GEN.labels.md:1055` | 0o301442 | 0 |
| `RS1755` | LABEL(md) | `include/LO_GEN.labels.md:1066`, `include/LO_GEN.labels.md:1207` | 0o301455 | 0 |
| `RS1757` | LABEL(md) | `include/LO_GEN.labels.md:1068`, `include/LO_GEN.labels.md:1314` | 0o301457 | 0 |
| `RS1761` | LABEL(md) | `include/LO_GEN.labels.md:1070` | 0o301461 | 0 |
| `SB1046` | LABEL(md) | `include/LO_GEN.labels.md:611` | 0o300546 | 0 |
| `SB1111` | LABEL(md) | `include/LO_GEN.labels.md:646`, `include/LO_GEN.labels.md:1267` | 0o300611 | 0 |
| `SH0063` | LABEL(md) | `include/LO_GEN.labels.md:112`, `include/LO_GEN.labels.md:1144` | 0o277563 | 0 |
| `SH0066` | LABEL(md) | `include/LO_GEN.labels.md:115`, `include/LO_GEN.labels.md:1144` | 0o277566 | 0 |
| `SH0070` | LABEL(md) | `include/LO_GEN.labels.md:117`, `include/LO_GEN.labels.md:1111` | 0o277570 | 0 |
| `SH0153` | LABEL(md) | `include/LO_GEN.labels.md:168`, `include/LO_GEN.labels.md:1111` | 0o277653 | 0 |
| `SH0163` | LABEL(md) | `include/LO_GEN.labels.md:176`, `include/LO_GEN.labels.md:1131` | 0o277663 | 0 |
| `SH0172` | LABEL(md) | `include/LO_GEN.labels.md:183`, `include/LO_GEN.labels.md:1144` | 0o277672 | 0 |
| `SH0212` | LABEL(md) | `include/LO_GEN.labels.md:199`, `include/LO_GEN.labels.md:1143` | 0o277712 | 0 |
| `SH0256` | LABEL(md) | `include/LO_GEN.labels.md:235`, `include/LO_GEN.labels.md:1131` | 0o277756 | 0 |
| `SH1034` | LABEL(md) | `include/LO_GEN.labels.md:601`, `include/LO_GEN.labels.md:1219` | 0o300534 | 0 |
| `SH1045` | LABEL(md) | `include/LO_GEN.labels.md:610`, `include/LO_GEN.labels.md:1099` | 0o300545 | 0 |
| `SH1055` | LABEL(md) | `include/LO_GEN.labels.md:618`, `include/LO_GEN.labels.md:1206` | 0o300555 | 0 |
| `SH1275` | LABEL(md) | `include/LO_GEN.labels.md:762`, `include/LO_GEN.labels.md:1222` | 0o300775 | 0 |
| `SH1363` | LABEL(md) | `include/LO_GEN.labels.md:816`, `include/LO_GEN.labels.md:1109` | 0o301063 | 0 |
| `SH1443` | LABEL(md) | `include/LO_GEN.labels.md:864`, `include/LO_GEN.labels.md:1233` | 0o301143 | 0 |
| `SH1602` | LABEL(md) | `include/LO_GEN.labels.md:959` | 0o301302 | 0 |
| `SH1744` | LABEL(md) | `include/LO_GEN.labels.md:1057`, `include/LO_GEN.labels.md:1233` | 0o301444 | 0 |
| `START` | ENTRY/LABEL(md) | `src/LO_GEN.mad:26`, `include/FOREX.labels.md:20`, `include/LO_GEN.labels.md:17`, `include/LO_GEN.labels.md:17`, `include/LO_GEN.labels.md:17`, `include/LO_SYN.labels.md:11` | — | 0 |
| `STKOF7` | LABEL(md) | `include/FOREX.labels.md:615` | — | 0 |
| `STOP` | LABEL(md) | `include/FOREX.labels.md:31` | 0o510332 | 0 |
| `TAK/PG` | SUBP | `src/LO_SYN.mad:29` | — | 0 |
| `TEXT` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `TIMMSK` | LABEL(md)/TEXT | `src/FOREX_RUNTIME.mad:420`, `include/FOREX.labels.md:646` | — | 0 |
| `TL0005` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:87`, `include/FOREX.labels.md:279`, `include/FOREX.labels.md:623` | 6H0000 | 0 |
| `TL0009` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:91`, `include/FOREX.labels.md:283`, `include/FOREX.labels.md:627` | 6H03 0 | 0 |
| `TL0020` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:102`, `include/FOREX.labels.md:294`, `include/FOREX.labels.md:638` | 6H'231'  ЯHB | 0 |
| `TXAAND` | LABEL(md)/TEXT | `src/LO_GEN.mad:506`, `include/LO_GEN.labels.md:35` | 8HA/AND | 0 |
| `TXANOT` | LABEL(md)/TEXT | `src/LO_GEN.mad:505`, `include/LO_GEN.labels.md:34` | 8HA/NOT | 0 |
| `TXARHO` | LABEL(md)/TEXT | `src/LO_GEN.mad:504`, `include/LO_GEN.labels.md:33` | 8HA/RHOCHI | 0 |
| `TXBACK` | LABEL(md)/TEXT | `src/LO_GEN.mad:529`, `include/LO_GEN.labels.md:58` | 8H*BACKS | 0 |
| `TXC002` | LABEL(md)/TEXT | `src/LO_GEN.mad:510`, `include/LO_GEN.labels.md:39` | 8HFC*002 | 0 |
| `TXC642` | LABEL(md)/TEXT | `src/LO_GEN.mad:521`, `include/LO_GEN.labels.md:50` | 8HFC*642 | 0 |
| `TXC722` | LABEL(md)/TEXT | `src/LO_GEN.mad:516`, `include/LO_GEN.labels.md:45` | 8HFC*722 | 0 |
| `TXD002` | LABEL(md)/TEXT | `src/LO_GEN.mad:509`, `include/LO_GEN.labels.md:38` | 8HFD*002 | 0 |
| `TXD642` | LABEL(md)/TEXT | `src/LO_GEN.mad:520`, `include/LO_GEN.labels.md:49` | 8HFD*642 | 0 |
| `TXD722` | LABEL(md)/TEXT | `src/LO_GEN.mad:515`, `include/LO_GEN.labels.md:44` | 8HFD*722 | 0 |
| `TXENDF` | LABEL(md)/TEXT | `src/LO_GEN.mad:530`, `include/LO_GEN.labels.md:59` | 8H*ENDFI | 0 |
| `TXF002` | LABEL(md)/TEXT | `src/LO_GEN.mad:508`, `include/LO_GEN.labels.md:37` | 8HFT*002 | 0 |
| `TXF003` | LABEL(md)/TEXT | `src/LO_GEN.mad:511`, `include/LO_GEN.labels.md:40` | 8HFT*003 | 0 |
| `TXF521` | LABEL(md)/TEXT | `src/LO_GEN.mad:512`, `include/LO_GEN.labels.md:41` | 8HFT*521 | 0 |
| `TXF531` | LABEL(md)/TEXT | `src/LO_GEN.mad:526`, `include/LO_GEN.labels.md:55` | 8HFT*531 | 0 |
| `TXF541` | LABEL(md)/TEXT | `src/LO_GEN.mad:523`, `include/LO_GEN.labels.md:52` | 8HFT*541 | 0 |
| `TXF561` | LABEL(md)/TEXT | `src/LO_GEN.mad:524`, `include/LO_GEN.labels.md:53` | 8HFT*561 | 0 |
| `TXF571` | LABEL(md)/TEXT | `src/LO_GEN.mad:525`, `include/LO_GEN.labels.md:54` | 8HFT*571 | 0 |
| `TXF611` | LABEL(md)/TEXT | `src/LO_GEN.mad:527`, `include/LO_GEN.labels.md:56` | 8HFT*611 | 0 |
| `TXF621` | LABEL(md)/TEXT | `src/LO_GEN.mad:507`, `include/LO_GEN.labels.md:36` | 8HFT*621 | 0 |
| `TXF641` | LABEL(md)/TEXT | `src/LO_GEN.mad:518`, `include/LO_GEN.labels.md:47` | 8HFT*641 | 0 |
| `TXF642` | LABEL(md)/TEXT | `src/LO_GEN.mad:519`, `include/LO_GEN.labels.md:48` | 8HFT*642 | 0 |
| `TXF643` | LABEL(md)/TEXT | `src/LO_GEN.mad:522`, `include/LO_GEN.labels.md:51` | 8HFT*643 | 0 |
| `TXF721` | LABEL(md)/TEXT | `src/LO_GEN.mad:513`, `include/LO_GEN.labels.md:42` | 8HFT*721 | 0 |
| `TXF722` | LABEL(md)/TEXT | `src/LO_GEN.mad:514`, `include/LO_GEN.labels.md:43` | 8HFT*722 | 0 |
| `TXF723` | LABEL(md)/TEXT | `src/LO_GEN.mad:517`, `include/LO_GEN.labels.md:46` | 8HFT*723 | 0 |
| `TXPOWE` | LABEL(md)/TEXT | `src/LO_GEN.mad:503`, `include/LO_GEN.labels.md:32` | 8HPOWER | 0 |
| `TXREWI` | LABEL(md)/TEXT | `src/LO_GEN.mad:528`, `include/LO_GEN.labels.md:57` | 8H*REWIN | 0 |
| `TXSTOP` | LABEL(md)/TEXT | `src/LO_GEN.mad:531`, `include/LO_GEN.labels.md:60` | 8HSTOP* | 0 |
| `VC0051` | LABEL(md) | `include/LO_GEN.labels.md:102`, `include/LO_GEN.labels.md:1308`, `include/LO_GEN.labels.md:1371` | 0o277551 | 0 |
| `VC1226` | LABEL(md) | `include/LO_GEN.labels.md:723`, `include/LO_GEN.labels.md:1335` | 0o300726 | 0 |
| `VC1355` | LABEL(md) | `include/LO_GEN.labels.md:810`, `include/LO_GEN.labels.md:1336` | 0o301055 | 0 |
| `W0000` | LABEL(md) | `include/LO_GEN.labels.md:61` | 0o277500 | 0 |
| `W0001` | LABEL(md) | `include/LO_GEN.labels.md:62` | 0o277501 | 0 |
| `W0002` | LABEL(md) | `include/LO_GEN.labels.md:63` | 0o277502 | 0 |
| `W0003` | LABEL(md) | `include/LO_GEN.labels.md:64` | 0o277503 | 0 |
| `W0004` | LABEL(md) | `include/LO_GEN.labels.md:65` | 0o277504 | 0 |
| `W0005` | LABEL(md) | `include/LO_GEN.labels.md:66` | 0o277505 | 0 |
| `W0006` | LABEL(md) | `include/LO_GEN.labels.md:67` | 0o277506 | 0 |
| `W0007` | LABEL(md) | `include/LO_GEN.labels.md:68` | 0o277507 | 0 |
| `W0010` | LABEL(md) | `include/LO_GEN.labels.md:69` | 0o277510 | 0 |
| `W0011` | LABEL(md) | `include/LO_GEN.labels.md:70` | 0o277511 | 0 |
| `W0012` | LABEL(md) | `include/LO_GEN.labels.md:71` | 0o277512 | 0 |
| `W0013` | LABEL(md) | `include/LO_GEN.labels.md:72` | 0o277513 | 0 |
| `W0014` | LABEL(md) | `include/LO_GEN.labels.md:73` | 0o277514 | 0 |
| `W0015` | LABEL(md) | `include/LO_GEN.labels.md:74` | 0o277515 | 0 |
| `W0016` | LABEL(md) | `include/LO_GEN.labels.md:75` | 0o277516 | 0 |
| `W0017` | LABEL(md) | `include/LO_GEN.labels.md:76` | 0o277517 | 0 |
| `W0020` | LABEL(md) | `include/LO_GEN.labels.md:77` | 0o277520 | 0 |
| `W0021` | LABEL(md) | `include/LO_GEN.labels.md:78` | 0o277521 | 0 |
| `W0022` | LABEL(md) | `include/LO_GEN.labels.md:79` | 0o277522 | 0 |
| `W0023` | LABEL(md) | `include/LO_GEN.labels.md:80` | 0o277523 | 0 |
| `W0024` | LABEL(md) | `include/LO_GEN.labels.md:81` | 0o277524 | 0 |
| `W0025` | LABEL(md) | `include/LO_GEN.labels.md:82` | 0o277525 | 0 |
| `W0026` | LABEL(md) | `include/LO_GEN.labels.md:83` | 0o277526 | 0 |
| `W0027` | LABEL(md) | `include/LO_GEN.labels.md:84` | 0o277527 | 0 |
| `W0030` | LABEL(md) | `include/LO_GEN.labels.md:85` | 0o277530 | 0 |
| `W0031` | LABEL(md) | `include/LO_GEN.labels.md:86` | 0o277531 | 0 |
| `W0032` | LABEL(md) | `include/LO_GEN.labels.md:87` | 0o277532 | 0 |
| `W0033` | LABEL(md) | `include/LO_GEN.labels.md:88` | 0o277533 | 0 |
| `W0034` | LABEL(md) | `include/LO_GEN.labels.md:89` | 0o277534 | 0 |
| `W0035` | LABEL(md) | `include/LO_GEN.labels.md:90` | 0o277535 | 0 |
| `W0036` | LABEL(md) | `include/LO_GEN.labels.md:91` | 0o277536 | 0 |
| `W0037` | LABEL(md) | `include/LO_GEN.labels.md:92` | 0o277537 | 0 |
| `W0040` | LABEL(md) | `include/LO_GEN.labels.md:93` | 0o277540 | 0 |
| `W0041` | LABEL(md) | `include/LO_GEN.labels.md:94` | 0o277541 | 0 |
| `W0042` | LABEL(md) | `include/LO_GEN.labels.md:95` | 0o277542 | 0 |
| `W0043` | LABEL(md) | `include/LO_GEN.labels.md:96` | 0o277543 | 0 |
| `W0044` | LABEL(md) | `include/LO_GEN.labels.md:97` | 0o277544 | 0 |
| `W0045` | LABEL(md) | `include/LO_GEN.labels.md:98` | 0o277545 | 0 |
| `W0046` | LABEL(md) | `include/LO_GEN.labels.md:99` | 0o277546 | 0 |
| `W0047` | LABEL(md) | `include/LO_GEN.labels.md:100` | 0o277547 | 0 |
| `W0050` | LABEL(md) | `include/LO_GEN.labels.md:101` | 0o277550 | 0 |
| `W0051` | LABEL(md) | `include/LO_GEN.labels.md:102` | 0o277551 | 0 |
| `W0052` | LABEL(md) | `include/LO_GEN.labels.md:103` | 0o277552 | 0 |
| `W0053` | LABEL(md) | `include/LO_GEN.labels.md:104` | 0o277553 | 0 |
| `W0054` | LABEL(md) | `include/LO_GEN.labels.md:105` | 0o277554 | 0 |
| `W0055` | LABEL(md) | `include/LO_GEN.labels.md:106` | 0o277555 | 0 |
| `W0056` | LABEL(md) | `include/LO_GEN.labels.md:107` | 0o277556 | 0 |
| `W0057` | LABEL(md) | `include/LO_GEN.labels.md:108` | 0o277557 | 0 |
| `W0060` | LABEL(md) | `include/LO_GEN.labels.md:109` | 0o277560 | 0 |
| `W0061` | LABEL(md) | `include/LO_GEN.labels.md:110` | 0o277561 | 0 |
| `W0062` | LABEL(md) | `include/LO_GEN.labels.md:111` | 0o277562 | 0 |
| `W0063` | LABEL(md) | `include/LO_GEN.labels.md:112` | 0o277563 | 0 |
| `W0064` | LABEL(md) | `include/LO_GEN.labels.md:113` | 0o277564 | 0 |
| `W0065` | LABEL(md) | `include/LO_GEN.labels.md:114` | 0o277565 | 0 |
| `W0066` | LABEL(md) | `include/LO_GEN.labels.md:115` | 0o277566 | 0 |
| `W0067` | LABEL(md) | `include/LO_GEN.labels.md:116` | 0o277567 | 0 |
| `W0070` | LABEL(md) | `include/LO_GEN.labels.md:117` | 0o277570 | 0 |
| `W0071` | LABEL(md) | `include/LO_GEN.labels.md:118` | 0o277571 | 0 |
| `W0072` | LABEL(md) | `include/LO_GEN.labels.md:119` | 0o277572 | 0 |
| `W0073` | LABEL(md) | `include/LO_GEN.labels.md:120` | 0o277573 | 0 |
| `W0074` | LABEL(md) | `include/LO_GEN.labels.md:121` | 0o277574 | 0 |
| `W0075` | LABEL(md) | `include/LO_GEN.labels.md:122` | 0o277575 | 0 |
| `W0076` | LABEL(md) | `include/LO_GEN.labels.md:123` | 0o277576 | 0 |
| `W0077` | LABEL(md) | `include/LO_GEN.labels.md:124` | 0o277577 | 0 |
| `W0100` | LABEL(md) | `include/LO_GEN.labels.md:125` | 0o277600 | 0 |
| `W0101` | LABEL(md) | `include/LO_GEN.labels.md:126` | 0o277601 | 0 |
| `W0102` | LABEL(md) | `include/LO_GEN.labels.md:127` | 0o277602 | 0 |
| `W0103` | LABEL(md) | `include/LO_GEN.labels.md:128` | 0o277603 | 0 |
| `W0104` | LABEL(md) | `include/LO_GEN.labels.md:129` | 0o277604 | 0 |
| `W0105` | LABEL(md) | `include/LO_GEN.labels.md:130` | 0o277605 | 0 |
| `W0106` | LABEL(md) | `include/LO_GEN.labels.md:131` | 0o277606 | 0 |
| `W0107` | LABEL(md) | `include/LO_GEN.labels.md:132` | 0o277607 | 0 |
| `W0110` | LABEL(md) | `include/LO_GEN.labels.md:133` | 0o277610 | 0 |
| `W0111` | LABEL(md) | `include/LO_GEN.labels.md:134` | 0o277611 | 0 |
| `W0112` | LABEL(md) | `include/LO_GEN.labels.md:135` | 0o277612 | 0 |
| `W0113` | LABEL(md) | `include/LO_GEN.labels.md:136` | 0o277613 | 0 |
| `W0114` | LABEL(md) | `include/LO_GEN.labels.md:137` | 0o277614 | 0 |
| `W0115` | LABEL(md) | `include/LO_GEN.labels.md:138` | 0o277615 | 0 |
| `W0116` | LABEL(md) | `include/LO_GEN.labels.md:139` | 0o277616 | 0 |
| `W0117` | LABEL(md) | `include/LO_GEN.labels.md:140` | 0o277617 | 0 |
| `W0120` | LABEL(md) | `include/LO_GEN.labels.md:141` | 0o277620 | 0 |
| `W0121` | LABEL(md) | `include/LO_GEN.labels.md:142` | 0o277621 | 0 |
| `W0122` | LABEL(md) | `include/LO_GEN.labels.md:143` | 0o277622 | 0 |
| `W0123` | LABEL(md) | `include/LO_GEN.labels.md:144` | 0o277623 | 0 |
| `W0124` | LABEL(md) | `include/LO_GEN.labels.md:145` | 0o277624 | 0 |
| `W0125` | LABEL(md) | `include/LO_GEN.labels.md:146` | 0o277625 | 0 |
| `W0126` | LABEL(md) | `include/LO_GEN.labels.md:147` | 0o277626 | 0 |
| `W0127` | LABEL(md) | `include/LO_GEN.labels.md:148` | 0o277627 | 0 |
| `W0130` | LABEL(md) | `include/LO_GEN.labels.md:149` | 0o277630 | 0 |
| `W0131` | LABEL(md) | `include/LO_GEN.labels.md:150` | 0o277631 | 0 |
| `W0132` | LABEL(md) | `include/LO_GEN.labels.md:151` | 0o277632 | 0 |
| `W0133` | LABEL(md) | `include/LO_GEN.labels.md:152` | 0o277633 | 0 |
| `W0134` | LABEL(md) | `include/LO_GEN.labels.md:153` | 0o277634 | 0 |
| `W0135` | LABEL(md) | `include/LO_GEN.labels.md:154` | 0o277635 | 0 |
| `W0136` | LABEL(md) | `include/LO_GEN.labels.md:155` | 0o277636 | 0 |
| `W0137` | LABEL(md) | `include/LO_GEN.labels.md:156` | 0o277637 | 0 |
| `W0140` | LABEL(md) | `include/LO_GEN.labels.md:157` | 0o277640 | 0 |
| `W0141` | LABEL(md) | `include/LO_GEN.labels.md:158` | 0o277641 | 0 |
| `W0142` | LABEL(md) | `include/LO_GEN.labels.md:159` | 0o277642 | 0 |
| `W0143` | LABEL(md) | `include/LO_GEN.labels.md:160` | 0o277643 | 0 |
| `W0144` | LABEL(md) | `include/LO_GEN.labels.md:161` | 0o277644 | 0 |
| `W0145` | LABEL(md) | `include/LO_GEN.labels.md:162` | 0o277645 | 0 |
| `W0146` | LABEL(md) | `include/LO_GEN.labels.md:163` | 0o277646 | 0 |
| `W0147` | LABEL(md) | `include/LO_GEN.labels.md:164` | 0o277647 | 0 |
| `W0150` | LABEL(md) | `include/LO_GEN.labels.md:165` | 0o277650 | 0 |
| `W0151` | LABEL(md) | `include/LO_GEN.labels.md:166` | 0o277651 | 0 |
| `W0152` | LABEL(md) | `include/LO_GEN.labels.md:167` | 0o277652 | 0 |
| `W0153` | LABEL(md) | `include/LO_GEN.labels.md:168` | 0o277653 | 0 |
| `W0154` | LABEL(md) | `include/LO_GEN.labels.md:169` | 0o277654 | 0 |
| `W0155` | LABEL(md) | `include/LO_GEN.labels.md:170` | 0o277655 | 0 |
| `W0156` | LABEL(md) | `include/LO_GEN.labels.md:171` | 0o277656 | 0 |
| `W0157` | LABEL(md) | `include/LO_GEN.labels.md:172` | 0o277657 | 0 |
| `W0160` | LABEL(md) | `include/LO_GEN.labels.md:173` | 0o277660 | 0 |
| `W0161` | LABEL(md) | `include/LO_GEN.labels.md:174` | 0o277661 | 0 |
| `W0162` | LABEL(md) | `include/LO_GEN.labels.md:175` | 0o277662 | 0 |
| `W0163` | LABEL(md) | `include/LO_GEN.labels.md:176` | 0o277663 | 0 |
| `W0164` | LABEL(md) | `include/LO_GEN.labels.md:177` | 0o277664 | 0 |
| `W0165` | LABEL(md) | `include/LO_GEN.labels.md:178` | 0o277665 | 0 |
| `W0166` | LABEL(md) | `include/LO_GEN.labels.md:179` | 0o277666 | 0 |
| `W0167` | LABEL(md) | `include/LO_GEN.labels.md:180` | 0o277667 | 0 |
| `W0170` | LABEL(md) | `include/LO_GEN.labels.md:181` | 0o277670 | 0 |
| `W0171` | LABEL(md) | `include/LO_GEN.labels.md:182` | 0o277671 | 0 |
| `W0172` | LABEL(md) | `include/LO_GEN.labels.md:183` | 0o277672 | 0 |
| `W0173` | LABEL(md) | `include/LO_GEN.labels.md:184` | 0o277673 | 0 |
| `W0174` | LABEL(md) | `include/LO_GEN.labels.md:185` | 0o277674 | 0 |
| `W0175` | LABEL(md) | `include/LO_GEN.labels.md:186` | 0o277675 | 0 |
| `W0176` | LABEL(md) | `include/LO_GEN.labels.md:187` | 0o277676 | 0 |
| `W0177` | LABEL(md) | `include/LO_GEN.labels.md:188` | 0o277677 | 0 |
| `W0200` | LABEL(md) | `include/LO_GEN.labels.md:189` | 0o277700 | 0 |
| `W0201` | LABEL(md) | `include/LO_GEN.labels.md:190` | 0o277701 | 0 |
| `W0202` | LABEL(md) | `include/LO_GEN.labels.md:191` | 0o277702 | 0 |
| `W0203` | LABEL(md) | `include/LO_GEN.labels.md:192` | 0o277703 | 0 |
| `W0204` | LABEL(md) | `include/LO_GEN.labels.md:193` | 0o277704 | 0 |
| `W0205` | LABEL(md) | `include/LO_GEN.labels.md:194` | 0o277705 | 0 |
| `W0206` | LABEL(md) | `include/LO_GEN.labels.md:195` | 0o277706 | 0 |
| `W0207` | LABEL(md) | `include/LO_GEN.labels.md:196` | 0o277707 | 0 |
| `W0210` | LABEL(md) | `include/LO_GEN.labels.md:197` | 0o277710 | 0 |
| `W0211` | LABEL(md) | `include/LO_GEN.labels.md:198` | 0o277711 | 0 |
| `W0212` | LABEL(md) | `include/LO_GEN.labels.md:199` | 0o277712 | 0 |
| `W0213` | LABEL(md) | `include/LO_GEN.labels.md:200` | 0o277713 | 0 |
| `W0214` | LABEL(md) | `include/LO_GEN.labels.md:201` | 0o277714 | 0 |
| `W0215` | LABEL(md) | `include/LO_GEN.labels.md:202` | 0o277715 | 0 |
| `W0216` | LABEL(md) | `include/LO_GEN.labels.md:203` | 0o277716 | 0 |
| `W0217` | LABEL(md) | `include/LO_GEN.labels.md:204` | 0o277717 | 0 |
| `W0220` | LABEL(md) | `include/LO_GEN.labels.md:205` | 0o277720 | 0 |
| `W0221` | LABEL(md) | `include/LO_GEN.labels.md:206` | 0o277721 | 0 |
| `W0222` | LABEL(md) | `include/LO_GEN.labels.md:207` | 0o277722 | 0 |
| `W0223` | LABEL(md) | `include/LO_GEN.labels.md:208` | 0o277723 | 0 |
| `W0224` | LABEL(md) | `include/LO_GEN.labels.md:209` | 0o277724 | 0 |
| `W0225` | LABEL(md) | `include/LO_GEN.labels.md:210` | 0o277725 | 0 |
| `W0226` | LABEL(md) | `include/LO_GEN.labels.md:211` | 0o277726 | 0 |
| `W0227` | LABEL(md) | `include/LO_GEN.labels.md:212` | 0o277727 | 0 |
| `W0230` | LABEL(md) | `include/LO_GEN.labels.md:213` | 0o277730 | 0 |
| `W0231` | LABEL(md) | `include/LO_GEN.labels.md:214` | 0o277731 | 0 |
| `W0232` | LABEL(md) | `include/LO_GEN.labels.md:215` | 0o277732 | 0 |
| `W0233` | LABEL(md) | `include/LO_GEN.labels.md:216` | 0o277733 | 0 |
| `W0234` | LABEL(md) | `include/LO_GEN.labels.md:217` | 0o277734 | 0 |
| `W0235` | LABEL(md) | `include/LO_GEN.labels.md:218` | 0o277735 | 0 |
| `W0236` | LABEL(md) | `include/LO_GEN.labels.md:219` | 0o277736 | 0 |
| `W0237` | LABEL(md) | `include/LO_GEN.labels.md:220` | 0o277737 | 0 |
| `W0240` | LABEL(md) | `include/LO_GEN.labels.md:221` | 0o277740 | 0 |
| `W0241` | LABEL(md) | `include/LO_GEN.labels.md:222` | 0o277741 | 0 |
| `W0242` | LABEL(md) | `include/LO_GEN.labels.md:223` | 0o277742 | 0 |
| `W0243` | LABEL(md) | `include/LO_GEN.labels.md:224` | 0o277743 | 0 |
| `W0244` | LABEL(md) | `include/LO_GEN.labels.md:225` | 0o277744 | 0 |
| `W0245` | LABEL(md) | `include/LO_GEN.labels.md:226` | 0o277745 | 0 |
| `W0246` | LABEL(md) | `include/LO_GEN.labels.md:227` | 0o277746 | 0 |
| `W0247` | LABEL(md) | `include/LO_GEN.labels.md:228` | 0o277747 | 0 |
| `W0250` | LABEL(md) | `include/LO_GEN.labels.md:229` | 0o277750 | 0 |
| `W0251` | LABEL(md) | `include/LO_GEN.labels.md:230` | 0o277751 | 0 |
| `W0252` | LABEL(md) | `include/LO_GEN.labels.md:231` | 0o277752 | 0 |
| `W0253` | LABEL(md) | `include/LO_GEN.labels.md:232` | 0o277753 | 0 |
| `W0254` | LABEL(md) | `include/LO_GEN.labels.md:233` | 0o277754 | 0 |
| `W0255` | LABEL(md) | `include/LO_GEN.labels.md:234` | 0o277755 | 0 |
| `W0256` | LABEL(md) | `include/LO_GEN.labels.md:235` | 0o277756 | 0 |
| `W0257` | LABEL(md) | `include/LO_GEN.labels.md:236` | 0o277757 | 0 |
| `W0260` | LABEL(md) | `include/LO_GEN.labels.md:237` | 0o277760 | 0 |
| `W0261` | LABEL(md) | `include/LO_GEN.labels.md:238` | 0o277761 | 0 |
| `W0262` | LABEL(md) | `include/LO_GEN.labels.md:239` | 0o277762 | 0 |
| `W0263` | LABEL(md) | `include/LO_GEN.labels.md:240` | 0o277763 | 0 |
| `W0264` | LABEL(md) | `include/LO_GEN.labels.md:241` | 0o277764 | 0 |
| `W0265` | LABEL(md) | `include/LO_GEN.labels.md:242` | 0o277765 | 0 |
| `W0266` | LABEL(md) | `include/LO_GEN.labels.md:243` | 0o277766 | 0 |
| `W0267` | LABEL(md) | `include/LO_GEN.labels.md:244` | 0o277767 | 0 |
| `W0270` | LABEL(md) | `include/LO_GEN.labels.md:245` | 0o277770 | 0 |
| `W0271` | LABEL(md) | `include/LO_GEN.labels.md:246` | 0o277771 | 0 |
| `W0272` | LABEL(md) | `include/LO_GEN.labels.md:247` | 0o277772 | 0 |
| `W0273` | LABEL(md) | `include/LO_GEN.labels.md:248` | 0o277773 | 0 |
| `W0274` | LABEL(md) | `include/LO_GEN.labels.md:249` | 0o277774 | 0 |
| `W0275` | LABEL(md) | `include/LO_GEN.labels.md:250` | 0o277775 | 0 |
| `W0276` | LABEL(md) | `include/LO_GEN.labels.md:251` | 0o277776 | 0 |
| `W0277` | LABEL(md) | `include/LO_GEN.labels.md:252` | 0o277777 | 0 |
| `W0300` | LABEL(md) | `include/LO_GEN.labels.md:253` | 0o300000 | 0 |
| `W0301` | LABEL(md) | `include/LO_GEN.labels.md:254` | 0o300001 | 0 |
| `W0302` | LABEL(md) | `include/LO_GEN.labels.md:255` | 0o300002 | 0 |
| `W0303` | LABEL(md) | `include/LO_GEN.labels.md:256` | 0o300003 | 0 |
| `W0304` | LABEL(md) | `include/LO_GEN.labels.md:257` | 0o300004 | 0 |
| `W0305` | LABEL(md) | `include/LO_GEN.labels.md:258` | 0o300005 | 0 |
| `W0306` | LABEL(md) | `include/LO_GEN.labels.md:259` | 0o300006 | 0 |
| `W0307` | LABEL(md) | `include/LO_GEN.labels.md:260` | 0o300007 | 0 |
| `W0310` | LABEL(md) | `include/LO_GEN.labels.md:261` | 0o300010 | 0 |
| `W0311` | LABEL(md) | `include/LO_GEN.labels.md:262` | 0o300011 | 0 |
| `W0312` | LABEL(md) | `include/LO_GEN.labels.md:263` | 0o300012 | 0 |
| `W0313` | LABEL(md) | `include/LO_GEN.labels.md:264` | 0o300013 | 0 |
| `W0314` | LABEL(md) | `include/LO_GEN.labels.md:265` | 0o300014 | 0 |
| `W0315` | LABEL(md) | `include/LO_GEN.labels.md:266` | 0o300015 | 0 |
| `W0316` | LABEL(md) | `include/LO_GEN.labels.md:267` | 0o300016 | 0 |
| `W0317` | LABEL(md) | `include/LO_GEN.labels.md:268` | 0o300017 | 0 |
| `W0320` | LABEL(md) | `include/LO_GEN.labels.md:269` | 0o300020 | 0 |
| `W0321` | LABEL(md) | `include/LO_GEN.labels.md:270` | 0o300021 | 0 |
| `W0322` | LABEL(md) | `include/LO_GEN.labels.md:271` | 0o300022 | 0 |
| `W0323` | LABEL(md) | `include/LO_GEN.labels.md:272` | 0o300023 | 0 |
| `W0324` | LABEL(md) | `include/LO_GEN.labels.md:273` | 0o300024 | 0 |
| `W0325` | LABEL(md) | `include/LO_GEN.labels.md:274` | 0o300025 | 0 |
| `W0326` | LABEL(md) | `include/LO_GEN.labels.md:275` | 0o300026 | 0 |
| `W0327` | LABEL(md) | `include/LO_GEN.labels.md:276` | 0o300027 | 0 |
| `W0330` | LABEL(md) | `include/LO_GEN.labels.md:277` | 0o300030 | 0 |
| `W0331` | LABEL(md) | `include/LO_GEN.labels.md:278` | 0o300031 | 0 |
| `W0332` | LABEL(md) | `include/LO_GEN.labels.md:279` | 0o300032 | 0 |
| `W0333` | LABEL(md) | `include/LO_GEN.labels.md:280` | 0o300033 | 0 |
| `W0334` | LABEL(md) | `include/LO_GEN.labels.md:281` | 0o300034 | 0 |
| `W0335` | LABEL(md) | `include/LO_GEN.labels.md:282` | 0o300035 | 0 |
| `W0336` | LABEL(md) | `include/LO_GEN.labels.md:283` | 0o300036 | 0 |
| `W0337` | LABEL(md) | `include/LO_GEN.labels.md:284` | 0o300037 | 0 |
| `W0340` | LABEL(md) | `include/LO_GEN.labels.md:285` | 0o300040 | 0 |
| `W0341` | LABEL(md) | `include/LO_GEN.labels.md:286` | 0o300041 | 0 |
| `W0342` | LABEL(md) | `include/LO_GEN.labels.md:287` | 0o300042 | 0 |
| `W0343` | LABEL(md) | `include/LO_GEN.labels.md:288` | 0o300043 | 0 |
| `W0344` | LABEL(md) | `include/LO_GEN.labels.md:289` | 0o300044 | 0 |
| `W0345` | LABEL(md) | `include/LO_GEN.labels.md:290` | 0o300045 | 0 |
| `W0346` | LABEL(md) | `include/LO_GEN.labels.md:291` | 0o300046 | 0 |
| `W0347` | LABEL(md) | `include/LO_GEN.labels.md:292` | 0o300047 | 0 |
| `W0350` | LABEL(md) | `include/LO_GEN.labels.md:293` | 0o300050 | 0 |
| `W0351` | LABEL(md) | `include/LO_GEN.labels.md:294` | 0o300051 | 0 |
| `W0352` | LABEL(md) | `include/LO_GEN.labels.md:295` | 0o300052 | 0 |
| `W0353` | LABEL(md) | `include/LO_GEN.labels.md:296` | 0o300053 | 0 |
| `W0354` | LABEL(md) | `include/LO_GEN.labels.md:297` | 0o300054 | 0 |
| `W0355` | LABEL(md) | `include/LO_GEN.labels.md:298` | 0o300055 | 0 |
| `W0356` | LABEL(md) | `include/LO_GEN.labels.md:299` | 0o300056 | 0 |
| `W0357` | LABEL(md) | `include/LO_GEN.labels.md:300` | 0o300057 | 0 |
| `W0360` | LABEL(md) | `include/LO_GEN.labels.md:301` | 0o300060 | 0 |
| `W0361` | LABEL(md) | `include/LO_GEN.labels.md:302` | 0o300061 | 0 |
| `W0362` | LABEL(md) | `include/LO_GEN.labels.md:303` | 0o300062 | 0 |
| `W0363` | LABEL(md) | `include/LO_GEN.labels.md:304` | 0o300063 | 0 |
| `W0364` | LABEL(md) | `include/LO_GEN.labels.md:305` | 0o300064 | 0 |
| `W0365` | LABEL(md) | `include/LO_GEN.labels.md:306` | 0o300065 | 0 |
| `W0366` | LABEL(md) | `include/LO_GEN.labels.md:307` | 0o300066 | 0 |
| `W0367` | LABEL(md) | `include/LO_GEN.labels.md:308` | 0o300067 | 0 |
| `W0370` | LABEL(md) | `include/LO_GEN.labels.md:309` | 0o300070 | 0 |
| `W0371` | LABEL(md) | `include/LO_GEN.labels.md:310` | 0o300071 | 0 |
| `W0372` | LABEL(md) | `include/LO_GEN.labels.md:311` | 0o300072 | 0 |
| `W0373` | LABEL(md) | `include/LO_GEN.labels.md:312` | 0o300073 | 0 |
| `W0374` | LABEL(md) | `include/LO_GEN.labels.md:313` | 0o300074 | 0 |
| `W0375` | LABEL(md) | `include/LO_GEN.labels.md:314` | 0o300075 | 0 |
| `W0376` | LABEL(md) | `include/LO_GEN.labels.md:315` | 0o300076 | 0 |
| `W0377` | LABEL(md) | `include/LO_GEN.labels.md:316` | 0o300077 | 0 |
| `W0400` | LABEL(md) | `include/LO_GEN.labels.md:317` | 0o300100 | 0 |
| `W0401` | LABEL(md) | `include/LO_GEN.labels.md:318` | 0o300101 | 0 |
| `W0402` | LABEL(md) | `include/LO_GEN.labels.md:319` | 0o300102 | 0 |
| `W0403` | LABEL(md) | `include/LO_GEN.labels.md:320` | 0o300103 | 0 |
| `W0404` | LABEL(md) | `include/LO_GEN.labels.md:321` | 0o300104 | 0 |
| `W0405` | LABEL(md) | `include/LO_GEN.labels.md:322` | 0o300105 | 0 |
| `W0406` | LABEL(md) | `include/LO_GEN.labels.md:323` | 0o300106 | 0 |
| `W0407` | LABEL(md) | `include/LO_GEN.labels.md:324` | 0o300107 | 0 |
| `W0410` | LABEL(md) | `include/LO_GEN.labels.md:325` | 0o300110 | 0 |
| `W0411` | LABEL(md) | `include/LO_GEN.labels.md:326` | 0o300111 | 0 |
| `W0412` | LABEL(md) | `include/LO_GEN.labels.md:327` | 0o300112 | 0 |
| `W0413` | LABEL(md) | `include/LO_GEN.labels.md:328` | 0o300113 | 0 |
| `W0414` | LABEL(md) | `include/LO_GEN.labels.md:329` | 0o300114 | 0 |
| `W0415` | LABEL(md) | `include/LO_GEN.labels.md:330` | 0o300115 | 0 |
| `W0416` | LABEL(md) | `include/LO_GEN.labels.md:331` | 0o300116 | 0 |
| `W0417` | LABEL(md) | `include/LO_GEN.labels.md:332` | 0o300117 | 0 |
| `W0420` | LABEL(md) | `include/LO_GEN.labels.md:333` | 0o300120 | 0 |
| `W0421` | LABEL(md) | `include/LO_GEN.labels.md:334` | 0o300121 | 0 |
| `W0422` | LABEL(md) | `include/LO_GEN.labels.md:335` | 0o300122 | 0 |
| `W0423` | LABEL(md) | `include/LO_GEN.labels.md:336` | 0o300123 | 0 |
| `W0424` | LABEL(md) | `include/LO_GEN.labels.md:337` | 0o300124 | 0 |
| `W0425` | LABEL(md) | `include/LO_GEN.labels.md:338` | 0o300125 | 0 |
| `W0426` | LABEL(md) | `include/LO_GEN.labels.md:339` | 0o300126 | 0 |
| `W0427` | LABEL(md) | `include/LO_GEN.labels.md:340` | 0o300127 | 0 |
| `W0430` | LABEL(md) | `include/LO_GEN.labels.md:341` | 0o300130 | 0 |
| `W0431` | LABEL(md) | `include/LO_GEN.labels.md:342` | 0o300131 | 0 |
| `W0432` | LABEL(md) | `include/LO_GEN.labels.md:343` | 0o300132 | 0 |
| `W0433` | LABEL(md) | `include/LO_GEN.labels.md:344` | 0o300133 | 0 |
| `W0434` | LABEL(md) | `include/LO_GEN.labels.md:345` | 0o300134 | 0 |
| `W0435` | LABEL(md) | `include/LO_GEN.labels.md:346` | 0o300135 | 0 |
| `W0436` | LABEL(md) | `include/LO_GEN.labels.md:347` | 0o300136 | 0 |
| `W0437` | LABEL(md) | `include/LO_GEN.labels.md:348` | 0o300137 | 0 |
| `W0440` | LABEL(md) | `include/LO_GEN.labels.md:349` | 0o300140 | 0 |
| `W0441` | LABEL(md) | `include/LO_GEN.labels.md:350` | 0o300141 | 0 |
| `W0442` | LABEL(md) | `include/LO_GEN.labels.md:351` | 0o300142 | 0 |
| `W0443` | LABEL(md) | `include/LO_GEN.labels.md:352` | 0o300143 | 0 |
| `W0444` | LABEL(md) | `include/LO_GEN.labels.md:353` | 0o300144 | 0 |
| `W0445` | LABEL(md) | `include/LO_GEN.labels.md:354` | 0o300145 | 0 |
| `W0446` | LABEL(md) | `include/LO_GEN.labels.md:355` | 0o300146 | 0 |
| `W0447` | LABEL(md) | `include/LO_GEN.labels.md:356` | 0o300147 | 0 |
| `W0450` | LABEL(md) | `include/LO_GEN.labels.md:357` | 0o300150 | 0 |
| `W0451` | LABEL(md) | `include/LO_GEN.labels.md:358` | 0o300151 | 0 |
| `W0452` | LABEL(md) | `include/LO_GEN.labels.md:359` | 0o300152 | 0 |
| `W0453` | LABEL(md) | `include/LO_GEN.labels.md:360` | 0o300153 | 0 |
| `W0454` | LABEL(md) | `include/LO_GEN.labels.md:361` | 0o300154 | 0 |
| `W0455` | LABEL(md) | `include/LO_GEN.labels.md:362` | 0o300155 | 0 |
| `W0456` | LABEL(md) | `include/LO_GEN.labels.md:363` | 0o300156 | 0 |
| `W0457` | LABEL(md) | `include/LO_GEN.labels.md:364` | 0o300157 | 0 |
| `W0460` | LABEL(md) | `include/LO_GEN.labels.md:365` | 0o300160 | 0 |
| `W0461` | LABEL(md) | `include/LO_GEN.labels.md:366` | 0o300161 | 0 |
| `W0462` | LABEL(md) | `include/LO_GEN.labels.md:367` | 0o300162 | 0 |
| `W0463` | LABEL(md) | `include/LO_GEN.labels.md:368` | 0o300163 | 0 |
| `W0464` | LABEL(md) | `include/LO_GEN.labels.md:369` | 0o300164 | 0 |
| `W0465` | LABEL(md) | `include/LO_GEN.labels.md:370` | 0o300165 | 0 |
| `W0466` | LABEL(md) | `include/LO_GEN.labels.md:371` | 0o300166 | 0 |
| `W0467` | LABEL(md) | `include/LO_GEN.labels.md:372` | 0o300167 | 0 |
| `W0470` | LABEL(md) | `include/LO_GEN.labels.md:373` | 0o300170 | 0 |
| `W0471` | LABEL(md) | `include/LO_GEN.labels.md:374` | 0o300171 | 0 |
| `W0472` | LABEL(md) | `include/LO_GEN.labels.md:375` | 0o300172 | 0 |
| `W0473` | LABEL(md) | `include/LO_GEN.labels.md:376` | 0o300173 | 0 |
| `W0474` | LABEL(md) | `include/LO_GEN.labels.md:377` | 0o300174 | 0 |
| `W0475` | LABEL(md) | `include/LO_GEN.labels.md:378` | 0o300175 | 0 |
| `W0476` | LABEL(md) | `include/LO_GEN.labels.md:379` | 0o300176 | 0 |
| `W0477` | LABEL(md) | `include/LO_GEN.labels.md:380` | 0o300177 | 0 |
| `W0500` | LABEL(md) | `include/LO_GEN.labels.md:381` | 0o300200 | 0 |
| `W0501` | LABEL(md) | `include/LO_GEN.labels.md:382` | 0o300201 | 0 |
| `W0502` | LABEL(md) | `include/LO_GEN.labels.md:383` | 0o300202 | 0 |
| `W0503` | LABEL(md) | `include/LO_GEN.labels.md:384` | 0o300203 | 0 |
| `W0504` | LABEL(md) | `include/LO_GEN.labels.md:385` | 0o300204 | 0 |
| `W0505` | LABEL(md) | `include/LO_GEN.labels.md:386` | 0o300205 | 0 |
| `W0506` | LABEL(md) | `include/LO_GEN.labels.md:387` | 0o300206 | 0 |
| `W0507` | LABEL(md) | `include/LO_GEN.labels.md:388` | 0o300207 | 0 |
| `W0510` | LABEL(md) | `include/LO_GEN.labels.md:389` | 0o300210 | 0 |
| `W0511` | LABEL(md) | `include/LO_GEN.labels.md:390` | 0o300211 | 0 |
| `W0512` | LABEL(md) | `include/LO_GEN.labels.md:391` | 0o300212 | 0 |
| `W0513` | LABEL(md) | `include/LO_GEN.labels.md:392` | 0o300213 | 0 |
| `W0514` | LABEL(md) | `include/LO_GEN.labels.md:393` | 0o300214 | 0 |
| `W0515` | LABEL(md) | `include/LO_GEN.labels.md:394` | 0o300215 | 0 |
| `W0516` | LABEL(md) | `include/LO_GEN.labels.md:395` | 0o300216 | 0 |
| `W0517` | LABEL(md) | `include/LO_GEN.labels.md:396` | 0o300217 | 0 |
| `W0520` | LABEL(md) | `include/LO_GEN.labels.md:397` | 0o300220 | 0 |
| `W0521` | LABEL(md) | `include/LO_GEN.labels.md:398` | 0o300221 | 0 |
| `W0522` | LABEL(md) | `include/LO_GEN.labels.md:399` | 0o300222 | 0 |
| `W0523` | LABEL(md) | `include/LO_GEN.labels.md:400` | 0o300223 | 0 |
| `W0524` | LABEL(md) | `include/LO_GEN.labels.md:401` | 0o300224 | 0 |
| `W0525` | LABEL(md) | `include/LO_GEN.labels.md:402` | 0o300225 | 0 |
| `W0526` | LABEL(md) | `include/LO_GEN.labels.md:403` | 0o300226 | 0 |
| `W0527` | LABEL(md) | `include/LO_GEN.labels.md:404` | 0o300227 | 0 |
| `W0530` | LABEL(md) | `include/LO_GEN.labels.md:405` | 0o300230 | 0 |
| `W0531` | LABEL(md) | `include/LO_GEN.labels.md:406` | 0o300231 | 0 |
| `W0532` | LABEL(md) | `include/LO_GEN.labels.md:407` | 0o300232 | 0 |
| `W0533` | LABEL(md) | `include/LO_GEN.labels.md:408` | 0o300233 | 0 |
| `W0534` | LABEL(md) | `include/LO_GEN.labels.md:409` | 0o300234 | 0 |
| `W0535` | LABEL(md) | `include/LO_GEN.labels.md:410` | 0o300235 | 0 |
| `W0536` | LABEL(md) | `include/LO_GEN.labels.md:411` | 0o300236 | 0 |
| `W0537` | LABEL(md) | `include/LO_GEN.labels.md:412` | 0o300237 | 0 |
| `W0540` | LABEL(md) | `include/LO_GEN.labels.md:413` | 0o300240 | 0 |
| `W0541` | LABEL(md) | `include/LO_GEN.labels.md:414` | 0o300241 | 0 |
| `W0542` | LABEL(md) | `include/LO_GEN.labels.md:415` | 0o300242 | 0 |
| `W0543` | LABEL(md) | `include/LO_GEN.labels.md:416` | 0o300243 | 0 |
| `W0544` | LABEL(md) | `include/LO_GEN.labels.md:417` | 0o300244 | 0 |
| `W0545` | LABEL(md) | `include/LO_GEN.labels.md:418` | 0o300245 | 0 |
| `W0546` | LABEL(md) | `include/LO_GEN.labels.md:419` | 0o300246 | 0 |
| `W0547` | LABEL(md) | `include/LO_GEN.labels.md:420` | 0o300247 | 0 |
| `W0550` | LABEL(md) | `include/LO_GEN.labels.md:421` | 0o300250 | 0 |
| `W0551` | LABEL(md) | `include/LO_GEN.labels.md:422` | 0o300251 | 0 |
| `W0552` | LABEL(md) | `include/LO_GEN.labels.md:423` | 0o300252 | 0 |
| `W0553` | LABEL(md) | `include/LO_GEN.labels.md:424` | 0o300253 | 0 |
| `W0554` | LABEL(md) | `include/LO_GEN.labels.md:425` | 0o300254 | 0 |
| `W0555` | LABEL(md) | `include/LO_GEN.labels.md:426` | 0o300255 | 0 |
| `W0556` | LABEL(md) | `include/LO_GEN.labels.md:427` | 0o300256 | 0 |
| `W0557` | LABEL(md) | `include/LO_GEN.labels.md:428` | 0o300257 | 0 |
| `W0560` | LABEL(md) | `include/LO_GEN.labels.md:429` | 0o300260 | 0 |
| `W0561` | LABEL(md) | `include/LO_GEN.labels.md:430` | 0o300261 | 0 |
| `W0562` | LABEL(md) | `include/LO_GEN.labels.md:431` | 0o300262 | 0 |
| `W0563` | LABEL(md) | `include/LO_GEN.labels.md:432` | 0o300263 | 0 |
| `W0564` | LABEL(md) | `include/LO_GEN.labels.md:433` | 0o300264 | 0 |
| `W0565` | LABEL(md) | `include/LO_GEN.labels.md:434` | 0o300265 | 0 |
| `W0566` | LABEL(md) | `include/LO_GEN.labels.md:435` | 0o300266 | 0 |
| `W0567` | LABEL(md) | `include/LO_GEN.labels.md:436` | 0o300267 | 0 |
| `W0570` | LABEL(md) | `include/LO_GEN.labels.md:437` | 0o300270 | 0 |
| `W0571` | LABEL(md) | `include/LO_GEN.labels.md:438` | 0o300271 | 0 |
| `W0572` | LABEL(md) | `include/LO_GEN.labels.md:439` | 0o300272 | 0 |
| `W0573` | LABEL(md) | `include/LO_GEN.labels.md:440` | 0o300273 | 0 |
| `W0574` | LABEL(md) | `include/LO_GEN.labels.md:441` | 0o300274 | 0 |
| `W0575` | LABEL(md) | `include/LO_GEN.labels.md:442` | 0o300275 | 0 |
| `W0576` | LABEL(md) | `include/LO_GEN.labels.md:443` | 0o300276 | 0 |
| `W0577` | LABEL(md) | `include/LO_GEN.labels.md:444` | 0o300277 | 0 |
| `W0600` | LABEL(md) | `include/LO_GEN.labels.md:445` | 0o300300 | 0 |
| `W0601` | LABEL(md) | `include/LO_GEN.labels.md:446` | 0o300301 | 0 |
| `W0602` | LABEL(md) | `include/LO_GEN.labels.md:447` | 0o300302 | 0 |
| `W0603` | LABEL(md) | `include/LO_GEN.labels.md:448` | 0o300303 | 0 |
| `W0604` | LABEL(md) | `include/LO_GEN.labels.md:449` | 0o300304 | 0 |
| `W0605` | LABEL(md) | `include/LO_GEN.labels.md:450` | 0o300305 | 0 |
| `W0606` | LABEL(md) | `include/LO_GEN.labels.md:451` | 0o300306 | 0 |
| `W0607` | LABEL(md) | `include/LO_GEN.labels.md:452` | 0o300307 | 0 |
| `W0610` | LABEL(md) | `include/LO_GEN.labels.md:453` | 0o300310 | 0 |
| `W0611` | LABEL(md) | `include/LO_GEN.labels.md:454` | 0o300311 | 0 |
| `W0612` | LABEL(md) | `include/LO_GEN.labels.md:455` | 0o300312 | 0 |
| `W0613` | LABEL(md) | `include/LO_GEN.labels.md:456` | 0o300313 | 0 |
| `W0614` | LABEL(md) | `include/LO_GEN.labels.md:457` | 0o300314 | 0 |
| `W0615` | LABEL(md) | `include/LO_GEN.labels.md:458` | 0o300315 | 0 |
| `W0616` | LABEL(md) | `include/LO_GEN.labels.md:459` | 0o300316 | 0 |
| `W0617` | LABEL(md) | `include/LO_GEN.labels.md:460` | 0o300317 | 0 |
| `W0620` | LABEL(md) | `include/LO_GEN.labels.md:461` | 0o300320 | 0 |
| `W0621` | LABEL(md) | `include/LO_GEN.labels.md:462` | 0o300321 | 0 |
| `W0622` | LABEL(md) | `include/LO_GEN.labels.md:463` | 0o300322 | 0 |
| `W0623` | LABEL(md) | `include/LO_GEN.labels.md:464` | 0o300323 | 0 |
| `W0624` | LABEL(md) | `include/LO_GEN.labels.md:465` | 0o300324 | 0 |
| `W0625` | LABEL(md) | `include/LO_GEN.labels.md:466` | 0o300325 | 0 |
| `W0626` | LABEL(md) | `include/LO_GEN.labels.md:467` | 0o300326 | 0 |
| `W0627` | LABEL(md) | `include/LO_GEN.labels.md:468` | 0o300327 | 0 |
| `W0630` | LABEL(md) | `include/LO_GEN.labels.md:469` | 0o300330 | 0 |
| `W0631` | LABEL(md) | `include/LO_GEN.labels.md:470` | 0o300331 | 0 |
| `W0632` | LABEL(md) | `include/LO_GEN.labels.md:471` | 0o300332 | 0 |
| `W0633` | LABEL(md) | `include/LO_GEN.labels.md:472` | 0o300333 | 0 |
| `W0634` | LABEL(md) | `include/LO_GEN.labels.md:473` | 0o300334 | 0 |
| `W0635` | LABEL(md) | `include/LO_GEN.labels.md:474` | 0o300335 | 0 |
| `W0636` | LABEL(md) | `include/LO_GEN.labels.md:475` | 0o300336 | 0 |
| `W0637` | LABEL(md) | `include/LO_GEN.labels.md:476` | 0o300337 | 0 |
| `W0640` | LABEL(md) | `include/LO_GEN.labels.md:477` | 0o300340 | 0 |
| `W0641` | LABEL(md) | `include/LO_GEN.labels.md:478` | 0o300341 | 0 |
| `W0642` | LABEL(md) | `include/LO_GEN.labels.md:479` | 0o300342 | 0 |
| `W0643` | LABEL(md) | `include/LO_GEN.labels.md:480` | 0o300343 | 0 |
| `W0644` | LABEL(md) | `include/LO_GEN.labels.md:481` | 0o300344 | 0 |
| `W0645` | LABEL(md) | `include/LO_GEN.labels.md:482` | 0o300345 | 0 |
| `W0646` | LABEL(md) | `include/LO_GEN.labels.md:483` | 0o300346 | 0 |
| `W0647` | LABEL(md) | `include/LO_GEN.labels.md:484` | 0o300347 | 0 |
| `W0650` | LABEL(md) | `include/LO_GEN.labels.md:485` | 0o300350 | 0 |
| `W0651` | LABEL(md) | `include/LO_GEN.labels.md:486` | 0o300351 | 0 |
| `W0652` | LABEL(md) | `include/LO_GEN.labels.md:487` | 0o300352 | 0 |
| `W0653` | LABEL(md) | `include/LO_GEN.labels.md:488` | 0o300353 | 0 |
| `W0654` | LABEL(md) | `include/LO_GEN.labels.md:489` | 0o300354 | 0 |
| `W0655` | LABEL(md) | `include/LO_GEN.labels.md:490` | 0o300355 | 0 |
| `W0656` | LABEL(md) | `include/LO_GEN.labels.md:491` | 0o300356 | 0 |
| `W0657` | LABEL(md) | `include/LO_GEN.labels.md:492` | 0o300357 | 0 |
| `W0660` | LABEL(md) | `include/LO_GEN.labels.md:493` | 0o300360 | 0 |
| `W0661` | LABEL(md) | `include/LO_GEN.labels.md:494` | 0o300361 | 0 |
| `W0662` | LABEL(md) | `include/LO_GEN.labels.md:495` | 0o300362 | 0 |
| `W0663` | LABEL(md) | `include/LO_GEN.labels.md:496` | 0o300363 | 0 |
| `W0664` | LABEL(md) | `include/LO_GEN.labels.md:497` | 0o300364 | 0 |
| `W0665` | LABEL(md) | `include/LO_GEN.labels.md:498` | 0o300365 | 0 |
| `W0666` | LABEL(md) | `include/LO_GEN.labels.md:499` | 0o300366 | 0 |
| `W0667` | LABEL(md) | `include/LO_GEN.labels.md:500` | 0o300367 | 0 |
| `W0670` | LABEL(md) | `include/LO_GEN.labels.md:501` | 0o300370 | 0 |
| `W0671` | LABEL(md) | `include/LO_GEN.labels.md:502` | 0o300371 | 0 |
| `W0672` | LABEL(md) | `include/LO_GEN.labels.md:503` | 0o300372 | 0 |
| `W0673` | LABEL(md) | `include/LO_GEN.labels.md:504` | 0o300373 | 0 |
| `W0674` | LABEL(md) | `include/LO_GEN.labels.md:505` | 0o300374 | 0 |
| `W0675` | LABEL(md) | `include/LO_GEN.labels.md:506` | 0o300375 | 0 |
| `W0676` | LABEL(md) | `include/LO_GEN.labels.md:507` | 0o300376 | 0 |
| `W0677` | LABEL(md) | `include/LO_GEN.labels.md:508` | 0o300377 | 0 |
| `W0700` | LABEL(md) | `include/LO_GEN.labels.md:509` | 0o300400 | 0 |
| `W0701` | LABEL(md) | `include/LO_GEN.labels.md:510` | 0o300401 | 0 |
| `W0702` | LABEL(md) | `include/LO_GEN.labels.md:511` | 0o300402 | 0 |
| `W0703` | LABEL(md) | `include/LO_GEN.labels.md:512` | 0o300403 | 0 |
| `W0704` | LABEL(md) | `include/LO_GEN.labels.md:513` | 0o300404 | 0 |
| `W0705` | LABEL(md) | `include/LO_GEN.labels.md:514` | 0o300405 | 0 |
| `W0706` | LABEL(md) | `include/LO_GEN.labels.md:515` | 0o300406 | 0 |
| `W0707` | LABEL(md) | `include/LO_GEN.labels.md:516` | 0o300407 | 0 |
| `W0710` | LABEL(md) | `include/LO_GEN.labels.md:517` | 0o300410 | 0 |
| `W0711` | LABEL(md) | `include/LO_GEN.labels.md:518` | 0o300411 | 0 |
| `W0712` | LABEL(md) | `include/LO_GEN.labels.md:519` | 0o300412 | 0 |
| `W0713` | LABEL(md) | `include/LO_GEN.labels.md:520` | 0o300413 | 0 |
| `W0714` | LABEL(md) | `include/LO_GEN.labels.md:521` | 0o300414 | 0 |
| `W0715` | LABEL(md) | `include/LO_GEN.labels.md:522` | 0o300415 | 0 |
| `W0716` | LABEL(md) | `include/LO_GEN.labels.md:523` | 0o300416 | 0 |
| `W0717` | LABEL(md) | `include/LO_GEN.labels.md:524` | 0o300417 | 0 |
| `W0720` | LABEL(md) | `include/LO_GEN.labels.md:525` | 0o300420 | 0 |
| `W0721` | LABEL(md) | `include/LO_GEN.labels.md:526` | 0o300421 | 0 |
| `W0722` | LABEL(md) | `include/LO_GEN.labels.md:527` | 0o300422 | 0 |
| `W0723` | LABEL(md) | `include/LO_GEN.labels.md:528` | 0o300423 | 0 |
| `W0724` | LABEL(md) | `include/LO_GEN.labels.md:529` | 0o300424 | 0 |
| `W0725` | LABEL(md) | `include/LO_GEN.labels.md:530` | 0o300425 | 0 |
| `W0726` | LABEL(md) | `include/LO_GEN.labels.md:531` | 0o300426 | 0 |
| `W0727` | LABEL(md) | `include/LO_GEN.labels.md:532` | 0o300427 | 0 |
| `W0730` | LABEL(md) | `include/LO_GEN.labels.md:533` | 0o300430 | 0 |
| `W0731` | LABEL(md) | `include/LO_GEN.labels.md:534` | 0o300431 | 0 |
| `W0732` | LABEL(md) | `include/LO_GEN.labels.md:535` | 0o300432 | 0 |
| `W0733` | LABEL(md) | `include/LO_GEN.labels.md:536` | 0o300433 | 0 |
| `W0734` | LABEL(md) | `include/LO_GEN.labels.md:537` | 0o300434 | 0 |
| `W0735` | LABEL(md) | `include/LO_GEN.labels.md:538` | 0o300435 | 0 |
| `W0736` | LABEL(md) | `include/LO_GEN.labels.md:539` | 0o300436 | 0 |
| `W0737` | LABEL(md) | `include/LO_GEN.labels.md:540` | 0o300437 | 0 |
| `W0740` | LABEL(md) | `include/LO_GEN.labels.md:541` | 0o300440 | 0 |
| `W0741` | LABEL(md) | `include/LO_GEN.labels.md:542` | 0o300441 | 0 |
| `W0742` | LABEL(md) | `include/LO_GEN.labels.md:543` | 0o300442 | 0 |
| `W0743` | LABEL(md) | `include/LO_GEN.labels.md:544` | 0o300443 | 0 |
| `W0744` | LABEL(md) | `include/LO_GEN.labels.md:545` | 0o300444 | 0 |
| `W0745` | LABEL(md) | `include/LO_GEN.labels.md:546` | 0o300445 | 0 |
| `W0746` | LABEL(md) | `include/LO_GEN.labels.md:547` | 0o300446 | 0 |
| `W0747` | LABEL(md) | `include/LO_GEN.labels.md:548` | 0o300447 | 0 |
| `W0750` | LABEL(md) | `include/LO_GEN.labels.md:549` | 0o300450 | 0 |
| `W0751` | LABEL(md) | `include/LO_GEN.labels.md:550` | 0o300451 | 0 |
| `W0752` | LABEL(md) | `include/LO_GEN.labels.md:551` | 0o300452 | 0 |
| `W0753` | LABEL(md) | `include/LO_GEN.labels.md:552` | 0o300453 | 0 |
| `W0754` | LABEL(md) | `include/LO_GEN.labels.md:553` | 0o300454 | 0 |
| `W0755` | LABEL(md) | `include/LO_GEN.labels.md:554` | 0o300455 | 0 |
| `W0756` | LABEL(md) | `include/LO_GEN.labels.md:555` | 0o300456 | 0 |
| `W0757` | LABEL(md) | `include/LO_GEN.labels.md:556` | 0o300457 | 0 |
| `W0760` | LABEL(md) | `include/LO_GEN.labels.md:557` | 0o300460 | 0 |
| `W0761` | LABEL(md) | `include/LO_GEN.labels.md:558` | 0o300461 | 0 |
| `W0762` | LABEL(md) | `include/LO_GEN.labels.md:559` | 0o300462 | 0 |
| `W0763` | LABEL(md) | `include/LO_GEN.labels.md:560` | 0o300463 | 0 |
| `W0764` | LABEL(md) | `include/LO_GEN.labels.md:561` | 0o300464 | 0 |
| `W0765` | LABEL(md) | `include/LO_GEN.labels.md:562` | 0o300465 | 0 |
| `W0766` | LABEL(md) | `include/LO_GEN.labels.md:563` | 0o300466 | 0 |
| `W0767` | LABEL(md) | `include/LO_GEN.labels.md:564` | 0o300467 | 0 |
| `W0770` | LABEL(md) | `include/LO_GEN.labels.md:565` | 0o300470 | 0 |
| `W0771` | LABEL(md) | `include/LO_GEN.labels.md:566` | 0o300471 | 0 |
| `W0772` | LABEL(md) | `include/LO_GEN.labels.md:567` | 0o300472 | 0 |
| `W0773` | LABEL(md) | `include/LO_GEN.labels.md:568` | 0o300473 | 0 |
| `W0774` | LABEL(md) | `include/LO_GEN.labels.md:569` | 0o300474 | 0 |
| `W0775` | LABEL(md) | `include/LO_GEN.labels.md:570` | 0o300475 | 0 |
| `W0776` | LABEL(md) | `include/LO_GEN.labels.md:571` | 0o300476 | 0 |
| `W0777` | LABEL(md) | `include/LO_GEN.labels.md:572` | 0o300477 | 0 |
| `W1000` | LABEL(md) | `include/LO_GEN.labels.md:573` | 0o300500 | 0 |
| `W1001` | LABEL(md) | `include/LO_GEN.labels.md:574` | 0o300501 | 0 |
| `W1002` | LABEL(md) | `include/LO_GEN.labels.md:575` | 0o300502 | 0 |
| `W1003` | LABEL(md) | `include/LO_GEN.labels.md:576` | 0o300503 | 0 |
| `W1004` | LABEL(md) | `include/LO_GEN.labels.md:577` | 0o300504 | 0 |
| `W1005` | LABEL(md) | `include/LO_GEN.labels.md:578` | 0o300505 | 0 |
| `W1006` | LABEL(md) | `include/LO_GEN.labels.md:579` | 0o300506 | 0 |
| `W1007` | LABEL(md) | `include/LO_GEN.labels.md:580` | 0o300507 | 0 |
| `W1010` | LABEL(md) | `include/LO_GEN.labels.md:581` | 0o300510 | 0 |
| `W1011` | LABEL(md) | `include/LO_GEN.labels.md:582` | 0o300511 | 0 |
| `W1012` | LABEL(md) | `include/LO_GEN.labels.md:583` | 0o300512 | 0 |
| `W1013` | LABEL(md) | `include/LO_GEN.labels.md:584` | 0o300513 | 0 |
| `W1014` | LABEL(md) | `include/LO_GEN.labels.md:585` | 0o300514 | 0 |
| `W1015` | LABEL(md) | `include/LO_GEN.labels.md:586` | 0o300515 | 0 |
| `W1016` | LABEL(md) | `include/LO_GEN.labels.md:587` | 0o300516 | 0 |
| `W1017` | LABEL(md) | `include/LO_GEN.labels.md:588` | 0o300517 | 0 |
| `W1020` | LABEL(md) | `include/LO_GEN.labels.md:589` | 0o300520 | 0 |
| `W1021` | LABEL(md) | `include/LO_GEN.labels.md:590` | 0o300521 | 0 |
| `W1022` | LABEL(md) | `include/LO_GEN.labels.md:591` | 0o300522 | 0 |
| `W1023` | LABEL(md) | `include/LO_GEN.labels.md:592` | 0o300523 | 0 |
| `W1024` | LABEL(md) | `include/LO_GEN.labels.md:593` | 0o300524 | 0 |
| `W1025` | LABEL(md) | `include/LO_GEN.labels.md:594` | 0o300525 | 0 |
| `W1026` | LABEL(md) | `include/LO_GEN.labels.md:595` | 0o300526 | 0 |
| `W1027` | LABEL(md) | `include/LO_GEN.labels.md:596` | 0o300527 | 0 |
| `W1030` | LABEL(md) | `include/LO_GEN.labels.md:597` | 0o300530 | 0 |
| `W1031` | LABEL(md) | `include/LO_GEN.labels.md:598` | 0o300531 | 0 |
| `W1032` | LABEL(md) | `include/LO_GEN.labels.md:599` | 0o300532 | 0 |
| `W1033` | LABEL(md) | `include/LO_GEN.labels.md:600` | 0o300533 | 0 |
| `W1034` | LABEL(md) | `include/LO_GEN.labels.md:601` | 0o300534 | 0 |
| `W1035` | LABEL(md) | `include/LO_GEN.labels.md:602` | 0o300535 | 0 |
| `W1036` | LABEL(md) | `include/LO_GEN.labels.md:603` | 0o300536 | 0 |
| `W1037` | LABEL(md) | `include/LO_GEN.labels.md:604` | 0o300537 | 0 |
| `W1040` | LABEL(md) | `include/LO_GEN.labels.md:605` | 0o300540 | 0 |
| `W1041` | LABEL(md) | `include/LO_GEN.labels.md:606` | 0o300541 | 0 |
| `W1042` | LABEL(md) | `include/LO_GEN.labels.md:607` | 0o300542 | 0 |
| `W1043` | LABEL(md) | `include/LO_GEN.labels.md:608` | 0o300543 | 0 |
| `W1044` | LABEL(md) | `include/LO_GEN.labels.md:609` | 0o300544 | 0 |
| `W1045` | LABEL(md) | `include/LO_GEN.labels.md:610` | 0o300545 | 0 |
| `W1046` | LABEL(md) | `include/LO_GEN.labels.md:611` | 0o300546 | 0 |
| `W1047` | LABEL(md) | `include/LO_GEN.labels.md:612` | 0o300547 | 0 |
| `W1050` | LABEL(md) | `include/LO_GEN.labels.md:613` | 0o300550 | 0 |
| `W1051` | LABEL(md) | `include/LO_GEN.labels.md:614` | 0o300551 | 0 |
| `W1052` | LABEL(md) | `include/LO_GEN.labels.md:615` | 0o300552 | 0 |
| `W1053` | LABEL(md) | `include/LO_GEN.labels.md:616` | 0o300553 | 0 |
| `W1054` | LABEL(md) | `include/LO_GEN.labels.md:617` | 0o300554 | 0 |
| `W1055` | LABEL(md) | `include/LO_GEN.labels.md:618` | 0o300555 | 0 |
| `W1056` | LABEL(md) | `include/LO_GEN.labels.md:619` | 0o300556 | 0 |
| `W1057` | LABEL(md) | `include/LO_GEN.labels.md:620` | 0o300557 | 0 |
| `W1060` | LABEL(md) | `include/LO_GEN.labels.md:621` | 0o300560 | 0 |
| `W1061` | LABEL(md) | `include/LO_GEN.labels.md:622` | 0o300561 | 0 |
| `W1062` | LABEL(md) | `include/LO_GEN.labels.md:623` | 0o300562 | 0 |
| `W1063` | LABEL(md) | `include/LO_GEN.labels.md:624` | 0o300563 | 0 |
| `W1064` | LABEL(md) | `include/LO_GEN.labels.md:625` | 0o300564 | 0 |
| `W1065` | LABEL(md) | `include/LO_GEN.labels.md:626` | 0o300565 | 0 |
| `W1066` | LABEL(md) | `include/LO_GEN.labels.md:627` | 0o300566 | 0 |
| `W1067` | LABEL(md) | `include/LO_GEN.labels.md:628` | 0o300567 | 0 |
| `W1070` | LABEL(md) | `include/LO_GEN.labels.md:629` | 0o300570 | 0 |
| `W1071` | LABEL(md) | `include/LO_GEN.labels.md:630` | 0o300571 | 0 |
| `W1072` | LABEL(md) | `include/LO_GEN.labels.md:631` | 0o300572 | 0 |
| `W1073` | LABEL(md) | `include/LO_GEN.labels.md:632` | 0o300573 | 0 |
| `W1074` | LABEL(md) | `include/LO_GEN.labels.md:633` | 0o300574 | 0 |
| `W1075` | LABEL(md) | `include/LO_GEN.labels.md:634` | 0o300575 | 0 |
| `W1076` | LABEL(md) | `include/LO_GEN.labels.md:635` | 0o300576 | 0 |
| `W1077` | LABEL(md) | `include/LO_GEN.labels.md:636` | 0o300577 | 0 |
| `W1100` | LABEL(md) | `include/LO_GEN.labels.md:637` | 0o300600 | 0 |
| `W1101` | LABEL(md) | `include/LO_GEN.labels.md:638` | 0o300601 | 0 |
| `W1102` | LABEL(md) | `include/LO_GEN.labels.md:639` | 0o300602 | 0 |
| `W1103` | LABEL(md) | `include/LO_GEN.labels.md:640` | 0o300603 | 0 |
| `W1104` | LABEL(md) | `include/LO_GEN.labels.md:641` | 0o300604 | 0 |
| `W1105` | LABEL(md) | `include/LO_GEN.labels.md:642` | 0o300605 | 0 |
| `W1106` | LABEL(md) | `include/LO_GEN.labels.md:643` | 0o300606 | 0 |
| `W1107` | LABEL(md) | `include/LO_GEN.labels.md:644` | 0o300607 | 0 |
| `W1110` | LABEL(md) | `include/LO_GEN.labels.md:645` | 0o300610 | 0 |
| `W1111` | LABEL(md) | `include/LO_GEN.labels.md:646` | 0o300611 | 0 |
| `W1112` | LABEL(md) | `include/LO_GEN.labels.md:647` | 0o300612 | 0 |
| `W1113` | LABEL(md) | `include/LO_GEN.labels.md:648` | 0o300613 | 0 |
| `W1114` | LABEL(md) | `include/LO_GEN.labels.md:649` | 0o300614 | 0 |
| `W1115` | LABEL(md) | `include/LO_GEN.labels.md:650` | 0o300615 | 0 |
| `W1116` | LABEL(md) | `include/LO_GEN.labels.md:651` | 0o300616 | 0 |
| `W1117` | LABEL(md) | `include/LO_GEN.labels.md:652` | 0o300617 | 0 |
| `W1120` | LABEL(md) | `include/LO_GEN.labels.md:653` | 0o300620 | 0 |
| `W1121` | LABEL(md) | `include/LO_GEN.labels.md:654` | 0o300621 | 0 |
| `W1122` | LABEL(md) | `include/LO_GEN.labels.md:655` | 0o300622 | 0 |
| `W1123` | LABEL(md) | `include/LO_GEN.labels.md:656` | 0o300623 | 0 |
| `W1124` | LABEL(md) | `include/LO_GEN.labels.md:657` | 0o300624 | 0 |
| `W1125` | LABEL(md) | `include/LO_GEN.labels.md:658` | 0o300625 | 0 |
| `W1126` | LABEL(md) | `include/LO_GEN.labels.md:659` | 0o300626 | 0 |
| `W1127` | LABEL(md) | `include/LO_GEN.labels.md:660` | 0o300627 | 0 |
| `W1130` | LABEL(md) | `include/LO_GEN.labels.md:661` | 0o300630 | 0 |
| `W1131` | LABEL(md) | `include/LO_GEN.labels.md:662` | 0o300631 | 0 |
| `W1132` | LABEL(md) | `include/LO_GEN.labels.md:663` | 0o300632 | 0 |
| `W1133` | LABEL(md) | `include/LO_GEN.labels.md:664` | 0o300633 | 0 |
| `W1134` | LABEL(md) | `include/LO_GEN.labels.md:665` | 0o300634 | 0 |
| `W1135` | LABEL(md) | `include/LO_GEN.labels.md:666` | 0o300635 | 0 |
| `W1136` | LABEL(md) | `include/LO_GEN.labels.md:667` | 0o300636 | 0 |
| `W1137` | LABEL(md) | `include/LO_GEN.labels.md:668` | 0o300637 | 0 |
| `W1140` | LABEL(md) | `include/LO_GEN.labels.md:669` | 0o300640 | 0 |
| `W1141` | LABEL(md) | `include/LO_GEN.labels.md:670` | 0o300641 | 0 |
| `W1142` | LABEL(md) | `include/LO_GEN.labels.md:671` | 0o300642 | 0 |
| `W1143` | LABEL(md) | `include/LO_GEN.labels.md:672` | 0o300643 | 0 |
| `W1144` | LABEL(md) | `include/LO_GEN.labels.md:673` | 0o300644 | 0 |
| `W1145` | LABEL(md) | `include/LO_GEN.labels.md:674` | 0o300645 | 0 |
| `W1146` | LABEL(md) | `include/LO_GEN.labels.md:675` | 0o300646 | 0 |
| `W1147` | LABEL(md) | `include/LO_GEN.labels.md:676` | 0o300647 | 0 |
| `W1150` | LABEL(md) | `include/LO_GEN.labels.md:677` | 0o300650 | 0 |
| `W1151` | LABEL(md) | `include/LO_GEN.labels.md:678` | 0o300651 | 0 |
| `W1152` | LABEL(md) | `include/LO_GEN.labels.md:679` | 0o300652 | 0 |
| `W1153` | LABEL(md) | `include/LO_GEN.labels.md:680` | 0o300653 | 0 |
| `W1154` | LABEL(md) | `include/LO_GEN.labels.md:681` | 0o300654 | 0 |
| `W1155` | LABEL(md) | `include/LO_GEN.labels.md:682` | 0o300655 | 0 |
| `W1156` | LABEL(md) | `include/LO_GEN.labels.md:683` | 0o300656 | 0 |
| `W1157` | LABEL(md) | `include/LO_GEN.labels.md:684` | 0o300657 | 0 |
| `W1160` | LABEL(md) | `include/LO_GEN.labels.md:685` | 0o300660 | 0 |
| `W1161` | LABEL(md) | `include/LO_GEN.labels.md:686` | 0o300661 | 0 |
| `W1162` | LABEL(md) | `include/LO_GEN.labels.md:687` | 0o300662 | 0 |
| `W1163` | LABEL(md) | `include/LO_GEN.labels.md:688` | 0o300663 | 0 |
| `W1164` | LABEL(md) | `include/LO_GEN.labels.md:689` | 0o300664 | 0 |
| `W1165` | LABEL(md) | `include/LO_GEN.labels.md:690` | 0o300665 | 0 |
| `W1166` | LABEL(md) | `include/LO_GEN.labels.md:691` | 0o300666 | 0 |
| `W1167` | LABEL(md) | `include/LO_GEN.labels.md:692` | 0o300667 | 0 |
| `W1170` | LABEL(md) | `include/LO_GEN.labels.md:693` | 0o300670 | 0 |
| `W1171` | LABEL(md) | `include/LO_GEN.labels.md:694` | 0o300671 | 0 |
| `W1172` | LABEL(md) | `include/LO_GEN.labels.md:695` | 0o300672 | 0 |
| `W1173` | LABEL(md) | `include/LO_GEN.labels.md:696` | 0o300673 | 0 |
| `W1174` | LABEL(md) | `include/LO_GEN.labels.md:697` | 0o300674 | 0 |
| `W1175` | LABEL(md) | `include/LO_GEN.labels.md:698` | 0o300675 | 0 |
| `W1176` | LABEL(md) | `include/LO_GEN.labels.md:699` | 0o300676 | 0 |
| `W1177` | LABEL(md) | `include/LO_GEN.labels.md:700` | 0o300677 | 0 |
| `W1200` | LABEL(md) | `include/LO_GEN.labels.md:701` | 0o300700 | 0 |
| `W1201` | LABEL(md) | `include/LO_GEN.labels.md:702` | 0o300701 | 0 |
| `W1202` | LABEL(md) | `include/LO_GEN.labels.md:703` | 0o300702 | 0 |
| `W1203` | LABEL(md) | `include/LO_GEN.labels.md:704` | 0o300703 | 0 |
| `W1204` | LABEL(md) | `include/LO_GEN.labels.md:705` | 0o300704 | 0 |
| `W1205` | LABEL(md) | `include/LO_GEN.labels.md:706` | 0o300705 | 0 |
| `W1206` | LABEL(md) | `include/LO_GEN.labels.md:707` | 0o300706 | 0 |
| `W1207` | LABEL(md) | `include/LO_GEN.labels.md:708` | 0o300707 | 0 |
| `W1210` | LABEL(md) | `include/LO_GEN.labels.md:709` | 0o300710 | 0 |
| `W1211` | LABEL(md) | `include/LO_GEN.labels.md:710` | 0o300711 | 0 |
| `W1212` | LABEL(md) | `include/LO_GEN.labels.md:711` | 0o300712 | 0 |
| `W1213` | LABEL(md) | `include/LO_GEN.labels.md:712` | 0o300713 | 0 |
| `W1214` | LABEL(md) | `include/LO_GEN.labels.md:713` | 0o300714 | 0 |
| `W1215` | LABEL(md) | `include/LO_GEN.labels.md:714` | 0o300715 | 0 |
| `W1216` | LABEL(md) | `include/LO_GEN.labels.md:715` | 0o300716 | 0 |
| `W1217` | LABEL(md) | `include/LO_GEN.labels.md:716` | 0o300717 | 0 |
| `W1220` | LABEL(md) | `include/LO_GEN.labels.md:717` | 0o300720 | 0 |
| `W1221` | LABEL(md) | `include/LO_GEN.labels.md:718` | 0o300721 | 0 |
| `W1222` | LABEL(md) | `include/LO_GEN.labels.md:719` | 0o300722 | 0 |
| `W1223` | LABEL(md) | `include/LO_GEN.labels.md:720` | 0o300723 | 0 |
| `W1224` | LABEL(md) | `include/LO_GEN.labels.md:721` | 0o300724 | 0 |
| `W1225` | LABEL(md) | `include/LO_GEN.labels.md:722` | 0o300725 | 0 |
| `W1226` | LABEL(md) | `include/LO_GEN.labels.md:723` | 0o300726 | 0 |
| `W1227` | LABEL(md) | `include/LO_GEN.labels.md:724` | 0o300727 | 0 |
| `W1230` | LABEL(md) | `include/LO_GEN.labels.md:725` | 0o300730 | 0 |
| `W1231` | LABEL(md) | `include/LO_GEN.labels.md:726` | 0o300731 | 0 |
| `W1232` | LABEL(md) | `include/LO_GEN.labels.md:727` | 0o300732 | 0 |
| `W1233` | LABEL(md) | `include/LO_GEN.labels.md:728` | 0o300733 | 0 |
| `W1234` | LABEL(md) | `include/LO_GEN.labels.md:729` | 0o300734 | 0 |
| `W1235` | LABEL(md) | `include/LO_GEN.labels.md:730` | 0o300735 | 0 |
| `W1236` | LABEL(md) | `include/LO_GEN.labels.md:731` | 0o300736 | 0 |
| `W1237` | LABEL(md) | `include/LO_GEN.labels.md:732` | 0o300737 | 0 |
| `W1240` | LABEL(md) | `include/LO_GEN.labels.md:733` | 0o300740 | 0 |
| `W1241` | LABEL(md) | `include/LO_GEN.labels.md:734` | 0o300741 | 0 |
| `W1242` | LABEL(md) | `include/LO_GEN.labels.md:735` | 0o300742 | 0 |
| `W1243` | LABEL(md) | `include/LO_GEN.labels.md:736` | 0o300743 | 0 |
| `W1244` | LABEL(md) | `include/LO_GEN.labels.md:737` | 0o300744 | 0 |
| `W1245` | LABEL(md) | `include/LO_GEN.labels.md:738` | 0o300745 | 0 |
| `W1246` | LABEL(md) | `include/LO_GEN.labels.md:739` | 0o300746 | 0 |
| `W1247` | LABEL(md) | `include/LO_GEN.labels.md:740` | 0o300747 | 0 |
| `W1250` | LABEL(md) | `include/LO_GEN.labels.md:741` | 0o300750 | 0 |
| `W1251` | LABEL(md) | `include/LO_GEN.labels.md:742` | 0o300751 | 0 |
| `W1252` | LABEL(md) | `include/LO_GEN.labels.md:743` | 0o300752 | 0 |
| `W1253` | LABEL(md) | `include/LO_GEN.labels.md:744` | 0o300753 | 0 |
| `W1254` | LABEL(md) | `include/LO_GEN.labels.md:745` | 0o300754 | 0 |
| `W1255` | LABEL(md) | `include/LO_GEN.labels.md:746` | 0o300755 | 0 |
| `W1256` | LABEL(md) | `include/LO_GEN.labels.md:747` | 0o300756 | 0 |
| `W1257` | LABEL(md) | `include/LO_GEN.labels.md:748` | 0o300757 | 0 |
| `W1260` | LABEL(md) | `include/LO_GEN.labels.md:749` | 0o300760 | 0 |
| `W1261` | LABEL(md) | `include/LO_GEN.labels.md:750` | 0o300761 | 0 |
| `W1262` | LABEL(md) | `include/LO_GEN.labels.md:751` | 0o300762 | 0 |
| `W1263` | LABEL(md) | `include/LO_GEN.labels.md:752` | 0o300763 | 0 |
| `W1264` | LABEL(md) | `include/LO_GEN.labels.md:753` | 0o300764 | 0 |
| `W1265` | LABEL(md) | `include/LO_GEN.labels.md:754` | 0o300765 | 0 |
| `W1266` | LABEL(md) | `include/LO_GEN.labels.md:755` | 0o300766 | 0 |
| `W1267` | LABEL(md) | `include/LO_GEN.labels.md:756` | 0o300767 | 0 |
| `W1270` | LABEL(md) | `include/LO_GEN.labels.md:757` | 0o300770 | 0 |
| `W1271` | LABEL(md) | `include/LO_GEN.labels.md:758` | 0o300771 | 0 |
| `W1272` | LABEL(md) | `include/LO_GEN.labels.md:759` | 0o300772 | 0 |
| `W1273` | LABEL(md) | `include/LO_GEN.labels.md:760` | 0o300773 | 0 |
| `W1274` | LABEL(md) | `include/LO_GEN.labels.md:761` | 0o300774 | 0 |
| `W1275` | LABEL(md) | `include/LO_GEN.labels.md:762` | 0o300775 | 0 |
| `W1276` | LABEL(md) | `include/LO_GEN.labels.md:763` | 0o300776 | 0 |
| `W1277` | LABEL(md) | `include/LO_GEN.labels.md:764` | 0o300777 | 0 |
| `W1300` | LABEL(md) | `include/LO_GEN.labels.md:765` | 0o301000 | 0 |
| `W1301` | LABEL(md) | `include/LO_GEN.labels.md:766` | 0o301001 | 0 |
| `W1302` | LABEL(md) | `include/LO_GEN.labels.md:767` | 0o301002 | 0 |
| `W1303` | LABEL(md) | `include/LO_GEN.labels.md:768` | 0o301003 | 0 |
| `W1304` | LABEL(md) | `include/LO_GEN.labels.md:769` | 0o301004 | 0 |
| `W1305` | LABEL(md) | `include/LO_GEN.labels.md:770` | 0o301005 | 0 |
| `W1306` | LABEL(md) | `include/LO_GEN.labels.md:771` | 0o301006 | 0 |
| `W1307` | LABEL(md) | `include/LO_GEN.labels.md:772` | 0o301007 | 0 |
| `W1310` | LABEL(md) | `include/LO_GEN.labels.md:773` | 0o301010 | 0 |
| `W1311` | LABEL(md) | `include/LO_GEN.labels.md:774` | 0o301011 | 0 |
| `W1312` | LABEL(md) | `include/LO_GEN.labels.md:775` | 0o301012 | 0 |
| `W1313` | LABEL(md) | `include/LO_GEN.labels.md:776` | 0o301013 | 0 |
| `W1314` | LABEL(md) | `include/LO_GEN.labels.md:777` | 0o301014 | 0 |
| `W1315` | LABEL(md) | `include/LO_GEN.labels.md:778` | 0o301015 | 0 |
| `W1316` | LABEL(md) | `include/LO_GEN.labels.md:779` | 0o301016 | 0 |
| `W1317` | LABEL(md) | `include/LO_GEN.labels.md:780` | 0o301017 | 0 |
| `W1320` | LABEL(md) | `include/LO_GEN.labels.md:781` | 0o301020 | 0 |
| `W1321` | LABEL(md) | `include/LO_GEN.labels.md:782` | 0o301021 | 0 |
| `W1322` | LABEL(md) | `include/LO_GEN.labels.md:783` | 0o301022 | 0 |
| `W1323` | LABEL(md) | `include/LO_GEN.labels.md:784` | 0o301023 | 0 |
| `W1324` | LABEL(md) | `include/LO_GEN.labels.md:785` | 0o301024 | 0 |
| `W1325` | LABEL(md) | `include/LO_GEN.labels.md:786` | 0o301025 | 0 |
| `W1326` | LABEL(md) | `include/LO_GEN.labels.md:787` | 0o301026 | 0 |
| `W1327` | LABEL(md) | `include/LO_GEN.labels.md:788` | 0o301027 | 0 |
| `W1330` | LABEL(md) | `include/LO_GEN.labels.md:789` | 0o301030 | 0 |
| `W1331` | LABEL(md) | `include/LO_GEN.labels.md:790` | 0o301031 | 0 |
| `W1332` | LABEL(md) | `include/LO_GEN.labels.md:791` | 0o301032 | 0 |
| `W1333` | LABEL(md) | `include/LO_GEN.labels.md:792` | 0o301033 | 0 |
| `W1334` | LABEL(md) | `include/LO_GEN.labels.md:793` | 0o301034 | 0 |
| `W1335` | LABEL(md) | `include/LO_GEN.labels.md:794` | 0o301035 | 0 |
| `W1336` | LABEL(md) | `include/LO_GEN.labels.md:795` | 0o301036 | 0 |
| `W1337` | LABEL(md) | `include/LO_GEN.labels.md:796` | 0o301037 | 0 |
| `W1340` | LABEL(md) | `include/LO_GEN.labels.md:797` | 0o301040 | 0 |
| `W1341` | LABEL(md) | `include/LO_GEN.labels.md:798` | 0o301041 | 0 |
| `W1342` | LABEL(md) | `include/LO_GEN.labels.md:799` | 0o301042 | 0 |
| `W1343` | LABEL(md) | `include/LO_GEN.labels.md:800` | 0o301043 | 0 |
| `W1344` | LABEL(md) | `include/LO_GEN.labels.md:801` | 0o301044 | 0 |
| `W1345` | LABEL(md) | `include/LO_GEN.labels.md:802` | 0o301045 | 0 |
| `W1346` | LABEL(md) | `include/LO_GEN.labels.md:803` | 0o301046 | 0 |
| `W1347` | LABEL(md) | `include/LO_GEN.labels.md:804` | 0o301047 | 0 |
| `W1350` | LABEL(md) | `include/LO_GEN.labels.md:805` | 0o301050 | 0 |
| `W1351` | LABEL(md) | `include/LO_GEN.labels.md:806` | 0o301051 | 0 |
| `W1352` | LABEL(md) | `include/LO_GEN.labels.md:807` | 0o301052 | 0 |
| `W1353` | LABEL(md) | `include/LO_GEN.labels.md:808` | 0o301053 | 0 |
| `W1354` | LABEL(md) | `include/LO_GEN.labels.md:809` | 0o301054 | 0 |
| `W1355` | LABEL(md) | `include/LO_GEN.labels.md:810` | 0o301055 | 0 |
| `W1356` | LABEL(md) | `include/LO_GEN.labels.md:811` | 0o301056 | 0 |
| `W1357` | LABEL(md) | `include/LO_GEN.labels.md:812` | 0o301057 | 0 |
| `W1360` | LABEL(md) | `include/LO_GEN.labels.md:813` | 0o301060 | 0 |
| `W1361` | LABEL(md) | `include/LO_GEN.labels.md:814` | 0o301061 | 0 |
| `W1362` | LABEL(md) | `include/LO_GEN.labels.md:815` | 0o301062 | 0 |
| `W1363` | LABEL(md) | `include/LO_GEN.labels.md:816` | 0o301063 | 0 |
| `W1364` | LABEL(md) | `include/LO_GEN.labels.md:817` | 0o301064 | 0 |
| `W1365` | LABEL(md) | `include/LO_GEN.labels.md:818` | 0o301065 | 0 |
| `W1366` | LABEL(md) | `include/LO_GEN.labels.md:819` | 0o301066 | 0 |
| `W1367` | LABEL(md) | `include/LO_GEN.labels.md:820` | 0o301067 | 0 |
| `W1370` | LABEL(md) | `include/LO_GEN.labels.md:821` | 0o301070 | 0 |
| `W1371` | LABEL(md) | `include/LO_GEN.labels.md:822` | 0o301071 | 0 |
| `W1372` | LABEL(md) | `include/LO_GEN.labels.md:823` | 0o301072 | 0 |
| `W1373` | LABEL(md) | `include/LO_GEN.labels.md:824` | 0o301073 | 0 |
| `W1374` | LABEL(md) | `include/LO_GEN.labels.md:825` | 0o301074 | 0 |
| `W1375` | LABEL(md) | `include/LO_GEN.labels.md:826` | 0o301075 | 0 |
| `W1376` | LABEL(md) | `include/LO_GEN.labels.md:827` | 0o301076 | 0 |
| `W1377` | LABEL(md) | `include/LO_GEN.labels.md:828` | 0o301077 | 0 |
| `W1400` | LABEL(md) | `include/LO_GEN.labels.md:829` | 0o301100 | 0 |
| `W1401` | LABEL(md) | `include/LO_GEN.labels.md:830` | 0o301101 | 0 |
| `W1402` | LABEL(md) | `include/LO_GEN.labels.md:831` | 0o301102 | 0 |
| `W1403` | LABEL(md) | `include/LO_GEN.labels.md:832` | 0o301103 | 0 |
| `W1404` | LABEL(md) | `include/LO_GEN.labels.md:833` | 0o301104 | 0 |
| `W1405` | LABEL(md) | `include/LO_GEN.labels.md:834` | 0o301105 | 0 |
| `W1406` | LABEL(md) | `include/LO_GEN.labels.md:835` | 0o301106 | 0 |
| `W1407` | LABEL(md) | `include/LO_GEN.labels.md:836` | 0o301107 | 0 |
| `W1410` | LABEL(md) | `include/LO_GEN.labels.md:837` | 0o301110 | 0 |
| `W1411` | LABEL(md) | `include/LO_GEN.labels.md:838` | 0o301111 | 0 |
| `W1412` | LABEL(md) | `include/LO_GEN.labels.md:839` | 0o301112 | 0 |
| `W1413` | LABEL(md) | `include/LO_GEN.labels.md:840` | 0o301113 | 0 |
| `W1414` | LABEL(md) | `include/LO_GEN.labels.md:841` | 0o301114 | 0 |
| `W1415` | LABEL(md) | `include/LO_GEN.labels.md:842` | 0o301115 | 0 |
| `W1416` | LABEL(md) | `include/LO_GEN.labels.md:843` | 0o301116 | 0 |
| `W1417` | LABEL(md) | `include/LO_GEN.labels.md:844` | 0o301117 | 0 |
| `W1420` | LABEL(md) | `include/LO_GEN.labels.md:845` | 0o301120 | 0 |
| `W1421` | LABEL(md) | `include/LO_GEN.labels.md:846` | 0o301121 | 0 |
| `W1422` | LABEL(md) | `include/LO_GEN.labels.md:847` | 0o301122 | 0 |
| `W1423` | LABEL(md) | `include/LO_GEN.labels.md:848` | 0o301123 | 0 |
| `W1424` | LABEL(md) | `include/LO_GEN.labels.md:849` | 0o301124 | 0 |
| `W1425` | LABEL(md) | `include/LO_GEN.labels.md:850` | 0o301125 | 0 |
| `W1426` | LABEL(md) | `include/LO_GEN.labels.md:851` | 0o301126 | 0 |
| `W1427` | LABEL(md) | `include/LO_GEN.labels.md:852` | 0o301127 | 0 |
| `W1430` | LABEL(md) | `include/LO_GEN.labels.md:853` | 0o301130 | 0 |
| `W1431` | LABEL(md) | `include/LO_GEN.labels.md:854` | 0o301131 | 0 |
| `W1432` | LABEL(md) | `include/LO_GEN.labels.md:855` | 0o301132 | 0 |
| `W1433` | LABEL(md) | `include/LO_GEN.labels.md:856` | 0o301133 | 0 |
| `W1434` | LABEL(md) | `include/LO_GEN.labels.md:857` | 0o301134 | 0 |
| `W1435` | LABEL(md) | `include/LO_GEN.labels.md:858` | 0o301135 | 0 |
| `W1436` | LABEL(md) | `include/LO_GEN.labels.md:859` | 0o301136 | 0 |
| `W1437` | LABEL(md) | `include/LO_GEN.labels.md:860` | 0o301137 | 0 |
| `W1440` | LABEL(md) | `include/LO_GEN.labels.md:861` | 0o301140 | 0 |
| `W1441` | LABEL(md) | `include/LO_GEN.labels.md:862` | 0o301141 | 0 |
| `W1442` | LABEL(md) | `include/LO_GEN.labels.md:863` | 0o301142 | 0 |
| `W1443` | LABEL(md) | `include/LO_GEN.labels.md:864` | 0o301143 | 0 |
| `W1444` | LABEL(md) | `include/LO_GEN.labels.md:865` | 0o301144 | 0 |
| `W1445` | LABEL(md) | `include/LO_GEN.labels.md:866` | 0o301145 | 0 |
| `W1446` | LABEL(md) | `include/LO_GEN.labels.md:867` | 0o301146 | 0 |
| `W1447` | LABEL(md) | `include/LO_GEN.labels.md:868` | 0o301147 | 0 |
| `W1450` | LABEL(md) | `include/LO_GEN.labels.md:869` | 0o301150 | 0 |
| `W1451` | LABEL(md) | `include/LO_GEN.labels.md:870` | 0o301151 | 0 |
| `W1452` | LABEL(md) | `include/LO_GEN.labels.md:871` | 0o301152 | 0 |
| `W1453` | LABEL(md) | `include/LO_GEN.labels.md:872` | 0o301153 | 0 |
| `W1454` | LABEL(md) | `include/LO_GEN.labels.md:873` | 0o301154 | 0 |
| `W1455` | LABEL(md) | `include/LO_GEN.labels.md:874` | 0o301155 | 0 |
| `W1456` | LABEL(md) | `include/LO_GEN.labels.md:875` | 0o301156 | 0 |
| `W1457` | LABEL(md) | `include/LO_GEN.labels.md:876` | 0o301157 | 0 |
| `W1460` | LABEL(md) | `include/LO_GEN.labels.md:877` | 0o301160 | 0 |
| `W1461` | LABEL(md) | `include/LO_GEN.labels.md:878` | 0o301161 | 0 |
| `W1462` | LABEL(md) | `include/LO_GEN.labels.md:879` | 0o301162 | 0 |
| `W1463` | LABEL(md) | `include/LO_GEN.labels.md:880` | 0o301163 | 0 |
| `W1464` | LABEL(md) | `include/LO_GEN.labels.md:881` | 0o301164 | 0 |
| `W1465` | LABEL(md) | `include/LO_GEN.labels.md:882` | 0o301165 | 0 |
| `W1466` | LABEL(md) | `include/LO_GEN.labels.md:883` | 0o301166 | 0 |
| `W1467` | LABEL(md) | `include/LO_GEN.labels.md:884` | 0o301167 | 0 |
| `W1470` | LABEL(md) | `include/LO_GEN.labels.md:885` | 0o301170 | 0 |
| `W1471` | LABEL(md) | `include/LO_GEN.labels.md:886` | 0o301171 | 0 |
| `W1472` | LABEL(md) | `include/LO_GEN.labels.md:887` | 0o301172 | 0 |
| `W1473` | LABEL(md) | `include/LO_GEN.labels.md:888` | 0o301173 | 0 |
| `W1474` | LABEL(md) | `include/LO_GEN.labels.md:889` | 0o301174 | 0 |
| `W1475` | LABEL(md) | `include/LO_GEN.labels.md:890` | 0o301175 | 0 |
| `W1476` | LABEL(md) | `include/LO_GEN.labels.md:891` | 0o301176 | 0 |
| `W1477` | LABEL(md) | `include/LO_GEN.labels.md:892` | 0o301177 | 0 |
| `W1500` | LABEL(md) | `include/LO_GEN.labels.md:893` | 0o301200 | 0 |
| `W1501` | LABEL(md) | `include/LO_GEN.labels.md:894` | 0o301201 | 0 |
| `W1502` | LABEL(md) | `include/LO_GEN.labels.md:895` | 0o301202 | 0 |
| `W1503` | LABEL(md) | `include/LO_GEN.labels.md:896` | 0o301203 | 0 |
| `W1504` | LABEL(md) | `include/LO_GEN.labels.md:897` | 0o301204 | 0 |
| `W1505` | LABEL(md) | `include/LO_GEN.labels.md:898` | 0o301205 | 0 |
| `W1506` | LABEL(md) | `include/LO_GEN.labels.md:899` | 0o301206 | 0 |
| `W1507` | LABEL(md) | `include/LO_GEN.labels.md:900` | 0o301207 | 0 |
| `W1510` | LABEL(md) | `include/LO_GEN.labels.md:901` | 0o301210 | 0 |
| `W1511` | LABEL(md) | `include/LO_GEN.labels.md:902` | 0o301211 | 0 |
| `W1512` | LABEL(md) | `include/LO_GEN.labels.md:903` | 0o301212 | 0 |
| `W1513` | LABEL(md) | `include/LO_GEN.labels.md:904` | 0o301213 | 0 |
| `W1514` | LABEL(md) | `include/LO_GEN.labels.md:905` | 0o301214 | 0 |
| `W1515` | LABEL(md) | `include/LO_GEN.labels.md:906` | 0o301215 | 0 |
| `W1516` | LABEL(md) | `include/LO_GEN.labels.md:907` | 0o301216 | 0 |
| `W1517` | LABEL(md) | `include/LO_GEN.labels.md:908` | 0o301217 | 0 |
| `W1520` | LABEL(md) | `include/LO_GEN.labels.md:909` | 0o301220 | 0 |
| `W1521` | LABEL(md) | `include/LO_GEN.labels.md:910` | 0o301221 | 0 |
| `W1522` | LABEL(md) | `include/LO_GEN.labels.md:911` | 0o301222 | 0 |
| `W1523` | LABEL(md) | `include/LO_GEN.labels.md:912` | 0o301223 | 0 |
| `W1524` | LABEL(md) | `include/LO_GEN.labels.md:913` | 0o301224 | 0 |
| `W1525` | LABEL(md) | `include/LO_GEN.labels.md:914` | 0o301225 | 0 |
| `W1526` | LABEL(md) | `include/LO_GEN.labels.md:915` | 0o301226 | 0 |
| `W1527` | LABEL(md) | `include/LO_GEN.labels.md:916` | 0o301227 | 0 |
| `W1530` | LABEL(md) | `include/LO_GEN.labels.md:917` | 0o301230 | 0 |
| `W1531` | LABEL(md) | `include/LO_GEN.labels.md:918` | 0o301231 | 0 |
| `W1532` | LABEL(md) | `include/LO_GEN.labels.md:919` | 0o301232 | 0 |
| `W1533` | LABEL(md) | `include/LO_GEN.labels.md:920` | 0o301233 | 0 |
| `W1534` | LABEL(md) | `include/LO_GEN.labels.md:921` | 0o301234 | 0 |
| `W1535` | LABEL(md) | `include/LO_GEN.labels.md:922` | 0o301235 | 0 |
| `W1536` | LABEL(md) | `include/LO_GEN.labels.md:923` | 0o301236 | 0 |
| `W1537` | LABEL(md) | `include/LO_GEN.labels.md:924` | 0o301237 | 0 |
| `W1540` | LABEL(md) | `include/LO_GEN.labels.md:925` | 0o301240 | 0 |
| `W1541` | LABEL(md) | `include/LO_GEN.labels.md:926` | 0o301241 | 0 |
| `W1542` | LABEL(md) | `include/LO_GEN.labels.md:927` | 0o301242 | 0 |
| `W1543` | LABEL(md) | `include/LO_GEN.labels.md:928` | 0o301243 | 0 |
| `W1544` | LABEL(md) | `include/LO_GEN.labels.md:929` | 0o301244 | 0 |
| `W1545` | LABEL(md) | `include/LO_GEN.labels.md:930` | 0o301245 | 0 |
| `W1546` | LABEL(md) | `include/LO_GEN.labels.md:931` | 0o301246 | 0 |
| `W1547` | LABEL(md) | `include/LO_GEN.labels.md:932` | 0o301247 | 0 |
| `W1550` | LABEL(md) | `include/LO_GEN.labels.md:933` | 0o301250 | 0 |
| `W1551` | LABEL(md) | `include/LO_GEN.labels.md:934` | 0o301251 | 0 |
| `W1552` | LABEL(md) | `include/LO_GEN.labels.md:935` | 0o301252 | 0 |
| `W1553` | LABEL(md) | `include/LO_GEN.labels.md:936` | 0o301253 | 0 |
| `W1554` | LABEL(md) | `include/LO_GEN.labels.md:937` | 0o301254 | 0 |
| `W1555` | LABEL(md) | `include/LO_GEN.labels.md:938` | 0o301255 | 0 |
| `W1556` | LABEL(md) | `include/LO_GEN.labels.md:939` | 0o301256 | 0 |
| `W1557` | LABEL(md) | `include/LO_GEN.labels.md:940` | 0o301257 | 0 |
| `W1560` | LABEL(md) | `include/LO_GEN.labels.md:941` | 0o301260 | 0 |
| `W1561` | LABEL(md) | `include/LO_GEN.labels.md:942` | 0o301261 | 0 |
| `W1562` | LABEL(md) | `include/LO_GEN.labels.md:943` | 0o301262 | 0 |
| `W1563` | LABEL(md) | `include/LO_GEN.labels.md:944` | 0o301263 | 0 |
| `W1564` | LABEL(md) | `include/LO_GEN.labels.md:945` | 0o301264 | 0 |
| `W1565` | LABEL(md) | `include/LO_GEN.labels.md:946` | 0o301265 | 0 |
| `W1566` | LABEL(md) | `include/LO_GEN.labels.md:947` | 0o301266 | 0 |
| `W1567` | LABEL(md) | `include/LO_GEN.labels.md:948` | 0o301267 | 0 |
| `W1570` | LABEL(md) | `include/LO_GEN.labels.md:949` | 0o301270 | 0 |
| `W1571` | LABEL(md) | `include/LO_GEN.labels.md:950` | 0o301271 | 0 |
| `W1572` | LABEL(md) | `include/LO_GEN.labels.md:951` | 0o301272 | 0 |
| `W1573` | LABEL(md) | `include/LO_GEN.labels.md:952` | 0o301273 | 0 |
| `W1574` | LABEL(md) | `include/LO_GEN.labels.md:953` | 0o301274 | 0 |
| `W1575` | LABEL(md) | `include/LO_GEN.labels.md:954` | 0o301275 | 0 |
| `W1576` | LABEL(md) | `include/LO_GEN.labels.md:955` | 0o301276 | 0 |
| `W1577` | LABEL(md) | `include/LO_GEN.labels.md:956` | 0o301277 | 0 |
| `W1600` | LABEL(md) | `include/LO_GEN.labels.md:957` | 0o301300 | 0 |
| `W1601` | LABEL(md) | `include/LO_GEN.labels.md:958` | 0o301301 | 0 |
| `W1602` | LABEL(md) | `include/LO_GEN.labels.md:959` | 0o301302 | 0 |
| `W1603` | LABEL(md) | `include/LO_GEN.labels.md:960` | 0o301303 | 0 |
| `W1604` | LABEL(md) | `include/LO_GEN.labels.md:961` | 0o301304 | 0 |
| `W1605` | LABEL(md) | `include/LO_GEN.labels.md:962` | 0o301305 | 0 |
| `W1606` | LABEL(md) | `include/LO_GEN.labels.md:963` | 0o301306 | 0 |
| `W1607` | LABEL(md) | `include/LO_GEN.labels.md:964` | 0o301307 | 0 |
| `W1610` | LABEL(md) | `include/LO_GEN.labels.md:965` | 0o301310 | 0 |
| `W1611` | LABEL(md) | `include/LO_GEN.labels.md:966` | 0o301311 | 0 |
| `W1612` | LABEL(md) | `include/LO_GEN.labels.md:967` | 0o301312 | 0 |
| `W1613` | LABEL(md) | `include/LO_GEN.labels.md:968` | 0o301313 | 0 |
| `W1614` | LABEL(md) | `include/LO_GEN.labels.md:969` | 0o301314 | 0 |
| `W1615` | LABEL(md) | `include/LO_GEN.labels.md:970` | 0o301315 | 0 |
| `W1616` | LABEL(md) | `include/LO_GEN.labels.md:971` | 0o301316 | 0 |
| `W1617` | LABEL(md) | `include/LO_GEN.labels.md:972` | 0o301317 | 0 |
| `W1620` | LABEL(md) | `include/LO_GEN.labels.md:973` | 0o301320 | 0 |
| `W1621` | LABEL(md) | `include/LO_GEN.labels.md:974` | 0o301321 | 0 |
| `W1622` | LABEL(md) | `include/LO_GEN.labels.md:975` | 0o301322 | 0 |
| `W1623` | LABEL(md) | `include/LO_GEN.labels.md:976` | 0o301323 | 0 |
| `W1624` | LABEL(md) | `include/LO_GEN.labels.md:977` | 0o301324 | 0 |
| `W1625` | LABEL(md) | `include/LO_GEN.labels.md:978` | 0o301325 | 0 |
| `W1626` | LABEL(md) | `include/LO_GEN.labels.md:979` | 0o301326 | 0 |
| `W1627` | LABEL(md) | `include/LO_GEN.labels.md:980` | 0o301327 | 0 |
| `W1630` | LABEL(md) | `include/LO_GEN.labels.md:981` | 0o301330 | 0 |
| `W1631` | LABEL(md) | `include/LO_GEN.labels.md:982` | 0o301331 | 0 |
| `W1632` | LABEL(md) | `include/LO_GEN.labels.md:983` | 0o301332 | 0 |
| `W1633` | LABEL(md) | `include/LO_GEN.labels.md:984` | 0o301333 | 0 |
| `W1634` | LABEL(md) | `include/LO_GEN.labels.md:985` | 0o301334 | 0 |
| `W1635` | LABEL(md) | `include/LO_GEN.labels.md:986` | 0o301335 | 0 |
| `W1636` | LABEL(md) | `include/LO_GEN.labels.md:987` | 0o301336 | 0 |
| `W1637` | LABEL(md) | `include/LO_GEN.labels.md:988` | 0o301337 | 0 |
| `W1640` | LABEL(md) | `include/LO_GEN.labels.md:989` | 0o301340 | 0 |
| `W1641` | LABEL(md) | `include/LO_GEN.labels.md:990` | 0o301341 | 0 |
| `W1642` | LABEL(md) | `include/LO_GEN.labels.md:991` | 0o301342 | 0 |
| `W1643` | LABEL(md) | `include/LO_GEN.labels.md:992` | 0o301343 | 0 |
| `W1644` | LABEL(md) | `include/LO_GEN.labels.md:993` | 0o301344 | 0 |
| `W1645` | LABEL(md) | `include/LO_GEN.labels.md:994` | 0o301345 | 0 |
| `W1646` | LABEL(md) | `include/LO_GEN.labels.md:995` | 0o301346 | 0 |
| `W1647` | LABEL(md) | `include/LO_GEN.labels.md:996` | 0o301347 | 0 |
| `W1650` | LABEL(md) | `include/LO_GEN.labels.md:997` | 0o301350 | 0 |
| `W1651` | LABEL(md) | `include/LO_GEN.labels.md:998` | 0o301351 | 0 |
| `W1652` | LABEL(md) | `include/LO_GEN.labels.md:999` | 0o301352 | 0 |
| `W1653` | LABEL(md) | `include/LO_GEN.labels.md:1000` | 0o301353 | 0 |
| `W1654` | LABEL(md) | `include/LO_GEN.labels.md:1001` | 0o301354 | 0 |
| `W1655` | LABEL(md) | `include/LO_GEN.labels.md:1002` | 0o301355 | 0 |
| `W1656` | LABEL(md) | `include/LO_GEN.labels.md:1003` | 0o301356 | 0 |
| `W1657` | LABEL(md) | `include/LO_GEN.labels.md:1004` | 0o301357 | 0 |
| `W1660` | LABEL(md) | `include/LO_GEN.labels.md:1005` | 0o301360 | 0 |
| `W1661` | LABEL(md) | `include/LO_GEN.labels.md:1006` | 0o301361 | 0 |
| `W1662` | LABEL(md) | `include/LO_GEN.labels.md:1007` | 0o301362 | 0 |
| `W1663` | LABEL(md) | `include/LO_GEN.labels.md:1008` | 0o301363 | 0 |
| `W1664` | LABEL(md) | `include/LO_GEN.labels.md:1009` | 0o301364 | 0 |
| `W1665` | LABEL(md) | `include/LO_GEN.labels.md:1010` | 0o301365 | 0 |
| `W1666` | LABEL(md) | `include/LO_GEN.labels.md:1011` | 0o301366 | 0 |
| `W1667` | LABEL(md) | `include/LO_GEN.labels.md:1012` | 0o301367 | 0 |
| `W1670` | LABEL(md) | `include/LO_GEN.labels.md:1013` | 0o301370 | 0 |
| `W1671` | LABEL(md) | `include/LO_GEN.labels.md:1014` | 0o301371 | 0 |
| `W1672` | LABEL(md) | `include/LO_GEN.labels.md:1015` | 0o301372 | 0 |
| `W1673` | LABEL(md) | `include/LO_GEN.labels.md:1016` | 0o301373 | 0 |
| `W1674` | LABEL(md) | `include/LO_GEN.labels.md:1017` | 0o301374 | 0 |
| `W1675` | LABEL(md) | `include/LO_GEN.labels.md:1018` | 0o301375 | 0 |
| `W1676` | LABEL(md) | `include/LO_GEN.labels.md:1019` | 0o301376 | 0 |
| `W1677` | LABEL(md) | `include/LO_GEN.labels.md:1020` | 0o301377 | 0 |
| `W1700` | LABEL(md) | `include/LO_GEN.labels.md:1021` | 0o301400 | 0 |
| `W1701` | LABEL(md) | `include/LO_GEN.labels.md:1022` | 0o301401 | 0 |
| `W1702` | LABEL(md) | `include/LO_GEN.labels.md:1023` | 0o301402 | 0 |
| `W1703` | LABEL(md) | `include/LO_GEN.labels.md:1024` | 0o301403 | 0 |
| `W1704` | LABEL(md) | `include/LO_GEN.labels.md:1025` | 0o301404 | 0 |
| `W1705` | LABEL(md) | `include/LO_GEN.labels.md:1026` | 0o301405 | 0 |
| `W1706` | LABEL(md) | `include/LO_GEN.labels.md:1027` | 0o301406 | 0 |
| `W1707` | LABEL(md) | `include/LO_GEN.labels.md:1028` | 0o301407 | 0 |
| `W1710` | LABEL(md) | `include/LO_GEN.labels.md:1029` | 0o301410 | 0 |
| `W1711` | LABEL(md) | `include/LO_GEN.labels.md:1030` | 0o301411 | 0 |
| `W1712` | LABEL(md) | `include/LO_GEN.labels.md:1031` | 0o301412 | 0 |
| `W1713` | LABEL(md) | `include/LO_GEN.labels.md:1032` | 0o301413 | 0 |
| `W1714` | LABEL(md) | `include/LO_GEN.labels.md:1033` | 0o301414 | 0 |
| `W1715` | LABEL(md) | `include/LO_GEN.labels.md:1034` | 0o301415 | 0 |
| `W1716` | LABEL(md) | `include/LO_GEN.labels.md:1035` | 0o301416 | 0 |
| `W1717` | LABEL(md) | `include/LO_GEN.labels.md:1036` | 0o301417 | 0 |
| `W1720` | LABEL(md) | `include/LO_GEN.labels.md:1037` | 0o301420 | 0 |
| `W1721` | LABEL(md) | `include/LO_GEN.labels.md:1038` | 0o301421 | 0 |
| `W1722` | LABEL(md) | `include/LO_GEN.labels.md:1039` | 0o301422 | 0 |
| `W1723` | LABEL(md) | `include/LO_GEN.labels.md:1040` | 0o301423 | 0 |
| `W1724` | LABEL(md) | `include/LO_GEN.labels.md:1041` | 0o301424 | 0 |
| `W1725` | LABEL(md) | `include/LO_GEN.labels.md:1042` | 0o301425 | 0 |
| `W1726` | LABEL(md) | `include/LO_GEN.labels.md:1043` | 0o301426 | 0 |
| `W1727` | LABEL(md) | `include/LO_GEN.labels.md:1044` | 0o301427 | 0 |
| `W1730` | LABEL(md) | `include/LO_GEN.labels.md:1045` | 0o301430 | 0 |
| `W1731` | LABEL(md) | `include/LO_GEN.labels.md:1046` | 0o301431 | 0 |
| `W1732` | LABEL(md) | `include/LO_GEN.labels.md:1047` | 0o301432 | 0 |
| `W1733` | LABEL(md) | `include/LO_GEN.labels.md:1048` | 0o301433 | 0 |
| `W1734` | LABEL(md) | `include/LO_GEN.labels.md:1049` | 0o301434 | 0 |
| `W1735` | LABEL(md) | `include/LO_GEN.labels.md:1050` | 0o301435 | 0 |
| `W1736` | LABEL(md) | `include/LO_GEN.labels.md:1051` | 0o301436 | 0 |
| `W1737` | LABEL(md) | `include/LO_GEN.labels.md:1052` | 0o301437 | 0 |
| `W1740` | LABEL(md) | `include/LO_GEN.labels.md:1053` | 0o301440 | 0 |
| `W1741` | LABEL(md) | `include/LO_GEN.labels.md:1054` | 0o301441 | 0 |
| `W1742` | LABEL(md) | `include/LO_GEN.labels.md:1055` | 0o301442 | 0 |
| `W1743` | LABEL(md) | `include/LO_GEN.labels.md:1056` | 0o301443 | 0 |
| `W1744` | LABEL(md) | `include/LO_GEN.labels.md:1057` | 0o301444 | 0 |
| `W1745` | LABEL(md) | `include/LO_GEN.labels.md:1058` | 0o301445 | 0 |
| `W1746` | LABEL(md) | `include/LO_GEN.labels.md:1059` | 0o301446 | 0 |
| `W1747` | LABEL(md) | `include/LO_GEN.labels.md:1060` | 0o301447 | 0 |
| `W1750` | LABEL(md) | `include/LO_GEN.labels.md:1061` | 0o301450 | 0 |
| `W1751` | LABEL(md) | `include/LO_GEN.labels.md:1062` | 0o301451 | 0 |
| `W1752` | LABEL(md) | `include/LO_GEN.labels.md:1063` | 0o301452 | 0 |
| `W1753` | LABEL(md) | `include/LO_GEN.labels.md:1064` | 0o301453 | 0 |
| `W1754` | LABEL(md) | `include/LO_GEN.labels.md:1065` | 0o301454 | 0 |
| `W1755` | LABEL(md) | `include/LO_GEN.labels.md:1066` | 0o301455 | 0 |
| `W1756` | LABEL(md) | `include/LO_GEN.labels.md:1067` | 0o301456 | 0 |
| `W1757` | LABEL(md) | `include/LO_GEN.labels.md:1068` | 0o301457 | 0 |
| `W1760` | LABEL(md) | `include/LO_GEN.labels.md:1069` | 0o301460 | 0 |
| `W1761` | LABEL(md) | `include/LO_GEN.labels.md:1070` | 0o301461 | 0 |
| `W1762` | LABEL(md) | `include/LO_GEN.labels.md:1071` | 0o301462 | 0 |
| `W1763` | LABEL(md) | `include/LO_GEN.labels.md:1072` | 0o301463 | 0 |
| `W1764` | LABEL(md) | `include/LO_GEN.labels.md:1073` | 0o301464 | 0 |
| `W1765` | LABEL(md) | `include/LO_GEN.labels.md:1074` | 0o301465 | 0 |
| `W1766` | LABEL(md) | `include/LO_GEN.labels.md:1075` | 0o301466 | 0 |
| `W1767` | LABEL(md) | `include/LO_GEN.labels.md:1076` | 0o301467 | 0 |
| `W1770` | LABEL(md) | `include/LO_GEN.labels.md:1077` | 0o301470 | 0 |
| `W1771` | LABEL(md) | `include/LO_GEN.labels.md:1078` | 0o301471 | 0 |
| `W1772` | LABEL(md) | `include/LO_GEN.labels.md:1079` | 0o301472 | 0 |
| `W1773` | LABEL(md) | `include/LO_GEN.labels.md:1080` | 0o301473 | 0 |
| `W1774` | LABEL(md) | `include/LO_GEN.labels.md:1081` | 0o301474 | 0 |
| `W1775` | LABEL(md) | `include/LO_GEN.labels.md:1082` | 0o301475 | 0 |
| `W1776` | LABEL(md) | `include/LO_GEN.labels.md:1083` | 0o301476 | 0 |
| `W1777` | LABEL(md) | `include/LO_GEN.labels.md:1084` | 0o301477 | 0 |
| `WT0533` | LABEL(md) | `include/LO_GEN.labels.md:32` | 0o300233 | 0 |
| `WT0535` | LABEL(md) | `include/LO_GEN.labels.md:33` | 0o300235 | 0 |
| `WT0537` | LABEL(md) | `include/LO_GEN.labels.md:34` | 0o300237 | 0 |
| `WT0541` | LABEL(md) | `include/LO_GEN.labels.md:35` | 0o300241 | 0 |
| `WT0543` | LABEL(md) | `include/LO_GEN.labels.md:36` | 0o300243 | 0 |
| `WT0545` | LABEL(md) | `include/LO_GEN.labels.md:37` | 0o300245 | 0 |
| `WT0547` | LABEL(md) | `include/LO_GEN.labels.md:38` | 0o300247 | 0 |
| `WT0551` | LABEL(md) | `include/LO_GEN.labels.md:39` | 0o300251 | 0 |
| `WT0553` | LABEL(md) | `include/LO_GEN.labels.md:40` | 0o300253 | 0 |
| `WT0555` | LABEL(md) | `include/LO_GEN.labels.md:41` | 0o300255 | 0 |
| `WT0557` | LABEL(md) | `include/LO_GEN.labels.md:42` | 0o300257 | 0 |
| `WT0561` | LABEL(md) | `include/LO_GEN.labels.md:43` | 0o300261 | 0 |
| `WT0563` | LABEL(md) | `include/LO_GEN.labels.md:44` | 0o300263 | 0 |
| `WT0565` | LABEL(md) | `include/LO_GEN.labels.md:45` | 0o300265 | 0 |
| `WT0567` | LABEL(md) | `include/LO_GEN.labels.md:46` | 0o300267 | 0 |
| `WT0571` | LABEL(md) | `include/LO_GEN.labels.md:47` | 0o300271 | 0 |
| `WT0573` | LABEL(md) | `include/LO_GEN.labels.md:48` | 0o300273 | 0 |
| `WT0575` | LABEL(md) | `include/LO_GEN.labels.md:49` | 0o300275 | 0 |
| `WT0577` | LABEL(md) | `include/LO_GEN.labels.md:50` | 0o300277 | 0 |
| `WT0601` | LABEL(md) | `include/LO_GEN.labels.md:51` | 0o300301 | 0 |
| `WT0603` | LABEL(md) | `include/LO_GEN.labels.md:52` | 0o300303 | 0 |
| `WT0605` | LABEL(md) | `include/LO_GEN.labels.md:53` | 0o300305 | 0 |
| `WT0607` | LABEL(md) | `include/LO_GEN.labels.md:54` | 0o300307 | 0 |
| `WT0611` | LABEL(md) | `include/LO_GEN.labels.md:55` | 0o300311 | 0 |
| `WT0613` | LABEL(md) | `include/LO_GEN.labels.md:56` | 0o300313 | 0 |
| `WT0615` | LABEL(md) | `include/LO_GEN.labels.md:57` | 0o300315 | 0 |
| `WT0617` | LABEL(md) | `include/LO_GEN.labels.md:58` | 0o300317 | 0 |
| `WT0621` | LABEL(md) | `include/LO_GEN.labels.md:59` | 0o300321 | 0 |
| `WT0623` | LABEL(md) | `include/LO_GEN.labels.md:60` | 0o300323 | 0 |
| `XCOM` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:168`, `include/FOREX.labels.md:654` | — | 0 |
| `XCON` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:167`, `include/FOREX.labels.md:655` | — | 0 |
| `XFOR` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:166`, `include/FOREX.labels.md:657` | — | 0 |
| `XOPR` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:169`, `include/FOREX.labels.md:659` | — | 0 |
| `XR0075` | LABEL(md) | `include/LO_GEN.labels.md:122`, `include/LO_GEN.labels.md:1218` | 0o277575 | 0 |
| `XR0123` | LABEL(md) | `include/LO_GEN.labels.md:144`, `include/LO_GEN.labels.md:1096` | 0o277623 | 0 |
| `XR0127` | LABEL(md) | `include/LO_GEN.labels.md:148`, `include/LO_GEN.labels.md:1097` | 0o277627 | 0 |
| `XR0155` | LABEL(md) | `include/LO_GEN.labels.md:170`, `include/LO_GEN.labels.md:1152` | 0o277655 | 0 |
| `XR0161` | LABEL(md) | `include/LO_GEN.labels.md:174`, `include/LO_GEN.labels.md:1136` | 0o277661 | 0 |
| `XR0214` | LABEL(md) | `include/LO_GEN.labels.md:201` | 0o277714 | 0 |
| `XR0215` | LABEL(md) | `include/LO_GEN.labels.md:202` | 0o277715 | 0 |
| `XR0251` | LABEL(md) | `include/LO_GEN.labels.md:230`, `include/LO_GEN.labels.md:1263` | 0o277751 | 0 |
| `XR0257` | LABEL(md) | `include/LO_GEN.labels.md:236` | 0o277757 | 0 |
| `XR0327` | LABEL(md) | `include/LO_GEN.labels.md:276`, `include/LO_GEN.labels.md:1136` | 0o300027 | 0 |
| `XR0676` | LABEL(md) | `include/LO_GEN.labels.md:507` | 0o300376 | 0 |
| `XR0766` | LABEL(md) | `include/LO_GEN.labels.md:563` | 0o300466 | 0 |
| `XR0767` | LABEL(md) | `include/LO_GEN.labels.md:564` | 0o300467 | 0 |
| `XR1040` | LABEL(md) | `include/LO_GEN.labels.md:605` | 0o300540 | 0 |
| `XR1041` | LABEL(md) | `include/LO_GEN.labels.md:606` | 0o300541 | 0 |
| `XR1047` | LABEL(md) | `include/LO_GEN.labels.md:612` | 0o300547 | 0 |
| `XR1050` | LABEL(md) | `include/LO_GEN.labels.md:613` | 0o300550 | 0 |
| `XR1271` | LABEL(md) | `include/LO_GEN.labels.md:758` | 0o300771 | 0 |
| `XR1272` | LABEL(md) | `include/LO_GEN.labels.md:759` | 0o300772 | 0 |
| `XR1304` | LABEL(md) | `include/LO_GEN.labels.md:769` | 0o301004 | 0 |
| `XR1305` | LABEL(md) | `include/LO_GEN.labels.md:770` | 0o301005 | 0 |
| `XR1314` | LABEL(md) | `include/LO_GEN.labels.md:777` | 0o301014 | 0 |
| `XR1315` | LABEL(md) | `include/LO_GEN.labels.md:778` | 0o301015 | 0 |
| `XR1320` | LABEL(md) | `include/LO_GEN.labels.md:781`, `include/LO_GEN.labels.md:1268` | 0o301020 | 0 |
| `XR1372` | LABEL(md) | `include/LO_GEN.labels.md:823` | 0o301072 | 0 |
| `XR1373` | LABEL(md) | `include/LO_GEN.labels.md:824` | 0o301073 | 0 |
| `XR1404` | LABEL(md) | `include/LO_GEN.labels.md:833` | 0o301104 | 0 |
| `XR1405` | LABEL(md) | `include/LO_GEN.labels.md:834` | 0o301105 | 0 |
| `XR1414` | LABEL(md) | `include/LO_GEN.labels.md:841`, `include/LO_GEN.labels.md:1172` | 0o301114 | 0 |
| `XR1473` | LABEL(md) | `include/LO_GEN.labels.md:888`, `include/LO_GEN.labels.md:1280` | 0o301173 | 0 |
| `XR1521` | LABEL(md) | `include/LO_GEN.labels.md:910` | 0o301221 | 0 |
| `XR1522` | LABEL(md) | `include/LO_GEN.labels.md:911` | 0o301222 | 0 |
| `XR1536` | LABEL(md) | `include/LO_GEN.labels.md:923` | 0o301236 | 0 |
| `XR1537` | LABEL(md) | `include/LO_GEN.labels.md:924` | 0o301237 | 0 |
| `XR1551` | LABEL(md) | `include/LO_GEN.labels.md:934` | 0o301251 | 0 |
| `XR1552` | LABEL(md) | `include/LO_GEN.labels.md:935` | 0o301252 | 0 |
| `XR1563` | LABEL(md) | `include/LO_GEN.labels.md:944` | 0o301263 | 0 |
| `XR1564` | LABEL(md) | `include/LO_GEN.labels.md:945` | 0o301264 | 0 |
| `XR1606` | LABEL(md) | `include/LO_GEN.labels.md:963` | 0o301306 | 0 |
| `XR1607` | LABEL(md) | `include/LO_GEN.labels.md:964` | 0o301307 | 0 |
| `XR1615` | LABEL(md) | `include/LO_GEN.labels.md:970` | 0o301315 | 0 |
| `XR1616` | LABEL(md) | `include/LO_GEN.labels.md:971` | 0o301316 | 0 |
| `XR1631` | LABEL(md) | `include/LO_GEN.labels.md:982` | 0o301331 | 0 |
| `XR1632` | LABEL(md) | `include/LO_GEN.labels.md:983` | 0o301332 | 0 |
| `XR1770` | LABEL(md) | `include/LO_GEN.labels.md:1077`, `include/LO_GEN.labels.md:1163` | 0o301470 | 0 |
| `XR1777` | LABEL(md) | `include/LO_GEN.labels.md:1084` | 0o301477 | 0 |
| `X_ПP` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:170`, `src/LO_GEN.mad:37`, `include/LO_GEN.labels.md:26`, `include/LO_GEN.labels.md:26`, `include/LO_GEN.labels.md:26` | — | 0 |
| `YRMSK` | LABEL(md)/TEXT | `src/FOREX_RUNTIME.mad:421`, `include/FOREX.labels.md:663` | — | 0 |
| `Z00` | LABEL(md) | `include/FOREX.labels.md:352` | — | 0 |
| `ИМЯ_` | LABEL(md) | `include/FOREX.labels.md:32`, `include/FOREX.labels.md:32`, `include/FOREX.labels.md:358` | 0o510413 | 0 |
| `ПP` | LABEL(md)/SUBP | `src/LO_SYN.mad:36`, `include/FOREX_ROOT.mad:77`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | — | 0 |
| `втбрз` | LABEL(md) | `include/LO_GEN.labels.md:1551` | — | 0 |
| `э20` | LABEL(md) | `include/LO_GEN.labels.md:1551` | — | 0 |

### 2.2 Именованные константы (`,EQU,`)

Требование «все литералы — в переменные»: числовые литералы выносятся в
именованные `EQU`-константы. Здесь собраны все такие объявления и их применения.

| Имя | Значение | Определение (файл:строка) | Применения | Всего |
|---|---|---|---|---:|
| `BS14R` | `14` | `include/FOREX_ROOT.mad:24` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `BUFALN` | `4000B` | `include/FOREX_ROOT.mad:25` | `src/FOREX_CORE.mad:457`, `include/FOREX_ROOT.mad:78` | 2 |
| `DEC_15` | `15` | `include/FOREX_ROOT.mad:26` | — | 0 |
| `DUMMYL` | `5` | `include/FOREX_ROOT.mad:27` | `src/FOREX_CORE.mad:154`, `include/FOREX_ROOT.mad:67` | 2 |
| `ENTTLN` | `50B` | `include/FOREX_ROOT.mad:28` | `src/FOREX_CORE.mad:393`, `include/FOREX_ROOT.mad:62` | 2 |
| `ERRTRT` | `18H'200'0OШ` | `include/FOREX_ROOT.mad:29` | `include/FOREX_ROOT.mad:149` | 1 |
| `FIXM2` | `2` | `include/FOREX_ROOT.mad:30` | `src/FOREX_RUNTIME.mad:509` | 1 |
| `GOST_V` | `1H'212'` | `include/FOREX_ROOT.mad:31` | `include/FOREX_ROOT.mad:145` | 1 |
| `GOSTVR` | `6HBPEMЯ-` | `include/FOREX_ROOT.mad:32` | `include/FOREX_ROOT.mad:146` | 1 |
| `GOSTYA` | `1H'231'` | `include/FOREX_ROOT.mad:33` | `include/FOREX_ROOT.mad:148` | 1 |
| `MODE_6` | `6` | `include/FOREX_ROOT.mad:34` | `src/FOREX_RUNTIME.mad:345`, `include/FOREX_ROOT.mad:82`, `include/FOREX_ROOT.mad:113`, `include/FOREX_ROOT.mad:126` | 4 |
| `MRT22D` | `18` | `include/FOREX_ROOT.mad:35` | `include/FOREX_ROOT.mad:112` | 1 |
| `ONEW` | `1` | `include/FOREX_ROOT.mad:36` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `PG17AD` | `17B` | `include/FOREX_ROOT.mad:37` | `include/FOREX_ROOT.mad:262`, `include/FOREX_ROOT.mad:268`, `include/FOREX_ROOT.mad:269`, `include/FOREX_ROOT.mad:271` | 4 |
| `PGMD73` | `=73401` | `include/FOREX_ROOT.mad:38` | `include/FOREX_ROOT.mad:244`, `include/FOREX_ROOT.mad:249` | 2 |
| `PGBLKM` | `=4000` | `include/FOREX_ROOT.mad:39` | `include/FOREX_ROOT.mad:282` | 1 |
| `PG67CD` | `=:11 4037 77` | `include/FOREX_ROOT.mad:40` | `include/FOREX_ROOT.mad:248` | 1 |
| `PGFLGS` | `64+12` | `include/FOREX_ROOT.mad:41` | `include/FOREX_ROOT.mad:245` | 1 |
| `PGGO1` | `=:00 2677` | `include/FOREX_ROOT.mad:42` | `include/FOREX_ROOT.mad:284` | 1 |
| `PGGO2` | `=:00 6736 77` | `include/FOREX_ROOT.mad:43` | `include/FOREX_ROOT.mad:285` | 1 |
| `PGWDSH` | `64-20` | `include/FOREX_ROOT.mad:44` | `include/FOREX_ROOT.mad:253` | 1 |
| `PRBKLN` | `002` | `include/FOREX_ROOT.mad:45` | — | 0 |
| `RMOD3` | `3` | `include/FOREX_ROOT.mad:46` | `src/FOREX_RUNTIME.mad:217`, `src/FOREX_RUNTIME.mad:490`, `include/FOREX_ROOT.mad:116` | 3 |
| `RETLR` | `13` | `include/FOREX_ROOT.mad:47` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `RMWD4` | `4` | `include/FOREX_ROOT.mad:48` | `include/FOREX_ROOT.mad:241` | 1 |
| `STKOF2` | `-2` | `include/FOREX_ROOT.mad:49` | `src/FOREX_RUNTIME.mad:350`, `src/FOREX_RUNTIME.mad:505`, `include/FOREX_ROOT.mad:255` | 3 |
| `TXLGEN` | `8HLO*GEN` | `include/FOREX_ROOT.mad:50` | `include/FOREX_ROOT.mad:152` | 1 |
| `TXLSYN` | `8HLO*SYN` | `include/FOREX_ROOT.mad:51` | `include/FOREX_ROOT.mad:151` | 1 |
| `TIMSCL` | `=R100.0` | `include/FOREX_ROOT.mad:52` | `include/FOREX_ROOT.mad:115` | 1 |
| `TIMSEA` | `=6H'''17''17''17''17''17'` | `include/FOREX_ROOT.mad:53` | `include/FOREX_ROOT.mad:120` | 1 |
| `TIMSEB` | `=6H'17''17''17''''17''17'` | `include/FOREX_ROOT.mad:54` | `include/FOREX_ROOT.mad:121` | 1 |
| `TIMSEC` | `=6H'''''''16'''''` | `include/FOREX_ROOT.mad:55` | `include/FOREX_ROOT.mad:122` | 1 |
| `LNK15` | `15` | `include/FOREX_ROOT.mad:56` | `include/FOREX_ROOT.mad:251`, `include/FOREX_ROOT.mad:264`, `include/FOREX_ROOT.mad:281` | 3 |
| `PGSTP2` | `2` | `include/FOREX_ROOT.mad:57` | `include/FOREX_ROOT.mad:256`, `include/FOREX_ROOT.mad:259` | 2 |
| `AOC4K` | `0o4000` | `src/FOREX_CORE.mad:33` | `src/FOREX_CORE.mad:156` | 1 |
| `AOC50` | `0o50` | `src/FOREX_CORE.mad:34` | `src/FOREX_CORE.mad:149` | 1 |
| `AI0AD` | `4007B` | `src/FOREX_CORE.mad:35` | `src/FOREX_CORE.mad:266`, `src/FOREX_CORE.mad:270` | 2 |
| `BS16A` | `74001B` | `src/FOREX_CORE.mad:36` | `src/FOREX_CORE.mad:208` | 1 |
| `BS14R` | `14` | `src/FOREX_CORE.mad:37` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `BUFALN` | `4000B` | `src/FOREX_CORE.mad:38` | `src/FOREX_CORE.mad:457`, `include/FOREX_ROOT.mad:78` | 2 |
| `DPRAD` | `74010B` | `src/FOREX_CORE.mad:98` | `src/FOREX_CORE.mad:224` | 1 |
| `DEC_38` | `38` | `src/FOREX_CORE.mad:99` | `src/FOREX_CORE.mad:354` | 1 |
| `DEC_43` | `43` | `src/FOREX_CORE.mad:100` | `src/FOREX_CORE.mad:337` | 1 |
| `DMB07` | `40007B` | `src/FOREX_CORE.mad:101` | `src/FOREX_CORE.mad:223` | 1 |
| `DMC04` | `4026B` | `src/FOREX_CORE.mad:102` | `src/FOREX_CORE.mad:218` | 1 |
| `DMC05` | `4027B` | `src/FOREX_CORE.mad:103` | `src/FOREX_CORE.mad:229` | 1 |
| `DMC06` | `4030B` | `src/FOREX_CORE.mad:104` | `src/FOREX_CORE.mad:234` | 1 |
| `DUMMYL` | `5` | `src/FOREX_CORE.mad:105` | `src/FOREX_CORE.mad:154`, `include/FOREX_ROOT.mad:67` | 2 |
| `DMTIM` | `4025B` | `src/FOREX_CORE.mad:106` | `src/FOREX_CORE.mad:207`, `src/FOREX_CORE.mad:297`, `src/FOREX_CORE.mad:317` | 3 |
| `ENTTA` | `4006B` | `src/FOREX_CORE.mad:107` | `src/FOREX_CORE.mad:213`, `src/FOREX_CORE.mad:473`, `src/FOREX_CORE.mad:477`, `src/FOREX_CORE.mad:481`, `src/FOREX_CORE.mad:485` | 5 |
| `ENTTLN` | `50B` | `src/FOREX_CORE.mad:108` | `src/FOREX_CORE.mad:393`, `include/FOREX_ROOT.mad:62` | 2 |
| `X57M6` | `6B` | `src/FOREX_CORE.mad:109` | `src/FOREX_CORE.mad:197`, `src/FOREX_CORE.mad:256`, `src/FOREX_CORE.mad:296` | 3 |
| `FLGAD` | `4002B` | `src/FOREX_CORE.mad:110` | `src/FOREX_CORE.mad:301` | 1 |
| `FMRZB` | `4035B` | `src/FOREX_CORE.mad:111` | `src/FOREX_CORE.mad:276` | 1 |
| `FMSBR` | `4034B` | `src/FOREX_CORE.mad:112` | `src/FOREX_CORE.mad:275` | 1 |
| `FULAD` | `4004B` | `src/FOREX_CORE.mad:113` | `src/FOREX_CORE.mad:228` | 1 |
| `GATAD` | `7417B` | `src/FOREX_CORE.mad:114` | `src/FOREX_CORE.mad:332`, `src/FOREX_CORE.mad:333`, `src/FOREX_CORE.mad:346`, `src/FOREX_CORE.mad:347`, `src/FOREX_CORE.mad:376`, `src/FOREX_CORE.mad:377` … (+2) | 8 |
| `INFAD` | `4036B` | `src/FOREX_CORE.mad:115` | `src/FOREX_CORE.mad:281` | 1 |
| `IC033` | `33B` | `src/FOREX_CORE.mad:116` | `src/FOREX_CORE.mad:187` | 1 |
| `IM150` | `1500B` | `src/FOREX_CORE.mad:117` | `src/FOREX_CORE.mad:186` | 1 |
| `IM170` | `1700B` | `src/FOREX_CORE.mad:118` | `src/FOREX_CORE.mad:182` | 1 |
| `LDADDR` | `74022B` | `src/FOREX_CORE.mad:119` | `src/FOREX_CORE.mad:245`, `src/FOREX_CORE.mad:250` | 2 |
| `LGTAD` | `4032B` | `src/FOREX_CORE.mad:120` | `src/FOREX_CORE.mad:249` | 1 |
| `LSTAD` | `4031B` | `src/FOREX_CORE.mad:121` | `src/FOREX_CORE.mad:244` | 1 |
| `MK760` | `7760B` | `src/FOREX_CORE.mad:122` | `src/FOREX_CORE.mad:588` | 1 |
| `MK761` | `7761B` | `src/FOREX_CORE.mad:123` | `src/FOREX_CORE.mad:596`, `src/FOREX_CORE.mad:604` | 2 |
| `MK763` | `7763B` | `src/FOREX_CORE.mad:124` | `src/FOREX_CORE.mad:600`, `src/FOREX_CORE.mad:608` | 2 |
| `MISAD` | `40037B` | `src/FOREX_CORE.mad:125` | `src/FOREX_CORE.mad:312` | 1 |
| `MRT22` | `22B` | `src/FOREX_CORE.mad:126` | `src/FOREX_CORE.mad:255` | 1 |
| `ML771` | `7771B` | `src/FOREX_CORE.mad:127` | `src/FOREX_CORE.mad:592` | 1 |
| `NOLAD` | `4003B` | `src/FOREX_CORE.mad:128` | `src/FOREX_CORE.mad:217` | 1 |
| `OCDAD` | `74013B` | `src/FOREX_CORE.mad:129` | `src/FOREX_CORE.mad:271` | 1 |
| `ONEW` | `1` | `src/FOREX_CORE.mad:130` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `PGVAD` | `74012B` | `src/FOREX_CORE.mad:131` | `src/FOREX_CORE.mad:238` | 1 |
| `PTKAD` | `74011B` | `src/FOREX_CORE.mad:132` | `src/FOREX_CORE.mad:307` | 1 |
| `PRMSAD` | `40023B` | `src/FOREX_CORE.mad:133` | `src/FOREX_CORE.mad:318` | 1 |
| `R100A` | `4033B` | `src/FOREX_CORE.mad:134` | `src/FOREX_CORE.mad:261` | 1 |
| `RZPAG` | `70000B` | `src/FOREX_CORE.mad:135` | `src/FOREX_CORE.mad:363`, `src/FOREX_CORE.mad:368`, `src/FOREX_CORE.mad:518`, `src/FOREX_CORE.mad:573` | 4 |
| `RETCL` | `4023B` | `src/FOREX_CORE.mad:136` | `src/FOREX_CORE.mad:193` | 1 |
| `RETLR` | `13` | `src/FOREX_CORE.mad:137` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `RETMA` | `40050B` | `src/FOREX_CORE.mad:138` | `src/FOREX_CORE.mad:302` | 1 |
| `SYMTG` | `65412B` | `src/FOREX_CORE.mad:139` | `src/FOREX_CORE.mad:527`, `src/FOREX_CORE.mad:531`, `src/FOREX_CORE.mad:535` | 3 |
| `TIMCL` | `4024B` | `src/FOREX_CORE.mad:140` | `src/FOREX_CORE.mad:202`, `src/FOREX_CORE.mad:260`, `src/FOREX_CORE.mad:282` | 3 |
| `TTXAD` | `4037B` | `src/FOREX_CORE.mad:141` | `src/FOREX_CORE.mad:290` | 1 |
| `TTXBA` | `40033B` | `src/FOREX_CORE.mad:142` | `src/FOREX_CORE.mad:285` | 1 |
| `NMENT` | `ENTRY*` | `src/FOREX_CORE.mad:614` | — | 0 |
| `NMFEX` | `FLGEX*` | `src/FOREX_CORE.mad:615` | — | 0 |
| `NMNOL` | `NOLISF` | `src/FOREX_CORE.mad:616` | — | 0 |
| `NMFUL` | `FULISF` | `src/FOREX_CORE.mad:617` | — | 0 |
| `NMCHK` | `CHECKF` | `src/FOREX_CORE.mad:618` | — | 0 |
| `NMDUM` | `*DUMON` | `src/FOREX_CORE.mad:619` | — | 0 |
| `NMDPR` | `DATAPR` | `src/FOREX_CORE.mad:620` | — | 0 |
| `NMTAK` | `TAK/PG` | `src/FOREX_CORE.mad:621` | — | 0 |
| `NMGIV` | `GIV/PG` | `src/FOREX_CORE.mad:622` | — | 0 |
| `NMOCT` | `OCTTDE` | `src/FOREX_CORE.mad:623` | — | 0 |
| `NMFOR` | `FOREX` | `src/FOREX_CORE.mad:624` | — | 0 |
| `NMCON` | `CONST` | `src/FOREX_CORE.mad:625` | — | 0 |
| `NMCOM` | `COMEQ` | `src/FOREX_CORE.mad:626` | — | 0 |
| `NMOPR` | `OPRTR` | `src/FOREX_CORE.mad:627` | — | 0 |
| `NMLDG` | `LOADAN` | `src/FOREX_CORE.mad:628` | — | 0 |
| `DR13` | `13` | `src/FOREX_DECODER_DISASM.mad:43` | `src/FOREX_DECODER_DISASM.mad:150`, `src/FOREX_DECODER_DISASM.mad:193`, `src/FOREX_DECODER_DISASM.mad:202`, `src/FOREX_DECODER_DISASM.mad:206`, `src/FOREX_DECODER_DISASM.mad:216` | 5 |
| `DR14` | `14` | `src/FOREX_DECODER_DISASM.mad:44` | — | 0 |
| `DR15` | `15` | `src/FOREX_DECODER_DISASM.mad:45` | `src/FOREX_DECODER_DISASM.mad:180` | 1 |
| `D64P16` | `64+16` | `src/FOREX_DECODER_DISASM.mad:46` | `src/FOREX_DECODER_DISASM.mad:165` | 1 |
| `D64P35` | `64+35` | `src/FOREX_DECODER_DISASM.mad:47` | `src/FOREX_DECODER_DISASM.mad:169` | 1 |
| `D64M24` | `64-24` | `src/FOREX_DECODER_DISASM.mad:48` | `src/FOREX_DECODER_DISASM.mad:181` | 1 |
| `D64M14` | `64-14` | `src/FOREX_DECODER_DISASM.mad:49` | `src/FOREX_DECODER_DISASM.mad:183`, `src/FOREX_DECODER_DISASM.mad:209` | 2 |
| `D64M22` | `64-22` | `src/FOREX_DECODER_DISASM.mad:50` | `src/FOREX_DECODER_DISASM.mad:188` | 1 |
| `DS06` | `6` | `src/FOREX_DECODER_DISASM.mad:51` | `src/FOREX_DECODER_DISASM.mad:157` | 1 |
| `DS03` | `3` | `src/FOREX_DECODER_DISASM.mad:52` | — | 0 |
| `DS02` | `2` | `src/FOREX_DECODER_DISASM.mad:53` | — | 0 |
| `DS01` | `1` | `src/FOREX_DECODER_DISASM.mad:54` | `src/FOREX_DECODER_DISASM.mad:195` | 1 |
| `DS24` | `24` | `src/FOREX_DECODER_DISASM.mad:55` | `src/FOREX_DECODER_DISASM.mad:172` | 1 |
| `DS16` | `16` | `src/FOREX_DECODER_DISASM.mad:56` | — | 0 |
| `DS00` | `0` | `src/FOREX_DECODER_DISASM.mad:57` | `src/FOREX_DECODER_DISASM.mad:155`, `src/FOREX_DECODER_DISASM.mad:170`, `src/FOREX_DECODER_DISASM.mad:171`, `src/FOREX_DECODER_DISASM.mad:174`, `src/FOREX_DECODER_DISASM.mad:178`, `src/FOREX_DECODER_DISASM.mad:185` … (+19) | 25 |
| `DN02` | `-2` | `src/FOREX_DECODER_DISASM.mad:58` | `src/FOREX_DECODER_DISASM.mad:163` | 1 |
| `DN03` | `-3` | `src/FOREX_DECODER_DISASM.mad:59` | `src/FOREX_DECODER_DISASM.mad:167` | 1 |
| `DN04` | `-4` | `src/FOREX_DECODER_DISASM.mad:60` | `src/FOREX_DECODER_DISASM.mad:182`, `src/FOREX_DECODER_DISASM.mad:187` | 2 |
| `DN06` | `-6` | `src/FOREX_DECODER_DISASM.mad:61` | `src/FOREX_DECODER_DISASM.mad:200` | 1 |
| `DN08` | `-8` | `src/FOREX_DECODER_DISASM.mad:62` | `src/FOREX_DECODER_DISASM.mad:192` | 1 |
| `DN01` | `-1` | `src/FOREX_DECODER_DISASM.mad:63` | — | 0 |
| `DN05` | `-5` | `src/FOREX_DECODER_DISASM.mad:64` | — | 0 |
| `DV067` | `67B` | `src/FOREX_DECODER_DISASM.mad:65` | `src/FOREX_DECODER_DISASM.mad:156` | 1 |
| `DV032` | `32B` | `src/FOREX_DECODER_DISASM.mad:66` | `src/FOREX_DECODER_DISASM.mad:162` | 1 |
| `DV043` | `43B` | `src/FOREX_DECODER_DISASM.mad:67` | `src/FOREX_DECODER_DISASM.mad:164`, `src/FOREX_DECODER_DISASM.mad:189` | 2 |
| `DV033` | `33B` | `src/FOREX_DECODER_DISASM.mad:68` | `src/FOREX_DECODER_DISASM.mad:166` | 1 |
| `DV047` | `47B` | `src/FOREX_DECODER_DISASM.mad:69` | `src/FOREX_DECODER_DISASM.mad:168` | 1 |
| `DV030` | `30B` | `src/FOREX_DECODER_DISASM.mad:70` | — | 0 |
| `DV035` | `35B` | `src/FOREX_DECODER_DISASM.mad:71` | `src/FOREX_DECODER_DISASM.mad:179`, `src/FOREX_DECODER_DISASM.mad:191` | 2 |
| `DV044` | `44B` | `src/FOREX_DECODER_DISASM.mad:72` | `src/FOREX_DECODER_DISASM.mad:184` | 1 |
| `DV034` | `34B` | `src/FOREX_DECODER_DISASM.mad:73` | `src/FOREX_DECODER_DISASM.mad:186` | 1 |
| `DV024` | `24B` | `src/FOREX_DECODER_DISASM.mad:74` | `src/FOREX_DECODER_DISASM.mad:190`, `src/FOREX_DECODER_DISASM.mad:210` | 2 |
| `DV027` | `27B` | `src/FOREX_DECODER_DISASM.mad:75` | `src/FOREX_DECODER_DISASM.mad:211` | 1 |
| `DV025` | `25B` | `src/FOREX_DECODER_DISASM.mad:76` | `src/FOREX_DECODER_DISASM.mad:213` | 1 |
| `DV026` | `26B` | `src/FOREX_DECODER_DISASM.mad:77` | `src/FOREX_DECODER_DISASM.mad:214` | 1 |
| `DV012` | `12B` | `src/FOREX_DECODER_DISASM.mad:78` | — | 0 |
| `DV013` | `13B` | `src/FOREX_DECODER_DISASM.mad:79` | — | 0 |
| `DV014` | `14B` | `src/FOREX_DECODER_DISASM.mad:80` | — | 0 |
| `DV773` | `7773B` | `src/FOREX_DECODER_DISASM.mad:81` | `src/FOREX_DECODER_DISASM.mad:220` | 1 |
| `DV777` | `7777B` | `src/FOREX_DECODER_DISASM.mad:82` | `src/FOREX_DECODER_DISASM.mad:221` | 1 |
| `DFUN67` | `67` | `src/FOREX_DECODER_DISASM.mad:83` | — | 0 |
| `DW00` | `4020741740003417` | `src/FOREX_DECODER_DISASM.mad:85` | `src/FOREX_DECODER_DISASM.mad:224` | 1 |
| `DW01` | `3700055000000017` | `src/FOREX_DECODER_DISASM.mad:86` | `src/FOREX_DECODER_DISASM.mad:225` | 1 |
| `DW02` | `0000000003600000` | `src/FOREX_DECODER_DISASM.mad:87` | `src/FOREX_DECODER_DISASM.mad:226` | 1 |
| `DW03` | `4620741717426442` | `src/FOREX_DECODER_DISASM.mad:88` | `src/FOREX_DECODER_DISASM.mad:227` | 1 |
| `DW04` | `150224421302006` | `src/FOREX_DECODER_DISASM.mad:89` | `src/FOREX_DECODER_DISASM.mad:228` | 1 |
| `DW05` | `1720000000000000` | `src/FOREX_DECODER_DISASM.mad:90` | `src/FOREX_DECODER_DISASM.mad:229` | 1 |
| `DW06` | `0000000000000000` | `src/FOREX_DECODER_DISASM.mad:91` | `src/FOREX_DECODER_DISASM.mad:230` | 1 |
| `DW07` | `1002104314222455` | `src/FOREX_DECODER_DISASM.mad:92` | `src/FOREX_DECODER_DISASM.mad:231` | 1 |
| `DW10` | `0000003600000034` | `src/FOREX_DECODER_DISASM.mad:93` | `src/FOREX_DECODER_DISASM.mad:232` | 1 |
| `DW11` | `0000141700007417` | `src/FOREX_DECODER_DISASM.mad:94` | `src/FOREX_DECODER_DISASM.mad:233` | 1 |
| `DW12` | `0000000000007417` | `src/FOREX_DECODER_DISASM.mad:95` | `src/FOREX_DECODER_DISASM.mad:234` | 1 |
| `DW13` | `1612221516360000` | `src/FOREX_DECODER_DISASM.mad:96` | `src/FOREX_DECODER_DISASM.mad:235` | 1 |
| `DW14` | `1102245203607417` | `src/FOREX_DECODER_DISASM.mad:97` | `src/FOREX_DECODER_DISASM.mad:236` | 1 |
| `DW15` | `0000000000000776` | `src/FOREX_DECODER_DISASM.mad:98` | `src/FOREX_DECODER_DISASM.mad:237` | 1 |
| `DW16` | `0000000000036074` | `src/FOREX_DECODER_DISASM.mad:99` | `src/FOREX_DECODER_DISASM.mad:238` | 1 |
| `DW17` | `0060740003607400` | `src/FOREX_DECODER_DISASM.mad:100` | `src/FOREX_DECODER_DISASM.mad:239` | 1 |
| `DW20` | `2020172020172020` | `src/FOREX_DECODER_DISASM.mad:101` | `src/FOREX_DECODER_DISASM.mad:240` | 1 |
| `OR12` | `12` | `src/FOREX_DECODER_DISASM.mad:103` | `src/FOREX_DECODER_DISASM.mad:250` | 1 |
| `OR13` | `13` | `src/FOREX_DECODER_DISASM.mad:104` | `src/FOREX_DECODER_DISASM.mad:301`, `src/FOREX_DECODER_DISASM.mad:311` | 2 |
| `OR14` | `14` | `src/FOREX_DECODER_DISASM.mad:105` | — | 0 |
| `OR15` | `15` | `src/FOREX_DECODER_DISASM.mad:106` | — | 0 |
| `ON02` | `-2` | `src/FOREX_DECODER_DISASM.mad:107` | `src/FOREX_DECODER_DISASM.mad:320` | 1 |
| `ON03` | `-3` | `src/FOREX_DECODER_DISASM.mad:108` | `src/FOREX_DECODER_DISASM.mad:306`, `src/FOREX_DECODER_DISASM.mad:308`, `src/FOREX_DECODER_DISASM.mad:314` | 3 |
| `ON04` | `-4` | `src/FOREX_DECODER_DISASM.mad:109` | `src/FOREX_DECODER_DISASM.mad:256`, `src/FOREX_DECODER_DISASM.mad:312` | 2 |
| `OI64` | `64` | `src/FOREX_DECODER_DISASM.mad:110` | `src/FOREX_DECODER_DISASM.mad:309` | 1 |
| `OI64M8` | `64-8` | `src/FOREX_DECODER_DISASM.mad:111` | `src/FOREX_DECODER_DISASM.mad:277` | 1 |
| `O64M24` | `64-24` | `src/FOREX_DECODER_DISASM.mad:112` | `src/FOREX_DECODER_DISASM.mad:321` | 1 |
| `OI10` | `10` | `src/FOREX_DECODER_DISASM.mad:113` | `src/FOREX_DECODER_DISASM.mad:274` | 1 |
| `OI03` | `3` | `src/FOREX_DECODER_DISASM.mad:114` | `src/FOREX_DECODER_DISASM.mad:262`, `src/FOREX_DECODER_DISASM.mad:303` | 2 |
| `OI02` | `2` | `src/FOREX_DECODER_DISASM.mad:115` | `src/FOREX_DECODER_DISASM.mad:265`, `src/FOREX_DECODER_DISASM.mad:324` | 2 |
| `OI01` | `1` | `src/FOREX_DECODER_DISASM.mad:116` | `src/FOREX_DECODER_DISASM.mad:325` | 1 |
| `OV015` | `15B` | `src/FOREX_DECODER_DISASM.mad:117` | `src/FOREX_DECODER_DISASM.mad:300` | 1 |
| `OV016` | `16B` | `src/FOREX_DECODER_DISASM.mad:118` | `src/FOREX_DECODER_DISASM.mad:310` | 1 |
| `OV017` | `17B` | `src/FOREX_DECODER_DISASM.mad:119` | `src/FOREX_DECODER_DISASM.mad:307` | 1 |
| `OV024` | `24B` | `src/FOREX_DECODER_DISASM.mad:120` | — | 0 |
| `OV100` | `100B` | `src/FOREX_DECODER_DISASM.mad:121` | — | 0 |
| `OV020` | `20B` | `src/FOREX_DECODER_DISASM.mad:122` | — | 0 |
| `OV021` | `21B` | `src/FOREX_DECODER_DISASM.mad:123` | — | 0 |
| `OMSK15` | `0000000000077777` | `src/FOREX_DECODER_DISASM.mad:124` | `src/FOREX_DECODER_DISASM.mad:253`, `src/FOREX_DECODER_DISASM.mad:270` | 2 |
| `OINT0` | `0` | `src/FOREX_DECODER_DISASM.mad:125` | `src/FOREX_DECODER_DISASM.mad:282` | 1 |
| `OREAL1` | `2030000000000000` | `src/FOREX_DECODER_DISASM.mad:126` | `src/FOREX_DECODER_DISASM.mad:283` | 1 |
| `ORL10` | `2112000000000000` | `src/FOREX_DECODER_DISASM.mad:127` | `src/FOREX_DECODER_DISASM.mad:284` | 1 |
| `ORL100` | `2174400000000000` | `src/FOREX_DECODER_DISASM.mad:128` | `src/FOREX_DECODER_DISASM.mad:285` | 1 |
| `ORL1K` | `2257500000000000` | `src/FOREX_DECODER_DISASM.mad:129` | `src/FOREX_DECODER_DISASM.mad:286` | 1 |
| `ORL10K` | `2351610000000000` | `src/FOREX_DECODER_DISASM.mad:130` | `src/FOREX_DECODER_DISASM.mad:287` | 1 |
| `ORL1E5` | `2434152000000000` | `src/FOREX_DECODER_DISASM.mad:131` | `src/FOREX_DECODER_DISASM.mad:288` | 1 |
| `OZEROS` | `2020202020200000` | `src/FOREX_DECODER_DISASM.mad:132` | `src/FOREX_DECODER_DISASM.mad:273`, `src/FOREX_DECODER_DISASM.mad:289` | 2 |
| `OXB40` | `0017777777777777` | `src/FOREX_DECODER_DISASM.mad:133` | `src/FOREX_DECODER_DISASM.mad:327` | 1 |
| `OXC10` | `4000000000000012` | `src/FOREX_DECODER_DISASM.mad:134` | `src/FOREX_DECODER_DISASM.mad:328` | 1 |
| `OXC1T` | `4001463146314632` | `src/FOREX_DECODER_DISASM.mad:135` | `src/FOREX_DECODER_DISASM.mad:329` | 1 |
| `OXMSK` | `0360741703607417` | `src/FOREX_DECODER_DISASM.mad:136` | `src/FOREX_DECODER_DISASM.mad:322`, `src/FOREX_DECODER_DISASM.mad:330` | 2 |
| `OXZER` | `2020202020200000` | `src/FOREX_DECODER_DISASM.mad:137` | `src/FOREX_DECODER_DISASM.mad:323`, `src/FOREX_DECODER_DISASM.mad:331` | 2 |
| `ALLMS` | `77777B` | `src/FOREX_RUNTIME.mad:27` | `src/FOREX_RUNTIME.mad:286` | 1 |
| `BS14R` | `14` | `src/FOREX_RUNTIME.mad:28` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `DW0000` | `0000000000077777` | `src/FOREX_RUNTIME.mad:29` | `src/FOREX_RUNTIME.mad:469` | 1 |
| `DW0001` | `00000000 00000000` | `src/FOREX_RUNTIME.mad:30` | `src/FOREX_RUNTIME.mad:301`, `src/FOREX_RUNTIME.mad:302`, `src/FOREX_RUNTIME.mad:303`, `src/FOREX_RUNTIME.mad:305`, `src/FOREX_RUNTIME.mad:308`, `src/FOREX_RUNTIME.mad:309` … (+4) | 10 |
| `DW0002` | `00000000 00000001` | `src/FOREX_RUNTIME.mad:31` | `src/FOREX_RUNTIME.mad:304` | 1 |
| `DW0003` | `00000000 00000002` | `src/FOREX_RUNTIME.mad:32` | `src/FOREX_RUNTIME.mad:313` | 1 |
| `DW0004` | `00000000 00001777` | `src/FOREX_RUNTIME.mad:33` | `src/FOREX_RUNTIME.mad:306` | 1 |
| `DW0005` | `00100000 00000000` | `src/FOREX_RUNTIME.mad:34` | `src/FOREX_RUNTIME.mad:307` | 1 |
| `DW0006` | `17 7777 7777 7777` | `src/FOREX_RUNTIME.mad:35` | `src/FOREX_RUNTIME.mad:512` | 1 |
| `DW0007` | `37777774 77777477` | `src/FOREX_RUNTIME.mad:36` | `src/FOREX_RUNTIME.mad:311` | 1 |
| `DW0008` | `77270707 00000000` | `src/FOREX_RUNTIME.mad:37` | `src/FOREX_RUNTIME.mad:314` | 1 |
| `DTDAYS` | `64+16` | `src/FOREX_RUNTIME.mad:38` | `src/FOREX_RUNTIME.mad:352` | 1 |
| `DTMISH` | `64-24` | `src/FOREX_RUNTIME.mad:39` | `src/FOREX_RUNTIME.mad:366`, `src/FOREX_RUNTIME.mad:506` | 2 |
| `DTMOSH` | `64+35` | `src/FOREX_RUNTIME.mad:40` | `src/FOREX_RUNTIME.mad:356` | 1 |
| `DTTMSH` | `64-22` | `src/FOREX_RUNTIME.mad:41` | `src/FOREX_RUNTIME.mad:373` | 1 |
| `DTYRSH` | `64-14` | `src/FOREX_RUNTIME.mad:42` | `src/FOREX_RUNTIME.mad:368`, `src/FOREX_RUNTIME.mad:394` | 2 |
| `DEC_7` | `7` | `src/FOREX_RUNTIME.mad:43` | `src/FOREX_RUNTIME.mad:200`, `src/FOREX_RUNTIME.mad:212`, `src/FOREX_RUNTIME.mad:224`, `src/FOREX_RUNTIME.mad:252` | 4 |
| `FIXM2` | `2` | `src/FOREX_RUNTIME.mad:44` | `src/FOREX_RUNTIME.mad:509` | 1 |
| `F002DS` | `77776B` | `src/FOREX_RUNTIME.mad:45` | `src/FOREX_RUNTIME.mad:182` | 1 |
| `F003DS` | `77775B` | `src/FOREX_RUNTIME.mad:46` | `src/FOREX_RUNTIME.mad:184` | 1 |
| `F521DS` | `77257B` | `src/FOREX_RUNTIME.mad:47` | `src/FOREX_RUNTIME.mad:176` | 1 |
| `F531DS` | `77247B` | `src/FOREX_RUNTIME.mad:48` | `src/FOREX_RUNTIME.mad:170` | 1 |
| `F541DS` | `77237B` | `src/FOREX_RUNTIME.mad:49` | `src/FOREX_RUNTIME.mad:166` | 1 |
| `F561DS` | `77217B` | `src/FOREX_RUNTIME.mad:50` | `src/FOREX_RUNTIME.mad:172` | 1 |
| `F571DS` | `77207B` | `src/FOREX_RUNTIME.mad:51` | `src/FOREX_RUNTIME.mad:164` | 1 |
| `F611DS` | `77167B` | `src/FOREX_RUNTIME.mad:52` | `src/FOREX_RUNTIME.mad:168` | 1 |
| `F621DS` | `77157B` | `src/FOREX_RUNTIME.mad:53` | `src/FOREX_RUNTIME.mad:174` | 1 |
| `F641DS` | `77137B` | `src/FOREX_RUNTIME.mad:54` | `src/FOREX_RUNTIME.mad:180` | 1 |
| `F721DS` | `77057B` | `src/FOREX_RUNTIME.mad:55` | `src/FOREX_RUNTIME.mad:178` | 1 |
| `FTDTBA` | `77766B` | `src/FOREX_RUNTIME.mad:56` | `src/FOREX_RUNTIME.mad:143` | 1 |
| `FTADFL` | `103B` | `src/FOREX_RUNTIME.mad:57` | `src/FOREX_RUNTIME.mad:136` | 1 |
| `FTOFMK` | `155B` | `src/FOREX_RUNTIME.mad:58` | `src/FOREX_RUNTIME.mad:154` | 1 |
| `GOSTBL` | `6H` | `src/FOREX_RUNTIME.mad:59` | `src/FOREX_RUNTIME.mad:515` | 1 |
| `INTZ` | `0` | `src/FOREX_RUNTIME.mad:60` | `src/FOREX_RUNTIME.mad:470` | 1 |
| `ISOCSH` | `54B` | `src/FOREX_RUNTIME.mad:61` | `src/FOREX_RUNTIME.mad:295` | 1 |
| `ISOWSH` | `64` | `src/FOREX_RUNTIME.mad:62` | `src/FOREX_RUNTIME.mad:365`, `src/FOREX_RUNTIME.mad:495`, `src/FOREX_RUNTIME.mad:497` | 3 |
| `LIBBLN` | `2000B` | `src/FOREX_RUNTIME.mad:63` | `src/FOREX_RUNTIME.mad:194` | 1 |
| `LIT_10` | `10` | `src/FOREX_RUNTIME.mad:64` | `src/FOREX_RUNTIME.mad:460` | 1 |
| `LIT10M` | `10000000 00000000` | `src/FOREX_RUNTIME.mad:65` | `src/FOREX_RUNTIME.mad:186` | 1 |
| `LIT_2` | `2` | `src/FOREX_RUNTIME.mad:66` | `src/FOREX_RUNTIME.mad:450` | 1 |
| `LIT_3` | `3` | `src/FOREX_RUNTIME.mad:67` | `src/FOREX_RUNTIME.mad:447` | 1 |
| `MODE_6` | `6` | `src/FOREX_RUNTIME.mad:68` | `src/FOREX_RUNTIME.mad:345`, `include/FOREX_ROOT.mad:82`, `include/FOREX_ROOT.mad:113`, `include/FOREX_ROOT.mad:126` | 4 |
| `MNTHIB` | `24` | `src/FOREX_RUNTIME.mad:69` | `src/FOREX_RUNTIME.mad:359` | 1 |
| `OCTSDM` | `=777 7777-C` | `src/FOREX_RUNTIME.mad:70` | `src/FOREX_RUNTIME.mad:438` | 1 |
| `ONEW` | `1` | `src/FOREX_RUNTIME.mad:71` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `P5` | `100000.0` | `src/FOREX_RUNTIME.mad:72` | `src/FOREX_RUNTIME.mad:472` | 1 |
| `RMOD3` | `3` | `src/FOREX_RUNTIME.mad:73` | `src/FOREX_RUNTIME.mad:217`, `src/FOREX_RUNTIME.mad:490`, `include/FOREX_ROOT.mad:116` | 3 |
| `RETLR` | `13` | `src/FOREX_RUNTIME.mad:74` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `STKOF1` | `-1` | `src/FOREX_RUNTIME.mad:75` | `src/FOREX_RUNTIME.mad:404` | 1 |
| `STKOF2` | `-2` | `src/FOREX_RUNTIME.mad:76` | `src/FOREX_RUNTIME.mad:350`, `src/FOREX_RUNTIME.mad:505`, `include/FOREX_ROOT.mad:255` | 3 |
| `STKOF3` | `-3` | `src/FOREX_RUNTIME.mad:77` | `src/FOREX_RUNTIME.mad:354`, `src/FOREX_RUNTIME.mad:494`, `src/FOREX_RUNTIME.mad:500` | 3 |
| `STKOF4` | `-4` | `src/FOREX_RUNTIME.mad:78` | `src/FOREX_RUNTIME.mad:367`, `src/FOREX_RUNTIME.mad:372`, `src/FOREX_RUNTIME.mad:498` | 3 |
| `STKOF5` | `-5` | `src/FOREX_RUNTIME.mad:79` | `src/FOREX_RUNTIME.mad:403`, `src/FOREX_RUNTIME.mad:441` | 2 |
| `STKOF6` | `-6` | `src/FOREX_RUNTIME.mad:80` | `src/FOREX_RUNTIME.mad:384` | 1 |
| `SOM` | `-8` | `src/FOREX_RUNTIME.mad:81` | `src/FOREX_RUNTIME.mad:377` | 1 |
| `TL0000` | `''000000''` | `src/FOREX_RUNTIME.mad:82` | `src/FOREX_RUNTIME.mad:478` | 1 |
| `TL0001` | `1H'055'` | `src/FOREX_RUNTIME.mad:83` | `src/FOREX_RUNTIME.mad:409` | 1 |
| `TL0002` | `2H '200'` | `src/FOREX_RUNTIME.mad:84` | `src/FOREX_RUNTIME.mad:407` | 1 |
| `TL0003` | `3H00` | `src/FOREX_RUNTIME.mad:85` | `src/FOREX_RUNTIME.mad:410` | 1 |
| `TL0004` | `=6H00` | `src/FOREX_RUNTIME.mad:86` | `src/FOREX_RUNTIME.mad:396` | 1 |
| `TL0005` | `6H0000` | `src/FOREX_RUNTIME.mad:87` | — | 0 |
| `TL0006` | `6H000000` | `src/FOREX_RUNTIME.mad:88` | `src/FOREX_RUNTIME.mad:516` | 1 |
| `TL0007` | `6H000 00` | `src/FOREX_RUNTIME.mad:89` | `src/FOREX_RUNTIME.mad:411` | 1 |
| `TL0008` | `=6H00/00/` | `src/FOREX_RUNTIME.mad:90` | `src/FOREX_RUNTIME.mad:399` | 1 |
| `TL0009` | `6H03 0` | `src/FOREX_RUNTIME.mad:91` | — | 0 |
| `TL0010` | `6HABГCEH` | `src/FOREX_RUNTIME.mad:92` | `src/FOREX_RUNTIME.mad:417` | 1 |
| `TL0011` | `6HARRAY` | `src/FOREX_RUNTIME.mad:93` | `src/FOREX_RUNTIME.mad:321` | 1 |
| `TL0012` | `6HAПPMAЯ` | `src/FOREX_RUNTIME.mad:94` | `src/FOREX_RUNTIME.mad:415` | 1 |
| `TL0013` | `6HERROR` | `src/FOREX_RUNTIME.mad:95` | `src/FOREX_RUNTIME.mad:318` | 1 |
| `TL0014` | `6HIN STA` | `src/FOREX_RUNTIME.mad:96` | `src/FOREX_RUNTIME.mad:319` | 1 |
| `TL0015` | `6HNDART` | `src/FOREX_RUNTIME.mad:97` | `src/FOREX_RUNTIME.mad:320` | 1 |
| `TL0016` | `6HOKTHOЯ` | `src/FOREX_RUNTIME.mad:98` | `src/FOREX_RUNTIME.mad:422` | 1 |
| `TL0017` | `6H 00.00` | `src/FOREX_RUNTIME.mad:99` | `src/FOREX_RUNTIME.mad:418` | 1 |
| `TL0018` | `=6H'17''17'''''''''` | `src/FOREX_RUNTIME.mad:100` | `src/FOREX_RUNTIME.mad:395` | 1 |
| `TL0019` | `6H'201'  '200'7` | `src/FOREX_RUNTIME.mad:101` | `src/FOREX_RUNTIME.mad:406` | 1 |
| `TL0020` | `6H'231'  ЯHB` | `src/FOREX_RUNTIME.mad:102` | — | 0 |
| `TL0021` | `=6H'3''17''''17''17'''` | `src/FOREX_RUNTIME.mad:103` | `src/FOREX_RUNTIME.mad:398` | 1 |
| `TL0022` | `6HФEBMAP` | `src/FOREX_RUNTIME.mad:104` | `src/FOREX_RUNTIME.mad:414` | 1 |
| `TL0023` | `6HДEK` | `src/FOREX_RUNTIME.mad:105` | `src/FOREX_RUNTIME.mad:423` | 1 |
| `TL0024` | `6HИЮHИЮЛ` | `src/FOREX_RUNTIME.mad:106` | `src/FOREX_RUNTIME.mad:416` | 1 |
| `FUNDTM` | `67B` | `src/FOREX_RUNTIME.mad:107` | `src/FOREX_RUNTIME.mad:344` | 1 |
| `DBFLN` | `2` | `src/FOREX_RUNTIME.mad:108` | `src/FOREX_RUNTIME.mad:330` | 1 |
| `MNTHFO` | `00 776` | `src/FOREX_RUNTIME.mad:109` | — | 0 |
| `OCTISS` | `64-8` | `src/FOREX_RUNTIME.mad:110` | `src/FOREX_RUNTIME.mad:463` | 1 |
| `P4` | `10000.0` | `src/FOREX_RUNTIME.mad:111` | `src/FOREX_RUNTIME.mad:473` | 1 |
| `P3` | `1000.0` | `src/FOREX_RUNTIME.mad:112` | `src/FOREX_RUNTIME.mad:474` | 1 |
| `P2` | `100.0` | `src/FOREX_RUNTIME.mad:113` | `src/FOREX_RUNTIME.mad:475` | 1 |
| `P1` | `10.0` | `src/FOREX_RUNTIME.mad:114` | `src/FOREX_RUNTIME.mad:476` | 1 |
| `BAS14` | `14` | `src/FOREX_RUNTIME_DISASM.mad:30` | `src/FOREX_RUNTIME_DISASM.mad:144`, `src/FOREX_RUNTIME_DISASM.mad:153`, `src/FOREX_RUNTIME_DISASM.mad:164`, `src/FOREX_RUNTIME_DISASM.mad:280`, `src/FOREX_RUNTIME_DISASM.mad:289`, `src/FOREX_RUNTIME_DISASM.mad:291` … (+1) | 7 |
| `LNK13` | `13` | `src/FOREX_RUNTIME_DISASM.mad:31` | `src/FOREX_RUNTIME_DISASM.mad:275`, `src/FOREX_RUNTIME_DISASM.mad:284` | 2 |
| `WRK07` | `7` | `src/FOREX_RUNTIME_DISASM.mad:32` | `src/FOREX_RUNTIME_DISASM.mad:274`, `src/FOREX_RUNTIME_DISASM.mad:285`, `src/FOREX_RUNTIME_DISASM.mad:296`, `src/FOREX_RUNTIME_DISASM.mad:322` | 4 |
| `FTADR` | `103B` | `src/FOREX_RUNTIME_DISASM.mad:34` | `src/FOREX_RUNTIME_DISASM.mad:146` | 1 |
| `FTOFSM` | `155B` | `src/FOREX_RUNTIME_DISASM.mad:35` | `src/FOREX_RUNTIME_DISASM.mad:161` | 1 |
| `FTBTAB` | `77766B` | `src/FOREX_RUNTIME_DISASM.mad:36` | `src/FOREX_RUNTIME_DISASM.mad:152` | 1 |
| `FTLOG` | `10000000 00000000` | `src/FOREX_RUNTIME_DISASM.mad:37` | `src/FOREX_RUNTIME_DISASM.mad:148`, `src/FOREX_RUNTIME_DISASM.mad:159` | 2 |
| `D571DS` | `77207B` | `src/FOREX_RUNTIME_DISASM.mad:39` | `src/FOREX_RUNTIME_DISASM.mad:168` | 1 |
| `D541DS` | `77237B` | `src/FOREX_RUNTIME_DISASM.mad:40` | `src/FOREX_RUNTIME_DISASM.mad:170` | 1 |
| `D611DS` | `77167B` | `src/FOREX_RUNTIME_DISASM.mad:41` | `src/FOREX_RUNTIME_DISASM.mad:172` | 1 |
| `D531DS` | `77247B` | `src/FOREX_RUNTIME_DISASM.mad:42` | `src/FOREX_RUNTIME_DISASM.mad:174` | 1 |
| `D561DS` | `77217B` | `src/FOREX_RUNTIME_DISASM.mad:43` | `src/FOREX_RUNTIME_DISASM.mad:176` | 1 |
| `D621DS` | `77157B` | `src/FOREX_RUNTIME_DISASM.mad:44` | `src/FOREX_RUNTIME_DISASM.mad:178` | 1 |
| `D521DS` | `77257B` | `src/FOREX_RUNTIME_DISASM.mad:45` | `src/FOREX_RUNTIME_DISASM.mad:180` | 1 |
| `D721DS` | `77057B` | `src/FOREX_RUNTIME_DISASM.mad:46` | `src/FOREX_RUNTIME_DISASM.mad:182` | 1 |
| `D641DS` | `77137B` | `src/FOREX_RUNTIME_DISASM.mad:47` | `src/FOREX_RUNTIME_DISASM.mad:184` | 1 |
| `D002DS` | `77776B` | `src/FOREX_RUNTIME_DISASM.mad:48` | `src/FOREX_RUNTIME_DISASM.mad:186` | 1 |
| `D003DS` | `77775B` | `src/FOREX_RUNTIME_DISASM.mad:49` | `src/FOREX_RUNTIME_DISASM.mad:188` | 1 |
| `X01` | `74001B` | `src/FOREX_RUNTIME_DISASM.mad:51` | `src/FOREX_RUNTIME_DISASM.mad:167`, `src/FOREX_RUNTIME_DISASM.mad:299` | 2 |
| `X02` | `74002B` | `src/FOREX_RUNTIME_DISASM.mad:52` | `src/FOREX_RUNTIME_DISASM.mad:169` | 1 |
| `X03` | `74003B` | `src/FOREX_RUNTIME_DISASM.mad:53` | `src/FOREX_RUNTIME_DISASM.mad:171` | 1 |
| `X04` | `74004B` | `src/FOREX_RUNTIME_DISASM.mad:54` | `src/FOREX_RUNTIME_DISASM.mad:173` | 1 |
| `X05` | `74005B` | `src/FOREX_RUNTIME_DISASM.mad:55` | `src/FOREX_RUNTIME_DISASM.mad:175` | 1 |
| `X06` | `74006B` | `src/FOREX_RUNTIME_DISASM.mad:56` | `src/FOREX_RUNTIME_DISASM.mad:177` | 1 |
| `X07` | `74007B` | `src/FOREX_RUNTIME_DISASM.mad:57` | `src/FOREX_RUNTIME_DISASM.mad:179` | 1 |
| `X10` | `74010B` | `src/FOREX_RUNTIME_DISASM.mad:58` | `src/FOREX_RUNTIME_DISASM.mad:181` | 1 |
| `X11` | `74011B` | `src/FOREX_RUNTIME_DISASM.mad:59` | `src/FOREX_RUNTIME_DISASM.mad:183` | 1 |
| `X12` | `74012B` | `src/FOREX_RUNTIME_DISASM.mad:60` | `src/FOREX_RUNTIME_DISASM.mad:185` | 1 |
| `X13` | `74013B` | `src/FOREX_RUNTIME_DISASM.mad:61` | `src/FOREX_RUNTIME_DISASM.mad:187` | 1 |
| `ZERO` | `0` | `src/FOREX_RUNTIME_DISASM.mad:63` | `src/FOREX_RUNTIME.mad:459`, `src/FOREX_RUNTIME.mad:508`, `src/FOREX_RUNTIME_DISASM.mad:371`, `src/FOREX_RUNTIME_DISASM.mad:372`, `src/FOREX_RUNTIME_DISASM.mad:373`, `src/FOREX_RUNTIME_DISASM.mad:375` … (+6) | 12 |
| `ONE` | `1` | `src/FOREX_RUNTIME_DISASM.mad:64` | `src/FOREX_RUNTIME_DISASM.mad:325`, `src/FOREX_RUNTIME_DISASM.mad:333`, `src/FOREX_RUNTIME_DISASM.mad:374` | 3 |
| `TWO` | `2` | `src/FOREX_RUNTIME_DISASM.mad:65` | `src/FOREX_RUNTIME_DISASM.mad:383` | 1 |
| `TRIO` | `3` | `src/FOREX_RUNTIME_DISASM.mad:66` | `src/FOREX_RUNTIME_DISASM.mad:290` | 1 |
| `SEVEN` | `7` | `src/FOREX_RUNTIME_DISASM.mad:67` | — | 0 |
| `M1777` | `1777B` | `src/FOREX_RUNTIME_DISASM.mad:68` | `src/FOREX_RUNTIME_DISASM.mad:376` | 1 |
| `ISOHI` | `10000000 00000000` | `src/FOREX_RUNTIME_DISASM.mad:69` | `src/FOREX_RUNTIME_DISASM.mad:377` | 1 |
| `MSK73` | `37777774 77777477` | `src/FOREX_RUNTIME_DISASM.mad:70` | `src/FOREX_RUNTIME_DISASM.mad:381` | 1 |
| `MSK76` | `77270707 00000000` | `src/FOREX_RUNTIME_DISASM.mad:71` | `src/FOREX_RUNTIME_DISASM.mad:384` | 1 |
| `ISOSHF` | `54B` | `src/FOREX_RUNTIME_DISASM.mad:72` | `src/FOREX_RUNTIME_DISASM.mad:364` | 1 |
| `ALL1` | `77777B` | `src/FOREX_RUNTIME_DISASM.mad:73` | `src/FOREX_RUNTIME_DISASM.mad:356` | 1 |
| `LIBBUF` | `2000B` | `src/FOREX_RUNTIME_DISASM.mad:74` | — | 0 |
| `LIBISO` | `C101` | `src/FOREX_RUNTIME_DISASM.mad:388` | — | 0 |
| `F541AD` | `77237B` | `src/LO_GEN.mad:44` | `src/LO_GEN.mad:3557`, `src/LO_GEN.mad:3561` | 2 |
| `F721AD` | `77057B` | `src/LO_GEN.mad:45` | `src/LO_GEN.mad:3224` | 1 |
| `AC0001` | `1B` | `src/LO_GEN.mad:46` | `src/LO_GEN.mad:694`, `src/LO_GEN.mad:697`, `src/LO_GEN.mad:703`, `src/LO_GEN.mad:706`, `src/LO_GEN.mad:789`, `src/LO_GEN.mad:792` … (+59) | 65 |
| `AC0010` | `10B` | `src/LO_GEN.mad:47` | `src/LO_GEN.mad:804`, `src/LO_GEN.mad:834`, `src/LO_GEN.mad:3020`, `src/LO_GEN.mad:3374`, `src/LO_GEN.mad:3465` | 5 |
| `AC0100` | `100B` | `src/LO_GEN.mad:48` | `src/LO_GEN.mad:638`, `src/LO_GEN.mad:673`, `src/LO_GEN.mad:3344` | 3 |
| `AC0101` | `101B` | `src/LO_GEN.mad:49` | `src/LO_GEN.mad:3347`, `src/LO_GEN.mad:3381` | 2 |
| `AC1010` | `1010B` | `src/LO_GEN.mad:50` | `src/LO_GEN.mad:1407` | 1 |
| `AC1017` | `1017B` | `src/LO_GEN.mad:51` | `src/LO_GEN.mad:1374` | 1 |
| `AC0102` | `102B` | `src/LO_GEN.mad:52` | `src/LO_GEN.mad:3356` | 1 |
| `AC1021` | `1021B` | `src/LO_GEN.mad:53` | `src/LO_GEN.mad:1377` | 1 |
| `AC0103` | `103B` | `src/LO_GEN.mad:54` | `src/LO_GEN.mad:3359` | 1 |
| `AC1031` | `1031B` | `src/LO_GEN.mad:55` | `src/LO_GEN.mad:1422` | 1 |
| `AC1035` | `1035B` | `src/LO_GEN.mad:56` | `src/LO_GEN.mad:1431` | 1 |
| `AC0104` | `104B` | `src/LO_GEN.mad:57` | `src/LO_GEN.mad:3362` | 1 |
| `AC1044` | `1044B` | `src/LO_GEN.mad:58` | `src/LO_GEN.mad:1425` | 1 |
| `AC0105` | `105B` | `src/LO_GEN.mad:59` | `src/LO_GEN.mad:3366` | 1 |
| `AC0011` | `11B` | `src/LO_GEN.mad:60` | `src/LO_GEN.mad:626`, `src/LO_GEN.mad:807`, `src/LO_GEN.mad:840`, `src/LO_GEN.mad:1167`, `src/LO_GEN.mad:1993`, `src/LO_GEN.mad:2842` … (+2) | 8 |
| `AC0117` | `117B` | `src/LO_GEN.mad:61` | — | 0 |
| `AC0012` | `12B` | `src/LO_GEN.mad:62` | `src/LO_GEN.mad:684`, `src/LO_GEN.mad:823`, `src/LO_GEN.mad:3384` | 3 |
| `AC1210` | `1210B` | `src/LO_GEN.mad:63` | `src/LO_GEN.mad:1476` | 1 |
| `AC0127` | `127B` | `src/LO_GEN.mad:64` | `src/LO_GEN.mad:2410` | 1 |
| `AC0013` | `13B` | `src/LO_GEN.mad:65` | `src/LO_GEN.mad:826`, `src/LO_GEN.mad:831`, `src/LO_GEN.mad:835`, `src/LO_GEN.mad:1012`, `src/LO_GEN.mad:1059`, `src/LO_GEN.mad:1080` … (+21) | 27 |
| `AC0132` | `132B` | `src/LO_GEN.mad:66` | `src/LO_GEN.mad:2484`, `src/LO_GEN.mad:2493`, `src/LO_GEN.mad:2508`, `src/LO_GEN.mad:2517`, `src/LO_GEN.mad:2544`, `src/LO_GEN.mad:2553` … (+3) | 9 |
| `AC1322` | `1322B` | `src/LO_GEN.mad:67` | `src/LO_GEN.mad:1290` | 1 |
| `AC1324` | `1324B` | `src/LO_GEN.mad:68` | `src/LO_GEN.mad:1293` | 1 |
| `AC1326` | `1326B` | `src/LO_GEN.mad:69` | `src/LO_GEN.mad:1296` | 1 |
| `AC0133` | `133B` | `src/LO_GEN.mad:70` | `src/LO_GEN.mad:693`, `src/LO_GEN.mad:1201` | 2 |
| `AC1330` | `1330B` | `src/LO_GEN.mad:71` | `src/LO_GEN.mad:1302` | 1 |
| `AC1332` | `1332B` | `src/LO_GEN.mad:72` | `src/LO_GEN.mad:1305` | 1 |
| `AC1334` | `1334B` | `src/LO_GEN.mad:73` | `src/LO_GEN.mad:1314` | 1 |
| `AC1336` | `1336B` | `src/LO_GEN.mad:74` | `src/LO_GEN.mad:1434` | 1 |
| `AC0134` | `134B` | `src/LO_GEN.mad:75` | `src/LO_GEN.mad:1821`, `src/LO_GEN.mad:1840`, `src/LO_GEN.mad:1848`, `src/LO_GEN.mad:1866`, `src/LO_GEN.mad:2230`, `src/LO_GEN.mad:2272` … (+6) | 12 |
| `AC1343` | `1343B` | `src/LO_GEN.mad:76` | `src/LO_GEN.mad:1329` | 1 |
| `AC1347` | `1347B` | `src/LO_GEN.mad:77` | `src/LO_GEN.mad:1299` | 1 |
| `AC0135` | `135B` | `src/LO_GEN.mad:78` | `src/LO_GEN.mad:2862`, `src/LO_GEN.mad:2869` | 2 |
| `AC1351` | `1351B` | `src/LO_GEN.mad:79` | `src/LO_GEN.mad:1512`, `src/LO_GEN.mad:1518` | 2 |
| `AC1355` | `1355B` | `src/LO_GEN.mad:80` | `src/LO_GEN.mad:1536` | 1 |
| `AC0136` | `136B` | `src/LO_GEN.mad:81` | `src/LO_GEN.mad:901`, `src/LO_GEN.mad:1710`, `src/LO_GEN.mad:1771`, `src/LO_GEN.mad:1783`, `src/LO_GEN.mad:1804`, `src/LO_GEN.mad:2032` … (+5) | 11 |
| `AC1360` | `1360B` | `src/LO_GEN.mad:82` | `src/LO_GEN.mad:1509`, `src/LO_GEN.mad:1515` | 2 |
| `AC1362` | `1362B` | `src/LO_GEN.mad:83` | `src/LO_GEN.mad:1524`, `src/LO_GEN.mad:1533` | 2 |
| `AC0137` | `137B` | `src/LO_GEN.mad:84` | `src/LO_GEN.mad:1924`, `src/LO_GEN.mad:1929`, `src/LO_GEN.mad:2380`, `src/LO_GEN.mad:3422` | 4 |
| `AC1374` | `1374B` | `src/LO_GEN.mad:85` | `src/LO_GEN.mad:1539` | 1 |
| `AC0014` | `14B` | `src/LO_GEN.mad:86` | `src/LO_GEN.mad:850`, `src/LO_GEN.mad:882`, `src/LO_GEN.mad:910`, `src/LO_GEN.mad:925`, `src/LO_GEN.mad:973`, `src/LO_GEN.mad:1129` … (+7) | 13 |
| `AC0140` | `140B` | `src/LO_GEN.mad:87` | `src/LO_GEN.mad:2722`, `src/LO_GEN.mad:2748`, `src/LO_GEN.mad:2893`, `src/LO_GEN.mad:3471` | 4 |
| `AC0141` | `141B` | `src/LO_GEN.mad:88` | `src/LO_GEN.mad:708`, `src/LO_GEN.mad:1128`, `src/LO_GEN.mad:1158`, `src/LO_GEN.mad:1737`, `src/LO_GEN.mad:1824`, `src/LO_GEN.mad:1828` … (+11) | 17 |
| `AC0142` | `142B` | `src/LO_GEN.mad:89` | `src/LO_GEN.mad:2535`, `src/LO_GEN.mad:3245`, `src/LO_GEN.mad:3264`, `src/LO_GEN.mad:3267`, `src/LO_GEN.mad:3269`, `src/LO_GEN.mad:3426` | 6 |
| `AC0143` | `143B` | `src/LO_GEN.mad:90` | `src/LO_GEN.mad:1731`, `src/LO_GEN.mad:2035`, `src/LO_GEN.mad:2191`, `src/LO_GEN.mad:2206`, `src/LO_GEN.mad:2208` | 5 |
| `AC1437` | `1437B` | `src/LO_GEN.mad:91` | `src/LO_GEN.mad:1542` | 1 |
| `AC0015` | `15B` | `src/LO_GEN.mad:92` | `src/LO_GEN.mad:595`, `src/LO_GEN.mad:855` | 2 |
| `AC0151` | `151B` | `src/LO_GEN.mad:93` | `src/LO_GEN.mad:934` | 1 |
| `AC0153` | `153B` | `src/LO_GEN.mad:94` | `src/LO_GEN.mad:880`, `src/LO_GEN.mad:1039`, `src/LO_GEN.mad:1186` | 3 |
| `AC1543` | `1543B` | `src/LO_GEN.mad:95` | `src/LO_GEN.mad:1527` | 1 |
| `AC0016` | `16B` | `src/LO_GEN.mad:96` | `src/LO_GEN.mad:572`, `src/LO_GEN.mad:856`, `src/LO_GEN.mad:3402`, `src/LO_GEN.mad:3429`, `src/LO_GEN.mad:3516` | 5 |
| `AC1641` | `1641B` | `src/LO_GEN.mad:97` | `src/LO_GEN.mad:682` | 1 |
| `AC1647` | `1647B` | `src/LO_GEN.mad:98` | `src/LO_GEN.mad:590` | 1 |
| `AC0017` | `17B` | `src/LO_GEN.mad:99` | `src/LO_GEN.mad:571`, `src/LO_GEN.mad:584`, `src/LO_GEN.mad:868` | 3 |
| `AC0176` | `176B` | `src/LO_GEN.mad:100` | `src/LO_GEN.mad:1521`, `src/LO_GEN.mad:1530` | 2 |
| `AC0002` | `2B` | `src/LO_GEN.mad:101` | `src/LO_GEN.mad:611`, `src/LO_GEN.mad:712`, `src/LO_GEN.mad:1120`, `src/LO_GEN.mad:2412`, `src/LO_GEN.mad:3053`, `src/LO_GEN.mad:3135` | 6 |
| `AC0020` | `20B` | `src/LO_GEN.mad:102` | `src/LO_GEN.mad:568`, `src/LO_GEN.mad:870` | 2 |
| `AC0021` | `21B` | `src/LO_GEN.mad:103` | `src/LO_GEN.mad:574`, `src/LO_GEN.mad:587`, `src/LO_GEN.mad:874`, `src/LO_GEN.mad:3177` | 4 |
| `AC0211` | `211B` | `src/LO_GEN.mad:104` | `src/LO_GEN.mad:560` | 1 |
| `AC0022` | `22B` | `src/LO_GEN.mad:105` | `src/LO_GEN.mad:886`, `src/LO_GEN.mad:2166` | 2 |
| `AC2200` | `2200B` | `src/LO_GEN.mad:106` | — | 0 |
| `AC2254` | `2254B` | `src/LO_GEN.mad:107` | `src/LO_GEN.mad:1362` | 1 |
| `AC0HHI` | `22662B` | `src/LO_GEN.mad:108` | `src/LO_GEN.mad:661` | 1 |
| `AC0023` | `23B` | `src/LO_GEN.mad:109` | `src/LO_GEN.mad:915`, `src/LO_GEN.mad:3011`, `src/LO_GEN.mad:3036` | 3 |
| `AC0024` | `24B` | `src/LO_GEN.mad:110` | `src/LO_GEN.mad:930`, `src/LO_GEN.mad:952`, `src/LO_GEN.mad:964`, `src/LO_GEN.mad:1066`, `src/LO_GEN.mad:1152`, `src/LO_GEN.mad:1708` … (+34) | 40 |
| `AC0025` | `25B` | `src/LO_GEN.mad:111` | `src/LO_GEN.mad:936` | 1 |
| `AC0026` | `26B` | `src/LO_GEN.mad:112` | `src/LO_GEN.mad:958`, `src/LO_GEN.mad:1086`, `src/LO_GEN.mad:1200`, `src/LO_GEN.mad:1773`, `src/LO_GEN.mad:1782`, `src/LO_GEN.mad:1857` … (+11) | 17 |
| `AC0027` | `27B` | `src/LO_GEN.mad:113` | `src/LO_GEN.mad:1009`, `src/LO_GEN.mad:1837`, `src/LO_GEN.mad:1894`, `src/LO_GEN.mad:2356`, `src/LO_GEN.mad:3539`, `src/LO_GEN.mad:3542` | 6 |
| `AC0003` | `3B` | `src/LO_GEN.mad:114` | `src/LO_GEN.mad:620`, `src/LO_GEN.mad:715`, `src/LO_GEN.mad:3059` | 3 |
| `AC0030` | `30B` | `src/LO_GEN.mad:115` | `src/LO_GEN.mad:1029`, `src/LO_GEN.mad:1116`, `src/LO_GEN.mad:2170`, `src/LO_GEN.mad:2460`, `src/LO_GEN.mad:2485`, `src/LO_GEN.mad:2509` … (+7) | 13 |
| `AC0NCY` | `30274B` | `src/LO_GEN.mad:116` | `src/LO_GEN.mad:565`, `src/LO_GEN.mad:583` | 2 |
| `AC0NE0` | `30312B` | `src/LO_GEN.mad:117` | `src/LO_GEN.mad:578` | 1 |
| `AC0NE2` | `30314B` | `src/LO_GEN.mad:118` | — | 0 |
| `AC0031` | `31B` | `src/LO_GEN.mad:119` | `src/LO_GEN.mad:1053`, `src/LO_GEN.mad:1203`, `src/LO_GEN.mad:2569`, `src/LO_GEN.mad:2697` | 4 |
| `AC0032` | `32B` | `src/LO_GEN.mad:120` | `src/LO_GEN.mad:1102`, `src/LO_GEN.mad:1944`, `src/LO_GEN.mad:2058`, `src/LO_GEN.mad:2103`, `src/LO_GEN.mad:2625`, `src/LO_GEN.mad:2673` … (+5) | 11 |
| `AC0033` | `33B` | `src/LO_GEN.mad:121` | `src/LO_GEN.mad:1110`, `src/LO_GEN.mad:2830` | 2 |
| `AC0034` | `34B` | `src/LO_GEN.mad:122` | `src/LO_GEN.mad:1111`, `src/LO_GEN.mad:2832` | 2 |
| `AC0035` | `35B` | `src/LO_GEN.mad:123` | `src/LO_GEN.mad:1134`, `src/LO_GEN.mad:1258`, `src/LO_GEN.mad:2494`, `src/LO_GEN.mad:2518`, `src/LO_GEN.mad:2554`, `src/LO_GEN.mad:2667` … (+1) | 7 |
| `AC0036` | `36B` | `src/LO_GEN.mad:124` | `src/LO_GEN.mad:1231`, `src/LO_GEN.mad:2981` | 2 |
| `AC0037` | `37B` | `src/LO_GEN.mad:125` | `src/LO_GEN.mad:1236`, `src/LO_GEN.mad:1968` | 2 |
| `AC0370` | `370B` | `src/LO_GEN.mad:126` | `src/LO_GEN.mad:614` | 1 |
| `AC0004` | `4B` | `src/LO_GEN.mad:127` | `src/LO_GEN.mad:721` | 1 |
| `AC0040` | `40B` | `src/LO_GEN.mad:128` | `src/LO_GEN.mad:1275` | 1 |
| `AC0400` | `400B` | `src/LO_GEN.mad:129` | — | 0 |
| `AC0V1F` | `40227B` | `src/LO_GEN.mad:130` | `src/LO_GEN.mad:744` | 1 |
| `AC0V5L` | `40377B` | `src/LO_GEN.mad:131` | `src/LO_GEN.mad:1182` | 1 |
| `AC0V69` | `40401B` | `src/LO_GEN.mad:132` | `src/LO_GEN.mad:1191` | 1 |
| `AC0V6B` | `40403B` | `src/LO_GEN.mad:133` | `src/LO_GEN.mad:1227` | 1 |
| `AC0V6D` | `40405B` | `src/LO_GEN.mad:134` | `src/LO_GEN.mad:1266` | 1 |
| `AC0V6F` | `40407B` | `src/LO_GEN.mad:135` | `src/LO_GEN.mad:1439` | 1 |
| `AC0V6J` | `40411B` | `src/LO_GEN.mad:136` | `src/LO_GEN.mad:2488`, `src/LO_GEN.mad:2548` | 2 |
| `AC0V6P` | `40417B` | `src/LO_GEN.mad:137` | `src/LO_GEN.mad:2512` | 1 |
| `AC0V6T` | `40421B` | `src/LO_GEN.mad:138` | `src/LO_GEN.mad:1436` | 1 |
| `AC0V6V` | `40423B` | `src/LO_GEN.mad:139` | `src/LO_GEN.mad:1499` | 1 |
| `AC0V6X` | `40425B` | `src/LO_GEN.mad:140` | `src/LO_GEN.mad:2502`, `src/LO_GEN.mad:2562` | 2 |
| `AC0V75` | `40433B` | `src/LO_GEN.mad:141` | `src/LO_GEN.mad:2526` | 1 |
| `AC0V77` | `40435B` | `src/LO_GEN.mad:142` | `src/LO_GEN.mad:1496` | 1 |
| `AC0V79` | `40437B` | `src/LO_GEN.mad:143` | `src/LO_GEN.mad:2497`, `src/LO_GEN.mad:2557` | 2 |
| `AC0V7H` | `40445B` | `src/LO_GEN.mad:144` | `src/LO_GEN.mad:2521` | 1 |
| `AC0V7J` | `40447B` | `src/LO_GEN.mad:145` | `src/LO_GEN.mad:1457` | 1 |
| `AC0V7N` | `40451B` | `src/LO_GEN.mad:146` | `src/LO_GEN.mad:1454` | 1 |
| `AC0V7P` | `40453B` | `src/LO_GEN.mad:147` | `src/LO_GEN.mad:1451` | 1 |
| `AC0V7R` | `40455B` | `src/LO_GEN.mad:148` | `src/LO_GEN.mad:1493` | 1 |
| `AC0V7T` | `40457B` | `src/LO_GEN.mad:149` | `src/LO_GEN.mad:1490` | 1 |
| `AC0V7X` | `40461B` | `src/LO_GEN.mad:150` | `src/LO_GEN.mad:1442` | 1 |
| `AC0V7Z` | `40463B` | `src/LO_GEN.mad:151` | `src/LO_GEN.mad:1445` | 1 |
| `AC0V81` | `40465B` | `src/LO_GEN.mad:152` | `src/LO_GEN.mad:1448` | 1 |
| `AC0V83` | `40467B` | `src/LO_GEN.mad:153` | `src/LO_GEN.mad:1460` | 1 |
| `AC0041` | `41B` | `src/LO_GEN.mad:154` | `src/LO_GEN.mad:1337` | 1 |
| `AC4114` | `4114B` | `src/LO_GEN.mad:155` | `src/LO_GEN.mad:632`, `src/LO_GEN.mad:667` | 2 |
| `AC0042` | `42B` | `src/LO_GEN.mad:156` | `src/LO_GEN.mad:1340` | 1 |
| `AC0WQ5` | `42413B` | `src/LO_GEN.mad:157` | `src/LO_GEN.mad:619`, `src/LO_GEN.mad:690`, `src/LO_GEN.mad:3506` | 3 |
| `AC0WTZ` | `42551B` | `src/LO_GEN.mad:158` | `src/LO_GEN.mad:1764`, `src/LO_GEN.mad:1797`, `src/LO_GEN.mad:2073` | 3 |
| `AC0WU4` | `42556B` | `src/LO_GEN.mad:159` | `src/LO_GEN.mad:2037`, `src/LO_GEN.mad:2193` | 2 |
| `AC0043` | `43B` | `src/LO_GEN.mad:160` | `src/LO_GEN.mad:1343`, `src/LO_GEN.mad:3216` | 2 |
| `AC0044` | `44B` | `src/LO_GEN.mad:161` | `src/LO_GEN.mad:1346`, `src/LO_GEN.mad:2022`, `src/LO_GEN.mad:3275` | 3 |
| `AC0045` | `45B` | `src/LO_GEN.mad:162` | `src/LO_GEN.mad:1758`, `src/LO_GEN.mad:2137`, `src/LO_GEN.mad:2313`, `src/LO_GEN.mad:2806`, `src/LO_GEN.mad:3326` | 5 |
| `AC0046` | `46B` | `src/LO_GEN.mad:163` | `src/LO_GEN.mad:1947`, `src/LO_GEN.mad:2061`, `src/LO_GEN.mad:2106`, `src/LO_GEN.mad:2628`, `src/LO_GEN.mad:2790`, `src/LO_GEN.mad:2817` … (+3) | 9 |
| `AC0ZLA` | `46126B` | `src/LO_GEN.mad:164` | `src/LO_GEN.mad:634` | 1 |
| `AC0047` | `47B` | `src/LO_GEN.mad:165` | `src/LO_GEN.mad:1986` | 1 |
| `AC0471` | `471B` | `src/LO_GEN.mad:166` | `src/LO_GEN.mad:1395` | 1 |
| `AC10UH` | `47753B` | `src/LO_GEN.mad:167` | `src/LO_GEN.mad:575` | 1 |
| `AC0005` | `5B` | `src/LO_GEN.mad:168` | `src/LO_GEN.mad:646`, `src/LO_GEN.mad:652`, `src/LO_GEN.mad:726`, `src/LO_GEN.mad:808`, `src/LO_GEN.mad:978`, `src/LO_GEN.mad:1018` … (+21) | 27 |
| `AC0050` | `50B` | `src/LO_GEN.mad:169` | `src/LO_GEN.mad:2007`, `src/LO_GEN.mad:2143`, `src/LO_GEN.mad:3233` | 3 |
| `AC12ZC` | `50520B` | `src/LO_GEN.mad:170` | `src/LO_GEN.mad:660` | 1 |
| `AC12ZM` | `50530B` | `src/LO_GEN.mad:171` | `src/LO_GEN.mad:635`, `src/LO_GEN.mad:670` | 2 |
| `AC0051` | `51B` | `src/LO_GEN.mad:172` | `src/LO_GEN.mad:2010`, `src/LO_GEN.mad:2125`, `src/LO_GEN.mad:2598`, `src/LO_GEN.mad:2638`, `src/LO_GEN.mad:2641`, `src/LO_GEN.mad:2904` … (+8) | 14 |
| `AC0052` | `52B` | `src/LO_GEN.mad:173` | `src/LO_GEN.mad:2019` | 1 |
| `AC147P` | `52117B` | `src/LO_GEN.mad:174` | `src/LO_GEN.mad:655` | 1 |
| `AC0523` | `523B` | `src/LO_GEN.mad:175` | `src/LO_GEN.mad:593` | 1 |
| `AC14IQ` | `52514B` | `src/LO_GEN.mad:176` | `src/LO_GEN.mad:669` | 1 |
| `AC5257` | `5257B` | `src/LO_GEN.mad:177` | `src/LO_GEN.mad:663` | 1 |
| `AC0053` | `53B` | `src/LO_GEN.mad:178` | `src/LO_GEN.mad:2115`, `src/LO_GEN.mad:2146` | 2 |
| `AC153D` | `53257B` | `src/LO_GEN.mad:179` | `src/LO_GEN.mad:631` | 1 |
| `AC5377` | `5377B` | `src/LO_GEN.mad:180` | `src/LO_GEN.mad:557` | 1 |
| `AC0054` | `54B` | `src/LO_GEN.mad:181` | `src/LO_GEN.mad:2122` | 1 |
| `AC0055` | `55B` | `src/LO_GEN.mad:182` | `src/LO_GEN.mad:2181`, `src/LO_GEN.mad:2212`, `src/LO_GEN.mad:2281` | 3 |
| `AC0056` | `56B` | `src/LO_GEN.mad:183` | `src/LO_GEN.mad:2184`, `src/LO_GEN.mad:2809` | 2 |
| `AC0565` | `565B` | `src/LO_GEN.mad:184` | `src/LO_GEN.mad:1365` | 1 |
| `AC17N5` | `56561B` | `src/LO_GEN.mad:185` | `src/LO_GEN.mad:1033`, `src/LO_GEN.mad:1081`, `src/LO_GEN.mad:1956`, `src/LO_GEN.mad:3260` | 4 |
| `AC17N7` | `56563B` | `src/LO_GEN.mad:186` | `src/LO_GEN.mad:1179`, `src/LO_GEN.mad:1263`, `src/LO_GEN.mad:2376`, `src/LO_GEN.mad:2394`, `src/LO_GEN.mad:3419` | 5 |
| `AC17N8` | `56564B` | `src/LO_GEN.mad:187` | `src/LO_GEN.mad:771`, `src/LO_GEN.mad:984`, `src/LO_GEN.mad:1746`, `src/LO_GEN.mad:2053` | 4 |
| `AC17N9` | `56565B` | `src/LO_GEN.mad:188` | `src/LO_GEN.mad:786` | 1 |
| `AC17NA` | `56566B` | `src/LO_GEN.mad:189` | `src/LO_GEN.mad:795`, `src/LO_GEN.mad:2028`, `src/LO_GEN.mad:2340` | 3 |
| `AC17NE` | `56570B` | `src/LO_GEN.mad:190` | `src/LO_GEN.mad:1818`, `src/LO_GEN.mad:1939`, `src/LO_GEN.mad:3008` | 3 |
| `AC17NF` | `56571B` | `src/LO_GEN.mad:191` | `src/LO_GEN.mad:1556`, `src/LO_GEN.mad:1565` | 2 |
| `AC17NG` | `56572B` | `src/LO_GEN.mad:192` | `src/LO_GEN.mad:1562`, `src/LO_GEN.mad:1571`, `src/LO_GEN.mad:1878` | 3 |
| `AC17NI` | `56574B` | `src/LO_GEN.mad:193` | `src/LO_GEN.mad:1281`, `src/LO_GEN.mad:1905` | 2 |
| `AC17NJ` | `56575B` | `src/LO_GEN.mad:194` | `src/LO_GEN.mad:813`, `src/LO_GEN.mad:1248`, `src/LO_GEN.mad:1559`, `src/LO_GEN.mad:1568` | 4 |
| `AC17NK` | `56576B` | `src/LO_GEN.mad:195` | `src/LO_GEN.mad:999` | 1 |
| `AC17NL` | `56577B` | `src/LO_GEN.mad:196` | `src/LO_GEN.mad:846` | 1 |
| `AC17O9` | `56601B` | `src/LO_GEN.mad:197` | `src/LO_GEN.mad:969` | 1 |
| `AC17OA` | `56602B` | `src/LO_GEN.mad:198` | `src/LO_GEN.mad:2244` | 1 |
| `AC17OC` | `56604B` | `src/LO_GEN.mad:199` | `src/LO_GEN.mad:1975`, `src/LO_GEN.mad:2764` | 2 |
| `AC17OI` | `56610B` | `src/LO_GEN.mad:200` | `src/LO_GEN.mad:3212` | 1 |
| `AC17OK` | `56612B` | `src/LO_GEN.mad:201` | `src/LO_GEN.mad:2431` | 1 |
| `AC17OL` | `56613B` | `src/LO_GEN.mad:202` | `src/LO_GEN.mad:3227` | 1 |
| `AC17ON` | `56615B` | `src/LO_GEN.mad:203` | `src/LO_GEN.mad:2014`, `src/LO_GEN.mad:3093`, `src/LO_GEN.mad:3240`, `src/LO_GEN.mad:3486` | 4 |
| `AC17OO` | `56616B` | `src/LO_GEN.mad:204` | `src/LO_GEN.mad:2602` | 1 |
| `AC17OP` | `56617B` | `src/LO_GEN.mad:205` | `src/LO_GEN.mad:1779`, `src/LO_GEN.mad:1791`, `src/LO_GEN.mad:2040`, `src/LO_GEN.mad:2223`, `src/LO_GEN.mad:2298`, `src/LO_GEN.mad:2325` | 6 |
| `AC17OS` | `56620B` | `src/LO_GEN.mad:206` | `src/LO_GEN.mad:1767`, `src/LO_GEN.mad:1800`, `src/LO_GEN.mad:2076`, `src/LO_GEN.mad:2226`, `src/LO_GEN.mad:2295`, `src/LO_GEN.mad:2322` … (+1) | 7 |
| `AC17OT` | `56621B` | `src/LO_GEN.mad:207` | `src/LO_GEN.mad:2130`, `src/LO_GEN.mad:2196` | 2 |
| `AC17OV` | `56623B` | `src/LO_GEN.mad:208` | `src/LO_GEN.mad:2607` | 1 |
| `AC17OW` | `56624B` | `src/LO_GEN.mad:209` | `src/LO_GEN.mad:2574`, `src/LO_GEN.mad:2881` | 2 |
| `AC0567` | `567B` | `src/LO_GEN.mad:210` | `src/LO_GEN.mad:1368` | 1 |
| `AC0057` | `57B` | `src/LO_GEN.mad:211` | `src/LO_GEN.mad:2241` | 1 |
| `AC0577` | `577B` | `src/LO_GEN.mad:212` | `src/LO_GEN.mad:1380` | 1 |
| `AC0006` | `6B` | `src/LO_GEN.mad:213` | `src/LO_GEN.mad:730`, `src/LO_GEN.mad:1050`, `src/LO_GEN.mad:1752`, `src/LO_GEN.mad:1761`, `src/LO_GEN.mad:1794`, `src/LO_GEN.mad:1830` … (+8) | 14 |
| `AC0060` | `60B` | `src/LO_GEN.mad:214` | `src/LO_GEN.mad:2245` | 1 |
| `AC0601` | `601B` | `src/LO_GEN.mad:215` | `src/LO_GEN.mad:1386` | 1 |
| `AC1AJ7` | `60307B` | `src/LO_GEN.mad:216` | `src/LO_GEN.mad:1776`, `src/LO_GEN.mad:1788` | 2 |
| `AC0061` | `61B` | `src/LO_GEN.mad:217` | `src/LO_GEN.mad:2247` | 1 |
| `AC0062` | `62B` | `src/LO_GEN.mad:218` | `src/LO_GEN.mad:2416`, `src/LO_GEN.mad:2652`, `src/LO_GEN.mad:2954` | 3 |
| `AC0063` | `63B` | `src/LO_GEN.mad:219` | `src/LO_GEN.mad:2440` | 1 |
| `AC0064` | `64B` | `src/LO_GEN.mad:220` | `src/LO_GEN.mad:2470` | 1 |
| `AC0065` | `65B` | `src/LO_GEN.mad:221` | `src/LO_GEN.mad:2683` | 1 |
| `AC0656` | `656B` | `src/LO_GEN.mad:222` | `src/LO_GEN.mad:623` | 1 |
| `AC0066` | `66B` | `src/LO_GEN.mad:223` | `src/LO_GEN.mad:2755` | 1 |
| `AC0067` | `67B` | `src/LO_GEN.mad:224` | `src/LO_GEN.mad:2910`, `src/LO_GEN.mad:3509` | 2 |
| `AC0007` | `7B` | `src/LO_GEN.mad:225` | `src/LO_GEN.mad:643`, `src/LO_GEN.mad:676`, `src/LO_GEN.mad:679`, `src/LO_GEN.mad:802`, `src/LO_GEN.mad:879`, `src/LO_GEN.mad:907` … (+7) | 13 |
| `AC0070` | `70B` | `src/LO_GEN.mad:226` | `src/LO_GEN.mad:2914` | 1 |
| `AC1I12` | `70022B` | `src/LO_GEN.mad:227` | `src/LO_GEN.mad:554` | 1 |
| `AC0702` | `702B` | `src/LO_GEN.mad:228` | — | 0 |
| `AC1I82` | `70274B` | `src/LO_GEN.mad:229` | `src/LO_GEN.mad:563` | 1 |
| `AC0071` | `71B` | `src/LO_GEN.mad:230` | `src/LO_GEN.mad:2972` | 1 |
| `AC0072` | `72B` | `src/LO_GEN.mad:231` | `src/LO_GEN.mad:2993` | 1 |
| `AC0073` | `73B` | `src/LO_GEN.mad:232` | `src/LO_GEN.mad:3086` | 1 |
| `AC0074` | `74B` | `src/LO_GEN.mad:233` | `src/LO_GEN.mad:3119` | 1 |
| `AC0746` | `746B` | `src/LO_GEN.mad:234` | `src/LO_GEN.mad:1419` | 1 |
| `AC0747` | `747B` | `src/LO_GEN.mad:235` | `src/LO_GEN.mad:1413`, `src/LO_GEN.mad:1416` | 2 |
| `AC0075` | `75B` | `src/LO_GEN.mad:236` | `src/LO_GEN.mad:3149` | 1 |
| `AC1LYB` | `75107B` | `src/LO_GEN.mad:237` | `src/LO_GEN.mad:654` | 1 |
| `AC1LYF` | `75111B` | `src/LO_GEN.mad:238` | `src/LO_GEN.mad:648` | 1 |
| `AC0076` | `76B` | `src/LO_GEN.mad:239` | `src/LO_GEN.mad:3272` | 1 |
| `AC7600` | `7600B` | `src/LO_GEN.mad:240` | — | 0 |
| `AC0077` | `77B` | `src/LO_GEN.mad:241` | `src/LO_GEN.mad:3341` | 1 |
| `AC0777` | `777B` | `src/LO_GEN.mad:242` | `src/LO_GEN.mad:1410` | 1 |
| `NMLN5D` | `0000000000020005` | `src/LO_GEN.mad:243` | `src/LO_GEN.mad:1584`, `src/LO_GEN.mad:1588`, `src/LO_GEN.mad:1592`, `src/LO_GEN.mad:1596`, `src/LO_GEN.mad:1600`, `src/LO_GEN.mad:1604` … (+23) | 29 |
| `MV08R7` | `11347` | `src/LO_GEN.mad:244` | `src/LO_GEN.mad:3378`, `src/LO_GEN.mad:3396` | 2 |
| `MV09N8` | `12500` | `src/LO_GEN.mad:245` | — | 0 |
| `MV09N9` | `12501` | `src/LO_GEN.mad:246` | `src/LO_GEN.mad:2632` | 1 |
| `MV09NO` | `12516` | `src/LO_GEN.mad:247` | `src/LO_GEN.mad:2728`, `src/LO_GEN.mad:2917` | 2 |
| `MV0COW` | `16448` | `src/LO_GEN.mad:248` | `src/LO_GEN.mad:637`, `src/LO_GEN.mad:672` | 2 |
| `MV0J3V` | `24763` | `src/LO_GEN.mad:249` | `src/LO_GEN.mad:754` | 1 |
| `MV0J42` | `24770` | `src/LO_GEN.mad:250` | `src/LO_GEN.mad:1930`, `src/LO_GEN.mad:2044`, `src/LO_GEN.mad:2119`, `src/LO_GEN.mad:2248`, `src/LO_GEN.mad:2422`, `src/LO_GEN.mad:2578` … (+11) | 17 |
| `MV0J46` | `24774` | `src/LO_GEN.mad:251` | `src/LO_GEN.mad:1228` | 1 |
| `MV0J47` | `24775` | `src/LO_GEN.mad:252` | `src/LO_GEN.mad:1717` | 1 |
| `MV0JSR` | `25659` | `src/LO_GEN.mad:253` | `src/LO_GEN.mad:700` | 1 |
| `RE0010` | `10` | `src/LO_GEN.mad:254` | `src/LO_GEN.mad:865`, `src/LO_GEN.mad:3060`, `src/LO_GEN.mad:3069`, `src/LO_GEN.mad:3099`, `src/LO_GEN.mad:3129` | 5 |
| `RS0011` | `11` | `src/LO_GEN.mad:255` | `src/LO_GEN.mad:787`, `src/LO_GEN.mad:1705`, `src/LO_GEN.mad:1714`, `src/LO_GEN.mad:1726` | 4 |
| `RS0012` | `12` | `src/LO_GEN.mad:256` | `src/LO_GEN.mad:1990`, `src/LO_GEN.mad:2098`, `src/LO_GEN.mad:2134`, `src/LO_GEN.mad:2467`, `src/LO_GEN.mad:2737`, `src/LO_GEN.mad:2749` … (+3) | 9 |
| `RS0013` | `13` | `src/LO_GEN.mad:257` | `src/LO_GEN.mad:566` | 1 |
| `RS0014` | `14` | `src/LO_GEN.mad:258` | `src/LO_GEN.mad:736`, `src/LO_GEN.mad:931`, `src/LO_GEN.mad:3459`, `src/LO_GEN.mad:3468`, `src/LO_GEN.mad:3492`, `src/LO_GEN.mad:3528` | 6 |
| `RS0015` | `15` | `src/LO_GEN.mad:259` | `src/LO_GEN.mad:569` | 1 |
| `RS0002` | `2` | `src/LO_GEN.mad:260` | `src/LO_GEN.mad:1060` | 1 |
| `RS0003` | `3` | `src/LO_GEN.mad:261` | `src/LO_GEN.mad:3420` | 1 |
| `RS0004` | `4` | `src/LO_GEN.mad:262` | — | 0 |
| `RS0005` | `5` | `src/LO_GEN.mad:263` | `src/LO_GEN.mad:742` | 1 |
| `RS0007` | `7` | `src/LO_GEN.mad:264` | `src/LO_GEN.mad:685`, `src/LO_GEN.mad:3501` | 2 |
| `RS0008` | `8` | `src/LO_GEN.mad:265` | — | 0 |
| `RS0009` | `9` | `src/LO_GEN.mad:266` | `src/LO_GEN.mad:790` | 1 |
| `NG0012` | `-12` | `src/LO_GEN.mad:267` | `src/LO_GEN.mad:3405` | 1 |
| `NG0002` | `-2` | `src/LO_GEN.mad:268` | `src/LO_GEN.mad:3447`, `src/LO_GEN.mad:3452` | 2 |
| `NG0003` | `-3` | `src/LO_GEN.mad:269` | `src/LO_GEN.mad:1042`, `src/LO_GEN.mad:1044`, `src/LO_GEN.mad:1048`, `src/LO_GEN.mad:3455` | 4 |
| `NG0004` | `-4` | `src/LO_GEN.mad:270` | `src/LO_GEN.mad:699`, `src/LO_GEN.mad:724`, `src/LO_GEN.mad:729`, `src/LO_GEN.mad:849`, `src/LO_GEN.mad:924`, `src/LO_GEN.mad:972` … (+13) | 19 |
| `NG0005` | `-5` | `src/LO_GEN.mad:271` | `src/LO_GEN.mad:714`, `src/LO_GEN.mad:717`, `src/LO_GEN.mad:741`, `src/LO_GEN.mad:3432`, `src/LO_GEN.mad:3494`, `src/LO_GEN.mad:3519` | 6 |
| `NG0006` | `-6` | `src/LO_GEN.mad:272` | `src/LO_GEN.mad:2458`, `src/LO_GEN.mad:2530`, `src/LO_GEN.mad:2538`, `src/LO_GEN.mad:2566`, `src/LO_GEN.mad:2575`, `src/LO_GEN.mad:2967` … (+1) | 7 |
| `NG0007` | `-7` | `src/LO_GEN.mad:273` | `src/LO_GEN.mad:718`, `src/LO_GEN.mad:720`, `src/LO_GEN.mad:735`, `src/LO_GEN.mad:1843`, `src/LO_GEN.mad:1851`, `src/LO_GEN.mad:1854` … (+11) | 17 |
| `ONE` | `1` | `src/LO_GEN.mad:274` | `src/FOREX_RUNTIME_DISASM.mad:325`, `src/FOREX_RUNTIME_DISASM.mad:333`, `src/FOREX_RUNTIME_DISASM.mad:374` | 3 |
| `HDMARK` | `0000000000200003` | `src/LO_GEN.mad:275` | `src/LO_GEN.mad:541` | 1 |
| `HDNMWD` | `5457124745560000` | `src/LO_GEN.mad:276` | `src/LO_GEN.mad:543` | 1 |
| `JT1672` | `1672B` | `src/LO_GEN.mad:277` | `src/LO_GEN.mad:2083`, `src/LO_GEN.mad:2770` | 2 |
| `JT0FIS` | `20116B` | `src/LO_GEN.mad:278` | `src/LO_GEN.mad:581` | 1 |
| `JT0FU1` | `20521B` | `src/LO_GEN.mad:279` | `src/LO_GEN.mad:3390` | 1 |
| `JT0KEA` | `26434B` | `src/LO_GEN.mad:280` | `src/LO_GEN.mad:599` | 1 |
| `JT0NDY` | `30310B` | `src/LO_GEN.mad:281` | `src/LO_GEN.mad:596` | 1 |
| `JT0VOW` | `41072B` | `src/LO_GEN.mad:282` | `src/LO_GEN.mad:2464` | 1 |
| `JT0VPS` | `41104B` | `src/LO_GEN.mad:283` | `src/LO_GEN.mad:2478` | 1 |
| `JT0VU4` | `41260B` | `src/LO_GEN.mad:284` | `src/LO_GEN.mad:2739` | 1 |
| `JT0VUF` | `41271B` | `src/LO_GEN.mad:285` | `src/LO_GEN.mad:2734` | 1 |
| `JT0W2J` | `41563B` | `src/LO_GEN.mad:286` | `src/LO_GEN.mad:2680` | 1 |
| `JT0W2U` | `41574B` | `src/LO_GEN.mad:287` | `src/LO_GEN.mad:1204`, `src/LO_GEN.mad:1237`, `src/LO_GEN.mad:2572`, `src/LO_GEN.mad:2698` | 4 |
| `JT0W3P` | `41605B` | `src/LO_GEN.mad:288` | `src/LO_GEN.mad:2800`, `src/LO_GEN.mad:2857` | 2 |
| `JT0W44` | `41620B` | `src/LO_GEN.mad:289` | `src/LO_GEN.mad:2506`, `src/LO_GEN.mad:2662` | 2 |
| `JT0W4F` | `41631B` | `src/LO_GEN.mad:290` | `src/LO_GEN.mad:1810`, `src/LO_GEN.mad:1816` | 2 |
| `JT0W58` | `41660B` | `src/LO_GEN.mad:291` | `src/LO_GEN.mad:3294` | 1 |
| `JT0W6I` | `41706B` | `src/LO_GEN.mad:292` | `src/LO_GEN.mad:3288` | 1 |
| `JT0WFS` | `42040B` | `src/LO_GEN.mad:293` | `src/LO_GEN.mad:1168`, `src/LO_GEN.mad:1219` | 2 |
| `JT0WG6` | `42054B` | `src/LO_GEN.mad:294` | `src/LO_GEN.mad:3321` | 1 |
| `JT0WHV` | `42115B` | `src/LO_GEN.mad:295` | `src/LO_GEN.mad:1762`, `src/LO_GEN.mad:1774`, `src/LO_GEN.mad:1795`, `src/LO_GEN.mad:2269`, `src/LO_GEN.mad:2317` | 5 |
| `JT0WIA` | `42130B` | `src/LO_GEN.mad:296` | `src/LO_GEN.mad:649` | 1 |
| `JT0WID` | `42133B` | `src/LO_GEN.mad:297` | `src/LO_GEN.mad:1921` | 1 |
| `JT0WIY` | `42154B` | `src/LO_GEN.mad:298` | `src/LO_GEN.mad:2371` | 1 |
| `JT0WJE` | `42170B` | `src/LO_GEN.mad:299` | `src/LO_GEN.mad:1915` | 1 |
| `JT0WLG` | `42244B` | `src/LO_GEN.mad:300` | `src/LO_GEN.mad:763`, `src/LO_GEN.mad:778`, `src/LO_GEN.mad:946`, `src/LO_GEN.mad:991`, `src/LO_GEN.mad:1270` | 5 |
| `JT0WLS` | `42256B` | `src/LO_GEN.mad:301` | `src/LO_GEN.mad:1114`, `src/LO_GEN.mad:1927`, `src/LO_GEN.mad:2260`, `src/LO_GEN.mad:2308`, `src/LO_GEN.mad:2746`, `src/LO_GEN.mad:3045` … (+1) | 7 |
| `JT0WMA` | `42274B` | `src/LO_GEN.mad:302` | `src/LO_GEN.mad:1765`, `src/LO_GEN.mad:1777`, `src/LO_GEN.mad:1789`, `src/LO_GEN.mad:1798`, `src/LO_GEN.mad:2038`, `src/LO_GEN.mad:2074` … (+2) | 8 |
| `JT0WNK` | `42320B` | `src/LO_GEN.mad:303` | `src/LO_GEN.mad:1735`, `src/LO_GEN.mad:2233`, `src/LO_GEN.mad:2305` | 3 |
| `JT0WNW` | `42332B` | `src/LO_GEN.mad:304` | `src/LO_GEN.mad:2692` | 1 |
| `JT0WOO` | `42360B` | `src/LO_GEN.mad:305` | `src/LO_GEN.mad:832`, `src/LO_GEN.mad:838`, `src/LO_GEN.mad:1165` | 3 |
| `JT0WVD` | `42601B` | `src/LO_GEN.mad:306` | `src/LO_GEN.mad:766`, `src/LO_GEN.mad:781`, `src/LO_GEN.mad:841`, `src/LO_GEN.mad:1243`, `src/LO_GEN.mad:1255`, `src/LO_GEN.mad:1873` | 6 |
| `JT0WW2` | `42626B` | `src/LO_GEN.mad:307` | `src/LO_GEN.mad:949`, `src/LO_GEN.mad:994`, `src/LO_GEN.mad:1138`, `src/LO_GEN.mad:1903`, `src/LO_GEN.mad:3006` | 5 |
| `JT0WWD` | `42637B` | `src/LO_GEN.mad:308` | `src/LO_GEN.mad:1174`, `src/LO_GEN.mad:1225`, `src/LO_GEN.mad:1273`, `src/LO_GEN.mad:1963`, `src/LO_GEN.mad:2332`, `src/LO_GEN.mad:2419` … (+2) | 8 |
| `JT0WX3` | `42663B` | `src/LO_GEN.mad:309` | `src/LO_GEN.mad:1072` | 1 |
| `JT0WZO` | `42756B` | `src/LO_GEN.mad:310` | `src/LO_GEN.mad:2539` | 1 |
| `JT0XET` | `43301B` | `src/LO_GEN.mad:311` | `src/LO_GEN.mad:940` | 1 |
| `JT0XHM` | `43402B` | `src/LO_GEN.mad:312` | `src/LO_GEN.mad:1213` | 1 |
| `JT0XJ8` | `43460B` | `src/LO_GEN.mad:313` | `src/LO_GEN.mad:2446` | 1 |
| `JT0Y46` | `44214B` | `src/LO_GEN.mad:314` | `src/LO_GEN.mad:811`, `src/LO_GEN.mad:1279` | 2 |
| `JT0Y9H` | `44405B` | `src/LO_GEN.mad:315` | `src/LO_GEN.mad:2710` | 1 |
| `JT0YGV` | `44671B` | `src/LO_GEN.mad:316` | `src/LO_GEN.mad:982`, `src/LO_GEN.mad:2026`, `src/LO_GEN.mad:2338` | 3 |
| `JT0Z1P` | `45421B` | `src/LO_GEN.mad:317` | `src/LO_GEN.mad:1021`, `src/LO_GEN.mad:1858`, `src/LO_GEN.mad:3315`, `src/LO_GEN.mad:3336`, `src/LO_GEN.mad:3549` | 5 |
| `JT10GL` | `47253B` | `src/LO_GEN.mad:318` | `src/LO_GEN.mad:664` | 1 |
| `JT12O2` | `50114B` | `src/LO_GEN.mad:319` | `src/LO_GEN.mad:666` | 1 |
| `JT1554` | `53320B` | `src/LO_GEN.mad:320` | `src/LO_GEN.mad:2218`, `src/LO_GEN.mad:2287` | 2 |
| `JT155H` | `53333B` | `src/LO_GEN.mad:321` | `src/LO_GEN.mad:2452` | 1 |
| `JT15PV` | `54067B` | `src/LO_GEN.mad:322` | `src/LO_GEN.mad:2656` | 1 |
| `JT15WF` | `54303B` | `src/LO_GEN.mad:323` | `src/LO_GEN.mad:3063` | 1 |
| `JT1864` | `57244B` | `src/LO_GEN.mad:324` | `src/LO_GEN.mad:1156` | 1 |
| `JT188D` | `57325B` | `src/LO_GEN.mad:325` | `src/LO_GEN.mad:769`, `src/LO_GEN.mad:784`, `src/LO_GEN.mad:844`, `src/LO_GEN.mad:997`, `src/LO_GEN.mad:1090`, `src/LO_GEN.mad:1177` … (+6) | 12 |
| `JT18CK` | `57476B` | `src/LO_GEN.mad:326` | `src/LO_GEN.mad:772`, `src/LO_GEN.mad:799`, `src/LO_GEN.mad:814`, `src/LO_GEN.mad:847`, `src/LO_GEN.mad:970`, `src/LO_GEN.mad:985` … (+39) | 45 |
| `JT18GG` | `57616B` | `src/LO_GEN.mad:327` | `src/LO_GEN.mad:2824` | 1 |
| `JT1AAP` | `60001B` | `src/LO_GEN.mad:328` | `src/LO_GEN.mad:748` | 1 |
| `JT1AEA` | `60130B` | `src/LO_GEN.mad:329` | `src/LO_GEN.mad:2023`, `src/LO_GEN.mad:3276`, `src/LO_GEN.mad:3456` | 3 |
| `JT1AQA` | `60562B` | `src/LO_GEN.mad:330` | `src/LO_GEN.mad:3021` | 1 |
| `JT1BA5` | `61277B` | `src/LO_GEN.mad:331` | `src/LO_GEN.mad:3003` | 1 |
| `JT1BCS` | `61372B` | `src/LO_GEN.mad:332` | `src/LO_GEN.mad:1054`, `src/LO_GEN.mad:2931`, `src/LO_GEN.mad:2937`, `src/LO_GEN.mad:2943`, `src/LO_GEN.mad:2949`, `src/LO_GEN.mad:2955` … (+4) | 10 |
| `JT1BXM` | `62122B` | `src/LO_GEN.mad:333` | `src/LO_GEN.mad:2383`, `src/LO_GEN.mad:3423` | 2 |
| `JT1C6B` | `62435B` | `src/LO_GEN.mad:334` | `src/LO_GEN.mad:2482`, `src/LO_GEN.mad:2704` | 2 |
| `JT1CA2` | `62570B` | `src/LO_GEN.mad:335` | `src/LO_GEN.mad:1867` | 1 |
| `JT1CBU` | `62634B` | `src/LO_GEN.mad:336` | `src/LO_GEN.mad:2347`, `src/LO_GEN.mad:2368` | 2 |
| `JT1COS` | `63100B` | `src/LO_GEN.mad:337` | `src/LO_GEN.mad:2362` | 1 |
| `JT1CSJ` | `63235B` | `src/LO_GEN.mad:338` | `src/LO_GEN.mad:2398` | 1 |
| `JT1CTN` | `63275B` | `src/LO_GEN.mad:339` | `src/LO_GEN.mad:2389`, `src/LO_GEN.mad:2404` | 2 |
| `JT1CVN` | `63347B` | `src/LO_GEN.mad:340` | `src/LO_GEN.mad:829`, `src/LO_GEN.mad:979`, `src/LO_GEN.mad:1126`, `src/LO_GEN.mad:1744`, `src/LO_GEN.mad:1981`, `src/LO_GEN.mad:2476` … (+3) | 9 |
| `JT1D1D` | `63553B` | `src/LO_GEN.mad:341` | `src/LO_GEN.mad:2719` | 1 |
| `JT1D2T` | `63605B` | `src/LO_GEN.mad:342` | `src/LO_GEN.mad:1078`, `src/LO_GEN.mad:2743` | 2 |
| `JT1D3O` | `63636B` | `src/LO_GEN.mad:343` | `src/LO_GEN.mad:2716` | 1 |
| `JT1DM9` | `64305B` | `src/LO_GEN.mad:344` | `src/LO_GEN.mad:1897` | 1 |
| `JT1E9S` | `65152B` | `src/LO_GEN.mad:345` | `src/LO_GEN.mad:1885` | 1 |
| `JT1F24` | `66172B` | `src/LO_GEN.mad:346` | `src/LO_GEN.mad:820` | 1 |
| `JT1M2O` | `75264B` | `src/LO_GEN.mad:347` | `src/LO_GEN.mad:628`, `src/LO_GEN.mad:3101`, `src/LO_GEN.mad:3131` | 3 |
| `JT1M3O` | `75300B` | `src/LO_GEN.mad:348` | `src/LO_GEN.mad:657`, `src/LO_GEN.mad:810`, `src/LO_GEN.mad:1278` | 3 |
| `JT1M4E` | `75326B` | `src/LO_GEN.mad:349` | `src/LO_GEN.mad:727`, `src/LO_GEN.mad:732` | 2 |
| `JT1M4I` | `75330B` | `src/LO_GEN.mad:350` | `src/LO_GEN.mad:1289` | 1 |
| `JT1M4N` | `75335B` | `src/LO_GEN.mad:351` | `src/LO_GEN.mad:753` | 1 |
| `JT1M4U` | `75342B` | `src/LO_GEN.mad:352` | `src/LO_GEN.mad:1292` | 1 |
| `JT1M53` | `75351B` | `src/LO_GEN.mad:353` | `src/LO_GEN.mad:793` | 1 |
| `JT1M5C` | `75360B` | `src/LO_GEN.mad:354` | `src/LO_GEN.mad:1295` | 1 |
| `JT1M6T` | `75413B` | `src/LO_GEN.mad:355` | `src/LO_GEN.mad:894` | 1 |
| `JT1M6V` | `75415B` | `src/LO_GEN.mad:356` | `src/LO_GEN.mad:898` | 1 |
| `JT1M70` | `75420B` | `src/LO_GEN.mad:357` | `src/LO_GEN.mad:871` | 1 |
| `JT1M73` | `75423B` | `src/LO_GEN.mad:358` | `src/LO_GEN.mad:1298` | 1 |
| `JT1M7C` | `75432B` | `src/LO_GEN.mad:359` | `src/LO_GEN.mad:927`, `src/LO_GEN.mad:937` | 2 |
| `JT1M7P` | `75445B` | `src/LO_GEN.mad:360` | `src/LO_GEN.mad:858`, `src/LO_GEN.mad:876`, `src/LO_GEN.mad:912`, `src/LO_GEN.mad:1209` | 4 |
| `JT1M7V` | `75451B` | `src/LO_GEN.mad:361` | `src/LO_GEN.mad:1301` | 1 |
| `JT1M80` | `75456B` | `src/LO_GEN.mad:362` | `src/LO_GEN.mad:1313` | 1 |
| `JT1M86` | `75462B` | `src/LO_GEN.mad:363` | `src/LO_GEN.mad:1006` | 1 |
| `JT1M8F` | `75471B` | `src/LO_GEN.mad:364` | `src/LO_GEN.mad:1011` | 1 |
| `JT1M8K` | `75476B` | `src/LO_GEN.mad:365` | `src/LO_GEN.mad:1047` | 1 |
| `JT1M98` | `75500B` | `src/LO_GEN.mad:366` | `src/LO_GEN.mad:1051` | 1 |
| `JT1M9E` | `75506B` | `src/LO_GEN.mad:367` | `src/LO_GEN.mad:1069` | 1 |
| `JT1M9F` | `75507B` | `src/LO_GEN.mad:368` | `src/LO_GEN.mad:1074` | 1 |
| `JT1M9O` | `75516B` | `src/LO_GEN.mad:369` | `src/LO_GEN.mad:1056` | 1 |
| `JT1M9X` | `75525B` | `src/LO_GEN.mad:370` | `src/LO_GEN.mad:1104`, `src/LO_GEN.mad:1113` | 2 |
| `JT1M9Y` | `75526B` | `src/LO_GEN.mad:371` | `src/LO_GEN.mad:1304` | 1 |
| `JT1MA6` | `75534B` | `src/LO_GEN.mad:372` | `src/LO_GEN.mad:1131`, `src/LO_GEN.mad:1135` | 2 |
| `JT1MAD` | `75541B` | `src/LO_GEN.mad:373` | `src/LO_GEN.mad:1149`, `src/LO_GEN.mad:1153` | 2 |
| `JT1MAI` | `75546B` | `src/LO_GEN.mad:374` | `src/LO_GEN.mad:1161` | 1 |
| `JT1MAJ` | `75547B` | `src/LO_GEN.mad:375` | `src/LO_GEN.mad:1170` | 1 |
| `JT1MAN` | `75551B` | `src/LO_GEN.mad:376` | `src/LO_GEN.mad:1140` | 1 |
| `JT1MAR` | `75555B` | `src/LO_GEN.mad:377` | `src/LO_GEN.mad:1189` | 1 |
| `JT1MAT` | `75557B` | `src/LO_GEN.mad:378` | `src/LO_GEN.mad:2686` | 1 |
| `JT1MAZ` | `75563B` | `src/LO_GEN.mad:379` | `src/LO_GEN.mad:1316`, `src/LO_GEN.mad:1520`, `src/LO_GEN.mad:1529` | 3 |
| `JT1MB1` | `75565B` | `src/LO_GEN.mad:380` | `src/LO_GEN.mad:1319` | 1 |
| `JT1MB3` | `75567B` | `src/LO_GEN.mad:381` | `src/LO_GEN.mad:1349` | 1 |
| `JT1MB6` | `75570B` | `src/LO_GEN.mad:382` | `src/LO_GEN.mad:1812` | 1 |
| `JT1MB9` | `75573B` | `src/LO_GEN.mad:383` | `src/LO_GEN.mad:1267` | 1 |
| `JT1MBB` | `75575B` | `src/LO_GEN.mad:384` | `src/LO_GEN.mad:1355` | 1 |
| `JT1MC1` | `75601B` | `src/LO_GEN.mad:385` | `src/LO_GEN.mad:1352` | 1 |
| `JT1MC5` | `75605B` | `src/LO_GEN.mad:386` | `src/LO_GEN.mad:1260` | 1 |
| `JT1MC6` | `75606B` | `src/LO_GEN.mad:387` | `src/LO_GEN.mad:1328` | 1 |
| `JT1MOO` | `76056B` | `src/LO_GEN.mad:388` | `src/LO_GEN.mad:1394` | 1 |
| `JT1MP7` | `76075B` | `src/LO_GEN.mad:389` | `src/LO_GEN.mad:1740` | 1 |
| `JT1MPY` | `76102B` | `src/LO_GEN.mad:390` | `src/LO_GEN.mad:1759` | 1 |
| `JT1MQ6` | `76110B` | `src/LO_GEN.mad:391` | `src/LO_GEN.mad:1806` | 1 |
| `JT1MQ8` | `76112B` | `src/LO_GEN.mad:392` | `src/LO_GEN.mad:1753` | 1 |
| `JT1MQH` | `76121B` | `src/LO_GEN.mad:393` | `src/LO_GEN.mad:1331` | 1 |
| `JT1MQJ` | `76123B` | `src/LO_GEN.mad:394` | `src/LO_GEN.mad:1334` | 1 |
| `JT1MQL` | `76125B` | `src/LO_GEN.mad:395` | `src/LO_GEN.mad:1338`, `src/LO_GEN.mad:1341`, `src/LO_GEN.mad:1344`, `src/LO_GEN.mad:1347` | 4 |
| `JT1MQW` | `76136B` | `src/LO_GEN.mad:396` | `src/LO_GEN.mad:1834` | 1 |
| `JT1MR0` | `76140B` | `src/LO_GEN.mad:397` | `src/LO_GEN.mad:1845` | 1 |
| `JT1MR4` | `76144B` | `src/LO_GEN.mad:398` | `src/LO_GEN.mad:1839` | 1 |
| `JT1MR6` | `76146B` | `src/LO_GEN.mad:399` | `src/LO_GEN.mad:1358` | 1 |
| `JT1MRC` | `76152B` | `src/LO_GEN.mad:400` | `src/LO_GEN.mad:1364` | 1 |
| `JT1MRE` | `76154B` | `src/LO_GEN.mad:401` | `src/LO_GEN.mad:1367` | 1 |
| `JT1MRK` | `76160B` | `src/LO_GEN.mad:402` | `src/LO_GEN.mad:1370` | 1 |
| `JT1MRO` | `76164B` | `src/LO_GEN.mad:403` | `src/LO_GEN.mad:1379` | 1 |
| `JT1MRQ` | `76166B` | `src/LO_GEN.mad:404` | `src/LO_GEN.mad:1385` | 1 |
| `JT1MSS` | `76204B` | `src/LO_GEN.mad:405` | `src/LO_GEN.mad:1388` | 1 |
| `JT1MTJ` | `76231B` | `src/LO_GEN.mad:406` | `src/LO_GEN.mad:1987` | 1 |
| `JT1MVK` | `76304B` | `src/LO_GEN.mad:407` | `src/LO_GEN.mad:1391` | 1 |
| `JT1MVU` | `76314B` | `src/LO_GEN.mad:408` | `src/LO_GEN.mad:1466` | 1 |
| `JT1MW4` | `76324B` | `src/LO_GEN.mad:409` | `src/LO_GEN.mad:1382` | 1 |
| `JT1MWD` | `76333B` | `src/LO_GEN.mad:410` | `src/LO_GEN.mad:1403`, `src/LO_GEN.mad:1418` | 2 |
| `JT1MWE` | `76334B` | `src/LO_GEN.mad:411` | `src/LO_GEN.mad:1412`, `src/LO_GEN.mad:1415` | 2 |
| `JT1MWF` | `76335B` | `src/LO_GEN.mad:412` | `src/LO_GEN.mad:2224` | 1 |
| `JT1MWR` | `76347B` | `src/LO_GEN.mad:413` | `src/LO_GEN.mad:2238`, `src/LO_GEN.mad:2242` | 2 |
| `JT1MWX` | `76353B` | `src/LO_GEN.mad:414` | `src/LO_GEN.mad:2266`, `src/LO_GEN.mad:2314`, `src/LO_GEN.mad:2319`, `src/LO_GEN.mad:2343` | 4 |
| `JT1MX5` | `76361B` | `src/LO_GEN.mad:415` | `src/LO_GEN.mad:2286` | 1 |
| `JT1MX7` | `76363B` | `src/LO_GEN.mad:416` | `src/LO_GEN.mad:1400` | 1 |
| `JT1MX8` | `76364B` | `src/LO_GEN.mad:417` | `src/LO_GEN.mad:1409` | 1 |
| `JT1MX9` | `76365B` | `src/LO_GEN.mad:418` | `src/LO_GEN.mad:2296` | 1 |
| `JT1MXI` | `76374B` | `src/LO_GEN.mad:419` | `src/LO_GEN.mad:1397` | 1 |
| `JT1MXJ` | `76375B` | `src/LO_GEN.mad:420` | `src/LO_GEN.mad:1406` | 1 |
| `JT1MXK` | `76376B` | `src/LO_GEN.mad:421` | `src/LO_GEN.mad:2323` | 1 |
| `JT1MYA` | `76402B` | `src/LO_GEN.mad:422` | `src/LO_GEN.mad:2337` | 1 |
| `JT1MYC` | `76404B` | `src/LO_GEN.mad:423` | `src/LO_GEN.mad:1373` | 1 |
| `JT1MYE` | `76406B` | `src/LO_GEN.mad:424` | `src/LO_GEN.mad:1376` | 1 |
| `JT1MYJ` | `76411B` | `src/LO_GEN.mad:425` | `src/LO_GEN.mad:2353` | 1 |
| `JT1MYL` | `76413B` | `src/LO_GEN.mad:426` | `src/LO_GEN.mad:2358` | 1 |
| `JT1MYO` | `76416B` | `src/LO_GEN.mad:427` | `src/LO_GEN.mad:1421` | 1 |
| `JT1MYP` | `76417B` | `src/LO_GEN.mad:428` | `src/LO_GEN.mad:2391` | 1 |
| `JT1MYU` | `76422B` | `src/LO_GEN.mad:429` | `src/LO_GEN.mad:1430` | 1 |
| `JT1MYW` | `76424B` | `src/LO_GEN.mad:430` | `src/LO_GEN.mad:1574` | 1 |
| `JT1MYX` | `76425B` | `src/LO_GEN.mad:431` | `src/LO_GEN.mad:2406` | 1 |
| `JT1MYZ` | `76427B` | `src/LO_GEN.mad:432` | `src/LO_GEN.mad:1577` | 1 |
| `JT1MZ3` | `76431B` | `src/LO_GEN.mad:433` | `src/LO_GEN.mad:1424` | 1 |
| `JT1MZH` | `76445B` | `src/LO_GEN.mad:434` | `src/LO_GEN.mad:2418` | 1 |
| `JT1MZJ` | `76447B` | `src/LO_GEN.mad:435` | `src/LO_GEN.mad:1427` | 1 |
| `JT1MZN` | `76451B` | `src/LO_GEN.mad:436` | `src/LO_GEN.mad:1433` | 1 |
| `JT1MZO` | `76452B` | `src/LO_GEN.mad:437` | `src/LO_GEN.mad:2973`, `src/LO_GEN.mad:2978` | 2 |
| `JT1N01` | `76465B` | `src/LO_GEN.mad:438` | `src/LO_GEN.mad:2487` | 1 |
| `JT1N06` | `76470B` | `src/LO_GEN.mad:439` | `src/LO_GEN.mad:2496` | 1 |
| `JT1N0B` | `76475B` | `src/LO_GEN.mad:440` | `src/LO_GEN.mad:2511` | 1 |
| `JT1N10` | `76500B` | `src/LO_GEN.mad:441` | `src/LO_GEN.mad:2520` | 1 |
| `JT1N11` | `76501B` | `src/LO_GEN.mad:442` | `src/LO_GEN.mad:2490`, `src/LO_GEN.mad:2499`, `src/LO_GEN.mad:2503`, `src/LO_GEN.mad:2514`, `src/LO_GEN.mad:2523` | 5 |
| `JT1N14` | `76504B` | `src/LO_GEN.mad:443` | `src/LO_GEN.mad:2472` | 1 |
| `JT1N1B` | `76511B` | `src/LO_GEN.mad:444` | `src/LO_GEN.mad:2547` | 1 |
| `JT1N1E` | `76514B` | `src/LO_GEN.mad:445` | `src/LO_GEN.mad:2556` | 1 |
| `JT1N1F` | `76515B` | `src/LO_GEN.mad:446` | `src/LO_GEN.mad:2550`, `src/LO_GEN.mad:2559` | 2 |
| `JT1N1Y` | `76534B` | `src/LO_GEN.mad:447` | `src/LO_GEN.mad:2577` | 1 |
| `JT1N2I` | `76554B` | `src/LO_GEN.mad:448` | `src/LO_GEN.mad:2653`, `src/LO_GEN.mad:2700` | 2 |
| `JT1N2L` | `76557B` | `src/LO_GEN.mad:449` | `src/LO_GEN.mad:1497` | 1 |
| `JT1N2P` | `76561B` | `src/LO_GEN.mad:450` | `src/LO_GEN.mad:1500` | 1 |
| `JT1N2R` | `76563B` | `src/LO_GEN.mad:451` | `src/LO_GEN.mad:1443`, `src/LO_GEN.mad:1446`, `src/LO_GEN.mad:1449` | 3 |
| `JT1N2U` | `76566B` | `src/LO_GEN.mad:452` | `src/LO_GEN.mad:1437`, `src/LO_GEN.mad:1440`, `src/LO_GEN.mad:1452`, `src/LO_GEN.mad:1455`, `src/LO_GEN.mad:1458`, `src/LO_GEN.mad:1491` … (+1) | 7 |
| `JT1N2V` | `76567B` | `src/LO_GEN.mad:453` | `src/LO_GEN.mad:2670`, `src/LO_GEN.mad:2676` | 2 |
| `JT1N2Z` | `76571B` | `src/LO_GEN.mad:454` | `src/LO_GEN.mad:1461`, `src/LO_GEN.mad:2536` | 2 |
| `JT1N31` | `76573B` | `src/LO_GEN.mad:455` | `src/LO_GEN.mad:1463` | 1 |
| `JT1N33` | `76575B` | `src/LO_GEN.mad:456` | `src/LO_GEN.mad:1475` | 1 |
| `JT1N35` | `76577B` | `src/LO_GEN.mad:457` | `src/LO_GEN.mad:1478` | 1 |
| `JT1N44` | `76612B` | `src/LO_GEN.mad:458` | `src/LO_GEN.mad:2838` | 1 |
| `JT1N57` | `76651B` | `src/LO_GEN.mad:459` | `src/LO_GEN.mad:2833` | 1 |
| `JT1N5G` | `76660B` | `src/LO_GEN.mad:460` | `src/LO_GEN.mad:1481` | 1 |
| `JT1N5J` | `76663B` | `src/LO_GEN.mad:461` | `src/LO_GEN.mad:2863` | 1 |
| `JT1N7G` | `76732B` | `src/LO_GEN.mad:462` | `src/LO_GEN.mad:1827`, `src/LO_GEN.mad:1831` | 2 |
| `JT1N7V` | `76747B` | `src/LO_GEN.mad:463` | `src/LO_GEN.mad:1523`, `src/LO_GEN.mad:1532` | 2 |
| `JT1N88` | `76760B` | `src/LO_GEN.mad:464` | `src/LO_GEN.mad:3050` | 1 |
| `JT1N89` | `76761B` | `src/LO_GEN.mad:465` | `src/LO_GEN.mad:1538` | 1 |
| `JT1NFK` | `77024B` | `src/LO_GEN.mad:466` | `src/LO_GEN.mad:1541` | 1 |
| `JT1NG3` | `77043B` | `src/LO_GEN.mad:467` | `src/LO_GEN.mad:3179` | 1 |
| `JT1NGC` | `77052B` | `src/LO_GEN.mad:468` | `src/LO_GEN.mad:3210` | 1 |
| `JT1NGD` | `77053B` | `src/LO_GEN.mad:469` | `src/LO_GEN.mad:3171`, `src/LO_GEN.mad:3203` | 2 |
| `JT1NGV` | `77071B` | `src/LO_GEN.mad:470` | `src/LO_GEN.mad:3248` | 1 |
| `JT1NGY` | `77074B` | `src/LO_GEN.mad:471` | `src/LO_GEN.mad:1502` | 1 |
| `JT1NH0` | `77076B` | `src/LO_GEN.mad:472` | `src/LO_GEN.mad:1505` | 1 |
| `JT1NHO` | `77100B` | `src/LO_GEN.mad:473` | `src/LO_GEN.mad:1891`, `src/LO_GEN.mad:1896` | 2 |
| `JT1NHP` | `77101B` | `src/LO_GEN.mad:474` | `src/LO_GEN.mad:3284`, `src/LO_GEN.mad:3290` | 2 |
| `JT1NHR` | `77103B` | `src/LO_GEN.mad:475` | `src/LO_GEN.mad:1547` | 1 |
| `JT1NHS` | `77104B` | `src/LO_GEN.mad:476` | `src/LO_GEN.mad:1550` | 1 |
| `JT1NHZ` | `77111B` | `src/LO_GEN.mad:477` | `src/LO_GEN.mad:1544` | 1 |
| `JT1NI1` | `77113B` | `src/LO_GEN.mad:478` | `src/LO_GEN.mad:1554` | 1 |
| `JT1NI2` | `77114B` | `src/LO_GEN.mad:479` | `src/LO_GEN.mad:3357`, `src/LO_GEN.mad:3360`, `src/LO_GEN.mad:3363` | 3 |
| `JT1NI3` | `77115B` | `src/LO_GEN.mad:480` | `src/LO_GEN.mad:3353` | 1 |
| `JT1NI8` | `77120B` | `src/LO_GEN.mad:481` | `src/LO_GEN.mad:1557` | 1 |
| `JT1NI9` | `77121B` | `src/LO_GEN.mad:482` | `src/LO_GEN.mad:1560` | 1 |
| `JT1NIA` | `77122B` | `src/LO_GEN.mad:483` | `src/LO_GEN.mad:1563` | 1 |
| `JT1NIB` | `77123B` | `src/LO_GEN.mad:484` | `src/LO_GEN.mad:3342`, `src/LO_GEN.mad:3345` | 2 |
| `JT1NID` | `77125B` | `src/LO_GEN.mad:485` | `src/LO_GEN.mad:1566` | 1 |
| `JT1NIE` | `77126B` | `src/LO_GEN.mad:486` | `src/LO_GEN.mad:1569` | 1 |
| `JT1NIF` | `77127B` | `src/LO_GEN.mad:487` | `src/LO_GEN.mad:1572` | 1 |
| `JT1NII` | `77130B` | `src/LO_GEN.mad:488` | `src/LO_GEN.mad:616`, `src/LO_GEN.mad:723`, `src/LO_GEN.mad:1307`, `src/LO_GEN.mad:1310`, `src/LO_GEN.mad:1322`, `src/LO_GEN.mad:1325` … (+4) | 10 |
| `JT1NIW` | `77144B` | `src/LO_GEN.mad:489` | `src/LO_GEN.mad:760`, `src/LO_GEN.mad:774`, `src/LO_GEN.mad:805`, `src/LO_GEN.mad:816`, `src/LO_GEN.mad:825`, `src/LO_GEN.mad:852` … (+63) | 69 |
| `JT1NL4` | `77224B` | `src/LO_GEN.mad:490` | `src/LO_GEN.mad:3536` | 1 |
| `JT1NL7` | `77227B` | `src/LO_GEN.mad:491` | `src/LO_GEN.mad:3540` | 1 |
| `JT1NLM` | `77242B` | `src/LO_GEN.mad:492` | `src/LO_GEN.mad:3551` | 1 |
| `WV0350` | `0003500000030264` | `src/LO_GEN.mad:493` | `src/LO_GEN.mad:547` | 1 |
| `WV0422` | `0004220010075377` | `src/LO_GEN.mad:494` | `src/LO_GEN.mad:545` | 1 |
| `SC0003` | `3B` | `src/LO_SYN.mad:44` | `src/LO_SYN.mad:766` | 1 |
| `EX1263` | `1263B` | `src/LO_SYN.mad:45` | `src/LO_SYN.mad:769` | 1 |
| `EX7000` | `70000B` | `src/LO_SYN.mad:46` | `src/LO_SYN.mad:770` | 1 |
| `ME2200` | `2200B` | `src/LO_SYN.mad:47` | `src/LO_SYN.mad:772`, `src/LO_SYN.mad:781` | 2 |
| `ME5377` | `5377B` | `src/LO_SYN.mad:48` | `src/LO_SYN.mad:773`, `src/LO_SYN.mad:782` | 2 |
| `ME5000` | `5000B` | `src/LO_SYN.mad:49` | `src/LO_SYN.mad:775` | 1 |
| `ME0264` | `264B` | `src/LO_SYN.mad:50` | `src/LO_SYN.mad:776` | 1 |
| `SC0001` | `1B` | `src/LO_SYN.mad:51` | `src/LO_SYN.mad:778`, `src/LO_SYN.mad:835` | 2 |
| `ME3000` | `3000B` | `src/LO_SYN.mad:52` | `src/LO_SYN.mad:784` | 1 |
| `ME2377` | `2377B` | `src/LO_SYN.mad:53` | `src/LO_SYN.mad:785` | 1 |
| `ME0400` | `400B` | `src/LO_SYN.mad:54` | `src/LO_SYN.mad:787` | 1 |
| `EX0274` | `274B` | `src/LO_SYN.mad:55` | `src/LO_SYN.mad:788` | 1 |
| `RG3027` | `30274B` | `src/LO_SYN.mad:56` | `src/LO_SYN.mad:790`, `src/LO_SYN.mad:814` | 2 |
| `RG0017` | `17B` | `src/LO_SYN.mad:57` | `src/LO_SYN.mad:791`, `src/LO_SYN.mad:817` | 2 |
| `SC0017` | `17B` | `src/LO_SYN.mad:58` | `src/LO_SYN.mad:793` | 1 |
| `RG0015` | `15B` | `src/LO_SYN.mad:59` | `src/LO_SYN.mad:794` | 1 |
| `SC0016` | `16B` | `src/LO_SYN.mad:60` | `src/LO_SYN.mad:796` | 1 |
| `ME0013` | `13B` | `src/LO_SYN.mad:61` | `src/LO_SYN.mad:797` | 1 |
| `ME0104` | `104B` | `src/LO_SYN.mad:62` | `src/LO_SYN.mad:799` | 1 |
| `ME0014` | `14B` | `src/LO_SYN.mad:63` | `src/LO_SYN.mad:800` | 1 |
| `SC0014` | `14B` | `src/LO_SYN.mad:64` | `src/LO_SYN.mad:802` | 1 |
| `EX0014` | `14B` | `src/LO_SYN.mad:65` | `src/LO_SYN.mad:803` | 1 |
| `RG3601` | `36017B` | `src/LO_SYN.mad:66` | `src/LO_SYN.mad:805` | 1 |
| `RG0016` | `16B` | `src/LO_SYN.mad:67` | `src/LO_SYN.mad:806`, `src/LO_SYN.mad:809` | 2 |
| `RG3031` | `30311B` | `src/LO_SYN.mad:68` | `src/LO_SYN.mad:808` | 1 |
| `EX2011` | `20116B` | `src/LO_SYN.mad:69` | `src/LO_SYN.mad:811` | 1 |
| `ME0017` | `17B` | `src/LO_SYN.mad:70` | `src/LO_SYN.mad:815` | 1 |
| `AP3031` | `30312B` | `src/LO_SYN.mad:71` | `src/LO_SYN.mad:818` | 1 |
| `ME2000` | `2000B` | `src/LO_SYN.mad:72` | `src/LO_SYN.mad:827` | 1 |
| `ME0003` | `3B` | `src/LO_SYN.mad:73` | `src/LO_SYN.mad:830` | 1 |
| `SC0002` | `2B` | `src/LO_SYN.mad:74` | `src/LO_SYN.mad:833` | 1 |
| `RG2174` | `2174B` | `src/LO_SYN.mad:75` | `src/LO_SYN.mad:836` | 1 |
| `EX7555` | `75551B` | `src/LO_SYN.mad:76` | `src/LO_SYN.mad:838`, `src/LO_SYN.mad:865`, `src/LO_SYN.mad:940`, `src/LO_SYN.mad:1069`, `src/LO_SYN.mad:1144`, `src/LO_SYN.mad:1978` … (+18) | 24 |
| `RG5501` | `5501B` | `src/LO_SYN.mad:77` | `src/LO_SYN.mad:839`, `src/LO_SYN.mad:866`, `src/LO_SYN.mad:941`, `src/LO_SYN.mad:1070`, `src/LO_SYN.mad:1145`, `src/LO_SYN.mad:1550` … (+20) | 26 |
| `ME1040` | `1040B` | `src/LO_SYN.mad:78` | `src/LO_SYN.mad:841`, `src/LO_SYN.mad:868`, `src/LO_SYN.mad:943`, `src/LO_SYN.mad:1939`, `src/LO_SYN.mad:1981`, `src/LO_SYN.mad:2020` … (+24) | 30 |
| `ME7554` | `7554B` | `src/LO_SYN.mad:79` | `src/LO_SYN.mad:842` | 1 |
| `ME7011` | `70115B` | `src/LO_SYN.mad:80` | `src/LO_SYN.mad:844`, `src/LO_SYN.mad:2156`, `src/LO_SYN.mad:2215` | 3 |
| `ME7211` | `72113B` | `src/LO_SYN.mad:81` | `src/LO_SYN.mad:845`, `src/LO_SYN.mad:1168`, `src/LO_SYN.mad:2158`, `src/LO_SYN.mad:2434`, `src/LO_SYN.mad:2536` | 5 |
| `AP2004` | `20040B` | `src/LO_SYN.mad:82` | `src/LO_SYN.mad:847`, `src/LO_SYN.mad:992`, `src/LO_SYN.mad:1067`, `src/LO_SYN.mad:1091`, `src/LO_SYN.mad:1141`, `src/LO_SYN.mad:1169` … (+5) | 11 |
| `MV0040` | `40B` | `src/LO_SYN.mad:83` | `src/LO_SYN.mad:848`, `src/LO_SYN.mad:863`, `src/LO_SYN.mad:890`, `src/LO_SYN.mad:902`, `src/LO_SYN.mad:947`, `src/LO_SYN.mad:962` … (+79) | 85 |
| `EX4252` | `42524B` | `src/LO_SYN.mad:84` | `src/LO_SYN.mad:850`, `src/LO_SYN.mad:1013`, `src/LO_SYN.mad:1024`, `src/LO_SYN.mad:2173`, `src/LO_SYN.mad:2242`, `src/LO_SYN.mad:2266` … (+2) | 8 |
| `EX4044` | `40440B` | `src/LO_SYN.mad:85` | `src/LO_SYN.mad:851`, `src/LO_SYN.mad:919`, `src/LO_SYN.mad:1015`, `src/LO_SYN.mad:1025`, `src/LO_SYN.mad:1120`, `src/LO_SYN.mad:2243` … (+7) | 13 |
| `AP2016` | `20160B` | `src/LO_SYN.mad:86` | `src/LO_SYN.mad:853` | 1 |
| `ME4572` | `4572B` | `src/LO_SYN.mad:87` | `src/LO_SYN.mad:854`, `src/LO_SYN.mad:2830` | 2 |
| `EX4051` | `40513B` | `src/LO_SYN.mad:88` | `src/LO_SYN.mad:856` | 1 |
| `ME0120` | `120B` | `src/LO_SYN.mad:89` | `src/LO_SYN.mad:857`, `src/LO_SYN.mad:2938` | 2 |
| `EX6211` | `62117B` | `src/LO_SYN.mad:90` | `src/LO_SYN.mad:859` | 1 |
| `EX7310` | `73105B` | `src/LO_SYN.mad:91` | `src/LO_SYN.mad:860`, `src/LO_SYN.mad:3017` | 2 |
| `EX6456` | `64561B` | `src/LO_SYN.mad:92` | `src/LO_SYN.mad:862` | 1 |
| `EX6614` | `66140B` | `src/LO_SYN.mad:93` | `src/LO_SYN.mad:869`, `src/LO_SYN.mad:896`, `src/LO_SYN.mad:1586` | 3 |
| `EX2010` | `20103B` | `src/LO_SYN.mad:94` | `src/LO_SYN.mad:871`, `src/LO_SYN.mad:898`, `src/LO_SYN.mad:1588`, `src/LO_SYN.mad:1709`, `src/LO_SYN.mad:2057`, `src/LO_SYN.mad:2087` … (+1) | 7 |
| `EX4750` | `47502B` | `src/LO_SYN.mad:95` | `src/LO_SYN.mad:872`, `src/LO_SYN.mad:899`, `src/LO_SYN.mad:1589` | 3 |
| `ME7015` | `70151B` | `src/LO_SYN.mad:96` | `src/LO_SYN.mad:874`, `src/LO_SYN.mad:1292`, `src/LO_SYN.mad:2035`, `src/LO_SYN.mad:2846` | 4 |
| `EX6444` | `64440B` | `src/LO_SYN.mad:97` | `src/LO_SYN.mad:875`, `src/LO_SYN.mad:958`, `src/LO_SYN.mad:1499`, `src/LO_SYN.mad:1514`, `src/LO_SYN.mad:1547`, `src/LO_SYN.mad:1592` … (+3) | 9 |
| `AP6210` | `62105B` | `src/LO_SYN.mad:98` | `src/LO_SYN.mad:877`, `src/LO_SYN.mad:1205`, `src/LO_SYN.mad:1210`, `src/LO_SYN.mad:1795` | 4 |
| `EX5204` | `52040B` | `src/LO_SYN.mad:99` | `src/LO_SYN.mad:878`, `src/LO_SYN.mad:1207`, `src/LO_SYN.mad:1211`, `src/LO_SYN.mad:1796` | 4 |
| `EX4254` | `42544B` | `src/LO_SYN.mad:100` | `src/LO_SYN.mad:880`, `src/LO_SYN.mad:1234`, `src/LO_SYN.mad:1246`, `src/LO_SYN.mad:1297`, `src/LO_SYN.mad:1330`, `src/LO_SYN.mad:1375` … (+12) | 18 |
| `EX7013` | `70131B` | `src/LO_SYN.mad:101` | `src/LO_SYN.mad:881`, `src/LO_SYN.mad:1235`, `src/LO_SYN.mad:1247`, `src/LO_SYN.mad:1298`, `src/LO_SYN.mad:1331`, `src/LO_SYN.mad:1376` … (+12) | 18 |
| `EX2151` | `2151B` | `src/LO_SYN.mad:102` | `src/LO_SYN.mad:883`, `src/LO_SYN.mad:1237`, `src/LO_SYN.mad:1249`, `src/LO_SYN.mad:1300`, `src/LO_SYN.mad:1333`, `src/LO_SYN.mad:1378` … (+13) | 19 |
| `EX0113` | `20113B` | `src/LO_SYN.mad:103` | `src/LO_SYN.mad:884`, `src/LO_SYN.mad:1598`, `src/LO_SYN.mad:2356` | 3 |
| `EX6017` | `60176B` | `src/LO_SYN.mad:104` | `src/LO_SYN.mad:886`, `src/LO_SYN.mad:1600` | 2 |
| `ME1554` | `1554B` | `src/LO_SYN.mad:105` | `src/LO_SYN.mad:887`, `src/LO_SYN.mad:1601` | 2 |
| `EX4111` | `41117B` | `src/LO_SYN.mad:106` | `src/LO_SYN.mad:889`, `src/LO_SYN.mad:1603` | 2 |
| `EX5210` | `52103B` | `src/LO_SYN.mad:107` | `src/LO_SYN.mad:892`, `src/LO_SYN.mad:913`, `src/LO_SYN.mad:1009`, `src/LO_SYN.mad:1042`, `src/LO_SYN.mad:1102`, `src/LO_SYN.mad:1192` … (+11) | 17 |
| `AP5210` | `52103B` | `src/LO_SYN.mad:108` | `src/LO_SYN.mad:893`, `src/LO_SYN.mad:914`, `src/LO_SYN.mad:1010`, `src/LO_SYN.mad:1043`, `src/LO_SYN.mad:1103`, `src/LO_SYN.mad:1193` … (+11) | 17 |
| `ME7104` | `71040B` | `src/LO_SYN.mad:109` | `src/LO_SYN.mad:895`, `src/LO_SYN.mad:916`, `src/LO_SYN.mad:1012`, `src/LO_SYN.mad:1045`, `src/LO_SYN.mad:1105`, `src/LO_SYN.mad:1195` … (+10) | 16 |
| `EX2004` | `20040B` | `src/LO_SYN.mad:110` | `src/LO_SYN.mad:901`, `src/LO_SYN.mad:2233`, `src/LO_SYN.mad:2257`, `src/LO_SYN.mad:2965` | 4 |
| `EX4250` | `42503B` | `src/LO_SYN.mad:111` | `src/LO_SYN.mad:904`, `src/LO_SYN.mad:964`, `src/LO_SYN.mad:2542` | 3 |
| `EX4752` | `47524B` | `src/LO_SYN.mad:112` | `src/LO_SYN.mad:905`, `src/LO_SYN.mad:965`, `src/LO_SYN.mad:2543` | 3 |
| `RG2524` | `2524B` | `src/LO_SYN.mad:113` | `src/LO_SYN.mad:907`, `src/LO_SYN.mad:967`, `src/LO_SYN.mad:2545`, `src/LO_SYN.mad:2789` | 4 |
| `ME1513` | `1513B` | `src/LO_SYN.mad:114` | `src/LO_SYN.mad:908`, `src/LO_SYN.mad:1049`, `src/LO_SYN.mad:1138`, `src/LO_SYN.mad:1186`, `src/LO_SYN.mad:1484`, `src/LO_SYN.mad:1519` … (+4) | 10 |
| `EX6111` | `61117B` | `src/LO_SYN.mad:115` | `src/LO_SYN.mad:910`, `src/LO_SYN.mad:2548` | 2 |
| `EX0010` | `20040B` | `src/LO_SYN.mad:116` | `src/LO_SYN.mad:911`, `src/LO_SYN.mad:1361`, `src/LO_SYN.mad:1535`, `src/LO_SYN.mad:1913`, `src/LO_SYN.mad:2318`, `src/LO_SYN.mad:2549` … (+1) | 7 |
| `ME7757` | `77576B` | `src/LO_SYN.mad:117` | `src/LO_SYN.mad:917` | 1 |
| `RG0154` | `154B` | `src/LO_SYN.mad:118` | `src/LO_SYN.mad:920` | 1 |
| `EX6355` | `63551B` | `src/LO_SYN.mad:119` | `src/LO_SYN.mad:922` | 1 |
| `EX0000` | `20117B` | `src/LO_SYN.mad:120` | `src/LO_SYN.mad:923`, `src/LO_SYN.mad:1250`, `src/LO_SYN.mad:1406`, `src/LO_SYN.mad:2912` | 4 |
| `ME2520` | `2520B` | `src/LO_SYN.mad:121` | `src/LO_SYN.mad:925`, `src/LO_SYN.mad:985`, `src/LO_SYN.mad:1084`, `src/LO_SYN.mad:1858`, `src/LO_SYN.mad:1927`, `src/LO_SYN.mad:1966` … (+13) | 19 |
| `ME1440` | `1440B` | `src/LO_SYN.mad:122` | `src/LO_SYN.mad:926`, `src/LO_SYN.mad:2915` | 2 |
| `RG0151` | `151B` | `src/LO_SYN.mad:123` | `src/LO_SYN.mad:928`, `src/LO_SYN.mad:1576` | 2 |
| `ME7251` | `72510B` | `src/LO_SYN.mad:124` | `src/LO_SYN.mad:929` | 1 |
| `MV7014` | `70142B` | `src/LO_SYN.mad:125` | `src/LO_SYN.mad:931`, `src/LO_SYN.mad:2047`, `src/LO_SYN.mad:2218` | 3 |
| `EX6617` | `66170B` | `src/LO_SYN.mad:126` | `src/LO_SYN.mad:932`, `src/LO_SYN.mad:1031`, `src/LO_SYN.mad:1063`, `src/LO_SYN.mad:3053`, `src/LO_SYN.mad:3149` | 5 |
| `EX4244` | `42440B` | `src/LO_SYN.mad:127` | `src/LO_SYN.mad:934`, `src/LO_SYN.mad:1064`, `src/LO_SYN.mad:1133`, `src/LO_SYN.mad:1181`, `src/LO_SYN.mad:1223`, `src/LO_SYN.mad:1258` … (+14) | 20 |
| `RG7655` | `76551B` | `src/LO_SYN.mad:128` | `src/LO_SYN.mad:935`, `src/LO_SYN.mad:3197` | 2 |
| `ME6151` | `6151B` | `src/LO_SYN.mad:129` | `src/LO_SYN.mad:937` | 1 |
| `ME7252` | `72520B` | `src/LO_SYN.mad:130` | `src/LO_SYN.mad:938` | 1 |
| `EX4751` | `47510B` | `src/LO_SYN.mad:131` | `src/LO_SYN.mad:944`, `src/LO_SYN.mad:973`, `src/LO_SYN.mad:997`, `src/LO_SYN.mad:1451`, `src/LO_SYN.mad:1462`, `src/LO_SYN.mad:2375` … (+5) | 11 |
| `EX2040` | `2040B` | `src/LO_SYN.mad:132` | `src/LO_SYN.mad:946`, `src/LO_SYN.mad:974`, `src/LO_SYN.mad:998`, `src/LO_SYN.mad:1453`, `src/LO_SYN.mad:1463`, `src/LO_SYN.mad:1964` … (+3) | 9 |
| `RG0122` | `122B` | `src/LO_SYN.mad:133` | `src/LO_SYN.mad:949` | 1 |
| `EX4551` | `45517B` | `src/LO_SYN.mad:134` | `src/LO_SYN.mad:950`, `src/LO_SYN.mad:3050`, `src/LO_SYN.mad:3146` | 3 |
| `EX4152` | `41524B` | `src/LO_SYN.mad:135` | `src/LO_SYN.mad:952`, `src/LO_SYN.mad:1730`, `src/LO_SYN.mad:2815`, `src/LO_SYN.mad:3047` | 4 |
| `ME1117` | `1117B` | `src/LO_SYN.mad:136` | `src/LO_SYN.mad:953`, `src/LO_SYN.mad:3022` | 2 |
| `EX7417` | `74173B` | `src/LO_SYN.mad:137` | `src/LO_SYN.mad:955`, `src/LO_SYN.mad:3023` | 2 |
| `ME7006` | `70066B` | `src/LO_SYN.mad:138` | `src/LO_SYN.mad:956` | 1 |
| `EX6452` | `64524B` | `src/LO_SYN.mad:139` | `src/LO_SYN.mad:959` | 1 |
| `ME7004` | `70040B` | `src/LO_SYN.mad:140` | `src/LO_SYN.mad:961`, `src/LO_SYN.mad:1583`, `src/LO_SYN.mad:1648`, `src/LO_SYN.mad:2285` | 4 |
| `ME5501` | `5501B` | `src/LO_SYN.mad:141` | `src/LO_SYN.mad:968` | 1 |
| `EX4576` | `4576B` | `src/LO_SYN.mad:142` | `src/LO_SYN.mad:970`, `src/LO_SYN.mad:2249` | 2 |
| `ME7544` | `75440B` | `src/LO_SYN.mad:143` | `src/LO_SYN.mad:971` | 1 |
| `RG4105` | `4105B` | `src/LO_SYN.mad:144` | `src/LO_SYN.mad:976`, `src/LO_SYN.mad:1000` | 2 |
| `ME2151` | `2151B` | `src/LO_SYN.mad:145` | `src/LO_SYN.mad:977`, `src/LO_SYN.mad:1001`, `src/LO_SYN.mad:1903`, `src/LO_SYN.mad:3002` | 4 |
| `ME0101` | `101B` | `src/LO_SYN.mad:146` | `src/LO_SYN.mad:979`, `src/LO_SYN.mad:1003`, `src/LO_SYN.mad:1006`, `src/LO_SYN.mad:1325`, `src/LO_SYN.mad:1534`, `src/LO_SYN.mad:2680` | 6 |
| `RG4751` | `47510B` | `src/LO_SYN.mad:147` | `src/LO_SYN.mad:980`, `src/LO_SYN.mad:1004` | 2 |
| `ME0040` | `40B` | `src/LO_SYN.mad:148` | `src/LO_SYN.mad:982`, `src/LO_SYN.mad:1052`, `src/LO_SYN.mad:1271`, `src/LO_SYN.mad:1474`, `src/LO_SYN.mad:1487`, `src/LO_SYN.mad:1522` … (+11) | 17 |
| `ME0000` | `70117B` | `src/LO_SYN.mad:149` | `src/LO_SYN.mad:986`, `src/LO_SYN.mad:1085`, `src/LO_SYN.mad:2669`, `src/LO_SYN.mad:2902`, `src/LO_SYN.mad:3137`, `src/LO_SYN.mad:3158` | 6 |
| `EX0001` | `20115B` | `src/LO_SYN.mad:150` | `src/LO_SYN.mad:988`, `src/LO_SYN.mad:1087` | 2 |
| `ME4124` | `4124B` | `src/LO_SYN.mad:151` | `src/LO_SYN.mad:989`, `src/LO_SYN.mad:1088` | 2 |
| `AP4150` | `41503B` | `src/LO_SYN.mad:152` | `src/LO_SYN.mad:991`, `src/LO_SYN.mad:1090` | 2 |
| `EX2554` | `2554B` | `src/LO_SYN.mad:153` | `src/LO_SYN.mad:994`, `src/LO_SYN.mad:1573`, `src/LO_SYN.mad:1678`, `src/LO_SYN.mad:2999` | 4 |
| `ME0440` | `440B` | `src/LO_SYN.mad:154` | `src/LO_SYN.mad:995`, `src/LO_SYN.mad:1040`, `src/LO_SYN.mad:1100`, `src/LO_SYN.mad:1396`, `src/LO_SYN.mad:2171`, `src/LO_SYN.mad:3004` … (+1) | 7 |
| `EX6466` | `6466B` | `src/LO_SYN.mad:155` | `src/LO_SYN.mad:1007` | 1 |
| `ME0151` | `151B` | `src/LO_SYN.mad:156` | `src/LO_SYN.mad:1016`, `src/LO_SYN.mad:1498`, `src/LO_SYN.mad:1513`, `src/LO_SYN.mad:1546`, `src/LO_SYN.mad:1660`, `src/LO_SYN.mad:1843` … (+3) | 9 |
| `ME3117` | `3117B` | `src/LO_SYN.mad:157` | `src/LO_SYN.mad:1018`, `src/LO_SYN.mad:1321`, `src/LO_SYN.mad:1766`, `src/LO_SYN.mad:2740` | 4 |
| `ME6501` | `6501B` | `src/LO_SYN.mad:158` | `src/LO_SYN.mad:1019`, `src/LO_SYN.mad:1322`, `src/LO_SYN.mad:1369`, `src/LO_SYN.mad:1741`, `src/LO_SYN.mad:1768`, `src/LO_SYN.mad:2741` | 6 |
| `ME7244` | `72440B` | `src/LO_SYN.mad:159` | `src/LO_SYN.mad:1021`, `src/LO_SYN.mad:1028`, `src/LO_SYN.mad:2558`, `src/LO_SYN.mad:2761`, `src/LO_SYN.mad:2782` | 5 |
| `ME0510` | `510B` | `src/LO_SYN.mad:160` | `src/LO_SYN.mad:1027`, `src/LO_SYN.mad:1777` | 2 |
| `AP4156` | `41560B` | `src/LO_SYN.mad:161` | `src/LO_SYN.mad:1030`, `src/LO_SYN.mad:3104` | 2 |
| `RG2011` | `20113B` | `src/LO_SYN.mad:162` | `src/LO_SYN.mad:1033` | 1 |
| `ME5440` | `5440B` | `src/LO_SYN.mad:163` | `src/LO_SYN.mad:1034`, `src/LO_SYN.mad:2357`, `src/LO_SYN.mad:2453`, `src/LO_SYN.mad:2684`, `src/LO_SYN.mad:3190` | 5 |
| `EX2042` | `42546B` | `src/LO_SYN.mad:164` | `src/LO_SYN.mad:1036` | 1 |
| `EX5011` | `50115B` | `src/LO_SYN.mad:165` | `src/LO_SYN.mad:1037`, `src/LO_SYN.mad:1079`, `src/LO_SYN.mad:1154`, `src/LO_SYN.mad:1529` | 4 |
| `ME2110` | `2110B` | `src/LO_SYN.mad:166` | `src/LO_SYN.mad:1039`, `src/LO_SYN.mad:3058`, `src/LO_SYN.mad:3194` | 3 |
| `EX5211` | `52113B` | `src/LO_SYN.mad:167` | `src/LO_SYN.mad:1046`, `src/LO_SYN.mad:1612` | 2 |
| `ME4502` | `4502B` | `src/LO_SYN.mad:168` | `src/LO_SYN.mad:1048`, `src/LO_SYN.mad:1136`, `src/LO_SYN.mad:1184`, `src/LO_SYN.mad:1483`, `src/LO_SYN.mad:1517`, `src/LO_SYN.mad:1613` … (+2) | 8 |
| `EX3661` | `61113B` | `src/LO_SYN.mad:169` | `src/LO_SYN.mad:1051`, `src/LO_SYN.mad:1139`, `src/LO_SYN.mad:1187`, `src/LO_SYN.mad:1486`, `src/LO_SYN.mad:1520`, `src/LO_SYN.mad:1616` … (+1) | 7 |
| `EX7613` | `76131B` | `src/LO_SYN.mad:170` | `src/LO_SYN.mad:1054` | 1 |
| `EX4510` | `4510B` | `src/LO_SYN.mad:171` | `src/LO_SYN.mad:1055` | 1 |
| `ME0102` | `102B` | `src/LO_SYN.mad:172` | `src/LO_SYN.mad:1057`, `src/LO_SYN.mad:2753` | 2 |
| `EX4756` | `47566B` | `src/LO_SYN.mad:173` | `src/LO_SYN.mad:1058`, `src/LO_SYN.mad:2185`, `src/LO_SYN.mad:2413` | 3 |
| `ME7415` | `74151B` | `src/LO_SYN.mad:174` | `src/LO_SYN.mad:1060`, `src/LO_SYN.mad:2833`, `src/LO_SYN.mad:2969` | 3 |
| `RG2014` | `20142B` | `src/LO_SYN.mad:175` | `src/LO_SYN.mad:1061` | 1 |
| `ME3055` | `3055B` | `src/LO_SYN.mad:176` | `src/LO_SYN.mad:1066` | 1 |
| `ME1560` | `1560B` | `src/LO_SYN.mad:177` | `src/LO_SYN.mad:1072`, `src/LO_SYN.mad:1147` | 2 |
| `ME7155` | `71551B` | `src/LO_SYN.mad:178` | `src/LO_SYN.mad:1073`, `src/LO_SYN.mad:1148` | 2 |
| `EX7451` | `74513B` | `src/LO_SYN.mad:179` | `src/LO_SYN.mad:1075`, `src/LO_SYN.mad:1150` | 2 |
| `ME1551` | `1551B` | `src/LO_SYN.mad:180` | `src/LO_SYN.mad:1076`, `src/LO_SYN.mad:1151`, `src/LO_SYN.mad:1294`, `src/LO_SYN.mad:2401`, `src/LO_SYN.mad:2420`, `src/LO_SYN.mad:2429` … (+6) | 12 |
| `AP2014` | `20146B` | `src/LO_SYN.mad:181` | `src/LO_SYN.mad:1078`, `src/LO_SYN.mad:1153` | 2 |
| `ME2101` | `2101B` | `src/LO_SYN.mad:182` | `src/LO_SYN.mad:1081`, `src/LO_SYN.mad:1156`, `src/LO_SYN.mad:1270`, `src/LO_SYN.mad:1427`, `src/LO_SYN.mad:1472`, `src/LO_SYN.mad:1496` … (+13) | 19 |
| `ME7755` | `77554B` | `src/LO_SYN.mad:183` | `src/LO_SYN.mad:1093`, `src/LO_SYN.mad:1456`, `src/LO_SYN.mad:1465`, `src/LO_SYN.mad:1489`, `src/LO_SYN.mad:1504`, `src/LO_SYN.mad:1537` … (+11) | 17 |
| `RG7410` | `74101B` | `src/LO_SYN.mad:184` | `src/LO_SYN.mad:1094`, `src/LO_SYN.mad:1457`, `src/LO_SYN.mad:1466`, `src/LO_SYN.mad:1607`, `src/LO_SYN.mad:1622` | 5 |
| `ME1171` | `1171B` | `src/LO_SYN.mad:185` | `src/LO_SYN.mad:1096`, `src/LO_SYN.mad:1459`, `src/LO_SYN.mad:1468`, `src/LO_SYN.mad:1492`, `src/LO_SYN.mad:1507`, `src/LO_SYN.mad:1540` … (+14) | 20 |
| `ME7404` | `74040B` | `src/LO_SYN.mad:186` | `src/LO_SYN.mad:1097`, `src/LO_SYN.mad:1433`, `src/LO_SYN.mad:1460`, `src/LO_SYN.mad:1469`, `src/LO_SYN.mad:1493`, `src/LO_SYN.mad:1508` … (+18) | 24 |
| `EX4546` | `4546B` | `src/LO_SYN.mad:187` | `src/LO_SYN.mad:1099` | 1 |
| `ME0572` | `572B` | `src/LO_SYN.mad:188` | `src/LO_SYN.mad:1106`, `src/LO_SYN.mad:1631`, `src/LO_SYN.mad:1787`, `src/LO_SYN.mad:1868`, `src/LO_SYN.mad:3170` | 5 |
| `ME7255` | `72554B` | `src/LO_SYN.mad:189` | `src/LO_SYN.mad:1108`, `src/LO_SYN.mad:1243`, `src/LO_SYN.mad:1789`, `src/LO_SYN.mad:2281`, `src/LO_SYN.mad:2905`, `src/LO_SYN.mad:2968` … (+1) | 7 |
| `AP2105` | `52105B` | `src/LO_SYN.mad:190` | `src/LO_SYN.mad:1109`, `src/LO_SYN.mad:1790` | 2 |
| `EX7404` | `74040B` | `src/LO_SYN.mad:191` | `src/LO_SYN.mad:1111`, `src/LO_SYN.mad:1792` | 2 |
| `AP6615` | `66151B` | `src/LO_SYN.mad:192` | `src/LO_SYN.mad:1112`, `src/LO_SYN.mad:2339`, `src/LO_SYN.mad:3130`, `src/LO_SYN.mad:3296` | 4 |
| `ME5101` | `5101B` | `src/LO_SYN.mad:193` | `src/LO_SYN.mad:1114`, `src/LO_SYN.mad:2168` | 2 |
| `EX5017` | `50171B` | `src/LO_SYN.mad:194` | `src/LO_SYN.mad:1115` | 1 |
| `RG0103` | `103B` | `src/LO_SYN.mad:195` | `src/LO_SYN.mad:1117`, `src/LO_SYN.mad:1220`, `src/LO_SYN.mad:1255`, `src/LO_SYN.mad:1280`, `src/LO_SYN.mad:1411`, `src/LO_SYN.mad:2149` … (+5) | 11 |
| `EX4754` | `47542B` | `src/LO_SYN.mad:196` | `src/LO_SYN.mad:1118`, `src/LO_SYN.mad:2150` | 2 |
| `EX4515` | `4515B` | `src/LO_SYN.mad:197` | `src/LO_SYN.mad:1123`, `src/LO_SYN.mad:1171` | 2 |
| `RG7554` | `7554B` | `src/LO_SYN.mad:198` | `src/LO_SYN.mad:1124`, `src/LO_SYN.mad:1172` | 2 |
| `ME1103` | `1103B` | `src/LO_SYN.mad:199` | `src/LO_SYN.mad:1126`, `src/LO_SYN.mad:1174`, `src/LO_SYN.mad:1214` | 3 |
| `ME7010` | `70105B` | `src/LO_SYN.mad:200` | `src/LO_SYN.mad:1127`, `src/LO_SYN.mad:1175`, `src/LO_SYN.mad:1216`, `src/LO_SYN.mad:1898`, `src/LO_SYN.mad:2572`, `src/LO_SYN.mad:2839` … (+3) | 9 |
| `ME7455` | `74554B` | `src/LO_SYN.mad:201` | `src/LO_SYN.mad:1129`, `src/LO_SYN.mad:1177` | 2 |
| `EX0440` | `440B` | `src/LO_SYN.mad:202` | `src/LO_SYN.mad:1130`, `src/LO_SYN.mad:1178`, `src/LO_SYN.mad:1219`, `src/LO_SYN.mad:3079`, `src/LO_SYN.mad:3100` | 5 |
| `ME7503` | `7503B` | `src/LO_SYN.mad:203` | `src/LO_SYN.mad:1132`, `src/LO_SYN.mad:1180`, `src/LO_SYN.mad:2161`, `src/LO_SYN.mad:2260`, `src/LO_SYN.mad:2491`, `src/LO_SYN.mad:2503` … (+3) | 9 |
| `RG4051` | `40513B` | `src/LO_SYN.mad:204` | `src/LO_SYN.mad:1135`, `src/LO_SYN.mad:1183`, `src/LO_SYN.mad:1481`, `src/LO_SYN.mad:1516`, `src/LO_SYN.mad:1663`, `src/LO_SYN.mad:2416` … (+1) | 7 |
| `ME7502` | `7502B` | `src/LO_SYN.mad:205` | `src/LO_SYN.mad:1159`, `src/LO_SYN.mad:1732`, `src/LO_SYN.mad:1904`, `src/LO_SYN.mad:2527`, `src/LO_SYN.mad:3115` | 5 |
| `ME7752` | `77520B` | `src/LO_SYN.mad:206` | `src/LO_SYN.mad:1160`, `src/LO_SYN.mad:1733`, `src/LO_SYN.mad:2528`, `src/LO_SYN.mad:3116` | 4 |
| `ME7560` | `7560B` | `src/LO_SYN.mad:207` | `src/LO_SYN.mad:1162`, `src/LO_SYN.mad:1736`, `src/LO_SYN.mad:2069`, `src/LO_SYN.mad:2530`, `src/LO_SYN.mad:2594` | 5 |
| `ME2544` | `2544B` | `src/LO_SYN.mad:208` | `src/LO_SYN.mad:1163`, `src/LO_SYN.mad:2531`, `src/LO_SYN.mad:2596` | 3 |
| `ME7610` | `76105B` | `src/LO_SYN.mad:209` | `src/LO_SYN.mad:1165`, `src/LO_SYN.mad:2533` | 2 |
| `EX2020` | `20115B` | `src/LO_SYN.mad:210` | `src/LO_SYN.mad:1166`, `src/LO_SYN.mad:2534` | 2 |
| `AP4656` | `46561B` | `src/LO_SYN.mad:211` | `src/LO_SYN.mad:1196`, `src/LO_SYN.mad:1309`, `src/LO_SYN.mad:1367`, `src/LO_SYN.mad:2477` | 4 |
| `ME0117` | `117B` | `src/LO_SYN.mad:212` | `src/LO_SYN.mad:1198`, `src/LO_SYN.mad:1439`, `src/LO_SYN.mad:1804`, `src/LO_SYN.mad:1963`, `src/LO_SYN.mad:2317`, `src/LO_SYN.mad:2479` … (+3) | 9 |
| `ME7012` | `70120B` | `src/LO_SYN.mad:213` | `src/LO_SYN.mad:1199`, `src/LO_SYN.mad:2480`, `src/LO_SYN.mad:3133` | 3 |
| `AP7310` | `73105B` | `src/LO_SYN.mad:214` | `src/LO_SYN.mad:1213` | 1 |
| `EX4055` | `40554B` | `src/LO_SYN.mad:215` | `src/LO_SYN.mad:1217`, `src/LO_SYN.mad:1226`, `src/LO_SYN.mad:1274`, `src/LO_SYN.mad:1339`, `src/LO_SYN.mad:2315`, `src/LO_SYN.mad:2872` | 6 |
| `ME4503` | `4503B` | `src/LO_SYN.mad:216` | `src/LO_SYN.mad:1222`, `src/LO_SYN.mad:1256`, `src/LO_SYN.mad:1282`, `src/LO_SYN.mad:1412`, `src/LO_SYN.mad:1879`, `src/LO_SYN.mad:2113` … (+7) | 13 |
| `RG7752` | `77520B` | `src/LO_SYN.mad:217` | `src/LO_SYN.mad:1225`, `src/LO_SYN.mad:1273`, `src/LO_SYN.mad:1337` | 3 |
| `EX4404` | `44040B` | `src/LO_SYN.mad:218` | `src/LO_SYN.mad:1228`, `src/LO_SYN.mad:1276`, `src/LO_SYN.mad:1340` | 3 |
| `ME0520` | `520B` | `src/LO_SYN.mad:219` | `src/LO_SYN.mad:1229`, `src/LO_SYN.mad:1277`, `src/LO_SYN.mad:1342`, `src/LO_SYN.mad:2447`, `src/LO_SYN.mad:2644` | 5 |
| `ME6440` | `6440B` | `src/LO_SYN.mad:220` | `src/LO_SYN.mad:1231`, `src/LO_SYN.mad:1279`, `src/LO_SYN.mad:1343`, `src/LO_SYN.mad:2645` | 4 |
| `EX2012` | `20120B` | `src/LO_SYN.mad:221` | `src/LO_SYN.mad:1238`, `src/LO_SYN.mad:1900`, `src/LO_SYN.mad:2671` | 3 |
| `ME5144` | `5144B` | `src/LO_SYN.mad:222` | `src/LO_SYN.mad:1240` | 1 |
| `ME7615` | `76151B` | `src/LO_SYN.mad:223` | `src/LO_SYN.mad:1241` | 1 |
| `EX0011` | `20040B` | `src/LO_SYN.mad:224` | `src/LO_SYN.mad:1244`, `src/LO_SYN.mad:2180`, `src/LO_SYN.mad:2512` | 3 |
| `RG6105` | `6105B` | `src/LO_SYN.mad:225` | `src/LO_SYN.mad:1252`, `src/LO_SYN.mad:1408` | 2 |
| `EX0007` | `52040B` | `src/LO_SYN.mad:226` | `src/LO_SYN.mad:1253`, `src/LO_SYN.mad:1409` | 2 |
| `ME7412` | `74124B` | `src/LO_SYN.mad:227` | `src/LO_SYN.mad:1259`, `src/LO_SYN.mad:1285` | 2 |
| `ME7111` | `71116B` | `src/LO_SYN.mad:228` | `src/LO_SYN.mad:1261`, `src/LO_SYN.mad:1286`, `src/LO_SYN.mad:2791` | 3 |
| `RG4056` | `40560B` | `src/LO_SYN.mad:229` | `src/LO_SYN.mad:1268`, `src/LO_SYN.mad:1471`, `src/LO_SYN.mad:1495`, `src/LO_SYN.mad:1510`, `src/LO_SYN.mad:1543`, `src/LO_SYN.mad:1657` … (+2) | 8 |
| `ME7712` | `77124B` | `src/LO_SYN.mad:230` | `src/LO_SYN.mad:1288` | 1 |
| `ME4440` | `4440B` | `src/LO_SYN.mad:231` | `src/LO_SYN.mad:1289`, `src/LO_SYN.mad:1856`, `src/LO_SYN.mad:2723` | 3 |
| `RG4131` | `4131B` | `src/LO_SYN.mad:232` | `src/LO_SYN.mad:1291` | 1 |
| `EX6610` | `66101B` | `src/LO_SYN.mad:233` | `src/LO_SYN.mad:1295`, `src/LO_SYN.mad:2402`, `src/LO_SYN.mad:2576`, `src/LO_SYN.mad:2896`, `src/LO_SYN.mad:2927`, `src/LO_SYN.mad:3014` | 6 |
| `EX2015` | `20151B` | `src/LO_SYN.mad:234` | `src/LO_SYN.mad:1301`, `src/LO_SYN.mad:1334`, `src/LO_SYN.mad:1379`, `src/LO_SYN.mad:1448` | 4 |
| `EX7044` | `70440B` | `src/LO_SYN.mad:235` | `src/LO_SYN.mad:1303`, `src/LO_SYN.mad:1336`, `src/LO_SYN.mad:1381`, `src/LO_SYN.mad:1450` | 4 |
| `ME4117` | `4117B` | `src/LO_SYN.mad:236` | `src/LO_SYN.mad:1304`, `src/LO_SYN.mad:1442`, `src/LO_SYN.mad:1807` | 3 |
| `ME7044` | `70440B` | `src/LO_SYN.mad:237` | `src/LO_SYN.mad:1306`, `src/LO_SYN.mad:1399`, `src/LO_SYN.mad:2617`, `src/LO_SYN.mad:2635`, `src/LO_SYN.mad:2656`, `src/LO_SYN.mad:2957` … (+2) | 8 |
| `ME1130` | `1130B` | `src/LO_SYN.mad:238` | `src/LO_SYN.mad:1310` | 1 |
| `EX6210` | `62101B` | `src/LO_SYN.mad:239` | `src/LO_SYN.mad:1312` | 1 |
| `ME4105` | `4105B` | `src/LO_SYN.mad:240` | `src/LO_SYN.mad:1313`, `src/LO_SYN.mad:1349`, `src/LO_SYN.mad:1765`, `src/LO_SYN.mad:1916`, `src/LO_SYN.mad:2033`, `src/LO_SYN.mad:2072` … (+4) | 10 |
| `ME2117` | `2117B` | `src/LO_SYN.mad:241` | `src/LO_SYN.mad:1315`, `src/LO_SYN.mad:1441`, `src/LO_SYN.mad:1718`, `src/LO_SYN.mad:1805`, `src/LO_SYN.mad:3016` | 5 |
| `EX7311` | `73110B` | `src/LO_SYN.mad:242` | `src/LO_SYN.mad:1316` | 1 |
| `EX2014` | `20142B` | `src/LO_SYN.mad:243` | `src/LO_SYN.mad:1318` | 1 |
| `AP5217` | `52170B` | `src/LO_SYN.mad:244` | `src/LO_SYN.mad:1319`, `src/LO_SYN.mad:2219`, `src/LO_SYN.mad:3020` | 3 |
| `EX7411` | `74110B` | `src/LO_SYN.mad:245` | `src/LO_SYN.mad:1324`, `src/LO_SYN.mad:1769` | 2 |
| `ME0515` | `515B` | `src/LO_SYN.mad:246` | `src/LO_SYN.mad:1327` | 1 |
| `ME7456` | `74560B` | `src/LO_SYN.mad:247` | `src/LO_SYN.mad:1345`, `src/LO_SYN.mad:1355`, `src/LO_SYN.mad:1421`, `src/LO_SYN.mad:1429`, `src/LO_SYN.mad:2068`, `src/LO_SYN.mad:2879` | 6 |
| `ME2516` | `2516B` | `src/LO_SYN.mad:248` | `src/LO_SYN.mad:1346`, `src/LO_SYN.mad:2755`, `src/LO_SYN.mad:2776` | 3 |
| `ME7113` | `71131B` | `src/LO_SYN.mad:249` | `src/LO_SYN.mad:1348`, `src/LO_SYN.mad:3166`, `src/LO_SYN.mad:3262` | 3 |
| `ME1517` | `1517B` | `src/LO_SYN.mad:250` | `src/LO_SYN.mad:1351`, `src/LO_SYN.mad:1910`, `src/LO_SYN.mad:2074` | 3 |
| `EX3652` | `52102B` | `src/LO_SYN.mad:251` | `src/LO_SYN.mad:1352`, `src/LO_SYN.mad:1834`, `src/LO_SYN.mad:2075` | 3 |
| `ME7204` | `72040B` | `src/LO_SYN.mad:252` | `src/LO_SYN.mad:1354`, `src/LO_SYN.mad:1835`, `src/LO_SYN.mad:2077`, `src/LO_SYN.mad:2186`, `src/LO_SYN.mad:2414`, `src/LO_SYN.mad:3167` … (+1) | 7 |
| `AP2010` | `20106B` | `src/LO_SYN.mad:253` | `src/LO_SYN.mad:1357` | 1 |
| `ME7710` | `77103B` | `src/LO_SYN.mad:254` | `src/LO_SYN.mad:1358` | 1 |
| `ME7451` | `74517B` | `src/LO_SYN.mad:255` | `src/LO_SYN.mad:1360` | 1 |
| `EX1551` | `1551B` | `src/LO_SYN.mad:256` | `src/LO_SYN.mad:1370`, `src/LO_SYN.mad:1742` | 2 |
| `RG0440` | `440B` | `src/LO_SYN.mad:257` | `src/LO_SYN.mad:1372`, `src/LO_SYN.mad:1628`, `src/LO_SYN.mad:1744`, `src/LO_SYN.mad:2717` | 4 |
| `EX7515` | `7515B` | `src/LO_SYN.mad:258` | `src/LO_SYN.mad:1382`, `src/LO_SYN.mad:1940` | 2 |
| `EX7516` | `47516B` | `src/LO_SYN.mad:259` | `src/LO_SYN.mad:1384`, `src/LO_SYN.mad:1942` | 2 |
| `ME1154` | `1154B` | `src/LO_SYN.mad:260` | `src/LO_SYN.mad:1385`, `src/LO_SYN.mad:3284` | 2 |
| `EX4550` | `45501B` | `src/LO_SYN.mad:261` | `src/LO_SYN.mad:1387` | 1 |
| `EX7503` | `47503B` | `src/LO_SYN.mad:262` | `src/LO_SYN.mad:1394` | 1 |
| `EX2520` | `42520B` | `src/LO_SYN.mad:263` | `src/LO_SYN.mad:1397` | 1 |
| `EX7015` | `70151B` | `src/LO_SYN.mad:264` | `src/LO_SYN.mad:1417`, `src/LO_SYN.mad:1690` | 2 |
| `EX0510` | `510B` | `src/LO_SYN.mad:265` | `src/LO_SYN.mad:1418`, `src/LO_SYN.mad:1691` | 2 |
| `AP4244` | `42440B` | `src/LO_SYN.mad:266` | `src/LO_SYN.mad:1420`, `src/LO_SYN.mad:1693` | 2 |
| `ME0160` | `160B` | `src/LO_SYN.mad:267` | `src/LO_SYN.mad:1423`, `src/LO_SYN.mad:1697` | 2 |
| `EX4155` | `41554B` | `src/LO_SYN.mad:268` | `src/LO_SYN.mad:1424`, `src/LO_SYN.mad:1699` | 2 |
| `ME0005` | `70104B` | `src/LO_SYN.mad:269` | `src/LO_SYN.mad:1426`, `src/LO_SYN.mad:1700` | 2 |
| `ME0105` | `105B` | `src/LO_SYN.mad:270` | `src/LO_SYN.mad:1430`, `src/LO_SYN.mad:1844`, `src/LO_SYN.mad:1885`, `src/LO_SYN.mad:2279`, `src/LO_SYN.mad:2293`, `src/LO_SYN.mad:2801` … (+3) | 9 |
| `ME2515` | `2515B` | `src/LO_SYN.mad:271` | `src/LO_SYN.mad:1432`, `src/LO_SYN.mad:1846`, `src/LO_SYN.mad:1886`, `src/LO_SYN.mad:2252`, `src/LO_SYN.mad:2294`, `src/LO_SYN.mad:2803` … (+1) | 7 |
| `EX7012` | `70120B` | `src/LO_SYN.mad:272` | `src/LO_SYN.mad:1435`, `src/LO_SYN.mad:1798`, `src/LO_SYN.mad:2288`, `src/LO_SYN.mad:2960` | 4 |
| `ME7210` | `72105B` | `src/LO_SYN.mad:273` | `src/LO_SYN.mad:1436`, `src/LO_SYN.mad:1799`, `src/LO_SYN.mad:2290`, `src/LO_SYN.mad:2962` | 4 |
| `EX4251` | `42510B` | `src/LO_SYN.mad:274` | `src/LO_SYN.mad:1438`, `src/LO_SYN.mad:1726`, `src/LO_SYN.mad:2176`, `src/LO_SYN.mad:2291`, `src/LO_SYN.mad:2557`, `src/LO_SYN.mad:2573` … (+6) | 12 |
| `RG7417` | `74171B` | `src/LO_SYN.mad:275` | `src/LO_SYN.mad:1490`, `src/LO_SYN.mad:1505`, `src/LO_SYN.mad:1538`, `src/LO_SYN.mad:1652`, `src/LO_SYN.mad:2995` | 5 |
| `ME7523` | `77523B` | `src/LO_SYN.mad:276` | `src/LO_SYN.mad:1501` | 1 |
| `RG0105` | `105B` | `src/LO_SYN.mad:277` | `src/LO_SYN.mad:1525`, `src/LO_SYN.mad:1810`, `src/LO_SYN.mad:1828`, `src/LO_SYN.mad:1852`, `src/LO_SYN.mad:1873`, `src/LO_SYN.mad:1894` | 6 |
| `ME2511` | `2511B` | `src/LO_SYN.mad:278` | `src/LO_SYN.mad:1526`, `src/LO_SYN.mad:1811`, `src/LO_SYN.mad:1829`, `src/LO_SYN.mad:1853`, `src/LO_SYN.mad:1874`, `src/LO_SYN.mad:1895` | 6 |
| `RG7014` | `70146B` | `src/LO_SYN.mad:279` | `src/LO_SYN.mad:1528` | 1 |
| `ME6170` | `6170B` | `src/LO_SYN.mad:280` | `src/LO_SYN.mad:1531` | 1 |
| `EX2016` | `20160B` | `src/LO_SYN.mad:281` | `src/LO_SYN.mad:1532` | 1 |
| `EX5517` | `5517B` | `src/LO_SYN.mad:282` | `src/LO_SYN.mad:1549`, `src/LO_SYN.mad:2720` | 2 |
| `EX4256` | `42560B` | `src/LO_SYN.mad:283` | `src/LO_SYN.mad:1552` | 1 |
| `ME0502` | `502B` | `src/LO_SYN.mad:284` | `src/LO_SYN.mad:1553` | 1 |
| `AP6617` | `66170B` | `src/LO_SYN.mad:285` | `src/LO_SYN.mad:1555`, `src/LO_SYN.mad:2974` | 2 |
| `EX4744` | `47440B` | `src/LO_SYN.mad:286` | `src/LO_SYN.mad:1556` | 1 |
| `RG4054` | `40544B` | `src/LO_SYN.mad:287` | `src/LO_SYN.mad:1558`, `src/LO_SYN.mad:2699` | 2 |
| `ME4040` | `4040B` | `src/LO_SYN.mad:288` | `src/LO_SYN.mad:1559` | 1 |
| `AP4414` | `44144B` | `src/LO_SYN.mad:289` | `src/LO_SYN.mad:1561`, `src/LO_SYN.mad:1564`, `src/LO_SYN.mad:1840`, `src/LO_SYN.mad:1955`, `src/LO_SYN.mad:1996` | 5 |
| `ME7550` | `75503B` | `src/LO_SYN.mad:290` | `src/LO_SYN.mad:1562`, `src/LO_SYN.mad:1822`, `src/LO_SYN.mad:1987`, `src/LO_SYN.mad:2138` | 4 |
| `EX4144` | `41440B` | `src/LO_SYN.mad:291` | `src/LO_SYN.mad:1565`, `src/LO_SYN.mad:1781`, `src/LO_SYN.mad:1841`, `src/LO_SYN.mad:1957`, `src/LO_SYN.mad:1997` | 5 |
| `RG7251` | `72510B` | `src/LO_SYN.mad:292` | `src/LO_SYN.mad:1568` | 1 |
| `AP4644` | `46440B` | `src/LO_SYN.mad:293` | `src/LO_SYN.mad:1574`, `src/LO_SYN.mad:1921` | 2 |
| `EX2062` | `62113B` | `src/LO_SYN.mad:294` | `src/LO_SYN.mad:1577`, `src/LO_SYN.mad:1757`, `src/LO_SYN.mad:1862`, `src/LO_SYN.mad:1972`, `src/LO_SYN.mad:2836` | 5 |
| `EX0110` | `110B` | `src/LO_SYN.mad:295` | `src/LO_SYN.mad:1579` | 1 |
| `ME7014` | `70143B` | `src/LO_SYN.mad:296` | `src/LO_SYN.mad:1580` | 1 |
| `ME7611` | `76117B` | `src/LO_SYN.mad:297` | `src/LO_SYN.mad:1582`, `src/LO_SYN.mad:1723`, `src/LO_SYN.mad:2876` | 3 |
| `EX2440` | `42440B` | `src/LO_SYN.mad:298` | `src/LO_SYN.mad:1585`, `src/LO_SYN.mad:1865`, `src/LO_SYN.mad:2002`, `src/LO_SYN.mad:2183`, `src/LO_SYN.mad:2240`, `src/LO_SYN.mad:2264` … (+13) | 19 |
| `EX3651` | `20151B` | `src/LO_SYN.mad:299` | `src/LO_SYN.mad:1591`, `src/LO_SYN.mad:2351` | 2 |
| `ME4513` | `4513B` | `src/LO_SYN.mad:300` | `src/LO_SYN.mad:1627`, `src/LO_SYN.mad:1634` | 2 |
| `ME7450` | `74501B` | `src/LO_SYN.mad:301` | `src/LO_SYN.mad:1630`, `src/LO_SYN.mad:1867` | 2 |
| `EX3644` | `44040B` | `src/LO_SYN.mad:302` | `src/LO_SYN.mad:1633` | 1 |
| `RG0110` | `110B` | `src/LO_SYN.mad:303` | `src/LO_SYN.mad:1636` | 1 |
| `ME0006` | `70102B` | `src/LO_SYN.mad:304` | `src/LO_SYN.mad:1637` | 1 |
| `ME0554` | `554B` | `src/LO_SYN.mad:305` | `src/LO_SYN.mad:1639` | 1 |
| `RG7050` | `70502B` | `src/LO_SYN.mad:306` | `src/LO_SYN.mad:1640` | 1 |
| `AP5211` | `52110B` | `src/LO_SYN.mad:307` | `src/LO_SYN.mad:1642` | 1 |
| `EX4644` | `46440B` | `src/LO_SYN.mad:308` | `src/LO_SYN.mad:1643`, `src/LO_SYN.mad:2254`, `src/LO_SYN.mad:2704` | 3 |
| `ME7520` | `7520B` | `src/LO_SYN.mad:309` | `src/LO_SYN.mad:1645` | 1 |
| `ME2113` | `2113B` | `src/LO_SYN.mad:310` | `src/LO_SYN.mad:1646` | 1 |
| `RG7411` | `74117B` | `src/LO_SYN.mad:311` | `src/LO_SYN.mad:1673`, `src/LO_SYN.mad:2144`, `src/LO_SYN.mad:2621`, `src/LO_SYN.mad:2639`, `src/LO_SYN.mad:2660`, `src/LO_SYN.mad:3229` | 6 |
| `EX3642` | `42440B` | `src/LO_SYN.mad:312` | `src/LO_SYN.mad:1679`, `src/LO_SYN.mad:2458`, `src/LO_SYN.mad:2887`, `src/LO_SYN.mad:3184`, `src/LO_SYN.mad:3238` | 5 |
| `EX0124` | `20124B` | `src/LO_SYN.mad:313` | `src/LO_SYN.mad:1685`, `src/LO_SYN.mad:1952`, `src/LO_SYN.mad:2689` | 3 |
| `AP7004` | `70040B` | `src/LO_SYN.mad:314` | `src/LO_SYN.mad:1687`, `src/LO_SYN.mad:1954` | 2 |
| `EX4050` | `40503B` | `src/LO_SYN.mad:315` | `src/LO_SYN.mad:1694`, `src/LO_SYN.mad:1762` | 2 |
| `EX4502` | `4502B` | `src/LO_SYN.mad:316` | `src/LO_SYN.mad:1696`, `src/LO_SYN.mad:1763` | 2 |
| `AP4650` | `46502B` | `src/LO_SYN.mad:317` | `src/LO_SYN.mad:1711`, `src/LO_SYN.mad:2059`, `src/LO_SYN.mad:2089` | 3 |
| `EX6604` | `66040B` | `src/LO_SYN.mad:318` | `src/LO_SYN.mad:1712`, `src/LO_SYN.mad:2060`, `src/LO_SYN.mad:2090` | 3 |
| `ME7756` | `77560B` | `src/LO_SYN.mad:319` | `src/LO_SYN.mad:1714`, `src/LO_SYN.mad:1918` | 2 |
| `AP4152` | `41524B` | `src/LO_SYN.mad:320` | `src/LO_SYN.mad:1715`, `src/LO_SYN.mad:1919`, `src/LO_SYN.mad:2705` | 3 |
| `AP6501` | `46501B` | `src/LO_SYN.mad:321` | `src/LO_SYN.mad:1717` | 1 |
| `EX4113` | `74113B` | `src/LO_SYN.mad:322` | `src/LO_SYN.mad:1720` | 1 |
| `EX3643` | `20143B` | `src/LO_SYN.mad:323` | `src/LO_SYN.mad:1721`, `src/LO_SYN.mad:2861` | 2 |
| `EX6450` | `64503B` | `src/LO_SYN.mad:324` | `src/LO_SYN.mad:1724` | 1 |
| `EX4056` | `40561B` | `src/LO_SYN.mad:325` | `src/LO_SYN.mad:1727`, `src/LO_SYN.mad:2405` | 2 |
| `ME5517` | `5517B` | `src/LO_SYN.mad:326` | `src/LO_SYN.mad:1729`, `src/LO_SYN.mad:2813`, `src/LO_SYN.mad:3043`, `src/LO_SYN.mad:3046` | 4 |
| `EX2047` | `47505B` | `src/LO_SYN.mad:327` | `src/LO_SYN.mad:1735` | 1 |
| `AP1501` | `41501B` | `src/LO_SYN.mad:328` | `src/LO_SYN.mad:1738` | 1 |
| `EX4505` | `64505B` | `src/LO_SYN.mad:329` | `src/LO_SYN.mad:1739`, `src/LO_SYN.mad:3188`, `src/LO_SYN.mad:3242`, `src/LO_SYN.mad:3283` | 4 |
| `EX0144` | `20144B` | `src/LO_SYN.mad:330` | `src/LO_SYN.mad:1751` | 1 |
| `AP4056` | `40560B` | `src/LO_SYN.mad:331` | `src/LO_SYN.mad:1753` | 1 |
| `ME5117` | `5117B` | `src/LO_SYN.mad:332` | `src/LO_SYN.mad:1754` | 1 |
| `EX2051` | `20151B` | `src/LO_SYN.mad:333` | `src/LO_SYN.mad:1756` | 1 |
| `EX0040` | `40B` | `src/LO_SYN.mad:334` | `src/LO_SYN.mad:1759` | 1 |
| `EX0147` | `20147B` | `src/LO_SYN.mad:335` | `src/LO_SYN.mad:1775` | 1 |
| `AP6144` | `61440B` | `src/LO_SYN.mad:336` | `src/LO_SYN.mad:1778` | 1 |
| `EX4414` | `44144B` | `src/LO_SYN.mad:337` | `src/LO_SYN.mad:1780` | 1 |
| `EX7050` | `70505B` | `src/LO_SYN.mad:338` | `src/LO_SYN.mad:1801` | 1 |
| `ME7156` | `71561B` | `src/LO_SYN.mad:339` | `src/LO_SYN.mad:1802` | 1 |
| `RG7051` | `70514B` | `src/LO_SYN.mad:340` | `src/LO_SYN.mad:1813` | 1 |
| `ME6161` | `6161B` | `src/LO_SYN.mad:341` | `src/LO_SYN.mad:1816` | 1 |
| `MV7010` | `70103B` | `src/LO_SYN.mad:342` | `src/LO_SYN.mad:1819`, `src/LO_SYN.mad:1969` | 2 |
| `ME4510` | `4510B` | `src/LO_SYN.mad:343` | `src/LO_SYN.mad:1820`, `src/LO_SYN.mad:1985`, `src/LO_SYN.mad:2093`, `src/LO_SYN.mad:2137`, `src/LO_SYN.mad:2407`, `src/LO_SYN.mad:3244` … (+1) | 7 |
| `ME0566` | `566B` | `src/LO_SYN.mad:344` | `src/LO_SYN.mad:1825`, `src/LO_SYN.mad:1990`, `src/LO_SYN.mad:2065` | 3 |
| `RG7011` | `70110B` | `src/LO_SYN.mad:345` | `src/LO_SYN.mad:1831`, `src/LO_SYN.mad:1876`, `src/LO_SYN.mad:2213` | 3 |
| `ME7151` | `71517B` | `src/LO_SYN.mad:346` | `src/LO_SYN.mad:1832`, `src/LO_SYN.mad:2759`, `src/LO_SYN.mad:2780` | 3 |
| `EX4755` | `47554B` | `src/LO_SYN.mad:347` | `src/LO_SYN.mad:1837`, `src/LO_SYN.mad:1993`, `src/LO_SYN.mad:2459`, `src/LO_SYN.mad:2929`, `src/LO_SYN.mad:3028` | 5 |
| `AP7704` | `77040B` | `src/LO_SYN.mad:348` | `src/LO_SYN.mad:1838`, `src/LO_SYN.mad:1994`, `src/LO_SYN.mad:2203`, `src/LO_SYN.mad:2224`, `src/LO_SYN.mad:2461`, `src/LO_SYN.mad:2930` … (+1) | 7 |
| `MV7004` | `70040B` | `src/LO_SYN.mad:349` | `src/LO_SYN.mad:1849`, `src/LO_SYN.mad:1891`, `src/LO_SYN.mad:1946`, `src/LO_SYN.mad:2437`, `src/LO_SYN.mad:2539`, `src/LO_SYN.mad:2743` … (+1) | 7 |
| `RG7016` | `70160B` | `src/LO_SYN.mad:350` | `src/LO_SYN.mad:1855`, `src/LO_SYN.mad:1897` | 2 |
| `ME7644` | `76440B` | `src/LO_SYN.mad:351` | `src/LO_SYN.mad:1859`, `src/LO_SYN.mad:1928`, `src/LO_SYN.mad:1967`, `src/LO_SYN.mad:2030`, `src/LO_SYN.mad:2303`, `src/LO_SYN.mad:2321` … (+1) | 7 |
| `MV7015` | `70151B` | `src/LO_SYN.mad:352` | `src/LO_SYN.mad:1861`, `src/LO_SYN.mad:2131` | 2 |
| `EX0102` | `102B` | `src/LO_SYN.mad:353` | `src/LO_SYN.mad:1864`, `src/LO_SYN.mad:1973` | 2 |
| `EX4410` | `44101B` | `src/LO_SYN.mad:354` | `src/LO_SYN.mad:1870` | 1 |
| `ME0002` | `72117B` | `src/LO_SYN.mad:355` | `src/LO_SYN.mad:1877` | 1 |
| `ME4515` | `74515B` | `src/LO_SYN.mad:356` | `src/LO_SYN.mad:1880` | 1 |
| `ME4560` | `4560B` | `src/LO_SYN.mad:357` | `src/LO_SYN.mad:1882` | 1 |
| `EX5212` | `52120B` | `src/LO_SYN.mad:358` | `src/LO_SYN.mad:1883` | 1 |
| `ME7411` | `74110B` | `src/LO_SYN.mad:359` | `src/LO_SYN.mad:1888` | 1 |
| `EX6504` | `65040B` | `src/LO_SYN.mad:360` | `src/LO_SYN.mad:1889`, `src/LO_SYN.mad:2435`, `src/LO_SYN.mad:3196` | 3 |
| `ME5110` | `5110B` | `src/LO_SYN.mad:361` | `src/LO_SYN.mad:1901`, `src/LO_SYN.mad:2380` | 2 |
| `ME0503` | `503B` | `src/LO_SYN.mad:362` | `src/LO_SYN.mad:1906` | 1 |
| `EX0013` | `64520B` | `src/LO_SYN.mad:363` | `src/LO_SYN.mad:1907` | 1 |
| `EX4651` | `46517B` | `src/LO_SYN.mad:364` | `src/LO_SYN.mad:1912` | 1 |
| `MV0102` | `70102B` | `src/LO_SYN.mad:365` | `src/LO_SYN.mad:1915`, `src/LO_SYN.mad:2062`, `src/LO_SYN.mad:2092`, `src/LO_SYN.mad:3251` | 4 |
| `EX2117` | `2117B` | `src/LO_SYN.mad:366` | `src/LO_SYN.mad:1922` | 1 |
| `ME7510` | `7510B` | `src/LO_SYN.mad:367` | `src/LO_SYN.mad:1924` | 1 |
| `MV7016` | `70160B` | `src/LO_SYN.mad:368` | `src/LO_SYN.mad:1930`, `src/LO_SYN.mad:2347` | 2 |
| `EX4112` | `41124B` | `src/LO_SYN.mad:369` | `src/LO_SYN.mad:1931`, `src/LO_SYN.mad:2348` | 2 |
| `EX3650` | `50110B` | `src/LO_SYN.mad:370` | `src/LO_SYN.mad:1933`, `src/LO_SYN.mad:2350` | 2 |
| `EX3620` | `20102B` | `src/LO_SYN.mad:371` | `src/LO_SYN.mad:1934` | 1 |
| `RG2544` | `2544B` | `src/LO_SYN.mad:372` | `src/LO_SYN.mad:1936` | 1 |
| `ME7410` | `74101B` | `src/LO_SYN.mad:373` | `src/LO_SYN.mad:1937` | 1 |
| `EX5110` | `51105B` | `src/LO_SYN.mad:374` | `src/LO_SYN.mad:1943` | 1 |
| `EX7522` | `7522B` | `src/LO_SYN.mad:375` | `src/LO_SYN.mad:1945` | 1 |
| `EX4520` | `4520B` | `src/LO_SYN.mad:376` | `src/LO_SYN.mad:1958`, `src/LO_SYN.mad:1999`, `src/LO_SYN.mad:2140`, `src/LO_SYN.mad:2204`, `src/LO_SYN.mad:2372`, `src/LO_SYN.mad:2591` … (+2) | 8 |
| `ME3040` | `3040B` | `src/LO_SYN.mad:377` | `src/LO_SYN.mad:1960`, `src/LO_SYN.mad:2000`, `src/LO_SYN.mad:2141`, `src/LO_SYN.mad:2206`, `src/LO_SYN.mad:2374`, `src/LO_SYN.mad:2627` … (+1) | 7 |
| `MV0151` | `151B` | `src/LO_SYN.mad:378` | `src/LO_SYN.mad:1970` | 1 |
| `AP5010` | `50101B` | `src/LO_SYN.mad:379` | `src/LO_SYN.mad:1975`, `src/LO_SYN.mad:2953`, `src/LO_SYN.mad:2987` | 3 |
| `RG7004` | `70040B` | `src/LO_SYN.mad:380` | `src/LO_SYN.mad:1976`, `src/LO_SYN.mad:3278` | 2 |
| `EX0151` | `151B` | `src/LO_SYN.mad:381` | `src/LO_SYN.mad:1982`, `src/LO_SYN.mad:2444`, `src/LO_SYN.mad:2560`, `src/LO_SYN.mad:2579`, `src/LO_SYN.mad:2798`, `src/LO_SYN.mad:2810` | 6 |
| `EX5505` | `5505B` | `src/LO_SYN.mad:382` | `src/LO_SYN.mad:1984`, `src/LO_SYN.mad:2446`, `src/LO_SYN.mad:2581`, `src/LO_SYN.mad:2800`, `src/LO_SYN.mad:2812` | 5 |
| `EX7517` | `7517B` | `src/LO_SYN.mad:383` | `src/LO_SYN.mad:2003` | 1 |
| `ME7110` | `71105B` | `src/LO_SYN.mad:384` | `src/LO_SYN.mad:2005` | 1 |
| `MV7012` | `70120B` | `src/LO_SYN.mad:385` | `src/LO_SYN.mad:2006`, `src/LO_SYN.mad:2032` | 2 |
| `ME5115` | `5115B` | `src/LO_SYN.mad:386` | `src/LO_SYN.mad:2008` | 1 |
| `ME0001` | `70110B` | `src/LO_SYN.mad:387` | `src/LO_SYN.mad:2009`, `src/LO_SYN.mad:2971`, `src/LO_SYN.mad:3025`, `src/LO_SYN.mad:3182`, `src/LO_SYN.mad:3203`, `src/LO_SYN.mad:3236` | 6 |
| `EX3641` | `41524B` | `src/LO_SYN.mad:388` | `src/LO_SYN.mad:2011`, `src/LO_SYN.mad:3059` | 2 |
| `AP2011` | `20115B` | `src/LO_SYN.mad:389` | `src/LO_SYN.mad:2012` | 1 |
| `ME1503` | `1503B` | `src/LO_SYN.mad:390` | `src/LO_SYN.mad:2014` | 1 |
| `AP4110` | `41101B` | `src/LO_SYN.mad:391` | `src/LO_SYN.mad:2015` | 1 |
| `EX7010` | `70105B` | `src/LO_SYN.mad:392` | `src/LO_SYN.mad:2021`, `src/LO_SYN.mad:2078` | 2 |
| `ME0524` | `524B` | `src/LO_SYN.mad:393` | `src/LO_SYN.mad:2023`, `src/LO_SYN.mad:2170` | 2 |
| `EX6313` | `63131B` | `src/LO_SYN.mad:394` | `src/LO_SYN.mad:2024` | 1 |
| `EX4554` | `45543B` | `src/LO_SYN.mad:395` | `src/LO_SYN.mad:2026` | 1 |
| `EX0117` | `117B` | `src/LO_SYN.mad:396` | `src/LO_SYN.mad:2036`, `src/LO_SYN.mad:2353` | 2 |
| `EX4172` | `74172B` | `src/LO_SYN.mad:397` | `src/LO_SYN.mad:2038`, `src/LO_SYN.mad:2354` | 2 |
| `ME1523` | `1523B` | `src/LO_SYN.mad:398` | `src/LO_SYN.mad:2041`, `src/LO_SYN.mad:2483`, `src/LO_SYN.mad:2519` | 3 |
| `AP4351` | `43516B` | `src/LO_SYN.mad:399` | `src/LO_SYN.mad:2042`, `src/LO_SYN.mad:2485`, `src/LO_SYN.mad:2521` | 3 |
| `ME0011` | `74510B` | `src/LO_SYN.mad:400` | `src/LO_SYN.mad:2044` | 1 |
| `EX6144` | `61440B` | `src/LO_SYN.mad:401` | `src/LO_SYN.mad:2045` | 1 |
| `ME7504` | `75040B` | `src/LO_SYN.mad:402` | `src/LO_SYN.mad:2048` | 1 |
| `ME0147` | `147B` | `src/LO_SYN.mad:403` | `src/LO_SYN.mad:2050`, `src/LO_SYN.mad:2462` | 2 |
| `EX0016` | `62101B` | `src/LO_SYN.mad:404` | `src/LO_SYN.mad:2071` | 1 |
| `ME0543` | `543B` | `src/LO_SYN.mad:405` | `src/LO_SYN.mad:2080` | 1 |
| `EX2120` | `2120B` | `src/LO_SYN.mad:406` | `src/LO_SYN.mad:2095`, `src/LO_SYN.mad:2408`, `src/LO_SYN.mad:2524`, `src/LO_SYN.mad:3208`, `src/LO_SYN.mad:3245`, `src/LO_SYN.mad:3308` | 6 |
| `AP4544` | `45440B` | `src/LO_SYN.mad:407` | `src/LO_SYN.mad:2096`, `src/LO_SYN.mad:2410`, `src/LO_SYN.mad:2525` | 3 |
| `EX1101` | `1101B` | `src/LO_SYN.mad:408` | `src/LO_SYN.mad:2099`, `src/LO_SYN.mad:2120` | 2 |
| `AP4104` | `41040B` | `src/LO_SYN.mad:409` | `src/LO_SYN.mad:2101`, `src/LO_SYN.mad:2122` | 2 |
| `AP4410` | `44103B` | `src/LO_SYN.mad:410` | `src/LO_SYN.mad:2108`, `src/LO_SYN.mad:2209`, `src/LO_SYN.mad:2468`, `src/LO_SYN.mad:3110` | 4 |
| `ME7013` | `70131B` | `src/LO_SYN.mad:411` | `src/LO_SYN.mad:2110`, `src/LO_SYN.mad:2210`, `src/LO_SYN.mad:2470`, `src/LO_SYN.mad:3112`, `src/LO_SYN.mad:3271` | 5 |
| `EX0021` | `20160B` | `src/LO_SYN.mad:412` | `src/LO_SYN.mad:2111`, `src/LO_SYN.mad:2570`, `src/LO_SYN.mad:2890`, `src/LO_SYN.mad:2945`, `src/LO_SYN.mad:3139` | 5 |
| `RG0551` | `551B` | `src/LO_SYN.mad:413` | `src/LO_SYN.mad:2114` | 1 |
| `RG0040` | `40B` | `src/LO_SYN.mad:414` | `src/LO_SYN.mad:2116`, `src/LO_SYN.mad:2564`, `src/LO_SYN.mad:2584`, `src/LO_SYN.mad:3301` | 4 |
| `ME7650` | `76505B` | `src/LO_SYN.mad:415` | `src/LO_SYN.mad:2125`, `src/LO_SYN.mad:2360`, `src/LO_SYN.mad:2384`, `src/LO_SYN.mad:2510`, `src/LO_SYN.mad:2855`, `src/LO_SYN.mad:3032` | 6 |
| `EX2043` | `20143B` | `src/LO_SYN.mad:416` | `src/LO_SYN.mad:2126`, `src/LO_SYN.mad:2362`, `src/LO_SYN.mad:2386` | 3 |
| `AP4555` | `45554B` | `src/LO_SYN.mad:417` | `src/LO_SYN.mad:2128`, `src/LO_SYN.mad:2363`, `src/LO_SYN.mad:2387`, `src/LO_SYN.mad:2863` | 4 |
| `EX6570` | `70101B` | `src/LO_SYN.mad:418` | `src/LO_SYN.mad:2134`, `src/LO_SYN.mad:2827` | 2 |
| `EX6454` | `64543B` | `src/LO_SYN.mad:419` | `src/LO_SYN.mad:2135`, `src/LO_SYN.mad:2828` | 2 |
| `EX4053` | `40530B` | `src/LO_SYN.mad:420` | `src/LO_SYN.mad:2152` | 1 |
| `MV7011` | `70110B` | `src/LO_SYN.mad:421` | `src/LO_SYN.mad:2155` | 1 |
| `EX6552` | `6552B` | `src/LO_SYN.mad:422` | `src/LO_SYN.mad:2164` | 1 |
| `ME6505` | `6505B` | `src/LO_SYN.mad:423` | `src/LO_SYN.mad:2165`, `src/LO_SYN.mad:2488`, `src/LO_SYN.mad:2599`, `src/LO_SYN.mad:3187` | 4 |
| `ME7555` | `75551B` | `src/LO_SYN.mad:424` | `src/LO_SYN.mad:2167` | 1 |
| `EX4544` | `45440B` | `src/LO_SYN.mad:425` | `src/LO_SYN.mad:2174` | 1 |
| `EX7550` | `75505B` | `src/LO_SYN.mad:426` | `src/LO_SYN.mad:2177` | 1 |
| `ME1455` | `1455B` | `src/LO_SYN.mad:427` | `src/LO_SYN.mad:2179` | 1 |
| `ME7744` | `77440B` | `src/LO_SYN.mad:428` | `src/LO_SYN.mad:2182`, `src/LO_SYN.mad:2263`, `src/LO_SYN.mad:2501`, `src/LO_SYN.mad:2506` | 4 |
| `EX4524` | `4524B` | `src/LO_SYN.mad:429` | `src/LO_SYN.mad:2188`, `src/LO_SYN.mad:2276`, `src/LO_SYN.mad:2312`, `src/LO_SYN.mad:2330`, `src/LO_SYN.mad:2869` | 5 |
| `EX2002` | `20102B` | `src/LO_SYN.mad:430` | `src/LO_SYN.mad:2189`, `src/LO_SYN.mad:3034` | 2 |
| `ME6117` | `6117B` | `src/LO_SYN.mad:431` | `src/LO_SYN.mad:2191` | 1 |
| `EX7457` | `74576B` | `src/LO_SYN.mad:432` | `src/LO_SYN.mad:2192` | 1 |
| `ME4506` | `4506B` | `src/LO_SYN.mad:433` | `src/LO_SYN.mad:2194`, `src/LO_SYN.mad:3290` | 2 |
| `EX7547` | `47547B` | `src/LO_SYN.mad:434` | `src/LO_SYN.mad:2201`, `src/LO_SYN.mad:2222` | 2 |
| `EX0111` | `20111B` | `src/LO_SYN.mad:435` | `src/LO_SYN.mad:2212` | 1 |
| `EX3673` | `73105B` | `src/LO_SYN.mad:436` | `src/LO_SYN.mad:2216`, `src/LO_SYN.mad:3286` | 2 |
| `AP4304` | `43040B` | `src/LO_SYN.mad:437` | `src/LO_SYN.mad:2225`, `src/LO_SYN.mad:3215`, `src/LO_SYN.mad:3266` | 3 |
| `EX7752` | `77524B` | `src/LO_SYN.mad:438` | `src/LO_SYN.mad:2231`, `src/LO_SYN.mad:2255` | 2 |
| `AP4155` | `41554B` | `src/LO_SYN.mad:439` | `src/LO_SYN.mad:2251` | 1 |
| `MV0144` | `70144B` | `src/LO_SYN.mad:440` | `src/LO_SYN.mad:2272`, `src/LO_SYN.mad:2308`, `src/LO_SYN.mad:2326`, `src/LO_SYN.mad:2455` | 4 |
| `EX6616` | `66166B` | `src/LO_SYN.mad:441` | `src/LO_SYN.mad:2273`, `src/LO_SYN.mad:2309`, `src/LO_SYN.mad:2327`, `src/LO_SYN.mad:2866`, `src/LO_SYN.mad:3092` | 5 |
| `EX0005` | `40440B` | `src/LO_SYN.mad:442` | `src/LO_SYN.mad:2275`, `src/LO_SYN.mad:2311`, `src/LO_SYN.mad:2329`, `src/LO_SYN.mad:2452`, `src/LO_SYN.mad:2867` | 5 |
| `EX0002` | `20117B` | `src/LO_SYN.mad:443` | `src/LO_SYN.mad:2278`, `src/LO_SYN.mad:3118` | 2 |
| `EX2064` | `64566B` | `src/LO_SYN.mad:444` | `src/LO_SYN.mad:2284` | 1 |
| `EX4513` | `4513B` | `src/LO_SYN.mad:445` | `src/LO_SYN.mad:2297`, `src/LO_SYN.mad:2305`, `src/LO_SYN.mad:2323`, `src/LO_SYN.mad:2647`, `src/LO_SYN.mad:3254` | 5 |
| `EX2003` | `20103B` | `src/LO_SYN.mad:446` | `src/LO_SYN.mad:2314`, `src/LO_SYN.mad:2870` | 2 |
| `EX2024` | `20124B` | `src/LO_SYN.mad:447` | `src/LO_SYN.mad:2332` | 1 |
| `AP7010` | `70101B` | `src/LO_SYN.mad:448` | `src/LO_SYN.mad:2333` | 1 |
| `ME4516` | `4516B` | `src/LO_SYN.mad:449` | `src/LO_SYN.mad:2335` | 1 |
| `ME7250` | `72507B` | `src/LO_SYN.mad:450` | `src/LO_SYN.mad:2336` | 1 |
| `ME1105` | `1105B` | `src/LO_SYN.mad:451` | `src/LO_SYN.mad:2341` | 1 |
| `ME6040` | `6040B` | `src/LO_SYN.mad:452` | `src/LO_SYN.mad:2342` | 1 |
| `ME7711` | `77110B` | `src/LO_SYN.mad:453` | `src/LO_SYN.mad:2377`, `src/LO_SYN.mad:2885` | 2 |
| `EX6351` | `63517B` | `src/LO_SYN.mad:454` | `src/LO_SYN.mad:2378`, `src/LO_SYN.mad:2924`, `src/LO_SYN.mad:3001`, `src/LO_SYN.mad:3011` | 4 |
| `ME7040` | `7040B` | `src/LO_SYN.mad:455` | `src/LO_SYN.mad:2381` | 1 |
| `RG0547` | `40547B` | `src/LO_SYN.mad:456` | `src/LO_SYN.mad:2396` | 1 |
| `EX6611` | `66117B` | `src/LO_SYN.mad:457` | `src/LO_SYN.mad:2398` | 1 |
| `RG5505` | `5505B` | `src/LO_SYN.mad:458` | `src/LO_SYN.mad:2399` | 1 |
| `ME7051` | `70510B` | `src/LO_SYN.mad:459` | `src/LO_SYN.mad:2404` | 1 |
| `ME2170` | `2170B` | `src/LO_SYN.mad:460` | `src/LO_SYN.mad:2419`, `src/LO_SYN.mad:3098` | 2 |
| `EX6040` | `66040B` | `src/LO_SYN.mad:461` | `src/LO_SYN.mad:2422`, `src/LO_SYN.mad:2431` | 2 |
| `ME4524` | `4524B` | `src/LO_SYN.mad:462` | `src/LO_SYN.mad:2428` | 1 |
| `EX0115` | `115B` | `src/LO_SYN.mad:463` | `src/LO_SYN.mad:2432` | 1 |
| `EX7004` | `70040B` | `src/LO_SYN.mad:464` | `src/LO_SYN.mad:2449` | 1 |
| `ME4547` | `4547B` | `src/LO_SYN.mad:465` | `src/LO_SYN.mad:2456` | 1 |
| `ME6114` | `6114B` | `src/LO_SYN.mad:466` | `src/LO_SYN.mad:2473` | 1 |
| `RG4044` | `40440B` | `src/LO_SYN.mad:467` | `src/LO_SYN.mad:2482`, `src/LO_SYN.mad:3178` | 2 |
| `ME0012` | `75501B` | `src/LO_SYN.mad:468` | `src/LO_SYN.mad:2489` | 1 |
| `EX6451` | `64510B` | `src/LO_SYN.mad:469` | `src/LO_SYN.mad:2522` | 1 |
| `EX6105` | `66105B` | `src/LO_SYN.mad:470` | `src/LO_SYN.mad:2555` | 1 |
| `EX5501` | `5501B` | `src/LO_SYN.mad:471` | `src/LO_SYN.mad:2561` | 1 |
| `ME1057` | `1057B` | `src/LO_SYN.mad:472` | `src/LO_SYN.mad:2563`, `src/LO_SYN.mad:2582` | 2 |
| `ME3054` | `3054B` | `src/LO_SYN.mad:473` | `src/LO_SYN.mad:2593` | 1 |
| `ME7616` | `76161B` | `src/LO_SYN.mad:474` | `src/LO_SYN.mad:2597` | 1 |
| `EX2017` | `20173B` | `src/LO_SYN.mad:475` | `src/LO_SYN.mad:2600` | 1 |
| `ME3440` | `3440B` | `src/LO_SYN.mad:476` | `src/LO_SYN.mad:2602` | 1 |
| `RG7502` | `7502B` | `src/LO_SYN.mad:477` | `src/LO_SYN.mad:2608` | 1 |
| `RG1117` | `1117B` | `src/LO_SYN.mad:478` | `src/LO_SYN.mad:2615`, `src/LO_SYN.mad:2633`, `src/LO_SYN.mad:2654` | 3 |
| `EX6115` | `61154B` | `src/LO_SYN.mad:479` | `src/LO_SYN.mad:2674` | 1 |
| `ME2120` | `2120B` | `src/LO_SYN.mad:480` | `src/LO_SYN.mad:2675` | 1 |
| `EX5010` | `50101B` | `src/LO_SYN.mad:481` | `src/LO_SYN.mad:2677` | 1 |
| `RG0117` | `20117B` | `src/LO_SYN.mad:482` | `src/LO_SYN.mad:2678` | 1 |
| `ME7452` | `74524B` | `src/LO_SYN.mad:483` | `src/LO_SYN.mad:2681` | 1 |
| `ME7157` | `71570B` | `src/LO_SYN.mad:484` | `src/LO_SYN.mad:2683` | 1 |
| `ME1124` | `1124B` | `src/LO_SYN.mad:485` | `src/LO_SYN.mad:2686` | 1 |
| `EX3601` | `50101B` | `src/LO_SYN.mad:486` | `src/LO_SYN.mad:2687` | 1 |
| `MV6520` | `6520B` | `src/LO_SYN.mad:487` | `src/LO_SYN.mad:2690` | 1 |
| `ME4151` | `4151B` | `src/LO_SYN.mad:488` | `src/LO_SYN.mad:2701` | 1 |
| `AP0110` | `20110B` | `src/LO_SYN.mad:489` | `src/LO_SYN.mad:2702`, `src/LO_SYN.mad:3089` | 2 |
| `MV6502` | `6502B` | `src/LO_SYN.mad:490` | `src/LO_SYN.mad:2707` | 1 |
| `EX0012` | `47515B` | `src/LO_SYN.mad:491` | `src/LO_SYN.mad:2713` | 1 |
| `ME7005` | `70055B` | `src/LO_SYN.mad:492` | `src/LO_SYN.mad:2716` | 1 |
| `EX1571` | `1571B` | `src/LO_SYN.mad:493` | `src/LO_SYN.mad:2735` | 1 |
| `EX0020` | `45505B` | `src/LO_SYN.mad:494` | `src/LO_SYN.mad:2737` | 1 |
| `ME4101` | `4101B` | `src/LO_SYN.mad:495` | `src/LO_SYN.mad:2738` | 1 |
| `EX7504` | `7504B` | `src/LO_SYN.mad:496` | `src/LO_SYN.mad:2756`, `src/LO_SYN.mad:2777` | 2 |
| `ME6104` | `76104B` | `src/LO_SYN.mad:497` | `src/LO_SYN.mad:2758`, `src/LO_SYN.mad:2779` | 2 |
| `AP4550` | `45501B` | `src/LO_SYN.mad:498` | `src/LO_SYN.mad:2768` | 1 |
| `RG0000` | `40510B` | `src/LO_SYN.mad:499` | `src/LO_SYN.mad:2770` | 1 |
| `AP6444` | `64440B` | `src/LO_SYN.mad:500` | `src/LO_SYN.mad:2771`, `src/LO_SYN.mad:3248` | 2 |
| `ME4546` | `4546B` | `src/LO_SYN.mad:501` | `src/LO_SYN.mad:2773` | 1 |
| `ME0007` | `70101B` | `src/LO_SYN.mad:502` | `src/LO_SYN.mad:2774` | 1 |
| `ME7052` | `70524B` | `src/LO_SYN.mad:503` | `src/LO_SYN.mad:2822`, `src/LO_SYN.mad:2843`, `src/LO_SYN.mad:2899` | 3 |
| `EX0160` | `160B` | `src/LO_SYN.mad:504` | `src/LO_SYN.mad:2837` | 1 |
| `ME0110` | `110B` | `src/LO_SYN.mad:505` | `src/LO_SYN.mad:2845`, `src/LO_SYN.mad:2900`, `src/LO_SYN.mad:2972` | 3 |
| `RG4110` | `41105B` | `src/LO_SYN.mad:506` | `src/LO_SYN.mad:2848` | 1 |
| `EX2110` | `2110B` | `src/LO_SYN.mad:507` | `src/LO_SYN.mad:2849` | 1 |
| `EX0003` | `20110B` | `src/LO_SYN.mad:508` | `src/LO_SYN.mad:2857` | 1 |
| `ME7050` | `70502B` | `src/LO_SYN.mad:509` | `src/LO_SYN.mad:2858` | 1 |
| `EX0015` | `47547B` | `src/LO_SYN.mad:510` | `src/LO_SYN.mad:2860` | 1 |
| `ME0144` | `144B` | `src/LO_SYN.mad:511` | `src/LO_SYN.mad:2864` | 1 |
| `EX0143` | `20143B` | `src/LO_SYN.mad:512` | `src/LO_SYN.mad:2875` | 1 |
| `EX7744` | `77440B` | `src/LO_SYN.mad:513` | `src/LO_SYN.mad:2878`, `src/LO_SYN.mad:3224` | 2 |
| `RG4410` | `44101B` | `src/LO_SYN.mad:514` | `src/LO_SYN.mad:2888`, `src/LO_SYN.mad:2950` | 2 |
| `ME0020` | `74117B` | `src/LO_SYN.mad:515` | `src/LO_SYN.mad:2906` | 1 |
| `RG0172` | `172B` | `src/LO_SYN.mad:516` | `src/LO_SYN.mad:2917` | 1 |
| `EX6455` | `64551B` | `src/LO_SYN.mad:517` | `src/LO_SYN.mad:2920` | 1 |
| `ME1110` | `1110B` | `src/LO_SYN.mad:518` | `src/LO_SYN.mad:2923`, `src/LO_SYN.mad:3010` | 2 |
| `RG0104` | `104B` | `src/LO_SYN.mad:519` | `src/LO_SYN.mad:2935`, `src/LO_SYN.mad:2980`, `src/LO_SYN.mad:3070` | 3 |
| `ME7117` | `71171B` | `src/LO_SYN.mad:520` | `src/LO_SYN.mad:2939` | 1 |
| `EX0505` | `40505B` | `src/LO_SYN.mad:521` | `src/LO_SYN.mad:2941` | 1 |
| `MV0113` | `70113B` | `src/LO_SYN.mad:522` | `src/LO_SYN.mad:2942` | 1 |
| `EX6615` | `66151B` | `src/LO_SYN.mad:523` | `src/LO_SYN.mad:2944` | 1 |
| `EX0006` | `20102B` | `src/LO_SYN.mad:524` | `src/LO_SYN.mad:2951` | 1 |
| `RG7010` | `70102B` | `src/LO_SYN.mad:525` | `src/LO_SYN.mad:2954`, `src/LO_SYN.mad:2989` | 2 |
| `EX7005` | `70055B` | `src/LO_SYN.mad:526` | `src/LO_SYN.mad:2983` | 1 |
| `ME7444` | `74440B` | `src/LO_SYN.mad:527` | `src/LO_SYN.mad:2984`, `src/LO_SYN.mad:3142` | 2 |
| `RG0102` | `102B` | `src/LO_SYN.mad:528` | `src/LO_SYN.mad:2986`, `src/LO_SYN.mad:3318` | 2 |
| `EX4054` | `40547B` | `src/LO_SYN.mad:529` | `src/LO_SYN.mad:3007` | 1 |
| `EX0142` | `20142B` | `src/LO_SYN.mad:530` | `src/LO_SYN.mad:3019` | 1 |
| `AP6616` | `66161B` | `src/LO_SYN.mad:531` | `src/LO_SYN.mad:3026` | 1 |
| `EX4573` | `4573B` | `src/LO_SYN.mad:532` | `src/LO_SYN.mad:3040` | 1 |
| `ME2524` | `2524B` | `src/LO_SYN.mad:533` | `src/LO_SYN.mad:3041`, `src/LO_SYN.mad:3077` | 2 |
| `EX6457` | `64576B` | `src/LO_SYN.mad:534` | `src/LO_SYN.mad:3044` | 1 |
| `EX6151` | `6151B` | `src/LO_SYN.mad:535` | `src/LO_SYN.mad:3049`, `src/LO_SYN.mad:3145` | 2 |
| `EX0017` | `20142B` | `src/LO_SYN.mad:536` | `src/LO_SYN.mad:3052`, `src/LO_SYN.mad:3148` | 2 |
| `EX0561` | `40561B` | `src/LO_SYN.mad:537` | `src/LO_SYN.mad:3055`, `src/LO_SYN.mad:3151`, `src/LO_SYN.mad:3175` | 3 |
| `ME5520` | `5520B` | `src/LO_SYN.mad:538` | `src/LO_SYN.mad:3056` | 1 |
| `EX2013` | `20113B` | `src/LO_SYN.mad:539` | `src/LO_SYN.mad:3061` | 1 |
| `EX3603` | `44103B` | `src/LO_SYN.mad:540` | `src/LO_SYN.mad:3062`, `src/LO_SYN.mad:3269` | 2 |
| `EX4257` | `42575B` | `src/LO_SYN.mad:541` | `src/LO_SYN.mad:3076` | 1 |
| `RG0160` | `160B` | `src/LO_SYN.mad:542` | `src/LO_SYN.mad:3080` | 1 |
| `ME2513` | `72513B` | `src/LO_SYN.mad:543` | `src/LO_SYN.mad:3085` | 1 |
| `EX4052` | `40520B` | `src/LO_SYN.mad:544` | `src/LO_SYN.mad:3086` | 1 |
| `ME0015` | `70144B` | `src/LO_SYN.mad:545` | `src/LO_SYN.mad:3091` | 1 |
| `EX7444` | `74440B` | `src/LO_SYN.mad:546` | `src/LO_SYN.mad:3094` | 1 |
| `RG1524` | `1524B` | `src/LO_SYN.mad:547` | `src/LO_SYN.mad:3095` | 1 |
| `ME2576` | `2576B` | `src/LO_SYN.mad:548` | `src/LO_SYN.mad:3097` | 1 |
| `EX3666` | `66110B` | `src/LO_SYN.mad:549` | `src/LO_SYN.mad:3106` | 1 |
| `AP5404` | `54040B` | `src/LO_SYN.mad:550` | `src/LO_SYN.mad:3109` | 1 |
| `AP6505` | `46505B` | `src/LO_SYN.mad:551` | `src/LO_SYN.mad:3124`, `src/LO_SYN.mad:3172` | 2 |
| `EX4440` | `64440B` | `src/LO_SYN.mad:552` | `src/LO_SYN.mad:3125` | 1 |
| `ME0055` | `55B` | `src/LO_SYN.mad:553` | `src/LO_SYN.mad:3127` | 1 |
| `EX0024` | `74440B` | `src/LO_SYN.mad:554` | `src/LO_SYN.mad:3128` | 1 |
| `ME6561` | `6561B` | `src/LO_SYN.mad:555` | `src/LO_SYN.mad:3140` | 1 |
| `ME2154` | `2154B` | `src/LO_SYN.mad:556` | `src/LO_SYN.mad:3152` | 1 |
| `AP4101` | `44101B` | `src/LO_SYN.mad:557` | `src/LO_SYN.mad:3154` | 1 |
| `ME1111` | `1111B` | `src/LO_SYN.mad:558` | `src/LO_SYN.mad:3155` | 1 |
| `MV7654` | `76543B` | `src/LO_SYN.mad:559` | `src/LO_SYN.mad:3157` | 1 |
| `EX4555` | `45551B` | `src/LO_SYN.mad:560` | `src/LO_SYN.mad:3160` | 1 |
| `ME0004` | `7544B` | `src/LO_SYN.mad:561` | `src/LO_SYN.mad:3169` | 1 |
| `RG0505` | `505B` | `src/LO_SYN.mad:562` | `src/LO_SYN.mad:3173` | 1 |
| `ME1101` | `1101B` | `src/LO_SYN.mad:563` | `src/LO_SYN.mad:3176` | 1 |
| `EX2502` | `42502B` | `src/LO_SYN.mad:564` | `src/LO_SYN.mad:3181`, `src/LO_SYN.mad:3202`, `src/LO_SYN.mad:3235` | 3 |
| `EX6112` | `61120B` | `src/LO_SYN.mad:565` | `src/LO_SYN.mad:3185` | 1 |
| `EX2101` | `2101B` | `src/LO_SYN.mad:566` | `src/LO_SYN.mad:3191` | 1 |
| `EX2001` | `62101B` | `src/LO_SYN.mad:567` | `src/LO_SYN.mad:3193` | 1 |
| `AP4554` | `45543B` | `src/LO_SYN.mad:568` | `src/LO_SYN.mad:3209`, `src/LO_SYN.mad:3247` | 2 |
| `AP7044` | `70440B` | `src/LO_SYN.mad:569` | `src/LO_SYN.mad:3211` | 1 |
| `AP4305` | `43055B` | `src/LO_SYN.mad:570` | `src/LO_SYN.mad:3212` | 1 |
| `ME0010` | `77104B` | `src/LO_SYN.mad:571` | `src/LO_SYN.mad:3214`, `src/LO_SYN.mad:3265` | 2 |
| `ME0021` | `74105B` | `src/LO_SYN.mad:572` | `src/LO_SYN.mad:3220` | 1 |
| `EX0004` | `20110B` | `src/LO_SYN.mad:573` | `src/LO_SYN.mad:3221` | 1 |
| `AP7710` | `77105B` | `src/LO_SYN.mad:574` | `src/LO_SYN.mad:3223` | 1 |
| `EX3645` | `45517B` | `src/LO_SYN.mad:575` | `src/LO_SYN.mad:3239` | 1 |
| `EX7710` | `77101B` | `src/LO_SYN.mad:576` | `src/LO_SYN.mad:3241` | 1 |
| `ME4111` | `74111B` | `src/LO_SYN.mad:577` | `src/LO_SYN.mad:3250` | 1 |
| `RG0113` | `113B` | `src/LO_SYN.mad:578` | `src/LO_SYN.mad:3268` | 1 |
| `EX6155` | `61551B` | `src/LO_SYN.mad:579` | `src/LO_SYN.mad:3272` | 1 |
| `AP0111` | `20111B` | `src/LO_SYN.mad:580` | `src/LO_SYN.mad:3274` | 1 |
| `RG7650` | `76505B` | `src/LO_SYN.mad:581` | `src/LO_SYN.mad:3275` | 1 |
| `EX4211` | `42111B` | `src/LO_SYN.mad:582` | `src/LO_SYN.mad:3277` | 1 |
| `EX0520` | `40520B` | `src/LO_SYN.mad:583` | `src/LO_SYN.mad:3280` | 1 |
| `AP7550` | `75505B` | `src/LO_SYN.mad:584` | `src/LO_SYN.mad:3281` | 1 |
| `EX4411` | `44117B` | `src/LO_SYN.mad:585` | `src/LO_SYN.mad:3287` | 1 |
| `EX2516` | `42516B` | `src/LO_SYN.mad:586` | `src/LO_SYN.mad:3292` | 1 |
| `ME0016` | `74506B` | `src/LO_SYN.mad:587` | `src/LO_SYN.mad:3293` | 1 |
| `ME4457` | `4457B` | `src/LO_SYN.mad:588` | `src/LO_SYN.mad:3295` | 1 |
| `EX6117` | `66117B` | `src/LO_SYN.mad:589` | `src/LO_SYN.mad:3299` | 1 |
| `ME7056` | `70561B` | `src/LO_SYN.mad:590` | `src/LO_SYN.mad:3305` | 1 |
| `SC0400` | `400B` | `src/LO_SYN.mad:591` | `src/LO_SYN.mad:3314`, `src/LO_SYN.mad:3323`, `src/LO_SYN.mad:3326`, `src/LO_SYN.mad:3329`, `src/LO_SYN.mad:3338`, `src/LO_SYN.mad:3350` … (+32) | 38 |
| `SC0101` | `101B` | `src/LO_SYN.mad:592` | `src/LO_SYN.mad:3315` | 1 |
| `SC0500` | `500B` | `src/LO_SYN.mad:593` | `src/LO_SYN.mad:3317`, `src/LO_SYN.mad:3320`, `src/LO_SYN.mad:3335`, `src/LO_SYN.mad:3344`, `src/LO_SYN.mad:3356`, `src/LO_SYN.mad:3359` … (+30) | 36 |
| `ME7031` | `70311B` | `src/LO_SYN.mad:594` | `src/LO_SYN.mad:3321` | 1 |
| `EX7031` | `70312B` | `src/LO_SYN.mad:595` | `src/LO_SYN.mad:3324` | 1 |
| `EX6070` | `70313B` | `src/LO_SYN.mad:596` | `src/LO_SYN.mad:3327` | 1 |
| `AP0314` | `314B` | `src/LO_SYN.mad:597` | `src/LO_SYN.mad:3330` | 1 |
| `SC0300` | `300B` | `src/LO_SYN.mad:598` | `src/LO_SYN.mad:3332`, `src/LO_SYN.mad:3341`, `src/LO_SYN.mad:3347`, `src/LO_SYN.mad:3353`, `src/LO_SYN.mad:3374`, `src/LO_SYN.mad:3377` … (+21) | 27 |
| `EX0317` | `317B` | `src/LO_SYN.mad:599` | `src/LO_SYN.mad:3339` | 1 |
| `SC0322` | `322B` | `src/LO_SYN.mad:600` | `src/LO_SYN.mad:3342` | 1 |
| `EX0323` | `323B` | `src/LO_SYN.mad:601` | `src/LO_SYN.mad:3345` | 1 |
| `SC7032` | `70324B` | `src/LO_SYN.mad:602` | `src/LO_SYN.mad:3348` | 1 |
| `EX7032` | `70325B` | `src/LO_SYN.mad:603` | `src/LO_SYN.mad:3351` | 1 |
| `EX0326` | `326B` | `src/LO_SYN.mad:604` | `src/LO_SYN.mad:3354` | 1 |
| `RG0327` | `327B` | `src/LO_SYN.mad:605` | `src/LO_SYN.mad:3357` | 1 |
| `SC0600` | `600B` | `src/LO_SYN.mad:606` | `src/LO_SYN.mad:3362`, `src/LO_SYN.mad:3416`, `src/LO_SYN.mad:3443`, `src/LO_SYN.mad:3557`, `src/LO_SYN.mad:3581`, `src/LO_SYN.mad:3674` … (+2) | 8 |
| `EX0501` | `501B` | `src/LO_SYN.mad:607` | `src/LO_SYN.mad:3363` | 1 |
| `RG0502` | `502B` | `src/LO_SYN.mad:608` | `src/LO_SYN.mad:3366` | 1 |
| `SC7050` | `70503B` | `src/LO_SYN.mad:609` | `src/LO_SYN.mad:3369` | 1 |
| `EX5070` | `70504B` | `src/LO_SYN.mad:610` | `src/LO_SYN.mad:3372` | 1 |
| `AP0505` | `505B` | `src/LO_SYN.mad:611` | `src/LO_SYN.mad:3375` | 1 |
| `RG0506` | `506B` | `src/LO_SYN.mad:612` | `src/LO_SYN.mad:3378` | 1 |
| `SC0700` | `700B` | `src/LO_SYN.mad:613` | `src/LO_SYN.mad:3380`, `src/LO_SYN.mad:3386`, `src/LO_SYN.mad:3398`, `src/LO_SYN.mad:3431`, `src/LO_SYN.mad:3503`, `src/LO_SYN.mad:3524` … (+9) | 15 |
| `RG0510` | `510B` | `src/LO_SYN.mad:614` | `src/LO_SYN.mad:3384` | 1 |
| `EX0512` | `512B` | `src/LO_SYN.mad:615` | `src/LO_SYN.mad:3390` | 1 |
| `EX7051` | `70513B` | `src/LO_SYN.mad:616` | `src/LO_SYN.mad:3393` | 1 |
| `EX0514` | `514B` | `src/LO_SYN.mad:617` | `src/LO_SYN.mad:3396` | 1 |
| `EX7100` | `71000B` | `src/LO_SYN.mad:618` | `src/LO_SYN.mad:3399` | 1 |
| `RG1002` | `1002B` | `src/LO_SYN.mad:619` | `src/LO_SYN.mad:3405` | 1 |
| `SC1000` | `1000B` | `src/LO_SYN.mad:620` | `src/LO_SYN.mad:3410`, `src/LO_SYN.mad:3584`, `src/LO_SYN.mad:3614`, `src/LO_SYN.mad:3713`, `src/LO_SYN.mad:3716`, `src/LO_SYN.mad:3719` | 6 |
| `RG1006` | `1006B` | `src/LO_SYN.mad:621` | `src/LO_SYN.mad:3414` | 1 |
| `SC7101` | `71013B` | `src/LO_SYN.mad:622` | `src/LO_SYN.mad:3417` | 1 |
| `EX7101` | `71015B` | `src/LO_SYN.mad:623` | `src/LO_SYN.mad:3420` | 1 |
| `EX1016` | `1016B` | `src/LO_SYN.mad:624` | `src/LO_SYN.mad:3423` | 1 |
| `RG1033` | `1033B` | `src/LO_SYN.mad:625` | `src/LO_SYN.mad:3435` | 1 |
| `RG1034` | `1034B` | `src/LO_SYN.mad:626` | `src/LO_SYN.mad:3438` | 1 |
| `RG1035` | `1035B` | `src/LO_SYN.mad:627` | `src/LO_SYN.mad:3441` | 1 |
| `ME7103` | `71037B` | `src/LO_SYN.mad:628` | `src/LO_SYN.mad:3444` | 1 |
| `EX7110` | `71101B` | `src/LO_SYN.mad:629` | `src/LO_SYN.mad:3447` | 1 |
| `RG1102` | `1102B` | `src/LO_SYN.mad:630` | `src/LO_SYN.mad:3450` | 1 |
| `EX6071` | `71105B` | `src/LO_SYN.mad:631` | `src/LO_SYN.mad:3453` | 1 |
| `AP1111` | `1111B` | `src/LO_SYN.mad:632` | `src/LO_SYN.mad:3456` | 1 |
| `RG1115` | `1115B` | `src/LO_SYN.mad:633` | `src/LO_SYN.mad:3465` | 1 |
| `ME1200` | `1200B` | `src/LO_SYN.mad:634` | `src/LO_SYN.mad:3468` | 1 |
| `EX1202` | `1202B` | `src/LO_SYN.mad:635` | `src/LO_SYN.mad:3474` | 1 |
| `RG1204` | `1204B` | `src/LO_SYN.mad:636` | `src/LO_SYN.mad:3477` | 1 |
| `SC7121` | `71213B` | `src/LO_SYN.mad:637` | `src/LO_SYN.mad:3480` | 1 |
| `RG1214` | `1214B` | `src/LO_SYN.mad:638` | `src/LO_SYN.mad:3483` | 1 |
| `EX7121` | `71215B` | `src/LO_SYN.mad:639` | `src/LO_SYN.mad:3486` | 1 |
| `RG1217` | `1217B` | `src/LO_SYN.mad:640` | `src/LO_SYN.mad:3489` | 1 |
| `RG1301` | `1301B` | `src/LO_SYN.mad:641` | `src/LO_SYN.mad:3492` | 1 |
| `EX1302` | `1302B` | `src/LO_SYN.mad:642` | `src/LO_SYN.mad:3495` | 1 |
| `RG1303` | `1303B` | `src/LO_SYN.mad:643` | `src/LO_SYN.mad:3498` | 1 |
| `EX1310` | `1310B` | `src/LO_SYN.mad:644` | `src/LO_SYN.mad:3504` | 1 |
| `EX1311` | `1311B` | `src/LO_SYN.mad:645` | `src/LO_SYN.mad:3507` | 1 |
| `ME7131` | `71312B` | `src/LO_SYN.mad:646` | `src/LO_SYN.mad:3510` | 1 |
| `EX7131` | `71313B` | `src/LO_SYN.mad:647` | `src/LO_SYN.mad:3513` | 1 |
| `AP1314` | `1314B` | `src/LO_SYN.mad:648` | `src/LO_SYN.mad:3516` | 1 |
| `RG1315` | `1315B` | `src/LO_SYN.mad:649` | `src/LO_SYN.mad:3519` | 1 |
| `SC1322` | `1322B` | `src/LO_SYN.mad:650` | `src/LO_SYN.mad:3528` | 1 |
| `EX1323` | `1323B` | `src/LO_SYN.mad:651` | `src/LO_SYN.mad:3531` | 1 |
| `EX1324` | `1324B` | `src/LO_SYN.mad:652` | `src/LO_SYN.mad:3534` | 1 |
| `SC7132` | `71325B` | `src/LO_SYN.mad:653` | `src/LO_SYN.mad:3537` | 1 |
| `EX7132` | `71326B` | `src/LO_SYN.mad:654` | `src/LO_SYN.mad:3540` | 1 |
| `ME1401` | `1401B` | `src/LO_SYN.mad:655` | `src/LO_SYN.mad:3555` | 1 |
| `RG1402` | `1402B` | `src/LO_SYN.mad:656` | `src/LO_SYN.mad:3558` | 1 |
| `RG1403` | `1403B` | `src/LO_SYN.mad:657` | `src/LO_SYN.mad:3561` | 1 |
| `SC7140` | `71404B` | `src/LO_SYN.mad:658` | `src/LO_SYN.mad:3564` | 1 |
| `EX7140` | `71405B` | `src/LO_SYN.mad:659` | `src/LO_SYN.mad:3567` | 1 |
| `RG1407` | `1407B` | `src/LO_SYN.mad:660` | `src/LO_SYN.mad:3570` | 1 |
| `RG2001` | `2001B` | `src/LO_SYN.mad:661` | `src/LO_SYN.mad:3582` | 1 |
| `SC7200` | `72002B` | `src/LO_SYN.mad:662` | `src/LO_SYN.mad:3585` | 1 |
| `AP2003` | `2003B` | `src/LO_SYN.mad:663` | `src/LO_SYN.mad:3588` | 1 |
| `AP0000` | `2004B` | `src/LO_SYN.mad:664` | `src/LO_SYN.mad:3591` | 1 |
| `EX2005` | `2005B` | `src/LO_SYN.mad:665` | `src/LO_SYN.mad:3594` | 1 |
| `SC2006` | `2006B` | `src/LO_SYN.mad:666` | `src/LO_SYN.mad:3597` | 1 |
| `RG2010` | `2010B` | `src/LO_SYN.mad:667` | `src/LO_SYN.mad:3600` | 1 |
| `EX7201` | `72011B` | `src/LO_SYN.mad:668` | `src/LO_SYN.mad:3603` | 1 |
| `AP3001` | `3001B` | `src/LO_SYN.mad:669` | `src/LO_SYN.mad:3606` | 1 |
| `EX3002` | `3002B` | `src/LO_SYN.mad:670` | `src/LO_SYN.mad:3609` | 1 |
| `EX3003` | `3003B` | `src/LO_SYN.mad:671` | `src/LO_SYN.mad:3612` | 1 |
| `ME3005` | `3005B` | `src/LO_SYN.mad:672` | `src/LO_SYN.mad:3615` | 1 |
| `ME7300` | `73007B` | `src/LO_SYN.mad:673` | `src/LO_SYN.mad:3618` | 1 |
| `EX7301` | `73010B` | `src/LO_SYN.mad:674` | `src/LO_SYN.mad:3621` | 1 |
| `AP3101` | `3101B` | `src/LO_SYN.mad:675` | `src/LO_SYN.mad:3624` | 1 |
| `RG3102` | `3102B` | `src/LO_SYN.mad:676` | `src/LO_SYN.mad:3627` | 1 |
| `RG3103` | `3103B` | `src/LO_SYN.mad:677` | `src/LO_SYN.mad:3630` | 1 |
| `EX3106` | `3106B` | `src/LO_SYN.mad:678` | `src/LO_SYN.mad:3633` | 1 |
| `SC0601` | `601B` | `src/LO_SYN.mad:679` | `src/LO_SYN.mad:3635`, `src/LO_SYN.mad:3638`, `src/LO_SYN.mad:3677`, `src/LO_SYN.mad:3773`, `src/LO_SYN.mad:3779`, `src/LO_SYN.mad:3806` … (+1) | 7 |
| `ME3107` | `3107B` | `src/LO_SYN.mad:680` | `src/LO_SYN.mad:3636` | 1 |
| `EX3110` | `3110B` | `src/LO_SYN.mad:681` | `src/LO_SYN.mad:3639` | 1 |
| `SC0701` | `701B` | `src/LO_SYN.mad:682` | `src/LO_SYN.mad:3641`, `src/LO_SYN.mad:3695`, `src/LO_SYN.mad:3728`, `src/LO_SYN.mad:3767`, `src/LO_SYN.mad:3776`, `src/LO_SYN.mad:3794` … (+3) | 9 |
| `EX5073` | `73111B` | `src/LO_SYN.mad:683` | `src/LO_SYN.mad:3642` | 1 |
| `EX4001` | `4001B` | `src/LO_SYN.mad:684` | `src/LO_SYN.mad:3645` | 1 |
| `EX4002` | `4002B` | `src/LO_SYN.mad:685` | `src/LO_SYN.mad:3648` | 1 |
| `EX7400` | `74003B` | `src/LO_SYN.mad:686` | `src/LO_SYN.mad:3651` | 1 |
| `SC0501` | `501B` | `src/LO_SYN.mad:687` | `src/LO_SYN.mad:3653`, `src/LO_SYN.mad:3689`, `src/LO_SYN.mad:3731`, `src/LO_SYN.mad:3758`, `src/LO_SYN.mad:3764`, `src/LO_SYN.mad:3791` … (+2) | 8 |
| `RG4010` | `4010B` | `src/LO_SYN.mad:688` | `src/LO_SYN.mad:3654` | 1 |
| `AP4011` | `4011B` | `src/LO_SYN.mad:689` | `src/LO_SYN.mad:3657` | 1 |
| `SC0200` | `200B` | `src/LO_SYN.mad:690` | `src/LO_SYN.mad:3659` | 1 |
| `EX4012` | `4012B` | `src/LO_SYN.mad:691` | `src/LO_SYN.mad:3660` | 1 |
| `EX4013` | `4013B` | `src/LO_SYN.mad:692` | `src/LO_SYN.mad:3663` | 1 |
| `EX4014` | `4014B` | `src/LO_SYN.mad:693` | `src/LO_SYN.mad:3666` | 1 |
| `SC4015` | `4015B` | `src/LO_SYN.mad:694` | `src/LO_SYN.mad:3669` | 1 |
| `EX4016` | `4016B` | `src/LO_SYN.mad:695` | `src/LO_SYN.mad:3672` | 1 |
| `ME7401` | `74017B` | `src/LO_SYN.mad:696` | `src/LO_SYN.mad:3675` | 1 |
| `EX4020` | `4020B` | `src/LO_SYN.mad:697` | `src/LO_SYN.mad:3678` | 1 |
| `EX7402` | `74021B` | `src/LO_SYN.mad:698` | `src/LO_SYN.mad:3681` | 1 |
| `AP4022` | `4022B` | `src/LO_SYN.mad:699` | `src/LO_SYN.mad:3684` | 1 |
| `RG4023` | `4023B` | `src/LO_SYN.mad:700` | `src/LO_SYN.mad:3687` | 1 |
| `EX4024` | `4024B` | `src/LO_SYN.mad:701` | `src/LO_SYN.mad:3690` | 1 |
| `SC0301` | `301B` | `src/LO_SYN.mad:702` | `src/LO_SYN.mad:3692`, `src/LO_SYN.mad:3746`, `src/LO_SYN.mad:3761`, `src/LO_SYN.mad:3812`, `src/LO_SYN.mad:3821` | 5 |
| `RG4025` | `4025B` | `src/LO_SYN.mad:703` | `src/LO_SYN.mad:3693` | 1 |
| `EX4026` | `4026B` | `src/LO_SYN.mad:704` | `src/LO_SYN.mad:3696` | 1 |
| `SC1001` | `1001B` | `src/LO_SYN.mad:705` | `src/LO_SYN.mad:3698`, `src/LO_SYN.mad:3770`, `src/LO_SYN.mad:3830` | 3 |
| `EX7403` | `74030B` | `src/LO_SYN.mad:706` | `src/LO_SYN.mad:3699` | 1 |
| `EX4031` | `4031B` | `src/LO_SYN.mad:707` | `src/LO_SYN.mad:3702` | 1 |
| `EX4032` | `4032B` | `src/LO_SYN.mad:708` | `src/LO_SYN.mad:3705` | 1 |
| `EX4033` | `4033B` | `src/LO_SYN.mad:709` | `src/LO_SYN.mad:3708` | 1 |
| `SC7403` | `74034B` | `src/LO_SYN.mad:710` | `src/LO_SYN.mad:3711` | 1 |
| `EX6035` | `74035B` | `src/LO_SYN.mad:711` | `src/LO_SYN.mad:3714` | 1 |
| `EX4036` | `4036B` | `src/LO_SYN.mad:712` | `src/LO_SYN.mad:3717` | 1 |
| `EX4037` | `4037B` | `src/LO_SYN.mad:713` | `src/LO_SYN.mad:3720` | 1 |
| `EX6074` | `74040B` | `src/LO_SYN.mad:714` | `src/LO_SYN.mad:3723` | 1 |
| `SC0401` | `401B` | `src/LO_SYN.mad:715` | `src/LO_SYN.mad:3725`, `src/LO_SYN.mad:3734`, `src/LO_SYN.mad:3737`, `src/LO_SYN.mad:3740`, `src/LO_SYN.mad:3749`, `src/LO_SYN.mad:3752` … (+3) | 9 |
| `EX4041` | `4041B` | `src/LO_SYN.mad:716` | `src/LO_SYN.mad:3726` | 1 |
| `SC7404` | `74042B` | `src/LO_SYN.mad:717` | `src/LO_SYN.mad:3729` | 1 |
| `EX4043` | `4043B` | `src/LO_SYN.mad:718` | `src/LO_SYN.mad:3732` | 1 |
| `EX0023` | `4052B` | `src/LO_SYN.mad:719` | `src/LO_SYN.mad:3735` | 1 |
| `EX0022` | `4053B` | `src/LO_SYN.mad:720` | `src/LO_SYN.mad:3738` | 1 |
| `EX3640` | `4054B` | `src/LO_SYN.mad:721` | `src/LO_SYN.mad:3741` | 1 |
| `SC0201` | `201B` | `src/LO_SYN.mad:722` | `src/LO_SYN.mad:3743` | 1 |
| `SC4061` | `4061B` | `src/LO_SYN.mad:723` | `src/LO_SYN.mad:3744` | 1 |
| `RG4071` | `4071B` | `src/LO_SYN.mad:724` | `src/LO_SYN.mad:3747` | 1 |
| `EX4072` | `4072B` | `src/LO_SYN.mad:725` | `src/LO_SYN.mad:3750` | 1 |
| `EX7407` | `74073B` | `src/LO_SYN.mad:726` | `src/LO_SYN.mad:3753` | 1 |
| `EX7074` | `74075B` | `src/LO_SYN.mad:727` | `src/LO_SYN.mad:3756` | 1 |
| `AP4201` | `4201B` | `src/LO_SYN.mad:728` | `src/LO_SYN.mad:3759` | 1 |
| `EX4301` | `4301B` | `src/LO_SYN.mad:729` | `src/LO_SYN.mad:3762` | 1 |
| `EX4302` | `4302B` | `src/LO_SYN.mad:730` | `src/LO_SYN.mad:3765` | 1 |
| `SC4303` | `4303B` | `src/LO_SYN.mad:731` | `src/LO_SYN.mad:3768` | 1 |
| `EX4311` | `4311B` | `src/LO_SYN.mad:732` | `src/LO_SYN.mad:3771` | 1 |
| `EX7431` | `74312B` | `src/LO_SYN.mad:733` | `src/LO_SYN.mad:3774` | 1 |
| `RG4313` | `4313B` | `src/LO_SYN.mad:734` | `src/LO_SYN.mad:3777` | 1 |
| `EX4314` | `4314B` | `src/LO_SYN.mad:735` | `src/LO_SYN.mad:3780` | 1 |
| `SC1101` | `1101B` | `src/LO_SYN.mad:736` | `src/LO_SYN.mad:3782`, `src/LO_SYN.mad:3785`, `src/LO_SYN.mad:3824` | 3 |
| `SC4315` | `4315B` | `src/LO_SYN.mad:737` | `src/LO_SYN.mad:3783` | 1 |
| `SC4317` | `4317B` | `src/LO_SYN.mad:738` | `src/LO_SYN.mad:3786` | 1 |
| `RG4321` | `4321B` | `src/LO_SYN.mad:739` | `src/LO_SYN.mad:3789` | 1 |
| `EX7432` | `74322B` | `src/LO_SYN.mad:740` | `src/LO_SYN.mad:3792` | 1 |
| `EX4323` | `4323B` | `src/LO_SYN.mad:741` | `src/LO_SYN.mad:3795` | 1 |
| `EX4324` | `4324B` | `src/LO_SYN.mad:742` | `src/LO_SYN.mad:3798` | 1 |
| `RG4325` | `4325B` | `src/LO_SYN.mad:743` | `src/LO_SYN.mad:3801` | 1 |
| `EX4326` | `4326B` | `src/LO_SYN.mad:744` | `src/LO_SYN.mad:3804` | 1 |
| `EX4327` | `4327B` | `src/LO_SYN.mad:745` | `src/LO_SYN.mad:3807` | 1 |
| `SC4330` | `4330B` | `src/LO_SYN.mad:746` | `src/LO_SYN.mad:3810` | 1 |
| `ME7440` | `74401B` | `src/LO_SYN.mad:747` | `src/LO_SYN.mad:3813` | 1 |
| `RG7440` | `74404B` | `src/LO_SYN.mad:748` | `src/LO_SYN.mad:3816` | 1 |
| `EX4405` | `4405B` | `src/LO_SYN.mad:749` | `src/LO_SYN.mad:3819` | 1 |
| `RG4406` | `4406B` | `src/LO_SYN.mad:750` | `src/LO_SYN.mad:3822` | 1 |
| `EX4407` | `4407B` | `src/LO_SYN.mad:751` | `src/LO_SYN.mad:3825` | 1 |
| `SC1201` | `1201B` | `src/LO_SYN.mad:752` | `src/LO_SYN.mad:3827` | 1 |
| `SC4412` | `4412B` | `src/LO_SYN.mad:753` | `src/LO_SYN.mad:3828` | 1 |
| `SC7441` | `74413B` | `src/LO_SYN.mad:754` | `src/LO_SYN.mad:3831` | 1 |
| `AP4416` | `4416B` | `src/LO_SYN.mad:755` | `src/LO_SYN.mad:3834` | 1 |
| `EX4421` | `4421B` | `src/LO_SYN.mad:756` | `src/LO_SYN.mad:3837` | 1 |
| `SC4422` | `4422B` | `src/LO_SYN.mad:757` | `src/LO_SYN.mad:3840` | 1 |
| `EX4423` | `4423B` | `src/LO_SYN.mad:758` | `src/LO_SYN.mad:3843` | 1 |

**Символы-кандидаты без объявления** (возможно, их нужно описать):

| Символ | Число применений | Пример |
|---|---:|---|
| `H` | 14 | `src/FOREX_RUNTIME.mad:59` (`EQU`) |
| `NEW` | 3 | `src/FOREX_CORE.mad:145` (`NAME`) |
| `DTRAN` | 3 | `src/FOREX_CORE.mad:145` (`NAME`) |
| `INFLOA` | 3 | `include/FOREX_ROOT.mad:237` (`CONT`) |
| `H00` | 2 | `src/FOREX_RUNTIME.mad:85` (`EQU`) |
| `STA` | 2 | `src/FOREX_RUNTIME.mad:96` (`EQU`) |
| `FL_COMPARE` | 2 | `src/FOREX_RUNTIME.mad:240` (`UZA`) |
| `FL_XOR_LOOP` | 2 | `src/FOREX_RUNTIME.mad:260` (`UJ`) |
| `HLO*GEN` | 2 | `src/LO_GEN.mad:502` (`TEXT`) |
| `HPOWER` | 2 | `src/LO_GEN.mad:503` (`TEXT`) |
| `HA/RHOCHI` | 2 | `src/LO_GEN.mad:504` (`TEXT`) |
| `HA/NOT` | 2 | `src/LO_GEN.mad:505` (`TEXT`) |
| `HA/AND` | 2 | `src/LO_GEN.mad:506` (`TEXT`) |
| `HFT*621` | 2 | `src/LO_GEN.mad:507` (`TEXT`) |
| `HFT*002` | 2 | `src/LO_GEN.mad:508` (`TEXT`) |
| `HFD*002` | 2 | `src/LO_GEN.mad:509` (`TEXT`) |
| `HFC*002` | 2 | `src/LO_GEN.mad:510` (`TEXT`) |
| `HFT*003` | 2 | `src/LO_GEN.mad:511` (`TEXT`) |
| `HFT*521` | 2 | `src/LO_GEN.mad:512` (`TEXT`) |
| `HFT*721` | 2 | `src/LO_GEN.mad:513` (`TEXT`) |
| `HFT*722` | 2 | `src/LO_GEN.mad:514` (`TEXT`) |
| `HFD*722` | 2 | `src/LO_GEN.mad:515` (`TEXT`) |
| `HFC*722` | 2 | `src/LO_GEN.mad:516` (`TEXT`) |
| `HFT*723` | 2 | `src/LO_GEN.mad:517` (`TEXT`) |
| `HFT*641` | 2 | `src/LO_GEN.mad:518` (`TEXT`) |
| `HFT*642` | 2 | `src/LO_GEN.mad:519` (`TEXT`) |
| `HFD*642` | 2 | `src/LO_GEN.mad:520` (`TEXT`) |
| `HFC*642` | 2 | `src/LO_GEN.mad:521` (`TEXT`) |
| `HFT*643` | 2 | `src/LO_GEN.mad:522` (`TEXT`) |
| `HFT*541` | 2 | `src/LO_GEN.mad:523` (`TEXT`) |

### 2.3 Оставшиеся «голые» литералы

Числовой литерал считается «голым», если он встречается непосредственно
в операнде и не вынесен в правую часть `,EQU,`. Цель — свести эту таблицу
к нулю по мере замены литералов именованными константами.

| Файл | Строк с литералами | Вхождений | Примеры (значение @ файл:строка) |
|---|---:|---:|---|
| `include/FOREX_ROOT.mad` | 10 | 10 | `2`×4, `3`×3, `1`×2, `4`×1 |
| `src/FOREX_CORE.mad` | 1 | 1 | `4300B`×1 |
| `src/FOREX_DECODER_DISASM.mad` | 2 | 2 | `2`×1, `1`×1 |
| `src/FOREX_RUNTIME.mad` | 7 | 15 | `1`×4, `0000`×2, `4631`×2, `0`×1, `1.0`×1 |
| `src/LO_GEN.mad` | 3 | 3 | `0o4000`×1, `0o50`×1, `5`×1 |
| `src/LO_SYN.mad` | 8 | 8 | `1`×4, `50B`×1, `4000B`×1, `5`×1, `15`×1 |

Из них **15** — в описаниях данных (`BSS/OCT/REAL/TEXT/…`) (приоритетные кандидаты на `EQU`), **24** — непосредственно в командах (часто адреса, пока не вынесенные в константы).

Описания данных с голыми литералами:

| Файл:строка | Описание | Литерал |
|---|---|---|
| `include/FOREX_ROOT.mad:66` | `LC` | `1` |
| `src/FOREX_DECODER_DISASM.mad:144` | `LC` | `2` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `1` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `0` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `1.0` |
| `src/LO_GEN.mad:497` | `BSS` | `0o4000` |
| `src/LO_GEN.mad:498` | `BSS` | `0o50` |
| `src/LO_GEN.mad:499` | `BSS` | `5` |
| `src/LO_SYN.mad:20` | `LC` | `50B` |
| `src/LO_SYN.mad:21` | `LC` | `4000B` |
| `src/LO_SYN.mad:22` | `LC` | `5` |
| `src/LO_SYN.mad:23` | `LC` | `1` |
| `src/LO_SYN.mad:24` | `LC` | `1` |
| `src/LO_SYN.mad:25` | `LC` | `1` |
| `src/LO_SYN.mad:27` | `LC` | `1` |

Наиболее частые голые литералы (топ-15, по всем модулям):

| Литерал | Вхождений | Где (первые 3) |
|---|---:|---|
| `1` | 11 | `src/FOREX_DECODER_DISASM.mad:212`, `src/FOREX_RUNTIME.mad:208`, `src/FOREX_RUNTIME.mad:397` |
| `2` | 5 | `src/FOREX_DECODER_DISASM.mad:144`, `include/FOREX_ROOT.mad:90`, `include/FOREX_ROOT.mad:243` |
| `3` | 3 | `include/FOREX_ROOT.mad:85`, `include/FOREX_ROOT.mad:127`, `include/FOREX_ROOT.mad:137` |
| `0000` | 2 | `src/FOREX_RUNTIME.mad:513`, `src/FOREX_RUNTIME.mad:513` |
| `4631` | 2 | `src/FOREX_RUNTIME.mad:514`, `src/FOREX_RUNTIME.mad:514` |
| `5` | 2 | `src/LO_GEN.mad:499`, `src/LO_SYN.mad:22` |
| `4300B` | 1 | `src/FOREX_CORE.mad:558` |
| `0` | 1 | `src/FOREX_RUNTIME.mad:477` |
| `1.0` | 1 | `src/FOREX_RUNTIME.mad:477` |
| `10` | 1 | `src/FOREX_RUNTIME.mad:493` |
| `4000` | 1 | `src/FOREX_RUNTIME.mad:513` |
| `0012` | 1 | `src/FOREX_RUNTIME.mad:513` |
| `4001` | 1 | `src/FOREX_RUNTIME.mad:514` |
| `4632` | 1 | `src/FOREX_RUNTIME.mad:514` |
| `0o4000` | 1 | `src/LO_GEN.mad:497` |

Полный список каждого литерала со строкой — в `logs/xref_all.txt` (раздел `LITERALS`).

## 3. Граф вызовов: корень → оверлеи → рантайм → MONSYS

```text
                         CALL / VJM 0o74022(15)
   FOREX* (root)  ───────────────►  LOADANGO ──XTS LO*SYN / LO*GEN──►  оверлеи
        │  CALL DATAPR* / GIV/PG / TAK/PG / OCTTDEC
        └──────────────────────────────►  рантайм (FORMAT, FORTLIBR, DATAPR*, OCTTDEC)
                                                    │  UJ FT*nnn → 0o77xxx
   LO*SYN / LO*GEN ── VJM/UJ/UZA (abs 0o4xxxx…0o7xxxx) ──►  MONSYS / library21
```

Все рёбра выведены из исходников; адреса `0o77xxx` подтверждены
`docs/06-address-map.md` §3.1. Ниже — рёбра с указанием источника.

| Откуда | Куда | Механизм | Источник (файл:строка) |
|---|---|---|---|
| FOREX* (root) | LOADANGO (LINK 0o74022) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:245`, `src/FOREX_CORE.mad:250` |
| FOREX* (root) | оверлей LO*GEN | XTS 0o4032 + LOADANGO | `include/FOREX_ROOT.mad:107` |
| FOREX* (root) | оверлей LO*SYN | XTS 0o4031 + LOADANGO | `include/FOREX_ROOT.mad:105` |
| FOREX* (root) | рантайм: DATAPR* (LINK 0o74010) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:224` |
| FOREX* (root) | рантайм: GIV/PG (LINK 0o74012) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:238` |
| FOREX* (root) | рантайм: OCTTDEC (LINK 0o74013) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:271` |
| FOREX* (root) | рантайм: TAK/PG (LINK 0o74011) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:307` |
| оверлей LO*GEN | MONSYS / library21 | VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx | `src/LO_GEN.mad:565`, `src/LO_GEN.mad:575`, `src/LO_GEN.mad:578` … (+573) |
| оверлей LO*SYN | MONSYS / library21 | VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx | `src/LO_SYN.mad:790`, `src/LO_SYN.mad:805`, `src/LO_SYN.mad:808` … (+274) |
| рантайм: FORMAT | FT*nnn (11 entry, 0o77xxx) | UJ FT*nnn | `src/FOREX_RUNTIME.mad:163`, `src/FOREX_RUNTIME.mad:165`, `src/FOREX_RUNTIME.mad:167` … (+8) |

**Оговорка.** LINK-ячейки `0o74010..0o74013` в корне и в FORMAT имеют
одинаковую нумерацию, но относятся к разным символам (выделяются пер-модульно) —
см. `docs/06-address-map.md` §3.1.

## 4. НЕразрешённые внешние адреса (частоты)

Считаются адреса ≥ `0o020000` в операндах команд передачи управления.
Если адрес вынесен в `EQU`, он разрешён по цепочке и показан с именем.
Имя процедуры для большинства адресов **не установлено** — для этого нужен
`SYSTEM LOAD LIST` (см. `docs/06-address-map.md` §7).

### 4.1. LO*SYN (синтаксический анализатор)

Различных адресов: **98**, всего переходов: **277** (эталон docs/06: 104 / 269 — разница объясняется другим набором мнемоник и источником листинга).

| Адрес | Входов | Имя через EQU | Область (docs/06 §2) |
|---|---:|---|---|
| `0o042440` | 20 | `EX4244` | резидентная библиотека 21 |
| `0o040440` | 15 | `EX4044`, `RG4044` | резидентная библиотека 21 |
| `0o047510` | 13 | `EX4751`, `RG4751` | резидентная библиотека 21 |
| `0o042510` | 12 | `EX4251` | резидентная библиотека 21 |
| `0o064440` | 9 | `EX6444` | резидентная библиотека 21 |
| `0o042524` | 8 | `EX4252` | резидентная библиотека 21 |
| `0o040560` | 8 | `RG4056` | резидентная библиотека 21 |
| `0o020103` | 7 | `EX2010` | резидентные таблицы MONSYS |
| `0o020040` | 7 | `EX0010` | резидентные таблицы MONSYS |
| `0o040513` | 7 | `RG4051` | резидентная библиотека 21 |
| `0o040554` | 6 | `EX4055` | резидентная библиотека 21 |
| `0o066101` | 6 | `EX6610` | резидентная библиотека 21 |
| `0o074117` | 6 | `RG7411` | прочее |
| `0o020117` | 5 | `EX0000`, `RG0117` | резидентные таблицы MONSYS |
| `0o074101` | 5 | `RG7410` | прочее |
| `0o074171` | 5 | `RG7417` | прочее |
| `0o041440` | 5 | `EX4144` | резидентная библиотека 21 |
| `0o047554` | 5 | `EX4755` | резидентная библиотека 21 |
| `0o020160` | 5 | `EX0021` | резидентные таблицы MONSYS |
| `0o020113` | 4 | `EX0113`, `RG2011` | резидентные таблицы MONSYS |
| `0o020151` | 4 | `EX2015` | резидентные таблицы MONSYS |
| `0o070440` | 4 | `EX7044` | резидентная библиотека 21 |
| `0o066140` | 3 | `EX6614` | резидентная библиотека 21 |
| `0o047502` | 3 | `EX4750` | резидентная библиотека 21 |
| `0o045517` | 3 | `EX4551` | резидентная библиотека 21 |
| `0o047566` | 3 | `EX4756` | резидентная библиотека 21 |
| `0o020142` | 3 | `EX0017`, `RG2014` | резидентные таблицы MONSYS |
| `0o077520` | 3 | `RG7752` | код/таблицы MONSYS |
| `0o020120` | 3 | `EX2012` | резидентные таблицы MONSYS |
| `0o020124` | 3 | `EX0124` | резидентные таблицы MONSYS |
| … | … | ещё 68 адресов | — |

### 4.2. LO*GEN (генератор кода)

Различных адресов: **271**, всего переходов: **576** (эталон docs/06: 225 / 504 — разница объясняется другим набором мнемоник и источником листинга).

| Адрес | Входов | Имя через EQU | Область (docs/06 §2) |
|---|---:|---|---|
| `0o077144` | 69 | `JT1NIW` | код/таблицы MONSYS |
| `0o057476` | 45 | `JT18CK` | резидентная библиотека 21 |
| `0o057325` | 12 | `JT188D` | резидентная библиотека 21 |
| `0o077130` | 10 | `JT1NII` | код/таблицы MONSYS |
| `0o061372` | 10 | `JT1BCS` | резидентная библиотека 21 |
| `0o063347` | 9 | `JT1CVN` | резидентная библиотека 21 |
| `0o042637` | 8 | `JT0WWD` | резидентная библиотека 21 |
| `0o042274` | 8 | `JT0WMA` | резидентная библиотека 21 |
| `0o042256` | 7 | `JT0WLS` | резидентная библиотека 21 |
| `0o076566` | 7 | `JT1N2U` | код/таблицы MONSYS |
| `0o056620` | 7 | `AC17OS` | резидентная библиотека 21 |
| `0o042601` | 6 | `JT0WVD` | резидентная библиотека 21 |
| `0o056617` | 6 | `AC17OP` | резидентная библиотека 21 |
| `0o042244` | 5 | `JT0WLG` | резидентная библиотека 21 |
| `0o042626` | 5 | `JT0WW2` | резидентная библиотека 21 |
| `0o045421` | 5 | `JT0Z1P` | резидентная библиотека 21 |
| `0o056563` | 5 | `AC17N7` | резидентная библиотека 21 |
| `0o042115` | 5 | `JT0WHV` | резидентная библиотека 21 |
| `0o076501` | 5 | `JT1N11` | код/таблицы MONSYS |
| `0o056564` | 4 | `AC17N8` | резидентная библиотека 21 |
| `0o056575` | 4 | `AC17NJ` | резидентная библиотека 21 |
| `0o075445` | 4 | `JT1M7P` | код/таблицы MONSYS |
| `0o056561` | 4 | `AC17N5` | резидентная библиотека 21 |
| `0o041574` | 4 | `JT0W2U` | резидентная библиотека 21 |
| `0o076125` | 4 | `JT1MQL` | код/таблицы MONSYS |
| `0o056615` | 4 | `AC17ON` | резидентная библиотека 21 |
| `0o076353` | 4 | `JT1MWX` | код/таблицы MONSYS |
| `0o042413` | 3 | `AC0WQ5` | резидентная библиотека 21 |
| `0o056566` | 3 | `AC17NA` | резидентная библиотека 21 |
| `0o042360` | 3 | `JT0WOO` | резидентная библиотека 21 |
| … | … | ещё 241 адресов | — |

Полный список всех адресов с частотами и строками — `logs/xref_all.txt`
(раздел `ADDRESSES`).

## 5. Подтверждённые соответствия (docs/06-address-map.md)

Извлечено из таблиц `docs/06-address-map.md` §3, §3.1. `confidence = confirmed`
означает подтверждение адреса/роли, но не всегда имени процедуры.

| Адрес | Имя / роль | Источник |
|---|---|---|
| `0o001770` | `FOREX*` | 0o510300-0o510347 |
| `0o004000` | `A/I0` | xts 4031/4032 |
| `0o022654` | `зона загрузки оверлеев` | *21 22654(12) |
| `0o040000` | `резидентные библиотечные модули (FOREX/CONST/COMEQ/OPRTR/ПP + runtime FT*/FD*/FC*)` | 042440/040440/042510/064440/057476/061372 |
| `0o074000` | `LINK-ячейки внешних ссылок (0o74010=DATAPR*, …)` | 0o74000..0o74077 |
| `0o075000` | `0o77120..0o77167` | 0o77120..0o77167 |
| `0o074010` | `DATAPR*` | 0o510311 |
| `0o074011` | `TAK/PG` | 0o510331 |
| `0o074012` | `GIV/PG` | 0o510314 |
| `0o074013` | `OCTTDEC` | 0o510322 |
| `0o074022` | `LOADANGO` | 0o510315-316 |
| `0o004024` | `слот DATAPR*` | 0o510305 |
| `0o004025` | `слот TAK/PG` | 0o510306 |
| `0o004026` | `слот GIV/PG` | 0o510310 |
| `0o004027` | `слот OCTTDEC` | 0o510312 |
| `0o004031` | `LO*SYN` | 0o510345 |
| `0o004032` | `LO*GEN` | 0o510346 |
| `0o022654` | `адрес загрузки оверлеев (LOADANGO)` | 0o774467 |
| `0o030264` | `служебное слово заголовка оверлеев` | 0o200013/15 |
| `0o774467` | `*21 22654(12)` | дамп ленты |
| `0o077207` | `FT*571` | confirmed (S1), likely (привязка ячейки) |
| `0o077237` | `FT*541` | то же |
| `0o077167` | `FT*611` | то же |
| `0o077247` | `FT*531` | то же |
| `0o077217` | `FT*561` | то же |
| `0o077157` | `FT*621` | то же |
| `0o077257` | `FT*521` | то же |
| `0o077057` | `FT*721` | то же |
| `0o077137` | `FT*641` | то же |
| `0o077776` | `FT*002` | то же |
| `0o077775` | `FT*003` | то же |

## 6. Пять объявленных, но не существующих SUBP

`FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP` объявлены как внешние `SUBP`
в корне, но их исполняемые тела в доступных образах **не найдены**:
LIBREFER помечает их `EN` (описаны, не используются), DTRAN в dispak
даёт `IS ABSENT`. Вызовы идут из оверлеев абсолютными адресами,
соответствие «адрес ↔ имя» не установлено.

| SUBP | Все объявления | Число применений по имени | Тело |
|---|---|---:|---|
| `FOREX` | `src/LO_SYN.mad:32`, `include/FOREX_ROOT.mad:73`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:700`, `include/FOREX.labels.md:704` | 0 | ❌ не найдено |
| `CONST` | `include/FOREX_ROOT.mad:74`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | 0 | ❌ не найдено |
| `COMEQ` | `include/FOREX_ROOT.mad:75`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | 0 | ❌ не найдено |
| `OPRTR` | `src/LO_GEN.mad:36`, `src/LO_SYN.mad:35`, `include/FOREX_ROOT.mad:76`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | 0 | ❌ не найдено |
| `ПP` | `src/LO_SYN.mad:36`, `include/FOREX_ROOT.mad:77`, `include/FOREX.labels.md:358`, `include/FOREX.labels.md:704` | 0 | ❌ не найдено |

Доказательства: `include/FOREX_CORE.xref.md` §3, `docs/06-core-modules.md`
§3, `logs/dtran_root.txt` (`IS ABSENT` для всех пяти).


## 7. НАРУШЕНИЯ 6-СИМВОЛЬНОГО ПРАВИЛА

МАДЛЕН (БЭСМ-6) хранит имя метки или `,EQU,`-константы в одном
шестисимвольном слове: различаются **только первые 6 знаков**.
Поэтому имя обязано быть ≤ 6 символов, а первые
6 знаков разных имён — уникальными. Ниже собрано
всё, что нарушает правило (источник — MAD-файлы и `*.labels.md`).

- имён длиннее 6 знаков: **0**;
- коллизий первых 6 знаков: **0**.

### 7.1 Имена длиннее 6 знаков

| Имя | Длина | Первые 6 | Тип | Где объявлено |
|---|---:|---|---|---|
| — | 0 | — | — | нарушений нет |

### 7.2 Коллизии первых 6 знаков

Если две разные метки имеют одинаковый префикс, ассемблер их не различает.

| Первые 6 | Конфликтующие имена | Где объявлено |
|---|---|---|
| — | — | коллизий нет |

Правило именования и примеры коротких имён — `docs/10-naming-conventions.md` §6.

## 8. Воспроизводимость

```bash
cd /tmp/.private/azizz/opencode/re-forex
python3 tools/xref_all.py --out docs/09-crossrefs.md
# лог: logs/xref_all.txt (переопределяется флагом --log)
```

Инструмент детерминирован: сортирует все таблицы, не использует текущее
время — повторный запуск даёт байт-в-байт тот же вывод (идемпотентность).

## 9. Связанные документы

- `include/FOREX_CORE.xref.md`, `include/FOREX_RUNTIME.xref.md`,
  `include/LO_SYN.xref.md`, `include/LO_GEN.xref.md` — подробные xref по модулям;
- `include/RUNTIME_DISASM.xref.md`, `include/RUNTIME_DECODER.xref.md` —
  xref по дизассемблированному рантайму;
- `docs/13-runtime-crossrefs.md` — подробный свод по рантайму;
- `docs/10-naming-conventions.md` §6 — 6-символьное правило МАДЛЕН;
- `docs/03-symbols.md` — символьный чек-лист (37/37);
- `docs/06-address-map.md` — карта внешних адресов;
- `logs/address_targets.txt` — сырые частоты адресов из листингов.
