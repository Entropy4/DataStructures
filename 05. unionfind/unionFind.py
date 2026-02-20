class UnionFind:
    
    

    def __init__(self, size):
        if size <= 0: raise ValueError('Size <= 0 is not allowed')

        # Number of elements in this Union Find
        self.size_of_uf = 0

        # Tracking size of each of the component
        self.sz = []

        # id_node[i] points to parent of i, if id_node[i] = i then i is a root node
        self.id_node = []

        # Number of components in the Union Find
        self.num_components = 0

        self.size_of_uf = self.num_components = size
        
        for i in range(size):
            self.id_node.append(i)      # link to itself (self root)
            self.sz.append(1)           # each component is originally of size one
    

    # Find which component/set 'p' belongs to, takes amortized constant time
    def find(self, p) -> int:

        # Find the root of the component/set
        root = p
        while root != self.id_node[root]: root = self.id_node[root]

        # Compress the path leading back to the root (IMP)
        while p != root:
            next_node = self.id_node[p]
            self.id_node[p] = root
            p = next_node
        
        return root
    
    # # Alternatively we can do recursively:
    # def find(self, p):
    #     if p == self.id_node[p]: return p
    #     self.id_node[p] = self.find(self.id_node[p])
    #     return self.id_node[p]

    # Return whether elements 'p' and 'q' are in same component
    def connected(self, p, q) -> bool:
        return self.find(p) == self.find(q)
    
    # Return size of component 'p' belongs to
    def componentSize(self, p) -> int:
        return self.sz[self.find(p)]
    
    # Return the number of elements in this UnionFind/Disjoint set
    def size(self) -> int:
        return self.size_of_uf
    
    # Returns the number of remaining components/sets
    def components(self) -> int:
        return self.num_components
    
    # unify the components/sets containing elements 'p' and 'q'
    def unify(self, p, q):
        if self.connected(p, q): return

        root1 = self.find(p)
        root2 = self.find(q)

        # Merge smaller component into the larger one
        if self.sz[root1] < self.sz[root2]:
            self.sz[root2] += self.sz[root1]
            self.id_node[root1] = root2
            self.sz[root1] = 0
        else:
            self.sz[root1] += self.sz[root2]
            self.id_node[root2] = root1
            self.sz[root2] = 0

        # since roots found are different, we know that #(components) has decreased by one
        self.num_components -= 1

    
# testing
def main():
    print("=== Creating UnionFind with 10 elements (0–9) ===")
    uf = UnionFind(10)

    print("Initial number of components:", uf.components())
    print()

    print("=== Basic unions ===")
    uf.unify(0, 1)
    uf.unify(1, 2)
    uf.unify(3, 4)
    uf.unify(5, 6)

    print("Connected(0,2)?", uf.connected(0, 2))  # True
    print("Connected(0,3)?", uf.connected(0, 3))  # False
    print("Connected(5,6)?", uf.connected(5, 6))  # True
    print("Components after unions:", uf.components())
    print()

    print("=== Component sizes ===")
    print("Size of component containing 0:", uf.componentSize(0))  # should be 3
    print("Size of component containing 3:", uf.componentSize(3))  # should be 2
    print("Size of component containing 5:", uf.componentSize(5))  # should be 2
    print()

    print("=== Merging larger groups ===")
    uf.unify(2, 4)  # merge {0,1,2} with {3,4}
    print("Connected(0,4)?", uf.connected(0, 4))  # True
    print("New size of component containing 3:", uf.componentSize(3))  # should be 5
    print("Components now:", uf.components())
    print()

    print("=== Redundant union (should not change anything) ===")
    before = uf.components()
    uf.unify(0, 4)  # already connected
    after = uf.components()
    print("Components unchanged?", before == after)
    print()

    print("=== Chain unions to test path compression ===")
    uf.unify(7, 8)
    uf.unify(8, 9)
    print("Connected(7,9)?", uf.connected(7, 9))  # True
    print("Size of component containing 7:", uf.componentSize(7))  # should be 3
    print("Components now:", uf.components())
    print()

    print("=== Final internal state (for debugging) ===")
    print("id_node array:", uf.id_node)
    print("sz array:", uf.sz)
    print()

    print("=== Edge Case: self union ===")
    uf.unify(0, 0)  # should do nothing
    print("Connected(0,0)?", uf.connected(0, 0))  # True
    print("Components still:", uf.components())   

if __name__ == "__main__":
    main()
