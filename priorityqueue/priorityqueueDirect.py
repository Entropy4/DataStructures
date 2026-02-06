import heapq

'''
use '_max' suffix on heapq functions for MaxHeap equivalents

HEAPQ METHODS FOR REFERENCE

Method 	                            Time Complexity     Description	
heapify(x)	                        O(n)                Transforms list x into a heap, in-place.	
heappush(heap, item)	            O(log n)            Pushes item onto the heap while maintaining the heap invariant.
heappop(heap)	                    O(log n)            Pops and returns the smallest item from the heap, maintaining the invariant.	
heappushpop(heap, item)	            O(log n)            Pushes item onto the heap then pops the smallest item. This combined action is more efficient than separate calls.	
heapreplace(heap, item)	            O(log n)            Pops and returns the smallest item, and pushes the new item. The heap size does not change.	O(log n)
nlargest(n, iterable, key=None)	    O(m + n log m) or O(m + n log k). If n is constant, it's O(m).                      Returns a list with the n largest elements from the iterable.
nsmallest(n, iterable, key=None)	O(m + n log m) or O(m + n log k). If n is constant, it's O(m).                      Returns a list with the n smallest elements from the iterable.
merge(*iterables, key=None)	        O(N log K) where N is the total elements and K is the number of iterables.          Merges multiple pre-sorted inputs into a single sorted iterator.	

'''
class BinaryHeap:
    heap: list = None

    def __init__(self, data=None): #data expected to be a list
        if data is not None:
            self.heap = data
            heapq.heapify(self.heap)
        else:
            self.heap = []
        return

    def size(self) -> int:
        return len(self.heap)
    
    def isEmpty(self) -> bool:
        return self.size() == 0
    
    def clear(self):
        self.heap.clear()

    def peek(self):
        return self.heap[0]
    
    def poll(self):
        return heapq.heappop(self.heap)
    
    def contains(self, elem):
        for data in self.heap:
            if data == elem:
                return True
            
        return False
    
    def add(self, elem):
        if elem is None: raise ValueError('cannot insert NoneType into Heap')

        heapq.heappush(self.heap, elem)

    def remove(self, elem) -> bool:
        try:
            self.heap.remove(elem)
        except ValueError:
            return False
        else:
            heapq.heapify(self.heap)
            return True
        
    def removeAt(self, index):
        if self.isEmpty(): return None
        data = self.heap.pop(index)
        heapq.heapify(self.heap)
        return data
    


# def main():
#     print("Creating empty heap")
#     h = BinaryHeap()
#     print("Empty?", h.isEmpty())
#     print("Size:", h.size())
#     print()

#     print("Adding elements: 5, 3, 8, 1, 6")
#     h.add(5)
#     h.add(3)
#     h.add(8)
#     h.add(1)
#     h.add(6)
#     print("Heap data:", h.heap)
#     print("Size:", h.size())
#     print("Empty?", h.isEmpty())
#     print("Peek (min):", h.peek())
#     print()

#     print("Polling elements (should be ascending):")
#     while not h.isEmpty():
#         print("Polled:", h.poll())
#         print("Heap:", h.heap)
#     print()

#     print("Rebuilding heap from initial data [7, 2, 9, 4, 1]")
#     h = BinaryHeap([7, 2, 9, 4, 1])
#     print("Heapified data:", h.heap)
#     print("Peek (min):", h.peek())
#     print()

#     print("Contains checks:")
#     print("Contains 4?", h.contains(4))
#     print("Contains 10?", h.contains(10))
#     print()

#     print("Removing element 4")
#     print("Removed?", h.remove(4))
#     print("Heap:", h.heap)
#     print()

#     print("Removing non-existent element 100")
#     print("Removed?", h.remove(100))
#     print("Heap:", h.heap)
#     print()

#     print("Removing element at index 0 (min)")
#     removed = h.removeAt(0)
#     print("Removed:", removed)
#     print("Heap:", h.heap)
#     print()

#     print("Clearing heap")
#     h.clear()
#     print("Heap:", h.heap)
#     print("Empty?", h.isEmpty())

#     # Uncomment to test error cases
#     # h.peek()          # IndexError on empty heap
#     # h.poll()          # IndexError on empty heap
#     # h.add(None)       # ValueError

# main()


    
