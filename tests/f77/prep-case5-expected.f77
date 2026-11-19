      PROGRAM PREP5
C@ IMPLICIT INTEGER (A-Z) -> (removed; explicit decls)
      INTEGER X
C@ INTEGER IA(10), IB(5) -> INTEGER IA(10)
      INTEGER IA(10)
C@ EQUIVALENCE (IA(2),IB(1)) -> (removed; rename map applied)
      X=3
C@ IB(1) = 7 -> IA(2) = 7
      IA(2) = 7
C@ PRINT *, IA(2), X -> PRINT 9000,IA(2),X
      PRINT 9000,IA(2),X
      STOP
C@ (end of program) -> 9000 FORMAT(1X,I10,I10)
 9000 FORMAT(1X,I10,I10)
      END
