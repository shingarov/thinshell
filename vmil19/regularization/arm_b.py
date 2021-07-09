from vexshape import ShapeAnalysis
import bit_iter

# b
# --- cond   op   h  offset24
spec = [4, '101', 1, 5, '00000000000000', 5]
import pudb ; pu.db

anal = ShapeAnalysis(spec, 'armv5')
section = anal.getSection()
#sens = anal.computeSensitivity()
sens = anal.sensitivity

fs = sens.asFieldSpec()
it = bit_iter.encodingspec_to_iter(fs)
for varPossibility in it:
    print("%s -> %d" % (varPossibility.bin, anal.P[varPossibility.uint]))
