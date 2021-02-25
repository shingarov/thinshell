# Squeak thinshell for RISC-V (RV64)

.section .rodata
# see implementors of getDefaultCogCodeSize
.skip 0x200000

# The R/W area.
.section .data
.skip 200*1024*1024

# Initial "thinshell prologue".
# See TargetAwareX86>>#runThinshellPrologue.
# NB: This is NOT the entry point used in Cog simulation,
# which is set by the Cogit in simulateCogCodeAt: address.
.section .text
.globl	_start
.type	_start, %function
_start:
    ebreak
    nop
    nop
    ret
