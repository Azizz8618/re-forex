      PROGRAM F25
      INTEGER A,B,C,D,K
      OPEN(23,FILE='RAW',STATUS='NEW',IOSTAT=K)
      A=111
      B=222
      WRITE(23) A,B
      READ(23,IOSTAT=K) C,D
      PRINT 10,C,D,K
   10 FORMAT(1X,'C ',I4,' D ',I4,' K ',I3)
      CLOSE(23)
      STOP
      END
