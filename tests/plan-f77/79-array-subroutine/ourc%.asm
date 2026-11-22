  OURC*   :  , NAME,
c
c  Minimal array + internal subroutine compiler body (monitor text).
c  A(1..3) live at body[0o41..0o43] -> RAM 0o2020..0o2022.
c  Internal routine OURSUB* owns the *64 print word.
c
  *1      :  ,BLOCК,M1,M2,M3,M4,M5,M6,M7,M8,M9
             , CONT,M10,M11,M12,M13,M14,M15
c--- entry: ACC = G1 + A(index), then store -------------------------------
  ENTRY   :  , XTA ,GOST
            , ARX ,AIDX
            , ATX ,GOST
c--- internal subroutine call --------------------------------------------
        15, VJM ,OURSUB
  BACK    :  , UJ  ,1
c--- array element (index selected at source) -----------------------------
  AIDX    :  , OCT ,0000000000000003
  GOST    :  , OCT ,0000041700207000
c--- internal subroutine: print, then return ------------------------------
  OURSUB  :  , *64 ,SDESC
        15, UJ  ,
  SDESC   :  , OCT ,2300000023000000
            , END ,
