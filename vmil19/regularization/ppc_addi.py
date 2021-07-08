from vexshape import ShapeAnalysis

# lis
# 0x3c60XXXX
# let's vary RA and D
#spec = ['001111', '00011', 5, 16]
spec = ['001111', '00011', 5, '000000', 10]
#spec = ['001111', '00011', 5, '1111000011110000']
import pudb ; pu.db

anal = ShapeAnalysis(spec, 'powerpc')
section = anal.getSection()
sens = anal.computeSensitivity()

