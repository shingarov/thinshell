
.section .text
.globl	_start
.type	_start, @function
_start:
    movabsq   $stack, %rsp
    movabsq   $stack, %rbp
    movabsq   $0x5555555555555555, %r15
    movabsq   $0x6666666666666666, %r14
    push %r15
    push %r14
    int3
.skip 20*1024*1024
stack:

