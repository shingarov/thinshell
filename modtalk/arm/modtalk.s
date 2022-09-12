
.text
.arm
.globl	_start
_start:
    nop
    ldr r1, =heap
    ldr lr, =nZone
    ldr sp, =st
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    bx lr

.data
.globl  nZone
nZone:
    .space 4096
.globl  heap
heap:
    .space 4096
.globl  st
st:
    .space 4096

