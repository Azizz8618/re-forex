# LIBDRU_ — перекрёстные ссылки

Модуль `LIBDRU*` (исходник `libra212.l21:995-1495`). Сверка: `disasm/lib21/LIBDRU_.madlen`.

Все метки переименованы в ≤6 символов (уникальные первые 6); полные имена сохранены в `; (POLN: ...)` в `src/lib21/LIBDRU_.mad`.

## 1. Таблица символов (метки и EQU)

| Короткое имя | Полное имя (POLN) | Тип | Строка |
|---|---|---|---|
| `LIB001` | `LIBDRU*` | метка | libra212.l21:995 |
| `PER002` | `PERSO` | метка | libra212.l21:996 |
| `CBO003` | `CBOБOДHO` | метка | libra212.l21:1005 |
| `TEM004` | `TEMPORAR` | метка | libra212.l21:1006 |
| `PER005` | `PERMANEN` | метка | libra212.l21:1007 |
| `PAR006` | `PARAMT*` | метка | libra212.l21:1008 |
| `MON007` | `*MONCRD*` | метка | libra212.l21:1009 |
| `KAT008` | `KATAЛOГИ` | метка | libra212.l21:1010 |
| `WBU009` | `WBUF` | метка | libra212.l21:1011 |
| `RBU010` | `RBUF` | метка | libra212.l21:1012 |
| `NRB011` | `NRBF` | метка | libra212.l21:1013 |
| `NWB012` | `NWBF` | метка | libra212.l21:1014 |
| `NPC013` | `NPC` | метка | libra212.l21:1015 |
| `NPO014` | `NPO` | метка | libra212.l21:1016 |
| `C015` | `*C` | метка | libra212.l21:1017 |
| `LCC016` | `LCC//` | метка | libra212.l21:1021 |
| `NOP017` | `NO PARAM` | метка | libra212.l21:1042 |
| `CON018` | `CONT` | метка | libra212.l21:1050 |
| `LOO019` | `LOOPCO` | метка | libra212.l21:1066 |
| `NOT020` | `NOT/EMPT` | метка | libra212.l21:1086 |
| `NEX021` | `NEXT*TRZ` | метка | libra212.l21:1088 |
| `MLZ022` | `ML*ZONE` | метка | libra212.l21:1098 |
| `END023` | `END CATO` | метка | libra212.l21:1100 |
| `LOO024` | `LOOPC` | метка | libra212.l21:1127 |
| `NOT025` | `NOT EMPT` | метка | libra212.l21:1141 |
| `END026` | `END CAT` | метка | libra212.l21:1143 |
| `NOS027` | `NO SWING` | метка | libra212.l21:1169 |
| `LOO028` | `LOOPC2` | метка | libra212.l21:1173 |
| `NOS029` | `NO SWOP` | метка | libra212.l21:1197 |
| `COB030` | `CЛOBO 1` | метка | libra212.l21:1206 |
| `COB031` | `CЛOBO 2` | метка | libra212.l21:1214 |
| `COB032` | `CЛOBO 3` | метка | libra212.l21:1220 |
| `AYE033` | `БЫЛA YЖE` | метка | libra212.l21:1257 |
| `ECT034` | `ECTЬ EЩE` | метка | libra212.l21:1260 |
| `ISP035` | `ISPLASE` | метка | libra212.l21:1269 |
| `LBL036` | `******` | метка | libra212.l21:1275 |
| `NOS037` | `NO SHAKE` | метка | libra212.l21:1283 |
| `LDE038` | `L/DEL1` | метка | libra212.l21:1293 |
| `LDE039` | `L/DEL2` | метка | libra212.l21:1307 |
| `GOO040` | `GOOD` | метка | libra212.l21:1312 |
| `LOO041` | `LOOPWRSM` | метка | libra212.l21:1323 |
| `RDW042` | `RDWRD` | метка | libra212.l21:1328 |
| `WRW043` | `WRWRD` | метка | libra212.l21:1340 |
| `FIN044` | `FIN/SM` | метка | libra212.l21:1355 |
| `FIN045` | `FIN/REF` | метка | libra212.l21:1377 |
| `DRU046` | `DRUMFULL` | метка | libra212.l21:1384 |
| `LOO047` | `LOOPADD` | метка | libra212.l21:1391 |
| `POB048` | `ПPOBBXOД` | метка | libra212.l21:1395 |
| `HET049` | `HET BXOДA` | метка | libra212.l21:1414 |
| `FIN050` | `FIN/ADD` | метка | libra212.l21:1420 |
| `LOW051` | `LOWC` | метка | libra212.l21:1438 |
| `KAY052` | `KAПYT1` | метка | libra212.l21:1446 |
| `LIB053` | `LIBEMPTY` | метка | libra212.l21:1447 |
| `EXI054` | `EXIT` | метка | libra212.l21:1450 |
| `OVE055` | `OVERFLOW` | метка | libra212.l21:1453 |
| `KAY056` | `KAПYT` | метка | libra212.l21:1454 |
| `TOL057` | `TO LONG` | метка | libra212.l21:1455 |
| `INF058` | `INFPR` | метка | libra212.l21:1458 |
| `IR059` | `IR*` | метка | libra212.l21:1462 |
| `IW060` | `IW*` | метка | libra212.l21:1464 |
| `IWC061` | `IWC*` | метка | libra212.l21:1466 |
| `IBA062` | `IBAD` | метка | libra212.l21:1468 |
| `YCT063` | `ПYCTO` | метка | libra212.l21:1472 |
| `OO064` | `БOЛЬШOЙ` | метка | libra212.l21:1473 |
| `OXO065` | `ПЛOXO` | метка | libra212.l21:1474 |
| `OPA066` | `ПOPЧA` | метка | libra212.l21:1475 |
| `EPE067` | `ПEPEП` | метка | libra212.l21:1476 |
| `P2068` | `ПPЧ2` | метка | libra212.l21:1477 |
| `LIN069` | `LINE` | метка | libra212.l21:1478 |
| `FLD070` | `FLDIAG` | метка | libra212.l21:1480 |
| `OGR071` | `OGR` | метка | libra212.l21:1481 |
| `PLA072` | `PLACE` | метка | libra212.l21:1482 |
| `LGS073` | `LG SM` | метка | libra212.l21:1483 |
| `LGS074` | `LG SB` | метка | libra212.l21:1484 |
| `BUF075` | `W0001` | метка | libra212.l21:1485 |
| `BUF076` | `W0002` | метка | libra212.l21:1486 |
| `BUF077` | `W0003` | метка | libra212.l21:1487 |
| `AHA078` | `A HAЧ` | метка | libra212.l21:1488 |
| `SHI079` | `SHIFT` | метка | libra212.l21:1489 |
| `RET080` | `RETURN` | метка | libra212.l21:1490 |
| `LEN081` | `LENCAT` | метка | libra212.l21:1491 |
| `END082` | `ENDCTL` | метка | libra212.l21:1492 |
| `END083` | `ENDCTLO` | метка | libra212.l21:1493 |
| `FLC084` | `FLCONT` | метка | libra212.l21:1494 |
| `PER005` | `PERMANEN` | EQU = `60B` | S2:1007 |
| `TEM004` | `TEMPORAR` | EQU = `47B` | S2:1006 |
| `CBO003` | `CBOБOДHO` | EQU = `54B` | S2:1005 |
| `EDC008` | `DEC_12` | EQU = `12` | S2:1009 |
| `EDC009` | `DEC_8192` | EQU = `8192` | S2:1010 |
| `EDC010` | `DEC_1024` | EQU = `1024` | S2:1011 |
| `EDC011` | `DEC_16` | EQU = `16` | S2:1013 |
| `EDC012` | `DEC_1` | EQU = `1` | S2:1020 |
| `EDC013` | `DEC_16384` | EQU = `16384` | S2:1020 |
| `EDC014` | `DEC_16383` | EQU = `16383` | S2:1021 |
| `EDC015` | `DEC_13` | EQU = `13` | S2:1024 |
| `ETX015` | `LITERAL__670000` | EQU = `=670000` | S2:1027 |
| `EDC016` | `DEC_4` | EQU = `4` | S2:1033 |
| `EDC017` | `DEC_6` | EQU = `6` | S2:1037 |
| `ETX017` | `LITERAL__6HCONT` | EQU = `=6HCONT` | S2:1040 |
| `EDC018` | `DEC_2` | EQU = `2` | S2:1043 |
| `EDC019` | `DEC_1022` | EQU = `1022` | S2:1044 |
| `ETX019` | `LITERAL__21_20000` | EQU = `=21 20000` | S2:1047 |
| `ETX020` | `LITERAL___7773_77` | EQU = `=:7773 77` | S2:1051 |
| `ETX021` | `LITERAL__200_0000` | EQU = `=200 0000` | S2:1057 |
| `ETX022` | `LITERAL__7777_7777_7000_0037` | EQU = `=7777 7777 7000 0037` | S2:1060 |
| `EDC022` | `DEC_1023` | EQU = `1023` | S2:1061 |
| `ETX023` | `LITERAL__70_0000` | EQU = `=70 0000` | S2:1064 |
| `EDC023` | `DEC_1025` | EQU = `1025` | S2:1066 |
| `ETX024` | `LITERAL__7777_7777_7777_7777` | EQU = `=7777 7777 7777 7777` | S2:1067 |
| `EDC024` | `DEC_8182` | EQU = `8182` | S2:1077 |
| `ETX025` | `LITERAL__1` | EQU = `=1` | S2:1088 |
| `ETX026` | `LITERAL__10_0000` | EQU = `=10 0000` | S2:1090 |
| `ETX027` | `LITERAL__40_0000` | EQU = `=40 0000` | S2:1091 |
| `ETX028` | `LITERAL__7740` | EQU = `=7740` | S2:1094 |
| `ETX029` | `LITERAL__1777` | EQU = `=1777` | S2:1145 |
| `EDC029` | `DEC_18` | EQU = `18` | S2:1153 |
| `ETX030` | `LITERAL__77_76000` | EQU = `=77 76000` | S2:1158 |
| `ETX031` | `LITERAL__77_0037` | EQU = `=77 0037` | S2:1159 |
| `ETX032` | `LITERAL___001` | EQU = `=:001` | S2:1161 |
| `EDC032` | `DEC_5` | EQU = `5` | S2:1165 |
| `ETX033` | `LITERAL___2` | EQU = `=:2` | S2:1177 |
| `ETX034` | `LITERAL__1740_0000_0000_0000` | EQU = `=1740 0000 0000 0000` | S2:1180 |
| `ETX035` | `LITERAL__1740` | EQU = `=1740` | S2:1181 |
| `EDC035` | `DEC_3` | EQU = `3` | S2:1182 |
| `ETX036` | `LITERAL__0037_7700_0000_0000` | EQU = `=0037 7700 0000 0000` | S2:1185 |
| `ETX037` | `LITERAL__0000_0000_0000_3777` | EQU = `=0000 0000 0000 3777` | S2:1186 |
| `ETX038` | `LITERAL__1040` | EQU = `=1040` | S2:1188 |
| `ETX039` | `LITERAL__3` | EQU = `=3` | S2:1197 |
| `ETX040` | `LITERAL__7777` | EQU = `=7777` | S2:1207 |
| `EDC040` | `DEC_64` | EQU = `64` | S2:1210 |
| `ETX041` | `LITERAL__77777` | EQU = `=77777` | S2:1215 |
| `EDC041` | `DEC_15` | EQU = `15` | S2:1218 |
| `EDC042` | `DEC_20` | EQU = `20` | S2:1259 |
| `EDC043` | `DEC_14` | EQU = `14` | S2:1263 |
| `EDC044` | `DEC_10` | EQU = `10` | S2:1303 |
| `ETX044` | `LITERAL__37` | EQU = `=37` | S2:1313 |
| `ETX045` | `LITERAL__2000_0077_7777_7777` | EQU = `=2000 0077 7777 7777` | S2:1361 |
| `ETX046` | `LITERAL__11` | EQU = `=11` | S2:1434 |
| `ETX047` | `LITERAL___0000_0100` | EQU = `=:0000 0100` | S2:1442 |
| `EDC047` | `DEC_19` | EQU = `19` | S2:1469 |
| `ETX048` | `LIT_20H_____OTEKA__YCTA__133__231_` | EQU = `20HБИБЛИOTEKA ПYCTAЯ'133''231'` | S2:1472 |
| `ETX049` | `LIT_18H_O___O__KATA_O__133__231_` | EQU = `18HБOЛЬШOЙ KATAЛOГ'133''231'` | S2:1473 |
| `ETX050` | `LIT_36H_C_OP_EH_KATA_O__TEMPORARY_` | EQU = `36HИCПOPЧEH KATAЛOГ TEMPORARY LIBRARY'133''231'` | S2:1474 |
| `ETX051` | `LIT_24H_C_OP_EH___O__PO_PAMM___231` | EQU = `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S2:1475 |
| `ETX052` | `LIT_36H_EPE_O_HEHA_BPEMEHHA_______` | EQU = `36HПEPEПOЛHEHA BPEMEHHAЯ БИБЛИOTEKA'133''231'` | S2:1476 |
| `ETX053` | `LIT_24H_____OTEKA__C_OP_EHA__133__` | EQU = `24HБИБЛИOTEKA ИCПOPЧEHA '133''231'` | S2:1477 |
| `ETX054` | `LIT_20` | EQU = `20` | S2:1478 |
| `ETX055` | `LIT_1H_231_` | EQU = `1H'231'` | S2:1479 |
| `ETX056` | `LIT_1` | EQU = `1` | S2:1481 |

## 2. Перекрёстные ссылки (определение → использования)

| Символ | Короткое | Использования (строка: операнд) |
|---|---|---|
| `******` | `LBL036` | 1271:`******` |
| `*MONCRD*` | `MON007` | 1039:`*MONCRD*` |
| `A HAЧ` | `AHA078` | 1258:`A HAЧ`; 1285:`A HAЧ`; 1291:`A HAЧ`; 1298:`A HAЧ` |
| `CBOБOДHO` | `CBO003` | 1048:`CBOБOДHO`; 1157:`CBOБOДHO`; 1163:`CBOБOДHO`; 1363:`CBOБOДHO`; 1368:`CBOБOДHO`; 1374:`CBOБOДHO`; 1375:`CBOБOДHO`; 1426:`CBOБOДHO` |
| `CONT` | `CON018` | 1046:`CONT` |
| `CЛOBO 1` | `COB030` | 1211:`CЛOBO 1` |
| `CЛOBO 2` | `COB031` | 1219:`CЛOBO 2` |
| `DRUMFULL` | `DRU046` | 1378:`DRUMFULL` |
| `ECTЬ EЩE` | `ECT034` | 1274:`ECTЬ EЩE` |
| `END CAT` | `END026` | 1128:`END CAT` |
| `END CATO` | `END023` | 1068:`END CATO`; 1070:`END CATO` |
| `ENDCTL` | `END082` | 1144:`ENDCTL`; 1288:`ENDCTL`; 1300:`ENDCTL`; 1302:`ENDCTL`; 1388:`ENDCTL` |
| `ENDCTLO` | `END083` | 1101:`ENDCTLO` |
| `EXIT` | `EXI054` | 1035:`EXIT`; 1438:`EXIT` |
| `FIN/ADD` | `FIN050` | 1393:`FIN/ADD` |
| `FIN/REF` | `FIN045` | 1175:`FIN/REF` |
| `FIN/SM` | `FIN044` | 1323:`FIN/SM` |
| `FLCONT` | `FLC084` | 1026:`FLCONT`; 1041:`FLCONT`; 1045:`FLCONT` |
| `FLDIAG` | `FLD070` | 1019:`FLDIAG`; 1251:`FLDIAG`; 1256:`FLDIAG` |
| `GOOD` | `GOO040` | 1246:`GOOD` |
| `HET BXOДA` | `HET049` | 1397:`HET BXOДA` |
| `IBAD` | `IBA062` | 1267:`IBAD`; 1278:`IBAD` |
| `INFPR` | `INF058` | 1254:`INFPR`; 1449:`INFPR`; 1456:`INFPR` |
| `IR*` | `IR059` | 1053:`IR*`; 1112:`IR*`; 1190:`IR*` |
| `ISPLASE` | `ISP035` | 1266:`ISPLASE` |
| `IW*` | `IW060` | 1160:`IW*` |
| `IWC*` | `IWC061` | 1436:`IWC*` |
| `KATAЛOГИ` | `KAT008` | 1021:`KATAЛOГИ+16383` |
| `KAПYT` | `KAY056` | 1058:`KAПYT`; 1062:`KAПYT`; 1065:`KAПYT` |
| `KAПYT1` | `KAY052` | 1117:`KAПYT1`; 1121:`KAПYT1`; 1124:`KAПYT1` |
| `L/DEL1` | `LDE038` | 1297:`L/DEL1` |
| `L/DEL2` | `LDE039` | 1310:`L/DEL2` |
| `LCC//` | `LCC016` | 1023:`LCC//` |
| `LG SB` | `LGS074` | 1200:`LG SB`; 1226:`LG SB`; 1227:`LG SB`; 1231:`LG SB`; 1232:`LG SB`; 1237:`LG SB`; 1238:`LG SB`; 1244:`LG SB` |
| `LG SM` | `LGS073` | 1198:`LG SM`; 1208:`LG SM`; 1209:`LG SM`; 1216:`LG SM`; 1217:`LG SM`; 1224:`LG SM`; 1225:`LG SM`; 1235:`LG SM`; 1236:`LG SM`; 1312:`LG SM`; 1316:`LG SM`; 1373:`LG SM` |
| `LIBDRU*` | `LIB001` | 1495:`LIBDRU*` |
| `LIBEMPTY` | `LIB053` | 1126:`LIBEMPTY` |
| `LINE` | `LIN069` | 1262:`LINE`; 1468:`LINE`; 1469:`LINE+19` |
| `LOOPADD` | `LOO047` | 1402:`LOOPADD`; 1404:`LOOPADD`; 1407:`LOOPADD`; 1413:`LOOPADD`; 1419:`LOOPADD` |
| `LOOPC` | `LOO024` | 1142:`LOOPC` |
| `LOOPC2` | `LOO028` | 1178:`LOOPC2`; 1311:`LOOPC2`; 1376:`LOOPC2` |
| `LOOPCO` | `LOO019` | 1087:`LOOPCO` |
| `LOOPWRSM` | `LOO041` | 1327:`LOOPWRSM` |
| `LOWC` | `LOW051` | 1445:`LOWC` |
| `ML*ZONE` | `MLZ022` | 1092:`ML*ZONE` |
| `NEXT*TRZ` | `NEX021` | 1083:`NEXT*TRZ`; 1138:`NEXT*TRZ`; 1335:`NEXT*TRZ`; 1352:`NEXT*TRZ`; 1443:`NEXT*TRZ` |
| `NO PARAM` | `NOP017` | 1031:`NO PARAM`; 1036:`NO PARAM` |
| `NO SHAKE` | `NOS037` | 1276:`NO SHAKE` |
| `NO SWING` | `NOS027` | 1167:`NO SWING` |
| `NO SWOP` | `NOS029` | 1193:`NO SWOP` |
| `NOT EMPT` | `NOT025` | 1135:`NOT EMPT` |
| `NOT/EMPT` | `NOT020` | 1080:`NOT/EMPT` |
| `NPC` | `NPC013` | 1466:`NPC` |
| `NRBF` | `NRB011` | 1462:`NRBF` |
| `NWBF` | `NWB012` | 1464:`NWBF` |
| `OVERFLOW` | `OVE055` | 1349:`OVERFLOW`; 1382:`OVERFLOW` |
| `PARAMT*` | `PAR006` | 1030:`PARAMT*`; 1034:`PARAMT*`; 1038:`PARAMT*` |
| `PERMANEN` | `PER005` | 1049:`PERMANEN-TEMPORAR` |
| `PLACE` | `PLA072` | 1028:`PLACE`; 1032:`PLACE`; 1111:`PLACE`; 1189:`PLACE` |
| `RBUF` | `RBU010` | 1013:`(RBUF)16`; 1044:`RBUF-1022`; 1079:`-RBUF`; 1086:`RBUF`; 1110:`RBUF-1022`; 1134:`-RBUF`; 1141:`RBUF`; 1151:`RBUF+2`; 1183:`RBUF`; 1318:`-RBUF`; 1329:`RBUF` |
| `RDWRD` | `RDW042` | 1324:`RDWRD` |
| `RETURN` | `RET080` | 1025:`RETURN`; 1451:`RETURN` |
| `SHIFT` | `SHI079` | 1286:`SHIFT`; 1293:`SHIFT`; 1301:`SHIFT`; 1304:`SHIFT` |
| `TEMPORAR` | `TEM004` | 1049:`PERMANEN-TEMPORAR`; 1050:`TEMPORAR` |
| `TO LONG` | `TOL057` | 1078:`TO LONG`; 1435:`TO LONG` |
| `W0001` | `BUF075` | 1054:`W0001`; 1055:`W0001`; 1082:`W0001`; 1084:`W0001`; 1085:`W0001`; 1113:`W0001`; 1114:`W0001`; 1137:`W0001`; 1139:`W0001`; 1140:`W0001`; 1192:`W0001`; 1196:`W0001` … (+7) |
| `W0002` | `BUF076` | 1191:`W0002`; 1194:`W0002`; 1195:`W0002` |
| `W0003` | `BUF077` | 1162:`W0003`; 1168:`W0003`; 1170:`W0003`; 1172:`W0003`; 1346:`W0003`; 1350:`W0003`; 1351:`W0003`; 1353:`W0003`; 1379:`W0003`; 1383:`W0003` |
| `WBUF` | `WBU009` | 1014:`(WBUF)16`; 1341:`WBUF` |
| `WRWRD` | `WRW043` | 1326:`WRWRD` |
| `БOЛЬШOЙ` | `OO064` | 1454:`ПЛOXO-БOЛЬШOЙ`; 1455:`БOЛЬШOЙ` |
| `БЫЛA YЖE` | `AYE033` | 1252:`БЫЛA YЖE` |
| `ПEPEП` | `EPE067` | 1453:`ПEPEП-ПЛOXO` |
| `ПOPЧA` | `OPA066` | 1253:`ПOPЧA` |
| `ПPOBBXOД` | `POB048` | 1399:`ПPOBBXOД` |
| `ПPЧ2` | `P2068` | 1446:`ПPЧ2-ПYCTO` |
| `ПYCTO` | `YCT063` | 1446:`ПPЧ2-ПYCTO`; 1448:`ПYCTO` |
| `ПЛOXO` | `OXO065` | 1453:`ПEPEП-ПЛOXO`; 1454:`ПЛOXO-БOЛЬШOЙ` |

