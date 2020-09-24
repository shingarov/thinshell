
.section .rodata
# see implementors of getDefaultCogCodeSize
.skip 0x200000

# The R/W area.
.section .data
.skip 200*1024*1024

# Initial "thinshell prologue".
# See TargetAwareX86>>#runThinshellPrologue.
.section .text
.arm
.globl	_start
.type	_start, %function
_start:
    bkpt

.type exit, %function
exit:
    mov R7, #1
    mov r0, #42
    svc 0

.type print, %function
print:
    mov r7, #4
    mov r0, #1
    mov r1, r5
    mov r2, #20
    svc 0
    mov pc, lr

.type s, %object
.size s, 20
s:
.ascii	"****** TEST ******\012\000"
