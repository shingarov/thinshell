
.text
.arm
.globl	_start
_start:
    bl print
    bl exit
    bkpt

.globl	exit
exit:
    mov r7, #1
    mov r0, #42
    svc 0

.globl	print
print:
    mov r7, #4    ;@ syscall No
    mov r0, #1    ;@ stdout fd
    ldr r1, =MSG
    ldr r2, =len
    svc 0
    mov pc, lr

.data
.globl	MSG
MSG:
    .asciz	"****** TEST ******\n"
len = .-MSG
