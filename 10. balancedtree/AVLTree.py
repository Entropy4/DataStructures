from collections import deque

class AVLTree:
    class Node:
        def __init__(self, value):
            # The value/data contained within the node.
            self.value = value
            # 'bf' is short for Balance Factor
            self.bf = 0
            # The height of this node in the tree.
            self.height = 0
            # The left and the right children of this node.
            self.left = None
            self.right = None
        def __str__(self):
            return str(self.value)
    
    def __init__(self):
        # The root node of the AVL tree.
        self.root = None
        # Tracks the number of nodes inside the tree.
        self.node_count = 0
    
    # The height of a rooted tree is the number of edges between the tree's
    # root and its furthest leaf. This means that a tree containing a single
    # node has a height of 0.
    def height(self) -> int:
        if self.root is None: return 0
        return self.root.height
    
    # Returns the number of nodes in the tree.
    def size(self) -> int:
        return self.node_count
    
    # Returns whether or not the tree is empty.
    def isEmpty(self) -> bool:
        return self.size() == 0
    
    # Return true/false depending on whether a value exists in the tree.
    def contains(self, value) -> bool:
        return self.containsIn(self.root, value)
    
    # Recursive contains helper method.
    def containsIn(self, node:Node, value) -> bool:
        if node is None: return False
        # Dig into left subtree.
        if value < node.value: return self.containsIn(node.left, value)
        # Dig into right subtree.
        if value > node.value: return self.containsIn(node.right, value)
        # Found value in tree.
        return True
    
    # Insert/add a value to the AVL tree. The value must not be null, O(log(n))
    def insert(self, value) -> bool:
        if value is None: return False
        if not self.containsIn(self.root, value):
            self.root = self.insertIn(self.root, value)
            self.node_count += 1
            return True
        return False
    
    # Inserts a value inside the AVL tree.
    def insertIn(self, node:Node, value) -> Node:
        # Base case.
        if node is None: return AVLTree.Node(value)

        # Insert node in left subtree.
        if value < node.value: 
            node.left = self.insertIn(node.left, value)
        # Insert node in right subtree.
        else:
            node.right = self.insertIn(node.right, value)

        # Update balance factor and height values.
        self.update(node)
        # Re-balance tree.
        return self.balance(node)
    
    # Update a node's height and balance factor.
    def update(self, node:Node):
        left_node_height = -1 if node.left is None else node.left.height
        right_node_height = -1 if node.right is None else node.right.height
        
        # Update this node's height.
        node.height = 1 + max(left_node_height, right_node_height)

        # Update this node's height.
        node.bf = right_node_height - left_node_height

    # Re-balance a node if its balance factor is +2 or -2.
    def balance(self, node:Node) -> Node:
        # Left heavy subtree.
        if node.bf == -2:
            if node.left.bf <= 0:
                return self.leftLeftCase(node)
            else:
                return self.leftRightCase(node)
            
        # Right heavy subtree needs balancing.
        elif node.bf == 2:
            if node.right.bf >= 0:
                return self.rightRightCase(node)
            else:
                return self.rightLeftCase(node)
            
        # Node either has a balance factor of 0, +1 or -1 which is fine.
        return node

    def leftLeftCase(self, node:Node):
        return self.rightRotation(node)
    
    def leftRightCase(self, node:Node):
        node.left = self.leftRotation(node.left)
        return self.leftLeftCase(node)
    
    def rightRightCase(self, node:Node):
        return self.leftRotation(node)
    
    def rightLeftCase(self, node:Node):
        node.right = self.rightRotation(node.right)
        return self.rightRightCase(node)
    
    """----------------------------------(LEFT ROTATION DIAGRAM)------------------------------------
                (node)                                                  (new_parent)
                /    \                                                  /          \    
    left_subtree      (new_parent)                -->              (node)          right_subtree
                     /            \                               /      \  
    [new_parent.left]              right_subtree      left_subtree       [new_parent.left]
    """
    def leftRotation(self, node:Node) -> Node:
        new_parent = node.right
        node.right = new_parent.left
        new_parent.left = node
        self.update(node)
        self.update(new_parent)
        return new_parent
    
    """----------------------------------(RIGHT ROTATION DIAGRAM)------------------------------------
                            (node)                                   (new_parent)
                            /    \                                   /          \    
                (new_parent)      right_subtree     -->   left_subtree          (node)
                /          \                                                   /      \  
    left_subtree            [new_parent.right]               [new_parent.right]        right_subtree
    """
    def rightRotation(self, node:Node) -> Node:
        new_parent = node.left
        node.left = new_parent.right
        new_parent.right = node
        self.update(node)
        self.update(new_parent)
        return new_parent
    
    # Remove a value from this binary tree if it exists, O(log(n))
    def remove(self, elem) -> bool:
        if elem is None: return False

        if self.containsIn(self.root, elem):
            self.root = self.removeFrom(self.root, elem)
            self.node_count -= 1
            return True

        return False
    
    # Removes a value from the AVL tree.
    def removeFrom(self, node:Node, elem) -> Node:
        if node is None: return None
        # Dig into left subtree, the value we're looking
        # for is smaller than the current value.
        if elem < node.value: node.left = self.removeFrom(node.left, elem)
        # Dig into right subtree, the value we're looking
        # for is greater than the current value.
        elif elem > node.value: node.right = self.removeFrom(node.right, elem)
        
        # Found the node we wish to remove.
        else:

            # case with only right subtree or no subtree at all
            if node.left is None: return node.right
            # case with only left subtree or no subtree at all
            elif node.right is None: return node.left

            else:

                # Choose to remove from left subtree
                if node.left.height > node.right.height:
                    successor_value = self.findMax(node.left)
                    node.value = successor_value
                    node.left = self.removeFrom(node.left, successor_value)
                
                else:
                    successor_value = self.findMin(node.right)
                    node.value = successor_value
                    node.right = self.removeFrom(node.right, successor_value)
        
        # update and re-balance tree
        self.update(node)
        return self.balance(node)

    def findMin(self, node:Node):
        while node.left is not None: node = node.left
        return node.value
    
    def findMax(self, node:Node):
        while node.right is not None: node = node.right
        return node.value
    

    class AVLIterator:
        def __init__(self, root):
            self.st = deque()
            self.st.append(root)
            self.trav = root

        def hasNext(self):
            return len(self.st) > 0
        
        def next(self):
            # Dig left
            while self.trav is not None and self.trav.left is not None:
                self.st.append(self.trav.left)
                self.trav = self.trav.left
            
            node = self.st.pop()

            # Try moving down right once
            if node.right is not None:
                self.st.append(node.right)
                self.trav = node.right
            
            return node.value

    def traverse(self):
        return AVLTree.AVLIterator(self.root)    
   
   
    # print AVL Tree in ASCII diagram format
    def __str__(self):
        if self.root is None:
            return "(empty)"

        def build(node, prefix="", is_tail=True):
            if node is None:
                return ""
            
            result = prefix
            result += "└── " if is_tail else "├── "
            result += f"{node.value}(h={node.height},bf={node.bf})\n"

            children = []
            if node.left:
                children.append(node.left)
            if node.right:
                children.append(node.right)

            for i, child in enumerate(children):
                last = i == len(children) - 1
                extension = "    " if is_tail else "│   "
                result += build(child, prefix + extension, last)

            return result

        return build(self.root)
    


