# CHEKJOB_ — перекрёстные ссылки

Модуль `CHEKJOB*` (исходник `libra211.l21:6019-6497`). Сверка: `disasm/lib21/CHEKJOB_.madlen`.

Все метки переименованы в ≤6 символов (уникальные первые 6); полные имена сохранены в `; (POLN: ...)` в `src/lib21/CHEKJOB_.mad`.

## 1. Таблица символов (метки и EQU)

| Короткое имя | Полное имя (POLN) | Тип | Строка |
|---|---|---|---|
| `CHE001` | `CHEKJOB*` | метка | libra211.l21:6019 |
| `MON002` | `MONITOR*` | метка | libra211.l21:6026 |
| `RM003` | `RM*` | метка | libra211.l21:6027 |
| `MON004` | `MONIT` | метка | libra211.l21:6028 |
| `LOA005` | `LOADGO` | метка | libra211.l21:6029 |
| `MON006` | `MONCARD*` | метка | libra211.l21:6030 |
| `KCO007` | `KCOUNT*` | метка | libra211.l21:6031 |
| `STA008` | `STATIC*` | метка | libra211.l21:6032 |
| `INF009` | `INFLOAD*` | метка | libra211.l21:6033 |
| `DAT010` | `DAT` | метка | libra211.l21:6034 |
| `LIB011` | `LIB` | метка | libra211.l21:6035 |
| `FLA012` | `*FLAG*` | метка | libra211.l21:6037 |
| `ORD013` | `*ORDEN` | метка | libra211.l21:6041 |
| `BIG014` | `BIGTITLE` | метка | libra211.l21:6042 |
| `CHE015` | `CHE*NAM` | метка | libra211.l21:6043 |
| `TAK016` | `TAK*COCA` | метка | libra211.l21:6044 |
| `CON017` | `CONCAR` | метка | libra211.l21:6045 |
| `LEN018` | `LEN` | метка | libra211.l21:6046 |
| `END019` | `END*CJOB` | метка | libra211.l21:6047 |
| `GIV020` | `GIVETIME` | метка | libra211.l21:6048 |
| `ISO021` | `ISO*TEX*` | метка | libra211.l21:6049 |
| `PUN022` | `PUNTEX/` | метка | libra211.l21:6050 |
| `PRE023` | `PREPDAT` | метка | libra211.l21:6051 |
| `NTA024` | `NTAPDISC` | метка | libra211.l21:6052 |
| `MON025` | `MONCARD/` | метка | libra211.l21:6053 |
| `MON026` | `*MONCRD*` | метка | libra211.l21:6054 |
| `MIS027` | `MIST10*` | метка | libra211.l21:6055 |
| `STA028` | `STARSTA` | метка | libra211.l21:6056 |
| `OUT029` | `OUT*OUT` | метка | libra211.l21:6057 |
| `DIS030` | `*DISPAR1` | метка | libra211.l21:6058 |
| `TRA031` | `TRANSFIO` | метка | libra211.l21:6059 |
| `GOS032` | `GOST/ISO` | метка | libra211.l21:6060 |
| `TAB033` | `TABSIMIS` | метка | libra211.l21:6061 |
| `GIV034` | `GIVETAP*` | метка | libra211.l21:6062 |
| `MON035` | `MONREAD*` | метка | libra211.l21:6064 |
| `PRI036` | `PRINT8` | метка | libra211.l21:6065 |
| `N1037` | `*1` | метка | libra211.l21:6067 |
| `C038` | `C` | метка | libra211.l21:6068 |
| `AD039` | `AD` | метка | libra211.l21:6069 |
| `TWO040` | `TWOPOINT` | метка | libra211.l21:6071 |
| `AYC041` | `A/ГYC` | метка | libra211.l21:6072 |
| `AK042` | `A/ИПK` | метка | libra211.l21:6073 |
| `A043` | `A/ИПД` | метка | libra211.l21:6074 |
| `XNF044` | `XNFM` | метка | libra211.l21:6075 |
| `ALI045` | `A/LINKP` | метка | libra211.l21:6076 |
| `SCC046` | `SC/CONC` | метка | libra211.l21:6077 |
| `CPO047` | `C......   ПPOBEPKA` | метка | libra211.l21:6080 |
| `NOS048` | `NO/STAT` | метка | libra211.l21:6096 |
| `MA049` | `MAШ` | метка | libra211.l21:6105 |
| `DIS050` | `DISP` | метка | libra211.l21:6115 |
| `CNT053` | `CNT` | метка | libra211.l21:6171 |
| `BPR054` | `B PRI` | метка | libra211.l21:6174 |
| `LOO055` | `LOOP` | метка | libra211.l21:6195 |
| `LO0056` | `LO 0` | метка | libra211.l21:6211 |
| `LO1057` | `LO 1` | метка | libra211.l21:6229 |
| `OUT058` | `OUT` | метка | libra211.l21:6235 |
| `N71059` | `*71` | метка | libra211.l21:6249 |
| `GIV061` | `GIVTAP` | метка | libra211.l21:6252 |
| `MUJ063` | `MUJ` | метка | libra211.l21:6295 |
| `TOI064` | `TOINFBA` | метка | libra211.l21:6299 |
| `GIV065` | `GIVTAP1` | метка | libra211.l21:6301 |
| `TAK067` | `TAKE` | метка | libra211.l21:6308 |
| `CAL068` | `CALL` | метка | libra211.l21:6311 |
| `SW2069` | `SW2` | метка | libra211.l21:6315 |
| `TOP070` | `TO PRI` | метка | libra211.l21:6320 |
| `TAK071` | `TAK LIST` | метка | libra211.l21:6331 |
| `PRI073` | `PRI PASS` | метка | libra211.l21:6337 |
| `PRI074` | `PRI PRIOR` | метка | libra211.l21:6341 |
| `LPR075` | `LPRIO` | метка | libra211.l21:6343 |
| `PRI078` | `PRI CHE` | метка | libra211.l21:6379 |
| `PRI079` | `PRINT` | метка | libra211.l21:6387 |
| `CHE081` | `CHECK` | метка | libra211.l21:6397 |
| `CHE082` | `CHE 1` | метка | libra211.l21:6404 |
| `GEN083` | `GEN ER` | метка | libra211.l21:6406 |
| `PUN084` | `PUNCH` | метка | libra211.l21:6412 |
| `ERN085` | `ER NAM` | метка | libra211.l21:6416 |
| `EN1086` | `EN 1` | метка | libra211.l21:6420 |
| `FAT087` | `FAT` | метка | libra211.l21:6424 |
| `STO088` | `STOP` | метка | libra211.l21:6429 |
| `ERC089` | `ER CAR` | метка | libra211.l21:6433 |
| `ERC090` | `ERCAR1` | метка | libra211.l21:6434 |
| `ERR091` | `ER REF` | метка | libra211.l21:6438 |
| `ERR092` | `ER REF1` | метка | libra211.l21:6446 |
| `I8B093` | `I 8BS` | метка | libra211.l21:6453 |
| `DUM094` | `DUM` | метка | libra211.l21:6457 |
| `MON095` | `MONAM` | метка | libra211.l21:6458 |
| `BES096` | `BESM6` | метка | libra211.l21:6460 |
| `BES097` | `BESM6/` | метка | libra211.l21:6462 |
| `SHI098` | `SHI` | метка | libra211.l21:6464 |
| `HEA099` | `HEAD` | метка | libra211.l21:6465 |
| `TDATE` | `DATE` | метка | libra211.l21:6467 |
| `DR1101` | `DR1` | метка | libra211.l21:6468 |
| `DR2102` | `DR2` | метка | libra211.l21:6469 |
| `B35103` | `B35/31` | метка | libra211.l21:6470 |
| `B1104` | `B1` | метка | libra211.l21:6471 |
| `B24105` | `B 24` | метка | libra211.l21:6472 |
| `B45106` | `B45` | метка | libra211.l21:6473 |
| `DOS107` | `*DOS` | метка | libra211.l21:6474 |
| `MB1108` | `MB1` | метка | libra211.l21:6475 |
| `MB1109` | `M B1/2` | метка | libra211.l21:6476 |
| `MB5110` | `M B5/6` | метка | libra211.l21:6477 |
| `TERROR` | `T ERN` | метка | libra211.l21:6483 |
| `TERRCD` | `T OШЗAП` | метка | libra211.l21:6484 |
| `TEARLY` | `T PAHO` | метка | libra211.l21:6486 |
| `TREDEF` | `T ПOBT` | метка | libra211.l21:6488 |
| `TBADLN` | `T OШCC` | метка | libra211.l21:6489 |
| `TNODSK` | `T HДИCK` | метка | libra211.l21:6491 |
| `TVYZOV` | `T БЫO` | метка | libra211.l21:6492 |
| `TEXPRS` | `T PRIOR` | метка | libra211.l21:6493 |
| `SBU119` | `SBUF` | метка | libra211.l21:6494 |
| `SAV120` | `SAV AD` | метка | libra211.l21:6495 |
| `INF121` | `INFBA` | метка | libra211.l21:6496 |
| `SCC046` | `SC/CONC` | EQU = `1` | S1:6077 |
| `ALI045` | `A/LINKP` | EQU = `560B` | S1:6076 |
| `XNF044` | `XNFM` | EQU = `1` | S1:6075 |
| `A043` | `A/ИПД` | EQU = `760B` | S1:6074 |
| `AK042` | `A/ИПK` | EQU = `761B` | S1:6073 |
| `AYC041` | `A/ГYC` | EQU = `502B` | S1:6072 |
| `TWO040` | `TWOPOINT` | EQU = `72B` | S1:6071 |
| `AD039` | `AD` | EQU = `12` | S1:6069 |
| `C038` | `C` | EQU = `10` | S1:6068 |
| `LEN018` | `LEN` | EQU = `CON017-1` | S1:6046 |
| `LIB011` | `LIB` | EQU = `73B` | S1:6035 |
| `DAT010` | `DAT` | EQU = `1776B` | S1:6034 |
| `MON004` | `MONIT` | EQU = `MON002+1` | S1:6028 |
| `EDC012` | `DEC_1` | EQU = `1` | S1:6030 |
| `EDC013` | `DEC_2` | EQU = `2` | S1:6037 |
| `EDC014` | `DEC_5` | EQU = `5` | S1:6037 |
| `EDC015` | `DEC_128` | EQU = `128` | S1:6041 |
| `EDC016` | `DEC_14` | EQU = `14` | S1:6053 |
| `EDC017` | `DEC_12` | EQU = `12` | S1:6054 |
| `EOC017` | `OCT_43` | EQU = `43B` | S1:6081 |
| `EDC018` | `DEC_64` | EQU = `64` | S1:6083 |
| `EDC019` | `DEC_20` | EQU = `20` | S1:6083 |
| `EOC019` | `OCT_1400` | EQU = `1400B` | S1:6087 |
| `EDC020` | `DEC_33` | EQU = `33` | S1:6091 |
| `ETX020` | `LITERAL___0000_3703` | EQU = `=:0000 3703` | S1:6092 |
| `ETX021` | `LITERAL__4014_0000_0021_0101` | EQU = `=4014 0000 0021 0101` | S1:6093 |
| `EOC021` | `OCT_765` | EQU = `765B` | S1:6102 |
| `EDC021` | `DEC_7` | EQU = `7` | S1:6107 |
| `ETX022` | `LITERAL__7` | EQU = `=7` | S1:6109 |
| `EDC022` | `DEC_32` | EQU = `32` | S1:6110 |
| `EOC022` | `OCT_502` | EQU = `502B` | S1:6116 |
| `EDC023` | `DEC_27` | EQU = `27` | S1:6119 |
| `ETX023` | `LITERAL__6H_7__7_________` | EQU = `=6H'7''7'''''''''` | S1:6120 |
| `EDC024` | `DEC_13` | EQU = `13` | S1:6147 |
| `EOC024` | `OCT_76` | EQU = `76B` | S1:6148 |
| `EOC025` | `OCT_64` | EQU = `64B` | S1:6151 |
| `EDC025` | `DEC_3` | EQU = `3` | S1:6155 |
| `EOC026` | `OCT_166` | EQU = `166B` | S1:6158 |
| `ETX026` | `LITERAL__100_00000_00000` | EQU = `=100 00000 00000` | S1:6163 |
| `ETX027` | `LITERAL__6H_360___________` | EQU = `=6H'360'''''''''''` | S1:6166 |
| `ETX028` | `LITERAL__6H_060___________` | EQU = `=6H'060'''''''''''` | S1:6167 |
| `EDC028` | `DEC_8` | EQU = `8` | S1:6172 |
| `EDC029` | `DEC_17` | EQU = `17` | S1:6175 |
| `EOC029` | `OCT_21` | EQU = `21B` | S1:6189 |
| `EDC030` | `DEC_0` | EQU = `0` | S1:6193 |
| `ETX030` | `LITERAL__6H_CHE081` | EQU = `=6H*CHE081` | S1:6205 |
| `ETX031` | `LITERAL__6H_` | EQU = `=6H(` | S1:6208 |
| `EDC031` | `DEC_40` | EQU = `40` | S1:6209 |
| `EDC032` | `DEC_24` | EQU = `24` | S1:6215 |
| `ETX032` | `LITERAL__6H` | EQU = `=6H` | S1:6246 |
| `EDC033` | `DEC_42` | EQU = `42` | S1:6257 |
| `EDC034` | `DEC_16` | EQU = `16` | S1:6273 |
| `ETX034` | `LITERAL__17_7777` | EQU = `=17 7777` | S1:6278 |
| `ETX035` | `LITERAL__6H_MU______` | EQU = `=6H-MU''''''` | S1:6283 |
| `ETX036` | `LITERAL__6H______` | EQU = `=6H     =` | S1:6287 |
| `ETX037` | `LITERAL__377` | EQU = `=377` | S1:6288 |
| `ETX038` | `LITERAL__6H_________1__7_` | EQU = `=6H'''''''''1''7'` | S1:6291 |
| `ETX039` | `LITERAL__20_0000` | EQU = `=20 0000` | S1:6293 |
| `ETX040` | `LITERAL__6H_____1__7_____` | EQU = `=6H'''''1''7'''''` | S1:6296 |
| `ETX041` | `LITERAL__40_0000` | EQU = `=40 0000` | S1:6298 |
| `ETX042` | `LIT_1` | EQU = `1` | S1:6319 |
| `EOC042` | `OCT_74100` | EQU = `74100B` | S1:6334 |
| `EOC043` | `OCT_571` | EQU = `571B` | S1:6334 |
| `EOC044` | `OCT_70100` | EQU = `70100B` | S1:6350 |
| `EOC045` | `OCT_114` | EQU = `114B` | S1:6350 |
| `EOC046` | `OCT_117` | EQU = `117B` | S1:6352 |
| `ETX046` | `LITERAL__1777` | EQU = `=1777` | S1:6353 |
| `EDC046` | `DEC_4` | EQU = `4` | S1:6355 |
| `EDC047` | `DEC_6` | EQU = `6` | S1:6362 |
| `EOC047` | `OCT_760` | EQU = `760B` | S1:6365 |
| `EOC048` | `OCT_762` | EQU = `762B` | S1:6369 |
| `ETX048` | `LITERAL__77777` | EQU = `=77777` | S1:6370 |
| `ETX049` | `LITERAL__4` | EQU = `=4` | S1:6373 |
| `ETX050` | `LITERAL__7770_0000_7760_0000` | EQU = `=7770 0000 7760 0000` | S1:6390 |
| `ETX051` | `LIT_2H__231_` | EQU = `2H '231'` | S1:6457 |
| `ETX052` | `LIT_8HMONITOR_` | EQU = `8HMONITOR*` | S1:6458 |
| `ETX053` | `LIT_12H` | EQU = `12H` | S1:6460 |
| `ETX054` | `LIT_6H__CM_6` | EQU = `6HБЭCM-6` | S1:6461 |
| `ETX055` | `LIT_6H_0` | EQU = `6H/0` | S1:6462 |
| `ETX056` | `LIT_6H____P_` | EQU = `6H ШИФP-` | S1:6463 |
| `ETX057` | `LIT_6H00` | EQU = `6H00` | S1:6464 |
| `ETX058` | `LIT_36HMOH_TOPHA__C038_CTEMA___47_` | EQU = `36HMOHИTOPHAЯ C038ИCTEMA  '47'Д Y Б H A'47'  -` | S1:6466 |
| `ETX059` | `LIT_2` | EQU = `2` | S1:6467 |
| `ETX060` | `LIT_14_0000_0021_0001` | EQU = `14 0000 0021 0001` | S1:6468 |
| `ETX061` | `LIT_4014_0003_0021_0101` | EQU = `4014 0003 0021 0101` | S1:6469 |
| `ETX062` | `LIT_0000_37` | EQU = `0000 37` | S1:6470 |
| `ETX063` | `LIT_4000_0000` | EQU = `4000 0000` | S1:6472 |
| `ETX064` | `LIT_04` | EQU = `04` | S1:6473 |
| `ETX065` | `LIT_6H_DOS` | EQU = `6H*DOS` | S1:6474 |
| `ETX066` | `LIT_6H_377_00000` | EQU = `6H'377'00000` | S1:6475 |
| `ETX067` | `LIT_6H_377__377_0000` | EQU = `6H'377''377'0000` | S1:6476 |
| `ETX068` | `LIT_6H0000_377__377_` | EQU = `6H0000'377''377'` | S1:6477 |
| `ETX069` | `LIT_21HOTCYTCTBYET___K__NAME` | EQU = `21HOTCYTCTBYET П/K *NAME` | S1:6483 |
| `ETX070` | `LIT_15HO___KA_B_KAPTE_` | EQU = `15HOШИБKA B KAPTE-` | S1:6484 |
| `ETX071` | `LIT_15HCHECK_PAHOBATO` | EQU = `15HCHECK PAHOBATO` | S1:6486 |
| `EDC071` | `DEC_47` | EQU = `47` | S1:6487 |
| `ETX072` | `LIT_19H_OBTOPHO_O_PE_E_EHO` | EQU = `19HПOBTOPHO OПPEДEЛEHO` | S1:6488 |
| `ETX073` | `LIT_20HHE_PAB___HA__CC__KA` | EQU = `20HHEПPABИЛЬHAЯ CCЫЛKA` | S1:6489 |
| `ETX074` | `LIT_18HHE_O__47__B_EH___CK` | EQU = `18HHE OБ'47'ЯBЛEH ДИCK` | S1:6491 |
| `ETX075` | `LIT_23H_____O___K__B_YK_PA_OT_` | EQU = `23HБЫЛИ OШИБKИ B YK PAБOTЫ` | S1:6492 |
| `ETX076` | `LIT_18H___KC_PECC__A_A_A_` | EQU = `18H <ЭKCПPECC-ЗAДAЧA>` | S1:6493 |
| `ETX077` | `LIT_144` | EQU = `144` | S1:6494 |

