from vexshape import shape_specimens

# lis
# 0x3c60XXXX
# let's vary RA and D
spec = ['001111', '00011', 5, 16]
#spec = ['001111', '00011', 5, '1111000011110000']
section = shape_specimens(spec, 'powerpc')
print(section)

