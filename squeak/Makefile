


x.elf: x.o
	i686-linux-gnu-ld -static -e 0 -Ttext 0 -o x.elf x.o

x.o: x.s
	i686-linux-gnu-as -o x.o x.s

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py
DEBUG5="--debug-flags=Fetch,SimpleCPU"
#DEBUG5="--debug-flags=GDBMisc,GDBRecv,GDBSend,Fetch,Decode,SimpleCPU,Event"

g5:
	$(G5DIR)/build/X86/gem5.debug $(DEBUG5) $(G5SEPY) -c x.elf --wait-gdb=1

d5:
	echo run $(DEBUG5) $(G5SEPY) -c x.elf --wait-gdb=1 | xclip -i
	/usr/bin/gdb $(G5DIR)/build/X86/gem5.debug


print-run:
	@echo /usr/bin/gdb $(G5DIR)/build/X86/gem5.debug
	@echo run $(DEBUG5) $(G5SEPY) -c x.elf --wait-gdb=1

clean:
	rm  -f x.o x.elf
	rm -rf m5out
