from bitstring import Bits
from itertools import product
from z3 import *

import bit_iter

def eitherThisOr0(x):
    yield x
    yield 0

def bool2bv(b):
    return If(b, BitVecVal(1,1), BitVecVal(0,1))

def bools2bv(bs):
    bits = [bool2bv(b) for b in bs]
    return Concat(*bits)



class SensitivityList:
    def __init__(self, width):
        # 'x': irrelevant
        # '!': significant
        # '?': unknown
        self.slist = ['?']*width
        self.constructiveMask = 0

    def __repr__(self):
        return '\xAB'+''.join(list(reversed(self.slist)))+'\xBB'

    def positionsToWiggleNotIncluding(self, excludedPos):
        a = range(0, len(self.slist))
        f = filter((lambda pos: (self.slist[pos] != 'x')&(pos!=excludedPos)), a)
        return list(f)

    def decideIfDepends(self, encodingTrueBits, bitPosition, p):
        encoding = sum(encodingTrueBits) | self.constructiveMask
        twinkle = 1<<bitPosition
        x = p[encoding]
        if x==None:
            self.nextConstructiveMask = self.constructiveMask | (1<<bitPosition)
            return False
        y = p[encoding|twinkle]
        if y==None:
            # leave the constructiveMask bit at 0
            return False
        return x != y


    def probeIrrelevant(self, bitPosition):
        self.nextConstructiveMask = self.constructiveMask
        positionsToWiggle = self.positionsToWiggleNotIncluding(bitPosition)
        iters = map(lambda pos: eitherThisOr0(2**pos), positionsToWiggle)
        productIter = product(*list(iters))
        for e in productIter:
            if self.decideIfDepends(e, bitPosition, p):
                self.constructiveMask = self.nextConstructiveMask
                return False
        self.constructiveMask = self.nextConstructiveMask
        return True

    def guess(self, p):
        width = len(self.slist)
        self.solver = Solver()
        self.P = Array('P', BitVecSort(width), IntSort())
        for i in range(2**width):
            x = BitVecVal(i, width)
            y = p[i]
            self.solver.add(self.P[x] == IntVal(y))
        return self.guess1()

    def guess1(self):
        import pudb; pu.db
        bools = Bools([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        bv = bools2bv(bools)
        # PROBLEM PROBLEM PROBLEM
        # other shapes (1) don't work because there is no
        # one fixed variable assignment, so Z3 returns empty list
        shape = 0
        xxxx = self.P[bv] == IntVal(shape)

        conseq = self.solver.consequences([xxxx], bools)
        sat = conseq[0]
        fixedVars = conseq[1]
        k = 0
        v = [simplify(fixedVar.arg(1)) for fixedVar in fixedVars]

        # we work until here.


        try:
            i = self.slist.index('?')
        except ValueError:
            return self
        self.solver.push()
        x = self.probeIrrelevant(i)
        self.slist[i] = 'x' if x else '!'
        return self.guess1()

    def slLetter_to_FieldSpecElement(self, i_l):
        index, letter = i_l
        if letter=='!':
            return 1 # a variable bit
        if letter=='x':
            return '1' if self.constructiveMask&(1<<index) else '0'
        error("cant have unknown sensitivity this late")

    def f(self):
        return lambda i_l: self.slLetter_to_FieldSpecElement(i_l)

    def asFieldSpec(self):
        l = list(map(self.f(), enumerate(self.slist)))
        #l = list(map(slLetter_to_FieldSpecElement, self.slist))
        l.reverse()
        return l

    def filterRelevantMembers(self, aList):
        z = list(zip(reversed(self.slist), aList))
        relevantElems = filter((lambda rel_bit: rel_bit[0]=='!'), z)
        snd = lambda a: a[1]
        return list(map(snd, relevantElems))

    def significantSlice(self, bits):
        return Bits(self.filterRelevantMembers(bits))

    @property
    def entropy(self):
        return len(list(filter(lambda x: x=='!', self.slist)))

    def isInsensitive(self):
        return self.entropy==0

    def twoPoints(self):
        if self.isInsensitive():
            raise Error()
        fff = self.asFieldSpec()
        # WRONG!!! needs to account for constructiveMask!
        itf = bit_iter.encodingspec_to_iter(fff)
        onePoint = next(itf)
        anotherPoint=next(itf)
        oneX = self.significantSlice(onePoint).uint
        anotherX = self.significantSlice(anotherPoint).uint
        oneY = proj[onePoint.uint]                                                                                                                            


#sl = SensitivityList(3)
#g = sl.guess([1, 2, 1, 2, 1, 2, 1, 2])
