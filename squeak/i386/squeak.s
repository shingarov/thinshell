
# The guard page is not included because these "skip" values can't be mapped
# to the guard page.
# We start directly from the R/O pages.
.section .rodata
.skip 0x200000

# The R/W area.
.section .data
.skip 200*1024*1024

# Initial "thinshell prologue".
# See TargetAwareX86>>#runThinshellPrologue.
.section .text
.globl	_start
.type	_start, @function
_start:
    int3
