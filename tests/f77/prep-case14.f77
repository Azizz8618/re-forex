      PROGRAM G8L
      CALL SUB(*10,*20)
   10 K=1
      GO TO 60
   20 K=2
   60 PRINT 70,K
   70 FORMAT(1X,I4)
      END
      SUBROUTINE SUB(RC)
      RETURN 1
      END