# # testing code
# def check_avl_balance(node):
#     """
#     Recursively verify AVL property:
#     - height is correct
#     - balance factor is correct
#     - |bf| <= 1
#     Returns (is_balanced, height)
#     """
#     if node is None:
#         return True, -1

#     left_ok, left_h = check_avl_balance(node.left)
#     right_ok, right_h = check_avl_balance(node.right)

#     expected_height = 1 + max(left_h, right_h)
#     expected_bf = right_h - left_h

#     node_ok = (
#         left_ok and
#         right_ok and
#         node.height == expected_height and
#         node.bf == expected_bf and
#         abs(node.bf) <= 1
#     )

#     return node_ok, expected_height


# def inorder_list(tree: AVLTree):
#     """Return elements using iterator traversal."""
#     it = tree.traverse()
#     result = []
#     while it.hasNext():
#         result.append(it.next())
#     return result


# def print_test(title):
#     print("\n" + "="*60)
#     print(title)
#     print("="*60)


# def main():
#     # ---------- Basic insertion ----------
#     print_test("Basic Insertions")
#     avl = AVLTree()
#     values = [10, 20, 30, 40, 50, 25]
#     for v in values:
#         avl.insert(v)
#         print(f"Inserted {v}")
#         print(avl)

#     print("Size:", avl.size())
#     print("Height:", avl.height())
#     print("Contains 25:", avl.contains(25))
#     print("Contains 99:", avl.contains(99))
#     balanced, _ = check_avl_balance(avl.root)
#     print("AVL balanced:", balanced)
#     print("Inorder:", inorder_list(avl))

