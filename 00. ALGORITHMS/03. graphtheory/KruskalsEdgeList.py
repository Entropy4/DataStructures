class KruskalsEdgeList:
    # An implementation of Kruskal's MST algorithm using an edge list 
    # Time Complexity: O(ElogE)

    # Union find data structure
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

    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost
    
    def __init__(self, graph:list[list[Edge]]):
        self.n = len(graph)
        self.graph = graph
        
        self.all_edges = [edge for node in graph for edge in node]
        self.mst_edges = []

    def kruskals(self) -> tuple[int|None, list|None]:
        if len(self.all_edges) == 0: return 0, []

        mst_sum = 0
        # O(m log m) to sort the edges
        self.all_edges = sorted(self.all_edges, key=lambda x: x.cost)
        uf = KruskalsEdgeList.UnionFind(self.n)

        for edge in self.all_edges:
            # Skip this edge to avoid creating a cycle in MST
            if uf.connected(edge.fro, edge.to): continue

            # Include this edge
            uf.unify(edge.fro, edge.to)
            mst_sum += edge.cost
            self.mst_edges.append(edge)

            # Optimization to stop early if we found
            # a MST that includes all the nodes
            if uf.componentSize(0) == self.n: break
        
        # Make sure we have a MST that includes all the nodes
        if uf.componentSize(0) != self.n: return None, None

        return mst_sum, self.mst_edges

     # ---------------------GRAPH RELATED------------------------------

    # Initialize an empty adjacency list that can hold up to n nodes.
    def createEmptyGraph(self, n:int) -> list[list]:
        graph = [[] for _ in range(n)]
        return graph

    # Add a directed edge from node 'u' to node 'v' with cost 'cost'.
    def addDirectedEdge(self, graph:list, u:int, v:int, cost:int):
        graph[u].append(self.Edge(u, v, cost))
    
    # Add an undirected edge between nodes 'u' and 'v'.
    def addUndirectedEdge(self, graph:list, u:int, v:int, cost:int):
        self.addDirectedEdge(graph, u, v, cost)
        self.addDirectedEdge(graph, v, u, cost)
    
    # Add an undirected unweighted edge between nodes 'u' and 'v'. The edge 
    # added will have a weight of 1 since its intended to be unweighted.
    def addUnweightedUndirectedEdge(self, graph:list, u:int, v:int):
        self.addUndirectedEdge(graph, u, v, 1)


# Test code

