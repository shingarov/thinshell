# Thinshell for Target-Agnostic Modtalk on PowerPC

# www.mouritzen.dk/aix-doc/en_US/a_doc_lib/aixassem/alangref/machine.htm
	.machine ppc

	.section	.data
	.align 4

nZone:
    .skip 4*1024*1024 # bytes

stack:
    .skip 1024*1024

heap:
    .skip 80*1024*1024


	.section	".text"
	.align 4
	.globl _start
	.type	_start, @function

_start:
    or 0,0,0 # magic

    mcrxr 0

    li 3,42
    li 0,1  # syscall No. in r0, sys_exit=1
    sc

