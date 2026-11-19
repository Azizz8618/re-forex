      PROGRAM F25
C@ F77A FILMAP: FM(1)=ISTAT FM(2)=OPENED FM(3)=EXIST
      INTEGER FM(320)
      COMMON /FILMAP/ FM
      DATA FM /320*0/
      INTEGER FMN23(2)
      DATA FMN23 /12HRAW         /
      INTEGER IB23(12)
      INTEGER A,B,C,D,K
C@ F77A OPEN(23,FILE='RAW',STATUS='NEW',IOSTAT=K) -> ZF bridge
      FM(4)=2
      FM(5)=0
      FM(6)=0
      FM(7)=0
      CALL ZFOPEN(FMN23,23,8,FM(1))
      K = FM(1)
      A=111
      B=222
C@ F77A WRITE(23) A,B -> ZF bridge
      IB23(1)=A
      IB23(2)=B
      CALL ZFWRIT(23,IB23,2,FM(1))
C@ F77A READ(23,IOSTAT=K) C,D -> ZF bridge
      CALL ZFREAD(23,IB23,2,FM(1))
      K = FM(1)
      C=IB23(1)
      D=IB23(2)
      PRINT 10,C,D,K
   10 FORMAT(1X,'C ',I4,' D ',I4,' K ',I3)
C@ F77A CLOSE(23) -> ZF bridge
      CALL ZFCLOSE(23,0,FM(1))
      STOP
      END
