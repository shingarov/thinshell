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
    name = irNode.__class__.__name__
    return getattr(ShapeDeterminant(), name) (irNode)

class ShapeDeterminant:
    def IMark(self, irNode):
        return ('IMark')

    def WrTmp(self, irNode):
        return ('WrTmp', irNode.tmp, termShape(irNode.data))

    def Put(self, irNode):
        return ('Put', 'offset', termShape(irNode.data))

    def Get(self, irNode):
        return ('Get', irNode.ty, 'offset')

    def Binop(self, irNode):
        opArgs = [termShape(arg) for arg in irNode.args]
        return tuple(['Binop', irNode.op]+opArgs)

    def RdTmp(self, irNode):
        return ('RdTmp', irNode.tmp)

    def Const(self, irNode):
        return ('Const', termShape(irNode.con))
    
    def U32(self, irNode):
        return ('U32')


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


class ShapeAnalysis:
    def __init__(self, spec, archName):
        self._sensitivity = None
        arch = findArchInfo(archName)
        self.specimens = {}
        k = 0
        self.shapes = {}
        self.shapeIndices = {} #reverse of shapes
        self.computeVarBitPositions(spec)
        self.P = [None] * (2**self.entropy)
        it = encodingspec_to_iter(spec)
        for encoding in it:
            thisSig = str(vexSignature(encoding.bytes, arch))
            if thisSig not in self.specimens:
                self.specimens[thisSig] = encoding
                self.shapes[k] = thisSig
                self.shapeIndices[thisSig] = k
                k = k+1
            encodingInt = int(self.variableSlice(encoding), 2)
            self.P[encodingInt] = self.shapeIndices[thisSig]

    def variableSlice(self, full):
        l = [('1' if full[31-i] else '0') for i in self.varBitPositions]
        return ''.join(l)

    def computeVarBitPositions(self, spec):
        self.varBitPositions = varBitPositionsFrom(spec, [], 31)
        self.varBitPositions.sort()
        self.varBitPositions.reverse()
        self.entropy = len(self.varBitPositions)

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

    def relevantBitPositions(self):
        return self.sensitivity.filterRelevantMembers(self.varBitPositions)

    def relevantBitPositionsString(self):
        relevantOnes = self.relevantBitPositions()
        l = lambda pos: '!' if pos in relevantOnes else '.'
        return ''.join(map(l, range(31,-1,-1)))