## 2. Перекрёстные ссылки (определение → использования)

| Символ | Короткое | Использования (строка: операнд) |
|---|---|---|
| `*71` | `N71059` | 6247:`*71` |
| `*MONCRD*` | `MON026` | 6228:`*MONCRD*` |
| `A/LINKP` | `ALI045` | 6270:`A/LINKP` |
| `A/ГYC` | `AYC041` | 6254:`A/ГYC` |
| `A/ИПK` | `AK042` | 6265:`A/ИПK` |
| `A/ИПД` | `A043` | 6260:`A/ИПД` |
| `AD` | `AD039` | 6220:`AD`; 6221:`SAV AD`; 6223:`SAV AD`; 6224:`AD`; 6389:`AD`; 6392:`AD`; 6394:`AD` |
| `B PRI` | `BPR054` | 6181:`B PRI` |
| `B1` | `B1104` | 6129:`B1`; 6135:`B1`; 6138:`B1`; 6201:`M B1`; 6248:`B1`; 6380:`M B1/2` |
| `B45` | `B45106` | 6333:`B45` |
| `BESM6` | `BES096` | 6104:`BESM6`; 6111:`BESM6/`; 6112:`BESM6/`; 6125:`BESM6` |
| `BESM6/` | `BES097` | 6111:`BESM6/`; 6112:`BESM6/` |
| `BIGTITLE` | `BIG014` | 6160:`BIGTITLE` |
| `C` | `C038` | 6317:`C ST1`; 6381:`C ST2`; 6385:`C ST3`; 6466:`36HMOHИTOPHAЯ CИCTEMA  '47'Д Y Б H A'47'  -` |
| `CALL` | `CAL068` | 6309:`CALL` |
| `CHE 1` | `CHE082` | 6402:`CHE 1` |
| `CHE*NAM` | `CHE015` | 6143:`CHE*NAM` |
| `CHECK` | `CHE081` | 6205:`=6H*CHECK`; 6326:`CHECK`; 6490:`18HHA KAPTY-*CHECK` |
| `CNT` | `CNT053` | 6164:`CNT`; 6168:`CNT` |
| `CONCAR` | `CON017` | 6046:`CONCAR-1` |
| `DAT` | `DAT010` | 6097:`DAT`; 6099:`DAT+1` |
| `DATE` | `TDATE` | 6098:`DATE`; 6100:`DATE+1`; 6133:`DATE+1` |
| `DR1` | `DR1101` | 6084:`DR1` |
| `DUM` | `DUM094` | 6453:`DUM`; 6454:`DUM` |
| `EN 1` | `EN1086` | 6418:`EN 1` |
| `END*CJOB` | `END019` | 6242:`END*CJOB` |
| `ER CAR` | `ERC089` | 6313:`ER CAR`; 6447:`ER CAR` |
| `ER NAM` | `ERN085` | 6144:`ER NAM` |
| `ER REF` | `ERR091` | 6325:`ER REF` |
| `ER REF1` | `ERR092` | 6440:`ER REF1` |
| `ERCAR1` | `ERC090` | 6399:`ERCAR1` |
| `FAT` | `FAT087` | 6432:`FAT` |
| `GEN ER` | `GEN083` | 6437:`GEN ER`; 6445:`GEN ER`; 6452:`GEN ER` |
| `GIVETAP*` | `GIV034` | 6306:`GIVETAP*` |
| `GIVETIME` | `GIV020` | 6236:`GIVETIME` |
| `GIVTAP` | `GIV061` | 6245:`GIVTAP` |
| `GIVTAP1` | `GIV065` | 6275:`GIVTAP1`; 6289:`GIVTAP1` |
| `HEAD` | `HEA099` | 6131:`HEAD` |
| `I 8BS` | `I8B093` | 6137:`I 8BS`; 6183:`I 8BS` |
| `INFBA` | `INF121` | 6269:`INFBA`; 6274:`INFBA`; 6279:`INFBA`; 6280:`INFBA`; 6299:`INFBA` |
| `KCOUNT*` | `KCO007` | 6139:`KCOUNT*+2` |
| `LEN` | `LEN018` | 6214:`LEN`; 6230:`LEN` |
| `LIB` | `LIB011` | 6085:`LIB`; 6086:`LIB`; 6191:`LIB` |
| `LO 0` | `LO0056` | 6206:`LO 0`; 6213:`LO 0` |
| `LO 1` | `LO1057` | 6226:`LO 1`; 6233:`LO 1` |
| `LOOP` | `LOO055` | 6320:`LOOP`; 6329:`LOOP`; 6347:`LOOP`; 6377:`LOOP`; 6397:`LOOP`; 6410:`LOOP`; 6414:`LOOP` |
| `M B1/2` | `MB1109` | 6380:`M B1/2` |
| `M B5/6` | `MB5110` | 6384:`M B5/6` |
| `MAШ` | `MA049` | 6103:`MAШ` |
| `MONAM` | `MON095` | 6088:`MONAM` |
| `MONCARD*` | `MON006` | 6142:`MONCARD*`; 6153:`MONCARD*+1`; 6154:`MONCARD*+2`; 6155:`MONCARD*+3`; 6165:`MONCARD*+1`; 6192:`MONCARD*`; 6197:`MONCARD*`; 6200:`MONCARD*`; 6204:`MONCARD*`; 6207:`MONCARD*+1`; 6211:`MONCARD*+13`; 6308:`MONCARD*` … (+7) |
| `MONCARD/` | `MON025` | 6212:`MONCARD/+13`; 6310:`MONCARD/` |
| `MONIT` | `MON004` | 6304:`MONIT`; 6305:`MONIT` |
| `MONITOR*` | `MON002` | 6028:`MONITOR*+1` |
| `MONREAD*` | `MON035` | 6141:`MONREAD*`; 6199:`MONREAD*` |
| `MUJ` | `MUJ063` | 6284:`MUJ` |
| `NO/STAT` | `NOS048` | 6089:`NO/STAT` |
| `OUT` | `OUT058` | 6202:`OUT`; 6210:`OUT`; 6218:`OUT*OUT` |
| `OUT*OUT` | `OUT029` | 6218:`OUT*OUT` |
| `PREPDAT` | `PRE023` | 6079:`PREPDAT` |
| `PRI CHE` | `PRI078` | 6327:`PRI CHE` |
| `PRI PASS` | `PRI073` | 6318:`PRI PASS` |
| `PRI PRIOR` | `PRI074` | 6328:`PRI PRIOR` |
| `PRINT` | `PRI079` | 6194:`PRINT`; 6321:`PRINT`; 6323:`PRINT`; 6336:`PRINT`; 6354:`PRINT`; 6356:`PRINT`; 6378:`PRINT`; 6419:`PRINT`; 6433:`PRINT`; 6438:`PRINT` |
| `PRINT8` | `PRI036` | 6130:`PRINT8`; 6136:`PRINT8`; 6179:`PRINT8`; 6396:`PRINT8`; 6411:`PRINT8`; 6427:`PRINT8` |
| `PUNCH` | `PUN084` | 6322:`PUNCH` |
| `PUNTEX/` | `PUN022` | 6415:`PUNTEX/` |
| `SAV AD` | `SAV120` | 6221:`SAV AD`; 6223:`SAV AD` |
| `SBUF` | `SBU119` | 6156:`SBUF`; 6173:`SBUF` |
| `SC/CONC` | `SCC046` | 6272:`SC/CONC` |
| `SHI` | `SHI098` | 6121:`SHI`; 6122:`SHI` |
| `STATIC*` | `STA008` | 6094:`STATIC*` |
| `STOP` | `STO088` | 6240:`STOP`; 6243:`STOP` |
| `SW2` | `SW2069` | 6314:`SW2-1` |
| `T ERN` | `TERROR` | 6421:`T ERN` |
| `T HДИCK` | `TNODSK` | 6449:`T HДИCK` |
| `T OШCC` | `TBADLN` | 6442:`T OШCC` |
| `T OШЗAП` | `TERRCD` | 6434:`T OШЗAП` |
| `T PAHO` | `TEARLY` | 6403:`T PAHO` |
| `T БЫO` | `TVYZOV` | 6429:`T БЫO` |
| `T ПOBT` | `TREDEF` | 6400:`T ПOBT` |
| `TAK LIST` | `TAK071` | 6330:`TAK LIST` |
| `TAK*COCA` | `TAK016` | 6312:`TAK*COCA` |
| `TAKE` | `TAK067` | 6232:`TAKE` |
| `TO PRI` | `TOP070` | 6324:`TO PRI`; 6340:`TO PRI` |
| `TOINFBA` | `TOI064` | 6294:`TOINFBA` |
| `TWOPOINT` | `TWO040` | 6225:`-TWOPOINT` |
| `XNFM` | `XNF044` | 6262:`XNFM` |

