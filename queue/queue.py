from collections import deque

class Queue:
    data = None
    max_size = 0

    def __init__(self, max_size=10, data=None):
        self.max_size = max_size
        if data is None:
            self.data = deque([], max_size)
        else:
            self.data = deque(data, max_size)
        return
    
    def size(self) -> int:
        return len(self.data)
    
    def isEmpty(self) -> bool:
        return len(self.data) == 0
    
    def isFull(self) -> bool:
        return len(self.data) == self.data.maxlen

    # admit elem to back of queue i.e. add to rear
    def offer(self, elem):
        if self.isFull(): raise RuntimeError('Queue is full')
        self.data.append(elem)

    # remove elem from front of queue i.e. remove from front
    def poll(self): # returns elem
        if self.isEmpty(): raise RuntimeError('Queue is already empty')
        return self.data.popleft()
    
    # check the elem at front of the queue
    def peek(self):
        if self.isEmpty(): raise RuntimeError('Cannot peek empty queue')
        return self.data[0]
    
    def __str__(self):
        s = 'front -> ['
        for i in range(len(self.data)):
            s += str(self.data[i])
            if i < len(self.data) - 1:
                s += ', '
        s += '] <- back'
        return s
    
# # testing
# def main():
#     q = Queue(max_size=3)

#     print("Initial queue:")
#     print(q)
#     print("Empty?", q.isEmpty())
#     print("Full?", q.isFull())
#     print()

#     print("Offering elements 10, 20, 30")
#     q.offer(10)
#     q.offer(20)
#     q.offer(30)
#     print(q)
#     print("Size:", q.size())
#     print("Empty?", q.isEmpty())
#     print("Full?", q.isFull())
#     print("Peek:", q.peek())
#     print()

#     print("Polling one element:")
#     removed = q.poll()
#     print("Removed:", removed)
#     print(q)
#     print("Size:", q.size())
#     print()

#     print("Offering element 40")
#     q.offer(40)
#     print(q)
#     print()

#     print("Polling all elements:")
#     while not q.isEmpty():
#         print("Polled:", q.poll())
#         print(q)
#     print()

#     print("Final queue:")
#     print(q)
#     print("Empty?", q.isEmpty())

#     # Uncomment these one at a time to test error cases
#     # q.poll()          # should raise RuntimeError (empty)
#     # q.peek()          # should raise RuntimeError (empty)
#     # q.offer(50)
#     # q.offer(60)
#     # q.offer(70)
#     # q.offer(80)       # should raise RuntimeError (full)

# main()
