# Squeak thinshell for PowerPC

.machine ppc

.section .rodata
# see implementors of getDefaultCogCodeSize
.skip 0x200000

# The R/W area.
.section .data
.skip 200*1024*1024

# Initial "thinshell prologue".
# See TargetAwareX86>>#runThinshellPrologue.
# NB: This is NOT the entry point used in Cog simulation,
# which is set by the Cogit in simulateCogCodeAt: address.
.section .text
.globl	_start
.type	_start, %function
_start:
    trap



# Stuff below this line is just some doodles to play around with branching
# to non-JIT-produced code.  This is NOT needed for simulating Cog.
# See CogILTest>>testCallFull.

.globl exit
.type exit, %function
exit:
    li 0, 1  # exit()
    li 3, 42
    sc

.globl print
.type print, %function
# Print the string pointed to by GPR5, 20 bytes of it
print:
    li 0, 4  # write()
    li 3, 1  # stdout
    lis 4, s@ha
    la 4, s@l(4)
    li 5, 20
    sc
    blr
    
.type s, %object
.size s, 20
s:
.ascii  "****** TEST ******\012\000"
