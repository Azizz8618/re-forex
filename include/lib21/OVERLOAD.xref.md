# OVERLOAD — перекрёстные ссылки

Модуль `OVERLOAD` (исходник `libra212.l21:8847-9746`). Сверка: `disasm/lib21/OVERLOAD.madlen`.

Все метки переименованы в ≤6 символов (уникальные первые 6); полные имена сохранены в `; (POLN: ...)` в `src/lib21/OVERLOAD.mad`.

## 1. Таблица символов (метки и EQU)

| Короткое имя | Полное имя (POLN) | Тип | Строка |
|---|---|---|---|
| `OVE001` | `OVERLOAD` | метка | libra212.l21:8847 |
| `SEC002` | `SECENTRY` | метка | libra212.l21:8909 |
| `ALF003` | `ALF1` | метка | libra212.l21:8910 |
| `ALF004` | `ALF2` | метка | libra212.l21:8911 |
| `LEX005` | `LEX` | метка | libra212.l21:8912 |
| `ALF006` | `ALFA` | метка | libra212.l21:8913 |
| `WLE007` | `WLEX` | метка | libra212.l21:8914 |
| `RCA008` | `RCAT` | метка | libra212.l21:8915 |
| `RET009` | `RETN` | метка | libra212.l21:8916 |
| `LDR010` | `LDRM` | метка | libra212.l21:8917 |
| `RLO011` | `RLOAD` | метка | libra212.l21:8918 |
| `LTA012` | `LTAPES` | метка | libra212.l21:8919 |
| `MON013` | `MONITOR*` | метка | libra212.l21:8921 |
| `MON014` | `MONCARD/` | метка | libra212.l21:8922 |
| `DAT015` | `DATA*` | метка | libra212.l21:8923 |
| `MON016` | `MONCARD*` | метка | libra212.l21:8924 |
| `LOA017` | `LOADLIS*` | метка | libra212.l21:8925 |
| `ERR018` | `ERROFLG*` | метка | libra212.l21:8926 |
| `RM019` | `RM*` | метка | libra212.l21:8927 |
| `KCO020` | `KCOUNT*` | метка | libra212.l21:8928 |
| `STO021` | `STOP*` | метка | libra212.l21:8930 |
| `MON022` | `MONREAD*` | метка | libra212.l21:8931 |
| `PRI023` | `PRINT8` | метка | libra212.l21:8932 |
| `SAV024` | `SAV*47` | метка | libra212.l21:8934 |
| `BLE025` | `BLEXPRIN` | метка | libra212.l21:8935 |
| `MON026` | `*MONCRD*` | метка | libra212.l21:8937 |
| `LTR027` | `LTREE` | метка | libra212.l21:8938 |
| `TRE028` | `TREE` | метка | libra212.l21:8939 |
| `PAR029` | `PARAMT*` | метка | libra212.l21:8940 |
| `BUF030` | `BUFP` | метка | libra212.l21:8942 |
| `LCA031` | `LCAT` | метка | libra212.l21:8943 |
| `ECA032` | `ECAT` | метка | libra212.l21:8944 |
| `NB033` | `/NB` | метка | libra212.l21:8945 |
| `LDL034` | `LDLP` | метка | libra212.l21:8947 |
| `NL035` | `/NL` | метка | libra212.l21:8948 |
| `N1036` | `*1` | метка | libra212.l21:8950 |
| `N5038` | `*5` | метка | libra212.l21:8952 |
| `N9039` | `*9` | метка | libra212.l21:8953 |
| `N13040` | `*13` | метка | libra212.l21:8954 |
| `LPA041` | `/LPAR` | метка | libra212.l21:8956 |
| `RPA042` | `/RPAR` | метка | libra212.l21:8957 |
| `PLU043` | `/PLUS` | метка | libra212.l21:8958 |
| `COM044` | `/COM` | метка | libra212.l21:8959 |
| `TWO045` | `/TWOP` | метка | libra212.l21:8960 |
| `RCA046` | `R CARD` | метка | libra212.l21:9010 |
| `CPO047` | `C.....   ПPOBEPKA` | метка | libra212.l21:9011 |
| `PRI048` | `PRI` | метка | libra212.l21:9035 |
| `PAR049` | `PARAM` | метка | libra212.l21:9042 |
| `PAR050` | `PAR1` | метка | libra212.l21:9052 |
| `SNA051` | `S/NAM` | метка | libra212.l21:9077 |
| `PLU052` | `*PLUS` | метка | libra212.l21:9094 |
| `XEO053` | `*EOC` | метка | libra212.l21:9107 |
| `COM054` | `*COM` | метка | libra212.l21:9110 |
| `LPA055` | `*LPAR` | метка | libra212.l21:9114 |
| `RPA056` | `*RPAR` | метка | libra212.l21:9120 |
| `NEX057` | `NEXT` | метка | libra212.l21:9128 |
| `WRI058` | `WRI` | метка | libra212.l21:9131 |
| `WRE059` | `WRE` | метка | libra212.l21:9148 |
| `MIS060` | `MIST` | метка | libra212.l21:9151 |
| `PRI061` | `PRIER` | метка | libra212.l21:9157 |
| `FIN062` | `FIN` | метка | libra212.l21:9165 |
| `FIN063` | `FIN1` | метка | libra212.l21:9177 |
| `VEC064` | `VECT` | метка | libra212.l21:9189 |
| `VEC065` | `VEC` | метка | libra212.l21:9198 |
| `VEC066` | `VECT1` | метка | libra212.l21:9225 |
| `CHV067` | `CH V` | метка | libra212.l21:9246 |
| `CHB068` | `CH BR` | метка | libra212.l21:9268 |
| `END069` | `END BR` | метка | libra212.l21:9274 |
| `BF1070` | `OVL_BUFFER_1070` | метка | libra212.l21:9308 |
| `DIF071` | `DIF` | метка | libra212.l21:9335 |
| `RD6072` | `OVL_MEM_READ_6072` | метка | libra212.l21:9338 |
| `LOA073` | `LOADER` | метка | libra212.l21:9346 |
| `LOA074` | `LOAD` | метка | libra212.l21:9373 |
| `RCT075` | `RCTW` | метка | libra212.l21:9404 |
| `RCT076` | `RCTE` | метка | libra212.l21:9412 |
| `RES077` | `RES CT` | метка | libra212.l21:9419 |
| `END078` | `END CT` | метка | libra212.l21:9423 |
| `LOA079` | `LOAD1` | метка | libra212.l21:9425 |
| `FIR080` | `FIR*LEV` | метка | libra212.l21:9450 |
| `PRE081` | `PRESS` | метка | libra212.l21:9478 |
| `SEE082` | `SE/EQ` | метка | libra212.l21:9483 |
| `EQU083` | `EQU0` | метка | libra212.l21:9499 |
| `EQU084` | `EQU` | метка | libra212.l21:9502 |
| `WRI085` | `WRI1` | метка | libra212.l21:9512 |
| `LWR086` | `LWRI` | метка | libra212.l21:9529 |
| `EWR087` | `EWRI` | метка | libra212.l21:9535 |
| `FIN088` | `FINI` | метка | libra212.l21:9537 |
| `MIX089` | `MIX` | метка | libra212.l21:9543 |
| `COP090` | `COP FR` | метка | libra212.l21:9576 |
| `END091` | `END FR` | метка | libra212.l21:9584 |
| `VOI092` | `VOID FR` | метка | libra212.l21:9587 |
| `FIN093` | `FINT` | метка | libra212.l21:9590 |
| `WOR094` | `WORD` | метка | libra212.l21:9595 |
| `C095` | `C=====   П/П` | метка | libra212.l21:9596 |
| `IWS096` | `IWSET` | метка | libra212.l21:9611 |
| `FIN097` | `FIN LOAD` | метка | libra212.l21:9624 |
| `FLO098` | `FLO 1` | метка | libra212.l21:9641 |
| `HEM099` | `HE MAЛ` | метка | libra212.l21:9650 |
| `RNE101` | `RNEXP` | метка | libra212.l21:9662 |
| `RBE102` | `RBEGP` | метка | libra212.l21:9665 |
| `IPR103` | `IPRI` | метка | libra212.l21:9674 |
| `ICC104` | `ICCO` | метка | libra212.l21:9678 |
| `ICC105` | `ICCT` | метка | libra212.l21:9680 |
| `ICL106` | `ICLL` | метка | libra212.l21:9682 |
| `IRL107` | `IRLL` | метка | libra212.l21:9684 |
| `ITC108` | `ITC` | метка | libra212.l21:9687 |
| `IT0109` | `IT0` | метка | libra212.l21:9689 |
| `LIM110` | `LIM NZ` | метка | libra212.l21:9690 |
| `XT111` | `XT` | метка | libra212.l21:9691 |
| `Z12112` | `Z12/6` | метка | libra212.l21:9693 |
| `B48113` | `B48` | метка | libra212.l21:9694 |
| `B47114` | `B47` | метка | libra212.l21:9695 |
| `B40115` | `B40` | метка | libra212.l21:9696 |
| `B26116` | `B26` | метка | libra212.l21:9697 |
| `B18117` | `B18` | метка | libra212.l21:9698 |
| `B16118` | `B16` | метка | libra212.l21:9699 |
| `C77119` | `C77777` | метка | libra212.l21:9700 |
| `C37120` | `C3740` | метка | libra212.l21:9701 |
| `C17121` | `C1777` | метка | libra212.l21:9702 |
| `C37122` | `C37` | метка | libra212.l21:9703 |
| `C10123` | `C10` | метка | libra212.l21:9704 |
| `B2124` | `B2` | метка | libra212.l21:9705 |
| `B1125` | `B1` | метка | libra212.l21:9706 |
| `FRA126` | `FRAG TPП` | метка | libra212.l21:9707 |
| `TMA127` | `TMAЛ` | метка | libra212.l21:9708 |
| `T128` | `TДЛИ` | метка | libra212.l21:9709 |
| `UPM129` | `UPM` | метка | libra212.l21:9710 |
| `CGT130` | `CGT` | метка | libra212.l21:9711 |
| `CAL131` | `CALFA` | метка | libra212.l21:9712 |
| `CRC132` | `CRCAT` | метка | libra212.l21:9713 |
| `CLD133` | `CLDRM` | метка | libra212.l21:9714 |
| `CTN134` | `CTN` | метка | libra212.l21:9715 |
| `FMI135` | `FMIX` | метка | libra212.l21:9716 |
| `FRE136` | `FRES` | метка | libra212.l21:9717 |
| `ITL137` | `ITL` | метка | libra212.l21:9718 |
| `IWC138` | `IWCT` | метка | libra212.l21:9719 |
| `NAM139` | `NAME` | метка | libra212.l21:9720 |
| `ETA140` | `ETAL` | метка | libra212.l21:9721 |
| `AP141` | `AP` | метка | libra212.l21:9722 |
| `PAP142` | `PAP` | метка | libra212.l21:9723 |
| `IRD143` | `IRD` | метка | libra212.l21:9724 |
| `ELO144` | `ELOADER` | метка | libra212.l21:9725 |
| `NON145` | `NONTEX` | метка | libra212.l21:9728 |
| `ERC146` | `ERCA` | метка | libra212.l21:9729 |
| `ERP147` | `ERPAR` | метка | libra212.l21:9730 |
| `LON148` | `LONCAT` | метка | libra212.l21:9731 |
| `EMP149` | `EMPCAT` | метка | libra212.l21:9732 |
| `SOO150` | `SOONDF` | метка | libra212.l21:9733 |
| `DUP151` | `DUPDEF` | метка | libra212.l21:9734 |
| `ERT152` | `ERTA` | метка | libra212.l21:9735 |
| `TOV153` | `TOV` | метка | libra212.l21:9736 |
| `EOR154` | `*EOR` | метка | libra212.l21:9737 |
| `MON155` | `MON*` | метка | libra212.l21:9738 |
| `B48156` | `B48*L` | метка | libra212.l21:9739 |
| `B45157` | `B45` | метка | libra212.l21:9740 |
| `PLU158` | `PLUS` | метка | libra212.l21:9742 |
| `PL159` | `PL*` | метка | libra212.l21:9743 |
| `DIF071` | `DIF` | EQU = `ELO144-LOA073` | S2:9335 |
| `TWO045` | `/TWOP` | EQU = `72B` | S2:8960 |
| `COM044` | `/COM` | EQU = `54B` | S2:8959 |
| `PLU043` | `/PLUS` | EQU = `53B` | S2:8958 |
| `RPA042` | `/RPAR` | EQU = `51B` | S2:8957 |
| `LPA041` | `/LPAR` | EQU = `50B` | S2:8956 |
| `LDL034` | `LDLP` | EQU = `2000B` | S2:8947 |
| `ECA032` | `ECAT` | EQU = `BUF030+LCA031` | S2:8944 |
| `LCA031` | `LCAT` | EQU = `1762B` | S2:8943 |
| `LTR027` | `LTREE` | EQU = `2020` | S2:8938 |
| `LTA012` | `LTAPES` | EQU = `73B` | S2:8919 |
| `RLO011` | `RLOAD` | EQU = `61B` | S2:8918 |
| `LDR010` | `LDRM` | EQU = `54B` | S2:8917 |
| `RET009` | `RETN` | EQU = `51B` | S2:8916 |
| `RCA008` | `RCAT` | EQU = `47B` | S2:8915 |
| `WLE007` | `WLEX` | EQU = `46B` | S2:8914 |
| `ALF006` | `ALFA` | EQU = `44B` | S2:8913 |
| `LEX005` | `LEX` | EQU = `43B` | S2:8912 |
| `ALF004` | `ALF2` | EQU = `17B` | S2:8911 |
| `ALF003` | `ALF1` | EQU = `16B` | S2:8910 |
| `SEC002` | `SECENTRY` | EQU = `15B` | S2:8909 |
| `EDC016` | `DEC_60` | EQU = `60` | S2:8848 |
| `EDC017` | `DEC_1` | EQU = `1` | S2:8934 |
| `EDC018` | `DEC_12` | EQU = `12` | S2:8937 |
| `EDC019` | `DEC_16` | EQU = `16` | S2:8945 |
| `EDC020` | `DEC_4` | EQU = `4` | S2:8971 |
| `EDC021` | `DEC_8` | EQU = `8` | S2:8983 |
| `EDC022` | `DEC_5` | EQU = `5` | S2:8985 |
| `ETX022` | `LITERAL__777` | EQU = `=777` | S2:8988 |
| `EDC023` | `DEC_64` | EQU = `64` | S2:8989 |
| `EDC024` | `DEC_10` | EQU = `10` | S2:8989 |
| `EDC025` | `DEC_40` | EQU = `40` | S2:9013 |
| `EDC026` | `DEC_14` | EQU = `14` | S2:9019 |
| `EDC027` | `DEC_13` | EQU = `13` | S2:9021 |
| `EDC028` | `DEC_9` | EQU = `9` | S2:9030 |
| `EDC029` | `DEC_6` | EQU = `6` | S2:9032 |
| `EDC030` | `DEC_3` | EQU = `3` | S2:9044 |
| `EDC031` | `DEC_2` | EQU = `2` | S2:9079 |
| `EDC032` | `DEC_15` | EQU = `15` | S2:9086 |
| `ETX032` | `LITERAL__7_7777_7770_0000` | EQU = `=7 7777 7770 0000` | S2:9088 |
| `EOC032` | `OCT_10` | EQU = `10B` | S2:9234 |
| `EOC033` | `OCT_2000` | EQU = `2000B` | S2:9296 |
| `EOC034` | `OCT_15` | EQU = `15B` | S2:9317 |
| `EOC035` | `OCT_12` | EQU = `12B` | S2:9334 |
| `EOC036` | `OCT_73413` | EQU = `73413B` | S2:9350 |
| `EDC036` | `DEC_7` | EQU = `7` | S2:9369 |
| `EDC037` | `DEC_30` | EQU = `30` | S2:9370 |
| `EDC038` | `DEC_24` | EQU = `24` | S2:9389 |
| `EOC038` | `OCT_1777` | EQU = `1777B` | S2:9405 |
| `EOC039` | `OCT_777` | EQU = `777B` | S2:9669 |
| `EOC040` | `OCT_77` | EQU = `77B` | S2:9678 |
| `ETX040` | `LIT_60_0000` | EQU = `60 0000` | S2:9689 |
| `ETX041` | `LIT_1000` | EQU = `1000` | S2:9690 |
| `ETX042` | `LIT_0000_4` | EQU = `0000 4` | S2:9691 |
| `ETX043` | `LIT_7777_7777_7777_0037` | EQU = `7777 7777 7777 0037` | S2:9693 |
| `ETX044` | `LIT_4` | EQU = `4` | S2:9694 |
| `ETX045` | `LIT_2` | EQU = `2` | S2:9695 |
| `ETX046` | `LIT_001` | EQU = `001` | S2:9696 |
| `ETX047` | `LIT_0000_0002` | EQU = `0000 0002` | S2:9697 |
| `ETX048` | `LIT_40_0000` | EQU = `40 0000` | S2:9698 |
| `ETX049` | `LIT_10_0000` | EQU = `10 0000` | S2:9699 |
| `ETX050` | `LIT_77777` | EQU = `77777` | S2:9700 |
| `ETX051` | `LIT_3740` | EQU = `3740` | S2:9701 |
| `ETX052` | `LIT_1777` | EQU = `1777` | S2:9702 |
| `ETX053` | `LIT_37` | EQU = `37` | S2:9703 |
| `ETX054` | `LIT_10` | EQU = `10` | S2:9704 |
| `ETX055` | `LIT_1` | EQU = `1` | S2:9706 |
| `ETX056` | `LIT_8HFRAG_TP_` | EQU = `8HFRAG TPП` | S2:9707 |
| `ETX057` | `LIT_18H_____MA_O_M_______231_` | EQU = `18H***  MAЛO MЛ  ***'231'` | S2:9708 |
| `ETX058` | `LIT_25H___HA______OTEK___077_37_23` | EQU = `25HДЛИHA БИБЛИOTEKИ  077 37'231'` | S2:9709 |
| `ETX059` | `LIT_6H_367_77037` | EQU = `6H'367'77037` | S2:9710 |
| `ETX060` | `LIT_6H000_00` | EQU = `6H000 00` | S2:9711 |
| `ETX061` | `LIT_24HHETEKCTOBA__KAPTA` | EQU = `24HHETEKCTOBAЯ KAPTA` | S2:9728 |
| `ETX062` | `LIT_24HO_` | EQU = `24HOШ` | S2:9729 |
| `ETX063` | `LIT_24HHET__AKP_BA__E__CKO_K_` | EQU = `24HHET ЗAKPЫBAЮЩEЙ CKOБKИ` | S2:9730 |
| `ETX064` | `LIT_24HC___KOM_MHO_O_PA__E_OB` | EQU = `24HCЛИШKOM MHOГO PAЗДEЛOB` | S2:9731 |
| `ETX065` | `LIT_24H_YCTA______` | EQU = `24HПYCTAЯ БИБЛ` | S2:9732 |
| `ETX066` | `LIT_24HPAHOBATO_O__CAH_PA__E_` | EQU = `24HPAHOBATO OПИCAH PAЗДEЛ` | S2:9733 |
| `ETX067` | `LIT_24H_OBTOP` | EQU = `24HПOBTOP` | S2:9734 |
| `ETX068` | `LIT_24H_____O___K__B__A_AH__` | EQU = `24HБЫЛИ OШИБKИ B ЗAДAHИИ` | S2:9735 |
| `ETX069` | `LIT_12HOVERLAY_OT` | EQU = `12HOVERLAY OT` | S2:9736 |
| `ETX070` | `LIT_6H_END_R` | EQU = `6H*END R` | S2:9737 |
| `ETX071` | `LIT_8HMONITOR_` | EQU = `8HMONITOR*` | S2:9738 |
| `ETX072` | `LIT_4007_7777_7770_0000` | EQU = `4007 7777 7770 0000` | S2:9739 |
| `ETX073` | `LIT_04` | EQU = `04` | S2:9740 |

