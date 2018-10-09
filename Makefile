


ppc: ppc.o
	powerpc-e300c3-linux-gnu-ld -static -o ppc ppc.o

ppc.o: ppc.s
	powerpc-e300c3-linux-gnu-as -g -o ppc.o ppc.s


mips: mips.o
	mipsel-linux-gnu-ld -static -o mips mips.o

mips.o: mips.s
	mipsel-linux-gnu-as -o mips.o mips.s

