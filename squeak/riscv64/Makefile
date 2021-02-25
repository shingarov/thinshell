### Thinshell for running in gem5

squeak.elf: squeak.o
	riscv64-linux-gnu-ld -static -T Link -o squeak.elf squeak.o

squeak.o: squeak.s
	riscv64-linux-gnu-as -o squeak.o squeak.s
clean:
	rm  -f squeak.o squeak.elf
