# search_algorithms/dfs.py

def dfs(graph, start, goal):
    visited = set()
    stack = [[start]]

    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            for adjacent in graph.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                stack.append(new_path)
            visited.add(node)

    return None
