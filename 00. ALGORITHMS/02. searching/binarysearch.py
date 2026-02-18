class BinarySearch:
    # Time complexity:  O(log(n))
    # Space complexity: O(1)        extra space; (O(log(n)) if recursive way)
    def __init__(self):
        pass

    # ---------- exact match ----------
    def search(self, ar:list, target) -> int:
        lo, hi = 0, len(ar) - 1

        while lo <= hi:
            mid = (hi + lo) // 2
            value = ar[mid]

            if value > target:
                hi = mid - 1
            elif value < target:
                lo = mid + 1
            else:
                return mid
        
        return -1

    # ---------- lower_bound ----------
    # first index i such that ar[i] >= target
    def lower_bound(self, ar: list, target) -> int:
        lo, hi = 0, len(ar)

        while lo < hi:
            mid = (lo + hi) // 2
            value = ar[mid]

            if value < target:
                lo = mid + 1
            else:
                hi = mid

        return lo

    # ---------- upper_bound ----------
    # first index i such that ar[i] > target
    def upper_bound(self, ar: list, target) -> int:
        lo, hi = 0, len(ar)

        while lo < hi:
            mid = (lo + hi) // 2
            value = ar[mid]

            if value <= target:
                lo = mid + 1
            else:
                hi = mid

        return lo

    # ---------- first occurrence ----------
    def first_occurrence(self, ar: list, target) -> int:
        idx = self.lower_bound(ar, target)
        if idx < len(ar) and ar[idx] == target:
            return idx
        return -1

    # ---------- last occurrence ----------
    def last_occurrence(self, ar: list, target) -> int:
        idx = self.upper_bound(ar, target) - 1
        if idx >= 0 and ar[idx] == target:
            return idx
        return -1


# # testing
# import random

# def main():
#     bs = BinarySearch()

#     test_arrays = [
#         [],
#         [1],
#         [1, 2, 2, 2, 3, 4],
#         [5, 10, 15, 20, 25],
#         [1, 3, 5, 7, 9],
#     ]

#     # random sorted arrays
#     for _ in range(5):
#         arr = sorted(random.randint(0, 10) for _ in range(random.randint(0, 12)))
#         test_arrays.append(arr)

#     targets = [0, 1, 2, 3, 5, 8, 10]

#     tid = 1
#     for arr in test_arrays:
#         for t in targets:
#             s = bs.search(arr, t)
#             lb = bs.lower_bound(arr, t)
#             ub = bs.upper_bound(arr, t)
#             fo = bs.first_occurrence(arr, t)
#             lo = bs.last_occurrence(arr, t)

#             # expected
#             if t in arr:
#                 ok_search = (s != -1 and arr[s] == t)
#             else:
#                 ok_search = (s == -1)
#             exp_lb = next((i for i,x in enumerate(arr) if x >= t), len(arr))
#             exp_ub = next((i for i,x in enumerate(arr) if x > t), len(arr))
#             exp_fo = exp_lb if exp_lb < len(arr) and arr[exp_lb] == t else -1
#             exp_lo = exp_ub - 1 if exp_ub-1 >= 0 and exp_ub-1 < len(arr) and arr[exp_ub-1] == t else -1

#             ok = (ok_search and lb==exp_lb and ub==exp_ub and fo==exp_fo and lo==exp_lo)

#             print(f"Test {tid}: arr={arr}, target={t}")
#             print(f"  search={s} exp={ok_search}")
#             print(f"  lower ={lb} exp={exp_lb}")
#             print(f"  upper ={ub} exp={exp_ub}")
#             print(f"  first ={fo} exp={exp_fo}")
#             print(f"  last  ={lo} exp={exp_lo}")
#             print("  PASS" if ok else "  FAIL", "\n")

#             tid += 1

# if __name__ == "__main__":
#     main()


