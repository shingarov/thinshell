	.machine ppc

	.section	.data
	.align 4

A:
    .byte 0x11
    .byte 0x22
    .byte 0x22
    .byte 0x33
    .byte 0x00
    .byte 0x33
    .byte 0x33
    .byte 0x33


B:
    .byte 0x11
    .byte 0x22
    .byte 0x22
    .byte 0x33
    .byte 0x00
    .byte 0x55
    .byte 0x33
    .byte 0x33
    .string "aaa"

nZone:
    .skip 4*102400 # bytes

heap:
    .skip 4*102400

stack:
    .skip 4*102400


	.section	".text"
	.align 4
	.globl _start
	.type	_start, @function

_start:
    or 0,0,0 # magic


lis 4,0x7f7f
ori  4,4,0x7f7f



lis 11,A@ha
ori 11,11,A@l

lis 12,B@ha
ori 12,12,B@l

NextWord:

 # Load from RAM
lwz 1, 0(11)
lwz 2, 0(12)

 # See which chars are 0 in string A
and 5,1,4
add 5,5,4
or 5,5,1
nor 5,5,4
 # 0x80 in position of every zero byte of string A, 0x00 in other places
cntlzw 5,5
rlwinm 5,5,29,24,31
 # R5 now contains the number of leftmost zero byte of string A,
 # or 4 if all are non-zero

xor. 2,1,2
 # if equal, either increment or signal found!
bne cr0, Ldifferent
 # The words are the same. Are there zero bytes in them?
cmpwi cr0, 5, 4 # if R5 equal to 4, then no zero bytes
bne cr0, FoundMatch
addi 11, 11, 4
addi 12, 12, 4
b NextWord

FoundMatch:
blr

Ldifferent:
cntlzw 3,2
rlwinm 3,3,29,24,31
 # now the number of leftmost different byte in R3

 # If R5 is strictly less than R3, then the two strings are equal
cmpw cr0, 3, 5
bgt FoundMatch

trap


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

