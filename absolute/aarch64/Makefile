# build this in a native arm64 environment

rodatasegv: rodatasegv.o
	ld -static -o $@ rodatasegv.o

rodatasegv.o: rodatasegv.s
	as -g -o $@ rodatasegv.s

exec-native: rodatasegv
	./rodatasegv

G5DIR=/home/boris/work/gem5

exec-gem5: rodatasegv
	$(G5DIR)/build/ARM/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c rodatasegv




dump-default-linkscript:
▸···ld --verbose > default-linkscript

clean:
▸···rm -rf m5out *.o absolute rodatasegv
