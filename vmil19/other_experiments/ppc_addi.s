	.machine ppc

	.section	".text"
	.align 4
	.globl _start
	.type	_start, @function

_start:
	addi 3, 3, 1
	sc

