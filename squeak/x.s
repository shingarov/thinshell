.text
.globl	_start
.type	_start, @function

_start:
movl	$1, %eax
movl	$2, %eax
movl	$3, %eax
movl	%ecx, %ebp
nop
movl	$255, %eax
movl	$111, %ebp
nop
nop
nop
nop
nop
.skip 120*1024*1024
