	.machine ppc
	.section	".text"
	.align 4
	.globl _start
	.type	_start, @function

_start:
    li 9, -1
    stw 0, 0(9)
