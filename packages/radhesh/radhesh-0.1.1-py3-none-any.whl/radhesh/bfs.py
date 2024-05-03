from collections import deque

def bfs(initial_state, goal_state):
    visited = set()
    queue = deque([[initial_state]])

    while queue:
        path = queue.popleft()
        state = path[-1]
        
        if state == goal_state:
            return path
        
        if state not in visited:
            for neighbor in get_neighbors(state):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(state)

    return None

def get_neighbors(state):
    # Find the position of the empty tile (0)
    empty_tile_index = state.index(0)
    row, col = divmod(empty_tile_index, 3)

    neighbors = []
    # Check adjacent tiles and swap with the empty tile
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_empty_tile_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[empty_tile_index], new_state[new_empty_tile_index] = new_state[new_empty_tile_index], new_state[empty_tile_index]
            neighbors.append(tuple(new_state))
    return neighbors