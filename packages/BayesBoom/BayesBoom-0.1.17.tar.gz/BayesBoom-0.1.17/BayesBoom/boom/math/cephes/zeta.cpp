/*
  Copyright (C) 2005-2013 Steven L. Scott

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
*/

// This file was modified from the public domain cephes math library
// taken from netlib.

#include "cephes_impl.hpp"
namespace BOOM {
  namespace Cephes {

  /*                                                    zeta.c
   *
   *    Riemann zeta function of two arguments
   *
   *
   *
   * SYNOPSIS:
   *
   * double x, q, y, zeta();
   *
   * y = zeta( x, q );
   *
   *
   *
   * DESCRIPTION:
   *
   *
   *
   *                 inf.
   *                  -        -x
   *   zeta(x,q)  =   >   (k+q)
   *                  -
   *                 k=0
   *
   * where x > 1 and q is not a negative integer or zero.
   * The Euler-Maclaurin summation formula is used to obtain
   * the expansion
   *
   *                n
   *                -       -x
   * zeta(x,q)  =   >  (k+q)
   *                -
   *               k=1
   *
   *           1-x                 inf.  B   x(x+1)...(x+2j)
   *      (n+q)           1         -     2j
   *  +  ---------  -  -------  +   >    --------------------
   *        x-1              x      -                   x+2j+1
   *                   2(n+q)      j=1       (2j)! (n+q)
   *
   * where the B2j are Bernoulli numbers.  Note that (see zetac.c)
   * zeta(x,1) = zetac(x) + 1.
   *
   *
   *
   * ACCURACY:
   *
   *
   *
   * REFERENCE:
   *
   * Gradshteyn, I. S., and I. M. Ryzhik, Tables of Integrals,
   * Series, and Products, p. 1073; Academic Press, 1980.
   *
   */

  /*
    Cephes Math Library Release 2.8:  June, 2000
    Copyright 1984, 1987, 2000 by Stephen L. Moshier
  */

  /* Expansion coefficients
   * for Euler-Maclaurin summation formula
   * (2k)! / B2k
   * where B2k are Bernoulli numbers
   */
  static double A[] = {
    12.0,
    -720.0,
    30240.0,
    -1209600.0,
    47900160.0,
    -1.8924375803183791606e9, /*1.307674368e12/691*/
    7.47242496e10,
    -2.950130727918164224e12, /*1.067062284288e16/3617*/
    1.1646782814350067249e14, /*5.109094217170944e18/43867*/
    -4.5979787224074726105e15, /*8.028576626982912e20/174611*/
    1.8152105401943546773e17, /*1.5511210043330985984e23/854513*/
    -7.1661652561756670113e18 /*1.6938241367317436694528e27/236364091*/
  };
  /* 30 Nov 86 -- error in third coefficient fixed */

    double zeta(double x, double q) {
      int i;
      double a, b, k, s, t, w;

      if( x == 1.0 )
        goto retinf;

      if( x < 1.0 )
      {
     domerr:
        report_error("Domain error in BOOM::Cephes::zeta().");
        return(0.0);
      }

      if( q <= 0.0 )
      {
        if(q == floor(q))
        {
          report_error("Singularity in BOOM::Cephes::zeta().");
       retinf:
          return( MAXNUM );
        }
        if( x != floor(x) )
          goto domerr; /* because q^-x not defined */
      }

      /* Euler-Maclaurin summation formula */
      /*
        if( x < 25.0 )
      */
      {
        /* Permit negative q but continue sum until n+q > +9 .
         * This case should be handled by a reflection formula.
         * If q<0 and x is an integer, there is a relation to
         * the polygamma function.
         */
        s = pow( q, -x );
        a = q;
        i = 0;
        b = 0.0;
        while( (i < 9) || (a <= 9.0) )
        {
          i += 1;
          a += 1.0;
          b = pow( a, -x );
          s += b;
          if( fabs(b/s) < MACHEP )
            goto done;
        }

        w = a;
        s += b*w/(x-1.0);
        s -= 0.5 * b;
        a = 1.0;
        k = 0.0;
        for( i=0; i<12; i++ )
        {
          a *= x + k;
          b /= w;
          t = a*b/A[i];
          s = s + t;
          t = fabs(t/s);
          if( t < MACHEP )
            goto done;
          k += 1.0;
          a *= x + k;
          b /= w;
          k += 1.0;
        }
     done:
        return(s);
      }

    }
  }  // namespace Cephes
}  // namespace BOOM
