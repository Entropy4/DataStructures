# This file contains an implementation of the Floyd-Warshall algorithm to find all pairs of
# shortest paths between nodes in a graph. We also demonstrate how to detect negative cycles and
# reconstruct the shortest path.
class FloydWarshallAdjacencyMatrix:
    # Time Complexity: O(V^3)
    REACHES_NEGATIVE_CYCLE = -1
    """
    As input, this class takes an adjacency matrix with edge weights between nodes, where
    POSITIVE_INFINITY is used to indicate that two nodes are not connected.
    
    <p>NOTE: Usually the diagonal of the adjacency matrix is all zeros (i.e. matrix[i][i] = 0 for
    all i) since there is typically no cost to go from a node to itself, but this may depend on
    your graph and the problem you are trying to solve.
   """
    def __init__(self, matrix:list[list[int|float]]):
        self.n = len(matrix)
        self.solved = False
        self.dp = [[0]* self.n for _ in range(self.n)]
        self.next = [[0]* self.n for _ in range(self.n)]

        # Copy input matrix and setup 'next' matrix for path reconstruction.      
        for i in range(self.n):
            for j in range(self.n):
                if matrix[i][j] != float('inf'): self.next[i][j] = j
                self.dp[i][j] = matrix[i][j]
        
    # Runs Floyd-Warshall to compute the shortest distance between every pair of nodes.
    # @return The solved All Pairs Shortest Path (APSP) matrix.
    def getApspMatrix(self) -> list[list[int|float]]:
        self.solve()
        return self.dp
    
    # Executes the Floyd-Warshall algorithm
    def solve(self):
        if self.solved: return

        # Compute all pairs shortest paths.
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if self.dp[i][k] + self.dp[k][j] < self.dp[i][j]:
                        self.dp[i][j] = self.dp[i][k] + self.dp[k][j]
                        self.next[i][j] = self.next[i][k]
        
        # Identify negative cycles by propagating the value 'NEGATIVE_INFINITY'
        # to every edge that is part of or reaches into a negative cycle.
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if (self.dp[i][k] != float('inf')
                    and self.dp[k][j] != float('inf')
                    and self.dp[k][k] < 0
                    ):
                        self.dp[i][j] = float('-inf')
                        self.next[i][j] = self.REACHES_NEGATIVE_CYCLE

        solved = True

    """
    Reconstructs the shortest path (of nodes) from 'start' to 'end' inclusive.
    
    @return An array of nodes indexes of the shortest path from 'start' to 'end'. If 'start' and
        'end' are not connected return an empty array. If the shortest path from 'start' to 'end'
        are reachable by a negative cycle return -1.
    """
    def reconstructShortestPath(self, start:int, end:int) -> list[int]|None:
        self.solve()
        path = []
        if self.dp[start][end] == float('inf'): return path
        at = start
        while at != end:
            # Return null since there are an infinite number of shortest paths.
            if at == self.REACHES_NEGATIVE_CYCLE: return None
            path.append(at)
            at = self.next[at][end]
               
        # Return null since there are an infinite number of shortest paths.
        if self.next[at][end] == self.REACHES_NEGATIVE_CYCLE: return None
        path.append(end)
        return path
    
    # ------------GRAPH RELATED-------------------

    # Creates a graph with n nodes. The adjacency matrix is constructed
    # such that the value of going from a node to itself is 0.
    def createGraph(n:int) -> list[list[float|int]]:
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0

        return matrix
    
# testing
def main():
    # Construct graph
    n = 7
    m = FloydWarshallAdjacencyMatrix.createGraph(n)

    # Add edge values
    m[0][1] = 2
    m[0][2] = 5
    m[0][6] = 10
    m[1][2] = 2
    m[1][4] = 11
    m[2][6] = 2
    m[6][5] = 11
    m[4][5] = 1
    m[5][4] = -2

    solver = FloydWarshallAdjacencyMatrix(m)
    dist = solver.getApspMatrix()

    # Print APSP distances
    for i in range(n):
        for j in range(n):
            print(
                f"This shortest path from node {i} to node {j} is {dist[i][j]:.3f}"
            )

    print()

    # Reconstruct paths
    for i in range(n):
        for j in range(n):
            path = solver.reconstructShortestPath(i, j)

            if path is None:
                s = "HAS AN ∞ NUMBER OF SOLUTIONS! (negative cycle case)"
            elif len(path) == 0:
                s = f"DOES NOT EXIST (node {i} doesn't reach node {j})"
            else:
                s = "is: [" + " -> ".join(map(str, path)) + "]"

            print(f"The shortest path from node {i} to node {j} {s}")


if __name__ == "__main__":
    main()