## 3. Вызовы и переходы (VJM / CALL / UJ)

| Строка | Команда | Операнд |
|---|---|---|
| S2:1030 | `VJM` | `PARAMT*` |
| S2:1034 | `VJM` | `PARAMT*` |
| S2:1038 | `VJM` | `PARAMT*` |
| S2:1083 | `VJM` | `NEXT*TRZ` |
| S2:1087 | `UJ` | `LOOPCO` |
| S2:1097 | `UJ` | `(через индексный регистр)` |
| S2:1099 | `UJ` | `(через индексный регистр)` |
| S2:1138 | `VJM` | `NEXT*TRZ` |
| S2:1142 | `UJ` | `LOOPC` |
| S2:1156 | `CALL` | `PRINT8` |
| S2:1264 | `CALL` | `PT6/G` |
| S2:1311 | `UJ` | `LOOPC2` |
| S2:1324 | `VJM` | `RDWRD` |
| S2:1326 | `VJM` | `WRWRD` |
| S2:1327 | `UJ` | `LOOPWRSM` |
| S2:1335 | `VJM` | `NEXT*TRZ` |
| S2:1339 | `UJ` | `(через индексный регистр)` |
| S2:1352 | `VJM` | `NEXT*TRZ` |
| S2:1354 | `UJ` | `(через индексный регистр)` |
| S2:1376 | `UJ` | `LOOPC2` |
| S2:1413 | `UJ` | `LOOPADD` |
| S2:1419 | `UJ` | `LOOPADD` |
| S2:1443 | `VJM` | `NEXT*TRZ` |
| S2:1445 | `UJ` | `LOWC` |
| S2:1452 | `UJ` | `(через индексный регистр)` |

