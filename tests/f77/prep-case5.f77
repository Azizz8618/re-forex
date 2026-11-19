      PROGRAM PREP5
      IMPLICIT INTEGER (A-Z)
      INTEGER IA(10), IB(5)
      EQUIVALENCE (IA(2),IB(1))
      X=3
      IB(1) = 7
      PRINT *, IA(2), X
      STOP
      END