def main():
    print("=== Kruskal's MST Test Driver ===\n")

    def validate_mst(n, original_graph, mst_edges, expected_cost=None):
        """
        Validates MST properties:
        - edge count = n-1
        - no cycles
        - connected
        - cost matches expected (optional)
        - edges exist in original graph
        """
        if mst_edges is None:
            return False, "MST is None"

        if len(mst_edges) != n - 1:
            return False, f"Edge count incorrect: {len(mst_edges)} != {n-1}"

        # Check all edges exist in original graph
        original_edges = set()
        for u in range(n):
            for e in original_graph[u]:
                original_edges.add((e.fro, e.to, e.cost))

        for e in mst_edges:
            if (e.fro, e.to, e.cost) not in original_edges and \
            (e.to, e.fro, e.cost) not in original_edges:
                return False, "Edge not in original graph"

        # Union-Find cycle + connectivity check
        uf = KruskalsEdgeList.UnionFind(n)
        total_cost = 0

        for e in mst_edges:
            if uf.connected(e.fro, e.to):
                return False, "Cycle detected"
            uf.unify(e.fro, e.to)
            total_cost += e.cost

        if uf.componentSize(0) != n:
            return False, "Graph not connected"

        if expected_cost is not None and total_cost != expected_cost:
            return False, f"Cost mismatch {total_cost} != {expected_cost}"

        return True, "OK"

    # Pretty print MST
    def print_mst(cost, edges):
        if edges is None:
            print("MST does not exist (graph disconnected)")
            return

        print("MST cost =", cost)
        print("Edges:")
        for e in edges:
            print(f"{e.fro} --({e.cost})--> {e.to}")
        print()

    # Single test helper
    def run_test(name, graph, expected_cost=None, expect_exists=True):
        print(f"[{name}]")
        kr = KruskalsEdgeList(graph)
        cost, edges = kr.kruskals()

        if not expect_exists:
            print("Expected: No MST")
            print("Result  :", "No MST" if edges is None else "MST FOUND ❌")
            print()
            return

        print("MST cost =", cost)
        if expected_cost is not None:
            print("Cost OK =", cost == expected_cost)

        # Validate structure
        valid, msg = validate_mst(len(graph), graph, edges, expected_cost)
        print("Structure OK =", valid, f"({msg})")

        print("Edges:")
        if edges is not None:
            for e in edges:
                print(f"{e.fro} --({e.cost})--> {e.to}")
        print()

    # Graph builder
    builder = KruskalsEdgeList([])

    # -------------------------------------------------
    # Test 1: Standard connected graph
    # -------------------------------------------------
    g1 = builder.createEmptyGraph(5)
    builder.addUndirectedEdge(g1, 0, 1, 2)
    builder.addUndirectedEdge(g1, 0, 3, 6)
    builder.addUndirectedEdge(g1, 1, 2, 3)
    builder.addUndirectedEdge(g1, 1, 3, 8)
    builder.addUndirectedEdge(g1, 1, 4, 5)
    builder.addUndirectedEdge(g1, 2, 4, 7)
    builder.addUndirectedEdge(g1, 3, 4, 9)

    # Known MST cost = 16
    run_test("Connected weighted graph", g1, expected_cost=16)

    # -------------------------------------------------
    # Test 2: Small graph
    # -------------------------------------------------
    g2 = builder.createEmptyGraph(4)
    builder.addUndirectedEdge(g2, 0, 1, 1)
    builder.addUndirectedEdge(g2, 0, 2, 4)
    builder.addUndirectedEdge(g2, 1, 2, 2)
    builder.addUndirectedEdge(g2, 1, 3, 5)
    builder.addUndirectedEdge(g2, 2, 3, 3)

    # MST = 1 + 2 + 3 = 6
    run_test("Small graph", g2, expected_cost=6)

    # -------------------------------------------------
    # Test 3: Disconnected graph
    # -------------------------------------------------
    g3 = builder.createEmptyGraph(4)
    builder.addUndirectedEdge(g3, 0, 1, 1)
    builder.addUndirectedEdge(g3, 2, 3, 2)

    run_test("Disconnected graph", g3, expect_exists=False)

    # -------------------------------------------------
    # Test 4: Single node graph
    # -------------------------------------------------
    g4 = builder.createEmptyGraph(1)
    run_test("Single node", g4, expected_cost=0)

    # -------------------------------------------------
    # Test 5: Multiple valid MSTs
    # -------------------------------------------------
    g5 = builder.createEmptyGraph(4)
    builder.addUndirectedEdge(g5, 0, 1, 1)
    builder.addUndirectedEdge(g5, 0, 2, 1)
    builder.addUndirectedEdge(g5, 1, 3, 1)
    builder.addUndirectedEdge(g5, 2, 3, 1)

    # Any MST cost = 3
    run_test("Multiple MSTs", g5, expected_cost=3)

    # -------------------------------------------------
    # Test 6: Unweighted graph
    # -------------------------------------------------
    g6 = builder.createEmptyGraph(5)
    builder.addUnweightedUndirectedEdge(g6, 0, 1)
    builder.addUnweightedUndirectedEdge(g6, 0, 2)
    builder.addUnweightedUndirectedEdge(g6, 1, 3)
    builder.addUnweightedUndirectedEdge(g6, 2, 4)

    # MST edges = 4
    run_test("Unweighted graph", g6, expected_cost=4)


if __name__ == "__main__":
    main()