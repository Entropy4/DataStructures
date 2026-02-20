from collections import deque

class BFSAdjacencyListIterative:
    # Time complexity:      O(V + E)
    # Space complexity:     O(V)       <-  we maintain a queue of nodes + who is their predecessors as well as 'visited' boolean for each vertex
    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost

    # 'graph' is a List of 'List of Edges' == List of Vertices
    def __init__(self, graph:list[list[Edge]]): 
        self.n = len(graph)
        self.graph = graph
        self.prev = None    # stores a list of int; 
        # prev[i] stores the index of the node previous to the node 'i'
    
    """  
    Reconstructs the path (of nodes) from 'start' to 'end' inclusive. 
    If the edges are unweighted then this method returns the shortest path from 'start' to 'end'
    
    @return An array of nodes' indexes of the shortest path from 'start' to 'end'. If 'start' and
    'end' are not connected then an empty array is returned.
    """ 
    def reconstructPath(self, start:int, end:int) -> list[int]:
        self.bfs(start)
        path = []
        at = end

        # trace the way backward from 'end' according to the 
        # 'prev's of the nodes, populated by BFS
        while at is not None:
            path.append(at)
            at = self.prev[at]

        # if the backward path reaches 'start' then both are connected
        path.reverse()
        if path[0] == start: return path

        # else no such path connecting them exists, return empty path
        path.clear()
        return path
    
    # Perform a breadth first search on a graph a starting node 'start'.
    def bfs(self, start:int):
        self.prev = [None] * self.n
        visited = [False] * self.n
        queue = deque([], self.n)

        # Start by visiting the 'start' node and add it to the queue.
        queue.append(start)
        visited[start] = True

        # Continue until the BFS is done.
        while len(queue) != 0:
            node = queue.popleft()
            edges = self.graph[node]

            # Loop through all edges attached to this node. Mark nodes as visited once they're
            # in the queue. This will prevent having duplicate nodes in the queue and speedup the BFS.
            for edge in edges:
                if not visited[edge.to]:
                    visited[edge.to] = True
                    self.prev[edge.to] = node
                    queue.append(edge.to)
    

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
    
    # helper function to print path easily
    def formatPath(self, path:list) -> str:
        return '->'.join(map(str, path))



# testing

import random

