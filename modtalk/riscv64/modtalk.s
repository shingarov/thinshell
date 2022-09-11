# Thinshell for Target-Agnostic Modtalk on 64-bit RISC-V

.section .text
.globl	_start
.type	_start, %function
_start:
    nop

    # load address of the nZone into x16
    lui  x16, %hi(nZone)
    addi x16, x16, %lo(nZone)

    # heap goes in x17
    lui  x17, %hi(heap)
    addi x17, x17, %lo(heap)

    # stack goes in x18
    lui  x17, %hi(heap)
    addi x17, x17, %lo(heap)

    nop
    nop
    nop
    nop
    nop
    nop
    # jump to the nZone
    jalr x16
    li x1, 42
    ecall


.section .data
nZone:
.skip 4194304
heap:
.skip 8388608
st:
.skip 409600


