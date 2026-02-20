from collections import deque

class DFSAdjacencyListIterative:
    # Time complexity:      O(V + E)
    # Space complexity:     O(V)      BUT generally uses less memory than BFS
    class Edge:
        def __init__(self, fro:int, to:int, cost:int):
            self.fro = fro
            self.to = to
            self.cost = cost

    def __init__(self):
        pass

    # Perform a depth first search on a graph with n nodes
    # from a starting point to count the number of nodes
    # in a given component.
    def dfs(self, graph:list, start:int, n:int) -> int:
        # 'graph' is a Map of Int (node label) x ['List of Edges' == Vertices]
        # trying with list, and expecting index to work as label
        count = 0
        visited = [False] * n
        stack = deque()

        stack.append(start)
        visited[start] = True

        while len(stack) != 0:
            node = stack.pop()
            count += 1
            edges = graph[node]

            for edge in edges:
                if not visited[edge.to]:
                    stack.append(edge.to)
                    visited[edge.to] = True
        
        return count

    # topologically sorts the graph nodes. O(V + E) Time complexity
    def topologicalSort(self, graph:list, n:int) -> list:
        visited = [False] * n
        order = []
        for i in range(n):
            if not visited[i]:
                self._dfs_topsort(graph, i, n, visited, order)
        
        order.reverse()
        return order
    
    def _dfs_topsort(self, graph:list, start:int, n:int, visited:list, order:list):
        stack = deque()
        visited[start] = True
        stack.append((start, 0))

        while len(stack) != 0:
            node, idx = stack[-1]

            # if there are more unexplored edges arising from 'node', explore deeper
            if idx < len(graph[node]):
                edge = graph[node][idx]
                stack[-1] = (node, idx + 1)

                # if the destination is unexplored, add it to stack. 
                # We will explore that node in next iteration of the loop
                if not visited[edge.to]:
                    visited[edge.to] = True
                    stack.append((edge.to, 0))

            # when there are no more unexplored edges from 'node'. time to backtrack
            else:
                order.append(node)
                stack.pop()


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
    

# Testing
import random

