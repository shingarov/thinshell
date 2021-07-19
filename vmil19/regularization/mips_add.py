from bitstring import Bits

from vexshape import ShapeAnalysis
from senslist import SensitivityList
import bit_iter


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


import pudb ; pu.db

# infer operand formulae for the wide shape
thisShapeN = anal.wide
print("=== shape %d: ============" % thisShapeN)
print(anal.shapes[thisShapeN]) # cant to better because it's a string
print("=== operands: ===========")

exampleOps = anal.specimenOpsOfShape(thisShapeN)
#opNum proshpandulivae range(exampleOps.len())
opRT = 1
opRD = 10
opNum = opRD

f = anal.inferFormulaFor(opNum, anal.wide)





