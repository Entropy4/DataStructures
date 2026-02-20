# An implementation of the Bellman-Ford algorithm. The algorithm finds the shortest path between a
# starting node and all other nodes in the graph. The algorithm also detects negative cycles.
class BellmanFordAdjacencyList:
    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost
    
    def __init__(self, graph:list[list[Edge]]):
        self.n = len(graph)
        self.graph = graph
        self.dist = []

    """
    An implementation of the Bellman-Ford algorithm. The algorithm finds the shortest path between
    a starting node and all other nodes in the graph. The algorithm also detects negative cycles.
    If a node is part of a negative cycle then the minimum cost for that node is set to
    float('-inf').

   @param start - The id of the starting node
    """
    def bellmanFord(self, start:int) -> list[float|int]:
        V = self.n
        # Initialize the distance to all nodes to be infinity
        # except for the start node which is zero.
        self.dist = [float('inf')] * V
        self.dist[start] = 0

        # For each vertex, apply relaxation for all the edges
        for i in range(V-1):
            for edges in self.graph:
                for edge in edges:
                    if self.dist[edge.fro] + edge.cost < self.dist[edge.to]:
                        self.dist[edge.to] = self.dist[edge.fro] + edge.cost
        
        # Run algorithm a second time to detect which nodes are part
        # of a negative cycle. A negative cycle has occurred if we
        # can find a better path beyond the optimal solution.
        for i in range(V-1):
            for edges in self.graph:
                for edge in edges:
                    if self.dist[edge.fro] + edge.cost < self.dist[edge.to]:
                        self.dist[edge.to] = float('-inf')
        
        # Return the array containing the shortest distance to every node
        return self.dist



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
    bf = BellmanFordAdjacencyList([])

    print("TEST 1: Basic directed graph")
    g = bf.createEmptyGraph(5)
    bf.addDirectedEdge(g, 0, 1, 4)
    bf.addDirectedEdge(g, 0, 2, 2)
    bf.addDirectedEdge(g, 1, 3, 3)
    bf.addDirectedEdge(g, 2, 1, 1)
    bf.addDirectedEdge(g, 2, 3, 5)
    bf.addDirectedEdge(g, 3, 4, 1)

    solver = BellmanFordAdjacencyList(g)
    dist = solver.bellmanFord(0)
    print("Distances:", dist)
    print("Expected: [0, 3, 2, 6, 7]")
    print()

    print("TEST 2: Negative edge (no cycle)")
    g = bf.createEmptyGraph(4)
    bf.addDirectedEdge(g, 0, 1, 1)
    bf.addDirectedEdge(g, 1, 2, -1)
    bf.addDirectedEdge(g, 2, 3, -1)
    bf.addDirectedEdge(g, 0, 3, 4)

    solver = BellmanFordAdjacencyList(g)
    dist = solver.bellmanFord(0)
    print("Distances:", dist)
    print("Expected: [0, 1, 0, -1]")
    print()

    print("TEST 3: Negative cycle detection")
    g = bf.createEmptyGraph(4)
    bf.addDirectedEdge(g, 0, 1, 1)
    bf.addDirectedEdge(g, 1, 2, -1)
    bf.addDirectedEdge(g, 2, 1, -1)  # negative cycle
    bf.addDirectedEdge(g, 2, 3, 1)

    solver = BellmanFordAdjacencyList(g)
    dist = solver.bellmanFord(0)
    print("Distances:", dist)
    print("Expected: [0, -inf, -inf, -inf]")
    print()

    print("TEST 4: Unreachable nodes")
    g = bf.createEmptyGraph(5)
    bf.addDirectedEdge(g, 0, 1, 2)
    bf.addDirectedEdge(g, 1, 2, 3)
    # nodes 3,4 unreachable

    solver = BellmanFordAdjacencyList(g)
    dist = solver.bellmanFord(0)
    print("Distances:", dist)
    print("Expected: [0, 2, 5, inf, inf]")
    print()

    print("TEST 5: Undirected graph helper")
    g = bf.createEmptyGraph(3)
    bf.addUndirectedEdge(g, 0, 1, 5)
    bf.addUndirectedEdge(g, 1, 2, 2)

    solver = BellmanFordAdjacencyList(g)
    dist = solver.bellmanFord(0)
    print("Distances:", dist)
    print("Expected: [0, 5, 7]")
    print()


if __name__ == "__main__":
    main()