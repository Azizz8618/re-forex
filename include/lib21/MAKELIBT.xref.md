# MAKELIBT — перекрёстные ссылки

Модуль `MAKELIBT` (исходник `libra212.l21:5240-6117`). Сверка: `disasm/lib21/MAKELIBT.madlen`.

Все метки переименованы в ≤6 символов (уникальные первые 6); полные имена сохранены в `; (POLN: ...)` в `src/lib21/MAKELIBT.mad`.

## 1. Таблица символов (метки и EQU)

| Короткое имя | Полное имя (POLN) | Тип | Строка |
|---|---|---|---|
| `MAK001` | `MAKELIBT` | метка | libra212.l21:5240 |
| `MON002` | `MONITOR*` | метка | libra212.l21:5262 |
| `DAT003` | `DATA*` | метка | libra212.l21:5263 |
| `PRI004` | `PRINT8` | метка | libra212.l21:5264 |
| `AOC005` | `A/OCTDEC` | метка | libra212.l21:5265 |
| `PAR006` | `PARAMT*` | метка | libra212.l21:5266 |
| `MON007` | `*MONCRD*` | метка | libra212.l21:5267 |
| `OUT008` | `OUT*OUT` | метка | libra212.l21:5268 |
| `LIB009` | `LIB**KAT` | метка | libra212.l21:5269 |
| `RBU010` | `RBUF` | метка | libra212.l21:5273 |
| `EXC011` | `EXCLUDE` | метка | libra212.l21:5274 |
| `KAT012` | `KAT/P` | метка | libra212.l21:5275 |
| `RBP013` | `RB/P` | метка | libra212.l21:5276 |
| `WBP014` | `WB/P` | метка | libra212.l21:5277 |
| `PT6015` | `PT6/G` | метка | libra212.l21:5278 |
| `C016` | `*C` | метка | libra212.l21:5279 |
| `CLC017` | `CL/COM` | метка | libra212.l21:5299 |
| `LPN018` | `L/PNTT` | метка | libra212.l21:5320 |
| `TES019` | `TEST*IW` | метка | libra212.l21:5335 |
| `GIV020` | `GIV*OГP` | метка | libra212.l21:5339 |
| `LSC021` | `LS/COM` | метка | libra212.l21:5348 |
| `NOP022` | `NO/PARAM` | метка | libra212.l21:5354 |
| `NOP023` | `NO*PARAM` | метка | libra212.l21:5356 |
| `NOT024` | `NOT*TEMP` | метка | libra212.l21:5363 |
| `LCC025` | `L///CC` | метка | libra212.l21:5384 |
| `LIB026` | `LIB/LOOP` | метка | libra212.l21:5389 |
| `LCH027` | `L/CH*CTL` | метка | libra212.l21:5426 |
| `NOT028` | `NO*TMPL` | метка | libra212.l21:5433 |
| `ECH029` | `E/CH*CTL` | метка | libra212.l21:5438 |
| `OKC030` | `OK*CTL` | метка | libra212.l21:5441 |
| `PCH031` | `P/CH*CTL` | метка | libra212.l21:5443 |
| `KAT032` | `KAT*NEW` | метка | libra212.l21:5452 |
| `LCH033` | `L/CH*EXC` | метка | libra212.l21:5457 |
| `ECH034` | `E/CH*EXC` | метка | libra212.l21:5463 |
| `LCH035` | `L/CH*ECT` | метка | libra212.l21:5465 |
| `MAK036` | `MAK**EXC` | метка | libra212.l21:5471 |
| `MAK037` | `MAK//EXC` | метка | libra212.l21:5487 |
| `NOD038` | `NO*D*E` | метка | libra212.l21:5493 |
| `NOC039` | `NO*CH*EX` | метка | libra212.l21:5497 |
| `SHI040` | `SHI*ENTR` | метка | libra212.l21:5499 |
| `SHI041` | `SHI*FIN` | метка | libra212.l21:5508 |
| `ISE042` | `IS***EXC` | метка | libra212.l21:5521 |
| `ALL043` | `ALL//LIB` | метка | libra212.l21:5527 |
| `LWB044` | `L/WBF` | метка | libra212.l21:5530 |
| `LOO045` | `LOOPC2` | метка | libra212.l21:5563 |
| `NOS046` | `NO//SWOP` | метка | libra212.l21:5597 |
| `COB047` | `CЛOBO 1` | метка | libra212.l21:5600 |
| `COB048` | `CЛOBO 2` | метка | libra212.l21:5608 |
| `COB049` | `CЛOBO 3` | метка | libra212.l21:5616 |
| `AYE050` | `БЫЛA YЖE` | метка | libra212.l21:5644 |
| `ECT051` | `ECTЬ EЩE` | метка | libra212.l21:5647 |
| `ISP052` | `ISPLASE` | метка | libra212.l21:5656 |
| `LBL053` | `******` | метка | libra212.l21:5662 |
| `NOS054` | `NO SHAKE` | метка | libra212.l21:5670 |
| `LDE055` | `L/DEL1` | метка | libra212.l21:5680 |
| `LDE056` | `L/DEL2` | метка | libra212.l21:5694 |
| `SMG057` | `SM//GOOD` | метка | libra212.l21:5699 |
| `LOO058` | `LOOP/RW` | метка | libra212.l21:5719 |
| `CON059` | `CONT///` | метка | libra212.l21:5735 |
| `CON060` | `CONT/R` | метка | libra212.l21:5737 |
| `OKW061` | `БЛOK/W` | метка | libra212.l21:5750 |
| `LCW062` | `L/CWB` | метка | libra212.l21:5755 |
| `CON063` | `CONT/W` | метка | libra212.l21:5759 |
| `FIN064` | `FIN*SM` | метка | libra212.l21:5771 |
| `LWR065` | `LW/REF` | метка | libra212.l21:5776 |
| `DOR066` | `DO/REF` | метка | libra212.l21:5795 |
| `GVR067` | `GV/REF` | метка | libra212.l21:5802 |
| `PTR068` | `PT/REF` | метка | libra212.l21:5809 |
| `PTR069` | `PT*REF` | метка | libra212.l21:5814 |
| `WWR070` | `WW/RF` | метка | libra212.l21:5817 |
| `CON071` | `CONT/F` | метка | libra212.l21:5827 |
| `ELW072` | `ELW/REF` | метка | libra212.l21:5828 |
| `FIN073` | `FIN**LIB` | метка | libra212.l21:5851 |
| `HET074` | `HET/CБ` | метка | libra212.l21:5858 |
| `CON075` | `CON/DO` | метка | libra212.l21:5864 |
| `ADR076` | `L/0001` | метка | libra212.l21:5866 |
| `LOO077` | `LOOP/F` | метка | libra212.l21:5875 |
| `NXT078` | `NXT/R` | метка | libra212.l21:5885 |
| `SER079` | `SERCH*R` | метка | libra212.l21:5890 |
| `CHE080` | `CH*ENT/R` | метка | libra212.l21:5900 |
| `LSS081` | `L/SS*` | метка | libra212.l21:5918 |
| `WSR082` | `WSR*` | метка | libra212.l21:5925 |
| `R00083` | `R*001` | метка | libra212.l21:5943 |
| `RNX084` | `R/NXTR` | метка | libra212.l21:5944 |
| `ERR085` | `ERR*LIBT` | метка | libra212.l21:5959 |
| `MAO086` | `MAЛO*MЛ` | метка | libra212.l21:5975 |
| `KAT087` | `KAT*OVFL` | метка | libra212.l21:5979 |
| `ERR088` | `ERR*CALL` | метка | libra212.l21:5981 |
| `WRA089` | `WR/ALL` | метка | libra212.l21:5985 |
| `LWC090` | `LWCMNT` | метка | libra212.l21:6002 |
| `LWC091` | `L/WCT` | метка | libra212.l21:6008 |
| `IBA092` | `IBAD` | метка | libra212.l21:6051 |
| `INF093` | `INF` | метка | libra212.l21:6055 |
| `DAT094` | `W0004*` | метка | libra212.l21:6059 |
| `DAT095` | `W0005*` | метка | libra212.l21:6061 |
| `IWR096` | `IW*R` | метка | libra212.l21:6063 |
| `CWC097` | `CWCAT` | метка | libra212.l21:6065 |
| `CWW098` | `CWWD` | метка | libra212.l21:6067 |
| `TO099` | `ИTOГ` | метка | libra212.l21:6069 |
| `LIN100` | `LINE` | метка | libra212.l21:6070 |
| `OPA101` | `ПOPЧA` | метка | libra212.l21:6072 |
| `OHA102` | `ЗOHA*` | метка | libra212.l21:6073 |
| `TCK103` | `T*ИCKЛ` | метка | libra212.l21:6074 |
| `MAO104` | `MAЛO/MЛ` | метка | libra212.l21:6075 |
| `TBA105` | `T*BADLIB` | метка | libra212.l21:6076 |
| `OHA106` | `ЗOHA/` | метка | libra212.l21:6077 |
| `TER107` | `T*ERRC` | метка | libra212.l21:6079 |
| `BIG108` | `BIG*KT` | метка | libra212.l21:6080 |
| `PRO109` | `PROGRAM` | метка | libra212.l21:6081 |
| `SVN110` | `SVNEW` | метка | libra212.l21:6082 |
| `FLM111` | `FL/MAL` | метка | libra212.l21:6083 |
| `SHI112` | `SHIFT` | метка | libra212.l21:6084 |
| `AHA113` | `A HAЧ` | метка | libra212.l21:6085 |
| `ARE114` | `A/REF` | метка | libra212.l21:6086 |
| `ADR115` | `ADR/REF` | метка | libra212.l21:6087 |
| `END116` | `END//KAT` | метка | libra212.l21:6088 |
| `BEG117` | `BEG*DFT` | метка | libra212.l21:6089 |
| `TEK118` | `TEK*ADR` | метка | libra212.l21:6090 |
| `LGS119` | `LG SM` | метка | libra212.l21:6091 |
| `AO120` | `ЗAГOЛ` | метка | libra212.l21:6092 |
| `OOH121` | `OБOЗH` | метка | libra212.l21:6093 |
| `KOM122` | `KOMMEHT` | метка | libra212.l21:6094 |
| `PE2123` | `PEЗ*2` | метка | libra212.l21:6095 |
| `SET124` | `SET` | метка | libra212.l21:6096 |
| `DAT125` | `DATA` | метка | libra212.l21:6097 |
| `LON126` | `LONG/ID` | метка | libra212.l21:6098 |
| `KOM127` | `KOMAHДЫ` | метка | libra212.l21:6099 |
| `BSS128` | `BSS` | метка | libra212.l21:6100 |
| `KOH129` | `KOHCT` | метка | libra212.l21:6101 |
| `PUK130` | `P/UKAZ` | метка | libra212.l21:6102 |
| `OPA131` | `*OГPAH*` | метка | libra212.l21:6103 |
| `BUF132` | `W0001` | метка | libra212.l21:6104 |
| `BUF133` | `W0002` | метка | libra212.l21:6105 |
| `BUF134` | `W0003` | метка | libra212.l21:6106 |
| `BUF135` | `W0004` | метка | libra212.l21:6107 |
| `BUF136` | `W0005` | метка | libra212.l21:6108 |
| `CBO137` | `CBOБOДHO` | метка | libra212.l21:6109 |
| `FLD138` | `FLDIAG` | метка | libra212.l21:6110 |
| `COM139` | `COMMENT` | метка | libra212.l21:6111 |
| `NPE140` | `N/PERSO` | метка | libra212.l21:6112 |
| `FLT141` | `FL/TEMPO` | метка | libra212.l21:6113 |
| `FLT142` | `FL*TEMPO` | метка | libra212.l21:6114 |
| `IWN143` | `IWNEW` | метка | libra212.l21:6115 |
| `LIS144` | `LIST` | метка | libra212.l21:6116 |
| `RBU010` | `RBUF` | EQU = `CCЫЛKИ` | S2:5273 |
| `EDC014` | `DEC_2` | EQU = `2` | S2:5263 |
| `EDC015` | `DEC_12` | EQU = `12` | S2:5267 |
| `EDC016` | `DEC_1` | EQU = `1` | S2:5268 |
| `EDC017` | `DEC_2048` | EQU = `2048` | S2:5269 |
| `EDC018` | `DEC_1024` | EQU = `1024` | S2:5270 |
| `EDC019` | `DEC_16` | EQU = `16` | S2:5275 |
| `EDC020` | `DEC_1023` | EQU = `1023` | S2:5286 |
| `ETX020` | `LITERAL__1` | EQU = `=1` | S2:5287 |
| `ETX021` | `LITERAL__211_2000` | EQU = `=211 2000` | S2:5289 |
| `ETX022` | `LITERAL__400` | EQU = `=400` | S2:5291 |
| `ETX023` | `LITERAL__66_0000` | EQU = `=66 0000` | S2:5293 |
| `EDC023` | `DEC_7` | EQU = `7` | S2:5295 |
| `EDC024` | `DEC_11` | EQU = `11` | S2:5297 |
| `ETX024` | `LITERAL__6H` | EQU = `=6H` | S2:5298 |
| `EDC025` | `DEC_10` | EQU = `10` | S2:5302 |
| `ETX025` | `LITERAL__6H___________` | EQU = `=6H''''''''''-` | S2:5305 |
| `ETX026` | `LITERAL__6H___________` | EQU = `=6H''''''''''(` | S2:5309 |
| `EDC026` | `DEC_4` | EQU = `4` | S2:5312 |
| `ETX027` | `LITERAL__6H___________` | EQU = `=6H'''''''''')` | S2:5328 |
| `ETX028` | `LITERAL__10_0000` | EQU = `=10 0000` | S2:5335 |
| `ETX029` | `LITERAL__40_0000` | EQU = `=40 0000` | S2:5336 |
| `EDC029` | `DEC_5` | EQU = `5` | S2:5340 |
| `ETX030` | `LITERAL__21_0000` | EQU = `=21 0000` | S2:5359 |
| `EDC030` | `DEC_3` | EQU = `3` | S2:5366 |
| `ETX031` | `LITERAL__6` | EQU = `=6` | S2:5369 |
| `EDC031` | `DEC_2047` | EQU = `2047` | S2:5383 |
| `ETX032` | `LITERAL__7777_7777_7777_7777` | EQU = `=7777 7777 7777 7777` | S2:5387 |
| `EDC032` | `DEC_64` | EQU = `64` | S2:5393 |
| `EDC033` | `DEC_38` | EQU = `38` | S2:5393 |
| `ETX033` | `LITERAL__100_0000_0001` | EQU = `=100 0000 0001` | S2:5407 |
| `ETX034` | `LITERAL__200_0000` | EQU = `=200 0000` | S2:5412 |
| `ETX035` | `LITERAL__7777_7777_7000_0037` | EQU = `=7777 7777 7000 0037` | S2:5415 |
| `ETX036` | `LITERAL__70_0000` | EQU = `=70 0000` | S2:5419 |
| `EDC036` | `DEC_1022` | EQU = `1022` | S2:5424 |
| `ETX037` | `LITERAL___4` | EQU = `=:4` | S2:5429 |
| `ETX038` | `LITERAL___2` | EQU = `=:2` | S2:5473 |
| `ETX039` | `LITERAL__7743_7777_7770_0000` | EQU = `=7743 7777 7770 0000` | S2:5480 |
| `EDC039` | `DEC_13` | EQU = `13` | S2:5490 |
| `ETX040` | `LITERAL__7743_7777_7777_7777` | EQU = `=7743 7777 7777 7777` | S2:5513 |
| `EDC040` | `DEC_2032` | EQU = `2032` | S2:5519 |
| `EDC041` | `DEC_14` | EQU = `14` | S2:5523 |
| `ETX041` | `LITERAL___0034` | EQU = `=:0034` | S2:5570 |
| `ETX042` | `LITERAL__7` | EQU = `=7` | S2:5571 |
| `ETX043` | `LITERAL___1740` | EQU = `=:1740` | S2:5578 |
| `ETX044` | `LITERAL__1740` | EQU = `=1740` | S2:5579 |
| `ETX045` | `LITERAL___0003_77` | EQU = `=:0003 77` | S2:5583 |
| `ETX046` | `LITERAL__377` | EQU = `=377` | S2:5584 |
| `ETX047` | `LITERAL__7740` | EQU = `=7740` | S2:5585 |
| `ETX048` | `LITERAL__7777` | EQU = `=7777` | S2:5586 |
| `ETX049` | `LITERAL__77777` | EQU = `=77777` | S2:5609 |
| `EDC049` | `DEC_15` | EQU = `15` | S2:5612 |
| `EDC050` | `DEC_20` | EQU = `20` | S2:5646 |
| `ETX050` | `LITERAL__3` | EQU = `=3` | S2:5704 |
| `ETX051` | `LITERAL__37` | EQU = `=37` | S2:5710 |
| `ETX052` | `LITERAL__77740` | EQU = `=77740` | S2:5711 |
| `EOC052` | `OCT_17` | EQU = `17B` | S2:5716 |
| `EOC053` | `OCT_11` | EQU = `11B` | S2:5717 |
| `ETX053` | `LITERAL__700_0000` | EQU = `=700 0000` | S2:5781 |
| `ETX054` | `LITERAL__2000_0000` | EQU = `=2000 0000` | S2:5796 |
| `ETX055` | `LITERAL___7777_7777` | EQU = `=:7777 7777` | S2:5799 |
| `EDC055` | `DEC_24` | EQU = `24` | S2:5803 |
| `EOC055` | `OCT_4000` | EQU = `4000B` | S2:5805 |
| `EDC056` | `DEC_42` | EQU = `42` | S2:5811 |
| `ETX056` | `LITERAL__12` | EQU = `=12` | S2:5812 |
| `ETX057` | `LITERAL__7741` | EQU = `=7741` | S2:5822 |
| `ETX058` | `LITERAL__2000_0077_7777_7777` | EQU = `=2000 0077 7777 7777` | S2:5833 |
| `ETX059` | `LITERAL__77_76000` | EQU = `=77 76000` | S2:5841 |
| `ETX060` | `LITERAL___0037_77` | EQU = `=:0037 77` | S2:5842 |
| `EDC060` | `DEC_3071` | EQU = `3071` | S2:5865 |
| `EDC061` | `DEC_48` | EQU = `48` | S2:5869 |
| `EDC062` | `DEC_8` | EQU = `8` | S2:5901 |
| `EDC063` | `DEC_9` | EQU = `9` | S2:5909 |
| `ETX063` | `LITERAL__77_0000` | EQU = `=77 0000` | S2:5963 |
| `ETX064` | `LITERAL__6H_7__7_________` | EQU = `=6H'7''7'''''''''` | S2:5964 |
| `ETX065` | `LITERAL__6H_____7__7__7__7_` | EQU = `=6H'''''7''7''7''7'` | S2:5969 |
| `ETX066` | `LITERAL__6HLIBRAR` | EQU = `=6HLIBRAR` | S2:5991 |
| `ETX067` | `LITERAL__6HY_OT` | EQU = `=6HY OT` | S2:5993 |
| `ETX068` | `LITERAL__6H_377__377_________` | EQU = `=6H'377''377'''''''''` | S2:5998 |
| `ETX069` | `LITERAL__6H____` | EQU = `=6H''''` | S2:5999 |
| `ETX070` | `LITERAL__210_0000` | EQU = `=210 0000` | S2:6024 |
| `ETX071` | `LITERAL__6H___3__7_______` | EQU = `=6H'''3''7'''''''` | S2:6030 |
| `ETX072` | `LITERAL__6H_00` | EQU = `=6H 00` | S2:6031 |
| `ETX073` | `LITERAL__1777_6000` | EQU = `=1777 6000` | S2:6034 |
| `ETX074` | `LITERAL__6H___7__7__7__7___` | EQU = `=6H'''7''7''7''7'''` | S2:6035 |
| `ETX075` | `LITERAL__6H_0000` | EQU = `=6H 0000` | S2:6036 |
| `ETX076` | `LITERAL__6H_______7__7___` | EQU = `=6H'''''''7''7'''` | S2:6040 |
| `ETX077` | `LITERAL__6HHO_00` | EQU = `=6HHO 00` | S2:6041 |
| `EDC077` | `DEC_6` | EQU = `6` | S2:6043 |
| `EDC078` | `DEC_19` | EQU = `19` | S2:6052 |
| `EOC078` | `OCT_100` | EQU = `100B` | S2:6059 |
| `ETX078` | `LIT_30HCBO_O_HO_66__0120__37___BXO` | EQU = `30HCBOБOДHO 66  0120  37   BXOДOB` | S2:6069 |
| `ETX079` | `LIT_20` | EQU = `20` | S2:6070 |
| `ETX080` | `LIT_1H_231_` | EQU = `1H'231'` | S2:6071 |
| `ETX081` | `LIT_24H_C_OP_EH___O__PO_PAMM___231` | EQU = `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S2:6072 |
| `ETX082` | `LIT_12H00__OHA_0000` | EQU = `12H00 ЗOHA 0000` | S2:6073 |
| `ETX083` | `LIT_18H_CK___EH__BXO____231_` | EQU = `18HИCKЛЮЧEHЫ BXOДЫ:'231'` | S2:6074 |
| `ETX084` | `LIT_12HMA_O_M___133__231_` | EQU = `12HMAЛO MЛ '133''231'` | S2:6075 |
| `ETX085` | `LIT_18H__C_OP_EH_KATA_O_` | EQU = `18H ИCПOPЧEH KATAЛOГ` | S2:6076 |
| `ETX086` | `LIT_12H` | EQU = `12H` | S2:6077 |
| `ETX087` | `LIT_30HO___O_H___C__COK__APAMETPOB` | EQU = `30HOШИБOЧHЫЙ CПИCOK ПAPAMETPOB'231'` | S2:6079 |
| `ETX088` | `LIT_30H_EPE_O_HEH_E_KATA_O_A_O_C__` | EQU = `30HПEPEПOЛHEHИE KATAЛOГA OБCП !'231'` | S2:6080 |
| `ETX089` | `LIT_8HPROGRAM` | EQU = `8HPROGRAM` | S2:6081 |
| `ETX090` | `LIT_1` | EQU = `1` | S2:6082 |
| `ETX091` | `LIT_12` | EQU = `12` | S2:6111 |
| `ETX092` | `LIT_8` | EQU = `8` | S2:6116 |

## 2. Перекрёстные ссылки (определение → использования)

| Символ | Короткое | Использования (строка: операнд) |
|---|---|---|
| `******` | `LBL053` | 5658:`******` |
| `*MONCRD*` | `MON007` | 5348:`*MONCRD*` |
| `*OГPAH*` | `OPA131` | 5292:`*OГPAH*`; 5339:`*OГPAH*`; 5367:`*OГPAH*`; 5372:`*OГPAH*`; 5743:`*OГPAH*`; 5748:`*OГPAH*` |
| `A HAЧ` | `AHA113` | 5645:`A HAЧ`; 5672:`A HAЧ`; 5678:`A HAЧ`; 5685:`A HAЧ` |
| `A/OCTDEC` | `AOC005` | 6020:`A/OCTDEC` |
| `A/REF` | `ARE114` | 5288:`A/REF`; 5883:`A/REF`; 5926:`A/REF`; 5928:`A/REF` |
| `ADR/REF` | `ADR115` | 5884:`ADR/REF`; 5904:`ADR/REF` |
| `ALL//LIB` | `ALL043` | 5390:`ALL//LIB` |
| `BEG*DFT` | `BEG117` | 5627:`BEG*DFT`; 5700:`BEG*DFT`; 5705:`BEG*DFT`; 5765:`BEG*DFT` |
| `BIG*KT` | `BIG108` | 5980:`BIG*KT-T*ERRC` |
| `BSS` | `BSS128` | 5628:`BSS` |
| `CBOБOДHO` | `CBO137` | 5290:`CBOБOДHO`; 5835:`CBOБOДHO`; 5840:`CBOБOДHO`; 5846:`CBOБOДHO`; 5847:`CBOБOДHO`; 5986:`CBOБOДHO`; 6023:`CBOБOДHO` |
| `CH*ENT/R` | `CHE080` | 5887:`CH*ENT/R` |
| `CL/COM` | `CLC017` | 5301:`CL/COM` |
| `COMMENT` | `COM139` | 5299:`COMMENT`; 5350:`COMMENT`; 6002:`COMMENT` |
| `CON/DO` | `CON075` | 5861:`CON/DO` |
| `CONT///` | `CON059` | 5729:`CONT///` |
| `CONT/F` | `CON071` | 5819:`CONT/F` |
| `CONT/R` | `CON060` | 5723:`CONT/R` |
| `CONT/W` | `CON063` | 5741:`CONT/W` |
| `CWCAT` | `CWC097` | 5378:`CWCAT` |
| `CWWD` | `CWW098` | 5375:`CWWD` |
| `CЛOBO 1` | `COB047` | 5605:`CЛOBO 1` |
| `CЛOBO 2` | `COB048` | 5613:`CЛOBO 2` |
| `CЛOBO 3` | `COB049` | 5621:`CЛOBO 3` |
| `DATA` | `DAT125` | 5702:`DATA`; 5995:`DATA*`; 5997:`DATA*+1` |
| `DATA*` | `DAT003` | 5995:`DATA*`; 5997:`DATA*+1` |
| `DO/REF` | `DOR066` | 5789:`DO/REF`; 5794:`DO/REF` |
| `E/CH*CTL` | `ECH029` | 5435:`E/CH*CTL` |
| `E/CH*EXC` | `ECH034` | 5459:`E/CH*EXC` |
| `ECTЬ EЩE` | `ECT051` | 5661:`ECTЬ EЩE` |
| `ELW/REF` | `ELW072` | 5777:`ELW/REF` |
| `END//KAT` | `END116` | 5561:`END//KAT`; 5675:`END//KAT`; 5687:`END//KAT`; 5689:`END//KAT`; 5873:`END//KAT`; 5888:`END//KAT`; 5989:`END//KAT`; 6016:`END//KAT` |
| `ERR*CALL` | `ERR088` | 5314:`ERR*CALL`; 5324:`ERR*CALL`; 5331:`ERR*CALL`; 5337:`ERR*CALL`; 5342:`ERR*CALL`; 5346:`ERR*CALL` |
| `ERR*LIBT` | `ERR085` | 5413:`ERR*LIBT`; 5417:`ERR*LIBT`; 5420:`ERR*LIBT`; 5440:`ERR*LIBT` |
| `EXCLUDE` | `EXC011` | 5456:`EXCLUDE` |
| `FIN**LIB` | `FIN073` | 5565:`FIN**LIB` |
| `FIN*SM` | `FIN064` | 5719:`FIN*SM` |
| `FL*TEMPO` | `FLT142` | 5401:`FL*TEMPO`; 5426:`FL*TEMPO`; 5431:`FL*TEMPO` |
| `FL/MAL` | `FLM111` | 5368:`FL/MAL`; 5744:`FL/MAL`; 5855:`FL/MAL`; 5860:`FL/MAL` |
| `FL/TEMPO` | `FLT141` | 5306:`FL/TEMPO`; 5355:`FL/TEMPO`; 5357:`FL/TEMPO` |
| `FLDIAG` | `FLD138` | 5281:`FLDIAG`; 5487:`FLDIAG`; 5491:`FLDIAG`; 5534:`FLDIAG`; 5638:`FLDIAG`; 5643:`FLDIAG` |
| `GIV*OГP` | `GIV020` | 5319:`GIV*OГP`; 5329:`GIV*OГP` |
| `GV/REF` | `GVR067` | 5797:`GV/REF` |
| `HET/CБ` | `HET074` | 5854:`HET/CБ`; 5856:`HET/CБ` |
| `IBAD` | `IBA092` | 5654:`IBAD`; 5665:`IBAD` |
| `INF` | `INF093` | 5492:`INF`; 5641:`INF`; 5863:`INF`; 5973:`INF`; 5977:`INF`; 5983:`INF` |
| `IS***EXC` | `ISE042` | 5474:`IS***EXC`; 5478:`IS***EXC`; 5486:`IS***EXC` |
| `ISPLASE` | `ISP052` | 5653:`ISPLASE` |
| `IW*R` | `IWR096` | 5403:`IW*R`; 5575:`IW*R` |
| `IWNEW` | `IWN143` | 5294:`IWNEW`; 5311:`IWNEW`; 5373:`IWNEW`; 5377:`IWNEW`; 5379:`IWNEW`; 6008:`IWNEW`; 6009:`IWNEW`; 6011:`IWNEW`; 6038:`IWNEW` |
| `KAT*NEW` | `KAT032` | 5525:`KAT*NEW` |
| `KAT*OVFL` | `KAT087` | 5520:`KAT*OVFL`; 5942:`KAT*OVFL` |
| `KAT/P` | `KAT012` | 6065:`KAT/P` |
| `KOHCT` | `KOH129` | 5626:`KOHCT` |
| `KOMAHДЫ` | `KOM127` | 5619:`KOMAHДЫ`; 5625:`KOMAHДЫ` |
| `KOMMEHT` | `KOM122` | 5706:`KOMMEHT` |
| `L///CC` | `LCC025` | 5386:`L///CC` |
| `L/0001` | `ADR076` | 5868:`L/0001` |
| `L/CH*CTL` | `LCH027` | 5439:`L/CH*CTL` |
| `L/CH*ECT` | `LCH035` | 5470:`L/CH*ECT` |
| `L/CH*EXC` | `LCH033` | 5462:`L/CH*EXC` |
| `L/CWB` | `LCW062` | 5757:`L/CWB` |
| `L/DEL1` | `LDE055` | 5684:`L/DEL1` |
| `L/DEL2` | `LDE056` | 5697:`L/DEL2` |
| `L/PNTT` | `LPN018` | 5310:`L/PNTT`; 5330:`L/PNTT` |
| `L/SS*` | `LSS081` | 5924:`L/SS*` |
| `L/WBF` | `LWB044` | 5532:`L/WBF` |
| `L/WCT` | `LWC091` | 6012:`L/WCT` |
| `LG SM` | `LGS119` | 5713:`LG SM`; 5845:`LG SM` |
| `LIB**KAT` | `LIB009` | 5381:`LIB**KAT+2`; 5464:`LIB**KAT+2`; 5475:`LIB**KAT`; 5482:`LIB**KAT`; 5484:`LIB**KAT`; 5504:`-LIB**KAT`; 5506:`LIB**KAT`; 5510:`LIB**KAT`; 5515:`LIB**KAT`; 5518:`-LIB**KAT`; 5895:`-LIB**KAT`; 5911:`-LIB**KAT` … (+1) |
| `LIB/LOOP` | `LIB026` | 5526:`LIB/LOOP`; 5974:`LIB/LOOP` |
| `LINE` | `LIN100` | 5649:`LINE`; 6051:`LINE`; 6052:`LINE+19` |
| `LIST` | `LIS144` | 5321:`LIST`; 5361:`LIST`; 5398:`LIST`; 5574:`LIST`; 5960:`LIST` |
| `LONG/ID` | `LON126` | 5708:`LONG/ID` |
| `LOOP/F` | `LOO077` | 5881:`LOOP/F`; 5921:`LOOP/F` |
| `LOOP/RW` | `LOO058` | 5766:`LOOP/RW`; 5769:`LOOP/RW` |
| `LOOPC2` | `LOO045` | 5568:`LOOPC2`; 5698:`LOOPC2`; 5849:`LOOPC2` |
| `LS/COM` | `LSC021` | 5352:`LS/COM` |
| `LW/REF` | `LWR065` | 5785:`LW/REF`; 5786:`LW/REF`; 5787:`LW/REF`; 5790:`LW/REF`; 5791:`LW/REF`; 5792:`LW/REF`; 5813:`LW/REF`; 5816:`LW/REF` |
| `LWCMNT` | `LWC090` | 6006:`LWCMNT` |
| `MAK**EXC` | `MAK036` | 5468:`MAK**EXC`; 5496:`MAK**EXC` |
| `MAK//EXC` | `MAK037` | 5461:`MAK//EXC` |
| `MAKELIBT` | `MAK001` | 6117:`MAKELIBT` |
| `MAЛO*MЛ` | `MAO086` | 5370:`MAЛO*MЛ` |
| `MAЛO/MЛ` | `MAO104` | 5862:`MAЛO/MЛ`; 5976:`MAЛO/MЛ` |
| `MONITOR*` | `MON002` | 6049:`MONITOR*+1` |
| `N/PERSO` | `NPE140` | 5365:`N/PERSO` |
| `NO SHAKE` | `NOS054` | 5663:`NO SHAKE` |
| `NO*CH*EX` | `NOC039` | 5455:`NO*CH*EX`; 5466:`NO*CH*EX` |
| `NO*D*E` | `NOD038` | 5488:`NO*D*E` |
| `NO*PARAM` | `NOP023` | 5307:`NO*PARAM`; 5343:`NO*PARAM`; 5353:`NO*PARAM` |
| `NO*TMPL` | `NOT028` | 5427:`NO*TMPL`; 5430:`NO*TMPL` |
| `NO//SWOP` | `NOS046` | 5590:`NO//SWOP` |
| `NO/PARAM` | `NOP022` | 5315:`NO/PARAM` |
| `NOT*TEMP` | `NOT024` | 5358:`NOT*TEMP` |
| `NXT/R` | `NXT078` | 5892:`NXT/R`; 5899:`NXT/R` |
| `OK*CTL` | `OKC030` | 5437:`OK*CTL` |
| `OБOЗH` | `OOH121` | 5709:`OБOЗH`; 5774:`OБOЗH` |
| `P/CH*CTL` | `PCH031` | 5441:`P/CH*CTL` |
| `P/UKAZ` | `PUK130` | 5394:`P/UKAZ`; 5481:`P/UKAZ`; 5514:`P/UKAZ` |
| `PARAMT*` | `PAR006` | 5303:`PARAMT*`; 5313:`PARAMT*`; 5323:`PARAMT*`; 5341:`PARAMT*`; 5345:`PARAMT*` |
| `PEЗ*2` | `PE2123` | 5707:`PEЗ*2` |
| `PRINT8` | `PRI004` | 6050:`PRINT8` |
| `PROGRAM` | `PRO109` | 5454:`PROGRAM` |
| `PT*REF` | `PTR069` | 5809:`PT*REF` |
| `PT/REF` | `PTR068` | 5801:`PT/REF` |
| `PT6/G` | `PT6015` | 5495:`PT6/G`; 5651:`PT6/G` |
| `R*001` | `R00083` | 5939:`R*001`; 5941:`R*001` |
| `R/NXTR` | `RNX084` | 5886:`R/NXTR` |
| `RB/P` | `RBP013` | 6059:`RB/P+100B`; 6063:`RB/P` |
| `RBUF` | `RBU010` | 5276:`(RBUF)16`; 5410:`RBUF`; 5524:`-RBUF`; 5581:`RBUF`; 5718:`-RBUF-1023`; 5720:`RBUF`; 5817:`RBUF` |
| `SERCH*R` | `SER079` | 5894:`SERCH*R` |
| `SET` | `SET124` | 5611:`SET`; 5703:`SET` |
| `SHI*ENTR` | `SHI040` | 5507:`SHI*ENTR` |
| `SHI*FIN` | `SHI041` | 5505:`SHI*FIN` |
| `SHIFT` | `SHI112` | 5673:`SHIFT`; 5680:`SHIFT`; 5688:`SHIFT`; 5691:`SHIFT` |
| `SM//GOOD` | `SMG057` | 5633:`SM//GOOD` |
| `SVNEW` | `SVN110` | 5374:`SVNEW`; 6025:`SVNEW`; 6028:`SVNEW`; 6033:`SVNEW` |
| `T*BADLIB` | `TBA105` | 5972:`T*BADLIB` |
| `T*ERRC` | `TER107` | 5980:`BIG*KT-T*ERRC`; 5982:`T*ERRC` |
| `T*ИCKЛ` | `TCK103` | 5489:`T*ИCKЛ` |
| `TEK*ADR` | `TEK118` | 5715:`TEK*ADR`; 5760:`TEK*ADR`; 5762:`TEK*ADR` |
| `TEST*IW` | `TES019` | 5316:`TEST*IW`; 5325:`TEST*IW` |
| `W0001` | `BUF132` | 5404:`W0001`; 5405:`W0001`; 5406:`W0001`; 5408:`W0001`; 5409:`W0001`; 5589:`W0001`; 5593:`W0001`; 5724:`W0001`; 5726:`W0001`; 5730:`W0001`; 5734:`W0001`; 5736:`W0001` … (+2) |
| `W0002` | `BUF133` | 5576:`W0002`; 5587:`W0002`; 5588:`W0002`; 5591:`W0002`; 5592:`W0002`; 5722:`W0002`; 5738:`W0002`; 5767:`W0002`; 5800:`W0002`; 5808:`W0002`; 5810:`W0002`; 5814:`W0002` … (+5) |
| `W0003` | `BUF134` | 5376:`W0003`; 5749:`W0003`; 5751:`W0003`; 5753:`W0003`; 5857:`W0003` |
| `W0004` | `BUF135` | 5282:`W0004*`; 5283:`W0004`; 5820:`W0004`; 5821:`W0004`; 5825:`W0004`; 5859:`W0004` |
| `W0004*` | `DAT094` | 5282:`W0004*` |
| `W0005` | `BUF136` | 5284:`W0005*`; 5285:`W0005`; 5872:`W0005`; 5950:`W0005`; 5954:`W0005`; 5956:`W0005` |
| `W0005*` | `DAT095` | 5284:`W0005*` |
| `WB/P` | `WBP014` | 6061:`WB/P`; 6067:`WB/P` |
| `WR/ALL` | `WRA089` | 5878:`WR/ALL` |
| `WSR*` | `WSR082` | 5898:`WSR*` |
| `WW/RF` | `WWR070` | 5815:`WW/RF`; 5850:`WW/RF` |
| `БЛOK/W` | `OKW061` | 5745:`БЛOK/W` |
| `БЫЛA YЖE` | `AYE050` | 5639:`БЫЛA YЖE` |
| `ЗAГOЛ` | `AO120` | 5603:`ЗAГOЛ`; 5701:`ЗAГOЛ` |
| `ЗOHA*` | `OHA102` | 5965:`ЗOHA*`; 5970:`ЗOHA*+1` |
| `ЗOHA/` | `OHA106` | 5966:`ЗOHA/`; 5971:`ЗOHA/+1` |
| `ИTOГ` | `TO099` | 6021:`ИTOГ+5`; 6032:`ИTOГ+3`; 6037:`ИTOГ+2`; 6042:`ИTOГ+1`; 6044:`ИTOГ` |
| `ПOPЧA` | `OPA101` | 5640:`ПOPЧA` |

