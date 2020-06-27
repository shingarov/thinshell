
### Thinshell for running in gem5

squeak.elf: squeak.o
	x86_64-linux-gnu-ld -static -Ttext 0x20000 -o squeak.elf squeak.o

squeak.o: squeak.s
	x86_64-linux-gnu-as -o squeak.o  squeak.s

G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py

#DEBUG5=--debug-flags=Exec  --debug-file=sqTrace
DEBUG5=--debug-flags=Exec

g5:
	$(G5DIR)/build/X86/gem5.debug $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1

d5:
	echo run $(DEBUG5) $(G5SEPY) -c squeak.elf --wait-gdb=1 | xclip -i
	/usr/bin/gdb $(G5DIR)/build/X86/gem5.debug

clean:
	rm  -f squeak.o squeak.elf
	rm -rf m5out
