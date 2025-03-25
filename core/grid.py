import math
from core.constants import (
    HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, GRID_COLS, GRID_ROWS
)

def hex_center(col, row):
    """
    Return the center (x, y) of the hex at (col, row),
    using odd-r offset layout and margin from constants.
    """
    from core.constants import MARGIN  # avoid circular import at top
    x = MARGIN + HEX_WIDTH * (col + 0.5 * (row & 1))
    y = MARGIN + HEX_HEIGHT * 0.75 * row + HEX_RADIUS
    return (x, y)

def hex_corners(center):
    """
    Return the list of (x, y) corners of a hex given its center.
    """
    cx, cy = center
    corners = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = cx + HEX_RADIUS * math.cos(angle)
        y = cy + HEX_RADIUS * math.sin(angle)
        corners.append((x, y))
    return corners

def get_hex_neighbors(cell):
    """
    Return the neighbouring cells of a given (col, row) cell,
    accounting for the offset layout.
    """
    col, row = cell
    if row & 1:
        directions = [(+1, 0), (+1, -1), (0, -1), (-1, 0), (0, +1), (+1, +1)]
    else:
        directions = [(+1, 0), (0, -1), (-1, -1), (-1, 0), (-1, +1), (0, +1)]
    
    neighbors = []
    for dc, dr in directions:
        ncol = col + dc
        nrow = row + dr
        if 0 <= ncol < GRID_COLS and 0 <= nrow < GRID_ROWS:
            neighbors.append((ncol, nrow))
    return neighbors
