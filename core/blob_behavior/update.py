def update(self, blobs, occupied_cells):
    from core.grid import hex_center, get_hex_neighbors
    from pygame.math import Vector2
    import random
    from core.colony import Colony

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
                        colony.world_blobs = blobs  # Assign the global blob list to the colony
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


