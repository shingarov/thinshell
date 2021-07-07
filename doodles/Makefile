
# POWER

# Big-Endian version
ppc.elf: ppc.o
	powerpc-linux-gnu-ld -static -o ppc.elf ppc.o

ppc.o: ppc.s
	powerpc-linux-gnu-as -g -o ppc.o ppc.s


# Little-Endian version
ppcle.elf: ppcle.o
	powerpc-linux-gnu-ld --oformat elf32-powerpcle -static -o ppcle.elf ppcle.o

ppcle.o: ppc.s
	powerpc-linux-gnu-as -mlittle -g -o ppcle.o ppc.s

# ARM

arm.elf: arm.o
	arm-linux-gnueabihf-ld -static -o arm.elf arm.o

arm.o: arm.s
	arm-linux-gnueabihf-as -g -o arm.o arm.s



# gem5 simulation
G5DIR=/home/boris/work/gem5
G5SEPY=$(G5DIR)/configs/example/se.py
DEBUG5="--debug-flags=GDBRecv,GDBSend,Fetch,Decode"

g5:
	$(G5DIR)/build/POWER/gem5.debug $(DEBUG5) $(G5SEPY) -c ppc.elf --wait-gdb=1

# inside gdb:
# run --debug-flags=GDBRecv,GDBSend,Fetch,Decode /home/boris/work/gem5/configs/example/se.py -c ppc.elf --wait-gdb=1
