from vexshape import ShapeAnalysis
import bit_iter

# mcrf BF, BFA
# Move Condition Register Field XL-form
# The contents of Condition Register field BFA
# are copied into Condition Register field BF
#
#        _opcd_  bf   --  bfa  -------    ___xog____    -
spec = ['001111', '100', '00', '011', '0000000', '0000000000', '0']
#spec = ['001111', 3, '00', 3, '0000000', '0000000000', '0']

import pudb ; pu.db

anal = ShapeAnalysis(spec, 'powerpc')
section = anal.getSection()
sens = anal.sensitivity

fs = sens.asFieldSpec()
it = bit_iter.encodingspec_to_iter(fs)
for varPossibility in it:
    print("%s -> %d" % (varPossibility.bin, anal.P[varPossibility.uint]))
