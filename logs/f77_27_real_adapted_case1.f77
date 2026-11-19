      PROGRAM PREPCASE
C@ IMPLICIT NONE -> (removed)
      INTEGER N
C@ SAVE N -> (removed)
      N=42
C@ PRINT *,N -> PRINT 9000,N
      PRINT 9000,N
      STOP
C@ (end of program) -> 9000 FORMAT(1X,I10)
 9000 FORMAT(1X,I10)
      END
