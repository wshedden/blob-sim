import random
from core.constants import GRID_COLS, GRID_ROWS
from core.grid import get_hex_neighbors, hex_center
from core.blob_base import Blob


class Colony:
    def __init__(self, founder, colour):
        self.id = founder.id
        self.colour = colour
        self.members = [founder]
        self.territory = set([founder.current_cell])
        self.production_timer = 0
        self.production_rate = 600  # frames
        self.world_blobs = None  # must be assigned by caller

        founder.colony = self
        founder.role = "Leader"

    def claim(self, cell):
        self.territory.add(cell)

    def add_member(self, blob):
        blob.colony = self
        blob.role = self.assign_role()
        self.members.append(blob)
        self.claim(blob.current_cell)

    def assign_role(self):
        roles = ["Worker", "Defender", "Recruiter", "Scout"]
        weights = [0.5, 0.2, 0.2, 0.1]
        return random.choices(roles, weights)[0]

    def update(self, occupied_cells):
        self.production_timer += 1
        if self.production_timer >= self.production_rate:
            self.production_timer = 0
            self._try_spawn_blob(occupied_cells)

    def _try_spawn_blob(self, occupied_cells):
        candidate_cells = list(self.territory)
        random.shuffle(candidate_cells)
        for cell in candidate_cells:
            for neighbor in get_hex_neighbors(cell):
                if (
                    0 <= neighbor[0] < GRID_COLS and
                    0 <= neighbor[1] < GRID_ROWS and
                    neighbor not in occupied_cells
                ):
                    self._spawn_blob_at(neighbor)
                    return

    def _spawn_blob_at(self, cell):
        if self.world_blobs is None:
            return  # can't place blobs without world reference
        new_blob = Blob(*cell)
        self.add_member(new_blob)
        self.world_blobs.append(new_blob)