## 2. Перекрёстные ссылки (определение → использования)

| Символ | Короткое | Использования (строка: операнд) |
|---|---|---|
| `*COM` | `COM054` | 9063:`*COM` |
| `*EOC` | `XEO053` | 9055:`*EOC`; 9100:`*EOC` |
| `*EOR` | `EOR154` | 9027:`*EOR` |
| `*LPAR` | `LPA055` | 9065:`*LPAR` |
| `*PLUS` | `PLU052` | 9058:`*PLUS` |
| `*RPAR` | `RPA056` | 9067:`*RPAR` |
| `/COM` | `COM044` | 9059:`/PLUS-/COM`; 9064:`/COM-/LPAR` |
| `/LPAR` | `LPA041` | 9064:`/COM-/LPAR`; 9066:`/LPAR-/RPAR` |
| `/NB` | `NB033` | 9678:`/NB+77B`; 9680:`/NB+77B`; 9687:`/NB` |
| `/NL` | `NL035` | 9682:`/NL+77B`; 9684:`/NL` |
| `/PLUS` | `PLU043` | 8974:`-/PLUS`; 8978:`-/PLUS`; 8990:`-/PLUS`; 9057:`-/PLUS`; 9059:`/PLUS-/COM` |
| `/RPAR` | `RPA042` | 9066:`/LPAR-/RPAR`; 9068:`/RPAR-/TWOP` |
| `/TWOP` | `TWO045` | 9068:`/RPAR-/TWOP` |
| `ALF1` | `ALF003` | 9327:`ALF1`; 9366:`ALF1`; 9440:`ALF1` |
| `ALF2` | `ALF004` | 9329:`ALF2`; 9368:`ALF2`; 9427:`ALF2`; 9431:`ALF2`; 9453:`ALF2`; 9550:`ALF2`; 9564:`ALF2` |
| `ALFA` | `ALF006` | 9298:`ALFA`; 9304:`ALFA`; 9307:`ALFA`; 9655:`ALFA` |
| `AP` | `AP141` | 9433:`AP`; 9463:`AP`; 9547:`AP` |
| `B1` | `B1125` | 9163:`B1`; 9226:`B1`; 9243:`B1`; 9319:`B1`; 9609:`B1`; 9663:`B1` |
| `B16` | `B16118` | 9614:`B16` |
| `B18` | `B18117` | 9615:`B18` |
| `B2` | `B2124` | 9384:`B2` |
| `B26` | `B26116` | 9599:`B26` |
| `B40` | `B40115` | 9414:`B40` |
| `B45` | `B45157` | 9124:`B45`; 9175:`B45`; 9270:`B45` |
| `B47` | `B47114` | 9004:`B47`; 9127:`B47`; 9193:`B47`; 9216:`B47` |
| `B48` | `B48113` | 9096:`B48`; 9257:`B48*L`; 9468:`B48`; 9521:`B48` |
| `B48*L` | `B48156` | 9257:`B48*L` |
| `BLEXPRIN` | `BLE025` | 9182:`BLEXPRIN` |
| `BUFP` | `BUF030` | 8944:`BUFP+LCAT`; 8945:`(BUFP)16`; 9229:`BUFP-2`; 9232:`BUFP+LCAT-1`; 9278:`BUFP`; 9320:`BUFP`; 9405:`BUFP+1777B`; 9438:`BUFP+2`; 9446:`2-BUFP`; 9598:`BUFP+1777B` |
| `C10` | `C10123` | 9430:`C10`; 9549:`C10` |
| `C1777` | `C17121` | 9568:`C1777`; 9637:`C1777` |
| `C37` | `C37122` | 9591:`C37` |
| `C3740` | `C37120` | 9618:`C3740` |
| `C77777` | `C77119` | 9356:`C77777`; 9456:`C77777`; 9551:`C77777` |
| `CALFA` | `CAL131` | 9299:`CALFA`; 9654:`CALFA` |
| `CGT` | `CGT130` | 9631:`CGT` |
| `CH BR` | `CHB068` | 9261:`CH BR`; 9277:`CH BR` |
| `CH V` | `CHV067` | 9239:`CH V`; 9266:`CH V`; 9271:`CH V` |
| `CLDRM` | `CLD133` | 9397:`CLDRM`; 9417:`CLDRM` |
| `COP FR` | `COP090` | 9575:`COP FR`; 9582:`COP FR` |
| `CRCAT` | `CRC132` | 9301:`CRCAT`; 9656:`CRCAT` |
| `CTN` | `CTN134` | 9008:`CTN`; 9091:`CTN`; 9391:`CTN`; 9658:`CTN` |
| `DIF` | `DIF071` | 9336:`-DIF`; 9339:`DIF` |
| `DUPDEF` | `DUP151` | 9218:`DUPDEF` |
| `ECAT` | `ECA032` | 9250:`4-ECAT`; 9253:`ECAT-2`; 9286:`ECAT`; 9288:`ECAT+1`; 9290:`ECAT+2`; 9292:`ECAT+3`; 9294:`ECAT+4+10B`; 9317:`ECAT+15B`; 9648:`ECAT+15B` |
| `ELOADER` | `ELO144` | 9335:`ELOADER-LOADER`; 9338:`ELOADER` |
| `EMPCAT` | `EMP149` | 9168:`EMPCAT`; 9279:`EMPCAT` |
| `END BR` | `END069` | 9249:`END BR` |
| `END CT` | `END078` | 9418:`END CT` |
| `END FR` | `END091` | 9578:`END FR` |
| `EQU` | `EQU084` | 9510:`EQU` |
| `EQU0` | `EQU083` | 9494:`EQU0` |
| `ERCA` | `ERC146` | 9155:`ERCA` |
| `ERPAR` | `ERP147` | 9170:`ERPAR` |
| `ERROFLG*` | `ERR018` | 9181:`ERROFLG*` |
| `ERTA` | `ERT152` | 9178:`ERTA` |
| `ETAL` | `ETA140` | 9490:`ETAL`; 9493:`ETAL`; 9508:`ETAL`; 9517:`ETAL`; 9519:`ETAL`; 9525:`ETAL` |
| `EWRI` | `EWR087` | 9530:`EWRI` |
| `FIN` | `FIN062` | 9028:`FIN`; 9353:`FIN LOAD` |
| `FIN LOAD` | `FIN097` | 9353:`FIN LOAD` |
| `FIN1` | `FIN063` | 9141:`FIN1`; 9167:`FIN1`; 9173:`FIN1`; 9187:`FIN1` |
| `FINI` | `FIN088` | 9592:`FINI` |
| `FINT` | `FIN093` | 9546:`FINT`; 9594:`FINT` |
| `FIR*LEV` | `FIR080` | 9443:`FIR*LEV` |
| `FLO 1` | `FLO098` | 9638:`FLO 1` |
| `FMIX` | `FMI135` | 8976:`FMIX`; 9466:`FMIX` |
| `FRAG TPП` | `FRA126` | 9562:`FRAG TPП` |
| `FRES` | `FRE136` | 8994:`FRES`; 9394:`FRES` |
| `HE MAЛ` | `HEM099` | 9646:`HE MAЛ` |
| `ICCO` | `ICC104` | 9476:`ICCO`; 9540:`ICCO`; 9634:`ICCO`; 9642:`ICCO` |
| `ICCT` | `ICC105` | 9396:`ICCT`; 9424:`ICCT` |
| `ICLL` | `ICL106` | 9553:`ICLL`; 9585:`ICLL` |
| `IPRI` | `IPR103` | 9649:`IPRI`; 9653:`IPRI` |
| `IRD` | `IRD143` | 9413:`IRD`; 9664:`IRD`; 9666:`IRD`; 9667:`IRD` |
| `IRLL` | `IRL107` | 9559:`IRLL` |
| `IT0` | `IT0109` | 8970:`IT0`; 9310:`IT0` |
| `ITC` | `ITC108` | 9311:`ITC`; 9312:`ITC`; 9610:`ITL-ITC`; 9612:`ITC`; 9651:`ITC` |
| `ITL` | `ITL137` | 9316:`ITL`; 9605:`ITL`; 9608:`ITL`; 9610:`ITL-ITC`; 9613:`ITL`; 9617:`ITL`; 9620:`ITL`; 9622:`ITL`; 9644:`ITL` |
| `IWCT` | `IWC138` | 9415:`IWCT`; 9422:`IWCT` |
| `IWSET` | `IWS096` | 9315:`IWSET`; 9321:`IWSET` |
| `LCAT` | `LCA031` | 8944:`BUFP+LCAT`; 9231:`1-LCAT`; 9232:`BUFP+LCAT-1` |
| `LDLP` | `LDL034` | 8948:`(LDLP)16`; 9580:`LDLP+1777B` |
| `LDRM` | `LDR010` | 9416:`LDRM`; 9421:`LDRM` |
| `LEX` | `LEX005` | 8942:`LEX` |
| `LIM NZ` | `LIM110` | 8984:`LIM NZ`; 9313:`LIM NZ`; 9318:`LIM NZ`; 9606:`LIM NZ`; 9643:`LIM NZ` |
| `LOAD` | `LOA074` | 8981:`LOAD`; 9353:`FIN LOAD`; 9357:`LOAD` |
| `LOAD1` | `LOA079` | 9385:`LOAD1`; 9395:`LOAD1` |
| `LOADER` | `LOA073` | 9314:`LOADER`; 9335:`ELOADER-LOADER`; 9372:`LOADER`; 9542:`LOADER` |
| `LOADLIS*` | `LOA017` | 9302:`LOADLIS*` |
| `LONCAT` | `LON148` | 9142:`LONCAT`; 9251:`LONCAT` |
| `LTAPES` | `LTA012` | 9007:`LTAPES`; 9085:`LTAPES`; 9092:`LTAPES`; 9392:`LTAPES`; 9659:`LTAPES` |
| `LTREE` | `LTR027` | 8939:`LTREE`; 9140:`2-LTREE`; 9144:`LTREE` |
| `LWRI` | `LWR086` | 9526:`LWRI`; 9534:`LWRI` |
| `MIST` | `MIS060` | 9051:`MIST`; 9061:`MIST`; 9069:`MIST`; 9074:`MIST`; 9078:`MIST`; 9099:`MIST`; 9104:`MIST`; 9105:`MIST`; 9112:`MIST`; 9116:`MIST`; 9122:`MIST` |
| `MIX` | `MIX089` | 9479:`MIX` |
| `MON*` | `MON155` | 9238:`MON*` |
| `MONITOR*` | `MON013` | 9660:`MONITOR*+1` |
| `MONREAD*` | `MON022` | 9024:`MONREAD*` |
| `NAME` | `NAM139` | 9053:`NAME`; 9081:`NAME`; 9134:`NAME`; 9352:`NAME`; 9437:`NAME` |
| `NEXT` | `NEX057` | 9047:`NEXT`; 9119:`NEXT`; 9156:`NEXT` |
| `NONTEX` | `NON145` | 9015:`NONTEX` |
| `PAP` | `PAP142` | 9360:`PAP`; 9371:`PAP`; 9442:`PAP`; 9458:`PAP` |
| `PAR1` | `PAR050` | 9048:`PAR1`; 9049:`PAR1`; 9050:`PAR1` |
| `PARAM` | `PAR049` | 9033:`PARAM`; 9130:`PARAM` |
| `PARAMT*` | `PAR029` | 8967:`PARAMT*`; 8972:`PARAMT*`; 8986:`PARAMT*`; 8997:`PARAMT*`; 9031:`PARAMT*`; 9045:`PARAMT*` |
| `PL*` | `PL159` | 9106:`PL*`; 9136:`PL*` |
| `PLUS` | `PLU158` | 8974:`-/PLUS`; 8978:`-/PLUS`; 8990:`-/PLUS`; 9057:`-/PLUS`; 9058:`*PLUS`; 9059:`/PLUS-/COM`; 9097:`PLUS`; 9098:`PLUS`; 9137:`PLUS`; 9147:`PLUS`; 9154:`PLUS` |
| `PRESS` | `PRE081` | 9536:`PRESS` |
| `PRI` | `PRI048` | 9029:`PRI` |
| `PRIER` | `PRI061` | 9017:`PRIER`; 9143:`PRIER`; 9169:`PRIER`; 9171:`PRIER`; 9176:`PRIER`; 9180:`PRIER`; 9209:`PRIER`; 9219:`PRIER`; 9252:`PRIER`; 9280:`PRIER` |
| `PRINT8` | `PRI023` | 9041:`PRINT8`; 9164:`PRINT8` |
| `R CARD` | `RCA046` | 9093:`R CARD`; 9129:`R CARD` |
| `RBEGP` | `RBE102` | 9403:`RBEGP`; 9560:`RBEGP` |
| `RCAT` | `RCA008` | 9402:`RCAT`; 9657:`RCAT` |
| `RCTE` | `RCT076` | 9406:`RCTE` |
| `RCTW` | `RCT075` | 9408:`RCTW`; 9409:`RCTW` |
| `RES CT` | `RES077` | 9398:`RES CT` |
| `RETN` | `RET009` | 9382:`RETN` |
| `RLOAD` | `RLO011` | 9436:`RLOAD` |
| `RM*` | `RM019` | 9326:`RM*`; 9328:`RM*+1`; 9331:`RM*+2` |
| `RNEXP` | `RNE101` | 9410:`RNEXP`; 9583:`RNEXP` |
| `S/NAM` | `SNA051` | 9082:`S/NAM` |
| `SAV*47` | `SAV024` | 9300:`SAV*47` |
| `SE/EQ` | `SEE082` | 9488:`SE/EQ`; 9492:`SE/EQ`; 9497:`SE/EQ`; 9500:`SE/EQ` |
| `SECENTRY` | `SEC002` | 9451:`SECENTRY` |
| `SOONDF` | `SOO150` | 9208:`SOONDF` |
| `STOP*` | `STO021` | 9016:`STOP*`; 9179:`STOP*` |
| `OVL_BUFFER_1070` | `BF1070` | 9303:`TL 1` |
| `OVL_MEM_READ_6072` | `RD6072` | 9341:`TL 6` |
| `TMAЛ` | `TMA127` | 9645:`TMAЛ`; 9652:`TДЛИ-TMAЛ` |
| `TOV` | `TOV153` | 9285:`TOV`; 9287:`TOV+1` |
| `TREE` | `TRE028` | 9080:`TREE`; 9087:`TREE+1`; 9089:`TREE+1`; 9090:`TREE+1`; 9125:`TREE-1`; 9126:`TREE-1`; 9135:`TREE`; 9139:`TREE+1`; 9146:`TREE`; 9174:`TREE+1`; 9186:`TREE`; 9196:`TREE` … (+1) |
| `TДЛИ` | `T128` | 9632:`TДЛИ+3`; 9652:`TДЛИ-TMAЛ` |
| `UPM` | `UPM129` | 9630:`UPM` |
| `VEC` | `VEC065` | 9202:`VEC`; 9214:`VEC`; 9223:`VEC` |
| `VECT` | `VEC064` | 9194:`VECT`; 9200:`VECT` |
| `VECT1` | `VEC066` | 9191:`VECT1` |
| `VOID FR` | `VOI092` | 9552:`VOID FR` |
| `WLEX` | `WLE007` | 9434:`WLEX` |
| `WORD` | `WOR094` | 9524:`WORD`; 9527:`WORD`; 9533:`WORD`; 9563:`WORD`; 9574:`WORD`; 9581:`WORD`; 9588:`WORD`; 9640:`WORD` |
| `WRE` | `WRE059` | 9133:`WRE` |
| `WRI` | `WRI058` | 9108:`WRI`; 9109:`WRI`; 9113:`WRI`; 9117:`WRI`; 9123:`WRI` |
| `WRI1` | `WRI085` | 9485:`WRI1`; 9507:`WRI1` |
| `XT` | `XT111` | 9464:`XT`; 9600:`XT`; 9601:`XT`; 9628:`XT` |
| `Z12/6` | `Z12112` | 9621:`Z12/6` |

