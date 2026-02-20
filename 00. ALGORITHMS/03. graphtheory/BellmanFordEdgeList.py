# An implementation of the Bellman-Ford algorithm. The algorithm finds the shortest path between a
# starting node and all other nodes in the graph. The algorithm also detects negative cycles.
class BellmanFordEdgeList:
    # Time complexity:      O(E * V)
    # Space complexity:     O(V)
    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost

    def bellmanFord(edges:list[Edge], V:int, start:int) -> list[float|int]:
        dist = [float('inf')] * V
        dist[start] = 0

        # Only in the worst case does it take V-1 iterations for the Bellman-Ford
        # algorithm to complete. Another stopping condition is when we're unable to
        # relax an edge, this means we have reached the optimal solution early.
        relaxedAnEdge = True
        # For each vertex, apply relaxation for all the edges
        for num_hops in range(V-1):     # indicates increasing no. of allowed hops
            if not relaxedAnEdge: break
            relaxedAnEdge = False
            for edge in edges:
                if dist[edge.fro] + edge.cost < dist[edge.to]:
                    dist[edge.to] = dist[edge.fro] + edge.cost
                    relaxedAnEdge = True
        
        # Run algorithm a second time to detect which nodes are part
        # of a negative cycle. A negative cycle has occurred if we
        # can find a better path beyond the optimal solution.
        relaxedAnEdge = True
        for num_hops in range(V-1):     # indicates increasing no. of allowed hops
            if not relaxedAnEdge: break
            relaxedAnEdge = False
            for edge in edges:
                if dist[edge.fro] + edge.cost < dist[edge.to]:
                    dist[edge.to] = float('-inf')
                    relaxedAnEdge = True

        # Return the array containing the shortest distance to every node
        return dist
    
# testing
def main():
    E, V, start = 10, 9, 0
    edges = [None] * E
    edges[0] = BellmanFordEdgeList.Edge(0, 1, 1)
    edges[1] = BellmanFordEdgeList.Edge(1, 2, 1)
    edges[2] = BellmanFordEdgeList.Edge(2, 4, 1)
    edges[3] = BellmanFordEdgeList.Edge(4, 3, -3)
    edges[4] = BellmanFordEdgeList.Edge(3, 2, 1)
    edges[5] = BellmanFordEdgeList.Edge(1, 5, 4)
    edges[6] = BellmanFordEdgeList.Edge(1, 6, 4)
    edges[7] = BellmanFordEdgeList.Edge(5, 6, 5)
    edges[8] = BellmanFordEdgeList.Edge(6, 7, 4)
    edges[9] = BellmanFordEdgeList.Edge(5, 7, 3)

    print('OK')
    d = BellmanFordEdgeList.bellmanFord(edges, V, start)
    for i in range(V):
        print(f"The cost to get from node {start} to {i} is {d[i]}")
    
    # Output:
    # The cost to get from node 0 to 0 is 0.00
    # The cost to get from node 0 to 1 is 1.00
    # The cost to get from node 0 to 2 is -Infinity
    # The cost to get from node 0 to 3 is -Infinity
    # The cost to get from node 0 to 4 is -Infinity
    # The cost to get from node 0 to 5 is 5.00
    # The cost to get from node 0 to 6 is 5.00
    # The cost to get from node 0 to 7 is 8.00
    # The cost to get from node 0 to 8 is Infinity

if __name__ == "__main__":
    main()