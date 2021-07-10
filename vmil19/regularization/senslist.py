from itertools import product

def eitherThisOr0(x):
    yield x
    yield 0

class SensitivityList:
    def __init__(self, width):
        # 'x': irrelevant
        # '!': significant
        # '?': unknown
        self.slist = ['?']*width

    def __repr__(self):
        return '\xAB'+''.join(list(reversed(self.slist)))+'\xBB'

    def positionsToWiggleNotIncluding(self, excludedPos):
        a = range(0, len(self.slist))
        f = filter((lambda pos: (self.slist[pos] != 'x')&(pos!=excludedPos)), a)
        return list(f)

    def probeIrrelevant(self, bitPosition, p):
        positionsToWiggle = self.positionsToWiggleNotIncluding(bitPosition)
        iters = map(lambda pos: eitherThisOr0(2**pos), positionsToWiggle)
        productIter = product(*list(iters))
        for e in productIter:
            encoding = sum(e)
            twinkle = 1<<bitPosition
            good = p[encoding] == p[encoding|twinkle]
            if not good: return False
        return True

    def guess(self, p):
        try:
            i = self.slist.index('?')
        except ValueError:
            return self
        x = self.probeIrrelevant(i, p)
        self.slist[i] = 'x' if x else '!'
        return self.guess(p)

    def asFieldSpec(self):
        l = list(map(slLetter_to_FieldSpecElement, self.slist))
        l.reverse()
        return l

def slLetter_to_FieldSpecElement(slLetter):
    if slLetter=='x':
        return '0'
    if slLetter=='!':
        return 1
    error("cant have unknown sensitivity this late")

#sl = SensitivityList(3)
#g = sl.guess([1, 2, 1, 2, 1, 2, 1, 2])
