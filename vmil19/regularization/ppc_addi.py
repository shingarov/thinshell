from vexshape import ShapeAnalysis
from senslist import SensitivityList
import bit_iter

class OperandProjection:
    def __init__(self, OPS, opIndex):
        self.OPS = OPS
        self.opIndex = opIndex

    def __getitem__(self, k):
        ops = self.OPS[k]
        return ops[self.opIndex]


# lis
#          op       RT    RA       d
spec = ['001111', '00011', 5, '000000000000000',1]
#spec = ['001111',   5, '11100',   '00000000',8]
#spec = ['001111',  5, '00011', '1111000011110000']
import pudb ; pu.db

anal = ShapeAnalysis(spec, 'powerpc')
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

import pudb ; pu.db
anal.phase2_partitioning()

shapeN = 0
opN = 999999
proj = OperandProjection(anal.OPS, 1)

sl = SensitivityList(anal.entropy)
# nonono, this is wrong,
# because we should be exploring one particular shape,
# not the whole instruction
opSensitivity = sl.guess(proj)

if opSensitivity.isInsensitive():
    theConst = proj[0]
    print(hex(theConst))
else:
    # we found at least one sensitive bit, so at least 2 points.
    # at this point, we can't handle anything nonlinear.
    fff = opSensitivity.asFieldSpec()
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




