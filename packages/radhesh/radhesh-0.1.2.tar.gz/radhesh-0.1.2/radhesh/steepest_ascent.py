def steepest_ascent(state, goal_state, heuristic, max_iterations=1000):
    current_state = state
    for _ in range(max_iterations):
        neighbors = get_neighbors_8puzzle(current_state)
        neighbor_states = [(neighbor, heuristic(neighbor, goal_state)) for neighbor in neighbors]
        best_neighbor, best_heuristic = min(neighbor_states, key=lambda x: x[1])
        if heuristic(current_state, goal_state) <= best_heuristic:
            return current_state
        current_state = best_neighbor
    return None

def get_neighbors_8puzzle(state):
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

# Example Manhattan distance heuristic for the 8-puzzle problem
def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i * 3 + j] != 0:
                target_row, target_col = divmod(state[i * 3 + j] - 1, 3)
                distance += abs(i - target_row) + abs(j - target_col)
    return distance
