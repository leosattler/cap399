#include <stdio.h>
#include <sys/time.h>

#define LEN 30000
#define LEN2 500

int dummy(float a[LEN], float b[LEN], float c[LEN], float d[LEN], float e[LEN], float aa[LEN2][LEN2], float bb[LEN2][LEN2], float cc[LEN2][LEN2], float s){
	// --  called in each loop to make all computations appear required
	return 0;
}


/* The gettimeofday function may have low resolution, so do not use this
   for high-resolution (microsecond) timing.

   Note that gettimeofday is not guaranteed to be monotone increasing.
   However,for short timing tests, it is likely to be to be accurate.
   This function is used because it is the most portable timer without
   using either OpenMP or MPI.
*/
double mysecond(void)
{
    struct timeval tVal;
    gettimeofday(&tVal,NULL);
    return (double)tVal.tv_sec + 1.0e-6 * (double)tVal.tv_usec;
}
/* By adding this name, most Fortran program will be able to use
   mysecond() as a double precision function */
double mysecond_(void)
{
    return mysecond();
}
