class MergeSort:
    # Time complexity:  O(nlog(n))
    # Space complexity: O(n)        extra space
    def __init__(self):
        pass

    def sort(self, values:list):
        sorted_values = self.mergesort(values)
        for i in range(len(values)):
            values[i] = sorted_values[i]
    
    def mergesort(self, ar:list) -> list:
        n = len(ar)
        # Base case is when a single element (which is already sorted)
        if n <= 1: return ar

        # Split array into two parts and recursively sort them
        left = self.mergesort(ar[0:n//2])
        right = self.mergesort(ar[n//2:n])

        # Combine the two arrays into one larger array
        return self.merge(left, right)
    
    # Merge two sorted arrays into a larger sorted array
    def merge(self, ar1:list, ar2:list) -> list:
        n1 = len(ar1)
        n2 = len(ar2)
        n = n1 + n2
        i1 = 0
        i2 = 0
        ar = [0] * n

        for i in range(n):
            if i1 == n1:
                ar[i] = ar2[i2]
                i2 += 1
            elif i2 == n2:
                ar[i] = ar1[i1]
                i1 += 1
            else:
                if ar1[i1] < ar2[i2]:
                    ar[i] = ar1[i1]
                    i1 += 1
                else:
                    ar[i] = ar2[i2]
                    i2 += 1


        return ar
    


# # testing
# import random

# def main():
#     ms = MergeSort()

#     test_cases = [
#         [],                         # empty
#         [1],                        # single element
#         [5, 3, 8, 4, 2, 7, 1, 10],  # random
#         [1, 2, 3, 4, 5, 6],         # already sorted
#         [6, 5, 4, 3, 2, 1],         # reverse sorted
#         [3, 3, 3, 3],               # all equal
#         [5, 1, 3, 5, 2, 5, 4],      # duplicates
#     ]

#     # add random tests
#     for _ in range(5):
#         arr = [random.randint(0, 50) for _ in range(random.randint(0, 15))]
#         test_cases.append(arr)

#     for idx, arr in enumerate(test_cases, 1):
#         original = arr.copy()
#         ms.sort(arr)
#         expected = sorted(original)

#         print(f"Test {idx}:")
#         print("  Original :", original)
#         print("  Sorted   :", arr)
#         print("  Expected :", expected)
#         print("  PASS" if arr == expected else "  FAIL", "\n")

# if __name__ == "__main__":
#     main()