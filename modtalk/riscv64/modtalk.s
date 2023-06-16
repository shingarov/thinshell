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

    # At this point, a0 contains return value from
    # the last initializer (should be a program initializer).

    # If the return value is SMI, convert it to native (signed) integer
    # and store it in t0.
    # If not, store 254 in t0 (so 254 will be the exit status code when
    # initializer returns non-SMI object)
    addi t0, zero, 254
    andi t1, a0, 1
    beqz t1, .L_nonSMI
    srai t0, a0, 4
.L_nonSMI:

    # Just call exit. The exit status code is in t0 at this point
    # (see above).
    mv a0,t0
    li a7, 93 # SYS_exit
    ecall


.section .data
nZone:
.skip 4194304
heap:
.skip 8388608
st:
.skip 409600