## 3. Вызовы и переходы (VJM / CALL / UJ)

| Строка | Команда | Операнд |
|---|---|---|
| S2:5303 | `CALL` | `PARAMT*` |
| S2:5313 | `CALL` | `PARAMT*` |
| S2:5316 | `VJM` | `TEST*IW` |
| S2:5323 | `CALL` | `PARAMT*` |
| S2:5325 | `VJM` | `TEST*IW` |
| S2:5331 | `UJ` | `ERR*CALL` |
| S2:5338 | `UJ` | `(через индексный регистр)` |
| S2:5341 | `CALL` | `PARAMT*` |
| S2:5345 | `CALL` | `PARAMT*` |
| S2:5353 | `UJ` | `NO*PARAM` |
| S2:5440 | `UJ` | `ERR*LIBT` |
| S2:5470 | `UJ` | `L/CH*ECT` |
| S2:5486 | `UJ` | `IS***EXC` |
| S2:5495 | `CALL` | `PT6/G` |
| S2:5496 | `UJ` | `MAK**EXC` |
| S2:5507 | `UJ` | `SHI*ENTR` |
| S2:5526 | `UJ` | `LIB/LOOP` |
| S2:5651 | `CALL` | `PT6/G` |
| S2:5698 | `UJ` | `LOOPC2` |
| S2:5784 | `UJ` | `*+1` |
| S2:5785 | `UJ` | `LW/REF` |
| S2:5786 | `UJ` | `LW/REF` |
| S2:5787 | `UJ` | `LW/REF` |
| S2:5789 | `UJ` | `DO/REF` |
| S2:5790 | `UJ` | `LW/REF` |
| S2:5791 | `UJ` | `LW/REF` |
| S2:5792 | `UJ` | `LW/REF` |
| S2:5794 | `UJ` | `DO/REF` |
| S2:5801 | `UJ` | `PT/REF` |
| S2:5815 | `VJM` | `WW/RF` |
| S2:5816 | `UJ` | `LW/REF` |
| S2:5827 | `UJ` | `(через индексный регистр)` |
| S2:5850 | `UJ` | `WW/RF` |
| S2:5886 | `VJM` | `R/NXTR` |
| S2:5898 | `VJM` | `WSR*` |
| S2:5899 | `UJ` | `NXT/R` |
| S2:5942 | `UJ` | `KAT*OVFL` |
| S2:5943 | `UJ` | `(через индексный регистр)` |
| S2:5958 | `UJ` | `(через индексный регистр)` |
| S2:5974 | `UJ` | `LIB/LOOP` |
| S2:6020 | `CALL` | `A/OCTDEC` |
| S2:6050 | `UJ` | `PRINT8` |

