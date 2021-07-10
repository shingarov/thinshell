# Here is a little experiment with vex regularization.

# In Pharo-ArchC and related fundamental parts of Smalltalk-25,
# we call things of the form (using PPC example here)
#    addis RT, RA, D
# "instruction declarations", and things of the form
#    addis r3, r1, 0x1234
# "ground instruction instances".
#
# We say that two VEX IRSBs have the same shape if they only differ
# in the leaf constants.  This means, the U16/U32/etc constants in Const
# expressions, but also things like register offsets in GET and PUT
# (because, say, when RA varies those will vary too).  This has the
# disadvantage that special offsets like PC=1168 on PPC, are not recognized
# as special; cf. criticism of ARM uniform SPRs in Waterman's thesis.
#
# Of course, two IRSBs of different shapes can still denote the same
# function; in this sense shape is not a hash for homotopy.
#
# An instruction is called vex-regular if all its ground instances
# lift to VEX of the same shape.


import pyvex
import archinfo
from bit_iter import encodingspec_to_iter
from bitstring import Bits

from senslist import SensitivityList

def termShape(irNode):
    #import pudb ; pu.db
    if irNode.__class__==pyvex.stmt.IMark:
        return ('IMark')
    if irNode.__class__==pyvex.stmt.WrTmp:
        return ('WrTmp', irNode.tmp, termShape(irNode.data))
    if irNode.__class__==pyvex.stmt.Put:
        return ('Put', 'offset', termShape(irNode.data))
    if irNode.__class__==pyvex.expr.Get:
        return ('Get', irNode.ty, 'offset')
    if irNode.__class__==pyvex.expr.Binop:
        opArgs = [termShape(arg) for arg in irNode.args]
        return tuple(['Binop', irNode.op]+opArgs)
    if irNode.__class__==pyvex.expr.RdTmp:
        return ('RdTmp', irNode.tmp)
    if irNode.__class__==pyvex.expr.Const:
        return ('Const', termShape(irNode.con))
    if irNode.__class__==pyvex.const.U32:
        return ('U32')
    else:
        import pudb ; pu.db
        irNode.pp()
        raise Exception('should be implemented')
        #return irNode.__class__.__name__


def vexSignature(code, arch):
    irsb = pyvex.block.IRSB(code, 0x1000, arch, opt_level=-1)
    sig = [ termShape(t) for t in irsb.statements ]
    return irsb.tyenv.types, sig

def findArchInfo(archName):
    if archName=='powerpc':
        return archinfo.ArchPPC32(archinfo.Endness.BE)
    if archName=='armv5':
        return archinfo.ArchARM()
    raise NotFoundError(archName)

def varBitPositionsFrom(spec, soFar, msb):
    if not spec:
        return soFar
    car = spec[0]
    if isinstance(car, str):
        return varBitPositionsFrom(spec[1:], soFar, msb-len(car))
    l = [msb-pos for pos in range(car)]+soFar
    return varBitPositionsFrom(spec[1:], l, msb-car)



def varBitPositions(spec):
    ps = varBitPositionsFrom(spec, [], 31)
    ps.sort()
    return ps

class ShapeAnalysis:
    def __init__(self, spec, archName):
        self._sensitivity = None
        arch = findArchInfo(archName)
        self.specimens = {}
        k = 0
        self.shapes = {}
        self.shapeIndices = {} #reverse of shapes
        varBits = varBitPositions(spec)
        varBits.reverse()
        self.entropy = len(varBits)
        self.P = [None] * (2**self.entropy)
        it = encodingspec_to_iter(spec)
        for encoding in it:
            thisSig = str(vexSignature(encoding.bytes, arch))
            if thisSig not in self.specimens:
                self.specimens[thisSig] = encoding
                self.shapes[k] = thisSig
                self.shapeIndices[thisSig] = k
                k = k+1
            v = ''.join([('1' if encoding[31-i] else '0') for i in varBits])
            encodingInt = int(v,2)
            self.P[encodingInt] = self.shapeIndices[thisSig]

    def getSection(self):
        return list(self.specimens.values())

    def computeSensitivity(self):
        sl = SensitivityList(self.entropy)
        self._sensitivity = sl.guess(self.P)

    @property
    def sensitivity(self):
        if not self._sensitivity:
            self.computeSensitivity()
        return self._sensitivity
