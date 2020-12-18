CC = icc

flags = -std=c99 -O3 
vecflags = -qopt-report=2 -qopt-report-phase=vec
novecflags = -no-vec
libs = -lm
noopt = -O0

all : tscvec tscnovec

tscnovec: tscnovec.o dummy.o
	$(CC) $(noopt) dummy.o tscnovec.o -o tscnovec $(libs)

tscvec: tscvec.o dummy.o
	$(CC) $(noopt) dummy.o tscvec.o -o tscvec $(libs)

tscvec.o : tsc.c
	$(CC) $(flags) $(vecflags) -c -o tscvec.o tsc.c 

tscnovec.o : tsc.c
	$(CC) $(flags) $(novecflags) -c -o tscnovec.o tsc.c

dummy.o : dummy.c
	$(CC) -c dummy.c

clean :
	rm -f *.o tscnovec tscvec *.optrpt *.s
