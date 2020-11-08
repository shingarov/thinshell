


modtalk.elf: modtalk.o
	mipsel-linux-gnu-ld -static -T Link -o modtalk.elf modtalk.o

modtalk.o: modtalk.s
	mipsel-linux-gnu-as -g -o modtalk.o modtalk.s




G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py
DEBUG5="--debug-flags=GDBRecv,GDBSend,Fetch,Decode"

g5:
	$(G5DIR)/build/MIPS/gem5.debug $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1

# inside gdb:
# run --debug-flags=GDBRecv,GDBSend,Fetch,Decode /home/boris/work/gem5/configs/example/se.py -c ppc.elf --wait-gdb=1


clean:
	rm -f *.elf *.o
