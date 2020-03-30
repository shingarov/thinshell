


ppc.elf: ppc.o
	powerpc-linux-gnu-ld -static -o ppc.elf ppc.o

ppc.o: ppc.s
	powerpc-linux-gnu-as -g -o ppc.o ppc.s


mips.elf: mips.o
	mipsel-linux-gnu-ld -static -o mips.elf mips.o

mips.o: mips.s
	mipsel-linux-gnu-as -o mips.o mips.s


HelloNB.so: HelloNB.c
	i686-linux-gnu-gcc-9 -ggdb -shared  -o HelloNB.so HelloNB.c -lrt

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py
DEBUG5="--debug-flags=GDBRecv,GDBSend,Fetch,Decode"

gem5-ppc:
	$(G5DIR)/build/POWER/gem5.debug $(DEBUG5) $(G5SEPY) -c ppc.elf --wait-gdb=1

# inside gdb:
# run --debug-flags=GDBRecv,GDBSend,Fetch,Decode /home/boris/work/gem5/configs/example/se.py -c ppc.elf --wait-gdb=1