## 3. Вызовы и переходы (VJM / CALL / UJ)

| Строка | Команда | Операнд |
|---|---|---|
| S1:6079 | `CALL` | `PREPDAT` |
| S1:6130 | `CALL` | `PRINT8` |
| S1:6136 | `CALL` | `PRINT8` |
| S1:6141 | `CALL` | `MONREAD*` |
| S1:6143 | `CALL` | `CHE*NAM` |
| S1:6160 | `CALL` | `BIGTITLE` |
| S1:6170 | `UJ` | `ERNAM` |
| S1:6179 | `CALL` | `PRINT8` |
| S1:6194 | `VJM` | `PRINT` |
| S1:6199 | `CALL` | `MONREAD*` |
| S1:6222 | `CALL` | `PARAMT*` |
| S1:6236 | `CALL` | `GIVETIME` |
| S1:6238 | `CALL` | `PRI*NEWS` |
| S1:6242 | `CALL` | `END*CJOB` |
| S1:6294 | `UJ` | `TOINFBA` |
| S1:6306 | `UJ` | `GIVETAP*` |
| S1:6312 | `CALL` | `TAK*COCA` |
| S1:6314 | `UJ` | `SW2-1` |
| S1:6318 | `UJ` | `PRI PASS` |
| S1:6321 | `UJ` | `PRINT` |
| S1:6323 | `UJ` | `PRINT` |
| S1:6325 | `UJ` | `ER REF` |
| S1:6327 | `UJ` | `PRI CHE` |
| S1:6328 | `UJ` | `PRI PRIOR` |
| S1:6330 | `UJ` | `TAK LIST` |
| S1:6336 | `UJ` | `PRINT` |
| S1:6340 | `UJ` | `TO PRI` |
| S1:6378 | `UJ` | `PRINT` |
| S1:6396 | `UJ` | `PRINT8` |
| S1:6411 | `UJ` | `PRINT8` |
| S1:6415 | `UJ` | `PUNTEX/` |
| S1:6419 | `VJM` | `PRINT` |
| S1:6427 | `CALL` | `PRINT8` |
| S1:6432 | `UJ` | `FAT` |
| S1:6433 | `VJM` | `PRINT` |
| S1:6437 | `UJ` | `GEN ER` |
| S1:6438 | `VJM` | `PRINT` |
| S1:6445 | `UJ` | `GEN ER` |
| S1:6452 | `UJ` | `GEN ER` |

