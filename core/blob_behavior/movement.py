import random
def markov_decision(self):
    import random
    r = random.random()
    if self.markov_state == "Move":
        self.markov_state = "Move" if r < 0.6 else "Stay"
    else:
        self.markov_state = "Stay" if r < 0.7 else "Move"

def decide_path(self, blobs, occupied_cells):
    from core.pathfinding import a_star_hex
    from core.constants import GRID_COLS, GRID_ROWS

    self.markov_decision()

    if self.markov_state == "Stay":
        self.path = []
        self.decision = "Staying"
        return

    possible = [
        (c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)
        if (c, r) != self.current_cell and (c, r) not in occupied_cells
    ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

    if self.colony:
        possible = [cell for cell in possible if cell in self.colony.territory]

    if not possible:
        self.path = []
        self.decision = "No options"
        return

    target = random.choice(possible)
    new_path = a_star_hex(self.current_cell, target)

    if len(new_path) > 1 and all(cell not in occupied_cells for cell in new_path[1:]):
        self.path = new_path[1:]
        self.decision = f"Target {target}"
    else:
        self.path = []
        self.decision = "No valid path"
        
def get_nearby_blobs(current_blob, blobs, radius):
    """
    Finds blobs within a certain radius of the current blob.
    """
    nearby_blobs = []
    for blob in blobs:
        if blob is not current_blob and blob.position.distance_to(current_blob.position) <= radius:
            nearby_blobs.append(blob)
    return nearby_blobs
