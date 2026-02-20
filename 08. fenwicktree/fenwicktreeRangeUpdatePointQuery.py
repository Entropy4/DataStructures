import copy

class fenwickTreeRangeUpdatePointQuery:
    def __init__(self, values:list):
        # values must be a 1-indexed input array i.e. 0th index must be unused
        if values is None: raise Exception('Values array cannot be None')

        self.N = len(values)
        values[0] = 0           # why?

        # Make a clone of the values array since we manipulate
        # the array in place destroying all its original content.
        self.originalTree = copy.deepcopy(values)

        # Linear construction of fenwick tree
        for i in range(1, self.N+1):
            parent = i + self.lsb(i)
            if parent < self.N: self.originalTree[parent] += self.originalTree[i]

        # the current tree will store original Tree, PLUS any range updates
        # we make as we call updateRange(l, r, v) later on. Any range updates 
        # that affect the value at index i will be captured by prefixSum(i, currentTree)
        self.currentTree = copy.deepcopy(self.originalTree)

    # Returns the value of the least significant bit (LSB)
    # lsb(108) = lsb(0b1101100) =     0b100 = 4
    # lsb(104) = lsb(0b1101000) =    0b1000 = 8
    # lsb(96)  = lsb(0b1100000) =  0b100000 = 32
    # lsb(64)  = lsb(0b1000000) = 0b1000000 = 64
    def lsb(self, i:int) -> int:
        # Isolates the lowest one bit value
        return i & -i
    
    # Update the interval [left, right] with the value 'val', O(log(n))
    def updateRange(self, left:int, right:int, val):
        self.add(left, +val)
        self.add(right + 1, -val)
    
    # Add 'v' to index 'i' and all the ranges responsible for 'i', O(log(n))
    def add(self, i:int, v):
        while i < self.N:
            self.currentTree[i] += v
            i += self.lsb(i)
    
    # Get the value at a specific index. The logic behind this method is the
    # same as finding the prefix sum in a Fenwick tree except that you need to
    # take the difference between the current tree and the original to get
    # the point value.
    def get(self, i:int):
        return self.prefixSum(i, self.currentTree) - self.prefixSum(i - 1, self.originalTree)
    
    # Computes the prefix sum from [1, i], O(log(n))
    def prefixSum(self, i:int, tree:list):
        p_sum = 0
        while i != 0:
            p_sum += tree[i]
            i &= ~self.lsb(i)   # Alternatively, i -= lsb(i)
        return p_sum

    def __str__(self):
        return f"Current Tree: {self.currentTree} \nOriginal Tree: {self.originalTree}"


# testing
def main():
    print("=== Fenwick Tree (Range Update, Point Query) Test ===")

    # 1-indexed input array
    values = [0, 5, 3, 7, 9, 6, 2, 1, 8]
    reference = values.copy()

    ft = fenwickTreeRangeUpdatePointQuery(values)

    print("Initial structure:")
    print(ft)
    print()

    # ---------------- INITIAL GET TEST ----------------
    print("Testing initial point queries...")
    for i in range(1, len(reference)):
        assert ft.get(i) == reference[i]
        print(f"get({i}) = {ft.get(i)}")
    print("Initial values verified.\n")

    # ---------------- RANGE UPDATE TEST ----------------
    print("Applying range updates...")

    updates = [
        (2, 5, 10),   # add 10 to indices 2..5
        (1, 3, -2),   # subtract 2 from 1..3
        (4, 8, 7),    # add 7 to 4..8
        (6, 6, -5)    # subtract 5 from index 6
    ]

    for l, r, v in updates:
        print(f"updateRange({l}, {r}, {v})")
        ft.updateRange(l, r, v)
        for i in range(l, r+1):
            reference[i] += v

    print()

    # ---------------- VERIFY POINT QUERIES ----------------
    print("Verifying point queries after updates...")
    for i in range(1, len(reference)):
        actual = ft.get(i)
        expected = reference[i]
        print(f"get({i}) = {actual}, expected = {expected}")
        assert actual == expected
    print("Point queries verified.\n")

    # ---------------- EDGE CASES ----------------
    print("Testing edge boundary updates...")
    ft.updateRange(1, 1, 100)
    reference[1] += 100

    ft.updateRange(len(reference)-1, len(reference)-1, -50)
    reference[-1] -= 50

    for i in range(1, len(reference)):
        assert ft.get(i) == reference[i]
    print("Edge cases verified.\n")

    print("🎉 All functional tests passed!")

if __name__ == "__main__":
    main()