def main():
    bfs_solver = BFSAdjacencyListIterative([])

    tid = 1

    # ---------- Test 1: simple connected graph ----------
    g1 = bfs_solver.createEmptyGraph(7)
    bfs_solver.addUnweightedUndirectedEdge(g1, 0, 1)
    bfs_solver.addUnweightedUndirectedEdge(g1, 0, 2)
    bfs_solver.addUnweightedUndirectedEdge(g1, 1, 3)
    bfs_solver.addUnweightedUndirectedEdge(g1, 2, 3)
    bfs_solver.addUnweightedUndirectedEdge(g1, 3, 4)
    bfs_solver.addUnweightedUndirectedEdge(g1, 4, 5)

    solver1 = BFSAdjacencyListIterative(g1)

    tests = [
        (0, 5, True),
        (1, 2, True),
        (0, 6, False),
        (3, 3, True),
    ]

    for start, end, should_exist in tests:
        path = solver1.reconstructPath(start, end)
        print(f"Test {tid}: {start} → {end}")
        print("  Path:", solver1.formatPath(path) if path else "None")

        if should_exist:
            ok = (len(path)>0 and path[0]==start and path[-1]==end)
        else:
            ok = (len(path)==0)

        print("  PASS" if ok else "  FAIL", "\n")
        tid += 1


    # ---------- Test 2: multiple shortest paths ----------
    g2 = bfs_solver.createEmptyGraph(6)
    bfs_solver.addUnweightedUndirectedEdge(g2, 0, 1)
    bfs_solver.addUnweightedUndirectedEdge(g2, 0, 2)
    bfs_solver.addUnweightedUndirectedEdge(g2, 1, 3)
    bfs_solver.addUnweightedUndirectedEdge(g2, 2, 3)
    bfs_solver.addUnweightedUndirectedEdge(g2, 3, 4)
    bfs_solver.addUnweightedUndirectedEdge(g2, 4, 5)

    solver2 = BFSAdjacencyListIterative(g2)

    path = solver2.reconstructPath(0, 3)
    print(f"Test {tid}: multiple shortest paths 0 → 3")
    print("  Path:", solver2.formatPath(path))
    ok = (len(path)==3 and path[0]==0 and path[-1]==3)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 3: directed graph ----------
    g3 = bfs_solver.createEmptyGraph(6)
    bfs_solver.addDirectedEdge(g3, 0, 1, 1)
    bfs_solver.addDirectedEdge(g3, 1, 2, 1)
    bfs_solver.addDirectedEdge(g3, 2, 3, 1)
    bfs_solver.addDirectedEdge(g3, 0, 4, 1)
    bfs_solver.addDirectedEdge(g3, 4, 3, 1)

    solver3 = BFSAdjacencyListIterative(g3)

    path = solver3.reconstructPath(0, 3)
    print(f"Test {tid}: directed 0 → 3")
    print("  Path:", solver3.formatPath(path))
    ok = (len(path)>0 and path[0]==0 and path[-1]==3)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1

    path = solver3.reconstructPath(3, 0)
    print(f"Test {tid}: directed 3 → 0 (should fail)")
    print("  Path:", path if path else "None")
    ok = (len(path)==0)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 4: weighted graph ----------
    g4 = bfs_solver.createEmptyGraph(5)
    bfs_solver.addDirectedEdge(g4, 0, 1, 100)
    bfs_solver.addDirectedEdge(g4, 1, 4, 100)
    bfs_solver.addDirectedEdge(g4, 0, 2, 1)
    bfs_solver.addDirectedEdge(g4, 2, 3, 1)
    bfs_solver.addDirectedEdge(g4, 3, 4, 1)

    solver4 = BFSAdjacencyListIterative(g4)

    path = solver4.reconstructPath(0, 4)
    print(f"Test {tid}: weighted graph BFS 0 → 4")
    print("  Path:", solver4.formatPath(path))
    ok = (len(path)==3)  # BFS minimizes edge count
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 5: disconnected clusters ----------
    g5 = bfs_solver.createEmptyGraph(8)
    bfs_solver.addUnweightedUndirectedEdge(g5, 0, 1)
    bfs_solver.addUnweightedUndirectedEdge(g5, 1, 2)
    bfs_solver.addUnweightedUndirectedEdge(g5, 3, 4)
    bfs_solver.addUnweightedUndirectedEdge(g5, 5, 6)

    solver5 = BFSAdjacencyListIterative(g5)

    path = solver5.reconstructPath(0, 2)
    print(f"Test {tid}: cluster 0 → 2")
    print("  Path:", solver5.formatPath(path))
    ok = (len(path)>0)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1

    path = solver5.reconstructPath(0, 4)
    print(f"Test {tid}: cluster 0 → 4 (unreachable)")
    print("  Path:", path if path else "None")
    ok = (len(path)==0)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 6: random graph ----------
    def random_graph(n, p=0.25):
        g = bfs_solver.createEmptyGraph(n)
        for u in range(n):
            for v in range(n):
                if u!=v and random.random()<p:
                    bfs_solver.addUnweightedUndirectedEdge(g, u, v)
        return g

    g6 = random_graph(12, 0.2)
    solver6 = BFSAdjacencyListIterative(g6)

    start, end = 0, 10
    path = solver6.reconstructPath(start, end)

    print(f"Test {tid}: random graph {start} → {end}")
    print("  Path:", solver6.formatPath(path) if path else "None")

    ok = True
    if path:
        if path[0]!=start or path[-1]!=end:
            ok=False
        else:
            for i in range(len(path)-1):
                u,v = path[i], path[i+1]
                if not any(e.to==v for e in g6[u]):
                    ok=False
                    break

    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 7: stress ----------
    g7 = bfs_solver.createEmptyGraph(200)
    for _ in range(400):
        u = random.randint(0,199)
        v = random.randint(0,199)
        if u!=v:
            bfs_solver.addUnweightedUndirectedEdge(g7, u, v)

    solver7 = BFSAdjacencyListIterative(g7)

    path = solver7.reconstructPath(0, 199)
    print(f"Test {tid}: stress 0 → 199")
    print("  Path length:", len(path))
    ok = (len(path)==0 or (path[0]==0 and path[-1]==199))
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


if __name__ == "__main__":
    main()
