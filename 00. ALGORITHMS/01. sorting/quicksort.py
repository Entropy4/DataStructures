class QuickSort:
    # Time complexity:  O(nlog(n))
    # Space complexity: O(1)        <- inplace
    def __init__(self):
        pass

    def sort(self, ar:list):
        if ar is None: return
        self.quicksort(ar, 0, len(ar) - 1)

    # Sort interval [lo, hi] inplace recursively
    def quicksort(self, ar:list, lo:int, hi:int):
        if lo < hi:
            pivot_idx = self.partition(ar, lo, hi)
            self.quicksort(ar, lo, pivot_idx)
            self.quicksort(ar, pivot_idx + 1, hi)
    
    # Performs Hoare partition algorithm for quicksort. O(n)
    def partition(self, ar:list, lo:int, hi:int) -> int:
        # storing arbitrary pivot value at start
        pivot = ar[lo]
        i = lo - 1
        j = hi + 1
        while True:
            # keeps advancing i till it points to the first element 
            # that is bigger than our arbitrary 'pivot' element
            while True:
                i += 1
                if ar[i] >= pivot: break
            # keeps retreating j till it points to the first element 
            # that is smaller than our arbitrary 'pivot' element
            while True:
                j -= 1
                if ar[j] <= pivot: break
            # if i < j, we simply swap the two elements and let i, j move on
            if i < j: self.swap(ar, i, j)
            # i >= j, in which case we have finished partitioning.
            # the element at j is now occupying its rightful position.
            else: return j
    
    def swap(self, ar:list, i:int, j:int):
        tmp = ar[i]
        ar[i] = ar[j]
        ar[j] = tmp


# # Testing code
# import random

# def main():
#     qs = QuickSort()

#     test_cases = [
#         [],                         # empty
#         [1],                        # single element
#         [5, 3, 8, 4, 2, 7, 1, 10],  # random
#         [1, 2, 3, 4, 5, 6],         # already sorted
#         [6, 5, 4, 3, 2, 1],         # reverse sorted
#         [3, 3, 3, 3],               # all equal
#         [5, 1, 3, 5, 2, 5, 4],      # duplicates
#     ]

#     # also add some random tests
#     for _ in range(5):
#         arr = [random.randint(0, 50) for _ in range(random.randint(0, 15))]
#         test_cases.append(arr)

#     for idx, arr in enumerate(test_cases, 1):
#         original = arr.copy()
#         qs.sort(arr)
#         expected = sorted(original)

#         print(f"Test {idx}:")
#         print("  Original :", original)
#         print("  Sorted   :", arr)
#         print("  Expected :", expected)
#         print("  PASS" if arr == expected else "  FAIL", "\n")

# if __name__ == "__main__":
#     main()