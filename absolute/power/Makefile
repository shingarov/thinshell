
elves: absolute.elf rodatasegv.elf

ARCH=powerpc
GEM5_ARCH ?= POWER
QEMU_ARCH ?= ppc

rodatasegv.elf: rodatasegv.o
	$(LD) -static -o $@ rodatasegv.o

rodatasegv.o: rodatasegv.s
	$(AS) -g -o $@ rodatasegv.s

absolute.elf: absolute.o
	$(LD) -static -e 0 -Ttext 0 -o $@ absolute.o

absolute.o: absolute.s
	$(AS) -g -o $@ absolute.s

exec-native-rodata: rodatasegv.elf
	./rodatasegv

g5-absolute: absolute.elf
	$(GEM5_DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(GEM5_DIR)/configs/example/se.py -c absolute.elf --wait-gdb

g5-rodata: rodatasegv.elf
	$(GEM5_DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(GEM5_DIR)/configs/example/se.py -c rodatasegv.elf --wait-gdb

dump-default-linkscript:
	$(LD) --verbose > default-linkscript

include ../../Makefile.common
