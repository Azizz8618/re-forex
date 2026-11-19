# 09 — Глобальный свод перекрёстных ссылок компилятора ФОРЭКС

> **Автоматически сгенерировано** `tools/xref_all.py`. Не редактировать вручную —
> перегенерируйте командой из раздела «Воспроизводимость».

## 1. Метод и источники

Инструмент сканирует все MAD-источники и извлекает объявления символов,
все применения, переходы/вызовы и внешние абсолютные адреса. Операнды,
вынесенные в `,EQU,`, разрешаются по цепочке при подсчёте адресов.

- MAD-файлов: **5**; строк: **8923**.
- Файлов `*.labels.md`: **3**: `include/FOREX.labels.md`, `include/LO_GEN.labels.md`, `include/LO_SYN.labels.md`
- Различных символов с определением: **3753**.
- Команд управления/перехода: **1265**.
- Внешних абсолютных адресов (переходы ≥ `0o020000`): **379**.
- Именованных констант `EQU`: **1354**.

Входные файлы:

- `include/FOREX.labels.md`
- `include/FOREX_ROOT.mad`
- `include/LO_GEN.labels.md`
- `include/LO_SYN.labels.md`
- `src/FOREX_CORE.mad`
- `src/FOREX_RUNTIME.mad`
- `src/LO_GEN.mad`
- `src/LO_SYN.mad`
- `include/*.xref.md`, `include/catalog.md`, `docs/03-symbols.md`, `docs/06-address-map.md` (для раздела 5)

## 2. Глобальная таблица символов

### 2.1 Метки, точки входа и внешние имена

«Определение» — файл:строка объявления; «Применения» — все операнды,
где символ встречается (полный список — в `logs/xref_all.txt`).

| Символ | Тип | Определение | Значение / примечание | Применения (всего) |
|---|---|---|---|---:|
| `MODVAL_40` | EQU/LABEL(md) | `src/LO_SYN.mad:80`, `include/LO_SYN.labels.md:422` | 40B | 85 |
| `JUMP_TARGET_77144` | EQU/LABEL(md) | `src/LO_GEN.mad:489`, `include/LO_GEN.labels.md:1539` | 77144B | 69 |
| `ADDR_1` | EQU/LABEL(md) | `src/LO_GEN.mad:46`, `include/LO_GEN.labels.md:1094` | 1B | 65 |
| `JUMP_TARGET_57476` | EQU/LABEL(md) | `src/LO_GEN.mad:326`, `include/LO_GEN.labels.md:1376` | 57476B | 45 |
| `ADDR_24` | EQU/LABEL(md) | `src/LO_GEN.mad:110`, `include/LO_GEN.labels.md:1158` | 24B | 40 |
| `FL_CONST_BASE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:301`, `include/FOREX.labels.md:57` | — | 40 |
| `SVCELL_400` | EQU/LABEL(md) | `src/LO_SYN.mad:588`, `include/LO_SYN.labels.md:448` | 400B | 38 |
| `SVCELL_500` | EQU/LABEL(md) | `src/LO_SYN.mad:590`, `include/LO_SYN.labels.md:450` | 500B | 36 |
| `MEM_1040` | EQU/LABEL(md) | `src/LO_SYN.mad:75`, `include/LO_SYN.labels.md:601` | 1040B | 30 |
| `NAME_LEN5_DESCRIPTOR` | EQU/LABEL(md) | `src/LO_GEN.mad:243`, `include/LO_GEN.labels.md:1295` | 0000000000020005 | 29 |
| `ADDR_13` | EQU/LABEL(md) | `src/LO_GEN.mad:65`, `include/LO_GEN.labels.md:1113` | 13B | 27 |
| `ADDR_5` | EQU/LABEL(md) | `src/LO_GEN.mad:168`, `include/LO_GEN.labels.md:1216` | 5B | 27 |
| `SVCELL_300` | EQU/LABEL(md) | `src/LO_SYN.mad:595`, `include/LO_SYN.labels.md:451` | 300B | 27 |
| `REGVAL_5501` | EQU/LABEL(md) | `src/LO_SYN.mad:74`, `include/LO_SYN.labels.md:498` | 5501B | 26 |
| `EX36_75551` | EQU/LABEL(md) | `src/LO_SYN.mad:73`, `include/LO_SYN.labels.md:58` | 75551B | 24 |
| `MEM_74040` | EQU/LABEL(md) | `src/LO_SYN.mad:183`, `include/LO_SYN.labels.md:645` | 74040B | 24 |
| `EXT_42440` | EQU/LABEL(md) | `src/LO_SYN.mad:124`, `include/LO_SYN.labels.md:257` | 42440B | 20 |
| `MEM_1171` | EQU/LABEL(md) | `src/LO_SYN.mad:182`, `include/LO_SYN.labels.md:644` | 1171B | 20 |
| `ONE_WORD` | EQU/LABEL(md) | `src/FOREX_CORE.mad:130`, `src/FOREX_RUNTIME.mad:71`, `include/FOREX_ROOT.mad:36`, `include/FOREX.labels.md:201`, `include/FOREX.labels.md:263`, `include/FOREX.labels.md:324` | 1 | 20 |
| `EX20_42440` | EQU/LABEL(md) | `src/LO_SYN.mad:295`, `include/LO_SYN.labels.md:108` | 42440B | 19 |
| `EX65_2151` | EQU/LABEL(md) | `src/LO_SYN.mad:99`, `include/LO_SYN.labels.md:65` | 2151B | 19 |
| `MEM_2101` | EQU/LABEL(md) | `src/LO_SYN.mad:179`, `include/LO_SYN.labels.md:642` | 2101B | 19 |
| `MEM_2520` | EQU/LABEL(md) | `src/LO_SYN.mad:118`, `include/LO_SYN.labels.md:612` | 2520B | 19 |
| `NEG_4` | EQU/LABEL(md) | `src/LO_GEN.mad:270`, `include/LO_GEN.labels.md:1322` | -4 | 19 |
| `EX20_42544` | EQU/LABEL(md) | `src/LO_SYN.mad:97`, `include/LO_SYN.labels.md:63` | 42544B | 18 |
| `EX36_70131` | EQU/LABEL(md) | `src/LO_SYN.mad:98`, `include/LO_SYN.labels.md:64` | 70131B | 18 |
| `ADDR_141` | EQU/LABEL(md) | `src/LO_GEN.mad:88`, `include/LO_GEN.labels.md:1136` | 141B | 17 |
| `ADDR_26` | EQU/LABEL(md) | `src/LO_GEN.mad:112`, `include/LO_GEN.labels.md:1160` | 26B | 17 |
| `ADRPTR_52103` | EQU/LABEL(md) | `src/LO_SYN.mad:105`, `include/LO_SYN.labels.md:358` | 52103B | 17 |
| `EX36_52103` | EQU/LABEL(md) | `src/LO_SYN.mad:104`, `include/LO_SYN.labels.md:67` | 52103B | 17 |
| `MEM_40` | EQU/LABEL(md) | `src/LO_SYN.mad:145`, `include/LO_SYN.labels.md:624` | 40B | 17 |
| `MEM_77554` | EQU/LABEL(md) | `src/LO_SYN.mad:180`, `include/LO_SYN.labels.md:643` | 77554B | 17 |
| `MODVAL_24770` | EQU/LABEL(md) | `src/LO_GEN.mad:250`, `include/LO_GEN.labels.md:1302` | 24770 | 17 |
| `NEG_7` | EQU/LABEL(md) | `src/LO_GEN.mad:273`, `include/LO_GEN.labels.md:1325` | -7 | 17 |
| `MEM_71040` | EQU/LABEL(md) | `src/LO_SYN.mad:106`, `include/LO_SYN.labels.md:609` | 71040B | 16 |
| `SVCELL_700` | EQU/LABEL(md) | `src/LO_SYN.mad:610`, `include/LO_SYN.labels.md:456` | 700B | 15 |
| `ADDR_51` | EQU/LABEL(md) | `src/LO_GEN.mad:172`, `include/LO_GEN.labels.md:1220` | 51B | 14 |
| `ADDR_6` | EQU/LABEL(md) | `src/LO_GEN.mad:213`, `include/LO_GEN.labels.md:1261` | 6B | 14 |
| `ADDR_14` | EQU/LABEL(md) | `src/LO_GEN.mad:86`, `include/LO_GEN.labels.md:1134` | 14B | 13 |
| `ADDR_30` | EQU/LABEL(md) | `src/LO_GEN.mad:115`, `include/LO_GEN.labels.md:1163` | 30B | 13 |
| `ADDR_7` | EQU/LABEL(md) | `src/LO_GEN.mad:225`, `include/LO_GEN.labels.md:1273` | 7B | 13 |
| `EXT_40440` | EQU/LABEL(md) | `src/LO_SYN.mad:82`, `include/LO_SYN.labels.md:247` | 40440B | 13 |
| `MEM_4503` | EQU/LABEL(md) | `src/LO_SYN.mad:213`, `include/LO_SYN.labels.md:660` | 4503B | 13 |
| `ADDR_134` | EQU/LABEL(md) | `src/LO_GEN.mad:75`, `include/LO_GEN.labels.md:1123` | 134B | 12 |
| `EXT_42510` | EQU/LABEL(md) | `src/LO_SYN.mad:271`, `include/LO_SYN.labels.md:278` | 42510B | 12 |
| `JUMP_TARGET_57325` | EQU/LABEL(md) | `src/LO_GEN.mad:325`, `include/LO_GEN.labels.md:1375` | 57325B | 12 |
| `MEM_1551` | EQU/LABEL(md) | `src/LO_SYN.mad:177`, `include/LO_SYN.labels.md:641` | 1551B | 12 |
| `OCT_BASE` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:433`, `include/FOREX.labels.md:68` | — | 12 |
| `RET_LINK_REG` | EQU/LABEL(md) | `src/FOREX_CORE.mad:137`, `src/FOREX_RUNTIME.mad:74`, `include/FOREX_ROOT.mad:47`, `include/FOREX.labels.md:208`, `include/FOREX.labels.md:266`, `include/FOREX.labels.md:335` … (+1) | 13 | 12 |
| `ADDR_136` | EQU/LABEL(md) | `src/LO_GEN.mad:81`, `include/LO_GEN.labels.md:1129` | 136B | 11 |
| `ADDR_32` | EQU/LABEL(md) | `src/LO_GEN.mad:120`, `include/LO_GEN.labels.md:1168` | 32B | 11 |
| `ADRPTR_20040` | EQU/LABEL(md) | `src/LO_SYN.mad:79`, `include/LO_SYN.labels.md:355` | 20040B | 11 |
| `EXT_47510` | EQU/LABEL(md) | `src/LO_SYN.mad:128`, `include/LO_SYN.labels.md:258` | 47510B | 11 |
| `REGVAL_103` | EQU/LABEL(md) | `src/LO_SYN.mad:192`, `include/LO_SYN.labels.md:509` | 103B | 11 |
| `DATA_WORD_00000000_00000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:30`, `include/FOREX.labels.md:222` | 00000000 00000000 | 10 |
| `JUMP_TARGET_61372` | EQU/LABEL(md) | `src/LO_GEN.mad:332`, `include/LO_GEN.labels.md:1382` | 61372B | 10 |
| `JUMP_TARGET_77130` | EQU/LABEL(md) | `src/LO_GEN.mad:488`, `include/LO_GEN.labels.md:1538` | 77130B | 10 |
| `MEM_1513` | EQU/LABEL(md) | `src/LO_SYN.mad:111`, `include/LO_SYN.labels.md:610` | 1513B | 10 |
| `MEM_4105` | EQU/LABEL(md) | `src/LO_SYN.mad:237`, `include/LO_SYN.labels.md:672` | 4105B | 10 |
| `ADDR_132` | EQU/LABEL(md) | `src/LO_GEN.mad:66`, `include/LO_GEN.labels.md:1114` | 132B | 9 |
| `ADDR_46` | EQU/LABEL(md) | `src/LO_GEN.mad:163`, `include/LO_GEN.labels.md:1211` | 46B | 9 |
| `BASE_REG14` | EQU/LABEL(md) | `src/FOREX_CORE.mad:37`, `src/FOREX_RUNTIME.mad:28`, `include/FOREX_ROOT.mad:24`, `include/FOREX.labels.md:108`, `include/FOREX.labels.md:220`, `include/FOREX.labels.md:312` … (+1) | 14 | 9 |
| `EX65_2040` | EQU/LABEL(md) | `src/LO_SYN.mad:129`, `include/LO_SYN.labels.md:74` | 2040B | 9 |
| `EXT_64440` | EQU/LABEL(md) | `src/LO_SYN.mad:94`, `include/LO_SYN.labels.md:252` | 64440B | 9 |
| `JUMP_TARGET_63347` | EQU/LABEL(md) | `src/LO_GEN.mad:340`, `include/LO_GEN.labels.md:1390` | 63347B | 9 |
| `MEM_105` | EQU/LABEL(md) | `src/LO_SYN.mad:267`, `include/LO_SYN.labels.md:685` | 105B | 9 |
| `MEM_117` | EQU/LABEL(md) | `src/LO_SYN.mad:209`, `include/LO_SYN.labels.md:658` | 117B | 9 |
| `MEM_151` | EQU/LABEL(md) | `src/LO_SYN.mad:153`, `include/LO_SYN.labels.md:628` | 151B | 9 |
| `MEM_70105` | EQU/LABEL(md) | `src/LO_SYN.mad:197`, `include/LO_SYN.labels.md:650` | 70105B | 9 |
| `MEM_7503` | EQU/LABEL(md) | `src/LO_SYN.mad:200`, `include/LO_SYN.labels.md:652` | 7503B | 9 |
| `REGSEL_12` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:256`, `src/LO_GEN.mad:584`, `src/LO_GEN.mad:587`, `src/LO_GEN.mad:1108`, `src/LO_GEN.mad:2113`, `src/LO_GEN.mad:2116` … (+13) | 12 | 9 |
| `SVCELL_401` | EQU/LABEL(md) | `src/LO_SYN.mad:712`, `include/LO_SYN.labels.md:473` | 401B | 9 |
| `SVCELL_701` | EQU/LABEL(md) | `src/LO_SYN.mad:679`, `include/LO_SYN.labels.md:466` | 701B | 9 |
| `*DUMON*` | COMMON | `src/FOREX_CORE.mad:154`, `src/LO_GEN.mad:499`, `src/LO_SYN.mad:19`, `include/FOREX_ROOT.mad:67` | DUMON_LEN | 8 |
| `ADDR_11` | EQU/LABEL(md) | `src/LO_GEN.mad:60`, `include/LO_GEN.labels.md:1108` | 11B | 8 |
| `EX47_4520` | EQU/LABEL(md) | `src/LO_SYN.mad:373`, `include/LO_SYN.labels.md:132` | 4520B | 8 |
| `EXT_42524` | EQU/LABEL(md) | `src/LO_SYN.mad:81`, `include/LO_SYN.labels.md:246` | 42524B | 8 |
| `GOST_ATTR_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:114`, `include/FOREX.labels.md:185` | 7417B | 8 |
| `JUMP_TARGET_42274` | EQU/LABEL(md) | `src/LO_GEN.mad:302`, `include/LO_GEN.labels.md:1352` | 42274B | 8 |
| `JUMP_TARGET_42637` | EQU/LABEL(md) | `src/LO_GEN.mad:308`, `include/LO_GEN.labels.md:1358` | 42637B | 8 |
| `MEM_4502` | EQU/LABEL(md) | `src/LO_SYN.mad:165`, `include/LO_SYN.labels.md:635` | 4502B | 8 |
| `MEM_70440` | EQU/LABEL(md) | `src/LO_SYN.mad:234`, `include/LO_SYN.labels.md:670` | 70440B | 8 |
| `REGVAL_40560` | EQU/LABEL(md) | `src/LO_SYN.mad:226`, `include/LO_SYN.labels.md:514` | 40560B | 8 |
| `SVCELL_501` | EQU/LABEL(md) | `src/LO_SYN.mad:684`, `include/LO_SYN.labels.md:467` | 501B | 8 |
| `SVCELL_600` | EQU/LABEL(md) | `src/LO_SYN.mad:603`, `include/LO_SYN.labels.md:454` | 600B | 8 |
| `ADDR_35` | EQU/LABEL(md) | `src/LO_GEN.mad:123`, `include/LO_GEN.labels.md:1171` | 35B | 7 |
| `ADDR_56620` | EQU/LABEL(md) | `src/LO_GEN.mad:206`, `include/LO_GEN.labels.md:1254` | 56620B | 7 |
| `ADRPTR_77040` | EQU/LABEL(md) | `src/LO_SYN.mad:345`, `include/LO_SYN.labels.md:380` | 77040B | 7 |
| `CORE_WORD1` | LABEL(md) | `include/FOREX.labels.md:165` | — | 7 |
| `EX36_61113` | EQU/LABEL(md) | `src/LO_SYN.mad:166`, `include/LO_SYN.labels.md:82` | 61113B | 7 |
| `EXT_20040` | EQU/LABEL(md) | `src/LO_SYN.mad:113`, `include/LO_SYN.labels.md:255` | 20040B | 7 |
| `EXT_20103` | EQU/LABEL(md) | `src/LO_SYN.mad:91`, `include/LO_SYN.labels.md:250` | 20103B | 7 |
| `JUMP_TARGET_42256` | EQU/LABEL(md) | `src/LO_GEN.mad:301`, `include/LO_GEN.labels.md:1351` | 42256B | 7 |
| `JUMP_TARGET_76566` | EQU/LABEL(md) | `src/LO_GEN.mad:452`, `include/LO_GEN.labels.md:1502` | 76566B | 7 |
| `MEM_2515` | EQU/LABEL(md) | `src/LO_SYN.mad:268`, `include/LO_SYN.labels.md:686` | 2515B | 7 |
| `MEM_3040` | EQU/LABEL(md) | `src/LO_SYN.mad:374`, `include/LO_SYN.labels.md:719` | 3040B | 7 |
| `MEM_440` | EQU/LABEL(md) | `src/LO_SYN.mad:151`, `include/LO_SYN.labels.md:627` | 440B | 7 |
| `MEM_4510` | EQU/LABEL(md) | `src/LO_SYN.mad:340`, `include/LO_SYN.labels.md:707` | 4510B | 7 |
| `MEM_72040` | EQU/LABEL(md) | `src/LO_SYN.mad:249`, `include/LO_SYN.labels.md:679` | 72040B | 7 |
| `MEM_72554` | EQU/LABEL(md) | `src/LO_SYN.mad:186`, `include/LO_SYN.labels.md:647` | 72554B | 7 |
| `MEM_76440` | EQU/LABEL(md) | `src/LO_SYN.mad:348`, `include/LO_SYN.labels.md:710` | 76440B | 7 |
| `MODVAL_70040` | EQU/LABEL(md) | `src/LO_SYN.mad:346`, `include/LO_SYN.labels.md:425` | 70040B | 7 |
| `NEG_6` | EQU/LABEL(md) | `src/LO_GEN.mad:272`, `include/LO_GEN.labels.md:1324` | -6 | 7 |
| `REGVAL_40513` | EQU/LABEL(md) | `src/LO_SYN.mad:201`, `include/LO_SYN.labels.md:511` | 40513B | 7 |
| `SVCELL_601` | EQU/LABEL(md) | `src/LO_SYN.mad:676`, `include/LO_SYN.labels.md:465` | 601B | 7 |
| `*00072` | LABEL | `src/FOREX_RUNTIME.mad:310` | — | 6 |
| `*00077` | LABEL | `src/FOREX_RUNTIME.mad:315` | — | 6 |
| `ADDR_142` | EQU/LABEL(md) | `src/LO_GEN.mad:89`, `include/LO_GEN.labels.md:1137` | 142B | 6 |
| `ADDR_2` | EQU/LABEL(md) | `src/LO_GEN.mad:101`, `include/LO_GEN.labels.md:1149` | 2B | 6 |
| `ADDR_27` | EQU/LABEL(md) | `src/LO_GEN.mad:113`, `include/LO_GEN.labels.md:1161` | 27B | 6 |
| `ADDR_56617` | EQU/LABEL(md) | `src/LO_GEN.mad:205`, `include/LO_GEN.labels.md:1253` | 56617B | 6 |
| `EX65_2120` | EQU/LABEL(md) | `src/LO_SYN.mad:403`, `include/LO_SYN.labels.md:140` | 2120B | 6 |
| `EX67_151` | EQU/LABEL(md) | `src/LO_SYN.mad:378`, `include/LO_SYN.labels.md:133` | 151B | 6 |
| `EXT_40554` | EQU/LABEL(md) | `src/LO_SYN.mad:212`, `include/LO_SYN.labels.md:267` | 40554B | 6 |
| `EXT_66101` | EQU/LABEL(md) | `src/LO_SYN.mad:230`, `include/LO_SYN.labels.md:270` | 66101B | 6 |
| `JUMP_TARGET_42601` | EQU/LABEL(md) | `src/LO_GEN.mad:306`, `include/LO_GEN.labels.md:1356` | 42601B | 6 |
| `MEM_101` | EQU/LABEL(md) | `src/LO_SYN.mad:143`, `include/LO_SYN.labels.md:623` | 101B | 6 |
| `MEM_2511` | EQU/LABEL(md) | `src/LO_SYN.mad:275`, `include/LO_SYN.labels.md:689` | 2511B | 6 |
| `MEM_6501` | EQU/LABEL(md) | `src/LO_SYN.mad:155`, `include/LO_SYN.labels.md:630` | 6501B | 6 |
| `MEM_70110` | EQU/LABEL(md) | `src/LO_SYN.mad:384`, `include/LO_SYN.labels.md:722` | 70110B | 6 |
| `MEM_70117` | EQU/LABEL(md) | `src/LO_SYN.mad:146`, `include/LO_SYN.labels.md:625` | 70117B | 6 |
| `MEM_74560` | EQU/LABEL(md) | `src/LO_SYN.mad:244`, `include/LO_SYN.labels.md:675` | 74560B | 6 |
| `MEM_76505` | EQU/LABEL(md) | `src/LO_SYN.mad:412`, `include/LO_SYN.labels.md:731` | 76505B | 6 |
| `NEG_5` | EQU/LABEL(md) | `src/LO_GEN.mad:271`, `include/LO_GEN.labels.md:1323` | -5 | 6 |
| `REGSEL_14` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:258`, `src/LO_GEN.mad:575`, `src/LO_GEN.mad:578`, `src/LO_GEN.mad:748`, `src/LO_GEN.mad:763`, `src/LO_GEN.mad:766` … (+295) | 14 | 6 |
| `REGVAL_105` | EQU/LABEL(md) | `src/LO_SYN.mad:274`, `include/LO_SYN.labels.md:518` | 105B | 6 |
| `REGVAL_74117` | EQU/LABEL(md) | `src/LO_SYN.mad:308`, `include/LO_SYN.labels.md:524` | 74117B | 6 |
| `SVCELL_1000` | EQU/LABEL(md) | `src/LO_SYN.mad:617`, `include/LO_SYN.labels.md:457` | 1000B | 6 |
| `ADDR_10` | EQU/LABEL(md) | `src/LO_GEN.mad:47`, `include/LO_GEN.labels.md:1095` | 10B | 5 |
| `ADDR_143` | EQU/LABEL(md) | `src/LO_GEN.mad:90`, `include/LO_GEN.labels.md:1138` | 143B | 5 |
| `ADDR_16` | EQU/LABEL(md) | `src/LO_GEN.mad:96`, `include/LO_GEN.labels.md:1144` | 16B | 5 |
| `ADDR_45` | EQU/LABEL(md) | `src/LO_GEN.mad:162`, `include/LO_GEN.labels.md:1210` | 45B | 5 |
| `ADDR_56563` | EQU/LABEL(md) | `src/LO_GEN.mad:186`, `include/LO_GEN.labels.md:1234` | 56563B | 5 |
| `ADRPTR_44144` | EQU/LABEL(md) | `src/LO_SYN.mad:286`, `include/LO_SYN.labels.md:370` | 44144B | 5 |
| `ENTRY_TAB_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:107`, `include/FOREX.labels.md:178` | 4006B | 5 |
| `EX20_40440` | EQU/LABEL(md) | `src/LO_SYN.mad:439`, `include/LO_SYN.labels.md:154` | 40440B | 5 |
| `EX20_62113` | EQU/LABEL(md) | `src/LO_SYN.mad:291`, `include/LO_SYN.labels.md:106` | 62113B | 5 |
| `EX36_42440` | EQU/LABEL(md) | `src/LO_SYN.mad:309`, `include/LO_SYN.labels.md:112` | 42440B | 5 |
| `EX36_66166` | EQU/LABEL(md) | `src/LO_SYN.mad:438`, `include/LO_SYN.labels.md:153` | 66166B | 5 |
| `EX36_66170` | EQU/LABEL(md) | `src/LO_SYN.mad:123`, `include/LO_SYN.labels.md:73` | 66170B | 5 |
| `EX47_4524` | EQU/LABEL(md) | `src/LO_SYN.mad:426`, `include/LO_SYN.labels.md:148` | 4524B | 5 |
| `EX64_5505` | EQU/LABEL(md) | `src/LO_SYN.mad:379`, `include/LO_SYN.labels.md:134` | 5505B | 5 |
| `EX66_4513` | EQU/LABEL(md) | `src/LO_SYN.mad:442`, `include/LO_SYN.labels.md:157` | 4513B | 5 |
| `EX67_440` | EQU/LABEL(md) | `src/LO_SYN.mad:199`, `include/LO_SYN.labels.md:88` | 440B | 5 |
| `EXT_20160` | EQU/LABEL(md) | `src/LO_SYN.mad:409`, `include/LO_SYN.labels.md:294` | 20160B | 5 |
| `EXT_41440` | EQU/LABEL(md) | `src/LO_SYN.mad:288`, `include/LO_SYN.labels.md:279` | 41440B | 5 |
| `EXT_47554` | EQU/LABEL(md) | `src/LO_SYN.mad:344`, `include/LO_SYN.labels.md:287` | 47554B | 5 |
| `JUMP_TARGET_42115` | EQU/LABEL(md) | `src/LO_GEN.mad:295`, `include/LO_GEN.labels.md:1345` | 42115B | 5 |
| `JUMP_TARGET_42244` | EQU/LABEL(md) | `src/LO_GEN.mad:300`, `include/LO_GEN.labels.md:1350` | 42244B | 5 |
| `JUMP_TARGET_42626` | EQU/LABEL(md) | `src/LO_GEN.mad:307`, `include/LO_GEN.labels.md:1357` | 42626B | 5 |
| `JUMP_TARGET_45421` | EQU/LABEL(md) | `src/LO_GEN.mad:317`, `include/LO_GEN.labels.md:1367` | 45421B | 5 |
| `JUMP_TARGET_76501` | EQU/LABEL(md) | `src/LO_GEN.mad:442`, `include/LO_GEN.labels.md:1492` | 76501B | 5 |
| `MEM_2117` | EQU/LABEL(md) | `src/LO_SYN.mad:238`, `include/LO_SYN.labels.md:673` | 2117B | 5 |
| `MEM_520` | EQU/LABEL(md) | `src/LO_SYN.mad:216`, `include/LO_SYN.labels.md:661` | 520B | 5 |
| `MEM_5440` | EQU/LABEL(md) | `src/LO_SYN.mad:160`, `include/LO_SYN.labels.md:633` | 5440B | 5 |
| `MEM_572` | EQU/LABEL(md) | `src/LO_SYN.mad:185`, `include/LO_SYN.labels.md:646` | 572B | 5 |
| `MEM_70131` | EQU/LABEL(md) | `src/LO_SYN.mad:408`, `include/LO_SYN.labels.md:730` | 70131B | 5 |
| `MEM_72113` | EQU/LABEL(md) | `src/LO_SYN.mad:78`, `include/LO_SYN.labels.md:604` | 72113B | 5 |
| `MEM_72440` | EQU/LABEL(md) | `src/LO_SYN.mad:156`, `include/LO_SYN.labels.md:631` | 72440B | 5 |
| `MEM_7502` | EQU/LABEL(md) | `src/LO_SYN.mad:202`, `include/LO_SYN.labels.md:653` | 7502B | 5 |
| `MEM_7560` | EQU/LABEL(md) | `src/LO_SYN.mad:204`, `include/LO_SYN.labels.md:655` | 7560B | 5 |
| `REGSEL_10` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:254`, `src/LO_GEN.mad:635`, `src/LO_GEN.mad:661`, `src/LO_GEN.mad:670`, `src/LO_GEN.mad:709`, `src/LO_GEN.mad:3105` … (+2) | 10 | 5 |
| `REGVAL_74101` | EQU/LABEL(md) | `src/LO_SYN.mad:181`, `include/LO_SYN.labels.md:508` | 74101B | 5 |
| `REGVAL_74171` | EQU/LABEL(md) | `src/LO_SYN.mad:272`, `include/LO_SYN.labels.md:517` | 74171B | 5 |
| `SVCELL_301` | EQU/LABEL(md) | `src/LO_SYN.mad:699`, `include/LO_SYN.labels.md:470` | 301B | 5 |
| `*00063` | LABEL | `src/FOREX_RUNTIME.mad:303` | — | 4 |
| `*00064` | LABEL | `src/FOREX_RUNTIME.mad:304` | — | 4 |
| `*00071` | LABEL | `src/FOREX_RUNTIME.mad:309` | — | 4 |
| `*00074` | LABEL | `src/FOREX_RUNTIME.mad:312` | — | 4 |
| `ADDR_137` | EQU/LABEL(md) | `src/LO_GEN.mad:84`, `include/LO_GEN.labels.md:1132` | 137B | 4 |
| `ADDR_140` | EQU/LABEL(md) | `src/LO_GEN.mad:87`, `include/LO_GEN.labels.md:1135` | 140B | 4 |
| `ADDR_21` | EQU/LABEL(md) | `src/LO_GEN.mad:103`, `include/LO_GEN.labels.md:1151` | 21B | 4 |
| `ADDR_31` | EQU/LABEL(md) | `src/LO_GEN.mad:119`, `include/LO_GEN.labels.md:1167` | 31B | 4 |
| `ADDR_56561` | EQU/LABEL(md) | `src/LO_GEN.mad:185`, `include/LO_GEN.labels.md:1233` | 56561B | 4 |
| `ADDR_56564` | EQU/LABEL(md) | `src/LO_GEN.mad:187`, `include/LO_GEN.labels.md:1235` | 56564B | 4 |
| `ADDR_56575` | EQU/LABEL(md) | `src/LO_GEN.mad:194`, `include/LO_GEN.labels.md:1242` | 56575B | 4 |
| `ADDR_56615` | EQU/LABEL(md) | `src/LO_GEN.mad:203`, `include/LO_GEN.labels.md:1251` | 56615B | 4 |
| `ADRPTR_44103` | EQU/LABEL(md) | `src/LO_SYN.mad:407`, `include/LO_SYN.labels.md:387` | 44103B | 4 |
| `ADRPTR_45554` | EQU/LABEL(md) | `src/LO_SYN.mad:414`, `include/LO_SYN.labels.md:388` | 45554B | 4 |
| `ADRPTR_46561` | EQU/LABEL(md) | `src/LO_SYN.mad:208`, `include/LO_SYN.labels.md:364` | 46561B | 4 |
| `ADRPTR_62105` | EQU/LABEL(md) | `src/LO_SYN.mad:95`, `include/LO_SYN.labels.md:357` | 62105B | 4 |
| `ADRPTR_66151` | EQU/LABEL(md) | `src/LO_SYN.mad:189`, `include/LO_SYN.labels.md:363` | 66151B | 4 |
| `DEC_7` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:43`, `include/FOREX.labels.md:235` | 7 | 4 |
| `EX20_41524` | EQU/LABEL(md) | `src/LO_SYN.mad:132`, `include/LO_SYN.labels.md:75` | 41524B | 4 |
| `EX20_52040` | EQU/LABEL(md) | `src/LO_SYN.mad:96`, `include/LO_SYN.labels.md:62` | 52040B | 4 |
| `EX20_64505` | EQU/LABEL(md) | `src/LO_SYN.mad:326`, `include/LO_SYN.labels.md:118` | 64505B | 4 |
| `EX36_20040` | EQU/LABEL(md) | `src/LO_SYN.mad:107`, `include/LO_SYN.labels.md:68` | 20040B | 4 |
| `EX36_50115` | EQU/LABEL(md) | `src/LO_SYN.mad:162`, `include/LO_SYN.labels.md:80` | 50115B | 4 |
| `EX36_63517` | EQU/LABEL(md) | `src/LO_SYN.mad:451`, `include/LO_SYN.labels.md:160` | 63517B | 4 |
| `EX36_70120` | EQU/LABEL(md) | `src/LO_SYN.mad:269`, `include/LO_SYN.labels.md:101` | 70120B | 4 |
| `EX64_2554` | EQU/LABEL(md) | `src/LO_SYN.mad:150`, `include/LO_SYN.labels.md:77` | 2554B | 4 |
| `EXT_20117` | EQU/LABEL(md) | `src/LO_SYN.mad:117`, `include/LO_SYN.labels.md:256` | 20117B | 4 |
| `EXT_20151` | EQU/LABEL(md) | `src/LO_SYN.mad:231`, `include/LO_SYN.labels.md:271` | 20151B | 4 |
| `EXT_70440` | EQU/LABEL(md) | `src/LO_SYN.mad:232`, `include/LO_SYN.labels.md:272` | 70440B | 4 |
| `JUMP_TARGET_41574` | EQU/LABEL(md) | `src/LO_GEN.mad:287`, `include/LO_GEN.labels.md:1337` | 41574B | 4 |
| `JUMP_TARGET_75445` | EQU/LABEL(md) | `src/LO_GEN.mad:360`, `include/LO_GEN.labels.md:1410` | 75445B | 4 |
| `JUMP_TARGET_76125` | EQU/LABEL(md) | `src/LO_GEN.mad:395`, `include/LO_GEN.labels.md:1445` | 76125B | 4 |
| `JUMP_TARGET_76353` | EQU/LABEL(md) | `src/LO_GEN.mad:414`, `include/LO_GEN.labels.md:1464` | 76353B | 4 |
| `MEM_2151` | EQU/LABEL(md) | `src/LO_SYN.mad:142`, `include/LO_SYN.labels.md:622` | 2151B | 4 |
| `MEM_3117` | EQU/LABEL(md) | `src/LO_SYN.mad:154`, `include/LO_SYN.labels.md:629` | 3117B | 4 |
| `MEM_5517` | EQU/LABEL(md) | `src/LO_SYN.mad:323`, `include/LO_SYN.labels.md:703` | 5517B | 4 |
| `MEM_6440` | EQU/LABEL(md) | `src/LO_SYN.mad:217`, `include/LO_SYN.labels.md:662` | 6440B | 4 |
| `MEM_6505` | EQU/LABEL(md) | `src/LO_SYN.mad:420`, `include/LO_SYN.labels.md:732` | 6505B | 4 |
| `MEM_70040` | EQU/LABEL(md) | `src/LO_SYN.mad:137`, `include/LO_SYN.labels.md:619` | 70040B | 4 |
| `MEM_70151` | EQU/LABEL(md) | `src/LO_SYN.mad:93`, `include/LO_SYN.labels.md:607` | 70151B | 4 |
| `MEM_72105` | EQU/LABEL(md) | `src/LO_SYN.mad:270`, `include/LO_SYN.labels.md:687` | 72105B | 4 |
| `MEM_75503` | EQU/LABEL(md) | `src/LO_SYN.mad:287`, `include/LO_SYN.labels.md:693` | 75503B | 4 |
| `MEM_77440` | EQU/LABEL(md) | `src/LO_SYN.mad:425`, `include/LO_SYN.labels.md:735` | 77440B | 4 |
| `MEM_77520` | EQU/LABEL(md) | `src/LO_SYN.mad:203`, `include/LO_SYN.labels.md:654` | 77520B | 4 |
| `MODE_6` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:68`, `include/FOREX_ROOT.mad:34`, `include/FOREX.labels.md:260`, `include/FOREX.labels.md:322` | 6 | 4 |
| `MODVAL_70102` | EQU/LABEL(md) | `src/LO_SYN.mad:362`, `include/LO_SYN.labels.md:427` | 70102B | 4 |
| `MODVAL_70144` | EQU/LABEL(md) | `src/LO_SYN.mad:437`, `include/LO_SYN.labels.md:432` | 70144B | 4 |
| `NEG_3` | EQU/LABEL(md) | `src/LO_GEN.mad:269`, `include/LO_GEN.labels.md:1321` | -3 | 4 |
| `OCT` | DATA/LABEL(md) | `src/FOREX_RUNTIME.mad:468`, `include/FOREX.labels.md:357` | — | 4 |
| `PAGE17_ADDR` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:37`, `include/FOREX.labels.md:325` | 17B | 4 |
| `REGSEL_11` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:255`, `src/LO_GEN.mad:862`, `src/LO_GEN.mad:877`, `src/LO_GEN.mad:895`, `include/LO_GEN.labels.md:1307` | 11 | 4 |
| `REGVAL_2524` | EQU/LABEL(md) | `src/LO_SYN.mad:110`, `include/LO_SYN.labels.md:499` | 2524B | 4 |
| `REGVAL_40` | EQU/LABEL(md) | `src/LO_SYN.mad:411`, `include/LO_SYN.labels.md:531` | 40B | 4 |
| `REGVAL_440` | EQU/LABEL(md) | `src/LO_SYN.mad:254`, `include/LO_SYN.labels.md:516` | 440B | 4 |
| `RESIDENT_ZERO_PAGE` | EQU/LABEL(md) | `src/FOREX_CORE.mad:135`, `include/FOREX.labels.md:206` | 70000B | 4 |
| `*00062` | LABEL | `src/FOREX_RUNTIME.mad:302` | — | 3 |
| `*00070` | LABEL | `src/FOREX_RUNTIME.mad:308` | — | 3 |
| `*00100` | LABEL | `src/FOREX_RUNTIME.mad:316` | — | 3 |
| `ADDR_100` | EQU/LABEL(md) | `src/LO_GEN.mad:48`, `include/LO_GEN.labels.md:1096` | 100B | 3 |
| `ADDR_12` | EQU/LABEL(md) | `src/LO_GEN.mad:62`, `include/LO_GEN.labels.md:1110` | 12B | 3 |
| `ADDR_153` | EQU/LABEL(md) | `src/LO_GEN.mad:94`, `include/LO_GEN.labels.md:1142` | 153B | 3 |
| `ADDR_17` | EQU/LABEL(md) | `src/LO_GEN.mad:99`, `include/LO_GEN.labels.md:1147` | 17B | 3 |
| `ADDR_23` | EQU/LABEL(md) | `src/LO_GEN.mad:109`, `include/LO_GEN.labels.md:1157` | 23B | 3 |
| `ADDR_3` | EQU/LABEL(md) | `src/LO_GEN.mad:114`, `include/LO_GEN.labels.md:1162` | 3B | 3 |
| `ADDR_42413` | EQU/LABEL(md) | `src/LO_GEN.mad:157`, `include/LO_GEN.labels.md:1205` | 42413B | 3 |
| `ADDR_42551` | EQU/LABEL(md) | `src/LO_GEN.mad:158`, `include/LO_GEN.labels.md:1206` | 42551B | 3 |
| `ADDR_44` | EQU/LABEL(md) | `src/LO_GEN.mad:161`, `include/LO_GEN.labels.md:1209` | 44B | 3 |
| `ADDR_50` | EQU/LABEL(md) | `src/LO_GEN.mad:169`, `include/LO_GEN.labels.md:1217` | 50B | 3 |
| `ADDR_55` | EQU/LABEL(md) | `src/LO_GEN.mad:182`, `include/LO_GEN.labels.md:1230` | 55B | 3 |
| `ADDR_56566` | EQU/LABEL(md) | `src/LO_GEN.mad:189`, `include/LO_GEN.labels.md:1237` | 56566B | 3 |
| `ADDR_56570` | EQU/LABEL(md) | `src/LO_GEN.mad:190`, `include/LO_GEN.labels.md:1238` | 56570B | 3 |
| `ADDR_56572` | EQU/LABEL(md) | `src/LO_GEN.mad:192`, `include/LO_GEN.labels.md:1240` | 56572B | 3 |
| `ADDR_62` | EQU/LABEL(md) | `src/LO_GEN.mad:218`, `include/LO_GEN.labels.md:1266` | 62B | 3 |
| `ADRPTR_41524` | EQU/LABEL(md) | `src/LO_SYN.mad:317`, `include/LO_SYN.labels.md:375` | 41524B | 3 |
| `ADRPTR_43040` | EQU/LABEL(md) | `src/LO_SYN.mad:434`, `include/LO_SYN.labels.md:389` | 43040B | 3 |
| `ADRPTR_43516` | EQU/LABEL(md) | `src/LO_SYN.mad:396`, `include/LO_SYN.labels.md:384` | 43516B | 3 |
| `ADRPTR_45440` | EQU/LABEL(md) | `src/LO_SYN.mad:404`, `include/LO_SYN.labels.md:385` | 45440B | 3 |
| `ADRPTR_46502` | EQU/LABEL(md) | `src/LO_SYN.mad:314`, `include/LO_SYN.labels.md:374` | 46502B | 3 |
| `ADRPTR_50101` | EQU/LABEL(md) | `src/LO_SYN.mad:376`, `include/LO_SYN.labels.md:381` | 50101B | 3 |
| `ADRPTR_52170` | EQU/LABEL(md) | `src/LO_SYN.mad:241`, `include/LO_SYN.labels.md:366` | 52170B | 3 |
| `DATE_PRINT` | COMMON/LABEL(md)/NAME/SUBP | `src/FOREX_RUNTIME.mad:329`, `src/FOREX_RUNTIME.mad:331`, `include/FOREX_ROOT.mad:69`, `include/FOREX.labels.md:58`, `include/FOREX.labels.md:83` | — | 3 |
| `DUMON_TIME_CELL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:106`, `include/FOREX.labels.md:177` | 4025B | 3 |
| `EX20_20040` | EQU/LABEL(md) | `src/LO_SYN.mad:221`, `include/LO_SYN.labels.md:91` | 20040B | 3 |
| `EX20_20143` | EQU/LABEL(md) | `src/LO_SYN.mad:413`, `include/LO_SYN.labels.md:142` | 20143B | 3 |
| `EX20_42502` | EQU/LABEL(md) | `src/LO_SYN.mad:561`, `include/LO_SYN.labels.md:186` | 42502B | 3 |
| `EX20_42503` | EQU/LABEL(md) | `src/LO_SYN.mad:108`, `include/LO_SYN.labels.md:69` | 42503B | 3 |
| `EX20_44040` | EQU/LABEL(md) | `src/LO_SYN.mad:215`, `include/LO_SYN.labels.md:90` | 44040B | 3 |
| `EX36_46440` | EQU/LABEL(md) | `src/LO_SYN.mad:305`, `include/LO_SYN.labels.md:111` | 46440B | 3 |
| `EX36_47524` | EQU/LABEL(md) | `src/LO_SYN.mad:109`, `include/LO_SYN.labels.md:70` | 47524B | 3 |
| `EX36_52102` | EQU/LABEL(md) | `src/LO_SYN.mad:248`, `include/LO_SYN.labels.md:94` | 52102B | 3 |
| `EX36_65040` | EQU/LABEL(md) | `src/LO_SYN.mad:357`, `include/LO_SYN.labels.md:125` | 65040B | 3 |
| `EX36_66040` | EQU/LABEL(md) | `src/LO_SYN.mad:315`, `include/LO_SYN.labels.md:114` | 66040B | 3 |
| `EX57_MODE6` | EQU/LABEL(md) | `src/FOREX_CORE.mad:109`, `include/FOREX.labels.md:180` | 6B | 3 |
| `EXT_20113` | EQU/LABEL(md) | `src/LO_SYN.mad:100`, `include/LO_SYN.labels.md:253` | 20113B | 3 |
| `EXT_20120` | EQU/LABEL(md) | `src/LO_SYN.mad:218`, `include/LO_SYN.labels.md:268` | 20120B | 3 |
| `EXT_20124` | EQU/LABEL(md) | `src/LO_SYN.mad:310`, `include/LO_SYN.labels.md:280` | 20124B | 3 |
| `EXT_40561` | EQU/LABEL(md) | `src/LO_SYN.mad:534`, `include/LO_SYN.labels.md:310` | 40561B | 3 |
| `EXT_45517` | EQU/LABEL(md) | `src/LO_SYN.mad:131`, `include/LO_SYN.labels.md:259` | 45517B | 3 |
| `EXT_47502` | EQU/LABEL(md) | `src/LO_SYN.mad:92`, `include/LO_SYN.labels.md:251` | 47502B | 3 |
| `EXT_47566` | EQU/LABEL(md) | `src/LO_SYN.mad:170`, `include/LO_SYN.labels.md:263` | 47566B | 3 |
| `EXT_66140` | EQU/LABEL(md) | `src/LO_SYN.mad:90`, `include/LO_SYN.labels.md:249` | 66140B | 3 |
| `ISO_WORD_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:62`, `include/FOREX.labels.md:254` | 64 | 3 |
| `JUMP_TARGET_42320` | EQU/LABEL(md) | `src/LO_GEN.mad:303`, `include/LO_GEN.labels.md:1353` | 42320B | 3 |
| `JUMP_TARGET_42360` | EQU/LABEL(md) | `src/LO_GEN.mad:305`, `include/LO_GEN.labels.md:1355` | 42360B | 3 |
| `JUMP_TARGET_44671` | EQU/LABEL(md) | `src/LO_GEN.mad:316`, `include/LO_GEN.labels.md:1366` | 44671B | 3 |
| `JUMP_TARGET_60130` | EQU/LABEL(md) | `src/LO_GEN.mad:329`, `include/LO_GEN.labels.md:1379` | 60130B | 3 |
| `JUMP_TARGET_75264` | EQU/LABEL(md) | `src/LO_GEN.mad:347`, `include/LO_GEN.labels.md:1397` | 75264B | 3 |
| `JUMP_TARGET_75300` | EQU/LABEL(md) | `src/LO_GEN.mad:348`, `include/LO_GEN.labels.md:1398` | 75300B | 3 |
| `JUMP_TARGET_75563` | EQU/LABEL(md) | `src/LO_GEN.mad:379`, `include/LO_GEN.labels.md:1429` | 75563B | 3 |
| `JUMP_TARGET_76563` | EQU/LABEL(md) | `src/LO_GEN.mad:451`, `include/LO_GEN.labels.md:1501` | 76563B | 3 |
| `JUMP_TARGET_77114` | EQU/LABEL(md) | `src/LO_GEN.mad:479`, `include/LO_GEN.labels.md:1529` | 77114B | 3 |
| `LINK_REG_15` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:56`, `include/FOREX.labels.md:344`, `include/FOREX.labels.md:351` | 15 | 3 |
| `MEM_110` | EQU/LABEL(md) | `src/LO_SYN.mad:502`, `include/LO_SYN.labels.md:765` | 110B | 3 |
| `MEM_1103` | EQU/LABEL(md) | `src/LO_SYN.mad:196`, `include/LO_SYN.labels.md:649` | 1103B | 3 |
| `MEM_1517` | EQU/LABEL(md) | `src/LO_SYN.mad:247`, `include/LO_SYN.labels.md:678` | 1517B | 3 |
| `MEM_1523` | EQU/LABEL(md) | `src/LO_SYN.mad:395`, `include/LO_SYN.labels.md:725` | 1523B | 3 |
| `MEM_2110` | EQU/LABEL(md) | `src/LO_SYN.mad:163`, `include/LO_SYN.labels.md:634` | 2110B | 3 |
| `MEM_2516` | EQU/LABEL(md) | `src/LO_SYN.mad:245`, `include/LO_SYN.labels.md:676` | 2516B | 3 |
| `MEM_2544` | EQU/LABEL(md) | `src/LO_SYN.mad:205`, `include/LO_SYN.labels.md:656` | 2544B | 3 |
| `MEM_4117` | EQU/LABEL(md) | `src/LO_SYN.mad:233`, `include/LO_SYN.labels.md:669` | 4117B | 3 |
| `MEM_4440` | EQU/LABEL(md) | `src/LO_SYN.mad:228`, `include/LO_SYN.labels.md:668` | 4440B | 3 |
| `MEM_566` | EQU/LABEL(md) | `src/LO_SYN.mad:341`, `include/LO_SYN.labels.md:708` | 566B | 3 |
| `MEM_70115` | EQU/LABEL(md) | `src/LO_SYN.mad:77`, `include/LO_SYN.labels.md:603` | 70115B | 3 |
| `MEM_70120` | EQU/LABEL(md) | `src/LO_SYN.mad:210`, `include/LO_SYN.labels.md:659` | 70120B | 3 |
| `MEM_70524` | EQU/LABEL(md) | `src/LO_SYN.mad:500`, `include/LO_SYN.labels.md:764` | 70524B | 3 |
| `MEM_71116` | EQU/LABEL(md) | `src/LO_SYN.mad:225`, `include/LO_SYN.labels.md:666` | 71116B | 3 |
| `MEM_71131` | EQU/LABEL(md) | `src/LO_SYN.mad:246`, `include/LO_SYN.labels.md:677` | 71131B | 3 |
| `MEM_71517` | EQU/LABEL(md) | `src/LO_SYN.mad:343`, `include/LO_SYN.labels.md:709` | 71517B | 3 |
| `MEM_74151` | EQU/LABEL(md) | `src/LO_SYN.mad:171`, `include/LO_SYN.labels.md:637` | 74151B | 3 |
| `MEM_76117` | EQU/LABEL(md) | `src/LO_SYN.mad:294`, `include/LO_SYN.labels.md:695` | 76117B | 3 |
| `MODVAL_70142` | EQU/LABEL(md) | `src/LO_SYN.mad:122`, `include/LO_SYN.labels.md:423` | 70142B | 3 |
| `REAL_MODE_3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:73`, `include/FOREX_ROOT.mad:46`, `include/FOREX.labels.md:265`, `include/FOREX.labels.md:334` | 3 | 3 |
| `REGVAL_104` | EQU/LABEL(md) | `src/LO_SYN.mad:516`, `include/LO_SYN.labels.md:542` | 104B | 3 |
| `REGVAL_1117` | EQU/LABEL(md) | `src/LO_SYN.mad:475`, `include/LO_SYN.labels.md:536` | 1117B | 3 |
| `REGVAL_70110` | EQU/LABEL(md) | `src/LO_SYN.mad:342`, `include/LO_SYN.labels.md:526` | 70110B | 3 |
| `REGVAL_77520` | EQU/LABEL(md) | `src/LO_SYN.mad:214`, `include/LO_SYN.labels.md:512` | 77520B | 3 |
| `RM*` | COMMON | `include/FOREX_ROOT.mad:241` | RM_WORDS_4 | 3 |
| `STACK_OFF_M2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:76`, `include/FOREX_ROOT.mad:49`, `include/FOREX.labels.md:268`, `include/FOREX.labels.md:337` | -2 | 3 |
| `STACK_OFF_M3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:77`, `include/FOREX.labels.md:269` | -3 | 3 |
| `STACK_OFF_M4` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:78`, `include/FOREX.labels.md:270` | -4 | 3 |
| `SVCELL_1001` | EQU/LABEL(md) | `src/LO_SYN.mad:702`, `include/LO_SYN.labels.md:471` | 1001B | 3 |
| `SVCELL_1101` | EQU/LABEL(md) | `src/LO_SYN.mad:733`, `include/LO_SYN.labels.md:478` | 1101B | 3 |
| `SYMTAB_TARGET` | EQU/LABEL(md) | `src/FOREX_CORE.mad:139`, `include/FOREX.labels.md:210` | 65412B | 3 |
| `TIME_CELL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:140`, `include/FOREX.labels.md:211` | 4024B | 3 |
| `*00065` | LABEL | `src/FOREX_RUNTIME.mad:305` | — | 2 |
| `A/I0` | COMMON | `src/FOREX_CORE.mad:155`, `src/LO_SYN.mad:24`, `include/FOREX_ROOT.mad:68` | ONE_WORD | 2 |
| `ADDR_101` | EQU/LABEL(md) | `src/LO_GEN.mad:49`, `include/LO_GEN.labels.md:1097` | 101B | 2 |
| `ADDR_133` | EQU/LABEL(md) | `src/LO_GEN.mad:70`, `include/LO_GEN.labels.md:1118` | 133B | 2 |
| `ADDR_135` | EQU/LABEL(md) | `src/LO_GEN.mad:78`, `include/LO_GEN.labels.md:1126` | 135B | 2 |
| `ADDR_1351` | EQU/LABEL(md) | `src/LO_GEN.mad:79`, `include/LO_GEN.labels.md:1127` | 1351B | 2 |
| `ADDR_1360` | EQU/LABEL(md) | `src/LO_GEN.mad:82`, `include/LO_GEN.labels.md:1130` | 1360B | 2 |
| `ADDR_1362` | EQU/LABEL(md) | `src/LO_GEN.mad:83`, `include/LO_GEN.labels.md:1131` | 1362B | 2 |
| `ADDR_15` | EQU/LABEL(md) | `src/LO_GEN.mad:92`, `include/LO_GEN.labels.md:1140` | 15B | 2 |
| `ADDR_176` | EQU/LABEL(md) | `src/LO_GEN.mad:100`, `include/LO_GEN.labels.md:1148` | 176B | 2 |
| `ADDR_20` | EQU/LABEL(md) | `src/LO_GEN.mad:102`, `include/LO_GEN.labels.md:1150` | 20B | 2 |
| `ADDR_22` | EQU/LABEL(md) | `src/LO_GEN.mad:105`, `include/LO_GEN.labels.md:1153` | 22B | 2 |
| `ADDR_30274` | EQU/LABEL(md) | `src/LO_GEN.mad:116`, `include/LO_GEN.labels.md:1164` | 30274B | 2 |
| `ADDR_33` | EQU/LABEL(md) | `src/LO_GEN.mad:121`, `include/LO_GEN.labels.md:1169` | 33B | 2 |
| `ADDR_34` | EQU/LABEL(md) | `src/LO_GEN.mad:122`, `include/LO_GEN.labels.md:1170` | 34B | 2 |
| `ADDR_36` | EQU/LABEL(md) | `src/LO_GEN.mad:124`, `include/LO_GEN.labels.md:1172` | 36B | 2 |
| `ADDR_37` | EQU/LABEL(md) | `src/LO_GEN.mad:125`, `include/LO_GEN.labels.md:1173` | 37B | 2 |
| `ADDR_40411` | EQU/LABEL(md) | `src/LO_GEN.mad:136`, `include/LO_GEN.labels.md:1184` | 40411B | 2 |
| `ADDR_40425` | EQU/LABEL(md) | `src/LO_GEN.mad:140`, `include/LO_GEN.labels.md:1188` | 40425B | 2 |
| `ADDR_40437` | EQU/LABEL(md) | `src/LO_GEN.mad:143`, `include/LO_GEN.labels.md:1191` | 40437B | 2 |
| `ADDR_4114` | EQU/LABEL(md) | `src/LO_GEN.mad:155`, `include/LO_GEN.labels.md:1203` | 4114B | 2 |
| `ADDR_42556` | EQU/LABEL(md) | `src/LO_GEN.mad:159`, `include/LO_GEN.labels.md:1207` | 42556B | 2 |
| `ADDR_43` | EQU/LABEL(md) | `src/LO_GEN.mad:160`, `include/LO_GEN.labels.md:1208` | 43B | 2 |
| `ADDR_50530` | EQU/LABEL(md) | `src/LO_GEN.mad:171`, `include/LO_GEN.labels.md:1219` | 50530B | 2 |
| `ADDR_53` | EQU/LABEL(md) | `src/LO_GEN.mad:178`, `include/LO_GEN.labels.md:1226` | 53B | 2 |
| `ADDR_56` | EQU/LABEL(md) | `src/LO_GEN.mad:183`, `include/LO_GEN.labels.md:1231` | 56B | 2 |
| `ADDR_56571` | EQU/LABEL(md) | `src/LO_GEN.mad:191`, `include/LO_GEN.labels.md:1239` | 56571B | 2 |
| `ADDR_56574` | EQU/LABEL(md) | `src/LO_GEN.mad:193`, `include/LO_GEN.labels.md:1241` | 56574B | 2 |
| `ADDR_56604` | EQU/LABEL(md) | `src/LO_GEN.mad:199`, `include/LO_GEN.labels.md:1247` | 56604B | 2 |
| `ADDR_56621` | EQU/LABEL(md) | `src/LO_GEN.mad:207`, `include/LO_GEN.labels.md:1255` | 56621B | 2 |
| `ADDR_56624` | EQU/LABEL(md) | `src/LO_GEN.mad:209`, `include/LO_GEN.labels.md:1257` | 56624B | 2 |
| `ADDR_60307` | EQU/LABEL(md) | `src/LO_GEN.mad:216`, `include/LO_GEN.labels.md:1264` | 60307B | 2 |
| `ADDR_67` | EQU/LABEL(md) | `src/LO_GEN.mad:224`, `include/LO_GEN.labels.md:1272` | 67B | 2 |
| `ADDR_747` | EQU/LABEL(md) | `src/LO_GEN.mad:235`, `include/LO_GEN.labels.md:1283` | 747B | 2 |
| `ADRPTR_20110` | EQU/LABEL(md) | `src/LO_SYN.mad:486`, `include/LO_SYN.labels.md:392` | 20110B | 2 |
| `ADRPTR_20146` | EQU/LABEL(md) | `src/LO_SYN.mad:178`, `include/LO_SYN.labels.md:361` | 20146B | 2 |
| `ADRPTR_41040` | EQU/LABEL(md) | `src/LO_SYN.mad:406`, `include/LO_SYN.labels.md:386` | 41040B | 2 |
| `ADRPTR_41503` | EQU/LABEL(md) | `src/LO_SYN.mad:149`, `include/LO_SYN.labels.md:359` | 41503B | 2 |
| `ADRPTR_41560` | EQU/LABEL(md) | `src/LO_SYN.mad:158`, `include/LO_SYN.labels.md:360` | 41560B | 2 |
| `ADRPTR_42440` | EQU/LABEL(md) | `src/LO_SYN.mad:263`, `include/LO_SYN.labels.md:368` | 42440B | 2 |
| `ADRPTR_45543` | EQU/LABEL(md) | `src/LO_SYN.mad:565`, `include/LO_SYN.labels.md:399` | 45543B | 2 |
| `ADRPTR_46440` | EQU/LABEL(md) | `src/LO_SYN.mad:290`, `include/LO_SYN.labels.md:371` | 46440B | 2 |
| `ADRPTR_46505` | EQU/LABEL(md) | `src/LO_SYN.mad:548`, `include/LO_SYN.labels.md:397` | 46505B | 2 |
| `ADRPTR_52105` | EQU/LABEL(md) | `src/LO_SYN.mad:187`, `include/LO_SYN.labels.md:362` | 52105B | 2 |
| `ADRPTR_64440` | EQU/LABEL(md) | `src/LO_SYN.mad:497`, `include/LO_SYN.labels.md:394` | 64440B | 2 |
| `ADRPTR_66170` | EQU/LABEL(md) | `src/LO_SYN.mad:282`, `include/LO_SYN.labels.md:369` | 66170B | 2 |
| `ADRPTR_70040` | EQU/LABEL(md) | `src/LO_SYN.mad:311`, `include/LO_SYN.labels.md:373` | 70040B | 2 |
| `A_I0_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:35`, `include/FOREX.labels.md:106` | 4007B | 2 |
| `BUFFER_A_LEN` | EQU/LABEL(md) | `src/FOREX_CORE.mad:38`, `include/FOREX_ROOT.mad:25`, `include/FOREX.labels.md:109`, `include/FOREX.labels.md:313` | 4000B | 2 |
| `CORE_ADDR_76245` | LABEL(md) | `include/FOREX.labels.md:162` | 0o076245 | 2 |
| `CORE_MODE3` | LABEL(md) | `include/FOREX.labels.md:164` | — | 2 |
| `DATA*` | COMMON | `src/FOREX_RUNTIME.mad:330` | DATE_BUF_LEN | 2 |
| `DATE_MONTH_INDEX_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:39`, `include/FOREX.labels.md:231` | 64-24 | 2 |
| `DATE_YEAR_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:42`, `include/FOREX.labels.md:234` | 64-14 | 2 |
| `DUMON_LEN` | EQU/LABEL(md) | `src/FOREX_CORE.mad:105`, `include/FOREX_ROOT.mad:27`, `include/FOREX.labels.md:176`, `include/FOREX.labels.md:315` | 5 | 2 |
| `ENTRY*` | COMMON | `src/FOREX_CORE.mad:149`, `src/LO_GEN.mad:498`, `src/LO_SYN.mad:17`, `include/FOREX_ROOT.mad:62` | ADDR_OCT_50 | 2 |
| `ENTRY_TAB_LEN` | EQU/LABEL(md) | `src/FOREX_CORE.mad:108`, `include/FOREX_ROOT.mad:28`, `include/FOREX.labels.md:179`, `include/FOREX.labels.md:316` | 50B | 2 |
| `EX20_20102` | EQU/LABEL(md) | `src/LO_SYN.mad:427`, `include/LO_SYN.labels.md:149` | 20102B | 2 |
| `EX20_20103` | EQU/LABEL(md) | `src/LO_SYN.mad:443`, `include/LO_SYN.labels.md:158` | 20103B | 2 |
| `EX20_20115` | EQU/LABEL(md) | `src/LO_SYN.mad:207`, `include/LO_SYN.labels.md:89` | 20115B | 2 |
| `EX20_20117` | EQU/LABEL(md) | `src/LO_SYN.mad:440`, `include/LO_SYN.labels.md:155` | 20117B | 2 |
| `EX20_40561` | EQU/LABEL(md) | `src/LO_SYN.mad:322`, `include/LO_SYN.labels.md:116` | 40561B | 2 |
| `EX20_64543` | EQU/LABEL(md) | `src/LO_SYN.mad:416`, `include/LO_SYN.labels.md:144` | 64543B | 2 |
| `EX36_20143` | EQU/LABEL(md) | `src/LO_SYN.mad:320`, `include/LO_SYN.labels.md:115` | 20143B | 2 |
| `EX36_20151` | EQU/LABEL(md) | `src/LO_SYN.mad:296`, `include/LO_SYN.labels.md:109` | 20151B | 2 |
| `EX36_41117` | EQU/LABEL(md) | `src/LO_SYN.mad:103`, `include/LO_SYN.labels.md:66` | 41117B | 2 |
| `EX36_41124` | EQU/LABEL(md) | `src/LO_SYN.mad:366`, `include/LO_SYN.labels.md:127` | 41124B | 2 |
| `EX36_41524` | EQU/LABEL(md) | `src/LO_SYN.mad:385`, `include/LO_SYN.labels.md:136` | 41524B | 2 |
| `EX36_41554` | EQU/LABEL(md) | `src/LO_SYN.mad:265`, `include/LO_SYN.labels.md:100` | 41554B | 2 |
| `EX36_44103` | EQU/LABEL(md) | `src/LO_SYN.mad:537`, `include/LO_SYN.labels.md:182` | 44103B | 2 |
| `EX36_50110` | EQU/LABEL(md) | `src/LO_SYN.mad:367`, `include/LO_SYN.labels.md:128` | 50110B | 2 |
| `EX36_52113` | EQU/LABEL(md) | `src/LO_SYN.mad:164`, `include/LO_SYN.labels.md:81` | 52113B | 2 |
| `EX36_61117` | EQU/LABEL(md) | `src/LO_SYN.mad:112`, `include/LO_SYN.labels.md:71` | 61117B | 2 |
| `EX36_70105` | EQU/LABEL(md) | `src/LO_SYN.mad:389`, `include/LO_SYN.labels.md:137` | 70105B | 2 |
| `EX36_70151` | EQU/LABEL(md) | `src/LO_SYN.mad:261`, `include/LO_SYN.labels.md:98` | 70151B | 2 |
| `EX36_73105` | EQU/LABEL(md) | `src/LO_SYN.mad:433`, `include/LO_SYN.labels.md:151` | 73105B | 2 |
| `EX46_74513` | EQU/LABEL(md) | `src/LO_SYN.mad:176`, `include/LO_SYN.labels.md:85` | 74513B | 2 |
| `EX47_4576` | EQU/LABEL(md) | `src/LO_SYN.mad:139`, `include/LO_SYN.labels.md:76` | 4576B | 2 |
| `EX62_102` | EQU/LABEL(md) | `src/LO_SYN.mad:350`, `include/LO_SYN.labels.md:122` | 102B | 2 |
| `EX64_1101` | EQU/LABEL(md) | `src/LO_SYN.mad:405`, `include/LO_SYN.labels.md:141` | 1101B | 2 |
| `EX64_1551` | EQU/LABEL(md) | `src/LO_SYN.mad:253`, `include/LO_SYN.labels.md:95` | 1551B | 2 |
| `EX64_510` | EQU/LABEL(md) | `src/LO_SYN.mad:262`, `include/LO_SYN.labels.md:99` | 510B | 2 |
| `EX64_5517` | EQU/LABEL(md) | `src/LO_SYN.mad:279`, `include/LO_SYN.labels.md:103` | 5517B | 2 |
| `EX64_7504` | EQU/LABEL(md) | `src/LO_SYN.mad:493`, `include/LO_SYN.labels.md:169` | 7504B | 2 |
| `EX64_7515` | EQU/LABEL(md) | `src/LO_SYN.mad:255`, `include/LO_SYN.labels.md:96` | 7515B | 2 |
| `EX64_77440` | EQU/LABEL(md) | `src/LO_SYN.mad:510`, `include/LO_SYN.labels.md:174` | 77440B | 2 |
| `EX64_77524` | EQU/LABEL(md) | `src/LO_SYN.mad:435`, `include/LO_SYN.labels.md:152` | 77524B | 2 |
| `EX65_70101` | EQU/LABEL(md) | `src/LO_SYN.mad:415`, `include/LO_SYN.labels.md:143` | 70101B | 2 |
| `EX66_4502` | EQU/LABEL(md) | `src/LO_SYN.mad:313`, `include/LO_SYN.labels.md:113` | 4502B | 2 |
| `EX66_4515` | EQU/LABEL(md) | `src/LO_SYN.mad:194`, `include/LO_SYN.labels.md:87` | 4515B | 2 |
| `EX66_6151` | EQU/LABEL(md) | `src/LO_SYN.mad:532`, `include/LO_SYN.labels.md:180` | 6151B | 2 |
| `EX67_117` | EQU/LABEL(md) | `src/LO_SYN.mad:393`, `include/LO_SYN.labels.md:139` | 117B | 2 |
| `EXT_20115` | EQU/LABEL(md) | `src/LO_SYN.mad:147`, `include/LO_SYN.labels.md:262` | 20115B | 2 |
| `EXT_20142` | EQU/LABEL(md) | `src/LO_SYN.mad:533`, `include/LO_SYN.labels.md:309` | 20142B | 2 |
| `EXT_40503` | EQU/LABEL(md) | `src/LO_SYN.mad:312`, `include/LO_SYN.labels.md:281` | 40503B | 2 |
| `EXT_47516` | EQU/LABEL(md) | `src/LO_SYN.mad:256`, `include/LO_SYN.labels.md:275` | 47516B | 2 |
| `EXT_47542` | EQU/LABEL(md) | `src/LO_SYN.mad:193`, `include/LO_SYN.labels.md:266` | 47542B | 2 |
| `EXT_47547` | EQU/LABEL(md) | `src/LO_SYN.mad:431`, `include/LO_SYN.labels.md:296` | 47547B | 2 |
| `EXT_52040` | EQU/LABEL(md) | `src/LO_SYN.mad:223`, `include/LO_SYN.labels.md:269` | 52040B | 2 |
| `EXT_60176` | EQU/LABEL(md) | `src/LO_SYN.mad:101`, `include/LO_SYN.labels.md:254` | 60176B | 2 |
| `EXT_66040` | EQU/LABEL(md) | `src/LO_SYN.mad:458`, `include/LO_SYN.labels.md:298` | 66040B | 2 |
| `EXT_73105` | EQU/LABEL(md) | `src/LO_SYN.mad:88`, `include/LO_SYN.labels.md:248` | 73105B | 2 |
| `EXT_74040` | EQU/LABEL(md) | `src/LO_SYN.mad:188`, `include/LO_SYN.labels.md:264` | 74040B | 2 |
| `EXT_74110` | EQU/LABEL(md) | `src/LO_SYN.mad:242`, `include/LO_SYN.labels.md:274` | 74110B | 2 |
| `EXT_74172` | EQU/LABEL(md) | `src/LO_SYN.mad:394`, `include/LO_SYN.labels.md:291` | 74172B | 2 |
| `EXT_74173` | EQU/LABEL(md) | `src/LO_SYN.mad:134`, `include/LO_SYN.labels.md:260` | 74173B | 2 |
| `FLGEX*` | COMMON | `src/FOREX_CORE.mad:150`, `src/LO_SYN.mad:20`, `include/FOREX_ROOT.mad:63` | ONE_WORD | 2 |
| `FL_COMPARE` | LABEL(md) | `include/FOREX.labels.md:54` | — | 2 |
| `FL_XOR_LOOP` | LABEL(md) | `include/FOREX.labels.md:50` | — | 2 |
| `FT541_ADDR` | EQU/LABEL(md) | `src/LO_GEN.mad:44`, `include/LO_GEN.labels.md:1092` | 77237B | 2 |
| `FTD_CONST` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:186`, `include/FOREX.labels.md:44` | — | 2 |
| `FTD_TABLE_END` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:183`, `include/FOREX.labels.md:43` | — | 2 |
| `FULISFL*` | COMMON | `src/FOREX_CORE.mad:152`, `src/LO_SYN.mad:22`, `include/FOREX_ROOT.mad:65` | ONE_WORD | 2 |
| `JUMP_TARGET_1672` | EQU/LABEL(md) | `src/LO_GEN.mad:277`, `include/LO_GEN.labels.md:1327` | 1672B | 2 |
| `JUMP_TARGET_41605` | EQU/LABEL(md) | `src/LO_GEN.mad:288`, `include/LO_GEN.labels.md:1338` | 41605B | 2 |
| `JUMP_TARGET_41620` | EQU/LABEL(md) | `src/LO_GEN.mad:289`, `include/LO_GEN.labels.md:1339` | 41620B | 2 |
| `JUMP_TARGET_41631` | EQU/LABEL(md) | `src/LO_GEN.mad:290`, `include/LO_GEN.labels.md:1340` | 41631B | 2 |
| `JUMP_TARGET_42040` | EQU/LABEL(md) | `src/LO_GEN.mad:293`, `include/LO_GEN.labels.md:1343` | 42040B | 2 |
| `JUMP_TARGET_44214` | EQU/LABEL(md) | `src/LO_GEN.mad:314`, `include/LO_GEN.labels.md:1364` | 44214B | 2 |
| `JUMP_TARGET_53320` | EQU/LABEL(md) | `src/LO_GEN.mad:320`, `include/LO_GEN.labels.md:1370` | 53320B | 2 |
| `JUMP_TARGET_62122` | EQU/LABEL(md) | `src/LO_GEN.mad:333`, `include/LO_GEN.labels.md:1383` | 62122B | 2 |
| `JUMP_TARGET_62435` | EQU/LABEL(md) | `src/LO_GEN.mad:334`, `include/LO_GEN.labels.md:1384` | 62435B | 2 |
| `JUMP_TARGET_62634` | EQU/LABEL(md) | `src/LO_GEN.mad:336`, `include/LO_GEN.labels.md:1386` | 62634B | 2 |
| `JUMP_TARGET_63275` | EQU/LABEL(md) | `src/LO_GEN.mad:339`, `include/LO_GEN.labels.md:1389` | 63275B | 2 |
| `JUMP_TARGET_63605` | EQU/LABEL(md) | `src/LO_GEN.mad:342`, `include/LO_GEN.labels.md:1392` | 63605B | 2 |
| `JUMP_TARGET_75326` | EQU/LABEL(md) | `src/LO_GEN.mad:349`, `include/LO_GEN.labels.md:1399` | 75326B | 2 |
| `JUMP_TARGET_75432` | EQU/LABEL(md) | `src/LO_GEN.mad:359`, `include/LO_GEN.labels.md:1409` | 75432B | 2 |
| `JUMP_TARGET_75525` | EQU/LABEL(md) | `src/LO_GEN.mad:370`, `include/LO_GEN.labels.md:1420` | 75525B | 2 |
| `JUMP_TARGET_75534` | EQU/LABEL(md) | `src/LO_GEN.mad:372`, `include/LO_GEN.labels.md:1422` | 75534B | 2 |
| `JUMP_TARGET_75541` | EQU/LABEL(md) | `src/LO_GEN.mad:373`, `include/LO_GEN.labels.md:1423` | 75541B | 2 |
| `JUMP_TARGET_76333` | EQU/LABEL(md) | `src/LO_GEN.mad:410`, `include/LO_GEN.labels.md:1460` | 76333B | 2 |
| `JUMP_TARGET_76334` | EQU/LABEL(md) | `src/LO_GEN.mad:411`, `include/LO_GEN.labels.md:1461` | 76334B | 2 |
| `JUMP_TARGET_76347` | EQU/LABEL(md) | `src/LO_GEN.mad:413`, `include/LO_GEN.labels.md:1463` | 76347B | 2 |
| `JUMP_TARGET_76452` | EQU/LABEL(md) | `src/LO_GEN.mad:437`, `include/LO_GEN.labels.md:1487` | 76452B | 2 |
| `JUMP_TARGET_76515` | EQU/LABEL(md) | `src/LO_GEN.mad:446`, `include/LO_GEN.labels.md:1496` | 76515B | 2 |
| `JUMP_TARGET_76554` | EQU/LABEL(md) | `src/LO_GEN.mad:448`, `include/LO_GEN.labels.md:1498` | 76554B | 2 |
| `JUMP_TARGET_76567` | EQU/LABEL(md) | `src/LO_GEN.mad:453`, `include/LO_GEN.labels.md:1503` | 76567B | 2 |
| `JUMP_TARGET_76571` | EQU/LABEL(md) | `src/LO_GEN.mad:454`, `include/LO_GEN.labels.md:1504` | 76571B | 2 |
| `JUMP_TARGET_76732` | EQU/LABEL(md) | `src/LO_GEN.mad:462`, `include/LO_GEN.labels.md:1512` | 76732B | 2 |
| `JUMP_TARGET_76747` | EQU/LABEL(md) | `src/LO_GEN.mad:463`, `include/LO_GEN.labels.md:1513` | 76747B | 2 |
| `JUMP_TARGET_77053` | EQU/LABEL(md) | `src/LO_GEN.mad:469`, `include/LO_GEN.labels.md:1519` | 77053B | 2 |
| `JUMP_TARGET_77100` | EQU/LABEL(md) | `src/LO_GEN.mad:473`, `include/LO_GEN.labels.md:1523` | 77100B | 2 |
| `JUMP_TARGET_77101` | EQU/LABEL(md) | `src/LO_GEN.mad:474`, `include/LO_GEN.labels.md:1524` | 77101B | 2 |
| `JUMP_TARGET_77123` | EQU/LABEL(md) | `src/LO_GEN.mad:484`, `include/LO_GEN.labels.md:1534` | 77123B | 2 |
| `LOADANGO` | LABEL(md)/SUBP | `src/LO_SYN.mad:34`, `include/FOREX.labels.md:7`, `include/FOREX.labels.md:358` | — | 2 |
| `LOADANGO_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:119`, `include/FOREX.labels.md:190` | 74022B | 2 |
| `MASK_7761` | EQU/LABEL(md) | `src/FOREX_CORE.mad:123`, `include/FOREX.labels.md:194` | 7761B | 2 |
| `MASK_7763` | EQU/LABEL(md) | `src/FOREX_CORE.mad:124`, `include/FOREX.labels.md:195` | 7763B | 2 |
| `MEM_102` | EQU/LABEL(md) | `src/LO_SYN.mad:169`, `include/LO_SYN.labels.md:636` | 102B | 2 |
| `MEM_1057` | EQU/LABEL(md) | `src/LO_SYN.mad:469`, `include/LO_SYN.labels.md:750` | 1057B | 2 |
| `MEM_1110` | EQU/LABEL(md) | `src/LO_SYN.mad:515`, `include/LO_SYN.labels.md:769` | 1110B | 2 |
| `MEM_1117` | EQU/LABEL(md) | `src/LO_SYN.mad:133`, `include/LO_SYN.labels.md:617` | 1117B | 2 |
| `MEM_1154` | EQU/LABEL(md) | `src/LO_SYN.mad:257`, `include/LO_SYN.labels.md:682` | 1154B | 2 |
| `MEM_120` | EQU/LABEL(md) | `src/LO_SYN.mad:86`, `include/LO_SYN.labels.md:606` | 120B | 2 |
| `MEM_1440` | EQU/LABEL(md) | `src/LO_SYN.mad:119`, `include/LO_SYN.labels.md:613` | 1440B | 2 |
| `MEM_147` | EQU/LABEL(md) | `src/LO_SYN.mad:400`, `include/LO_SYN.labels.md:728` | 147B | 2 |
| `MEM_1554` | EQU/LABEL(md) | `src/LO_SYN.mad:102`, `include/LO_SYN.labels.md:608` | 1554B | 2 |
| `MEM_1560` | EQU/LABEL(md) | `src/LO_SYN.mad:174`, `include/LO_SYN.labels.md:639` | 1560B | 2 |
| `MEM_160` | EQU/LABEL(md) | `src/LO_SYN.mad:264`, `include/LO_SYN.labels.md:683` | 160B | 2 |
| `MEM_2170` | EQU/LABEL(md) | `src/LO_SYN.mad:457`, `include/LO_SYN.labels.md:745` | 2170B | 2 |
| `MEM_2200` | EQU/LABEL(md) | `src/LO_SYN.mad:44`, `include/LO_SYN.labels.md:588` | 2200B | 2 |
| `MEM_2524` | EQU/LABEL(md) | `src/LO_SYN.mad:530`, `include/LO_SYN.labels.md:772` | 2524B | 2 |
| `MEM_4124` | EQU/LABEL(md) | `src/LO_SYN.mad:148`, `include/LO_SYN.labels.md:626` | 4124B | 2 |
| `MEM_4506` | EQU/LABEL(md) | `src/LO_SYN.mad:430`, `include/LO_SYN.labels.md:737` | 4506B | 2 |
| `MEM_4513` | EQU/LABEL(md) | `src/LO_SYN.mad:297`, `include/LO_SYN.labels.md:696` | 4513B | 2 |
| `MEM_4572` | EQU/LABEL(md) | `src/LO_SYN.mad:84`, `include/LO_SYN.labels.md:605` | 4572B | 2 |
| `MEM_510` | EQU/LABEL(md) | `src/LO_SYN.mad:157`, `include/LO_SYN.labels.md:632` | 510B | 2 |
| `MEM_5101` | EQU/LABEL(md) | `src/LO_SYN.mad:190`, `include/LO_SYN.labels.md:648` | 5101B | 2 |
| `MEM_5110` | EQU/LABEL(md) | `src/LO_SYN.mad:358`, `include/LO_SYN.labels.md:715` | 5110B | 2 |
| `MEM_524` | EQU/LABEL(md) | `src/LO_SYN.mad:390`, `include/LO_SYN.labels.md:724` | 524B | 2 |
| `MEM_5377` | EQU/LABEL(md) | `src/LO_SYN.mad:45`, `include/LO_SYN.labels.md:589` | 5377B | 2 |
| `MEM_70104` | EQU/LABEL(md) | `src/LO_SYN.mad:266`, `include/LO_SYN.labels.md:684` | 70104B | 2 |
| `MEM_71551` | EQU/LABEL(md) | `src/LO_SYN.mad:175`, `include/LO_SYN.labels.md:640` | 71551B | 2 |
| `MEM_74124` | EQU/LABEL(md) | `src/LO_SYN.mad:224`, `include/LO_SYN.labels.md:665` | 74124B | 2 |
| `MEM_74440` | EQU/LABEL(md) | `src/LO_SYN.mad:524`, `include/LO_SYN.labels.md:771` | 74440B | 2 |
| `MEM_74501` | EQU/LABEL(md) | `src/LO_SYN.mad:298`, `include/LO_SYN.labels.md:697` | 74501B | 2 |
| `MEM_74554` | EQU/LABEL(md) | `src/LO_SYN.mad:198`, `include/LO_SYN.labels.md:651` | 74554B | 2 |
| `MEM_76104` | EQU/LABEL(md) | `src/LO_SYN.mad:494`, `include/LO_SYN.labels.md:761` | 76104B | 2 |
| `MEM_76105` | EQU/LABEL(md) | `src/LO_SYN.mad:206`, `include/LO_SYN.labels.md:657` | 76105B | 2 |
| `MEM_77104` | EQU/LABEL(md) | `src/LO_SYN.mad:568`, `include/LO_SYN.labels.md:783` | 77104B | 2 |
| `MEM_77110` | EQU/LABEL(md) | `src/LO_SYN.mad:450`, `include/LO_SYN.labels.md:742` | 77110B | 2 |
| `MEM_77560` | EQU/LABEL(md) | `src/LO_SYN.mad:316`, `include/LO_SYN.labels.md:702` | 77560B | 2 |
| `MODVAL_11347` | EQU/LABEL(md) | `src/LO_GEN.mad:244`, `include/LO_GEN.labels.md:1296` | 11347 | 2 |
| `MODVAL_12516` | EQU/LABEL(md) | `src/LO_GEN.mad:247`, `include/LO_GEN.labels.md:1299` | 12516 | 2 |
| `MODVAL_16448` | EQU/LABEL(md) | `src/LO_GEN.mad:248`, `include/LO_GEN.labels.md:1300` | 16448 | 2 |
| `MODVAL_70103` | EQU/LABEL(md) | `src/LO_SYN.mad:339`, `include/LO_SYN.labels.md:424` | 70103B | 2 |
| `MODVAL_70120` | EQU/LABEL(md) | `src/LO_SYN.mad:382`, `include/LO_SYN.labels.md:430` | 70120B | 2 |
| `MODVAL_70151` | EQU/LABEL(md) | `src/LO_SYN.mad:349`, `include/LO_SYN.labels.md:426` | 70151B | 2 |
| `MODVAL_70160` | EQU/LABEL(md) | `src/LO_SYN.mad:365`, `include/LO_SYN.labels.md:428` | 70160B | 2 |
| `NEG_2` | EQU/LABEL(md) | `src/LO_GEN.mad:268`, `include/LO_GEN.labels.md:1320` | -2 | 2 |
| `NOLISFL*` | COMMON | `src/FOREX_CORE.mad:151`, `src/LO_SYN.mad:21`, `include/FOREX_ROOT.mad:64` | ONE_WORD | 2 |
| `PAGE_MODE_73401` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:38`, `include/FOREX.labels.md:326` | =73401 | 2 |
| `PG_EX67_SAVE` | COMMON | `include/FOREX_ROOT.mad:289` | ONE_WORD | 2 |
| `PG_FLAG_SAVE` | COMMON/LABEL(md) | `include/FOREX_ROOT.mad:288`, `include/FOREX.labels.md:88` | ONE_WORD | 2 |
| `PG_SHIFT_WORD` | COMMON | `include/FOREX_ROOT.mad:287` | ONE_WORD | 2 |
| `PG_STEP_2` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:57`, `include/FOREX.labels.md:345` | 2 | 2 |
| `PG_WORK_BASE` | LABEL/LABEL(md) | `include/FOREX_ROOT.mad:242`, `include/FOREX.labels.md:87` | — | 2 |
| `REGSEL_7` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:264`, `src/LO_GEN.mad:554`, `src/LO_GEN.mad:691`, `src/LO_GEN.mad:697`, `src/LO_GEN.mad:706`, `src/LO_GEN.mad:712` … (+210) | 7 | 2 |
| `REGVAL_102` | EQU/LABEL(md) | `src/LO_SYN.mad:525`, `include/LO_SYN.labels.md:544` | 102B | 2 |
| `REGVAL_151` | EQU/LABEL(md) | `src/LO_SYN.mad:120`, `include/LO_SYN.labels.md:501` | 151B | 2 |
| `REGVAL_16` | EQU/LABEL(md) | `src/LO_SYN.mad:64`, `include/LO_SYN.labels.md:495` | 16B | 2 |
| `REGVAL_17` | EQU/LABEL(md) | `src/LO_SYN.mad:54`, `include/LO_SYN.labels.md:492` | 17B | 2 |
| `REGVAL_30274` | EQU/LABEL(md) | `src/LO_SYN.mad:53`, `include/LO_SYN.labels.md:491` | 30274B | 2 |
| `REGVAL_40440` | EQU/LABEL(md) | `src/LO_SYN.mad:464`, `include/LO_SYN.labels.md:534` | 40440B | 2 |
| `REGVAL_40544` | EQU/LABEL(md) | `src/LO_SYN.mad:284`, `include/LO_SYN.labels.md:520` | 40544B | 2 |
| `REGVAL_4105` | EQU/LABEL(md) | `src/LO_SYN.mad:141`, `include/LO_SYN.labels.md:504` | 4105B | 2 |
| `REGVAL_44101` | EQU/LABEL(md) | `src/LO_SYN.mad:511`, `include/LO_SYN.labels.md:540` | 44101B | 2 |
| `REGVAL_47510` | EQU/LABEL(md) | `src/LO_SYN.mad:144`, `include/LO_SYN.labels.md:505` | 47510B | 2 |
| `REGVAL_6105` | EQU/LABEL(md) | `src/LO_SYN.mad:222`, `include/LO_SYN.labels.md:513` | 6105B | 2 |
| `REGVAL_70040` | EQU/LABEL(md) | `src/LO_SYN.mad:377`, `include/LO_SYN.labels.md:529` | 70040B | 2 |
| `REGVAL_70102` | EQU/LABEL(md) | `src/LO_SYN.mad:522`, `include/LO_SYN.labels.md:543` | 70102B | 2 |
| `REGVAL_70160` | EQU/LABEL(md) | `src/LO_SYN.mad:347`, `include/LO_SYN.labels.md:527` | 70160B | 2 |
| `REGVAL_7554` | EQU/LABEL(md) | `src/LO_SYN.mad:195`, `include/LO_SYN.labels.md:510` | 7554B | 2 |
| `REGVAL_76551` | EQU/LABEL(md) | `src/LO_SYN.mad:125`, `include/LO_SYN.labels.md:502` | 76551B | 2 |
| `RET` | COMMON | `src/FOREX_CORE.mad:157` | ONE_WORD | 2 |
| `STACK_OFF_M5` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:79`, `include/FOREX.labels.md:271` | -5 | 2 |
| `SVCELL_1` | EQU/LABEL(md) | `src/LO_SYN.mad:48`, `include/LO_SYN.labels.md:443` | 1B | 2 |
| `ZERO` | TEXT | `src/FOREX_RUNTIME.mad:478`, `src/FOREX_RUNTIME.mad:516` | TEXT_LIT_000000 | 2 |
| `*00014` | LABEL | `src/FOREX_RUNTIME.mad:224` | — | 1 |
| `*00066` | LABEL | `src/FOREX_RUNTIME.mad:306` | — | 1 |
| `*00067` | LABEL | `src/FOREX_RUNTIME.mad:307` | — | 1 |
| `*00073` | LABEL | `src/FOREX_RUNTIME.mad:311` | — | 1 |
| `*00075` | LABEL | `src/FOREX_RUNTIME.mad:313` | — | 1 |
| `*00101` | TEXT | `src/FOREX_RUNTIME.mad:318` | TEXT_LIT_6HERROR | 1 |
| `ADDR_1010` | EQU/LABEL(md) | `src/LO_GEN.mad:50`, `include/LO_GEN.labels.md:1098` | 1010B | 1 |
| `ADDR_1017` | EQU/LABEL(md) | `src/LO_GEN.mad:51`, `include/LO_GEN.labels.md:1099` | 1017B | 1 |
| `ADDR_102` | EQU/LABEL(md) | `src/LO_GEN.mad:52`, `include/LO_GEN.labels.md:1100` | 102B | 1 |
| `ADDR_1021` | EQU/LABEL(md) | `src/LO_GEN.mad:53`, `include/LO_GEN.labels.md:1101` | 1021B | 1 |
| `ADDR_103` | EQU/LABEL(md) | `src/LO_GEN.mad:54`, `include/LO_GEN.labels.md:1102` | 103B | 1 |
| `ADDR_1031` | EQU/LABEL(md) | `src/LO_GEN.mad:55`, `include/LO_GEN.labels.md:1103` | 1031B | 1 |
| `ADDR_1035` | EQU/LABEL(md) | `src/LO_GEN.mad:56`, `include/LO_GEN.labels.md:1104` | 1035B | 1 |
| `ADDR_104` | EQU/LABEL(md) | `src/LO_GEN.mad:57`, `include/LO_GEN.labels.md:1105` | 104B | 1 |
| `ADDR_1044` | EQU/LABEL(md) | `src/LO_GEN.mad:58`, `include/LO_GEN.labels.md:1106` | 1044B | 1 |
| `ADDR_105` | EQU/LABEL(md) | `src/LO_GEN.mad:59`, `include/LO_GEN.labels.md:1107` | 105B | 1 |
| `ADDR_1210` | EQU/LABEL(md) | `src/LO_GEN.mad:63`, `include/LO_GEN.labels.md:1111` | 1210B | 1 |
| `ADDR_127` | EQU/LABEL(md) | `src/LO_GEN.mad:64`, `include/LO_GEN.labels.md:1112` | 127B | 1 |
| `ADDR_1322` | EQU/LABEL(md) | `src/LO_GEN.mad:67`, `include/LO_GEN.labels.md:1115` | 1322B | 1 |
| `ADDR_1324` | EQU/LABEL(md) | `src/LO_GEN.mad:68`, `include/LO_GEN.labels.md:1116` | 1324B | 1 |
| `ADDR_1326` | EQU/LABEL(md) | `src/LO_GEN.mad:69`, `include/LO_GEN.labels.md:1117` | 1326B | 1 |
| `ADDR_1330` | EQU/LABEL(md) | `src/LO_GEN.mad:71`, `include/LO_GEN.labels.md:1119` | 1330B | 1 |
| `ADDR_1332` | EQU/LABEL(md) | `src/LO_GEN.mad:72`, `include/LO_GEN.labels.md:1120` | 1332B | 1 |
| `ADDR_1334` | EQU/LABEL(md) | `src/LO_GEN.mad:73`, `include/LO_GEN.labels.md:1121` | 1334B | 1 |
| `ADDR_1336` | EQU/LABEL(md) | `src/LO_GEN.mad:74`, `include/LO_GEN.labels.md:1122` | 1336B | 1 |
| `ADDR_1343` | EQU/LABEL(md) | `src/LO_GEN.mad:76`, `include/LO_GEN.labels.md:1124` | 1343B | 1 |
| `ADDR_1347` | EQU/LABEL(md) | `src/LO_GEN.mad:77`, `include/LO_GEN.labels.md:1125` | 1347B | 1 |
| `ADDR_1355` | EQU/LABEL(md) | `src/LO_GEN.mad:80`, `include/LO_GEN.labels.md:1128` | 1355B | 1 |
| `ADDR_1374` | EQU/LABEL(md) | `src/LO_GEN.mad:85`, `include/LO_GEN.labels.md:1133` | 1374B | 1 |
| `ADDR_1437` | EQU/LABEL(md) | `src/LO_GEN.mad:91`, `include/LO_GEN.labels.md:1139` | 1437B | 1 |
| `ADDR_151` | EQU/LABEL(md) | `src/LO_GEN.mad:93`, `include/LO_GEN.labels.md:1141` | 151B | 1 |
| `ADDR_1543` | EQU/LABEL(md) | `src/LO_GEN.mad:95`, `include/LO_GEN.labels.md:1143` | 1543B | 1 |
| `ADDR_1641` | EQU/LABEL(md) | `src/LO_GEN.mad:97`, `include/LO_GEN.labels.md:1145` | 1641B | 1 |
| `ADDR_1647` | EQU/LABEL(md) | `src/LO_GEN.mad:98`, `include/LO_GEN.labels.md:1146` | 1647B | 1 |
| `ADDR_211` | EQU/LABEL(md) | `src/LO_GEN.mad:104`, `include/LO_GEN.labels.md:1152` | 211B | 1 |
| `ADDR_2254` | EQU/LABEL(md) | `src/LO_GEN.mad:107`, `include/LO_GEN.labels.md:1155` | 2254B | 1 |
| `ADDR_22662` | EQU/LABEL(md) | `src/LO_GEN.mad:108`, `include/LO_GEN.labels.md:1156` | 22662B | 1 |
| `ADDR_25` | EQU/LABEL(md) | `src/LO_GEN.mad:111`, `include/LO_GEN.labels.md:1159` | 25B | 1 |
| `ADDR_30312` | EQU/LABEL(md) | `src/LO_GEN.mad:117`, `include/LO_GEN.labels.md:1165` | 30312B | 1 |
| `ADDR_370` | EQU/LABEL(md) | `src/LO_GEN.mad:126`, `include/LO_GEN.labels.md:1174` | 370B | 1 |
| `ADDR_4` | EQU/LABEL(md) | `src/LO_GEN.mad:127`, `include/LO_GEN.labels.md:1175` | 4B | 1 |
| `ADDR_40` | EQU/LABEL(md) | `src/LO_GEN.mad:128`, `include/LO_GEN.labels.md:1176` | 40B | 1 |
| `ADDR_40227` | EQU/LABEL(md) | `src/LO_GEN.mad:130`, `include/LO_GEN.labels.md:1178` | 40227B | 1 |
| `ADDR_40377` | EQU/LABEL(md) | `src/LO_GEN.mad:131`, `include/LO_GEN.labels.md:1179` | 40377B | 1 |
| `ADDR_40401` | EQU/LABEL(md) | `src/LO_GEN.mad:132`, `include/LO_GEN.labels.md:1180` | 40401B | 1 |
| `ADDR_40403` | EQU/LABEL(md) | `src/LO_GEN.mad:133`, `include/LO_GEN.labels.md:1181` | 40403B | 1 |
| `ADDR_40405` | EQU/LABEL(md) | `src/LO_GEN.mad:134`, `include/LO_GEN.labels.md:1182` | 40405B | 1 |
| `ADDR_40407` | EQU/LABEL(md) | `src/LO_GEN.mad:135`, `include/LO_GEN.labels.md:1183` | 40407B | 1 |
| `ADDR_40417` | EQU/LABEL(md) | `src/LO_GEN.mad:137`, `include/LO_GEN.labels.md:1185` | 40417B | 1 |
| `ADDR_40421` | EQU/LABEL(md) | `src/LO_GEN.mad:138`, `include/LO_GEN.labels.md:1186` | 40421B | 1 |
| `ADDR_40423` | EQU/LABEL(md) | `src/LO_GEN.mad:139`, `include/LO_GEN.labels.md:1187` | 40423B | 1 |
| `ADDR_40433` | EQU/LABEL(md) | `src/LO_GEN.mad:141`, `include/LO_GEN.labels.md:1189` | 40433B | 1 |
| `ADDR_40435` | EQU/LABEL(md) | `src/LO_GEN.mad:142`, `include/LO_GEN.labels.md:1190` | 40435B | 1 |
| `ADDR_40445` | EQU/LABEL(md) | `src/LO_GEN.mad:144`, `include/LO_GEN.labels.md:1192` | 40445B | 1 |
| `ADDR_40447` | EQU/LABEL(md) | `src/LO_GEN.mad:145`, `include/LO_GEN.labels.md:1193` | 40447B | 1 |
| `ADDR_40451` | EQU/LABEL(md) | `src/LO_GEN.mad:146`, `include/LO_GEN.labels.md:1194` | 40451B | 1 |
| `ADDR_40453` | EQU/LABEL(md) | `src/LO_GEN.mad:147`, `include/LO_GEN.labels.md:1195` | 40453B | 1 |
| `ADDR_40455` | EQU/LABEL(md) | `src/LO_GEN.mad:148`, `include/LO_GEN.labels.md:1196` | 40455B | 1 |
| `ADDR_40457` | EQU/LABEL(md) | `src/LO_GEN.mad:149`, `include/LO_GEN.labels.md:1197` | 40457B | 1 |
| `ADDR_40461` | EQU/LABEL(md) | `src/LO_GEN.mad:150`, `include/LO_GEN.labels.md:1198` | 40461B | 1 |
| `ADDR_40463` | EQU/LABEL(md) | `src/LO_GEN.mad:151`, `include/LO_GEN.labels.md:1199` | 40463B | 1 |
| `ADDR_40465` | EQU/LABEL(md) | `src/LO_GEN.mad:152`, `include/LO_GEN.labels.md:1200` | 40465B | 1 |
| `ADDR_40467` | EQU/LABEL(md) | `src/LO_GEN.mad:153`, `include/LO_GEN.labels.md:1201` | 40467B | 1 |
| `ADDR_41` | EQU/LABEL(md) | `src/LO_GEN.mad:154`, `include/LO_GEN.labels.md:1202` | 41B | 1 |
| `ADDR_42` | EQU/LABEL(md) | `src/LO_GEN.mad:156`, `include/LO_GEN.labels.md:1204` | 42B | 1 |
| `ADDR_46126` | EQU/LABEL(md) | `src/LO_GEN.mad:164`, `include/LO_GEN.labels.md:1212` | 46126B | 1 |
| `ADDR_47` | EQU/LABEL(md) | `src/LO_GEN.mad:165`, `include/LO_GEN.labels.md:1213` | 47B | 1 |
| `ADDR_471` | EQU/LABEL(md) | `src/LO_GEN.mad:166`, `include/LO_GEN.labels.md:1214` | 471B | 1 |
| `ADDR_47753` | EQU/LABEL(md) | `src/LO_GEN.mad:167`, `include/LO_GEN.labels.md:1215` | 47753B | 1 |
| `ADDR_50520` | EQU/LABEL(md) | `src/LO_GEN.mad:170`, `include/LO_GEN.labels.md:1218` | 50520B | 1 |
| `ADDR_52` | EQU/LABEL(md) | `src/LO_GEN.mad:173`, `include/LO_GEN.labels.md:1221` | 52B | 1 |
| `ADDR_52117` | EQU/LABEL(md) | `src/LO_GEN.mad:174`, `include/LO_GEN.labels.md:1222` | 52117B | 1 |
| `ADDR_523` | EQU/LABEL(md) | `src/LO_GEN.mad:175`, `include/LO_GEN.labels.md:1223` | 523B | 1 |
| `ADDR_52514` | EQU/LABEL(md) | `src/LO_GEN.mad:176`, `include/LO_GEN.labels.md:1224` | 52514B | 1 |
| `ADDR_5257` | EQU/LABEL(md) | `src/LO_GEN.mad:177`, `include/LO_GEN.labels.md:1225` | 5257B | 1 |
| `ADDR_53257` | EQU/LABEL(md) | `src/LO_GEN.mad:179`, `include/LO_GEN.labels.md:1227` | 53257B | 1 |
| `ADDR_5377` | EQU/LABEL(md) | `src/LO_GEN.mad:180`, `include/LO_GEN.labels.md:1228` | 5377B | 1 |
| `ADDR_54` | EQU/LABEL(md) | `src/LO_GEN.mad:181`, `include/LO_GEN.labels.md:1229` | 54B | 1 |
| `ADDR_565` | EQU/LABEL(md) | `src/LO_GEN.mad:184`, `include/LO_GEN.labels.md:1232` | 565B | 1 |
| `ADDR_56565` | EQU/LABEL(md) | `src/LO_GEN.mad:188`, `include/LO_GEN.labels.md:1236` | 56565B | 1 |
| `ADDR_56576` | EQU/LABEL(md) | `src/LO_GEN.mad:195`, `include/LO_GEN.labels.md:1243` | 56576B | 1 |
| `ADDR_56577` | EQU/LABEL(md) | `src/LO_GEN.mad:196`, `include/LO_GEN.labels.md:1244` | 56577B | 1 |
| `ADDR_56601` | EQU/LABEL(md) | `src/LO_GEN.mad:197`, `include/LO_GEN.labels.md:1245` | 56601B | 1 |
| `ADDR_56602` | EQU/LABEL(md) | `src/LO_GEN.mad:198`, `include/LO_GEN.labels.md:1246` | 56602B | 1 |
| `ADDR_56610` | EQU/LABEL(md) | `src/LO_GEN.mad:200`, `include/LO_GEN.labels.md:1248` | 56610B | 1 |
| `ADDR_56612` | EQU/LABEL(md) | `src/LO_GEN.mad:201`, `include/LO_GEN.labels.md:1249` | 56612B | 1 |
| `ADDR_56613` | EQU/LABEL(md) | `src/LO_GEN.mad:202`, `include/LO_GEN.labels.md:1250` | 56613B | 1 |
| `ADDR_56616` | EQU/LABEL(md) | `src/LO_GEN.mad:204`, `include/LO_GEN.labels.md:1252` | 56616B | 1 |
| `ADDR_56623` | EQU/LABEL(md) | `src/LO_GEN.mad:208`, `include/LO_GEN.labels.md:1256` | 56623B | 1 |
| `ADDR_567` | EQU/LABEL(md) | `src/LO_GEN.mad:210`, `include/LO_GEN.labels.md:1258` | 567B | 1 |
| `ADDR_57` | EQU/LABEL(md) | `src/LO_GEN.mad:211`, `include/LO_GEN.labels.md:1259` | 57B | 1 |
| `ADDR_577` | EQU/LABEL(md) | `src/LO_GEN.mad:212`, `include/LO_GEN.labels.md:1260` | 577B | 1 |
| `ADDR_60` | EQU/LABEL(md) | `src/LO_GEN.mad:214`, `include/LO_GEN.labels.md:1262` | 60B | 1 |
| `ADDR_601` | EQU/LABEL(md) | `src/LO_GEN.mad:215`, `include/LO_GEN.labels.md:1263` | 601B | 1 |
| `ADDR_61` | EQU/LABEL(md) | `src/LO_GEN.mad:217`, `include/LO_GEN.labels.md:1265` | 61B | 1 |
| `ADDR_63` | EQU/LABEL(md) | `src/LO_GEN.mad:219`, `include/LO_GEN.labels.md:1267` | 63B | 1 |
| `ADDR_64` | EQU/LABEL(md) | `src/LO_GEN.mad:220`, `include/LO_GEN.labels.md:1268` | 64B | 1 |
| `ADDR_65` | EQU/LABEL(md) | `src/LO_GEN.mad:221`, `include/LO_GEN.labels.md:1269` | 65B | 1 |
| `ADDR_656` | EQU/LABEL(md) | `src/LO_GEN.mad:222`, `include/LO_GEN.labels.md:1270` | 656B | 1 |
| `ADDR_66` | EQU/LABEL(md) | `src/LO_GEN.mad:223`, `include/LO_GEN.labels.md:1271` | 66B | 1 |
| `ADDR_70` | EQU/LABEL(md) | `src/LO_GEN.mad:226`, `include/LO_GEN.labels.md:1274` | 70B | 1 |
| `ADDR_70022` | EQU/LABEL(md) | `src/LO_GEN.mad:227`, `include/LO_GEN.labels.md:1275` | 70022B | 1 |
| `ADDR_70274` | EQU/LABEL(md) | `src/LO_GEN.mad:229`, `include/LO_GEN.labels.md:1277` | 70274B | 1 |
| `ADDR_71` | EQU/LABEL(md) | `src/LO_GEN.mad:230`, `include/LO_GEN.labels.md:1278` | 71B | 1 |
| `ADDR_72` | EQU/LABEL(md) | `src/LO_GEN.mad:231`, `include/LO_GEN.labels.md:1279` | 72B | 1 |
| `ADDR_73` | EQU/LABEL(md) | `src/LO_GEN.mad:232`, `include/LO_GEN.labels.md:1280` | 73B | 1 |
| `ADDR_74` | EQU/LABEL(md) | `src/LO_GEN.mad:233`, `include/LO_GEN.labels.md:1281` | 74B | 1 |
| `ADDR_746` | EQU/LABEL(md) | `src/LO_GEN.mad:234`, `include/LO_GEN.labels.md:1282` | 746B | 1 |
| `ADDR_75` | EQU/LABEL(md) | `src/LO_GEN.mad:236`, `include/LO_GEN.labels.md:1284` | 75B | 1 |
| `ADDR_75107` | EQU/LABEL(md) | `src/LO_GEN.mad:237`, `include/LO_GEN.labels.md:1285` | 75107B | 1 |
| `ADDR_75111` | EQU/LABEL(md) | `src/LO_GEN.mad:238`, `include/LO_GEN.labels.md:1286` | 75111B | 1 |
| `ADDR_76` | EQU/LABEL(md) | `src/LO_GEN.mad:239`, `include/LO_GEN.labels.md:1287` | 76B | 1 |
| `ADDR_77` | EQU/LABEL(md) | `src/LO_GEN.mad:241`, `include/LO_GEN.labels.md:1289` | 77B | 1 |
| `ADDR_777` | EQU/LABEL(md) | `src/LO_GEN.mad:242`, `include/LO_GEN.labels.md:1290` | 777B | 1 |
| `ADDR_OCT_4000` | EQU/LABEL(md) | `src/FOREX_CORE.mad:33`, `include/FOREX.labels.md:104` | 0o4000 | 1 |
| `ADDR_OCT_50` | EQU/LABEL(md) | `src/FOREX_CORE.mad:34`, `include/FOREX.labels.md:105` | 0o50 | 1 |
| `ADRPTR_1111` | EQU/LABEL(md) | `src/LO_SYN.mad:629`, `include/LO_SYN.labels.md:407` | 1111B | 1 |
| `ADRPTR_1314` | EQU/LABEL(md) | `src/LO_SYN.mad:645`, `include/LO_SYN.labels.md:408` | 1314B | 1 |
| `ADRPTR_2003` | EQU/LABEL(md) | `src/LO_SYN.mad:660`, `include/LO_SYN.labels.md:409` | 2003B | 1 |
| `ADRPTR_2004` | EQU/LABEL(md) | `src/LO_SYN.mad:661`, `include/LO_SYN.labels.md:410` | 2004B | 1 |
| `ADRPTR_20106` | EQU/LABEL(md) | `src/LO_SYN.mad:250`, `include/LO_SYN.labels.md:367` | 20106B | 1 |
| `ADRPTR_20111` | EQU/LABEL(md) | `src/LO_SYN.mad:577`, `include/LO_SYN.labels.md:403` | 20111B | 1 |
| `ADRPTR_20115` | EQU/LABEL(md) | `src/LO_SYN.mad:386`, `include/LO_SYN.labels.md:382` | 20115B | 1 |
| `ADRPTR_20160` | EQU/LABEL(md) | `src/LO_SYN.mad:83`, `include/LO_SYN.labels.md:356` | 20160B | 1 |
| `ADRPTR_3001` | EQU/LABEL(md) | `src/LO_SYN.mad:666`, `include/LO_SYN.labels.md:411` | 3001B | 1 |
| `ADRPTR_30312` | EQU/LABEL(md) | `src/LO_SYN.mad:68`, `include/LO_SYN.labels.md:354` | 30312B | 1 |
| `ADRPTR_3101` | EQU/LABEL(md) | `src/LO_SYN.mad:672`, `include/LO_SYN.labels.md:412` | 3101B | 1 |
| `ADRPTR_314` | EQU/LABEL(md) | `src/LO_SYN.mad:594`, `include/LO_SYN.labels.md:405` | 314B | 1 |
| `ADRPTR_4011` | EQU/LABEL(md) | `src/LO_SYN.mad:686`, `include/LO_SYN.labels.md:413` | 4011B | 1 |
| `ADRPTR_4022` | EQU/LABEL(md) | `src/LO_SYN.mad:696`, `include/LO_SYN.labels.md:414` | 4022B | 1 |
| `ADRPTR_40560` | EQU/LABEL(md) | `src/LO_SYN.mad:328`, `include/LO_SYN.labels.md:378` | 40560B | 1 |
| `ADRPTR_41101` | EQU/LABEL(md) | `src/LO_SYN.mad:388`, `include/LO_SYN.labels.md:383` | 41101B | 1 |
| `ADRPTR_41501` | EQU/LABEL(md) | `src/LO_SYN.mad:325`, `include/LO_SYN.labels.md:377` | 41501B | 1 |
| `ADRPTR_41554` | EQU/LABEL(md) | `src/LO_SYN.mad:436`, `include/LO_SYN.labels.md:390` | 41554B | 1 |
| `ADRPTR_4201` | EQU/LABEL(md) | `src/LO_SYN.mad:725`, `include/LO_SYN.labels.md:415` | 4201B | 1 |
| `ADRPTR_43055` | EQU/LABEL(md) | `src/LO_SYN.mad:567`, `include/LO_SYN.labels.md:401` | 43055B | 1 |
| `ADRPTR_44101` | EQU/LABEL(md) | `src/LO_SYN.mad:554`, `include/LO_SYN.labels.md:398` | 44101B | 1 |
| `ADRPTR_4416` | EQU/LABEL(md) | `src/LO_SYN.mad:752`, `include/LO_SYN.labels.md:416` | 4416B | 1 |
| `ADRPTR_45501` | EQU/LABEL(md) | `src/LO_SYN.mad:495`, `include/LO_SYN.labels.md:393` | 45501B | 1 |
| `ADRPTR_46501` | EQU/LABEL(md) | `src/LO_SYN.mad:318`, `include/LO_SYN.labels.md:376` | 46501B | 1 |
| `ADRPTR_505` | EQU/LABEL(md) | `src/LO_SYN.mad:608`, `include/LO_SYN.labels.md:406` | 505B | 1 |
| `ADRPTR_52110` | EQU/LABEL(md) | `src/LO_SYN.mad:304`, `include/LO_SYN.labels.md:372` | 52110B | 1 |
| `ADRPTR_54040` | EQU/LABEL(md) | `src/LO_SYN.mad:547`, `include/LO_SYN.labels.md:396` | 54040B | 1 |
| `ADRPTR_61440` | EQU/LABEL(md) | `src/LO_SYN.mad:333`, `include/LO_SYN.labels.md:379` | 61440B | 1 |
| `ADRPTR_66161` | EQU/LABEL(md) | `src/LO_SYN.mad:528`, `include/LO_SYN.labels.md:395` | 66161B | 1 |
| `ADRPTR_70101` | EQU/LABEL(md) | `src/LO_SYN.mad:445`, `include/LO_SYN.labels.md:391` | 70101B | 1 |
| `ADRPTR_70440` | EQU/LABEL(md) | `src/LO_SYN.mad:566`, `include/LO_SYN.labels.md:400` | 70440B | 1 |
| `ADRPTR_73105` | EQU/LABEL(md) | `src/LO_SYN.mad:211`, `include/LO_SYN.labels.md:365` | 73105B | 1 |
| `ADRPTR_75505` | EQU/LABEL(md) | `src/LO_SYN.mad:581`, `include/LO_SYN.labels.md:404` | 75505B | 1 |
| `ADRPTR_77105` | EQU/LABEL(md) | `src/LO_SYN.mad:571`, `include/LO_SYN.labels.md:402` | 77105B | 1 |
| `ALL_ONES_MASK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:27`, `include/FOREX.labels.md:219` | 77777B | 1 |
| `B` | LABEL(md) | `include/FOREX.labels.md:62`, `include/LO_SYN.labels.md:48` | — | 1 |
| `BASE16_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:36`, `include/FOREX.labels.md:107` | 74001B | 1 |
| `C` | LABEL(md) | `include/FOREX.labels.md:68`, `include/FOREX.labels.md:87` | — | 1 |
| `C10` | LABEL | `src/FOREX_RUNTIME.mad:513` | — | 1 |
| `CHECKFL*` | COMMON | `include/FOREX_ROOT.mad:66` | 1 | 1 |
| `CHECK_ADDR` | LABEL(md) | `include/FOREX.labels.md:110` | — | 1 |
| `CORE_ADDR_11200` | LABEL(md) | `include/FOREX.labels.md:111` | — | 1 |
| `CORE_ADDR_1200` | LABEL(md) | `include/FOREX.labels.md:112` | — | 1 |
| `CORE_ADDR_1247` | LABEL(md) | `include/FOREX.labels.md:113` | — | 1 |
| `CORE_ADDR_1263` | LABEL(md) | `include/FOREX.labels.md:114` | — | 1 |
| `CORE_ADDR_16617` | LABEL(md) | `include/FOREX.labels.md:115` | — | 1 |
| `CORE_ADDR_231` | LABEL(md) | `include/FOREX.labels.md:116` | — | 1 |
| `CORE_ADDR_30453` | LABEL(md) | `include/FOREX.labels.md:117` | — | 1 |
| `CORE_ADDR_31056` | LABEL(md) | `include/FOREX.labels.md:118` | — | 1 |
| `CORE_ADDR_36464` | LABEL(md) | `include/FOREX.labels.md:119` | — | 1 |
| `CORE_ADDR_37013` | LABEL(md) | `include/FOREX.labels.md:120` | — | 1 |
| `CORE_ADDR_4040` | LABEL(md) | `include/FOREX.labels.md:121` | — | 1 |
| `CORE_ADDR_4041` | LABEL(md) | `include/FOREX.labels.md:122` | — | 1 |
| `CORE_ADDR_4042` | LABEL(md) | `include/FOREX.labels.md:123` | — | 1 |
| `CORE_ADDR_4043` | LABEL(md) | `include/FOREX.labels.md:124` | — | 1 |
| `CORE_ADDR_4044` | LABEL(md) | `include/FOREX.labels.md:125` | — | 1 |
| `CORE_ADDR_4045` | LABEL(md) | `include/FOREX.labels.md:126` | — | 1 |
| `CORE_ADDR_4046` | LABEL(md) | `include/FOREX.labels.md:127` | — | 1 |
| `CORE_ADDR_4047` | LABEL(md) | `include/FOREX.labels.md:128` | — | 1 |
| `CORE_ADDR_4050` | LABEL(md) | `include/FOREX.labels.md:129` | — | 1 |
| `CORE_ADDR_4051` | LABEL(md) | `include/FOREX.labels.md:130` | — | 1 |
| `CORE_ADDR_4052` | LABEL(md) | `include/FOREX.labels.md:131` | — | 1 |
| `CORE_ADDR_4053` | LABEL(md) | `include/FOREX.labels.md:132` | — | 1 |
| `CORE_ADDR_4054` | LABEL(md) | `include/FOREX.labels.md:133` | — | 1 |
| `CORE_ADDR_4055` | LABEL(md) | `include/FOREX.labels.md:134` | — | 1 |
| `CORE_ADDR_4056` | LABEL(md) | `include/FOREX.labels.md:135` | — | 1 |
| `CORE_ADDR_4144` | LABEL(md) | `include/FOREX.labels.md:136` | — | 1 |
| `CORE_ADDR_44000` | LABEL(md) | `include/FOREX.labels.md:137` | 0o044000 | 1 |
| `CORE_ADDR_44745` | LABEL(md) | `include/FOREX.labels.md:138` | 0o044745 | 1 |
| `CORE_ADDR_4543` | LABEL(md) | `include/FOREX.labels.md:139` | — | 1 |
| `CORE_ADDR_46555` | LABEL(md) | `include/FOREX.labels.md:140` | 0o046555 | 1 |
| `CORE_ADDR_5317` | LABEL(md) | `include/FOREX.labels.md:141` | — | 1 |
| `CORE_ADDR_55451` | LABEL(md) | `include/FOREX.labels.md:142` | 0o055451 | 1 |
| `CORE_ADDR_56` | LABEL(md) | `include/FOREX.labels.md:143` | — | 1 |
| `CORE_ADDR_61200` | LABEL(md) | `include/FOREX.labels.md:144` | 0o061200 | 1 |
| `CORE_ADDR_6264` | LABEL(md) | `include/FOREX.labels.md:145` | — | 1 |
| `CORE_ADDR_6441` | LABEL(md) | `include/FOREX.labels.md:146` | — | 1 |
| `CORE_ADDR_70031` | LABEL(md) | `include/FOREX.labels.md:147` | 0o070031 | 1 |
| `CORE_ADDR_70035` | LABEL(md) | `include/FOREX.labels.md:148` | 0o070035 | 1 |
| `CORE_ADDR_70042` | LABEL(md) | `include/FOREX.labels.md:149` | 0o070042 | 1 |
| `CORE_ADDR_70043` | LABEL(md) | `include/FOREX.labels.md:150` | 0o070043 | 1 |
| `CORE_ADDR_70044` | LABEL(md) | `include/FOREX.labels.md:151` | 0o070044 | 1 |
| `CORE_ADDR_70045` | LABEL(md) | `include/FOREX.labels.md:152` | 0o070045 | 1 |
| `CORE_ADDR_70046` | LABEL(md) | `include/FOREX.labels.md:153` | 0o070046 | 1 |
| `CORE_ADDR_70047` | LABEL(md) | `include/FOREX.labels.md:154` | 0o070047 | 1 |
| `CORE_ADDR_70050` | LABEL(md) | `include/FOREX.labels.md:155` | 0o070050 | 1 |
| `CORE_ADDR_7017` | LABEL(md) | `include/FOREX.labels.md:156` | — | 1 |
| `CORE_ADDR_74757` | LABEL(md) | `include/FOREX.labels.md:157` | 0o074757 | 1 |
| `CORE_ADDR_75120` | LABEL(md) | `include/FOREX.labels.md:158` | 0o075120 | 1 |
| `CORE_ADDR_75451` | LABEL(md) | `include/FOREX.labels.md:159` | 0o075451 | 1 |
| `CORE_ADDR_75545` | LABEL(md) | `include/FOREX.labels.md:160` | 0o075545 | 1 |
| `CORE_ADDR_75663` | LABEL(md) | `include/FOREX.labels.md:161` | 0o075663 | 1 |
| `CORE_ADDR_76462` | LABEL(md) | `include/FOREX.labels.md:163` | 0o076462 | 1 |
| `CORE_WORD2` | LABEL(md) | `include/FOREX.labels.md:166` | — | 1 |
| `CORE_WORD4` | LABEL(md) | `include/FOREX.labels.md:167` | — | 1 |
| `CORE_WORD5` | LABEL(md) | `include/FOREX.labels.md:168` | — | 1 |
| `DATAPR_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:98`, `include/FOREX.labels.md:169` | 74010B | 1 |
| `DATA_WORD_0000000000077777` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:29`, `include/FOREX.labels.md:221` | 0000000000077777 | 1 |
| `DATA_WORD_00000000_00000001` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:31`, `include/FOREX.labels.md:223` | 00000000 00000001 | 1 |
| `DATA_WORD_00000000_00000002` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:32`, `include/FOREX.labels.md:224` | 00000000 00000002 | 1 |
| `DATA_WORD_00000000_00001777` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:33`, `include/FOREX.labels.md:225` | 00000000 00001777 | 1 |
| `DATA_WORD_00100000_00000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:34`, `include/FOREX.labels.md:226` | 00100000 00000000 | 1 |
| `DATA_WORD_17_7777_7777_7777` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:35`, `include/FOREX.labels.md:227` | 17 7777 7777 7777 | 1 |
| `DATA_WORD_37777774_77777477` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:36`, `include/FOREX.labels.md:228` | 37777774 77777477 | 1 |
| `DATA_WORD_77270707_00000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:37`, `include/FOREX.labels.md:229` | 77270707 00000000 | 1 |
| `DATE0` | TEXT | `src/FOREX_RUNTIME.mad:406` | TEXT_LIT_6H_201_200_7 | 1 |
| `DATE1` | TEXT | `src/FOREX_RUNTIME.mad:407` | TEXT_LIT_2H_200 | 1 |
| `DATE2` | TEXT | `src/FOREX_RUNTIME.mad:411` | TEXT_LIT_6H000_00 | 1 |
| `DATE3` | TEXT | `src/FOREX_RUNTIME.mad:418` | TEXT_LIT_6H_00_00 | 1 |
| `DATE4` | COMMON | `src/FOREX_RUNTIME.mad:412` | — | 1 |
| `DATE_BUF_LEN` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:108`, `include/FOREX.labels.md:300` | 2 | 1 |
| `DATE_DAY_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:38`, `include/FOREX.labels.md:230` | 64+16 | 1 |
| `DATE_END_CHECK` | LABEL | `src/FOREX_RUNTIME.mad:381` | — | 1 |
| `DATE_GET` | COMMON/ENTRY/LABEL(md) | `src/FOREX_RUNTIME.mad:341`, `src/FOREX_RUNTIME.mad:342`, `include/FOREX.labels.md:59` | — | 1 |
| `DATE_MONTH_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:40`, `include/FOREX.labels.md:232` | 64+35 | 1 |
| `DATE_PARSE` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:348`, `include/FOREX.labels.md:60` | — | 1 |
| `DATE_PREP_BASE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:392`, `include/FOREX.labels.md:62` | — | 1 |
| `DATE_PRINT_RETURN` | LABEL/LABEL(md) | `src/FOREX_CORE.mad:222`, `include/FOREX_ROOT.mad:93`, `include/FOREX.labels.md:27`, `include/FOREX.labels.md:78` | — | 1 |
| `DATE_STACK_ADJUST` | LABEL | `src/FOREX_RUNTIME.mad:403` | — | 1 |
| `DATE_TIME_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:41`, `include/FOREX.labels.md:233` | 64-22 | 1 |
| `DATE_WTC_SET` | LABEL | `src/FOREX_RUNTIME.mad:362` | — | 1 |
| `DAY_MASK` | COMMON | `src/FOREX_RUNTIME.mad:419` | — | 1 |
| `DEC_38` | EQU/LABEL(md) | `src/FOREX_CORE.mad:99`, `include/FOREX.labels.md:170` | 38 | 1 |
| `DEC_43` | EQU/LABEL(md) | `src/FOREX_CORE.mad:100`, `include/FOREX.labels.md:171` | 43 | 1 |
| `DUMON_BASE_7` | EQU/LABEL(md) | `src/FOREX_CORE.mad:101`, `include/FOREX.labels.md:172` | 40007B | 1 |
| `DUMON_CELL4` | EQU/LABEL(md) | `src/FOREX_CORE.mad:102`, `include/FOREX.labels.md:173` | 4026B | 1 |
| `DUMON_CELL5` | EQU/LABEL(md) | `src/FOREX_CORE.mad:103`, `include/FOREX.labels.md:174` | 4027B | 1 |
| `DUMON_CELL6` | EQU/LABEL(md) | `src/FOREX_CORE.mad:104`, `include/FOREX.labels.md:175` | 4030B | 1 |
| `ERR_TRANSLATOR_TEXT` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:29`, `include/FOREX.labels.md:317` | 18H'200'0OШ | 1 |
| `EX20_20110` | EQU/LABEL(md) | `src/LO_SYN.mad:505`, `include/LO_SYN.labels.md:172` | 20110B | 1 |
| `EX20_20113` | EQU/LABEL(md) | `src/LO_SYN.mad:536`, `include/LO_SYN.labels.md:181` | 20113B | 1 |
| `EX20_20124` | EQU/LABEL(md) | `src/LO_SYN.mad:444`, `include/LO_SYN.labels.md:159` | 20124B | 1 |
| `EX20_20142` | EQU/LABEL(md) | `src/LO_SYN.mad:527`, `include/LO_SYN.labels.md:178` | 20142B | 1 |
| `EX20_20151` | EQU/LABEL(md) | `src/LO_SYN.mad:330`, `include/LO_SYN.labels.md:119` | 20151B | 1 |
| `EX20_20160` | EQU/LABEL(md) | `src/LO_SYN.mad:278`, `include/LO_SYN.labels.md:102` | 20160B | 1 |
| `EX20_40513` | EQU/LABEL(md) | `src/LO_SYN.mad:85`, `include/LO_SYN.labels.md:59` | 40513B | 1 |
| `EX20_40520` | EQU/LABEL(md) | `src/LO_SYN.mad:580`, `include/LO_SYN.labels.md:192` | 40520B | 1 |
| `EX20_42546` | EQU/LABEL(md) | `src/LO_SYN.mad:161`, `include/LO_SYN.labels.md:79` | 42546B | 1 |
| `EX20_42560` | EQU/LABEL(md) | `src/LO_SYN.mad:280`, `include/LO_SYN.labels.md:104` | 42560B | 1 |
| `EX20_4323` | EQU/LABEL(md) | `src/LO_SYN.mad:738`, `include/LO_SYN.labels.md:237` | 4323B | 1 |
| `EX20_4405` | EQU/LABEL(md) | `src/LO_SYN.mad:746`, `include/LO_SYN.labels.md:238` | 4405B | 1 |
| `EX20_44117` | EQU/LABEL(md) | `src/LO_SYN.mad:582`, `include/LO_SYN.labels.md:193` | 44117B | 1 |
| `EX20_44144` | EQU/LABEL(md) | `src/LO_SYN.mad:334`, `include/LO_SYN.labels.md:121` | 44144B | 1 |
| `EX20_45543` | EQU/LABEL(md) | `src/LO_SYN.mad:392`, `include/LO_SYN.labels.md:138` | 45543B | 1 |
| `EX20_47440` | EQU/LABEL(md) | `src/LO_SYN.mad:283`, `include/LO_SYN.labels.md:105` | 47440B | 1 |
| `EX20_47505` | EQU/LABEL(md) | `src/LO_SYN.mad:324`, `include/LO_SYN.labels.md:117` | 47505B | 1 |
| `EX20_47515` | EQU/LABEL(md) | `src/LO_SYN.mad:488`, `include/LO_SYN.labels.md:167` | 47515B | 1 |
| `EX20_47547` | EQU/LABEL(md) | `src/LO_SYN.mad:507`, `include/LO_SYN.labels.md:173` | 47547B | 1 |
| `EX20_62101` | EQU/LABEL(md) | `src/LO_SYN.mad:564`, `include/LO_SYN.labels.md:189` | 62101B | 1 |
| `EX20_64440` | EQU/LABEL(md) | `src/LO_SYN.mad:549`, `include/LO_SYN.labels.md:185` | 64440B | 1 |
| `EX20_64551` | EQU/LABEL(md) | `src/LO_SYN.mad:514`, `include/LO_SYN.labels.md:175` | 64551B | 1 |
| `EX20_64561` | EQU/LABEL(md) | `src/LO_SYN.mad:89`, `include/LO_SYN.labels.md:61` | 64561B | 1 |
| `EX20_64566` | EQU/LABEL(md) | `src/LO_SYN.mad:441`, `include/LO_SYN.labels.md:156` | 64566B | 1 |
| `EX20_74440` | EQU/LABEL(md) | `src/LO_SYN.mad:543`, `include/LO_SYN.labels.md:183` | 74440B | 1 |
| `EX20_75505` | EQU/LABEL(md) | `src/LO_SYN.mad:423`, `include/LO_SYN.labels.md:147` | 75505B | 1 |
| `EX20_77101` | EQU/LABEL(md) | `src/LO_SYN.mad:573`, `include/LO_SYN.labels.md:191` | 77101B | 1 |
| `EX21_1016` | EQU/LABEL(md) | `src/LO_SYN.mad:621`, `include/LO_SYN.labels.md:206` | 1016B | 1 |
| `EX21_1302` | EQU/LABEL(md) | `src/LO_SYN.mad:639`, `include/LO_SYN.labels.md:211` | 1302B | 1 |
| `EX21_326` | EQU/LABEL(md) | `src/LO_SYN.mad:601`, `include/LO_SYN.labels.md:199` | 326B | 1 |
| `EX21_4043` | EQU/LABEL(md) | `src/LO_SYN.mad:715`, `include/LO_SYN.labels.md:231` | 4043B | 1 |
| `EX36_1310` | EQU/LABEL(md) | `src/LO_SYN.mad:641`, `include/LO_SYN.labels.md:212` | 1310B | 1 |
| `EX36_20102` | EQU/LABEL(md) | `src/LO_SYN.mad:368`, `include/LO_SYN.labels.md:129` | 20102B | 1 |
| `EX36_20142` | EQU/LABEL(md) | `src/LO_SYN.mad:240`, `include/LO_SYN.labels.md:93` | 20142B | 1 |
| `EX36_317` | EQU/LABEL(md) | `src/LO_SYN.mad:596`, `include/LO_SYN.labels.md:196` | 317B | 1 |
| `EX36_4037` | EQU/LABEL(md) | `src/LO_SYN.mad:710`, `include/LO_SYN.labels.md:228` | 4037B | 1 |
| `EX36_4054` | EQU/LABEL(md) | `src/LO_SYN.mad:718`, `include/LO_SYN.labels.md:232` | 4054B | 1 |
| `EX36_44040` | EQU/LABEL(md) | `src/LO_SYN.mad:299`, `include/LO_SYN.labels.md:110` | 44040B | 1 |
| `EX36_44101` | EQU/LABEL(md) | `src/LO_SYN.mad:351`, `include/LO_SYN.labels.md:123` | 44101B | 1 |
| `EX36_45440` | EQU/LABEL(md) | `src/LO_SYN.mad:422`, `include/LO_SYN.labels.md:146` | 45440B | 1 |
| `EX36_45501` | EQU/LABEL(md) | `src/LO_SYN.mad:258`, `include/LO_SYN.labels.md:97` | 45501B | 1 |
| `EX36_45517` | EQU/LABEL(md) | `src/LO_SYN.mad:572`, `include/LO_SYN.labels.md:190` | 45517B | 1 |
| `EX36_501` | EQU/LABEL(md) | `src/LO_SYN.mad:604`, `include/LO_SYN.labels.md:200` | 501B | 1 |
| `EX36_50101` | EQU/LABEL(md) | `src/LO_SYN.mad:483`, `include/LO_SYN.labels.md:166` | 50101B | 1 |
| `EX36_51105` | EQU/LABEL(md) | `src/LO_SYN.mad:371`, `include/LO_SYN.labels.md:130` | 51105B | 1 |
| `EX36_52120` | EQU/LABEL(md) | `src/LO_SYN.mad:355`, `include/LO_SYN.labels.md:124` | 52120B | 1 |
| `EX36_61120` | EQU/LABEL(md) | `src/LO_SYN.mad:562`, `include/LO_SYN.labels.md:187` | 61120B | 1 |
| `EX36_61154` | EQU/LABEL(md) | `src/LO_SYN.mad:476`, `include/LO_SYN.labels.md:165` | 61154B | 1 |
| `EX36_62101` | EQU/LABEL(md) | `src/LO_SYN.mad:236`, `include/LO_SYN.labels.md:92` | 62101B | 1 |
| `EX36_62117` | EQU/LABEL(md) | `src/LO_SYN.mad:87`, `include/LO_SYN.labels.md:60` | 62117B | 1 |
| `EX36_63551` | EQU/LABEL(md) | `src/LO_SYN.mad:116`, `include/LO_SYN.labels.md:72` | 63551B | 1 |
| `EX36_66110` | EQU/LABEL(md) | `src/LO_SYN.mad:546`, `include/LO_SYN.labels.md:184` | 66110B | 1 |
| `EX36_66117` | EQU/LABEL(md) | `src/LO_SYN.mad:454`, `include/LO_SYN.labels.md:161` | 66117B | 1 |
| `EX36_66151` | EQU/LABEL(md) | `src/LO_SYN.mad:520`, `include/LO_SYN.labels.md:176` | 66151B | 1 |
| `EX36_70055` | EQU/LABEL(md) | `src/LO_SYN.mad:523`, `include/LO_SYN.labels.md:177` | 70055B | 1 |
| `EX46_4510` | EQU/LABEL(md) | `src/LO_SYN.mad:168`, `include/LO_SYN.labels.md:84` | 4510B | 1 |
| `EX47_4573` | EQU/LABEL(md) | `src/LO_SYN.mad:529`, `include/LO_SYN.labels.md:179` | 4573B | 1 |
| `EX50_1202` | EQU/LABEL(md) | `src/LO_SYN.mad:632`, `include/LO_SYN.labels.md:209` | 1202B | 1 |
| `EX50_1311` | EQU/LABEL(md) | `src/LO_SYN.mad:642`, `include/LO_SYN.labels.md:213` | 1311B | 1 |
| `EX50_1323` | EQU/LABEL(md) | `src/LO_SYN.mad:648`, `include/LO_SYN.labels.md:215` | 1323B | 1 |
| `EX50_1324` | EQU/LABEL(md) | `src/LO_SYN.mad:649`, `include/LO_SYN.labels.md:216` | 1324B | 1 |
| `EX50_323` | EQU/LABEL(md) | `src/LO_SYN.mad:598`, `include/LO_SYN.labels.md:197` | 323B | 1 |
| `EX50_4016` | EQU/LABEL(md) | `src/LO_SYN.mad:692`, `include/LO_SYN.labels.md:223` | 4016B | 1 |
| `EX50_70325` | EQU/LABEL(md) | `src/LO_SYN.mad:600`, `include/LO_SYN.labels.md:198` | 70325B | 1 |
| `EX50_70504` | EQU/LABEL(md) | `src/LO_SYN.mad:607`, `include/LO_SYN.labels.md:201` | 70504B | 1 |
| `EX50_73010` | EQU/LABEL(md) | `src/LO_SYN.mad:671`, `include/LO_SYN.labels.md:219` | 73010B | 1 |
| `EX50_73111` | EQU/LABEL(md) | `src/LO_SYN.mad:680`, `include/LO_SYN.labels.md:221` | 73111B | 1 |
| `EX56_70000` | EQU/LABEL(md) | `src/LO_SYN.mad:43`, `include/LO_SYN.labels.md:55` | 70000B | 1 |
| `EX57_1263` | EQU/LABEL(md) | `src/LO_SYN.mad:42`, `include/LO_SYN.labels.md:54` | 1263B | 1 |
| `EX60_4002` | EQU/LABEL(md) | `src/LO_SYN.mad:682`, `include/LO_SYN.labels.md:222` | 4002B | 1 |
| `EX60_4041` | EQU/LABEL(md) | `src/LO_SYN.mad:713`, `include/LO_SYN.labels.md:230` | 4041B | 1 |
| `EX60_4423` | EQU/LABEL(md) | `src/LO_SYN.mad:755`, `include/LO_SYN.labels.md:239` | 4423B | 1 |
| `EX60_512` | EQU/LABEL(md) | `src/LO_SYN.mad:612`, `include/LO_SYN.labels.md:202` | 512B | 1 |
| `EX60_514` | EQU/LABEL(md) | `src/LO_SYN.mad:614`, `include/LO_SYN.labels.md:203` | 514B | 1 |
| `EX60_70312` | EQU/LABEL(md) | `src/LO_SYN.mad:592`, `include/LO_SYN.labels.md:194` | 70312B | 1 |
| `EX60_70313` | EQU/LABEL(md) | `src/LO_SYN.mad:593`, `include/LO_SYN.labels.md:195` | 70313B | 1 |
| `EX60_71015` | EQU/LABEL(md) | `src/LO_SYN.mad:620`, `include/LO_SYN.labels.md:205` | 71015B | 1 |
| `EX60_71105` | EQU/LABEL(md) | `src/LO_SYN.mad:628`, `include/LO_SYN.labels.md:208` | 71105B | 1 |
| `EX60_71215` | EQU/LABEL(md) | `src/LO_SYN.mad:636`, `include/LO_SYN.labels.md:210` | 71215B | 1 |
| `EX60_71313` | EQU/LABEL(md) | `src/LO_SYN.mad:644`, `include/LO_SYN.labels.md:214` | 71313B | 1 |
| `EX60_74030` | EQU/LABEL(md) | `src/LO_SYN.mad:703`, `include/LO_SYN.labels.md:226` | 74030B | 1 |
| `EX60_74035` | EQU/LABEL(md) | `src/LO_SYN.mad:708`, `include/LO_SYN.labels.md:227` | 74035B | 1 |
| `EX60_74040` | EQU/LABEL(md) | `src/LO_SYN.mad:711`, `include/LO_SYN.labels.md:229` | 74040B | 1 |
| `EX62_110` | EQU/LABEL(md) | `src/LO_SYN.mad:292`, `include/LO_SYN.labels.md:107` | 110B | 1 |
| `EX62_115` | EQU/LABEL(md) | `src/LO_SYN.mad:460`, `include/LO_SYN.labels.md:162` | 115B | 1 |
| `EX62_160` | EQU/LABEL(md) | `src/LO_SYN.mad:501`, `include/LO_SYN.labels.md:170` | 160B | 1 |
| `EX62_40` | EQU/LABEL(md) | `src/LO_SYN.mad:331`, `include/LO_SYN.labels.md:120` | 40B | 1 |
| `EX62_6466` | EQU/LABEL(md) | `src/LO_SYN.mad:152`, `include/LO_SYN.labels.md:78` | 6466B | 1 |
| `EX62_6552` | EQU/LABEL(md) | `src/LO_SYN.mad:419`, `include/LO_SYN.labels.md:145` | 6552B | 1 |
| `EX62_70040` | EQU/LABEL(md) | `src/LO_SYN.mad:461`, `include/LO_SYN.labels.md:163` | 70040B | 1 |
| `EX63_274` | EQU/LABEL(md) | `src/LO_SYN.mad:52`, `include/LO_SYN.labels.md:56` | 274B | 1 |
| `EX64_1571` | EQU/LABEL(md) | `src/LO_SYN.mad:490`, `include/LO_SYN.labels.md:168` | 1571B | 1 |
| `EX64_5501` | EQU/LABEL(md) | `src/LO_SYN.mad:468`, `include/LO_SYN.labels.md:164` | 5501B | 1 |
| `EX64_7517` | EQU/LABEL(md) | `src/LO_SYN.mad:380`, `include/LO_SYN.labels.md:135` | 7517B | 1 |
| `EX64_7522` | EQU/LABEL(md) | `src/LO_SYN.mad:372`, `include/LO_SYN.labels.md:131` | 7522B | 1 |
| `EX65_2101` | EQU/LABEL(md) | `src/LO_SYN.mad:563`, `include/LO_SYN.labels.md:188` | 2101B | 1 |
| `EX65_2110` | EQU/LABEL(md) | `src/LO_SYN.mad:504`, `include/LO_SYN.labels.md:171` | 2110B | 1 |
| `EX65_2117` | EQU/LABEL(md) | `src/LO_SYN.mad:363`, `include/LO_SYN.labels.md:126` | 2117B | 1 |
| `EX66_4546` | EQU/LABEL(md) | `src/LO_SYN.mad:184`, `include/LO_SYN.labels.md:86` | 4546B | 1 |
| `EX66_74576` | EQU/LABEL(md) | `src/LO_SYN.mad:429`, `include/LO_SYN.labels.md:150` | 74576B | 1 |
| `EX66_76131` | EQU/LABEL(md) | `src/LO_SYN.mad:167`, `include/LO_SYN.labels.md:83` | 76131B | 1 |
| `EX70_14` | EQU/LABEL(md) | `src/LO_SYN.mad:62`, `include/LO_SYN.labels.md:57` | 14B | 1 |
| `EX70_3110` | EQU/LABEL(md) | `src/LO_SYN.mad:678`, `include/LO_SYN.labels.md:220` | 3110B | 1 |
| `EX70_4026` | EQU/LABEL(md) | `src/LO_SYN.mad:701`, `include/LO_SYN.labels.md:225` | 4026B | 1 |
| `EX70_4072` | EQU/LABEL(md) | `src/LO_SYN.mad:722`, `include/LO_SYN.labels.md:233` | 4072B | 1 |
| `EX70_4311` | EQU/LABEL(md) | `src/LO_SYN.mad:729`, `include/LO_SYN.labels.md:235` | 4311B | 1 |
| `EX70_71000` | EQU/LABEL(md) | `src/LO_SYN.mad:615`, `include/LO_SYN.labels.md:204` | 71000B | 1 |
| `EX70_71101` | EQU/LABEL(md) | `src/LO_SYN.mad:626`, `include/LO_SYN.labels.md:207` | 71101B | 1 |
| `EX70_71326` | EQU/LABEL(md) | `src/LO_SYN.mad:651`, `include/LO_SYN.labels.md:217` | 71326B | 1 |
| `EX70_71405` | EQU/LABEL(md) | `src/LO_SYN.mad:656`, `include/LO_SYN.labels.md:218` | 71405B | 1 |
| `EX70_74021` | EQU/LABEL(md) | `src/LO_SYN.mad:695`, `include/LO_SYN.labels.md:224` | 74021B | 1 |
| `EX70_74075` | EQU/LABEL(md) | `src/LO_SYN.mad:724`, `include/LO_SYN.labels.md:234` | 74075B | 1 |
| `EX70_74312` | EQU/LABEL(md) | `src/LO_SYN.mad:730`, `include/LO_SYN.labels.md:236` | 74312B | 1 |
| `EXT_2005` | EQU/LABEL(md) | `src/LO_SYN.mad:662`, `include/LO_SYN.labels.md:321` | 2005B | 1 |
| `EXT_20102` | EQU/LABEL(md) | `src/LO_SYN.mad:521`, `include/LO_SYN.labels.md:306` | 20102B | 1 |
| `EXT_20110` | EQU/LABEL(md) | `src/LO_SYN.mad:570`, `include/LO_SYN.labels.md:315` | 20110B | 1 |
| `EXT_20111` | EQU/LABEL(md) | `src/LO_SYN.mad:432`, `include/LO_SYN.labels.md:297` | 20111B | 1 |
| `EXT_20116` | EQU/LABEL(md) | `src/LO_SYN.mad:66`, `include/LO_SYN.labels.md:245` | 20116B | 1 |
| `EXT_20143` | EQU/LABEL(md) | `src/LO_SYN.mad:509`, `include/LO_SYN.labels.md:304` | 20143B | 1 |
| `EXT_20144` | EQU/LABEL(md) | `src/LO_SYN.mad:327`, `include/LO_SYN.labels.md:284` | 20144B | 1 |
| `EXT_20147` | EQU/LABEL(md) | `src/LO_SYN.mad:332`, `include/LO_SYN.labels.md:285` | 20147B | 1 |
| `EXT_20173` | EQU/LABEL(md) | `src/LO_SYN.mad:472`, `include/LO_SYN.labels.md:301` | 20173B | 1 |
| `EXT_3002` | EQU/LABEL(md) | `src/LO_SYN.mad:667`, `include/LO_SYN.labels.md:323` | 3002B | 1 |
| `EXT_3003` | EQU/LABEL(md) | `src/LO_SYN.mad:668`, `include/LO_SYN.labels.md:324` | 3003B | 1 |
| `EXT_3106` | EQU/LABEL(md) | `src/LO_SYN.mad:675`, `include/LO_SYN.labels.md:325` | 3106B | 1 |
| `EXT_4001` | EQU/LABEL(md) | `src/LO_SYN.mad:681`, `include/LO_SYN.labels.md:326` | 4001B | 1 |
| `EXT_4012` | EQU/LABEL(md) | `src/LO_SYN.mad:688`, `include/LO_SYN.labels.md:328` | 4012B | 1 |
| `EXT_4013` | EQU/LABEL(md) | `src/LO_SYN.mad:689`, `include/LO_SYN.labels.md:329` | 4013B | 1 |
| `EXT_4014` | EQU/LABEL(md) | `src/LO_SYN.mad:690`, `include/LO_SYN.labels.md:330` | 4014B | 1 |
| `EXT_4020` | EQU/LABEL(md) | `src/LO_SYN.mad:694`, `include/LO_SYN.labels.md:331` | 4020B | 1 |
| `EXT_4024` | EQU/LABEL(md) | `src/LO_SYN.mad:698`, `include/LO_SYN.labels.md:332` | 4024B | 1 |
| `EXT_4031` | EQU/LABEL(md) | `src/LO_SYN.mad:704`, `include/LO_SYN.labels.md:333` | 4031B | 1 |
| `EXT_4032` | EQU/LABEL(md) | `src/LO_SYN.mad:705`, `include/LO_SYN.labels.md:334` | 4032B | 1 |
| `EXT_4033` | EQU/LABEL(md) | `src/LO_SYN.mad:706`, `include/LO_SYN.labels.md:335` | 4033B | 1 |
| `EXT_4036` | EQU/LABEL(md) | `src/LO_SYN.mad:709`, `include/LO_SYN.labels.md:336` | 4036B | 1 |
| `EXT_40505` | EQU/LABEL(md) | `src/LO_SYN.mad:518`, `include/LO_SYN.labels.md:305` | 40505B | 1 |
| `EXT_4052` | EQU/LABEL(md) | `src/LO_SYN.mad:716`, `include/LO_SYN.labels.md:337` | 4052B | 1 |
| `EXT_40520` | EQU/LABEL(md) | `src/LO_SYN.mad:541`, `include/LO_SYN.labels.md:312` | 40520B | 1 |
| `EXT_4053` | EQU/LABEL(md) | `src/LO_SYN.mad:717`, `include/LO_SYN.labels.md:338` | 4053B | 1 |
| `EXT_40530` | EQU/LABEL(md) | `src/LO_SYN.mad:417`, `include/LO_SYN.labels.md:295` | 40530B | 1 |
| `EXT_40547` | EQU/LABEL(md) | `src/LO_SYN.mad:526`, `include/LO_SYN.labels.md:307` | 40547B | 1 |
| `EXT_42111` | EQU/LABEL(md) | `src/LO_SYN.mad:579`, `include/LO_SYN.labels.md:317` | 42111B | 1 |
| `EXT_42516` | EQU/LABEL(md) | `src/LO_SYN.mad:583`, `include/LO_SYN.labels.md:318` | 42516B | 1 |
| `EXT_42520` | EQU/LABEL(md) | `src/LO_SYN.mad:260`, `include/LO_SYN.labels.md:277` | 42520B | 1 |
| `EXT_42575` | EQU/LABEL(md) | `src/LO_SYN.mad:538`, `include/LO_SYN.labels.md:311` | 42575B | 1 |
| `EXT_4301` | EQU/LABEL(md) | `src/LO_SYN.mad:726`, `include/LO_SYN.labels.md:340` | 4301B | 1 |
| `EXT_4302` | EQU/LABEL(md) | `src/LO_SYN.mad:727`, `include/LO_SYN.labels.md:341` | 4302B | 1 |
| `EXT_4314` | EQU/LABEL(md) | `src/LO_SYN.mad:732`, `include/LO_SYN.labels.md:342` | 4314B | 1 |
| `EXT_4324` | EQU/LABEL(md) | `src/LO_SYN.mad:739`, `include/LO_SYN.labels.md:344` | 4324B | 1 |
| `EXT_4326` | EQU/LABEL(md) | `src/LO_SYN.mad:741`, `include/LO_SYN.labels.md:345` | 4326B | 1 |
| `EXT_4327` | EQU/LABEL(md) | `src/LO_SYN.mad:742`, `include/LO_SYN.labels.md:346` | 4327B | 1 |
| `EXT_4407` | EQU/LABEL(md) | `src/LO_SYN.mad:748`, `include/LO_SYN.labels.md:347` | 4407B | 1 |
| `EXT_4421` | EQU/LABEL(md) | `src/LO_SYN.mad:753`, `include/LO_SYN.labels.md:348` | 4421B | 1 |
| `EXT_45505` | EQU/LABEL(md) | `src/LO_SYN.mad:491`, `include/LO_SYN.labels.md:303` | 45505B | 1 |
| `EXT_45551` | EQU/LABEL(md) | `src/LO_SYN.mad:557`, `include/LO_SYN.labels.md:314` | 45551B | 1 |
| `EXT_46517` | EQU/LABEL(md) | `src/LO_SYN.mad:361`, `include/LO_SYN.labels.md:289` | 46517B | 1 |
| `EXT_47503` | EQU/LABEL(md) | `src/LO_SYN.mad:259`, `include/LO_SYN.labels.md:276` | 47503B | 1 |
| `EXT_50101` | EQU/LABEL(md) | `src/LO_SYN.mad:478`, `include/LO_SYN.labels.md:302` | 50101B | 1 |
| `EXT_50171` | EQU/LABEL(md) | `src/LO_SYN.mad:191`, `include/LO_SYN.labels.md:265` | 50171B | 1 |
| `EXT_61440` | EQU/LABEL(md) | `src/LO_SYN.mad:398`, `include/LO_SYN.labels.md:292` | 61440B | 1 |
| `EXT_61551` | EQU/LABEL(md) | `src/LO_SYN.mad:576`, `include/LO_SYN.labels.md:316` | 61551B | 1 |
| `EXT_62101` | EQU/LABEL(md) | `src/LO_SYN.mad:401`, `include/LO_SYN.labels.md:293` | 62101B | 1 |
| `EXT_63131` | EQU/LABEL(md) | `src/LO_SYN.mad:391`, `include/LO_SYN.labels.md:290` | 63131B | 1 |
| `EXT_64503` | EQU/LABEL(md) | `src/LO_SYN.mad:321`, `include/LO_SYN.labels.md:283` | 64503B | 1 |
| `EXT_64510` | EQU/LABEL(md) | `src/LO_SYN.mad:466`, `include/LO_SYN.labels.md:299` | 64510B | 1 |
| `EXT_64520` | EQU/LABEL(md) | `src/LO_SYN.mad:360`, `include/LO_SYN.labels.md:288` | 64520B | 1 |
| `EXT_64524` | EQU/LABEL(md) | `src/LO_SYN.mad:136`, `include/LO_SYN.labels.md:261` | 64524B | 1 |
| `EXT_64576` | EQU/LABEL(md) | `src/LO_SYN.mad:531`, `include/LO_SYN.labels.md:308` | 64576B | 1 |
| `EXT_66105` | EQU/LABEL(md) | `src/LO_SYN.mad:467`, `include/LO_SYN.labels.md:300` | 66105B | 1 |
| `EXT_66117` | EQU/LABEL(md) | `src/LO_SYN.mad:586`, `include/LO_SYN.labels.md:319` | 66117B | 1 |
| `EXT_70505` | EQU/LABEL(md) | `src/LO_SYN.mad:335`, `include/LO_SYN.labels.md:286` | 70505B | 1 |
| `EXT_70513` | EQU/LABEL(md) | `src/LO_SYN.mad:613`, `include/LO_SYN.labels.md:320` | 70513B | 1 |
| `EXT_72011` | EQU/LABEL(md) | `src/LO_SYN.mad:665`, `include/LO_SYN.labels.md:322` | 72011B | 1 |
| `EXT_73110` | EQU/LABEL(md) | `src/LO_SYN.mad:239`, `include/LO_SYN.labels.md:273` | 73110B | 1 |
| `EXT_74003` | EQU/LABEL(md) | `src/LO_SYN.mad:683`, `include/LO_SYN.labels.md:327` | 74003B | 1 |
| `EXT_74073` | EQU/LABEL(md) | `src/LO_SYN.mad:723`, `include/LO_SYN.labels.md:339` | 74073B | 1 |
| `EXT_74113` | EQU/LABEL(md) | `src/LO_SYN.mad:319`, `include/LO_SYN.labels.md:282` | 74113B | 1 |
| `EXT_74322` | EQU/LABEL(md) | `src/LO_SYN.mad:737`, `include/LO_SYN.labels.md:343` | 74322B | 1 |
| `EXT_74440` | EQU/LABEL(md) | `src/LO_SYN.mad:551`, `include/LO_SYN.labels.md:313` | 74440B | 1 |
| `FIXED_MODE_2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:44`, `include/FOREX_ROOT.mad:30`, `include/FOREX.labels.md:236`, `include/FOREX.labels.md:318` | 2 | 1 |
| `FLGEX_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:110`, `include/FOREX.labels.md:181` | 4002B | 1 |
| `FL_AFTER_WRITE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:215`, `include/FOREX.labels.md:48` | — | 1 |
| `FL_ALT_CASE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:262`, `include/FOREX.labels.md:52` | — | 1 |
| `FL_ASSEMBLE` | LABEL(md) | `include/FOREX.labels.md:56` | — | 1 |
| `FL_MASK_CASE` | LABEL(md) | `include/FOREX.labels.md:55` | — | 1 |
| `FL_SHIFT_IN` | LABEL(md) | `include/FOREX.labels.md:53` | — | 1 |
| `FL_SIGN_CHECK` | LABEL(md) | `include/FOREX.labels.md:49` | — | 1 |
| `FL_WTC_CASE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:254`, `include/FOREX.labels.md:51` | — | 1 |
| `FMT_RZB_MASK` | EQU/LABEL(md) | `src/FOREX_CORE.mad:111`, `include/FOREX.labels.md:182` | 4035B | 1 |
| `FMT_SBR_MASK` | EQU/LABEL(md) | `src/FOREX_CORE.mad:112`, `include/FOREX.labels.md:183` | 4034B | 1 |
| `FT*002` | SUBP | `src/FOREX_RUNTIME.mad:131` | — | 1 |
| `FT*003` | SUBP | `src/FOREX_RUNTIME.mad:132` | — | 1 |
| `FT*521` | SUBP | `src/FOREX_RUNTIME.mad:128` | — | 1 |
| `FT*531` | SUBP | `src/FOREX_RUNTIME.mad:125` | — | 1 |
| `FT*541` | SUBP | `src/FOREX_RUNTIME.mad:123` | — | 1 |
| `FT*561` | SUBP | `src/FOREX_RUNTIME.mad:126` | — | 1 |
| `FT*571` | SUBP | `src/FOREX_RUNTIME.mad:122` | — | 1 |
| `FT*611` | SUBP | `src/FOREX_RUNTIME.mad:124` | — | 1 |
| `FT*621` | SUBP | `src/FOREX_RUNTIME.mad:127` | — | 1 |
| `FT*641` | SUBP | `src/FOREX_RUNTIME.mad:130` | — | 1 |
| `FT*721` | SUBP | `src/FOREX_RUNTIME.mad:129` | — | 1 |
| `FT002_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:45`, `include/FOREX.labels.md:237` | 77776B | 1 |
| `FT003_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:46`, `include/FOREX.labels.md:238` | 77775B | 1 |
| `FT521_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:47`, `include/FOREX.labels.md:239` | 77257B | 1 |
| `FT531_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:48`, `include/FOREX.labels.md:240` | 77247B | 1 |
| `FT541_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:49`, `include/FOREX.labels.md:241` | 77237B | 1 |
| `FT561_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:50`, `include/FOREX.labels.md:242` | 77217B | 1 |
| `FT571_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:51`, `include/FOREX.labels.md:243` | 77207B | 1 |
| `FT611_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:52`, `include/FOREX.labels.md:244` | 77167B | 1 |
| `FT621_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:53`, `include/FOREX.labels.md:245` | 77157B | 1 |
| `FT641_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:54`, `include/FOREX.labels.md:246` | 77137B | 1 |
| `FT721_ADDR` | EQU/LABEL(md) | `src/LO_GEN.mad:45`, `include/LO_GEN.labels.md:1093` | 77057B | 1 |
| `FT721_DISPATCH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:55`, `include/FOREX.labels.md:247` | 77057B | 1 |
| `FTD_LOOP` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:145`, `include/FOREX.labels.md:40` | — | 1 |
| `FTD_OFFSET` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:152`, `include/FOREX.labels.md:41` | — | 1 |
| `FTD_STORE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:157`, `include/FOREX.labels.md:42` | — | 1 |
| `FTD_TABLE_BASE` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:143`, `include/FOREX.labels.md:39` | — | 1 |
| `FTD_TABLE_BASE_ADDR` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:56`, `include/FOREX.labels.md:248` | 77766B | 1 |
| `FT_ADDR_FIELD` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:57`, `include/FOREX.labels.md:249` | 103B | 1 |
| `FT_LIB_BUFFER` | LABEL/LABEL(md) | `src/FOREX_RUNTIME.mad:194`, `include/FOREX.labels.md:46` | — | 1 |
| `FT_OFFSET_MASK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:58`, `include/FOREX.labels.md:250` | 155B | 1 |
| `FULIS_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:113`, `include/FOREX.labels.md:184` | 4004B | 1 |
| `FUN_DATE_TIME` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:107`, `include/FOREX.labels.md:299` | 67B | 1 |
| `GIV/PG` | SUBP | `src/LO_SYN.mad:27` | — | 1 |
| `GOST_BLANK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:59`, `include/FOREX.labels.md:251` | 6H | 1 |
| `GOST_V` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:31`, `include/FOREX.labels.md:319` | 1H'212' | 1 |
| `GOST_VREMYA` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:32`, `include/FOREX.labels.md:320` | 6HBPEMЯ- | 1 |
| `GOST_YA` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:33`, `include/FOREX.labels.md:321` | 1H'231' | 1 |
| `HEADER_MODULE_MARKER` | EQU/LABEL(md) | `src/LO_GEN.mad:275`, `include/LO_GEN.labels.md:1291` | 0000000000200003 | 1 |
| `HEADER_MODULE_NAME_WORD` | EQU/LABEL(md) | `src/LO_GEN.mad:276`, `include/LO_GEN.labels.md:1292` | 5457124745560000 | 1 |
| `INF_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:115`, `include/FOREX.labels.md:186` | 4036B | 1 |
| `INIT_CONST_33` | EQU/LABEL(md) | `src/FOREX_CORE.mad:116`, `include/FOREX.labels.md:187` | 33B | 1 |
| `INIT_MODE_1500` | EQU/LABEL(md) | `src/FOREX_CORE.mad:117`, `include/FOREX.labels.md:188` | 1500B | 1 |
| `INIT_MODE_1700` | EQU/LABEL(md) | `src/FOREX_CORE.mad:118`, `include/FOREX.labels.md:189` | 1700B | 1 |
| `INT_ZERO` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:60`, `include/FOREX.labels.md:252` | 0 | 1 |
| `ISO_CODE_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:61`, `include/FOREX.labels.md:253` | 54B | 1 |
| `JUMP_TARGET_20116` | EQU/LABEL(md) | `src/LO_GEN.mad:278`, `include/LO_GEN.labels.md:1328` | 20116B | 1 |
| `JUMP_TARGET_20521` | EQU/LABEL(md) | `src/LO_GEN.mad:279`, `include/LO_GEN.labels.md:1329` | 20521B | 1 |
| `JUMP_TARGET_26434` | EQU/LABEL(md) | `src/LO_GEN.mad:280`, `include/LO_GEN.labels.md:1330` | 26434B | 1 |
| `JUMP_TARGET_30310` | EQU/LABEL(md) | `src/LO_GEN.mad:281`, `include/LO_GEN.labels.md:1331` | 30310B | 1 |
| `JUMP_TARGET_41072` | EQU/LABEL(md) | `src/LO_GEN.mad:282`, `include/LO_GEN.labels.md:1332` | 41072B | 1 |
| `JUMP_TARGET_41104` | EQU/LABEL(md) | `src/LO_GEN.mad:283`, `include/LO_GEN.labels.md:1333` | 41104B | 1 |
| `JUMP_TARGET_41260` | EQU/LABEL(md) | `src/LO_GEN.mad:284`, `include/LO_GEN.labels.md:1334` | 41260B | 1 |
| `JUMP_TARGET_41271` | EQU/LABEL(md) | `src/LO_GEN.mad:285`, `include/LO_GEN.labels.md:1335` | 41271B | 1 |
| `JUMP_TARGET_41563` | EQU/LABEL(md) | `src/LO_GEN.mad:286`, `include/LO_GEN.labels.md:1336` | 41563B | 1 |
| `JUMP_TARGET_41660` | EQU/LABEL(md) | `src/LO_GEN.mad:291`, `include/LO_GEN.labels.md:1341` | 41660B | 1 |
| `JUMP_TARGET_41706` | EQU/LABEL(md) | `src/LO_GEN.mad:292`, `include/LO_GEN.labels.md:1342` | 41706B | 1 |
| `JUMP_TARGET_42054` | EQU/LABEL(md) | `src/LO_GEN.mad:294`, `include/LO_GEN.labels.md:1344` | 42054B | 1 |
| `JUMP_TARGET_42130` | EQU/LABEL(md) | `src/LO_GEN.mad:296`, `include/LO_GEN.labels.md:1346` | 42130B | 1 |
| `JUMP_TARGET_42133` | EQU/LABEL(md) | `src/LO_GEN.mad:297`, `include/LO_GEN.labels.md:1347` | 42133B | 1 |
| `JUMP_TARGET_42154` | EQU/LABEL(md) | `src/LO_GEN.mad:298`, `include/LO_GEN.labels.md:1348` | 42154B | 1 |
| `JUMP_TARGET_42170` | EQU/LABEL(md) | `src/LO_GEN.mad:299`, `include/LO_GEN.labels.md:1349` | 42170B | 1 |
| `JUMP_TARGET_42332` | EQU/LABEL(md) | `src/LO_GEN.mad:304`, `include/LO_GEN.labels.md:1354` | 42332B | 1 |
| `JUMP_TARGET_42663` | EQU/LABEL(md) | `src/LO_GEN.mad:309`, `include/LO_GEN.labels.md:1359` | 42663B | 1 |
| `JUMP_TARGET_42756` | EQU/LABEL(md) | `src/LO_GEN.mad:310`, `include/LO_GEN.labels.md:1360` | 42756B | 1 |
| `JUMP_TARGET_43301` | EQU/LABEL(md) | `src/LO_GEN.mad:311`, `include/LO_GEN.labels.md:1361` | 43301B | 1 |
| `JUMP_TARGET_43402` | EQU/LABEL(md) | `src/LO_GEN.mad:312`, `include/LO_GEN.labels.md:1362` | 43402B | 1 |
| `JUMP_TARGET_43460` | EQU/LABEL(md) | `src/LO_GEN.mad:313`, `include/LO_GEN.labels.md:1363` | 43460B | 1 |
| `JUMP_TARGET_44405` | EQU/LABEL(md) | `src/LO_GEN.mad:315`, `include/LO_GEN.labels.md:1365` | 44405B | 1 |
| `JUMP_TARGET_47253` | EQU/LABEL(md) | `src/LO_GEN.mad:318`, `include/LO_GEN.labels.md:1368` | 47253B | 1 |
| `JUMP_TARGET_50114` | EQU/LABEL(md) | `src/LO_GEN.mad:319`, `include/LO_GEN.labels.md:1369` | 50114B | 1 |
| `JUMP_TARGET_53333` | EQU/LABEL(md) | `src/LO_GEN.mad:321`, `include/LO_GEN.labels.md:1371` | 53333B | 1 |
| `JUMP_TARGET_54067` | EQU/LABEL(md) | `src/LO_GEN.mad:322`, `include/LO_GEN.labels.md:1372` | 54067B | 1 |
| `JUMP_TARGET_54303` | EQU/LABEL(md) | `src/LO_GEN.mad:323`, `include/LO_GEN.labels.md:1373` | 54303B | 1 |
| `JUMP_TARGET_57244` | EQU/LABEL(md) | `src/LO_GEN.mad:324`, `include/LO_GEN.labels.md:1374` | 57244B | 1 |
| `JUMP_TARGET_57616` | EQU/LABEL(md) | `src/LO_GEN.mad:327`, `include/LO_GEN.labels.md:1377` | 57616B | 1 |
| `JUMP_TARGET_60001` | EQU/LABEL(md) | `src/LO_GEN.mad:328`, `include/LO_GEN.labels.md:1378` | 60001B | 1 |
| `JUMP_TARGET_60562` | EQU/LABEL(md) | `src/LO_GEN.mad:330`, `include/LO_GEN.labels.md:1380` | 60562B | 1 |
| `JUMP_TARGET_61277` | EQU/LABEL(md) | `src/LO_GEN.mad:331`, `include/LO_GEN.labels.md:1381` | 61277B | 1 |
| `JUMP_TARGET_62570` | EQU/LABEL(md) | `src/LO_GEN.mad:335`, `include/LO_GEN.labels.md:1385` | 62570B | 1 |
| `JUMP_TARGET_63100` | EQU/LABEL(md) | `src/LO_GEN.mad:337`, `include/LO_GEN.labels.md:1387` | 63100B | 1 |
| `JUMP_TARGET_63235` | EQU/LABEL(md) | `src/LO_GEN.mad:338`, `include/LO_GEN.labels.md:1388` | 63235B | 1 |
| `JUMP_TARGET_63553` | EQU/LABEL(md) | `src/LO_GEN.mad:341`, `include/LO_GEN.labels.md:1391` | 63553B | 1 |
| `JUMP_TARGET_63636` | EQU/LABEL(md) | `src/LO_GEN.mad:343`, `include/LO_GEN.labels.md:1393` | 63636B | 1 |
| `JUMP_TARGET_64305` | EQU/LABEL(md) | `src/LO_GEN.mad:344`, `include/LO_GEN.labels.md:1394` | 64305B | 1 |
| `JUMP_TARGET_65152` | EQU/LABEL(md) | `src/LO_GEN.mad:345`, `include/LO_GEN.labels.md:1395` | 65152B | 1 |
| `JUMP_TARGET_66172` | EQU/LABEL(md) | `src/LO_GEN.mad:346`, `include/LO_GEN.labels.md:1396` | 66172B | 1 |
| `JUMP_TARGET_75330` | EQU/LABEL(md) | `src/LO_GEN.mad:350`, `include/LO_GEN.labels.md:1400` | 75330B | 1 |
| `JUMP_TARGET_75335` | EQU/LABEL(md) | `src/LO_GEN.mad:351`, `include/LO_GEN.labels.md:1401` | 75335B | 1 |
| `JUMP_TARGET_75342` | EQU/LABEL(md) | `src/LO_GEN.mad:352`, `include/LO_GEN.labels.md:1402` | 75342B | 1 |
| `JUMP_TARGET_75351` | EQU/LABEL(md) | `src/LO_GEN.mad:353`, `include/LO_GEN.labels.md:1403` | 75351B | 1 |
| `JUMP_TARGET_75360` | EQU/LABEL(md) | `src/LO_GEN.mad:354`, `include/LO_GEN.labels.md:1404` | 75360B | 1 |
| `JUMP_TARGET_75413` | EQU/LABEL(md) | `src/LO_GEN.mad:355`, `include/LO_GEN.labels.md:1405` | 75413B | 1 |
| `JUMP_TARGET_75415` | EQU/LABEL(md) | `src/LO_GEN.mad:356`, `include/LO_GEN.labels.md:1406` | 75415B | 1 |
| `JUMP_TARGET_75420` | EQU/LABEL(md) | `src/LO_GEN.mad:357`, `include/LO_GEN.labels.md:1407` | 75420B | 1 |
| `JUMP_TARGET_75423` | EQU/LABEL(md) | `src/LO_GEN.mad:358`, `include/LO_GEN.labels.md:1408` | 75423B | 1 |
| `JUMP_TARGET_75451` | EQU/LABEL(md) | `src/LO_GEN.mad:361`, `include/LO_GEN.labels.md:1411` | 75451B | 1 |
| `JUMP_TARGET_75456` | EQU/LABEL(md) | `src/LO_GEN.mad:362`, `include/LO_GEN.labels.md:1412` | 75456B | 1 |
| `JUMP_TARGET_75462` | EQU/LABEL(md) | `src/LO_GEN.mad:363`, `include/LO_GEN.labels.md:1413` | 75462B | 1 |
| `JUMP_TARGET_75471` | EQU/LABEL(md) | `src/LO_GEN.mad:364`, `include/LO_GEN.labels.md:1414` | 75471B | 1 |
| `JUMP_TARGET_75476` | EQU/LABEL(md) | `src/LO_GEN.mad:365`, `include/LO_GEN.labels.md:1415` | 75476B | 1 |
| `JUMP_TARGET_75500` | EQU/LABEL(md) | `src/LO_GEN.mad:366`, `include/LO_GEN.labels.md:1416` | 75500B | 1 |
| `JUMP_TARGET_75506` | EQU/LABEL(md) | `src/LO_GEN.mad:367`, `include/LO_GEN.labels.md:1417` | 75506B | 1 |
| `JUMP_TARGET_75507` | EQU/LABEL(md) | `src/LO_GEN.mad:368`, `include/LO_GEN.labels.md:1418` | 75507B | 1 |
| `JUMP_TARGET_75516` | EQU/LABEL(md) | `src/LO_GEN.mad:369`, `include/LO_GEN.labels.md:1419` | 75516B | 1 |
| `JUMP_TARGET_75526` | EQU/LABEL(md) | `src/LO_GEN.mad:371`, `include/LO_GEN.labels.md:1421` | 75526B | 1 |
| `JUMP_TARGET_75546` | EQU/LABEL(md) | `src/LO_GEN.mad:374`, `include/LO_GEN.labels.md:1424` | 75546B | 1 |
| `JUMP_TARGET_75547` | EQU/LABEL(md) | `src/LO_GEN.mad:375`, `include/LO_GEN.labels.md:1425` | 75547B | 1 |
| `JUMP_TARGET_75551` | EQU/LABEL(md) | `src/LO_GEN.mad:376`, `include/LO_GEN.labels.md:1426` | 75551B | 1 |
| `JUMP_TARGET_75555` | EQU/LABEL(md) | `src/LO_GEN.mad:377`, `include/LO_GEN.labels.md:1427` | 75555B | 1 |
| `JUMP_TARGET_75557` | EQU/LABEL(md) | `src/LO_GEN.mad:378`, `include/LO_GEN.labels.md:1428` | 75557B | 1 |
| `JUMP_TARGET_75565` | EQU/LABEL(md) | `src/LO_GEN.mad:380`, `include/LO_GEN.labels.md:1430` | 75565B | 1 |
| `JUMP_TARGET_75567` | EQU/LABEL(md) | `src/LO_GEN.mad:381`, `include/LO_GEN.labels.md:1431` | 75567B | 1 |
| `JUMP_TARGET_75570` | EQU/LABEL(md) | `src/LO_GEN.mad:382`, `include/LO_GEN.labels.md:1432` | 75570B | 1 |
| `JUMP_TARGET_75573` | EQU/LABEL(md) | `src/LO_GEN.mad:383`, `include/LO_GEN.labels.md:1433` | 75573B | 1 |
| `JUMP_TARGET_75575` | EQU/LABEL(md) | `src/LO_GEN.mad:384`, `include/LO_GEN.labels.md:1434` | 75575B | 1 |
| `JUMP_TARGET_75601` | EQU/LABEL(md) | `src/LO_GEN.mad:385`, `include/LO_GEN.labels.md:1435` | 75601B | 1 |
| `JUMP_TARGET_75605` | EQU/LABEL(md) | `src/LO_GEN.mad:386`, `include/LO_GEN.labels.md:1436` | 75605B | 1 |
| `JUMP_TARGET_75606` | EQU/LABEL(md) | `src/LO_GEN.mad:387`, `include/LO_GEN.labels.md:1437` | 75606B | 1 |
| `JUMP_TARGET_76056` | EQU/LABEL(md) | `src/LO_GEN.mad:388`, `include/LO_GEN.labels.md:1438` | 76056B | 1 |
| `JUMP_TARGET_76075` | EQU/LABEL(md) | `src/LO_GEN.mad:389`, `include/LO_GEN.labels.md:1439` | 76075B | 1 |
| `JUMP_TARGET_76102` | EQU/LABEL(md) | `src/LO_GEN.mad:390`, `include/LO_GEN.labels.md:1440` | 76102B | 1 |
| `JUMP_TARGET_76110` | EQU/LABEL(md) | `src/LO_GEN.mad:391`, `include/LO_GEN.labels.md:1441` | 76110B | 1 |
| `JUMP_TARGET_76112` | EQU/LABEL(md) | `src/LO_GEN.mad:392`, `include/LO_GEN.labels.md:1442` | 76112B | 1 |
| `JUMP_TARGET_76121` | EQU/LABEL(md) | `src/LO_GEN.mad:393`, `include/LO_GEN.labels.md:1443` | 76121B | 1 |
| `JUMP_TARGET_76123` | EQU/LABEL(md) | `src/LO_GEN.mad:394`, `include/LO_GEN.labels.md:1444` | 76123B | 1 |
| `JUMP_TARGET_76136` | EQU/LABEL(md) | `src/LO_GEN.mad:396`, `include/LO_GEN.labels.md:1446` | 76136B | 1 |
| `JUMP_TARGET_76140` | EQU/LABEL(md) | `src/LO_GEN.mad:397`, `include/LO_GEN.labels.md:1447` | 76140B | 1 |
| `JUMP_TARGET_76144` | EQU/LABEL(md) | `src/LO_GEN.mad:398`, `include/LO_GEN.labels.md:1448` | 76144B | 1 |
| `JUMP_TARGET_76146` | EQU/LABEL(md) | `src/LO_GEN.mad:399`, `include/LO_GEN.labels.md:1449` | 76146B | 1 |
| `JUMP_TARGET_76152` | EQU/LABEL(md) | `src/LO_GEN.mad:400`, `include/LO_GEN.labels.md:1450` | 76152B | 1 |
| `JUMP_TARGET_76154` | EQU/LABEL(md) | `src/LO_GEN.mad:401`, `include/LO_GEN.labels.md:1451` | 76154B | 1 |
| `JUMP_TARGET_76160` | EQU/LABEL(md) | `src/LO_GEN.mad:402`, `include/LO_GEN.labels.md:1452` | 76160B | 1 |
| `JUMP_TARGET_76164` | EQU/LABEL(md) | `src/LO_GEN.mad:403`, `include/LO_GEN.labels.md:1453` | 76164B | 1 |
| `JUMP_TARGET_76166` | EQU/LABEL(md) | `src/LO_GEN.mad:404`, `include/LO_GEN.labels.md:1454` | 76166B | 1 |
| `JUMP_TARGET_76204` | EQU/LABEL(md) | `src/LO_GEN.mad:405`, `include/LO_GEN.labels.md:1455` | 76204B | 1 |
| `JUMP_TARGET_76231` | EQU/LABEL(md) | `src/LO_GEN.mad:406`, `include/LO_GEN.labels.md:1456` | 76231B | 1 |
| `JUMP_TARGET_76304` | EQU/LABEL(md) | `src/LO_GEN.mad:407`, `include/LO_GEN.labels.md:1457` | 76304B | 1 |
| `JUMP_TARGET_76314` | EQU/LABEL(md) | `src/LO_GEN.mad:408`, `include/LO_GEN.labels.md:1458` | 76314B | 1 |
| `JUMP_TARGET_76324` | EQU/LABEL(md) | `src/LO_GEN.mad:409`, `include/LO_GEN.labels.md:1459` | 76324B | 1 |
| `JUMP_TARGET_76335` | EQU/LABEL(md) | `src/LO_GEN.mad:412`, `include/LO_GEN.labels.md:1462` | 76335B | 1 |
| `JUMP_TARGET_76361` | EQU/LABEL(md) | `src/LO_GEN.mad:415`, `include/LO_GEN.labels.md:1465` | 76361B | 1 |
| `JUMP_TARGET_76363` | EQU/LABEL(md) | `src/LO_GEN.mad:416`, `include/LO_GEN.labels.md:1466` | 76363B | 1 |
| `JUMP_TARGET_76364` | EQU/LABEL(md) | `src/LO_GEN.mad:417`, `include/LO_GEN.labels.md:1467` | 76364B | 1 |
| `JUMP_TARGET_76365` | EQU/LABEL(md) | `src/LO_GEN.mad:418`, `include/LO_GEN.labels.md:1468` | 76365B | 1 |
| `JUMP_TARGET_76374` | EQU/LABEL(md) | `src/LO_GEN.mad:419`, `include/LO_GEN.labels.md:1469` | 76374B | 1 |
| `JUMP_TARGET_76375` | EQU/LABEL(md) | `src/LO_GEN.mad:420`, `include/LO_GEN.labels.md:1470` | 76375B | 1 |
| `JUMP_TARGET_76376` | EQU/LABEL(md) | `src/LO_GEN.mad:421`, `include/LO_GEN.labels.md:1471` | 76376B | 1 |
| `JUMP_TARGET_76402` | EQU/LABEL(md) | `src/LO_GEN.mad:422`, `include/LO_GEN.labels.md:1472` | 76402B | 1 |
| `JUMP_TARGET_76404` | EQU/LABEL(md) | `src/LO_GEN.mad:423`, `include/LO_GEN.labels.md:1473` | 76404B | 1 |
| `JUMP_TARGET_76406` | EQU/LABEL(md) | `src/LO_GEN.mad:424`, `include/LO_GEN.labels.md:1474` | 76406B | 1 |
| `JUMP_TARGET_76411` | EQU/LABEL(md) | `src/LO_GEN.mad:425`, `include/LO_GEN.labels.md:1475` | 76411B | 1 |
| `JUMP_TARGET_76413` | EQU/LABEL(md) | `src/LO_GEN.mad:426`, `include/LO_GEN.labels.md:1476` | 76413B | 1 |
| `JUMP_TARGET_76416` | EQU/LABEL(md) | `src/LO_GEN.mad:427`, `include/LO_GEN.labels.md:1477` | 76416B | 1 |
| `JUMP_TARGET_76417` | EQU/LABEL(md) | `src/LO_GEN.mad:428`, `include/LO_GEN.labels.md:1478` | 76417B | 1 |
| `JUMP_TARGET_76422` | EQU/LABEL(md) | `src/LO_GEN.mad:429`, `include/LO_GEN.labels.md:1479` | 76422B | 1 |
| `JUMP_TARGET_76424` | EQU/LABEL(md) | `src/LO_GEN.mad:430`, `include/LO_GEN.labels.md:1480` | 76424B | 1 |
| `JUMP_TARGET_76425` | EQU/LABEL(md) | `src/LO_GEN.mad:431`, `include/LO_GEN.labels.md:1481` | 76425B | 1 |
| `JUMP_TARGET_76427` | EQU/LABEL(md) | `src/LO_GEN.mad:432`, `include/LO_GEN.labels.md:1482` | 76427B | 1 |
| `JUMP_TARGET_76431` | EQU/LABEL(md) | `src/LO_GEN.mad:433`, `include/LO_GEN.labels.md:1483` | 76431B | 1 |
| `JUMP_TARGET_76445` | EQU/LABEL(md) | `src/LO_GEN.mad:434`, `include/LO_GEN.labels.md:1484` | 76445B | 1 |
| `JUMP_TARGET_76447` | EQU/LABEL(md) | `src/LO_GEN.mad:435`, `include/LO_GEN.labels.md:1485` | 76447B | 1 |
| `JUMP_TARGET_76451` | EQU/LABEL(md) | `src/LO_GEN.mad:436`, `include/LO_GEN.labels.md:1486` | 76451B | 1 |
| `JUMP_TARGET_76465` | EQU/LABEL(md) | `src/LO_GEN.mad:438`, `include/LO_GEN.labels.md:1488` | 76465B | 1 |
| `JUMP_TARGET_76470` | EQU/LABEL(md) | `src/LO_GEN.mad:439`, `include/LO_GEN.labels.md:1489` | 76470B | 1 |
| `JUMP_TARGET_76475` | EQU/LABEL(md) | `src/LO_GEN.mad:440`, `include/LO_GEN.labels.md:1490` | 76475B | 1 |
| `JUMP_TARGET_76500` | EQU/LABEL(md) | `src/LO_GEN.mad:441`, `include/LO_GEN.labels.md:1491` | 76500B | 1 |
| `JUMP_TARGET_76504` | EQU/LABEL(md) | `src/LO_GEN.mad:443`, `include/LO_GEN.labels.md:1493` | 76504B | 1 |
| `JUMP_TARGET_76511` | EQU/LABEL(md) | `src/LO_GEN.mad:444`, `include/LO_GEN.labels.md:1494` | 76511B | 1 |
| `JUMP_TARGET_76514` | EQU/LABEL(md) | `src/LO_GEN.mad:445`, `include/LO_GEN.labels.md:1495` | 76514B | 1 |
| `JUMP_TARGET_76534` | EQU/LABEL(md) | `src/LO_GEN.mad:447`, `include/LO_GEN.labels.md:1497` | 76534B | 1 |
| `JUMP_TARGET_76557` | EQU/LABEL(md) | `src/LO_GEN.mad:449`, `include/LO_GEN.labels.md:1499` | 76557B | 1 |
| `JUMP_TARGET_76561` | EQU/LABEL(md) | `src/LO_GEN.mad:450`, `include/LO_GEN.labels.md:1500` | 76561B | 1 |
| `JUMP_TARGET_76573` | EQU/LABEL(md) | `src/LO_GEN.mad:455`, `include/LO_GEN.labels.md:1505` | 76573B | 1 |
| `JUMP_TARGET_76575` | EQU/LABEL(md) | `src/LO_GEN.mad:456`, `include/LO_GEN.labels.md:1506` | 76575B | 1 |
| `JUMP_TARGET_76577` | EQU/LABEL(md) | `src/LO_GEN.mad:457`, `include/LO_GEN.labels.md:1507` | 76577B | 1 |
| `JUMP_TARGET_76612` | EQU/LABEL(md) | `src/LO_GEN.mad:458`, `include/LO_GEN.labels.md:1508` | 76612B | 1 |
| `JUMP_TARGET_76651` | EQU/LABEL(md) | `src/LO_GEN.mad:459`, `include/LO_GEN.labels.md:1509` | 76651B | 1 |
| `JUMP_TARGET_76660` | EQU/LABEL(md) | `src/LO_GEN.mad:460`, `include/LO_GEN.labels.md:1510` | 76660B | 1 |
| `JUMP_TARGET_76663` | EQU/LABEL(md) | `src/LO_GEN.mad:461`, `include/LO_GEN.labels.md:1511` | 76663B | 1 |
| `JUMP_TARGET_76760` | EQU/LABEL(md) | `src/LO_GEN.mad:464`, `include/LO_GEN.labels.md:1514` | 76760B | 1 |
| `JUMP_TARGET_76761` | EQU/LABEL(md) | `src/LO_GEN.mad:465`, `include/LO_GEN.labels.md:1515` | 76761B | 1 |
| `JUMP_TARGET_77024` | EQU/LABEL(md) | `src/LO_GEN.mad:466`, `include/LO_GEN.labels.md:1516` | 77024B | 1 |
| `JUMP_TARGET_77043` | EQU/LABEL(md) | `src/LO_GEN.mad:467`, `include/LO_GEN.labels.md:1517` | 77043B | 1 |
| `JUMP_TARGET_77052` | EQU/LABEL(md) | `src/LO_GEN.mad:468`, `include/LO_GEN.labels.md:1518` | 77052B | 1 |
| `JUMP_TARGET_77071` | EQU/LABEL(md) | `src/LO_GEN.mad:470`, `include/LO_GEN.labels.md:1520` | 77071B | 1 |
| `JUMP_TARGET_77074` | EQU/LABEL(md) | `src/LO_GEN.mad:471`, `include/LO_GEN.labels.md:1521` | 77074B | 1 |
| `JUMP_TARGET_77076` | EQU/LABEL(md) | `src/LO_GEN.mad:472`, `include/LO_GEN.labels.md:1522` | 77076B | 1 |
| `JUMP_TARGET_77103` | EQU/LABEL(md) | `src/LO_GEN.mad:475`, `include/LO_GEN.labels.md:1525` | 77103B | 1 |
| `JUMP_TARGET_77104` | EQU/LABEL(md) | `src/LO_GEN.mad:476`, `include/LO_GEN.labels.md:1526` | 77104B | 1 |
| `JUMP_TARGET_77111` | EQU/LABEL(md) | `src/LO_GEN.mad:477`, `include/LO_GEN.labels.md:1527` | 77111B | 1 |
| `JUMP_TARGET_77113` | EQU/LABEL(md) | `src/LO_GEN.mad:478`, `include/LO_GEN.labels.md:1528` | 77113B | 1 |
| `JUMP_TARGET_77115` | EQU/LABEL(md) | `src/LO_GEN.mad:480`, `include/LO_GEN.labels.md:1530` | 77115B | 1 |
| `JUMP_TARGET_77120` | EQU/LABEL(md) | `src/LO_GEN.mad:481`, `include/LO_GEN.labels.md:1531` | 77120B | 1 |
| `JUMP_TARGET_77121` | EQU/LABEL(md) | `src/LO_GEN.mad:482`, `include/LO_GEN.labels.md:1532` | 77121B | 1 |
| `JUMP_TARGET_77122` | EQU/LABEL(md) | `src/LO_GEN.mad:483`, `include/LO_GEN.labels.md:1533` | 77122B | 1 |
| `JUMP_TARGET_77125` | EQU/LABEL(md) | `src/LO_GEN.mad:485`, `include/LO_GEN.labels.md:1535` | 77125B | 1 |
| `JUMP_TARGET_77126` | EQU/LABEL(md) | `src/LO_GEN.mad:486`, `include/LO_GEN.labels.md:1536` | 77126B | 1 |
| `JUMP_TARGET_77127` | EQU/LABEL(md) | `src/LO_GEN.mad:487`, `include/LO_GEN.labels.md:1537` | 77127B | 1 |
| `JUMP_TARGET_77224` | EQU/LABEL(md) | `src/LO_GEN.mad:490`, `include/LO_GEN.labels.md:1540` | 77224B | 1 |
| `JUMP_TARGET_77227` | EQU/LABEL(md) | `src/LO_GEN.mad:491`, `include/LO_GEN.labels.md:1541` | 77227B | 1 |
| `JUMP_TARGET_77242` | EQU/LABEL(md) | `src/LO_GEN.mad:492`, `include/LO_GEN.labels.md:1542` | 77242B | 1 |
| `LIB_BUFFER_LEN` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:63`, `include/FOREX.labels.md:255` | 2000B | 1 |
| `LIT_10` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:64`, `include/FOREX.labels.md:256` | 10 | 1 |
| `LIT_10000000_00000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:65`, `include/FOREX.labels.md:257` | 10000000 00000000 | 1 |
| `LIT_2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:66`, `include/FOREX.labels.md:258` | 2 | 1 |
| `LIT_3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:67`, `include/FOREX.labels.md:259` | 3 | 1 |
| `LO*GEN` | LABEL(md)/NAME | `src/LO_GEN.mad:18`, `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358`, `include/LO_GEN.labels.md:29` | NEW DTRAN | 1 |
| `LO*SYN` | LABEL(md)/NAME | `src/LO_SYN.mad:16`, `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358` | NEW DTRAN | 1 |
| `LO_GEN_TEXT_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:120`, `include/FOREX.labels.md:191` | 4032B | 1 |
| `LO_SYN_TEXT_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:121`, `include/FOREX.labels.md:192` | 4031B | 1 |
| `L_PROLOG_GO_MAIN` | LABEL/LABEL(md) | `src/LO_SYN.mad:814`, `include/LO_SYN.labels.md:10` | — | 1 |
| `L_ST1000_BRANCH_1005` | LABEL/LABEL(md) | `src/LO_SYN.mad:2317`, `include/LO_SYN.labels.md:18` | — | 1 |
| `L_ST300_CALL_1003` | LABEL/LABEL(md) | `src/LO_SYN.mad:2311`, `include/LO_SYN.labels.md:17` | — | 1 |
| `L_ST300_CALL_1331` | LABEL/LABEL(md) | `src/LO_SYN.mad:2953`, `include/LO_SYN.labels.md:30` | — | 1 |
| `L_ST300_TEST_0315` | LABEL/LABEL(md) | `src/LO_SYN.mad:1381`, `include/LO_SYN.labels.md:11` | — | 1 |
| `L_ST300_TEST_1001` | LABEL/LABEL(md) | `src/LO_SYN.mad:2305`, `include/LO_SYN.labels.md:16` | — | 1 |
| `L_ST300_TEST_1030` | LABEL/LABEL(md) | `src/LO_SYN.mad:2374`, `include/LO_SYN.labels.md:19` | — | 1 |
| `L_ST300_TEST_1317` | LABEL/LABEL(md) | `src/LO_SYN.mad:2923`, `include/LO_SYN.labels.md:26` | — | 1 |
| `L_ST300_TEST_1330` | LABEL/LABEL(md) | `src/LO_SYN.mad:2950`, `include/LO_SYN.labels.md:29` | — | 1 |
| `L_ST400_CALL_1031` | LABEL/LABEL(md) | `src/LO_SYN.mad:2377`, `include/LO_SYN.labels.md:20` | — | 1 |
| `L_ST400_HALT_1427` | LABEL/LABEL(md) | `src/LO_SYN.mad:3139`, `include/LO_SYN.labels.md:33` | — | 1 |
| `L_ST400_JMP_1112` | LABEL/LABEL(md) | `src/LO_SYN.mad:2524`, `include/LO_SYN.labels.md:22` | — | 1 |
| `L_ST400_TEST1_1410` | LABEL/LABEL(md) | `src/LO_SYN.mad:3094`, `include/LO_SYN.labels.md:32` | — | 1 |
| `L_ST500_BRANCH_1113` | LABEL/LABEL(md) | `src/LO_SYN.mad:2527`, `include/LO_SYN.labels.md:23` | — | 1 |
| `L_ST500_BRANCH_1201` | LABEL/LABEL(md) | `src/LO_SYN.mad:2689`, `include/LO_SYN.labels.md:24` | — | 1 |
| `L_ST500_BRANCH_1400` | LABEL/LABEL(md) | `src/LO_SYN.mad:3070`, `include/LO_SYN.labels.md:31` | — | 1 |
| `L_ST500_BRANCH_1430` | LABEL/LABEL(md) | `src/LO_SYN.mad:3142`, `include/LO_SYN.labels.md:34` | — | 1 |
| `L_ST500_CALL_0316` | LABEL/LABEL(md) | `src/LO_SYN.mad:1384`, `include/LO_SYN.labels.md:12` | — | 1 |
| `L_ST500_CALL_0500` | LABEL/LABEL(md) | `src/LO_SYN.mad:1726`, `include/LO_SYN.labels.md:13` | — | 1 |
| `L_ST500_CALL_1304` | LABEL/LABEL(md) | `src/LO_SYN.mad:2890`, `include/LO_SYN.labels.md:25` | — | 1 |
| `L_ST500_CALL_1327` | LABEL/LABEL(md) | `src/LO_SYN.mad:2947`, `include/LO_SYN.labels.md:28` | — | 1 |
| `L_ST700_BRANCH_0511` | LABEL/LABEL(md) | `src/LO_SYN.mad:1753`, `include/LO_SYN.labels.md:15` | — | 1 |
| `L_ST700_BRANCH_1032` | LABEL/LABEL(md) | `src/LO_SYN.mad:2380`, `include/LO_SYN.labels.md:21` | — | 1 |
| `L_ST700_CALL_1321` | LABEL/LABEL(md) | `src/LO_SYN.mad:2929`, `include/LO_SYN.labels.md:27` | — | 1 |
| `L_ST700_JMP_0507` | LABEL/LABEL(md) | `src/LO_SYN.mad:1747`, `include/LO_SYN.labels.md:14` | — | 1 |
| `MASK_7760` | EQU/LABEL(md) | `src/FOREX_CORE.mad:122`, `include/FOREX.labels.md:193` | 7760B | 1 |
| `MEM_104` | EQU/LABEL(md) | `src/LO_SYN.mad:59`, `include/LO_SYN.labels.md:596` | 104B | 1 |
| `MEM_1101` | EQU/LABEL(md) | `src/LO_SYN.mad:560`, `include/LO_SYN.labels.md:782` | 1101B | 1 |
| `MEM_1105` | EQU/LABEL(md) | `src/LO_SYN.mad:448`, `include/LO_SYN.labels.md:740` | 1105B | 1 |
| `MEM_1111` | EQU/LABEL(md) | `src/LO_SYN.mad:555`, `include/LO_SYN.labels.md:780` | 1111B | 1 |
| `MEM_1124` | EQU/LABEL(md) | `src/LO_SYN.mad:482`, `include/LO_SYN.labels.md:757` | 1124B | 1 |
| `MEM_1130` | EQU/LABEL(md) | `src/LO_SYN.mad:235`, `include/LO_SYN.labels.md:671` | 1130B | 1 |
| `MEM_1200` | EQU/LABEL(md) | `src/LO_SYN.mad:631`, `include/LO_SYN.labels.md:791` | 1200B | 1 |
| `MEM_13` | EQU/LABEL(md) | `src/LO_SYN.mad:58`, `include/LO_SYN.labels.md:595` | 13B | 1 |
| `MEM_14` | EQU/LABEL(md) | `src/LO_SYN.mad:60`, `include/LO_SYN.labels.md:597` | 14B | 1 |
| `MEM_1401` | EQU/LABEL(md) | `src/LO_SYN.mad:652`, `include/LO_SYN.labels.md:793` | 1401B | 1 |
| `MEM_144` | EQU/LABEL(md) | `src/LO_SYN.mad:508`, `include/LO_SYN.labels.md:767` | 144B | 1 |
| `MEM_1455` | EQU/LABEL(md) | `src/LO_SYN.mad:424`, `include/LO_SYN.labels.md:734` | 1455B | 1 |
| `MEM_1503` | EQU/LABEL(md) | `src/LO_SYN.mad:387`, `include/LO_SYN.labels.md:723` | 1503B | 1 |
| `MEM_17` | EQU/LABEL(md) | `src/LO_SYN.mad:67`, `include/LO_SYN.labels.md:598` | 17B | 1 |
| `MEM_2000` | EQU/LABEL(md) | `src/LO_SYN.mad:69`, `include/LO_SYN.labels.md:599` | 2000B | 1 |
| `MEM_2113` | EQU/LABEL(md) | `src/LO_SYN.mad:307`, `include/LO_SYN.labels.md:701` | 2113B | 1 |
| `MEM_2120` | EQU/LABEL(md) | `src/LO_SYN.mad:477`, `include/LO_SYN.labels.md:754` | 2120B | 1 |
| `MEM_2154` | EQU/LABEL(md) | `src/LO_SYN.mad:553`, `include/LO_SYN.labels.md:779` | 2154B | 1 |
| `MEM_2377` | EQU/LABEL(md) | `src/LO_SYN.mad:50`, `include/LO_SYN.labels.md:593` | 2377B | 1 |
| `MEM_2576` | EQU/LABEL(md) | `src/LO_SYN.mad:545`, `include/LO_SYN.labels.md:776` | 2576B | 1 |
| `MEM_264` | EQU/LABEL(md) | `src/LO_SYN.mad:47`, `include/LO_SYN.labels.md:591` | 264B | 1 |
| `MEM_3` | EQU/LABEL(md) | `src/LO_SYN.mad:70`, `include/LO_SYN.labels.md:600` | 3B | 1 |
| `MEM_3000` | EQU/LABEL(md) | `src/LO_SYN.mad:49`, `include/LO_SYN.labels.md:592` | 3000B | 1 |
| `MEM_3005` | EQU/LABEL(md) | `src/LO_SYN.mad:669`, `include/LO_SYN.labels.md:794` | 3005B | 1 |
| `MEM_3054` | EQU/LABEL(md) | `src/LO_SYN.mad:470`, `include/LO_SYN.labels.md:751` | 3054B | 1 |
| `MEM_3055` | EQU/LABEL(md) | `src/LO_SYN.mad:173`, `include/LO_SYN.labels.md:638` | 3055B | 1 |
| `MEM_3107` | EQU/LABEL(md) | `src/LO_SYN.mad:677`, `include/LO_SYN.labels.md:796` | 3107B | 1 |
| `MEM_3440` | EQU/LABEL(md) | `src/LO_SYN.mad:473`, `include/LO_SYN.labels.md:753` | 3440B | 1 |
| `MEM_400` | EQU/LABEL(md) | `src/LO_SYN.mad:51`, `include/LO_SYN.labels.md:594` | 400B | 1 |
| `MEM_4040` | EQU/LABEL(md) | `src/LO_SYN.mad:285`, `include/LO_SYN.labels.md:692` | 4040B | 1 |
| `MEM_4101` | EQU/LABEL(md) | `src/LO_SYN.mad:492`, `include/LO_SYN.labels.md:760` | 4101B | 1 |
| `MEM_4151` | EQU/LABEL(md) | `src/LO_SYN.mad:485`, `include/LO_SYN.labels.md:758` | 4151B | 1 |
| `MEM_4457` | EQU/LABEL(md) | `src/LO_SYN.mad:585`, `include/LO_SYN.labels.md:787` | 4457B | 1 |
| `MEM_4516` | EQU/LABEL(md) | `src/LO_SYN.mad:446`, `include/LO_SYN.labels.md:738` | 4516B | 1 |
| `MEM_4524` | EQU/LABEL(md) | `src/LO_SYN.mad:459`, `include/LO_SYN.labels.md:746` | 4524B | 1 |
| `MEM_4546` | EQU/LABEL(md) | `src/LO_SYN.mad:498`, `include/LO_SYN.labels.md:762` | 4546B | 1 |
| `MEM_4547` | EQU/LABEL(md) | `src/LO_SYN.mad:462`, `include/LO_SYN.labels.md:747` | 4547B | 1 |
| `MEM_4560` | EQU/LABEL(md) | `src/LO_SYN.mad:354`, `include/LO_SYN.labels.md:713` | 4560B | 1 |
| `MEM_5000` | EQU/LABEL(md) | `src/LO_SYN.mad:46`, `include/LO_SYN.labels.md:590` | 5000B | 1 |
| `MEM_502` | EQU/LABEL(md) | `src/LO_SYN.mad:281`, `include/LO_SYN.labels.md:691` | 502B | 1 |
| `MEM_503` | EQU/LABEL(md) | `src/LO_SYN.mad:359`, `include/LO_SYN.labels.md:716` | 503B | 1 |
| `MEM_5115` | EQU/LABEL(md) | `src/LO_SYN.mad:383`, `include/LO_SYN.labels.md:721` | 5115B | 1 |
| `MEM_5117` | EQU/LABEL(md) | `src/LO_SYN.mad:329`, `include/LO_SYN.labels.md:704` | 5117B | 1 |
| `MEM_5144` | EQU/LABEL(md) | `src/LO_SYN.mad:219`, `include/LO_SYN.labels.md:663` | 5144B | 1 |
| `MEM_515` | EQU/LABEL(md) | `src/LO_SYN.mad:243`, `include/LO_SYN.labels.md:674` | 515B | 1 |
| `MEM_543` | EQU/LABEL(md) | `src/LO_SYN.mad:402`, `include/LO_SYN.labels.md:729` | 543B | 1 |
| `MEM_55` | EQU/LABEL(md) | `src/LO_SYN.mad:550`, `include/LO_SYN.labels.md:777` | 55B | 1 |
| `MEM_5501` | EQU/LABEL(md) | `src/LO_SYN.mad:138`, `include/LO_SYN.labels.md:620` | 5501B | 1 |
| `MEM_5520` | EQU/LABEL(md) | `src/LO_SYN.mad:535`, `include/LO_SYN.labels.md:773` | 5520B | 1 |
| `MEM_554` | EQU/LABEL(md) | `src/LO_SYN.mad:302`, `include/LO_SYN.labels.md:699` | 554B | 1 |
| `MEM_6040` | EQU/LABEL(md) | `src/LO_SYN.mad:449`, `include/LO_SYN.labels.md:741` | 6040B | 1 |
| `MEM_6114` | EQU/LABEL(md) | `src/LO_SYN.mad:463`, `include/LO_SYN.labels.md:748` | 6114B | 1 |
| `MEM_6117` | EQU/LABEL(md) | `src/LO_SYN.mad:428`, `include/LO_SYN.labels.md:736` | 6117B | 1 |
| `MEM_6151` | EQU/LABEL(md) | `src/LO_SYN.mad:126`, `include/LO_SYN.labels.md:615` | 6151B | 1 |
| `MEM_6161` | EQU/LABEL(md) | `src/LO_SYN.mad:338`, `include/LO_SYN.labels.md:706` | 6161B | 1 |
| `MEM_6170` | EQU/LABEL(md) | `src/LO_SYN.mad:277`, `include/LO_SYN.labels.md:690` | 6170B | 1 |
| `MEM_6561` | EQU/LABEL(md) | `src/LO_SYN.mad:552`, `include/LO_SYN.labels.md:778` | 6561B | 1 |
| `MEM_70055` | EQU/LABEL(md) | `src/LO_SYN.mad:489`, `include/LO_SYN.labels.md:759` | 70055B | 1 |
| `MEM_70066` | EQU/LABEL(md) | `src/LO_SYN.mad:135`, `include/LO_SYN.labels.md:618` | 70066B | 1 |
| `MEM_70101` | EQU/LABEL(md) | `src/LO_SYN.mad:499`, `include/LO_SYN.labels.md:763` | 70101B | 1 |
| `MEM_70102` | EQU/LABEL(md) | `src/LO_SYN.mad:301`, `include/LO_SYN.labels.md:698` | 70102B | 1 |
| `MEM_70143` | EQU/LABEL(md) | `src/LO_SYN.mad:293`, `include/LO_SYN.labels.md:694` | 70143B | 1 |
| `MEM_70144` | EQU/LABEL(md) | `src/LO_SYN.mad:542`, `include/LO_SYN.labels.md:775` | 70144B | 1 |
| `MEM_70311` | EQU/LABEL(md) | `src/LO_SYN.mad:591`, `include/LO_SYN.labels.md:789` | 70311B | 1 |
| `MEM_7040` | EQU/LABEL(md) | `src/LO_SYN.mad:452`, `include/LO_SYN.labels.md:743` | 7040B | 1 |
| `MEM_70502` | EQU/LABEL(md) | `src/LO_SYN.mad:506`, `include/LO_SYN.labels.md:766` | 70502B | 1 |
| `MEM_70510` | EQU/LABEL(md) | `src/LO_SYN.mad:456`, `include/LO_SYN.labels.md:744` | 70510B | 1 |
| `MEM_70561` | EQU/LABEL(md) | `src/LO_SYN.mad:587`, `include/LO_SYN.labels.md:788` | 70561B | 1 |
| `MEM_71037` | EQU/LABEL(md) | `src/LO_SYN.mad:625`, `include/LO_SYN.labels.md:790` | 71037B | 1 |
| `MEM_71105` | EQU/LABEL(md) | `src/LO_SYN.mad:381`, `include/LO_SYN.labels.md:720` | 71105B | 1 |
| `MEM_71171` | EQU/LABEL(md) | `src/LO_SYN.mad:517`, `include/LO_SYN.labels.md:770` | 71171B | 1 |
| `MEM_71312` | EQU/LABEL(md) | `src/LO_SYN.mad:643`, `include/LO_SYN.labels.md:792` | 71312B | 1 |
| `MEM_71561` | EQU/LABEL(md) | `src/LO_SYN.mad:336`, `include/LO_SYN.labels.md:705` | 71561B | 1 |
| `MEM_71570` | EQU/LABEL(md) | `src/LO_SYN.mad:481`, `include/LO_SYN.labels.md:756` | 71570B | 1 |
| `MEM_72117` | EQU/LABEL(md) | `src/LO_SYN.mad:352`, `include/LO_SYN.labels.md:711` | 72117B | 1 |
| `MEM_72507` | EQU/LABEL(md) | `src/LO_SYN.mad:447`, `include/LO_SYN.labels.md:739` | 72507B | 1 |
| `MEM_72510` | EQU/LABEL(md) | `src/LO_SYN.mad:121`, `include/LO_SYN.labels.md:614` | 72510B | 1 |
| `MEM_72513` | EQU/LABEL(md) | `src/LO_SYN.mad:540`, `include/LO_SYN.labels.md:774` | 72513B | 1 |
| `MEM_72520` | EQU/LABEL(md) | `src/LO_SYN.mad:127`, `include/LO_SYN.labels.md:616` | 72520B | 1 |
| `MEM_73007` | EQU/LABEL(md) | `src/LO_SYN.mad:670`, `include/LO_SYN.labels.md:795` | 73007B | 1 |
| `MEM_74017` | EQU/LABEL(md) | `src/LO_SYN.mad:693`, `include/LO_SYN.labels.md:797` | 74017B | 1 |
| `MEM_74101` | EQU/LABEL(md) | `src/LO_SYN.mad:370`, `include/LO_SYN.labels.md:718` | 74101B | 1 |
| `MEM_74105` | EQU/LABEL(md) | `src/LO_SYN.mad:569`, `include/LO_SYN.labels.md:784` | 74105B | 1 |
| `MEM_74110` | EQU/LABEL(md) | `src/LO_SYN.mad:356`, `include/LO_SYN.labels.md:714` | 74110B | 1 |
| `MEM_74111` | EQU/LABEL(md) | `src/LO_SYN.mad:574`, `include/LO_SYN.labels.md:785` | 74111B | 1 |
| `MEM_74117` | EQU/LABEL(md) | `src/LO_SYN.mad:512`, `include/LO_SYN.labels.md:768` | 74117B | 1 |
| `MEM_74401` | EQU/LABEL(md) | `src/LO_SYN.mad:744`, `include/LO_SYN.labels.md:798` | 74401B | 1 |
| `MEM_74506` | EQU/LABEL(md) | `src/LO_SYN.mad:584`, `include/LO_SYN.labels.md:786` | 74506B | 1 |
| `MEM_74510` | EQU/LABEL(md) | `src/LO_SYN.mad:397`, `include/LO_SYN.labels.md:726` | 74510B | 1 |
| `MEM_74515` | EQU/LABEL(md) | `src/LO_SYN.mad:353`, `include/LO_SYN.labels.md:712` | 74515B | 1 |
| `MEM_74517` | EQU/LABEL(md) | `src/LO_SYN.mad:252`, `include/LO_SYN.labels.md:681` | 74517B | 1 |
| `MEM_74524` | EQU/LABEL(md) | `src/LO_SYN.mad:480`, `include/LO_SYN.labels.md:755` | 74524B | 1 |
| `MEM_75040` | EQU/LABEL(md) | `src/LO_SYN.mad:399`, `include/LO_SYN.labels.md:727` | 75040B | 1 |
| `MEM_7510` | EQU/LABEL(md) | `src/LO_SYN.mad:364`, `include/LO_SYN.labels.md:717` | 7510B | 1 |
| `MEM_7520` | EQU/LABEL(md) | `src/LO_SYN.mad:306`, `include/LO_SYN.labels.md:700` | 7520B | 1 |
| `MEM_7544` | EQU/LABEL(md) | `src/LO_SYN.mad:558`, `include/LO_SYN.labels.md:781` | 7544B | 1 |
| `MEM_75440` | EQU/LABEL(md) | `src/LO_SYN.mad:140`, `include/LO_SYN.labels.md:621` | 75440B | 1 |
| `MEM_75501` | EQU/LABEL(md) | `src/LO_SYN.mad:465`, `include/LO_SYN.labels.md:749` | 75501B | 1 |
| `MEM_7554` | EQU/LABEL(md) | `src/LO_SYN.mad:76`, `include/LO_SYN.labels.md:602` | 7554B | 1 |
| `MEM_75551` | EQU/LABEL(md) | `src/LO_SYN.mad:421`, `include/LO_SYN.labels.md:733` | 75551B | 1 |
| `MEM_76151` | EQU/LABEL(md) | `src/LO_SYN.mad:220`, `include/LO_SYN.labels.md:664` | 76151B | 1 |
| `MEM_76161` | EQU/LABEL(md) | `src/LO_SYN.mad:471`, `include/LO_SYN.labels.md:752` | 76161B | 1 |
| `MEM_77103` | EQU/LABEL(md) | `src/LO_SYN.mad:251`, `include/LO_SYN.labels.md:680` | 77103B | 1 |
| `MEM_77124` | EQU/LABEL(md) | `src/LO_SYN.mad:227`, `include/LO_SYN.labels.md:667` | 77124B | 1 |
| `MEM_77523` | EQU/LABEL(md) | `src/LO_SYN.mad:273`, `include/LO_SYN.labels.md:688` | 77523B | 1 |
| `MEM_77576` | EQU/LABEL(md) | `src/LO_SYN.mad:114`, `include/LO_SYN.labels.md:611` | 77576B | 1 |
| `MIST_BASE_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:125`, `include/FOREX.labels.md:196` | 40037B | 1 |
| `MODE_RT_OCT22` | EQU/LABEL(md) | `src/FOREX_CORE.mad:126`, `include/FOREX.labels.md:197` | 22B | 1 |
| `MODE_RT_OCT22_DEC` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:35`, `include/FOREX.labels.md:323` | 18 | 1 |
| `MODVAL_12501` | EQU/LABEL(md) | `src/LO_GEN.mad:246`, `include/LO_GEN.labels.md:1298` | 12501 | 1 |
| `MODVAL_151` | EQU/LABEL(md) | `src/LO_SYN.mad:375`, `include/LO_SYN.labels.md:429` | 151B | 1 |
| `MODVAL_24763` | EQU/LABEL(md) | `src/LO_GEN.mad:249`, `include/LO_GEN.labels.md:1301` | 24763 | 1 |
| `MODVAL_24774` | EQU/LABEL(md) | `src/LO_GEN.mad:251`, `include/LO_GEN.labels.md:1303` | 24774 | 1 |
| `MODVAL_24775` | EQU/LABEL(md) | `src/LO_GEN.mad:252`, `include/LO_GEN.labels.md:1304` | 24775 | 1 |
| `MODVAL_25659` | EQU/LABEL(md) | `src/LO_GEN.mad:253`, `include/LO_GEN.labels.md:1305` | 25659 | 1 |
| `MODVAL_6502` | EQU/LABEL(md) | `src/LO_SYN.mad:487`, `include/LO_SYN.labels.md:434` | 6502B | 1 |
| `MODVAL_6520` | EQU/LABEL(md) | `src/LO_SYN.mad:484`, `include/LO_SYN.labels.md:433` | 6520B | 1 |
| `MODVAL_70110` | EQU/LABEL(md) | `src/LO_SYN.mad:418`, `include/LO_SYN.labels.md:431` | 70110B | 1 |
| `MODVAL_70113` | EQU/LABEL(md) | `src/LO_SYN.mad:519`, `include/LO_SYN.labels.md:435` | 70113B | 1 |
| `MODVAL_76543` | EQU/LABEL(md) | `src/LO_SYN.mad:556`, `include/LO_SYN.labels.md:436` | 76543B | 1 |
| `MONTHFI` | LABEL(md) | `include/FOREX.labels.md:66` | — | 1 |
| `MONTH_INDEX_BASE` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:69`, `include/FOREX.labels.md:261` | 24 | 1 |
| `MONTH_NAMES` | LABEL(md)/TEXT | `src/FOREX_RUNTIME.mad:413`, `include/FOREX.labels.md:64` | — | 1 |
| `MSK` | TEXT | `src/FOREX_RUNTIME.mad:515` | GOST_BLANK | 1 |
| `MUL_7771` | EQU/LABEL(md) | `src/FOREX_CORE.mad:127`, `include/FOREX.labels.md:198` | 7771B | 1 |
| `NEG_12` | EQU/LABEL(md) | `src/LO_GEN.mad:267`, `include/LO_GEN.labels.md:1319` | -12 | 1 |
| `NOLIS_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:128`, `include/FOREX.labels.md:199` | 4003B | 1 |
| `NPR` | LABEL(md) | `include/FOREX.labels.md:27`, `include/FOREX.labels.md:78` | — | 1 |
| `OCT_CYCLE` | LABEL | `src/FOREX_RUNTIME.mad:443` | — | 1 |
| `OCT_DEC` | LABEL(md)/NAME/SUBP | `src/FOREX_RUNTIME.mad:432`, `include/FOREX_ROOT.mad:72`, `include/FOREX.labels.md:67`, `include/FOREX.labels.md:84` | — | 1 |
| `OCT_DEC_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:129`, `include/FOREX.labels.md:200` | 74013B | 1 |
| `OCT_EX_DIGIT_LOOP` | LABEL | `src/FOREX_RUNTIME.mad:492` | — | 1 |
| `OCT_EX_RETURN` | LABEL | `src/FOREX_RUNTIME.mad:504` | — | 1 |
| `OCT_ISO_SHIFT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:110`, `include/FOREX.labels.md:302` | 64-8 | 1 |
| `OCT_SIX_DIGIT_MASK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:70`, `include/FOREX.labels.md:262` | =777 7777-C | 1 |
| `OCT_SYMBOL` | COMMON | `src/FOREX_RUNTIME.mad:462` | — | 1 |
| `PAGE_GIVE` | LABEL(md)/NAME/SUBP | `include/FOREX_ROOT.mad:71`, `include/FOREX_ROOT.mad:235`, `include/FOREX.labels.md:85` | — | 1 |
| `PAGE_GIVE_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:131`, `include/FOREX.labels.md:202` | 74012B | 1 |
| `PAGE_TAKE` | ENTRY/LABEL(md)/SUBP | `include/FOREX_ROOT.mad:70`, `include/FOREX_ROOT.mad:276`, `include/FOREX.labels.md:86` | — | 1 |
| `PAGE_TAKE_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:132`, `include/FOREX.labels.md:203` | 74011B | 1 |
| `PG_BLOCK_MASK` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:39`, `include/FOREX.labels.md:327` | =4000 | 1 |
| `PG_COMMON` | LABEL | `include/FOREX_ROOT.mad:255` | — | 1 |
| `PG_COPY_LOOP` | LABEL | `include/FOREX_ROOT.mad:256` | — | 1 |
| `PG_EX67` | LABEL | `include/FOREX_ROOT.mad:273` | — | 1 |
| `PG_EX67_CODE` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:40`, `include/FOREX.labels.md:328` | =:11 4037 77 | 1 |
| `PG_EX67_CONST` | LABEL | `include/FOREX_ROOT.mad:275` | — | 1 |
| `PG_FLAG_SHIFT` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:41`, `include/FOREX.labels.md:329` | 64+12 | 1 |
| `PG_GO_CODE_1` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:42`, `include/FOREX.labels.md:330` | =:00 2677 | 1 |
| `PG_GO_CODE_2` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:43`, `include/FOREX.labels.md:331` | =:00 6736 77 | 1 |
| `PG_RESTORE17` | LABEL | `include/FOREX_ROOT.mad:270` | — | 1 |
| `PG_SAVE_S` | COMMON | `include/FOREX_ROOT.mad:290` | ONE_WORD | 1 |
| `PG_WORD_SHIFT` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:44`, `include/FOREX.labels.md:332` | 64-20 | 1 |
| `POW10_1` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:114`, `include/FOREX.labels.md:306` | 10.0 | 1 |
| `POW10_2` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:113`, `include/FOREX.labels.md:305` | 100.0 | 1 |
| `POW10_3` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:112`, `include/FOREX.labels.md:304` | 1000.0 | 1 |
| `POW10_4` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:111`, `include/FOREX.labels.md:303` | 10000.0 | 1 |
| `POW10_5` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:72`, `include/FOREX.labels.md:264` | 100000.0 | 1 |
| `PRIN` | LABEL(md) | `include/FOREX.labels.md:30`, `include/FOREX.labels.md:81` | 0o510327 | 1 |
| `PRINT8` | SUBP | `src/FOREX_RUNTIME.mad:196` | — | 1 |
| `PRINT_MESSAGE` | LABEL/LABEL(md) | `src/FOREX_CORE.mad:295`, `include/FOREX_ROOT.mad:125`, `include/FOREX.labels.md:30`, `include/FOREX.labels.md:81` | — | 1 |
| `PRINT_MESSAGE_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:133`, `include/FOREX.labels.md:204` | 40023B | 1 |
| `R100_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:134`, `include/FOREX.labels.md:205` | 4033B | 1 |
| `REGSEL_13` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:257`, `src/LO_GEN.mad:581`, `src/LO_GEN.mad:599`, `src/LO_GEN.mad:664`, `include/LO_GEN.labels.md:1309` | 13 | 1 |
| `REGSEL_15` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:259`, `src/LO_GEN.mad:688`, `src/LO_GEN.mad:718`, `src/LO_GEN.mad:724`, `src/LO_GEN.mad:808`, `src/LO_GEN.mad:889` … (+39) | 15 | 1 |
| `REGSEL_2` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:260`, `src/LO_GEN.mad:557`, `src/LO_GEN.mad:3507`, `src/LO_GEN.mad:3510`, `include/LO_GEN.labels.md:1312` | 2 | 1 |
| `REGSEL_3` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:261`, `src/LO_GEN.mad:626`, `src/LO_GEN.mad:1033`, `src/LO_GEN.mad:1081`, `src/LO_GEN.mad:1939`, `src/LO_GEN.mad:1975` … (+11) | 3 | 1 |
| `REGSEL_5` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:263`, `src/LO_GEN.mad:632`, `src/LO_GEN.mad:667`, `src/LO_GEN.mad:3330`, `src/LO_GEN.mad:3351`, `include/LO_GEN.labels.md:1315` | 5 | 1 |
| `REGSEL_9` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:266`, `src/LO_GEN.mad:703`, `src/LO_GEN.mad:835`, `src/LO_GEN.mad:928`, `src/LO_GEN.mad:1117`, `src/LO_GEN.mad:1120` … (+10) | 9 | 1 |
| `REGVAL_1002` | EQU/LABEL(md) | `src/LO_SYN.mad:616`, `include/LO_SYN.labels.md:554` | 1002B | 1 |
| `REGVAL_1006` | EQU/LABEL(md) | `src/LO_SYN.mad:618`, `include/LO_SYN.labels.md:555` | 1006B | 1 |
| `REGVAL_1033` | EQU/LABEL(md) | `src/LO_SYN.mad:622`, `include/LO_SYN.labels.md:556` | 1033B | 1 |
| `REGVAL_1034` | EQU/LABEL(md) | `src/LO_SYN.mad:623`, `include/LO_SYN.labels.md:557` | 1034B | 1 |
| `REGVAL_1035` | EQU/LABEL(md) | `src/LO_SYN.mad:624`, `include/LO_SYN.labels.md:558` | 1035B | 1 |
| `REGVAL_110` | EQU/LABEL(md) | `src/LO_SYN.mad:300`, `include/LO_SYN.labels.md:522` | 110B | 1 |
| `REGVAL_1102` | EQU/LABEL(md) | `src/LO_SYN.mad:627`, `include/LO_SYN.labels.md:559` | 1102B | 1 |
| `REGVAL_1115` | EQU/LABEL(md) | `src/LO_SYN.mad:630`, `include/LO_SYN.labels.md:560` | 1115B | 1 |
| `REGVAL_113` | EQU/LABEL(md) | `src/LO_SYN.mad:575`, `include/LO_SYN.labels.md:548` | 113B | 1 |
| `REGVAL_1204` | EQU/LABEL(md) | `src/LO_SYN.mad:633`, `include/LO_SYN.labels.md:561` | 1204B | 1 |
| `REGVAL_1214` | EQU/LABEL(md) | `src/LO_SYN.mad:635`, `include/LO_SYN.labels.md:562` | 1214B | 1 |
| `REGVAL_1217` | EQU/LABEL(md) | `src/LO_SYN.mad:637`, `include/LO_SYN.labels.md:563` | 1217B | 1 |
| `REGVAL_122` | EQU/LABEL(md) | `src/LO_SYN.mad:130`, `include/LO_SYN.labels.md:503` | 122B | 1 |
| `REGVAL_1301` | EQU/LABEL(md) | `src/LO_SYN.mad:638`, `include/LO_SYN.labels.md:564` | 1301B | 1 |
| `REGVAL_1303` | EQU/LABEL(md) | `src/LO_SYN.mad:640`, `include/LO_SYN.labels.md:565` | 1303B | 1 |
| `REGVAL_1315` | EQU/LABEL(md) | `src/LO_SYN.mad:646`, `include/LO_SYN.labels.md:566` | 1315B | 1 |
| `REGVAL_1402` | EQU/LABEL(md) | `src/LO_SYN.mad:653`, `include/LO_SYN.labels.md:567` | 1402B | 1 |
| `REGVAL_1403` | EQU/LABEL(md) | `src/LO_SYN.mad:654`, `include/LO_SYN.labels.md:568` | 1403B | 1 |
| `REGVAL_1407` | EQU/LABEL(md) | `src/LO_SYN.mad:657`, `include/LO_SYN.labels.md:569` | 1407B | 1 |
| `REGVAL_15` | EQU/LABEL(md) | `src/LO_SYN.mad:56`, `include/LO_SYN.labels.md:493` | 15B | 1 |
| `REGVAL_1524` | EQU/LABEL(md) | `src/LO_SYN.mad:544`, `include/LO_SYN.labels.md:546` | 1524B | 1 |
| `REGVAL_154` | EQU/LABEL(md) | `src/LO_SYN.mad:115`, `include/LO_SYN.labels.md:500` | 154B | 1 |
| `REGVAL_160` | EQU/LABEL(md) | `src/LO_SYN.mad:539`, `include/LO_SYN.labels.md:545` | 160B | 1 |
| `REGVAL_172` | EQU/LABEL(md) | `src/LO_SYN.mad:513`, `include/LO_SYN.labels.md:541` | 172B | 1 |
| `REGVAL_2001` | EQU/LABEL(md) | `src/LO_SYN.mad:658`, `include/LO_SYN.labels.md:570` | 2001B | 1 |
| `REGVAL_2010` | EQU/LABEL(md) | `src/LO_SYN.mad:664`, `include/LO_SYN.labels.md:571` | 2010B | 1 |
| `REGVAL_20113` | EQU/LABEL(md) | `src/LO_SYN.mad:159`, `include/LO_SYN.labels.md:506` | 20113B | 1 |
| `REGVAL_20117` | EQU/LABEL(md) | `src/LO_SYN.mad:479`, `include/LO_SYN.labels.md:537` | 20117B | 1 |
| `REGVAL_20142` | EQU/LABEL(md) | `src/LO_SYN.mad:172`, `include/LO_SYN.labels.md:507` | 20142B | 1 |
| `REGVAL_2174` | EQU/LABEL(md) | `src/LO_SYN.mad:72`, `include/LO_SYN.labels.md:497` | 2174B | 1 |
| `REGVAL_2544` | EQU/LABEL(md) | `src/LO_SYN.mad:369`, `include/LO_SYN.labels.md:528` | 2544B | 1 |
| `REGVAL_30311` | EQU/LABEL(md) | `src/LO_SYN.mad:65`, `include/LO_SYN.labels.md:496` | 30311B | 1 |
| `REGVAL_3102` | EQU/LABEL(md) | `src/LO_SYN.mad:673`, `include/LO_SYN.labels.md:572` | 3102B | 1 |
| `REGVAL_3103` | EQU/LABEL(md) | `src/LO_SYN.mad:674`, `include/LO_SYN.labels.md:573` | 3103B | 1 |
| `REGVAL_327` | EQU/LABEL(md) | `src/LO_SYN.mad:602`, `include/LO_SYN.labels.md:550` | 327B | 1 |
| `REGVAL_36017` | EQU/LABEL(md) | `src/LO_SYN.mad:63`, `include/LO_SYN.labels.md:494` | 36017B | 1 |
| `REGVAL_4010` | EQU/LABEL(md) | `src/LO_SYN.mad:685`, `include/LO_SYN.labels.md:574` | 4010B | 1 |
| `REGVAL_4023` | EQU/LABEL(md) | `src/LO_SYN.mad:697`, `include/LO_SYN.labels.md:575` | 4023B | 1 |
| `REGVAL_4025` | EQU/LABEL(md) | `src/LO_SYN.mad:700`, `include/LO_SYN.labels.md:576` | 4025B | 1 |
| `REGVAL_40510` | EQU/LABEL(md) | `src/LO_SYN.mad:496`, `include/LO_SYN.labels.md:538` | 40510B | 1 |
| `REGVAL_40547` | EQU/LABEL(md) | `src/LO_SYN.mad:453`, `include/LO_SYN.labels.md:532` | 40547B | 1 |
| `REGVAL_4071` | EQU/LABEL(md) | `src/LO_SYN.mad:721`, `include/LO_SYN.labels.md:577` | 4071B | 1 |
| `REGVAL_41105` | EQU/LABEL(md) | `src/LO_SYN.mad:503`, `include/LO_SYN.labels.md:539` | 41105B | 1 |
| `REGVAL_4131` | EQU/LABEL(md) | `src/LO_SYN.mad:229`, `include/LO_SYN.labels.md:515` | 4131B | 1 |
| `REGVAL_4313` | EQU/LABEL(md) | `src/LO_SYN.mad:731`, `include/LO_SYN.labels.md:578` | 4313B | 1 |
| `REGVAL_4321` | EQU/LABEL(md) | `src/LO_SYN.mad:736`, `include/LO_SYN.labels.md:579` | 4321B | 1 |
| `REGVAL_4325` | EQU/LABEL(md) | `src/LO_SYN.mad:740`, `include/LO_SYN.labels.md:580` | 4325B | 1 |
| `REGVAL_4406` | EQU/LABEL(md) | `src/LO_SYN.mad:747`, `include/LO_SYN.labels.md:582` | 4406B | 1 |
| `REGVAL_502` | EQU/LABEL(md) | `src/LO_SYN.mad:605`, `include/LO_SYN.labels.md:551` | 502B | 1 |
| `REGVAL_505` | EQU/LABEL(md) | `src/LO_SYN.mad:559`, `include/LO_SYN.labels.md:547` | 505B | 1 |
| `REGVAL_506` | EQU/LABEL(md) | `src/LO_SYN.mad:609`, `include/LO_SYN.labels.md:552` | 506B | 1 |
| `REGVAL_510` | EQU/LABEL(md) | `src/LO_SYN.mad:611`, `include/LO_SYN.labels.md:553` | 510B | 1 |
| `REGVAL_5505` | EQU/LABEL(md) | `src/LO_SYN.mad:455`, `include/LO_SYN.labels.md:533` | 5505B | 1 |
| `REGVAL_551` | EQU/LABEL(md) | `src/LO_SYN.mad:410`, `include/LO_SYN.labels.md:530` | 551B | 1 |
| `REGVAL_70146` | EQU/LABEL(md) | `src/LO_SYN.mad:276`, `include/LO_SYN.labels.md:519` | 70146B | 1 |
| `REGVAL_70502` | EQU/LABEL(md) | `src/LO_SYN.mad:303`, `include/LO_SYN.labels.md:523` | 70502B | 1 |
| `REGVAL_70514` | EQU/LABEL(md) | `src/LO_SYN.mad:337`, `include/LO_SYN.labels.md:525` | 70514B | 1 |
| `REGVAL_72510` | EQU/LABEL(md) | `src/LO_SYN.mad:289`, `include/LO_SYN.labels.md:521` | 72510B | 1 |
| `REGVAL_74404` | EQU/LABEL(md) | `src/LO_SYN.mad:745`, `include/LO_SYN.labels.md:581` | 74404B | 1 |
| `REGVAL_7502` | EQU/LABEL(md) | `src/LO_SYN.mad:474`, `include/LO_SYN.labels.md:535` | 7502B | 1 |
| `REGVAL_76505` | EQU/LABEL(md) | `src/LO_SYN.mad:578`, `include/LO_SYN.labels.md:549` | 76505B | 1 |
| `RET_CELL` | EQU/LABEL(md) | `src/FOREX_CORE.mad:136`, `include/FOREX.labels.md:207` | 4023B | 1 |
| `RET_MOD_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:138`, `include/FOREX.labels.md:209` | 40050B | 1 |
| `RM_WORDS_4` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:48`, `include/FOREX.labels.md:336` | 4 | 1 |
| `STACK_OFF_M1` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:75`, `include/FOREX.labels.md:267` | -1 | 1 |
| `STACK_OFF_M6` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:80`, `include/FOREX.labels.md:272` | -6 | 1 |
| `STACK_OFF_M8` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:81`, `include/FOREX.labels.md:273` | -8 | 1 |
| `SVCELL_101` | EQU/LABEL(md) | `src/LO_SYN.mad:589`, `include/LO_SYN.labels.md:449` | 101B | 1 |
| `SVCELL_1201` | EQU/LABEL(md) | `src/LO_SYN.mad:749`, `include/LO_SYN.labels.md:482` | 1201B | 1 |
| `SVCELL_1322` | EQU/LABEL(md) | `src/LO_SYN.mad:647`, `include/LO_SYN.labels.md:460` | 1322B | 1 |
| `SVCELL_14` | EQU/LABEL(md) | `src/LO_SYN.mad:61`, `include/LO_SYN.labels.md:446` | 14B | 1 |
| `SVCELL_16` | EQU/LABEL(md) | `src/LO_SYN.mad:57`, `include/LO_SYN.labels.md:445` | 16B | 1 |
| `SVCELL_17` | EQU/LABEL(md) | `src/LO_SYN.mad:55`, `include/LO_SYN.labels.md:444` | 17B | 1 |
| `SVCELL_2` | EQU/LABEL(md) | `src/LO_SYN.mad:71`, `include/LO_SYN.labels.md:447` | 2B | 1 |
| `SVCELL_200` | EQU/LABEL(md) | `src/LO_SYN.mad:687`, `include/LO_SYN.labels.md:468` | 200B | 1 |
| `SVCELL_2006` | EQU/LABEL(md) | `src/LO_SYN.mad:663`, `include/LO_SYN.labels.md:464` | 2006B | 1 |
| `SVCELL_201` | EQU/LABEL(md) | `src/LO_SYN.mad:719`, `include/LO_SYN.labels.md:475` | 201B | 1 |
| `SVCELL_3` | EQU/LABEL(md) | `src/LO_SYN.mad:41`, `include/LO_SYN.labels.md:442` | 3B | 1 |
| `SVCELL_322` | EQU/LABEL(md) | `src/LO_SYN.mad:597`, `include/LO_SYN.labels.md:452` | 322B | 1 |
| `SVCELL_4015` | EQU/LABEL(md) | `src/LO_SYN.mad:691`, `include/LO_SYN.labels.md:469` | 4015B | 1 |
| `SVCELL_4061` | EQU/LABEL(md) | `src/LO_SYN.mad:720`, `include/LO_SYN.labels.md:476` | 4061B | 1 |
| `SVCELL_4303` | EQU/LABEL(md) | `src/LO_SYN.mad:728`, `include/LO_SYN.labels.md:477` | 4303B | 1 |
| `SVCELL_4315` | EQU/LABEL(md) | `src/LO_SYN.mad:734`, `include/LO_SYN.labels.md:479` | 4315B | 1 |
| `SVCELL_4317` | EQU/LABEL(md) | `src/LO_SYN.mad:735`, `include/LO_SYN.labels.md:480` | 4317B | 1 |
| `SVCELL_4330` | EQU/LABEL(md) | `src/LO_SYN.mad:743`, `include/LO_SYN.labels.md:481` | 4330B | 1 |
| `SVCELL_4412` | EQU/LABEL(md) | `src/LO_SYN.mad:750`, `include/LO_SYN.labels.md:483` | 4412B | 1 |
| `SVCELL_4422` | EQU/LABEL(md) | `src/LO_SYN.mad:754`, `include/LO_SYN.labels.md:485` | 4422B | 1 |
| `SVCELL_70324` | EQU/LABEL(md) | `src/LO_SYN.mad:599`, `include/LO_SYN.labels.md:453` | 70324B | 1 |
| `SVCELL_70503` | EQU/LABEL(md) | `src/LO_SYN.mad:606`, `include/LO_SYN.labels.md:455` | 70503B | 1 |
| `SVCELL_71013` | EQU/LABEL(md) | `src/LO_SYN.mad:619`, `include/LO_SYN.labels.md:458` | 71013B | 1 |
| `SVCELL_71213` | EQU/LABEL(md) | `src/LO_SYN.mad:634`, `include/LO_SYN.labels.md:459` | 71213B | 1 |
| `SVCELL_71325` | EQU/LABEL(md) | `src/LO_SYN.mad:650`, `include/LO_SYN.labels.md:461` | 71325B | 1 |
| `SVCELL_71404` | EQU/LABEL(md) | `src/LO_SYN.mad:655`, `include/LO_SYN.labels.md:462` | 71404B | 1 |
| `SVCELL_72002` | EQU/LABEL(md) | `src/LO_SYN.mad:659`, `include/LO_SYN.labels.md:463` | 72002B | 1 |
| `SVCELL_74034` | EQU/LABEL(md) | `src/LO_SYN.mad:707`, `include/LO_SYN.labels.md:472` | 74034B | 1 |
| `SVCELL_74042` | EQU/LABEL(md) | `src/LO_SYN.mad:714`, `include/LO_SYN.labels.md:474` | 74042B | 1 |
| `SVCELL_74413` | EQU/LABEL(md) | `src/LO_SYN.mad:751`, `include/LO_SYN.labels.md:484` | 74413B | 1 |
| `TEXT_LIT_000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:82`, `include/FOREX.labels.md:274` | ''000000'' | 1 |
| `TEXT_LIT_1H_055` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:83`, `include/FOREX.labels.md:275` | 1H'055' | 1 |
| `TEXT_LIT_2H_200` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:84`, `include/FOREX.labels.md:276` | 2H '200' | 1 |
| `TEXT_LIT_3H00` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:85`, `include/FOREX.labels.md:277` | 3H00 | 1 |
| `TEXT_LIT_6H00` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:86`, `include/FOREX.labels.md:278` | =6H00 | 1 |
| `TEXT_LIT_6H000000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:88`, `include/FOREX.labels.md:280` | 6H000000 | 1 |
| `TEXT_LIT_6H000_00` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:89`, `include/FOREX.labels.md:281` | 6H000 00 | 1 |
| `TEXT_LIT_6H00_00` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:90`, `include/FOREX.labels.md:282` | =6H00/00/ | 1 |
| `TEXT_LIT_6HAB_CEH` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:92`, `include/FOREX.labels.md:284` | 6HABГCEH | 1 |
| `TEXT_LIT_6HARRAY` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:93`, `include/FOREX.labels.md:285` | 6HARRAY | 1 |
| `TEXT_LIT_6HA_PMA` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:94`, `include/FOREX.labels.md:286` | 6HAПPMAЯ | 1 |
| `TEXT_LIT_6HERROR` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:95`, `include/FOREX.labels.md:287` | 6HERROR | 1 |
| `TEXT_LIT_6HIN_STA` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:96`, `include/FOREX.labels.md:288` | 6HIN STA | 1 |
| `TEXT_LIT_6HNDART` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:97`, `include/FOREX.labels.md:289` | 6HNDART | 1 |
| `TEXT_LIT_6HOKTHO` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:98`, `include/FOREX.labels.md:290` | 6HOKTHOЯ | 1 |
| `TEXT_LIT_6H_00_00` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:99`, `include/FOREX.labels.md:291` | 6H 00.00 | 1 |
| `TEXT_LIT_6H_17_17` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:100`, `include/FOREX.labels.md:292` | =6H'17''17''''''''' | 1 |
| `TEXT_LIT_6H_201_200_7` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:101`, `include/FOREX.labels.md:293` | 6H'201'  '200'7 | 1 |
| `TEXT_LIT_6H_3_17_17_17` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:103`, `include/FOREX.labels.md:295` | =6H'3''17''''17''17''' | 1 |
| `TEXT_LIT_6H_EBMAP` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:104`, `include/FOREX.labels.md:296` | 6HФEBMAP | 1 |
| `TEXT_LIT_6H_EK` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:105`, `include/FOREX.labels.md:297` | 6HДEK | 1 |
| `TEXT_LIT_6H_H` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:106`, `include/FOREX.labels.md:298` | 6HИЮHИЮЛ | 1 |
| `TEXT_LO_GEN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:50`, `include/FOREX.labels.md:338` | 8HLO*GEN | 1 |
| `TEXT_LO_SYN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:51`, `include/FOREX.labels.md:339` | 8HLO*SYN | 1 |
| `TIME_SCALE` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:52`, `include/FOREX.labels.md:340` | =R100.0 | 1 |
| `TIME_SEP_A` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:53`, `include/FOREX.labels.md:341` | =6H'''17''17''17''17''17' | 1 |
| `TIME_SEP_B` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:54`, `include/FOREX.labels.md:342` | =6H'17''17''17''''17''17' | 1 |
| `TIME_SEP_C` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:55`, `include/FOREX.labels.md:343` | =6H'''''''16''''' | 1 |
| `TTEX_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:141`, `include/FOREX.labels.md:212` | 4037B | 1 |
| `TTEX_BASE_ADDR` | EQU/LABEL(md) | `src/FOREX_CORE.mad:142`, `include/FOREX.labels.md:213` | 40033B | 1 |
| `WORDVAL_0003500000030264` | EQU/LABEL(md) | `src/LO_GEN.mad:493`, `include/LO_GEN.labels.md:1293` | 0003500000030264 | 1 |
| `WORDVAL_0004220010075377` | EQU/LABEL(md) | `src/LO_GEN.mad:494`, `include/LO_GEN.labels.md:1294` | 0004220010075377 | 1 |
| `WRITLIBR` | SUBP | `src/FOREX_RUNTIME.mad:195` | — | 1 |
| `*A*` | COMMON | `src/FOREX_CORE.mad:156`, `src/LO_GEN.mad:497`, `src/LO_SYN.mad:18`, `include/FOREX_ROOT.mad:78` | ADDR_OCT_4000 | 0 |
| `A` | LABEL(md) | `include/FOREX.labels.md:8`, `include/LO_GEN.labels.md:26` | — | 0 |
| `ADDR_117` | EQU/LABEL(md) | `src/LO_GEN.mad:61`, `include/LO_GEN.labels.md:1109` | 117B | 0 |
| `ADDR_2200` | EQU/LABEL(md) | `src/LO_GEN.mad:106`, `include/LO_GEN.labels.md:1154` | 2200B | 0 |
| `ADDR_30314` | EQU/LABEL(md) | `src/LO_GEN.mad:118`, `include/LO_GEN.labels.md:1166` | 30314B | 0 |
| `ADDR_400` | EQU/LABEL(md) | `src/LO_GEN.mad:129`, `include/LO_GEN.labels.md:1177` | 400B | 0 |
| `ADDR_702` | EQU/LABEL(md) | `src/LO_GEN.mad:228`, `include/LO_GEN.labels.md:1276` | 702B | 0 |
| `ADDR_7600` | EQU/LABEL(md) | `src/LO_GEN.mad:240`, `include/LO_GEN.labels.md:1288` | 7600B | 0 |
| `ADDR_MOD_0023` | LABEL(md) | `include/LO_GEN.labels.md:78`, `include/LO_GEN.labels.md:1326` | 0o277523 | 0 |
| `ADDR_MOD_0037` | LABEL(md) | `include/LO_GEN.labels.md:90`, `include/LO_GEN.labels.md:1300`, `include/LO_GEN.labels.md:1314` | 0o277537 | 0 |
| `ADDR_MOD_0053` | LABEL(md) | `include/LO_GEN.labels.md:102`, `include/LO_GEN.labels.md:1300` | 0o277553 | 0 |
| `ADDR_MOD_0104` | LABEL(md) | `include/LO_GEN.labels.md:127` | 0o277604 | 0 |
| `ADDR_MOD_0105` | LABEL(md) | `include/LO_GEN.labels.md:128`, `include/LO_GEN.labels.md:1301` | 0o277605 | 0 |
| `ADDR_MOD_0111` | LABEL(md) | `include/LO_GEN.labels.md:132` | 0o277611 | 0 |
| `ADDR_MOD_0112` | LABEL(md) | `include/LO_GEN.labels.md:133` | 0o277612 | 0 |
| `ADDR_MOD_0113` | LABEL(md) | `include/LO_GEN.labels.md:134` | 0o277613 | 0 |
| `ADDR_MOD_0116` | LABEL(md) | `include/LO_GEN.labels.md:137` | 0o277616 | 0 |
| `ADDR_MOD_0117` | LABEL(md) | `include/LO_GEN.labels.md:138` | 0o277617 | 0 |
| `ADDR_MOD_0120` | LABEL(md) | `include/LO_GEN.labels.md:139` | 0o277620 | 0 |
| `ADDR_MOD_0125` | LABEL(md) | `include/LO_GEN.labels.md:144` | 0o277625 | 0 |
| `ADDR_MOD_0134` | LABEL(md) | `include/LO_GEN.labels.md:151` | 0o277634 | 0 |
| `ADDR_MOD_0137` | LABEL(md) | `include/LO_GEN.labels.md:154` | 0o277637 | 0 |
| `ADDR_MOD_0142` | LABEL(md) | `include/LO_GEN.labels.md:157` | 0o277642 | 0 |
| `ADDR_MOD_0144` | LABEL(md) | `include/LO_GEN.labels.md:159` | 0o277644 | 0 |
| `ADDR_MOD_0204` | LABEL(md) | `include/LO_GEN.labels.md:191` | 0o277704 | 0 |
| `ADDR_MOD_0206` | LABEL(md) | `include/LO_GEN.labels.md:193` | 0o277706 | 0 |
| `ADDR_MOD_0207` | LABEL(md) | `include/LO_GEN.labels.md:194` | 0o277707 | 0 |
| `ADDR_MOD_0213` | LABEL(md) | `include/LO_GEN.labels.md:198`, `include/LO_GEN.labels.md:1302` | 0o277713 | 0 |
| `ADDR_MOD_0222` | LABEL(md) | `include/LO_GEN.labels.md:205` | 0o277722 | 0 |
| `ADDR_MOD_0225` | LABEL(md) | `include/LO_GEN.labels.md:208` | 0o277725 | 0 |
| `ADDR_MOD_0226` | LABEL(md) | `include/LO_GEN.labels.md:209` | 0o277726 | 0 |
| `ADDR_MOD_0227` | LABEL(md) | `include/LO_GEN.labels.md:210` | 0o277727 | 0 |
| `ADDR_MOD_0260` | LABEL(md) | `include/LO_GEN.labels.md:235` | 0o277760 | 0 |
| `ADDR_MOD_0262` | LABEL(md) | `include/LO_GEN.labels.md:237` | 0o277762 | 0 |
| `ADDR_MOD_0264` | LABEL(md) | `include/LO_GEN.labels.md:239`, `include/LO_GEN.labels.md:1301` | 0o277764 | 0 |
| `ADDR_MOD_0266` | LABEL(md) | `include/LO_GEN.labels.md:241` | 0o277766 | 0 |
| `ADDR_MOD_0267` | LABEL(md) | `include/LO_GEN.labels.md:242`, `include/LO_GEN.labels.md:1301` | 0o277767 | 0 |
| `ADDR_MOD_0271` | LABEL(md) | `include/LO_GEN.labels.md:244` | 0o277771 | 0 |
| `ADDR_MOD_0306` | LABEL(md) | `include/LO_GEN.labels.md:257` | 0o300006 | 0 |
| `ADDR_MOD_0314` | LABEL(md) | `include/LO_GEN.labels.md:263` | 0o300014 | 0 |
| `ADDR_MOD_0317` | LABEL(md) | `include/LO_GEN.labels.md:266` | 0o300017 | 0 |
| `ADDR_MOD_0322` | LABEL(md) | `include/LO_GEN.labels.md:269` | 0o300022 | 0 |
| `ADDR_MOD_0323` | LABEL(md) | `include/LO_GEN.labels.md:270` | 0o300023 | 0 |
| `ADDR_MOD_0331` | LABEL(md) | `include/LO_GEN.labels.md:276`, `include/LO_GEN.labels.md:1303` | 0o300031 | 0 |
| `ADDR_MOD_0337` | LABEL(md) | `include/LO_GEN.labels.md:282` | 0o300037 | 0 |
| `ADDR_MOD_0341` | LABEL(md) | `include/LO_GEN.labels.md:284` | 0o300041 | 0 |
| `ADDR_MOD_0343` | LABEL(md) | `include/LO_GEN.labels.md:286` | 0o300043 | 0 |
| `ADDR_MOD_0351` | LABEL(md) | `include/LO_GEN.labels.md:292` | 0o300051 | 0 |
| `ADDR_MOD_0352` | LABEL(md) | `include/LO_GEN.labels.md:293` | 0o300052 | 0 |
| `ADDR_MOD_0355` | LABEL(md) | `include/LO_GEN.labels.md:296` | 0o300055 | 0 |
| `ADDR_MOD_0362` | LABEL(md) | `include/LO_GEN.labels.md:301` | 0o300062 | 0 |
| `ADDR_MOD_0363` | LABEL(md) | `include/LO_GEN.labels.md:302` | 0o300063 | 0 |
| `ADDR_MOD_0636` | LABEL(md) | `include/LO_GEN.labels.md:473` | 0o300336 | 0 |
| `ADDR_MOD_0641` | LABEL(md) | `include/LO_GEN.labels.md:476` | 0o300341 | 0 |
| `ADDR_MOD_0643` | LABEL(md) | `include/LO_GEN.labels.md:478`, `include/LO_GEN.labels.md:1303` | 0o300343 | 0 |
| `ADDR_MOD_0645` | LABEL(md) | `include/LO_GEN.labels.md:480`, `include/LO_GEN.labels.md:1303` | 0o300345 | 0 |
| `ADDR_MOD_0667` | LABEL(md) | `include/LO_GEN.labels.md:498` | 0o300367 | 0 |
| `ADDR_MOD_0671` | LABEL(md) | `include/LO_GEN.labels.md:500` | 0o300371 | 0 |
| `ADDR_MOD_0710` | LABEL(md) | `include/LO_GEN.labels.md:515`, `include/LO_GEN.labels.md:1302` | 0o300410 | 0 |
| `ADDR_MOD_0714` | LABEL(md) | `include/LO_GEN.labels.md:519` | 0o300414 | 0 |
| `ADDR_MOD_0715` | LABEL(md) | `include/LO_GEN.labels.md:520` | 0o300415 | 0 |
| `ADDR_MOD_0720` | LABEL(md) | `include/LO_GEN.labels.md:523` | 0o300420 | 0 |
| `ADDR_MOD_0726` | LABEL(md) | `include/LO_GEN.labels.md:529` | 0o300426 | 0 |
| `ADDR_MOD_0730` | LABEL(md) | `include/LO_GEN.labels.md:531` | 0o300430 | 0 |
| `ADDR_MOD_0732` | LABEL(md) | `include/LO_GEN.labels.md:533` | 0o300432 | 0 |
| `ADDR_MOD_0734` | LABEL(md) | `include/LO_GEN.labels.md:535` | 0o300434 | 0 |
| `ADDR_MOD_0736` | LABEL(md) | `include/LO_GEN.labels.md:537` | 0o300436 | 0 |
| `ADDR_MOD_0743` | LABEL(md) | `include/LO_GEN.labels.md:542`, `include/LO_GEN.labels.md:1302` | 0o300443 | 0 |
| `ADDR_MOD_0752` | LABEL(md) | `include/LO_GEN.labels.md:549` | 0o300452 | 0 |
| `ADDR_MOD_0753` | LABEL(md) | `include/LO_GEN.labels.md:550` | 0o300453 | 0 |
| `ADDR_MOD_0757` | LABEL(md) | `include/LO_GEN.labels.md:554` | 0o300457 | 0 |
| `ADDR_MOD_0761` | LABEL(md) | `include/LO_GEN.labels.md:556`, `include/LO_GEN.labels.md:1296` | 0o300461 | 0 |
| `ADDR_MOD_0765` | LABEL(md) | `include/LO_GEN.labels.md:560` | 0o300465 | 0 |
| `ADDR_MOD_0770` | LABEL(md) | `include/LO_GEN.labels.md:563` | 0o300470 | 0 |
| `ADDR_MOD_0774` | LABEL(md) | `include/LO_GEN.labels.md:567` | 0o300474 | 0 |
| `ADDR_MOD_0777` | LABEL(md) | `include/LO_GEN.labels.md:570` | 0o300477 | 0 |
| `ADDR_MOD_1011` | LABEL(md) | `include/LO_GEN.labels.md:580` | 0o300511 | 0 |
| `ADDR_MOD_1022` | LABEL(md) | `include/LO_GEN.labels.md:589` | 0o300522 | 0 |
| `ADDR_MOD_1023` | LABEL(md) | `include/LO_GEN.labels.md:590` | 0o300523 | 0 |
| `ADDR_MOD_1030` | LABEL(md) | `include/LO_GEN.labels.md:595` | 0o300530 | 0 |
| `ADDR_MOD_1044` | LABEL(md) | `include/LO_GEN.labels.md:607`, `include/LO_GEN.labels.md:1296` | 0o300544 | 0 |
| `ADDR_MOD_1062` | LABEL(md) | `include/LO_GEN.labels.md:621` | 0o300562 | 0 |
| `ADDR_MOD_1075` | LABEL(md) | `include/LO_GEN.labels.md:632`, `include/LO_GEN.labels.md:1296` | 0o300575 | 0 |
| `ADDR_MOD_1104` | LABEL(md) | `include/LO_GEN.labels.md:639` | 0o300604 | 0 |
| `ADDR_MOD_1115` | LABEL(md) | `include/LO_GEN.labels.md:648` | 0o300615 | 0 |
| `ADDR_MOD_1116` | LABEL(md) | `include/LO_GEN.labels.md:649` | 0o300616 | 0 |
| `ADDR_MOD_1124` | LABEL(md) | `include/LO_GEN.labels.md:655` | 0o300624 | 0 |
| `ADDR_MOD_1127` | LABEL(md) | `include/LO_GEN.labels.md:658` | 0o300627 | 0 |
| `ADDR_MOD_1134` | LABEL(md) | `include/LO_GEN.labels.md:663` | 0o300634 | 0 |
| `ADDR_MOD_1135` | LABEL(md) | `include/LO_GEN.labels.md:664` | 0o300635 | 0 |
| `ADDR_MOD_1136` | LABEL(md) | `include/LO_GEN.labels.md:665` | 0o300636 | 0 |
| `ADDR_MOD_1145` | LABEL(md) | `include/LO_GEN.labels.md:672` | 0o300645 | 0 |
| `ADDR_MOD_1152` | LABEL(md) | `include/LO_GEN.labels.md:677` | 0o300652 | 0 |
| `ADDR_MOD_1157` | LABEL(md) | `include/LO_GEN.labels.md:682` | 0o300657 | 0 |
| `ADDR_MOD_1161` | LABEL(md) | `include/LO_GEN.labels.md:684` | 0o300661 | 0 |
| `ADDR_MOD_1162` | LABEL(md) | `include/LO_GEN.labels.md:685` | 0o300662 | 0 |
| `ADDR_MOD_1166` | LABEL(md) | `include/LO_GEN.labels.md:689` | 0o300666 | 0 |
| `ADDR_MOD_1170` | LABEL(md) | `include/LO_GEN.labels.md:691` | 0o300670 | 0 |
| `ADDR_MOD_1173` | LABEL(md) | `include/LO_GEN.labels.md:694` | 0o300673 | 0 |
| `ADDR_MOD_1175` | LABEL(md) | `include/LO_GEN.labels.md:696` | 0o300675 | 0 |
| `ADDR_MOD_1207` | LABEL(md) | `include/LO_GEN.labels.md:706` | 0o300707 | 0 |
| `ADDR_MOD_1210` | LABEL(md) | `include/LO_GEN.labels.md:707` | 0o300710 | 0 |
| `ADDR_MOD_1213` | LABEL(md) | `include/LO_GEN.labels.md:710` | 0o300713 | 0 |
| `ADDR_MOD_1215` | LABEL(md) | `include/LO_GEN.labels.md:712` | 0o300715 | 0 |
| `ADDR_MOD_1227` | LABEL(md) | `include/LO_GEN.labels.md:722` | 0o300727 | 0 |
| `ADDR_MOD_1237` | LABEL(md) | `include/LO_GEN.labels.md:730` | 0o300737 | 0 |
| `ADDR_MOD_1265` | LABEL(md) | `include/LO_GEN.labels.md:752` | 0o300765 | 0 |
| `ADDR_MOD_1273` | LABEL(md) | `include/LO_GEN.labels.md:758`, `include/LO_GEN.labels.md:1298` | 0o300773 | 0 |
| `ADDR_MOD_1274` | LABEL(md) | `include/LO_GEN.labels.md:759` | 0o300774 | 0 |
| `ADDR_MOD_1300` | LABEL(md) | `include/LO_GEN.labels.md:763` | 0o301000 | 0 |
| `ADDR_MOD_1302` | LABEL(md) | `include/LO_GEN.labels.md:765`, `include/LO_GEN.labels.md:1297` | 0o301002 | 0 |
| `ADDR_MOD_1303` | LABEL(md) | `include/LO_GEN.labels.md:766` | 0o301003 | 0 |
| `ADDR_MOD_1306` | LABEL(md) | `include/LO_GEN.labels.md:769` | 0o301006 | 0 |
| `ADDR_MOD_1316` | LABEL(md) | `include/LO_GEN.labels.md:777` | 0o301016 | 0 |
| `ADDR_MOD_1317` | LABEL(md) | `include/LO_GEN.labels.md:778`, `include/LO_GEN.labels.md:1298` | 0o301017 | 0 |
| `ADDR_MOD_1321` | LABEL(md) | `include/LO_GEN.labels.md:780` | 0o301021 | 0 |
| `ADDR_MOD_1331` | LABEL(md) | `include/LO_GEN.labels.md:788` | 0o301031 | 0 |
| `ADDR_MOD_1335` | LABEL(md) | `include/LO_GEN.labels.md:792` | 0o301035 | 0 |
| `ADDR_MOD_1343` | LABEL(md) | `include/LO_GEN.labels.md:798` | 0o301043 | 0 |
| `ADDR_MOD_1345` | LABEL(md) | `include/LO_GEN.labels.md:800` | 0o301045 | 0 |
| `ADDR_MOD_1346` | LABEL(md) | `include/LO_GEN.labels.md:801` | 0o301046 | 0 |
| `ADDR_MOD_1356` | LABEL(md) | `include/LO_GEN.labels.md:809` | 0o301056 | 0 |
| `ADDR_MOD_1357` | LABEL(md) | `include/LO_GEN.labels.md:810` | 0o301057 | 0 |
| `ADDR_MOD_1366` | LABEL(md) | `include/LO_GEN.labels.md:817` | 0o301066 | 0 |
| `ADDR_MOD_1367` | LABEL(md) | `include/LO_GEN.labels.md:818` | 0o301067 | 0 |
| `ADDR_MOD_1371` | LABEL(md) | `include/LO_GEN.labels.md:820` | 0o301071 | 0 |
| `ADDR_MOD_1374` | LABEL(md) | `include/LO_GEN.labels.md:823` | 0o301074 | 0 |
| `ADDR_MOD_1400` | LABEL(md) | `include/LO_GEN.labels.md:827` | 0o301100 | 0 |
| `ADDR_MOD_1401` | LABEL(md) | `include/LO_GEN.labels.md:828` | 0o301101 | 0 |
| `ADDR_MOD_1406` | LABEL(md) | `include/LO_GEN.labels.md:833` | 0o301106 | 0 |
| `ADDR_MOD_1415` | LABEL(md) | `include/LO_GEN.labels.md:840` | 0o301115 | 0 |
| `ADDR_MOD_1424` | LABEL(md) | `include/LO_GEN.labels.md:847` | 0o301124 | 0 |
| `ADDR_MOD_1435` | LABEL(md) | `include/LO_GEN.labels.md:856` | 0o301135 | 0 |
| `ADDR_MOD_1442` | LABEL(md) | `include/LO_GEN.labels.md:861` | 0o301142 | 0 |
| `ADDR_MOD_1452` | LABEL(md) | `include/LO_GEN.labels.md:869`, `include/LO_GEN.labels.md:1299` | 0o301152 | 0 |
| `ADDR_MOD_1453` | LABEL(md) | `include/LO_GEN.labels.md:870` | 0o301153 | 0 |
| `ADDR_MOD_1504` | LABEL(md) | `include/LO_GEN.labels.md:895` | 0o301204 | 0 |
| `ADDR_MOD_1505` | LABEL(md) | `include/LO_GEN.labels.md:896` | 0o301205 | 0 |
| `ADDR_MOD_1506` | LABEL(md) | `include/LO_GEN.labels.md:897` | 0o301206 | 0 |
| `ADDR_MOD_1523` | LABEL(md) | `include/LO_GEN.labels.md:910` | 0o301223 | 0 |
| `ADDR_MOD_1531` | LABEL(md) | `include/LO_GEN.labels.md:916` | 0o301231 | 0 |
| `ADDR_MOD_1540` | LABEL(md) | `include/LO_GEN.labels.md:923` | 0o301240 | 0 |
| `ADDR_MOD_1544` | LABEL(md) | `include/LO_GEN.labels.md:927` | 0o301244 | 0 |
| `ADDR_MOD_1550` | LABEL(md) | `include/LO_GEN.labels.md:931` | 0o301250 | 0 |
| `ADDR_MOD_1553` | LABEL(md) | `include/LO_GEN.labels.md:934` | 0o301253 | 0 |
| `ADDR_MOD_1562` | LABEL(md) | `include/LO_GEN.labels.md:941` | 0o301262 | 0 |
| `ADDR_MOD_1565` | LABEL(md) | `include/LO_GEN.labels.md:944` | 0o301265 | 0 |
| `ADDR_MOD_1572` | LABEL(md) | `include/LO_GEN.labels.md:949` | 0o301272 | 0 |
| `ADDR_MOD_1574` | LABEL(md) | `include/LO_GEN.labels.md:951` | 0o301274 | 0 |
| `ADDR_MOD_1601` | LABEL(md) | `include/LO_GEN.labels.md:956` | 0o301301 | 0 |
| `ADDR_MOD_1611` | LABEL(md) | `include/LO_GEN.labels.md:964` | 0o301311 | 0 |
| `ADDR_MOD_1621` | LABEL(md) | `include/LO_GEN.labels.md:972` | 0o301321 | 0 |
| `ADDR_MOD_1625` | LABEL(md) | `include/LO_GEN.labels.md:976` | 0o301325 | 0 |
| `ADDR_MOD_1644` | LABEL(md) | `include/LO_GEN.labels.md:991` | 0o301344 | 0 |
| `ADDR_MOD_1655` | LABEL(md) | `include/LO_GEN.labels.md:1000` | 0o301355 | 0 |
| `ADDR_MOD_1657` | LABEL(md) | `include/LO_GEN.labels.md:1002` | 0o301357 | 0 |
| `ADDR_MOD_1706` | LABEL(md) | `include/LO_GEN.labels.md:1025` | 0o301406 | 0 |
| `ADDR_MOD_1707` | LABEL(md) | `include/LO_GEN.labels.md:1026` | 0o301407 | 0 |
| `ADDR_MOD_1743` | LABEL(md) | `include/LO_GEN.labels.md:1054` | 0o301443 | 0 |
| `ADDR_MOD_1747` | LABEL(md) | `include/LO_GEN.labels.md:1058` | 0o301447 | 0 |
| `ADD_0005` | LABEL(md) | `include/LO_GEN.labels.md:64`, `include/LO_GEN.labels.md:1154` | 0o277505 | 0 |
| `ADD_0072` | LABEL(md) | `include/LO_GEN.labels.md:117`, `include/LO_GEN.labels.md:1323` | 0o277572 | 0 |
| `ADD_0702` | LABEL(md) | `include/LO_GEN.labels.md:509` | 0o300402 | 0 |
| `ADD_1710` | LABEL(md) | `include/LO_GEN.labels.md:1027` | 0o301410 | 0 |
| `AND_MASK_0022` | LABEL(md) | `include/LO_GEN.labels.md:77`, `include/LO_GEN.labels.md:1140` | 0o277522 | 0 |
| `AND_MASK_0150` | LABEL(md) | `include/LO_GEN.labels.md:163`, `include/LO_GEN.labels.md:1140` | 0o277650 | 0 |
| `AND_MASK_0160` | LABEL(md) | `include/LO_GEN.labels.md:171`, `include/LO_GEN.labels.md:1273` | 0o277660 | 0 |
| `AND_MASK_0175` | LABEL(md) | `include/LO_GEN.labels.md:184`, `include/LO_GEN.labels.md:1273` | 0o277675 | 0 |
| `AND_MASK_0201` | LABEL(md) | `include/LO_GEN.labels.md:188`, `include/LO_GEN.labels.md:1158` | 0o277701 | 0 |
| `AND_MASK_0246` | LABEL(md) | `include/LO_GEN.labels.md:225` | 0o277746 | 0 |
| `AND_MASK_0275` | LABEL(md) | `include/LO_GEN.labels.md:248`, `include/LO_GEN.labels.md:1169` | 0o277775 | 0 |
| `AND_MASK_0305` | LABEL(md) | `include/LO_GEN.labels.md:256`, `include/LO_GEN.labels.md:1171` | 0o300005 | 0 |
| `AND_MASK_0313` | LABEL(md) | `include/LO_GEN.labels.md:262`, `include/LO_GEN.labels.md:1158` | 0o300013 | 0 |
| `AND_MASK_0326` | LABEL(md) | `include/LO_GEN.labels.md:273` | 0o300026 | 0 |
| `AND_MASK_0644` | LABEL(md) | `include/LO_GEN.labels.md:479`, `include/LO_GEN.labels.md:1261` | 0o300344 | 0 |
| `AND_MASK_0646` | LABEL(md) | `include/LO_GEN.labels.md:481`, `include/LO_GEN.labels.md:1210` | 0o300346 | 0 |
| `AND_MASK_0741` | LABEL(md) | `include/LO_GEN.labels.md:540`, `include/LO_GEN.labels.md:1158` | 0o300441 | 0 |
| `AND_MASK_0745` | LABEL(md) | `include/LO_GEN.labels.md:544`, `include/LO_GEN.labels.md:1211` | 0o300445 | 0 |
| `AND_MASK_0755` | LABEL(md) | `include/LO_GEN.labels.md:552` | 0o300455 | 0 |
| `AND_MASK_0762` | LABEL(md) | `include/LO_GEN.labels.md:557`, `include/LO_GEN.labels.md:1213` | 0o300462 | 0 |
| `AND_MASK_0772` | LABEL(md) | `include/LO_GEN.labels.md:565`, `include/LO_GEN.labels.md:1220` | 0o300472 | 0 |
| `AND_MASK_1002` | LABEL(md) | `include/LO_GEN.labels.md:573` | 0o300502 | 0 |
| `AND_MASK_1007` | LABEL(md) | `include/LO_GEN.labels.md:578` | 0o300507 | 0 |
| `AND_MASK_1013` | LABEL(md) | `include/LO_GEN.labels.md:582`, `include/LO_GEN.labels.md:1211` | 0o300513 | 0 |
| `AND_MASK_1016` | LABEL(md) | `include/LO_GEN.labels.md:585` | 0o300516 | 0 |
| `AND_MASK_1025` | LABEL(md) | `include/LO_GEN.labels.md:592` | 0o300525 | 0 |
| `AND_MASK_1032` | LABEL(md) | `include/LO_GEN.labels.md:597`, `include/LO_GEN.labels.md:1211` | 0o300532 | 0 |
| `AND_MASK_1035` | LABEL(md) | `include/LO_GEN.labels.md:600`, `include/LO_GEN.labels.md:1226` | 0o300535 | 0 |
| `AND_MASK_1053` | LABEL(md) | `include/LO_GEN.labels.md:614` | 0o300553 | 0 |
| `AND_MASK_1056` | LABEL(md) | `include/LO_GEN.labels.md:617`, `include/LO_GEN.labels.md:1153` | 0o300556 | 0 |
| `AND_MASK_1064` | LABEL(md) | `include/LO_GEN.labels.md:623`, `include/LO_GEN.labels.md:1231` | 0o300564 | 0 |
| `AND_MASK_1066` | LABEL(md) | `include/LO_GEN.labels.md:625` | 0o300566 | 0 |
| `AND_MASK_1076` | LABEL(md) | `include/LO_GEN.labels.md:633` | 0o300576 | 0 |
| `AND_MASK_1107` | LABEL(md) | `include/LO_GEN.labels.md:642`, `include/LO_GEN.labels.md:1259` | 0o300607 | 0 |
| `AND_MASK_1113` | LABEL(md) | `include/LO_GEN.labels.md:646` | 0o300613 | 0 |
| `AND_MASK_1117` | LABEL(md) | `include/LO_GEN.labels.md:650` | 0o300617 | 0 |
| `AND_MASK_1125` | LABEL(md) | `include/LO_GEN.labels.md:656` | 0o300625 | 0 |
| `AND_MASK_1137` | LABEL(md) | `include/LO_GEN.labels.md:666`, `include/LO_GEN.labels.md:1210` | 0o300637 | 0 |
| `AND_MASK_1200` | LABEL(md) | `include/LO_GEN.labels.md:699`, `include/LO_GEN.labels.md:1149` | 0o300700 | 0 |
| `AND_MASK_1205` | LABEL(md) | `include/LO_GEN.labels.md:704` | 0o300705 | 0 |
| `AND_MASK_1276` | LABEL(md) | `include/LO_GEN.labels.md:761`, `include/LO_GEN.labels.md:1220` | 0o300776 | 0 |
| `AND_MASK_1310` | LABEL(md) | `include/LO_GEN.labels.md:771`, `include/LO_GEN.labels.md:1211` | 0o301010 | 0 |
| `AND_MASK_1364` | LABEL(md) | `include/LO_GEN.labels.md:815` | 0o301064 | 0 |
| `AND_MASK_1376` | LABEL(md) | `include/LO_GEN.labels.md:825` | 0o301076 | 0 |
| `AND_MASK_1410` | LABEL(md) | `include/LO_GEN.labels.md:835` | 0o301110 | 0 |
| `AND_MASK_1422` | LABEL(md) | `include/LO_GEN.labels.md:845` | 0o301122 | 0 |
| `AND_MASK_1433` | LABEL(md) | `include/LO_GEN.labels.md:854` | 0o301133 | 0 |
| `AND_MASK_1437` | LABEL(md) | `include/LO_GEN.labels.md:858` | 0o301137 | 0 |
| `AND_MASK_1444` | LABEL(md) | `include/LO_GEN.labels.md:863` | 0o301144 | 0 |
| `AND_MASK_1446` | LABEL(md) | `include/LO_GEN.labels.md:865`, `include/LO_GEN.labels.md:1272` | 0o301146 | 0 |
| `AND_MASK_1511` | LABEL(md) | `include/LO_GEN.labels.md:900` | 0o301211 | 0 |
| `AND_MASK_1542` | LABEL(md) | `include/LO_GEN.labels.md:925` | 0o301242 | 0 |
| `AND_MASK_1555` | LABEL(md) | `include/LO_GEN.labels.md:936` | 0o301255 | 0 |
| `AND_MASK_1567` | LABEL(md) | `include/LO_GEN.labels.md:946` | 0o301267 | 0 |
| `AND_MASK_1575` | LABEL(md) | `include/LO_GEN.labels.md:952` | 0o301275 | 0 |
| `AND_MASK_1603` | LABEL(md) | `include/LO_GEN.labels.md:958` | 0o301303 | 0 |
| `AND_MASK_1612` | LABEL(md) | `include/LO_GEN.labels.md:965` | 0o301312 | 0 |
| `AND_MASK_1623` | LABEL(md) | `include/LO_GEN.labels.md:974` | 0o301323 | 0 |
| `AND_MASK_1704` | LABEL(md) | `include/LO_GEN.labels.md:1023` | 0o301404 | 0 |
| `AND_MASK_1745` | LABEL(md) | `include/LO_GEN.labels.md:1056` | 0o301445 | 0 |
| `AND_MASK_1756` | LABEL(md) | `include/LO_GEN.labels.md:1065`, `include/LO_GEN.labels.md:1272` | 0o301456 | 0 |
| `B40/1` | LABEL | `src/FOREX_RUNTIME.mad:512` | — | 0 |
| `BR_NONZERO_0136` | LABEL(md) | `include/LO_GEN.labels.md:153`, `include/LO_GEN.labels.md:1539` | 0o277636 | 0 |
| `BR_NONZERO_0147` | LABEL(md) | `include/LO_GEN.labels.md:162` | 0o277647 | 0 |
| `BR_NONZERO_0151` | LABEL(md) | `include/LO_GEN.labels.md:164`, `include/LO_GEN.labels.md:1410` | 0o277651 | 0 |
| `BR_NONZERO_0165` | LABEL(md) | `include/LO_GEN.labels.md:176`, `include/LO_GEN.labels.md:1405` | 0o277665 | 0 |
| `BR_NONZERO_0173` | LABEL(md) | `include/LO_GEN.labels.md:182`, `include/LO_GEN.labels.md:1410` | 0o277673 | 0 |
| `BR_NONZERO_0200` | LABEL(md) | `include/LO_GEN.labels.md:187`, `include/LO_GEN.labels.md:1409` | 0o277700 | 0 |
| `BR_NONZERO_0220` | LABEL(md) | `include/LO_GEN.labels.md:203` | 0o277720 | 0 |
| `BR_NONZERO_0234` | LABEL(md) | `include/LO_GEN.labels.md:215`, `include/LO_GEN.labels.md:1414` | 0o277734 | 0 |
| `BR_NONZERO_0273` | LABEL(md) | `include/LO_GEN.labels.md:246`, `include/LO_GEN.labels.md:1420` | 0o277773 | 0 |
| `BR_NONZERO_0312` | LABEL(md) | `include/LO_GEN.labels.md:261`, `include/LO_GEN.labels.md:1423` | 0o300012 | 0 |
| `BR_NONZERO_0316` | LABEL(md) | `include/LO_GEN.labels.md:265`, `include/LO_GEN.labels.md:1424` | 0o300016 | 0 |
| `BR_NONZERO_0357` | LABEL(md) | `include/LO_GEN.labels.md:298`, `include/LO_GEN.labels.md:1436` | 0o300057 | 0 |
| `BR_NONZERO_0640` | LABEL(md) | `include/LO_GEN.labels.md:475`, `include/LO_GEN.labels.md:1439` | 0o300340 | 0 |
| `BR_NONZERO_0701` | LABEL(md) | `include/LO_GEN.labels.md:508`, `include/LO_GEN.labels.md:1448` | 0o300401 | 0 |
| `BR_NONZERO_1077` | LABEL(md) | `include/LO_GEN.labels.md:634` | 0o300577 | 0 |
| `BR_NONZERO_1106` | LABEL(md) | `include/LO_GEN.labels.md:641`, `include/LO_GEN.labels.md:1463` | 0o300606 | 0 |
| `BR_NONZERO_1126` | LABEL(md) | `include/LO_GEN.labels.md:657`, `include/LO_GEN.labels.md:1465` | 0o300626 | 0 |
| `BR_NONZERO_1147` | LABEL(md) | `include/LO_GEN.labels.md:674`, `include/LO_GEN.labels.md:1472` | 0o300647 | 0 |
| `BR_NONZERO_1156` | LABEL(md) | `include/LO_GEN.labels.md:681`, `include/LO_GEN.labels.md:1476` | 0o300656 | 0 |
| `BR_NONZERO_1224` | LABEL(md) | `include/LO_GEN.labels.md:719`, `include/LO_GEN.labels.md:1493` | 0o300724 | 0 |
| `BR_NONZERO_1525` | LABEL(md) | `include/LO_GEN.labels.md:912`, `include/LO_GEN.labels.md:1514` | 0o301225 | 0 |
| `BR_ZERO_0074` | LABEL(md) | `include/LO_GEN.labels.md:119`, `include/LO_GEN.labels.md:1538` | 0o277574 | 0 |
| `BR_ZERO_0077` | LABEL(md) | `include/LO_GEN.labels.md:122`, `include/LO_GEN.labels.md:1399` | 0o277577 | 0 |
| `BR_ZERO_0106` | LABEL(md) | `include/LO_GEN.labels.md:129`, `include/LO_GEN.labels.md:1401` | 0o277606 | 0 |
| `BR_ZERO_0157` | LABEL(md) | `include/LO_GEN.labels.md:170`, `include/LO_GEN.labels.md:1410` | 0o277657 | 0 |
| `BR_ZERO_0250` | LABEL(md) | `include/LO_GEN.labels.md:227`, `include/LO_GEN.labels.md:1415` | 0o277750 | 0 |
| `BR_ZERO_0276` | LABEL(md) | `include/LO_GEN.labels.md:249`, `include/LO_GEN.labels.md:1420` | 0o277776 | 0 |
| `BR_ZERO_0304` | LABEL(md) | `include/LO_GEN.labels.md:255`, `include/LO_GEN.labels.md:1422` | 0o300004 | 0 |
| `BR_ZERO_0336` | LABEL(md) | `include/LO_GEN.labels.md:281`, `include/LO_GEN.labels.md:1410` | 0o300036 | 0 |
| `BR_ZERO_0675` | LABEL(md) | `include/LO_GEN.labels.md:504`, `include/LO_GEN.labels.md:1512` | 0o300375 | 0 |
| `BR_ZERO_0711` | LABEL(md) | `include/LO_GEN.labels.md:516` | 0o300411 | 0 |
| `BR_ZERO_0724` | LABEL(md) | `include/LO_GEN.labels.md:527`, `include/LO_GEN.labels.md:1523` | 0o300424 | 0 |
| `BR_ZERO_1202` | LABEL(md) | `include/LO_GEN.labels.md:701`, `include/LO_GEN.labels.md:1484` | 0o300702 | 0 |
| `BR_ZERO_1231` | LABEL(md) | `include/LO_GEN.labels.md:724`, `include/LO_GEN.labels.md:1488` | 0o300731 | 0 |
| `BR_ZERO_1234` | LABEL(md) | `include/LO_GEN.labels.md:727`, `include/LO_GEN.labels.md:1489` | 0o300734 | 0 |
| `BR_ZERO_1241` | LABEL(md) | `include/LO_GEN.labels.md:732`, `include/LO_GEN.labels.md:1490` | 0o300741 | 0 |
| `BR_ZERO_1244` | LABEL(md) | `include/LO_GEN.labels.md:735`, `include/LO_GEN.labels.md:1491` | 0o300744 | 0 |
| `BR_ZERO_1255` | LABEL(md) | `include/LO_GEN.labels.md:744`, `include/LO_GEN.labels.md:1494` | 0o300755 | 0 |
| `BR_ZERO_1260` | LABEL(md) | `include/LO_GEN.labels.md:747`, `include/LO_GEN.labels.md:1495` | 0o300760 | 0 |
| `BR_ZERO_1267` | LABEL(md) | `include/LO_GEN.labels.md:754`, `include/LO_GEN.labels.md:1497` | 0o300767 | 0 |
| `BR_ZERO_1600` | LABEL(md) | `include/LO_GEN.labels.md:955`, `include/LO_GEN.labels.md:1517` | 0o301300 | 0 |
| `BR_ZERO_1627` | LABEL(md) | `include/LO_GEN.labels.md:978`, `include/LO_GEN.labels.md:1520` | 0o301327 | 0 |
| `BR_ZERO_1767` | LABEL(md) | `include/LO_GEN.labels.md:1074`, `include/LO_GEN.labels.md:1540` | 0o301467 | 0 |
| `BR_ZERO_1776` | LABEL(md) | `include/LO_GEN.labels.md:1081`, `include/LO_GEN.labels.md:1092` | 0o301476 | 0 |
| `BSS` | COMMON/LABEL(md) | `src/FOREX_RUNTIME.mad:187`, `src/FOREX_RUNTIME.mad:323`, `include/FOREX.labels.md:357`, `include/LO_GEN.labels.md:1550` | — | 0 |
| `BUFFER` | LABEL(md) | `include/FOREX.labels.md:46` | — | 0 |
| `BUF_WRITE_0004` | LABEL(md) | `include/LO_GEN.labels.md:63`, `include/LO_GEN.labels.md:1273` | 0o277504 | 0 |
| `BUF_WRITE_0011` | LABEL(md) | `include/LO_GEN.labels.md:68`, `include/LO_GEN.labels.md:1150`, `include/LO_GEN.labels.md:1308` | 0o277511 | 0 |
| `BUF_WRITE_0012` | LABEL(md) | `include/LO_GEN.labels.md:69`, `include/LO_GEN.labels.md:1147`, `include/LO_GEN.labels.md:1308` | 0o277512 | 0 |
| `BUF_WRITE_0013` | LABEL(md) | `include/LO_GEN.labels.md:70`, `include/LO_GEN.labels.md:1151` | 0o277513 | 0 |
| `BUF_WRITE_0020` | LABEL(md) | `include/LO_GEN.labels.md:75`, `include/LO_GEN.labels.md:1144` | 0o277520 | 0 |
| `BUF_WRITE_0021` | LABEL(md) | `include/LO_GEN.labels.md:76`, `include/LO_GEN.labels.md:1276` | 0o277521 | 0 |
| `BUF_WRITE_0025` | LABEL(md) | `include/LO_GEN.labels.md:80`, `include/LO_GEN.labels.md:1317` | 0o277525 | 0 |
| `BUF_WRITE_0026` | LABEL(md) | `include/LO_GEN.labels.md:81`, `include/LO_GEN.labels.md:1309` | 0o277526 | 0 |
| `BUF_WRITE_0027` | LABEL(md) | `include/LO_GEN.labels.md:82`, `include/LO_GEN.labels.md:1317` | 0o277527 | 0 |
| `BUF_WRITE_0032` | LABEL(md) | `include/LO_GEN.labels.md:85`, `include/LO_GEN.labels.md:1094` | 0o277532 | 0 |
| `BUF_WRITE_0033` | LABEL(md) | `include/LO_GEN.labels.md:86` | 0o277533 | 0 |
| `BUF_WRITE_0040` | LABEL(md) | `include/LO_GEN.labels.md:91`, `include/LO_GEN.labels.md:1312` | 0o277540 | 0 |
| `BUF_WRITE_0042` | LABEL(md) | `include/LO_GEN.labels.md:93` | 0o277542 | 0 |
| `BUF_WRITE_0044` | LABEL(md) | `include/LO_GEN.labels.md:95` | 0o277544 | 0 |
| `BUF_WRITE_0054` | LABEL(md) | `include/LO_GEN.labels.md:103` | 0o277554 | 0 |
| `BUF_WRITE_0055` | LABEL(md) | `include/LO_GEN.labels.md:104`, `include/LO_GEN.labels.md:1326` | 0o277555 | 0 |
| `BUF_WRITE_0062` | LABEL(md) | `include/LO_GEN.labels.md:109`, `include/LO_GEN.labels.md:1118` | 0o277562 | 0 |
| `BUF_WRITE_0064` | LABEL(md) | `include/LO_GEN.labels.md:111`, `include/LO_GEN.labels.md:1311`, `include/LO_GEN.labels.md:1322` | 0o277564 | 0 |
| `BUF_WRITE_0065` | LABEL(md) | `include/LO_GEN.labels.md:112` | 0o277565 | 0 |
| `BUF_WRITE_0067` | LABEL(md) | `include/LO_GEN.labels.md:114`, `include/LO_GEN.labels.md:1136` | 0o277567 | 0 |
| `BUF_WRITE_0071` | LABEL(md) | `include/LO_GEN.labels.md:116`, `include/LO_GEN.labels.md:1323` | 0o277571 | 0 |
| `BUF_WRITE_0110` | LABEL(md) | `include/LO_GEN.labels.md:131` | 0o277610 | 0 |
| `BUF_WRITE_0122` | LABEL(md) | `include/LO_GEN.labels.md:141`, `include/LO_GEN.labels.md:1094` | 0o277622 | 0 |
| `BUF_WRITE_0176` | LABEL(md) | `include/LO_GEN.labels.md:185` | 0o277676 | 0 |
| `BUF_WRITE_0235` | LABEL(md) | `include/LO_GEN.labels.md:216` | 0o277735 | 0 |
| `BUF_WRITE_0243` | LABEL(md) | `include/LO_GEN.labels.md:222` | 0o277743 | 0 |
| `BUF_WRITE_0255` | LABEL(md) | `include/LO_GEN.labels.md:232` | 0o277755 | 0 |
| `BUF_WRITE_0300` | LABEL(md) | `include/LO_GEN.labels.md:251` | 0o300000 | 0 |
| `BUF_WRITE_0346` | LABEL(md) | `include/LO_GEN.labels.md:289` | 0o300046 | 0 |
| `BUF_WRITE_0370` | LABEL(md) | `include/LO_GEN.labels.md:307` | 0o300070 | 0 |
| `BUF_WRITE_0421` | LABEL(md) | `include/LO_GEN.labels.md:332` | 0o300121 | 0 |
| `BUF_WRITE_0502` | LABEL(md) | `include/LO_GEN.labels.md:381` | 0o300202 | 0 |
| `BUF_WRITE_0503` | LABEL(md) | `include/LO_GEN.labels.md:382` | 0o300203 | 0 |
| `BUF_WRITE_0504` | LABEL(md) | `include/LO_GEN.labels.md:383` | 0o300204 | 0 |
| `BUF_WRITE_0505` | LABEL(md) | `include/LO_GEN.labels.md:384` | 0o300205 | 0 |
| `BUF_WRITE_0510` | LABEL(md) | `include/LO_GEN.labels.md:387` | 0o300210 | 0 |
| `BUF_WRITE_0513` | LABEL(md) | `include/LO_GEN.labels.md:390` | 0o300213 | 0 |
| `BUF_WRITE_0626` | LABEL(md) | `include/LO_GEN.labels.md:465`, `include/LO_GEN.labels.md:1129` | 0o300326 | 0 |
| `BUF_WRITE_0632` | LABEL(md) | `include/LO_GEN.labels.md:469` | 0o300332 | 0 |
| `BUF_WRITE_0635` | LABEL(md) | `include/LO_GEN.labels.md:472`, `include/LO_GEN.labels.md:1138` | 0o300335 | 0 |
| `BUF_WRITE_0673` | LABEL(md) | `include/LO_GEN.labels.md:502`, `include/LO_GEN.labels.md:1123` | 0o300373 | 0 |
| `BUF_WRITE_0705` | LABEL(md) | `include/LO_GEN.labels.md:512`, `include/LO_GEN.labels.md:1325` | 0o300405 | 0 |
| `BUF_WRITE_0742` | LABEL(md) | `include/LO_GEN.labels.md:541` | 0o300442 | 0 |
| `BUF_WRITE_0746` | LABEL(md) | `include/LO_GEN.labels.md:545` | 0o300446 | 0 |
| `BUF_WRITE_0756` | LABEL(md) | `include/LO_GEN.labels.md:553` | 0o300456 | 0 |
| `BUF_WRITE_0773` | LABEL(md) | `include/LO_GEN.labels.md:566` | 0o300473 | 0 |
| `BUF_WRITE_1010` | LABEL(md) | `include/LO_GEN.labels.md:579` | 0o300510 | 0 |
| `BUF_WRITE_1014` | LABEL(md) | `include/LO_GEN.labels.md:583` | 0o300514 | 0 |
| `BUF_WRITE_1026` | LABEL(md) | `include/LO_GEN.labels.md:593` | 0o300526 | 0 |
| `BUF_WRITE_1027` | LABEL(md) | `include/LO_GEN.labels.md:594` | 0o300527 | 0 |
| `BUF_WRITE_1033` | LABEL(md) | `include/LO_GEN.labels.md:598` | 0o300533 | 0 |
| `BUF_WRITE_1036` | LABEL(md) | `include/LO_GEN.labels.md:601` | 0o300536 | 0 |
| `BUF_WRITE_1054` | LABEL(md) | `include/LO_GEN.labels.md:615` | 0o300554 | 0 |
| `BUF_WRITE_1057` | LABEL(md) | `include/LO_GEN.labels.md:618` | 0o300557 | 0 |
| `BUF_WRITE_1065` | LABEL(md) | `include/LO_GEN.labels.md:624` | 0o300565 | 0 |
| `BUF_WRITE_1073` | LABEL(md) | `include/LO_GEN.labels.md:630` | 0o300573 | 0 |
| `BUF_WRITE_1114` | LABEL(md) | `include/LO_GEN.labels.md:647` | 0o300614 | 0 |
| `BUF_WRITE_1206` | LABEL(md) | `include/LO_GEN.labels.md:705` | 0o300706 | 0 |
| `BUF_WRITE_1212` | LABEL(md) | `include/LO_GEN.labels.md:709` | 0o300712 | 0 |
| `BUF_WRITE_1221` | LABEL(md) | `include/LO_GEN.labels.md:716` | 0o300721 | 0 |
| `BUF_WRITE_1251` | LABEL(md) | `include/LO_GEN.labels.md:740`, `include/LO_GEN.labels.md:1137` | 0o300751 | 0 |
| `BUF_WRITE_1277` | LABEL(md) | `include/LO_GEN.labels.md:762` | 0o300777 | 0 |
| `BUF_WRITE_1311` | LABEL(md) | `include/LO_GEN.labels.md:772` | 0o301011 | 0 |
| `BUF_WRITE_1323` | LABEL(md) | `include/LO_GEN.labels.md:782` | 0o301023 | 0 |
| `BUF_WRITE_1333` | LABEL(md) | `include/LO_GEN.labels.md:790` | 0o301033 | 0 |
| `BUF_WRITE_1351` | LABEL(md) | `include/LO_GEN.labels.md:804` | 0o301051 | 0 |
| `BUF_WRITE_1353` | LABEL(md) | `include/LO_GEN.labels.md:806` | 0o301053 | 0 |
| `BUF_WRITE_1365` | LABEL(md) | `include/LO_GEN.labels.md:816` | 0o301065 | 0 |
| `BUF_WRITE_1377` | LABEL(md) | `include/LO_GEN.labels.md:826` | 0o301077 | 0 |
| `BUF_WRITE_1411` | LABEL(md) | `include/LO_GEN.labels.md:836` | 0o301111 | 0 |
| `BUF_WRITE_1423` | LABEL(md) | `include/LO_GEN.labels.md:846` | 0o301123 | 0 |
| `BUF_WRITE_1434` | LABEL(md) | `include/LO_GEN.labels.md:855` | 0o301134 | 0 |
| `BUF_WRITE_1440` | LABEL(md) | `include/LO_GEN.labels.md:859` | 0o301140 | 0 |
| `BUF_WRITE_1445` | LABEL(md) | `include/LO_GEN.labels.md:864` | 0o301145 | 0 |
| `BUF_WRITE_1450` | LABEL(md) | `include/LO_GEN.labels.md:867` | 0o301150 | 0 |
| `BUF_WRITE_1512` | LABEL(md) | `include/LO_GEN.labels.md:901` | 0o301212 | 0 |
| `BUF_WRITE_1520` | LABEL(md) | `include/LO_GEN.labels.md:907` | 0o301220 | 0 |
| `BUF_WRITE_1533` | LABEL(md) | `include/LO_GEN.labels.md:918` | 0o301233 | 0 |
| `BUF_WRITE_1543` | LABEL(md) | `include/LO_GEN.labels.md:926` | 0o301243 | 0 |
| `BUF_WRITE_1547` | LABEL(md) | `include/LO_GEN.labels.md:930` | 0o301247 | 0 |
| `BUF_WRITE_1556` | LABEL(md) | `include/LO_GEN.labels.md:937` | 0o301256 | 0 |
| `BUF_WRITE_1561` | LABEL(md) | `include/LO_GEN.labels.md:940` | 0o301261 | 0 |
| `BUF_WRITE_1570` | LABEL(md) | `include/LO_GEN.labels.md:947` | 0o301270 | 0 |
| `BUF_WRITE_1604` | LABEL(md) | `include/LO_GEN.labels.md:959` | 0o301304 | 0 |
| `BUF_WRITE_1624` | LABEL(md) | `include/LO_GEN.labels.md:975` | 0o301324 | 0 |
| `BUF_WRITE_1636` | LABEL(md) | `include/LO_GEN.labels.md:985`, `include/LO_GEN.labels.md:1137` | 0o301336 | 0 |
| `BUF_WRITE_1650` | LABEL(md) | `include/LO_GEN.labels.md:995` | 0o301350 | 0 |
| `BUF_WRITE_1653` | LABEL(md) | `include/LO_GEN.labels.md:998` | 0o301353 | 0 |
| `BUF_WRITE_1654` | LABEL(md) | `include/LO_GEN.labels.md:999` | 0o301354 | 0 |
| `BUF_WRITE_1662` | LABEL(md) | `include/LO_GEN.labels.md:1005` | 0o301362 | 0 |
| `BUF_WRITE_1671` | LABEL(md) | `include/LO_GEN.labels.md:1012` | 0o301371 | 0 |
| `BUF_WRITE_1676` | LABEL(md) | `include/LO_GEN.labels.md:1017` | 0o301376 | 0 |
| `BUF_WRITE_1677` | LABEL(md) | `include/LO_GEN.labels.md:1018` | 0o301377 | 0 |
| `BUF_WRITE_1700` | LABEL(md) | `include/LO_GEN.labels.md:1019` | 0o301400 | 0 |
| `BUF_WRITE_1701` | LABEL(md) | `include/LO_GEN.labels.md:1020`, `include/LO_GEN.labels.md:1095` | 0o301401 | 0 |
| `BUF_WRITE_1702` | LABEL(md) | `include/LO_GEN.labels.md:1021` | 0o301402 | 0 |
| `BUF_WRITE_1711` | LABEL(md) | `include/LO_GEN.labels.md:1028` | 0o301411 | 0 |
| `BUF_WRITE_1721` | LABEL(md) | `include/LO_GEN.labels.md:1036`, `include/LO_GEN.labels.md:1132` | 0o301421 | 0 |
| `BUF_WRITE_1727` | LABEL(md) | `include/LO_GEN.labels.md:1042` | 0o301427 | 0 |
| `BUF_WRITE_1741` | LABEL(md) | `include/LO_GEN.labels.md:1052` | 0o301441 | 0 |
| `BUF_WRITE_1746` | LABEL(md) | `include/LO_GEN.labels.md:1057` | 0o301446 | 0 |
| `BUF_WRITE_1765` | LABEL(md) | `include/LO_GEN.labels.md:1072` | 0o301465 | 0 |
| `BUF_WRITE_1766` | LABEL(md) | `include/LO_GEN.labels.md:1073` | 0o301466 | 0 |
| `C1/10` | LABEL | `src/FOREX_RUNTIME.mad:514` | — | 0 |
| `COMEQ` | LABEL(md)/SUBP | `include/FOREX_ROOT.mad:75`, `include/FOREX.labels.md:358` | — | 0 |
| `COMMON` | LABEL(md) | `include/LO_GEN.labels.md:1550` | 0o4000 | 0 |
| `CONST` | LABEL(md)/SUBP | `include/FOREX_ROOT.mad:74`, `include/FOREX.labels.md:358` | — | 0 |
| `DARET` | LABEL(md) | `include/FOREX.labels.md:60` | — | 0 |
| `DATAPR` | LABEL(md) | `include/FOREX.labels.md:7`, `include/FOREX.labels.md:58`, `include/FOREX.labels.md:358` | — | 0 |
| `DATAPR*` | SUBP | `src/LO_SYN.mad:25` | — | 0 |
| `DATA_0035` | LABEL(md) | `include/LO_GEN.labels.md:88`, `include/LO_GEN.labels.md:1227`, `include/LO_GEN.labels.md:1314` | 0o277535 | 0 |
| `DATA_0036` | LABEL(md) | `include/LO_GEN.labels.md:89`, `include/LO_GEN.labels.md:1212`, `include/LO_GEN.labels.md:1314` | 0o277536 | 0 |
| `DATA_0041` | LABEL(md) | `include/LO_GEN.labels.md:92`, `include/LO_GEN.labels.md:1313` | 0o277541 | 0 |
| `DATA_0043` | LABEL(md) | `include/LO_GEN.labels.md:94`, `include/LO_GEN.labels.md:1286`, `include/LO_GEN.labels.md:1315` | 0o277543 | 0 |
| `DATA_0045` | LABEL(md) | `include/LO_GEN.labels.md:96`, `include/LO_GEN.labels.md:1285`, `include/LO_GEN.labels.md:1315` | 0o277545 | 0 |
| `DATA_0047` | LABEL(md) | `include/LO_GEN.labels.md:98`, `include/LO_GEN.labels.md:1218` | 0o277547 | 0 |
| `DATA_0050` | LABEL(md) | `include/LO_GEN.labels.md:99`, `include/LO_GEN.labels.md:1225`, `include/LO_GEN.labels.md:1307` | 0o277550 | 0 |
| `DATA_0052` | LABEL(md) | `include/LO_GEN.labels.md:101`, `include/LO_GEN.labels.md:1224`, `include/LO_GEN.labels.md:1306` | 0o277552 | 0 |
| `DATA_0056` | LABEL(md) | `include/LO_GEN.labels.md:105`, `include/LO_GEN.labels.md:1216` | 0o277556 | 0 |
| `DATA_0140` | LABEL(md) | `include/LO_GEN.labels.md:155`, `include/LO_GEN.labels.md:1113`, `include/LO_GEN.labels.md:1317` | 0o277640 | 0 |
| `DATA_0141` | LABEL(md) | `include/LO_GEN.labels.md:156`, `include/LO_GEN.labels.md:1095`, `include/LO_GEN.labels.md:1307` | 0o277641 | 0 |
| `DATA_0143` | LABEL(md) | `include/LO_GEN.labels.md:158`, `include/LO_GEN.labels.md:1108`, `include/LO_GEN.labels.md:1307` | 0o277643 | 0 |
| `DATA_0203` | LABEL(md) | `include/LO_GEN.labels.md:190`, `include/LO_GEN.labels.md:1159` | 0o277703 | 0 |
| `DATA_0254` | LABEL(md) | `include/LO_GEN.labels.md:231`, `include/LO_GEN.labels.md:1113` | 0o277754 | 0 |
| `DATA_0263` | LABEL(md) | `include/LO_GEN.labels.md:238`, `include/LO_GEN.labels.md:1113`, `include/LO_GEN.labels.md:1318` | 0o277763 | 0 |
| `DATA_0320` | LABEL(md) | `include/LO_GEN.labels.md:267`, `include/LO_GEN.labels.md:1108` | 0o300020 | 0 |
| `DATA_0747` | LABEL(md) | `include/LO_GEN.labels.md:546` | 0o300447 | 0 |
| `DATA_1060` | LABEL(md) | `include/LO_GEN.labels.md:619` | 0o300560 | 0 |
| `DATA_1121` | LABEL(md) | `include/LO_GEN.labels.md:652` | 0o300621 | 0 |
| `DATA_1336` | LABEL(md) | `include/LO_GEN.labels.md:793`, `include/LO_GEN.labels.md:1134` | 0o301036 | 0 |
| `DATA_1420` | LABEL(md) | `include/LO_GEN.labels.md:843` | 0o301120 | 0 |
| `DATA_1513` | LABEL(md) | `include/LO_GEN.labels.md:902`, `include/LO_GEN.labels.md:1095` | 0o301213 | 0 |
| `DATA_1526` | LABEL(md) | `include/LO_GEN.labels.md:913`, `include/LO_GEN.labels.md:1149` | 0o301226 | 0 |
| `DATA_1573` | LABEL(md) | `include/LO_GEN.labels.md:950` | 0o301273 | 0 |
| `DATA_1646` | LABEL(md) | `include/LO_GEN.labels.md:993` | 0o301346 | 0 |
| `DATA_1737` | LABEL(md) | `include/LO_GEN.labels.md:1050` | 0o301437 | 0 |
| `DATA_1763` | LABEL(md) | `include/LO_GEN.labels.md:1070` | 0o301463 | 0 |
| `DATE` | LABEL(md) | `include/FOREX.labels.md:59` | — | 0 |
| `DATE_PREPARE` | ENTRY/LABEL(md) | `src/FOREX_RUNTIME.mad:389`, `include/FOREX.labels.md:63` | — | 0 |
| `DEC_15` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:26`, `include/FOREX.labels.md:314` | 15 | 0 |
| `DIV_0007` | LABEL(md) | `include/LO_GEN.labels.md:66`, `include/LO_GEN.labels.md:1177` | 0o277507 | 0 |
| `DUMON` | LABEL(md) | `include/FOREX.labels.md:8`, `include/FOREX.labels.md:358`, `include/LO_GEN.labels.md:28`, `include/LO_GEN.labels.md:1551` | — | 0 |
| `EQU` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `ERR_TRANSLATOR` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:311`, `include/FOREX_ROOT.mad:134`, `include/FOREX.labels.md:31`, `include/FOREX.labels.md:82` | — | 0 |
| `EXT_` | LABEL(md) | `include/LO_SYN.labels.md:43` | — | 0 |
| `FL*SAV` | LABEL(md) | `include/FOREX.labels.md:88` | — | 0 |
| `FOREX` | LABEL(md)/SUBP | `src/LO_SYN.mad:29`, `include/FOREX_ROOT.mad:73`, `include/FOREX.labels.md:358` | — | 0 |
| `FOREX*` | NAME | `include/FOREX_ROOT.mad:61` | — | 0 |
| `FOREX_CORE` | LABEL(md)/NAME | `src/FOREX_CORE.mad:145`, `include/FOREX.labels.md:19`, `include/FOREX.labels.md:19` | NEW DTRAN | 0 |
| `FOREX_START` | ENTRY/LABEL(md) | `src/FOREX_CORE.mad:146`, `include/FOREX.labels.md:20` | — | 0 |
| `FORMAT` | LABEL(md) | `include/FOREX.labels.md:38` | — | 0 |
| `FORTLIBR` | LABEL(md) | `include/FOREX.labels.md:45` | — | 0 |
| `FT_FORMAT_DISPATCH` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:120`, `include/FOREX.labels.md:38` | — | 0 |
| `FT_LIBRARY_IO` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:193`, `include/FOREX.labels.md:45` | — | 0 |
| `GOST` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `HEADER_0000` | LABEL/LABEL(md) | `src/LO_GEN.mad:541`, `include/LO_GEN.labels.md:59`, `include/LO_GEN.labels.md:1291` | — | 0 |
| `HEADER_0001` | LABEL/LABEL(md) | `src/LO_GEN.mad:543`, `include/LO_GEN.labels.md:29`, `include/LO_GEN.labels.md:60`, `include/LO_GEN.labels.md:1292` | — | 0 |
| `HEADER_0002` | LABEL/LABEL(md) | `src/LO_GEN.mad:545`, `include/LO_GEN.labels.md:61`, `include/LO_GEN.labels.md:1294` | — | 0 |
| `HEADER_0003` | LABEL/LABEL(md) | `src/LO_GEN.mad:547`, `include/LO_GEN.labels.md:62`, `include/LO_GEN.labels.md:1293` | — | 0 |
| `INITFOR` | LABEL(md) | `include/FOREX.labels.md:7`, `include/FOREX.labels.md:26`, `include/FOREX.labels.md:77` | — | 0 |
| `INIT_FOREX` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:191`, `include/FOREX_ROOT.mad:79`, `include/FOREX.labels.md:26`, `include/FOREX.labels.md:77` | — | 0 |
| `ISO` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `JUMP_0030` | LABEL(md) | `include/LO_GEN.labels.md:83`, `include/LO_GEN.labels.md:1316`, `include/LO_GEN.labels.md:1538` | 0o277530 | 0 |
| `JUMP_0034` | LABEL(md) | `include/LO_GEN.labels.md:87`, `include/LO_GEN.labels.md:1316`, `include/LO_GEN.labels.md:1397` | 0o277534 | 0 |
| `JUMP_0046` | LABEL(md) | `include/LO_GEN.labels.md:97`, `include/LO_GEN.labels.md:1398` | 0o277546 | 0 |
| `JUMP_0101` | LABEL(md) | `include/LO_GEN.labels.md:124` | 0o277601 | 0 |
| `JUMP_0115` | LABEL(md) | `include/LO_GEN.labels.md:136`, `include/LO_GEN.labels.md:1539` | 0o277615 | 0 |
| `JUMP_0133` | LABEL(md) | `include/LO_GEN.labels.md:150`, `include/LO_GEN.labels.md:1539` | 0o277633 | 0 |
| `JUMP_0205` | LABEL(md) | `include/LO_GEN.labels.md:192` | 0o277705 | 0 |
| `JUMP_0224` | LABEL(md) | `include/LO_GEN.labels.md:207` | 0o277724 | 0 |
| `JUMP_0231` | LABEL(md) | `include/LO_GEN.labels.md:212` | 0o277731 | 0 |
| `JUMP_0244` | LABEL(md) | `include/LO_GEN.labels.md:223` | 0o277744 | 0 |
| `JUMP_0253` | LABEL(md) | `include/LO_GEN.labels.md:230`, `include/LO_GEN.labels.md:1419` | 0o277753 | 0 |
| `JUMP_0261` | LABEL(md) | `include/LO_GEN.labels.md:236`, `include/LO_GEN.labels.md:1418` | 0o277761 | 0 |
| `JUMP_0301` | LABEL(md) | `include/LO_GEN.labels.md:252` | 0o300001 | 0 |
| `JUMP_0307` | LABEL(md) | `include/LO_GEN.labels.md:258`, `include/LO_GEN.labels.md:1426` | 0o300007 | 0 |
| `JUMP_0321` | LABEL(md) | `include/LO_GEN.labels.md:268`, `include/LO_GEN.labels.md:1425` | 0o300021 | 0 |
| `JUMP_0340` | LABEL(md) | `include/LO_GEN.labels.md:283` | 0o300040 | 0 |
| `JUMP_0342` | LABEL(md) | `include/LO_GEN.labels.md:285` | 0o300042 | 0 |
| `JUMP_0350` | LABEL(md) | `include/LO_GEN.labels.md:291` | 0o300050 | 0 |
| `JUMP_0354` | LABEL(md) | `include/LO_GEN.labels.md:295` | 0o300054 | 0 |
| `JUMP_0367` | LABEL(md) | `include/LO_GEN.labels.md:306` | 0o300067 | 0 |
| `JUMP_0371` | LABEL(md) | `include/LO_GEN.labels.md:308`, `include/LO_GEN.labels.md:1400` | 0o300071 | 0 |
| `JUMP_0372` | LABEL(md) | `include/LO_GEN.labels.md:309`, `include/LO_GEN.labels.md:1402` | 0o300072 | 0 |
| `JUMP_0373` | LABEL(md) | `include/LO_GEN.labels.md:310`, `include/LO_GEN.labels.md:1404` | 0o300073 | 0 |
| `JUMP_0374` | LABEL(md) | `include/LO_GEN.labels.md:311`, `include/LO_GEN.labels.md:1408` | 0o300074 | 0 |
| `JUMP_0375` | LABEL(md) | `include/LO_GEN.labels.md:312`, `include/LO_GEN.labels.md:1411` | 0o300075 | 0 |
| `JUMP_0376` | LABEL(md) | `include/LO_GEN.labels.md:313`, `include/LO_GEN.labels.md:1421` | 0o300076 | 0 |
| `JUMP_0377` | LABEL(md) | `include/LO_GEN.labels.md:314`, `include/LO_GEN.labels.md:1538` | 0o300077 | 0 |
| `JUMP_0400` | LABEL(md) | `include/LO_GEN.labels.md:315`, `include/LO_GEN.labels.md:1538` | 0o300100 | 0 |
| `JUMP_0401` | LABEL(md) | `include/LO_GEN.labels.md:316`, `include/LO_GEN.labels.md:1412` | 0o300101 | 0 |
| `JUMP_0402` | LABEL(md) | `include/LO_GEN.labels.md:317`, `include/LO_GEN.labels.md:1429` | 0o300102 | 0 |
| `JUMP_0403` | LABEL(md) | `include/LO_GEN.labels.md:318`, `include/LO_GEN.labels.md:1430` | 0o300103 | 0 |
| `JUMP_0404` | LABEL(md) | `include/LO_GEN.labels.md:319` | 0o300104 | 0 |
| `JUMP_0405` | LABEL(md) | `include/LO_GEN.labels.md:320` | 0o300105 | 0 |
| `JUMP_0406` | LABEL(md) | `include/LO_GEN.labels.md:321`, `include/LO_GEN.labels.md:1437` | 0o300106 | 0 |
| `JUMP_0407` | LABEL(md) | `include/LO_GEN.labels.md:322`, `include/LO_GEN.labels.md:1443` | 0o300107 | 0 |
| `JUMP_0410` | LABEL(md) | `include/LO_GEN.labels.md:323`, `include/LO_GEN.labels.md:1444` | 0o300110 | 0 |
| `JUMP_0415` | LABEL(md) | `include/LO_GEN.labels.md:328`, `include/LO_GEN.labels.md:1431` | 0o300115 | 0 |
| `JUMP_0416` | LABEL(md) | `include/LO_GEN.labels.md:329`, `include/LO_GEN.labels.md:1435` | 0o300116 | 0 |
| `JUMP_0417` | LABEL(md) | `include/LO_GEN.labels.md:330`, `include/LO_GEN.labels.md:1434` | 0o300117 | 0 |
| `JUMP_0420` | LABEL(md) | `include/LO_GEN.labels.md:331`, `include/LO_GEN.labels.md:1449` | 0o300120 | 0 |
| `JUMP_0422` | LABEL(md) | `include/LO_GEN.labels.md:333`, `include/LO_GEN.labels.md:1450` | 0o300122 | 0 |
| `JUMP_0423` | LABEL(md) | `include/LO_GEN.labels.md:334`, `include/LO_GEN.labels.md:1451` | 0o300123 | 0 |
| `JUMP_0424` | LABEL(md) | `include/LO_GEN.labels.md:335`, `include/LO_GEN.labels.md:1452` | 0o300124 | 0 |
| `JUMP_0425` | LABEL(md) | `include/LO_GEN.labels.md:336`, `include/LO_GEN.labels.md:1473` | 0o300125 | 0 |
| `JUMP_0426` | LABEL(md) | `include/LO_GEN.labels.md:337`, `include/LO_GEN.labels.md:1474` | 0o300126 | 0 |
| `JUMP_0427` | LABEL(md) | `include/LO_GEN.labels.md:338`, `include/LO_GEN.labels.md:1453` | 0o300127 | 0 |
| `JUMP_0430` | LABEL(md) | `include/LO_GEN.labels.md:339`, `include/LO_GEN.labels.md:1459` | 0o300130 | 0 |
| `JUMP_0431` | LABEL(md) | `include/LO_GEN.labels.md:340`, `include/LO_GEN.labels.md:1454` | 0o300131 | 0 |
| `JUMP_0432` | LABEL(md) | `include/LO_GEN.labels.md:341`, `include/LO_GEN.labels.md:1455` | 0o300132 | 0 |
| `JUMP_0433` | LABEL(md) | `include/LO_GEN.labels.md:342`, `include/LO_GEN.labels.md:1457` | 0o300133 | 0 |
| `JUMP_0434` | LABEL(md) | `include/LO_GEN.labels.md:343`, `include/LO_GEN.labels.md:1438` | 0o300134 | 0 |
| `JUMP_0435` | LABEL(md) | `include/LO_GEN.labels.md:344`, `include/LO_GEN.labels.md:1469` | 0o300135 | 0 |
| `JUMP_0436` | LABEL(md) | `include/LO_GEN.labels.md:345`, `include/LO_GEN.labels.md:1466` | 0o300136 | 0 |
| `JUMP_0437` | LABEL(md) | `include/LO_GEN.labels.md:346`, `include/LO_GEN.labels.md:1460` | 0o300137 | 0 |
| `JUMP_0440` | LABEL(md) | `include/LO_GEN.labels.md:347`, `include/LO_GEN.labels.md:1470` | 0o300140 | 0 |
| `JUMP_0441` | LABEL(md) | `include/LO_GEN.labels.md:348`, `include/LO_GEN.labels.md:1467` | 0o300141 | 0 |
| `JUMP_0442` | LABEL(md) | `include/LO_GEN.labels.md:349`, `include/LO_GEN.labels.md:1461` | 0o300142 | 0 |
| `JUMP_0443` | LABEL(md) | `include/LO_GEN.labels.md:350`, `include/LO_GEN.labels.md:1461` | 0o300143 | 0 |
| `JUMP_0444` | LABEL(md) | `include/LO_GEN.labels.md:351`, `include/LO_GEN.labels.md:1460` | 0o300144 | 0 |
| `JUMP_0445` | LABEL(md) | `include/LO_GEN.labels.md:352`, `include/LO_GEN.labels.md:1477` | 0o300145 | 0 |
| `JUMP_0446` | LABEL(md) | `include/LO_GEN.labels.md:353`, `include/LO_GEN.labels.md:1483` | 0o300146 | 0 |
| `JUMP_0447` | LABEL(md) | `include/LO_GEN.labels.md:354`, `include/LO_GEN.labels.md:1485` | 0o300147 | 0 |
| `JUMP_0450` | LABEL(md) | `include/LO_GEN.labels.md:355`, `include/LO_GEN.labels.md:1479` | 0o300150 | 0 |
| `JUMP_0451` | LABEL(md) | `include/LO_GEN.labels.md:356`, `include/LO_GEN.labels.md:1486` | 0o300151 | 0 |
| `JUMP_0463` | LABEL(md) | `include/LO_GEN.labels.md:366`, `include/LO_GEN.labels.md:1505` | 0o300163 | 0 |
| `JUMP_0464` | LABEL(md) | `include/LO_GEN.labels.md:367`, `include/LO_GEN.labels.md:1458` | 0o300164 | 0 |
| `JUMP_0465` | LABEL(md) | `include/LO_GEN.labels.md:368` | 0o300165 | 0 |
| `JUMP_0466` | LABEL(md) | `include/LO_GEN.labels.md:369` | 0o300166 | 0 |
| `JUMP_0467` | LABEL(md) | `include/LO_GEN.labels.md:370`, `include/LO_GEN.labels.md:1506` | 0o300167 | 0 |
| `JUMP_0470` | LABEL(md) | `include/LO_GEN.labels.md:371`, `include/LO_GEN.labels.md:1507` | 0o300170 | 0 |
| `JUMP_0471` | LABEL(md) | `include/LO_GEN.labels.md:372`, `include/LO_GEN.labels.md:1510` | 0o300171 | 0 |
| `JUMP_0472` | LABEL(md) | `include/LO_GEN.labels.md:373` | 0o300172 | 0 |
| `JUMP_0473` | LABEL(md) | `include/LO_GEN.labels.md:374` | 0o300173 | 0 |
| `JUMP_0500` | LABEL(md) | `include/LO_GEN.labels.md:379`, `include/LO_GEN.labels.md:1521` | 0o300200 | 0 |
| `JUMP_0501` | LABEL(md) | `include/LO_GEN.labels.md:380`, `include/LO_GEN.labels.md:1522` | 0o300201 | 0 |
| `JUMP_0506` | LABEL(md) | `include/LO_GEN.labels.md:385`, `include/LO_GEN.labels.md:1429` | 0o300206 | 0 |
| `JUMP_0507` | LABEL(md) | `include/LO_GEN.labels.md:386`, `include/LO_GEN.labels.md:1513` | 0o300207 | 0 |
| `JUMP_0511` | LABEL(md) | `include/LO_GEN.labels.md:388`, `include/LO_GEN.labels.md:1429` | 0o300211 | 0 |
| `JUMP_0512` | LABEL(md) | `include/LO_GEN.labels.md:389`, `include/LO_GEN.labels.md:1513` | 0o300212 | 0 |
| `JUMP_0514` | LABEL(md) | `include/LO_GEN.labels.md:391`, `include/LO_GEN.labels.md:1515` | 0o300214 | 0 |
| `JUMP_0515` | LABEL(md) | `include/LO_GEN.labels.md:392`, `include/LO_GEN.labels.md:1516` | 0o300215 | 0 |
| `JUMP_0516` | LABEL(md) | `include/LO_GEN.labels.md:393`, `include/LO_GEN.labels.md:1527` | 0o300216 | 0 |
| `JUMP_0517` | LABEL(md) | `include/LO_GEN.labels.md:394`, `include/LO_GEN.labels.md:1525` | 0o300217 | 0 |
| `JUMP_0520` | LABEL(md) | `include/LO_GEN.labels.md:395`, `include/LO_GEN.labels.md:1526` | 0o300220 | 0 |
| `JUMP_0530` | LABEL(md) | `include/LO_GEN.labels.md:403`, `include/LO_GEN.labels.md:1480` | 0o300230 | 0 |
| `JUMP_0531` | LABEL(md) | `include/LO_GEN.labels.md:404`, `include/LO_GEN.labels.md:1482` | 0o300231 | 0 |
| `JUMP_0657` | LABEL(md) | `include/LO_GEN.labels.md:490` | 0o300357 | 0 |
| `JUMP_0666` | LABEL(md) | `include/LO_GEN.labels.md:497`, `include/LO_GEN.labels.md:1441` | 0o300366 | 0 |
| `JUMP_0670` | LABEL(md) | `include/LO_GEN.labels.md:499`, `include/LO_GEN.labels.md:1432` | 0o300370 | 0 |
| `JUMP_0703` | LABEL(md) | `include/LO_GEN.labels.md:510`, `include/LO_GEN.labels.md:1447` | 0o300403 | 0 |
| `JUMP_0713` | LABEL(md) | `include/LO_GEN.labels.md:518` | 0o300413 | 0 |
| `JUMP_0717` | LABEL(md) | `include/LO_GEN.labels.md:522` | 0o300417 | 0 |
| `JUMP_0721` | LABEL(md) | `include/LO_GEN.labels.md:524` | 0o300421 | 0 |
| `JUMP_0725` | LABEL(md) | `include/LO_GEN.labels.md:528` | 0o300425 | 0 |
| `JUMP_0731` | LABEL(md) | `include/LO_GEN.labels.md:532` | 0o300431 | 0 |
| `JUMP_0733` | LABEL(md) | `include/LO_GEN.labels.md:534` | 0o300433 | 0 |
| `JUMP_0751` | LABEL(md) | `include/LO_GEN.labels.md:548` | 0o300451 | 0 |
| `JUMP_1051` | LABEL(md) | `include/LO_GEN.labels.md:612` | 0o300551 | 0 |
| `JUMP_1061` | LABEL(md) | `include/LO_GEN.labels.md:620` | 0o300561 | 0 |
| `JUMP_1071` | LABEL(md) | `include/LO_GEN.labels.md:628` | 0o300571 | 0 |
| `JUMP_1100` | LABEL(md) | `include/LO_GEN.labels.md:635` | 0o300600 | 0 |
| `JUMP_1130` | LABEL(md) | `include/LO_GEN.labels.md:659` | 0o300630 | 0 |
| `JUMP_1141` | LABEL(md) | `include/LO_GEN.labels.md:668`, `include/LO_GEN.labels.md:1464` | 0o300641 | 0 |
| `JUMP_1151` | LABEL(md) | `include/LO_GEN.labels.md:676`, `include/LO_GEN.labels.md:1464` | 0o300651 | 0 |
| `JUMP_1153` | LABEL(md) | `include/LO_GEN.labels.md:678` | 0o300653 | 0 |
| `JUMP_1160` | LABEL(md) | `include/LO_GEN.labels.md:683` | 0o300660 | 0 |
| `JUMP_1163` | LABEL(md) | `include/LO_GEN.labels.md:686` | 0o300663 | 0 |
| `JUMP_1167` | LABEL(md) | `include/LO_GEN.labels.md:690` | 0o300667 | 0 |
| `JUMP_1171` | LABEL(md) | `include/LO_GEN.labels.md:692`, `include/LO_GEN.labels.md:1478` | 0o300671 | 0 |
| `JUMP_1174` | LABEL(md) | `include/LO_GEN.labels.md:695` | 0o300674 | 0 |
| `JUMP_1176` | LABEL(md) | `include/LO_GEN.labels.md:697`, `include/LO_GEN.labels.md:1481` | 0o300676 | 0 |
| `JUMP_1214` | LABEL(md) | `include/LO_GEN.labels.md:711` | 0o300714 | 0 |
| `JUMP_1216` | LABEL(md) | `include/LO_GEN.labels.md:713` | 0o300716 | 0 |
| `JUMP_1232` | LABEL(md) | `include/LO_GEN.labels.md:725`, `include/LO_GEN.labels.md:1492` | 0o300732 | 0 |
| `JUMP_1235` | LABEL(md) | `include/LO_GEN.labels.md:728`, `include/LO_GEN.labels.md:1492` | 0o300735 | 0 |
| `JUMP_1242` | LABEL(md) | `include/LO_GEN.labels.md:733`, `include/LO_GEN.labels.md:1492` | 0o300742 | 0 |
| `JUMP_1245` | LABEL(md) | `include/LO_GEN.labels.md:736` | 0o300745 | 0 |
| `JUMP_1256` | LABEL(md) | `include/LO_GEN.labels.md:745`, `include/LO_GEN.labels.md:1496` | 0o300756 | 0 |
| `JUMP_1261` | LABEL(md) | `include/LO_GEN.labels.md:748`, `include/LO_GEN.labels.md:1496` | 0o300761 | 0 |
| `JUMP_1324` | LABEL(md) | `include/LO_GEN.labels.md:783` | 0o301024 | 0 |
| `JUMP_1326` | LABEL(md) | `include/LO_GEN.labels.md:785`, `include/LO_GEN.labels.md:1503` | 0o301026 | 0 |
| `JUMP_1330` | LABEL(md) | `include/LO_GEN.labels.md:787`, `include/LO_GEN.labels.md:1503` | 0o301030 | 0 |
| `JUMP_1340` | LABEL(md) | `include/LO_GEN.labels.md:795`, `include/LO_GEN.labels.md:1498` | 0o301040 | 0 |
| `JUMP_1342` | LABEL(md) | `include/LO_GEN.labels.md:797` | 0o301042 | 0 |
| `JUMP_1344` | LABEL(md) | `include/LO_GEN.labels.md:799` | 0o301044 | 0 |
| `JUMP_1412` | LABEL(md) | `include/LO_GEN.labels.md:837` | 0o301112 | 0 |
| `JUMP_1416` | LABEL(md) | `include/LO_GEN.labels.md:841`, `include/LO_GEN.labels.md:1508` | 0o301116 | 0 |
| `JUMP_1425` | LABEL(md) | `include/LO_GEN.labels.md:848` | 0o301125 | 0 |
| `JUMP_1454` | LABEL(md) | `include/LO_GEN.labels.md:871` | 0o301154 | 0 |
| `JUMP_1456` | LABEL(md) | `include/LO_GEN.labels.md:873` | 0o301156 | 0 |
| `JUMP_1460` | LABEL(md) | `include/LO_GEN.labels.md:875` | 0o301160 | 0 |
| `JUMP_1462` | LABEL(md) | `include/LO_GEN.labels.md:877` | 0o301162 | 0 |
| `JUMP_1464` | LABEL(md) | `include/LO_GEN.labels.md:879` | 0o301164 | 0 |
| `JUMP_1466` | LABEL(md) | `include/LO_GEN.labels.md:881` | 0o301166 | 0 |
| `JUMP_1470` | LABEL(md) | `include/LO_GEN.labels.md:883` | 0o301170 | 0 |
| `JUMP_1475` | LABEL(md) | `include/LO_GEN.labels.md:888`, `include/LO_GEN.labels.md:1487` | 0o301175 | 0 |
| `JUMP_1477` | LABEL(md) | `include/LO_GEN.labels.md:890` | 0o301177 | 0 |
| `JUMP_1501` | LABEL(md) | `include/LO_GEN.labels.md:892` | 0o301201 | 0 |
| `JUMP_1503` | LABEL(md) | `include/LO_GEN.labels.md:894` | 0o301203 | 0 |
| `JUMP_1514` | LABEL(md) | `include/LO_GEN.labels.md:903` | 0o301214 | 0 |
| `JUMP_1571` | LABEL(md) | `include/LO_GEN.labels.md:948` | 0o301271 | 0 |
| `JUMP_1610` | LABEL(md) | `include/LO_GEN.labels.md:963`, `include/LO_GEN.labels.md:1519` | 0o301310 | 0 |
| `JUMP_1617` | LABEL(md) | `include/LO_GEN.labels.md:970`, `include/LO_GEN.labels.md:1093` | 0o301317 | 0 |
| `JUMP_1641` | LABEL(md) | `include/LO_GEN.labels.md:988` | 0o301341 | 0 |
| `JUMP_1643` | LABEL(md) | `include/LO_GEN.labels.md:990`, `include/LO_GEN.labels.md:1524` | 0o301343 | 0 |
| `JUMP_1645` | LABEL(md) | `include/LO_GEN.labels.md:992`, `include/LO_GEN.labels.md:1524` | 0o301345 | 0 |
| `JUMP_1656` | LABEL(md) | `include/LO_GEN.labels.md:1001` | 0o301356 | 0 |
| `JUMP_1660` | LABEL(md) | `include/LO_GEN.labels.md:1003` | 0o301360 | 0 |
| `JUMP_1665` | LABEL(md) | `include/LO_GEN.labels.md:1008` | 0o301365 | 0 |
| `JUMP_1672` | LABEL(md) | `include/LO_GEN.labels.md:1013`, `include/LO_GEN.labels.md:1530` | 0o301372 | 0 |
| `JUMP_1714` | LABEL(md) | `include/LO_GEN.labels.md:1031` | 0o301414 | 0 |
| `JUMP_1725` | LABEL(md) | `include/LO_GEN.labels.md:1040` | 0o301425 | 0 |
| `JUMP_1762` | LABEL(md) | `include/LO_GEN.labels.md:1069` | 0o301462 | 0 |
| `JUMP_1774` | LABEL(md) | `include/LO_GEN.labels.md:1079`, `include/LO_GEN.labels.md:1542` | 0o301474 | 0 |
| `KCOUNT*` | COMMON | `include/FOREX_ROOT.mad:240` | ONE_WORD | 0 |
| `L` | LABEL | `src/FOREX_RUNTIME.mad:199`, `src/FOREX_RUNTIME.mad:203`, `src/FOREX_RUNTIME.mad:204`, `src/FOREX_RUNTIME.mad:208`, `src/FOREX_RUNTIME.mad:230`, `src/FOREX_RUNTIME.mad:234` … (+26) | — | 0 |
| `L*00023` | LABEL | `src/FOREX_RUNTIME.mad:239` | — | 0 |
| `L*00027` | LABEL | `src/FOREX_RUNTIME.mad:248` | — | 0 |
| `L*00042` | LABEL | `src/FOREX_RUNTIME.mad:270` | — | 0 |
| `L*00045` | LABEL | `src/FOREX_RUNTIME.mad:276` | — | 0 |
| `L*00050` | LABEL | `src/FOREX_RUNTIME.mad:282` | — | 0 |
| `L*00053` | LABEL | `src/FOREX_RUNTIME.mad:288` | — | 0 |
| `L0021` | LABEL(md) | `include/LO_SYN.labels.md:10` | — | 0 |
| `L0315` | LABEL(md) | `include/LO_SYN.labels.md:11` | — | 0 |
| `L0316` | LABEL(md) | `include/LO_SYN.labels.md:12` | — | 0 |
| `L0500` | LABEL(md) | `include/LO_SYN.labels.md:13` | — | 0 |
| `L0507` | LABEL(md) | `include/LO_SYN.labels.md:14` | — | 0 |
| `L0511` | LABEL(md) | `include/LO_SYN.labels.md:15` | — | 0 |
| `L1001` | LABEL(md) | `include/LO_SYN.labels.md:16` | — | 0 |
| `L1003` | LABEL(md) | `include/LO_SYN.labels.md:17` | — | 0 |
| `L1005` | LABEL(md) | `include/LO_SYN.labels.md:18` | — | 0 |
| `L1030` | LABEL(md) | `include/LO_SYN.labels.md:19` | — | 0 |
| `L1031` | LABEL(md) | `include/LO_SYN.labels.md:20` | — | 0 |
| `L1032` | LABEL(md) | `include/LO_SYN.labels.md:21` | — | 0 |
| `L1112` | LABEL(md) | `include/LO_SYN.labels.md:22` | — | 0 |
| `L1113` | LABEL(md) | `include/LO_SYN.labels.md:23` | — | 0 |
| `L1201` | LABEL(md) | `include/LO_SYN.labels.md:24` | — | 0 |
| `L1304` | LABEL(md) | `include/LO_SYN.labels.md:25` | — | 0 |
| `L1317` | LABEL(md) | `include/LO_SYN.labels.md:26` | — | 0 |
| `L1321` | LABEL(md) | `include/LO_SYN.labels.md:27` | — | 0 |
| `L1327` | LABEL(md) | `include/LO_SYN.labels.md:28` | — | 0 |
| `L1330` | LABEL(md) | `include/LO_SYN.labels.md:29` | — | 0 |
| `L1331` | LABEL(md) | `include/LO_SYN.labels.md:30` | — | 0 |
| `L1400` | LABEL(md) | `include/LO_SYN.labels.md:31` | — | 0 |
| `L1410` | LABEL(md) | `include/LO_SYN.labels.md:32` | — | 0 |
| `L1427` | LABEL(md) | `include/LO_SYN.labels.md:33` | — | 0 |
| `L1430` | LABEL(md) | `include/LO_SYN.labels.md:34` | — | 0 |
| `LC` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `LOAD_0006` | LABEL(md) | `include/LO_GEN.labels.md:65`, `include/LO_GEN.labels.md:1288` | 0o277506 | 0 |
| `LOAD_0073` | LABEL(md) | `include/LO_GEN.labels.md:118`, `include/LO_GEN.labels.md:1325` | 0o277573 | 0 |
| `LOAD_0076` | LABEL(md) | `include/LO_GEN.labels.md:121`, `include/LO_GEN.labels.md:1322` | 0o277576 | 0 |
| `LOAD_0100` | LABEL(md) | `include/LO_GEN.labels.md:123`, `include/LO_GEN.labels.md:1325` | 0o277600 | 0 |
| `LOAD_0102` | LABEL(md) | `include/LO_GEN.labels.md:125`, `include/LO_GEN.labels.md:1323` | 0o277602 | 0 |
| `LOAD_0126` | LABEL(md) | `include/LO_GEN.labels.md:145`, `include/LO_GEN.labels.md:1318` | 0o277626 | 0 |
| `LOAD_0130` | LABEL(md) | `include/LO_GEN.labels.md:147`, `include/LO_GEN.labels.md:1108` | 0o277630 | 0 |
| `LOAD_0131` | LABEL(md) | `include/LO_GEN.labels.md:148`, `include/LO_GEN.labels.md:1398` | 0o277631 | 0 |
| `LOAD_0135` | LABEL(md) | `include/LO_GEN.labels.md:152` | 0o277635 | 0 |
| `LOAD_0146` | LABEL(md) | `include/LO_GEN.labels.md:161`, `include/LO_GEN.labels.md:1322` | 0o277646 | 0 |
| `LOAD_0154` | LABEL(md) | `include/LO_GEN.labels.md:167`, `include/LO_GEN.labels.md:1306` | 0o277654 | 0 |
| `LOAD_0156` | LABEL(md) | `include/LO_GEN.labels.md:169` | 0o277656 | 0 |
| `LOAD_0162` | LABEL(md) | `include/LO_GEN.labels.md:173` | 0o277662 | 0 |
| `LOAD_0167` | LABEL(md) | `include/LO_GEN.labels.md:178` | 0o277667 | 0 |
| `LOAD_0171` | LABEL(md) | `include/LO_GEN.labels.md:180` | 0o277671 | 0 |
| `LOAD_0174` | LABEL(md) | `include/LO_GEN.labels.md:183`, `include/LO_GEN.labels.md:1157` | 0o277674 | 0 |
| `LOAD_0177` | LABEL(md) | `include/LO_GEN.labels.md:186` | 0o277677 | 0 |
| `LOAD_0202` | LABEL(md) | `include/LO_GEN.labels.md:189` | 0o277702 | 0 |
| `LOAD_0210` | LABEL(md) | `include/LO_GEN.labels.md:195`, `include/LO_GEN.labels.md:1318` | 0o277710 | 0 |
| `LOAD_0217` | LABEL(md) | `include/LO_GEN.labels.md:202` | 0o277717 | 0 |
| `LOAD_0221` | LABEL(md) | `include/LO_GEN.labels.md:204`, `include/LO_GEN.labels.md:1216` | 0o277721 | 0 |
| `LOAD_0232` | LABEL(md) | `include/LO_GEN.labels.md:213` | 0o277732 | 0 |
| `LOAD_0233` | LABEL(md) | `include/LO_GEN.labels.md:214` | 0o277733 | 0 |
| `LOAD_0236` | LABEL(md) | `include/LO_GEN.labels.md:217` | 0o277736 | 0 |
| `LOAD_0237` | LABEL(md) | `include/LO_GEN.labels.md:218` | 0o277737 | 0 |
| `LOAD_0240` | LABEL(md) | `include/LO_GEN.labels.md:219` | 0o277740 | 0 |
| `LOAD_0241` | LABEL(md) | `include/LO_GEN.labels.md:220` | 0o277741 | 0 |
| `LOAD_0242` | LABEL(md) | `include/LO_GEN.labels.md:221`, `include/LO_GEN.labels.md:1163` | 0o277742 | 0 |
| `LOAD_0245` | LABEL(md) | `include/LO_GEN.labels.md:224` | 0o277745 | 0 |
| `LOAD_0247` | LABEL(md) | `include/LO_GEN.labels.md:226`, `include/LO_GEN.labels.md:1321` | 0o277747 | 0 |
| `LOAD_0252` | LABEL(md) | `include/LO_GEN.labels.md:229`, `include/LO_GEN.labels.md:1167` | 0o277752 | 0 |
| `LOAD_0265` | LABEL(md) | `include/LO_GEN.labels.md:240`, `include/LO_GEN.labels.md:1160` | 0o277765 | 0 |
| `LOAD_0270` | LABEL(md) | `include/LO_GEN.labels.md:243` | 0o277770 | 0 |
| `LOAD_0272` | LABEL(md) | `include/LO_GEN.labels.md:245` | 0o277772 | 0 |
| `LOAD_0277` | LABEL(md) | `include/LO_GEN.labels.md:250`, `include/LO_GEN.labels.md:1163` | 0o277777 | 0 |
| `LOAD_0302` | LABEL(md) | `include/LO_GEN.labels.md:253` | 0o300002 | 0 |
| `LOAD_0303` | LABEL(md) | `include/LO_GEN.labels.md:254`, `include/LO_GEN.labels.md:1136` | 0o300003 | 0 |
| `LOAD_0315` | LABEL(md) | `include/LO_GEN.labels.md:264`, `include/LO_GEN.labels.md:1136` | 0o300015 | 0 |
| `LOAD_0332` | LABEL(md) | `include/LO_GEN.labels.md:277` | 0o300032 | 0 |
| `LOAD_0333` | LABEL(md) | `include/LO_GEN.labels.md:278`, `include/LO_GEN.labels.md:1160` | 0o300033 | 0 |
| `LOAD_0334` | LABEL(md) | `include/LO_GEN.labels.md:279`, `include/LO_GEN.labels.md:1167` | 0o300034 | 0 |
| `LOAD_0335` | LABEL(md) | `include/LO_GEN.labels.md:280` | 0o300035 | 0 |
| `LOAD_0347` | LABEL(md) | `include/LO_GEN.labels.md:290`, `include/LO_GEN.labels.md:1173` | 0o300047 | 0 |
| `LOAD_0356` | LABEL(md) | `include/LO_GEN.labels.md:297` | 0o300056 | 0 |
| `LOAD_0364` | LABEL(md) | `include/LO_GEN.labels.md:303`, `include/LO_GEN.labels.md:1176` | 0o300064 | 0 |
| `LOAD_0365` | LABEL(md) | `include/LO_GEN.labels.md:304`, `include/LO_GEN.labels.md:1398` | 0o300065 | 0 |
| `LOAD_0411` | LABEL(md) | `include/LO_GEN.labels.md:324`, `include/LO_GEN.labels.md:1202` | 0o300111 | 0 |
| `LOAD_0412` | LABEL(md) | `include/LO_GEN.labels.md:325`, `include/LO_GEN.labels.md:1204` | 0o300112 | 0 |
| `LOAD_0413` | LABEL(md) | `include/LO_GEN.labels.md:326`, `include/LO_GEN.labels.md:1208` | 0o300113 | 0 |
| `LOAD_0414` | LABEL(md) | `include/LO_GEN.labels.md:327`, `include/LO_GEN.labels.md:1209` | 0o300114 | 0 |
| `LOAD_0624` | LABEL(md) | `include/LO_GEN.labels.md:463`, `include/LO_GEN.labels.md:1326` | 0o300324 | 0 |
| `LOAD_0625` | LABEL(md) | `include/LO_GEN.labels.md:464` | 0o300325 | 0 |
| `LOAD_0627` | LABEL(md) | `include/LO_GEN.labels.md:466` | 0o300327 | 0 |
| `LOAD_0630` | LABEL(md) | `include/LO_GEN.labels.md:467` | 0o300330 | 0 |
| `LOAD_0633` | LABEL(md) | `include/LO_GEN.labels.md:470` | 0o300333 | 0 |
| `LOAD_0634` | LABEL(md) | `include/LO_GEN.labels.md:471` | 0o300334 | 0 |
| `LOAD_0637` | LABEL(md) | `include/LO_GEN.labels.md:474` | 0o300337 | 0 |
| `LOAD_0647` | LABEL(md) | `include/LO_GEN.labels.md:482`, `include/LO_GEN.labels.md:1261` | 0o300347 | 0 |
| `LOAD_0652` | LABEL(md) | `include/LO_GEN.labels.md:485` | 0o300352 | 0 |
| `LOAD_0653` | LABEL(md) | `include/LO_GEN.labels.md:486`, `include/LO_GEN.labels.md:1160` | 0o300353 | 0 |
| `LOAD_0656` | LABEL(md) | `include/LO_GEN.labels.md:489` | 0o300356 | 0 |
| `LOAD_0662` | LABEL(md) | `include/LO_GEN.labels.md:493` | 0o300362 | 0 |
| `LOAD_0665` | LABEL(md) | `include/LO_GEN.labels.md:496` | 0o300365 | 0 |
| `LOAD_0674` | LABEL(md) | `include/LO_GEN.labels.md:503` | 0o300374 | 0 |
| `LOAD_0677` | LABEL(md) | `include/LO_GEN.labels.md:506` | 0o300377 | 0 |
| `LOAD_0700` | LABEL(md) | `include/LO_GEN.labels.md:507` | 0o300400 | 0 |
| `LOAD_0704` | LABEL(md) | `include/LO_GEN.labels.md:511`, `include/LO_GEN.labels.md:1123` | 0o300404 | 0 |
| `LOAD_0706` | LABEL(md) | `include/LO_GEN.labels.md:513` | 0o300406 | 0 |
| `LOAD_0707` | LABEL(md) | `include/LO_GEN.labels.md:514` | 0o300407 | 0 |
| `LOAD_0712` | LABEL(md) | `include/LO_GEN.labels.md:517`, `include/LO_GEN.labels.md:1123` | 0o300412 | 0 |
| `LOAD_0722` | LABEL(md) | `include/LO_GEN.labels.md:525` | 0o300422 | 0 |
| `LOAD_0723` | LABEL(md) | `include/LO_GEN.labels.md:526` | 0o300423 | 0 |
| `LOAD_0737` | LABEL(md) | `include/LO_GEN.labels.md:538`, `include/LO_GEN.labels.md:1132` | 0o300437 | 0 |
| `LOAD_0744` | LABEL(md) | `include/LO_GEN.labels.md:543`, `include/LO_GEN.labels.md:1168` | 0o300444 | 0 |
| `LOAD_0754` | LABEL(md) | `include/LO_GEN.labels.md:551`, `include/LO_GEN.labels.md:1173` | 0o300454 | 0 |
| `LOAD_0760` | LABEL(md) | `include/LO_GEN.labels.md:555` | 0o300460 | 0 |
| `LOAD_0763` | LABEL(md) | `include/LO_GEN.labels.md:558` | 0o300463 | 0 |
| `LOAD_0764` | LABEL(md) | `include/LO_GEN.labels.md:559` | 0o300464 | 0 |
| `LOAD_0771` | LABEL(md) | `include/LO_GEN.labels.md:564`, `include/LO_GEN.labels.md:1217` | 0o300471 | 0 |
| `LOAD_0775` | LABEL(md) | `include/LO_GEN.labels.md:568`, `include/LO_GEN.labels.md:1221` | 0o300475 | 0 |
| `LOAD_0776` | LABEL(md) | `include/LO_GEN.labels.md:569`, `include/LO_GEN.labels.md:1209` | 0o300476 | 0 |
| `LOAD_1001` | LABEL(md) | `include/LO_GEN.labels.md:572` | 0o300501 | 0 |
| `LOAD_1005` | LABEL(md) | `include/LO_GEN.labels.md:576` | 0o300505 | 0 |
| `LOAD_1012` | LABEL(md) | `include/LO_GEN.labels.md:581`, `include/LO_GEN.labels.md:1168` | 0o300512 | 0 |
| `LOAD_1015` | LABEL(md) | `include/LO_GEN.labels.md:584` | 0o300515 | 0 |
| `LOAD_1021` | LABEL(md) | `include/LO_GEN.labels.md:588` | 0o300521 | 0 |
| `LOAD_1031` | LABEL(md) | `include/LO_GEN.labels.md:596`, `include/LO_GEN.labels.md:1168` | 0o300531 | 0 |
| `LOAD_1043` | LABEL(md) | `include/LO_GEN.labels.md:606` | 0o300543 | 0 |
| `LOAD_1052` | LABEL(md) | `include/LO_GEN.labels.md:613` | 0o300552 | 0 |
| `LOAD_1063` | LABEL(md) | `include/LO_GEN.labels.md:622`, `include/LO_GEN.labels.md:1230` | 0o300563 | 0 |
| `LOAD_1072` | LABEL(md) | `include/LO_GEN.labels.md:629` | 0o300572 | 0 |
| `LOAD_1074` | LABEL(md) | `include/LO_GEN.labels.md:631`, `include/LO_GEN.labels.md:1138` | 0o300574 | 0 |
| `LOAD_1105` | LABEL(md) | `include/LO_GEN.labels.md:640` | 0o300605 | 0 |
| `LOAD_1120` | LABEL(md) | `include/LO_GEN.labels.md:651` | 0o300620 | 0 |
| `LOAD_1140` | LABEL(md) | `include/LO_GEN.labels.md:667` | 0o300640 | 0 |
| `LOAD_1146` | LABEL(md) | `include/LO_GEN.labels.md:673` | 0o300646 | 0 |
| `LOAD_1154` | LABEL(md) | `include/LO_GEN.labels.md:679` | 0o300654 | 0 |
| `LOAD_1155` | LABEL(md) | `include/LO_GEN.labels.md:680` | 0o300655 | 0 |
| `LOAD_1177` | LABEL(md) | `include/LO_GEN.labels.md:698` | 0o300677 | 0 |
| `LOAD_1201` | LABEL(md) | `include/LO_GEN.labels.md:700` | 0o300701 | 0 |
| `LOAD_1203` | LABEL(md) | `include/LO_GEN.labels.md:702` | 0o300703 | 0 |
| `LOAD_1211` | LABEL(md) | `include/LO_GEN.labels.md:708` | 0o300711 | 0 |
| `LOAD_1217` | LABEL(md) | `include/LO_GEN.labels.md:714` | 0o300717 | 0 |
| `LOAD_1220` | LABEL(md) | `include/LO_GEN.labels.md:715`, `include/LO_GEN.labels.md:1163` | 0o300720 | 0 |
| `LOAD_1222` | LABEL(md) | `include/LO_GEN.labels.md:717` | 0o300722 | 0 |
| `LOAD_1223` | LABEL(md) | `include/LO_GEN.labels.md:718` | 0o300723 | 0 |
| `LOAD_1225` | LABEL(md) | `include/LO_GEN.labels.md:720` | 0o300725 | 0 |
| `LOAD_1230` | LABEL(md) | `include/LO_GEN.labels.md:723`, `include/LO_GEN.labels.md:1114` | 0o300730 | 0 |
| `LOAD_1233` | LABEL(md) | `include/LO_GEN.labels.md:726`, `include/LO_GEN.labels.md:1114` | 0o300733 | 0 |
| `LOAD_1240` | LABEL(md) | `include/LO_GEN.labels.md:731`, `include/LO_GEN.labels.md:1114` | 0o300740 | 0 |
| `LOAD_1243` | LABEL(md) | `include/LO_GEN.labels.md:734` | 0o300743 | 0 |
| `LOAD_1252` | LABEL(md) | `include/LO_GEN.labels.md:741`, `include/LO_GEN.labels.md:1324` | 0o300752 | 0 |
| `LOAD_1253` | LABEL(md) | `include/LO_GEN.labels.md:742` | 0o300753 | 0 |
| `LOAD_1254` | LABEL(md) | `include/LO_GEN.labels.md:743` | 0o300754 | 0 |
| `LOAD_1257` | LABEL(md) | `include/LO_GEN.labels.md:746` | 0o300757 | 0 |
| `LOAD_1307` | LABEL(md) | `include/LO_GEN.labels.md:770` | 0o301007 | 0 |
| `LOAD_1312` | LABEL(md) | `include/LO_GEN.labels.md:773` | 0o301012 | 0 |
| `LOAD_1322` | LABEL(md) | `include/LO_GEN.labels.md:781` | 0o301022 | 0 |
| `LOAD_1325` | LABEL(md) | `include/LO_GEN.labels.md:784`, `include/LO_GEN.labels.md:1171` | 0o301025 | 0 |
| `LOAD_1327` | LABEL(md) | `include/LO_GEN.labels.md:786` | 0o301027 | 0 |
| `LOAD_1332` | LABEL(md) | `include/LO_GEN.labels.md:789` | 0o301032 | 0 |
| `LOAD_1334` | LABEL(md) | `include/LO_GEN.labels.md:791` | 0o301034 | 0 |
| `LOAD_1337` | LABEL(md) | `include/LO_GEN.labels.md:794`, `include/LO_GEN.labels.md:1167` | 0o301037 | 0 |
| `LOAD_1341` | LABEL(md) | `include/LO_GEN.labels.md:796` | 0o301041 | 0 |
| `LOAD_1350` | LABEL(md) | `include/LO_GEN.labels.md:803` | 0o301050 | 0 |
| `LOAD_1354` | LABEL(md) | `include/LO_GEN.labels.md:807` | 0o301054 | 0 |
| `LOAD_1360` | LABEL(md) | `include/LO_GEN.labels.md:811`, `include/LO_GEN.labels.md:1135` | 0o301060 | 0 |
| `LOAD_1361` | LABEL(md) | `include/LO_GEN.labels.md:812` | 0o301061 | 0 |
| `LOAD_1375` | LABEL(md) | `include/LO_GEN.labels.md:824` | 0o301075 | 0 |
| `LOAD_1402` | LABEL(md) | `include/LO_GEN.labels.md:829` | 0o301102 | 0 |
| `LOAD_1407` | LABEL(md) | `include/LO_GEN.labels.md:834` | 0o301107 | 0 |
| `LOAD_1413` | LABEL(md) | `include/LO_GEN.labels.md:838` | 0o301113 | 0 |
| `LOAD_1417` | LABEL(md) | `include/LO_GEN.labels.md:842` | 0o301117 | 0 |
| `LOAD_1426` | LABEL(md) | `include/LO_GEN.labels.md:849`, `include/LO_GEN.labels.md:1126` | 0o301126 | 0 |
| `LOAD_1427` | LABEL(md) | `include/LO_GEN.labels.md:850` | 0o301127 | 0 |
| `LOAD_1430` | LABEL(md) | `include/LO_GEN.labels.md:851` | 0o301130 | 0 |
| `LOAD_1431` | LABEL(md) | `include/LO_GEN.labels.md:852` | 0o301131 | 0 |
| `LOAD_1436` | LABEL(md) | `include/LO_GEN.labels.md:857` | 0o301136 | 0 |
| `LOAD_1447` | LABEL(md) | `include/LO_GEN.labels.md:866` | 0o301147 | 0 |
| `LOAD_1451` | LABEL(md) | `include/LO_GEN.labels.md:868` | 0o301151 | 0 |
| `LOAD_1455` | LABEL(md) | `include/LO_GEN.labels.md:872` | 0o301155 | 0 |
| `LOAD_1457` | LABEL(md) | `include/LO_GEN.labels.md:874` | 0o301157 | 0 |
| `LOAD_1461` | LABEL(md) | `include/LO_GEN.labels.md:876` | 0o301161 | 0 |
| `LOAD_1463` | LABEL(md) | `include/LO_GEN.labels.md:878` | 0o301163 | 0 |
| `LOAD_1465` | LABEL(md) | `include/LO_GEN.labels.md:880`, `include/LO_GEN.labels.md:1266` | 0o301165 | 0 |
| `LOAD_1467` | LABEL(md) | `include/LO_GEN.labels.md:882` | 0o301167 | 0 |
| `LOAD_1471` | LABEL(md) | `include/LO_GEN.labels.md:884` | 0o301171 | 0 |
| `LOAD_1472` | LABEL(md) | `include/LO_GEN.labels.md:885` | 0o301172 | 0 |
| `LOAD_1474` | LABEL(md) | `include/LO_GEN.labels.md:887` | 0o301174 | 0 |
| `LOAD_1476` | LABEL(md) | `include/LO_GEN.labels.md:889`, `include/LO_GEN.labels.md:1172` | 0o301176 | 0 |
| `LOAD_1500` | LABEL(md) | `include/LO_GEN.labels.md:891` | 0o301200 | 0 |
| `LOAD_1502` | LABEL(md) | `include/LO_GEN.labels.md:893`, `include/LO_GEN.labels.md:1279` | 0o301202 | 0 |
| `LOAD_1510` | LABEL(md) | `include/LO_GEN.labels.md:899`, `include/LO_GEN.labels.md:1157` | 0o301210 | 0 |
| `LOAD_1515` | LABEL(md) | `include/LO_GEN.labels.md:904` | 0o301215 | 0 |
| `LOAD_1516` | LABEL(md) | `include/LO_GEN.labels.md:905` | 0o301216 | 0 |
| `LOAD_1517` | LABEL(md) | `include/LO_GEN.labels.md:906` | 0o301217 | 0 |
| `LOAD_1524` | LABEL(md) | `include/LO_GEN.labels.md:911` | 0o301224 | 0 |
| `LOAD_1527` | LABEL(md) | `include/LO_GEN.labels.md:914` | 0o301227 | 0 |
| `LOAD_1530` | LABEL(md) | `include/LO_GEN.labels.md:915`, `include/LO_GEN.labels.md:1162` | 0o301230 | 0 |
| `LOAD_1532` | LABEL(md) | `include/LO_GEN.labels.md:917` | 0o301232 | 0 |
| `LOAD_1534` | LABEL(md) | `include/LO_GEN.labels.md:919` | 0o301234 | 0 |
| `LOAD_1541` | LABEL(md) | `include/LO_GEN.labels.md:924`, `include/LO_GEN.labels.md:1280` | 0o301241 | 0 |
| `LOAD_1545` | LABEL(md) | `include/LO_GEN.labels.md:928` | 0o301245 | 0 |
| `LOAD_1546` | LABEL(md) | `include/LO_GEN.labels.md:929`, `include/LO_GEN.labels.md:1397` | 0o301246 | 0 |
| `LOAD_1554` | LABEL(md) | `include/LO_GEN.labels.md:935`, `include/LO_GEN.labels.md:1281` | 0o301254 | 0 |
| `LOAD_1557` | LABEL(md) | `include/LO_GEN.labels.md:938` | 0o301257 | 0 |
| `LOAD_1560` | LABEL(md) | `include/LO_GEN.labels.md:939`, `include/LO_GEN.labels.md:1397` | 0o301260 | 0 |
| `LOAD_1566` | LABEL(md) | `include/LO_GEN.labels.md:945`, `include/LO_GEN.labels.md:1284` | 0o301266 | 0 |
| `LOAD_1576` | LABEL(md) | `include/LO_GEN.labels.md:953` | 0o301276 | 0 |
| `LOAD_1577` | LABEL(md) | `include/LO_GEN.labels.md:954` | 0o301277 | 0 |
| `LOAD_1622` | LABEL(md) | `include/LO_GEN.labels.md:973`, `include/LO_GEN.labels.md:1217` | 0o301322 | 0 |
| `LOAD_1626` | LABEL(md) | `include/LO_GEN.labels.md:977`, `include/LO_GEN.labels.md:1137` | 0o301326 | 0 |
| `LOAD_1634` | LABEL(md) | `include/LO_GEN.labels.md:983` | 0o301334 | 0 |
| `LOAD_1635` | LABEL(md) | `include/LO_GEN.labels.md:984` | 0o301335 | 0 |
| `LOAD_1637` | LABEL(md) | `include/LO_GEN.labels.md:986`, `include/LO_GEN.labels.md:1287` | 0o301337 | 0 |
| `LOAD_1640` | LABEL(md) | `include/LO_GEN.labels.md:987`, `include/LO_GEN.labels.md:1209` | 0o301340 | 0 |
| `LOAD_1642` | LABEL(md) | `include/LO_GEN.labels.md:989` | 0o301342 | 0 |
| `LOAD_1647` | LABEL(md) | `include/LO_GEN.labels.md:994` | 0o301347 | 0 |
| `LOAD_1651` | LABEL(md) | `include/LO_GEN.labels.md:996` | 0o301351 | 0 |
| `LOAD_1652` | LABEL(md) | `include/LO_GEN.labels.md:997` | 0o301352 | 0 |
| `LOAD_1661` | LABEL(md) | `include/LO_GEN.labels.md:1004`, `include/LO_GEN.labels.md:1210` | 0o301361 | 0 |
| `LOAD_1663` | LABEL(md) | `include/LO_GEN.labels.md:1006` | 0o301363 | 0 |
| `LOAD_1664` | LABEL(md) | `include/LO_GEN.labels.md:1007` | 0o301364 | 0 |
| `LOAD_1666` | LABEL(md) | `include/LO_GEN.labels.md:1009`, `include/LO_GEN.labels.md:1289` | 0o301366 | 0 |
| `LOAD_1667` | LABEL(md) | `include/LO_GEN.labels.md:1010`, `include/LO_GEN.labels.md:1096` | 0o301367 | 0 |
| `LOAD_1670` | LABEL(md) | `include/LO_GEN.labels.md:1011`, `include/LO_GEN.labels.md:1097` | 0o301370 | 0 |
| `LOAD_1673` | LABEL(md) | `include/LO_GEN.labels.md:1014`, `include/LO_GEN.labels.md:1100` | 0o301373 | 0 |
| `LOAD_1674` | LABEL(md) | `include/LO_GEN.labels.md:1015`, `include/LO_GEN.labels.md:1102` | 0o301374 | 0 |
| `LOAD_1675` | LABEL(md) | `include/LO_GEN.labels.md:1016`, `include/LO_GEN.labels.md:1105` | 0o301375 | 0 |
| `LOAD_1703` | LABEL(md) | `include/LO_GEN.labels.md:1022` | 0o301403 | 0 |
| `LOAD_1705` | LABEL(md) | `include/LO_GEN.labels.md:1024` | 0o301405 | 0 |
| `LOAD_1712` | LABEL(md) | `include/LO_GEN.labels.md:1029` | 0o301412 | 0 |
| `LOAD_1722` | LABEL(md) | `include/LO_GEN.labels.md:1037` | 0o301422 | 0 |
| `LOAD_1723` | LABEL(md) | `include/LO_GEN.labels.md:1038` | 0o301423 | 0 |
| `LOAD_1726` | LABEL(md) | `include/LO_GEN.labels.md:1041` | 0o301426 | 0 |
| `LOAD_1732` | LABEL(md) | `include/LO_GEN.labels.md:1045` | 0o301432 | 0 |
| `LOAD_1733` | LABEL(md) | `include/LO_GEN.labels.md:1046`, `include/LO_GEN.labels.md:1320` | 0o301433 | 0 |
| `LOAD_1734` | LABEL(md) | `include/LO_GEN.labels.md:1047`, `include/LO_GEN.labels.md:1321` | 0o301434 | 0 |
| `LOAD_1735` | LABEL(md) | `include/LO_GEN.labels.md:1048` | 0o301435 | 0 |
| `LOAD_1750` | LABEL(md) | `include/LO_GEN.labels.md:1059` | 0o301450 | 0 |
| `LOAD_1760` | LABEL(md) | `include/LO_GEN.labels.md:1067` | 0o301460 | 0 |
| `LOAD_1771` | LABEL(md) | `include/LO_GEN.labels.md:1076`, `include/LO_GEN.labels.md:1161` | 0o301471 | 0 |
| `LOAD_1772` | LABEL(md) | `include/LO_GEN.labels.md:1077` | 0o301472 | 0 |
| `LOAD_1773` | LABEL(md) | `include/LO_GEN.labels.md:1078` | 0o301473 | 0 |
| `LOAD_1775` | LABEL(md) | `include/LO_GEN.labels.md:1080` | 0o301475 | 0 |
| `LOAD_OVERLAYS` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:243`, `include/FOREX_ROOT.mad:104`, `include/FOREX.labels.md:28`, `include/FOREX.labels.md:79` | — | 0 |
| `LOG` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `LOGTXT` | LABEL(md) | `include/LO_GEN.labels.md:29` | 0o277501 | 0 |
| `LOREX` | LABEL(md) | `include/FOREX.labels.md:7`, `include/FOREX.labels.md:28`, `include/FOREX.labels.md:79` | — | 0 |
| `L_ENTRY_OVL` | LABEL/LABEL(md) | `src/LO_SYN.mad:762`, `include/LO_SYN.labels.md:9` | — | 0 |
| `MARR` | LABEL(md) | `include/FOREX.labels.md:64` | — | 0 |
| `MODULE_NAME_TEXT` | LABEL(md)/TEXT | `src/LO_GEN.mad:502`, `include/LO_GEN.labels.md:29` | 8HLO*GEN | 0 |
| `MODVAL_12500` | EQU/LABEL(md) | `src/LO_GEN.mad:245`, `include/LO_GEN.labels.md:1297` | 12500 | 0 |
| `MOD_SET_0024` | LABEL(md) | `include/LO_GEN.labels.md:79`, `include/LO_GEN.labels.md:1166` | 0o277524 | 0 |
| `MOD_SET_0103` | LABEL(md) | `include/LO_GEN.labels.md:126`, `include/LO_GEN.labels.md:1178`, `include/LO_GEN.labels.md:1315` | 0o277603 | 0 |
| `MONTH_FIELD` | DATA/LABEL(md) | `src/FOREX_RUNTIME.mad:424`, `include/FOREX.labels.md:66` | — | 0 |
| `MONTH_FIELD_OCT` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:109`, `include/FOREX.labels.md:301` | 00 776 | 0 |
| `MUL_1715` | LABEL(md) | `include/LO_GEN.labels.md:1032` | 0o301415 | 0 |
| `MUL_1752` | LABEL(md) | `include/LO_GEN.labels.md:1061` | 0o301452 | 0 |
| `NAMETAB_DESC_0532` | LABEL/LABEL(md) | `src/LO_GEN.mad:1584`, `include/LO_GEN.labels.md:405`, `include/LO_GEN.labels.md:1295` | — | 0 |
| `NAMETAB_DESC_0534` | LABEL/LABEL(md) | `src/LO_GEN.mad:1588`, `include/LO_GEN.labels.md:407`, `include/LO_GEN.labels.md:1295` | — | 0 |
| `NAMETAB_DESC_0536` | LABEL/LABEL(md) | `src/LO_GEN.mad:1592`, `include/LO_GEN.labels.md:409`, `include/LO_GEN.labels.md:1295` | — | 0 |
| `NAMETAB_DESC_0540` | LABEL/LABEL(md) | `src/LO_GEN.mad:1596`, `include/LO_GEN.labels.md:411`, `include/LO_GEN.labels.md:1295` | — | 0 |
| `NAMETAB_DESC_0542` | LABEL/LABEL(md) | `src/LO_GEN.mad:1600`, `include/LO_GEN.labels.md:413` | — | 0 |
| `NAMETAB_DESC_0544` | LABEL/LABEL(md) | `src/LO_GEN.mad:1604`, `include/LO_GEN.labels.md:415` | — | 0 |
| `NAMETAB_DESC_0546` | LABEL/LABEL(md) | `src/LO_GEN.mad:1608`, `include/LO_GEN.labels.md:417` | — | 0 |
| `NAMETAB_DESC_0550` | LABEL/LABEL(md) | `src/LO_GEN.mad:1612`, `include/LO_GEN.labels.md:419` | — | 0 |
| `NAMETAB_DESC_0552` | LABEL/LABEL(md) | `src/LO_GEN.mad:1616`, `include/LO_GEN.labels.md:421` | — | 0 |
| `NAMETAB_DESC_0554` | LABEL/LABEL(md) | `src/LO_GEN.mad:1620`, `include/LO_GEN.labels.md:423` | — | 0 |
| `NAMETAB_DESC_0556` | LABEL/LABEL(md) | `src/LO_GEN.mad:1624`, `include/LO_GEN.labels.md:425` | — | 0 |
| `NAMETAB_DESC_0560` | LABEL/LABEL(md) | `src/LO_GEN.mad:1628`, `include/LO_GEN.labels.md:427` | — | 0 |
| `NAMETAB_DESC_0562` | LABEL/LABEL(md) | `src/LO_GEN.mad:1632`, `include/LO_GEN.labels.md:429` | — | 0 |
| `NAMETAB_DESC_0564` | LABEL/LABEL(md) | `src/LO_GEN.mad:1636`, `include/LO_GEN.labels.md:431` | — | 0 |
| `NAMETAB_DESC_0566` | LABEL/LABEL(md) | `src/LO_GEN.mad:1640`, `include/LO_GEN.labels.md:433` | — | 0 |
| `NAMETAB_DESC_0570` | LABEL/LABEL(md) | `src/LO_GEN.mad:1644`, `include/LO_GEN.labels.md:435` | — | 0 |
| `NAMETAB_DESC_0572` | LABEL/LABEL(md) | `src/LO_GEN.mad:1648`, `include/LO_GEN.labels.md:437` | — | 0 |
| `NAMETAB_DESC_0574` | LABEL/LABEL(md) | `src/LO_GEN.mad:1652`, `include/LO_GEN.labels.md:439` | — | 0 |
| `NAMETAB_DESC_0576` | LABEL/LABEL(md) | `src/LO_GEN.mad:1656`, `include/LO_GEN.labels.md:441` | — | 0 |
| `NAMETAB_DESC_0600` | LABEL/LABEL(md) | `src/LO_GEN.mad:1660`, `include/LO_GEN.labels.md:443` | — | 0 |
| `NAMETAB_DESC_0602` | LABEL/LABEL(md) | `src/LO_GEN.mad:1664`, `include/LO_GEN.labels.md:445` | — | 0 |
| `NAMETAB_DESC_0604` | LABEL/LABEL(md) | `src/LO_GEN.mad:1668`, `include/LO_GEN.labels.md:447` | — | 0 |
| `NAMETAB_DESC_0606` | LABEL/LABEL(md) | `src/LO_GEN.mad:1672`, `include/LO_GEN.labels.md:449` | — | 0 |
| `NAMETAB_DESC_0610` | LABEL/LABEL(md) | `src/LO_GEN.mad:1676`, `include/LO_GEN.labels.md:451` | — | 0 |
| `NAMETAB_DESC_0612` | LABEL/LABEL(md) | `src/LO_GEN.mad:1680`, `include/LO_GEN.labels.md:453` | — | 0 |
| `NAMETAB_DESC_0614` | LABEL/LABEL(md) | `src/LO_GEN.mad:1684`, `include/LO_GEN.labels.md:455` | — | 0 |
| `NAMETAB_DESC_0616` | LABEL/LABEL(md) | `src/LO_GEN.mad:1688`, `include/LO_GEN.labels.md:457` | — | 0 |
| `NAMETAB_DESC_0620` | LABEL/LABEL(md) | `src/LO_GEN.mad:1692`, `include/LO_GEN.labels.md:459` | — | 0 |
| `NAMETAB_DESC_0622` | LABEL/LABEL(md) | `src/LO_GEN.mad:1696`, `include/LO_GEN.labels.md:461` | — | 0 |
| `NAMETAB_TEXT_0533` | LABEL(md)/TEXT | `src/LO_GEN.mad:1586`, `include/LO_GEN.labels.md:406` | 8HPOWER | 0 |
| `NAMETAB_TEXT_0535` | LABEL(md)/TEXT | `src/LO_GEN.mad:1590`, `include/LO_GEN.labels.md:408` | 8HA/RHOCHI | 0 |
| `NAMETAB_TEXT_0537` | LABEL(md)/TEXT | `src/LO_GEN.mad:1594`, `include/LO_GEN.labels.md:410` | 8HA/NOT | 0 |
| `NAMETAB_TEXT_0541` | LABEL(md)/TEXT | `src/LO_GEN.mad:1598`, `include/LO_GEN.labels.md:412` | 8HA/AND | 0 |
| `NAMETAB_TEXT_0543` | LABEL(md)/TEXT | `src/LO_GEN.mad:1602`, `include/LO_GEN.labels.md:414` | 8HFT*621 | 0 |
| `NAMETAB_TEXT_0545` | LABEL(md)/TEXT | `src/LO_GEN.mad:1606`, `include/LO_GEN.labels.md:416` | 8HFT*002 | 0 |
| `NAMETAB_TEXT_0547` | LABEL(md)/TEXT | `src/LO_GEN.mad:1610`, `include/LO_GEN.labels.md:418` | 8HFD*002 | 0 |
| `NAMETAB_TEXT_0551` | LABEL(md)/TEXT | `src/LO_GEN.mad:1614`, `include/LO_GEN.labels.md:420` | 8HFC*002 | 0 |
| `NAMETAB_TEXT_0553` | LABEL(md)/TEXT | `src/LO_GEN.mad:1618`, `include/LO_GEN.labels.md:422` | 8HFT*003 | 0 |
| `NAMETAB_TEXT_0555` | LABEL(md)/TEXT | `src/LO_GEN.mad:1622`, `include/LO_GEN.labels.md:424` | 8HFT*521 | 0 |
| `NAMETAB_TEXT_0557` | LABEL(md)/TEXT | `src/LO_GEN.mad:1626`, `include/LO_GEN.labels.md:426` | 8HFT*721 | 0 |
| `NAMETAB_TEXT_0561` | LABEL(md)/TEXT | `src/LO_GEN.mad:1630`, `include/LO_GEN.labels.md:428` | 8HFT*722 | 0 |
| `NAMETAB_TEXT_0563` | LABEL(md)/TEXT | `src/LO_GEN.mad:1634`, `include/LO_GEN.labels.md:430` | 8HFD*722 | 0 |
| `NAMETAB_TEXT_0565` | LABEL(md)/TEXT | `src/LO_GEN.mad:1638`, `include/LO_GEN.labels.md:432` | 8HFC*722 | 0 |
| `NAMETAB_TEXT_0567` | LABEL(md)/TEXT | `src/LO_GEN.mad:1642`, `include/LO_GEN.labels.md:434` | 8HFT*723 | 0 |
| `NAMETAB_TEXT_0571` | LABEL(md)/TEXT | `src/LO_GEN.mad:1646`, `include/LO_GEN.labels.md:436` | 8HFT*641 | 0 |
| `NAMETAB_TEXT_0573` | LABEL(md)/TEXT | `src/LO_GEN.mad:1650`, `include/LO_GEN.labels.md:438` | 8HFT*642 | 0 |
| `NAMETAB_TEXT_0575` | LABEL(md)/TEXT | `src/LO_GEN.mad:1654`, `include/LO_GEN.labels.md:440` | 8HFD*642 | 0 |
| `NAMETAB_TEXT_0577` | LABEL(md)/TEXT | `src/LO_GEN.mad:1658`, `include/LO_GEN.labels.md:442` | 8HFC*642 | 0 |
| `NAMETAB_TEXT_0601` | LABEL(md)/TEXT | `src/LO_GEN.mad:1662`, `include/LO_GEN.labels.md:444` | 8HFT*643 | 0 |
| `NAMETAB_TEXT_0603` | LABEL(md)/TEXT | `src/LO_GEN.mad:1666`, `include/LO_GEN.labels.md:446` | 8HFT*541 | 0 |
| `NAMETAB_TEXT_0605` | LABEL(md)/TEXT | `src/LO_GEN.mad:1670`, `include/LO_GEN.labels.md:448` | 8HFT*561 | 0 |
| `NAMETAB_TEXT_0607` | LABEL(md)/TEXT | `src/LO_GEN.mad:1674`, `include/LO_GEN.labels.md:450` | 8HFT*571 | 0 |
| `NAMETAB_TEXT_0611` | LABEL(md)/TEXT | `src/LO_GEN.mad:1678`, `include/LO_GEN.labels.md:452` | 8HFT*531 | 0 |
| `NAMETAB_TEXT_0613` | LABEL(md)/TEXT | `src/LO_GEN.mad:1682`, `include/LO_GEN.labels.md:454` | 8HFT*611 | 0 |
| `NAMETAB_TEXT_0615` | LABEL(md)/TEXT | `src/LO_GEN.mad:1686`, `include/LO_GEN.labels.md:456` | 8H*REWIN | 0 |
| `NAMETAB_TEXT_0617` | LABEL(md)/TEXT | `src/LO_GEN.mad:1690`, `include/LO_GEN.labels.md:458` | 8H*BACKS | 0 |
| `NAMETAB_TEXT_0621` | LABEL(md)/TEXT | `src/LO_GEN.mad:1694`, `include/LO_GEN.labels.md:460` | 8H*ENDFI | 0 |
| `NAMETAB_TEXT_0623` | LABEL(md)/TEXT | `src/LO_GEN.mad:1698`, `include/LO_GEN.labels.md:462` | 8HSTOP* | 0 |
| `NN` | LABEL(md) | `include/LO_GEN.labels.md:1549` | — | 0 |
| `NNNNB` | LABEL(md) | `include/LO_GEN.labels.md:1088` | — | 0 |
| `OCTTDEC` | LABEL(md)/SUBP | `src/LO_SYN.mad:28`, `include/FOREX.labels.md:7` | — | 0 |
| `OCT_BEGIN` | LABEL | `src/FOREX_RUNTIME.mad:435` | — | 0 |
| `OCT_DEC_EXFOR` | LABEL(md)/NAME | `src/FOREX_RUNTIME.mad:485`, `include/FOREX.labels.md:70` | — | 0 |
| `ONE` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:274`, `src/LO_GEN.mad:682`, `src/LO_GEN.mad:1711`, `src/LO_GEN.mad:1723`, `src/LO_GEN.mad:1732`, `src/LO_GEN.mad:3411` … (+2) | 1 | 0 |
| `OPRTR` | LABEL(md)/SUBP | `src/LO_SYN.mad:32`, `include/FOREX_ROOT.mad:76`, `include/FOREX.labels.md:358` | — | 0 |
| `PG_PG_GO` | LABEL | `include/FOREX_ROOT.mad:285` | — | 0 |
| `PREPDAT` | LABEL(md) | `include/FOREX.labels.md:63` | — | 0 |
| `PRINT_BLOCK_LEN` | EQU/LABEL(md) | `include/FOREX_ROOT.mad:45`, `include/FOREX.labels.md:333` | 002 | 0 |
| `PRINT_TIME` | ENTRY/LABEL/LABEL(md) | `src/FOREX_CORE.mad:254`, `include/FOREX_ROOT.mad:111`, `include/FOREX.labels.md:29`, `include/FOREX.labels.md:80` | — | 0 |
| `PU` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `REAL` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `REGSEL_4` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:262`, `src/LO_GEN.mad:638`, `src/LO_GEN.mad:649`, `src/LO_GEN.mad:655`, `src/LO_GEN.mad:673`, `src/LO_GEN.mad:694` … (+22) | 4 | 0 |
| `REGSEL_8` | EQU/LABEL/LABEL(md) | `src/LO_GEN.mad:265`, `src/LO_GEN.mad:1105`, `src/LO_GEN.mad:1150`, `src/LO_GEN.mad:1183`, `src/LO_GEN.mad:2161`, `src/LO_GEN.mad:3180` … (+1) | 8 | 0 |
| `REG_INC_0057` | LABEL(md) | `include/LO_GEN.labels.md:106`, `include/LO_GEN.labels.md:1110`, `include/LO_GEN.labels.md:1311` | 0o277557 | 0 |
| `REG_INC_1716` | LABEL(md) | `include/LO_GEN.labels.md:1033` | 0o301416 | 0 |
| `REG_INC_1736` | LABEL(md) | `include/LO_GEN.labels.md:1049` | 0o301436 | 0 |
| `REG_INC_1740` | LABEL(md) | `include/LO_GEN.labels.md:1051` | 0o301440 | 0 |
| `REG_INC_1751` | LABEL(md) | `include/LO_GEN.labels.md:1060` | 0o301451 | 0 |
| `REG_INC_1753` | LABEL(md) | `include/LO_GEN.labels.md:1062` | 0o301453 | 0 |
| `REG_INC_1764` | LABEL(md) | `include/LO_GEN.labels.md:1071` | 0o301464 | 0 |
| `REG_READ_0014` | LABEL(md) | `include/LO_GEN.labels.md:71`, `include/LO_GEN.labels.md:1310` | 0o277514 | 0 |
| `REG_READ_0015` | LABEL(md) | `include/LO_GEN.labels.md:72`, `include/LO_GEN.labels.md:1310` | 0o277515 | 0 |
| `REG_READ_0060` | LABEL(md) | `include/LO_GEN.labels.md:107`, `include/LO_GEN.labels.md:1310` | 0o277560 | 0 |
| `REG_READ_0164` | LABEL(md) | `include/LO_GEN.labels.md:175` | 0o277664 | 0 |
| `REG_READ_0310` | LABEL(md) | `include/LO_GEN.labels.md:259`, `include/LO_GEN.labels.md:1312` | 0o300010 | 0 |
| `REG_READ_0311` | LABEL(md) | `include/LO_GEN.labels.md:260` | 0o300011 | 0 |
| `REG_READ_0735` | LABEL(md) | `include/LO_GEN.labels.md:536` | 0o300435 | 0 |
| `REG_READ_1024` | LABEL(md) | `include/LO_GEN.labels.md:591` | 0o300524 | 0 |
| `REG_READ_1103` | LABEL(md) | `include/LO_GEN.labels.md:638` | 0o300603 | 0 |
| `REG_READ_1123` | LABEL(md) | `include/LO_GEN.labels.md:654` | 0o300623 | 0 |
| `REG_READ_1133` | LABEL(md) | `include/LO_GEN.labels.md:662` | 0o300633 | 0 |
| `REG_READ_1144` | LABEL(md) | `include/LO_GEN.labels.md:671` | 0o300644 | 0 |
| `REG_READ_1165` | LABEL(md) | `include/LO_GEN.labels.md:688` | 0o300665 | 0 |
| `REG_READ_1247` | LABEL(md) | `include/LO_GEN.labels.md:738` | 0o300747 | 0 |
| `REG_READ_1263` | LABEL(md) | `include/LO_GEN.labels.md:750` | 0o300763 | 0 |
| `REG_READ_1347` | LABEL(md) | `include/LO_GEN.labels.md:802` | 0o301047 | 0 |
| `REG_READ_1370` | LABEL(md) | `include/LO_GEN.labels.md:819` | 0o301070 | 0 |
| `REG_READ_1717` | LABEL(md) | `include/LO_GEN.labels.md:1034` | 0o301417 | 0 |
| `REG_READ_1730` | LABEL(md) | `include/LO_GEN.labels.md:1043` | 0o301430 | 0 |
| `REG_READ_1731` | LABEL(md) | `include/LO_GEN.labels.md:1044` | 0o301431 | 0 |
| `REG_READ_1754` | LABEL(md) | `include/LO_GEN.labels.md:1063` | 0o301454 | 0 |
| `REG_SET_0010` | LABEL(md) | `include/LO_GEN.labels.md:67`, `include/LO_GEN.labels.md:1164`, `include/LO_GEN.labels.md:1308` | 0o277510 | 0 |
| `REG_SET_0016` | LABEL(md) | `include/LO_GEN.labels.md:73`, `include/LO_GEN.labels.md:1164` | 0o277516 | 0 |
| `REG_SET_0017` | LABEL(md) | `include/LO_GEN.labels.md:74`, `include/LO_GEN.labels.md:1311` | 0o277517 | 0 |
| `REG_SET_0031` | LABEL(md) | `include/LO_GEN.labels.md:84`, `include/LO_GEN.labels.md:1205`, `include/LO_GEN.labels.md:1316` | 0o277531 | 0 |
| `REG_SET_0061` | LABEL(md) | `include/LO_GEN.labels.md:108`, `include/LO_GEN.labels.md:1205` | 0o277561 | 0 |
| `REG_SET_0107` | LABEL(md) | `include/LO_GEN.labels.md:130` | 0o277607 | 0 |
| `REG_SET_0114` | LABEL(md) | `include/LO_GEN.labels.md:135`, `include/LO_GEN.labels.md:1235`, `include/LO_GEN.labels.md:1313` | 0o277614 | 0 |
| `REG_SET_0121` | LABEL(md) | `include/LO_GEN.labels.md:140`, `include/LO_GEN.labels.md:1236`, `include/LO_GEN.labels.md:1313` | 0o277621 | 0 |
| `REG_SET_0124` | LABEL(md) | `include/LO_GEN.labels.md:143`, `include/LO_GEN.labels.md:1237` | 0o277624 | 0 |
| `REG_SET_0132` | LABEL(md) | `include/LO_GEN.labels.md:149`, `include/LO_GEN.labels.md:1242` | 0o277632 | 0 |
| `REG_SET_0145` | LABEL(md) | `include/LO_GEN.labels.md:160`, `include/LO_GEN.labels.md:1244` | 0o277645 | 0 |
| `REG_SET_0152` | LABEL(md) | `include/LO_GEN.labels.md:165` | 0o277652 | 0 |
| `REG_SET_0166` | LABEL(md) | `include/LO_GEN.labels.md:177` | 0o277666 | 0 |
| `REG_SET_0170` | LABEL(md) | `include/LO_GEN.labels.md:179` | 0o277670 | 0 |
| `REG_SET_0211` | LABEL(md) | `include/LO_GEN.labels.md:196` | 0o277711 | 0 |
| `REG_SET_0216` | LABEL(md) | `include/LO_GEN.labels.md:201`, `include/LO_GEN.labels.md:1245` | 0o277716 | 0 |
| `REG_SET_0223` | LABEL(md) | `include/LO_GEN.labels.md:206`, `include/LO_GEN.labels.md:1235` | 0o277723 | 0 |
| `REG_SET_0230` | LABEL(md) | `include/LO_GEN.labels.md:211`, `include/LO_GEN.labels.md:1243` | 0o277730 | 0 |
| `REG_SET_0274` | LABEL(md) | `include/LO_GEN.labels.md:247` | 0o277774 | 0 |
| `REG_SET_0324` | LABEL(md) | `include/LO_GEN.labels.md:271`, `include/LO_GEN.labels.md:1234` | 0o300024 | 0 |
| `REG_SET_0325` | LABEL(md) | `include/LO_GEN.labels.md:272`, `include/LO_GEN.labels.md:1179` | 0o300025 | 0 |
| `REG_SET_0330` | LABEL(md) | `include/LO_GEN.labels.md:275`, `include/LO_GEN.labels.md:1180` | 0o300030 | 0 |
| `REG_SET_0344` | LABEL(md) | `include/LO_GEN.labels.md:287`, `include/LO_GEN.labels.md:1181` | 0o300044 | 0 |
| `REG_SET_0345` | LABEL(md) | `include/LO_GEN.labels.md:288` | 0o300045 | 0 |
| `REG_SET_0353` | LABEL(md) | `include/LO_GEN.labels.md:294`, `include/LO_GEN.labels.md:1242` | 0o300053 | 0 |
| `REG_SET_0360` | LABEL(md) | `include/LO_GEN.labels.md:299`, `include/LO_GEN.labels.md:1234` | 0o300060 | 0 |
| `REG_SET_0361` | LABEL(md) | `include/LO_GEN.labels.md:300`, `include/LO_GEN.labels.md:1182` | 0o300061 | 0 |
| `REG_SET_0366` | LABEL(md) | `include/LO_GEN.labels.md:305`, `include/LO_GEN.labels.md:1241` | 0o300066 | 0 |
| `REG_SET_0452` | LABEL(md) | `include/LO_GEN.labels.md:357`, `include/LO_GEN.labels.md:1186` | 0o300152 | 0 |
| `REG_SET_0453` | LABEL(md) | `include/LO_GEN.labels.md:358`, `include/LO_GEN.labels.md:1183` | 0o300153 | 0 |
| `REG_SET_0454` | LABEL(md) | `include/LO_GEN.labels.md:359`, `include/LO_GEN.labels.md:1198` | 0o300154 | 0 |
| `REG_SET_0455` | LABEL(md) | `include/LO_GEN.labels.md:360`, `include/LO_GEN.labels.md:1199` | 0o300155 | 0 |
| `REG_SET_0456` | LABEL(md) | `include/LO_GEN.labels.md:361`, `include/LO_GEN.labels.md:1200` | 0o300156 | 0 |
| `REG_SET_0457` | LABEL(md) | `include/LO_GEN.labels.md:362`, `include/LO_GEN.labels.md:1195` | 0o300157 | 0 |
| `REG_SET_0460` | LABEL(md) | `include/LO_GEN.labels.md:363`, `include/LO_GEN.labels.md:1194` | 0o300160 | 0 |
| `REG_SET_0461` | LABEL(md) | `include/LO_GEN.labels.md:364`, `include/LO_GEN.labels.md:1193` | 0o300161 | 0 |
| `REG_SET_0462` | LABEL(md) | `include/LO_GEN.labels.md:365`, `include/LO_GEN.labels.md:1201` | 0o300162 | 0 |
| `REG_SET_0474` | LABEL(md) | `include/LO_GEN.labels.md:375`, `include/LO_GEN.labels.md:1197` | 0o300174 | 0 |
| `REG_SET_0475` | LABEL(md) | `include/LO_GEN.labels.md:376`, `include/LO_GEN.labels.md:1196` | 0o300175 | 0 |
| `REG_SET_0476` | LABEL(md) | `include/LO_GEN.labels.md:377`, `include/LO_GEN.labels.md:1190` | 0o300176 | 0 |
| `REG_SET_0477` | LABEL(md) | `include/LO_GEN.labels.md:378`, `include/LO_GEN.labels.md:1187` | 0o300177 | 0 |
| `REG_SET_0521` | LABEL(md) | `include/LO_GEN.labels.md:396` | 0o300221 | 0 |
| `REG_SET_0522` | LABEL(md) | `include/LO_GEN.labels.md:397`, `include/LO_GEN.labels.md:1239` | 0o300222 | 0 |
| `REG_SET_0523` | LABEL(md) | `include/LO_GEN.labels.md:398`, `include/LO_GEN.labels.md:1242` | 0o300223 | 0 |
| `REG_SET_0524` | LABEL(md) | `include/LO_GEN.labels.md:399`, `include/LO_GEN.labels.md:1240` | 0o300224 | 0 |
| `REG_SET_0525` | LABEL(md) | `include/LO_GEN.labels.md:400`, `include/LO_GEN.labels.md:1239` | 0o300225 | 0 |
| `REG_SET_0526` | LABEL(md) | `include/LO_GEN.labels.md:401`, `include/LO_GEN.labels.md:1242` | 0o300226 | 0 |
| `REG_SET_0527` | LABEL(md) | `include/LO_GEN.labels.md:402`, `include/LO_GEN.labels.md:1240` | 0o300227 | 0 |
| `REG_SET_0631` | LABEL(md) | `include/LO_GEN.labels.md:468` | 0o300331 | 0 |
| `REG_SET_0642` | LABEL(md) | `include/LO_GEN.labels.md:477`, `include/LO_GEN.labels.md:1235` | 0o300342 | 0 |
| `REG_SET_0650` | LABEL(md) | `include/LO_GEN.labels.md:483`, `include/LO_GEN.labels.md:1206` | 0o300350 | 0 |
| `REG_SET_0651` | LABEL(md) | `include/LO_GEN.labels.md:484`, `include/LO_GEN.labels.md:1254` | 0o300351 | 0 |
| `REG_SET_0654` | LABEL(md) | `include/LO_GEN.labels.md:487`, `include/LO_GEN.labels.md:1264` | 0o300354 | 0 |
| `REG_SET_0655` | LABEL(md) | `include/LO_GEN.labels.md:488`, `include/LO_GEN.labels.md:1253` | 0o300355 | 0 |
| `REG_SET_0660` | LABEL(md) | `include/LO_GEN.labels.md:491`, `include/LO_GEN.labels.md:1264` | 0o300360 | 0 |
| `REG_SET_0661` | LABEL(md) | `include/LO_GEN.labels.md:492`, `include/LO_GEN.labels.md:1253` | 0o300361 | 0 |
| `REG_SET_0663` | LABEL(md) | `include/LO_GEN.labels.md:494`, `include/LO_GEN.labels.md:1206` | 0o300363 | 0 |
| `REG_SET_0664` | LABEL(md) | `include/LO_GEN.labels.md:495`, `include/LO_GEN.labels.md:1254` | 0o300364 | 0 |
| `REG_SET_0672` | LABEL(md) | `include/LO_GEN.labels.md:501`, `include/LO_GEN.labels.md:1238` | 0o300372 | 0 |
| `REG_SET_0716` | LABEL(md) | `include/LO_GEN.labels.md:521`, `include/LO_GEN.labels.md:1240` | 0o300416 | 0 |
| `REG_SET_0727` | LABEL(md) | `include/LO_GEN.labels.md:530`, `include/LO_GEN.labels.md:1241` | 0o300427 | 0 |
| `REG_SET_0740` | LABEL(md) | `include/LO_GEN.labels.md:539` | 0o300440 | 0 |
| `REG_SET_0750` | LABEL(md) | `include/LO_GEN.labels.md:547`, `include/LO_GEN.labels.md:1233` | 0o300450 | 0 |
| `REG_SET_1000` | LABEL(md) | `include/LO_GEN.labels.md:571`, `include/LO_GEN.labels.md:1237` | 0o300500 | 0 |
| `REG_SET_1003` | LABEL(md) | `include/LO_GEN.labels.md:574`, `include/LO_GEN.labels.md:1207` | 0o300503 | 0 |
| `REG_SET_1004` | LABEL(md) | `include/LO_GEN.labels.md:575`, `include/LO_GEN.labels.md:1253` | 0o300504 | 0 |
| `REG_SET_1006` | LABEL(md) | `include/LO_GEN.labels.md:577` | 0o300506 | 0 |
| `REG_SET_1017` | LABEL(md) | `include/LO_GEN.labels.md:586`, `include/LO_GEN.labels.md:1206` | 0o300517 | 0 |
| `REG_SET_1020` | LABEL(md) | `include/LO_GEN.labels.md:587`, `include/LO_GEN.labels.md:1254` | 0o300520 | 0 |
| `REG_SET_1037` | LABEL(md) | `include/LO_GEN.labels.md:602` | 0o300537 | 0 |
| `REG_SET_1042` | LABEL(md) | `include/LO_GEN.labels.md:605`, `include/LO_GEN.labels.md:1255` | 0o300542 | 0 |
| `REG_SET_1067` | LABEL(md) | `include/LO_GEN.labels.md:626`, `include/LO_GEN.labels.md:1207` | 0o300567 | 0 |
| `REG_SET_1070` | LABEL(md) | `include/LO_GEN.labels.md:627`, `include/LO_GEN.labels.md:1255` | 0o300570 | 0 |
| `REG_SET_1101` | LABEL(md) | `include/LO_GEN.labels.md:636`, `include/LO_GEN.labels.md:1253` | 0o300601 | 0 |
| `REG_SET_1102` | LABEL(md) | `include/LO_GEN.labels.md:637`, `include/LO_GEN.labels.md:1254` | 0o300602 | 0 |
| `REG_SET_1110` | LABEL(md) | `include/LO_GEN.labels.md:643`, `include/LO_GEN.labels.md:1246` | 0o300610 | 0 |
| `REG_SET_1112` | LABEL(md) | `include/LO_GEN.labels.md:645` | 0o300612 | 0 |
| `REG_SET_1122` | LABEL(md) | `include/LO_GEN.labels.md:653` | 0o300622 | 0 |
| `REG_SET_1131` | LABEL(md) | `include/LO_GEN.labels.md:660` | 0o300631 | 0 |
| `REG_SET_1132` | LABEL(md) | `include/LO_GEN.labels.md:661` | 0o300632 | 0 |
| `REG_SET_1142` | LABEL(md) | `include/LO_GEN.labels.md:669` | 0o300642 | 0 |
| `REG_SET_1143` | LABEL(md) | `include/LO_GEN.labels.md:670` | 0o300643 | 0 |
| `REG_SET_1150` | LABEL(md) | `include/LO_GEN.labels.md:675`, `include/LO_GEN.labels.md:1237` | 0o300650 | 0 |
| `REG_SET_1164` | LABEL(md) | `include/LO_GEN.labels.md:687`, `include/LO_GEN.labels.md:1234` | 0o300664 | 0 |
| `REG_SET_1172` | LABEL(md) | `include/LO_GEN.labels.md:693`, `include/LO_GEN.labels.md:1234` | 0o300672 | 0 |
| `REG_SET_1204` | LABEL(md) | `include/LO_GEN.labels.md:703` | 0o300704 | 0 |
| `REG_SET_1236` | LABEL(md) | `include/LO_GEN.labels.md:729`, `include/LO_GEN.labels.md:1188` | 0o300736 | 0 |
| `REG_SET_1246` | LABEL(md) | `include/LO_GEN.labels.md:737`, `include/LO_GEN.labels.md:1189` | 0o300746 | 0 |
| `REG_SET_1250` | LABEL(md) | `include/LO_GEN.labels.md:739` | 0o300750 | 0 |
| `REG_SET_1262` | LABEL(md) | `include/LO_GEN.labels.md:749`, `include/LO_GEN.labels.md:1188` | 0o300762 | 0 |
| `REG_SET_1264` | LABEL(md) | `include/LO_GEN.labels.md:751` | 0o300764 | 0 |
| `REG_SET_1266` | LABEL(md) | `include/LO_GEN.labels.md:753`, `include/LO_GEN.labels.md:1257` | 0o300766 | 0 |
| `REG_SET_1270` | LABEL(md) | `include/LO_GEN.labels.md:755` | 0o300770 | 0 |
| `REG_SET_1301` | LABEL(md) | `include/LO_GEN.labels.md:764`, `include/LO_GEN.labels.md:1256` | 0o301001 | 0 |
| `REG_SET_1313` | LABEL(md) | `include/LO_GEN.labels.md:774` | 0o301013 | 0 |
| `REG_SET_1352` | LABEL(md) | `include/LO_GEN.labels.md:805` | 0o301052 | 0 |
| `REG_SET_1362` | LABEL(md) | `include/LO_GEN.labels.md:813` | 0o301062 | 0 |
| `REG_SET_1403` | LABEL(md) | `include/LO_GEN.labels.md:830` | 0o301103 | 0 |
| `REG_SET_1421` | LABEL(md) | `include/LO_GEN.labels.md:844` | 0o301121 | 0 |
| `REG_SET_1432` | LABEL(md) | `include/LO_GEN.labels.md:853` | 0o301132 | 0 |
| `REG_SET_1441` | LABEL(md) | `include/LO_GEN.labels.md:860` | 0o301141 | 0 |
| `REG_SET_1507` | LABEL(md) | `include/LO_GEN.labels.md:898`, `include/LO_GEN.labels.md:1238` | 0o301207 | 0 |
| `REG_SET_1535` | LABEL(md) | `include/LO_GEN.labels.md:920` | 0o301235 | 0 |
| `REG_SET_1605` | LABEL(md) | `include/LO_GEN.labels.md:960` | 0o301305 | 0 |
| `REG_SET_1613` | LABEL(md) | `include/LO_GEN.labels.md:966`, `include/LO_GEN.labels.md:1248` | 0o301313 | 0 |
| `REG_SET_1614` | LABEL(md) | `include/LO_GEN.labels.md:967` | 0o301314 | 0 |
| `REG_SET_1620` | LABEL(md) | `include/LO_GEN.labels.md:971`, `include/LO_GEN.labels.md:1250` | 0o301320 | 0 |
| `REG_SET_1630` | LABEL(md) | `include/LO_GEN.labels.md:979` | 0o301330 | 0 |
| `REG_SET_1633` | LABEL(md) | `include/LO_GEN.labels.md:982`, `include/LO_GEN.labels.md:1233` | 0o301333 | 0 |
| `REG_SET_1713` | LABEL(md) | `include/LO_GEN.labels.md:1030` | 0o301413 | 0 |
| `REG_SET_1720` | LABEL(md) | `include/LO_GEN.labels.md:1035` | 0o301420 | 0 |
| `REG_SET_1724` | LABEL(md) | `include/LO_GEN.labels.md:1039` | 0o301424 | 0 |
| `REG_SET_1742` | LABEL(md) | `include/LO_GEN.labels.md:1053` | 0o301442 | 0 |
| `REG_SET_1755` | LABEL(md) | `include/LO_GEN.labels.md:1064`, `include/LO_GEN.labels.md:1205` | 0o301455 | 0 |
| `REG_SET_1757` | LABEL(md) | `include/LO_GEN.labels.md:1066`, `include/LO_GEN.labels.md:1312` | 0o301457 | 0 |
| `REG_SET_1761` | LABEL(md) | `include/LO_GEN.labels.md:1068` | 0o301461 | 0 |
| `RMON` | LABEL(md) | `include/FOREX.labels.md:29`, `include/FOREX.labels.md:80` | 0o510317 | 0 |
| `SHIFT_0063` | LABEL(md) | `include/LO_GEN.labels.md:110`, `include/LO_GEN.labels.md:1142` | 0o277563 | 0 |
| `SHIFT_0066` | LABEL(md) | `include/LO_GEN.labels.md:113`, `include/LO_GEN.labels.md:1142` | 0o277566 | 0 |
| `SHIFT_0070` | LABEL(md) | `include/LO_GEN.labels.md:115`, `include/LO_GEN.labels.md:1109` | 0o277570 | 0 |
| `SHIFT_0153` | LABEL(md) | `include/LO_GEN.labels.md:166`, `include/LO_GEN.labels.md:1109` | 0o277653 | 0 |
| `SHIFT_0163` | LABEL(md) | `include/LO_GEN.labels.md:174`, `include/LO_GEN.labels.md:1129` | 0o277663 | 0 |
| `SHIFT_0172` | LABEL(md) | `include/LO_GEN.labels.md:181`, `include/LO_GEN.labels.md:1142` | 0o277672 | 0 |
| `SHIFT_0212` | LABEL(md) | `include/LO_GEN.labels.md:197`, `include/LO_GEN.labels.md:1141` | 0o277712 | 0 |
| `SHIFT_0256` | LABEL(md) | `include/LO_GEN.labels.md:233`, `include/LO_GEN.labels.md:1129` | 0o277756 | 0 |
| `SHIFT_1034` | LABEL(md) | `include/LO_GEN.labels.md:599`, `include/LO_GEN.labels.md:1217` | 0o300534 | 0 |
| `SHIFT_1045` | LABEL(md) | `include/LO_GEN.labels.md:608`, `include/LO_GEN.labels.md:1097` | 0o300545 | 0 |
| `SHIFT_1055` | LABEL(md) | `include/LO_GEN.labels.md:616`, `include/LO_GEN.labels.md:1204` | 0o300555 | 0 |
| `SHIFT_1275` | LABEL(md) | `include/LO_GEN.labels.md:760`, `include/LO_GEN.labels.md:1220` | 0o300775 | 0 |
| `SHIFT_1363` | LABEL(md) | `include/LO_GEN.labels.md:814`, `include/LO_GEN.labels.md:1107` | 0o301063 | 0 |
| `SHIFT_1443` | LABEL(md) | `include/LO_GEN.labels.md:862`, `include/LO_GEN.labels.md:1231` | 0o301143 | 0 |
| `SHIFT_1602` | LABEL(md) | `include/LO_GEN.labels.md:957` | 0o301302 | 0 |
| `SHIFT_1744` | LABEL(md) | `include/LO_GEN.labels.md:1055`, `include/LO_GEN.labels.md:1231` | 0o301444 | 0 |
| `START` | ENTRY/LABEL(md) | `src/LO_GEN.mad:26`, `include/FOREX.labels.md:20`, `include/LO_GEN.labels.md:15`, `include/LO_GEN.labels.md:15`, `include/LO_SYN.labels.md:9` | — | 0 |
| `STOP` | LABEL(md) | `include/FOREX.labels.md:31` | 0o510332 | 0 |
| `SUB_1046` | LABEL(md) | `include/LO_GEN.labels.md:609` | 0o300546 | 0 |
| `SUB_1111` | LABEL(md) | `include/LO_GEN.labels.md:644`, `include/LO_GEN.labels.md:1265` | 0o300611 | 0 |
| `TAK/PG` | SUBP | `src/LO_SYN.mad:26` | — | 0 |
| `TEXT` | LABEL(md) | `include/FOREX.labels.md:357` | — | 0 |
| `TEXT_A_AND` | LABEL(md)/TEXT | `src/LO_GEN.mad:506`, `include/LO_GEN.labels.md:33` | 8HA/AND | 0 |
| `TEXT_A_NOT` | LABEL(md)/TEXT | `src/LO_GEN.mad:505`, `include/LO_GEN.labels.md:32` | 8HA/NOT | 0 |
| `TEXT_A_RHOCHI` | LABEL(md)/TEXT | `src/LO_GEN.mad:504`, `include/LO_GEN.labels.md:31` | 8HA/RHOCHI | 0 |
| `TEXT_BACKS` | LABEL(md)/TEXT | `src/LO_GEN.mad:529`, `include/LO_GEN.labels.md:56` | 8H*BACKS | 0 |
| `TEXT_ENDFI` | LABEL(md)/TEXT | `src/LO_GEN.mad:530`, `include/LO_GEN.labels.md:57` | 8H*ENDFI | 0 |
| `TEXT_FC_002` | LABEL(md)/TEXT | `src/LO_GEN.mad:510`, `include/LO_GEN.labels.md:37` | 8HFC*002 | 0 |
| `TEXT_FC_642` | LABEL(md)/TEXT | `src/LO_GEN.mad:521`, `include/LO_GEN.labels.md:48` | 8HFC*642 | 0 |
| `TEXT_FC_722` | LABEL(md)/TEXT | `src/LO_GEN.mad:516`, `include/LO_GEN.labels.md:43` | 8HFC*722 | 0 |
| `TEXT_FD_002` | LABEL(md)/TEXT | `src/LO_GEN.mad:509`, `include/LO_GEN.labels.md:36` | 8HFD*002 | 0 |
| `TEXT_FD_642` | LABEL(md)/TEXT | `src/LO_GEN.mad:520`, `include/LO_GEN.labels.md:47` | 8HFD*642 | 0 |
| `TEXT_FD_722` | LABEL(md)/TEXT | `src/LO_GEN.mad:515`, `include/LO_GEN.labels.md:42` | 8HFD*722 | 0 |
| `TEXT_FT_002` | LABEL(md)/TEXT | `src/LO_GEN.mad:508`, `include/LO_GEN.labels.md:35` | 8HFT*002 | 0 |
| `TEXT_FT_003` | LABEL(md)/TEXT | `src/LO_GEN.mad:511`, `include/LO_GEN.labels.md:38` | 8HFT*003 | 0 |
| `TEXT_FT_521` | LABEL(md)/TEXT | `src/LO_GEN.mad:512`, `include/LO_GEN.labels.md:39` | 8HFT*521 | 0 |
| `TEXT_FT_531` | LABEL(md)/TEXT | `src/LO_GEN.mad:526`, `include/LO_GEN.labels.md:53` | 8HFT*531 | 0 |
| `TEXT_FT_541` | LABEL(md)/TEXT | `src/LO_GEN.mad:523`, `include/LO_GEN.labels.md:50` | 8HFT*541 | 0 |
| `TEXT_FT_561` | LABEL(md)/TEXT | `src/LO_GEN.mad:524`, `include/LO_GEN.labels.md:51` | 8HFT*561 | 0 |
| `TEXT_FT_571` | LABEL(md)/TEXT | `src/LO_GEN.mad:525`, `include/LO_GEN.labels.md:52` | 8HFT*571 | 0 |
| `TEXT_FT_611` | LABEL(md)/TEXT | `src/LO_GEN.mad:527`, `include/LO_GEN.labels.md:54` | 8HFT*611 | 0 |
| `TEXT_FT_621` | LABEL(md)/TEXT | `src/LO_GEN.mad:507`, `include/LO_GEN.labels.md:34` | 8HFT*621 | 0 |
| `TEXT_FT_641` | LABEL(md)/TEXT | `src/LO_GEN.mad:518`, `include/LO_GEN.labels.md:45` | 8HFT*641 | 0 |
| `TEXT_FT_642` | LABEL(md)/TEXT | `src/LO_GEN.mad:519`, `include/LO_GEN.labels.md:46` | 8HFT*642 | 0 |
| `TEXT_FT_643` | LABEL(md)/TEXT | `src/LO_GEN.mad:522`, `include/LO_GEN.labels.md:49` | 8HFT*643 | 0 |
| `TEXT_FT_721` | LABEL(md)/TEXT | `src/LO_GEN.mad:513`, `include/LO_GEN.labels.md:40` | 8HFT*721 | 0 |
| `TEXT_FT_722` | LABEL(md)/TEXT | `src/LO_GEN.mad:514`, `include/LO_GEN.labels.md:41` | 8HFT*722 | 0 |
| `TEXT_FT_723` | LABEL(md)/TEXT | `src/LO_GEN.mad:517`, `include/LO_GEN.labels.md:44` | 8HFT*723 | 0 |
| `TEXT_LIT_6H0000` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:87`, `include/FOREX.labels.md:279` | 6H0000 | 0 |
| `TEXT_LIT_6H03_0` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:91`, `include/FOREX.labels.md:283` | 6H03 0 | 0 |
| `TEXT_LIT_6H_231_HB` | EQU/LABEL(md) | `src/FOREX_RUNTIME.mad:102`, `include/FOREX.labels.md:294` | 6H'231'  ЯHB | 0 |
| `TEXT_POWER` | LABEL(md)/TEXT | `src/LO_GEN.mad:503`, `include/LO_GEN.labels.md:30` | 8HPOWER | 0 |
| `TEXT_REWIN` | LABEL(md)/TEXT | `src/LO_GEN.mad:528`, `include/LO_GEN.labels.md:55` | 8H*REWIN | 0 |
| `TEXT_STOP` | LABEL(md)/TEXT | `src/LO_GEN.mad:531`, `include/LO_GEN.labels.md:58` | 8HSTOP* | 0 |
| `TIME_MASK` | TEXT | `src/FOREX_RUNTIME.mad:420` | — | 0 |
| `VCALL_0051` | LABEL(md) | `include/LO_GEN.labels.md:100`, `include/LO_GEN.labels.md:1306`, `include/LO_GEN.labels.md:1369` | 0o277551 | 0 |
| `VCALL_1226` | LABEL(md) | `include/LO_GEN.labels.md:721`, `include/LO_GEN.labels.md:1333` | 0o300726 | 0 |
| `VCALL_1355` | LABEL(md) | `include/LO_GEN.labels.md:808`, `include/LO_GEN.labels.md:1334` | 0o301055 | 0 |
| `W0000` | LABEL(md) | `include/LO_GEN.labels.md:59` | 0o277500 | 0 |
| `W0001` | LABEL(md) | `include/LO_GEN.labels.md:60` | 0o277501 | 0 |
| `W0002` | LABEL(md) | `include/LO_GEN.labels.md:61` | 0o277502 | 0 |
| `W0003` | LABEL(md) | `include/LO_GEN.labels.md:62` | 0o277503 | 0 |
| `W0004` | LABEL(md) | `include/LO_GEN.labels.md:63` | 0o277504 | 0 |
| `W0005` | LABEL(md) | `include/LO_GEN.labels.md:64` | 0o277505 | 0 |
| `W0006` | LABEL(md) | `include/LO_GEN.labels.md:65` | 0o277506 | 0 |
| `W0007` | LABEL(md) | `include/LO_GEN.labels.md:66` | 0o277507 | 0 |
| `W0010` | LABEL(md) | `include/LO_GEN.labels.md:67` | 0o277510 | 0 |
| `W0011` | LABEL(md) | `include/LO_GEN.labels.md:68` | 0o277511 | 0 |
| `W0012` | LABEL(md) | `include/LO_GEN.labels.md:69` | 0o277512 | 0 |
| `W0013` | LABEL(md) | `include/LO_GEN.labels.md:70` | 0o277513 | 0 |
| `W0014` | LABEL(md) | `include/LO_GEN.labels.md:71` | 0o277514 | 0 |
| `W0015` | LABEL(md) | `include/LO_GEN.labels.md:72` | 0o277515 | 0 |
| `W0016` | LABEL(md) | `include/LO_GEN.labels.md:73` | 0o277516 | 0 |
| `W0017` | LABEL(md) | `include/LO_GEN.labels.md:74` | 0o277517 | 0 |
| `W0020` | LABEL(md) | `include/LO_GEN.labels.md:75` | 0o277520 | 0 |
| `W0021` | LABEL(md) | `include/LO_GEN.labels.md:76` | 0o277521 | 0 |
| `W0022` | LABEL(md) | `include/LO_GEN.labels.md:77` | 0o277522 | 0 |
| `W0023` | LABEL(md) | `include/LO_GEN.labels.md:78` | 0o277523 | 0 |
| `W0024` | LABEL(md) | `include/LO_GEN.labels.md:79` | 0o277524 | 0 |
| `W0025` | LABEL(md) | `include/LO_GEN.labels.md:80` | 0o277525 | 0 |
| `W0026` | LABEL(md) | `include/LO_GEN.labels.md:81` | 0o277526 | 0 |
| `W0027` | LABEL(md) | `include/LO_GEN.labels.md:82` | 0o277527 | 0 |
| `W0030` | LABEL(md) | `include/LO_GEN.labels.md:83` | 0o277530 | 0 |
| `W0031` | LABEL(md) | `include/LO_GEN.labels.md:84` | 0o277531 | 0 |
| `W0032` | LABEL(md) | `include/LO_GEN.labels.md:85` | 0o277532 | 0 |
| `W0033` | LABEL(md) | `include/LO_GEN.labels.md:86` | 0o277533 | 0 |
| `W0034` | LABEL(md) | `include/LO_GEN.labels.md:87` | 0o277534 | 0 |
| `W0035` | LABEL(md) | `include/LO_GEN.labels.md:88` | 0o277535 | 0 |
| `W0036` | LABEL(md) | `include/LO_GEN.labels.md:89` | 0o277536 | 0 |
| `W0037` | LABEL(md) | `include/LO_GEN.labels.md:90` | 0o277537 | 0 |
| `W0040` | LABEL(md) | `include/LO_GEN.labels.md:91` | 0o277540 | 0 |
| `W0041` | LABEL(md) | `include/LO_GEN.labels.md:92` | 0o277541 | 0 |
| `W0042` | LABEL(md) | `include/LO_GEN.labels.md:93` | 0o277542 | 0 |
| `W0043` | LABEL(md) | `include/LO_GEN.labels.md:94` | 0o277543 | 0 |
| `W0044` | LABEL(md) | `include/LO_GEN.labels.md:95` | 0o277544 | 0 |
| `W0045` | LABEL(md) | `include/LO_GEN.labels.md:96` | 0o277545 | 0 |
| `W0046` | LABEL(md) | `include/LO_GEN.labels.md:97` | 0o277546 | 0 |
| `W0047` | LABEL(md) | `include/LO_GEN.labels.md:98` | 0o277547 | 0 |
| `W0050` | LABEL(md) | `include/LO_GEN.labels.md:99` | 0o277550 | 0 |
| `W0051` | LABEL(md) | `include/LO_GEN.labels.md:100` | 0o277551 | 0 |
| `W0052` | LABEL(md) | `include/LO_GEN.labels.md:101` | 0o277552 | 0 |
| `W0053` | LABEL(md) | `include/LO_GEN.labels.md:102` | 0o277553 | 0 |
| `W0054` | LABEL(md) | `include/LO_GEN.labels.md:103` | 0o277554 | 0 |
| `W0055` | LABEL(md) | `include/LO_GEN.labels.md:104` | 0o277555 | 0 |
| `W0056` | LABEL(md) | `include/LO_GEN.labels.md:105` | 0o277556 | 0 |
| `W0057` | LABEL(md) | `include/LO_GEN.labels.md:106` | 0o277557 | 0 |
| `W0060` | LABEL(md) | `include/LO_GEN.labels.md:107` | 0o277560 | 0 |
| `W0061` | LABEL(md) | `include/LO_GEN.labels.md:108` | 0o277561 | 0 |
| `W0062` | LABEL(md) | `include/LO_GEN.labels.md:109` | 0o277562 | 0 |
| `W0063` | LABEL(md) | `include/LO_GEN.labels.md:110` | 0o277563 | 0 |
| `W0064` | LABEL(md) | `include/LO_GEN.labels.md:111` | 0o277564 | 0 |
| `W0065` | LABEL(md) | `include/LO_GEN.labels.md:112` | 0o277565 | 0 |
| `W0066` | LABEL(md) | `include/LO_GEN.labels.md:113` | 0o277566 | 0 |
| `W0067` | LABEL(md) | `include/LO_GEN.labels.md:114` | 0o277567 | 0 |
| `W0070` | LABEL(md) | `include/LO_GEN.labels.md:115` | 0o277570 | 0 |
| `W0071` | LABEL(md) | `include/LO_GEN.labels.md:116` | 0o277571 | 0 |
| `W0072` | LABEL(md) | `include/LO_GEN.labels.md:117` | 0o277572 | 0 |
| `W0073` | LABEL(md) | `include/LO_GEN.labels.md:118` | 0o277573 | 0 |
| `W0074` | LABEL(md) | `include/LO_GEN.labels.md:119` | 0o277574 | 0 |
| `W0075` | LABEL(md) | `include/LO_GEN.labels.md:120` | 0o277575 | 0 |
| `W0076` | LABEL(md) | `include/LO_GEN.labels.md:121` | 0o277576 | 0 |
| `W0077` | LABEL(md) | `include/LO_GEN.labels.md:122` | 0o277577 | 0 |
| `W0100` | LABEL(md) | `include/LO_GEN.labels.md:123` | 0o277600 | 0 |
| `W0101` | LABEL(md) | `include/LO_GEN.labels.md:124` | 0o277601 | 0 |
| `W0102` | LABEL(md) | `include/LO_GEN.labels.md:125` | 0o277602 | 0 |
| `W0103` | LABEL(md) | `include/LO_GEN.labels.md:126` | 0o277603 | 0 |
| `W0104` | LABEL(md) | `include/LO_GEN.labels.md:127` | 0o277604 | 0 |
| `W0105` | LABEL(md) | `include/LO_GEN.labels.md:128` | 0o277605 | 0 |
| `W0106` | LABEL(md) | `include/LO_GEN.labels.md:129` | 0o277606 | 0 |
| `W0107` | LABEL(md) | `include/LO_GEN.labels.md:130` | 0o277607 | 0 |
| `W0110` | LABEL(md) | `include/LO_GEN.labels.md:131` | 0o277610 | 0 |
| `W0111` | LABEL(md) | `include/LO_GEN.labels.md:132` | 0o277611 | 0 |
| `W0112` | LABEL(md) | `include/LO_GEN.labels.md:133` | 0o277612 | 0 |
| `W0113` | LABEL(md) | `include/LO_GEN.labels.md:134` | 0o277613 | 0 |
| `W0114` | LABEL(md) | `include/LO_GEN.labels.md:135` | 0o277614 | 0 |
| `W0115` | LABEL(md) | `include/LO_GEN.labels.md:136` | 0o277615 | 0 |
| `W0116` | LABEL(md) | `include/LO_GEN.labels.md:137` | 0o277616 | 0 |
| `W0117` | LABEL(md) | `include/LO_GEN.labels.md:138` | 0o277617 | 0 |
| `W0120` | LABEL(md) | `include/LO_GEN.labels.md:139` | 0o277620 | 0 |
| `W0121` | LABEL(md) | `include/LO_GEN.labels.md:140` | 0o277621 | 0 |
| `W0122` | LABEL(md) | `include/LO_GEN.labels.md:141` | 0o277622 | 0 |
| `W0123` | LABEL(md) | `include/LO_GEN.labels.md:142` | 0o277623 | 0 |
| `W0124` | LABEL(md) | `include/LO_GEN.labels.md:143` | 0o277624 | 0 |
| `W0125` | LABEL(md) | `include/LO_GEN.labels.md:144` | 0o277625 | 0 |
| `W0126` | LABEL(md) | `include/LO_GEN.labels.md:145` | 0o277626 | 0 |
| `W0127` | LABEL(md) | `include/LO_GEN.labels.md:146` | 0o277627 | 0 |
| `W0130` | LABEL(md) | `include/LO_GEN.labels.md:147` | 0o277630 | 0 |
| `W0131` | LABEL(md) | `include/LO_GEN.labels.md:148` | 0o277631 | 0 |
| `W0132` | LABEL(md) | `include/LO_GEN.labels.md:149` | 0o277632 | 0 |
| `W0133` | LABEL(md) | `include/LO_GEN.labels.md:150` | 0o277633 | 0 |
| `W0134` | LABEL(md) | `include/LO_GEN.labels.md:151` | 0o277634 | 0 |
| `W0135` | LABEL(md) | `include/LO_GEN.labels.md:152` | 0o277635 | 0 |
| `W0136` | LABEL(md) | `include/LO_GEN.labels.md:153` | 0o277636 | 0 |
| `W0137` | LABEL(md) | `include/LO_GEN.labels.md:154` | 0o277637 | 0 |
| `W0140` | LABEL(md) | `include/LO_GEN.labels.md:155` | 0o277640 | 0 |
| `W0141` | LABEL(md) | `include/LO_GEN.labels.md:156` | 0o277641 | 0 |
| `W0142` | LABEL(md) | `include/LO_GEN.labels.md:157` | 0o277642 | 0 |
| `W0143` | LABEL(md) | `include/LO_GEN.labels.md:158` | 0o277643 | 0 |
| `W0144` | LABEL(md) | `include/LO_GEN.labels.md:159` | 0o277644 | 0 |
| `W0145` | LABEL(md) | `include/LO_GEN.labels.md:160` | 0o277645 | 0 |
| `W0146` | LABEL(md) | `include/LO_GEN.labels.md:161` | 0o277646 | 0 |
| `W0147` | LABEL(md) | `include/LO_GEN.labels.md:162` | 0o277647 | 0 |
| `W0150` | LABEL(md) | `include/LO_GEN.labels.md:163` | 0o277650 | 0 |
| `W0151` | LABEL(md) | `include/LO_GEN.labels.md:164` | 0o277651 | 0 |
| `W0152` | LABEL(md) | `include/LO_GEN.labels.md:165` | 0o277652 | 0 |
| `W0153` | LABEL(md) | `include/LO_GEN.labels.md:166` | 0o277653 | 0 |
| `W0154` | LABEL(md) | `include/LO_GEN.labels.md:167` | 0o277654 | 0 |
| `W0155` | LABEL(md) | `include/LO_GEN.labels.md:168` | 0o277655 | 0 |
| `W0156` | LABEL(md) | `include/LO_GEN.labels.md:169` | 0o277656 | 0 |
| `W0157` | LABEL(md) | `include/LO_GEN.labels.md:170` | 0o277657 | 0 |
| `W0160` | LABEL(md) | `include/LO_GEN.labels.md:171` | 0o277660 | 0 |
| `W0161` | LABEL(md) | `include/LO_GEN.labels.md:172` | 0o277661 | 0 |
| `W0162` | LABEL(md) | `include/LO_GEN.labels.md:173` | 0o277662 | 0 |
| `W0163` | LABEL(md) | `include/LO_GEN.labels.md:174` | 0o277663 | 0 |
| `W0164` | LABEL(md) | `include/LO_GEN.labels.md:175` | 0o277664 | 0 |
| `W0165` | LABEL(md) | `include/LO_GEN.labels.md:176` | 0o277665 | 0 |
| `W0166` | LABEL(md) | `include/LO_GEN.labels.md:177` | 0o277666 | 0 |
| `W0167` | LABEL(md) | `include/LO_GEN.labels.md:178` | 0o277667 | 0 |
| `W0170` | LABEL(md) | `include/LO_GEN.labels.md:179` | 0o277670 | 0 |
| `W0171` | LABEL(md) | `include/LO_GEN.labels.md:180` | 0o277671 | 0 |
| `W0172` | LABEL(md) | `include/LO_GEN.labels.md:181` | 0o277672 | 0 |
| `W0173` | LABEL(md) | `include/LO_GEN.labels.md:182` | 0o277673 | 0 |
| `W0174` | LABEL(md) | `include/LO_GEN.labels.md:183` | 0o277674 | 0 |
| `W0175` | LABEL(md) | `include/LO_GEN.labels.md:184` | 0o277675 | 0 |
| `W0176` | LABEL(md) | `include/LO_GEN.labels.md:185` | 0o277676 | 0 |
| `W0177` | LABEL(md) | `include/LO_GEN.labels.md:186` | 0o277677 | 0 |
| `W0200` | LABEL(md) | `include/LO_GEN.labels.md:187` | 0o277700 | 0 |
| `W0201` | LABEL(md) | `include/LO_GEN.labels.md:188` | 0o277701 | 0 |
| `W0202` | LABEL(md) | `include/LO_GEN.labels.md:189` | 0o277702 | 0 |
| `W0203` | LABEL(md) | `include/LO_GEN.labels.md:190` | 0o277703 | 0 |
| `W0204` | LABEL(md) | `include/LO_GEN.labels.md:191` | 0o277704 | 0 |
| `W0205` | LABEL(md) | `include/LO_GEN.labels.md:192` | 0o277705 | 0 |
| `W0206` | LABEL(md) | `include/LO_GEN.labels.md:193` | 0o277706 | 0 |
| `W0207` | LABEL(md) | `include/LO_GEN.labels.md:194` | 0o277707 | 0 |
| `W0210` | LABEL(md) | `include/LO_GEN.labels.md:195` | 0o277710 | 0 |
| `W0211` | LABEL(md) | `include/LO_GEN.labels.md:196` | 0o277711 | 0 |
| `W0212` | LABEL(md) | `include/LO_GEN.labels.md:197` | 0o277712 | 0 |
| `W0213` | LABEL(md) | `include/LO_GEN.labels.md:198` | 0o277713 | 0 |
| `W0214` | LABEL(md) | `include/LO_GEN.labels.md:199` | 0o277714 | 0 |
| `W0215` | LABEL(md) | `include/LO_GEN.labels.md:200` | 0o277715 | 0 |
| `W0216` | LABEL(md) | `include/LO_GEN.labels.md:201` | 0o277716 | 0 |
| `W0217` | LABEL(md) | `include/LO_GEN.labels.md:202` | 0o277717 | 0 |
| `W0220` | LABEL(md) | `include/LO_GEN.labels.md:203` | 0o277720 | 0 |
| `W0221` | LABEL(md) | `include/LO_GEN.labels.md:204` | 0o277721 | 0 |
| `W0222` | LABEL(md) | `include/LO_GEN.labels.md:205` | 0o277722 | 0 |
| `W0223` | LABEL(md) | `include/LO_GEN.labels.md:206` | 0o277723 | 0 |
| `W0224` | LABEL(md) | `include/LO_GEN.labels.md:207` | 0o277724 | 0 |
| `W0225` | LABEL(md) | `include/LO_GEN.labels.md:208` | 0o277725 | 0 |
| `W0226` | LABEL(md) | `include/LO_GEN.labels.md:209` | 0o277726 | 0 |
| `W0227` | LABEL(md) | `include/LO_GEN.labels.md:210` | 0o277727 | 0 |
| `W0230` | LABEL(md) | `include/LO_GEN.labels.md:211` | 0o277730 | 0 |
| `W0231` | LABEL(md) | `include/LO_GEN.labels.md:212` | 0o277731 | 0 |
| `W0232` | LABEL(md) | `include/LO_GEN.labels.md:213` | 0o277732 | 0 |
| `W0233` | LABEL(md) | `include/LO_GEN.labels.md:214` | 0o277733 | 0 |
| `W0234` | LABEL(md) | `include/LO_GEN.labels.md:215` | 0o277734 | 0 |
| `W0235` | LABEL(md) | `include/LO_GEN.labels.md:216` | 0o277735 | 0 |
| `W0236` | LABEL(md) | `include/LO_GEN.labels.md:217` | 0o277736 | 0 |
| `W0237` | LABEL(md) | `include/LO_GEN.labels.md:218` | 0o277737 | 0 |
| `W0240` | LABEL(md) | `include/LO_GEN.labels.md:219` | 0o277740 | 0 |
| `W0241` | LABEL(md) | `include/LO_GEN.labels.md:220` | 0o277741 | 0 |
| `W0242` | LABEL(md) | `include/LO_GEN.labels.md:221` | 0o277742 | 0 |
| `W0243` | LABEL(md) | `include/LO_GEN.labels.md:222` | 0o277743 | 0 |
| `W0244` | LABEL(md) | `include/LO_GEN.labels.md:223` | 0o277744 | 0 |
| `W0245` | LABEL(md) | `include/LO_GEN.labels.md:224` | 0o277745 | 0 |
| `W0246` | LABEL(md) | `include/LO_GEN.labels.md:225` | 0o277746 | 0 |
| `W0247` | LABEL(md) | `include/LO_GEN.labels.md:226` | 0o277747 | 0 |
| `W0250` | LABEL(md) | `include/LO_GEN.labels.md:227` | 0o277750 | 0 |
| `W0251` | LABEL(md) | `include/LO_GEN.labels.md:228` | 0o277751 | 0 |
| `W0252` | LABEL(md) | `include/LO_GEN.labels.md:229` | 0o277752 | 0 |
| `W0253` | LABEL(md) | `include/LO_GEN.labels.md:230` | 0o277753 | 0 |
| `W0254` | LABEL(md) | `include/LO_GEN.labels.md:231` | 0o277754 | 0 |
| `W0255` | LABEL(md) | `include/LO_GEN.labels.md:232` | 0o277755 | 0 |
| `W0256` | LABEL(md) | `include/LO_GEN.labels.md:233` | 0o277756 | 0 |
| `W0257` | LABEL(md) | `include/LO_GEN.labels.md:234` | 0o277757 | 0 |
| `W0260` | LABEL(md) | `include/LO_GEN.labels.md:235` | 0o277760 | 0 |
| `W0261` | LABEL(md) | `include/LO_GEN.labels.md:236` | 0o277761 | 0 |
| `W0262` | LABEL(md) | `include/LO_GEN.labels.md:237` | 0o277762 | 0 |
| `W0263` | LABEL(md) | `include/LO_GEN.labels.md:238` | 0o277763 | 0 |
| `W0264` | LABEL(md) | `include/LO_GEN.labels.md:239` | 0o277764 | 0 |
| `W0265` | LABEL(md) | `include/LO_GEN.labels.md:240` | 0o277765 | 0 |
| `W0266` | LABEL(md) | `include/LO_GEN.labels.md:241` | 0o277766 | 0 |
| `W0267` | LABEL(md) | `include/LO_GEN.labels.md:242` | 0o277767 | 0 |
| `W0270` | LABEL(md) | `include/LO_GEN.labels.md:243` | 0o277770 | 0 |
| `W0271` | LABEL(md) | `include/LO_GEN.labels.md:244` | 0o277771 | 0 |
| `W0272` | LABEL(md) | `include/LO_GEN.labels.md:245` | 0o277772 | 0 |
| `W0273` | LABEL(md) | `include/LO_GEN.labels.md:246` | 0o277773 | 0 |
| `W0274` | LABEL(md) | `include/LO_GEN.labels.md:247` | 0o277774 | 0 |
| `W0275` | LABEL(md) | `include/LO_GEN.labels.md:248` | 0o277775 | 0 |
| `W0276` | LABEL(md) | `include/LO_GEN.labels.md:249` | 0o277776 | 0 |
| `W0277` | LABEL(md) | `include/LO_GEN.labels.md:250` | 0o277777 | 0 |
| `W0300` | LABEL(md) | `include/LO_GEN.labels.md:251` | 0o300000 | 0 |
| `W0301` | LABEL(md) | `include/LO_GEN.labels.md:252` | 0o300001 | 0 |
| `W0302` | LABEL(md) | `include/LO_GEN.labels.md:253` | 0o300002 | 0 |
| `W0303` | LABEL(md) | `include/LO_GEN.labels.md:254` | 0o300003 | 0 |
| `W0304` | LABEL(md) | `include/LO_GEN.labels.md:255` | 0o300004 | 0 |
| `W0305` | LABEL(md) | `include/LO_GEN.labels.md:256` | 0o300005 | 0 |
| `W0306` | LABEL(md) | `include/LO_GEN.labels.md:257` | 0o300006 | 0 |
| `W0307` | LABEL(md) | `include/LO_GEN.labels.md:258` | 0o300007 | 0 |
| `W0310` | LABEL(md) | `include/LO_GEN.labels.md:259` | 0o300010 | 0 |
| `W0311` | LABEL(md) | `include/LO_GEN.labels.md:260` | 0o300011 | 0 |
| `W0312` | LABEL(md) | `include/LO_GEN.labels.md:261` | 0o300012 | 0 |
| `W0313` | LABEL(md) | `include/LO_GEN.labels.md:262` | 0o300013 | 0 |
| `W0314` | LABEL(md) | `include/LO_GEN.labels.md:263` | 0o300014 | 0 |
| `W0315` | LABEL(md) | `include/LO_GEN.labels.md:264` | 0o300015 | 0 |
| `W0316` | LABEL(md) | `include/LO_GEN.labels.md:265` | 0o300016 | 0 |
| `W0317` | LABEL(md) | `include/LO_GEN.labels.md:266` | 0o300017 | 0 |
| `W0320` | LABEL(md) | `include/LO_GEN.labels.md:267` | 0o300020 | 0 |
| `W0321` | LABEL(md) | `include/LO_GEN.labels.md:268` | 0o300021 | 0 |
| `W0322` | LABEL(md) | `include/LO_GEN.labels.md:269` | 0o300022 | 0 |
| `W0323` | LABEL(md) | `include/LO_GEN.labels.md:270` | 0o300023 | 0 |
| `W0324` | LABEL(md) | `include/LO_GEN.labels.md:271` | 0o300024 | 0 |
| `W0325` | LABEL(md) | `include/LO_GEN.labels.md:272` | 0o300025 | 0 |
| `W0326` | LABEL(md) | `include/LO_GEN.labels.md:273` | 0o300026 | 0 |
| `W0327` | LABEL(md) | `include/LO_GEN.labels.md:274` | 0o300027 | 0 |
| `W0330` | LABEL(md) | `include/LO_GEN.labels.md:275` | 0o300030 | 0 |
| `W0331` | LABEL(md) | `include/LO_GEN.labels.md:276` | 0o300031 | 0 |
| `W0332` | LABEL(md) | `include/LO_GEN.labels.md:277` | 0o300032 | 0 |
| `W0333` | LABEL(md) | `include/LO_GEN.labels.md:278` | 0o300033 | 0 |
| `W0334` | LABEL(md) | `include/LO_GEN.labels.md:279` | 0o300034 | 0 |
| `W0335` | LABEL(md) | `include/LO_GEN.labels.md:280` | 0o300035 | 0 |
| `W0336` | LABEL(md) | `include/LO_GEN.labels.md:281` | 0o300036 | 0 |
| `W0337` | LABEL(md) | `include/LO_GEN.labels.md:282` | 0o300037 | 0 |
| `W0340` | LABEL(md) | `include/LO_GEN.labels.md:283` | 0o300040 | 0 |
| `W0341` | LABEL(md) | `include/LO_GEN.labels.md:284` | 0o300041 | 0 |
| `W0342` | LABEL(md) | `include/LO_GEN.labels.md:285` | 0o300042 | 0 |
| `W0343` | LABEL(md) | `include/LO_GEN.labels.md:286` | 0o300043 | 0 |
| `W0344` | LABEL(md) | `include/LO_GEN.labels.md:287` | 0o300044 | 0 |
| `W0345` | LABEL(md) | `include/LO_GEN.labels.md:288` | 0o300045 | 0 |
| `W0346` | LABEL(md) | `include/LO_GEN.labels.md:289` | 0o300046 | 0 |
| `W0347` | LABEL(md) | `include/LO_GEN.labels.md:290` | 0o300047 | 0 |
| `W0350` | LABEL(md) | `include/LO_GEN.labels.md:291` | 0o300050 | 0 |
| `W0351` | LABEL(md) | `include/LO_GEN.labels.md:292` | 0o300051 | 0 |
| `W0352` | LABEL(md) | `include/LO_GEN.labels.md:293` | 0o300052 | 0 |
| `W0353` | LABEL(md) | `include/LO_GEN.labels.md:294` | 0o300053 | 0 |
| `W0354` | LABEL(md) | `include/LO_GEN.labels.md:295` | 0o300054 | 0 |
| `W0355` | LABEL(md) | `include/LO_GEN.labels.md:296` | 0o300055 | 0 |
| `W0356` | LABEL(md) | `include/LO_GEN.labels.md:297` | 0o300056 | 0 |
| `W0357` | LABEL(md) | `include/LO_GEN.labels.md:298` | 0o300057 | 0 |
| `W0360` | LABEL(md) | `include/LO_GEN.labels.md:299` | 0o300060 | 0 |
| `W0361` | LABEL(md) | `include/LO_GEN.labels.md:300` | 0o300061 | 0 |
| `W0362` | LABEL(md) | `include/LO_GEN.labels.md:301` | 0o300062 | 0 |
| `W0363` | LABEL(md) | `include/LO_GEN.labels.md:302` | 0o300063 | 0 |
| `W0364` | LABEL(md) | `include/LO_GEN.labels.md:303` | 0o300064 | 0 |
| `W0365` | LABEL(md) | `include/LO_GEN.labels.md:304` | 0o300065 | 0 |
| `W0366` | LABEL(md) | `include/LO_GEN.labels.md:305` | 0o300066 | 0 |
| `W0367` | LABEL(md) | `include/LO_GEN.labels.md:306` | 0o300067 | 0 |
| `W0370` | LABEL(md) | `include/LO_GEN.labels.md:307` | 0o300070 | 0 |
| `W0371` | LABEL(md) | `include/LO_GEN.labels.md:308` | 0o300071 | 0 |
| `W0372` | LABEL(md) | `include/LO_GEN.labels.md:309` | 0o300072 | 0 |
| `W0373` | LABEL(md) | `include/LO_GEN.labels.md:310` | 0o300073 | 0 |
| `W0374` | LABEL(md) | `include/LO_GEN.labels.md:311` | 0o300074 | 0 |
| `W0375` | LABEL(md) | `include/LO_GEN.labels.md:312` | 0o300075 | 0 |
| `W0376` | LABEL(md) | `include/LO_GEN.labels.md:313` | 0o300076 | 0 |
| `W0377` | LABEL(md) | `include/LO_GEN.labels.md:314` | 0o300077 | 0 |
| `W0400` | LABEL(md) | `include/LO_GEN.labels.md:315` | 0o300100 | 0 |
| `W0401` | LABEL(md) | `include/LO_GEN.labels.md:316` | 0o300101 | 0 |
| `W0402` | LABEL(md) | `include/LO_GEN.labels.md:317` | 0o300102 | 0 |
| `W0403` | LABEL(md) | `include/LO_GEN.labels.md:318` | 0o300103 | 0 |
| `W0404` | LABEL(md) | `include/LO_GEN.labels.md:319` | 0o300104 | 0 |
| `W0405` | LABEL(md) | `include/LO_GEN.labels.md:320` | 0o300105 | 0 |
| `W0406` | LABEL(md) | `include/LO_GEN.labels.md:321` | 0o300106 | 0 |
| `W0407` | LABEL(md) | `include/LO_GEN.labels.md:322` | 0o300107 | 0 |
| `W0410` | LABEL(md) | `include/LO_GEN.labels.md:323` | 0o300110 | 0 |
| `W0411` | LABEL(md) | `include/LO_GEN.labels.md:324` | 0o300111 | 0 |
| `W0412` | LABEL(md) | `include/LO_GEN.labels.md:325` | 0o300112 | 0 |
| `W0413` | LABEL(md) | `include/LO_GEN.labels.md:326` | 0o300113 | 0 |
| `W0414` | LABEL(md) | `include/LO_GEN.labels.md:327` | 0o300114 | 0 |
| `W0415` | LABEL(md) | `include/LO_GEN.labels.md:328` | 0o300115 | 0 |
| `W0416` | LABEL(md) | `include/LO_GEN.labels.md:329` | 0o300116 | 0 |
| `W0417` | LABEL(md) | `include/LO_GEN.labels.md:330` | 0o300117 | 0 |
| `W0420` | LABEL(md) | `include/LO_GEN.labels.md:331` | 0o300120 | 0 |
| `W0421` | LABEL(md) | `include/LO_GEN.labels.md:332` | 0o300121 | 0 |
| `W0422` | LABEL(md) | `include/LO_GEN.labels.md:333` | 0o300122 | 0 |
| `W0423` | LABEL(md) | `include/LO_GEN.labels.md:334` | 0o300123 | 0 |
| `W0424` | LABEL(md) | `include/LO_GEN.labels.md:335` | 0o300124 | 0 |
| `W0425` | LABEL(md) | `include/LO_GEN.labels.md:336` | 0o300125 | 0 |
| `W0426` | LABEL(md) | `include/LO_GEN.labels.md:337` | 0o300126 | 0 |
| `W0427` | LABEL(md) | `include/LO_GEN.labels.md:338` | 0o300127 | 0 |
| `W0430` | LABEL(md) | `include/LO_GEN.labels.md:339` | 0o300130 | 0 |
| `W0431` | LABEL(md) | `include/LO_GEN.labels.md:340` | 0o300131 | 0 |
| `W0432` | LABEL(md) | `include/LO_GEN.labels.md:341` | 0o300132 | 0 |
| `W0433` | LABEL(md) | `include/LO_GEN.labels.md:342` | 0o300133 | 0 |
| `W0434` | LABEL(md) | `include/LO_GEN.labels.md:343` | 0o300134 | 0 |
| `W0435` | LABEL(md) | `include/LO_GEN.labels.md:344` | 0o300135 | 0 |
| `W0436` | LABEL(md) | `include/LO_GEN.labels.md:345` | 0o300136 | 0 |
| `W0437` | LABEL(md) | `include/LO_GEN.labels.md:346` | 0o300137 | 0 |
| `W0440` | LABEL(md) | `include/LO_GEN.labels.md:347` | 0o300140 | 0 |
| `W0441` | LABEL(md) | `include/LO_GEN.labels.md:348` | 0o300141 | 0 |
| `W0442` | LABEL(md) | `include/LO_GEN.labels.md:349` | 0o300142 | 0 |
| `W0443` | LABEL(md) | `include/LO_GEN.labels.md:350` | 0o300143 | 0 |
| `W0444` | LABEL(md) | `include/LO_GEN.labels.md:351` | 0o300144 | 0 |
| `W0445` | LABEL(md) | `include/LO_GEN.labels.md:352` | 0o300145 | 0 |
| `W0446` | LABEL(md) | `include/LO_GEN.labels.md:353` | 0o300146 | 0 |
| `W0447` | LABEL(md) | `include/LO_GEN.labels.md:354` | 0o300147 | 0 |
| `W0450` | LABEL(md) | `include/LO_GEN.labels.md:355` | 0o300150 | 0 |
| `W0451` | LABEL(md) | `include/LO_GEN.labels.md:356` | 0o300151 | 0 |
| `W0452` | LABEL(md) | `include/LO_GEN.labels.md:357` | 0o300152 | 0 |
| `W0453` | LABEL(md) | `include/LO_GEN.labels.md:358` | 0o300153 | 0 |
| `W0454` | LABEL(md) | `include/LO_GEN.labels.md:359` | 0o300154 | 0 |
| `W0455` | LABEL(md) | `include/LO_GEN.labels.md:360` | 0o300155 | 0 |
| `W0456` | LABEL(md) | `include/LO_GEN.labels.md:361` | 0o300156 | 0 |
| `W0457` | LABEL(md) | `include/LO_GEN.labels.md:362` | 0o300157 | 0 |
| `W0460` | LABEL(md) | `include/LO_GEN.labels.md:363` | 0o300160 | 0 |
| `W0461` | LABEL(md) | `include/LO_GEN.labels.md:364` | 0o300161 | 0 |
| `W0462` | LABEL(md) | `include/LO_GEN.labels.md:365` | 0o300162 | 0 |
| `W0463` | LABEL(md) | `include/LO_GEN.labels.md:366` | 0o300163 | 0 |
| `W0464` | LABEL(md) | `include/LO_GEN.labels.md:367` | 0o300164 | 0 |
| `W0465` | LABEL(md) | `include/LO_GEN.labels.md:368` | 0o300165 | 0 |
| `W0466` | LABEL(md) | `include/LO_GEN.labels.md:369` | 0o300166 | 0 |
| `W0467` | LABEL(md) | `include/LO_GEN.labels.md:370` | 0o300167 | 0 |
| `W0470` | LABEL(md) | `include/LO_GEN.labels.md:371` | 0o300170 | 0 |
| `W0471` | LABEL(md) | `include/LO_GEN.labels.md:372` | 0o300171 | 0 |
| `W0472` | LABEL(md) | `include/LO_GEN.labels.md:373` | 0o300172 | 0 |
| `W0473` | LABEL(md) | `include/LO_GEN.labels.md:374` | 0o300173 | 0 |
| `W0474` | LABEL(md) | `include/LO_GEN.labels.md:375` | 0o300174 | 0 |
| `W0475` | LABEL(md) | `include/LO_GEN.labels.md:376` | 0o300175 | 0 |
| `W0476` | LABEL(md) | `include/LO_GEN.labels.md:377` | 0o300176 | 0 |
| `W0477` | LABEL(md) | `include/LO_GEN.labels.md:378` | 0o300177 | 0 |
| `W0500` | LABEL(md) | `include/LO_GEN.labels.md:379` | 0o300200 | 0 |
| `W0501` | LABEL(md) | `include/LO_GEN.labels.md:380` | 0o300201 | 0 |
| `W0502` | LABEL(md) | `include/LO_GEN.labels.md:381` | 0o300202 | 0 |
| `W0503` | LABEL(md) | `include/LO_GEN.labels.md:382` | 0o300203 | 0 |
| `W0504` | LABEL(md) | `include/LO_GEN.labels.md:383` | 0o300204 | 0 |
| `W0505` | LABEL(md) | `include/LO_GEN.labels.md:384` | 0o300205 | 0 |
| `W0506` | LABEL(md) | `include/LO_GEN.labels.md:385` | 0o300206 | 0 |
| `W0507` | LABEL(md) | `include/LO_GEN.labels.md:386` | 0o300207 | 0 |
| `W0510` | LABEL(md) | `include/LO_GEN.labels.md:387` | 0o300210 | 0 |
| `W0511` | LABEL(md) | `include/LO_GEN.labels.md:388` | 0o300211 | 0 |
| `W0512` | LABEL(md) | `include/LO_GEN.labels.md:389` | 0o300212 | 0 |
| `W0513` | LABEL(md) | `include/LO_GEN.labels.md:390` | 0o300213 | 0 |
| `W0514` | LABEL(md) | `include/LO_GEN.labels.md:391` | 0o300214 | 0 |
| `W0515` | LABEL(md) | `include/LO_GEN.labels.md:392` | 0o300215 | 0 |
| `W0516` | LABEL(md) | `include/LO_GEN.labels.md:393` | 0o300216 | 0 |
| `W0517` | LABEL(md) | `include/LO_GEN.labels.md:394` | 0o300217 | 0 |
| `W0520` | LABEL(md) | `include/LO_GEN.labels.md:395` | 0o300220 | 0 |
| `W0521` | LABEL(md) | `include/LO_GEN.labels.md:396` | 0o300221 | 0 |
| `W0522` | LABEL(md) | `include/LO_GEN.labels.md:397` | 0o300222 | 0 |
| `W0523` | LABEL(md) | `include/LO_GEN.labels.md:398` | 0o300223 | 0 |
| `W0524` | LABEL(md) | `include/LO_GEN.labels.md:399` | 0o300224 | 0 |
| `W0525` | LABEL(md) | `include/LO_GEN.labels.md:400` | 0o300225 | 0 |
| `W0526` | LABEL(md) | `include/LO_GEN.labels.md:401` | 0o300226 | 0 |
| `W0527` | LABEL(md) | `include/LO_GEN.labels.md:402` | 0o300227 | 0 |
| `W0530` | LABEL(md) | `include/LO_GEN.labels.md:403` | 0o300230 | 0 |
| `W0531` | LABEL(md) | `include/LO_GEN.labels.md:404` | 0o300231 | 0 |
| `W0532` | LABEL(md) | `include/LO_GEN.labels.md:405` | 0o300232 | 0 |
| `W0533` | LABEL(md) | `include/LO_GEN.labels.md:406` | 0o300233 | 0 |
| `W0534` | LABEL(md) | `include/LO_GEN.labels.md:407` | 0o300234 | 0 |
| `W0535` | LABEL(md) | `include/LO_GEN.labels.md:408` | 0o300235 | 0 |
| `W0536` | LABEL(md) | `include/LO_GEN.labels.md:409` | 0o300236 | 0 |
| `W0537` | LABEL(md) | `include/LO_GEN.labels.md:410` | 0o300237 | 0 |
| `W0540` | LABEL(md) | `include/LO_GEN.labels.md:411` | 0o300240 | 0 |
| `W0541` | LABEL(md) | `include/LO_GEN.labels.md:412` | 0o300241 | 0 |
| `W0542` | LABEL(md) | `include/LO_GEN.labels.md:413` | 0o300242 | 0 |
| `W0543` | LABEL(md) | `include/LO_GEN.labels.md:414` | 0o300243 | 0 |
| `W0544` | LABEL(md) | `include/LO_GEN.labels.md:415` | 0o300244 | 0 |
| `W0545` | LABEL(md) | `include/LO_GEN.labels.md:416` | 0o300245 | 0 |
| `W0546` | LABEL(md) | `include/LO_GEN.labels.md:417` | 0o300246 | 0 |
| `W0547` | LABEL(md) | `include/LO_GEN.labels.md:418` | 0o300247 | 0 |
| `W0550` | LABEL(md) | `include/LO_GEN.labels.md:419` | 0o300250 | 0 |
| `W0551` | LABEL(md) | `include/LO_GEN.labels.md:420` | 0o300251 | 0 |
| `W0552` | LABEL(md) | `include/LO_GEN.labels.md:421` | 0o300252 | 0 |
| `W0553` | LABEL(md) | `include/LO_GEN.labels.md:422` | 0o300253 | 0 |
| `W0554` | LABEL(md) | `include/LO_GEN.labels.md:423` | 0o300254 | 0 |
| `W0555` | LABEL(md) | `include/LO_GEN.labels.md:424` | 0o300255 | 0 |
| `W0556` | LABEL(md) | `include/LO_GEN.labels.md:425` | 0o300256 | 0 |
| `W0557` | LABEL(md) | `include/LO_GEN.labels.md:426` | 0o300257 | 0 |
| `W0560` | LABEL(md) | `include/LO_GEN.labels.md:427` | 0o300260 | 0 |
| `W0561` | LABEL(md) | `include/LO_GEN.labels.md:428` | 0o300261 | 0 |
| `W0562` | LABEL(md) | `include/LO_GEN.labels.md:429` | 0o300262 | 0 |
| `W0563` | LABEL(md) | `include/LO_GEN.labels.md:430` | 0o300263 | 0 |
| `W0564` | LABEL(md) | `include/LO_GEN.labels.md:431` | 0o300264 | 0 |
| `W0565` | LABEL(md) | `include/LO_GEN.labels.md:432` | 0o300265 | 0 |
| `W0566` | LABEL(md) | `include/LO_GEN.labels.md:433` | 0o300266 | 0 |
| `W0567` | LABEL(md) | `include/LO_GEN.labels.md:434` | 0o300267 | 0 |
| `W0570` | LABEL(md) | `include/LO_GEN.labels.md:435` | 0o300270 | 0 |
| `W0571` | LABEL(md) | `include/LO_GEN.labels.md:436` | 0o300271 | 0 |
| `W0572` | LABEL(md) | `include/LO_GEN.labels.md:437` | 0o300272 | 0 |
| `W0573` | LABEL(md) | `include/LO_GEN.labels.md:438` | 0o300273 | 0 |
| `W0574` | LABEL(md) | `include/LO_GEN.labels.md:439` | 0o300274 | 0 |
| `W0575` | LABEL(md) | `include/LO_GEN.labels.md:440` | 0o300275 | 0 |
| `W0576` | LABEL(md) | `include/LO_GEN.labels.md:441` | 0o300276 | 0 |
| `W0577` | LABEL(md) | `include/LO_GEN.labels.md:442` | 0o300277 | 0 |
| `W0600` | LABEL(md) | `include/LO_GEN.labels.md:443` | 0o300300 | 0 |
| `W0601` | LABEL(md) | `include/LO_GEN.labels.md:444` | 0o300301 | 0 |
| `W0602` | LABEL(md) | `include/LO_GEN.labels.md:445` | 0o300302 | 0 |
| `W0603` | LABEL(md) | `include/LO_GEN.labels.md:446` | 0o300303 | 0 |
| `W0604` | LABEL(md) | `include/LO_GEN.labels.md:447` | 0o300304 | 0 |
| `W0605` | LABEL(md) | `include/LO_GEN.labels.md:448` | 0o300305 | 0 |
| `W0606` | LABEL(md) | `include/LO_GEN.labels.md:449` | 0o300306 | 0 |
| `W0607` | LABEL(md) | `include/LO_GEN.labels.md:450` | 0o300307 | 0 |
| `W0610` | LABEL(md) | `include/LO_GEN.labels.md:451` | 0o300310 | 0 |
| `W0611` | LABEL(md) | `include/LO_GEN.labels.md:452` | 0o300311 | 0 |
| `W0612` | LABEL(md) | `include/LO_GEN.labels.md:453` | 0o300312 | 0 |
| `W0613` | LABEL(md) | `include/LO_GEN.labels.md:454` | 0o300313 | 0 |
| `W0614` | LABEL(md) | `include/LO_GEN.labels.md:455` | 0o300314 | 0 |
| `W0615` | LABEL(md) | `include/LO_GEN.labels.md:456` | 0o300315 | 0 |
| `W0616` | LABEL(md) | `include/LO_GEN.labels.md:457` | 0o300316 | 0 |
| `W0617` | LABEL(md) | `include/LO_GEN.labels.md:458` | 0o300317 | 0 |
| `W0620` | LABEL(md) | `include/LO_GEN.labels.md:459` | 0o300320 | 0 |
| `W0621` | LABEL(md) | `include/LO_GEN.labels.md:460` | 0o300321 | 0 |
| `W0622` | LABEL(md) | `include/LO_GEN.labels.md:461` | 0o300322 | 0 |
| `W0623` | LABEL(md) | `include/LO_GEN.labels.md:462` | 0o300323 | 0 |
| `W0624` | LABEL(md) | `include/LO_GEN.labels.md:463` | 0o300324 | 0 |
| `W0625` | LABEL(md) | `include/LO_GEN.labels.md:464` | 0o300325 | 0 |
| `W0626` | LABEL(md) | `include/LO_GEN.labels.md:465` | 0o300326 | 0 |
| `W0627` | LABEL(md) | `include/LO_GEN.labels.md:466` | 0o300327 | 0 |
| `W0630` | LABEL(md) | `include/LO_GEN.labels.md:467` | 0o300330 | 0 |
| `W0631` | LABEL(md) | `include/LO_GEN.labels.md:468` | 0o300331 | 0 |
| `W0632` | LABEL(md) | `include/LO_GEN.labels.md:469` | 0o300332 | 0 |
| `W0633` | LABEL(md) | `include/LO_GEN.labels.md:470` | 0o300333 | 0 |
| `W0634` | LABEL(md) | `include/LO_GEN.labels.md:471` | 0o300334 | 0 |
| `W0635` | LABEL(md) | `include/LO_GEN.labels.md:472` | 0o300335 | 0 |
| `W0636` | LABEL(md) | `include/LO_GEN.labels.md:473` | 0o300336 | 0 |
| `W0637` | LABEL(md) | `include/LO_GEN.labels.md:474` | 0o300337 | 0 |
| `W0640` | LABEL(md) | `include/LO_GEN.labels.md:475` | 0o300340 | 0 |
| `W0641` | LABEL(md) | `include/LO_GEN.labels.md:476` | 0o300341 | 0 |
| `W0642` | LABEL(md) | `include/LO_GEN.labels.md:477` | 0o300342 | 0 |
| `W0643` | LABEL(md) | `include/LO_GEN.labels.md:478` | 0o300343 | 0 |
| `W0644` | LABEL(md) | `include/LO_GEN.labels.md:479` | 0o300344 | 0 |
| `W0645` | LABEL(md) | `include/LO_GEN.labels.md:480` | 0o300345 | 0 |
| `W0646` | LABEL(md) | `include/LO_GEN.labels.md:481` | 0o300346 | 0 |
| `W0647` | LABEL(md) | `include/LO_GEN.labels.md:482` | 0o300347 | 0 |
| `W0650` | LABEL(md) | `include/LO_GEN.labels.md:483` | 0o300350 | 0 |
| `W0651` | LABEL(md) | `include/LO_GEN.labels.md:484` | 0o300351 | 0 |
| `W0652` | LABEL(md) | `include/LO_GEN.labels.md:485` | 0o300352 | 0 |
| `W0653` | LABEL(md) | `include/LO_GEN.labels.md:486` | 0o300353 | 0 |
| `W0654` | LABEL(md) | `include/LO_GEN.labels.md:487` | 0o300354 | 0 |
| `W0655` | LABEL(md) | `include/LO_GEN.labels.md:488` | 0o300355 | 0 |
| `W0656` | LABEL(md) | `include/LO_GEN.labels.md:489` | 0o300356 | 0 |
| `W0657` | LABEL(md) | `include/LO_GEN.labels.md:490` | 0o300357 | 0 |
| `W0660` | LABEL(md) | `include/LO_GEN.labels.md:491` | 0o300360 | 0 |
| `W0661` | LABEL(md) | `include/LO_GEN.labels.md:492` | 0o300361 | 0 |
| `W0662` | LABEL(md) | `include/LO_GEN.labels.md:493` | 0o300362 | 0 |
| `W0663` | LABEL(md) | `include/LO_GEN.labels.md:494` | 0o300363 | 0 |
| `W0664` | LABEL(md) | `include/LO_GEN.labels.md:495` | 0o300364 | 0 |
| `W0665` | LABEL(md) | `include/LO_GEN.labels.md:496` | 0o300365 | 0 |
| `W0666` | LABEL(md) | `include/LO_GEN.labels.md:497` | 0o300366 | 0 |
| `W0667` | LABEL(md) | `include/LO_GEN.labels.md:498` | 0o300367 | 0 |
| `W0670` | LABEL(md) | `include/LO_GEN.labels.md:499` | 0o300370 | 0 |
| `W0671` | LABEL(md) | `include/LO_GEN.labels.md:500` | 0o300371 | 0 |
| `W0672` | LABEL(md) | `include/LO_GEN.labels.md:501` | 0o300372 | 0 |
| `W0673` | LABEL(md) | `include/LO_GEN.labels.md:502` | 0o300373 | 0 |
| `W0674` | LABEL(md) | `include/LO_GEN.labels.md:503` | 0o300374 | 0 |
| `W0675` | LABEL(md) | `include/LO_GEN.labels.md:504` | 0o300375 | 0 |
| `W0676` | LABEL(md) | `include/LO_GEN.labels.md:505` | 0o300376 | 0 |
| `W0677` | LABEL(md) | `include/LO_GEN.labels.md:506` | 0o300377 | 0 |
| `W0700` | LABEL(md) | `include/LO_GEN.labels.md:507` | 0o300400 | 0 |
| `W0701` | LABEL(md) | `include/LO_GEN.labels.md:508` | 0o300401 | 0 |
| `W0702` | LABEL(md) | `include/LO_GEN.labels.md:509` | 0o300402 | 0 |
| `W0703` | LABEL(md) | `include/LO_GEN.labels.md:510` | 0o300403 | 0 |
| `W0704` | LABEL(md) | `include/LO_GEN.labels.md:511` | 0o300404 | 0 |
| `W0705` | LABEL(md) | `include/LO_GEN.labels.md:512` | 0o300405 | 0 |
| `W0706` | LABEL(md) | `include/LO_GEN.labels.md:513` | 0o300406 | 0 |
| `W0707` | LABEL(md) | `include/LO_GEN.labels.md:514` | 0o300407 | 0 |
| `W0710` | LABEL(md) | `include/LO_GEN.labels.md:515` | 0o300410 | 0 |
| `W0711` | LABEL(md) | `include/LO_GEN.labels.md:516` | 0o300411 | 0 |
| `W0712` | LABEL(md) | `include/LO_GEN.labels.md:517` | 0o300412 | 0 |
| `W0713` | LABEL(md) | `include/LO_GEN.labels.md:518` | 0o300413 | 0 |
| `W0714` | LABEL(md) | `include/LO_GEN.labels.md:519` | 0o300414 | 0 |
| `W0715` | LABEL(md) | `include/LO_GEN.labels.md:520` | 0o300415 | 0 |
| `W0716` | LABEL(md) | `include/LO_GEN.labels.md:521` | 0o300416 | 0 |
| `W0717` | LABEL(md) | `include/LO_GEN.labels.md:522` | 0o300417 | 0 |
| `W0720` | LABEL(md) | `include/LO_GEN.labels.md:523` | 0o300420 | 0 |
| `W0721` | LABEL(md) | `include/LO_GEN.labels.md:524` | 0o300421 | 0 |
| `W0722` | LABEL(md) | `include/LO_GEN.labels.md:525` | 0o300422 | 0 |
| `W0723` | LABEL(md) | `include/LO_GEN.labels.md:526` | 0o300423 | 0 |
| `W0724` | LABEL(md) | `include/LO_GEN.labels.md:527` | 0o300424 | 0 |
| `W0725` | LABEL(md) | `include/LO_GEN.labels.md:528` | 0o300425 | 0 |
| `W0726` | LABEL(md) | `include/LO_GEN.labels.md:529` | 0o300426 | 0 |
| `W0727` | LABEL(md) | `include/LO_GEN.labels.md:530` | 0o300427 | 0 |
| `W0730` | LABEL(md) | `include/LO_GEN.labels.md:531` | 0o300430 | 0 |
| `W0731` | LABEL(md) | `include/LO_GEN.labels.md:532` | 0o300431 | 0 |
| `W0732` | LABEL(md) | `include/LO_GEN.labels.md:533` | 0o300432 | 0 |
| `W0733` | LABEL(md) | `include/LO_GEN.labels.md:534` | 0o300433 | 0 |
| `W0734` | LABEL(md) | `include/LO_GEN.labels.md:535` | 0o300434 | 0 |
| `W0735` | LABEL(md) | `include/LO_GEN.labels.md:536` | 0o300435 | 0 |
| `W0736` | LABEL(md) | `include/LO_GEN.labels.md:537` | 0o300436 | 0 |
| `W0737` | LABEL(md) | `include/LO_GEN.labels.md:538` | 0o300437 | 0 |
| `W0740` | LABEL(md) | `include/LO_GEN.labels.md:539` | 0o300440 | 0 |
| `W0741` | LABEL(md) | `include/LO_GEN.labels.md:540` | 0o300441 | 0 |
| `W0742` | LABEL(md) | `include/LO_GEN.labels.md:541` | 0o300442 | 0 |
| `W0743` | LABEL(md) | `include/LO_GEN.labels.md:542` | 0o300443 | 0 |
| `W0744` | LABEL(md) | `include/LO_GEN.labels.md:543` | 0o300444 | 0 |
| `W0745` | LABEL(md) | `include/LO_GEN.labels.md:544` | 0o300445 | 0 |
| `W0746` | LABEL(md) | `include/LO_GEN.labels.md:545` | 0o300446 | 0 |
| `W0747` | LABEL(md) | `include/LO_GEN.labels.md:546` | 0o300447 | 0 |
| `W0750` | LABEL(md) | `include/LO_GEN.labels.md:547` | 0o300450 | 0 |
| `W0751` | LABEL(md) | `include/LO_GEN.labels.md:548` | 0o300451 | 0 |
| `W0752` | LABEL(md) | `include/LO_GEN.labels.md:549` | 0o300452 | 0 |
| `W0753` | LABEL(md) | `include/LO_GEN.labels.md:550` | 0o300453 | 0 |
| `W0754` | LABEL(md) | `include/LO_GEN.labels.md:551` | 0o300454 | 0 |
| `W0755` | LABEL(md) | `include/LO_GEN.labels.md:552` | 0o300455 | 0 |
| `W0756` | LABEL(md) | `include/LO_GEN.labels.md:553` | 0o300456 | 0 |
| `W0757` | LABEL(md) | `include/LO_GEN.labels.md:554` | 0o300457 | 0 |
| `W0760` | LABEL(md) | `include/LO_GEN.labels.md:555` | 0o300460 | 0 |
| `W0761` | LABEL(md) | `include/LO_GEN.labels.md:556` | 0o300461 | 0 |
| `W0762` | LABEL(md) | `include/LO_GEN.labels.md:557` | 0o300462 | 0 |
| `W0763` | LABEL(md) | `include/LO_GEN.labels.md:558` | 0o300463 | 0 |
| `W0764` | LABEL(md) | `include/LO_GEN.labels.md:559` | 0o300464 | 0 |
| `W0765` | LABEL(md) | `include/LO_GEN.labels.md:560` | 0o300465 | 0 |
| `W0766` | LABEL(md) | `include/LO_GEN.labels.md:561` | 0o300466 | 0 |
| `W0767` | LABEL(md) | `include/LO_GEN.labels.md:562` | 0o300467 | 0 |
| `W0770` | LABEL(md) | `include/LO_GEN.labels.md:563` | 0o300470 | 0 |
| `W0771` | LABEL(md) | `include/LO_GEN.labels.md:564` | 0o300471 | 0 |
| `W0772` | LABEL(md) | `include/LO_GEN.labels.md:565` | 0o300472 | 0 |
| `W0773` | LABEL(md) | `include/LO_GEN.labels.md:566` | 0o300473 | 0 |
| `W0774` | LABEL(md) | `include/LO_GEN.labels.md:567` | 0o300474 | 0 |
| `W0775` | LABEL(md) | `include/LO_GEN.labels.md:568` | 0o300475 | 0 |
| `W0776` | LABEL(md) | `include/LO_GEN.labels.md:569` | 0o300476 | 0 |
| `W0777` | LABEL(md) | `include/LO_GEN.labels.md:570` | 0o300477 | 0 |
| `W1000` | LABEL(md) | `include/LO_GEN.labels.md:571` | 0o300500 | 0 |
| `W1001` | LABEL(md) | `include/LO_GEN.labels.md:572` | 0o300501 | 0 |
| `W1002` | LABEL(md) | `include/LO_GEN.labels.md:573` | 0o300502 | 0 |
| `W1003` | LABEL(md) | `include/LO_GEN.labels.md:574` | 0o300503 | 0 |
| `W1004` | LABEL(md) | `include/LO_GEN.labels.md:575` | 0o300504 | 0 |
| `W1005` | LABEL(md) | `include/LO_GEN.labels.md:576` | 0o300505 | 0 |
| `W1006` | LABEL(md) | `include/LO_GEN.labels.md:577` | 0o300506 | 0 |
| `W1007` | LABEL(md) | `include/LO_GEN.labels.md:578` | 0o300507 | 0 |
| `W1010` | LABEL(md) | `include/LO_GEN.labels.md:579` | 0o300510 | 0 |
| `W1011` | LABEL(md) | `include/LO_GEN.labels.md:580` | 0o300511 | 0 |
| `W1012` | LABEL(md) | `include/LO_GEN.labels.md:581` | 0o300512 | 0 |
| `W1013` | LABEL(md) | `include/LO_GEN.labels.md:582` | 0o300513 | 0 |
| `W1014` | LABEL(md) | `include/LO_GEN.labels.md:583` | 0o300514 | 0 |
| `W1015` | LABEL(md) | `include/LO_GEN.labels.md:584` | 0o300515 | 0 |
| `W1016` | LABEL(md) | `include/LO_GEN.labels.md:585` | 0o300516 | 0 |
| `W1017` | LABEL(md) | `include/LO_GEN.labels.md:586` | 0o300517 | 0 |
| `W1020` | LABEL(md) | `include/LO_GEN.labels.md:587` | 0o300520 | 0 |
| `W1021` | LABEL(md) | `include/LO_GEN.labels.md:588` | 0o300521 | 0 |
| `W1022` | LABEL(md) | `include/LO_GEN.labels.md:589` | 0o300522 | 0 |
| `W1023` | LABEL(md) | `include/LO_GEN.labels.md:590` | 0o300523 | 0 |
| `W1024` | LABEL(md) | `include/LO_GEN.labels.md:591` | 0o300524 | 0 |
| `W1025` | LABEL(md) | `include/LO_GEN.labels.md:592` | 0o300525 | 0 |
| `W1026` | LABEL(md) | `include/LO_GEN.labels.md:593` | 0o300526 | 0 |
| `W1027` | LABEL(md) | `include/LO_GEN.labels.md:594` | 0o300527 | 0 |
| `W1030` | LABEL(md) | `include/LO_GEN.labels.md:595` | 0o300530 | 0 |
| `W1031` | LABEL(md) | `include/LO_GEN.labels.md:596` | 0o300531 | 0 |
| `W1032` | LABEL(md) | `include/LO_GEN.labels.md:597` | 0o300532 | 0 |
| `W1033` | LABEL(md) | `include/LO_GEN.labels.md:598` | 0o300533 | 0 |
| `W1034` | LABEL(md) | `include/LO_GEN.labels.md:599` | 0o300534 | 0 |
| `W1035` | LABEL(md) | `include/LO_GEN.labels.md:600` | 0o300535 | 0 |
| `W1036` | LABEL(md) | `include/LO_GEN.labels.md:601` | 0o300536 | 0 |
| `W1037` | LABEL(md) | `include/LO_GEN.labels.md:602` | 0o300537 | 0 |
| `W1040` | LABEL(md) | `include/LO_GEN.labels.md:603` | 0o300540 | 0 |
| `W1041` | LABEL(md) | `include/LO_GEN.labels.md:604` | 0o300541 | 0 |
| `W1042` | LABEL(md) | `include/LO_GEN.labels.md:605` | 0o300542 | 0 |
| `W1043` | LABEL(md) | `include/LO_GEN.labels.md:606` | 0o300543 | 0 |
| `W1044` | LABEL(md) | `include/LO_GEN.labels.md:607` | 0o300544 | 0 |
| `W1045` | LABEL(md) | `include/LO_GEN.labels.md:608` | 0o300545 | 0 |
| `W1046` | LABEL(md) | `include/LO_GEN.labels.md:609` | 0o300546 | 0 |
| `W1047` | LABEL(md) | `include/LO_GEN.labels.md:610` | 0o300547 | 0 |
| `W1050` | LABEL(md) | `include/LO_GEN.labels.md:611` | 0o300550 | 0 |
| `W1051` | LABEL(md) | `include/LO_GEN.labels.md:612` | 0o300551 | 0 |
| `W1052` | LABEL(md) | `include/LO_GEN.labels.md:613` | 0o300552 | 0 |
| `W1053` | LABEL(md) | `include/LO_GEN.labels.md:614` | 0o300553 | 0 |
| `W1054` | LABEL(md) | `include/LO_GEN.labels.md:615` | 0o300554 | 0 |
| `W1055` | LABEL(md) | `include/LO_GEN.labels.md:616` | 0o300555 | 0 |
| `W1056` | LABEL(md) | `include/LO_GEN.labels.md:617` | 0o300556 | 0 |
| `W1057` | LABEL(md) | `include/LO_GEN.labels.md:618` | 0o300557 | 0 |
| `W1060` | LABEL(md) | `include/LO_GEN.labels.md:619` | 0o300560 | 0 |
| `W1061` | LABEL(md) | `include/LO_GEN.labels.md:620` | 0o300561 | 0 |
| `W1062` | LABEL(md) | `include/LO_GEN.labels.md:621` | 0o300562 | 0 |
| `W1063` | LABEL(md) | `include/LO_GEN.labels.md:622` | 0o300563 | 0 |
| `W1064` | LABEL(md) | `include/LO_GEN.labels.md:623` | 0o300564 | 0 |
| `W1065` | LABEL(md) | `include/LO_GEN.labels.md:624` | 0o300565 | 0 |
| `W1066` | LABEL(md) | `include/LO_GEN.labels.md:625` | 0o300566 | 0 |
| `W1067` | LABEL(md) | `include/LO_GEN.labels.md:626` | 0o300567 | 0 |
| `W1070` | LABEL(md) | `include/LO_GEN.labels.md:627` | 0o300570 | 0 |
| `W1071` | LABEL(md) | `include/LO_GEN.labels.md:628` | 0o300571 | 0 |
| `W1072` | LABEL(md) | `include/LO_GEN.labels.md:629` | 0o300572 | 0 |
| `W1073` | LABEL(md) | `include/LO_GEN.labels.md:630` | 0o300573 | 0 |
| `W1074` | LABEL(md) | `include/LO_GEN.labels.md:631` | 0o300574 | 0 |
| `W1075` | LABEL(md) | `include/LO_GEN.labels.md:632` | 0o300575 | 0 |
| `W1076` | LABEL(md) | `include/LO_GEN.labels.md:633` | 0o300576 | 0 |
| `W1077` | LABEL(md) | `include/LO_GEN.labels.md:634` | 0o300577 | 0 |
| `W1100` | LABEL(md) | `include/LO_GEN.labels.md:635` | 0o300600 | 0 |
| `W1101` | LABEL(md) | `include/LO_GEN.labels.md:636` | 0o300601 | 0 |
| `W1102` | LABEL(md) | `include/LO_GEN.labels.md:637` | 0o300602 | 0 |
| `W1103` | LABEL(md) | `include/LO_GEN.labels.md:638` | 0o300603 | 0 |
| `W1104` | LABEL(md) | `include/LO_GEN.labels.md:639` | 0o300604 | 0 |
| `W1105` | LABEL(md) | `include/LO_GEN.labels.md:640` | 0o300605 | 0 |
| `W1106` | LABEL(md) | `include/LO_GEN.labels.md:641` | 0o300606 | 0 |
| `W1107` | LABEL(md) | `include/LO_GEN.labels.md:642` | 0o300607 | 0 |
| `W1110` | LABEL(md) | `include/LO_GEN.labels.md:643` | 0o300610 | 0 |
| `W1111` | LABEL(md) | `include/LO_GEN.labels.md:644` | 0o300611 | 0 |
| `W1112` | LABEL(md) | `include/LO_GEN.labels.md:645` | 0o300612 | 0 |
| `W1113` | LABEL(md) | `include/LO_GEN.labels.md:646` | 0o300613 | 0 |
| `W1114` | LABEL(md) | `include/LO_GEN.labels.md:647` | 0o300614 | 0 |
| `W1115` | LABEL(md) | `include/LO_GEN.labels.md:648` | 0o300615 | 0 |
| `W1116` | LABEL(md) | `include/LO_GEN.labels.md:649` | 0o300616 | 0 |
| `W1117` | LABEL(md) | `include/LO_GEN.labels.md:650` | 0o300617 | 0 |
| `W1120` | LABEL(md) | `include/LO_GEN.labels.md:651` | 0o300620 | 0 |
| `W1121` | LABEL(md) | `include/LO_GEN.labels.md:652` | 0o300621 | 0 |
| `W1122` | LABEL(md) | `include/LO_GEN.labels.md:653` | 0o300622 | 0 |
| `W1123` | LABEL(md) | `include/LO_GEN.labels.md:654` | 0o300623 | 0 |
| `W1124` | LABEL(md) | `include/LO_GEN.labels.md:655` | 0o300624 | 0 |
| `W1125` | LABEL(md) | `include/LO_GEN.labels.md:656` | 0o300625 | 0 |
| `W1126` | LABEL(md) | `include/LO_GEN.labels.md:657` | 0o300626 | 0 |
| `W1127` | LABEL(md) | `include/LO_GEN.labels.md:658` | 0o300627 | 0 |
| `W1130` | LABEL(md) | `include/LO_GEN.labels.md:659` | 0o300630 | 0 |
| `W1131` | LABEL(md) | `include/LO_GEN.labels.md:660` | 0o300631 | 0 |
| `W1132` | LABEL(md) | `include/LO_GEN.labels.md:661` | 0o300632 | 0 |
| `W1133` | LABEL(md) | `include/LO_GEN.labels.md:662` | 0o300633 | 0 |
| `W1134` | LABEL(md) | `include/LO_GEN.labels.md:663` | 0o300634 | 0 |
| `W1135` | LABEL(md) | `include/LO_GEN.labels.md:664` | 0o300635 | 0 |
| `W1136` | LABEL(md) | `include/LO_GEN.labels.md:665` | 0o300636 | 0 |
| `W1137` | LABEL(md) | `include/LO_GEN.labels.md:666` | 0o300637 | 0 |
| `W1140` | LABEL(md) | `include/LO_GEN.labels.md:667` | 0o300640 | 0 |
| `W1141` | LABEL(md) | `include/LO_GEN.labels.md:668` | 0o300641 | 0 |
| `W1142` | LABEL(md) | `include/LO_GEN.labels.md:669` | 0o300642 | 0 |
| `W1143` | LABEL(md) | `include/LO_GEN.labels.md:670` | 0o300643 | 0 |
| `W1144` | LABEL(md) | `include/LO_GEN.labels.md:671` | 0o300644 | 0 |
| `W1145` | LABEL(md) | `include/LO_GEN.labels.md:672` | 0o300645 | 0 |
| `W1146` | LABEL(md) | `include/LO_GEN.labels.md:673` | 0o300646 | 0 |
| `W1147` | LABEL(md) | `include/LO_GEN.labels.md:674` | 0o300647 | 0 |
| `W1150` | LABEL(md) | `include/LO_GEN.labels.md:675` | 0o300650 | 0 |
| `W1151` | LABEL(md) | `include/LO_GEN.labels.md:676` | 0o300651 | 0 |
| `W1152` | LABEL(md) | `include/LO_GEN.labels.md:677` | 0o300652 | 0 |
| `W1153` | LABEL(md) | `include/LO_GEN.labels.md:678` | 0o300653 | 0 |
| `W1154` | LABEL(md) | `include/LO_GEN.labels.md:679` | 0o300654 | 0 |
| `W1155` | LABEL(md) | `include/LO_GEN.labels.md:680` | 0o300655 | 0 |
| `W1156` | LABEL(md) | `include/LO_GEN.labels.md:681` | 0o300656 | 0 |
| `W1157` | LABEL(md) | `include/LO_GEN.labels.md:682` | 0o300657 | 0 |
| `W1160` | LABEL(md) | `include/LO_GEN.labels.md:683` | 0o300660 | 0 |
| `W1161` | LABEL(md) | `include/LO_GEN.labels.md:684` | 0o300661 | 0 |
| `W1162` | LABEL(md) | `include/LO_GEN.labels.md:685` | 0o300662 | 0 |
| `W1163` | LABEL(md) | `include/LO_GEN.labels.md:686` | 0o300663 | 0 |
| `W1164` | LABEL(md) | `include/LO_GEN.labels.md:687` | 0o300664 | 0 |
| `W1165` | LABEL(md) | `include/LO_GEN.labels.md:688` | 0o300665 | 0 |
| `W1166` | LABEL(md) | `include/LO_GEN.labels.md:689` | 0o300666 | 0 |
| `W1167` | LABEL(md) | `include/LO_GEN.labels.md:690` | 0o300667 | 0 |
| `W1170` | LABEL(md) | `include/LO_GEN.labels.md:691` | 0o300670 | 0 |
| `W1171` | LABEL(md) | `include/LO_GEN.labels.md:692` | 0o300671 | 0 |
| `W1172` | LABEL(md) | `include/LO_GEN.labels.md:693` | 0o300672 | 0 |
| `W1173` | LABEL(md) | `include/LO_GEN.labels.md:694` | 0o300673 | 0 |
| `W1174` | LABEL(md) | `include/LO_GEN.labels.md:695` | 0o300674 | 0 |
| `W1175` | LABEL(md) | `include/LO_GEN.labels.md:696` | 0o300675 | 0 |
| `W1176` | LABEL(md) | `include/LO_GEN.labels.md:697` | 0o300676 | 0 |
| `W1177` | LABEL(md) | `include/LO_GEN.labels.md:698` | 0o300677 | 0 |
| `W1200` | LABEL(md) | `include/LO_GEN.labels.md:699` | 0o300700 | 0 |
| `W1201` | LABEL(md) | `include/LO_GEN.labels.md:700` | 0o300701 | 0 |
| `W1202` | LABEL(md) | `include/LO_GEN.labels.md:701` | 0o300702 | 0 |
| `W1203` | LABEL(md) | `include/LO_GEN.labels.md:702` | 0o300703 | 0 |
| `W1204` | LABEL(md) | `include/LO_GEN.labels.md:703` | 0o300704 | 0 |
| `W1205` | LABEL(md) | `include/LO_GEN.labels.md:704` | 0o300705 | 0 |
| `W1206` | LABEL(md) | `include/LO_GEN.labels.md:705` | 0o300706 | 0 |
| `W1207` | LABEL(md) | `include/LO_GEN.labels.md:706` | 0o300707 | 0 |
| `W1210` | LABEL(md) | `include/LO_GEN.labels.md:707` | 0o300710 | 0 |
| `W1211` | LABEL(md) | `include/LO_GEN.labels.md:708` | 0o300711 | 0 |
| `W1212` | LABEL(md) | `include/LO_GEN.labels.md:709` | 0o300712 | 0 |
| `W1213` | LABEL(md) | `include/LO_GEN.labels.md:710` | 0o300713 | 0 |
| `W1214` | LABEL(md) | `include/LO_GEN.labels.md:711` | 0o300714 | 0 |
| `W1215` | LABEL(md) | `include/LO_GEN.labels.md:712` | 0o300715 | 0 |
| `W1216` | LABEL(md) | `include/LO_GEN.labels.md:713` | 0o300716 | 0 |
| `W1217` | LABEL(md) | `include/LO_GEN.labels.md:714` | 0o300717 | 0 |
| `W1220` | LABEL(md) | `include/LO_GEN.labels.md:715` | 0o300720 | 0 |
| `W1221` | LABEL(md) | `include/LO_GEN.labels.md:716` | 0o300721 | 0 |
| `W1222` | LABEL(md) | `include/LO_GEN.labels.md:717` | 0o300722 | 0 |
| `W1223` | LABEL(md) | `include/LO_GEN.labels.md:718` | 0o300723 | 0 |
| `W1224` | LABEL(md) | `include/LO_GEN.labels.md:719` | 0o300724 | 0 |
| `W1225` | LABEL(md) | `include/LO_GEN.labels.md:720` | 0o300725 | 0 |
| `W1226` | LABEL(md) | `include/LO_GEN.labels.md:721` | 0o300726 | 0 |
| `W1227` | LABEL(md) | `include/LO_GEN.labels.md:722` | 0o300727 | 0 |
| `W1230` | LABEL(md) | `include/LO_GEN.labels.md:723` | 0o300730 | 0 |
| `W1231` | LABEL(md) | `include/LO_GEN.labels.md:724` | 0o300731 | 0 |
| `W1232` | LABEL(md) | `include/LO_GEN.labels.md:725` | 0o300732 | 0 |
| `W1233` | LABEL(md) | `include/LO_GEN.labels.md:726` | 0o300733 | 0 |
| `W1234` | LABEL(md) | `include/LO_GEN.labels.md:727` | 0o300734 | 0 |
| `W1235` | LABEL(md) | `include/LO_GEN.labels.md:728` | 0o300735 | 0 |
| `W1236` | LABEL(md) | `include/LO_GEN.labels.md:729` | 0o300736 | 0 |
| `W1237` | LABEL(md) | `include/LO_GEN.labels.md:730` | 0o300737 | 0 |
| `W1240` | LABEL(md) | `include/LO_GEN.labels.md:731` | 0o300740 | 0 |
| `W1241` | LABEL(md) | `include/LO_GEN.labels.md:732` | 0o300741 | 0 |
| `W1242` | LABEL(md) | `include/LO_GEN.labels.md:733` | 0o300742 | 0 |
| `W1243` | LABEL(md) | `include/LO_GEN.labels.md:734` | 0o300743 | 0 |
| `W1244` | LABEL(md) | `include/LO_GEN.labels.md:735` | 0o300744 | 0 |
| `W1245` | LABEL(md) | `include/LO_GEN.labels.md:736` | 0o300745 | 0 |
| `W1246` | LABEL(md) | `include/LO_GEN.labels.md:737` | 0o300746 | 0 |
| `W1247` | LABEL(md) | `include/LO_GEN.labels.md:738` | 0o300747 | 0 |
| `W1250` | LABEL(md) | `include/LO_GEN.labels.md:739` | 0o300750 | 0 |
| `W1251` | LABEL(md) | `include/LO_GEN.labels.md:740` | 0o300751 | 0 |
| `W1252` | LABEL(md) | `include/LO_GEN.labels.md:741` | 0o300752 | 0 |
| `W1253` | LABEL(md) | `include/LO_GEN.labels.md:742` | 0o300753 | 0 |
| `W1254` | LABEL(md) | `include/LO_GEN.labels.md:743` | 0o300754 | 0 |
| `W1255` | LABEL(md) | `include/LO_GEN.labels.md:744` | 0o300755 | 0 |
| `W1256` | LABEL(md) | `include/LO_GEN.labels.md:745` | 0o300756 | 0 |
| `W1257` | LABEL(md) | `include/LO_GEN.labels.md:746` | 0o300757 | 0 |
| `W1260` | LABEL(md) | `include/LO_GEN.labels.md:747` | 0o300760 | 0 |
| `W1261` | LABEL(md) | `include/LO_GEN.labels.md:748` | 0o300761 | 0 |
| `W1262` | LABEL(md) | `include/LO_GEN.labels.md:749` | 0o300762 | 0 |
| `W1263` | LABEL(md) | `include/LO_GEN.labels.md:750` | 0o300763 | 0 |
| `W1264` | LABEL(md) | `include/LO_GEN.labels.md:751` | 0o300764 | 0 |
| `W1265` | LABEL(md) | `include/LO_GEN.labels.md:752` | 0o300765 | 0 |
| `W1266` | LABEL(md) | `include/LO_GEN.labels.md:753` | 0o300766 | 0 |
| `W1267` | LABEL(md) | `include/LO_GEN.labels.md:754` | 0o300767 | 0 |
| `W1270` | LABEL(md) | `include/LO_GEN.labels.md:755` | 0o300770 | 0 |
| `W1271` | LABEL(md) | `include/LO_GEN.labels.md:756` | 0o300771 | 0 |
| `W1272` | LABEL(md) | `include/LO_GEN.labels.md:757` | 0o300772 | 0 |
| `W1273` | LABEL(md) | `include/LO_GEN.labels.md:758` | 0o300773 | 0 |
| `W1274` | LABEL(md) | `include/LO_GEN.labels.md:759` | 0o300774 | 0 |
| `W1275` | LABEL(md) | `include/LO_GEN.labels.md:760` | 0o300775 | 0 |
| `W1276` | LABEL(md) | `include/LO_GEN.labels.md:761` | 0o300776 | 0 |
| `W1277` | LABEL(md) | `include/LO_GEN.labels.md:762` | 0o300777 | 0 |
| `W1300` | LABEL(md) | `include/LO_GEN.labels.md:763` | 0o301000 | 0 |
| `W1301` | LABEL(md) | `include/LO_GEN.labels.md:764` | 0o301001 | 0 |
| `W1302` | LABEL(md) | `include/LO_GEN.labels.md:765` | 0o301002 | 0 |
| `W1303` | LABEL(md) | `include/LO_GEN.labels.md:766` | 0o301003 | 0 |
| `W1304` | LABEL(md) | `include/LO_GEN.labels.md:767` | 0o301004 | 0 |
| `W1305` | LABEL(md) | `include/LO_GEN.labels.md:768` | 0o301005 | 0 |
| `W1306` | LABEL(md) | `include/LO_GEN.labels.md:769` | 0o301006 | 0 |
| `W1307` | LABEL(md) | `include/LO_GEN.labels.md:770` | 0o301007 | 0 |
| `W1310` | LABEL(md) | `include/LO_GEN.labels.md:771` | 0o301010 | 0 |
| `W1311` | LABEL(md) | `include/LO_GEN.labels.md:772` | 0o301011 | 0 |
| `W1312` | LABEL(md) | `include/LO_GEN.labels.md:773` | 0o301012 | 0 |
| `W1313` | LABEL(md) | `include/LO_GEN.labels.md:774` | 0o301013 | 0 |
| `W1314` | LABEL(md) | `include/LO_GEN.labels.md:775` | 0o301014 | 0 |
| `W1315` | LABEL(md) | `include/LO_GEN.labels.md:776` | 0o301015 | 0 |
| `W1316` | LABEL(md) | `include/LO_GEN.labels.md:777` | 0o301016 | 0 |
| `W1317` | LABEL(md) | `include/LO_GEN.labels.md:778` | 0o301017 | 0 |
| `W1320` | LABEL(md) | `include/LO_GEN.labels.md:779` | 0o301020 | 0 |
| `W1321` | LABEL(md) | `include/LO_GEN.labels.md:780` | 0o301021 | 0 |
| `W1322` | LABEL(md) | `include/LO_GEN.labels.md:781` | 0o301022 | 0 |
| `W1323` | LABEL(md) | `include/LO_GEN.labels.md:782` | 0o301023 | 0 |
| `W1324` | LABEL(md) | `include/LO_GEN.labels.md:783` | 0o301024 | 0 |
| `W1325` | LABEL(md) | `include/LO_GEN.labels.md:784` | 0o301025 | 0 |
| `W1326` | LABEL(md) | `include/LO_GEN.labels.md:785` | 0o301026 | 0 |
| `W1327` | LABEL(md) | `include/LO_GEN.labels.md:786` | 0o301027 | 0 |
| `W1330` | LABEL(md) | `include/LO_GEN.labels.md:787` | 0o301030 | 0 |
| `W1331` | LABEL(md) | `include/LO_GEN.labels.md:788` | 0o301031 | 0 |
| `W1332` | LABEL(md) | `include/LO_GEN.labels.md:789` | 0o301032 | 0 |
| `W1333` | LABEL(md) | `include/LO_GEN.labels.md:790` | 0o301033 | 0 |
| `W1334` | LABEL(md) | `include/LO_GEN.labels.md:791` | 0o301034 | 0 |
| `W1335` | LABEL(md) | `include/LO_GEN.labels.md:792` | 0o301035 | 0 |
| `W1336` | LABEL(md) | `include/LO_GEN.labels.md:793` | 0o301036 | 0 |
| `W1337` | LABEL(md) | `include/LO_GEN.labels.md:794` | 0o301037 | 0 |
| `W1340` | LABEL(md) | `include/LO_GEN.labels.md:795` | 0o301040 | 0 |
| `W1341` | LABEL(md) | `include/LO_GEN.labels.md:796` | 0o301041 | 0 |
| `W1342` | LABEL(md) | `include/LO_GEN.labels.md:797` | 0o301042 | 0 |
| `W1343` | LABEL(md) | `include/LO_GEN.labels.md:798` | 0o301043 | 0 |
| `W1344` | LABEL(md) | `include/LO_GEN.labels.md:799` | 0o301044 | 0 |
| `W1345` | LABEL(md) | `include/LO_GEN.labels.md:800` | 0o301045 | 0 |
| `W1346` | LABEL(md) | `include/LO_GEN.labels.md:801` | 0o301046 | 0 |
| `W1347` | LABEL(md) | `include/LO_GEN.labels.md:802` | 0o301047 | 0 |
| `W1350` | LABEL(md) | `include/LO_GEN.labels.md:803` | 0o301050 | 0 |
| `W1351` | LABEL(md) | `include/LO_GEN.labels.md:804` | 0o301051 | 0 |
| `W1352` | LABEL(md) | `include/LO_GEN.labels.md:805` | 0o301052 | 0 |
| `W1353` | LABEL(md) | `include/LO_GEN.labels.md:806` | 0o301053 | 0 |
| `W1354` | LABEL(md) | `include/LO_GEN.labels.md:807` | 0o301054 | 0 |
| `W1355` | LABEL(md) | `include/LO_GEN.labels.md:808` | 0o301055 | 0 |
| `W1356` | LABEL(md) | `include/LO_GEN.labels.md:809` | 0o301056 | 0 |
| `W1357` | LABEL(md) | `include/LO_GEN.labels.md:810` | 0o301057 | 0 |
| `W1360` | LABEL(md) | `include/LO_GEN.labels.md:811` | 0o301060 | 0 |
| `W1361` | LABEL(md) | `include/LO_GEN.labels.md:812` | 0o301061 | 0 |
| `W1362` | LABEL(md) | `include/LO_GEN.labels.md:813` | 0o301062 | 0 |
| `W1363` | LABEL(md) | `include/LO_GEN.labels.md:814` | 0o301063 | 0 |
| `W1364` | LABEL(md) | `include/LO_GEN.labels.md:815` | 0o301064 | 0 |
| `W1365` | LABEL(md) | `include/LO_GEN.labels.md:816` | 0o301065 | 0 |
| `W1366` | LABEL(md) | `include/LO_GEN.labels.md:817` | 0o301066 | 0 |
| `W1367` | LABEL(md) | `include/LO_GEN.labels.md:818` | 0o301067 | 0 |
| `W1370` | LABEL(md) | `include/LO_GEN.labels.md:819` | 0o301070 | 0 |
| `W1371` | LABEL(md) | `include/LO_GEN.labels.md:820` | 0o301071 | 0 |
| `W1372` | LABEL(md) | `include/LO_GEN.labels.md:821` | 0o301072 | 0 |
| `W1373` | LABEL(md) | `include/LO_GEN.labels.md:822` | 0o301073 | 0 |
| `W1374` | LABEL(md) | `include/LO_GEN.labels.md:823` | 0o301074 | 0 |
| `W1375` | LABEL(md) | `include/LO_GEN.labels.md:824` | 0o301075 | 0 |
| `W1376` | LABEL(md) | `include/LO_GEN.labels.md:825` | 0o301076 | 0 |
| `W1377` | LABEL(md) | `include/LO_GEN.labels.md:826` | 0o301077 | 0 |
| `W1400` | LABEL(md) | `include/LO_GEN.labels.md:827` | 0o301100 | 0 |
| `W1401` | LABEL(md) | `include/LO_GEN.labels.md:828` | 0o301101 | 0 |
| `W1402` | LABEL(md) | `include/LO_GEN.labels.md:829` | 0o301102 | 0 |
| `W1403` | LABEL(md) | `include/LO_GEN.labels.md:830` | 0o301103 | 0 |
| `W1404` | LABEL(md) | `include/LO_GEN.labels.md:831` | 0o301104 | 0 |
| `W1405` | LABEL(md) | `include/LO_GEN.labels.md:832` | 0o301105 | 0 |
| `W1406` | LABEL(md) | `include/LO_GEN.labels.md:833` | 0o301106 | 0 |
| `W1407` | LABEL(md) | `include/LO_GEN.labels.md:834` | 0o301107 | 0 |
| `W1410` | LABEL(md) | `include/LO_GEN.labels.md:835` | 0o301110 | 0 |
| `W1411` | LABEL(md) | `include/LO_GEN.labels.md:836` | 0o301111 | 0 |
| `W1412` | LABEL(md) | `include/LO_GEN.labels.md:837` | 0o301112 | 0 |
| `W1413` | LABEL(md) | `include/LO_GEN.labels.md:838` | 0o301113 | 0 |
| `W1414` | LABEL(md) | `include/LO_GEN.labels.md:839` | 0o301114 | 0 |
| `W1415` | LABEL(md) | `include/LO_GEN.labels.md:840` | 0o301115 | 0 |
| `W1416` | LABEL(md) | `include/LO_GEN.labels.md:841` | 0o301116 | 0 |
| `W1417` | LABEL(md) | `include/LO_GEN.labels.md:842` | 0o301117 | 0 |
| `W1420` | LABEL(md) | `include/LO_GEN.labels.md:843` | 0o301120 | 0 |
| `W1421` | LABEL(md) | `include/LO_GEN.labels.md:844` | 0o301121 | 0 |
| `W1422` | LABEL(md) | `include/LO_GEN.labels.md:845` | 0o301122 | 0 |
| `W1423` | LABEL(md) | `include/LO_GEN.labels.md:846` | 0o301123 | 0 |
| `W1424` | LABEL(md) | `include/LO_GEN.labels.md:847` | 0o301124 | 0 |
| `W1425` | LABEL(md) | `include/LO_GEN.labels.md:848` | 0o301125 | 0 |
| `W1426` | LABEL(md) | `include/LO_GEN.labels.md:849` | 0o301126 | 0 |
| `W1427` | LABEL(md) | `include/LO_GEN.labels.md:850` | 0o301127 | 0 |
| `W1430` | LABEL(md) | `include/LO_GEN.labels.md:851` | 0o301130 | 0 |
| `W1431` | LABEL(md) | `include/LO_GEN.labels.md:852` | 0o301131 | 0 |
| `W1432` | LABEL(md) | `include/LO_GEN.labels.md:853` | 0o301132 | 0 |
| `W1433` | LABEL(md) | `include/LO_GEN.labels.md:854` | 0o301133 | 0 |
| `W1434` | LABEL(md) | `include/LO_GEN.labels.md:855` | 0o301134 | 0 |
| `W1435` | LABEL(md) | `include/LO_GEN.labels.md:856` | 0o301135 | 0 |
| `W1436` | LABEL(md) | `include/LO_GEN.labels.md:857` | 0o301136 | 0 |
| `W1437` | LABEL(md) | `include/LO_GEN.labels.md:858` | 0o301137 | 0 |
| `W1440` | LABEL(md) | `include/LO_GEN.labels.md:859` | 0o301140 | 0 |
| `W1441` | LABEL(md) | `include/LO_GEN.labels.md:860` | 0o301141 | 0 |
| `W1442` | LABEL(md) | `include/LO_GEN.labels.md:861` | 0o301142 | 0 |
| `W1443` | LABEL(md) | `include/LO_GEN.labels.md:862` | 0o301143 | 0 |
| `W1444` | LABEL(md) | `include/LO_GEN.labels.md:863` | 0o301144 | 0 |
| `W1445` | LABEL(md) | `include/LO_GEN.labels.md:864` | 0o301145 | 0 |
| `W1446` | LABEL(md) | `include/LO_GEN.labels.md:865` | 0o301146 | 0 |
| `W1447` | LABEL(md) | `include/LO_GEN.labels.md:866` | 0o301147 | 0 |
| `W1450` | LABEL(md) | `include/LO_GEN.labels.md:867` | 0o301150 | 0 |
| `W1451` | LABEL(md) | `include/LO_GEN.labels.md:868` | 0o301151 | 0 |
| `W1452` | LABEL(md) | `include/LO_GEN.labels.md:869` | 0o301152 | 0 |
| `W1453` | LABEL(md) | `include/LO_GEN.labels.md:870` | 0o301153 | 0 |
| `W1454` | LABEL(md) | `include/LO_GEN.labels.md:871` | 0o301154 | 0 |
| `W1455` | LABEL(md) | `include/LO_GEN.labels.md:872` | 0o301155 | 0 |
| `W1456` | LABEL(md) | `include/LO_GEN.labels.md:873` | 0o301156 | 0 |
| `W1457` | LABEL(md) | `include/LO_GEN.labels.md:874` | 0o301157 | 0 |
| `W1460` | LABEL(md) | `include/LO_GEN.labels.md:875` | 0o301160 | 0 |
| `W1461` | LABEL(md) | `include/LO_GEN.labels.md:876` | 0o301161 | 0 |
| `W1462` | LABEL(md) | `include/LO_GEN.labels.md:877` | 0o301162 | 0 |
| `W1463` | LABEL(md) | `include/LO_GEN.labels.md:878` | 0o301163 | 0 |
| `W1464` | LABEL(md) | `include/LO_GEN.labels.md:879` | 0o301164 | 0 |
| `W1465` | LABEL(md) | `include/LO_GEN.labels.md:880` | 0o301165 | 0 |
| `W1466` | LABEL(md) | `include/LO_GEN.labels.md:881` | 0o301166 | 0 |
| `W1467` | LABEL(md) | `include/LO_GEN.labels.md:882` | 0o301167 | 0 |
| `W1470` | LABEL(md) | `include/LO_GEN.labels.md:883` | 0o301170 | 0 |
| `W1471` | LABEL(md) | `include/LO_GEN.labels.md:884` | 0o301171 | 0 |
| `W1472` | LABEL(md) | `include/LO_GEN.labels.md:885` | 0o301172 | 0 |
| `W1473` | LABEL(md) | `include/LO_GEN.labels.md:886` | 0o301173 | 0 |
| `W1474` | LABEL(md) | `include/LO_GEN.labels.md:887` | 0o301174 | 0 |
| `W1475` | LABEL(md) | `include/LO_GEN.labels.md:888` | 0o301175 | 0 |
| `W1476` | LABEL(md) | `include/LO_GEN.labels.md:889` | 0o301176 | 0 |
| `W1477` | LABEL(md) | `include/LO_GEN.labels.md:890` | 0o301177 | 0 |
| `W1500` | LABEL(md) | `include/LO_GEN.labels.md:891` | 0o301200 | 0 |
| `W1501` | LABEL(md) | `include/LO_GEN.labels.md:892` | 0o301201 | 0 |
| `W1502` | LABEL(md) | `include/LO_GEN.labels.md:893` | 0o301202 | 0 |
| `W1503` | LABEL(md) | `include/LO_GEN.labels.md:894` | 0o301203 | 0 |
| `W1504` | LABEL(md) | `include/LO_GEN.labels.md:895` | 0o301204 | 0 |
| `W1505` | LABEL(md) | `include/LO_GEN.labels.md:896` | 0o301205 | 0 |
| `W1506` | LABEL(md) | `include/LO_GEN.labels.md:897` | 0o301206 | 0 |
| `W1507` | LABEL(md) | `include/LO_GEN.labels.md:898` | 0o301207 | 0 |
| `W1510` | LABEL(md) | `include/LO_GEN.labels.md:899` | 0o301210 | 0 |
| `W1511` | LABEL(md) | `include/LO_GEN.labels.md:900` | 0o301211 | 0 |
| `W1512` | LABEL(md) | `include/LO_GEN.labels.md:901` | 0o301212 | 0 |
| `W1513` | LABEL(md) | `include/LO_GEN.labels.md:902` | 0o301213 | 0 |
| `W1514` | LABEL(md) | `include/LO_GEN.labels.md:903` | 0o301214 | 0 |
| `W1515` | LABEL(md) | `include/LO_GEN.labels.md:904` | 0o301215 | 0 |
| `W1516` | LABEL(md) | `include/LO_GEN.labels.md:905` | 0o301216 | 0 |
| `W1517` | LABEL(md) | `include/LO_GEN.labels.md:906` | 0o301217 | 0 |
| `W1520` | LABEL(md) | `include/LO_GEN.labels.md:907` | 0o301220 | 0 |
| `W1521` | LABEL(md) | `include/LO_GEN.labels.md:908` | 0o301221 | 0 |
| `W1522` | LABEL(md) | `include/LO_GEN.labels.md:909` | 0o301222 | 0 |
| `W1523` | LABEL(md) | `include/LO_GEN.labels.md:910` | 0o301223 | 0 |
| `W1524` | LABEL(md) | `include/LO_GEN.labels.md:911` | 0o301224 | 0 |
| `W1525` | LABEL(md) | `include/LO_GEN.labels.md:912` | 0o301225 | 0 |
| `W1526` | LABEL(md) | `include/LO_GEN.labels.md:913` | 0o301226 | 0 |
| `W1527` | LABEL(md) | `include/LO_GEN.labels.md:914` | 0o301227 | 0 |
| `W1530` | LABEL(md) | `include/LO_GEN.labels.md:915` | 0o301230 | 0 |
| `W1531` | LABEL(md) | `include/LO_GEN.labels.md:916` | 0o301231 | 0 |
| `W1532` | LABEL(md) | `include/LO_GEN.labels.md:917` | 0o301232 | 0 |
| `W1533` | LABEL(md) | `include/LO_GEN.labels.md:918` | 0o301233 | 0 |
| `W1534` | LABEL(md) | `include/LO_GEN.labels.md:919` | 0o301234 | 0 |
| `W1535` | LABEL(md) | `include/LO_GEN.labels.md:920` | 0o301235 | 0 |
| `W1536` | LABEL(md) | `include/LO_GEN.labels.md:921` | 0o301236 | 0 |
| `W1537` | LABEL(md) | `include/LO_GEN.labels.md:922` | 0o301237 | 0 |
| `W1540` | LABEL(md) | `include/LO_GEN.labels.md:923` | 0o301240 | 0 |
| `W1541` | LABEL(md) | `include/LO_GEN.labels.md:924` | 0o301241 | 0 |
| `W1542` | LABEL(md) | `include/LO_GEN.labels.md:925` | 0o301242 | 0 |
| `W1543` | LABEL(md) | `include/LO_GEN.labels.md:926` | 0o301243 | 0 |
| `W1544` | LABEL(md) | `include/LO_GEN.labels.md:927` | 0o301244 | 0 |
| `W1545` | LABEL(md) | `include/LO_GEN.labels.md:928` | 0o301245 | 0 |
| `W1546` | LABEL(md) | `include/LO_GEN.labels.md:929` | 0o301246 | 0 |
| `W1547` | LABEL(md) | `include/LO_GEN.labels.md:930` | 0o301247 | 0 |
| `W1550` | LABEL(md) | `include/LO_GEN.labels.md:931` | 0o301250 | 0 |
| `W1551` | LABEL(md) | `include/LO_GEN.labels.md:932` | 0o301251 | 0 |
| `W1552` | LABEL(md) | `include/LO_GEN.labels.md:933` | 0o301252 | 0 |
| `W1553` | LABEL(md) | `include/LO_GEN.labels.md:934` | 0o301253 | 0 |
| `W1554` | LABEL(md) | `include/LO_GEN.labels.md:935` | 0o301254 | 0 |
| `W1555` | LABEL(md) | `include/LO_GEN.labels.md:936` | 0o301255 | 0 |
| `W1556` | LABEL(md) | `include/LO_GEN.labels.md:937` | 0o301256 | 0 |
| `W1557` | LABEL(md) | `include/LO_GEN.labels.md:938` | 0o301257 | 0 |
| `W1560` | LABEL(md) | `include/LO_GEN.labels.md:939` | 0o301260 | 0 |
| `W1561` | LABEL(md) | `include/LO_GEN.labels.md:940` | 0o301261 | 0 |
| `W1562` | LABEL(md) | `include/LO_GEN.labels.md:941` | 0o301262 | 0 |
| `W1563` | LABEL(md) | `include/LO_GEN.labels.md:942` | 0o301263 | 0 |
| `W1564` | LABEL(md) | `include/LO_GEN.labels.md:943` | 0o301264 | 0 |
| `W1565` | LABEL(md) | `include/LO_GEN.labels.md:944` | 0o301265 | 0 |
| `W1566` | LABEL(md) | `include/LO_GEN.labels.md:945` | 0o301266 | 0 |
| `W1567` | LABEL(md) | `include/LO_GEN.labels.md:946` | 0o301267 | 0 |
| `W1570` | LABEL(md) | `include/LO_GEN.labels.md:947` | 0o301270 | 0 |
| `W1571` | LABEL(md) | `include/LO_GEN.labels.md:948` | 0o301271 | 0 |
| `W1572` | LABEL(md) | `include/LO_GEN.labels.md:949` | 0o301272 | 0 |
| `W1573` | LABEL(md) | `include/LO_GEN.labels.md:950` | 0o301273 | 0 |
| `W1574` | LABEL(md) | `include/LO_GEN.labels.md:951` | 0o301274 | 0 |
| `W1575` | LABEL(md) | `include/LO_GEN.labels.md:952` | 0o301275 | 0 |
| `W1576` | LABEL(md) | `include/LO_GEN.labels.md:953` | 0o301276 | 0 |
| `W1577` | LABEL(md) | `include/LO_GEN.labels.md:954` | 0o301277 | 0 |
| `W1600` | LABEL(md) | `include/LO_GEN.labels.md:955` | 0o301300 | 0 |
| `W1601` | LABEL(md) | `include/LO_GEN.labels.md:956` | 0o301301 | 0 |
| `W1602` | LABEL(md) | `include/LO_GEN.labels.md:957` | 0o301302 | 0 |
| `W1603` | LABEL(md) | `include/LO_GEN.labels.md:958` | 0o301303 | 0 |
| `W1604` | LABEL(md) | `include/LO_GEN.labels.md:959` | 0o301304 | 0 |
| `W1605` | LABEL(md) | `include/LO_GEN.labels.md:960` | 0o301305 | 0 |
| `W1606` | LABEL(md) | `include/LO_GEN.labels.md:961` | 0o301306 | 0 |
| `W1607` | LABEL(md) | `include/LO_GEN.labels.md:962` | 0o301307 | 0 |
| `W1610` | LABEL(md) | `include/LO_GEN.labels.md:963` | 0o301310 | 0 |
| `W1611` | LABEL(md) | `include/LO_GEN.labels.md:964` | 0o301311 | 0 |
| `W1612` | LABEL(md) | `include/LO_GEN.labels.md:965` | 0o301312 | 0 |
| `W1613` | LABEL(md) | `include/LO_GEN.labels.md:966` | 0o301313 | 0 |
| `W1614` | LABEL(md) | `include/LO_GEN.labels.md:967` | 0o301314 | 0 |
| `W1615` | LABEL(md) | `include/LO_GEN.labels.md:968` | 0o301315 | 0 |
| `W1616` | LABEL(md) | `include/LO_GEN.labels.md:969` | 0o301316 | 0 |
| `W1617` | LABEL(md) | `include/LO_GEN.labels.md:970` | 0o301317 | 0 |
| `W1620` | LABEL(md) | `include/LO_GEN.labels.md:971` | 0o301320 | 0 |
| `W1621` | LABEL(md) | `include/LO_GEN.labels.md:972` | 0o301321 | 0 |
| `W1622` | LABEL(md) | `include/LO_GEN.labels.md:973` | 0o301322 | 0 |
| `W1623` | LABEL(md) | `include/LO_GEN.labels.md:974` | 0o301323 | 0 |
| `W1624` | LABEL(md) | `include/LO_GEN.labels.md:975` | 0o301324 | 0 |
| `W1625` | LABEL(md) | `include/LO_GEN.labels.md:976` | 0o301325 | 0 |
| `W1626` | LABEL(md) | `include/LO_GEN.labels.md:977` | 0o301326 | 0 |
| `W1627` | LABEL(md) | `include/LO_GEN.labels.md:978` | 0o301327 | 0 |
| `W1630` | LABEL(md) | `include/LO_GEN.labels.md:979` | 0o301330 | 0 |
| `W1631` | LABEL(md) | `include/LO_GEN.labels.md:980` | 0o301331 | 0 |
| `W1632` | LABEL(md) | `include/LO_GEN.labels.md:981` | 0o301332 | 0 |
| `W1633` | LABEL(md) | `include/LO_GEN.labels.md:982` | 0o301333 | 0 |
| `W1634` | LABEL(md) | `include/LO_GEN.labels.md:983` | 0o301334 | 0 |
| `W1635` | LABEL(md) | `include/LO_GEN.labels.md:984` | 0o301335 | 0 |
| `W1636` | LABEL(md) | `include/LO_GEN.labels.md:985` | 0o301336 | 0 |
| `W1637` | LABEL(md) | `include/LO_GEN.labels.md:986` | 0o301337 | 0 |
| `W1640` | LABEL(md) | `include/LO_GEN.labels.md:987` | 0o301340 | 0 |
| `W1641` | LABEL(md) | `include/LO_GEN.labels.md:988` | 0o301341 | 0 |
| `W1642` | LABEL(md) | `include/LO_GEN.labels.md:989` | 0o301342 | 0 |
| `W1643` | LABEL(md) | `include/LO_GEN.labels.md:990` | 0o301343 | 0 |
| `W1644` | LABEL(md) | `include/LO_GEN.labels.md:991` | 0o301344 | 0 |
| `W1645` | LABEL(md) | `include/LO_GEN.labels.md:992` | 0o301345 | 0 |
| `W1646` | LABEL(md) | `include/LO_GEN.labels.md:993` | 0o301346 | 0 |
| `W1647` | LABEL(md) | `include/LO_GEN.labels.md:994` | 0o301347 | 0 |
| `W1650` | LABEL(md) | `include/LO_GEN.labels.md:995` | 0o301350 | 0 |
| `W1651` | LABEL(md) | `include/LO_GEN.labels.md:996` | 0o301351 | 0 |
| `W1652` | LABEL(md) | `include/LO_GEN.labels.md:997` | 0o301352 | 0 |
| `W1653` | LABEL(md) | `include/LO_GEN.labels.md:998` | 0o301353 | 0 |
| `W1654` | LABEL(md) | `include/LO_GEN.labels.md:999` | 0o301354 | 0 |
| `W1655` | LABEL(md) | `include/LO_GEN.labels.md:1000` | 0o301355 | 0 |
| `W1656` | LABEL(md) | `include/LO_GEN.labels.md:1001` | 0o301356 | 0 |
| `W1657` | LABEL(md) | `include/LO_GEN.labels.md:1002` | 0o301357 | 0 |
| `W1660` | LABEL(md) | `include/LO_GEN.labels.md:1003` | 0o301360 | 0 |
| `W1661` | LABEL(md) | `include/LO_GEN.labels.md:1004` | 0o301361 | 0 |
| `W1662` | LABEL(md) | `include/LO_GEN.labels.md:1005` | 0o301362 | 0 |
| `W1663` | LABEL(md) | `include/LO_GEN.labels.md:1006` | 0o301363 | 0 |
| `W1664` | LABEL(md) | `include/LO_GEN.labels.md:1007` | 0o301364 | 0 |
| `W1665` | LABEL(md) | `include/LO_GEN.labels.md:1008` | 0o301365 | 0 |
| `W1666` | LABEL(md) | `include/LO_GEN.labels.md:1009` | 0o301366 | 0 |
| `W1667` | LABEL(md) | `include/LO_GEN.labels.md:1010` | 0o301367 | 0 |
| `W1670` | LABEL(md) | `include/LO_GEN.labels.md:1011` | 0o301370 | 0 |
| `W1671` | LABEL(md) | `include/LO_GEN.labels.md:1012` | 0o301371 | 0 |
| `W1672` | LABEL(md) | `include/LO_GEN.labels.md:1013` | 0o301372 | 0 |
| `W1673` | LABEL(md) | `include/LO_GEN.labels.md:1014` | 0o301373 | 0 |
| `W1674` | LABEL(md) | `include/LO_GEN.labels.md:1015` | 0o301374 | 0 |
| `W1675` | LABEL(md) | `include/LO_GEN.labels.md:1016` | 0o301375 | 0 |
| `W1676` | LABEL(md) | `include/LO_GEN.labels.md:1017` | 0o301376 | 0 |
| `W1677` | LABEL(md) | `include/LO_GEN.labels.md:1018` | 0o301377 | 0 |
| `W1700` | LABEL(md) | `include/LO_GEN.labels.md:1019` | 0o301400 | 0 |
| `W1701` | LABEL(md) | `include/LO_GEN.labels.md:1020` | 0o301401 | 0 |
| `W1702` | LABEL(md) | `include/LO_GEN.labels.md:1021` | 0o301402 | 0 |
| `W1703` | LABEL(md) | `include/LO_GEN.labels.md:1022` | 0o301403 | 0 |
| `W1704` | LABEL(md) | `include/LO_GEN.labels.md:1023` | 0o301404 | 0 |
| `W1705` | LABEL(md) | `include/LO_GEN.labels.md:1024` | 0o301405 | 0 |
| `W1706` | LABEL(md) | `include/LO_GEN.labels.md:1025` | 0o301406 | 0 |
| `W1707` | LABEL(md) | `include/LO_GEN.labels.md:1026` | 0o301407 | 0 |
| `W1710` | LABEL(md) | `include/LO_GEN.labels.md:1027` | 0o301410 | 0 |
| `W1711` | LABEL(md) | `include/LO_GEN.labels.md:1028` | 0o301411 | 0 |
| `W1712` | LABEL(md) | `include/LO_GEN.labels.md:1029` | 0o301412 | 0 |
| `W1713` | LABEL(md) | `include/LO_GEN.labels.md:1030` | 0o301413 | 0 |
| `W1714` | LABEL(md) | `include/LO_GEN.labels.md:1031` | 0o301414 | 0 |
| `W1715` | LABEL(md) | `include/LO_GEN.labels.md:1032` | 0o301415 | 0 |
| `W1716` | LABEL(md) | `include/LO_GEN.labels.md:1033` | 0o301416 | 0 |
| `W1717` | LABEL(md) | `include/LO_GEN.labels.md:1034` | 0o301417 | 0 |
| `W1720` | LABEL(md) | `include/LO_GEN.labels.md:1035` | 0o301420 | 0 |
| `W1721` | LABEL(md) | `include/LO_GEN.labels.md:1036` | 0o301421 | 0 |
| `W1722` | LABEL(md) | `include/LO_GEN.labels.md:1037` | 0o301422 | 0 |
| `W1723` | LABEL(md) | `include/LO_GEN.labels.md:1038` | 0o301423 | 0 |
| `W1724` | LABEL(md) | `include/LO_GEN.labels.md:1039` | 0o301424 | 0 |
| `W1725` | LABEL(md) | `include/LO_GEN.labels.md:1040` | 0o301425 | 0 |
| `W1726` | LABEL(md) | `include/LO_GEN.labels.md:1041` | 0o301426 | 0 |
| `W1727` | LABEL(md) | `include/LO_GEN.labels.md:1042` | 0o301427 | 0 |
| `W1730` | LABEL(md) | `include/LO_GEN.labels.md:1043` | 0o301430 | 0 |
| `W1731` | LABEL(md) | `include/LO_GEN.labels.md:1044` | 0o301431 | 0 |
| `W1732` | LABEL(md) | `include/LO_GEN.labels.md:1045` | 0o301432 | 0 |
| `W1733` | LABEL(md) | `include/LO_GEN.labels.md:1046` | 0o301433 | 0 |
| `W1734` | LABEL(md) | `include/LO_GEN.labels.md:1047` | 0o301434 | 0 |
| `W1735` | LABEL(md) | `include/LO_GEN.labels.md:1048` | 0o301435 | 0 |
| `W1736` | LABEL(md) | `include/LO_GEN.labels.md:1049` | 0o301436 | 0 |
| `W1737` | LABEL(md) | `include/LO_GEN.labels.md:1050` | 0o301437 | 0 |
| `W1740` | LABEL(md) | `include/LO_GEN.labels.md:1051` | 0o301440 | 0 |
| `W1741` | LABEL(md) | `include/LO_GEN.labels.md:1052` | 0o301441 | 0 |
| `W1742` | LABEL(md) | `include/LO_GEN.labels.md:1053` | 0o301442 | 0 |
| `W1743` | LABEL(md) | `include/LO_GEN.labels.md:1054` | 0o301443 | 0 |
| `W1744` | LABEL(md) | `include/LO_GEN.labels.md:1055` | 0o301444 | 0 |
| `W1745` | LABEL(md) | `include/LO_GEN.labels.md:1056` | 0o301445 | 0 |
| `W1746` | LABEL(md) | `include/LO_GEN.labels.md:1057` | 0o301446 | 0 |
| `W1747` | LABEL(md) | `include/LO_GEN.labels.md:1058` | 0o301447 | 0 |
| `W1750` | LABEL(md) | `include/LO_GEN.labels.md:1059` | 0o301450 | 0 |
| `W1751` | LABEL(md) | `include/LO_GEN.labels.md:1060` | 0o301451 | 0 |
| `W1752` | LABEL(md) | `include/LO_GEN.labels.md:1061` | 0o301452 | 0 |
| `W1753` | LABEL(md) | `include/LO_GEN.labels.md:1062` | 0o301453 | 0 |
| `W1754` | LABEL(md) | `include/LO_GEN.labels.md:1063` | 0o301454 | 0 |
| `W1755` | LABEL(md) | `include/LO_GEN.labels.md:1064` | 0o301455 | 0 |
| `W1756` | LABEL(md) | `include/LO_GEN.labels.md:1065` | 0o301456 | 0 |
| `W1757` | LABEL(md) | `include/LO_GEN.labels.md:1066` | 0o301457 | 0 |
| `W1760` | LABEL(md) | `include/LO_GEN.labels.md:1067` | 0o301460 | 0 |
| `W1761` | LABEL(md) | `include/LO_GEN.labels.md:1068` | 0o301461 | 0 |
| `W1762` | LABEL(md) | `include/LO_GEN.labels.md:1069` | 0o301462 | 0 |
| `W1763` | LABEL(md) | `include/LO_GEN.labels.md:1070` | 0o301463 | 0 |
| `W1764` | LABEL(md) | `include/LO_GEN.labels.md:1071` | 0o301464 | 0 |
| `W1765` | LABEL(md) | `include/LO_GEN.labels.md:1072` | 0o301465 | 0 |
| `W1766` | LABEL(md) | `include/LO_GEN.labels.md:1073` | 0o301466 | 0 |
| `W1767` | LABEL(md) | `include/LO_GEN.labels.md:1074` | 0o301467 | 0 |
| `W1770` | LABEL(md) | `include/LO_GEN.labels.md:1075` | 0o301470 | 0 |
| `W1771` | LABEL(md) | `include/LO_GEN.labels.md:1076` | 0o301471 | 0 |
| `W1772` | LABEL(md) | `include/LO_GEN.labels.md:1077` | 0o301472 | 0 |
| `W1773` | LABEL(md) | `include/LO_GEN.labels.md:1078` | 0o301473 | 0 |
| `W1774` | LABEL(md) | `include/LO_GEN.labels.md:1079` | 0o301474 | 0 |
| `W1775` | LABEL(md) | `include/LO_GEN.labels.md:1080` | 0o301475 | 0 |
| `W1776` | LABEL(md) | `include/LO_GEN.labels.md:1081` | 0o301476 | 0 |
| `W1777` | LABEL(md) | `include/LO_GEN.labels.md:1082` | 0o301477 | 0 |
| `WT0533` | LABEL(md) | `include/LO_GEN.labels.md:30` | 0o300233 | 0 |
| `WT0535` | LABEL(md) | `include/LO_GEN.labels.md:31` | 0o300235 | 0 |
| `WT0537` | LABEL(md) | `include/LO_GEN.labels.md:32` | 0o300237 | 0 |
| `WT0541` | LABEL(md) | `include/LO_GEN.labels.md:33` | 0o300241 | 0 |
| `WT0543` | LABEL(md) | `include/LO_GEN.labels.md:34` | 0o300243 | 0 |
| `WT0545` | LABEL(md) | `include/LO_GEN.labels.md:35` | 0o300245 | 0 |
| `WT0547` | LABEL(md) | `include/LO_GEN.labels.md:36` | 0o300247 | 0 |
| `WT0551` | LABEL(md) | `include/LO_GEN.labels.md:37` | 0o300251 | 0 |
| `WT0553` | LABEL(md) | `include/LO_GEN.labels.md:38` | 0o300253 | 0 |
| `WT0555` | LABEL(md) | `include/LO_GEN.labels.md:39` | 0o300255 | 0 |
| `WT0557` | LABEL(md) | `include/LO_GEN.labels.md:40` | 0o300257 | 0 |
| `WT0561` | LABEL(md) | `include/LO_GEN.labels.md:41` | 0o300261 | 0 |
| `WT0563` | LABEL(md) | `include/LO_GEN.labels.md:42` | 0o300263 | 0 |
| `WT0565` | LABEL(md) | `include/LO_GEN.labels.md:43` | 0o300265 | 0 |
| `WT0567` | LABEL(md) | `include/LO_GEN.labels.md:44` | 0o300267 | 0 |
| `WT0571` | LABEL(md) | `include/LO_GEN.labels.md:45` | 0o300271 | 0 |
| `WT0573` | LABEL(md) | `include/LO_GEN.labels.md:46` | 0o300273 | 0 |
| `WT0575` | LABEL(md) | `include/LO_GEN.labels.md:47` | 0o300275 | 0 |
| `WT0577` | LABEL(md) | `include/LO_GEN.labels.md:48` | 0o300277 | 0 |
| `WT0601` | LABEL(md) | `include/LO_GEN.labels.md:49` | 0o300301 | 0 |
| `WT0603` | LABEL(md) | `include/LO_GEN.labels.md:50` | 0o300303 | 0 |
| `WT0605` | LABEL(md) | `include/LO_GEN.labels.md:51` | 0o300305 | 0 |
| `WT0607` | LABEL(md) | `include/LO_GEN.labels.md:52` | 0o300307 | 0 |
| `WT0611` | LABEL(md) | `include/LO_GEN.labels.md:53` | 0o300311 | 0 |
| `WT0613` | LABEL(md) | `include/LO_GEN.labels.md:54` | 0o300313 | 0 |
| `WT0615` | LABEL(md) | `include/LO_GEN.labels.md:55` | 0o300315 | 0 |
| `WT0617` | LABEL(md) | `include/LO_GEN.labels.md:56` | 0o300317 | 0 |
| `WT0621` | LABEL(md) | `include/LO_GEN.labels.md:57` | 0o300321 | 0 |
| `WT0623` | LABEL(md) | `include/LO_GEN.labels.md:58` | 0o300323 | 0 |
| `XOR_MASK_0075` | LABEL(md) | `include/LO_GEN.labels.md:120`, `include/LO_GEN.labels.md:1216` | 0o277575 | 0 |
| `XOR_MASK_0123` | LABEL(md) | `include/LO_GEN.labels.md:142`, `include/LO_GEN.labels.md:1094` | 0o277623 | 0 |
| `XOR_MASK_0127` | LABEL(md) | `include/LO_GEN.labels.md:146`, `include/LO_GEN.labels.md:1095` | 0o277627 | 0 |
| `XOR_MASK_0155` | LABEL(md) | `include/LO_GEN.labels.md:168`, `include/LO_GEN.labels.md:1150` | 0o277655 | 0 |
| `XOR_MASK_0161` | LABEL(md) | `include/LO_GEN.labels.md:172`, `include/LO_GEN.labels.md:1134` | 0o277661 | 0 |
| `XOR_MASK_0214` | LABEL(md) | `include/LO_GEN.labels.md:199` | 0o277714 | 0 |
| `XOR_MASK_0215` | LABEL(md) | `include/LO_GEN.labels.md:200` | 0o277715 | 0 |
| `XOR_MASK_0251` | LABEL(md) | `include/LO_GEN.labels.md:228`, `include/LO_GEN.labels.md:1261` | 0o277751 | 0 |
| `XOR_MASK_0257` | LABEL(md) | `include/LO_GEN.labels.md:234` | 0o277757 | 0 |
| `XOR_MASK_0327` | LABEL(md) | `include/LO_GEN.labels.md:274`, `include/LO_GEN.labels.md:1134` | 0o300027 | 0 |
| `XOR_MASK_0676` | LABEL(md) | `include/LO_GEN.labels.md:505` | 0o300376 | 0 |
| `XOR_MASK_0766` | LABEL(md) | `include/LO_GEN.labels.md:561` | 0o300466 | 0 |
| `XOR_MASK_0767` | LABEL(md) | `include/LO_GEN.labels.md:562` | 0o300467 | 0 |
| `XOR_MASK_1040` | LABEL(md) | `include/LO_GEN.labels.md:603` | 0o300540 | 0 |
| `XOR_MASK_1041` | LABEL(md) | `include/LO_GEN.labels.md:604` | 0o300541 | 0 |
| `XOR_MASK_1047` | LABEL(md) | `include/LO_GEN.labels.md:610` | 0o300547 | 0 |
| `XOR_MASK_1050` | LABEL(md) | `include/LO_GEN.labels.md:611` | 0o300550 | 0 |
| `XOR_MASK_1271` | LABEL(md) | `include/LO_GEN.labels.md:756` | 0o300771 | 0 |
| `XOR_MASK_1272` | LABEL(md) | `include/LO_GEN.labels.md:757` | 0o300772 | 0 |
| `XOR_MASK_1304` | LABEL(md) | `include/LO_GEN.labels.md:767` | 0o301004 | 0 |
| `XOR_MASK_1305` | LABEL(md) | `include/LO_GEN.labels.md:768` | 0o301005 | 0 |
| `XOR_MASK_1314` | LABEL(md) | `include/LO_GEN.labels.md:775` | 0o301014 | 0 |
| `XOR_MASK_1315` | LABEL(md) | `include/LO_GEN.labels.md:776` | 0o301015 | 0 |
| `XOR_MASK_1320` | LABEL(md) | `include/LO_GEN.labels.md:779`, `include/LO_GEN.labels.md:1266` | 0o301020 | 0 |
| `XOR_MASK_1372` | LABEL(md) | `include/LO_GEN.labels.md:821` | 0o301072 | 0 |
| `XOR_MASK_1373` | LABEL(md) | `include/LO_GEN.labels.md:822` | 0o301073 | 0 |
| `XOR_MASK_1404` | LABEL(md) | `include/LO_GEN.labels.md:831` | 0o301104 | 0 |
| `XOR_MASK_1405` | LABEL(md) | `include/LO_GEN.labels.md:832` | 0o301105 | 0 |
| `XOR_MASK_1414` | LABEL(md) | `include/LO_GEN.labels.md:839`, `include/LO_GEN.labels.md:1170` | 0o301114 | 0 |
| `XOR_MASK_1473` | LABEL(md) | `include/LO_GEN.labels.md:886`, `include/LO_GEN.labels.md:1278` | 0o301173 | 0 |
| `XOR_MASK_1521` | LABEL(md) | `include/LO_GEN.labels.md:908` | 0o301221 | 0 |
| `XOR_MASK_1522` | LABEL(md) | `include/LO_GEN.labels.md:909` | 0o301222 | 0 |
| `XOR_MASK_1536` | LABEL(md) | `include/LO_GEN.labels.md:921` | 0o301236 | 0 |
| `XOR_MASK_1537` | LABEL(md) | `include/LO_GEN.labels.md:922` | 0o301237 | 0 |
| `XOR_MASK_1551` | LABEL(md) | `include/LO_GEN.labels.md:932` | 0o301251 | 0 |
| `XOR_MASK_1552` | LABEL(md) | `include/LO_GEN.labels.md:933` | 0o301252 | 0 |
| `XOR_MASK_1563` | LABEL(md) | `include/LO_GEN.labels.md:942` | 0o301263 | 0 |
| `XOR_MASK_1564` | LABEL(md) | `include/LO_GEN.labels.md:943` | 0o301264 | 0 |
| `XOR_MASK_1606` | LABEL(md) | `include/LO_GEN.labels.md:961` | 0o301306 | 0 |
| `XOR_MASK_1607` | LABEL(md) | `include/LO_GEN.labels.md:962` | 0o301307 | 0 |
| `XOR_MASK_1615` | LABEL(md) | `include/LO_GEN.labels.md:968` | 0o301315 | 0 |
| `XOR_MASK_1616` | LABEL(md) | `include/LO_GEN.labels.md:969` | 0o301316 | 0 |
| `XOR_MASK_1631` | LABEL(md) | `include/LO_GEN.labels.md:980` | 0o301331 | 0 |
| `XOR_MASK_1632` | LABEL(md) | `include/LO_GEN.labels.md:981` | 0o301332 | 0 |
| `XOR_MASK_1770` | LABEL(md) | `include/LO_GEN.labels.md:1075`, `include/LO_GEN.labels.md:1161` | 0o301470 | 0 |
| `XOR_MASK_1777` | LABEL(md) | `include/LO_GEN.labels.md:1082` | 0o301477 | 0 |
| `X_COMEQ` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:168`, `src/LO_GEN.mad:35`, `include/LO_GEN.labels.md:22`, `include/LO_GEN.labels.md:22` | — | 0 |
| `X_CONST` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:167`, `src/LO_GEN.mad:34`, `include/LO_GEN.labels.md:21`, `include/LO_GEN.labels.md:21` | — | 0 |
| `X_DATAPRS` | LABEL(md)/SUBP | `src/LO_GEN.mad:29`, `include/FOREX.labels.md:21`, `include/LO_GEN.labels.md:16`, `include/LO_GEN.labels.md:16` | — | 0 |
| `X_DATE_PRINT` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:161`, `include/FOREX.labels.md:21` | — | 0 |
| `X_FOREX` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:166`, `src/LO_GEN.mad:33`, `include/LO_GEN.labels.md:20`, `include/LO_GEN.labels.md:20` | — | 0 |
| `X_GIV_PG` | LABEL(md)/SUBP | `src/LO_GEN.mad:31`, `include/FOREX.labels.md:23`, `include/LO_GEN.labels.md:18`, `include/LO_GEN.labels.md:18` | — | 0 |
| `X_LOADANGO` | LABEL(md)/SUBP | `src/LO_GEN.mad:38`, `include/FOREX.labels.md:25`, `include/LO_GEN.labels.md:25`, `include/LO_GEN.labels.md:25` | — | 0 |
| `X_OCTTDEC` | LABEL(md)/SUBP | `src/LO_GEN.mad:32`, `include/FOREX.labels.md:24`, `include/LO_GEN.labels.md:19`, `include/LO_GEN.labels.md:19` | — | 0 |
| `X_OCT_DEC` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:164`, `include/FOREX.labels.md:24` | — | 0 |
| `X_OPRTR` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:169`, `src/LO_GEN.mad:36`, `include/LO_GEN.labels.md:23`, `include/LO_GEN.labels.md:23` | — | 0 |
| `X_OVERLAY_LOADER` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:165`, `include/FOREX.labels.md:25` | — | 0 |
| `X_PAGE_GIVE` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:163`, `include/FOREX.labels.md:23` | — | 0 |
| `X_PAGE_TAKE` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:162`, `include/FOREX.labels.md:22` | — | 0 |
| `X_TAK_PG` | LABEL(md)/SUBP | `src/LO_GEN.mad:30`, `include/FOREX.labels.md:22`, `include/LO_GEN.labels.md:17`, `include/LO_GEN.labels.md:17` | — | 0 |
| `X_ПP` | LABEL(md)/SUBP | `src/FOREX_CORE.mad:170`, `src/LO_GEN.mad:37`, `include/LO_GEN.labels.md:24`, `include/LO_GEN.labels.md:24` | — | 0 |
| `YEAR_MASK` | TEXT | `src/FOREX_RUNTIME.mad:421` | — | 0 |
| `Z00` | LABEL(md) | `include/FOREX.labels.md:352` | — | 0 |
| `ИМЯ_` | LABEL(md) | `include/FOREX.labels.md:32`, `include/FOREX.labels.md:32`, `include/FOREX.labels.md:358` | 0o510413 | 0 |
| `ПP` | LABEL(md)/SUBP | `src/LO_SYN.mad:33`, `include/FOREX_ROOT.mad:77`, `include/FOREX.labels.md:358` | — | 0 |
| `РОЛЬ_NNNN` | LABEL(md) | `include/LO_GEN.labels.md:10` | — | 0 |
| `РОЛЬ_ЗНАЧЕНИЕ` | LABEL(md) | `include/LO_SYN.labels.md:48` | — | 0 |
| `втбрз` | LABEL(md) | `include/LO_GEN.labels.md:1549` | — | 0 |
| `э20` | LABEL(md) | `include/LO_GEN.labels.md:1549` | — | 0 |

### 2.2 Именованные константы (`,EQU,`)

Требование «все литералы — в переменные»: числовые литералы выносятся в
именованные `EQU`-константы. Здесь собраны все такие объявления и их применения.

| Имя | Значение | Определение (файл:строка) | Применения | Всего |
|---|---|---|---|---:|
| `BASE_REG14` | `14` | `include/FOREX_ROOT.mad:24` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `BUFFER_A_LEN` | `4000B` | `include/FOREX_ROOT.mad:25` | `src/FOREX_CORE.mad:457`, `include/FOREX_ROOT.mad:78` | 2 |
| `DEC_15` | `15` | `include/FOREX_ROOT.mad:26` | — | 0 |
| `DUMON_LEN` | `5` | `include/FOREX_ROOT.mad:27` | `src/FOREX_CORE.mad:154`, `include/FOREX_ROOT.mad:67` | 2 |
| `ENTRY_TAB_LEN` | `50B` | `include/FOREX_ROOT.mad:28` | `src/FOREX_CORE.mad:393`, `include/FOREX_ROOT.mad:62` | 2 |
| `ERR_TRANSLATOR_TEXT` | `18H'200'0OШ` | `include/FOREX_ROOT.mad:29` | `include/FOREX_ROOT.mad:149` | 1 |
| `FIXED_MODE_2` | `2` | `include/FOREX_ROOT.mad:30` | `src/FOREX_RUNTIME.mad:509` | 1 |
| `GOST_V` | `1H'212'` | `include/FOREX_ROOT.mad:31` | `include/FOREX_ROOT.mad:145` | 1 |
| `GOST_VREMYA` | `6HBPEMЯ-` | `include/FOREX_ROOT.mad:32` | `include/FOREX_ROOT.mad:146` | 1 |
| `GOST_YA` | `1H'231'` | `include/FOREX_ROOT.mad:33` | `include/FOREX_ROOT.mad:148` | 1 |
| `MODE_6` | `6` | `include/FOREX_ROOT.mad:34` | `src/FOREX_RUNTIME.mad:345`, `include/FOREX_ROOT.mad:82`, `include/FOREX_ROOT.mad:113`, `include/FOREX_ROOT.mad:126` | 4 |
| `MODE_RT_OCT22_DEC` | `18` | `include/FOREX_ROOT.mad:35` | `include/FOREX_ROOT.mad:112` | 1 |
| `ONE_WORD` | `1` | `include/FOREX_ROOT.mad:36` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `PAGE17_ADDR` | `17B` | `include/FOREX_ROOT.mad:37` | `include/FOREX_ROOT.mad:262`, `include/FOREX_ROOT.mad:268`, `include/FOREX_ROOT.mad:269`, `include/FOREX_ROOT.mad:271` | 4 |
| `PAGE_MODE_73401` | `=73401` | `include/FOREX_ROOT.mad:38` | `include/FOREX_ROOT.mad:244`, `include/FOREX_ROOT.mad:249` | 2 |
| `PG_BLOCK_MASK` | `=4000` | `include/FOREX_ROOT.mad:39` | `include/FOREX_ROOT.mad:282` | 1 |
| `PG_EX67_CODE` | `=:11 4037 77` | `include/FOREX_ROOT.mad:40` | `include/FOREX_ROOT.mad:248` | 1 |
| `PG_FLAG_SHIFT` | `64+12` | `include/FOREX_ROOT.mad:41` | `include/FOREX_ROOT.mad:245` | 1 |
| `PG_GO_CODE_1` | `=:00 2677` | `include/FOREX_ROOT.mad:42` | `include/FOREX_ROOT.mad:284` | 1 |
| `PG_GO_CODE_2` | `=:00 6736 77` | `include/FOREX_ROOT.mad:43` | `include/FOREX_ROOT.mad:285` | 1 |
| `PG_WORD_SHIFT` | `64-20` | `include/FOREX_ROOT.mad:44` | `include/FOREX_ROOT.mad:253` | 1 |
| `PRINT_BLOCK_LEN` | `002` | `include/FOREX_ROOT.mad:45` | — | 0 |
| `REAL_MODE_3` | `3` | `include/FOREX_ROOT.mad:46` | `src/FOREX_RUNTIME.mad:217`, `src/FOREX_RUNTIME.mad:490`, `include/FOREX_ROOT.mad:116` | 3 |
| `RET_LINK_REG` | `13` | `include/FOREX_ROOT.mad:47` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `RM_WORDS_4` | `4` | `include/FOREX_ROOT.mad:48` | `include/FOREX_ROOT.mad:241` | 1 |
| `STACK_OFF_M2` | `-2` | `include/FOREX_ROOT.mad:49` | `src/FOREX_RUNTIME.mad:350`, `src/FOREX_RUNTIME.mad:505`, `include/FOREX_ROOT.mad:255` | 3 |
| `TEXT_LO_GEN` | `8HLO*GEN` | `include/FOREX_ROOT.mad:50` | `include/FOREX_ROOT.mad:152` | 1 |
| `TEXT_LO_SYN` | `8HLO*SYN` | `include/FOREX_ROOT.mad:51` | `include/FOREX_ROOT.mad:151` | 1 |
| `TIME_SCALE` | `=R100.0` | `include/FOREX_ROOT.mad:52` | `include/FOREX_ROOT.mad:115` | 1 |
| `TIME_SEP_A` | `=6H'''17''17''17''17''17'` | `include/FOREX_ROOT.mad:53` | `include/FOREX_ROOT.mad:120` | 1 |
| `TIME_SEP_B` | `=6H'17''17''17''''17''17'` | `include/FOREX_ROOT.mad:54` | `include/FOREX_ROOT.mad:121` | 1 |
| `TIME_SEP_C` | `=6H'''''''16'''''` | `include/FOREX_ROOT.mad:55` | `include/FOREX_ROOT.mad:122` | 1 |
| `LINK_REG_15` | `15` | `include/FOREX_ROOT.mad:56` | `include/FOREX_ROOT.mad:251`, `include/FOREX_ROOT.mad:264`, `include/FOREX_ROOT.mad:281` | 3 |
| `PG_STEP_2` | `2` | `include/FOREX_ROOT.mad:57` | `include/FOREX_ROOT.mad:256`, `include/FOREX_ROOT.mad:259` | 2 |
| `ADDR_OCT_4000` | `0o4000` | `src/FOREX_CORE.mad:33` | `src/FOREX_CORE.mad:156` | 1 |
| `ADDR_OCT_50` | `0o50` | `src/FOREX_CORE.mad:34` | `src/FOREX_CORE.mad:149` | 1 |
| `A_I0_ADDR` | `4007B` | `src/FOREX_CORE.mad:35` | `src/FOREX_CORE.mad:266`, `src/FOREX_CORE.mad:270` | 2 |
| `BASE16_ADDR` | `74001B` | `src/FOREX_CORE.mad:36` | `src/FOREX_CORE.mad:208` | 1 |
| `BASE_REG14` | `14` | `src/FOREX_CORE.mad:37` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `BUFFER_A_LEN` | `4000B` | `src/FOREX_CORE.mad:38` | `src/FOREX_CORE.mad:457`, `include/FOREX_ROOT.mad:78` | 2 |
| `DATAPR_ADDR` | `74010B` | `src/FOREX_CORE.mad:98` | `src/FOREX_CORE.mad:224` | 1 |
| `DEC_38` | `38` | `src/FOREX_CORE.mad:99` | `src/FOREX_CORE.mad:354` | 1 |
| `DEC_43` | `43` | `src/FOREX_CORE.mad:100` | `src/FOREX_CORE.mad:337` | 1 |
| `DUMON_BASE_7` | `40007B` | `src/FOREX_CORE.mad:101` | `src/FOREX_CORE.mad:223` | 1 |
| `DUMON_CELL4` | `4026B` | `src/FOREX_CORE.mad:102` | `src/FOREX_CORE.mad:218` | 1 |
| `DUMON_CELL5` | `4027B` | `src/FOREX_CORE.mad:103` | `src/FOREX_CORE.mad:229` | 1 |
| `DUMON_CELL6` | `4030B` | `src/FOREX_CORE.mad:104` | `src/FOREX_CORE.mad:234` | 1 |
| `DUMON_LEN` | `5` | `src/FOREX_CORE.mad:105` | `src/FOREX_CORE.mad:154`, `include/FOREX_ROOT.mad:67` | 2 |
| `DUMON_TIME_CELL` | `4025B` | `src/FOREX_CORE.mad:106` | `src/FOREX_CORE.mad:207`, `src/FOREX_CORE.mad:297`, `src/FOREX_CORE.mad:317` | 3 |
| `ENTRY_TAB_ADDR` | `4006B` | `src/FOREX_CORE.mad:107` | `src/FOREX_CORE.mad:213`, `src/FOREX_CORE.mad:473`, `src/FOREX_CORE.mad:477`, `src/FOREX_CORE.mad:481`, `src/FOREX_CORE.mad:485` | 5 |
| `ENTRY_TAB_LEN` | `50B` | `src/FOREX_CORE.mad:108` | `src/FOREX_CORE.mad:393`, `include/FOREX_ROOT.mad:62` | 2 |
| `EX57_MODE6` | `6B` | `src/FOREX_CORE.mad:109` | `src/FOREX_CORE.mad:197`, `src/FOREX_CORE.mad:256`, `src/FOREX_CORE.mad:296` | 3 |
| `FLGEX_ADDR` | `4002B` | `src/FOREX_CORE.mad:110` | `src/FOREX_CORE.mad:301` | 1 |
| `FMT_RZB_MASK` | `4035B` | `src/FOREX_CORE.mad:111` | `src/FOREX_CORE.mad:276` | 1 |
| `FMT_SBR_MASK` | `4034B` | `src/FOREX_CORE.mad:112` | `src/FOREX_CORE.mad:275` | 1 |
| `FULIS_ADDR` | `4004B` | `src/FOREX_CORE.mad:113` | `src/FOREX_CORE.mad:228` | 1 |
| `GOST_ATTR_ADDR` | `7417B` | `src/FOREX_CORE.mad:114` | `src/FOREX_CORE.mad:332`, `src/FOREX_CORE.mad:333`, `src/FOREX_CORE.mad:346`, `src/FOREX_CORE.mad:347`, `src/FOREX_CORE.mad:376`, `src/FOREX_CORE.mad:377` … (+2) | 8 |
| `INF_ADDR` | `4036B` | `src/FOREX_CORE.mad:115` | `src/FOREX_CORE.mad:281` | 1 |
| `INIT_CONST_33` | `33B` | `src/FOREX_CORE.mad:116` | `src/FOREX_CORE.mad:187` | 1 |
| `INIT_MODE_1500` | `1500B` | `src/FOREX_CORE.mad:117` | `src/FOREX_CORE.mad:186` | 1 |
| `INIT_MODE_1700` | `1700B` | `src/FOREX_CORE.mad:118` | `src/FOREX_CORE.mad:182` | 1 |
| `LOADANGO_ADDR` | `74022B` | `src/FOREX_CORE.mad:119` | `src/FOREX_CORE.mad:245`, `src/FOREX_CORE.mad:250` | 2 |
| `LO_GEN_TEXT_ADDR` | `4032B` | `src/FOREX_CORE.mad:120` | `src/FOREX_CORE.mad:249` | 1 |
| `LO_SYN_TEXT_ADDR` | `4031B` | `src/FOREX_CORE.mad:121` | `src/FOREX_CORE.mad:244` | 1 |
| `MASK_7760` | `7760B` | `src/FOREX_CORE.mad:122` | `src/FOREX_CORE.mad:588` | 1 |
| `MASK_7761` | `7761B` | `src/FOREX_CORE.mad:123` | `src/FOREX_CORE.mad:596`, `src/FOREX_CORE.mad:604` | 2 |
| `MASK_7763` | `7763B` | `src/FOREX_CORE.mad:124` | `src/FOREX_CORE.mad:600`, `src/FOREX_CORE.mad:608` | 2 |
| `MIST_BASE_ADDR` | `40037B` | `src/FOREX_CORE.mad:125` | `src/FOREX_CORE.mad:312` | 1 |
| `MODE_RT_OCT22` | `22B` | `src/FOREX_CORE.mad:126` | `src/FOREX_CORE.mad:255` | 1 |
| `MUL_7771` | `7771B` | `src/FOREX_CORE.mad:127` | `src/FOREX_CORE.mad:592` | 1 |
| `NOLIS_ADDR` | `4003B` | `src/FOREX_CORE.mad:128` | `src/FOREX_CORE.mad:217` | 1 |
| `OCT_DEC_ADDR` | `74013B` | `src/FOREX_CORE.mad:129` | `src/FOREX_CORE.mad:271` | 1 |
| `ONE_WORD` | `1` | `src/FOREX_CORE.mad:130` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `PAGE_GIVE_ADDR` | `74012B` | `src/FOREX_CORE.mad:131` | `src/FOREX_CORE.mad:238` | 1 |
| `PAGE_TAKE_ADDR` | `74011B` | `src/FOREX_CORE.mad:132` | `src/FOREX_CORE.mad:307` | 1 |
| `PRINT_MESSAGE_ADDR` | `40023B` | `src/FOREX_CORE.mad:133` | `src/FOREX_CORE.mad:318` | 1 |
| `R100_ADDR` | `4033B` | `src/FOREX_CORE.mad:134` | `src/FOREX_CORE.mad:261` | 1 |
| `RESIDENT_ZERO_PAGE` | `70000B` | `src/FOREX_CORE.mad:135` | `src/FOREX_CORE.mad:363`, `src/FOREX_CORE.mad:368`, `src/FOREX_CORE.mad:518`, `src/FOREX_CORE.mad:573` | 4 |
| `RET_CELL` | `4023B` | `src/FOREX_CORE.mad:136` | `src/FOREX_CORE.mad:193` | 1 |
| `RET_LINK_REG` | `13` | `src/FOREX_CORE.mad:137` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `RET_MOD_ADDR` | `40050B` | `src/FOREX_CORE.mad:138` | `src/FOREX_CORE.mad:302` | 1 |
| `SYMTAB_TARGET` | `65412B` | `src/FOREX_CORE.mad:139` | `src/FOREX_CORE.mad:527`, `src/FOREX_CORE.mad:531`, `src/FOREX_CORE.mad:535` | 3 |
| `TIME_CELL` | `4024B` | `src/FOREX_CORE.mad:140` | `src/FOREX_CORE.mad:202`, `src/FOREX_CORE.mad:260`, `src/FOREX_CORE.mad:282` | 3 |
| `TTEX_ADDR` | `4037B` | `src/FOREX_CORE.mad:141` | `src/FOREX_CORE.mad:290` | 1 |
| `TTEX_BASE_ADDR` | `40033B` | `src/FOREX_CORE.mad:142` | `src/FOREX_CORE.mad:285` | 1 |
| `ИМЯ_ENTRY` | `ENTRY*` | `src/FOREX_CORE.mad:614` | — | 0 |
| `ИМЯ_FLGEX` | `FLGEX*` | `src/FOREX_CORE.mad:615` | — | 0 |
| `ИМЯ_NOLIS` | `NOLISFL*` | `src/FOREX_CORE.mad:616` | — | 0 |
| `ИМЯ_FULIS` | `FULISFL*` | `src/FOREX_CORE.mad:617` | — | 0 |
| `ИМЯ_CHECK` | `CHECKFL*` | `src/FOREX_CORE.mad:618` | — | 0 |
| `ИМЯ_DUMON` | `*DUMON*` | `src/FOREX_CORE.mad:619` | — | 0 |
| `ИМЯ_DATAPR` | `DATAPR*` | `src/FOREX_CORE.mad:620` | — | 0 |
| `ИМЯ_TAKPG` | `TAK/PG` | `src/FOREX_CORE.mad:621` | — | 0 |
| `ИМЯ_GIVPG` | `GIV/PG` | `src/FOREX_CORE.mad:622` | — | 0 |
| `ИМЯ_OCTTDEC` | `OCTTDEC` | `src/FOREX_CORE.mad:623` | — | 0 |
| `ИМЯ_FOREX` | `FOREX` | `src/FOREX_CORE.mad:624` | — | 0 |
| `ИМЯ_CONST` | `CONST` | `src/FOREX_CORE.mad:625` | — | 0 |
| `ИМЯ_COMEQ` | `COMEQ` | `src/FOREX_CORE.mad:626` | — | 0 |
| `ИМЯ_OPRTR` | `OPRTR` | `src/FOREX_CORE.mad:627` | — | 0 |
| `ИМЯ_LOADANG` | `LOADANGO` | `src/FOREX_CORE.mad:628` | — | 0 |
| `ALL_ONES_MASK` | `77777B` | `src/FOREX_RUNTIME.mad:27` | `src/FOREX_RUNTIME.mad:286` | 1 |
| `BASE_REG14` | `14` | `src/FOREX_RUNTIME.mad:28` | `src/FOREX_CORE.mad:212`, `src/FOREX_RUNTIME.mad:134`, `src/FOREX_RUNTIME.mad:145`, `src/FOREX_RUNTIME.mad:158`, `src/FOREX_RUNTIME.mad:206`, `src/FOREX_RUNTIME.mad:216` … (+3) | 9 |
| `DATA_WORD_0000000000077777` | `0000000000077777` | `src/FOREX_RUNTIME.mad:29` | `src/FOREX_RUNTIME.mad:469` | 1 |
| `DATA_WORD_00000000_00000000` | `00000000 00000000` | `src/FOREX_RUNTIME.mad:30` | `src/FOREX_RUNTIME.mad:301`, `src/FOREX_RUNTIME.mad:302`, `src/FOREX_RUNTIME.mad:303`, `src/FOREX_RUNTIME.mad:305`, `src/FOREX_RUNTIME.mad:308`, `src/FOREX_RUNTIME.mad:309` … (+4) | 10 |
| `DATA_WORD_00000000_00000001` | `00000000 00000001` | `src/FOREX_RUNTIME.mad:31` | `src/FOREX_RUNTIME.mad:304` | 1 |
| `DATA_WORD_00000000_00000002` | `00000000 00000002` | `src/FOREX_RUNTIME.mad:32` | `src/FOREX_RUNTIME.mad:313` | 1 |
| `DATA_WORD_00000000_00001777` | `00000000 00001777` | `src/FOREX_RUNTIME.mad:33` | `src/FOREX_RUNTIME.mad:306` | 1 |
| `DATA_WORD_00100000_00000000` | `00100000 00000000` | `src/FOREX_RUNTIME.mad:34` | `src/FOREX_RUNTIME.mad:307` | 1 |
| `DATA_WORD_17_7777_7777_7777` | `17 7777 7777 7777` | `src/FOREX_RUNTIME.mad:35` | `src/FOREX_RUNTIME.mad:512` | 1 |
| `DATA_WORD_37777774_77777477` | `37777774 77777477` | `src/FOREX_RUNTIME.mad:36` | `src/FOREX_RUNTIME.mad:311` | 1 |
| `DATA_WORD_77270707_00000000` | `77270707 00000000` | `src/FOREX_RUNTIME.mad:37` | `src/FOREX_RUNTIME.mad:314` | 1 |
| `DATE_DAY_SHIFT` | `64+16` | `src/FOREX_RUNTIME.mad:38` | `src/FOREX_RUNTIME.mad:352` | 1 |
| `DATE_MONTH_INDEX_SHIFT` | `64-24` | `src/FOREX_RUNTIME.mad:39` | `src/FOREX_RUNTIME.mad:366`, `src/FOREX_RUNTIME.mad:506` | 2 |
| `DATE_MONTH_SHIFT` | `64+35` | `src/FOREX_RUNTIME.mad:40` | `src/FOREX_RUNTIME.mad:356` | 1 |
| `DATE_TIME_SHIFT` | `64-22` | `src/FOREX_RUNTIME.mad:41` | `src/FOREX_RUNTIME.mad:373` | 1 |
| `DATE_YEAR_SHIFT` | `64-14` | `src/FOREX_RUNTIME.mad:42` | `src/FOREX_RUNTIME.mad:368`, `src/FOREX_RUNTIME.mad:394` | 2 |
| `DEC_7` | `7` | `src/FOREX_RUNTIME.mad:43` | `src/FOREX_RUNTIME.mad:200`, `src/FOREX_RUNTIME.mad:212`, `src/FOREX_RUNTIME.mad:224`, `src/FOREX_RUNTIME.mad:252` | 4 |
| `FIXED_MODE_2` | `2` | `src/FOREX_RUNTIME.mad:44` | `src/FOREX_RUNTIME.mad:509` | 1 |
| `FT002_DISPATCH` | `77776B` | `src/FOREX_RUNTIME.mad:45` | `src/FOREX_RUNTIME.mad:182` | 1 |
| `FT003_DISPATCH` | `77775B` | `src/FOREX_RUNTIME.mad:46` | `src/FOREX_RUNTIME.mad:184` | 1 |
| `FT521_DISPATCH` | `77257B` | `src/FOREX_RUNTIME.mad:47` | `src/FOREX_RUNTIME.mad:176` | 1 |
| `FT531_DISPATCH` | `77247B` | `src/FOREX_RUNTIME.mad:48` | `src/FOREX_RUNTIME.mad:170` | 1 |
| `FT541_DISPATCH` | `77237B` | `src/FOREX_RUNTIME.mad:49` | `src/FOREX_RUNTIME.mad:166` | 1 |
| `FT561_DISPATCH` | `77217B` | `src/FOREX_RUNTIME.mad:50` | `src/FOREX_RUNTIME.mad:172` | 1 |
| `FT571_DISPATCH` | `77207B` | `src/FOREX_RUNTIME.mad:51` | `src/FOREX_RUNTIME.mad:164` | 1 |
| `FT611_DISPATCH` | `77167B` | `src/FOREX_RUNTIME.mad:52` | `src/FOREX_RUNTIME.mad:168` | 1 |
| `FT621_DISPATCH` | `77157B` | `src/FOREX_RUNTIME.mad:53` | `src/FOREX_RUNTIME.mad:174` | 1 |
| `FT641_DISPATCH` | `77137B` | `src/FOREX_RUNTIME.mad:54` | `src/FOREX_RUNTIME.mad:180` | 1 |
| `FT721_DISPATCH` | `77057B` | `src/FOREX_RUNTIME.mad:55` | `src/FOREX_RUNTIME.mad:178` | 1 |
| `FTD_TABLE_BASE_ADDR` | `77766B` | `src/FOREX_RUNTIME.mad:56` | `src/FOREX_RUNTIME.mad:143` | 1 |
| `FT_ADDR_FIELD` | `103B` | `src/FOREX_RUNTIME.mad:57` | `src/FOREX_RUNTIME.mad:136` | 1 |
| `FT_OFFSET_MASK` | `155B` | `src/FOREX_RUNTIME.mad:58` | `src/FOREX_RUNTIME.mad:154` | 1 |
| `GOST_BLANK` | `6H` | `src/FOREX_RUNTIME.mad:59` | `src/FOREX_RUNTIME.mad:515` | 1 |
| `INT_ZERO` | `0` | `src/FOREX_RUNTIME.mad:60` | `src/FOREX_RUNTIME.mad:470` | 1 |
| `ISO_CODE_SHIFT` | `54B` | `src/FOREX_RUNTIME.mad:61` | `src/FOREX_RUNTIME.mad:295` | 1 |
| `ISO_WORD_SHIFT` | `64` | `src/FOREX_RUNTIME.mad:62` | `src/FOREX_RUNTIME.mad:365`, `src/FOREX_RUNTIME.mad:495`, `src/FOREX_RUNTIME.mad:497` | 3 |
| `LIB_BUFFER_LEN` | `2000B` | `src/FOREX_RUNTIME.mad:63` | `src/FOREX_RUNTIME.mad:194` | 1 |
| `LIT_10` | `10` | `src/FOREX_RUNTIME.mad:64` | `src/FOREX_RUNTIME.mad:460` | 1 |
| `LIT_10000000_00000000` | `10000000 00000000` | `src/FOREX_RUNTIME.mad:65` | `src/FOREX_RUNTIME.mad:186` | 1 |
| `LIT_2` | `2` | `src/FOREX_RUNTIME.mad:66` | `src/FOREX_RUNTIME.mad:450` | 1 |
| `LIT_3` | `3` | `src/FOREX_RUNTIME.mad:67` | `src/FOREX_RUNTIME.mad:447` | 1 |
| `MODE_6` | `6` | `src/FOREX_RUNTIME.mad:68` | `src/FOREX_RUNTIME.mad:345`, `include/FOREX_ROOT.mad:82`, `include/FOREX_ROOT.mad:113`, `include/FOREX_ROOT.mad:126` | 4 |
| `MONTH_INDEX_BASE` | `24` | `src/FOREX_RUNTIME.mad:69` | `src/FOREX_RUNTIME.mad:359` | 1 |
| `OCT_SIX_DIGIT_MASK` | `=777 7777-C` | `src/FOREX_RUNTIME.mad:70` | `src/FOREX_RUNTIME.mad:438` | 1 |
| `ONE_WORD` | `1` | `src/FOREX_RUNTIME.mad:71` | `src/FOREX_CORE.mad:150`, `src/FOREX_CORE.mad:151`, `src/FOREX_CORE.mad:152`, `src/FOREX_CORE.mad:155`, `src/FOREX_CORE.mad:157`, `src/FOREX_RUNTIME.mad:255` … (+14) | 20 |
| `POW10_5` | `100000.0` | `src/FOREX_RUNTIME.mad:72` | `src/FOREX_RUNTIME.mad:472` | 1 |
| `REAL_MODE_3` | `3` | `src/FOREX_RUNTIME.mad:73` | `src/FOREX_RUNTIME.mad:217`, `src/FOREX_RUNTIME.mad:490`, `include/FOREX_ROOT.mad:116` | 3 |
| `RET_LINK_REG` | `13` | `src/FOREX_RUNTIME.mad:74` | `src/FOREX_CORE.mad:192`, `src/FOREX_CORE.mad:313`, `src/FOREX_RUNTIME.mad:201`, `src/FOREX_RUNTIME.mad:211`, `src/FOREX_RUNTIME.mad:338`, `src/FOREX_RUNTIME.mad:378` … (+6) | 12 |
| `STACK_OFF_M1` | `-1` | `src/FOREX_RUNTIME.mad:75` | `src/FOREX_RUNTIME.mad:404` | 1 |
| `STACK_OFF_M2` | `-2` | `src/FOREX_RUNTIME.mad:76` | `src/FOREX_RUNTIME.mad:350`, `src/FOREX_RUNTIME.mad:505`, `include/FOREX_ROOT.mad:255` | 3 |
| `STACK_OFF_M3` | `-3` | `src/FOREX_RUNTIME.mad:77` | `src/FOREX_RUNTIME.mad:354`, `src/FOREX_RUNTIME.mad:494`, `src/FOREX_RUNTIME.mad:500` | 3 |
| `STACK_OFF_M4` | `-4` | `src/FOREX_RUNTIME.mad:78` | `src/FOREX_RUNTIME.mad:367`, `src/FOREX_RUNTIME.mad:372`, `src/FOREX_RUNTIME.mad:498` | 3 |
| `STACK_OFF_M5` | `-5` | `src/FOREX_RUNTIME.mad:79` | `src/FOREX_RUNTIME.mad:403`, `src/FOREX_RUNTIME.mad:441` | 2 |
| `STACK_OFF_M6` | `-6` | `src/FOREX_RUNTIME.mad:80` | `src/FOREX_RUNTIME.mad:384` | 1 |
| `STACK_OFF_M8` | `-8` | `src/FOREX_RUNTIME.mad:81` | `src/FOREX_RUNTIME.mad:377` | 1 |
| `TEXT_LIT_000000` | `''000000''` | `src/FOREX_RUNTIME.mad:82` | `src/FOREX_RUNTIME.mad:478` | 1 |
| `TEXT_LIT_1H_055` | `1H'055'` | `src/FOREX_RUNTIME.mad:83` | `src/FOREX_RUNTIME.mad:409` | 1 |
| `TEXT_LIT_2H_200` | `2H '200'` | `src/FOREX_RUNTIME.mad:84` | `src/FOREX_RUNTIME.mad:407` | 1 |
| `TEXT_LIT_3H00` | `3H00` | `src/FOREX_RUNTIME.mad:85` | `src/FOREX_RUNTIME.mad:410` | 1 |
| `TEXT_LIT_6H00` | `=6H00` | `src/FOREX_RUNTIME.mad:86` | `src/FOREX_RUNTIME.mad:396` | 1 |
| `TEXT_LIT_6H0000` | `6H0000` | `src/FOREX_RUNTIME.mad:87` | — | 0 |
| `TEXT_LIT_6H000000` | `6H000000` | `src/FOREX_RUNTIME.mad:88` | `src/FOREX_RUNTIME.mad:516` | 1 |
| `TEXT_LIT_6H000_00` | `6H000 00` | `src/FOREX_RUNTIME.mad:89` | `src/FOREX_RUNTIME.mad:411` | 1 |
| `TEXT_LIT_6H00_00` | `=6H00/00/` | `src/FOREX_RUNTIME.mad:90` | `src/FOREX_RUNTIME.mad:399` | 1 |
| `TEXT_LIT_6H03_0` | `6H03 0` | `src/FOREX_RUNTIME.mad:91` | — | 0 |
| `TEXT_LIT_6HAB_CEH` | `6HABГCEH` | `src/FOREX_RUNTIME.mad:92` | `src/FOREX_RUNTIME.mad:417` | 1 |
| `TEXT_LIT_6HARRAY` | `6HARRAY` | `src/FOREX_RUNTIME.mad:93` | `src/FOREX_RUNTIME.mad:321` | 1 |
| `TEXT_LIT_6HA_PMA` | `6HAПPMAЯ` | `src/FOREX_RUNTIME.mad:94` | `src/FOREX_RUNTIME.mad:415` | 1 |
| `TEXT_LIT_6HERROR` | `6HERROR` | `src/FOREX_RUNTIME.mad:95` | `src/FOREX_RUNTIME.mad:318` | 1 |
| `TEXT_LIT_6HIN_STA` | `6HIN STA` | `src/FOREX_RUNTIME.mad:96` | `src/FOREX_RUNTIME.mad:319` | 1 |
| `TEXT_LIT_6HNDART` | `6HNDART` | `src/FOREX_RUNTIME.mad:97` | `src/FOREX_RUNTIME.mad:320` | 1 |
| `TEXT_LIT_6HOKTHO` | `6HOKTHOЯ` | `src/FOREX_RUNTIME.mad:98` | `src/FOREX_RUNTIME.mad:422` | 1 |
| `TEXT_LIT_6H_00_00` | `6H 00.00` | `src/FOREX_RUNTIME.mad:99` | `src/FOREX_RUNTIME.mad:418` | 1 |
| `TEXT_LIT_6H_17_17` | `=6H'17''17'''''''''` | `src/FOREX_RUNTIME.mad:100` | `src/FOREX_RUNTIME.mad:395` | 1 |
| `TEXT_LIT_6H_201_200_7` | `6H'201'  '200'7` | `src/FOREX_RUNTIME.mad:101` | `src/FOREX_RUNTIME.mad:406` | 1 |
| `TEXT_LIT_6H_231_HB` | `6H'231'  ЯHB` | `src/FOREX_RUNTIME.mad:102` | — | 0 |
| `TEXT_LIT_6H_3_17_17_17` | `=6H'3''17''''17''17'''` | `src/FOREX_RUNTIME.mad:103` | `src/FOREX_RUNTIME.mad:398` | 1 |
| `TEXT_LIT_6H_EBMAP` | `6HФEBMAP` | `src/FOREX_RUNTIME.mad:104` | `src/FOREX_RUNTIME.mad:414` | 1 |
| `TEXT_LIT_6H_EK` | `6HДEK` | `src/FOREX_RUNTIME.mad:105` | `src/FOREX_RUNTIME.mad:423` | 1 |
| `TEXT_LIT_6H_H` | `6HИЮHИЮЛ` | `src/FOREX_RUNTIME.mad:106` | `src/FOREX_RUNTIME.mad:416` | 1 |
| `FUN_DATE_TIME` | `67B` | `src/FOREX_RUNTIME.mad:107` | `src/FOREX_RUNTIME.mad:344` | 1 |
| `DATE_BUF_LEN` | `2` | `src/FOREX_RUNTIME.mad:108` | `src/FOREX_RUNTIME.mad:330` | 1 |
| `MONTH_FIELD_OCT` | `00 776` | `src/FOREX_RUNTIME.mad:109` | — | 0 |
| `OCT_ISO_SHIFT` | `64-8` | `src/FOREX_RUNTIME.mad:110` | `src/FOREX_RUNTIME.mad:463` | 1 |
| `POW10_4` | `10000.0` | `src/FOREX_RUNTIME.mad:111` | `src/FOREX_RUNTIME.mad:473` | 1 |
| `POW10_3` | `1000.0` | `src/FOREX_RUNTIME.mad:112` | `src/FOREX_RUNTIME.mad:474` | 1 |
| `POW10_2` | `100.0` | `src/FOREX_RUNTIME.mad:113` | `src/FOREX_RUNTIME.mad:475` | 1 |
| `POW10_1` | `10.0` | `src/FOREX_RUNTIME.mad:114` | `src/FOREX_RUNTIME.mad:476` | 1 |
| `FT541_ADDR` | `77237B` | `src/LO_GEN.mad:44` | `src/LO_GEN.mad:3557`, `src/LO_GEN.mad:3561` | 2 |
| `FT721_ADDR` | `77057B` | `src/LO_GEN.mad:45` | `src/LO_GEN.mad:3224` | 1 |
| `ADDR_1` | `1B` | `src/LO_GEN.mad:46` | `src/LO_GEN.mad:694`, `src/LO_GEN.mad:697`, `src/LO_GEN.mad:703`, `src/LO_GEN.mad:706`, `src/LO_GEN.mad:789`, `src/LO_GEN.mad:792` … (+59) | 65 |
| `ADDR_10` | `10B` | `src/LO_GEN.mad:47` | `src/LO_GEN.mad:804`, `src/LO_GEN.mad:834`, `src/LO_GEN.mad:3020`, `src/LO_GEN.mad:3374`, `src/LO_GEN.mad:3465` | 5 |
| `ADDR_100` | `100B` | `src/LO_GEN.mad:48` | `src/LO_GEN.mad:638`, `src/LO_GEN.mad:673`, `src/LO_GEN.mad:3344` | 3 |
| `ADDR_101` | `101B` | `src/LO_GEN.mad:49` | `src/LO_GEN.mad:3347`, `src/LO_GEN.mad:3381` | 2 |
| `ADDR_1010` | `1010B` | `src/LO_GEN.mad:50` | `src/LO_GEN.mad:1407` | 1 |
| `ADDR_1017` | `1017B` | `src/LO_GEN.mad:51` | `src/LO_GEN.mad:1374` | 1 |
| `ADDR_102` | `102B` | `src/LO_GEN.mad:52` | `src/LO_GEN.mad:3356` | 1 |
| `ADDR_1021` | `1021B` | `src/LO_GEN.mad:53` | `src/LO_GEN.mad:1377` | 1 |
| `ADDR_103` | `103B` | `src/LO_GEN.mad:54` | `src/LO_GEN.mad:3359` | 1 |
| `ADDR_1031` | `1031B` | `src/LO_GEN.mad:55` | `src/LO_GEN.mad:1422` | 1 |
| `ADDR_1035` | `1035B` | `src/LO_GEN.mad:56` | `src/LO_GEN.mad:1431` | 1 |
| `ADDR_104` | `104B` | `src/LO_GEN.mad:57` | `src/LO_GEN.mad:3362` | 1 |
| `ADDR_1044` | `1044B` | `src/LO_GEN.mad:58` | `src/LO_GEN.mad:1425` | 1 |
| `ADDR_105` | `105B` | `src/LO_GEN.mad:59` | `src/LO_GEN.mad:3366` | 1 |
| `ADDR_11` | `11B` | `src/LO_GEN.mad:60` | `src/LO_GEN.mad:626`, `src/LO_GEN.mad:807`, `src/LO_GEN.mad:840`, `src/LO_GEN.mad:1167`, `src/LO_GEN.mad:1993`, `src/LO_GEN.mad:2842` … (+2) | 8 |
| `ADDR_117` | `117B` | `src/LO_GEN.mad:61` | — | 0 |
| `ADDR_12` | `12B` | `src/LO_GEN.mad:62` | `src/LO_GEN.mad:684`, `src/LO_GEN.mad:823`, `src/LO_GEN.mad:3384` | 3 |
| `ADDR_1210` | `1210B` | `src/LO_GEN.mad:63` | `src/LO_GEN.mad:1476` | 1 |
| `ADDR_127` | `127B` | `src/LO_GEN.mad:64` | `src/LO_GEN.mad:2410` | 1 |
| `ADDR_13` | `13B` | `src/LO_GEN.mad:65` | `src/LO_GEN.mad:826`, `src/LO_GEN.mad:831`, `src/LO_GEN.mad:835`, `src/LO_GEN.mad:1012`, `src/LO_GEN.mad:1059`, `src/LO_GEN.mad:1080` … (+21) | 27 |
| `ADDR_132` | `132B` | `src/LO_GEN.mad:66` | `src/LO_GEN.mad:2484`, `src/LO_GEN.mad:2493`, `src/LO_GEN.mad:2508`, `src/LO_GEN.mad:2517`, `src/LO_GEN.mad:2544`, `src/LO_GEN.mad:2553` … (+3) | 9 |
| `ADDR_1322` | `1322B` | `src/LO_GEN.mad:67` | `src/LO_GEN.mad:1290` | 1 |
| `ADDR_1324` | `1324B` | `src/LO_GEN.mad:68` | `src/LO_GEN.mad:1293` | 1 |
| `ADDR_1326` | `1326B` | `src/LO_GEN.mad:69` | `src/LO_GEN.mad:1296` | 1 |
| `ADDR_133` | `133B` | `src/LO_GEN.mad:70` | `src/LO_GEN.mad:693`, `src/LO_GEN.mad:1201` | 2 |
| `ADDR_1330` | `1330B` | `src/LO_GEN.mad:71` | `src/LO_GEN.mad:1302` | 1 |
| `ADDR_1332` | `1332B` | `src/LO_GEN.mad:72` | `src/LO_GEN.mad:1305` | 1 |
| `ADDR_1334` | `1334B` | `src/LO_GEN.mad:73` | `src/LO_GEN.mad:1314` | 1 |
| `ADDR_1336` | `1336B` | `src/LO_GEN.mad:74` | `src/LO_GEN.mad:1434` | 1 |
| `ADDR_134` | `134B` | `src/LO_GEN.mad:75` | `src/LO_GEN.mad:1821`, `src/LO_GEN.mad:1840`, `src/LO_GEN.mad:1848`, `src/LO_GEN.mad:1866`, `src/LO_GEN.mad:2230`, `src/LO_GEN.mad:2272` … (+6) | 12 |
| `ADDR_1343` | `1343B` | `src/LO_GEN.mad:76` | `src/LO_GEN.mad:1329` | 1 |
| `ADDR_1347` | `1347B` | `src/LO_GEN.mad:77` | `src/LO_GEN.mad:1299` | 1 |
| `ADDR_135` | `135B` | `src/LO_GEN.mad:78` | `src/LO_GEN.mad:2862`, `src/LO_GEN.mad:2869` | 2 |
| `ADDR_1351` | `1351B` | `src/LO_GEN.mad:79` | `src/LO_GEN.mad:1512`, `src/LO_GEN.mad:1518` | 2 |
| `ADDR_1355` | `1355B` | `src/LO_GEN.mad:80` | `src/LO_GEN.mad:1536` | 1 |
| `ADDR_136` | `136B` | `src/LO_GEN.mad:81` | `src/LO_GEN.mad:901`, `src/LO_GEN.mad:1710`, `src/LO_GEN.mad:1771`, `src/LO_GEN.mad:1783`, `src/LO_GEN.mad:1804`, `src/LO_GEN.mad:2032` … (+5) | 11 |
| `ADDR_1360` | `1360B` | `src/LO_GEN.mad:82` | `src/LO_GEN.mad:1509`, `src/LO_GEN.mad:1515` | 2 |
| `ADDR_1362` | `1362B` | `src/LO_GEN.mad:83` | `src/LO_GEN.mad:1524`, `src/LO_GEN.mad:1533` | 2 |
| `ADDR_137` | `137B` | `src/LO_GEN.mad:84` | `src/LO_GEN.mad:1924`, `src/LO_GEN.mad:1929`, `src/LO_GEN.mad:2380`, `src/LO_GEN.mad:3422` | 4 |
| `ADDR_1374` | `1374B` | `src/LO_GEN.mad:85` | `src/LO_GEN.mad:1539` | 1 |
| `ADDR_14` | `14B` | `src/LO_GEN.mad:86` | `src/LO_GEN.mad:850`, `src/LO_GEN.mad:882`, `src/LO_GEN.mad:910`, `src/LO_GEN.mad:925`, `src/LO_GEN.mad:973`, `src/LO_GEN.mad:1129` … (+7) | 13 |
| `ADDR_140` | `140B` | `src/LO_GEN.mad:87` | `src/LO_GEN.mad:2722`, `src/LO_GEN.mad:2748`, `src/LO_GEN.mad:2893`, `src/LO_GEN.mad:3471` | 4 |
| `ADDR_141` | `141B` | `src/LO_GEN.mad:88` | `src/LO_GEN.mad:708`, `src/LO_GEN.mad:1128`, `src/LO_GEN.mad:1158`, `src/LO_GEN.mad:1737`, `src/LO_GEN.mad:1824`, `src/LO_GEN.mad:1828` … (+11) | 17 |
| `ADDR_142` | `142B` | `src/LO_GEN.mad:89` | `src/LO_GEN.mad:2535`, `src/LO_GEN.mad:3245`, `src/LO_GEN.mad:3264`, `src/LO_GEN.mad:3267`, `src/LO_GEN.mad:3269`, `src/LO_GEN.mad:3426` | 6 |
| `ADDR_143` | `143B` | `src/LO_GEN.mad:90` | `src/LO_GEN.mad:1731`, `src/LO_GEN.mad:2035`, `src/LO_GEN.mad:2191`, `src/LO_GEN.mad:2206`, `src/LO_GEN.mad:2208` | 5 |
| `ADDR_1437` | `1437B` | `src/LO_GEN.mad:91` | `src/LO_GEN.mad:1542` | 1 |
| `ADDR_15` | `15B` | `src/LO_GEN.mad:92` | `src/LO_GEN.mad:595`, `src/LO_GEN.mad:855` | 2 |
| `ADDR_151` | `151B` | `src/LO_GEN.mad:93` | `src/LO_GEN.mad:934` | 1 |
| `ADDR_153` | `153B` | `src/LO_GEN.mad:94` | `src/LO_GEN.mad:880`, `src/LO_GEN.mad:1039`, `src/LO_GEN.mad:1186` | 3 |
| `ADDR_1543` | `1543B` | `src/LO_GEN.mad:95` | `src/LO_GEN.mad:1527` | 1 |
| `ADDR_16` | `16B` | `src/LO_GEN.mad:96` | `src/LO_GEN.mad:572`, `src/LO_GEN.mad:856`, `src/LO_GEN.mad:3402`, `src/LO_GEN.mad:3429`, `src/LO_GEN.mad:3516` | 5 |
| `ADDR_1641` | `1641B` | `src/LO_GEN.mad:97` | `src/LO_GEN.mad:682` | 1 |
| `ADDR_1647` | `1647B` | `src/LO_GEN.mad:98` | `src/LO_GEN.mad:590` | 1 |
| `ADDR_17` | `17B` | `src/LO_GEN.mad:99` | `src/LO_GEN.mad:571`, `src/LO_GEN.mad:584`, `src/LO_GEN.mad:868` | 3 |
| `ADDR_176` | `176B` | `src/LO_GEN.mad:100` | `src/LO_GEN.mad:1521`, `src/LO_GEN.mad:1530` | 2 |
| `ADDR_2` | `2B` | `src/LO_GEN.mad:101` | `src/LO_GEN.mad:611`, `src/LO_GEN.mad:712`, `src/LO_GEN.mad:1120`, `src/LO_GEN.mad:2412`, `src/LO_GEN.mad:3053`, `src/LO_GEN.mad:3135` | 6 |
| `ADDR_20` | `20B` | `src/LO_GEN.mad:102` | `src/LO_GEN.mad:568`, `src/LO_GEN.mad:870` | 2 |
| `ADDR_21` | `21B` | `src/LO_GEN.mad:103` | `src/LO_GEN.mad:574`, `src/LO_GEN.mad:587`, `src/LO_GEN.mad:874`, `src/LO_GEN.mad:3177` | 4 |
| `ADDR_211` | `211B` | `src/LO_GEN.mad:104` | `src/LO_GEN.mad:560` | 1 |
| `ADDR_22` | `22B` | `src/LO_GEN.mad:105` | `src/LO_GEN.mad:886`, `src/LO_GEN.mad:2166` | 2 |
| `ADDR_2200` | `2200B` | `src/LO_GEN.mad:106` | — | 0 |
| `ADDR_2254` | `2254B` | `src/LO_GEN.mad:107` | `src/LO_GEN.mad:1362` | 1 |
| `ADDR_22662` | `22662B` | `src/LO_GEN.mad:108` | `src/LO_GEN.mad:661` | 1 |
| `ADDR_23` | `23B` | `src/LO_GEN.mad:109` | `src/LO_GEN.mad:915`, `src/LO_GEN.mad:3011`, `src/LO_GEN.mad:3036` | 3 |
| `ADDR_24` | `24B` | `src/LO_GEN.mad:110` | `src/LO_GEN.mad:930`, `src/LO_GEN.mad:952`, `src/LO_GEN.mad:964`, `src/LO_GEN.mad:1066`, `src/LO_GEN.mad:1152`, `src/LO_GEN.mad:1708` … (+34) | 40 |
| `ADDR_25` | `25B` | `src/LO_GEN.mad:111` | `src/LO_GEN.mad:936` | 1 |
| `ADDR_26` | `26B` | `src/LO_GEN.mad:112` | `src/LO_GEN.mad:958`, `src/LO_GEN.mad:1086`, `src/LO_GEN.mad:1200`, `src/LO_GEN.mad:1773`, `src/LO_GEN.mad:1782`, `src/LO_GEN.mad:1857` … (+11) | 17 |
| `ADDR_27` | `27B` | `src/LO_GEN.mad:113` | `src/LO_GEN.mad:1009`, `src/LO_GEN.mad:1837`, `src/LO_GEN.mad:1894`, `src/LO_GEN.mad:2356`, `src/LO_GEN.mad:3539`, `src/LO_GEN.mad:3542` | 6 |
| `ADDR_3` | `3B` | `src/LO_GEN.mad:114` | `src/LO_GEN.mad:620`, `src/LO_GEN.mad:715`, `src/LO_GEN.mad:3059` | 3 |
| `ADDR_30` | `30B` | `src/LO_GEN.mad:115` | `src/LO_GEN.mad:1029`, `src/LO_GEN.mad:1116`, `src/LO_GEN.mad:2170`, `src/LO_GEN.mad:2460`, `src/LO_GEN.mad:2485`, `src/LO_GEN.mad:2509` … (+7) | 13 |
| `ADDR_30274` | `30274B` | `src/LO_GEN.mad:116` | `src/LO_GEN.mad:565`, `src/LO_GEN.mad:583` | 2 |
| `ADDR_30312` | `30312B` | `src/LO_GEN.mad:117` | `src/LO_GEN.mad:578` | 1 |
| `ADDR_30314` | `30314B` | `src/LO_GEN.mad:118` | — | 0 |
| `ADDR_31` | `31B` | `src/LO_GEN.mad:119` | `src/LO_GEN.mad:1053`, `src/LO_GEN.mad:1203`, `src/LO_GEN.mad:2569`, `src/LO_GEN.mad:2697` | 4 |
| `ADDR_32` | `32B` | `src/LO_GEN.mad:120` | `src/LO_GEN.mad:1102`, `src/LO_GEN.mad:1944`, `src/LO_GEN.mad:2058`, `src/LO_GEN.mad:2103`, `src/LO_GEN.mad:2625`, `src/LO_GEN.mad:2673` … (+5) | 11 |
| `ADDR_33` | `33B` | `src/LO_GEN.mad:121` | `src/LO_GEN.mad:1110`, `src/LO_GEN.mad:2830` | 2 |
| `ADDR_34` | `34B` | `src/LO_GEN.mad:122` | `src/LO_GEN.mad:1111`, `src/LO_GEN.mad:2832` | 2 |
| `ADDR_35` | `35B` | `src/LO_GEN.mad:123` | `src/LO_GEN.mad:1134`, `src/LO_GEN.mad:1258`, `src/LO_GEN.mad:2494`, `src/LO_GEN.mad:2518`, `src/LO_GEN.mad:2554`, `src/LO_GEN.mad:2667` … (+1) | 7 |
| `ADDR_36` | `36B` | `src/LO_GEN.mad:124` | `src/LO_GEN.mad:1231`, `src/LO_GEN.mad:2981` | 2 |
| `ADDR_37` | `37B` | `src/LO_GEN.mad:125` | `src/LO_GEN.mad:1236`, `src/LO_GEN.mad:1968` | 2 |
| `ADDR_370` | `370B` | `src/LO_GEN.mad:126` | `src/LO_GEN.mad:614` | 1 |
| `ADDR_4` | `4B` | `src/LO_GEN.mad:127` | `src/LO_GEN.mad:721` | 1 |
| `ADDR_40` | `40B` | `src/LO_GEN.mad:128` | `src/LO_GEN.mad:1275` | 1 |
| `ADDR_400` | `400B` | `src/LO_GEN.mad:129` | — | 0 |
| `ADDR_40227` | `40227B` | `src/LO_GEN.mad:130` | `src/LO_GEN.mad:744` | 1 |
| `ADDR_40377` | `40377B` | `src/LO_GEN.mad:131` | `src/LO_GEN.mad:1182` | 1 |
| `ADDR_40401` | `40401B` | `src/LO_GEN.mad:132` | `src/LO_GEN.mad:1191` | 1 |
| `ADDR_40403` | `40403B` | `src/LO_GEN.mad:133` | `src/LO_GEN.mad:1227` | 1 |
| `ADDR_40405` | `40405B` | `src/LO_GEN.mad:134` | `src/LO_GEN.mad:1266` | 1 |
| `ADDR_40407` | `40407B` | `src/LO_GEN.mad:135` | `src/LO_GEN.mad:1439` | 1 |
| `ADDR_40411` | `40411B` | `src/LO_GEN.mad:136` | `src/LO_GEN.mad:2488`, `src/LO_GEN.mad:2548` | 2 |
| `ADDR_40417` | `40417B` | `src/LO_GEN.mad:137` | `src/LO_GEN.mad:2512` | 1 |
| `ADDR_40421` | `40421B` | `src/LO_GEN.mad:138` | `src/LO_GEN.mad:1436` | 1 |
| `ADDR_40423` | `40423B` | `src/LO_GEN.mad:139` | `src/LO_GEN.mad:1499` | 1 |
| `ADDR_40425` | `40425B` | `src/LO_GEN.mad:140` | `src/LO_GEN.mad:2502`, `src/LO_GEN.mad:2562` | 2 |
| `ADDR_40433` | `40433B` | `src/LO_GEN.mad:141` | `src/LO_GEN.mad:2526` | 1 |
| `ADDR_40435` | `40435B` | `src/LO_GEN.mad:142` | `src/LO_GEN.mad:1496` | 1 |
| `ADDR_40437` | `40437B` | `src/LO_GEN.mad:143` | `src/LO_GEN.mad:2497`, `src/LO_GEN.mad:2557` | 2 |
| `ADDR_40445` | `40445B` | `src/LO_GEN.mad:144` | `src/LO_GEN.mad:2521` | 1 |
| `ADDR_40447` | `40447B` | `src/LO_GEN.mad:145` | `src/LO_GEN.mad:1457` | 1 |
| `ADDR_40451` | `40451B` | `src/LO_GEN.mad:146` | `src/LO_GEN.mad:1454` | 1 |
| `ADDR_40453` | `40453B` | `src/LO_GEN.mad:147` | `src/LO_GEN.mad:1451` | 1 |
| `ADDR_40455` | `40455B` | `src/LO_GEN.mad:148` | `src/LO_GEN.mad:1493` | 1 |
| `ADDR_40457` | `40457B` | `src/LO_GEN.mad:149` | `src/LO_GEN.mad:1490` | 1 |
| `ADDR_40461` | `40461B` | `src/LO_GEN.mad:150` | `src/LO_GEN.mad:1442` | 1 |
| `ADDR_40463` | `40463B` | `src/LO_GEN.mad:151` | `src/LO_GEN.mad:1445` | 1 |
| `ADDR_40465` | `40465B` | `src/LO_GEN.mad:152` | `src/LO_GEN.mad:1448` | 1 |
| `ADDR_40467` | `40467B` | `src/LO_GEN.mad:153` | `src/LO_GEN.mad:1460` | 1 |
| `ADDR_41` | `41B` | `src/LO_GEN.mad:154` | `src/LO_GEN.mad:1337` | 1 |
| `ADDR_4114` | `4114B` | `src/LO_GEN.mad:155` | `src/LO_GEN.mad:632`, `src/LO_GEN.mad:667` | 2 |
| `ADDR_42` | `42B` | `src/LO_GEN.mad:156` | `src/LO_GEN.mad:1340` | 1 |
| `ADDR_42413` | `42413B` | `src/LO_GEN.mad:157` | `src/LO_GEN.mad:619`, `src/LO_GEN.mad:690`, `src/LO_GEN.mad:3506` | 3 |
| `ADDR_42551` | `42551B` | `src/LO_GEN.mad:158` | `src/LO_GEN.mad:1764`, `src/LO_GEN.mad:1797`, `src/LO_GEN.mad:2073` | 3 |
| `ADDR_42556` | `42556B` | `src/LO_GEN.mad:159` | `src/LO_GEN.mad:2037`, `src/LO_GEN.mad:2193` | 2 |
| `ADDR_43` | `43B` | `src/LO_GEN.mad:160` | `src/LO_GEN.mad:1343`, `src/LO_GEN.mad:3216` | 2 |
| `ADDR_44` | `44B` | `src/LO_GEN.mad:161` | `src/LO_GEN.mad:1346`, `src/LO_GEN.mad:2022`, `src/LO_GEN.mad:3275` | 3 |
| `ADDR_45` | `45B` | `src/LO_GEN.mad:162` | `src/LO_GEN.mad:1758`, `src/LO_GEN.mad:2137`, `src/LO_GEN.mad:2313`, `src/LO_GEN.mad:2806`, `src/LO_GEN.mad:3326` | 5 |
| `ADDR_46` | `46B` | `src/LO_GEN.mad:163` | `src/LO_GEN.mad:1947`, `src/LO_GEN.mad:2061`, `src/LO_GEN.mad:2106`, `src/LO_GEN.mad:2628`, `src/LO_GEN.mad:2790`, `src/LO_GEN.mad:2817` … (+3) | 9 |
| `ADDR_46126` | `46126B` | `src/LO_GEN.mad:164` | `src/LO_GEN.mad:634` | 1 |
| `ADDR_47` | `47B` | `src/LO_GEN.mad:165` | `src/LO_GEN.mad:1986` | 1 |
| `ADDR_471` | `471B` | `src/LO_GEN.mad:166` | `src/LO_GEN.mad:1395` | 1 |
| `ADDR_47753` | `47753B` | `src/LO_GEN.mad:167` | `src/LO_GEN.mad:575` | 1 |
| `ADDR_5` | `5B` | `src/LO_GEN.mad:168` | `src/LO_GEN.mad:646`, `src/LO_GEN.mad:652`, `src/LO_GEN.mad:726`, `src/LO_GEN.mad:808`, `src/LO_GEN.mad:978`, `src/LO_GEN.mad:1018` … (+21) | 27 |
| `ADDR_50` | `50B` | `src/LO_GEN.mad:169` | `src/LO_GEN.mad:2007`, `src/LO_GEN.mad:2143`, `src/LO_GEN.mad:3233` | 3 |
| `ADDR_50520` | `50520B` | `src/LO_GEN.mad:170` | `src/LO_GEN.mad:660` | 1 |
| `ADDR_50530` | `50530B` | `src/LO_GEN.mad:171` | `src/LO_GEN.mad:635`, `src/LO_GEN.mad:670` | 2 |
| `ADDR_51` | `51B` | `src/LO_GEN.mad:172` | `src/LO_GEN.mad:2010`, `src/LO_GEN.mad:2125`, `src/LO_GEN.mad:2598`, `src/LO_GEN.mad:2638`, `src/LO_GEN.mad:2641`, `src/LO_GEN.mad:2904` … (+8) | 14 |
| `ADDR_52` | `52B` | `src/LO_GEN.mad:173` | `src/LO_GEN.mad:2019` | 1 |
| `ADDR_52117` | `52117B` | `src/LO_GEN.mad:174` | `src/LO_GEN.mad:655` | 1 |
| `ADDR_523` | `523B` | `src/LO_GEN.mad:175` | `src/LO_GEN.mad:593` | 1 |
| `ADDR_52514` | `52514B` | `src/LO_GEN.mad:176` | `src/LO_GEN.mad:669` | 1 |
| `ADDR_5257` | `5257B` | `src/LO_GEN.mad:177` | `src/LO_GEN.mad:663` | 1 |
| `ADDR_53` | `53B` | `src/LO_GEN.mad:178` | `src/LO_GEN.mad:2115`, `src/LO_GEN.mad:2146` | 2 |
| `ADDR_53257` | `53257B` | `src/LO_GEN.mad:179` | `src/LO_GEN.mad:631` | 1 |
| `ADDR_5377` | `5377B` | `src/LO_GEN.mad:180` | `src/LO_GEN.mad:557` | 1 |
| `ADDR_54` | `54B` | `src/LO_GEN.mad:181` | `src/LO_GEN.mad:2122` | 1 |
| `ADDR_55` | `55B` | `src/LO_GEN.mad:182` | `src/LO_GEN.mad:2181`, `src/LO_GEN.mad:2212`, `src/LO_GEN.mad:2281` | 3 |
| `ADDR_56` | `56B` | `src/LO_GEN.mad:183` | `src/LO_GEN.mad:2184`, `src/LO_GEN.mad:2809` | 2 |
| `ADDR_565` | `565B` | `src/LO_GEN.mad:184` | `src/LO_GEN.mad:1365` | 1 |
| `ADDR_56561` | `56561B` | `src/LO_GEN.mad:185` | `src/LO_GEN.mad:1033`, `src/LO_GEN.mad:1081`, `src/LO_GEN.mad:1956`, `src/LO_GEN.mad:3260` | 4 |
| `ADDR_56563` | `56563B` | `src/LO_GEN.mad:186` | `src/LO_GEN.mad:1179`, `src/LO_GEN.mad:1263`, `src/LO_GEN.mad:2376`, `src/LO_GEN.mad:2394`, `src/LO_GEN.mad:3419` | 5 |
| `ADDR_56564` | `56564B` | `src/LO_GEN.mad:187` | `src/LO_GEN.mad:771`, `src/LO_GEN.mad:984`, `src/LO_GEN.mad:1746`, `src/LO_GEN.mad:2053` | 4 |
| `ADDR_56565` | `56565B` | `src/LO_GEN.mad:188` | `src/LO_GEN.mad:786` | 1 |
| `ADDR_56566` | `56566B` | `src/LO_GEN.mad:189` | `src/LO_GEN.mad:795`, `src/LO_GEN.mad:2028`, `src/LO_GEN.mad:2340` | 3 |
| `ADDR_56570` | `56570B` | `src/LO_GEN.mad:190` | `src/LO_GEN.mad:1818`, `src/LO_GEN.mad:1939`, `src/LO_GEN.mad:3008` | 3 |
| `ADDR_56571` | `56571B` | `src/LO_GEN.mad:191` | `src/LO_GEN.mad:1556`, `src/LO_GEN.mad:1565` | 2 |
| `ADDR_56572` | `56572B` | `src/LO_GEN.mad:192` | `src/LO_GEN.mad:1562`, `src/LO_GEN.mad:1571`, `src/LO_GEN.mad:1878` | 3 |
| `ADDR_56574` | `56574B` | `src/LO_GEN.mad:193` | `src/LO_GEN.mad:1281`, `src/LO_GEN.mad:1905` | 2 |
| `ADDR_56575` | `56575B` | `src/LO_GEN.mad:194` | `src/LO_GEN.mad:813`, `src/LO_GEN.mad:1248`, `src/LO_GEN.mad:1559`, `src/LO_GEN.mad:1568` | 4 |
| `ADDR_56576` | `56576B` | `src/LO_GEN.mad:195` | `src/LO_GEN.mad:999` | 1 |
| `ADDR_56577` | `56577B` | `src/LO_GEN.mad:196` | `src/LO_GEN.mad:846` | 1 |
| `ADDR_56601` | `56601B` | `src/LO_GEN.mad:197` | `src/LO_GEN.mad:969` | 1 |
| `ADDR_56602` | `56602B` | `src/LO_GEN.mad:198` | `src/LO_GEN.mad:2244` | 1 |
| `ADDR_56604` | `56604B` | `src/LO_GEN.mad:199` | `src/LO_GEN.mad:1975`, `src/LO_GEN.mad:2764` | 2 |
| `ADDR_56610` | `56610B` | `src/LO_GEN.mad:200` | `src/LO_GEN.mad:3212` | 1 |
| `ADDR_56612` | `56612B` | `src/LO_GEN.mad:201` | `src/LO_GEN.mad:2431` | 1 |
| `ADDR_56613` | `56613B` | `src/LO_GEN.mad:202` | `src/LO_GEN.mad:3227` | 1 |
| `ADDR_56615` | `56615B` | `src/LO_GEN.mad:203` | `src/LO_GEN.mad:2014`, `src/LO_GEN.mad:3093`, `src/LO_GEN.mad:3240`, `src/LO_GEN.mad:3486` | 4 |
| `ADDR_56616` | `56616B` | `src/LO_GEN.mad:204` | `src/LO_GEN.mad:2602` | 1 |
| `ADDR_56617` | `56617B` | `src/LO_GEN.mad:205` | `src/LO_GEN.mad:1779`, `src/LO_GEN.mad:1791`, `src/LO_GEN.mad:2040`, `src/LO_GEN.mad:2223`, `src/LO_GEN.mad:2298`, `src/LO_GEN.mad:2325` | 6 |
| `ADDR_56620` | `56620B` | `src/LO_GEN.mad:206` | `src/LO_GEN.mad:1767`, `src/LO_GEN.mad:1800`, `src/LO_GEN.mad:2076`, `src/LO_GEN.mad:2226`, `src/LO_GEN.mad:2295`, `src/LO_GEN.mad:2322` … (+1) | 7 |
| `ADDR_56621` | `56621B` | `src/LO_GEN.mad:207` | `src/LO_GEN.mad:2130`, `src/LO_GEN.mad:2196` | 2 |
| `ADDR_56623` | `56623B` | `src/LO_GEN.mad:208` | `src/LO_GEN.mad:2607` | 1 |
| `ADDR_56624` | `56624B` | `src/LO_GEN.mad:209` | `src/LO_GEN.mad:2574`, `src/LO_GEN.mad:2881` | 2 |
| `ADDR_567` | `567B` | `src/LO_GEN.mad:210` | `src/LO_GEN.mad:1368` | 1 |
| `ADDR_57` | `57B` | `src/LO_GEN.mad:211` | `src/LO_GEN.mad:2241` | 1 |
| `ADDR_577` | `577B` | `src/LO_GEN.mad:212` | `src/LO_GEN.mad:1380` | 1 |
| `ADDR_6` | `6B` | `src/LO_GEN.mad:213` | `src/LO_GEN.mad:730`, `src/LO_GEN.mad:1050`, `src/LO_GEN.mad:1752`, `src/LO_GEN.mad:1761`, `src/LO_GEN.mad:1794`, `src/LO_GEN.mad:1830` … (+8) | 14 |
| `ADDR_60` | `60B` | `src/LO_GEN.mad:214` | `src/LO_GEN.mad:2245` | 1 |
| `ADDR_601` | `601B` | `src/LO_GEN.mad:215` | `src/LO_GEN.mad:1386` | 1 |
| `ADDR_60307` | `60307B` | `src/LO_GEN.mad:216` | `src/LO_GEN.mad:1776`, `src/LO_GEN.mad:1788` | 2 |
| `ADDR_61` | `61B` | `src/LO_GEN.mad:217` | `src/LO_GEN.mad:2247` | 1 |
| `ADDR_62` | `62B` | `src/LO_GEN.mad:218` | `src/LO_GEN.mad:2416`, `src/LO_GEN.mad:2652`, `src/LO_GEN.mad:2954` | 3 |
| `ADDR_63` | `63B` | `src/LO_GEN.mad:219` | `src/LO_GEN.mad:2440` | 1 |
| `ADDR_64` | `64B` | `src/LO_GEN.mad:220` | `src/LO_GEN.mad:2470` | 1 |
| `ADDR_65` | `65B` | `src/LO_GEN.mad:221` | `src/LO_GEN.mad:2683` | 1 |
| `ADDR_656` | `656B` | `src/LO_GEN.mad:222` | `src/LO_GEN.mad:623` | 1 |
| `ADDR_66` | `66B` | `src/LO_GEN.mad:223` | `src/LO_GEN.mad:2755` | 1 |
| `ADDR_67` | `67B` | `src/LO_GEN.mad:224` | `src/LO_GEN.mad:2910`, `src/LO_GEN.mad:3509` | 2 |
| `ADDR_7` | `7B` | `src/LO_GEN.mad:225` | `src/LO_GEN.mad:643`, `src/LO_GEN.mad:676`, `src/LO_GEN.mad:679`, `src/LO_GEN.mad:802`, `src/LO_GEN.mad:879`, `src/LO_GEN.mad:907` … (+7) | 13 |
| `ADDR_70` | `70B` | `src/LO_GEN.mad:226` | `src/LO_GEN.mad:2914` | 1 |
| `ADDR_70022` | `70022B` | `src/LO_GEN.mad:227` | `src/LO_GEN.mad:554` | 1 |
| `ADDR_702` | `702B` | `src/LO_GEN.mad:228` | — | 0 |
| `ADDR_70274` | `70274B` | `src/LO_GEN.mad:229` | `src/LO_GEN.mad:563` | 1 |
| `ADDR_71` | `71B` | `src/LO_GEN.mad:230` | `src/LO_GEN.mad:2972` | 1 |
| `ADDR_72` | `72B` | `src/LO_GEN.mad:231` | `src/LO_GEN.mad:2993` | 1 |
| `ADDR_73` | `73B` | `src/LO_GEN.mad:232` | `src/LO_GEN.mad:3086` | 1 |
| `ADDR_74` | `74B` | `src/LO_GEN.mad:233` | `src/LO_GEN.mad:3119` | 1 |
| `ADDR_746` | `746B` | `src/LO_GEN.mad:234` | `src/LO_GEN.mad:1419` | 1 |
| `ADDR_747` | `747B` | `src/LO_GEN.mad:235` | `src/LO_GEN.mad:1413`, `src/LO_GEN.mad:1416` | 2 |
| `ADDR_75` | `75B` | `src/LO_GEN.mad:236` | `src/LO_GEN.mad:3149` | 1 |
| `ADDR_75107` | `75107B` | `src/LO_GEN.mad:237` | `src/LO_GEN.mad:654` | 1 |
| `ADDR_75111` | `75111B` | `src/LO_GEN.mad:238` | `src/LO_GEN.mad:648` | 1 |
| `ADDR_76` | `76B` | `src/LO_GEN.mad:239` | `src/LO_GEN.mad:3272` | 1 |
| `ADDR_7600` | `7600B` | `src/LO_GEN.mad:240` | — | 0 |
| `ADDR_77` | `77B` | `src/LO_GEN.mad:241` | `src/LO_GEN.mad:3341` | 1 |
| `ADDR_777` | `777B` | `src/LO_GEN.mad:242` | `src/LO_GEN.mad:1410` | 1 |
| `NAME_LEN5_DESCRIPTOR` | `0000000000020005` | `src/LO_GEN.mad:243` | `src/LO_GEN.mad:1584`, `src/LO_GEN.mad:1588`, `src/LO_GEN.mad:1592`, `src/LO_GEN.mad:1596`, `src/LO_GEN.mad:1600`, `src/LO_GEN.mad:1604` … (+23) | 29 |
| `MODVAL_11347` | `11347` | `src/LO_GEN.mad:244` | `src/LO_GEN.mad:3378`, `src/LO_GEN.mad:3396` | 2 |
| `MODVAL_12500` | `12500` | `src/LO_GEN.mad:245` | — | 0 |
| `MODVAL_12501` | `12501` | `src/LO_GEN.mad:246` | `src/LO_GEN.mad:2632` | 1 |
| `MODVAL_12516` | `12516` | `src/LO_GEN.mad:247` | `src/LO_GEN.mad:2728`, `src/LO_GEN.mad:2917` | 2 |
| `MODVAL_16448` | `16448` | `src/LO_GEN.mad:248` | `src/LO_GEN.mad:637`, `src/LO_GEN.mad:672` | 2 |
| `MODVAL_24763` | `24763` | `src/LO_GEN.mad:249` | `src/LO_GEN.mad:754` | 1 |
| `MODVAL_24770` | `24770` | `src/LO_GEN.mad:250` | `src/LO_GEN.mad:1930`, `src/LO_GEN.mad:2044`, `src/LO_GEN.mad:2119`, `src/LO_GEN.mad:2248`, `src/LO_GEN.mad:2422`, `src/LO_GEN.mad:2578` … (+11) | 17 |
| `MODVAL_24774` | `24774` | `src/LO_GEN.mad:251` | `src/LO_GEN.mad:1228` | 1 |
| `MODVAL_24775` | `24775` | `src/LO_GEN.mad:252` | `src/LO_GEN.mad:1717` | 1 |
| `MODVAL_25659` | `25659` | `src/LO_GEN.mad:253` | `src/LO_GEN.mad:700` | 1 |
| `REGSEL_10` | `10` | `src/LO_GEN.mad:254` | `src/LO_GEN.mad:865`, `src/LO_GEN.mad:3060`, `src/LO_GEN.mad:3069`, `src/LO_GEN.mad:3099`, `src/LO_GEN.mad:3129` | 5 |
| `REGSEL_11` | `11` | `src/LO_GEN.mad:255` | `src/LO_GEN.mad:787`, `src/LO_GEN.mad:1705`, `src/LO_GEN.mad:1714`, `src/LO_GEN.mad:1726` | 4 |
| `REGSEL_12` | `12` | `src/LO_GEN.mad:256` | `src/LO_GEN.mad:1990`, `src/LO_GEN.mad:2098`, `src/LO_GEN.mad:2134`, `src/LO_GEN.mad:2467`, `src/LO_GEN.mad:2737`, `src/LO_GEN.mad:2749` … (+3) | 9 |
| `REGSEL_13` | `13` | `src/LO_GEN.mad:257` | `src/LO_GEN.mad:566` | 1 |
| `REGSEL_14` | `14` | `src/LO_GEN.mad:258` | `src/LO_GEN.mad:736`, `src/LO_GEN.mad:931`, `src/LO_GEN.mad:3459`, `src/LO_GEN.mad:3468`, `src/LO_GEN.mad:3492`, `src/LO_GEN.mad:3528` | 6 |
| `REGSEL_15` | `15` | `src/LO_GEN.mad:259` | `src/LO_GEN.mad:569` | 1 |
| `REGSEL_2` | `2` | `src/LO_GEN.mad:260` | `src/LO_GEN.mad:1060` | 1 |
| `REGSEL_3` | `3` | `src/LO_GEN.mad:261` | `src/LO_GEN.mad:3420` | 1 |
| `REGSEL_4` | `4` | `src/LO_GEN.mad:262` | — | 0 |
| `REGSEL_5` | `5` | `src/LO_GEN.mad:263` | `src/LO_GEN.mad:742` | 1 |
| `REGSEL_7` | `7` | `src/LO_GEN.mad:264` | `src/LO_GEN.mad:685`, `src/LO_GEN.mad:3501` | 2 |
| `REGSEL_8` | `8` | `src/LO_GEN.mad:265` | — | 0 |
| `REGSEL_9` | `9` | `src/LO_GEN.mad:266` | `src/LO_GEN.mad:790` | 1 |
| `NEG_12` | `-12` | `src/LO_GEN.mad:267` | `src/LO_GEN.mad:3405` | 1 |
| `NEG_2` | `-2` | `src/LO_GEN.mad:268` | `src/LO_GEN.mad:3447`, `src/LO_GEN.mad:3452` | 2 |
| `NEG_3` | `-3` | `src/LO_GEN.mad:269` | `src/LO_GEN.mad:1042`, `src/LO_GEN.mad:1044`, `src/LO_GEN.mad:1048`, `src/LO_GEN.mad:3455` | 4 |
| `NEG_4` | `-4` | `src/LO_GEN.mad:270` | `src/LO_GEN.mad:699`, `src/LO_GEN.mad:724`, `src/LO_GEN.mad:729`, `src/LO_GEN.mad:849`, `src/LO_GEN.mad:924`, `src/LO_GEN.mad:972` … (+13) | 19 |
| `NEG_5` | `-5` | `src/LO_GEN.mad:271` | `src/LO_GEN.mad:714`, `src/LO_GEN.mad:717`, `src/LO_GEN.mad:741`, `src/LO_GEN.mad:3432`, `src/LO_GEN.mad:3494`, `src/LO_GEN.mad:3519` | 6 |
| `NEG_6` | `-6` | `src/LO_GEN.mad:272` | `src/LO_GEN.mad:2458`, `src/LO_GEN.mad:2530`, `src/LO_GEN.mad:2538`, `src/LO_GEN.mad:2566`, `src/LO_GEN.mad:2575`, `src/LO_GEN.mad:2967` … (+1) | 7 |
| `NEG_7` | `-7` | `src/LO_GEN.mad:273` | `src/LO_GEN.mad:718`, `src/LO_GEN.mad:720`, `src/LO_GEN.mad:735`, `src/LO_GEN.mad:1843`, `src/LO_GEN.mad:1851`, `src/LO_GEN.mad:1854` … (+11) | 17 |
| `ONE` | `1` | `src/LO_GEN.mad:274` | — | 0 |
| `HEADER_MODULE_MARKER` | `0000000000200003` | `src/LO_GEN.mad:275` | `src/LO_GEN.mad:541` | 1 |
| `HEADER_MODULE_NAME_WORD` | `5457124745560000` | `src/LO_GEN.mad:276` | `src/LO_GEN.mad:543` | 1 |
| `JUMP_TARGET_1672` | `1672B` | `src/LO_GEN.mad:277` | `src/LO_GEN.mad:2083`, `src/LO_GEN.mad:2770` | 2 |
| `JUMP_TARGET_20116` | `20116B` | `src/LO_GEN.mad:278` | `src/LO_GEN.mad:581` | 1 |
| `JUMP_TARGET_20521` | `20521B` | `src/LO_GEN.mad:279` | `src/LO_GEN.mad:3390` | 1 |
| `JUMP_TARGET_26434` | `26434B` | `src/LO_GEN.mad:280` | `src/LO_GEN.mad:599` | 1 |
| `JUMP_TARGET_30310` | `30310B` | `src/LO_GEN.mad:281` | `src/LO_GEN.mad:596` | 1 |
| `JUMP_TARGET_41072` | `41072B` | `src/LO_GEN.mad:282` | `src/LO_GEN.mad:2464` | 1 |
| `JUMP_TARGET_41104` | `41104B` | `src/LO_GEN.mad:283` | `src/LO_GEN.mad:2478` | 1 |
| `JUMP_TARGET_41260` | `41260B` | `src/LO_GEN.mad:284` | `src/LO_GEN.mad:2739` | 1 |
| `JUMP_TARGET_41271` | `41271B` | `src/LO_GEN.mad:285` | `src/LO_GEN.mad:2734` | 1 |
| `JUMP_TARGET_41563` | `41563B` | `src/LO_GEN.mad:286` | `src/LO_GEN.mad:2680` | 1 |
| `JUMP_TARGET_41574` | `41574B` | `src/LO_GEN.mad:287` | `src/LO_GEN.mad:1204`, `src/LO_GEN.mad:1237`, `src/LO_GEN.mad:2572`, `src/LO_GEN.mad:2698` | 4 |
| `JUMP_TARGET_41605` | `41605B` | `src/LO_GEN.mad:288` | `src/LO_GEN.mad:2800`, `src/LO_GEN.mad:2857` | 2 |
| `JUMP_TARGET_41620` | `41620B` | `src/LO_GEN.mad:289` | `src/LO_GEN.mad:2506`, `src/LO_GEN.mad:2662` | 2 |
| `JUMP_TARGET_41631` | `41631B` | `src/LO_GEN.mad:290` | `src/LO_GEN.mad:1810`, `src/LO_GEN.mad:1816` | 2 |
| `JUMP_TARGET_41660` | `41660B` | `src/LO_GEN.mad:291` | `src/LO_GEN.mad:3294` | 1 |
| `JUMP_TARGET_41706` | `41706B` | `src/LO_GEN.mad:292` | `src/LO_GEN.mad:3288` | 1 |
| `JUMP_TARGET_42040` | `42040B` | `src/LO_GEN.mad:293` | `src/LO_GEN.mad:1168`, `src/LO_GEN.mad:1219` | 2 |
| `JUMP_TARGET_42054` | `42054B` | `src/LO_GEN.mad:294` | `src/LO_GEN.mad:3321` | 1 |
| `JUMP_TARGET_42115` | `42115B` | `src/LO_GEN.mad:295` | `src/LO_GEN.mad:1762`, `src/LO_GEN.mad:1774`, `src/LO_GEN.mad:1795`, `src/LO_GEN.mad:2269`, `src/LO_GEN.mad:2317` | 5 |
| `JUMP_TARGET_42130` | `42130B` | `src/LO_GEN.mad:296` | `src/LO_GEN.mad:649` | 1 |
| `JUMP_TARGET_42133` | `42133B` | `src/LO_GEN.mad:297` | `src/LO_GEN.mad:1921` | 1 |
| `JUMP_TARGET_42154` | `42154B` | `src/LO_GEN.mad:298` | `src/LO_GEN.mad:2371` | 1 |
| `JUMP_TARGET_42170` | `42170B` | `src/LO_GEN.mad:299` | `src/LO_GEN.mad:1915` | 1 |
| `JUMP_TARGET_42244` | `42244B` | `src/LO_GEN.mad:300` | `src/LO_GEN.mad:763`, `src/LO_GEN.mad:778`, `src/LO_GEN.mad:946`, `src/LO_GEN.mad:991`, `src/LO_GEN.mad:1270` | 5 |
| `JUMP_TARGET_42256` | `42256B` | `src/LO_GEN.mad:301` | `src/LO_GEN.mad:1114`, `src/LO_GEN.mad:1927`, `src/LO_GEN.mad:2260`, `src/LO_GEN.mad:2308`, `src/LO_GEN.mad:2746`, `src/LO_GEN.mad:3045` … (+1) | 7 |
| `JUMP_TARGET_42274` | `42274B` | `src/LO_GEN.mad:302` | `src/LO_GEN.mad:1765`, `src/LO_GEN.mad:1777`, `src/LO_GEN.mad:1789`, `src/LO_GEN.mad:1798`, `src/LO_GEN.mad:2038`, `src/LO_GEN.mad:2074` … (+2) | 8 |
| `JUMP_TARGET_42320` | `42320B` | `src/LO_GEN.mad:303` | `src/LO_GEN.mad:1735`, `src/LO_GEN.mad:2233`, `src/LO_GEN.mad:2305` | 3 |
| `JUMP_TARGET_42332` | `42332B` | `src/LO_GEN.mad:304` | `src/LO_GEN.mad:2692` | 1 |
| `JUMP_TARGET_42360` | `42360B` | `src/LO_GEN.mad:305` | `src/LO_GEN.mad:832`, `src/LO_GEN.mad:838`, `src/LO_GEN.mad:1165` | 3 |
| `JUMP_TARGET_42601` | `42601B` | `src/LO_GEN.mad:306` | `src/LO_GEN.mad:766`, `src/LO_GEN.mad:781`, `src/LO_GEN.mad:841`, `src/LO_GEN.mad:1243`, `src/LO_GEN.mad:1255`, `src/LO_GEN.mad:1873` | 6 |
| `JUMP_TARGET_42626` | `42626B` | `src/LO_GEN.mad:307` | `src/LO_GEN.mad:949`, `src/LO_GEN.mad:994`, `src/LO_GEN.mad:1138`, `src/LO_GEN.mad:1903`, `src/LO_GEN.mad:3006` | 5 |
| `JUMP_TARGET_42637` | `42637B` | `src/LO_GEN.mad:308` | `src/LO_GEN.mad:1174`, `src/LO_GEN.mad:1225`, `src/LO_GEN.mad:1273`, `src/LO_GEN.mad:1963`, `src/LO_GEN.mad:2332`, `src/LO_GEN.mad:2419` … (+2) | 8 |
| `JUMP_TARGET_42663` | `42663B` | `src/LO_GEN.mad:309` | `src/LO_GEN.mad:1072` | 1 |
| `JUMP_TARGET_42756` | `42756B` | `src/LO_GEN.mad:310` | `src/LO_GEN.mad:2539` | 1 |
| `JUMP_TARGET_43301` | `43301B` | `src/LO_GEN.mad:311` | `src/LO_GEN.mad:940` | 1 |
| `JUMP_TARGET_43402` | `43402B` | `src/LO_GEN.mad:312` | `src/LO_GEN.mad:1213` | 1 |
| `JUMP_TARGET_43460` | `43460B` | `src/LO_GEN.mad:313` | `src/LO_GEN.mad:2446` | 1 |
| `JUMP_TARGET_44214` | `44214B` | `src/LO_GEN.mad:314` | `src/LO_GEN.mad:811`, `src/LO_GEN.mad:1279` | 2 |
| `JUMP_TARGET_44405` | `44405B` | `src/LO_GEN.mad:315` | `src/LO_GEN.mad:2710` | 1 |
| `JUMP_TARGET_44671` | `44671B` | `src/LO_GEN.mad:316` | `src/LO_GEN.mad:982`, `src/LO_GEN.mad:2026`, `src/LO_GEN.mad:2338` | 3 |
| `JUMP_TARGET_45421` | `45421B` | `src/LO_GEN.mad:317` | `src/LO_GEN.mad:1021`, `src/LO_GEN.mad:1858`, `src/LO_GEN.mad:3315`, `src/LO_GEN.mad:3336`, `src/LO_GEN.mad:3549` | 5 |
| `JUMP_TARGET_47253` | `47253B` | `src/LO_GEN.mad:318` | `src/LO_GEN.mad:664` | 1 |
| `JUMP_TARGET_50114` | `50114B` | `src/LO_GEN.mad:319` | `src/LO_GEN.mad:666` | 1 |
| `JUMP_TARGET_53320` | `53320B` | `src/LO_GEN.mad:320` | `src/LO_GEN.mad:2218`, `src/LO_GEN.mad:2287` | 2 |
| `JUMP_TARGET_53333` | `53333B` | `src/LO_GEN.mad:321` | `src/LO_GEN.mad:2452` | 1 |
| `JUMP_TARGET_54067` | `54067B` | `src/LO_GEN.mad:322` | `src/LO_GEN.mad:2656` | 1 |
| `JUMP_TARGET_54303` | `54303B` | `src/LO_GEN.mad:323` | `src/LO_GEN.mad:3063` | 1 |
| `JUMP_TARGET_57244` | `57244B` | `src/LO_GEN.mad:324` | `src/LO_GEN.mad:1156` | 1 |
| `JUMP_TARGET_57325` | `57325B` | `src/LO_GEN.mad:325` | `src/LO_GEN.mad:769`, `src/LO_GEN.mad:784`, `src/LO_GEN.mad:844`, `src/LO_GEN.mad:997`, `src/LO_GEN.mad:1090`, `src/LO_GEN.mad:1177` … (+6) | 12 |
| `JUMP_TARGET_57476` | `57476B` | `src/LO_GEN.mad:326` | `src/LO_GEN.mad:772`, `src/LO_GEN.mad:799`, `src/LO_GEN.mad:814`, `src/LO_GEN.mad:847`, `src/LO_GEN.mad:970`, `src/LO_GEN.mad:985` … (+39) | 45 |
| `JUMP_TARGET_57616` | `57616B` | `src/LO_GEN.mad:327` | `src/LO_GEN.mad:2824` | 1 |
| `JUMP_TARGET_60001` | `60001B` | `src/LO_GEN.mad:328` | `src/LO_GEN.mad:748` | 1 |
| `JUMP_TARGET_60130` | `60130B` | `src/LO_GEN.mad:329` | `src/LO_GEN.mad:2023`, `src/LO_GEN.mad:3276`, `src/LO_GEN.mad:3456` | 3 |
| `JUMP_TARGET_60562` | `60562B` | `src/LO_GEN.mad:330` | `src/LO_GEN.mad:3021` | 1 |
| `JUMP_TARGET_61277` | `61277B` | `src/LO_GEN.mad:331` | `src/LO_GEN.mad:3003` | 1 |
| `JUMP_TARGET_61372` | `61372B` | `src/LO_GEN.mad:332` | `src/LO_GEN.mad:1054`, `src/LO_GEN.mad:2931`, `src/LO_GEN.mad:2937`, `src/LO_GEN.mad:2943`, `src/LO_GEN.mad:2949`, `src/LO_GEN.mad:2955` … (+4) | 10 |
| `JUMP_TARGET_62122` | `62122B` | `src/LO_GEN.mad:333` | `src/LO_GEN.mad:2383`, `src/LO_GEN.mad:3423` | 2 |
| `JUMP_TARGET_62435` | `62435B` | `src/LO_GEN.mad:334` | `src/LO_GEN.mad:2482`, `src/LO_GEN.mad:2704` | 2 |
| `JUMP_TARGET_62570` | `62570B` | `src/LO_GEN.mad:335` | `src/LO_GEN.mad:1867` | 1 |
| `JUMP_TARGET_62634` | `62634B` | `src/LO_GEN.mad:336` | `src/LO_GEN.mad:2347`, `src/LO_GEN.mad:2368` | 2 |
| `JUMP_TARGET_63100` | `63100B` | `src/LO_GEN.mad:337` | `src/LO_GEN.mad:2362` | 1 |
| `JUMP_TARGET_63235` | `63235B` | `src/LO_GEN.mad:338` | `src/LO_GEN.mad:2398` | 1 |
| `JUMP_TARGET_63275` | `63275B` | `src/LO_GEN.mad:339` | `src/LO_GEN.mad:2389`, `src/LO_GEN.mad:2404` | 2 |
| `JUMP_TARGET_63347` | `63347B` | `src/LO_GEN.mad:340` | `src/LO_GEN.mad:829`, `src/LO_GEN.mad:979`, `src/LO_GEN.mad:1126`, `src/LO_GEN.mad:1744`, `src/LO_GEN.mad:1981`, `src/LO_GEN.mad:2476` … (+3) | 9 |
| `JUMP_TARGET_63553` | `63553B` | `src/LO_GEN.mad:341` | `src/LO_GEN.mad:2719` | 1 |
| `JUMP_TARGET_63605` | `63605B` | `src/LO_GEN.mad:342` | `src/LO_GEN.mad:1078`, `src/LO_GEN.mad:2743` | 2 |
| `JUMP_TARGET_63636` | `63636B` | `src/LO_GEN.mad:343` | `src/LO_GEN.mad:2716` | 1 |
| `JUMP_TARGET_64305` | `64305B` | `src/LO_GEN.mad:344` | `src/LO_GEN.mad:1897` | 1 |
| `JUMP_TARGET_65152` | `65152B` | `src/LO_GEN.mad:345` | `src/LO_GEN.mad:1885` | 1 |
| `JUMP_TARGET_66172` | `66172B` | `src/LO_GEN.mad:346` | `src/LO_GEN.mad:820` | 1 |
| `JUMP_TARGET_75264` | `75264B` | `src/LO_GEN.mad:347` | `src/LO_GEN.mad:628`, `src/LO_GEN.mad:3101`, `src/LO_GEN.mad:3131` | 3 |
| `JUMP_TARGET_75300` | `75300B` | `src/LO_GEN.mad:348` | `src/LO_GEN.mad:657`, `src/LO_GEN.mad:810`, `src/LO_GEN.mad:1278` | 3 |
| `JUMP_TARGET_75326` | `75326B` | `src/LO_GEN.mad:349` | `src/LO_GEN.mad:727`, `src/LO_GEN.mad:732` | 2 |
| `JUMP_TARGET_75330` | `75330B` | `src/LO_GEN.mad:350` | `src/LO_GEN.mad:1289` | 1 |
| `JUMP_TARGET_75335` | `75335B` | `src/LO_GEN.mad:351` | `src/LO_GEN.mad:753` | 1 |
| `JUMP_TARGET_75342` | `75342B` | `src/LO_GEN.mad:352` | `src/LO_GEN.mad:1292` | 1 |
| `JUMP_TARGET_75351` | `75351B` | `src/LO_GEN.mad:353` | `src/LO_GEN.mad:793` | 1 |
| `JUMP_TARGET_75360` | `75360B` | `src/LO_GEN.mad:354` | `src/LO_GEN.mad:1295` | 1 |
| `JUMP_TARGET_75413` | `75413B` | `src/LO_GEN.mad:355` | `src/LO_GEN.mad:894` | 1 |
| `JUMP_TARGET_75415` | `75415B` | `src/LO_GEN.mad:356` | `src/LO_GEN.mad:898` | 1 |
| `JUMP_TARGET_75420` | `75420B` | `src/LO_GEN.mad:357` | `src/LO_GEN.mad:871` | 1 |
| `JUMP_TARGET_75423` | `75423B` | `src/LO_GEN.mad:358` | `src/LO_GEN.mad:1298` | 1 |
| `JUMP_TARGET_75432` | `75432B` | `src/LO_GEN.mad:359` | `src/LO_GEN.mad:927`, `src/LO_GEN.mad:937` | 2 |
| `JUMP_TARGET_75445` | `75445B` | `src/LO_GEN.mad:360` | `src/LO_GEN.mad:858`, `src/LO_GEN.mad:876`, `src/LO_GEN.mad:912`, `src/LO_GEN.mad:1209` | 4 |
| `JUMP_TARGET_75451` | `75451B` | `src/LO_GEN.mad:361` | `src/LO_GEN.mad:1301` | 1 |
| `JUMP_TARGET_75456` | `75456B` | `src/LO_GEN.mad:362` | `src/LO_GEN.mad:1313` | 1 |
| `JUMP_TARGET_75462` | `75462B` | `src/LO_GEN.mad:363` | `src/LO_GEN.mad:1006` | 1 |
| `JUMP_TARGET_75471` | `75471B` | `src/LO_GEN.mad:364` | `src/LO_GEN.mad:1011` | 1 |
| `JUMP_TARGET_75476` | `75476B` | `src/LO_GEN.mad:365` | `src/LO_GEN.mad:1047` | 1 |
| `JUMP_TARGET_75500` | `75500B` | `src/LO_GEN.mad:366` | `src/LO_GEN.mad:1051` | 1 |
| `JUMP_TARGET_75506` | `75506B` | `src/LO_GEN.mad:367` | `src/LO_GEN.mad:1069` | 1 |
| `JUMP_TARGET_75507` | `75507B` | `src/LO_GEN.mad:368` | `src/LO_GEN.mad:1074` | 1 |
| `JUMP_TARGET_75516` | `75516B` | `src/LO_GEN.mad:369` | `src/LO_GEN.mad:1056` | 1 |
| `JUMP_TARGET_75525` | `75525B` | `src/LO_GEN.mad:370` | `src/LO_GEN.mad:1104`, `src/LO_GEN.mad:1113` | 2 |
| `JUMP_TARGET_75526` | `75526B` | `src/LO_GEN.mad:371` | `src/LO_GEN.mad:1304` | 1 |
| `JUMP_TARGET_75534` | `75534B` | `src/LO_GEN.mad:372` | `src/LO_GEN.mad:1131`, `src/LO_GEN.mad:1135` | 2 |
| `JUMP_TARGET_75541` | `75541B` | `src/LO_GEN.mad:373` | `src/LO_GEN.mad:1149`, `src/LO_GEN.mad:1153` | 2 |
| `JUMP_TARGET_75546` | `75546B` | `src/LO_GEN.mad:374` | `src/LO_GEN.mad:1161` | 1 |
| `JUMP_TARGET_75547` | `75547B` | `src/LO_GEN.mad:375` | `src/LO_GEN.mad:1170` | 1 |
| `JUMP_TARGET_75551` | `75551B` | `src/LO_GEN.mad:376` | `src/LO_GEN.mad:1140` | 1 |
| `JUMP_TARGET_75555` | `75555B` | `src/LO_GEN.mad:377` | `src/LO_GEN.mad:1189` | 1 |
| `JUMP_TARGET_75557` | `75557B` | `src/LO_GEN.mad:378` | `src/LO_GEN.mad:2686` | 1 |
| `JUMP_TARGET_75563` | `75563B` | `src/LO_GEN.mad:379` | `src/LO_GEN.mad:1316`, `src/LO_GEN.mad:1520`, `src/LO_GEN.mad:1529` | 3 |
| `JUMP_TARGET_75565` | `75565B` | `src/LO_GEN.mad:380` | `src/LO_GEN.mad:1319` | 1 |
| `JUMP_TARGET_75567` | `75567B` | `src/LO_GEN.mad:381` | `src/LO_GEN.mad:1349` | 1 |
| `JUMP_TARGET_75570` | `75570B` | `src/LO_GEN.mad:382` | `src/LO_GEN.mad:1812` | 1 |
| `JUMP_TARGET_75573` | `75573B` | `src/LO_GEN.mad:383` | `src/LO_GEN.mad:1267` | 1 |
| `JUMP_TARGET_75575` | `75575B` | `src/LO_GEN.mad:384` | `src/LO_GEN.mad:1355` | 1 |
| `JUMP_TARGET_75601` | `75601B` | `src/LO_GEN.mad:385` | `src/LO_GEN.mad:1352` | 1 |
| `JUMP_TARGET_75605` | `75605B` | `src/LO_GEN.mad:386` | `src/LO_GEN.mad:1260` | 1 |
| `JUMP_TARGET_75606` | `75606B` | `src/LO_GEN.mad:387` | `src/LO_GEN.mad:1328` | 1 |
| `JUMP_TARGET_76056` | `76056B` | `src/LO_GEN.mad:388` | `src/LO_GEN.mad:1394` | 1 |
| `JUMP_TARGET_76075` | `76075B` | `src/LO_GEN.mad:389` | `src/LO_GEN.mad:1740` | 1 |
| `JUMP_TARGET_76102` | `76102B` | `src/LO_GEN.mad:390` | `src/LO_GEN.mad:1759` | 1 |
| `JUMP_TARGET_76110` | `76110B` | `src/LO_GEN.mad:391` | `src/LO_GEN.mad:1806` | 1 |
| `JUMP_TARGET_76112` | `76112B` | `src/LO_GEN.mad:392` | `src/LO_GEN.mad:1753` | 1 |
| `JUMP_TARGET_76121` | `76121B` | `src/LO_GEN.mad:393` | `src/LO_GEN.mad:1331` | 1 |
| `JUMP_TARGET_76123` | `76123B` | `src/LO_GEN.mad:394` | `src/LO_GEN.mad:1334` | 1 |
| `JUMP_TARGET_76125` | `76125B` | `src/LO_GEN.mad:395` | `src/LO_GEN.mad:1338`, `src/LO_GEN.mad:1341`, `src/LO_GEN.mad:1344`, `src/LO_GEN.mad:1347` | 4 |
| `JUMP_TARGET_76136` | `76136B` | `src/LO_GEN.mad:396` | `src/LO_GEN.mad:1834` | 1 |
| `JUMP_TARGET_76140` | `76140B` | `src/LO_GEN.mad:397` | `src/LO_GEN.mad:1845` | 1 |
| `JUMP_TARGET_76144` | `76144B` | `src/LO_GEN.mad:398` | `src/LO_GEN.mad:1839` | 1 |
| `JUMP_TARGET_76146` | `76146B` | `src/LO_GEN.mad:399` | `src/LO_GEN.mad:1358` | 1 |
| `JUMP_TARGET_76152` | `76152B` | `src/LO_GEN.mad:400` | `src/LO_GEN.mad:1364` | 1 |
| `JUMP_TARGET_76154` | `76154B` | `src/LO_GEN.mad:401` | `src/LO_GEN.mad:1367` | 1 |
| `JUMP_TARGET_76160` | `76160B` | `src/LO_GEN.mad:402` | `src/LO_GEN.mad:1370` | 1 |
| `JUMP_TARGET_76164` | `76164B` | `src/LO_GEN.mad:403` | `src/LO_GEN.mad:1379` | 1 |
| `JUMP_TARGET_76166` | `76166B` | `src/LO_GEN.mad:404` | `src/LO_GEN.mad:1385` | 1 |
| `JUMP_TARGET_76204` | `76204B` | `src/LO_GEN.mad:405` | `src/LO_GEN.mad:1388` | 1 |
| `JUMP_TARGET_76231` | `76231B` | `src/LO_GEN.mad:406` | `src/LO_GEN.mad:1987` | 1 |
| `JUMP_TARGET_76304` | `76304B` | `src/LO_GEN.mad:407` | `src/LO_GEN.mad:1391` | 1 |
| `JUMP_TARGET_76314` | `76314B` | `src/LO_GEN.mad:408` | `src/LO_GEN.mad:1466` | 1 |
| `JUMP_TARGET_76324` | `76324B` | `src/LO_GEN.mad:409` | `src/LO_GEN.mad:1382` | 1 |
| `JUMP_TARGET_76333` | `76333B` | `src/LO_GEN.mad:410` | `src/LO_GEN.mad:1403`, `src/LO_GEN.mad:1418` | 2 |
| `JUMP_TARGET_76334` | `76334B` | `src/LO_GEN.mad:411` | `src/LO_GEN.mad:1412`, `src/LO_GEN.mad:1415` | 2 |
| `JUMP_TARGET_76335` | `76335B` | `src/LO_GEN.mad:412` | `src/LO_GEN.mad:2224` | 1 |
| `JUMP_TARGET_76347` | `76347B` | `src/LO_GEN.mad:413` | `src/LO_GEN.mad:2238`, `src/LO_GEN.mad:2242` | 2 |
| `JUMP_TARGET_76353` | `76353B` | `src/LO_GEN.mad:414` | `src/LO_GEN.mad:2266`, `src/LO_GEN.mad:2314`, `src/LO_GEN.mad:2319`, `src/LO_GEN.mad:2343` | 4 |
| `JUMP_TARGET_76361` | `76361B` | `src/LO_GEN.mad:415` | `src/LO_GEN.mad:2286` | 1 |
| `JUMP_TARGET_76363` | `76363B` | `src/LO_GEN.mad:416` | `src/LO_GEN.mad:1400` | 1 |
| `JUMP_TARGET_76364` | `76364B` | `src/LO_GEN.mad:417` | `src/LO_GEN.mad:1409` | 1 |
| `JUMP_TARGET_76365` | `76365B` | `src/LO_GEN.mad:418` | `src/LO_GEN.mad:2296` | 1 |
| `JUMP_TARGET_76374` | `76374B` | `src/LO_GEN.mad:419` | `src/LO_GEN.mad:1397` | 1 |
| `JUMP_TARGET_76375` | `76375B` | `src/LO_GEN.mad:420` | `src/LO_GEN.mad:1406` | 1 |
| `JUMP_TARGET_76376` | `76376B` | `src/LO_GEN.mad:421` | `src/LO_GEN.mad:2323` | 1 |
| `JUMP_TARGET_76402` | `76402B` | `src/LO_GEN.mad:422` | `src/LO_GEN.mad:2337` | 1 |
| `JUMP_TARGET_76404` | `76404B` | `src/LO_GEN.mad:423` | `src/LO_GEN.mad:1373` | 1 |
| `JUMP_TARGET_76406` | `76406B` | `src/LO_GEN.mad:424` | `src/LO_GEN.mad:1376` | 1 |
| `JUMP_TARGET_76411` | `76411B` | `src/LO_GEN.mad:425` | `src/LO_GEN.mad:2353` | 1 |
| `JUMP_TARGET_76413` | `76413B` | `src/LO_GEN.mad:426` | `src/LO_GEN.mad:2358` | 1 |
| `JUMP_TARGET_76416` | `76416B` | `src/LO_GEN.mad:427` | `src/LO_GEN.mad:1421` | 1 |
| `JUMP_TARGET_76417` | `76417B` | `src/LO_GEN.mad:428` | `src/LO_GEN.mad:2391` | 1 |
| `JUMP_TARGET_76422` | `76422B` | `src/LO_GEN.mad:429` | `src/LO_GEN.mad:1430` | 1 |
| `JUMP_TARGET_76424` | `76424B` | `src/LO_GEN.mad:430` | `src/LO_GEN.mad:1574` | 1 |
| `JUMP_TARGET_76425` | `76425B` | `src/LO_GEN.mad:431` | `src/LO_GEN.mad:2406` | 1 |
| `JUMP_TARGET_76427` | `76427B` | `src/LO_GEN.mad:432` | `src/LO_GEN.mad:1577` | 1 |
| `JUMP_TARGET_76431` | `76431B` | `src/LO_GEN.mad:433` | `src/LO_GEN.mad:1424` | 1 |
| `JUMP_TARGET_76445` | `76445B` | `src/LO_GEN.mad:434` | `src/LO_GEN.mad:2418` | 1 |
| `JUMP_TARGET_76447` | `76447B` | `src/LO_GEN.mad:435` | `src/LO_GEN.mad:1427` | 1 |
| `JUMP_TARGET_76451` | `76451B` | `src/LO_GEN.mad:436` | `src/LO_GEN.mad:1433` | 1 |
| `JUMP_TARGET_76452` | `76452B` | `src/LO_GEN.mad:437` | `src/LO_GEN.mad:2973`, `src/LO_GEN.mad:2978` | 2 |
| `JUMP_TARGET_76465` | `76465B` | `src/LO_GEN.mad:438` | `src/LO_GEN.mad:2487` | 1 |
| `JUMP_TARGET_76470` | `76470B` | `src/LO_GEN.mad:439` | `src/LO_GEN.mad:2496` | 1 |
| `JUMP_TARGET_76475` | `76475B` | `src/LO_GEN.mad:440` | `src/LO_GEN.mad:2511` | 1 |
| `JUMP_TARGET_76500` | `76500B` | `src/LO_GEN.mad:441` | `src/LO_GEN.mad:2520` | 1 |
| `JUMP_TARGET_76501` | `76501B` | `src/LO_GEN.mad:442` | `src/LO_GEN.mad:2490`, `src/LO_GEN.mad:2499`, `src/LO_GEN.mad:2503`, `src/LO_GEN.mad:2514`, `src/LO_GEN.mad:2523` | 5 |
| `JUMP_TARGET_76504` | `76504B` | `src/LO_GEN.mad:443` | `src/LO_GEN.mad:2472` | 1 |
| `JUMP_TARGET_76511` | `76511B` | `src/LO_GEN.mad:444` | `src/LO_GEN.mad:2547` | 1 |
| `JUMP_TARGET_76514` | `76514B` | `src/LO_GEN.mad:445` | `src/LO_GEN.mad:2556` | 1 |
| `JUMP_TARGET_76515` | `76515B` | `src/LO_GEN.mad:446` | `src/LO_GEN.mad:2550`, `src/LO_GEN.mad:2559` | 2 |
| `JUMP_TARGET_76534` | `76534B` | `src/LO_GEN.mad:447` | `src/LO_GEN.mad:2577` | 1 |
| `JUMP_TARGET_76554` | `76554B` | `src/LO_GEN.mad:448` | `src/LO_GEN.mad:2653`, `src/LO_GEN.mad:2700` | 2 |
| `JUMP_TARGET_76557` | `76557B` | `src/LO_GEN.mad:449` | `src/LO_GEN.mad:1497` | 1 |
| `JUMP_TARGET_76561` | `76561B` | `src/LO_GEN.mad:450` | `src/LO_GEN.mad:1500` | 1 |
| `JUMP_TARGET_76563` | `76563B` | `src/LO_GEN.mad:451` | `src/LO_GEN.mad:1443`, `src/LO_GEN.mad:1446`, `src/LO_GEN.mad:1449` | 3 |
| `JUMP_TARGET_76566` | `76566B` | `src/LO_GEN.mad:452` | `src/LO_GEN.mad:1437`, `src/LO_GEN.mad:1440`, `src/LO_GEN.mad:1452`, `src/LO_GEN.mad:1455`, `src/LO_GEN.mad:1458`, `src/LO_GEN.mad:1491` … (+1) | 7 |
| `JUMP_TARGET_76567` | `76567B` | `src/LO_GEN.mad:453` | `src/LO_GEN.mad:2670`, `src/LO_GEN.mad:2676` | 2 |
| `JUMP_TARGET_76571` | `76571B` | `src/LO_GEN.mad:454` | `src/LO_GEN.mad:1461`, `src/LO_GEN.mad:2536` | 2 |
| `JUMP_TARGET_76573` | `76573B` | `src/LO_GEN.mad:455` | `src/LO_GEN.mad:1463` | 1 |
| `JUMP_TARGET_76575` | `76575B` | `src/LO_GEN.mad:456` | `src/LO_GEN.mad:1475` | 1 |
| `JUMP_TARGET_76577` | `76577B` | `src/LO_GEN.mad:457` | `src/LO_GEN.mad:1478` | 1 |
| `JUMP_TARGET_76612` | `76612B` | `src/LO_GEN.mad:458` | `src/LO_GEN.mad:2838` | 1 |
| `JUMP_TARGET_76651` | `76651B` | `src/LO_GEN.mad:459` | `src/LO_GEN.mad:2833` | 1 |
| `JUMP_TARGET_76660` | `76660B` | `src/LO_GEN.mad:460` | `src/LO_GEN.mad:1481` | 1 |
| `JUMP_TARGET_76663` | `76663B` | `src/LO_GEN.mad:461` | `src/LO_GEN.mad:2863` | 1 |
| `JUMP_TARGET_76732` | `76732B` | `src/LO_GEN.mad:462` | `src/LO_GEN.mad:1827`, `src/LO_GEN.mad:1831` | 2 |
| `JUMP_TARGET_76747` | `76747B` | `src/LO_GEN.mad:463` | `src/LO_GEN.mad:1523`, `src/LO_GEN.mad:1532` | 2 |
| `JUMP_TARGET_76760` | `76760B` | `src/LO_GEN.mad:464` | `src/LO_GEN.mad:3050` | 1 |
| `JUMP_TARGET_76761` | `76761B` | `src/LO_GEN.mad:465` | `src/LO_GEN.mad:1538` | 1 |
| `JUMP_TARGET_77024` | `77024B` | `src/LO_GEN.mad:466` | `src/LO_GEN.mad:1541` | 1 |
| `JUMP_TARGET_77043` | `77043B` | `src/LO_GEN.mad:467` | `src/LO_GEN.mad:3179` | 1 |
| `JUMP_TARGET_77052` | `77052B` | `src/LO_GEN.mad:468` | `src/LO_GEN.mad:3210` | 1 |
| `JUMP_TARGET_77053` | `77053B` | `src/LO_GEN.mad:469` | `src/LO_GEN.mad:3171`, `src/LO_GEN.mad:3203` | 2 |
| `JUMP_TARGET_77071` | `77071B` | `src/LO_GEN.mad:470` | `src/LO_GEN.mad:3248` | 1 |
| `JUMP_TARGET_77074` | `77074B` | `src/LO_GEN.mad:471` | `src/LO_GEN.mad:1502` | 1 |
| `JUMP_TARGET_77076` | `77076B` | `src/LO_GEN.mad:472` | `src/LO_GEN.mad:1505` | 1 |
| `JUMP_TARGET_77100` | `77100B` | `src/LO_GEN.mad:473` | `src/LO_GEN.mad:1891`, `src/LO_GEN.mad:1896` | 2 |
| `JUMP_TARGET_77101` | `77101B` | `src/LO_GEN.mad:474` | `src/LO_GEN.mad:3284`, `src/LO_GEN.mad:3290` | 2 |
| `JUMP_TARGET_77103` | `77103B` | `src/LO_GEN.mad:475` | `src/LO_GEN.mad:1547` | 1 |
| `JUMP_TARGET_77104` | `77104B` | `src/LO_GEN.mad:476` | `src/LO_GEN.mad:1550` | 1 |
| `JUMP_TARGET_77111` | `77111B` | `src/LO_GEN.mad:477` | `src/LO_GEN.mad:1544` | 1 |
| `JUMP_TARGET_77113` | `77113B` | `src/LO_GEN.mad:478` | `src/LO_GEN.mad:1554` | 1 |
| `JUMP_TARGET_77114` | `77114B` | `src/LO_GEN.mad:479` | `src/LO_GEN.mad:3357`, `src/LO_GEN.mad:3360`, `src/LO_GEN.mad:3363` | 3 |
| `JUMP_TARGET_77115` | `77115B` | `src/LO_GEN.mad:480` | `src/LO_GEN.mad:3353` | 1 |
| `JUMP_TARGET_77120` | `77120B` | `src/LO_GEN.mad:481` | `src/LO_GEN.mad:1557` | 1 |
| `JUMP_TARGET_77121` | `77121B` | `src/LO_GEN.mad:482` | `src/LO_GEN.mad:1560` | 1 |
| `JUMP_TARGET_77122` | `77122B` | `src/LO_GEN.mad:483` | `src/LO_GEN.mad:1563` | 1 |
| `JUMP_TARGET_77123` | `77123B` | `src/LO_GEN.mad:484` | `src/LO_GEN.mad:3342`, `src/LO_GEN.mad:3345` | 2 |
| `JUMP_TARGET_77125` | `77125B` | `src/LO_GEN.mad:485` | `src/LO_GEN.mad:1566` | 1 |
| `JUMP_TARGET_77126` | `77126B` | `src/LO_GEN.mad:486` | `src/LO_GEN.mad:1569` | 1 |
| `JUMP_TARGET_77127` | `77127B` | `src/LO_GEN.mad:487` | `src/LO_GEN.mad:1572` | 1 |
| `JUMP_TARGET_77130` | `77130B` | `src/LO_GEN.mad:488` | `src/LO_GEN.mad:616`, `src/LO_GEN.mad:723`, `src/LO_GEN.mad:1307`, `src/LO_GEN.mad:1310`, `src/LO_GEN.mad:1322`, `src/LO_GEN.mad:1325` … (+4) | 10 |
| `JUMP_TARGET_77144` | `77144B` | `src/LO_GEN.mad:489` | `src/LO_GEN.mad:760`, `src/LO_GEN.mad:774`, `src/LO_GEN.mad:805`, `src/LO_GEN.mad:816`, `src/LO_GEN.mad:825`, `src/LO_GEN.mad:852` … (+63) | 69 |
| `JUMP_TARGET_77224` | `77224B` | `src/LO_GEN.mad:490` | `src/LO_GEN.mad:3536` | 1 |
| `JUMP_TARGET_77227` | `77227B` | `src/LO_GEN.mad:491` | `src/LO_GEN.mad:3540` | 1 |
| `JUMP_TARGET_77242` | `77242B` | `src/LO_GEN.mad:492` | `src/LO_GEN.mad:3551` | 1 |
| `WORDVAL_0003500000030264` | `0003500000030264` | `src/LO_GEN.mad:493` | `src/LO_GEN.mad:547` | 1 |
| `WORDVAL_0004220010075377` | `0004220010075377` | `src/LO_GEN.mad:494` | `src/LO_GEN.mad:545` | 1 |
| `SVCELL_3` | `3B` | `src/LO_SYN.mad:41` | `src/LO_SYN.mad:763` | 1 |
| `EX57_1263` | `1263B` | `src/LO_SYN.mad:42` | `src/LO_SYN.mad:766` | 1 |
| `EX56_70000` | `70000B` | `src/LO_SYN.mad:43` | `src/LO_SYN.mad:767` | 1 |
| `MEM_2200` | `2200B` | `src/LO_SYN.mad:44` | `src/LO_SYN.mad:769`, `src/LO_SYN.mad:778` | 2 |
| `MEM_5377` | `5377B` | `src/LO_SYN.mad:45` | `src/LO_SYN.mad:770`, `src/LO_SYN.mad:779` | 2 |
| `MEM_5000` | `5000B` | `src/LO_SYN.mad:46` | `src/LO_SYN.mad:772` | 1 |
| `MEM_264` | `264B` | `src/LO_SYN.mad:47` | `src/LO_SYN.mad:773` | 1 |
| `SVCELL_1` | `1B` | `src/LO_SYN.mad:48` | `src/LO_SYN.mad:775`, `src/LO_SYN.mad:832` | 2 |
| `MEM_3000` | `3000B` | `src/LO_SYN.mad:49` | `src/LO_SYN.mad:781` | 1 |
| `MEM_2377` | `2377B` | `src/LO_SYN.mad:50` | `src/LO_SYN.mad:782` | 1 |
| `MEM_400` | `400B` | `src/LO_SYN.mad:51` | `src/LO_SYN.mad:784` | 1 |
| `EX63_274` | `274B` | `src/LO_SYN.mad:52` | `src/LO_SYN.mad:785` | 1 |
| `REGVAL_30274` | `30274B` | `src/LO_SYN.mad:53` | `src/LO_SYN.mad:787`, `src/LO_SYN.mad:811` | 2 |
| `REGVAL_17` | `17B` | `src/LO_SYN.mad:54` | `src/LO_SYN.mad:788`, `src/LO_SYN.mad:814` | 2 |
| `SVCELL_17` | `17B` | `src/LO_SYN.mad:55` | `src/LO_SYN.mad:790` | 1 |
| `REGVAL_15` | `15B` | `src/LO_SYN.mad:56` | `src/LO_SYN.mad:791` | 1 |
| `SVCELL_16` | `16B` | `src/LO_SYN.mad:57` | `src/LO_SYN.mad:793` | 1 |
| `MEM_13` | `13B` | `src/LO_SYN.mad:58` | `src/LO_SYN.mad:794` | 1 |
| `MEM_104` | `104B` | `src/LO_SYN.mad:59` | `src/LO_SYN.mad:796` | 1 |
| `MEM_14` | `14B` | `src/LO_SYN.mad:60` | `src/LO_SYN.mad:797` | 1 |
| `SVCELL_14` | `14B` | `src/LO_SYN.mad:61` | `src/LO_SYN.mad:799` | 1 |
| `EX70_14` | `14B` | `src/LO_SYN.mad:62` | `src/LO_SYN.mad:800` | 1 |
| `REGVAL_36017` | `36017B` | `src/LO_SYN.mad:63` | `src/LO_SYN.mad:802` | 1 |
| `REGVAL_16` | `16B` | `src/LO_SYN.mad:64` | `src/LO_SYN.mad:803`, `src/LO_SYN.mad:806` | 2 |
| `REGVAL_30311` | `30311B` | `src/LO_SYN.mad:65` | `src/LO_SYN.mad:805` | 1 |
| `EXT_20116` | `20116B` | `src/LO_SYN.mad:66` | `src/LO_SYN.mad:808` | 1 |
| `MEM_17` | `17B` | `src/LO_SYN.mad:67` | `src/LO_SYN.mad:812` | 1 |
| `ADRPTR_30312` | `30312B` | `src/LO_SYN.mad:68` | `src/LO_SYN.mad:815` | 1 |
| `MEM_2000` | `2000B` | `src/LO_SYN.mad:69` | `src/LO_SYN.mad:824` | 1 |
| `MEM_3` | `3B` | `src/LO_SYN.mad:70` | `src/LO_SYN.mad:827` | 1 |
| `SVCELL_2` | `2B` | `src/LO_SYN.mad:71` | `src/LO_SYN.mad:830` | 1 |
| `REGVAL_2174` | `2174B` | `src/LO_SYN.mad:72` | `src/LO_SYN.mad:833` | 1 |
| `EX36_75551` | `75551B` | `src/LO_SYN.mad:73` | `src/LO_SYN.mad:835`, `src/LO_SYN.mad:862`, `src/LO_SYN.mad:937`, `src/LO_SYN.mad:1066`, `src/LO_SYN.mad:1141`, `src/LO_SYN.mad:1975` … (+18) | 24 |
| `REGVAL_5501` | `5501B` | `src/LO_SYN.mad:74` | `src/LO_SYN.mad:836`, `src/LO_SYN.mad:863`, `src/LO_SYN.mad:938`, `src/LO_SYN.mad:1067`, `src/LO_SYN.mad:1142`, `src/LO_SYN.mad:1547` … (+20) | 26 |
| `MEM_1040` | `1040B` | `src/LO_SYN.mad:75` | `src/LO_SYN.mad:838`, `src/LO_SYN.mad:865`, `src/LO_SYN.mad:940`, `src/LO_SYN.mad:1936`, `src/LO_SYN.mad:1978`, `src/LO_SYN.mad:2017` … (+24) | 30 |
| `MEM_7554` | `7554B` | `src/LO_SYN.mad:76` | `src/LO_SYN.mad:839` | 1 |
| `MEM_70115` | `70115B` | `src/LO_SYN.mad:77` | `src/LO_SYN.mad:841`, `src/LO_SYN.mad:2153`, `src/LO_SYN.mad:2212` | 3 |
| `MEM_72113` | `72113B` | `src/LO_SYN.mad:78` | `src/LO_SYN.mad:842`, `src/LO_SYN.mad:1165`, `src/LO_SYN.mad:2155`, `src/LO_SYN.mad:2431`, `src/LO_SYN.mad:2533` | 5 |
| `ADRPTR_20040` | `20040B` | `src/LO_SYN.mad:79` | `src/LO_SYN.mad:844`, `src/LO_SYN.mad:989`, `src/LO_SYN.mad:1064`, `src/LO_SYN.mad:1088`, `src/LO_SYN.mad:1138`, `src/LO_SYN.mad:1166` … (+5) | 11 |
| `MODVAL_40` | `40B` | `src/LO_SYN.mad:80` | `src/LO_SYN.mad:845`, `src/LO_SYN.mad:860`, `src/LO_SYN.mad:887`, `src/LO_SYN.mad:899`, `src/LO_SYN.mad:944`, `src/LO_SYN.mad:959` … (+79) | 85 |
| `EXT_42524` | `42524B` | `src/LO_SYN.mad:81` | `src/LO_SYN.mad:847`, `src/LO_SYN.mad:1010`, `src/LO_SYN.mad:1021`, `src/LO_SYN.mad:2170`, `src/LO_SYN.mad:2239`, `src/LO_SYN.mad:2263` … (+2) | 8 |
| `EXT_40440` | `40440B` | `src/LO_SYN.mad:82` | `src/LO_SYN.mad:848`, `src/LO_SYN.mad:916`, `src/LO_SYN.mad:1012`, `src/LO_SYN.mad:1022`, `src/LO_SYN.mad:1117`, `src/LO_SYN.mad:2240` … (+7) | 13 |
| `ADRPTR_20160` | `20160B` | `src/LO_SYN.mad:83` | `src/LO_SYN.mad:850` | 1 |
| `MEM_4572` | `4572B` | `src/LO_SYN.mad:84` | `src/LO_SYN.mad:851`, `src/LO_SYN.mad:2827` | 2 |
| `EX20_40513` | `40513B` | `src/LO_SYN.mad:85` | `src/LO_SYN.mad:853` | 1 |
| `MEM_120` | `120B` | `src/LO_SYN.mad:86` | `src/LO_SYN.mad:854`, `src/LO_SYN.mad:2935` | 2 |
| `EX36_62117` | `62117B` | `src/LO_SYN.mad:87` | `src/LO_SYN.mad:856` | 1 |
| `EXT_73105` | `73105B` | `src/LO_SYN.mad:88` | `src/LO_SYN.mad:857`, `src/LO_SYN.mad:3014` | 2 |
| `EX20_64561` | `64561B` | `src/LO_SYN.mad:89` | `src/LO_SYN.mad:859` | 1 |
| `EXT_66140` | `66140B` | `src/LO_SYN.mad:90` | `src/LO_SYN.mad:866`, `src/LO_SYN.mad:893`, `src/LO_SYN.mad:1583` | 3 |
| `EXT_20103` | `20103B` | `src/LO_SYN.mad:91` | `src/LO_SYN.mad:868`, `src/LO_SYN.mad:895`, `src/LO_SYN.mad:1585`, `src/LO_SYN.mad:1706`, `src/LO_SYN.mad:2054`, `src/LO_SYN.mad:2084` … (+1) | 7 |
| `EXT_47502` | `47502B` | `src/LO_SYN.mad:92` | `src/LO_SYN.mad:869`, `src/LO_SYN.mad:896`, `src/LO_SYN.mad:1586` | 3 |
| `MEM_70151` | `70151B` | `src/LO_SYN.mad:93` | `src/LO_SYN.mad:871`, `src/LO_SYN.mad:1289`, `src/LO_SYN.mad:2032`, `src/LO_SYN.mad:2843` | 4 |
| `EXT_64440` | `64440B` | `src/LO_SYN.mad:94` | `src/LO_SYN.mad:872`, `src/LO_SYN.mad:955`, `src/LO_SYN.mad:1496`, `src/LO_SYN.mad:1511`, `src/LO_SYN.mad:1544`, `src/LO_SYN.mad:1589` … (+3) | 9 |
| `ADRPTR_62105` | `62105B` | `src/LO_SYN.mad:95` | `src/LO_SYN.mad:874`, `src/LO_SYN.mad:1202`, `src/LO_SYN.mad:1207`, `src/LO_SYN.mad:1792` | 4 |
| `EX20_52040` | `52040B` | `src/LO_SYN.mad:96` | `src/LO_SYN.mad:875`, `src/LO_SYN.mad:1204`, `src/LO_SYN.mad:1208`, `src/LO_SYN.mad:1793` | 4 |
| `EX20_42544` | `42544B` | `src/LO_SYN.mad:97` | `src/LO_SYN.mad:877`, `src/LO_SYN.mad:1231`, `src/LO_SYN.mad:1243`, `src/LO_SYN.mad:1294`, `src/LO_SYN.mad:1327`, `src/LO_SYN.mad:1372` … (+12) | 18 |
| `EX36_70131` | `70131B` | `src/LO_SYN.mad:98` | `src/LO_SYN.mad:878`, `src/LO_SYN.mad:1232`, `src/LO_SYN.mad:1244`, `src/LO_SYN.mad:1295`, `src/LO_SYN.mad:1328`, `src/LO_SYN.mad:1373` … (+12) | 18 |
| `EX65_2151` | `2151B` | `src/LO_SYN.mad:99` | `src/LO_SYN.mad:880`, `src/LO_SYN.mad:1234`, `src/LO_SYN.mad:1246`, `src/LO_SYN.mad:1297`, `src/LO_SYN.mad:1330`, `src/LO_SYN.mad:1375` … (+13) | 19 |
| `EXT_20113` | `20113B` | `src/LO_SYN.mad:100` | `src/LO_SYN.mad:881`, `src/LO_SYN.mad:1595`, `src/LO_SYN.mad:2353` | 3 |
| `EXT_60176` | `60176B` | `src/LO_SYN.mad:101` | `src/LO_SYN.mad:883`, `src/LO_SYN.mad:1597` | 2 |
| `MEM_1554` | `1554B` | `src/LO_SYN.mad:102` | `src/LO_SYN.mad:884`, `src/LO_SYN.mad:1598` | 2 |
| `EX36_41117` | `41117B` | `src/LO_SYN.mad:103` | `src/LO_SYN.mad:886`, `src/LO_SYN.mad:1600` | 2 |
| `EX36_52103` | `52103B` | `src/LO_SYN.mad:104` | `src/LO_SYN.mad:889`, `src/LO_SYN.mad:910`, `src/LO_SYN.mad:1006`, `src/LO_SYN.mad:1039`, `src/LO_SYN.mad:1099`, `src/LO_SYN.mad:1189` … (+11) | 17 |
| `ADRPTR_52103` | `52103B` | `src/LO_SYN.mad:105` | `src/LO_SYN.mad:890`, `src/LO_SYN.mad:911`, `src/LO_SYN.mad:1007`, `src/LO_SYN.mad:1040`, `src/LO_SYN.mad:1100`, `src/LO_SYN.mad:1190` … (+11) | 17 |
| `MEM_71040` | `71040B` | `src/LO_SYN.mad:106` | `src/LO_SYN.mad:892`, `src/LO_SYN.mad:913`, `src/LO_SYN.mad:1009`, `src/LO_SYN.mad:1042`, `src/LO_SYN.mad:1102`, `src/LO_SYN.mad:1192` … (+10) | 16 |
| `EX36_20040` | `20040B` | `src/LO_SYN.mad:107` | `src/LO_SYN.mad:898`, `src/LO_SYN.mad:2230`, `src/LO_SYN.mad:2254`, `src/LO_SYN.mad:2962` | 4 |
| `EX20_42503` | `42503B` | `src/LO_SYN.mad:108` | `src/LO_SYN.mad:901`, `src/LO_SYN.mad:961`, `src/LO_SYN.mad:2539` | 3 |
| `EX36_47524` | `47524B` | `src/LO_SYN.mad:109` | `src/LO_SYN.mad:902`, `src/LO_SYN.mad:962`, `src/LO_SYN.mad:2540` | 3 |
| `REGVAL_2524` | `2524B` | `src/LO_SYN.mad:110` | `src/LO_SYN.mad:904`, `src/LO_SYN.mad:964`, `src/LO_SYN.mad:2542`, `src/LO_SYN.mad:2786` | 4 |
| `MEM_1513` | `1513B` | `src/LO_SYN.mad:111` | `src/LO_SYN.mad:905`, `src/LO_SYN.mad:1046`, `src/LO_SYN.mad:1135`, `src/LO_SYN.mad:1183`, `src/LO_SYN.mad:1481`, `src/LO_SYN.mad:1516` … (+4) | 10 |
| `EX36_61117` | `61117B` | `src/LO_SYN.mad:112` | `src/LO_SYN.mad:907`, `src/LO_SYN.mad:2545` | 2 |
| `EXT_20040` | `20040B` | `src/LO_SYN.mad:113` | `src/LO_SYN.mad:908`, `src/LO_SYN.mad:1358`, `src/LO_SYN.mad:1532`, `src/LO_SYN.mad:1910`, `src/LO_SYN.mad:2315`, `src/LO_SYN.mad:2546` … (+1) | 7 |
| `MEM_77576` | `77576B` | `src/LO_SYN.mad:114` | `src/LO_SYN.mad:914` | 1 |
| `REGVAL_154` | `154B` | `src/LO_SYN.mad:115` | `src/LO_SYN.mad:917` | 1 |
| `EX36_63551` | `63551B` | `src/LO_SYN.mad:116` | `src/LO_SYN.mad:919` | 1 |
| `EXT_20117` | `20117B` | `src/LO_SYN.mad:117` | `src/LO_SYN.mad:920`, `src/LO_SYN.mad:1247`, `src/LO_SYN.mad:1403`, `src/LO_SYN.mad:2909` | 4 |
| `MEM_2520` | `2520B` | `src/LO_SYN.mad:118` | `src/LO_SYN.mad:922`, `src/LO_SYN.mad:982`, `src/LO_SYN.mad:1081`, `src/LO_SYN.mad:1855`, `src/LO_SYN.mad:1924`, `src/LO_SYN.mad:1963` … (+13) | 19 |
| `MEM_1440` | `1440B` | `src/LO_SYN.mad:119` | `src/LO_SYN.mad:923`, `src/LO_SYN.mad:2912` | 2 |
| `REGVAL_151` | `151B` | `src/LO_SYN.mad:120` | `src/LO_SYN.mad:925`, `src/LO_SYN.mad:1573` | 2 |
| `MEM_72510` | `72510B` | `src/LO_SYN.mad:121` | `src/LO_SYN.mad:926` | 1 |
| `MODVAL_70142` | `70142B` | `src/LO_SYN.mad:122` | `src/LO_SYN.mad:928`, `src/LO_SYN.mad:2044`, `src/LO_SYN.mad:2215` | 3 |
| `EX36_66170` | `66170B` | `src/LO_SYN.mad:123` | `src/LO_SYN.mad:929`, `src/LO_SYN.mad:1028`, `src/LO_SYN.mad:1060`, `src/LO_SYN.mad:3050`, `src/LO_SYN.mad:3146` | 5 |
| `EXT_42440` | `42440B` | `src/LO_SYN.mad:124` | `src/LO_SYN.mad:931`, `src/LO_SYN.mad:1061`, `src/LO_SYN.mad:1130`, `src/LO_SYN.mad:1178`, `src/LO_SYN.mad:1220`, `src/LO_SYN.mad:1255` … (+14) | 20 |
| `REGVAL_76551` | `76551B` | `src/LO_SYN.mad:125` | `src/LO_SYN.mad:932`, `src/LO_SYN.mad:3194` | 2 |
| `MEM_6151` | `6151B` | `src/LO_SYN.mad:126` | `src/LO_SYN.mad:934` | 1 |
| `MEM_72520` | `72520B` | `src/LO_SYN.mad:127` | `src/LO_SYN.mad:935` | 1 |
| `EXT_47510` | `47510B` | `src/LO_SYN.mad:128` | `src/LO_SYN.mad:941`, `src/LO_SYN.mad:970`, `src/LO_SYN.mad:994`, `src/LO_SYN.mad:1448`, `src/LO_SYN.mad:1459`, `src/LO_SYN.mad:2372` … (+5) | 11 |
| `EX65_2040` | `2040B` | `src/LO_SYN.mad:129` | `src/LO_SYN.mad:943`, `src/LO_SYN.mad:971`, `src/LO_SYN.mad:995`, `src/LO_SYN.mad:1450`, `src/LO_SYN.mad:1460`, `src/LO_SYN.mad:1961` … (+3) | 9 |
| `REGVAL_122` | `122B` | `src/LO_SYN.mad:130` | `src/LO_SYN.mad:946` | 1 |
| `EXT_45517` | `45517B` | `src/LO_SYN.mad:131` | `src/LO_SYN.mad:947`, `src/LO_SYN.mad:3047`, `src/LO_SYN.mad:3143` | 3 |
| `EX20_41524` | `41524B` | `src/LO_SYN.mad:132` | `src/LO_SYN.mad:949`, `src/LO_SYN.mad:1727`, `src/LO_SYN.mad:2812`, `src/LO_SYN.mad:3044` | 4 |
| `MEM_1117` | `1117B` | `src/LO_SYN.mad:133` | `src/LO_SYN.mad:950`, `src/LO_SYN.mad:3019` | 2 |
| `EXT_74173` | `74173B` | `src/LO_SYN.mad:134` | `src/LO_SYN.mad:952`, `src/LO_SYN.mad:3020` | 2 |
| `MEM_70066` | `70066B` | `src/LO_SYN.mad:135` | `src/LO_SYN.mad:953` | 1 |
| `EXT_64524` | `64524B` | `src/LO_SYN.mad:136` | `src/LO_SYN.mad:956` | 1 |
| `MEM_70040` | `70040B` | `src/LO_SYN.mad:137` | `src/LO_SYN.mad:958`, `src/LO_SYN.mad:1580`, `src/LO_SYN.mad:1645`, `src/LO_SYN.mad:2282` | 4 |
| `MEM_5501` | `5501B` | `src/LO_SYN.mad:138` | `src/LO_SYN.mad:965` | 1 |
| `EX47_4576` | `4576B` | `src/LO_SYN.mad:139` | `src/LO_SYN.mad:967`, `src/LO_SYN.mad:2246` | 2 |
| `MEM_75440` | `75440B` | `src/LO_SYN.mad:140` | `src/LO_SYN.mad:968` | 1 |
| `REGVAL_4105` | `4105B` | `src/LO_SYN.mad:141` | `src/LO_SYN.mad:973`, `src/LO_SYN.mad:997` | 2 |
| `MEM_2151` | `2151B` | `src/LO_SYN.mad:142` | `src/LO_SYN.mad:974`, `src/LO_SYN.mad:998`, `src/LO_SYN.mad:1900`, `src/LO_SYN.mad:2999` | 4 |
| `MEM_101` | `101B` | `src/LO_SYN.mad:143` | `src/LO_SYN.mad:976`, `src/LO_SYN.mad:1000`, `src/LO_SYN.mad:1003`, `src/LO_SYN.mad:1322`, `src/LO_SYN.mad:1531`, `src/LO_SYN.mad:2677` | 6 |
| `REGVAL_47510` | `47510B` | `src/LO_SYN.mad:144` | `src/LO_SYN.mad:977`, `src/LO_SYN.mad:1001` | 2 |
| `MEM_40` | `40B` | `src/LO_SYN.mad:145` | `src/LO_SYN.mad:979`, `src/LO_SYN.mad:1049`, `src/LO_SYN.mad:1268`, `src/LO_SYN.mad:1471`, `src/LO_SYN.mad:1484`, `src/LO_SYN.mad:1519` … (+11) | 17 |
| `MEM_70117` | `70117B` | `src/LO_SYN.mad:146` | `src/LO_SYN.mad:983`, `src/LO_SYN.mad:1082`, `src/LO_SYN.mad:2666`, `src/LO_SYN.mad:2899`, `src/LO_SYN.mad:3134`, `src/LO_SYN.mad:3155` | 6 |
| `EXT_20115` | `20115B` | `src/LO_SYN.mad:147` | `src/LO_SYN.mad:985`, `src/LO_SYN.mad:1084` | 2 |
| `MEM_4124` | `4124B` | `src/LO_SYN.mad:148` | `src/LO_SYN.mad:986`, `src/LO_SYN.mad:1085` | 2 |
| `ADRPTR_41503` | `41503B` | `src/LO_SYN.mad:149` | `src/LO_SYN.mad:988`, `src/LO_SYN.mad:1087` | 2 |
| `EX64_2554` | `2554B` | `src/LO_SYN.mad:150` | `src/LO_SYN.mad:991`, `src/LO_SYN.mad:1570`, `src/LO_SYN.mad:1675`, `src/LO_SYN.mad:2996` | 4 |
| `MEM_440` | `440B` | `src/LO_SYN.mad:151` | `src/LO_SYN.mad:992`, `src/LO_SYN.mad:1037`, `src/LO_SYN.mad:1097`, `src/LO_SYN.mad:1393`, `src/LO_SYN.mad:2168`, `src/LO_SYN.mad:3001` … (+1) | 7 |
| `EX62_6466` | `6466B` | `src/LO_SYN.mad:152` | `src/LO_SYN.mad:1004` | 1 |
| `MEM_151` | `151B` | `src/LO_SYN.mad:153` | `src/LO_SYN.mad:1013`, `src/LO_SYN.mad:1495`, `src/LO_SYN.mad:1510`, `src/LO_SYN.mad:1543`, `src/LO_SYN.mad:1657`, `src/LO_SYN.mad:1840` … (+3) | 9 |
| `MEM_3117` | `3117B` | `src/LO_SYN.mad:154` | `src/LO_SYN.mad:1015`, `src/LO_SYN.mad:1318`, `src/LO_SYN.mad:1763`, `src/LO_SYN.mad:2737` | 4 |
| `MEM_6501` | `6501B` | `src/LO_SYN.mad:155` | `src/LO_SYN.mad:1016`, `src/LO_SYN.mad:1319`, `src/LO_SYN.mad:1366`, `src/LO_SYN.mad:1738`, `src/LO_SYN.mad:1765`, `src/LO_SYN.mad:2738` | 6 |
| `MEM_72440` | `72440B` | `src/LO_SYN.mad:156` | `src/LO_SYN.mad:1018`, `src/LO_SYN.mad:1025`, `src/LO_SYN.mad:2555`, `src/LO_SYN.mad:2758`, `src/LO_SYN.mad:2779` | 5 |
| `MEM_510` | `510B` | `src/LO_SYN.mad:157` | `src/LO_SYN.mad:1024`, `src/LO_SYN.mad:1774` | 2 |
| `ADRPTR_41560` | `41560B` | `src/LO_SYN.mad:158` | `src/LO_SYN.mad:1027`, `src/LO_SYN.mad:3101` | 2 |
| `REGVAL_20113` | `20113B` | `src/LO_SYN.mad:159` | `src/LO_SYN.mad:1030` | 1 |
| `MEM_5440` | `5440B` | `src/LO_SYN.mad:160` | `src/LO_SYN.mad:1031`, `src/LO_SYN.mad:2354`, `src/LO_SYN.mad:2450`, `src/LO_SYN.mad:2681`, `src/LO_SYN.mad:3187` | 5 |
| `EX20_42546` | `42546B` | `src/LO_SYN.mad:161` | `src/LO_SYN.mad:1033` | 1 |
| `EX36_50115` | `50115B` | `src/LO_SYN.mad:162` | `src/LO_SYN.mad:1034`, `src/LO_SYN.mad:1076`, `src/LO_SYN.mad:1151`, `src/LO_SYN.mad:1526` | 4 |
| `MEM_2110` | `2110B` | `src/LO_SYN.mad:163` | `src/LO_SYN.mad:1036`, `src/LO_SYN.mad:3055`, `src/LO_SYN.mad:3191` | 3 |
| `EX36_52113` | `52113B` | `src/LO_SYN.mad:164` | `src/LO_SYN.mad:1043`, `src/LO_SYN.mad:1609` | 2 |
| `MEM_4502` | `4502B` | `src/LO_SYN.mad:165` | `src/LO_SYN.mad:1045`, `src/LO_SYN.mad:1133`, `src/LO_SYN.mad:1181`, `src/LO_SYN.mad:1480`, `src/LO_SYN.mad:1514`, `src/LO_SYN.mad:1610` … (+2) | 8 |
| `EX36_61113` | `61113B` | `src/LO_SYN.mad:166` | `src/LO_SYN.mad:1048`, `src/LO_SYN.mad:1136`, `src/LO_SYN.mad:1184`, `src/LO_SYN.mad:1483`, `src/LO_SYN.mad:1517`, `src/LO_SYN.mad:1613` … (+1) | 7 |
| `EX66_76131` | `76131B` | `src/LO_SYN.mad:167` | `src/LO_SYN.mad:1051` | 1 |
| `EX46_4510` | `4510B` | `src/LO_SYN.mad:168` | `src/LO_SYN.mad:1052` | 1 |
| `MEM_102` | `102B` | `src/LO_SYN.mad:169` | `src/LO_SYN.mad:1054`, `src/LO_SYN.mad:2750` | 2 |
| `EXT_47566` | `47566B` | `src/LO_SYN.mad:170` | `src/LO_SYN.mad:1055`, `src/LO_SYN.mad:2182`, `src/LO_SYN.mad:2410` | 3 |
| `MEM_74151` | `74151B` | `src/LO_SYN.mad:171` | `src/LO_SYN.mad:1057`, `src/LO_SYN.mad:2830`, `src/LO_SYN.mad:2966` | 3 |
| `REGVAL_20142` | `20142B` | `src/LO_SYN.mad:172` | `src/LO_SYN.mad:1058` | 1 |
| `MEM_3055` | `3055B` | `src/LO_SYN.mad:173` | `src/LO_SYN.mad:1063` | 1 |
| `MEM_1560` | `1560B` | `src/LO_SYN.mad:174` | `src/LO_SYN.mad:1069`, `src/LO_SYN.mad:1144` | 2 |
| `MEM_71551` | `71551B` | `src/LO_SYN.mad:175` | `src/LO_SYN.mad:1070`, `src/LO_SYN.mad:1145` | 2 |
| `EX46_74513` | `74513B` | `src/LO_SYN.mad:176` | `src/LO_SYN.mad:1072`, `src/LO_SYN.mad:1147` | 2 |
| `MEM_1551` | `1551B` | `src/LO_SYN.mad:177` | `src/LO_SYN.mad:1073`, `src/LO_SYN.mad:1148`, `src/LO_SYN.mad:1291`, `src/LO_SYN.mad:2398`, `src/LO_SYN.mad:2417`, `src/LO_SYN.mad:2426` … (+6) | 12 |
| `ADRPTR_20146` | `20146B` | `src/LO_SYN.mad:178` | `src/LO_SYN.mad:1075`, `src/LO_SYN.mad:1150` | 2 |
| `MEM_2101` | `2101B` | `src/LO_SYN.mad:179` | `src/LO_SYN.mad:1078`, `src/LO_SYN.mad:1153`, `src/LO_SYN.mad:1267`, `src/LO_SYN.mad:1424`, `src/LO_SYN.mad:1469`, `src/LO_SYN.mad:1493` … (+13) | 19 |
| `MEM_77554` | `77554B` | `src/LO_SYN.mad:180` | `src/LO_SYN.mad:1090`, `src/LO_SYN.mad:1453`, `src/LO_SYN.mad:1462`, `src/LO_SYN.mad:1486`, `src/LO_SYN.mad:1501`, `src/LO_SYN.mad:1534` … (+11) | 17 |
| `REGVAL_74101` | `74101B` | `src/LO_SYN.mad:181` | `src/LO_SYN.mad:1091`, `src/LO_SYN.mad:1454`, `src/LO_SYN.mad:1463`, `src/LO_SYN.mad:1604`, `src/LO_SYN.mad:1619` | 5 |
| `MEM_1171` | `1171B` | `src/LO_SYN.mad:182` | `src/LO_SYN.mad:1093`, `src/LO_SYN.mad:1456`, `src/LO_SYN.mad:1465`, `src/LO_SYN.mad:1489`, `src/LO_SYN.mad:1504`, `src/LO_SYN.mad:1537` … (+14) | 20 |
| `MEM_74040` | `74040B` | `src/LO_SYN.mad:183` | `src/LO_SYN.mad:1094`, `src/LO_SYN.mad:1430`, `src/LO_SYN.mad:1457`, `src/LO_SYN.mad:1466`, `src/LO_SYN.mad:1490`, `src/LO_SYN.mad:1505` … (+18) | 24 |
| `EX66_4546` | `4546B` | `src/LO_SYN.mad:184` | `src/LO_SYN.mad:1096` | 1 |
| `MEM_572` | `572B` | `src/LO_SYN.mad:185` | `src/LO_SYN.mad:1103`, `src/LO_SYN.mad:1628`, `src/LO_SYN.mad:1784`, `src/LO_SYN.mad:1865`, `src/LO_SYN.mad:3167` | 5 |
| `MEM_72554` | `72554B` | `src/LO_SYN.mad:186` | `src/LO_SYN.mad:1105`, `src/LO_SYN.mad:1240`, `src/LO_SYN.mad:1786`, `src/LO_SYN.mad:2278`, `src/LO_SYN.mad:2902`, `src/LO_SYN.mad:2965` … (+1) | 7 |
| `ADRPTR_52105` | `52105B` | `src/LO_SYN.mad:187` | `src/LO_SYN.mad:1106`, `src/LO_SYN.mad:1787` | 2 |
| `EXT_74040` | `74040B` | `src/LO_SYN.mad:188` | `src/LO_SYN.mad:1108`, `src/LO_SYN.mad:1789` | 2 |
| `ADRPTR_66151` | `66151B` | `src/LO_SYN.mad:189` | `src/LO_SYN.mad:1109`, `src/LO_SYN.mad:2336`, `src/LO_SYN.mad:3127`, `src/LO_SYN.mad:3293` | 4 |
| `MEM_5101` | `5101B` | `src/LO_SYN.mad:190` | `src/LO_SYN.mad:1111`, `src/LO_SYN.mad:2165` | 2 |
| `EXT_50171` | `50171B` | `src/LO_SYN.mad:191` | `src/LO_SYN.mad:1112` | 1 |
| `REGVAL_103` | `103B` | `src/LO_SYN.mad:192` | `src/LO_SYN.mad:1114`, `src/LO_SYN.mad:1217`, `src/LO_SYN.mad:1252`, `src/LO_SYN.mad:1277`, `src/LO_SYN.mad:1408`, `src/LO_SYN.mad:2146` … (+5) | 11 |
| `EXT_47542` | `47542B` | `src/LO_SYN.mad:193` | `src/LO_SYN.mad:1115`, `src/LO_SYN.mad:2147` | 2 |
| `EX66_4515` | `4515B` | `src/LO_SYN.mad:194` | `src/LO_SYN.mad:1120`, `src/LO_SYN.mad:1168` | 2 |
| `REGVAL_7554` | `7554B` | `src/LO_SYN.mad:195` | `src/LO_SYN.mad:1121`, `src/LO_SYN.mad:1169` | 2 |
| `MEM_1103` | `1103B` | `src/LO_SYN.mad:196` | `src/LO_SYN.mad:1123`, `src/LO_SYN.mad:1171`, `src/LO_SYN.mad:1211` | 3 |
| `MEM_70105` | `70105B` | `src/LO_SYN.mad:197` | `src/LO_SYN.mad:1124`, `src/LO_SYN.mad:1172`, `src/LO_SYN.mad:1213`, `src/LO_SYN.mad:1895`, `src/LO_SYN.mad:2569`, `src/LO_SYN.mad:2836` … (+3) | 9 |
| `MEM_74554` | `74554B` | `src/LO_SYN.mad:198` | `src/LO_SYN.mad:1126`, `src/LO_SYN.mad:1174` | 2 |
| `EX67_440` | `440B` | `src/LO_SYN.mad:199` | `src/LO_SYN.mad:1127`, `src/LO_SYN.mad:1175`, `src/LO_SYN.mad:1216`, `src/LO_SYN.mad:3076`, `src/LO_SYN.mad:3097` | 5 |
| `MEM_7503` | `7503B` | `src/LO_SYN.mad:200` | `src/LO_SYN.mad:1129`, `src/LO_SYN.mad:1177`, `src/LO_SYN.mad:2158`, `src/LO_SYN.mad:2257`, `src/LO_SYN.mad:2488`, `src/LO_SYN.mad:2500` … (+3) | 9 |
| `REGVAL_40513` | `40513B` | `src/LO_SYN.mad:201` | `src/LO_SYN.mad:1132`, `src/LO_SYN.mad:1180`, `src/LO_SYN.mad:1478`, `src/LO_SYN.mad:1513`, `src/LO_SYN.mad:1660`, `src/LO_SYN.mad:2413` … (+1) | 7 |
| `MEM_7502` | `7502B` | `src/LO_SYN.mad:202` | `src/LO_SYN.mad:1156`, `src/LO_SYN.mad:1729`, `src/LO_SYN.mad:1901`, `src/LO_SYN.mad:2524`, `src/LO_SYN.mad:3112` | 5 |
| `MEM_77520` | `77520B` | `src/LO_SYN.mad:203` | `src/LO_SYN.mad:1157`, `src/LO_SYN.mad:1730`, `src/LO_SYN.mad:2525`, `src/LO_SYN.mad:3113` | 4 |
| `MEM_7560` | `7560B` | `src/LO_SYN.mad:204` | `src/LO_SYN.mad:1159`, `src/LO_SYN.mad:1733`, `src/LO_SYN.mad:2066`, `src/LO_SYN.mad:2527`, `src/LO_SYN.mad:2591` | 5 |
| `MEM_2544` | `2544B` | `src/LO_SYN.mad:205` | `src/LO_SYN.mad:1160`, `src/LO_SYN.mad:2528`, `src/LO_SYN.mad:2593` | 3 |
| `MEM_76105` | `76105B` | `src/LO_SYN.mad:206` | `src/LO_SYN.mad:1162`, `src/LO_SYN.mad:2530` | 2 |
| `EX20_20115` | `20115B` | `src/LO_SYN.mad:207` | `src/LO_SYN.mad:1163`, `src/LO_SYN.mad:2531` | 2 |
| `ADRPTR_46561` | `46561B` | `src/LO_SYN.mad:208` | `src/LO_SYN.mad:1193`, `src/LO_SYN.mad:1306`, `src/LO_SYN.mad:1364`, `src/LO_SYN.mad:2474` | 4 |
| `MEM_117` | `117B` | `src/LO_SYN.mad:209` | `src/LO_SYN.mad:1195`, `src/LO_SYN.mad:1436`, `src/LO_SYN.mad:1801`, `src/LO_SYN.mad:1960`, `src/LO_SYN.mad:2314`, `src/LO_SYN.mad:2476` … (+3) | 9 |
| `MEM_70120` | `70120B` | `src/LO_SYN.mad:210` | `src/LO_SYN.mad:1196`, `src/LO_SYN.mad:2477`, `src/LO_SYN.mad:3130` | 3 |
| `ADRPTR_73105` | `73105B` | `src/LO_SYN.mad:211` | `src/LO_SYN.mad:1210` | 1 |
| `EXT_40554` | `40554B` | `src/LO_SYN.mad:212` | `src/LO_SYN.mad:1214`, `src/LO_SYN.mad:1223`, `src/LO_SYN.mad:1271`, `src/LO_SYN.mad:1336`, `src/LO_SYN.mad:2312`, `src/LO_SYN.mad:2869` | 6 |
| `MEM_4503` | `4503B` | `src/LO_SYN.mad:213` | `src/LO_SYN.mad:1219`, `src/LO_SYN.mad:1253`, `src/LO_SYN.mad:1279`, `src/LO_SYN.mad:1409`, `src/LO_SYN.mad:1876`, `src/LO_SYN.mad:2110` … (+7) | 13 |
| `REGVAL_77520` | `77520B` | `src/LO_SYN.mad:214` | `src/LO_SYN.mad:1222`, `src/LO_SYN.mad:1270`, `src/LO_SYN.mad:1334` | 3 |
| `EX20_44040` | `44040B` | `src/LO_SYN.mad:215` | `src/LO_SYN.mad:1225`, `src/LO_SYN.mad:1273`, `src/LO_SYN.mad:1337` | 3 |
| `MEM_520` | `520B` | `src/LO_SYN.mad:216` | `src/LO_SYN.mad:1226`, `src/LO_SYN.mad:1274`, `src/LO_SYN.mad:1339`, `src/LO_SYN.mad:2444`, `src/LO_SYN.mad:2641` | 5 |
| `MEM_6440` | `6440B` | `src/LO_SYN.mad:217` | `src/LO_SYN.mad:1228`, `src/LO_SYN.mad:1276`, `src/LO_SYN.mad:1340`, `src/LO_SYN.mad:2642` | 4 |
| `EXT_20120` | `20120B` | `src/LO_SYN.mad:218` | `src/LO_SYN.mad:1235`, `src/LO_SYN.mad:1897`, `src/LO_SYN.mad:2668` | 3 |
| `MEM_5144` | `5144B` | `src/LO_SYN.mad:219` | `src/LO_SYN.mad:1237` | 1 |
| `MEM_76151` | `76151B` | `src/LO_SYN.mad:220` | `src/LO_SYN.mad:1238` | 1 |
| `EX20_20040` | `20040B` | `src/LO_SYN.mad:221` | `src/LO_SYN.mad:1241`, `src/LO_SYN.mad:2177`, `src/LO_SYN.mad:2509` | 3 |
| `REGVAL_6105` | `6105B` | `src/LO_SYN.mad:222` | `src/LO_SYN.mad:1249`, `src/LO_SYN.mad:1405` | 2 |
| `EXT_52040` | `52040B` | `src/LO_SYN.mad:223` | `src/LO_SYN.mad:1250`, `src/LO_SYN.mad:1406` | 2 |
| `MEM_74124` | `74124B` | `src/LO_SYN.mad:224` | `src/LO_SYN.mad:1256`, `src/LO_SYN.mad:1282` | 2 |
| `MEM_71116` | `71116B` | `src/LO_SYN.mad:225` | `src/LO_SYN.mad:1258`, `src/LO_SYN.mad:1283`, `src/LO_SYN.mad:2788` | 3 |
| `REGVAL_40560` | `40560B` | `src/LO_SYN.mad:226` | `src/LO_SYN.mad:1265`, `src/LO_SYN.mad:1468`, `src/LO_SYN.mad:1492`, `src/LO_SYN.mad:1507`, `src/LO_SYN.mad:1540`, `src/LO_SYN.mad:1654` … (+2) | 8 |
| `MEM_77124` | `77124B` | `src/LO_SYN.mad:227` | `src/LO_SYN.mad:1285` | 1 |
| `MEM_4440` | `4440B` | `src/LO_SYN.mad:228` | `src/LO_SYN.mad:1286`, `src/LO_SYN.mad:1853`, `src/LO_SYN.mad:2720` | 3 |
| `REGVAL_4131` | `4131B` | `src/LO_SYN.mad:229` | `src/LO_SYN.mad:1288` | 1 |
| `EXT_66101` | `66101B` | `src/LO_SYN.mad:230` | `src/LO_SYN.mad:1292`, `src/LO_SYN.mad:2399`, `src/LO_SYN.mad:2573`, `src/LO_SYN.mad:2893`, `src/LO_SYN.mad:2924`, `src/LO_SYN.mad:3011` | 6 |
| `EXT_20151` | `20151B` | `src/LO_SYN.mad:231` | `src/LO_SYN.mad:1298`, `src/LO_SYN.mad:1331`, `src/LO_SYN.mad:1376`, `src/LO_SYN.mad:1445` | 4 |
| `EXT_70440` | `70440B` | `src/LO_SYN.mad:232` | `src/LO_SYN.mad:1300`, `src/LO_SYN.mad:1333`, `src/LO_SYN.mad:1378`, `src/LO_SYN.mad:1447` | 4 |
| `MEM_4117` | `4117B` | `src/LO_SYN.mad:233` | `src/LO_SYN.mad:1301`, `src/LO_SYN.mad:1439`, `src/LO_SYN.mad:1804` | 3 |
| `MEM_70440` | `70440B` | `src/LO_SYN.mad:234` | `src/LO_SYN.mad:1303`, `src/LO_SYN.mad:1396`, `src/LO_SYN.mad:2614`, `src/LO_SYN.mad:2632`, `src/LO_SYN.mad:2653`, `src/LO_SYN.mad:2954` … (+2) | 8 |
| `MEM_1130` | `1130B` | `src/LO_SYN.mad:235` | `src/LO_SYN.mad:1307` | 1 |
| `EX36_62101` | `62101B` | `src/LO_SYN.mad:236` | `src/LO_SYN.mad:1309` | 1 |
| `MEM_4105` | `4105B` | `src/LO_SYN.mad:237` | `src/LO_SYN.mad:1310`, `src/LO_SYN.mad:1346`, `src/LO_SYN.mad:1762`, `src/LO_SYN.mad:1913`, `src/LO_SYN.mad:2030`, `src/LO_SYN.mad:2069` … (+4) | 10 |
| `MEM_2117` | `2117B` | `src/LO_SYN.mad:238` | `src/LO_SYN.mad:1312`, `src/LO_SYN.mad:1438`, `src/LO_SYN.mad:1715`, `src/LO_SYN.mad:1802`, `src/LO_SYN.mad:3013` | 5 |
| `EXT_73110` | `73110B` | `src/LO_SYN.mad:239` | `src/LO_SYN.mad:1313` | 1 |
| `EX36_20142` | `20142B` | `src/LO_SYN.mad:240` | `src/LO_SYN.mad:1315` | 1 |
| `ADRPTR_52170` | `52170B` | `src/LO_SYN.mad:241` | `src/LO_SYN.mad:1316`, `src/LO_SYN.mad:2216`, `src/LO_SYN.mad:3017` | 3 |
| `EXT_74110` | `74110B` | `src/LO_SYN.mad:242` | `src/LO_SYN.mad:1321`, `src/LO_SYN.mad:1766` | 2 |
| `MEM_515` | `515B` | `src/LO_SYN.mad:243` | `src/LO_SYN.mad:1324` | 1 |
| `MEM_74560` | `74560B` | `src/LO_SYN.mad:244` | `src/LO_SYN.mad:1342`, `src/LO_SYN.mad:1352`, `src/LO_SYN.mad:1418`, `src/LO_SYN.mad:1426`, `src/LO_SYN.mad:2065`, `src/LO_SYN.mad:2876` | 6 |
| `MEM_2516` | `2516B` | `src/LO_SYN.mad:245` | `src/LO_SYN.mad:1343`, `src/LO_SYN.mad:2752`, `src/LO_SYN.mad:2773` | 3 |
| `MEM_71131` | `71131B` | `src/LO_SYN.mad:246` | `src/LO_SYN.mad:1345`, `src/LO_SYN.mad:3163`, `src/LO_SYN.mad:3259` | 3 |
| `MEM_1517` | `1517B` | `src/LO_SYN.mad:247` | `src/LO_SYN.mad:1348`, `src/LO_SYN.mad:1907`, `src/LO_SYN.mad:2071` | 3 |
| `EX36_52102` | `52102B` | `src/LO_SYN.mad:248` | `src/LO_SYN.mad:1349`, `src/LO_SYN.mad:1831`, `src/LO_SYN.mad:2072` | 3 |
| `MEM_72040` | `72040B` | `src/LO_SYN.mad:249` | `src/LO_SYN.mad:1351`, `src/LO_SYN.mad:1832`, `src/LO_SYN.mad:2074`, `src/LO_SYN.mad:2183`, `src/LO_SYN.mad:2411`, `src/LO_SYN.mad:3164` … (+1) | 7 |
| `ADRPTR_20106` | `20106B` | `src/LO_SYN.mad:250` | `src/LO_SYN.mad:1354` | 1 |
| `MEM_77103` | `77103B` | `src/LO_SYN.mad:251` | `src/LO_SYN.mad:1355` | 1 |
| `MEM_74517` | `74517B` | `src/LO_SYN.mad:252` | `src/LO_SYN.mad:1357` | 1 |
| `EX64_1551` | `1551B` | `src/LO_SYN.mad:253` | `src/LO_SYN.mad:1367`, `src/LO_SYN.mad:1739` | 2 |
| `REGVAL_440` | `440B` | `src/LO_SYN.mad:254` | `src/LO_SYN.mad:1369`, `src/LO_SYN.mad:1625`, `src/LO_SYN.mad:1741`, `src/LO_SYN.mad:2714` | 4 |
| `EX64_7515` | `7515B` | `src/LO_SYN.mad:255` | `src/LO_SYN.mad:1379`, `src/LO_SYN.mad:1937` | 2 |
| `EXT_47516` | `47516B` | `src/LO_SYN.mad:256` | `src/LO_SYN.mad:1381`, `src/LO_SYN.mad:1939` | 2 |
| `MEM_1154` | `1154B` | `src/LO_SYN.mad:257` | `src/LO_SYN.mad:1382`, `src/LO_SYN.mad:3281` | 2 |
| `EX36_45501` | `45501B` | `src/LO_SYN.mad:258` | `src/LO_SYN.mad:1384` | 1 |
| `EXT_47503` | `47503B` | `src/LO_SYN.mad:259` | `src/LO_SYN.mad:1391` | 1 |
| `EXT_42520` | `42520B` | `src/LO_SYN.mad:260` | `src/LO_SYN.mad:1394` | 1 |
| `EX36_70151` | `70151B` | `src/LO_SYN.mad:261` | `src/LO_SYN.mad:1414`, `src/LO_SYN.mad:1687` | 2 |
| `EX64_510` | `510B` | `src/LO_SYN.mad:262` | `src/LO_SYN.mad:1415`, `src/LO_SYN.mad:1688` | 2 |
| `ADRPTR_42440` | `42440B` | `src/LO_SYN.mad:263` | `src/LO_SYN.mad:1417`, `src/LO_SYN.mad:1690` | 2 |
| `MEM_160` | `160B` | `src/LO_SYN.mad:264` | `src/LO_SYN.mad:1420`, `src/LO_SYN.mad:1694` | 2 |
| `EX36_41554` | `41554B` | `src/LO_SYN.mad:265` | `src/LO_SYN.mad:1421`, `src/LO_SYN.mad:1696` | 2 |
| `MEM_70104` | `70104B` | `src/LO_SYN.mad:266` | `src/LO_SYN.mad:1423`, `src/LO_SYN.mad:1697` | 2 |
| `MEM_105` | `105B` | `src/LO_SYN.mad:267` | `src/LO_SYN.mad:1427`, `src/LO_SYN.mad:1841`, `src/LO_SYN.mad:1882`, `src/LO_SYN.mad:2276`, `src/LO_SYN.mad:2290`, `src/LO_SYN.mad:2798` … (+3) | 9 |
| `MEM_2515` | `2515B` | `src/LO_SYN.mad:268` | `src/LO_SYN.mad:1429`, `src/LO_SYN.mad:1843`, `src/LO_SYN.mad:1883`, `src/LO_SYN.mad:2249`, `src/LO_SYN.mad:2291`, `src/LO_SYN.mad:2800` … (+1) | 7 |
| `EX36_70120` | `70120B` | `src/LO_SYN.mad:269` | `src/LO_SYN.mad:1432`, `src/LO_SYN.mad:1795`, `src/LO_SYN.mad:2285`, `src/LO_SYN.mad:2957` | 4 |
| `MEM_72105` | `72105B` | `src/LO_SYN.mad:270` | `src/LO_SYN.mad:1433`, `src/LO_SYN.mad:1796`, `src/LO_SYN.mad:2287`, `src/LO_SYN.mad:2959` | 4 |
| `EXT_42510` | `42510B` | `src/LO_SYN.mad:271` | `src/LO_SYN.mad:1435`, `src/LO_SYN.mad:1723`, `src/LO_SYN.mad:2173`, `src/LO_SYN.mad:2288`, `src/LO_SYN.mad:2554`, `src/LO_SYN.mad:2570` … (+6) | 12 |
| `REGVAL_74171` | `74171B` | `src/LO_SYN.mad:272` | `src/LO_SYN.mad:1487`, `src/LO_SYN.mad:1502`, `src/LO_SYN.mad:1535`, `src/LO_SYN.mad:1649`, `src/LO_SYN.mad:2992` | 5 |
| `MEM_77523` | `77523B` | `src/LO_SYN.mad:273` | `src/LO_SYN.mad:1498` | 1 |
| `REGVAL_105` | `105B` | `src/LO_SYN.mad:274` | `src/LO_SYN.mad:1522`, `src/LO_SYN.mad:1807`, `src/LO_SYN.mad:1825`, `src/LO_SYN.mad:1849`, `src/LO_SYN.mad:1870`, `src/LO_SYN.mad:1891` | 6 |
| `MEM_2511` | `2511B` | `src/LO_SYN.mad:275` | `src/LO_SYN.mad:1523`, `src/LO_SYN.mad:1808`, `src/LO_SYN.mad:1826`, `src/LO_SYN.mad:1850`, `src/LO_SYN.mad:1871`, `src/LO_SYN.mad:1892` | 6 |
| `REGVAL_70146` | `70146B` | `src/LO_SYN.mad:276` | `src/LO_SYN.mad:1525` | 1 |
| `MEM_6170` | `6170B` | `src/LO_SYN.mad:277` | `src/LO_SYN.mad:1528` | 1 |
| `EX20_20160` | `20160B` | `src/LO_SYN.mad:278` | `src/LO_SYN.mad:1529` | 1 |
| `EX64_5517` | `5517B` | `src/LO_SYN.mad:279` | `src/LO_SYN.mad:1546`, `src/LO_SYN.mad:2717` | 2 |
| `EX20_42560` | `42560B` | `src/LO_SYN.mad:280` | `src/LO_SYN.mad:1549` | 1 |
| `MEM_502` | `502B` | `src/LO_SYN.mad:281` | `src/LO_SYN.mad:1550` | 1 |
| `ADRPTR_66170` | `66170B` | `src/LO_SYN.mad:282` | `src/LO_SYN.mad:1552`, `src/LO_SYN.mad:2971` | 2 |
| `EX20_47440` | `47440B` | `src/LO_SYN.mad:283` | `src/LO_SYN.mad:1553` | 1 |
| `REGVAL_40544` | `40544B` | `src/LO_SYN.mad:284` | `src/LO_SYN.mad:1555`, `src/LO_SYN.mad:2696` | 2 |
| `MEM_4040` | `4040B` | `src/LO_SYN.mad:285` | `src/LO_SYN.mad:1556` | 1 |
| `ADRPTR_44144` | `44144B` | `src/LO_SYN.mad:286` | `src/LO_SYN.mad:1558`, `src/LO_SYN.mad:1561`, `src/LO_SYN.mad:1837`, `src/LO_SYN.mad:1952`, `src/LO_SYN.mad:1993` | 5 |
| `MEM_75503` | `75503B` | `src/LO_SYN.mad:287` | `src/LO_SYN.mad:1559`, `src/LO_SYN.mad:1819`, `src/LO_SYN.mad:1984`, `src/LO_SYN.mad:2135` | 4 |
| `EXT_41440` | `41440B` | `src/LO_SYN.mad:288` | `src/LO_SYN.mad:1562`, `src/LO_SYN.mad:1778`, `src/LO_SYN.mad:1838`, `src/LO_SYN.mad:1954`, `src/LO_SYN.mad:1994` | 5 |
| `REGVAL_72510` | `72510B` | `src/LO_SYN.mad:289` | `src/LO_SYN.mad:1565` | 1 |
| `ADRPTR_46440` | `46440B` | `src/LO_SYN.mad:290` | `src/LO_SYN.mad:1571`, `src/LO_SYN.mad:1918` | 2 |
| `EX20_62113` | `62113B` | `src/LO_SYN.mad:291` | `src/LO_SYN.mad:1574`, `src/LO_SYN.mad:1754`, `src/LO_SYN.mad:1859`, `src/LO_SYN.mad:1969`, `src/LO_SYN.mad:2833` | 5 |
| `EX62_110` | `110B` | `src/LO_SYN.mad:292` | `src/LO_SYN.mad:1576` | 1 |
| `MEM_70143` | `70143B` | `src/LO_SYN.mad:293` | `src/LO_SYN.mad:1577` | 1 |
| `MEM_76117` | `76117B` | `src/LO_SYN.mad:294` | `src/LO_SYN.mad:1579`, `src/LO_SYN.mad:1720`, `src/LO_SYN.mad:2873` | 3 |
| `EX20_42440` | `42440B` | `src/LO_SYN.mad:295` | `src/LO_SYN.mad:1582`, `src/LO_SYN.mad:1862`, `src/LO_SYN.mad:1999`, `src/LO_SYN.mad:2180`, `src/LO_SYN.mad:2237`, `src/LO_SYN.mad:2261` … (+13) | 19 |
| `EX36_20151` | `20151B` | `src/LO_SYN.mad:296` | `src/LO_SYN.mad:1588`, `src/LO_SYN.mad:2348` | 2 |
| `MEM_4513` | `4513B` | `src/LO_SYN.mad:297` | `src/LO_SYN.mad:1624`, `src/LO_SYN.mad:1631` | 2 |
| `MEM_74501` | `74501B` | `src/LO_SYN.mad:298` | `src/LO_SYN.mad:1627`, `src/LO_SYN.mad:1864` | 2 |
| `EX36_44040` | `44040B` | `src/LO_SYN.mad:299` | `src/LO_SYN.mad:1630` | 1 |
| `REGVAL_110` | `110B` | `src/LO_SYN.mad:300` | `src/LO_SYN.mad:1633` | 1 |
| `MEM_70102` | `70102B` | `src/LO_SYN.mad:301` | `src/LO_SYN.mad:1634` | 1 |
| `MEM_554` | `554B` | `src/LO_SYN.mad:302` | `src/LO_SYN.mad:1636` | 1 |
| `REGVAL_70502` | `70502B` | `src/LO_SYN.mad:303` | `src/LO_SYN.mad:1637` | 1 |
| `ADRPTR_52110` | `52110B` | `src/LO_SYN.mad:304` | `src/LO_SYN.mad:1639` | 1 |
| `EX36_46440` | `46440B` | `src/LO_SYN.mad:305` | `src/LO_SYN.mad:1640`, `src/LO_SYN.mad:2251`, `src/LO_SYN.mad:2701` | 3 |
| `MEM_7520` | `7520B` | `src/LO_SYN.mad:306` | `src/LO_SYN.mad:1642` | 1 |
| `MEM_2113` | `2113B` | `src/LO_SYN.mad:307` | `src/LO_SYN.mad:1643` | 1 |
| `REGVAL_74117` | `74117B` | `src/LO_SYN.mad:308` | `src/LO_SYN.mad:1670`, `src/LO_SYN.mad:2141`, `src/LO_SYN.mad:2618`, `src/LO_SYN.mad:2636`, `src/LO_SYN.mad:2657`, `src/LO_SYN.mad:3226` | 6 |
| `EX36_42440` | `42440B` | `src/LO_SYN.mad:309` | `src/LO_SYN.mad:1676`, `src/LO_SYN.mad:2455`, `src/LO_SYN.mad:2884`, `src/LO_SYN.mad:3181`, `src/LO_SYN.mad:3235` | 5 |
| `EXT_20124` | `20124B` | `src/LO_SYN.mad:310` | `src/LO_SYN.mad:1682`, `src/LO_SYN.mad:1949`, `src/LO_SYN.mad:2686` | 3 |
| `ADRPTR_70040` | `70040B` | `src/LO_SYN.mad:311` | `src/LO_SYN.mad:1684`, `src/LO_SYN.mad:1951` | 2 |
| `EXT_40503` | `40503B` | `src/LO_SYN.mad:312` | `src/LO_SYN.mad:1691`, `src/LO_SYN.mad:1759` | 2 |
| `EX66_4502` | `4502B` | `src/LO_SYN.mad:313` | `src/LO_SYN.mad:1693`, `src/LO_SYN.mad:1760` | 2 |
| `ADRPTR_46502` | `46502B` | `src/LO_SYN.mad:314` | `src/LO_SYN.mad:1708`, `src/LO_SYN.mad:2056`, `src/LO_SYN.mad:2086` | 3 |
| `EX36_66040` | `66040B` | `src/LO_SYN.mad:315` | `src/LO_SYN.mad:1709`, `src/LO_SYN.mad:2057`, `src/LO_SYN.mad:2087` | 3 |
| `MEM_77560` | `77560B` | `src/LO_SYN.mad:316` | `src/LO_SYN.mad:1711`, `src/LO_SYN.mad:1915` | 2 |
| `ADRPTR_41524` | `41524B` | `src/LO_SYN.mad:317` | `src/LO_SYN.mad:1712`, `src/LO_SYN.mad:1916`, `src/LO_SYN.mad:2702` | 3 |
| `ADRPTR_46501` | `46501B` | `src/LO_SYN.mad:318` | `src/LO_SYN.mad:1714` | 1 |
| `EXT_74113` | `74113B` | `src/LO_SYN.mad:319` | `src/LO_SYN.mad:1717` | 1 |
| `EX36_20143` | `20143B` | `src/LO_SYN.mad:320` | `src/LO_SYN.mad:1718`, `src/LO_SYN.mad:2858` | 2 |
| `EXT_64503` | `64503B` | `src/LO_SYN.mad:321` | `src/LO_SYN.mad:1721` | 1 |
| `EX20_40561` | `40561B` | `src/LO_SYN.mad:322` | `src/LO_SYN.mad:1724`, `src/LO_SYN.mad:2402` | 2 |
| `MEM_5517` | `5517B` | `src/LO_SYN.mad:323` | `src/LO_SYN.mad:1726`, `src/LO_SYN.mad:2810`, `src/LO_SYN.mad:3040`, `src/LO_SYN.mad:3043` | 4 |
| `EX20_47505` | `47505B` | `src/LO_SYN.mad:324` | `src/LO_SYN.mad:1732` | 1 |
| `ADRPTR_41501` | `41501B` | `src/LO_SYN.mad:325` | `src/LO_SYN.mad:1735` | 1 |
| `EX20_64505` | `64505B` | `src/LO_SYN.mad:326` | `src/LO_SYN.mad:1736`, `src/LO_SYN.mad:3185`, `src/LO_SYN.mad:3239`, `src/LO_SYN.mad:3280` | 4 |
| `EXT_20144` | `20144B` | `src/LO_SYN.mad:327` | `src/LO_SYN.mad:1748` | 1 |
| `ADRPTR_40560` | `40560B` | `src/LO_SYN.mad:328` | `src/LO_SYN.mad:1750` | 1 |
| `MEM_5117` | `5117B` | `src/LO_SYN.mad:329` | `src/LO_SYN.mad:1751` | 1 |
| `EX20_20151` | `20151B` | `src/LO_SYN.mad:330` | `src/LO_SYN.mad:1753` | 1 |
| `EX62_40` | `40B` | `src/LO_SYN.mad:331` | `src/LO_SYN.mad:1756` | 1 |
| `EXT_20147` | `20147B` | `src/LO_SYN.mad:332` | `src/LO_SYN.mad:1772` | 1 |
| `ADRPTR_61440` | `61440B` | `src/LO_SYN.mad:333` | `src/LO_SYN.mad:1775` | 1 |
| `EX20_44144` | `44144B` | `src/LO_SYN.mad:334` | `src/LO_SYN.mad:1777` | 1 |
| `EXT_70505` | `70505B` | `src/LO_SYN.mad:335` | `src/LO_SYN.mad:1798` | 1 |
| `MEM_71561` | `71561B` | `src/LO_SYN.mad:336` | `src/LO_SYN.mad:1799` | 1 |
| `REGVAL_70514` | `70514B` | `src/LO_SYN.mad:337` | `src/LO_SYN.mad:1810` | 1 |
| `MEM_6161` | `6161B` | `src/LO_SYN.mad:338` | `src/LO_SYN.mad:1813` | 1 |
| `MODVAL_70103` | `70103B` | `src/LO_SYN.mad:339` | `src/LO_SYN.mad:1816`, `src/LO_SYN.mad:1966` | 2 |
| `MEM_4510` | `4510B` | `src/LO_SYN.mad:340` | `src/LO_SYN.mad:1817`, `src/LO_SYN.mad:1982`, `src/LO_SYN.mad:2090`, `src/LO_SYN.mad:2134`, `src/LO_SYN.mad:2404`, `src/LO_SYN.mad:3241` … (+1) | 7 |
| `MEM_566` | `566B` | `src/LO_SYN.mad:341` | `src/LO_SYN.mad:1822`, `src/LO_SYN.mad:1987`, `src/LO_SYN.mad:2062` | 3 |
| `REGVAL_70110` | `70110B` | `src/LO_SYN.mad:342` | `src/LO_SYN.mad:1828`, `src/LO_SYN.mad:1873`, `src/LO_SYN.mad:2210` | 3 |
| `MEM_71517` | `71517B` | `src/LO_SYN.mad:343` | `src/LO_SYN.mad:1829`, `src/LO_SYN.mad:2756`, `src/LO_SYN.mad:2777` | 3 |
| `EXT_47554` | `47554B` | `src/LO_SYN.mad:344` | `src/LO_SYN.mad:1834`, `src/LO_SYN.mad:1990`, `src/LO_SYN.mad:2456`, `src/LO_SYN.mad:2926`, `src/LO_SYN.mad:3025` | 5 |
| `ADRPTR_77040` | `77040B` | `src/LO_SYN.mad:345` | `src/LO_SYN.mad:1835`, `src/LO_SYN.mad:1991`, `src/LO_SYN.mad:2200`, `src/LO_SYN.mad:2221`, `src/LO_SYN.mad:2458`, `src/LO_SYN.mad:2927` … (+1) | 7 |
| `MODVAL_70040` | `70040B` | `src/LO_SYN.mad:346` | `src/LO_SYN.mad:1846`, `src/LO_SYN.mad:1888`, `src/LO_SYN.mad:1943`, `src/LO_SYN.mad:2434`, `src/LO_SYN.mad:2536`, `src/LO_SYN.mad:2740` … (+1) | 7 |
| `REGVAL_70160` | `70160B` | `src/LO_SYN.mad:347` | `src/LO_SYN.mad:1852`, `src/LO_SYN.mad:1894` | 2 |
| `MEM_76440` | `76440B` | `src/LO_SYN.mad:348` | `src/LO_SYN.mad:1856`, `src/LO_SYN.mad:1925`, `src/LO_SYN.mad:1964`, `src/LO_SYN.mad:2027`, `src/LO_SYN.mad:2300`, `src/LO_SYN.mad:2318` … (+1) | 7 |
| `MODVAL_70151` | `70151B` | `src/LO_SYN.mad:349` | `src/LO_SYN.mad:1858`, `src/LO_SYN.mad:2128` | 2 |
| `EX62_102` | `102B` | `src/LO_SYN.mad:350` | `src/LO_SYN.mad:1861`, `src/LO_SYN.mad:1970` | 2 |
| `EX36_44101` | `44101B` | `src/LO_SYN.mad:351` | `src/LO_SYN.mad:1867` | 1 |
| `MEM_72117` | `72117B` | `src/LO_SYN.mad:352` | `src/LO_SYN.mad:1874` | 1 |
| `MEM_74515` | `74515B` | `src/LO_SYN.mad:353` | `src/LO_SYN.mad:1877` | 1 |
| `MEM_4560` | `4560B` | `src/LO_SYN.mad:354` | `src/LO_SYN.mad:1879` | 1 |
| `EX36_52120` | `52120B` | `src/LO_SYN.mad:355` | `src/LO_SYN.mad:1880` | 1 |
| `MEM_74110` | `74110B` | `src/LO_SYN.mad:356` | `src/LO_SYN.mad:1885` | 1 |
| `EX36_65040` | `65040B` | `src/LO_SYN.mad:357` | `src/LO_SYN.mad:1886`, `src/LO_SYN.mad:2432`, `src/LO_SYN.mad:3193` | 3 |
| `MEM_5110` | `5110B` | `src/LO_SYN.mad:358` | `src/LO_SYN.mad:1898`, `src/LO_SYN.mad:2377` | 2 |
| `MEM_503` | `503B` | `src/LO_SYN.mad:359` | `src/LO_SYN.mad:1903` | 1 |
| `EXT_64520` | `64520B` | `src/LO_SYN.mad:360` | `src/LO_SYN.mad:1904` | 1 |
| `EXT_46517` | `46517B` | `src/LO_SYN.mad:361` | `src/LO_SYN.mad:1909` | 1 |
| `MODVAL_70102` | `70102B` | `src/LO_SYN.mad:362` | `src/LO_SYN.mad:1912`, `src/LO_SYN.mad:2059`, `src/LO_SYN.mad:2089`, `src/LO_SYN.mad:3248` | 4 |
| `EX65_2117` | `2117B` | `src/LO_SYN.mad:363` | `src/LO_SYN.mad:1919` | 1 |
| `MEM_7510` | `7510B` | `src/LO_SYN.mad:364` | `src/LO_SYN.mad:1921` | 1 |
| `MODVAL_70160` | `70160B` | `src/LO_SYN.mad:365` | `src/LO_SYN.mad:1927`, `src/LO_SYN.mad:2344` | 2 |
| `EX36_41124` | `41124B` | `src/LO_SYN.mad:366` | `src/LO_SYN.mad:1928`, `src/LO_SYN.mad:2345` | 2 |
| `EX36_50110` | `50110B` | `src/LO_SYN.mad:367` | `src/LO_SYN.mad:1930`, `src/LO_SYN.mad:2347` | 2 |
| `EX36_20102` | `20102B` | `src/LO_SYN.mad:368` | `src/LO_SYN.mad:1931` | 1 |
| `REGVAL_2544` | `2544B` | `src/LO_SYN.mad:369` | `src/LO_SYN.mad:1933` | 1 |
| `MEM_74101` | `74101B` | `src/LO_SYN.mad:370` | `src/LO_SYN.mad:1934` | 1 |
| `EX36_51105` | `51105B` | `src/LO_SYN.mad:371` | `src/LO_SYN.mad:1940` | 1 |
| `EX64_7522` | `7522B` | `src/LO_SYN.mad:372` | `src/LO_SYN.mad:1942` | 1 |
| `EX47_4520` | `4520B` | `src/LO_SYN.mad:373` | `src/LO_SYN.mad:1955`, `src/LO_SYN.mad:1996`, `src/LO_SYN.mad:2137`, `src/LO_SYN.mad:2201`, `src/LO_SYN.mad:2369`, `src/LO_SYN.mad:2588` … (+2) | 8 |
| `MEM_3040` | `3040B` | `src/LO_SYN.mad:374` | `src/LO_SYN.mad:1957`, `src/LO_SYN.mad:1997`, `src/LO_SYN.mad:2138`, `src/LO_SYN.mad:2203`, `src/LO_SYN.mad:2371`, `src/LO_SYN.mad:2624` … (+1) | 7 |
| `MODVAL_151` | `151B` | `src/LO_SYN.mad:375` | `src/LO_SYN.mad:1967` | 1 |
| `ADRPTR_50101` | `50101B` | `src/LO_SYN.mad:376` | `src/LO_SYN.mad:1972`, `src/LO_SYN.mad:2950`, `src/LO_SYN.mad:2984` | 3 |
| `REGVAL_70040` | `70040B` | `src/LO_SYN.mad:377` | `src/LO_SYN.mad:1973`, `src/LO_SYN.mad:3275` | 2 |
| `EX67_151` | `151B` | `src/LO_SYN.mad:378` | `src/LO_SYN.mad:1979`, `src/LO_SYN.mad:2441`, `src/LO_SYN.mad:2557`, `src/LO_SYN.mad:2576`, `src/LO_SYN.mad:2795`, `src/LO_SYN.mad:2807` | 6 |
| `EX64_5505` | `5505B` | `src/LO_SYN.mad:379` | `src/LO_SYN.mad:1981`, `src/LO_SYN.mad:2443`, `src/LO_SYN.mad:2578`, `src/LO_SYN.mad:2797`, `src/LO_SYN.mad:2809` | 5 |
| `EX64_7517` | `7517B` | `src/LO_SYN.mad:380` | `src/LO_SYN.mad:2000` | 1 |
| `MEM_71105` | `71105B` | `src/LO_SYN.mad:381` | `src/LO_SYN.mad:2002` | 1 |
| `MODVAL_70120` | `70120B` | `src/LO_SYN.mad:382` | `src/LO_SYN.mad:2003`, `src/LO_SYN.mad:2029` | 2 |
| `MEM_5115` | `5115B` | `src/LO_SYN.mad:383` | `src/LO_SYN.mad:2005` | 1 |
| `MEM_70110` | `70110B` | `src/LO_SYN.mad:384` | `src/LO_SYN.mad:2006`, `src/LO_SYN.mad:2968`, `src/LO_SYN.mad:3022`, `src/LO_SYN.mad:3179`, `src/LO_SYN.mad:3200`, `src/LO_SYN.mad:3233` | 6 |
| `EX36_41524` | `41524B` | `src/LO_SYN.mad:385` | `src/LO_SYN.mad:2008`, `src/LO_SYN.mad:3056` | 2 |
| `ADRPTR_20115` | `20115B` | `src/LO_SYN.mad:386` | `src/LO_SYN.mad:2009` | 1 |
| `MEM_1503` | `1503B` | `src/LO_SYN.mad:387` | `src/LO_SYN.mad:2011` | 1 |
| `ADRPTR_41101` | `41101B` | `src/LO_SYN.mad:388` | `src/LO_SYN.mad:2012` | 1 |
| `EX36_70105` | `70105B` | `src/LO_SYN.mad:389` | `src/LO_SYN.mad:2018`, `src/LO_SYN.mad:2075` | 2 |
| `MEM_524` | `524B` | `src/LO_SYN.mad:390` | `src/LO_SYN.mad:2020`, `src/LO_SYN.mad:2167` | 2 |
| `EXT_63131` | `63131B` | `src/LO_SYN.mad:391` | `src/LO_SYN.mad:2021` | 1 |
| `EX20_45543` | `45543B` | `src/LO_SYN.mad:392` | `src/LO_SYN.mad:2023` | 1 |
| `EX67_117` | `117B` | `src/LO_SYN.mad:393` | `src/LO_SYN.mad:2033`, `src/LO_SYN.mad:2350` | 2 |
| `EXT_74172` | `74172B` | `src/LO_SYN.mad:394` | `src/LO_SYN.mad:2035`, `src/LO_SYN.mad:2351` | 2 |
| `MEM_1523` | `1523B` | `src/LO_SYN.mad:395` | `src/LO_SYN.mad:2038`, `src/LO_SYN.mad:2480`, `src/LO_SYN.mad:2516` | 3 |
| `ADRPTR_43516` | `43516B` | `src/LO_SYN.mad:396` | `src/LO_SYN.mad:2039`, `src/LO_SYN.mad:2482`, `src/LO_SYN.mad:2518` | 3 |
| `MEM_74510` | `74510B` | `src/LO_SYN.mad:397` | `src/LO_SYN.mad:2041` | 1 |
| `EXT_61440` | `61440B` | `src/LO_SYN.mad:398` | `src/LO_SYN.mad:2042` | 1 |
| `MEM_75040` | `75040B` | `src/LO_SYN.mad:399` | `src/LO_SYN.mad:2045` | 1 |
| `MEM_147` | `147B` | `src/LO_SYN.mad:400` | `src/LO_SYN.mad:2047`, `src/LO_SYN.mad:2459` | 2 |
| `EXT_62101` | `62101B` | `src/LO_SYN.mad:401` | `src/LO_SYN.mad:2068` | 1 |
| `MEM_543` | `543B` | `src/LO_SYN.mad:402` | `src/LO_SYN.mad:2077` | 1 |
| `EX65_2120` | `2120B` | `src/LO_SYN.mad:403` | `src/LO_SYN.mad:2092`, `src/LO_SYN.mad:2405`, `src/LO_SYN.mad:2521`, `src/LO_SYN.mad:3205`, `src/LO_SYN.mad:3242`, `src/LO_SYN.mad:3305` | 6 |
| `ADRPTR_45440` | `45440B` | `src/LO_SYN.mad:404` | `src/LO_SYN.mad:2093`, `src/LO_SYN.mad:2407`, `src/LO_SYN.mad:2522` | 3 |
| `EX64_1101` | `1101B` | `src/LO_SYN.mad:405` | `src/LO_SYN.mad:2096`, `src/LO_SYN.mad:2117` | 2 |
| `ADRPTR_41040` | `41040B` | `src/LO_SYN.mad:406` | `src/LO_SYN.mad:2098`, `src/LO_SYN.mad:2119` | 2 |
| `ADRPTR_44103` | `44103B` | `src/LO_SYN.mad:407` | `src/LO_SYN.mad:2105`, `src/LO_SYN.mad:2206`, `src/LO_SYN.mad:2465`, `src/LO_SYN.mad:3107` | 4 |
| `MEM_70131` | `70131B` | `src/LO_SYN.mad:408` | `src/LO_SYN.mad:2107`, `src/LO_SYN.mad:2207`, `src/LO_SYN.mad:2467`, `src/LO_SYN.mad:3109`, `src/LO_SYN.mad:3268` | 5 |
| `EXT_20160` | `20160B` | `src/LO_SYN.mad:409` | `src/LO_SYN.mad:2108`, `src/LO_SYN.mad:2567`, `src/LO_SYN.mad:2887`, `src/LO_SYN.mad:2942`, `src/LO_SYN.mad:3136` | 5 |
| `REGVAL_551` | `551B` | `src/LO_SYN.mad:410` | `src/LO_SYN.mad:2111` | 1 |
| `REGVAL_40` | `40B` | `src/LO_SYN.mad:411` | `src/LO_SYN.mad:2113`, `src/LO_SYN.mad:2561`, `src/LO_SYN.mad:2581`, `src/LO_SYN.mad:3298` | 4 |
| `MEM_76505` | `76505B` | `src/LO_SYN.mad:412` | `src/LO_SYN.mad:2122`, `src/LO_SYN.mad:2357`, `src/LO_SYN.mad:2381`, `src/LO_SYN.mad:2507`, `src/LO_SYN.mad:2852`, `src/LO_SYN.mad:3029` | 6 |
| `EX20_20143` | `20143B` | `src/LO_SYN.mad:413` | `src/LO_SYN.mad:2123`, `src/LO_SYN.mad:2359`, `src/LO_SYN.mad:2383` | 3 |
| `ADRPTR_45554` | `45554B` | `src/LO_SYN.mad:414` | `src/LO_SYN.mad:2125`, `src/LO_SYN.mad:2360`, `src/LO_SYN.mad:2384`, `src/LO_SYN.mad:2860` | 4 |
| `EX65_70101` | `70101B` | `src/LO_SYN.mad:415` | `src/LO_SYN.mad:2131`, `src/LO_SYN.mad:2824` | 2 |
| `EX20_64543` | `64543B` | `src/LO_SYN.mad:416` | `src/LO_SYN.mad:2132`, `src/LO_SYN.mad:2825` | 2 |
| `EXT_40530` | `40530B` | `src/LO_SYN.mad:417` | `src/LO_SYN.mad:2149` | 1 |
| `MODVAL_70110` | `70110B` | `src/LO_SYN.mad:418` | `src/LO_SYN.mad:2152` | 1 |
| `EX62_6552` | `6552B` | `src/LO_SYN.mad:419` | `src/LO_SYN.mad:2161` | 1 |
| `MEM_6505` | `6505B` | `src/LO_SYN.mad:420` | `src/LO_SYN.mad:2162`, `src/LO_SYN.mad:2485`, `src/LO_SYN.mad:2596`, `src/LO_SYN.mad:3184` | 4 |
| `MEM_75551` | `75551B` | `src/LO_SYN.mad:421` | `src/LO_SYN.mad:2164` | 1 |
| `EX36_45440` | `45440B` | `src/LO_SYN.mad:422` | `src/LO_SYN.mad:2171` | 1 |
| `EX20_75505` | `75505B` | `src/LO_SYN.mad:423` | `src/LO_SYN.mad:2174` | 1 |
| `MEM_1455` | `1455B` | `src/LO_SYN.mad:424` | `src/LO_SYN.mad:2176` | 1 |
| `MEM_77440` | `77440B` | `src/LO_SYN.mad:425` | `src/LO_SYN.mad:2179`, `src/LO_SYN.mad:2260`, `src/LO_SYN.mad:2498`, `src/LO_SYN.mad:2503` | 4 |
| `EX47_4524` | `4524B` | `src/LO_SYN.mad:426` | `src/LO_SYN.mad:2185`, `src/LO_SYN.mad:2273`, `src/LO_SYN.mad:2309`, `src/LO_SYN.mad:2327`, `src/LO_SYN.mad:2866` | 5 |
| `EX20_20102` | `20102B` | `src/LO_SYN.mad:427` | `src/LO_SYN.mad:2186`, `src/LO_SYN.mad:3031` | 2 |
| `MEM_6117` | `6117B` | `src/LO_SYN.mad:428` | `src/LO_SYN.mad:2188` | 1 |
| `EX66_74576` | `74576B` | `src/LO_SYN.mad:429` | `src/LO_SYN.mad:2189` | 1 |
| `MEM_4506` | `4506B` | `src/LO_SYN.mad:430` | `src/LO_SYN.mad:2191`, `src/LO_SYN.mad:3287` | 2 |
| `EXT_47547` | `47547B` | `src/LO_SYN.mad:431` | `src/LO_SYN.mad:2198`, `src/LO_SYN.mad:2219` | 2 |
| `EXT_20111` | `20111B` | `src/LO_SYN.mad:432` | `src/LO_SYN.mad:2209` | 1 |
| `EX36_73105` | `73105B` | `src/LO_SYN.mad:433` | `src/LO_SYN.mad:2213`, `src/LO_SYN.mad:3283` | 2 |
| `ADRPTR_43040` | `43040B` | `src/LO_SYN.mad:434` | `src/LO_SYN.mad:2222`, `src/LO_SYN.mad:3212`, `src/LO_SYN.mad:3263` | 3 |
| `EX64_77524` | `77524B` | `src/LO_SYN.mad:435` | `src/LO_SYN.mad:2228`, `src/LO_SYN.mad:2252` | 2 |
| `ADRPTR_41554` | `41554B` | `src/LO_SYN.mad:436` | `src/LO_SYN.mad:2248` | 1 |
| `MODVAL_70144` | `70144B` | `src/LO_SYN.mad:437` | `src/LO_SYN.mad:2269`, `src/LO_SYN.mad:2305`, `src/LO_SYN.mad:2323`, `src/LO_SYN.mad:2452` | 4 |
| `EX36_66166` | `66166B` | `src/LO_SYN.mad:438` | `src/LO_SYN.mad:2270`, `src/LO_SYN.mad:2306`, `src/LO_SYN.mad:2324`, `src/LO_SYN.mad:2863`, `src/LO_SYN.mad:3089` | 5 |
| `EX20_40440` | `40440B` | `src/LO_SYN.mad:439` | `src/LO_SYN.mad:2272`, `src/LO_SYN.mad:2308`, `src/LO_SYN.mad:2326`, `src/LO_SYN.mad:2449`, `src/LO_SYN.mad:2864` | 5 |
| `EX20_20117` | `20117B` | `src/LO_SYN.mad:440` | `src/LO_SYN.mad:2275`, `src/LO_SYN.mad:3115` | 2 |
| `EX20_64566` | `64566B` | `src/LO_SYN.mad:441` | `src/LO_SYN.mad:2281` | 1 |
| `EX66_4513` | `4513B` | `src/LO_SYN.mad:442` | `src/LO_SYN.mad:2294`, `src/LO_SYN.mad:2302`, `src/LO_SYN.mad:2320`, `src/LO_SYN.mad:2644`, `src/LO_SYN.mad:3251` | 5 |
| `EX20_20103` | `20103B` | `src/LO_SYN.mad:443` | `src/LO_SYN.mad:2311`, `src/LO_SYN.mad:2867` | 2 |
| `EX20_20124` | `20124B` | `src/LO_SYN.mad:444` | `src/LO_SYN.mad:2329` | 1 |
| `ADRPTR_70101` | `70101B` | `src/LO_SYN.mad:445` | `src/LO_SYN.mad:2330` | 1 |
| `MEM_4516` | `4516B` | `src/LO_SYN.mad:446` | `src/LO_SYN.mad:2332` | 1 |
| `MEM_72507` | `72507B` | `src/LO_SYN.mad:447` | `src/LO_SYN.mad:2333` | 1 |
| `MEM_1105` | `1105B` | `src/LO_SYN.mad:448` | `src/LO_SYN.mad:2338` | 1 |
| `MEM_6040` | `6040B` | `src/LO_SYN.mad:449` | `src/LO_SYN.mad:2339` | 1 |
| `MEM_77110` | `77110B` | `src/LO_SYN.mad:450` | `src/LO_SYN.mad:2374`, `src/LO_SYN.mad:2882` | 2 |
| `EX36_63517` | `63517B` | `src/LO_SYN.mad:451` | `src/LO_SYN.mad:2375`, `src/LO_SYN.mad:2921`, `src/LO_SYN.mad:2998`, `src/LO_SYN.mad:3008` | 4 |
| `MEM_7040` | `7040B` | `src/LO_SYN.mad:452` | `src/LO_SYN.mad:2378` | 1 |
| `REGVAL_40547` | `40547B` | `src/LO_SYN.mad:453` | `src/LO_SYN.mad:2393` | 1 |
| `EX36_66117` | `66117B` | `src/LO_SYN.mad:454` | `src/LO_SYN.mad:2395` | 1 |
| `REGVAL_5505` | `5505B` | `src/LO_SYN.mad:455` | `src/LO_SYN.mad:2396` | 1 |
| `MEM_70510` | `70510B` | `src/LO_SYN.mad:456` | `src/LO_SYN.mad:2401` | 1 |
| `MEM_2170` | `2170B` | `src/LO_SYN.mad:457` | `src/LO_SYN.mad:2416`, `src/LO_SYN.mad:3095` | 2 |
| `EXT_66040` | `66040B` | `src/LO_SYN.mad:458` | `src/LO_SYN.mad:2419`, `src/LO_SYN.mad:2428` | 2 |
| `MEM_4524` | `4524B` | `src/LO_SYN.mad:459` | `src/LO_SYN.mad:2425` | 1 |
| `EX62_115` | `115B` | `src/LO_SYN.mad:460` | `src/LO_SYN.mad:2429` | 1 |
| `EX62_70040` | `70040B` | `src/LO_SYN.mad:461` | `src/LO_SYN.mad:2446` | 1 |
| `MEM_4547` | `4547B` | `src/LO_SYN.mad:462` | `src/LO_SYN.mad:2453` | 1 |
| `MEM_6114` | `6114B` | `src/LO_SYN.mad:463` | `src/LO_SYN.mad:2470` | 1 |
| `REGVAL_40440` | `40440B` | `src/LO_SYN.mad:464` | `src/LO_SYN.mad:2479`, `src/LO_SYN.mad:3175` | 2 |
| `MEM_75501` | `75501B` | `src/LO_SYN.mad:465` | `src/LO_SYN.mad:2486` | 1 |
| `EXT_64510` | `64510B` | `src/LO_SYN.mad:466` | `src/LO_SYN.mad:2519` | 1 |
| `EXT_66105` | `66105B` | `src/LO_SYN.mad:467` | `src/LO_SYN.mad:2552` | 1 |
| `EX64_5501` | `5501B` | `src/LO_SYN.mad:468` | `src/LO_SYN.mad:2558` | 1 |
| `MEM_1057` | `1057B` | `src/LO_SYN.mad:469` | `src/LO_SYN.mad:2560`, `src/LO_SYN.mad:2579` | 2 |
| `MEM_3054` | `3054B` | `src/LO_SYN.mad:470` | `src/LO_SYN.mad:2590` | 1 |
| `MEM_76161` | `76161B` | `src/LO_SYN.mad:471` | `src/LO_SYN.mad:2594` | 1 |
| `EXT_20173` | `20173B` | `src/LO_SYN.mad:472` | `src/LO_SYN.mad:2597` | 1 |
| `MEM_3440` | `3440B` | `src/LO_SYN.mad:473` | `src/LO_SYN.mad:2599` | 1 |
| `REGVAL_7502` | `7502B` | `src/LO_SYN.mad:474` | `src/LO_SYN.mad:2605` | 1 |
| `REGVAL_1117` | `1117B` | `src/LO_SYN.mad:475` | `src/LO_SYN.mad:2612`, `src/LO_SYN.mad:2630`, `src/LO_SYN.mad:2651` | 3 |
| `EX36_61154` | `61154B` | `src/LO_SYN.mad:476` | `src/LO_SYN.mad:2671` | 1 |
| `MEM_2120` | `2120B` | `src/LO_SYN.mad:477` | `src/LO_SYN.mad:2672` | 1 |
| `EXT_50101` | `50101B` | `src/LO_SYN.mad:478` | `src/LO_SYN.mad:2674` | 1 |
| `REGVAL_20117` | `20117B` | `src/LO_SYN.mad:479` | `src/LO_SYN.mad:2675` | 1 |
| `MEM_74524` | `74524B` | `src/LO_SYN.mad:480` | `src/LO_SYN.mad:2678` | 1 |
| `MEM_71570` | `71570B` | `src/LO_SYN.mad:481` | `src/LO_SYN.mad:2680` | 1 |
| `MEM_1124` | `1124B` | `src/LO_SYN.mad:482` | `src/LO_SYN.mad:2683` | 1 |
| `EX36_50101` | `50101B` | `src/LO_SYN.mad:483` | `src/LO_SYN.mad:2684` | 1 |
| `MODVAL_6520` | `6520B` | `src/LO_SYN.mad:484` | `src/LO_SYN.mad:2687` | 1 |
| `MEM_4151` | `4151B` | `src/LO_SYN.mad:485` | `src/LO_SYN.mad:2698` | 1 |
| `ADRPTR_20110` | `20110B` | `src/LO_SYN.mad:486` | `src/LO_SYN.mad:2699`, `src/LO_SYN.mad:3086` | 2 |
| `MODVAL_6502` | `6502B` | `src/LO_SYN.mad:487` | `src/LO_SYN.mad:2704` | 1 |
| `EX20_47515` | `47515B` | `src/LO_SYN.mad:488` | `src/LO_SYN.mad:2710` | 1 |
| `MEM_70055` | `70055B` | `src/LO_SYN.mad:489` | `src/LO_SYN.mad:2713` | 1 |
| `EX64_1571` | `1571B` | `src/LO_SYN.mad:490` | `src/LO_SYN.mad:2732` | 1 |
| `EXT_45505` | `45505B` | `src/LO_SYN.mad:491` | `src/LO_SYN.mad:2734` | 1 |
| `MEM_4101` | `4101B` | `src/LO_SYN.mad:492` | `src/LO_SYN.mad:2735` | 1 |
| `EX64_7504` | `7504B` | `src/LO_SYN.mad:493` | `src/LO_SYN.mad:2753`, `src/LO_SYN.mad:2774` | 2 |
| `MEM_76104` | `76104B` | `src/LO_SYN.mad:494` | `src/LO_SYN.mad:2755`, `src/LO_SYN.mad:2776` | 2 |
| `ADRPTR_45501` | `45501B` | `src/LO_SYN.mad:495` | `src/LO_SYN.mad:2765` | 1 |
| `REGVAL_40510` | `40510B` | `src/LO_SYN.mad:496` | `src/LO_SYN.mad:2767` | 1 |
| `ADRPTR_64440` | `64440B` | `src/LO_SYN.mad:497` | `src/LO_SYN.mad:2768`, `src/LO_SYN.mad:3245` | 2 |
| `MEM_4546` | `4546B` | `src/LO_SYN.mad:498` | `src/LO_SYN.mad:2770` | 1 |
| `MEM_70101` | `70101B` | `src/LO_SYN.mad:499` | `src/LO_SYN.mad:2771` | 1 |
| `MEM_70524` | `70524B` | `src/LO_SYN.mad:500` | `src/LO_SYN.mad:2819`, `src/LO_SYN.mad:2840`, `src/LO_SYN.mad:2896` | 3 |
| `EX62_160` | `160B` | `src/LO_SYN.mad:501` | `src/LO_SYN.mad:2834` | 1 |
| `MEM_110` | `110B` | `src/LO_SYN.mad:502` | `src/LO_SYN.mad:2842`, `src/LO_SYN.mad:2897`, `src/LO_SYN.mad:2969` | 3 |
| `REGVAL_41105` | `41105B` | `src/LO_SYN.mad:503` | `src/LO_SYN.mad:2845` | 1 |
| `EX65_2110` | `2110B` | `src/LO_SYN.mad:504` | `src/LO_SYN.mad:2846` | 1 |
| `EX20_20110` | `20110B` | `src/LO_SYN.mad:505` | `src/LO_SYN.mad:2854` | 1 |
| `MEM_70502` | `70502B` | `src/LO_SYN.mad:506` | `src/LO_SYN.mad:2855` | 1 |
| `EX20_47547` | `47547B` | `src/LO_SYN.mad:507` | `src/LO_SYN.mad:2857` | 1 |
| `MEM_144` | `144B` | `src/LO_SYN.mad:508` | `src/LO_SYN.mad:2861` | 1 |
| `EXT_20143` | `20143B` | `src/LO_SYN.mad:509` | `src/LO_SYN.mad:2872` | 1 |
| `EX64_77440` | `77440B` | `src/LO_SYN.mad:510` | `src/LO_SYN.mad:2875`, `src/LO_SYN.mad:3221` | 2 |
| `REGVAL_44101` | `44101B` | `src/LO_SYN.mad:511` | `src/LO_SYN.mad:2885`, `src/LO_SYN.mad:2947` | 2 |
| `MEM_74117` | `74117B` | `src/LO_SYN.mad:512` | `src/LO_SYN.mad:2903` | 1 |
| `REGVAL_172` | `172B` | `src/LO_SYN.mad:513` | `src/LO_SYN.mad:2914` | 1 |
| `EX20_64551` | `64551B` | `src/LO_SYN.mad:514` | `src/LO_SYN.mad:2917` | 1 |
| `MEM_1110` | `1110B` | `src/LO_SYN.mad:515` | `src/LO_SYN.mad:2920`, `src/LO_SYN.mad:3007` | 2 |
| `REGVAL_104` | `104B` | `src/LO_SYN.mad:516` | `src/LO_SYN.mad:2932`, `src/LO_SYN.mad:2977`, `src/LO_SYN.mad:3067` | 3 |
| `MEM_71171` | `71171B` | `src/LO_SYN.mad:517` | `src/LO_SYN.mad:2936` | 1 |
| `EXT_40505` | `40505B` | `src/LO_SYN.mad:518` | `src/LO_SYN.mad:2938` | 1 |
| `MODVAL_70113` | `70113B` | `src/LO_SYN.mad:519` | `src/LO_SYN.mad:2939` | 1 |
| `EX36_66151` | `66151B` | `src/LO_SYN.mad:520` | `src/LO_SYN.mad:2941` | 1 |
| `EXT_20102` | `20102B` | `src/LO_SYN.mad:521` | `src/LO_SYN.mad:2948` | 1 |
| `REGVAL_70102` | `70102B` | `src/LO_SYN.mad:522` | `src/LO_SYN.mad:2951`, `src/LO_SYN.mad:2986` | 2 |
| `EX36_70055` | `70055B` | `src/LO_SYN.mad:523` | `src/LO_SYN.mad:2980` | 1 |
| `MEM_74440` | `74440B` | `src/LO_SYN.mad:524` | `src/LO_SYN.mad:2981`, `src/LO_SYN.mad:3139` | 2 |
| `REGVAL_102` | `102B` | `src/LO_SYN.mad:525` | `src/LO_SYN.mad:2983`, `src/LO_SYN.mad:3315` | 2 |
| `EXT_40547` | `40547B` | `src/LO_SYN.mad:526` | `src/LO_SYN.mad:3004` | 1 |
| `EX20_20142` | `20142B` | `src/LO_SYN.mad:527` | `src/LO_SYN.mad:3016` | 1 |
| `ADRPTR_66161` | `66161B` | `src/LO_SYN.mad:528` | `src/LO_SYN.mad:3023` | 1 |
| `EX47_4573` | `4573B` | `src/LO_SYN.mad:529` | `src/LO_SYN.mad:3037` | 1 |
| `MEM_2524` | `2524B` | `src/LO_SYN.mad:530` | `src/LO_SYN.mad:3038`, `src/LO_SYN.mad:3074` | 2 |
| `EXT_64576` | `64576B` | `src/LO_SYN.mad:531` | `src/LO_SYN.mad:3041` | 1 |
| `EX66_6151` | `6151B` | `src/LO_SYN.mad:532` | `src/LO_SYN.mad:3046`, `src/LO_SYN.mad:3142` | 2 |
| `EXT_20142` | `20142B` | `src/LO_SYN.mad:533` | `src/LO_SYN.mad:3049`, `src/LO_SYN.mad:3145` | 2 |
| `EXT_40561` | `40561B` | `src/LO_SYN.mad:534` | `src/LO_SYN.mad:3052`, `src/LO_SYN.mad:3148`, `src/LO_SYN.mad:3172` | 3 |
| `MEM_5520` | `5520B` | `src/LO_SYN.mad:535` | `src/LO_SYN.mad:3053` | 1 |
| `EX20_20113` | `20113B` | `src/LO_SYN.mad:536` | `src/LO_SYN.mad:3058` | 1 |
| `EX36_44103` | `44103B` | `src/LO_SYN.mad:537` | `src/LO_SYN.mad:3059`, `src/LO_SYN.mad:3266` | 2 |
| `EXT_42575` | `42575B` | `src/LO_SYN.mad:538` | `src/LO_SYN.mad:3073` | 1 |
| `REGVAL_160` | `160B` | `src/LO_SYN.mad:539` | `src/LO_SYN.mad:3077` | 1 |
| `MEM_72513` | `72513B` | `src/LO_SYN.mad:540` | `src/LO_SYN.mad:3082` | 1 |
| `EXT_40520` | `40520B` | `src/LO_SYN.mad:541` | `src/LO_SYN.mad:3083` | 1 |
| `MEM_70144` | `70144B` | `src/LO_SYN.mad:542` | `src/LO_SYN.mad:3088` | 1 |
| `EX20_74440` | `74440B` | `src/LO_SYN.mad:543` | `src/LO_SYN.mad:3091` | 1 |
| `REGVAL_1524` | `1524B` | `src/LO_SYN.mad:544` | `src/LO_SYN.mad:3092` | 1 |
| `MEM_2576` | `2576B` | `src/LO_SYN.mad:545` | `src/LO_SYN.mad:3094` | 1 |
| `EX36_66110` | `66110B` | `src/LO_SYN.mad:546` | `src/LO_SYN.mad:3103` | 1 |
| `ADRPTR_54040` | `54040B` | `src/LO_SYN.mad:547` | `src/LO_SYN.mad:3106` | 1 |
| `ADRPTR_46505` | `46505B` | `src/LO_SYN.mad:548` | `src/LO_SYN.mad:3121`, `src/LO_SYN.mad:3169` | 2 |
| `EX20_64440` | `64440B` | `src/LO_SYN.mad:549` | `src/LO_SYN.mad:3122` | 1 |
| `MEM_55` | `55B` | `src/LO_SYN.mad:550` | `src/LO_SYN.mad:3124` | 1 |
| `EXT_74440` | `74440B` | `src/LO_SYN.mad:551` | `src/LO_SYN.mad:3125` | 1 |
| `MEM_6561` | `6561B` | `src/LO_SYN.mad:552` | `src/LO_SYN.mad:3137` | 1 |
| `MEM_2154` | `2154B` | `src/LO_SYN.mad:553` | `src/LO_SYN.mad:3149` | 1 |
| `ADRPTR_44101` | `44101B` | `src/LO_SYN.mad:554` | `src/LO_SYN.mad:3151` | 1 |
| `MEM_1111` | `1111B` | `src/LO_SYN.mad:555` | `src/LO_SYN.mad:3152` | 1 |
| `MODVAL_76543` | `76543B` | `src/LO_SYN.mad:556` | `src/LO_SYN.mad:3154` | 1 |
| `EXT_45551` | `45551B` | `src/LO_SYN.mad:557` | `src/LO_SYN.mad:3157` | 1 |
| `MEM_7544` | `7544B` | `src/LO_SYN.mad:558` | `src/LO_SYN.mad:3166` | 1 |
| `REGVAL_505` | `505B` | `src/LO_SYN.mad:559` | `src/LO_SYN.mad:3170` | 1 |
| `MEM_1101` | `1101B` | `src/LO_SYN.mad:560` | `src/LO_SYN.mad:3173` | 1 |
| `EX20_42502` | `42502B` | `src/LO_SYN.mad:561` | `src/LO_SYN.mad:3178`, `src/LO_SYN.mad:3199`, `src/LO_SYN.mad:3232` | 3 |
| `EX36_61120` | `61120B` | `src/LO_SYN.mad:562` | `src/LO_SYN.mad:3182` | 1 |
| `EX65_2101` | `2101B` | `src/LO_SYN.mad:563` | `src/LO_SYN.mad:3188` | 1 |
| `EX20_62101` | `62101B` | `src/LO_SYN.mad:564` | `src/LO_SYN.mad:3190` | 1 |
| `ADRPTR_45543` | `45543B` | `src/LO_SYN.mad:565` | `src/LO_SYN.mad:3206`, `src/LO_SYN.mad:3244` | 2 |
| `ADRPTR_70440` | `70440B` | `src/LO_SYN.mad:566` | `src/LO_SYN.mad:3208` | 1 |
| `ADRPTR_43055` | `43055B` | `src/LO_SYN.mad:567` | `src/LO_SYN.mad:3209` | 1 |
| `MEM_77104` | `77104B` | `src/LO_SYN.mad:568` | `src/LO_SYN.mad:3211`, `src/LO_SYN.mad:3262` | 2 |
| `MEM_74105` | `74105B` | `src/LO_SYN.mad:569` | `src/LO_SYN.mad:3217` | 1 |
| `EXT_20110` | `20110B` | `src/LO_SYN.mad:570` | `src/LO_SYN.mad:3218` | 1 |
| `ADRPTR_77105` | `77105B` | `src/LO_SYN.mad:571` | `src/LO_SYN.mad:3220` | 1 |
| `EX36_45517` | `45517B` | `src/LO_SYN.mad:572` | `src/LO_SYN.mad:3236` | 1 |
| `EX20_77101` | `77101B` | `src/LO_SYN.mad:573` | `src/LO_SYN.mad:3238` | 1 |
| `MEM_74111` | `74111B` | `src/LO_SYN.mad:574` | `src/LO_SYN.mad:3247` | 1 |
| `REGVAL_113` | `113B` | `src/LO_SYN.mad:575` | `src/LO_SYN.mad:3265` | 1 |
| `EXT_61551` | `61551B` | `src/LO_SYN.mad:576` | `src/LO_SYN.mad:3269` | 1 |
| `ADRPTR_20111` | `20111B` | `src/LO_SYN.mad:577` | `src/LO_SYN.mad:3271` | 1 |
| `REGVAL_76505` | `76505B` | `src/LO_SYN.mad:578` | `src/LO_SYN.mad:3272` | 1 |
| `EXT_42111` | `42111B` | `src/LO_SYN.mad:579` | `src/LO_SYN.mad:3274` | 1 |
| `EX20_40520` | `40520B` | `src/LO_SYN.mad:580` | `src/LO_SYN.mad:3277` | 1 |
| `ADRPTR_75505` | `75505B` | `src/LO_SYN.mad:581` | `src/LO_SYN.mad:3278` | 1 |
| `EX20_44117` | `44117B` | `src/LO_SYN.mad:582` | `src/LO_SYN.mad:3284` | 1 |
| `EXT_42516` | `42516B` | `src/LO_SYN.mad:583` | `src/LO_SYN.mad:3289` | 1 |
| `MEM_74506` | `74506B` | `src/LO_SYN.mad:584` | `src/LO_SYN.mad:3290` | 1 |
| `MEM_4457` | `4457B` | `src/LO_SYN.mad:585` | `src/LO_SYN.mad:3292` | 1 |
| `EXT_66117` | `66117B` | `src/LO_SYN.mad:586` | `src/LO_SYN.mad:3296` | 1 |
| `MEM_70561` | `70561B` | `src/LO_SYN.mad:587` | `src/LO_SYN.mad:3302` | 1 |
| `SVCELL_400` | `400B` | `src/LO_SYN.mad:588` | `src/LO_SYN.mad:3311`, `src/LO_SYN.mad:3320`, `src/LO_SYN.mad:3323`, `src/LO_SYN.mad:3326`, `src/LO_SYN.mad:3335`, `src/LO_SYN.mad:3347` … (+32) | 38 |
| `SVCELL_101` | `101B` | `src/LO_SYN.mad:589` | `src/LO_SYN.mad:3312` | 1 |
| `SVCELL_500` | `500B` | `src/LO_SYN.mad:590` | `src/LO_SYN.mad:3314`, `src/LO_SYN.mad:3317`, `src/LO_SYN.mad:3332`, `src/LO_SYN.mad:3341`, `src/LO_SYN.mad:3353`, `src/LO_SYN.mad:3356` … (+30) | 36 |
| `MEM_70311` | `70311B` | `src/LO_SYN.mad:591` | `src/LO_SYN.mad:3318` | 1 |
| `EX60_70312` | `70312B` | `src/LO_SYN.mad:592` | `src/LO_SYN.mad:3321` | 1 |
| `EX60_70313` | `70313B` | `src/LO_SYN.mad:593` | `src/LO_SYN.mad:3324` | 1 |
| `ADRPTR_314` | `314B` | `src/LO_SYN.mad:594` | `src/LO_SYN.mad:3327` | 1 |
| `SVCELL_300` | `300B` | `src/LO_SYN.mad:595` | `src/LO_SYN.mad:3329`, `src/LO_SYN.mad:3338`, `src/LO_SYN.mad:3344`, `src/LO_SYN.mad:3350`, `src/LO_SYN.mad:3371`, `src/LO_SYN.mad:3374` … (+21) | 27 |
| `EX36_317` | `317B` | `src/LO_SYN.mad:596` | `src/LO_SYN.mad:3336` | 1 |
| `SVCELL_322` | `322B` | `src/LO_SYN.mad:597` | `src/LO_SYN.mad:3339` | 1 |
| `EX50_323` | `323B` | `src/LO_SYN.mad:598` | `src/LO_SYN.mad:3342` | 1 |
| `SVCELL_70324` | `70324B` | `src/LO_SYN.mad:599` | `src/LO_SYN.mad:3345` | 1 |
| `EX50_70325` | `70325B` | `src/LO_SYN.mad:600` | `src/LO_SYN.mad:3348` | 1 |
| `EX21_326` | `326B` | `src/LO_SYN.mad:601` | `src/LO_SYN.mad:3351` | 1 |
| `REGVAL_327` | `327B` | `src/LO_SYN.mad:602` | `src/LO_SYN.mad:3354` | 1 |
| `SVCELL_600` | `600B` | `src/LO_SYN.mad:603` | `src/LO_SYN.mad:3359`, `src/LO_SYN.mad:3413`, `src/LO_SYN.mad:3440`, `src/LO_SYN.mad:3554`, `src/LO_SYN.mad:3578`, `src/LO_SYN.mad:3671` … (+2) | 8 |
| `EX36_501` | `501B` | `src/LO_SYN.mad:604` | `src/LO_SYN.mad:3360` | 1 |
| `REGVAL_502` | `502B` | `src/LO_SYN.mad:605` | `src/LO_SYN.mad:3363` | 1 |
| `SVCELL_70503` | `70503B` | `src/LO_SYN.mad:606` | `src/LO_SYN.mad:3366` | 1 |
| `EX50_70504` | `70504B` | `src/LO_SYN.mad:607` | `src/LO_SYN.mad:3369` | 1 |
| `ADRPTR_505` | `505B` | `src/LO_SYN.mad:608` | `src/LO_SYN.mad:3372` | 1 |
| `REGVAL_506` | `506B` | `src/LO_SYN.mad:609` | `src/LO_SYN.mad:3375` | 1 |
| `SVCELL_700` | `700B` | `src/LO_SYN.mad:610` | `src/LO_SYN.mad:3377`, `src/LO_SYN.mad:3383`, `src/LO_SYN.mad:3395`, `src/LO_SYN.mad:3428`, `src/LO_SYN.mad:3500`, `src/LO_SYN.mad:3521` … (+9) | 15 |
| `REGVAL_510` | `510B` | `src/LO_SYN.mad:611` | `src/LO_SYN.mad:3381` | 1 |
| `EX60_512` | `512B` | `src/LO_SYN.mad:612` | `src/LO_SYN.mad:3387` | 1 |
| `EXT_70513` | `70513B` | `src/LO_SYN.mad:613` | `src/LO_SYN.mad:3390` | 1 |
| `EX60_514` | `514B` | `src/LO_SYN.mad:614` | `src/LO_SYN.mad:3393` | 1 |
| `EX70_71000` | `71000B` | `src/LO_SYN.mad:615` | `src/LO_SYN.mad:3396` | 1 |
| `REGVAL_1002` | `1002B` | `src/LO_SYN.mad:616` | `src/LO_SYN.mad:3402` | 1 |
| `SVCELL_1000` | `1000B` | `src/LO_SYN.mad:617` | `src/LO_SYN.mad:3407`, `src/LO_SYN.mad:3581`, `src/LO_SYN.mad:3611`, `src/LO_SYN.mad:3710`, `src/LO_SYN.mad:3713`, `src/LO_SYN.mad:3716` | 6 |
| `REGVAL_1006` | `1006B` | `src/LO_SYN.mad:618` | `src/LO_SYN.mad:3411` | 1 |
| `SVCELL_71013` | `71013B` | `src/LO_SYN.mad:619` | `src/LO_SYN.mad:3414` | 1 |
| `EX60_71015` | `71015B` | `src/LO_SYN.mad:620` | `src/LO_SYN.mad:3417` | 1 |
| `EX21_1016` | `1016B` | `src/LO_SYN.mad:621` | `src/LO_SYN.mad:3420` | 1 |
| `REGVAL_1033` | `1033B` | `src/LO_SYN.mad:622` | `src/LO_SYN.mad:3432` | 1 |
| `REGVAL_1034` | `1034B` | `src/LO_SYN.mad:623` | `src/LO_SYN.mad:3435` | 1 |
| `REGVAL_1035` | `1035B` | `src/LO_SYN.mad:624` | `src/LO_SYN.mad:3438` | 1 |
| `MEM_71037` | `71037B` | `src/LO_SYN.mad:625` | `src/LO_SYN.mad:3441` | 1 |
| `EX70_71101` | `71101B` | `src/LO_SYN.mad:626` | `src/LO_SYN.mad:3444` | 1 |
| `REGVAL_1102` | `1102B` | `src/LO_SYN.mad:627` | `src/LO_SYN.mad:3447` | 1 |
| `EX60_71105` | `71105B` | `src/LO_SYN.mad:628` | `src/LO_SYN.mad:3450` | 1 |
| `ADRPTR_1111` | `1111B` | `src/LO_SYN.mad:629` | `src/LO_SYN.mad:3453` | 1 |
| `REGVAL_1115` | `1115B` | `src/LO_SYN.mad:630` | `src/LO_SYN.mad:3462` | 1 |
| `MEM_1200` | `1200B` | `src/LO_SYN.mad:631` | `src/LO_SYN.mad:3465` | 1 |
| `EX50_1202` | `1202B` | `src/LO_SYN.mad:632` | `src/LO_SYN.mad:3471` | 1 |
| `REGVAL_1204` | `1204B` | `src/LO_SYN.mad:633` | `src/LO_SYN.mad:3474` | 1 |
| `SVCELL_71213` | `71213B` | `src/LO_SYN.mad:634` | `src/LO_SYN.mad:3477` | 1 |
| `REGVAL_1214` | `1214B` | `src/LO_SYN.mad:635` | `src/LO_SYN.mad:3480` | 1 |
| `EX60_71215` | `71215B` | `src/LO_SYN.mad:636` | `src/LO_SYN.mad:3483` | 1 |
| `REGVAL_1217` | `1217B` | `src/LO_SYN.mad:637` | `src/LO_SYN.mad:3486` | 1 |
| `REGVAL_1301` | `1301B` | `src/LO_SYN.mad:638` | `src/LO_SYN.mad:3489` | 1 |
| `EX21_1302` | `1302B` | `src/LO_SYN.mad:639` | `src/LO_SYN.mad:3492` | 1 |
| `REGVAL_1303` | `1303B` | `src/LO_SYN.mad:640` | `src/LO_SYN.mad:3495` | 1 |
| `EX36_1310` | `1310B` | `src/LO_SYN.mad:641` | `src/LO_SYN.mad:3501` | 1 |
| `EX50_1311` | `1311B` | `src/LO_SYN.mad:642` | `src/LO_SYN.mad:3504` | 1 |
| `MEM_71312` | `71312B` | `src/LO_SYN.mad:643` | `src/LO_SYN.mad:3507` | 1 |
| `EX60_71313` | `71313B` | `src/LO_SYN.mad:644` | `src/LO_SYN.mad:3510` | 1 |
| `ADRPTR_1314` | `1314B` | `src/LO_SYN.mad:645` | `src/LO_SYN.mad:3513` | 1 |
| `REGVAL_1315` | `1315B` | `src/LO_SYN.mad:646` | `src/LO_SYN.mad:3516` | 1 |
| `SVCELL_1322` | `1322B` | `src/LO_SYN.mad:647` | `src/LO_SYN.mad:3525` | 1 |
| `EX50_1323` | `1323B` | `src/LO_SYN.mad:648` | `src/LO_SYN.mad:3528` | 1 |
| `EX50_1324` | `1324B` | `src/LO_SYN.mad:649` | `src/LO_SYN.mad:3531` | 1 |
| `SVCELL_71325` | `71325B` | `src/LO_SYN.mad:650` | `src/LO_SYN.mad:3534` | 1 |
| `EX70_71326` | `71326B` | `src/LO_SYN.mad:651` | `src/LO_SYN.mad:3537` | 1 |
| `MEM_1401` | `1401B` | `src/LO_SYN.mad:652` | `src/LO_SYN.mad:3552` | 1 |
| `REGVAL_1402` | `1402B` | `src/LO_SYN.mad:653` | `src/LO_SYN.mad:3555` | 1 |
| `REGVAL_1403` | `1403B` | `src/LO_SYN.mad:654` | `src/LO_SYN.mad:3558` | 1 |
| `SVCELL_71404` | `71404B` | `src/LO_SYN.mad:655` | `src/LO_SYN.mad:3561` | 1 |
| `EX70_71405` | `71405B` | `src/LO_SYN.mad:656` | `src/LO_SYN.mad:3564` | 1 |
| `REGVAL_1407` | `1407B` | `src/LO_SYN.mad:657` | `src/LO_SYN.mad:3567` | 1 |
| `REGVAL_2001` | `2001B` | `src/LO_SYN.mad:658` | `src/LO_SYN.mad:3579` | 1 |
| `SVCELL_72002` | `72002B` | `src/LO_SYN.mad:659` | `src/LO_SYN.mad:3582` | 1 |
| `ADRPTR_2003` | `2003B` | `src/LO_SYN.mad:660` | `src/LO_SYN.mad:3585` | 1 |
| `ADRPTR_2004` | `2004B` | `src/LO_SYN.mad:661` | `src/LO_SYN.mad:3588` | 1 |
| `EXT_2005` | `2005B` | `src/LO_SYN.mad:662` | `src/LO_SYN.mad:3591` | 1 |
| `SVCELL_2006` | `2006B` | `src/LO_SYN.mad:663` | `src/LO_SYN.mad:3594` | 1 |
| `REGVAL_2010` | `2010B` | `src/LO_SYN.mad:664` | `src/LO_SYN.mad:3597` | 1 |
| `EXT_72011` | `72011B` | `src/LO_SYN.mad:665` | `src/LO_SYN.mad:3600` | 1 |
| `ADRPTR_3001` | `3001B` | `src/LO_SYN.mad:666` | `src/LO_SYN.mad:3603` | 1 |
| `EXT_3002` | `3002B` | `src/LO_SYN.mad:667` | `src/LO_SYN.mad:3606` | 1 |
| `EXT_3003` | `3003B` | `src/LO_SYN.mad:668` | `src/LO_SYN.mad:3609` | 1 |
| `MEM_3005` | `3005B` | `src/LO_SYN.mad:669` | `src/LO_SYN.mad:3612` | 1 |
| `MEM_73007` | `73007B` | `src/LO_SYN.mad:670` | `src/LO_SYN.mad:3615` | 1 |
| `EX50_73010` | `73010B` | `src/LO_SYN.mad:671` | `src/LO_SYN.mad:3618` | 1 |
| `ADRPTR_3101` | `3101B` | `src/LO_SYN.mad:672` | `src/LO_SYN.mad:3621` | 1 |
| `REGVAL_3102` | `3102B` | `src/LO_SYN.mad:673` | `src/LO_SYN.mad:3624` | 1 |
| `REGVAL_3103` | `3103B` | `src/LO_SYN.mad:674` | `src/LO_SYN.mad:3627` | 1 |
| `EXT_3106` | `3106B` | `src/LO_SYN.mad:675` | `src/LO_SYN.mad:3630` | 1 |
| `SVCELL_601` | `601B` | `src/LO_SYN.mad:676` | `src/LO_SYN.mad:3632`, `src/LO_SYN.mad:3635`, `src/LO_SYN.mad:3674`, `src/LO_SYN.mad:3770`, `src/LO_SYN.mad:3776`, `src/LO_SYN.mad:3803` … (+1) | 7 |
| `MEM_3107` | `3107B` | `src/LO_SYN.mad:677` | `src/LO_SYN.mad:3633` | 1 |
| `EX70_3110` | `3110B` | `src/LO_SYN.mad:678` | `src/LO_SYN.mad:3636` | 1 |
| `SVCELL_701` | `701B` | `src/LO_SYN.mad:679` | `src/LO_SYN.mad:3638`, `src/LO_SYN.mad:3692`, `src/LO_SYN.mad:3725`, `src/LO_SYN.mad:3764`, `src/LO_SYN.mad:3773`, `src/LO_SYN.mad:3791` … (+3) | 9 |
| `EX50_73111` | `73111B` | `src/LO_SYN.mad:680` | `src/LO_SYN.mad:3639` | 1 |
| `EXT_4001` | `4001B` | `src/LO_SYN.mad:681` | `src/LO_SYN.mad:3642` | 1 |
| `EX60_4002` | `4002B` | `src/LO_SYN.mad:682` | `src/LO_SYN.mad:3645` | 1 |
| `EXT_74003` | `74003B` | `src/LO_SYN.mad:683` | `src/LO_SYN.mad:3648` | 1 |
| `SVCELL_501` | `501B` | `src/LO_SYN.mad:684` | `src/LO_SYN.mad:3650`, `src/LO_SYN.mad:3686`, `src/LO_SYN.mad:3728`, `src/LO_SYN.mad:3755`, `src/LO_SYN.mad:3761`, `src/LO_SYN.mad:3788` … (+2) | 8 |
| `REGVAL_4010` | `4010B` | `src/LO_SYN.mad:685` | `src/LO_SYN.mad:3651` | 1 |
| `ADRPTR_4011` | `4011B` | `src/LO_SYN.mad:686` | `src/LO_SYN.mad:3654` | 1 |
| `SVCELL_200` | `200B` | `src/LO_SYN.mad:687` | `src/LO_SYN.mad:3656` | 1 |
| `EXT_4012` | `4012B` | `src/LO_SYN.mad:688` | `src/LO_SYN.mad:3657` | 1 |
| `EXT_4013` | `4013B` | `src/LO_SYN.mad:689` | `src/LO_SYN.mad:3660` | 1 |
| `EXT_4014` | `4014B` | `src/LO_SYN.mad:690` | `src/LO_SYN.mad:3663` | 1 |
| `SVCELL_4015` | `4015B` | `src/LO_SYN.mad:691` | `src/LO_SYN.mad:3666` | 1 |
| `EX50_4016` | `4016B` | `src/LO_SYN.mad:692` | `src/LO_SYN.mad:3669` | 1 |
| `MEM_74017` | `74017B` | `src/LO_SYN.mad:693` | `src/LO_SYN.mad:3672` | 1 |
| `EXT_4020` | `4020B` | `src/LO_SYN.mad:694` | `src/LO_SYN.mad:3675` | 1 |
| `EX70_74021` | `74021B` | `src/LO_SYN.mad:695` | `src/LO_SYN.mad:3678` | 1 |
| `ADRPTR_4022` | `4022B` | `src/LO_SYN.mad:696` | `src/LO_SYN.mad:3681` | 1 |
| `REGVAL_4023` | `4023B` | `src/LO_SYN.mad:697` | `src/LO_SYN.mad:3684` | 1 |
| `EXT_4024` | `4024B` | `src/LO_SYN.mad:698` | `src/LO_SYN.mad:3687` | 1 |
| `SVCELL_301` | `301B` | `src/LO_SYN.mad:699` | `src/LO_SYN.mad:3689`, `src/LO_SYN.mad:3743`, `src/LO_SYN.mad:3758`, `src/LO_SYN.mad:3809`, `src/LO_SYN.mad:3818` | 5 |
| `REGVAL_4025` | `4025B` | `src/LO_SYN.mad:700` | `src/LO_SYN.mad:3690` | 1 |
| `EX70_4026` | `4026B` | `src/LO_SYN.mad:701` | `src/LO_SYN.mad:3693` | 1 |
| `SVCELL_1001` | `1001B` | `src/LO_SYN.mad:702` | `src/LO_SYN.mad:3695`, `src/LO_SYN.mad:3767`, `src/LO_SYN.mad:3827` | 3 |
| `EX60_74030` | `74030B` | `src/LO_SYN.mad:703` | `src/LO_SYN.mad:3696` | 1 |
| `EXT_4031` | `4031B` | `src/LO_SYN.mad:704` | `src/LO_SYN.mad:3699` | 1 |
| `EXT_4032` | `4032B` | `src/LO_SYN.mad:705` | `src/LO_SYN.mad:3702` | 1 |
| `EXT_4033` | `4033B` | `src/LO_SYN.mad:706` | `src/LO_SYN.mad:3705` | 1 |
| `SVCELL_74034` | `74034B` | `src/LO_SYN.mad:707` | `src/LO_SYN.mad:3708` | 1 |
| `EX60_74035` | `74035B` | `src/LO_SYN.mad:708` | `src/LO_SYN.mad:3711` | 1 |
| `EXT_4036` | `4036B` | `src/LO_SYN.mad:709` | `src/LO_SYN.mad:3714` | 1 |
| `EX36_4037` | `4037B` | `src/LO_SYN.mad:710` | `src/LO_SYN.mad:3717` | 1 |
| `EX60_74040` | `74040B` | `src/LO_SYN.mad:711` | `src/LO_SYN.mad:3720` | 1 |
| `SVCELL_401` | `401B` | `src/LO_SYN.mad:712` | `src/LO_SYN.mad:3722`, `src/LO_SYN.mad:3731`, `src/LO_SYN.mad:3734`, `src/LO_SYN.mad:3737`, `src/LO_SYN.mad:3746`, `src/LO_SYN.mad:3749` … (+3) | 9 |
| `EX60_4041` | `4041B` | `src/LO_SYN.mad:713` | `src/LO_SYN.mad:3723` | 1 |
| `SVCELL_74042` | `74042B` | `src/LO_SYN.mad:714` | `src/LO_SYN.mad:3726` | 1 |
| `EX21_4043` | `4043B` | `src/LO_SYN.mad:715` | `src/LO_SYN.mad:3729` | 1 |
| `EXT_4052` | `4052B` | `src/LO_SYN.mad:716` | `src/LO_SYN.mad:3732` | 1 |
| `EXT_4053` | `4053B` | `src/LO_SYN.mad:717` | `src/LO_SYN.mad:3735` | 1 |
| `EX36_4054` | `4054B` | `src/LO_SYN.mad:718` | `src/LO_SYN.mad:3738` | 1 |
| `SVCELL_201` | `201B` | `src/LO_SYN.mad:719` | `src/LO_SYN.mad:3740` | 1 |
| `SVCELL_4061` | `4061B` | `src/LO_SYN.mad:720` | `src/LO_SYN.mad:3741` | 1 |
| `REGVAL_4071` | `4071B` | `src/LO_SYN.mad:721` | `src/LO_SYN.mad:3744` | 1 |
| `EX70_4072` | `4072B` | `src/LO_SYN.mad:722` | `src/LO_SYN.mad:3747` | 1 |
| `EXT_74073` | `74073B` | `src/LO_SYN.mad:723` | `src/LO_SYN.mad:3750` | 1 |
| `EX70_74075` | `74075B` | `src/LO_SYN.mad:724` | `src/LO_SYN.mad:3753` | 1 |
| `ADRPTR_4201` | `4201B` | `src/LO_SYN.mad:725` | `src/LO_SYN.mad:3756` | 1 |
| `EXT_4301` | `4301B` | `src/LO_SYN.mad:726` | `src/LO_SYN.mad:3759` | 1 |
| `EXT_4302` | `4302B` | `src/LO_SYN.mad:727` | `src/LO_SYN.mad:3762` | 1 |
| `SVCELL_4303` | `4303B` | `src/LO_SYN.mad:728` | `src/LO_SYN.mad:3765` | 1 |
| `EX70_4311` | `4311B` | `src/LO_SYN.mad:729` | `src/LO_SYN.mad:3768` | 1 |
| `EX70_74312` | `74312B` | `src/LO_SYN.mad:730` | `src/LO_SYN.mad:3771` | 1 |
| `REGVAL_4313` | `4313B` | `src/LO_SYN.mad:731` | `src/LO_SYN.mad:3774` | 1 |
| `EXT_4314` | `4314B` | `src/LO_SYN.mad:732` | `src/LO_SYN.mad:3777` | 1 |
| `SVCELL_1101` | `1101B` | `src/LO_SYN.mad:733` | `src/LO_SYN.mad:3779`, `src/LO_SYN.mad:3782`, `src/LO_SYN.mad:3821` | 3 |
| `SVCELL_4315` | `4315B` | `src/LO_SYN.mad:734` | `src/LO_SYN.mad:3780` | 1 |
| `SVCELL_4317` | `4317B` | `src/LO_SYN.mad:735` | `src/LO_SYN.mad:3783` | 1 |
| `REGVAL_4321` | `4321B` | `src/LO_SYN.mad:736` | `src/LO_SYN.mad:3786` | 1 |
| `EXT_74322` | `74322B` | `src/LO_SYN.mad:737` | `src/LO_SYN.mad:3789` | 1 |
| `EX20_4323` | `4323B` | `src/LO_SYN.mad:738` | `src/LO_SYN.mad:3792` | 1 |
| `EXT_4324` | `4324B` | `src/LO_SYN.mad:739` | `src/LO_SYN.mad:3795` | 1 |
| `REGVAL_4325` | `4325B` | `src/LO_SYN.mad:740` | `src/LO_SYN.mad:3798` | 1 |
| `EXT_4326` | `4326B` | `src/LO_SYN.mad:741` | `src/LO_SYN.mad:3801` | 1 |
| `EXT_4327` | `4327B` | `src/LO_SYN.mad:742` | `src/LO_SYN.mad:3804` | 1 |
| `SVCELL_4330` | `4330B` | `src/LO_SYN.mad:743` | `src/LO_SYN.mad:3807` | 1 |
| `MEM_74401` | `74401B` | `src/LO_SYN.mad:744` | `src/LO_SYN.mad:3810` | 1 |
| `REGVAL_74404` | `74404B` | `src/LO_SYN.mad:745` | `src/LO_SYN.mad:3813` | 1 |
| `EX20_4405` | `4405B` | `src/LO_SYN.mad:746` | `src/LO_SYN.mad:3816` | 1 |
| `REGVAL_4406` | `4406B` | `src/LO_SYN.mad:747` | `src/LO_SYN.mad:3819` | 1 |
| `EXT_4407` | `4407B` | `src/LO_SYN.mad:748` | `src/LO_SYN.mad:3822` | 1 |
| `SVCELL_1201` | `1201B` | `src/LO_SYN.mad:749` | `src/LO_SYN.mad:3824` | 1 |
| `SVCELL_4412` | `4412B` | `src/LO_SYN.mad:750` | `src/LO_SYN.mad:3825` | 1 |
| `SVCELL_74413` | `74413B` | `src/LO_SYN.mad:751` | `src/LO_SYN.mad:3828` | 1 |
| `ADRPTR_4416` | `4416B` | `src/LO_SYN.mad:752` | `src/LO_SYN.mad:3831` | 1 |
| `EXT_4421` | `4421B` | `src/LO_SYN.mad:753` | `src/LO_SYN.mad:3834` | 1 |
| `SVCELL_4422` | `4422B` | `src/LO_SYN.mad:754` | `src/LO_SYN.mad:3837` | 1 |
| `EX60_4423` | `4423B` | `src/LO_SYN.mad:755` | `src/LO_SYN.mad:3840` | 1 |

**Символы-кандидаты без объявления** (возможно, их нужно описать):

| Символ | Число применений | Пример |
|---|---:|---|
| `H` | 14 | `src/FOREX_RUNTIME.mad:59` (`EQU`) |
| `NEW` | 3 | `src/FOREX_CORE.mad:145` (`NAME`) |
| `DTRAN` | 3 | `src/FOREX_CORE.mad:145` (`NAME`) |
| `INFLOA` | 3 | `include/FOREX_ROOT.mad:237` (`CONT`) |
| `H00` | 2 | `src/FOREX_RUNTIME.mad:85` (`EQU`) |
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
| `HFT*561` | 2 | `src/LO_GEN.mad:524` (`TEXT`) |
| `HFT*571` | 2 | `src/LO_GEN.mad:525` (`TEXT`) |
| `HFT*531` | 2 | `src/LO_GEN.mad:526` (`TEXT`) |

### 2.3 Оставшиеся «голые» литералы

Числовой литерал считается «голым», если он встречается непосредственно
в операнде и не вынесен в правую часть `,EQU,`. Цель — свести эту таблицу
к нулю по мере замены литералов именованными константами.

| Файл | Строк с литералами | Вхождений | Примеры (значение @ файл:строка) |
|---|---:|---:|---|
| `include/FOREX_ROOT.mad` | 10 | 10 | `2`×4, `3`×3, `1`×2, `4`×1 |
| `src/FOREX_CORE.mad` | 1 | 1 | `4300B`×1 |
| `src/FOREX_RUNTIME.mad` | 7 | 15 | `1`×4, `0000`×2, `4631`×2, `0`×1, `1.0`×1 |
| `src/LO_GEN.mad` | 3 | 3 | `0o4000`×1, `0o50`×1, `5`×1 |
| `src/LO_SYN.mad` | 8 | 8 | `1`×4, `50B`×1, `4000B`×1, `5`×1, `15`×1 |

Из них **14** — в описаниях данных (`BSS/OCT/REAL/TEXT/…`) (приоритетные кандидаты на `EQU`), **23** — непосредственно в командах (часто адреса, пока не вынесенные в константы).

Описания данных с голыми литералами:

| Файл:строка | Описание | Литерал |
|---|---|---|
| `include/FOREX_ROOT.mad:66` | `LC` | `1` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `1` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `0` |
| `src/FOREX_RUNTIME.mad:477` | `REAL` | `1.0` |
| `src/LO_GEN.mad:497` | `BSS` | `0o4000` |
| `src/LO_GEN.mad:498` | `BSS` | `0o50` |
| `src/LO_GEN.mad:499` | `BSS` | `5` |
| `src/LO_SYN.mad:17` | `LC` | `50B` |
| `src/LO_SYN.mad:18` | `LC` | `4000B` |
| `src/LO_SYN.mad:19` | `LC` | `5` |
| `src/LO_SYN.mad:20` | `LC` | `1` |
| `src/LO_SYN.mad:21` | `LC` | `1` |
| `src/LO_SYN.mad:22` | `LC` | `1` |
| `src/LO_SYN.mad:24` | `LC` | `1` |

Наиболее частые голые литералы (топ-15, по всем модулям):

| Литерал | Вхождений | Где (первые 3) |
|---|---:|---|
| `1` | 10 | `src/FOREX_RUNTIME.mad:208`, `src/FOREX_RUNTIME.mad:397`, `src/FOREX_RUNTIME.mad:477` |
| `2` | 4 | `include/FOREX_ROOT.mad:90`, `include/FOREX_ROOT.mad:243`, `include/FOREX_ROOT.mad:252` |
| `3` | 3 | `include/FOREX_ROOT.mad:85`, `include/FOREX_ROOT.mad:127`, `include/FOREX_ROOT.mad:137` |
| `0000` | 2 | `src/FOREX_RUNTIME.mad:513`, `src/FOREX_RUNTIME.mad:513` |
| `4631` | 2 | `src/FOREX_RUNTIME.mad:514`, `src/FOREX_RUNTIME.mad:514` |
| `5` | 2 | `src/LO_GEN.mad:499`, `src/LO_SYN.mad:19` |
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
| FOREX* (root) | LOADANGO (загрузчик MONSYS) | CALL / VJM 0o74022(15) | `include/FOREX_ROOT.mad:106`, `include/FOREX_ROOT.mad:108` |
| FOREX* (root) | оверлей LO*GEN | XTS 0o4032 + LOADANGO | `include/FOREX_ROOT.mad:107` |
| FOREX* (root) | оверлей LO*SYN | XTS 0o4031 + LOADANGO | `include/FOREX_ROOT.mad:105` |
| FOREX* (root) | рантайм: DATAPR* (LINK 0o74010) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:224` |
| FOREX* (root) | рантайм: GIV/PG (LINK 0o74012) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:238` |
| FOREX* (root) | рантайм: OCTTDEC (LINK 0o74013) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:271` |
| FOREX* (root) | рантайм: TAK/PG (LINK 0o74011) | CALL / UJ через LINK-ячейку | `src/FOREX_CORE.mad:307` |
| оверлей LO*GEN | MONSYS / library21 | VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx | `src/LO_GEN.mad:565`, `src/LO_GEN.mad:575`, `src/LO_GEN.mad:578` … (+573) |
| оверлей LO*SYN | MONSYS / library21 | VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx | `src/LO_SYN.mad:787`, `src/LO_SYN.mad:802`, `src/LO_SYN.mad:805` … (+274) |
| рантайм: FORMAT | FT*nnn (11 entry, 0o77xxx) | UJ FT*nnn | `src/FOREX_RUNTIME.mad:163`, `src/FOREX_RUNTIME.mad:165`, `src/FOREX_RUNTIME.mad:167` … (+8) |

**Оговорка.** LINK-ячейки `0o74010..0o74013` в корне и в FORMAT имеют
одинаковую нумерацию, но relate к разным символам (выделяются пер-модульно) —
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
| `0o042440` | 20 | `EXT_42440` | резидентная библиотека 21 |
| `0o040440` | 15 | `EXT_40440`, `REGVAL_40440` | резидентная библиотека 21 |
| `0o047510` | 13 | `EXT_47510`, `REGVAL_47510` | резидентная библиотека 21 |
| `0o042510` | 12 | `EXT_42510` | резидентная библиотека 21 |
| `0o064440` | 9 | `EXT_64440` | резидентная библиотека 21 |
| `0o042524` | 8 | `EXT_42524` | резидентная библиотека 21 |
| `0o040560` | 8 | `REGVAL_40560` | резидентная библиотека 21 |
| `0o020103` | 7 | `EXT_20103` | резидентные таблицы MONSYS |
| `0o020040` | 7 | `EXT_20040` | резидентные таблицы MONSYS |
| `0o040513` | 7 | `REGVAL_40513` | резидентная библиотека 21 |
| `0o040554` | 6 | `EXT_40554` | резидентная библиотека 21 |
| `0o066101` | 6 | `EXT_66101` | резидентная библиотека 21 |
| `0o074117` | 6 | `REGVAL_74117` | прочее |
| `0o020117` | 5 | `EXT_20117`, `REGVAL_20117` | резидентные таблицы MONSYS |
| `0o074101` | 5 | `REGVAL_74101` | прочее |
| `0o074171` | 5 | `REGVAL_74171` | прочее |
| `0o041440` | 5 | `EXT_41440` | резидентная библиотека 21 |
| `0o047554` | 5 | `EXT_47554` | резидентная библиотека 21 |
| `0o020160` | 5 | `EXT_20160` | резидентные таблицы MONSYS |
| `0o020113` | 4 | `EXT_20113`, `REGVAL_20113` | резидентные таблицы MONSYS |
| `0o020151` | 4 | `EXT_20151` | резидентные таблицы MONSYS |
| `0o070440` | 4 | `EXT_70440` | резидентная библиотека 21 |
| `0o066140` | 3 | `EXT_66140` | резидентная библиотека 21 |
| `0o047502` | 3 | `EXT_47502` | резидентная библиотека 21 |
| `0o045517` | 3 | `EXT_45517` | резидентная библиотека 21 |
| `0o047566` | 3 | `EXT_47566` | резидентная библиотека 21 |
| `0o020142` | 3 | `EXT_20142`, `REGVAL_20142` | резидентные таблицы MONSYS |
| `0o077520` | 3 | `REGVAL_77520` | код/таблицы MONSYS |
| `0o020120` | 3 | `EXT_20120` | резидентные таблицы MONSYS |
| `0o020124` | 3 | `EXT_20124` | резидентные таблицы MONSYS |
| … | … | ещё 68 адресов | — |

### 4.2. LO*GEN (генератор кода)

Различных адресов: **271**, всего переходов: **576** (эталон docs/06: 225 / 504 — разница объясняется другим набором мнемоник и источником листинга).

| Адрес | Входов | Имя через EQU | Область (docs/06 §2) |
|---|---:|---|---|
| `0o077144` | 69 | `JUMP_TARGET_77144` | код/таблицы MONSYS |
| `0o057476` | 45 | `JUMP_TARGET_57476` | резидентная библиотека 21 |
| `0o057325` | 12 | `JUMP_TARGET_57325` | резидентная библиотека 21 |
| `0o077130` | 10 | `JUMP_TARGET_77130` | код/таблицы MONSYS |
| `0o061372` | 10 | `JUMP_TARGET_61372` | резидентная библиотека 21 |
| `0o063347` | 9 | `JUMP_TARGET_63347` | резидентная библиотека 21 |
| `0o042637` | 8 | `JUMP_TARGET_42637` | резидентная библиотека 21 |
| `0o042274` | 8 | `JUMP_TARGET_42274` | резидентная библиотека 21 |
| `0o042256` | 7 | `JUMP_TARGET_42256` | резидентная библиотека 21 |
| `0o076566` | 7 | `JUMP_TARGET_76566` | код/таблицы MONSYS |
| `0o056620` | 7 | `ADDR_56620` | резидентная библиотека 21 |
| `0o042601` | 6 | `JUMP_TARGET_42601` | резидентная библиотека 21 |
| `0o056617` | 6 | `ADDR_56617` | резидентная библиотека 21 |
| `0o042244` | 5 | `JUMP_TARGET_42244` | резидентная библиотека 21 |
| `0o042626` | 5 | `JUMP_TARGET_42626` | резидентная библиотека 21 |
| `0o045421` | 5 | `JUMP_TARGET_45421` | резидентная библиотека 21 |
| `0o056563` | 5 | `ADDR_56563` | резидентная библиотека 21 |
| `0o042115` | 5 | `JUMP_TARGET_42115` | резидентная библиотека 21 |
| `0o076501` | 5 | `JUMP_TARGET_76501` | код/таблицы MONSYS |
| `0o056564` | 4 | `ADDR_56564` | резидентная библиотека 21 |
| `0o056575` | 4 | `ADDR_56575` | резидентная библиотека 21 |
| `0o075445` | 4 | `JUMP_TARGET_75445` | код/таблицы MONSYS |
| `0o056561` | 4 | `ADDR_56561` | резидентная библиотека 21 |
| `0o041574` | 4 | `JUMP_TARGET_41574` | резидентная библиотека 21 |
| `0o076125` | 4 | `JUMP_TARGET_76125` | код/таблицы MONSYS |
| `0o056615` | 4 | `ADDR_56615` | резидентная библиотека 21 |
| `0o076353` | 4 | `JUMP_TARGET_76353` | код/таблицы MONSYS |
| `0o042413` | 3 | `ADDR_42413` | резидентная библиотека 21 |
| `0o056566` | 3 | `ADDR_56566` | резидентная библиотека 21 |
| `0o042360` | 3 | `JUMP_TARGET_42360` | резидентная библиотека 21 |
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
| `FOREX` | `src/LO_SYN.mad:29`, `include/FOREX_ROOT.mad:73`, `include/FOREX.labels.md:358` | 0 | ❌ не найдено |
| `CONST` | `include/FOREX_ROOT.mad:74`, `include/FOREX.labels.md:358` | 0 | ❌ не найдено |
| `COMEQ` | `include/FOREX_ROOT.mad:75`, `include/FOREX.labels.md:358` | 0 | ❌ не найдено |
| `OPRTR` | `src/LO_SYN.mad:32`, `include/FOREX_ROOT.mad:76`, `include/FOREX.labels.md:358` | 0 | ❌ не найдено |
| `ПP` | `src/LO_SYN.mad:33`, `include/FOREX_ROOT.mad:77`, `include/FOREX.labels.md:358` | 0 | ❌ не найдено |

Доказательства: `include/FOREX_CORE.xref.md` §3, `docs/06-core-modules.md`
§3, `logs/dtran_root.txt` (`IS ABSENT` для всех пяти).

## 7. Воспроизводимость

```bash
cd /tmp/.private/azizz/opencode/re-forex
python3 tools/xref_all.py --out docs/09-crossrefs.md
# лог: logs/xref_all.txt (переопределяется флагом --log)
```

Инструмент детерминирован: сортирует все таблицы, не использует текущее
время — повторный запуск даёт байт-в-байт тот же вывод (идемпотентность).

## 8. Связанные документы

- `include/FOREX_CORE.xref.md`, `include/FOREX_RUNTIME.xref.md`,
  `include/LO_SYN.xref.md`, `include/LO_GEN.xref.md` — подробные xref по модулям;
- `docs/03-symbols.md` — символьный чек-лист (37/37);
- `docs/06-address-map.md` — карта внешних адресов;
- `logs/address_targets.txt` — сырые частоты адресов из листингов.
