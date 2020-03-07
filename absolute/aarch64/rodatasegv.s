	.arch armv8-a
	.text
	.global	A

	.section	.rodata
	.align	3
	.type	A, %object
	.size	A, 18
A:
	.string	"This is read-only"


	.text
	.align	4
	.global	_start
_start:
	adrp	x0, A+1
	add	x0, x0, :lo12:A+1
	mov	w1, 5
	# the store into rodata on the next line will segfault
	strb	w1, [x0]

	# however, if the MMU does not trap on rodata, we successfully exit(42)

    # exit
    mov x0, #42
    mov x8, #93
    svc #0