def main():
    dfs_solver = DFSAdjacencyListIterative()
    tid = 1

    # ---------- Test 1: simple connected ----------
    g1 = dfs_solver.createEmptyGraph(6)
    dfs_solver.addUnweightedUndirectedEdge(g1, 0, 1)
    dfs_solver.addUnweightedUndirectedEdge(g1, 1, 2)
    dfs_solver.addUnweightedUndirectedEdge(g1, 2, 3)
    dfs_solver.addUnweightedUndirectedEdge(g1, 3, 4)
    dfs_solver.addUnweightedUndirectedEdge(g1, 4, 5)

    count = dfs_solver.dfs(g1, 0, 6)
    print(f"Test {tid}: chain component size from 0")
    print("  Count:", count)
    ok = (count == 6)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 2: disconnected clusters ----------
    g2 = dfs_solver.createEmptyGraph(8)
    dfs_solver.addUnweightedUndirectedEdge(g2, 0, 1)
    dfs_solver.addUnweightedUndirectedEdge(g2, 1, 2)
    dfs_solver.addUnweightedUndirectedEdge(g2, 3, 4)
    dfs_solver.addUnweightedUndirectedEdge(g2, 5, 6)

    count = dfs_solver.dfs(g2, 0, 8)
    print(f"Test {tid}: cluster size from 0")
    print("  Count:", count)
    ok = (count == 3)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1

    count = dfs_solver.dfs(g2, 3, 8)
    print(f"Test {tid}: cluster size from 3")
    print("  Count:", count)
    ok = (count == 2)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 3: directed graph ----------
    g3 = dfs_solver.createEmptyGraph(5)
    dfs_solver.addDirectedEdge(g3, 0, 1, 1)
    dfs_solver.addDirectedEdge(g3, 1, 2, 1)
    dfs_solver.addDirectedEdge(g3, 2, 3, 1)
    dfs_solver.addDirectedEdge(g3, 3, 4, 1)

    count = dfs_solver.dfs(g3, 0, 5)
    print(f"Test {tid}: directed chain from 0")
    print("  Count:", count)
    ok = (count == 5)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1

    count = dfs_solver.dfs(g3, 4, 5)
    print(f"Test {tid}: directed from 4 (sink)")
    print("  Count:", count)
    ok = (count == 1)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 4: cycle ----------
    g4 = dfs_solver.createEmptyGraph(4)
    dfs_solver.addUnweightedUndirectedEdge(g4, 0, 1)
    dfs_solver.addUnweightedUndirectedEdge(g4, 1, 2)
    dfs_solver.addUnweightedUndirectedEdge(g4, 2, 3)
    dfs_solver.addUnweightedUndirectedEdge(g4, 3, 0)

    count = dfs_solver.dfs(g4, 0, 4)
    print(f"Test {tid}: cycle component")
    print("  Count:", count)
    ok = (count == 4)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 5: isolated nodes ----------
    g5 = dfs_solver.createEmptyGraph(5)
    dfs_solver.addUnweightedUndirectedEdge(g5, 0, 1)

    count = dfs_solver.dfs(g5, 2, 5)
    print(f"Test {tid}: isolated node 2")
    print("  Count:", count)
    ok = (count == 1)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 6: random graph ----------
    def random_graph(n, p=0.2):
        g = dfs_solver.createEmptyGraph(n)
        for u in range(n):
            for v in range(u+1, n):
                if random.random() < p:
                    dfs_solver.addUnweightedUndirectedEdge(g, u, v)
        return g

    g6 = random_graph(12, 0.25)

    start = 0
    count = dfs_solver.dfs(g6, start, 12)

    print(f"Test {tid}: random graph component from {start}")
    print("  Count:", count)

    # verify via BFS-style reachability check
    visited = [False]*12
    stack=[start]
    visited[start]=True
    exp=0
    while stack:
        u=stack.pop()
        exp+=1
        for e in g6[u]:
            if not visited[e.to]:
                visited[e.to]=True
                stack.append(e.to)

    ok = (count == exp)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1


    # ---------- Test 7: stress ----------
    g7 = dfs_solver.createEmptyGraph(300)
    for _ in range(600):
        u = random.randint(0,299)
        v = random.randint(0,299)
        if u!=v:
            dfs_solver.addUnweightedUndirectedEdge(g7, u, v)

    count = dfs_solver.dfs(g7, 0, 300)
    print(f"Test {tid}: stress component from 0")
    print("  Count:", count)
    ok = (1 <= count <= 300)
    print("  PASS" if ok else "  FAIL", "\n")
    tid += 1

    # -------------------------------------------------------------
    print("\n===== TOPOLOGICAL SORT TESTS =====")

    def validate_topo(graph, order):
        pos = {node: i for i, node in enumerate(order)}
        for u in range(len(graph)):
            for edge in graph[u]:
                if pos[u] >= pos[edge.to]:
                    return False
        return True

    # Test 1: Linear DAG
    n = 5
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 0, 1, 1)
    dfs_solver.addDirectedEdge(g, 1, 2, 1)
    dfs_solver.addDirectedEdge(g, 2, 3, 1)
    dfs_solver.addDirectedEdge(g, 3, 4, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo Linear:", order, "valid=", validate_topo(g, order), "exp=True")

    # Test 2: Branching DAG
    # 0 → 1,2 ; 1→3 ; 2→3
    n = 4
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 0, 1, 1)
    dfs_solver.addDirectedEdge(g, 0, 2, 1)
    dfs_solver.addDirectedEdge(g, 1, 3, 1)
    dfs_solver.addDirectedEdge(g, 2, 3, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo Branch:", order, "valid=", validate_topo(g, order), "exp=True")

    # Test 3: Diamond DAG
    # 0→1,0→2,1→3,2→3
    n = 4
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 0, 1, 1)
    dfs_solver.addDirectedEdge(g, 0, 2, 1)
    dfs_solver.addDirectedEdge(g, 1, 3, 1)
    dfs_solver.addDirectedEdge(g, 2, 3, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo Diamond:", order, "valid=", validate_topo(g, order), "exp=True")

    # Test 4: Multiple components DAG
    # 0→1→2   and   3→4
    n = 5
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 0, 1, 1)
    dfs_solver.addDirectedEdge(g, 1, 2, 1)
    dfs_solver.addDirectedEdge(g, 3, 4, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo MultiComp:", order, "valid=", validate_topo(g, order), "exp=True")

    # Test 5: Disconnected nodes
    # 0→1 , 2 isolated , 3 isolated
    n = 4
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 0, 1, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo Disconnected:", order, "valid=", validate_topo(g, order), "exp=True")

    # Test 6: Larger DAG
    # 5→2,5→0,4→0,4→1,2→3,3→1
    n = 6
    g = dfs_solver.createEmptyGraph(n)
    dfs_solver.addDirectedEdge(g, 5, 2, 1)
    dfs_solver.addDirectedEdge(g, 5, 0, 1)
    dfs_solver.addDirectedEdge(g, 4, 0, 1)
    dfs_solver.addDirectedEdge(g, 4, 1, 1)
    dfs_solver.addDirectedEdge(g, 2, 3, 1)
    dfs_solver.addDirectedEdge(g, 3, 1, 1)

    order = dfs_solver.topologicalSort(g, n)
    print("Topo Large:", order, "valid=", validate_topo(g, order), "exp=True")


if __name__ == "__main__":
    main()