## 3. Вызовы и переходы (VJM / CALL / UJ)

| Строка | Команда | Операнд |
|---|---|---|
| S2:8967 | `CALL` | `PARAMT*` |
| S2:8972 | `CALL` | `PARAMT*` |
| S2:8986 | `CALL` | `PARAMT*` |
| S2:8997 | `CALL` | `PARAMT*` |
| S2:9024 | `CALL` | `MONREAD*` |
| S2:9031 | `CALL` | `PARAMT*` |
| S2:9041 | `UJ` | `PRINT8` |
| S2:9045 | `CALL` | `PARAMT*` |
| S2:9076 | `CALL` | `NEWLIBR/` |
| S2:9093 | `UJ` | `R CARD` |
| S2:9109 | `VJM` | `WRI` |
| S2:9113 | `UJ` | `WRI` |
| S2:9117 | `VJM` | `WRI` |
| S2:9119 | `UJ` | `NEXT` |
| S2:9123 | `VJM` | `WRI` |
| S2:9130 | `UJ` | `PARAM` |
| S2:9150 | `UJ` | `(через индексный регистр)` |
| S2:9164 | `UJ` | `PRINT8` |
| S2:9223 | `UJ` | `VEC` |
| S2:9315 | `VJM` | `IWSET` |
| S2:9321 | `VJM` | `IWSET` |
| S2:9342 | `UJ` | `(через индексный регистр)` |
| S2:9372 | `UJ` | `LOADER` |
| S2:9403 | `VJM` | `RBEGP` |
| S2:9418 | `UJ` | `END CT` |
| S2:9438 | `VJM` | `BUFP+2` |
| S2:9524 | `VJM` | `WORD` |
| S2:9527 | `VJM` | `WORD` |
| S2:9533 | `VJM` | `WORD` |
| S2:9536 | `UJ` | `PRESS` |
| S2:9542 | `UJ` | `LOADER` |
| S2:9560 | `VJM` | `RBEGP` |
| S2:9563 | `VJM` | `WORD` |
| S2:9574 | `VJM` | `WORD` |
| S2:9581 | `VJM` | `WORD` |
| S2:9583 | `UJ` | `RNEXP` |
| S2:9588 | `VJM` | `WORD` |
| S2:9623 | `UJ` | `(через индексный регистр)` |
| S2:9640 | `UJ` | `WORD` |
| S2:9660 | `UJ` | `MONITOR*+1` |
| S2:9670 | `UJ` | `(через индексный регистр)` |

