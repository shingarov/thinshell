# Thinshell for Target-Agnostic Modtalk on 64-bit RISC-V

.section .text
.globl	_start
.type	_start, %function
_start:
    nop

    # load address of the nZone into s9
    lui  s9, %hi(nZone)
    addi s9, s9, %lo(nZone)

    # heap goes in s10
    lui  s10, %hi(heap)
    addi s10, s10, %lo(heap)

    # stack goes in s11
    lui  s11, %hi(heap)
    addi s11, s11, %lo(heap)

    nop
    nop
    nop
    nop
    nop
    nop
    # jump to the nZone
    jalr s9
    li x1, 42
    ecall


.section .data
nZone:
.skip 4194304
heap:
.skip 8388608
st:
.skip 409600


