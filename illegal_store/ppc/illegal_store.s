# This is a guinea-pig program for playing with ULD's treatment
# of exception signals.
# Die of SEGV dereferencing 0xFFFFFFFF for writing;
# ThinshellTest>>testIllegalStore will catch the DebugStopped
# and verify the signal number.

.machine ppc
.text
.align 4
.globl _start
.type	_start, @function

_start:
    li 9, -1
    stw 0, 0(9)
    # this would exit to the OS with 42
    # if we didn't die on the previous line
    xor 3,3,3
    li 3, 42
    li 0, 1  # syscall No. in r0, sys_exit=1
    sc

