# Experiment with loading the process image at a given absolute address.
# This will be used for compatibility with Eliot's simulator.

	.machine ppc

	.section .text
	.align 16

	# simply exit to the OS with 42
	xor 3,3,3
	li 3, 42
	li 0, 1  # syscall No. in r0, sys_exit=1
	sc

