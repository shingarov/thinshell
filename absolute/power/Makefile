
# See if we are building in a native powerpc environment
BUILD_ARCH := $(shell uname -m)
ifeq ($(BUILD_ARCH), ppc)
	TOOLCHAIN_PREFIX=
else
	TOOLCHAIN_PREFIX=powerpc-linux-gnu-
endif


elves: absolute.elf rodatasegv.elf

rodatasegv.elf: rodatasegv.o
	$(TOOLCHAIN_PREFIX)ld -static -o $@ rodatasegv.o

rodatasegv.o: rodatasegv.s
	$(TOOLCHAIN_PREFIX)as -g -o $@ rodatasegv.s

absolute.elf: absolute.o
	$(TOOLCHAIN_PREFIX)ld -static -e 0 -Ttext 0 -o $@ absolute.o

absolute.o: absolute.s
	$(TOOLCHAIN_PREFIX)as -g -o $@ absolute.s

exec-native-rodata: rodatasegv.elf
	./rodatasegv

G5DIR=/home/boris/work/gem5

exec-gem5-absolute: absolute.elf
	$(G5DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c absolute.elf

exec-gem5-rodata: rodatasegv.elf
	$(G5DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c rodatasegv.elf


dump-default-linkscript:
	$(TOOLCHAIN_PREFIX)ld --verbose > default-linkscript

clean:
	rm -rf m5out *.o *.elf
