      PROGRAM C6
      LOGICAL A,B,R
      A=.TRUE.
      B=.FALSE.
C@ R=A .EQV. B -> R=(A .AND. B) .OR. (.NOT.A .AND. .NOT.B)
      R=(A .AND. B) .OR. (.NOT.A .AND. .NOT.B)
      IR=0
      IF (R) IR=1
      PRINT 10,IR
   10 FORMAT(1X,I3)
      STOP
      END
