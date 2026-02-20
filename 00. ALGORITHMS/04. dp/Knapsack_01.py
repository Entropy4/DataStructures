class Knapsack_01:

    """
    @param capacity - The maximum capacity of the knapsack
    @param W - The weights of the items
    @param V - The values of the items
    @return The maximum achievable profit of selecting a subset of the elements such that the
        capacity of the knapsack is not exceeded    
    """
    # Time complexity: O(n * capacity) 
    #       where, n         -> number of items
    #       and, capacity    -> max capacity of knapsack
    def knapsack(capacity:int, W:list, V:list) -> tuple[int, list[int]]:
        N = len(W)

        # Initialize a table where individual rows represent items
        # and columns represent the weight of the knapsack
        DP = [[0] * (capacity+1) for _ in range(N+1)]

        for i in range(1, N+1):
            # Get the value and weight of the item
            w, v = W[i-1], V[i-1]

            for sz in range(1, capacity+1):
                # Consider not picking this element
                DP[i][sz] = DP[i-1][sz]

                # Consider including the current element if your 
                # residual capacity 'sz' allows for it (sz >= w), and 
                # see if this would be more profitable
                if sz >= w and DP[i-1][sz-w] + v > DP[i][sz]:
                    DP[i][sz] = DP[i-1][sz-w] + v
        
        sz = capacity
        items_selected = []     # stores indexes of the selected items

        # Using the information inside the table we can backtrack and determine
        # which items were selected during the dynamic programming phase. The idea
        # is that if DP[i][sz] != DP[i-1][sz] then the item was selected
        for i in range(N, 0, -1):
            if DP[i][sz] != DP[i-1][sz]:
                item_idx = i-1
                items_selected.append(item_idx)
                sz -= W[item_idx]

        
        # return max profit and the items selected
        return DP[N][capacity], items_selected
    

# Testing
def main():
    def run_test(test_id, capacity, W, V, expected_value=None):
        print(f"\nTest {test_id}")
        print(f"Capacity: {capacity}")
        print(f"Weights:  {W}")
        print(f"Values:   {V}")

        max_value, items = Knapsack_01.knapsack(capacity, W, V)

        # Compute derived stats
        total_weight = sum(W[i] for i in items)
        total_value = sum(V[i] for i in items)

        print(f"Returned max value: {max_value}")
        print(f"Items selected: {items}")
        print(f"Total weight of selected items: {total_weight}")
        print(f"Total value of selected items: {total_value}")

        # Consistency checks
        if total_weight > capacity:
            print("❌ ERROR: Selected items exceed capacity!")
        if total_value != max_value:
            print("❌ ERROR: Value mismatch with selected items!")

        if expected_value is not None:
            if max_value == expected_value:
                print("✅ Max value matches expected.")
            else:
                print(f"❌ Expected {expected_value}, got {max_value}")
        else:
            print("ℹ️ No expected value provided.")

    # --- Standard textbook case ---
    run_test(
        test_id=1,
        capacity=50,
        W=[10, 20, 30],
        V=[60, 100, 120],
        expected_value=220  # items 1 and 2
    )

    # --- Small case ---
    run_test(
        test_id=2,
        capacity=7,
        W=[1, 3, 4, 5],
        V=[1, 4, 5, 7],
        expected_value=9  # items 1 and 2
    )

    # --- Zero capacity ---
    run_test(
        test_id=3,
        capacity=0,
        W=[1, 2, 3],
        V=[10, 20, 30],
        expected_value=0
    )

    # --- No items ---
    run_test(
        test_id=4,
        capacity=10,
        W=[],
        V=[],
        expected_value=0
    )

    # --- All items too heavy ---
    run_test(
        test_id=5,
        capacity=5,
        W=[6, 7, 8],
        V=[10, 20, 30],
        expected_value=0
    )

    # --- Exact fit case ---
    run_test(
        test_id=6,
        capacity=10,
        W=[2, 3, 5],
        V=[20, 30, 50],
        expected_value=100  # all items
    )

    # --- Multiple optimal subsets ---
    run_test(
        test_id=7,
        capacity=8,
        W=[3, 4, 5],
        V=[30, 50, 60],
        expected_value=90  # items 0+2 OR 1+? (depends)
    )


if __name__ == "__main__":
    main()