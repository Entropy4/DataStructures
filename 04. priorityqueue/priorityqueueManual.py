class BinaryHeapManual:

    def __init__(self, elems=None):
        if elems is not None:
            self.heap = elems
            heapSize = len(self.heap)

            # Heapify process, O(n)
            for i in range(max(0, heapSize//2 - 1), -1, -1):
                self.sink(i)
        else:
            self.heap = []
                
    def isEmpty(self) -> bool: # O(1)
        return self.size() == 0
    
    def clear(self):
        self.heap.clear()

    def size(self) -> int: # O(1)
        return len(self.heap)
    
    def peek(self): # O(1)
        if self.isEmpty(): return None
        return self.heap[0]
    
    # Removes root of heap, O(log(n))
    def poll(self):
        return self.removeAt(0)
    
    # Test if element is present in PQueue, O(n)
    def contains(self, elem):
        for data in self.heap:
            if data == elem:
                return True
        return False
    
    # add element to Priority Queue, O(log(n))
    def add(self, elem):
        if elem is None: raise ValueError('Cannot add NoneType to heap')

        self.heap.append(elem)
        self.swim(self.size() - 1)

    # Test if value at node i <= node j, O(1); assumes i and j are valid indices
    def less(self, i:int, j:int) -> bool:
        return self.heap[i] <= self.heap[j]
    
    # Perform bottom-up node swim, O(log(n))
    def swim(self, k):

        # Grab index of parent of k-th node
        parent = (k-1)//2

        # Keep swimming while we havent reached root and while we are less than parent
        while k>0 and self.less(k, parent):
            self.swap(parent, k)    # exchange k with parent
            k = parent              
            parent = (k-1)//2       # find index of next parent node wrt. k
        
    # Top-down node sink, O(log(n))
    def sink(self, k):
        heapSize = self.size()
        while True:
            left = 2 * k + 1    # left node
            right = 2 * k + 2   # right node
            smallest = left     # assume left node is the smallest of the two children

            # which is actually smaller, L or R? If R, update accordingly
            # if R is Out-Of-Bounds then the second condition wont be checked for
            if right < heapSize and self.less(right, left): smallest = right

            # if we are outside the bounds of tree, or if we cannot sink anymore, stop earlu
            if left >= heapSize or self.less(k, smallest): break

            # move down the tree following the smallest node
            self.swap(smallest, k)
            k = smallest
    # Swap two nodes, O(1); assumes i and j are valid indices
    def swap(self, i, j):
        e_i = self.heap[i]
        e_j = self.heap[j]

        self.heap[i] = e_j
        self.heap[j] = e_i
    
    # Removes a particular element in the heap, O(n)
    def remove(self, elem):
        if elem is None: return False
        for i in range(len(self.heap)):
            if self.heap[i] == elem:
                self.removeAt(i)
                return True
        return False
    
    # Removes a node at particular index, O(log(n))
    def removeAt(self, i):
        if self.isEmpty(): return None

        index_last = self.size() - 1
        removed_data = self.heap[i]
        self.swap(i, index_last)

        # Obliterate the value
        self.heap.pop()

        if i == index_last: return removed_data
        elem = self.heap[i]

        # try sinking element
        self.sink(i)

        #if sinking didnt work, try swimming
        if self.heap[i] == elem: self.swim(i)
        return removed_data
    

# Testing
def main():
    print("=== Creating heap with initial elements ===")
    initial = [5, 3, 8, 1, 2, 7]
    heap = BinaryHeapManual(initial)
    print("Initial heap array:", heap.heap)
    print("Peek (min element):", heap.peek())
    print("Size:", heap.size())
    print()

    print("=== Adding elements ===")
    heap.add(0)
    heap.add(6)
    print("Heap after adding 0 and 6:", heap.heap)
    print("Peek:", heap.peek())
    print()

    print("=== Contains check ===")
    print("Contains 7?", heap.contains(7))
    print("Contains 42?", heap.contains(42))
    print()

    print("=== Polling elements (should come out in sorted order) ===")
    while not heap.isEmpty():
        print("Polled:", heap.poll(), "| Heap now:", heap.heap)
    print()

    print("=== Testing remove(elem) ===")
    heap2 = BinaryHeapManual([10, 4, 15, 20, 0, 8])
    print("Heap2 initial:", heap2.heap)
    heap2.remove(15)
    print("After removing 15:", heap2.heap)
    heap2.remove(0)
    print("After removing 0 (root):", heap2.heap)
    print()

    print("=== Testing removeAt(index) ===")
    heap3 = BinaryHeapManual([9, 3, 6, 2, 8, 5])
    print("Heap3 initial:", heap3.heap)
    removed = heap3.removeAt(2)
    print(f"Removed element at index 2 ({removed}):", heap3.heap)
    print()

    print("=== Clearing heap ===")
    heap3.clear()
    print("Heap3 after clear:", heap3.heap)
    print("Is empty?", heap3.isEmpty())


if __name__ == "__main__":
    main()


