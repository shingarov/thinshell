.machine ppc

.section ".data"
.align 4

nZone:
	.string "Hello!"

.section ".text"
.align 4
.globl _start
.type	_start, @function

_start:
    or 0,0,0 # magic

    # load address of the nZone into r16
    lis 16, nZone@ha
    ori 16, 16, nZone@l   # r16 now has &nZone
	b Label1

	mflr 0
	mr 31,1

Label1:
	mtctr 16
    bctrl