## 4. Внешние символы (не определены в модуле)

- `PRINT8`
- `PT6/G`

## 5. Литералы → EQU

| EQU | Значение | Строка |
|---|---|---|
| `PER005` | `60B` | S2:1007 |
| `TEM004` | `47B` | S2:1006 |
| `CBO003` | `54B` | S2:1005 |
| `EDC008` | `12` | S2:1009 |
| `EDC009` | `8192` | S2:1010 |
| `EDC010` | `1024` | S2:1011 |
| `EDC011` | `16` | S2:1013 |
| `EDC012` | `1` | S2:1020 |
| `EDC013` | `16384` | S2:1020 |
| `EDC014` | `16383` | S2:1021 |
| `EDC015` | `13` | S2:1024 |
| `ETX015` | `=670000` | S2:1027 |
| `EDC016` | `4` | S2:1033 |
| `EDC017` | `6` | S2:1037 |
| `ETX017` | `=6HCONT` | S2:1040 |
| `EDC018` | `2` | S2:1043 |
| `EDC019` | `1022` | S2:1044 |
| `ETX019` | `=21 20000` | S2:1047 |
| `ETX020` | `=:7773 77` | S2:1051 |
| `ETX021` | `=200 0000` | S2:1057 |
| `ETX022` | `=7777 7777 7000 0037` | S2:1060 |
| `EDC022` | `1023` | S2:1061 |
| `ETX023` | `=70 0000` | S2:1064 |
| `EDC023` | `1025` | S2:1066 |
| `ETX024` | `=7777 7777 7777 7777` | S2:1067 |
| `EDC024` | `8182` | S2:1077 |
| `ETX025` | `=1` | S2:1088 |
| `ETX026` | `=10 0000` | S2:1090 |
| `ETX027` | `=40 0000` | S2:1091 |
| `ETX028` | `=7740` | S2:1094 |
| `ETX029` | `=1777` | S2:1145 |
| `EDC029` | `18` | S2:1153 |
| `ETX030` | `=77 76000` | S2:1158 |
| `ETX031` | `=77 0037` | S2:1159 |
| `ETX032` | `=:001` | S2:1161 |
| `EDC032` | `5` | S2:1165 |
| `ETX033` | `=:2` | S2:1177 |
| `ETX034` | `=1740 0000 0000 0000` | S2:1180 |
| `ETX035` | `=1740` | S2:1181 |
| `EDC035` | `3` | S2:1182 |
| `ETX036` | `=0037 7700 0000 0000` | S2:1185 |
| `ETX037` | `=0000 0000 0000 3777` | S2:1186 |
| `ETX038` | `=1040` | S2:1188 |
| `ETX039` | `=3` | S2:1197 |
| `ETX040` | `=7777` | S2:1207 |
| `EDC040` | `64` | S2:1210 |
| `ETX041` | `=77777` | S2:1215 |
| `EDC041` | `15` | S2:1218 |
| `EDC042` | `20` | S2:1259 |
| `EDC043` | `14` | S2:1263 |
| `EDC044` | `10` | S2:1303 |
| `ETX044` | `=37` | S2:1313 |
| `ETX045` | `=2000 0077 7777 7777` | S2:1361 |
| `ETX046` | `=11` | S2:1434 |
| `ETX047` | `=:0000 0100` | S2:1442 |
| `EDC047` | `19` | S2:1469 |
| `ETX048` | `20HБИБЛИOTEKA ПYCTAЯ'133''231'` | S2:1472 |
| `ETX049` | `18HБOЛЬШOЙ KATAЛOГ'133''231'` | S2:1473 |
| `ETX050` | `36HИCПOPЧEH KATAЛOГ TEMPORARY LIBRARY'133''231'` | S2:1474 |
| `ETX051` | `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S2:1475 |
| `ETX052` | `36HПEPEПOЛHEHA BPEMEHHAЯ БИБЛИOTEKA'133''231'` | S2:1476 |
| `ETX053` | `24HБИБЛИOTEKA ИCПOPЧEHA '133''231'` | S2:1477 |
| `ETX054` | `20` | S2:1478 |
| `ETX055` | `1H'231'` | S2:1479 |
| `ETX056` | `1` | S2:1481 |

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **3**.
- TEXT-констант переименовано по содержимому: **0**.
- Смещений `LABEL+NNNB` → десятичное: **0**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_core.txt`.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э70 | BUF075 | не найдено в rukava.be | — | 6 | `src/lib21/LIBDRU_.mad:137`, `src/lib21/LIBDRU_.mad:167`, `src/lib21/LIBDRU_.mad:196`, `src/lib21/LIBDRU_.mad:222`, `src/lib21/LIBDRU_.mad:419`, `src/lib21/LIBDRU_.mad:521` |
| Э70 | BUF076 | не найдено в rukava.be | — | 1 | `src/lib21/LIBDRU_.mad:276` |
| Э70 | BUF077 | не найдено в rukava.be | — | 3 | `src/lib21/LIBDRU_.mad:250`, `src/lib21/LIBDRU_.mad:432`, `src/lib21/LIBDRU_.mad:465` |