#     # ---------- Duplicate insertion ----------
#     print_test("Duplicate Insert")
#     print("Insert 25 again:", avl.insert(25))
#     print("Size (should be unchanged):", avl.size())

#     # ---------- Rotation tests ----------
#     # LL rotation
#     print_test("LL Rotation Test")
#     ll = AVLTree()
#     for v in [30, 20, 10]:
#         ll.insert(v)
#     print(ll)
#     balanced, _ = check_avl_balance(ll.root)
#     print("AVL balanced:", balanced)

#     # RR rotation
#     print_test("RR Rotation Test")
#     rr = AVLTree()
#     for v in [10, 20, 30]:
#         rr.insert(v)
#     print(rr)
#     balanced, _ = check_avl_balance(rr.root)
#     print("AVL balanced:", balanced)

#     # LR rotation
#     print_test("LR Rotation Test")
#     lr = AVLTree()
#     for v in [30, 10, 20]:
#         lr.insert(v)
#     print(lr)
#     balanced, _ = check_avl_balance(lr.root)
#     print("AVL balanced:", balanced)

#     # RL rotation
#     print_test("RL Rotation Test")
#     rl = AVLTree()
#     for v in [10, 30, 20]:
#         rl.insert(v)
#     print(rl)
#     balanced, _ = check_avl_balance(rl.root)
#     print("AVL balanced:", balanced)

#     # ---------- Removal tests ----------
#     print_test("Removal Tests")
#     avl2 = AVLTree()
#     for v in [50, 30, 70, 20, 40, 60, 80]:
#         avl2.insert(v)
#     print("Initial tree:")
#     print(avl2)

#     # remove leaf
#     print("\nRemove leaf 20")
#     avl2.remove(20)
#     print(avl2)

#     # remove node with one child
#     print("\nRemove node with one child 30")
#     avl2.remove(30)
#     print(avl2)

#     # remove node with two children
#     print("\nRemove node with two children 70")
#     avl2.remove(70)
#     print(avl2)

#     # remove root
#     print("\nRemove root 50")
#     avl2.remove(50)
#     print(avl2)

#     print("Size:", avl2.size())
#     balanced, _ = check_avl_balance(avl2.root)
#     print("AVL balanced:", balanced)
#     print("Inorder:", inorder_list(avl2))

#     # ---------- Iterator correctness ----------
#     print_test("Iterator Sorted Order Check")
#     arr = inorder_list(avl2)
#     print("Iterator output:", arr)
#     print("Sorted:", arr == sorted(arr))

#     # ---------- Empty tree ----------
#     print_test("Empty Tree Checks")
#     empty = AVLTree()
#     print("Is empty:", empty.isEmpty())
#     print("Size:", empty.size())
#     print("Height:", empty.height())
#     print("Remove from empty:", empty.remove(10))


# if __name__ == "__main__":
#     main()
