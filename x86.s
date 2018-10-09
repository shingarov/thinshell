
	.data
	.align 4

nZone:
    .skip 4*1024*1024 # bytes

stack:
    .skip 1024*1024

heap:
    .skip 80*1024*1024


	.text
	.align 4
	.globl _start
	.type	_start, @function

_start:
    movl $286331153, %eax
    movl $572662306, %ebx
    movl %esp, %ecx
    movl %esp, %edx
    movl %esp, %edi