## 4. Внешние символы (не определены в модуле)

- (нет)

## 5. Литералы → EQU

| EQU | Значение | Строка |
|---|---|---|
| `RBU010` | `CCЫЛKИ` | S2:5273 |
| `EDC014` | `2` | S2:5263 |
| `EDC015` | `12` | S2:5267 |
| `EDC016` | `1` | S2:5268 |
| `EDC017` | `2048` | S2:5269 |
| `EDC018` | `1024` | S2:5270 |
| `EDC019` | `16` | S2:5275 |
| `EDC020` | `1023` | S2:5286 |
| `ETX020` | `=1` | S2:5287 |
| `ETX021` | `=211 2000` | S2:5289 |
| `ETX022` | `=400` | S2:5291 |
| `ETX023` | `=66 0000` | S2:5293 |
| `EDC023` | `7` | S2:5295 |
| `EDC024` | `11` | S2:5297 |
| `ETX024` | `=6H` | S2:5298 |
| `EDC025` | `10` | S2:5302 |
| `ETX025` | `=6H''''''''''-` | S2:5305 |
| `ETX026` | `=6H''''''''''(` | S2:5309 |
| `EDC026` | `4` | S2:5312 |
| `ETX027` | `=6H'''''''''')` | S2:5328 |
| `ETX028` | `=10 0000` | S2:5335 |
| `ETX029` | `=40 0000` | S2:5336 |
| `EDC029` | `5` | S2:5340 |
| `ETX030` | `=21 0000` | S2:5359 |
| `EDC030` | `3` | S2:5366 |
| `ETX031` | `=6` | S2:5369 |
| `EDC031` | `2047` | S2:5383 |
| `ETX032` | `=7777 7777 7777 7777` | S2:5387 |
| `EDC032` | `64` | S2:5393 |
| `EDC033` | `38` | S2:5393 |
| `ETX033` | `=100 0000 0001` | S2:5407 |
| `ETX034` | `=200 0000` | S2:5412 |
| `ETX035` | `=7777 7777 7000 0037` | S2:5415 |
| `ETX036` | `=70 0000` | S2:5419 |
| `EDC036` | `1022` | S2:5424 |
| `ETX037` | `=:4` | S2:5429 |
| `ETX038` | `=:2` | S2:5473 |
| `ETX039` | `=7743 7777 7770 0000` | S2:5480 |
| `EDC039` | `13` | S2:5490 |
| `ETX040` | `=7743 7777 7777 7777` | S2:5513 |
| `EDC040` | `2032` | S2:5519 |
| `EDC041` | `14` | S2:5523 |
| `ETX041` | `=:0034` | S2:5570 |
| `ETX042` | `=7` | S2:5571 |
| `ETX043` | `=:1740` | S2:5578 |
| `ETX044` | `=1740` | S2:5579 |
| `ETX045` | `=:0003 77` | S2:5583 |
| `ETX046` | `=377` | S2:5584 |
| `ETX047` | `=7740` | S2:5585 |
| `ETX048` | `=7777` | S2:5586 |
| `ETX049` | `=77777` | S2:5609 |
| `EDC049` | `15` | S2:5612 |
| `EDC050` | `20` | S2:5646 |
| `ETX050` | `=3` | S2:5704 |
| `ETX051` | `=37` | S2:5710 |
| `ETX052` | `=77740` | S2:5711 |
| `EOC052` | `17B` | S2:5716 |
| `EOC053` | `11B` | S2:5717 |
| `ETX053` | `=700 0000` | S2:5781 |
| `ETX054` | `=2000 0000` | S2:5796 |
| `ETX055` | `=:7777 7777` | S2:5799 |
| `EDC055` | `24` | S2:5803 |
| `EOC055` | `4000B` | S2:5805 |
| `EDC056` | `42` | S2:5811 |
| `ETX056` | `=12` | S2:5812 |
| `ETX057` | `=7741` | S2:5822 |
| `ETX058` | `=2000 0077 7777 7777` | S2:5833 |
| `ETX059` | `=77 76000` | S2:5841 |
| `ETX060` | `=:0037 77` | S2:5842 |
| `EDC060` | `3071` | S2:5865 |
| `EDC061` | `48` | S2:5869 |
| `EDC062` | `8` | S2:5901 |
| `EDC063` | `9` | S2:5909 |
| `ETX063` | `=77 0000` | S2:5963 |
| `ETX064` | `=6H'7''7'''''''''` | S2:5964 |
| `ETX065` | `=6H'''''7''7''7''7'` | S2:5969 |
| `ETX066` | `=6HLIBRAR` | S2:5991 |
| `ETX067` | `=6HY OT` | S2:5993 |
| `ETX068` | `=6H'377''377'''''''''` | S2:5998 |
| `ETX069` | `=6H''''` | S2:5999 |
| `ETX070` | `=210 0000` | S2:6024 |
| `ETX071` | `=6H'''3''7'''''''` | S2:6030 |
| `ETX072` | `=6H 00` | S2:6031 |
| `ETX073` | `=1777 6000` | S2:6034 |
| `ETX074` | `=6H'''7''7''7''7'''` | S2:6035 |
| `ETX075` | `=6H 0000` | S2:6036 |
| `ETX076` | `=6H'''''''7''7'''` | S2:6040 |
| `ETX077` | `=6HHO 00` | S2:6041 |
| `EDC077` | `6` | S2:6043 |
| `EDC078` | `19` | S2:6052 |
| `EOC078` | `100B` | S2:6059 |
| `ETX078` | `30HCBOБOДHO 66  0120  37   BXOДOB` | S2:6069 |
| `ETX079` | `20` | S2:6070 |
| `ETX080` | `1H'231'` | S2:6071 |
| `ETX081` | `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S2:6072 |
| `ETX082` | `12H00 ЗOHA 0000` | S2:6073 |
| `ETX083` | `18HИCKЛЮЧEHЫ BXOДЫ:'231'` | S2:6074 |
| `ETX084` | `12HMAЛO MЛ '133''231'` | S2:6075 |
| `ETX085` | `18H ИCПOPЧEH KATAЛOГ` | S2:6076 |
| `ETX086` | `12H` | S2:6077 |
| `ETX087` | `30HOШИБOЧHЫЙ CПИCOK ПAPAMETPOB'231'` | S2:6079 |
| `ETX088` | `30HПEPEПOЛHEHИE KATAЛOГA OБCП !'231'` | S2:6080 |
| `ETX089` | `8HPROGRAM` | S2:6081 |
| `ETX090` | `1` | S2:6082 |
| `ETX091` | `12` | S2:6111 |
| `ETX092` | `8` | S2:6116 |

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **8**.
- TEXT-констант переименовано по содержимому: **0**.
- Смещений `LABEL+NNNB` → десятичное: **0**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_core.txt`.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э64 | INF093 | не найдено в rukava.be | — | 5 | `src/lib21/MAKELIBT.mad:372`, `src/lib21/MAKELIBT.mad:743`, `src/lib21/MAKELIBT.mad:853`, `src/lib21/MAKELIBT.mad:857`, `src/lib21/MAKELIBT.mad:863` |
| Э70 | BUF132 | не найдено в rukava.be | — | 3 | `src/lib21/MAKELIBT.mad:285`, `src/lib21/MAKELIBT.mad:289`, `src/lib21/MAKELIBT.mad:616` |
| Э70 | BUF133 | не найдено в rukava.be | — | 1 | `src/lib21/MAKELIBT.mad:471` |
| Э70 | BUF134 | не найдено в rukava.be | — | 2 | `src/lib21/MAKELIBT.mad:629`, `src/lib21/MAKELIBT.mad:737` |
| Э70 | BUF135 | не найдено в rukava.be | — | 2 | `src/lib21/MAKELIBT.mad:700`, `src/lib21/MAKELIBT.mad:739` |
| Э70 | BUF136 | не найдено в rukava.be | — | 2 | `src/lib21/MAKELIBT.mad:752`, `src/lib21/MAKELIBT.mad:836` |
| Э70 | IWN143 | не найдено в rukava.be | — | 1 | `src/lib21/MAKELIBT.mad:888` |
