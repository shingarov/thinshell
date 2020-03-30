
illst.elf: illst.o
	powerpc-linux-gnu-ld -static -o illst.elf illst.o

illst.o: illst.s
	powerpc-linux-gnu-as -g -o illst.o illst.s

G5DIR=/home/boris/work/gem5

gem5: illst.elf
	$(G5DIR)/build/POWER/gem5.debug --debug-flags=Fetch,Decode $(G5DIR)/configs/example/se.py -c illst.elf