## 4. Внешние символы (не определены в модуле)

- `CARD`
- `CT`
- `END`
- `NEWLIBR/`
- `R`

## 5. Литералы → EQU

| EQU | Значение | Строка |
|---|---|---|
| `DIF071` | `ELO144-LOA073` | S2:9335 |
| `TWO045` | `72B` | S2:8960 |
| `COM044` | `54B` | S2:8959 |
| `PLU043` | `53B` | S2:8958 |
| `RPA042` | `51B` | S2:8957 |
| `LPA041` | `50B` | S2:8956 |
| `LDL034` | `2000B` | S2:8947 |
| `ECA032` | `BUF030+LCA031` | S2:8944 |
| `LCA031` | `1762B` | S2:8943 |
| `LTR027` | `2020` | S2:8938 |
| `LTA012` | `73B` | S2:8919 |
| `RLO011` | `61B` | S2:8918 |
| `LDR010` | `54B` | S2:8917 |
| `RET009` | `51B` | S2:8916 |
| `RCA008` | `47B` | S2:8915 |
| `WLE007` | `46B` | S2:8914 |
| `ALF006` | `44B` | S2:8913 |
| `LEX005` | `43B` | S2:8912 |
| `ALF004` | `17B` | S2:8911 |
| `ALF003` | `16B` | S2:8910 |
| `SEC002` | `15B` | S2:8909 |
| `EDC016` | `60` | S2:8848 |
| `EDC017` | `1` | S2:8934 |
| `EDC018` | `12` | S2:8937 |
| `EDC019` | `16` | S2:8945 |
| `EDC020` | `4` | S2:8971 |
| `EDC021` | `8` | S2:8983 |
| `EDC022` | `5` | S2:8985 |
| `ETX022` | `=777` | S2:8988 |
| `EDC023` | `64` | S2:8989 |
| `EDC024` | `10` | S2:8989 |
| `EDC025` | `40` | S2:9013 |
| `EDC026` | `14` | S2:9019 |
| `EDC027` | `13` | S2:9021 |
| `EDC028` | `9` | S2:9030 |
| `EDC029` | `6` | S2:9032 |
| `EDC030` | `3` | S2:9044 |
| `EDC031` | `2` | S2:9079 |
| `EDC032` | `15` | S2:9086 |
| `ETX032` | `=7 7777 7770 0000` | S2:9088 |
| `EOC032` | `10B` | S2:9234 |
| `EOC033` | `2000B` | S2:9296 |
| `EOC034` | `15B` | S2:9317 |
| `EOC035` | `12B` | S2:9334 |
| `EOC036` | `73413B` | S2:9350 |
| `EDC036` | `7` | S2:9369 |
| `EDC037` | `30` | S2:9370 |
| `EDC038` | `24` | S2:9389 |
| `EOC038` | `1777B` | S2:9405 |
| `EOC039` | `777B` | S2:9669 |
| `EOC040` | `77B` | S2:9678 |
| `ETX040` | `60 0000` | S2:9689 |
| `ETX041` | `1000` | S2:9690 |
| `ETX042` | `0000 4` | S2:9691 |
| `ETX043` | `7777 7777 7777 0037` | S2:9693 |
| `ETX044` | `4` | S2:9694 |
| `ETX045` | `2` | S2:9695 |
| `ETX046` | `001` | S2:9696 |
| `ETX047` | `0000 0002` | S2:9697 |
| `ETX048` | `40 0000` | S2:9698 |
| `ETX049` | `10 0000` | S2:9699 |
| `ETX050` | `77777` | S2:9700 |
| `ETX051` | `3740` | S2:9701 |
| `ETX052` | `1777` | S2:9702 |
| `ETX053` | `37` | S2:9703 |
| `ETX054` | `10` | S2:9704 |
| `ETX055` | `1` | S2:9706 |
| `ETX056` | `8HFRAG TPП` | S2:9707 |
| `ETX057` | `18H***  MAЛO MЛ  ***'231'` | S2:9708 |
| `ETX058` | `25HДЛИHA БИБЛИOTEKИ  077 37'231'` | S2:9709 |
| `ETX059` | `6H'367'77037` | S2:9710 |
| `ETX060` | `6H000 00` | S2:9711 |
| `ETX061` | `24HHETEKCTOBAЯ KAPTA` | S2:9728 |
| `ETX062` | `24HOШ` | S2:9729 |
| `ETX063` | `24HHET ЗAKPЫBAЮЩEЙ CKOБKИ` | S2:9730 |
| `ETX064` | `24HCЛИШKOM MHOГO PAЗДEЛOB` | S2:9731 |
| `ETX065` | `24HПYCTAЯ БИБЛ` | S2:9732 |
| `ETX066` | `24HPAHOBATO OПИCAH PAЗДEЛ` | S2:9733 |
| `ETX067` | `24HПOBTOP` | S2:9734 |
| `ETX068` | `24HБЫЛИ OШИБKИ B ЗAДAHИИ` | S2:9735 |
| `ETX069` | `12HOVERLAY OT` | S2:9736 |
| `ETX070` | `6H*END R` | S2:9737 |
| `ETX071` | `8HMONITOR*` | S2:9738 |
| `ETX072` | `4007 7777 7770 0000` | S2:9739 |
| `ETX073` | `04` | S2:9740 |

