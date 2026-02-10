from collections import deque

class BinarySearchTree:
    class Node:
        def __init__(self, left, right, elem):
            self.data = elem
            self.left = left
            self.right = right
    
    def __init__(self):
        # Tracks the number of nodes in this BST
        self.node_count:int = 0
        # This BST is a rooted tree so we maintain a handle on the root node
        self.root = None    # of Node type

    def sizeOf(self) -> int:
        return self.node_count
    
    def isEmpty(self) -> bool:
        return self.sizeOf() == 0
    
    # Add an element to this binary tree. Returns true 
    # if we successfully perform an insertion
    def add(self, elem) -> bool:
        if self.contains(elem): return False
        else:
            self.root = self.addTo(self.root, elem)
            self.node_count += 1
            return True
        
    # Private method to recursively add a value in the binary tree, O(log(n))
    def addTo(self, node, elem) -> Node:
        # Base case: found a leaf node
        if node is None:
            node = BinarySearchTree.Node(None, None, elem)

        else:
            # Pick a subtree to insert element
            if elem < node.data:
                node.left = self.addTo(node.left, elem)
            else:
                node.right = self.addTo(node.right, elem)
        
        return node

    # Remove a value from this binary tree if it exists, O(n)
    def remove(self, elem) -> bool:
        # does the tree actually contain the elem?
        if self.contains(elem):
            self.root = self.removeFrom(self.root, elem)
            self.node_count -= 1
            return True  
        return False
    
    # Private recursive function to remove a node from a subtree
    def removeFrom(self, node, elem) -> Node:
        # Base case: found a leaf node i.e. no removal yet?
        if node is None: return None
        
        # Dig into left subtree, the value we're looking 
        # for is smaller than the current value
        if elem < node.data:
            node.left = self.removeFrom(node.left, elem)

        # Dig into right subtree, the value we're looking 
        # for is greater than the current value
        elif elem > node.data:
            node.right = self.removeFrom(node.right, elem)
        
        # found the node we wish to remove
        else:

            # Case where only a right subtree or no subtree 
            # at all. In this situation just swap the node we 
            # wish to remove with its right child
            if node.left is None:
                return node.right
            
            # Case where only a left subtree or no subtree 
            # at all. In this situation just swap the node we 
            # wish to remove with its left child
            elif node.right is None:
                return node.left
            
            # Case where both left and right subtrees exist. In this 
            # situation the successor can be largest element in left subtree
            # or the smallest element in right subtree. Here we choose latter
            else:

                # Find the leftmost node in the right subtree
                tmp = self.findMin(node.right)

                # Swap the data
                node.data = tmp.data

                # Go into right subtree and remove the leftmost node we
                # found and swapped data with. This prevents us from having 
                # two nodes in our tree with same value
                node.right = self.removeFrom(node.right, tmp.data)
            
        return node
    
    # Helper method to find the leftmost node (which has the smallest value)
    def findMin(self, node) -> Node:
        while node.left is not None: node = node.left
        return node
    
    # Helper method to find the rightmost node (which has the largest value)
    def findMax(self, node) -> Node:
        while node.right is not None: node = node.right
        return node
    
    # returns true is the element exists in the tree
    def contains(self, elem) -> bool:
        return self.containsIn(self.root, elem)
    
    # private recursive method to find an element in the tree
    def containsIn(self, node, elem) -> bool:

        # Nase case: reached bottom, val not found
        if node is None: return False

        # Dig into the left subtree because the value we're 
        # looking for is smaller than the current value
        if elem < node.data: return self.containsIn(node.left, elem)

        # Dig into the right subtree because the value we're 
        # looking for is greater than the current value
        elif elem > node.data: return self.containsIn(node.right, elem)

        # We found the value we were looking for
        else: return True

    # Computes the height of the tree, O(n)
    def height(self) -> int:
        return self.heightOf(self.root)
    
    # Recursive helper method to compute the height of the tree
    def heightOf(self, node) -> int:
        if node is None: return 0
        return max(self.heightOf(node.left), self.heightOf(node.right)) + 1

    
    class BSTIterator:
        def __init__(self, root, order='inorder'):
            VALID_ORDERS = {'preorder', 'inorder', 'postorder', 'levelorder', 'reversed'}
            if order not in VALID_ORDERS: 
                raise ValueError('Invalid traversal order')
            
            self.st = deque()
            self.order = order
            self.st.append(root)
            self.trav = root #  if order == 'inorder' or order == 'reversed' we use this

            # preparing postorder stack beforehand
            if order == 'postorder':
                # we need another stack for this
                st2 = deque()
                while len(self.st) != 0:
                    node = self.st.pop()
                    if node is not None:
                        st2.append(node)
                        if node.left is not None: self.st.append(node.left)
                        if node.right is not None: self.st.append(node.right)
                self.st = st2
        
        def hasNext(self):
            return len(self.st) > 0
        
        def next(self):

            if self.order == 'preorder':
                node = self.st.pop()
                if node.right is not None: self.st.append(node.right)
                if node.left is not None: self.st.append(node.left)
                return node.data


            if self.order == 'inorder':
                # Dig left
                while self.trav is not None and self.trav.left is not None:
                    self.st.append(self.trav.left)
                    self.trav = self.trav.left
                
                node = self.st.pop()

                # Try moving down right once
                if node.right is not None:
                    self.st.append(node.right)
                    self.trav = node.right
                
                return node.data


            if self.order == 'postorder':
                # Work has already been done earlier to get postorder stack
                return self.st.pop().data


            if self.order == 'levelorder':
                # Poll the queue to get root, then admit L and R child into queue
                node = self.st.popleft()
                if node.left is not None: self.st.append(node.left)
                if node.right is not None: self.st.append(node.right)
                return node.data


            if self.order == 'reversed':
                # Dig right
                while self.trav is not None and self.trav.right is not None:
                    self.st.append(self.trav.right)
                    self.trav = self.trav.right
                
                node = self.st.pop()

                # Try moving down left once
                if node.left is not None:
                    self.st.append(node.left)
                    self.trav = node.left
                
                return node.data


    def traverse(self, order='inorder'):
        return BinarySearchTree.BSTIterator(self.root, order)




