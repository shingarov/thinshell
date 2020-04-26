.text
.globl	_start
.type	_start, @function

_start:
movl	$0x12345678, %eax
movl	$0x12345678, %ebx
movl	$0x12345678, %ecx
movl	$0x12345678, %edx
movl	$0x12345678, %esi
movl	$0x12345678, %edi
nop
