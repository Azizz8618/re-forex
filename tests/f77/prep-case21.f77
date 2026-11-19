      PROGRAM E9V
      S=-1
      T=0
      DO 20 I=1,0,S
   20 T=T+I
      S=1
      DO 30 I=1,0,S
   30 T=T+I
      PRINT 40,T
   40 FORMAT(1X,I4)
      END
