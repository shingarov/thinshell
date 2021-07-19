from bitstring import Bits

from vexshape import ShapeAnalysis
from senslist import SensitivityList
import bit_iter


# MIPS add
#                      RS      RT      RD
spec = ['000000',  '1010',1,  5,   5,   '00000100000']
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

#anal.phase2_partitioning()
#if anal.isRegular():
#    print("Instruction is REGULAR")
#else:
#    print("Instruction is easily normalizable;")
#    print("Narrow shape is %d" % anal.narrow)



import pudb ; pu.db

shapeN = 3
exampleOps = anal.specimenOpsOfShape(shapeN)
ops = [anal.formulaFor(opNum, shapeN) for opNum in range(len(exampleOps))]
    
print(ops)