## Текстовые константы

Проверено 8 констант модуля `src/lib21/LIBDRU_.mad`. Методика: `t6()` из `tools/extract_words.py` (6 бит/символ, 8 символов/слово), GOST-10859 (`gost10859.h`), ISO/ASCII (6 байт/слово). Для ASCII-Hollerith-литералов первичен TEXT-decode; для кириллических GOST-литералов — GOST-decode. Полная таблица с вердиктами — `logs/text_constants_audit.txt`.

| Константа | Декодирование (GOST / TEXT / ISO) | Источник | Вердикт |
|-----------|----------------------------------|----------|---------|
| `=6HCONT` | GOST `ГПОФ0000` / TEXT `CONT    ` / ISO `······` | `src/lib21/LIBDRU_.mad:26` | добавлено |
| `20HБИБЛИOTEKA ПYCTAЯ'133''231'` | GOST `БИБЛИОТЕ` / TEXT `AHAKHNRE` / ISO `··k···` | `src/lib21/LIBDRU_.mad:68` | добавлено |
| `18HБOЛЬШOЙ KATAЛOГ'133''231'` | GOST `БОЛЬШОЙ ` / TEXT `ANK\XNI/` / ISO `·····O` | `src/lib21/LIBDRU_.mad:69` | добавлено |
| `36HИCПOPЧEH KATAЛOГ TEMPORARY LIBRARY'133''231'` | GOST `ИСПОРЧЕН` / TEXT `HQONPWEM` / ISO `····ym` | `src/lib21/LIBDRU_.mad:70` | добавлено |
| `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | GOST `ИСПОРЧЕН` / TEXT `HQONPWEM` / ISO `····ym` | `src/lib21/LIBDRU_.mad:71` | добавлено |
| `36HПEPEПOЛHEHA BPEMEHHAЯ БИБЛИOTEKA'133''231'` | GOST `ПЕРЕПОЛН` / TEXT `OEPEONKM` / ISO `·\%···` | `src/lib21/LIBDRU_.mad:72` | добавлено |
| `24HБИБЛИOTEKA ИCПOPЧEHA '133''231'` | GOST `БИБЛИОТЕ` / TEXT `AHAKHNRE` / ISO `··k···` | `src/lib21/LIBDRU_.mad:73` | добавлено |
| `1H'231'` | GOST `7()@7000` / TEXT `'231'   ` / ISO `·$····` | `src/lib21/LIBDRU_.mad:75` | добавлено |

