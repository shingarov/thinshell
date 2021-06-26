from vexshape import shape_specimens

# bla LI
# 010010,LI,11
# opcd=18, AA=1, LK=1
# let's vary LI (24 bits)
spec = ['010010', 24, '11']
#spec = ['010010', 4, '11111111111111111111', '11']
section = shape_specimens(spec, 'powerpc')
print(section)

