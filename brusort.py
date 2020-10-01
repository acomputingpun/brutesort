class ComparisonMapping():
    def __init__(self, length):
        self.length = length
        self.matrix = []
        self.reverseMatrix = []
        for k in range (0, length):
            self.reverseMatrix.append([])
            for j in range(k+1, length):
                self.reverseMatrix[-1].append( len(self.matrix) )
                self.matrix.append( (k, j) )

    def pairToBindex(self, pair):
        return self.reverseMatrix[pair[0]][pair[1]-pair[0]-1]

    def bindexToPair(self, bindex):
        return self.matrix[bindex]

class PermutationMapping():
    def __init__(self, presets):
        self.presets = presets

    @property
    def cMapping(self):
        return self.presets.cMapping

    @property
    def length(self):
        return self.cMapping.length

    @property
    def indices(self):
        yield from range(self.length)

    def rCreate(self, ordering):
        if len(ordering) == self.length:
            yield ordering

        for index in self.indices:
            if index not in ordering:
                if (self.presets.isValidAddition(ordering, index)):
                    yield from self.rCreate( [*ordering, index] )

class ComparisonSet():
    def __init__(self, cMapping):
        self.cMapping = cMapping
        self.matrix = {}

    def appendBindex(self, bindex, ordering):
        self.matrix[bindex] = ordering
    def appendPair(self, pair):
        if (pair[0] < pair[1]):
            reversed = False
            bindex = self.cMapping.pairToBindex( pair )
        else:
            reversed = True
            bindex = self.cMapping.pairToBindex( (pair[1], pair[0]) )
        self.appendBindex(bindex, reversed)

    def isValidAddition(self, ordering, addition):
        for index in ordering:
            if index < addition:
                reversed = False
                bindex = self.cMapping.pairToBindex( (index, addition) )
            else:
                reversed = True
                bindex = self.cMapping.pairToBindex( (addition, index) )

            if bindex not in self.matrix:
                continue
            else:
                if self.matrix[bindex] != reversed:
                    return False
        return True


    def isValid(self, ordering ):
        print("Ordering is", ordering)
        for (pos, k) in enumerate(ordering):
            for j in ordering[pos+1:]:
                print("  Testing", (k, j))
                if (k < j):
                    reversed = False
                    bindex = self.cMapping.pairToBindex( (k, j) )
                else:
                    reversed = True
                    bindex = self.cMapping.pairToBindex( (j, k) )

                print("  done lookup", (k, j), "- got bindex", bindex)

                if bindex not in self.matrix:
                    continue
                else:
                    if bool(self.matrix[bindex]) != bool(reversed):
                        return False
        return True

class Ordering():
    def __init__(self, cMapping):
        self.cMapping = cMapping
        self.indices = []

    def isComplete(self):
        return self.length == self.cMapping.length

    @property
    def length(self):
        return len(self.indices)

    def containsPair(self, pair):
        return self.doPairComparison(pair) is not None

    def doPairComparison(self, pair):
        found = []
        for index in self.indices:
            if index in pair:
                found.append(index)

        if pair == (found[0], found[1]):
            return 1
        if pair == (found[1], found[0]):
            return -1
        else:
            return None

    def doBindexComparison(self, bindex):
        return self.doPairComparison( self.cMapping.bindexToPair(bindex) )

cmap = ComparisonMapping( 11 )

presets = ComparisonSet(cmap)

presets.appendPair( (0, 1) )
presets.appendPair( (1, 2) )
presets.appendPair( (2, 3) )
presets.appendPair( (3, 4) )

presets.appendPair( (5, 6) )
presets.appendPair( (6, 7) )
presets.appendPair( (7, 8) )
presets.appendPair( (8, 9) )
presets.appendPair( (9, 10) )

pmap = PermutationMapping( presets )

print ( len([k for k in pmap.rCreate([])]) )
