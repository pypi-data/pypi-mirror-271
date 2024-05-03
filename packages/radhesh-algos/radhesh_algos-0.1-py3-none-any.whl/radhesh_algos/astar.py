# search_algorithms/astar.py

import heapq

def astar(graph, start, goal, heuristic):
    open_list = [(heuristic(start, goal), start)]
    closed_set = set()
    came_from = {}

    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

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

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + 1  # Assuming uniform cost
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, neighbor))

    return None
