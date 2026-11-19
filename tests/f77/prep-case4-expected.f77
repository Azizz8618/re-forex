      PROGRAM PREP4
C@ ASSIGN 100 TO I -> I = 1
      I = 1
C@ GO TO I -> IF-chain over 100
      IF (I .EQ. 1) GO TO 100
  100 CONTINUE
C@ GO TO (110,120),I -> IF-chain over 110,120
      IF (I .EQ. 1) GO TO 110
      IF (I .EQ. 2) GO TO 120
  110 CONTINUE
C@ PRINT *, 1 -> PRINT 9000,1
      PRINT 9000,1
      STOP
  120 CONTINUE
C@ PRINT *, 2 -> PRINT 9001,2
      PRINT 9001,2
      STOP
C@ (end of program) -> 9000 FORMAT(1X,F12.4)
 9000 FORMAT(1X,F12.4)
C@ (end of program) -> 9001 FORMAT(1X,F12.4)
 9001 FORMAT(1X,F12.4)
      END
