C---- K03: COMPLEX ARITHMETIC AND CABS.
      PROGRAM K03
C@ implicit COMPLEX WC (rule 22 complex-literal)
      COMPLEX WC
      WC=(3.0,4.0)
C@ R=CABS(WC) -> R = SQRT(REAL(WC)**2 + AIMAG(WC)**2)
      R = SQRT(REAL(WC)**2 + AIMAG(WC)**2)
      PRINT 10,R
   10 FORMAT(1X,F10.4)
      STOP
      END
