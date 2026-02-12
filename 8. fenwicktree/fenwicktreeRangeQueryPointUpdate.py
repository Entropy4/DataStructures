import copy

class fenwickTreeRangeQueryPointUpdate:
    def __init__(self, values:list):
        # values must be a 1-indexed input array i.e. 0th index must be unused
        if values is None: raise Exception('Values array cannot be None')

        self.N = len(values)
        values[0] = 0           # why?
        # Make a clone of the values array since we manipulate
        # the array in place destroying all its original content.
        self.tree = copy.deepcopy(values)

        # Linear construction of fenwick tree
        for i in range(1, self.N+1):
            parent = i + self.lsb(i)
            if parent < self.N: self.tree[parent] += self.tree[i]
    
    # Returns the value of the least significant bit (LSB)
    # lsb(108) = lsb(0b1101100) =     0b100 = 4
    # lsb(104) = lsb(0b1101000) =    0b1000 = 8
    # lsb(96)  = lsb(0b1100000) =  0b100000 = 32
    # lsb(64)  = lsb(0b1000000) = 0b1000000 = 64
    def lsb(self, i:int) -> int:
        # Isolates the lowest one bit value
        return i & -i
    
    # Computes the prefix sum from [1, i], O(log(n))
    def prefixSum(self, i:int):
        p_sum = 0
        while i != 0:
            p_sum += self.tree[i]
            i &= ~self.lsb(i)       # Alternatively, i -= lsb(i)
        return p_sum
    
    # Returns the sum of the interval [left, right], O(log(n))
    def rangeSum(self, left:int, right:int):
        if right<left: raise ValueError("Make sure Right > Left")
        return self.prefixSum(right) - self.prefixSum(left - 1)
    
    # Get the value at index i
    def get(self, i:int):
        return self.rangeSum(i, i)
    
    # Add 'v' to index 'i', O(log(n))
    def add(self, i:int, v):
        while i < self.N:
            self.tree[i] += v
            i += self.lsb(i)
    
    # Set index i to be equal to v, O(log(n))
    def set(self, i:int, v):
        self.add(i, v - self.rangeSum(i, i))

    def __str__(self):
        return str(self.tree)


# # testing
# def main():
#     print("=== Fenwick Tree Test ===")

#     # IMPORTANT: Fenwick tree is 1-indexed.
#     # So we insert dummy 0 at index 0.
#     values = [0, 3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    
#     # Keep brute-force reference copy
#     reference = values.copy()

#     ft = fenwickTreeRangeQueryPointUpdate(values)

#     print("Initial values:", values)
#     print("Initial Tree:", ft)

#     # ---------------- PREFIX SUM TEST ----------------
#     print("\nTesting prefix sums...")
#     for i in range(1, len(reference)):
#         expected = sum(reference[1:i+1])
#         actual = ft.prefixSum(i)
#         print(f"prefixSum({i}) = {actual}, expected = {expected}")
#         assert actual == expected

#     # ---------------- RANGE SUM TEST ----------------
#     print("\nTesting range sums...")
#     test_ranges = [(1,3), (2,5), (4,10), (1,10), (6,6)]
    
#     for l, r in test_ranges:
#         expected = sum(reference[l:r+1])
#         actual = ft.rangeSum(l, r)
#         print(f"rangeSum({l},{r}) = {actual}, expected = {expected}")
#         assert actual == expected

#     # ---------------- GET TEST ----------------
#     print("\nTesting get()...")
#     for i in range(1, len(reference)):
#         expected = reference[i]
#         actual = ft.get(i)
#         print(f"get({i}) = {actual}, expected = {expected}")
#         assert actual == expected

#     # ---------------- ADD TEST ----------------
#     print("\nTesting add()...")
#     ft.add(3, 5)
#     reference[3] += 5

#     ft.add(7, -2)
#     reference[7] -= 2

#     for i in range(1, len(reference)):
#         assert ft.get(i) == reference[i]

#     print("Add updates verified.")

#     # ---------------- SET TEST ----------------
#     print("\nTesting set()...")
#     ft.set(5, 20)
#     reference[5] = 20

#     ft.set(1, -4)
#     reference[1] = -4

#     for i in range(1, len(reference)):
#         assert ft.get(i) == reference[i]

#     print("Set updates verified.")

#     # ---------------- FINAL RANGE CHECK ----------------
#     print("\nFinal full validation...")
#     for l in range(1, len(reference)):
#         for r in range(l, len(reference)):
#             expected = sum(reference[l:r+1])
#             actual = ft.rangeSum(l, r)
#             assert actual == expected

#     print("🎉 All tests passed successfully!")


# if __name__ == "__main__":
#     main()