      PROGRAM PREP7
      CHARACTER*10 S
      CHARACTER*6 T
      S='ABCDEF'
      T = S(2:4) // 'XY'
      IF (S .EQ. T) GO TO 99
      PRINT *, S
   99 CONTINUE
      STOP
      END
