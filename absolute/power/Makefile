# build this in a native powerpc environment

elves: absolute rodatasegv

rodatasegv: rodatasegv.o
	ld -static -o $@ rodatasegv.o

rodatasegv.o: rodatasegv.s
	as -g -o $@ rodatasegv.s

absolute: absolute.o
	ld -static -e 0 -Ttext 0 -o absolute absolute.o

absolute.o: absolute.s
	as -g -o $@ absolute.s

exec-native-rodata: rodatasegv
	./rodatasegv

G5DIR=/home/boris/work/gem5

exec-gem5-absolute: absolute
	$(G5DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c absolute

exec-gem5-rodata: rodatasegv
	$(G5DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c rodatasegv


dump-default-linkscript:
	ld --verbose > default-linkscript

clean:
	rm -rf m5out *.o absolute rodatasegv
