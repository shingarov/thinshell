
.data
    hello:  .asciz  "Hello World\n"
    length: .word   12
.text
    .globl  __start
    .ent    __start
__start:
    li  $4, 1
    la  $5, hello
    lw  $6, length
    li  $2, 4004 # SYS_write
    syscall
    
    li $2, 4001 # SYS_exit
    li $4, 42
    syscall

    .end    __start