## 4. Внешние символы (не определены в модуле)

- `CHE`
- `ER`
- `ERNAM`
- `GEN`
- `LIST`
- `PARAMT*`
- `PASS`
- `PRI`
- `PRI*NEWS`
- `PRIOR`
- `REF`
- `TAK`
- `TO`

## 5. Литералы → EQU

| EQU | Значение | Строка |
|---|---|---|
| `SCC046` | `1` | S1:6077 |
| `ALI045` | `560B` | S1:6076 |
| `XNF044` | `1` | S1:6075 |
| `A043` | `760B` | S1:6074 |
| `AK042` | `761B` | S1:6073 |
| `AYC041` | `502B` | S1:6072 |
| `TWO040` | `72B` | S1:6071 |
| `AD039` | `12` | S1:6069 |
| `C038` | `10` | S1:6068 |
| `LEN018` | `CON017-1` | S1:6046 |
| `LIB011` | `73B` | S1:6035 |
| `DAT010` | `1776B` | S1:6034 |
| `MON004` | `MON002+1` | S1:6028 |
| `EDC012` | `1` | S1:6030 |
| `EDC013` | `2` | S1:6037 |
| `EDC014` | `5` | S1:6037 |
| `EDC015` | `128` | S1:6041 |
| `EDC016` | `14` | S1:6053 |
| `EDC017` | `12` | S1:6054 |
| `EOC017` | `43B` | S1:6081 |
| `EDC018` | `64` | S1:6083 |
| `EDC019` | `20` | S1:6083 |
| `EOC019` | `1400B` | S1:6087 |
| `EDC020` | `33` | S1:6091 |
| `ETX020` | `=:0000 3703` | S1:6092 |
| `ETX021` | `=4014 0000 0021 0101` | S1:6093 |
| `EOC021` | `765B` | S1:6102 |
| `EDC021` | `7` | S1:6107 |
| `ETX022` | `=7` | S1:6109 |
| `EDC022` | `32` | S1:6110 |
| `EOC022` | `502B` | S1:6116 |
| `EDC023` | `27` | S1:6119 |
| `ETX023` | `=6H'7''7'''''''''` | S1:6120 |
| `EDC024` | `13` | S1:6147 |
| `EOC024` | `76B` | S1:6148 |
| `EOC025` | `64B` | S1:6151 |
| `EDC025` | `3` | S1:6155 |
| `EOC026` | `166B` | S1:6158 |
| `ETX026` | `=100 00000 00000` | S1:6163 |
| `ETX027` | `=6H'360'''''''''''` | S1:6166 |
| `ETX028` | `=6H'060'''''''''''` | S1:6167 |
| `EDC028` | `8` | S1:6172 |
| `EDC029` | `17` | S1:6175 |
| `EOC029` | `21B` | S1:6189 |
| `EDC030` | `0` | S1:6193 |
| `ETX030` | `=6H*CHE081` | S1:6205 |
| `ETX031` | `=6H(` | S1:6208 |
| `EDC031` | `40` | S1:6209 |
| `EDC032` | `24` | S1:6215 |
| `ETX032` | `=6H` | S1:6246 |
| `EDC033` | `42` | S1:6257 |
| `EDC034` | `16` | S1:6273 |
| `ETX034` | `=17 7777` | S1:6278 |
| `ETX035` | `=6H-MU''''''` | S1:6283 |
| `ETX036` | `=6H     =` | S1:6287 |
| `ETX037` | `=377` | S1:6288 |
| `ETX038` | `=6H'''''''''1''7'` | S1:6291 |
| `ETX039` | `=20 0000` | S1:6293 |
| `ETX040` | `=6H'''''1''7'''''` | S1:6296 |
| `ETX041` | `=40 0000` | S1:6298 |
| `ETX042` | `1` | S1:6319 |
| `EOC042` | `74100B` | S1:6334 |
| `EOC043` | `571B` | S1:6334 |
| `EOC044` | `70100B` | S1:6350 |
| `EOC045` | `114B` | S1:6350 |
| `EOC046` | `117B` | S1:6352 |
| `ETX046` | `=1777` | S1:6353 |
| `EDC046` | `4` | S1:6355 |
| `EDC047` | `6` | S1:6362 |
| `EOC047` | `760B` | S1:6365 |
| `EOC048` | `762B` | S1:6369 |
| `ETX048` | `=77777` | S1:6370 |
| `ETX049` | `=4` | S1:6373 |
| `ETX050` | `=7770 0000 7760 0000` | S1:6390 |
| `ETX051` | `2H '231'` | S1:6457 |
| `ETX052` | `8HMONITOR*` | S1:6458 |
| `ETX053` | `12H` | S1:6460 |
| `ETX054` | `6HБЭCM-6` | S1:6461 |
| `ETX055` | `6H/0` | S1:6462 |
| `ETX056` | `6H ШИФP-` | S1:6463 |
| `ETX057` | `6H00` | S1:6464 |
| `ETX058` | `36HMOHИTOPHAЯ C038ИCTEMA  '47'Д Y Б H A'47'  -` | S1:6466 |
| `ETX059` | `2` | S1:6467 |
| `ETX060` | `14 0000 0021 0001` | S1:6468 |
| `ETX061` | `4014 0003 0021 0101` | S1:6469 |
| `ETX062` | `0000 37` | S1:6470 |
| `ETX063` | `4000 0000` | S1:6472 |
| `ETX064` | `04` | S1:6473 |
| `ETX065` | `6H*DOS` | S1:6474 |
| `ETX066` | `6H'377'00000` | S1:6475 |
| `ETX067` | `6H'377''377'0000` | S1:6476 |
| `ETX068` | `6H0000'377''377'` | S1:6477 |
| `ETX069` | `21HOTCYTCTBYET П/K *NAME` | S1:6483 |
| `ETX070` | `15HOШИБKA B KAPTE-` | S1:6484 |
| `ETX071` | `15HCHECK PAHOBATO` | S1:6486 |
| `EDC071` | `47` | S1:6487 |
| `ETX072` | `19HПOBTOPHO OПPEДEЛEHO` | S1:6488 |
| `ETX073` | `20HHEПPABИЛЬHAЯ CCЫЛKA` | S1:6489 |
| `ETX074` | `18HHE OБ'47'ЯBЛEH ДИCK` | S1:6491 |
| `ETX075` | `23HБЫЛИ OШИБKИ B YK PAБOTЫ` | S1:6492 |
| `ETX076` | `18H <ЭKCПPECC-ЗAДAЧA>` | S1:6493 |
| `ETX077` | `144` | S1:6494 |

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **0**.
- TEXT-констант переименовано по содержимому: **9**.
- Смещений `LABEL+NNNB` → десятичное: **0**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_sys.txt`.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э50 | EOC042+EOC043 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:419` |
| Э63 | 502 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:201` |
| Э63 | 7 | ЗАПРОС СВЕДЕНИЙ ОБ ОБЛАСТИ | ? | 2 | `src/lib21/CHEKJOB_.mad:192`, `src/lib21/CHEKJOB_.mad:247` |
| Э63 | 765 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:187` |
| Э65 | 1 | не найдено в rukava.be | — | 2 | `src/lib21/CHEKJOB_.mad:347`, `src/lib21/CHEKJOB_.mad:357` |
| Э65 | 502 | не найдено в rukava.be | — | 2 | `src/lib21/CHEKJOB_.mad:339`, `src/lib21/CHEKJOB_.mad:444` |
| Э65 | 560 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:355` |
| Э65 | 760 | не найдено в rukava.be | — | 2 | `src/lib21/CHEKJOB_.mad:345`, `src/lib21/CHEKJOB_.mad:450` |
| Э65 | 761 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:350` |
| Э65 | 762 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:454` |
| Э72 | 4 | не найдено в rukava.be | — | 1 | `src/lib21/CHEKJOB_.mad:476` |

## Текстовые константы

Проверено 30 констант модуля `src/lib21/CHEKJOB_.mad`. Методика: `t6()` из `tools/extract_words.py` (6 бит/символ, 8 символов/слово), GOST-10859 (`gost10859.h`), ISO/ASCII (6 байт/слово). Для ASCII-Hollerith-литералов первичен TEXT-decode; для кириллических GOST-литералов — GOST-decode. Полная таблица с вердиктами — `logs/text_constants_audit.txt`.

| Константа | Декодирование (GOST / TEXT / ISO) | Источник | Вердикт |
|-----------|----------------------------------|----------|---------|
| `=6H'7''7'''''''''` | GOST `7[77[777` / TEXT `'7''7'''` / ISO `·q·\q·` | `src/lib21/CHEKJOB_.mad:44` | добавлено |
| `=6H'360'''''''''''` | GOST `7);е7777` / TEXT `'360''''` / ISO `·5··q·` | `src/lib21/CHEKJOB_.mad:51` | добавлено |
| `=6H'060'''''''''''` | GOST `7е;е7777` / TEXT `'060''''` / ISO `····q·` | `src/lib21/CHEKJOB_.mad:52` | добавлено |
| `=6H*CHE081` | GOST `+ГИЕе]@0` / TEXT `*CHE081 ` / ISO `*:%A·@` | `src/lib21/CHEKJOB_.mad:57` | добавлено |
| `=6H(` | GOST `80000000` / TEXT `(       ` / ISO ` ·····` | `src/lib21/CHEKJOB_.mad:58` | добавлено |
| `=6H` | GOST `` / TEXT `` / ISO `` | `src/lib21/CHEKJOB_.mad:61` | добавлено |
| `=6H-MU''''''` | GOST `,НХ77777` / TEXT `-MU'''''` / ISO `6·G·q·` | `src/lib21/CHEKJOB_.mad:65` | добавлено |
| `=6H     =` | GOST `<0000000` / TEXT `=       ` / ISO `t·····` | `src/lib21/CHEKJOB_.mad:66` | добавлено |
| `=6H'''''''''1''7'` | GOST `77777777` / TEXT `''''''''` / ISO `·q··q·` | `src/lib21/CHEKJOB_.mad:68` | добавлено |
| `=6H'''''1''7'''''` | GOST `77777@77` / TEXT `'''''1''` / ISO `·q····` | `src/lib21/CHEKJOB_.mad:70` | добавлено |
| `2H '231'` | GOST `7()@7000` / TEXT `'231'   ` / ISO `·$····` | `src/lib21/CHEKJOB_.mad:86` | добавлено |
| `8HMONITOR*` | GOST `НПОЙФПТ+` / TEXT `MONITOR*` / ISO `······` | `src/lib21/CHEKJOB_.mad:87` | добавлено |
| `12H` | GOST `` / TEXT `` / ISO `` | `src/lib21/CHEKJOB_.mad:88` | добавлено |
| `6HБЭCM-6` | GOST `БЭСМ-6  ` / TEXT `A]QL+&//` / ISO `··l,c·` | `src/lib21/CHEKJOB_.mad:89` | добавлено |
| `6H/0` | GOST ` е000000` / TEXT `/0      ` / ISO `=·····` | `src/lib21/CHEKJOB_.mad:90` | добавлено |
| `6H ШИФP-` | GOST `ШИФР-   ` / TEXT `XHTP+///` / ISO `··0,··` | `src/lib21/CHEKJOB_.mad:91` | добавлено |
| `6H00` | GOST `ее000000` / TEXT `00      ` / ISO `A·····` | `src/lib21/CHEKJOB_.mad:92` | добавлено |
| `36HMOHИTOPHAЯ C038ИCTEMA  '47'Д Y Б H A'47'  -` | GOST `МОНИТОРН` / TEXT `LNMHRNPM` / ISO `··h··-` | `src/lib21/CHEKJOB_.mad:93` | добавлено |
| `6H*DOS` | GOST `+ДПУ0000` / TEXT `*DOS    ` / ISO `*K····` | `src/lib21/CHEKJOB_.mad:100` | добавлено |
| `6H'377'00000` | GOST `7)[[7еее` / TEXT `'377'000` / ISO `·5····` | `src/lib21/CHEKJOB_.mad:101` | добавлено |
| `6H'377''377'0000` | GOST `7)[[77)[` / TEXT `'377''37` / ISO `·5··t·` | `src/lib21/CHEKJOB_.mad:102` | добавлено |
| `6H0000'377''377'` | GOST `ееее7)[[` / TEXT `0000'377` / ISO `A···5·` | `src/lib21/CHEKJOB_.mad:103` | добавлено |
| `21HOTCYTCTBYET П/K *NAME` | GOST `ОТСУТСТВ` / TEXT `NRQSRQRB` / ISO `·,s···` | `src/lib21/CHEKJOB_.mad:104` | добавлено |
| `15HOШИБKA B KAPTE-` | GOST `ОШИБКА В` / TEXT `NXHAJ@/B` / ISO `··!···` | `src/lib21/CHEKJOB_.mad:105` | добавлено |
| `15HCHECK PAHOBATO` | GOST `ГИЕГЛ0РБ` / TEXT `CHECK PA` / ISO `··c··!` | `src/lib21/CHEKJOB_.mad:106` | добавлено |
| `19HПOBTOPHO OПPEДEЛEHO` | GOST `ПОВТОРНО` / TEXT `ONBRNPMN` / ISO `·····n` | `src/lib21/CHEKJOB_.mad:108` | добавлено |
| `20HHEПPABИЛЬHAЯ CCЫЛKA` | GOST `НЕПРАВИЛ` / TEXT `MEOP@BHK` / ISO `·[··*+` | `src/lib21/CHEKJOB_.mad:109` | добавлено |
| `18HHE OБ'47'ЯBЛEH ДИCK` | GOST `НЕ ОБ'47` / TEXT `ME/NA;$'` / ISO `·S····` | `src/lib21/CHEKJOB_.mad:110` | добавлено |
| `23HБЫЛИ OШИБKИ B YK PAБOTЫ` | GOST `БЫЛИ ОШИ` / TEXT `A[KH/NXH` / ISO `···>·(` | `src/lib21/CHEKJOB_.mad:111` | добавлено |
| `18H <ЭKCПPECC-ЗAДAЧA>` | GOST `<ЭКСПРЕС` / TEXT `=]JQOPEQ` / ISO `w····q` | `src/lib21/CHEKJOB_.mad:112` | добавлено |

## Текстовые константы и кодировки

Второй проход аудита (2026-11-19): не расшифрованные ранее текстовые
константы в кодировках ИСО (ISO), ГОСТ, UPP/континуации (CONT).
Первичное чтение — текст литерала из листинга Дубны/dtran; 6-битные
GOST6/TEXT6 — альтернативная интерпретация машиного слова.
Методика и сверка: `docs/19-dtran-text-encodings.md`,
`tools/dtran_text.py --audit`. Полный лог — `logs/text_audit_lib21_2.txt`.

| Метка/литерал | Кодировка | Первичное чтение | Источник |
|---|---|---|---|
| `******` | ISO | `******` | `src/lib21/CHEKJOB_.mad:563` |
| `''''**` | ISO | `''''**` | `src/lib21/CHEKJOB_.mad:564` |
| `****''` | ISO | `****''` | `src/lib21/CHEKJOB_.mad:565` |
| `ЗAПPOC PECYPCA` | CONT | `ЗAПPOC PECYPCA` | `src/lib21/CHEKJOB_.mad:570` |
| `OБ'EDC071'ЯBЛEH` | CONT | `OБ'EDC071'ЯBЛEH` | `src/lib21/CHEKJOB_.mad:572` |
| `HA KAPTY-*CHE081` | CONT | `HA KAPTY-*CHE081` | `src/lib21/CHEKJOB_.mad:575` |

Добавлено декодирований: 6.
