# search_algorithms/dfs_id.py

def dfs_id(graph, start, goal, max_depth):
    for depth in range(max_depth):
        result = dfs_recursive_limit(graph, start, goal, depth)
        if result:
            return result
    return None

def dfs_recursive_limit(graph, current, goal, depth_limit, path=None):
    if path is None:
        path = [current]

    if current == goal:
        return path

    if depth_limit <= 0:
        return None

    for neighbor in graph.get(current, []):
        if neighbor not in path:
            new_path = path + [neighbor]
            result = dfs_recursive_limit(graph, neighbor, goal, depth_limit - 1, new_path)
            if result:
                return result

    return None
