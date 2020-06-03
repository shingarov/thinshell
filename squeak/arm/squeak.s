
.section .rodata
# see implementors of getDefaultCogCodeSize
.skip 0x200000

# The R/W area.
.section .data
.skip 200*1024*1024

# Initial "thinshell prologue".
# See TargetAwareX86>>#runThinshellPrologue.
.section .text
.arm
.globl	_start
.type	_start, %function
_start:
    bkpt
