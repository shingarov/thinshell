
### Thinshell for running in gem5

squeak.elf: squeak.o
	i686-linux-gnu-ld -static -Trodata 0x20000 -o squeak.elf squeak.o

squeak.o: squeak.s
	i686-linux-gnu-as -o squeak.o squeak.s

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py

#DEBUG5=--debug-flags=Exec
#DEBUG5=--debug-flags=Exec  --debug-file=sqTrace
DEBUG5=--debug-flags=GDBMisc,GDBRecv,GDBSend

g5:
	$(G5DIR)/build/X86/gem5.debug $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1

d5:
	echo run $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 | xclip -i
	/usr/bin/gdb $(G5DIR)/build/X86/gem5.debug

### For running on stock silicon

share.elf: share.c
	i686-linux-gnu-gcc-9 -ggdb -o share.elf share.c -lrt

# run with:
#  gdbserver myhostname:7000 share.elf

###

clean:
	rm  -f squeak.o squeak.elf
	rm -rf m5out
