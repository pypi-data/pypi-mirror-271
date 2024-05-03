import os
import sys

# Add the parent directory of the package to Python's path
package_parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_parent_dir)

# Now import the radhesh module
import radhesh

# Define a simple graph as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Define start and goal nodes
start_node = 'A'
goal_node = 'F'

# Define a heuristic function for A* (assuming a uniform cost)
def heuristic(node, goal):
    return 0

# Use BFS to find the shortest path
bfs_path = radhesh.bfs(graph, start_node, goal_node)
print("BFS Path:", bfs_path)