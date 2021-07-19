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
from z3 import *
from bit_iter import encodingspec_to_iter
from bitstring import Bits

from senslist import SensitivityList
from special_chars import *


class OperandProjection:
    def __init__(self, OPS, SHAPES, correctShape, opIndex):
        self.OPS = OPS
        self.SHAPES = SHAPES
        self.correctShape = correctShape
        self.opIndex = opIndex

    def __getitem__(self, k):
        if self.SHAPES[k] != self.correctShape:
            return -1 #need something to construct a Z3 int
        ops = self.OPS[k]
        return ops[self.opIndex]

def termConstants(irNode):
    name = irNode.__class__.__name__
    return getattr(ConstExtractor(), name) (irNode)

class ConstExtractor:
    def IMark(self, irNode):
        return [irNode.addr, irNode.len, irNode.delta]

    def WrTmp(self, irNode):
        return (termConstants(irNode.data))

    def Put(self, irNode):
        return irNode.offset

    def Get(self, irNode):
        return irNode.offset

    def Binop(self, irNode):
        evenNones = [termConstants(arg) for arg in irNode.args]
        return [x for x in evenNones if x!=None]

    def Unop(self, irNode):
        evenNones = [termConstants(arg) for arg in irNode.args]
        return [x for x in evenNones if x!=None]

    def RdTmp(self, irNode):
        return None

    def Const(self, irNode):
        return termConstants(irNode.con)
    
    def U32(self, irNode):
        return irNode.value
    
    def Exit(self, irNode):
        return None # BOGUS -- please implement


def termShape(irNode):
    name = irNode.__class__.__name__
    return getattr(ShapeDeterminant(), name) (irNode)

class ShapeDeterminant:
    def IMark(self, irNode):
        return ('IMark', CenteredDot, CenteredDot, CenteredDot)

    def WrTmp(self, irNode):
        return ('WrTmp', irNode.tmp, termShape(irNode.data))

    def Put(self, irNode):
        return ('Put', CenteredDot, termShape(irNode.data))

    def Get(self, irNode):
        return ('Get', irNode.ty, CenteredDot)

    def Binop(self, irNode):
        opArgs = [termShape(arg) for arg in irNode.args]
        return tuple(['Binop', irNode.op]+opArgs)

    def Unop(self, irNode):
        opArgs = [termShape(arg) for arg in irNode.args]
        return tuple(['Unop', irNode.op]+opArgs)

    def RdTmp(self, irNode):
        return ('RdTmp', irNode.tmp)

    def Const(self, irNode):
        return ('Const', termShape(irNode.con))
    
    def U32(self, irNode):
        return ('U32', CenteredDot)

    def Exit(self, irNode):
        guard = termShape(irNode.guard)
        dst = termShape(irNode.dst)
        return ('Exit', guard, dst, irNode.jk, CenteredDot)

def flatten(l):
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

def vexSignature(code, arch):
    irsb = pyvex.block.IRSB(code, 0x1000, arch, opt_level=-1)
    sig = [ termShape(t) for t in irsb.statements ]
    ops = [ termConstants(t) for t in irsb.statements ]
    return irsb.tyenv.types, sig, flatten(ops)

