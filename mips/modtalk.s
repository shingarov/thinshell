
.text
.align 4
.type	__start, @function
.globl __start

__start:
    sll $0, $0, 0  # nop

    # load address of the nZone into r16
    la  $16, nZone

    # heap goes in r17
    la  $17, heap

    # stack goes in r18
    la  $18, st

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # jump to the nZone
    jalr $16
    nop # delay slot

.data
    .comm nZone,4194304 # bytes
    .comm heap, 8388608
    .comm st,409600

