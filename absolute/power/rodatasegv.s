	.machine ppc
	.section	".text"
	.globl A
	.section	.rodata
	.align 2
	.type	A, @object
	.size	A, 18
A:
	.string	"This is read-only"



	.section	".text"
	.align 2
	.globl _start
	.type	_start, @function
_start:
	lis 9,A+1@ha
	la 9,A+1@l(9)
	li 10,5
	stb 10,0(9)


	# simply exit to the OS with 42
	xor 3,3,3
	li 3, 42
	li 0, 1  # syscall No. in r0, sys_exit=1
	sc

