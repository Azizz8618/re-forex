      PROGRAM J7
C@ READ(*,*,END=99) X -> READ 9500,X  (END= label removed)
      READ 9500,X
C@ R11-END -> IF (X .EQ. -999999.) GO TO 99
      IF (X .EQ. -999999.) GO TO 99
      PRINT 20,X
      GO TO 100
   99 PRINT 21
  100 CONTINUE
   20 FORMAT(1X,F8.2)
   21 FORMAT(1X,'EOF')
C@ (end of program) -> 9500 FORMAT(F12.4)
 9500 FORMAT(F12.4)
      END
