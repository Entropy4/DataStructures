import heapq

class DijkstrasShortestPathAdjacencyList:
    # Time complexity:      O(Elog(V))
    # Space complexity:     O(V + E)
    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost
    

    def __init__(self, graph:list):
        self.n = len(graph)
        self.graph = graph
        self.dist = []
        self.prev = []
    
    """
    Reconstructs the shortest path (of nodes) from 'start' to 'end' inclusive.

    @return An array of nodes indexes of the shortest path from 'start' to 'end'. If 'start' and
    'end' are not connected then an empty array is returned.
    """
    def reconstructPath(self, start:int, end:int) -> list:
        dist = self.dijkstra(start, end)
        path = []
        if dist == float('inf'): return path
        
        at = end
        while at is not None:
            path.append(at)
            at = self.prev[at]
        path.reverse()
        return path

    """
    Reconstruct shortest paths from 'start' to all vertices.

    @return A list where paths[v] is the shortest path from start to v.
            If v is unreachable, paths[v] = [].
    """
    def reconstructAllPaths(self, start:int) -> list:
        self.dijkstraAll(start)
        all_paths = [[] for _ in range(self.n)]

        for v in range(self.n):
            # if dist[v] is 'inf', it is unreachable; ignore them
            if self.dist[v] == float('inf'): continue

            path = []
            at = v
            while at is not None:
                path.append(at)
                at = self.prev[at]
            path.reverse()
            all_paths[v] = path
        return all_paths


    """
    Run Dijkstra's algorithm on a directed graph to find the shortest path
    from a starting node to an ending node. If there is no path between the
    starting node and the destination node the returned value is set to be
    float('inf').
    """
    def dijkstra(self, start:int, end:int):
        self._dijkstra_internal(start, end)
        return self.dist[end]

    def dijkstraAll(self, start:int):
        self._dijkstra_internal(start, None)
        return self.dist

    def _dijkstra_internal(self, start:int, end:int|None):
        # Maintain an array of the minimum distance to each node
        self.dist = [float('inf')] * self.n
        self.dist[start] = 0
        # Array used to track which nodes have already been visited.
        visited = [False] * self.n
        self.prev = [None] * self.n

        # Keep a priority queue of the next most promising node to visit.
        # nodes in heap will be represented by tuple '(score, node_id)'
        pq = [(0, start)]
        
        while len(pq) != 0:
            node_score, node_id = heapq.heappop(pq)

            if visited[node_id]: continue
            visited[node_id] = True

            # Once we've visited all the nodes spanning from the end
            # node we know we can return the minimum distance value to
            # the end node because it cannot get any better after this point.
            if end is not None and node_id == end: return


            # We already found a better path before we got to
            # processing this node so we can ignore it.
            if self.dist[node_id] < node_score: continue

            edges = self.graph[node_id]
            for edge in edges:
                # You cannot get a shorter path by revisiting
                # a node you have already visited before.
                if visited[edge.to]: continue

                # Relax edge by updating minimum cost if applicable.
                new_dist = self.dist[edge.fro] + edge.cost
                if new_dist < self.dist[edge.to]:
                    self.prev[edge.to] = edge.fro
                    self.dist[edge.to] = new_dist
                    heapq.heappush(pq, (self.dist[edge.to], edge.to))

    
    # helper function to print path easily
    def formatPath(self, path:list) -> str:
        return '->'.join(map(str, path))


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
    


# # testing
# def main():
#     print("=== Dijkstra Improved Implementation Test ===\n")

#     # Helper: pretty print all distances & paths from start
#     def print_all(dsp, start):
#         dist = dsp.dist
#         paths = dsp.reconstructAllPaths(start)

#         for v in range(dsp.n):
#             if dist[v] == float('inf'):
#                 print(f"{start} -> {v} : unreachable")
#             else:
#                 print(f"{start} -> {v} : dist={dist[v]}  path={dsp.formatPath(paths[v])}")
#         print()

#     # Helper: run single-pair test
#     def run_pair_test(name, graph, start, end, exp_dist=None, exp_path=None):
#         dsp = DijkstrasShortestPathAdjacencyList(graph)

#         dist = dsp.dijkstra(start, end)
#         path = dsp.reconstructPath(start, end)

