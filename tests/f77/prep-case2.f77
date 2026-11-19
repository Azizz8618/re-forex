      PROGRAM PREPCASE2
      INTEGER N, M
      CHARACTER*4 S
      S='ABCD'
      N=1
      DO WHILE (N .LT. 3)
         READ(*,*,END=99) M
         PRINT *, N, M
         N=N+1
      END DO
      PRINT *, S
   99 CONTINUE
      STOP
      END
