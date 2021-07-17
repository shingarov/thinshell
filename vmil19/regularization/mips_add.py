from bitstring import Bits

from vexshape import ShapeAnalysis
from senslist import SensitivityList
import bit_iter

from z3 import *

class OperandProjection:
    def __init__(self, OPS, SHAPES, correctShape, opIndex):
        self.OPS = OPS
        self.SHAPES = SHAPES
        self.correctShape = correctShape
        self.opIndex = opIndex

    def __getitem__(self, k):
        if self.SHAPES[k] != self.correctShape:
            return -1 #need something to construct a Z3 int
        ops = self.OPS[k]
        return ops[self.opIndex]


# MIPS add
#                 RS  RT  RD
spec = ['000000',  '10101',  '1',4,   5,   '00000100000']
#spec = ['000000',  5,  5,  5,   '00000100000']
import pudb ; pu.db

anal = ShapeAnalysis(spec, 'mips')
anal.phase0_VEX()
print("Found %s shapes" % len(anal.shapes))
print(anal.sensitivity)
print("Representative instances:")
for specimen in anal.section:
    print(specimen)
print("=========================")

anal.phase1_shapes()
print(anal.relevantBitPositionsString())
for bits_shape in anal.shapeTags.items():
    print(bits_shape)
print("or in the opposite direction:")
print(anal.tagSets)

anal.phase2_partitioning()
if anal.isRegular():
    print("Instruction is REGULAR")
else:
    print("Instruction is easily normalizable;")
    print("Narrow shape is %d" % anal.narrow)


# infer operand formulae for the narrow shape
print("=== shape %d: ============" % anal.narrow)
print(anal.shapes[anal.narrow]) # cant do better because it's a string
print("=== operands: ===========")
print(".......")



# infer operand formulae for the wide shape
print("=== shape %d: ============" % anal.wide)
print(anal.shapes[anal.wide]) # cant to better because it's a string
print("=== operands: ===========")

# a representative instance to fetch from OPS
# this is only needed so that we know how many operands to iterate over
wideSpecimen = anal.section[anal.wide]
aaa = list(wideSpecimen).copy()
aaa.reverse()
b = Bits([aaa[k] for k in anal.varBitPositions])
exampleOps = anal.OPS[b.uint]
#opNum proshpandulivae range(exampleOps.len())
opRT = 1
opRD = 10
opNum = opRD

def inferFormulaFor(opNum, shapeN):
    proj = OperandProjection(anal.OPS, anal.P, shapeN, opNum)
    sl = SensitivityList(anal.entropy)
    opSensitivity = sl.guess(proj, anal.P, shapeN)
    if opSensitivity.isInsensitive():
        return proj[opNum]
    else:
        width = opSensitivity.entropy
        solver = Solver()
        Q = Array('Y', BitVecSort(width), BoolSort())
        Y = Array('Y', BitVecSort(width), IntSort())
        for i in range(2**width):
              x = BitVecVal(i, width)
              s = opSensitivity.section(i).uint
              solver.add(Q[x] == BoolVal(anal.P[s]==shapeN))
              y = proj[s]
              solver.add(Y[x] == IntVal(y))

        a = Int('a')
        b = Int('b')
        x = BitVec('x', width)
        thm = ForAll(x,
                Implies(Q[x],
                    Y[x] == (BV2Int(x)*a + b)))
        solver.add(thm)
        result = solver.check()
        if result != sat:
            raise Error()
        m = solver.model()
        return m.eval(a).as_long(), m.eval(b).as_long()

import pudb ; pu.db
f = inferFormulaFor(opNum, anal.wide)





