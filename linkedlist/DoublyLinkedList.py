"""
A doubly linked list implementation.

@author me
"""
class DoublyLinkedList:
    size_of_list: int = 0
    head = None
    tail = None

    def __init__(self):
        pass

    # Internal node class to represent data
    class Node:
        data = None
        prev = None         # Node class
        next = None          # Node class

        def __init__(self, data, prev=None, next=None):
            self.data = data
            self.prev = prev
            self.next = next

        def __str__(self):
            return f"{self.data}"


    # Empty this linked list, O(n)
    def clear(self):
        trav = self.head
        while (trav != None):
            next = trav.next
            trav.prev = trav.next = None
            trav = next
        self.head = self.tail = trav = None
        self.size_of_list = 0
    
    
    # Return size of linked list
    def sz(self) -> int:
        return self.size_of_list
    

    # Is the Linked list empty?
    def isEmpty(self) -> bool:
        return self.sz() == 0
    

    # Add an element to tail of linked list, O(1)
    def add(self, elem):
        self.addLast(elem)

    # Add a node to tail of linked list, O(1)
    def addLast(self, elem):
        if self.isEmpty():
            self.head = self.tail = self.Node(elem, None, None)
        else:
            self.tail.next = self.Node(elem, self.tail, None)
            self.tail = self.tail.next
        self.size_of_list += 1

    # Add an element to the beginning of linked list, O(1)
    def addFirst(self, elem):
        if self.isEmpty():
            self.head = self.tail = self.Node(elem, None, None)
        else:
            self.head.prev = self.Node(elem, None, self.head)
            self.head = self.head.prev
        self.size_of_list += 1

    # Add an element at a specified index, O(n)
    def addAt(self, index: int, data):
        if index < 0 or index > self.size_of_list: raise ValueError('Illegal Index')
        if index == 0:
            self.addFirst(index)
            return
        if index == self.size_of_list:
            self.addLast(index)
            return
        
        temp = self.head
        for i in range(0, index - 1):
            temp = temp.next
        newNode = self.Node(data, temp, temp.next)
        temp.next.prev = newNode
        temp.next = newNode

        self.size_of_list += 1

    # Check value of first node if it exists, O(1)
    def peekFirst(self):
        if self.isEmpty(): raise Exception('Empty list')
        return self.head.data
    
    # Check value of last node if it exists, O(1)    
    def peekLast(self):
        if self.isEmpty(): raise Exception('Empty list')
        return self.tail.data
    
    # Remove the first value at the head of linked list, O(1)
    def removeFirst(self): # returns data
        # Can't remove data from an empty list
        if self.isEmpty(): raise Exception('Empty list')    

        # Extract data at the head and move the head pointer forwards one node
        data = self.head.data
        self.head = self.head.next
        self.size_of_list -= 1

        # If the list is empty set the tail to null
        if self.isEmpty(): self.tail = None

        # Do a memory cleanup of the previous node
        else: self.head.prev = None

        # Return the data that was at the first node we just removed
        return data
    
    # Remove the last value at the tail of the linked list, O(1)
    def removeLast(self): # returns data
        # Can't remove data from an empty list
        if self.isEmpty(): raise Exception('Empty list')  

        # Extract data at the tail and move the tail pointer backwards one node
        data = self.tail.data
        self.tail = self.tail.prev
        self.size_of_list -= 1

        # If the list is now empty set the head to null
        if self.isEmpty(): self.head = None
        
        # Do a memory cleanup of the previous node
        else: self.tail.next = None

        # Return the data that was at the first node we just removed
        return data
    
    # Remove an arbitrary node from linked list, O(1)
    def removeNode(self, node: Node): # returns data
        if node.prev is None: return self.removeFirst()
        if node.next is None: return self.removeLast()

        # Make the pointers of adjacent nodes skip over 'node'
        node.next.prev = node.prev
        node.prev.next = node.next

        # Temporarily store the data we want to return
        data = node.data

        # Memory cleanup
        node.data = None
        node.prev = node.next = node = None     # left to right assignment

        self.size_of_list -= 1

        # Return the data in the node we just removed
        return data
    
    # Remove a node at a particular index, O(n)
    def removeAt(self, index: int): # returns data
        # Make sure the index provided is valid
        if index < 0 or index >= self.size_of_list: raise ValueError('Illegal Index')

        i = 0
        trav = None

        if index < int(self.size_of_list / 2):
           trav = self.head
           for i in range(0, index + 1):
               trav = trav.next
        else:
            trav = self.tail
            for i in range(self.size_of_list - 1, index, -1):
                trav = trav.prev
        return self.removeNode(trav)
    
    # Remove a particular value in the linked list, O(n)
    def remove(self, obj) -> bool:
        trav = None

        # Support searching for null
        if obj is None:
            trav = self.head
            while trav is not None:
                if trav.data is None: 
                    self.removeNode(trav)
                    return True
                trav = trav.next
        # Search for non null object
        else:
            trav = self.head
            while trav is not None:
                if obj == trav.data: 
                    self.removeNode(trav)
                    return True
                trav = trav.next
        return False
    
    # Find the index of a particular value in the linked list, O(n)
    def indexOf(self, obj) -> int:
        index = 0
        trav = self.head

        # Support searching for null
        if obj is None:
            while trav is not None:
                if trav.data is None: 
                    return index
                index += 1
                trav = trav.next
        # Search for non null object
        else:
            while trav is not None:
                if obj == trav.data: 
                    return index
                index += 1
                trav = trav.next
        return -1
    
    # Check is a value is contained within the linked list
    def contains(self, obj) -> bool:
        return self.indexOf(obj) != -1
    
    def __str__(self):
        s = '['
        trav = self.head
        while trav is not None:
            s += str(trav.data)
            if trav.next is not None:
                s += ', '
            trav = trav.next
        s += ']'
        return s


# # testing
# def main():
#     ls = DoublyLinkedList()
#     print(ls, ls.sz(), ls.isEmpty())
#     for i in range(0, 20, 2):
#         ls.add(i)
#         print('added ', i)
#     ls.addFirst(-1)
#     ls.addLast(22)
#     ls.addAt(11, 20)
#     print(ls.peekFirst())
#     print(ls.peekLast())
#     print(ls.sz())
#     print(ls)

#     print(ls.removeFirst())
#     print(ls.removeLast())
#     print(ls.removeAt(5))
#     print('removed 20?', ls.remove(20))
#     print(ls)
#     print('contains 20?', ls.contains(20))
#     print(ls)
#     print("is it empty now", ls.isEmpty())
#     ls.clear()
#     print(ls)
#     print("is it empty now", ls.isEmpty())
    
# main()