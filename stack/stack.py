from collections import deque

'''
DEQUE METHODS FOR REFERENCE

Operation	            Description	                                                                 Time Complexity
append(x)	            Adds x to the right end of the deque.	                                                O(1)
appendleft(x)	        Adds x to the left end of the deque.	                                                O(1)
pop()	                Removes and returns an element from right end of the deque.	                            O(1)
popleft()	            Removes and returns an element from left end of the deque.	                            O(1)
extend(iterable)	    Adds all elements from iterable to right end of the deque.	                            O(k)
extendleft(iterable)	Adds all elements from iterable to left end of the deque (reversed order).	            O(k)
remove(value)	        Removes the first occurrence of value from the deque. ValueError if not found.	        O(n)
rotate(n)	            Rotates the deque n steps to the right. If n negative, rotates to the left.	            O(k)
clear()	                Removes all elements from the deque.	                                                O(n)
count(value)	        Counts the number of occurrences of value in the deque.	                                O(n)
index(value)	        Returns index of the first occurrence of value in the deque. ValueError if not found.	O(n)
reverse()	            Reverses the elements of the deque in place.	                                        O(n)
'''



class Stack:

    def __init__(self, data=None): # data is iterable
        if data is None:
            self.data = deque()
        else:
            self.data = deque(data)
        return

    def size(self) -> int:
        return len(self.data)
    
    def isEmpty(self) -> bool:
        return len(self.data) == 0
    
    def push(self, elem): # O(1)
        self.data.append(elem)

    def pop(self): # pop and returns data at top, O(1)
        if len(self.data) == 0: raise Exception('Stack is empty already')
        return self.data.pop()
    
    def peek(self): # peek data at top of Stack, O(1)
        if len(self.data) == 0: raise Exception('Cannot peek empty Stack')
        return self.data[-1]       

    def __str__(self):
        s = '['
        for i in range(len(self.data)):
            s += str(self.data[i])
            if i < len(self.data) - 1:
                s += ', '
        s += '] <- top'
        return s

# # testing
# def main():
#     st1 = Stack()
#     st2 = Stack([1,2,3])
#     print(f'sizes {st1.size()}, {st2.size()}')
#     print(f'isEmpty? {st1.isEmpty()}, {st2.isEmpty()}')
#     print(st1)
#     print(st2)
#     st1.push(-1)
#     st2.pop()
#     print(f'peek st2: {st2.peek()}')
#     print(st1)
#     print(st2)

# main()

