from bitstring import Bits

from vexshape import ShapeAnalysis
from senslist import SensitivityList
import bit_iter

class OperandProjection:
    def __init__(self, OPS, SHAPES, correctShape, opIndex):
        self.OPS = OPS
        self.SHAPES = SHAPES
        self.correctShape = correctShape
        self.opIndex = opIndex

    def __getitem__(self, k):
        if self.SHAPES[k] != self.correctShape:
            return None
        ops = self.OPS[k]
        return ops[self.opIndex]


# MIPS add
#                 RS  RT  RD
spec = ['000000',  '10101',  '1111',1,   '000',2,   '00000100000']
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
    import pudb ; pu.db
    sl = SensitivityList(anal.entropy)
    opSensitivity = sl.guess(proj)
    if opSensitivity.isInsensitive():
        return proj[opNum]
    else:
        twoPoints = opSensitivity.twoPoints()
        # we found at least one sensitive bit, so at least 2 points.
        # this state of technology can't handle anything nonlinear,
        # so try linear interpolation
        fff = opSensitivity.asFieldSpec()
        # WRONG!!! needs to account for constructiveMask!
        itf = bit_iter.encodingspec_to_iter(fff)
        onePoint = next(itf)
        anotherPoint=next(itf)
        oneX = opSensitivity.significantSlice(onePoint).uint
        anotherX = opSensitivity.significantSlice(anotherPoint).uint
        oneY = proj[onePoint.uint]
        anotherY = proj[anotherPoint.uint]
        if (anotherY-oneY)%(anotherX-oneX) != 0:
            nonlinear
        A = (anotherY-oneY)//(anotherX-oneX)
        if (anotherY+oneY-A*(anotherX+oneX))%2 != 0:
            nonlinear
        B = (anotherY+oneY-A*(anotherX+oneX))//2
        special('constant')




f = inferFormulaFor(opNum, anal.wide)





