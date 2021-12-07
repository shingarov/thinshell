	.text
	.globl	_start
	.type	_start, @function

_start:
	subl	$-2, %eax
	.byte 0x72
	.byte 0x40
