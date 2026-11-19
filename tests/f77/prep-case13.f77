      PROGRAM F11
      CALL CNT(A)
      CALL CNT(B)
      PRINT 10,A,B
   10 FORMAT(1X,2I4)
      END
      SUBROUTINE CNT(K)
      DATA N/10/
      SAVE N
      N=N+1
      K=N
      END
