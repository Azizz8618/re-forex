      PROGRAM F11
      CALL CNT(A)
      CALL CNT(B)
      PRINT 10,A,B
   10 FORMAT(1X,2I4)
      END
      SUBROUTINE CNT(K)
C@ DATA N/10/ -> (moved to BLOCK DATA CNTSV)
C@ SAVE N -> COMMON /CNTSV/N (BLOCK DATA init)
      COMMON /CNTSV/N
      N=N+1
      K=N
      END
C@ (R-F11) -> BLOCK DATA for SAVEd variables
      BLOCK DATA
      INTEGER N
      COMMON /CNTSV/N
      DATA N/10/
      END
