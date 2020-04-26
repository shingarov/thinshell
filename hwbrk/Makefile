
##### HW breakpoint test #####

elves: hwbrk-ppc.elf hwbrk-i686.elf


### gem5 parameters

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py
DEBUG5="--debug-flags=GDBRecv,GDBSend,Fetch,Decode"


### running gem5

g5-ppc:
	$(G5DIR)/build/POWER/gem5.debug $(DEBUG5) $(G5SEPY) -c hwbrk-ppc.elf --wait-gdb=1

g5-i686:
	$(G5DIR)/build/X86/gem5.debug $(DEBUG5) $(G5SEPY) -c hwbrk-i686.elf --wait-gdb=1

d5-i686:
	echo run $(DEBUG5) $(G5SEPY) -c hwbrk-i686.elf --wait-gdb=1 | xclip -i
	/usr/bin/gdb $(G5DIR)/build/X86/gem5.debug


### running in gdbserver on physical hardware


### building binary executable

hwbrk-ppc.elf: hwbrk-ppc.o
	powerpc-linux-gnu-ld -static -e 10000 -Ttext 10000 -o hwbrk-ppc.elf hwbrk-ppc.o

hwbrk-ppc.o: hwbrk-ppc.s
	powerpc-linux-gnu-as -g -o hwbrk-ppc.o hwbrk-ppc.s

hwbrk-i686.elf: hwbrk-i686.o
	i686-linux-gnu-ld -static -e0x10000000 -Ttext=0x10000000 -o hwbrk-i686.elf hwbrk-i686.o

hwbrk-i686.o: hwbrk-i686.s
	i686-linux-gnu-as -g -o hwbrk-i686.o hwbrk-i686.s

