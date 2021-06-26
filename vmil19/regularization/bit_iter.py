
from bitstring import Bits
from itertools import product

def singleton_iterator(x):
    yield x

def singleton_field_iterator(binaryString):
    return singleton_iterator(Bits(bin=binaryString))

def bit_iterator(field_len):
    interval = range(0, 2**field_len)
    return ( Bits(uint=x, length=field_len) for x in interval )

def join_bits(bitArrays):
    return Bits().join(bitArrays)

# One field is either constant
#   -- in which case it's given by a string binary representation
# or variable of width w, assuming all possible values
#   -- in which case it's given by the int w
def fieldspec_to_iter(aStringOrInt):
    if isinstance(aStringOrInt, str):
        return singleton_field_iterator(aStringOrInt)
    else:
        return bit_iterator(aStringOrInt)

# The API to this module.
# specList is a list of one-field specs, where each one-field spec
# is a string or int suitable to pass to fieldspec_to_iter.
def encodingspec_to_iter(specList):
    l = map(fieldspec_to_iter, specList)
    p = product(*l)
    return map(join_bits, p)

