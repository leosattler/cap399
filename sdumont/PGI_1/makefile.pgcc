CC = pgcc

flags = -c99 -O3 
vecflags =  -Mvect=sse -Minfo
novecflags = -Mnovect
libs = -lm
noopt = -O0

all : tscvec tscnovec

tscnovec: tscnovec.o dummy.o
	$(CC) $(noopt) dummy.o tscnovec.o -o tscnovec $(libs)

tscvec: tscvec.o dummy.o
	$(CC) $(noopt) dummy.o tscvec.o -o tscvec $(libs)

tscvec.o : tsc.c
	$(CC) $(flags) $(vecflags) -c -o tscvec.o tsc.c  2> reportpgcc.lst

tscnovec.o : tsc.c
	$(CC) $(flags) $(novecflags) -c -o tscnovec.o tsc.c

dummy.o : dummy.c
	$(CC) -c dummy.c

clean :
	rm -f *.o tscnovec tscvec *.lst *.s
