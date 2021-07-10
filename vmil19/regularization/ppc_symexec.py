
import pyvex, angr, archinfo
from bitstring import Bits

import pudb ; pu.db

# lis r3, F0F0F0
#                op      RT      RA           d
lis_r3_F0F0 = '001111'+'00011'+'00000'+'1111000011110000'


arch = archinfo.ArchPPC32(archinfo.Endness.BE)
instr = lis_r3_F0F0
mcode = Bits(bin=instr).bytes
irsb = pyvex.block.IRSB(mcode, 0x1000, arch, opt_level=-1)

s0 = angr.SimState(arch=arch, mode="symbolic")
s0.ip = 0x1000

s1 = angr.engines.HeavyVEXMixin(project=None).process(s0, irsb=irsb)

succ = s1.flat_successors[0]
result = succ.regs.r3

print(result)