# testing
# def main():
#     bst = BinarySearchTree()

#     print("=== BST INITIAL STATE ===")
#     print("Empty?", bst.isEmpty())
#     print("Size:", bst.sizeOf())
#     print()

#     # ---------------- INSERT ----------------
#     values = [50, 30, 70, 20, 40, 60, 80]
#     print("Inserting values:", values)
#     for v in values:
#         print(f"Insert {v}:", bst.add(v))

#     print("\nTrying duplicate insert (30):", bst.add(30))
#     print("Size after inserts:", bst.sizeOf())
#     print("Empty?", bst.isEmpty())
#     print("Height:", bst.height())
#     print()

#     # ---------------- SEARCH ----------------
#     print("=== SEARCH TESTS ===")
#     print("Contains 40?", bst.contains(40))
#     print("Contains 100?", bst.contains(100))
#     print()

#     # ---------------- MIN / MAX ----------------
#     print("=== MIN / MAX ===")
#     print("Min value:", bst.findMin(bst.root).data)
#     print("Max value:", bst.findMax(bst.root).data)
#     print()

#     # ---------------- TRAVERSALS ----------------
#     print("=== TREE TRAVERSALS ===")

#     def print_traversal(order):
#         print(f"{order.capitalize()}:", end=" ")
#         it = bst.traverse(order)
#         while it.hasNext():
#             print(it.next(), end=" ")
#         print()

#     print_traversal('inorder')
#     print_traversal('preorder')
#     print_traversal('postorder')
#     print_traversal('levelorder')
#     print_traversal('reversed')
#     print()

#     # ---------------- REMOVE LEAF ----------------
#     print("=== REMOVE LEAF NODE (20) ===")
#     bst.remove(20)
#     print_traversal('inorder')
#     print("Size:", bst.sizeOf())
#     print()

#     # ---------------- REMOVE NODE WITH ONE CHILD ----------------
#     print("=== REMOVE NODE WITH ONE CHILD (30) ===")
#     bst.remove(30)
#     print_traversal('inorder')
#     print("Size:", bst.sizeOf())
#     print()

#     # ---------------- REMOVE NODE WITH TWO CHILDREN ----------------
#     print("=== REMOVE NODE WITH TWO CHILDREN (70) ===")
#     bst.remove(70)
#     print_traversal('inorder')
#     print("Size:", bst.sizeOf())
#     print()

#     # ---------------- REMOVE ROOT ----------------
#     print("=== REMOVE ROOT NODE (50) ===")
#     bst.remove(50)
#     print_traversal('inorder')
#     print("Size:", bst.sizeOf())
#     print("Height:", bst.height())
#     print()

#     # ---------------- FINAL STATE ----------------
#     print("=== FINAL TREE LEVEL ORDER ===")
#     print_traversal('levelorder')


# if __name__ == "__main__":
#     main()