## 4. Семантическое именование (этап 12)

- Авто-меток `TL#####` переименовано: **2** (`TL1070` → `BF1070`, `TL6072` → `RD6072`).
- Полное имя вынесено в `POLN:`; таблица — в `logs/labels_semantics_lib21_core.txt`.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э72 | ICC104 | не найдено в rukava.be | — | 4 | `src/lib21/OVERLOAD.mad:708`, `src/lib21/OVERLOAD.mad:772`, `src/lib21/OVERLOAD.mad:866`, `src/lib21/OVERLOAD.mad:874` |
| Э72 | ICC105 | не найдено в rukava.be | — | 2 | `src/lib21/OVERLOAD.mad:628`, `src/lib21/OVERLOAD.mad:656` |
| Э72 | ICL106 | не найдено в rukava.be | — | 2 | `src/lib21/OVERLOAD.mad:785`, `src/lib21/OVERLOAD.mad:817` |

## Текстовые константы

Проверено 16 констант модуля `src/lib21/OVERLOAD.mad`. Методика: `t6()` из `tools/extract_words.py` (6 бит/символ, 8 символов/слово), GOST-10859 (`gost10859.h`), ISO/ASCII (6 байт/слово). Для ASCII-Hollerith-литералов первичен TEXT-decode; для кириллических GOST-литералов — GOST-decode. Полная таблица с вердиктами — `logs/text_constants_audit.txt`.

