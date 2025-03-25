import heapq
from core.grid import get_hex_neighbors

def offset_to_cube(col, row):
    """
    Convert offset (odd-r) coordinates to cube coordinates for hex distance.
    """
    x = col - (row - (row & 1)) // 2
    z = row
    y = -x - z
    return (x, y, z)

def cube_distance(a, b):
    """
    Manhattan distance between two hexes in cube coordinates.
    """
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

def hex_distance(cell1, cell2):
    """
    Compute distance between two hexes using cube coordinates.
    """
    return cube_distance(offset_to_cube(*cell1), offset_to_cube(*cell2))

def a_star_hex(start, goal, faction=None):
    """
    A* pathfinding on a hex grid. Currently uses uniform cost (1 per move).
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        for next_cell in get_hex_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + hex_distance(goal, next_cell)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = current

    if goal not in came_from:
        return []

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
