      PROGRAM F26
C@ F77A FILMAP: FM(1)=ISTAT FM(2)=OPENED FM(3)=EXIST
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      INTEGER FMN24(2)
      DATA FMN24 /12HEOF         /
      INTEGER IB24(12)
      INTEGER A,K
C@ F77A OPEN(24,FILE='EOF',STATUS='NEW',IOSTAT=K) -> ZF bridge
      FM(4)=2
      FM(5)=0
      FM(6)=0
      FM(7)=0
      CALL ZFOPEN(FMN24,24,FM(1))
      K = FM(1)
C@ F77A WRITE(24) 7 -> ZF bridge
      IB24(1)=7
      CALL ZFWRIT(24,IB24,1,FM(1))
C@ F77A READ(24,IOSTAT=K) A -> ZF bridge
      CALL ZFREAD(24,IB24,1,FM(1))
      K = FM(1)
      A=IB24(1)
C@ F77A READ(24,END=80,IOSTAT=K) A -> ZF bridge
      CALL ZFREAD(24,IB24,1,FM(1))
      K = FM(1)
      IF (FM(1) .EQ. -1) GO TO 80
      A=IB24(1)
      PRINT 10
   10 FORMAT(1X,'NOEOF')
      GO TO 90
   80 PRINT 11,K
   11 FORMAT(1X,'EOF K ',I3)
C@ F77A CLOSE(24) -> ZF bridge
   90 CONTINUE
      CALL ZFCLOSE(24,0,FM(1))
      END
