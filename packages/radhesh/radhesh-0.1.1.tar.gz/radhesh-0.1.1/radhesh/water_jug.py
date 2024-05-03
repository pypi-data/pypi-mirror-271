# radhesh/waterjug.py

def water_jug_problem(capacities, initial_state, goal_state):
    # Unpack capacities
    jug1_capacity, jug2_capacity = capacities

    # Unpack initial and goal states
    initial_jug1, initial_jug2 = initial_state
    goal_jug1, goal_jug2 = goal_state

    # Check if the goal state is reachable
    if goal_jug1 > jug1_capacity or goal_jug2 > jug2_capacity:
        return None

    # Initialize visited set and queue for BFS
    visited = set()
    queue = [(0, 0, initial_jug1, initial_jug2, [])]  # (depth, cost, state1, state2, path)

    while queue:
        depth, cost, state1, state2, path = queue.pop(0)

        # Check if the goal state is reached
        if state1 == goal_jug1 and state2 == goal_jug2:
            return path

        # Explore all possible actions
        for action in ["fill jug 1", "fill jug 2", "empty jug 1", "empty jug 2", "pour jug 1 to jug 2", "pour jug 2 to jug 1"]:
            if action == "fill jug 1":
                new_state1 = jug1_capacity
                new_state2 = state2
            elif action == "fill jug 2":
                new_state1 = state1
                new_state2 = jug2_capacity
            elif action == "empty jug 1":
                new_state1 = 0
                new_state2 = state2
            elif action == "empty jug 2":
                new_state1 = state1
                new_state2 = 0
            elif action == "pour jug 1 to jug 2":
                pour_amount = min(state1, jug2_capacity - state2)
                new_state1 = state1 - pour_amount
                new_state2 = state2 + pour_amount
            elif action == "pour jug 2 to jug 1":
                pour_amount = min(state2, jug1_capacity - state1)
                new_state1 = state1 + pour_amount
                new_state2 = state2 - pour_amount

            # Check if the new state is valid and not visited
            if (new_state1, new_state2) not in visited:
                new_cost = cost + 1  # Assuming uniform cost
                new_path = path + [action]
                queue.append((depth + 1, new_cost, new_state1, new_state2, new_path))
                visited.add((new_state1, new_state2))

    return None