def findArchInfo(archName):
    if archName=='powerpc':
        return archinfo.ArchPPC32(archinfo.Endness.BE)
    if archName=='armv5':
        return archinfo.ArchARM()
    if archName=='mips':
        return archinfo.ArchMIPS32()
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
        self.spec = spec
        self.arch = findArchInfo(archName)
        self.computeVarBitPositions()

    def phase0_VEX(self):
        '''Lift VEX IR for every instance and collect the results.'''
        self._sensitivity = None
        self.specimens = {}
        self.shapes = {}
        self.shapeIndices = {} #reverse of shapes
        self.P   = [None] * (2**self.entropy)
        self.OPS = [None] * (2**self.entropy)
        it = encodingspec_to_iter(self.spec)
        k = 0
        for encoding in it:
            ty,sig,ops = vexSignature(encoding.bytes, self.arch)
            if ops[0]:
                raise Error("not IMark???")
            ops = ops[1:]
            thisSig = str((ty,sig))
            if thisSig not in self.specimens:
                self.specimens[thisSig] = encoding
                self.shapes[k] = thisSig
                self.shapeIndices[thisSig] = k
                k = k+1
            encodingInt = int(self.variableSlice(encoding), 2)
            self.P[encodingInt] = self.shapeIndices[thisSig]
            self.OPS[encodingInt] = ops

    def phase1_shapes(self):
        '''Group shapes'''
        self.shapeTags = {}
        self.tagSets = {k:set() for k in range(len(self.shapes))}
        fs = self.sensitivity.asFieldSpec()
        it = encodingspec_to_iter(fs)
        for varPossibility in it:
            sigBits = self.sensitivity.significantSlice(varPossibility)
            shapeNum = self.P[varPossibility.uint]
            self.shapeTags[sigBits] = shapeNum
            self.tagSets[shapeNum].add(sigBits)

    def phase2_partitioning(self):
        '''See if the partitioning of instances into shapes
        exhibits a simple structure.'''
        if self.isRegular():
            self.narrow = 0
            return "too easy: already regular"
        # We say an instruction is _easily normalizable_ if it
        # decomposes into exactly two shapes: the _narrow_ shape
        # with only one encoding of the discriminating bits,
        # and the _wide_ shape (everything else).
        # For example, addi has narrow RA=0 and wide RA!=0.
        # Obviously, when there is only one shape-discriminating
        # bit (e.g. H bit on ARM instruction b), both shapes can
        # be considered narrow.  In this case we arbitrarily choose
        # to call H=0 narrow and H=1 wide.
        if len(self.shapes) > 2:
            raise Error("Not easily normalizable")
        if len(self.tagSets) != 2:
            raise Error("what?!!!")
        if len(self.shapeTags) == 2:
            # special case of one discriminating bit
            should-be-implemented
        else:
            # either shape0 is narrow, or shape1 is
            ts0 = self.tagSets[0]
            ts1 = self.tagSets[1]
            if len(ts0)==1:
                self.narrow = 0
                self.wide = 1
                if len(ts1) != (2**self.sensitivity.entropy-1):
                    raise Error("what?!!!")
            else:
                self.narrow = 1
                self.wide = 0
                if len(ts0) != (2**self.sensitivity.entropy-1):
                    raise Error("what?!!!")

    def specimenEncodingOfShape(self, shapeN):
        thisShapeSpecimen = self.section[shapeN]
        aaa = list(thisShapeSpecimen).copy()
        aaa.reverse()
        return Bits([aaa[k] for k in self.varBitPositions])

    def specimenOpsOfShape(self, shapeN):
        return self.OPS[self.specimenEncodingOfShape(shapeN).uint]

    def inferFormulaFor(self, opNum, shapeN):
        proj = OperandProjection(self.OPS, self.P, shapeN, opNum)
        sl = SensitivityList(self.entropy)
        opSensitivity = sl.guess(proj, self.P, shapeN)
        if opSensitivity.isInsensitive(): # just a silly shortcut
            return repr(opSensitivity), 0, proj[opNum]
        width = opSensitivity.entropy
        solver = Solver()
        Q = Array('Y', BitVecSort(width), BoolSort())
        Y = Array('Y', BitVecSort(width), IntSort())
        for i in range(2**width):
            x = BitVecVal(i, width)
            s = opSensitivity.section(i).uint
            solver.add(Q[x] == BoolVal(self.P[s]==shapeN))
            y = proj[s]
            solver.add(Y[x] == IntVal(y))
        a = Int('a')
        b = Int('b')
        x = BitVec('x', width)
        thm = ForAll(x,
            Implies(Q[x],
            Y[x] == (BV2Int(x)*a + b)))
        solver.add(thm)
        result = solver.check()
        if result != sat:
            raise Error()
        m = solver.model()
        return repr(opSensitivity), m.eval(a).as_long(), m.eval(b).as_long()


    def variableSlice(self, full):
        l = [('1' if full[31-i] else '0') for i in self.varBitPositions]
        return ''.join(l)

    def isRegular(self):
        return len(self.shapes)==1

    def computeVarBitPositions(self):
        self.varBitPositions = varBitPositionsFrom(self.spec, [], 31)
        self.varBitPositions.sort()
        self.varBitPositions.reverse()
        self.entropy = len(self.varBitPositions)

    @property
    def section(self):
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
