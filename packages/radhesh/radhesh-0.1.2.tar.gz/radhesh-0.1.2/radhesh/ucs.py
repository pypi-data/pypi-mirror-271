import heapq

def ucs(graph, start, goal):
    open_list = [(0, start)]
    closed_set = set()
    came_from = {}
    cost_so_far = {node: float('inf') for node in graph}
    cost_so_far[start] = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))

        closed_set.add(current)

        for neighbor, cost in graph[current].items():
            new_cost = cost_so_far[current] + cost
            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(open_list, (new_cost, neighbor))

    return None