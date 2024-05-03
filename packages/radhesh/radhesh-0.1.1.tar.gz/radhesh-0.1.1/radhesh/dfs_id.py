# radhesh/dfs_id.py

def dfs_id(initial_state, goal_state, max_depth):
    for depth in range(max_depth):
        result = dfs_recursive_limit(initial_state, goal_state, depth)
        if result:
            return result
    return None

def dfs_recursive_limit(current_state, goal_state, depth_limit, path=None):
    if path is None:
        path = [current_state]

    if current_state == goal_state:
        return path

    if depth_limit <= 0:
        return None

    possible_actions = get_possible_actions(current_state)
    for action in possible_actions:
        new_state = apply_action(current_state, action)
        if new_state not in path:
            new_path = path + [new_state]
            result = dfs_recursive_limit(new_state, goal_state, depth_limit - 1, new_path)
            if result:
                return result

    return None

def get_possible_actions(state):
    # Find the position of the empty tile (0)
    empty_tile_index = state.index(0)
    row, col = divmod(empty_tile_index, 3)

    possible_actions = []
    # Check if the empty tile can move up, down, left, or right
    if row > 0:
        possible_actions.append('up')
    if row < 2:
        possible_actions.append('down')
    if col > 0:
        possible_actions.append('left')
    if col < 2:
        possible_actions.append('right')

    return possible_actions

def apply_action(state, action):
    # Find the position of the empty tile (0)
    empty_tile_index = state.index(0)
    row, col = divmod(empty_tile_index, 3)

    # Calculate the new position of the empty tile after applying the action
    if action == 'up':
        new_row = row - 1
        new_col = col
    elif action == 'down':
        new_row = row + 1
        new_col = col
    elif action == 'left':
        new_row = row
        new_col = col - 1
    elif action == 'right':
        new_row = row
        new_col = col + 1

    # Swap the empty tile with the tile at the new position
    new_empty_tile_index = new_row * 3 + new_col
    new_state = list(state)
    new_state[empty_tile_index], new_state[new_empty_tile_index] = new_state[new_empty_tile_index], new_state[empty_tile_index]
    return tuple(new_state)