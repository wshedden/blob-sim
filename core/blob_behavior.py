import random
from pygame.math import Vector2
from core.grid import get_hex_neighbors, hex_center
from core.pathfinding import a_star_hex, hex_distance
from core.colony import Colony

def markov_decision(self):
    r = random.random()
    if self.markov_state == "Move":
        self.markov_state = "Move" if r < 0.6 else "Stay"
    else:
        self.markov_state = "Stay" if r < 0.7 else "Move"

def get_nearby_blobs(self, blobs, radius=3):
    return [
        other for other in blobs
        if other is not self and hex_distance(self.current_cell, other.current_cell) <= radius
    ]

def wants_colony_with(self, other):
    return (
        self.colony is None and
        other.colony is None and
        self.sociability > 0.3 and
        other.loyalty > 0.3
    )

def decide_path(self, blobs, occupied_cells):
    self.markov_decision()

    if self.markov_state == "Stay":
        self.path = []
        self.decision = "Staying"
        return

    possible = [
        (c, r) for c in range(15) for r in range(15)
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

def update(self, blobs, occupied_cells):
    if self.convo_cooldown > 0:
        self.convo_cooldown -= 1

    if self.state == "Talking":
        self.conversation_timer -= 1
        if self.conversation_timer <= 0:
            self.state = "Idle"
            self.conversation_partner = None
            self.last_conversed_with = None
            self.conversation_lines = []
        return

    if self.colony and self.current_cell not in self.colony.territory:
        self.colony.claim(self.current_cell)

    if self.state == "Idle" and not self.path:
        for other in blobs:
            if other is self:
                continue
            if other.current_cell in get_hex_neighbors(self.current_cell):
                if (
                    other.state == "Idle"
                    and other.conversation_partner is None
                    and other.last_conversed_with != self
                    and self.convo_cooldown == 0
                    and other.convo_cooldown == 0
                ):
                    if self.colony and self.colony is other.colony:
                        if random.random() > 0.05:
                            continue
                        self._colony_chat(other)
                        return

                    self.state = other.state = "Talking"
                    self.conversation_partner = other
                    other.conversation_partner = self
                    self.conversation_timer = other.conversation_timer = random.randint(50, 90)
                    self.last_conversed_with = other
                    other.last_conversed_with = self

                    if self.wants_colony_with(other):
                        self.wants_colony = other.wants_colony = True
                        colony = Colony(founder=self, colour=self.colour_bias)
                        colony.add_member(other)
                        self.colony = colony
                        other.colony = colony
                        self.conversation_lines = [("Let’s start a colony.", self.color)]
                        other.conversation_lines = [("Yeah, I’m in.", other.color)]
                        self.convo_cooldown = other.convo_cooldown = 180
                    else:
                        self.conversation_lines = [("Ever think about teaming up?", self.color)]
                        other.conversation_lines = [("Not really.", other.color)]
                        self.conversation_timer = other.conversation_timer = 30
                        self.convo_cooldown = other.convo_cooldown = 120
                    return

    if not self.path:
        self.decide_path(blobs, occupied_cells)
        return

    next_cell = self.path[0]
    if next_cell in occupied_cells:
        self.path = []
        return

    start_pos = Vector2(hex_center(*self.current_cell))
    target_pos = Vector2(hex_center(*next_cell))
    self.progress += 1 / 60

    if self.progress >= 1:
        overshoot = self.progress - 1
        self.position = target_pos
        self.current_cell = next_cell
        self.path.pop(0)
        self.progress = overshoot
        if not self.path:
            self.decide_path(blobs, occupied_cells)
        if self.path:
            next_cell = self.path[0]
            target_pos = Vector2(hex_center(*next_cell))
            self.position = Vector2(hex_center(*self.current_cell)).lerp(target_pos, self.progress)
    else:
        self.position = start_pos.lerp(target_pos, self.progress)

def _colony_chat(self, other):
    self.state = other.state = "Talking"
    self.conversation_partner = other
    other.conversation_partner = self
    self.last_conversed_with = other
    other.last_conversed_with = self
    self.conversation_timer = other.conversation_timer = 40
    self.convo_cooldown = other.convo_cooldown = 180
    self.conversation_lines = [("Glad we formed this colony.", self.color)]
    other.conversation_lines = [("Yeah. Feels right.", other.color)]
