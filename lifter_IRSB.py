# synthesize the semantics of the following sequence:
# lis r3, 0x1234
# ori r3, r3, 0x5678
# prove that execution results in r3==0x12345678
# and in general, if x==a..b, a,b in I16,
# then r3==x

import angr
import pyvex
import archinfo
import claripy

import pdb

arch = archinfo.ArchPPC32(archinfo.Endness.BE)
s = angr.SimState(arch=arch, mode="symbolic")

x = s.solver.BVS('x', 32, explicit_name=True)

#code = bytes(bytearray.fromhex("3c601234")) # lis

tyenv = pyvex.block.IRTypeEnv(arch, [ 'Ity_I32','Ity_I32','Ity_I32' ])

imark = pyvex.stmt.IMark(0x100, 4, 0)

a = claripy.Concat( x[31:16],  s.solver.BVV(0, 16))
c = pyvex.const.UN(a)
constExpr = pyvex.expr.Const(c)
wr = pyvex.stmt.WrTmp(1, constExpr)

rd = pyvex.expr.RdTmp(1)
put = pyvex.stmt.Put(rd, 28)

advance = pyvex.stmt.Put(pyvex.expr.Const(pyvex.const.U32(0x104)), 1168)

statements = [imark, wr, put, advance]

nxt = pyvex.expr.Const(pyvex.const.U32(0x104))


irsb1 = pyvex.IRSB.from_py(tyenv, statements, nxt, 'Ijk_Boring', 0x100, arch)
irsb1.pp()


code = bytes(bytearray.fromhex("60635678")) # ori
irsb2 = pyvex.IRSB(code, 0x104, arch, opt_level=0)
binop = irsb2.statements[3].data
co = binop.args[1]
b = x[15:0]
co.con._value = claripy.Concat(s.solver.BVV(0, 16), b)
irsb2.pp()

print "*************************"

irsb1.extend(irsb2)
irsb = irsb1
irsb.pp()

result = angr.SimEngineVEX().process(s, irsb).flat_successors[0]
r3 = result.regs.r3
result.regs.__dir__()
print r3
