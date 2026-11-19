# CRELIB — перекрёстные ссылки

Модуль `CRELIB` (исходник `libra211.l21:8648-9695`). Сверка: `disasm/lib21/CRELIB.madlen`.

Все метки переименованы в ≤6 символов (уникальные первые 6); полные имена сохранены в `; (POLN: ...)` в `src/lib21/CRELIB.mad`.

## 1. Таблица символов (метки и EQU)

| Короткое имя | Полное имя (POLN) | Тип | Строка |
|---|---|---|---|
| `CRE001` | `CRELIB` | метка | libra211.l21:8648 |
| `RCA002` | `RCAT` | метка | libra211.l21:8713 |
| `LOA003` | `LOADANGO` | метка | libra211.l21:8715 |
| `LGO004` | `LGOSEQ` | метка | libra211.l21:8716 |
| `FUL005` | `FULISFL*` | метка | libra211.l21:8717 |
| `NOL006` | `NOLISFL*` | метка | libra211.l21:8718 |
| `ERR007` | `ERROFLG*` | метка | libra211.l21:8719 |
| `STO008` | `STOP*` | метка | libra211.l21:8721 |
| `PRI009` | `PRINT8` | метка | libra211.l21:8722 |
| `BLE010` | `BLEXPRIN` | метка | libra211.l21:8724 |
| `MON011` | `*MONCRD*` | метка | libra211.l21:8726 |
| `PAR012` | `PARAMT*` | метка | libra211.l21:8727 |
| `PT6013` | `PT6/G` | метка | libra211.l21:8728 |
| `RDB014` | `RDBUF` | метка | libra211.l21:8729 |
| `NPR015` | `NPR` | метка | libra211.l21:8734 |
| `NPW016` | `NPW` | метка | libra211.l21:8735 |
| `CAT017` | `CAT/2` | метка | libra211.l21:8736 |
| `N0018` | `*0` | метка | libra211.l21:8737 |
| `N1019` | `*1` | метка | libra211.l21:8739 |
| `N13020` | `*13` | метка | libra211.l21:8740 |
| `N2021` | `*2` | метка | libra211.l21:8742 |
| `N9022` | `*9` | метка | libra211.l21:8743 |
| `N3024` | `*3` | метка | libra211.l21:8748 |
| `N6026` | `*6` | метка | libra211.l21:8752 |
| `N10027` | `*10` | метка | libra211.l21:8756 |
| `PLU028` | `PLUS` | метка | libra211.l21:8758 |
| `MIN029` | `MINUS` | метка | libra211.l21:8759 |
| `BEG030` | `BEG` | метка | libra211.l21:8761 |
| `ADD031` | `ADDLIB` | метка | libra211.l21:8763 |
| `NOA032` | `NOADD` | метка | libra211.l21:8790 |
| `TEM033` | `TEMP` | метка | libra211.l21:8804 |
| `NOP034` | `NOPAR` | метка | libra211.l21:8833 |
| `RCA035` | `RCATL` | метка | libra211.l21:8867 |
| `RCA036` | `RCATW` | метка | libra211.l21:8888 |
| `RSK037` | `RSKIP` | метка | libra211.l21:8910 |
| `CPO038` | `C.....   ПPOBEPИM` | метка | libra211.l21:8914 |
| `CHL039` | `CHLIS` | метка | libra211.l21:8934 |
| `DEL040` | `DELPRI` | метка | libra211.l21:8942 |
| `WRE041` | `WRENT` | метка | libra211.l21:8954 |
| `RNE042` | `RNEXT` | метка | libra211.l21:8963 |
| `RCA043` | `RCATEND` | метка | libra211.l21:8970 |
| `PRO044` | `PROCREF` | метка | libra211.l21:8997 |
| `PRE045` | `PREFP` | метка | libra211.l21:9014 |
| `PRE046` | `PREFE` | метка | libra211.l21:9021 |
| `RDE047` | `RDECW` | метка | libra211.l21:9089 |
| `SEX048` | `SEXT` | метка | libra211.l21:9100 |
| `GET049` | `GETID` | метка | libra211.l21:9120 |
| `SHO050` | `SHORT` | метка | libra211.l21:9131 |
| `CHE051` | `CHECOM` | метка | libra211.l21:9134 |
| `SEC052` | `SECAT` | метка | libra211.l21:9144 |
| `WRE053` | `WREF` | метка | libra211.l21:9159 |
| `SEX054` | `SEXTEND` | метка | libra211.l21:9168 |
| `NOR055` | `NOREF` | метка | libra211.l21:9177 |
| `BAD056` | `BADPROG` | метка | libra211.l21:9193 |
| `NEX057` | `NEXBP` | метка | libra211.l21:9202 |
| `DEL058` | `DELBP` | метка | libra211.l21:9210 |
| `SHI059` | `SHIBP` | метка | libra211.l21:9221 |
| `PRE060` | `PREFEND` | метка | libra211.l21:9233 |
| `WRC061` | `WRCAT` | метка | libra211.l21:9286 |
| `WSK062` | `WSKIP` | метка | libra211.l21:9313 |
| `WCA063` | `WCATEND` | метка | libra211.l21:9316 |
| `WRE064` | `WREFT` | метка | libra211.l21:9334 |
| `WRL065` | `WRLIS` | метка | libra211.l21:9342 |
| `TRA066` | `TRANSP` | метка | libra211.l21:9361 |
| `TRA067` | `TRANSE` | метка | libra211.l21:9370 |
| `TRA068` | `TRANSW` | метка | libra211.l21:9394 |
| `PRI069` | `PRIHE` | метка | libra211.l21:9414 |
| `NOP070` | `NOPRENT` | метка | libra211.l21:9435 |
| `TRE071` | `TREND` | метка | libra211.l21:9473 |
| `FIN072` | `FINPRI` | метка | libra211.l21:9481 |
| `BAD073` | `BADCAT` | метка | libra211.l21:9498 |
| `LON074` | `LONCAT` | метка | libra211.l21:9504 |
| `EMP075` | `EMPLIB` | метка | libra211.l21:9506 |
| `LON076` | `LONLIB` | метка | libra211.l21:9508 |
| `WNE077` | `WNEXW` | метка | libra211.l21:9518 |
| `RBE078` | `RBEGP` | метка | libra211.l21:9530 |
| `REX079` | `REXCH` | метка | libra211.l21:9541 |
| `RNE080` | `RNEXW` | метка | libra211.l21:9550 |
| `RNE081` | `RNEXP` | метка | libra211.l21:9557 |
| `IFN082` | `IFNEX` | метка | libra211.l21:9563 |
| `IFS083` | `IFSET` | метка | libra211.l21:9567 |
| `PRI084` | `PRILIS` | метка | libra211.l21:9582 |
| `PRI085` | `PRILN` | метка | libra211.l21:9587 |
| `PRI086` | `PRILR` | метка | libra211.l21:9590 |
| `PRI087` | `PRILE` | метка | libra211.l21:9599 |
| `GOS088` | `GOSEQ` | метка | libra211.l21:9605 |
| `GOB089` | `GOBACK` | метка | libra211.l21:9607 |
| `IPR090` | `IPR` | метка | libra211.l21:9610 |
| `IPW091` | `IPW` | метка | libra211.l21:9612 |
| `INF092` | `INFPR` | метка | libra211.l21:9615 |
| `ILI093` | `ILINE` | метка | libra211.l21:9619 |
| `FUL094` | `FULW` | метка | libra211.l21:9624 |
| `B48095` | `B48/16` | метка | libra211.l21:9625 |
| `B48096` | `B48/25` | метка | libra211.l21:9626 |
| `B46097` | `B46/31` | метка | libra211.l21:9627 |
| `B39098` | `B39*18/1` | метка | libra211.l21:9628 |
| `B21099` | `B21/1` | метка | libra211.l21:9629 |
| `B18100` | `B18/1` | метка | libra211.l21:9630 |
| `B15101` | `B15/1` | метка | libra211.l21:9631 |
| `B12102` | `B12/1` | метка | libra211.l21:9632 |
| `B11103` | `B11/1` | метка | libra211.l21:9633 |
| `B10104` | `B10/1` | метка | libra211.l21:9634 |
| `C3105` | `C3` | метка | libra211.l21:9635 |
| `B1106` | `B1` | метка | libra211.l21:9636 |
| `Z48107` | `Z48` | метка | libra211.l21:9637 |
| `Z47108` | `Z47` | метка | libra211.l21:9638 |
| `Z12109` | `Z12/6` | метка | libra211.l21:9639 |
| `MTE110` | `MTEMP` | метка | libra211.l21:9640 |
| `MPE111` | `MPERS` | метка | libra211.l21:9641 |
| `PRO112` | `PROGRAM` | метка | libra211.l21:9643 |
| `LIB113` | `LIBLIST` | метка | libra211.l21:9644 |
| `DEL114` | `DELMES` | метка | libra211.l21:9645 |
| `DEL115` | `DELNAM` | метка | libra211.l21:9646 |
| `HEA116` | `HEADBP` | метка | libra211.l21:9648 |
| `TLD117` | `TLDRU` | метка | libra211.l21:9649 |
| `TLM118` | `TLMEM` | метка | libra211.l21:9650 |
| `HEA119` | `HEADPR` | метка | libra211.l21:9651 |
| `HEN120` | `HENAME` | метка | libra211.l21:9652 |
| `HEL121` | `HELDRU` | метка | libra211.l21:9654 |
| `HEL122` | `HELMEM` | метка | libra211.l21:9656 |
| `HEN123` | `HENT` | метка | libra211.l21:9657 |
| `HEX124` | `HEXT` | метка | libra211.l21:9658 |
| `ENT125` | `ENTMES` | метка | libra211.l21:9659 |
| `FIL126` | `FILCAT` | метка | libra211.l21:9660 |
| `TLL127` | `TLLIB1` | метка | libra211.l21:9661 |
| `TLL128` | `TLLIB2` | метка | libra211.l21:9662 |
| `LEN129` | `LENMES` | метка | libra211.l21:9663 |
| `FIL130` | `FILLIB` | метка | libra211.l21:9664 |
| `BCM131` | `BCMES` | метка | libra211.l21:9665 |
| `BCU132` | `BCUN` | метка | libra211.l21:9666 |
| `LCM133` | `LCMES` | метка | libra211.l21:9668 |
| `EMM134` | `EMMES` | метка | libra211.l21:9669 |
| `LLM135` | `LLMES` | метка | libra211.l21:9670 |
| `NOM136` | `NOMES` | метка | libra211.l21:9671 |
| `IUO137` | `IUO` | метка | libra211.l21:9673 |
| `IUA138` | `IUA` | метка | libra211.l21:9674 |
| `IUN139` | `IUN` | метка | libra211.l21:9675 |
| `IUL140` | `IUL` | метка | libra211.l21:9676 |
| `LCA141` | `LCAT` | метка | libra211.l21:9677 |
| `LCT142` | `LCTL` | метка | libra211.l21:9678 |
| `LLI143` | `LLIB` | метка | libra211.l21:9679 |
| `LIN144` | `LIND` | метка | libra211.l21:9680 |
| `ADR145` | `ADRU` | метка | libra211.l21:9681 |
| `LDR146` | `LDRU` | метка | libra211.l21:9682 |
| `LME147` | `LMEM` | метка | libra211.l21:9683 |
| `ADE148` | `ADEC` | метка | libra211.l21:9684 |
| `LDE149` | `LDEC` | метка | libra211.l21:9685 |
| `LDE150` | `LDEF` | метка | libra211.l21:9686 |
| `TYP151` | `TYPE` | метка | libra211.l21:9687 |
| `FLD152` | `FLDL` | метка | libra211.l21:9688 |
| `FLN153` | `FLNP` | метка | libra211.l21:9689 |
| `FLB154` | `FLBP` | метка | libra211.l21:9690 |
| `POI155` | `POIN` | метка | libra211.l21:9691 |
| `RIF156` | `RIF` | метка | libra211.l21:9692 |
| `WIF157` | `WIF` | метка | libra211.l21:9693 |
| `LIN158` | `LINE` | метка | libra211.l21:9694 |
| `MIN029` | `MINUS` | EQU = `55B` | S1:8759 |
| `PLU028` | `PLUS` | EQU = `53B` | S1:8758 |
| `LGO004` | `LGOSEQ` | EQU = `LOA003+17` | S1:8716 |
| `RCA002` | `RCAT` | EQU = `47B` | S1:8713 |
| `EDC015` | `DEC_61` | EQU = `61` | S1:8649 |
| `EDC016` | `DEC_1` | EQU = `1` | S1:8717 |
| `EDC017` | `DEC_12` | EQU = `12` | S1:8726 |
| `EDC018` | `DEC_1024` | EQU = `1024` | S1:8729 |
| `EDC019` | `DEC_0` | EQU = `0` | S1:8730 |
| `EDC020` | `DEC_2048` | EQU = `2048` | S1:8731 |
| `EDC021` | `DEC_4096` | EQU = `4096` | S1:8732 |
| `EDC022` | `DEC_8192` | EQU = `8192` | S1:8733 |
| `EDC023` | `DEC_16` | EQU = `16` | S1:8734 |
| `EDC024` | `DEC_2` | EQU = `2` | S1:8736 |
| `ETX024` | `LITERAL__65_0000` | EQU = `=65 0000` | S1:8769 |
| `ETX025` | `LITERAL__66_0000` | EQU = `=66 0000` | S1:8774 |
| `ETX026` | `LITERAL__1000` | EQU = `=1000` | S1:8776 |
| `EDC026` | `DEC_4` | EQU = `4` | S1:8786 |
| `EDC027` | `DEC_6` | EQU = `6` | S1:8792 |
| `ETX027` | `LITERAL__4HTEMP` | EQU = `=4HTEMP` | S1:8795 |
| `ETX028` | `LITERAL__67_0000` | EQU = `=67 0000` | S1:8798 |
| `EDC028` | `DEC_5` | EQU = `5` | S1:8818 |
| `EDC029` | `DEC_7` | EQU = `7` | S1:8832 |
| `EDC030` | `DEC_3` | EQU = `3` | S1:8837 |
| `ETX030` | `LITERAL__21_00000` | EQU = `=21 00000` | S1:8880 |
| `ETX031` | `LITERAL__7_00000` | EQU = `=7 00000` | S1:8882 |
| `EOC031` | `OCT_776` | EQU = `776B` | S1:8886 |
| `EDC031` | `DEC_64` | EQU = `64` | S1:8898 |
| `EDC032` | `DEC_20` | EQU = `20` | S1:8898 |
| `EDC033` | `DEC_25` | EQU = `25` | S1:8903 |
| `ETX033` | `LITERAL___2` | EQU = `=:2` | S1:8908 |
| `EOC033` | `OCT_777` | EQU = `777B` | S1:8966 |
| `EDC034` | `DEC_13` | EQU = `13` | S1:8991 |
| `EDC035` | `DEC_15` | EQU = `15` | S1:9027 |
| `EDC036` | `DEC_10` | EQU = `10` | S1:9034 |
| `ETX036` | `LITERAL__7777_0000_7777` | EQU = `=7777 0000 7777` | S1:9041 |
| `EDC037` | `DEC_36` | EQU = `36` | S1:9049 |
| `EDC038` | `DEC_30` | EQU = `30` | S1:9052 |
| `EDC039` | `DEC_11` | EQU = `11` | S1:9058 |
| `ETX039` | `LITERAL__37` | EQU = `=37` | S1:9075 |
| `EDC040` | `DEC_18` | EQU = `18` | S1:9107 |
| `ETX040` | `LITERAL__57` | EQU = `=57` | S1:9109 |
| `ETX041` | `LITERAL__42` | EQU = `=42` | S1:9110 |
| `ETX042` | `LITERAL__47` | EQU = `=47` | S1:9112 |
| `ETX043` | `LITERAL__4` | EQU = `=4` | S1:9116 |
| `ETX044` | `LITERAL__20` | EQU = `=20` | S1:9122 |
| `EDC044` | `DEC_42` | EQU = `42` | S1:9140 |
| `ETX045` | `LITERAL__12` | EQU = `=12` | S1:9141 |
| `EDC045` | `DEC_48` | EQU = `48` | S1:9154 |
| `EOC045` | `OCT_17777` | EQU = `17777B` | S1:9155 |
| `EOC046` | `OCT_20000` | EQU = `20000B` | S1:9157 |
| `EOC047` | `OCT_100` | EQU = `100B` | S1:9252 |
| `EDC047` | `DEC_31` | EQU = `31` | S1:9262 |
| `ETX047` | `LITERAL__6H_____7__7__7__7_` | EQU = `=6H'''''7''7''7''7'` | S1:9263 |
| `EDC048` | `DEC_43` | EQU = `43` | S1:9267 |
| `ETX048` | `LITERAL__6H___3__7_______` | EQU = `=6H'''3''7'''''''` | S1:9268 |
| `EDC049` | `DEC_19` | EQU = `19` | S1:9273 |
| `EOC049` | `OCT_1775` | EQU = `1775B` | S1:9283 |
| `EOC050` | `OCT_67` | EQU = `67B` | S1:9323 |
| `ETX050` | `LITERAL__6H_3__17__17__17__17__17_` | EQU = `=6H'3''17''17''17''17''17'` | S1:9324 |
| `ETX051` | `LITERAL__6H000000` | EQU = `=6H000000` | S1:9325 |
| `EOC051` | `OCT_37` | EQU = `37B` | S1:9351 |
| `EDC051` | `DEC_37` | EQU = `37` | S1:9386 |
| `ETX052` | `LITERAL__6H___7__7____3__7_` | EQU = `=6H'''7''7''''3''7'` | S1:9387 |
| `ETX053` | `LITERAL__6H_7__7__7__7__7___` | EQU = `=6H'7''7''7''7''7'''` | S1:9405 |
| `EOC053` | `OCT_2000` | EQU = `2000B` | S1:9477 |
| `ETX054` | `LITERAL__6H_7__7__7__7__7__7_` | EQU = `=6H'7''7''7''7''7''7'` | S1:9501 |
| `EOC054` | `OCT_1777` | EQU = `1777B` | S1:9526 |
| `ETX055` | `LITERAL__2777_6000` | EQU = `=2777 6000` | S1:9538 |
| `ETX056` | `LITERAL__4_0000_0000_3777` | EQU = `=4 0000 0000 3777` | S1:9539 |
| `ETX057` | `LITERAL__10_0000` | EQU = `=10 0000` | S1:9570 |
| `ETX058` | `LITERAL__40_0000` | EQU = `=40 0000` | S1:9571 |
| `ETX059` | `LITERAL__3740` | EQU = `=3740` | S1:9574 |
| `EDC059` | `DEC_9` | EQU = `9` | S1:9586 |
| `ETX060` | `LIT_7777_7777_7777_7777` | EQU = `7777 7777 7777 7777` | S1:9624 |
| `ETX061` | `LIT_7777_7777_777` | EQU = `7777 7777 777` | S1:9625 |
| `ETX062` | `LIT_7777_7777` | EQU = `7777 7777` | S1:9626 |
| `ETX063` | `LIT_1777_77` | EQU = `1777 77` | S1:9627 |
| `ETX064` | `LIT_4_0000_0077_7777` | EQU = `4 0000 0077 7777` | S1:9628 |
| `ETX065` | `LIT_777_7777` | EQU = `777 7777` | S1:9629 |
| `ETX066` | `LIT_77_7777` | EQU = `77 7777` | S1:9630 |
| `ETX067` | `LIT_7_7777` | EQU = `7 7777` | S1:9631 |
| `ETX068` | `LIT_7777` | EQU = `7777` | S1:9632 |
| `ETX069` | `LIT_3777` | EQU = `3777` | S1:9633 |
| `ETX070` | `LIT_1777` | EQU = `1777` | S1:9634 |
| `ETX071` | `LIT_3` | EQU = `3` | S1:9635 |
| `ETX072` | `LIT_1` | EQU = `1` | S1:9636 |
| `ETX073` | `LIT_3777_7777_7777_7777` | EQU = `3777 7777 7777 7777` | S1:9637 |
| `ETX074` | `LIT_5777_7777_7777_7777` | EQU = `5777 7777 7777 7777` | S1:9638 |
| `ETX075` | `LIT_7777_7777_7777_0037` | EQU = `7777 7777 7777 0037` | S1:9639 |
| `ETX076` | `LIT_7777_7777_7000_0037` | EQU = `7777 7777 7000 0037` | S1:9640 |
| `ETX077` | `LIT_7776_0000_7000_0037` | EQU = `7776 0000 7000 0037` | S1:9641 |
| `ETX078` | `LIT_7HPROGRAM` | EQU = `7HPROGRAM` | S1:9643 |
| `ETX079` | `LIT_7HLIBLIST` | EQU = `7HLIBLIST` | S1:9644 |
| `ETX080` | `LIT_18H____CK___EH_BXO__` | EQU = `18H   ИCKЛЮЧEH BXOД:` | S1:9645 |
| `ETX081` | `LIT_2` | EQU = `2` | S1:9646 |
| `ETX082` | `LIT_1H_231_` | EQU = `1H'231'` | S1:9647 |
| `ETX083` | `LIT_24H_C_OP_EH___O__PO_PAMM___231` | EQU = `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S1:9648 |
| `ETX084` | `LIT_6H_00_00` | EQU = `6H 00 00` | S1:9649 |
| `ETX085` | `LIT_6H00000_231_` | EQU = `6H00000'231'` | S1:9650 |
| `ETX086` | `LIT_24H____BK___EHA__PO_PAMMA_` | EQU = `24H    BKЛЮЧEHA ПPOГPAMMA:` | S1:9651 |
| `ETX087` | `LIT_6H___HA_` | EQU = `6HДЛИHA:` | S1:9653 |
| `ETX088` | `LIT_12H_____AM_T__` | EQU = `12H    ПAMЯTЬ:` | S1:9655 |
| `ETX089` | `LIT_7HBXO____231_` | EQU = `7HBXOДЫ:'231'` | S1:9657 |
| `ETX090` | `LIT_8HCC__K___231_` | EQU = `8HCCЫЛKИ:'231'` | S1:9658 |
| `ETX091` | `LIT_30H__C_O__O__PO_PAMM___BXO_OB_` | EQU = `30HЧИCЛO ПOДПPOГPAMM И BXOДOB:` | S1:9659 |
| `ETX092` | `LIT_6HY_0000` | EQU = `6HY 0000` | S1:9661 |
| `ETX093` | `LIT_6H_00_231_` | EQU = `6H 00'231'` | S1:9662 |
| `ETX094` | `LIT_12H___HA_LIBRAR` | EQU = `12HДЛИHA LIBRAR` | S1:9663 |
| `ETX095` | `LIT_18H_C_OP_EH_KATA_O__` | EQU = `18HИCПOPЧEH KATAЛOГ:` | S1:9665 |
| `ETX096` | `LIT_3H__133__231_` | EQU = `3H '133''231'` | S1:9667 |
| `ETX097` | `LIT_20H_EPE_O_HEH_KATA_O__133__231` | EQU = `20HПEPEПOЛHEH KATAЛOГ'133''231'` | S1:9668 |
| `ETX098` | `LIT_17HHET__O__PO_PAMM_133__231_` | EQU = `17HHET ПOДПPOГPAMM'133''231'` | S1:9669 |
| `ETX099` | `LIT_9HMA_O_M__133__231_` | EQU = `9HMAЛO MЛ'133''231'` | S1:9670 |
| `ETX100` | `LIT_24H_____OTEKA_HE__A__CAHA_133_` | EQU = `24HБИБЛИOTEKA HE ЗAПИCAHA'133''231'` | S1:9671 |
| `ETX101` | `LIT_20` | EQU = `20` | S1:9694 |

## 2. Перекрёстные ссылки (определение → использования)

| Символ | Короткое | Использования (строка: операнд) |
|---|---|---|
| `*MONCRD*` | `MON011` | 8794:`*MONCRD*` |
| `ADEC` | `ADE148` | 9073:`ADEC`; 9086:`ADEC` |
| `ADRU` | `ADR145` | 9035:`ADRU`; 9085:`ADRU`; 9256:`ADRU`; 9261:`ADRU`; 9266:`ADRU`; 9274:`ADRU`; 9299:`ADRU`; 9300:`ADRU` |
| `B1` | `B1106` | 9010:`B1`; 9042:`B1`; 9054:`B1`; 9057:`B1`; 9113:`B1`; 9390:`B1`; 9442:`B1`; 9445:`B1`; 9491:`B1`; 9564:`B1` |
| `B10/1` | `B10104` | 9532:`B10/1` |
| `B11/1` | `B11103` | 9126:`B11/1` |
| `B12/1` | `B12102` | 9046:`B12/1`; 9464:`B12/1` |
| `B15/1` | `B15101` | 8956:`B15/1`; 9030:`B15/1`; 9061:`B15/1`; 9067:`B15/1`; 9070:`B15/1`; 9080:`B15/1`; 9444:`B15/1` |
| `B18/1` | `B18100` | 8854:`B18/1`; 9298:`B18/1`; 9384:`B18/1` |
| `B21/1` | `B21099` | 8879:`B21/1` |
| `B39*18/1` | `B39098` | 8772:`B39*18/1` |
| `B46/31` | `B46097` | 8896:`B46/31`; 8905:`B46/31`; 9308:`B46/31` |
| `B48/16` | `B48095` | 8892:`B48/16`; 9293:`B48/16`; 9380:`B48/16` |
| `B48/25` | `B48096` | 9133:`B48/25` |
| `BADCAT` | `BAD073` | 8876:`BADCAT`; 8881:`BADCAT`; 8884:`BADCAT`; 8897:`BADCAT`; 8909:`BADCAT`; 8913:`BADCAT`; 8975:`BADCAT` |
| `BADPROG` | `BAD056` | 9043:`BADPROG`; 9059:`BADPROG`; 9083:`BADPROG` |
| `BCMES` | `BCM131` | 9503:`BCMES-LCMES` |
| `BCUN` | `BCU132` | 9502:`BCUN` |
| `BEG` | `BEG030` | 8765:`BEG` |
| `BLEXPRIN` | `BLE010` | 8841:`BLEXPRIN` |
| `C3` | `C3105` | 9072:`C3`; 9451:`C3`; 9484:`C3` |
| `CAT/2` | `CAT017` | 9172:`ERTAB-CAT/2-1` |
| `CHECOM` | `CHE051` | 9130:`CHECOM` |
| `CHLIS` | `CHL039` | 8921:`CHLIS`; 8930:`CHLIS`; 8940:`CHLIS` |
| `DELBP` | `DEL058` | 9203:`DELBP` |
| `DELMES` | `DEL114` | 8949:`DELMES` |
| `DELNAM` | `DEL115` | 8946:`DELNAM` |
| `DELPRI` | `DEL040` | 8919:`DELPRI` |
| `EMMES` | `EMM134` | 9505:`LCMES-EMMES`; 9507:`EMMES-LLMES` |
| `EMPLIB` | `EMP075` | 9237:`EMPLIB` |
| `ENTMES` | `ENT125` | 9487:`ENTMES` |
| `ERROFLG*` | `ERR007` | 8839:`ERROFLG*` |
| `FILCAT` | `FIL126` | 9486:`FILCAT`; 9489:`FILCAT` |
| `FILLIB` | `FIL130` | 9265:`FILLIB`; 9270:`FILLIB+1` |
| `FINPRI` | `FIN072` | 9476:`FINPRI` |
| `FLBP` | `FLB154` | 9009:`FLBP`; 9196:`FLBP`; 9201:`FLBP`; 9234:`FLBP` |
| `FLDL` | `FLD152` | 8812:`FLDL`; 8929:`FLDL` |
| `FLNP` | `FLN153` | 8863:`FLNP`; 9366:`FLNP`; 9410:`FLNP` |
| `FULISFL*` | `FUL005` | 9412:`FULISFL*`; 9423:`FULISFL*` |
| `FULW` | `FUL094` | 8972:`FULW`; 8981:`FULW`; 9319:`FULW` |
| `GETID` | `GET049` | 9111:`GETID`; 9114:`GETID` |
| `GOBACK` | `GOB089` | 8824:`GOBACK` |
| `GOSEQ` | `GOS088` | 8828:`GOSEQ` |
| `HEADBP` | `HEA116` | 9198:`HEADBP` |
| `HEADPR` | `HEA119` | 9419:`HEADPR` |
| `HELDRU` | `HEL121` | 9389:`HELDRU` |
| `HELMEM` | `HEL122` | 9407:`HELMEM` |
| `HENAME` | `HEN120` | 9416:`HENAME` |
| `HENT` | `HEN123` | 9428:`HENT` |
| `HEXT` | `HEX124` | 9458:`HEXT` |
| `IFNEX` | `IFN082` | 9528:`IFNEX` |
| `IFSET` | `IFS083` | 9282:`IFSET`; 9540:`IFSET` |
| `ILINE` | `ILI093` | 9596:`ILINE`; 9601:`ILINE` |
| `INFPR` | `INF092` | 8950:`INFPR`; 9199:`INFPR`; 9420:`INFPR`; 9429:`INFPR`; 9459:`INFPR`; 9494:`INFPR`; 9510:`INFPR`; 9512:`INFPR` |
| `IPR` | `IPR090` | 8849:`IPR`; 8852:`IPR`; 8855:`IPR` |
| `IPW` | `IPW091` | 8860:`IPW` |
| `IUA` | `IUA138` | 8773:`IUA`; 8799:`IUA`; 8851:`IUA`; 8856:`IUA`; 9019:`IUA`; 9367:`IUA` |
| `IUL` | `IUL140` | 8777:`IUL`; 8819:`IUL`; 9259:`IUL` |
| `IUN` | `IUN139` | 8775:`IUN`; 8805:`IUN`; 8859:`IUN` |
| `IUO` | `IUO137` | 8770:`IUO`; 8787:`IUO`; 8848:`IUO`; 8850:`IUO`; 8858:`IUO`; 8977:`IUO`; 8999:`IUO`; 9357:`IUO` |
| `LCAT` | `LCA141` | 8990:`LCAT`; 9001:`LCAT`; 9136:`LCAT`; 9215:`LCAT`; 9220:`LCAT`; 9244:`LCAT`; 9332:`LCAT`; 9359:`LCAT`; 9449:`LCAT`; 9482:`LCAT` |
| `LCMES` | `LCM133` | 9503:`BCMES-LCMES`; 9505:`LCMES-EMMES` |
| `LCTL` | `LCT142` | 9248:`LCTL`; 9272:`LCTL`; 9348:`LCTL` |
| `LDEC` | `LDE149` | 9055:`LDEC`; 9074:`LDEC` |
| `LDEF` | `LDE150` | 9047:`LDEF`; 9097:`LDEF` |
| `LDRU` | `LDR146` | 9077:`LDRU`; 9179:`LDRU`; 9184:`LDRU` |
| `LENMES` | `LEN129` | 9493:`LENMES` |
| `LGOSEQ` | `LGO004` | 8825:`LGOSEQ`; 8829:`LGOSEQ` |
| `LIBLIST` | `LIB113` | 8826:`LIBLIST`; 8924:`LIBLIST` |
| `LIND` | `LIN144` | 9011:`LIND`; 9176:`LIND`; 9188:`LIND`; 9189:`LIND` |
| `LINE` | `LIN158` | 9585:`LINE-2`; 9597:`LINE-2`; 9619:`LINE` |
| `LLIB` | `LLI143` | 9008:`LLIB`; 9185:`LLIB`; 9186:`LLIB`; 9236:`LLIB`; 9255:`LLIB` |
| `LLMES` | `LLM135` | 9507:`EMMES-LLMES`; 9509:`LLMES` |
| `LMEM` | `LME147` | 9031:`LMEM`; 9082:`LMEM` |
| `LOADANGO` | `LOA003` | 8716:`LOADANGO+17`; 8827:`LOADANGO` |
| `LONCAT` | `LON074` | 8969:`LONCAT`; 8992:`LONCAT`; 9156:`LONCAT`; 9250:`LONCAT` |
| `LONLIB` | `LON076` | 9260:`LONLIB` |
| `MINUS` | `MIN029` | 8809:`PLUS-MINUS` |
| `MPERS` | `MPE111` | 8872:`MTEMP-MPERS`; 8873:`MPERS` |
| `MTEMP` | `MTE110` | 8872:`MTEMP-MPERS` |
| `NEXBP` | `NEX057` | 9197:`NEXBP` |
| `NOADD` | `NOA032` | 8784:`NOADD` |
| `NOLISFL*` | `NOL006` | 8943:`NOLISFL*`; 9401:`NOLISFL*` |
| `NOMES` | `NOM136` | 9511:`NOMES` |
| `NOPAR` | `NOP034` | 8783:`NOPAR`; 8822:`NOPAR` |
| `NOPRENT` | `NOP070` | 9425:`NOPRENT`; 9430:`NOPRENT` |
| `NOREF` | `NOR055` | 9174:`NOREF` |
| `NPR` | `NPR015` | 9610:`NPR` |
| `NPW` | `NPW016` | 9612:`NPW` |
| `PARAMT*` | `PAR012` | 8781:`PARAMT*`; 8788:`PARAMT*`; 8793:`PARAMT*`; 8801:`PARAMT*`; 8815:`PARAMT*`; 8820:`PARAMT*` |
| `PLUS` | `PLU028` | 8807:`-PLUS`; 8809:`PLUS-MINUS` |
| `POIN` | `POI155` | 8895:`POIN`; 8904:`POIN`; 8906:`POIN`; 8907:`POIN`; 8957:`POIN`; 8961:`POIN` |
| `PREFE` | `PRE046` | 9018:`PREFE`; 9028:`PREFE` |
| `PREFEND` | `PRE060` | 9024:`PREFEND` |
| `PREFP` | `PRE045` | 9190:`PREFP`; 9231:`PREFP` |
| `PRIHE` | `PRI069` | 9411:`PRIHE` |
| `PRILE` | `PRI087` | 9594:`PRILE`; 9595:`PRILE` |
| `PRILIS` | `PRI084` | 9204:`PRILIS`; 9431:`PRILIS`; 9461:`PRILIS` |
| `PRILN` | `PRI085` | 9600:`PRILN` |
| `PRILR` | `PRI086` | 9207:`PRILR`; 9434:`PRILR`; 9469:`PRILR`; 9471:`PRILR` |
| `PRINT8` | `PRI009` | 9492:`PRINT8` |
| `PROCREF` | `PRO044` | 9235:`PROCREF` |
| `PROGRAM` | `PRO112` | 8915:`PROGRAM` |
| `PT6/G` | `PT6013` | 8948:`PT6/G`; 9418:`PT6/G`; 9592:`PT6/G` |
| `RBEGP` | `RBE078` | 8869:`RBEGP`; 9036:`RBEGP`; 9088:`RBEGP`; 9382:`RBEGP` |
| `RCAT` | `RCA002` | 8771:`RCAT` |
| `RCATEND` | `RCA043` | 8891:`RCATEND` |
| `RCATL` | `RCA035` | 8987:`RCATL` |
| `RCATW` | `RCA036` | 8965:`RCATW`; 8967:`RCATW` |
| `RDBUF` | `RDB014` | 8734:`(RDBUF)16`; 9535:`RDBUF`; 9558:`RDBUF` |
| `RDECW` | `RDE047` | 9094:`RDECW` |
| `REXCH` | `REX079` | 9561:`REXCH` |
| `RIF` | `RIF156` | 8844:`RIF+IWP`; 8853:`RIF+IWI`; 8978:`RIF+IWI`; 9000:`RIF+IWI`; 9020:`RIF+IWI`; 9358:`RIF+IWI`; 9368:`RIF+IWI`; 9499:`RIF+IWI`; 9537:`RIF`; 9560:`RIF` |
| `RNEXP` | `RNE081` | 8968:`RNEXP`; 9552:`RNEXP` |
| `RNEXT` | `RNE042` | 8916:`RNEXT`; 8926:`RNEXT`; 8932:`RNEXT`; 8944:`RNEXT`; 8952:`RNEXT` |
| `RNEXW` | `RNE080` | 9091:`RNEXW`; 9395:`RNEXW` |
| `RSKIP` | `RSK037` | 8893:`RSKIP` |
| `SECAT` | `SEC052` | 9138:`SECAT`; 9149:`SECAT` |
| `SEXT` | `SEX048` | 9117:`SEXT`; 9142:`SEXT`; 9147:`SEXT`; 9165:`SEXT` |
| `SEXTEND` | `SEX054` | 9101:`SEXTEND` |
| `SHIBP` | `SHI059` | 9226:`SHIBP` |
| `SHORT` | `SHO050` | 9123:`SHORT` |
| `STOP*` | `STO008` | 8840:`STOP*`; 8842:`STOP*`; 9513:`STOP*` |
| `TEMP` | `TEM033` | 8797:`TEMP` |
| `TLDRU` | `TLD117` | 9388:`TLDRU` |
| `TLLIB1` | `TLL127` | 9264:`TLLIB1` |
| `TLLIB2` | `TLL128` | 9269:`TLLIB2` |
| `TLMEM` | `TLM118` | 9406:`TLMEM` |
| `TRANSE` | `TRA067` | 9365:`TRANSE`; 9378:`TRANSE` |
| `TRANSP` | `TRA066` | 9402:`TRANSP`; 9413:`TRANSP`; 9424:`TRANSP`; 9439:`TRANSP`; 9460:`TRANSP` |
| `TRANSW` | `TRA068` | 9397:`TRANSW`; 9399:`TRANSW` |
| `TREND` | `TRE071` | 9373:`TREND` |
| `TYPE` | `TYP151` | 9108:`TYPE`; 9121:`TYPE`; 9124:`TYPE` |
| `WCATEND` | `WCA063` | 9290:`WCATEND` |
| `WIF` | `WIF157` | 8861:`WIF+IWI`; 9281:`WIF`; 9523:`WIF` |
| `WNEXW` | `WNE077` | 9291:`WNEXW`; 9312:`WNEXW`; 9315:`WNEXW`; 9318:`WNEXW`; 9320:`WNEXW`; 9326:`WNEXW`; 9328:`WNEXW`; 9338:`WNEXW`; 9344:`WNEXW`; 9354:`WNEXW`; 9396:`WNEXW`; 9479:`WNEXW` |
| `WRCAT` | `WRC061` | 9294:`WRCAT` |
| `WREF` | `WRE053` | 9153:`WREF` |
| `WREFT` | `WRE064` | 9340:`WREFT` |
| `WRENT` | `WRE041` | 8920:`WRENT`; 8931:`WRENT` |
| `WRLIS` | `WRL065` | 9346:`WRLIS` |
| `WSKIP` | `WSK062` | 9295:`WSKIP` |
| `Z12/6` | `Z12109` | 9577:`Z12/6` |
| `Z47` | `Z47108` | 8983:`Z47`; 9227:`Z47` |
| `Z48` | `Z48107` | 9310:`Z48` |

## 3. Вызовы и переходы (VJM / CALL / UJ)

| Строка | Команда | Операнд |
|---|---|---|
| S1:8781 | `CALL` | `PARAMT*` |
| S1:8788 | `CALL` | `PARAMT*` |
| S1:8793 | `CALL` | `PARAMT*` |
| S1:8801 | `CALL` | `PARAMT*` |
| S1:8815 | `CALL` | `PARAMT*` |
| S1:8820 | `CALL` | `PARAMT*` |
| S1:8827 | `CALL` | `LOADANGO` |
| S1:8869 | `VJM` | `RBEGP` |
| S1:8940 | `UJ` | `CHLIS` |
| S1:8948 | `CALL` | `PT6/G` |
| S1:8952 | `UJ` | `RNEXT` |
| S1:8969 | `UJ` | `LONCAT` |
| S1:9036 | `VJM` | `RBEGP` |
| S1:9088 | `VJM` | `RBEGP` |
| S1:9091 | `VJM` | `RNEXW` |
| S1:9130 | `UJ` | `CHECOM` |
| S1:9165 | `UJ` | `SEXT` |
| S1:9190 | `UJ` | `PREFP` |
| S1:9204 | `VJM` | `PRILIS` |
| S1:9207 | `UJ` | `PRILR` |
| S1:9231 | `UJ` | `PREFP` |
| S1:9282 | `VJM` | `IFSET` |
| S1:9291 | `VJM` | `WNEXW` |
| S1:9318 | `VJM` | `WNEXW` |
| S1:9320 | `VJM` | `WNEXW` |
| S1:9326 | `VJM` | `WNEXW` |
| S1:9328 | `VJM` | `WNEXW` |
| S1:9338 | `VJM` | `WNEXW` |
| S1:9344 | `VJM` | `WNEXW` |
| S1:9382 | `VJM` | `RBEGP` |
| S1:9395 | `VJM` | `RNEXW` |
| S1:9396 | `VJM` | `WNEXW` |
| S1:9418 | `CALL` | `PT6/G` |
| S1:9431 | `VJM` | `PRILIS` |
| S1:9434 | `UJ` | `PRILR` |
| S1:9461 | `VJM` | `PRILIS` |
| S1:9485 | `CALL` | `A/OCTDEC` |
| S1:9492 | `CALL` | `PRINT8` |
| S1:9496 | `UJ` | `(через индексный регистр)` |
| S1:9513 | `UJ` | `STOP*` |
| S1:9528 | `UJ` | `IFNEX` |
| S1:9540 | `VJM` | `IFSET` |
| S1:9548 | `UJ` | `(через индексный регистр)` |
| S1:9552 | `VJM` | `RNEXP` |
| S1:9555 | `UJ` | `(через индексный регистр)` |
| S1:9579 | `UJ` | `(через индексный регистр)` |
| S1:9589 | `UJ` | `(через индексный регистр)` |
| S1:9592 | `CALL` | `PT6/G` |
| S1:9603 | `UJ` | `(через индексный регистр)` |
| S1:9606 | `UJ` | `(через индексный регистр)` |
| S1:9608 | `UJ` | `(через индексный регистр)` |

## 4. Внешние символы (не определены в модуле)

- `A/OCTDEC`

## 5. Литералы → EQU

| EQU | Значение | Строка |
|---|---|---|
| `MIN029` | `55B` | S1:8759 |
| `PLU028` | `53B` | S1:8758 |
| `LGO004` | `LOA003+17` | S1:8716 |
| `RCA002` | `47B` | S1:8713 |
| `EDC015` | `61` | S1:8649 |
| `EDC016` | `1` | S1:8717 |
| `EDC017` | `12` | S1:8726 |
| `EDC018` | `1024` | S1:8729 |
| `EDC019` | `0` | S1:8730 |
| `EDC020` | `2048` | S1:8731 |
| `EDC021` | `4096` | S1:8732 |
| `EDC022` | `8192` | S1:8733 |
| `EDC023` | `16` | S1:8734 |
| `EDC024` | `2` | S1:8736 |
| `ETX024` | `=65 0000` | S1:8769 |
| `ETX025` | `=66 0000` | S1:8774 |
| `ETX026` | `=1000` | S1:8776 |
| `EDC026` | `4` | S1:8786 |
| `EDC027` | `6` | S1:8792 |
| `ETX027` | `=4HTEMP` | S1:8795 |
| `ETX028` | `=67 0000` | S1:8798 |
| `EDC028` | `5` | S1:8818 |
| `EDC029` | `7` | S1:8832 |
| `EDC030` | `3` | S1:8837 |
| `ETX030` | `=21 00000` | S1:8880 |
| `ETX031` | `=7 00000` | S1:8882 |
| `EOC031` | `776B` | S1:8886 |
| `EDC031` | `64` | S1:8898 |
| `EDC032` | `20` | S1:8898 |
| `EDC033` | `25` | S1:8903 |
| `ETX033` | `=:2` | S1:8908 |
| `EOC033` | `777B` | S1:8966 |
| `EDC034` | `13` | S1:8991 |
| `EDC035` | `15` | S1:9027 |
| `EDC036` | `10` | S1:9034 |
| `ETX036` | `=7777 0000 7777` | S1:9041 |
| `EDC037` | `36` | S1:9049 |
| `EDC038` | `30` | S1:9052 |
| `EDC039` | `11` | S1:9058 |
| `ETX039` | `=37` | S1:9075 |
| `EDC040` | `18` | S1:9107 |
| `ETX040` | `=57` | S1:9109 |
| `ETX041` | `=42` | S1:9110 |
| `ETX042` | `=47` | S1:9112 |
| `ETX043` | `=4` | S1:9116 |
| `ETX044` | `=20` | S1:9122 |
| `EDC044` | `42` | S1:9140 |
| `ETX045` | `=12` | S1:9141 |
| `EDC045` | `48` | S1:9154 |
| `EOC045` | `17777B` | S1:9155 |
| `EOC046` | `20000B` | S1:9157 |
| `EOC047` | `100B` | S1:9252 |
| `EDC047` | `31` | S1:9262 |
| `ETX047` | `=6H'''''7''7''7''7'` | S1:9263 |
| `EDC048` | `43` | S1:9267 |
| `ETX048` | `=6H'''3''7'''''''` | S1:9268 |
| `EDC049` | `19` | S1:9273 |
| `EOC049` | `1775B` | S1:9283 |
| `EOC050` | `67B` | S1:9323 |
| `ETX050` | `=6H'3''17''17''17''17''17'` | S1:9324 |
| `ETX051` | `=6H000000` | S1:9325 |
| `EOC051` | `37B` | S1:9351 |
| `EDC051` | `37` | S1:9386 |
| `ETX052` | `=6H'''7''7''''3''7'` | S1:9387 |
| `ETX053` | `=6H'7''7''7''7''7'''` | S1:9405 |
| `EOC053` | `2000B` | S1:9477 |
| `ETX054` | `=6H'7''7''7''7''7''7'` | S1:9501 |
| `EOC054` | `1777B` | S1:9526 |
| `ETX055` | `=2777 6000` | S1:9538 |
| `ETX056` | `=4 0000 0000 3777` | S1:9539 |
| `ETX057` | `=10 0000` | S1:9570 |
| `ETX058` | `=40 0000` | S1:9571 |
| `ETX059` | `=3740` | S1:9574 |
| `EDC059` | `9` | S1:9586 |
| `ETX060` | `7777 7777 7777 7777` | S1:9624 |
| `ETX061` | `7777 7777 777` | S1:9625 |
| `ETX062` | `7777 7777` | S1:9626 |
| `ETX063` | `1777 77` | S1:9627 |
| `ETX064` | `4 0000 0077 7777` | S1:9628 |
| `ETX065` | `777 7777` | S1:9629 |
| `ETX066` | `77 7777` | S1:9630 |
| `ETX067` | `7 7777` | S1:9631 |
| `ETX068` | `7777` | S1:9632 |
| `ETX069` | `3777` | S1:9633 |
| `ETX070` | `1777` | S1:9634 |
| `ETX071` | `3` | S1:9635 |
| `ETX072` | `1` | S1:9636 |
| `ETX073` | `3777 7777 7777 7777` | S1:9637 |
| `ETX074` | `5777 7777 7777 7777` | S1:9638 |
| `ETX075` | `7777 7777 7777 0037` | S1:9639 |
| `ETX076` | `7777 7777 7000 0037` | S1:9640 |
| `ETX077` | `7776 0000 7000 0037` | S1:9641 |
| `ETX078` | `7HPROGRAM` | S1:9643 |
| `ETX079` | `7HLIBLIST` | S1:9644 |
| `ETX080` | `18H   ИCKЛЮЧEH BXOД:` | S1:9645 |
| `ETX081` | `2` | S1:9646 |
| `ETX082` | `1H'231'` | S1:9647 |
| `ETX083` | `24HИCПOPЧEHЫ ПOДПPOГPAMMЫ:'231'` | S1:9648 |
| `ETX084` | `6H 00 00` | S1:9649 |
| `ETX085` | `6H00000'231'` | S1:9650 |
| `ETX086` | `24H    BKЛЮЧEHA ПPOГPAMMA:` | S1:9651 |
| `ETX087` | `6HДЛИHA:` | S1:9653 |
| `ETX088` | `12H    ПAMЯTЬ:` | S1:9655 |
| `ETX089` | `7HBXOДЫ:'231'` | S1:9657 |
| `ETX090` | `8HCCЫЛKИ:'231'` | S1:9658 |
| `ETX091` | `30HЧИCЛO ПOДПPOГPAMM И BXOДOB:` | S1:9659 |
| `ETX092` | `6HY 0000` | S1:9661 |
| `ETX093` | `6H 00'231'` | S1:9662 |
| `ETX094` | `12HДЛИHA LIBRAR` | S1:9663 |
| `ETX095` | `18HИCПOPЧEH KATAЛOГ:` | S1:9665 |
| `ETX096` | `3H '133''231'` | S1:9667 |
| `ETX097` | `20HПEPEПOЛHEH KATAЛOГ'133''231'` | S1:9668 |
| `ETX098` | `17HHET ПOДПPOГPAMM'133''231'` | S1:9669 |
| `ETX099` | `9HMAЛO MЛ'133''231'` | S1:9670 |
| `ETX100` | `24HБИБЛИOTEKA HE ЗAПИCAHA'133''231'` | S1:9671 |
| `ETX101` | `20` | S1:9694 |

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **0**.
- TEXT-констант переименовано по содержимому: **0**.
- Смещений `LABEL+NNNB` → десятичное: **1**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_sys.txt`.
