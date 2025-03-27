def get_nearby_blobs(self, blobs, radius=3):
    from core.pathfinding import hex_distance
    return [
        other for other in blobs
        if other is not self and hex_distance(self.current_cell, other.current_cell) <= radius
    ]
