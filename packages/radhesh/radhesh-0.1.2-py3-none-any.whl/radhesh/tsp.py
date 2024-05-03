import sys
from itertools import permutations

def tsp(graph):
    n = len(graph)
    # Initialize memoization table
    dp = [[None] * n for _ in range(2**n)]

    # Base case: when only one city is visited
    for i in range(n):
        dp[1 << i][i] = graph[i][0]

    # Recursive function to compute the shortest tour
    def dfs(mask, last):
        if dp[mask][last] is not None:
            return dp[mask][last]

        min_cost = sys.maxsize
        for next_city in range(n):
            if mask & (1 << next_city):  # Check if next_city is not visited
                new_mask = mask & ~(1 << next_city)  # Mark next_city as visited
                cost = graph[last][next_city] + dfs(new_mask, next_city)
                min_cost = min(min_cost, cost)

        dp[mask][last] = min_cost
        return min_cost

    # Compute the shortest tour starting from any city
    min_tour = min(graph[0][city] + dfs(((1 << n) - 1) & ~(1 << city), city) for city in range(1, n))
    return min_tour