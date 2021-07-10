from vexshape import ShapeAnalysis
import bit_iter

# lis
# 0x3c60XXXX
# let's vary RA and D
#spec = ['001111', '00011', 5, 16]
spec = ['001111', '00011', 5, '00000000', 8]
#spec = ['001111', '00011', 5, '1111000011110000']
import pudb ; pu.db
#input("Input please:")

anal = ShapeAnalysis(spec, 'powerpc')
section = anal.getSection()
#sens = anal.computeSensitivity()
sens = anal.sensitivity

fs = sens.asFieldSpec()
it = bit_iter.encodingspec_to_iter(fs)
for varPossibility in it:
    print("%s -> %d" % (varPossibility.bin, anal.P[varPossibility.uint]))
spec  = ['001111', '01001', '00011', '00000000', 8]