| Константа | Декодирование (GOST / TEXT / ISO) | Источник | Вердикт |
|-----------|----------------------------------|----------|---------|
| `8HFRAG TPП` | GOST `18Б2 ТРП` / TEXT `!(A"/RPO` / ISO `··B?,/` | `src/lib21/OVERLOAD.mad:79` | добавлено |
| `18H***  MAЛO MЛ  ***'231'` | GOST `***  МАЛ` / TEXT `999//L@K` / ISO `e·O>·+` | `src/lib21/OVERLOAD.mad:80` | добавлено |
| `25HДЛИHA БИБЛИOTEKИ  077 37'231'` | GOST `ДЛИНА БИ` / TEXT `DKHM@/AH` / ISO `··-··h` | `src/lib21/OVERLOAD.mad:81` | добавлено |
| `6H'367'77037` | GOST `7);[7[[е` / TEXT `'367'770` / ISO `·5··u·` | `src/lib21/OVERLOAD.mad:82` | добавлено |
| `6H000 00` | GOST `еее0ее00` / TEXT `000 00  ` / ISO `A··A··` | `src/lib21/OVERLOAD.mad:83` | добавлено |
| `24HHETEKCTOBAЯ KAPTA` | GOST `НЕТЕКСТО` / TEXT `MEREJQRN` / ISO `·\····` | `src/lib21/OVERLOAD.mad:84` | добавлено |
| `24HOШ` | GOST `ОШ      ` / TEXT `NX//////` / ISO `···<··` | `src/lib21/OVERLOAD.mad:85` | добавлено |
| `24HHET ЗAKPЫBAЮЩEЙ CKOБKИ` | GOST `НЕТ ЗАКР` / TEXT `MER/G@JP` / ISO `·\····` | `src/lib21/OVERLOAD.mad:86` | добавлено |
| `24HCЛИШKOM MHOГO PAЗДEЛOB` | GOST `СЛИШКОМ ` / TEXT `QKHXJNL/` / ISO `··8···` | `src/lib21/OVERLOAD.mad:87` | добавлено |
| `24HПYCTAЯ БИБЛ` | GOST `ПУСТАЯ Б` / TEXT `OSQR@_/A` / ISO `·<r···` | `src/lib21/OVERLOAD.mad:88` | добавлено |
| `24HPAHOBATO OПИCAH PAЗДEЛ` | GOST `РАНОВАТО` / TEXT `P@MNB@RN` / ISO `··n···` | `src/lib21/OVERLOAD.mad:89` | добавлено |
| `24HПOBTOP` | GOST `ПОВТОР  ` / TEXT `ONBRNP//` / ISO `······` | `src/lib21/OVERLOAD.mad:90` | добавлено |
| `24HБЫЛИ OШИБKИ B ЗAДAHИИ` | GOST `БЫЛИ ОШИ` / TEXT `A[KH/NXH` / ISO `···>·(` | `src/lib21/OVERLOAD.mad:91` | добавлено |
| `12HOVERLAY OT` | GOST `ПЦЕТМБЩ0` / TEXT `OVERLAY ` / ISO `·ir··@` | `src/lib21/OVERLOAD.mad:92` | добавлено |
| `6H*END R` | GOST `+ЕОД0Т00` / TEXT `*END R  ` / ISO `*[·· ·` | `src/lib21/OVERLOAD.mad:93` | добавлено |
| `8HMONITOR*` | GOST `НПОЙФПТ+` / TEXT `MONITOR*` / ISO `······` | `src/lib21/OVERLOAD.mad:94` | добавлено |

