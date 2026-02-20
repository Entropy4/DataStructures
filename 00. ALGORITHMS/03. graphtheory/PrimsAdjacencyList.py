import heapq

class PrimsAdjacencyList:
    # This is the lazy version: we may add redundant edges 
    # that point to within the MST itself. For eager version,
    # use a D-ary Heap and update the values in heap when required
    # Time complexity:      O(Elog(E))     
    # Space complexity:     O(V + E)

    # To break ties (minimum edge cost) in the heap, we keep a 
    # global counter to indicate their order of entering the heap
    _counter = 0

    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost
    
    def __init__(self, graph:list):
        self.n = len(graph)
        self.graph = graph

        self.solved = False
        self.mst_exists = False
        self.visited = []
        self.pq = []

        self.min_cost_sum = 0
        self.mst_edges = []

    def getMst(self) -> list|None:
        self.solve()
        return self.mst_edges if self.mst_exists else None
    
    def getMstCost(self) -> float:
        self.solve()
        return self.min_cost_sum if self.mst_exists else None
    
    def addEdgesToHeap(self, curr_node_idx:int):
        self.visited[curr_node_idx] = True

        # edges will never be null if the createEmptyGraph method was used to build the graph.
        edges = self.graph[curr_node_idx]
        for edge in edges:
            dest_node_idx = edge.to
            # You cannot get an MST by revisiting
            # a node you have already visited before.
            if self.visited[dest_node_idx]: continue
            heapq.heappush(self.pq, (edge.cost, self._counter, edge))
            self._counter += 1


    # Computes the minimum spanning tree and minimum spanning tree cost.
    def solve(self):
        if self.solved: return
        self.solved = True

        m, edge_count = self.n - 1, 0
        self.pq = []
        self.visited = [False] * self.n
        self.mst_edges = [None] * m         # will store m Edge-type objects

        # Add initial set of edges to the priority queue starting at node 0.
        self.addEdgesToHeap(0)

        # Loop while the MST is not complete.
        while self.pq and edge_count != m:
            _, _, edge = heapq.heappop(self.pq)
            # Skip any edge pointing to an already visited node.
            if self.visited[edge.to]: continue

            self.mst_edges[edge_count] = edge
            self.min_cost_sum += edge.cost
            edge_count += 1

            self.addEdgesToHeap(edge.to)
        
        self.mst_exists = (edge_count == m)


    # ---------------------GRAPH RELATED------------------------------

    # Initialize an empty adjacency list that can hold up to n nodes.
    def createEmptyGraph(self, n:int) -> list:
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
    

# testing
def main():
    print("=== Prim's MST (Lazy) Test Driver ===\n")

    # Pretty print MST
    def print_mst(prim):
        mst = prim.getMst()
        cost = prim.getMstCost()

        if mst is None:
            print("MST does not exist (graph disconnected)")
            return

        print("MST cost =", cost)
        print("Edges:")
        for e in mst:
            print(f"{e.fro} --({e.cost})--> {e.to}")
        print()

    # Single test helper
    def run_test(name, graph, expected_cost=None, expect_exists=True):
        print(f"[{name}]")
        prim = PrimsAdjacencyList(graph)
        mst = prim.getMst()
        cost = prim.getMstCost()

        if not expect_exists:
            print("Expected: No MST")
            print("Result  :", "No MST" if mst is None else "MST FOUND ❌")
            print()
            return

        print("MST cost =", cost)
        if expected_cost is not None:
            print("Cost OK =", cost == expected_cost)

        print("Edges:")
        for e in mst:
            print(f"{e.fro} --({e.cost})--> {e.to}")
        print()

    # Graph builder
    builder = PrimsAdjacencyList([])

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
    # Test 2: Another connected graph
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

    # MST edges = 4 (n-1)
    run_test("Unweighted graph", g6, expected_cost=4)


if __name__ == "__main__":
    main()
