# An example program to test hardware breakpoints.
# Corresponds to HwBrkDoodle in the Smalltalk image.
# Make gives the flag "-e 10000" to ld to locate _start at 16r10000;
# connect to gdbserver, set hw breakpoint at 10008, continue and
# see which registers got set to 0x12340000 and which not yet.

.machine ppc
.section	".text"
.align 4
.globl _start
.type	_start, @function

_start:
    lis 1, 0x1234
    lis 2, 0x1234
    lis 3, 0x1234
    lis 4, 0x1234
    lis 5, 0x1234
    lis 6, 0x1234
    lis 7, 0x1234
    lis 8, 0x1234
    lis 9, 0x1234
    lis 10, 0x1234

