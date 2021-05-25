    .section .text
    .globl _start
_start:
    set 4, %g1
    set 1, %o0
    set msg, %o1
    set 4, %o2
    ta 0x10

    set 1, %g1
    set 42, %o0
    ta 0x10

msg:
    .ascii "YES\n"
