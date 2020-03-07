# Athens 2019, Figure 2.
# addi r3, r3, 0x1
# put X in r3, execute, find X+1 in r3

import angr
import pyvex
import archinfo
import claripy

import pdb

arch = archinfo.ArchPPC32(archinfo.Endness.BE)
s = angr.SimState(arch=arch, mode="symbolic")

x = s.solver.BVS('X', 32, explicit_name=True)

code = bytes(bytearray.fromhex("38630001")) # addi

irsb = pyvex.IRSB(code, 0x100, arch, opt_level=0)
irsb.pp()

s.regs.r3 = x

result = angr.SimEngineVEX().process(s, irsb).flat_successors[0]

r3 = result.regs.r3
result.regs.__dir__()
print "*************************"
print r3
