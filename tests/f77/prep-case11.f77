      PROGRAM C6
      LOGICAL A,B,R
      A=.TRUE.
      B=.FALSE.
      R=A .EQV. B
      IR=0
      IF (R) IR=1
      PRINT 10,IR
   10 FORMAT(1X,I3)
      STOP
      END
