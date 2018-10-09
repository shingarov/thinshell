	.machine ppc

	.section	.data
	.align 4

nZone:
    .skip 4*1024*1024 # bytes

stack:
    .skip 1024*1024

heap:
    .skip 80*1024*1024


	.section	".text"
	.align 4
	.globl _start
	.type	_start, @function

_start:
    or 0,0,0 # magic

    # load address of the nZone into r16
    lis 16, nZone@ha
    ori 16, 16, nZone@l   # r16 now has &nZone

    # heap goes in r17
    lis 17, heap@ha
    ori 17, 17, heap@l   # r17 now has &heap

    # stack goes in r18
    lis 18, stack@ha
    ori 18, 18, stack@l

    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0
    or 0,0,0

    # jump to the nZone
    mtctr 16
    bctrl

    # The exit code is in #R (r1).
    # It is encoded as a SmallInteger.
    # Mask it out by 00000000 00000000 00001111 11110000 and >>4
    # (in fact, the spec talks about rotating first, then masking).
    rlwinm 3,1,28,24,31 # exit arg in r3
    li 0,1  # syscall No. in r0, sys_exit=1
    sc

