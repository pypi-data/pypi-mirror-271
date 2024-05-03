# search_algorithms/steepest_ascent.py

def steepest_ascent(state, goal_state, heuristic, max_iterations=1000):
    current_state = state
    for _ in range(max_iterations):
        neighbors = get_neighbors(current_state)
        neighbor_states = [(neighbor, heuristic(neighbor, goal_state)) for neighbor in neighbors]
        best_neighbor, best_heuristic = min(neighbor_states, key=lambda x: x[1])
        if heuristic(current_state, goal_state) <= best_heuristic:
            return current_state
        current_state = best_neighbor
    return None

def get_neighbors(state):
    # Implement how to generate neighboring states
    pass
