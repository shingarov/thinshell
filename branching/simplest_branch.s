# put r1==0? 42:43 into r3 and return

.file	"simplest_branch.c"
.machine ppc
.section	".text"
.align 2
.globl _start
.type	_start, @function

_start:
	cmpwi 0,1,0
	bne 0,.L
	li 3,42
	blr

.L:
	li 3,43
	blr