#         print(f"[{name}] {start}->{end}")
#         print("dist =", dist)
#         print("path =", dsp.formatPath(path) if path else "unreachable")

#         if exp_dist is not None:
#             print("dist OK =", dist == exp_dist)
#         if exp_path is not None:
#             print("path OK =", path == exp_path)
#         print()

#     # Graph builder
#     builder = DijkstrasShortestPathAdjacencyList([])

#     # -------------------------------------------------
#     # Test 1: Directed weighted graph
#     # -------------------------------------------------
#     g1 = builder.createEmptyGraph(6)
#     builder.addDirectedEdge(g1, 0, 1, 4)
#     builder.addDirectedEdge(g1, 0, 2, 1)
#     builder.addDirectedEdge(g1, 2, 1, 2)
#     builder.addDirectedEdge(g1, 1, 3, 1)
#     builder.addDirectedEdge(g1, 2, 3, 5)
#     builder.addDirectedEdge(g1, 3, 4, 3)
#     builder.addDirectedEdge(g1, 4, 5, 1)

#     run_pair_test(
#         "Directed shortest path",
#         g1,
#         0,
#         5,
#         exp_dist=8,
#         exp_path=[0, 2, 1, 3, 4, 5]
#     )

#     dsp1 = DijkstrasShortestPathAdjacencyList(g1)
#     dsp1.dijkstraAll(0)
#     print("[Directed all paths from 0]")
#     print_all(dsp1, 0)

#     # -------------------------------------------------
#     # Test 2: Undirected graph
#     # -------------------------------------------------
#     g2 = builder.createEmptyGraph(5)
#     builder.addUndirectedEdge(g2, 0, 1, 2)
#     builder.addUndirectedEdge(g2, 1, 2, 3)
#     builder.addUndirectedEdge(g2, 0, 3, 6)
#     builder.addUndirectedEdge(g2, 3, 4, 2)
#     builder.addUndirectedEdge(g2, 4, 2, 1)

#     run_pair_test(
#         "Undirected shortest path",
#         g2,
#         0,
#         2,
#         exp_dist=5,
#         exp_path=[0, 1, 2]
#     )

#     dsp2 = DijkstrasShortestPathAdjacencyList(g2)
#     dsp2.dijkstraAll(0)
#     print("[Undirected all paths from 0]")
#     print_all(dsp2, 0)

#     # -------------------------------------------------
#     # Test 3: Unreachable node
#     # -------------------------------------------------
#     g3 = builder.createEmptyGraph(4)
#     builder.addDirectedEdge(g3, 0, 1, 1)
#     builder.addDirectedEdge(g3, 1, 2, 2)

#     run_pair_test(
#         "Unreachable node",
#         g3,
#         0,
#         3,
#         exp_dist=float('inf'),
#         exp_path=[]
#     )

#     dsp3 = DijkstrasShortestPathAdjacencyList(g3)
#     dsp3.dijkstraAll(0)
#     print("[Graph with unreachable nodes from 0]")
#     print_all(dsp3, 0)

#     # -------------------------------------------------
#     # Test 4: Single node graph
#     # -------------------------------------------------
#     g4 = builder.createEmptyGraph(1)

#     run_pair_test(
#         "Single node",
#         g4,
#         0,
#         0,
#         exp_dist=0,
#         exp_path=[0]
#     )

#     dsp4 = DijkstrasShortestPathAdjacencyList(g4)
#     dsp4.dijkstraAll(0)
#     print("[Single node all paths]")
#     print_all(dsp4, 0)

#     # -------------------------------------------------
#     # Test 5: Multiple equal shortest paths
#     # -------------------------------------------------
#     g5 = builder.createEmptyGraph(4)
#     builder.addDirectedEdge(g5, 0, 1, 1)
#     builder.addDirectedEdge(g5, 0, 2, 1)
#     builder.addDirectedEdge(g5, 1, 3, 1)
#     builder.addDirectedEdge(g5, 2, 3, 1)

#     run_pair_test(
#         "Multiple equal paths",
#         g5,
#         0,
#         3,
#         exp_dist=2
#     )

#     dsp5 = DijkstrasShortestPathAdjacencyList(g5)
#     dsp5.dijkstraAll(0)
#     print("[Multiple shortest paths graph from 0]")
#     print_all(dsp5, 0)


# if __name__ == "__main__":
#     main()
