
# The guard page is not included because these "skip" values can't be mapped
# to the guard page.
# We start directly from the R/O pages.
.section .rodata
.skip 0x100000

# The R/W area.
.section .data
.skip 120*1024*1024

# Initial text.
.section .text
.globl	_start
.type	_start, @function
_start:
    mov $1, %eax
    mov $2, %eax
    int3
