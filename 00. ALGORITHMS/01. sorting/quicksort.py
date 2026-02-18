class QuickSort:
    def __init__(self):
        pass

    def sort(self, ar:list):
        if ar is None: return
        self.quicksort(ar, 0, len(ar) - 1)

    # Sort interval [lo, hi] inplace recursively
    def quicksort(self, ar:list, lo:int, hi:int):
        if lo < hi:
            pivot = self.partition(ar, lo, hi)
            self.quicksort(ar, lo, pivot)
            self.quicksort(ar, pivot + 1, hi)
    
    # Performs Hoare partition algorithm for quicksort
    def partition(self, ar:list, lo:int, hi:int) -> int:
        pivot = ar[lo]
        i = lo - 1
        j = hi + 1
        while True:

            while True:
                i += 1
                if ar[i] >= pivot: break

            while True:
                j -= 1
                if ar[j] <= pivot: break

            if i < j: self.swap(ar, i, j)
            else: return j
    
    def swap(self, ar:list, i:int, j:int):
        tmp = ar[i]
        ar[i] = ar[j]
        ar[j] = tmp
