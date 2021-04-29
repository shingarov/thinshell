
### Thinshell for running in gem5

squeak.elf: squeak.o
	arm-linux-gnueabihf-ld -static -T Link -o squeak.elf squeak.o

squeak.o: squeak.s
	arm-linux-gnueabihf-as -ggdb -o squeak.o squeak.s

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py

DEBUG5=--debug-flags=Fetch,Exec,Fault
#DEBUG5=--debug-flags=GDBMisc,GDBSend,GDBRecv,AddrRanges

g5:
	$(G5DIR)/build/ARM/gem5.debug $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 --param 'system.shared_backstore = "/gem5"'

#$(G5DIR)/build/ARM/gem5.debug $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 --param 'system.shared_backstore = "/gem5"' -I 40

d5:
	echo run $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 | xclip -i
	/usr/bin/gdb $(G5DIR)/build/ARM/gem5.debug

d5v:
	echo run $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 | xclip -i
	vim -c "Termdebug $(G5DIR)/build/ARM/gem5.debug" -c "Break _start" -c "Run $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1"


###

clean:
	rm  -f squeak.o squeak.elf
	rm -rf m5out
