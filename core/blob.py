import random
import pygame
from pygame.math import Vector2

from core.constants import MOVE_DURATION, EYE_COLOR, GRID_COLS, GRID_ROWS, TARGET_OUTLINE_WIDTH
from core.grid import hex_center, get_hex_neighbors
from core.pathfinding import a_star_hex, hex_distance
from ui.drawing import draw_arrow


class Blob:
    def __init__(self, col, row):
        self.current_cell = (col, row)
        self.position = Vector2(hex_center(col, row))
        self.path = []
        self.progress = 1

        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

        self.markov_state = "Move"
        self.decision = "Idle"

        self.state = "Idle"
        self.conversation_partner = None
        self.conversation_timer = 0
        self.last_conversed_with = 0# --- Personality Traits (0.0–1.0 floats) ---
        self.sociability = round(random.uniform(0.0, 1.0), 2)
        self.territorial = round(random.uniform(0.0, 1.0), 2)
        self.loyalty = round(random.uniform(0.0, 1.0), 2)
        self.boldness = round(random.uniform(0.0, 1.0), 2)

        # --- Personality Colour Bias (for territory blending) ---
        self.colour_bias = tuple(
            min(255, int(c + random.randint(-20, 20))) for c in self.color
        )
        
        self.conversation_lines = []
                
                

    def markov_decision(self):
        r = random.random()
        if self.markov_state == "Move":
            self.markov_state = "Move" if r < 0.6 else "Stay"
        else:
            self.markov_state = "Stay" if r < 0.7  else "Move"

    def get_nearby_blobs(self, blobs, radius=3):
        return [
            other for other in blobs
            if other is not self and hex_distance(self.current_cell, other.current_cell) <= radius
        ]

    def decide_path(self, blobs, occupied_cells):
        self.markov_decision()

        if self.markov_state == "Stay":
            self.path = []
            self.decision = "Staying"
            return

        possible = [
            (c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)
            if (c, r) != self.current_cell and (c, r) not in occupied_cells
        ]

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
        if self.state == "Talking":
            self.conversation_timer -= 1
            if self.conversation_timer <= 0:
                self.state = "Idle"
                self.conversation_partner = None
                self.last_conversed_with = None
                self.conversation_lines = []
            return

        if self.state == "Idle" and not self.path:
            for other in blobs:
                if other is self:
                    continue
                if other.current_cell in get_hex_neighbors(self.current_cell):
                    if (
                        other.state == "Idle"
                        and other.conversation_partner is None
                        and other.last_conversed_with != self
                    ):
                        self.state = "Talking"
                        other.state = "Talking"

                        self.conversation_partner = other
                        other.conversation_partner = self

                        duration = random.randint(50, 90)
                        self.conversation_timer = other.conversation_timer = duration

                        self.last_conversed_with = other
                        other.last_conversed_with = self

                        initiator_lines = [
                            "Hey there!",
                            "What brings you here?",
                            "You move well.",
                            "Cool hex!"
                        ]
                        reply_lines = [
                            "Hey!",
                            "Just wandering.",
                            "Thanks, you too!",
                            "Haha thanks."
                        ]

                        self.conversation_lines = [(random.choice(initiator_lines), self.color)]
                        other.conversation_lines = [(random.choice(reply_lines), other.color)]
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
        self.progress += 1 / MOVE_DURATION

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

    def draw(self, surface):
        pos = self.position
        pygame.draw.circle(surface, self.color, (int(pos.x), int(pos.y)), 10)
        offset = 4
        pygame.draw.circle(surface, EYE_COLOR, (int(pos.x - offset), int(pos.y - offset)), 2)
        pygame.draw.circle(surface, EYE_COLOR, (int(pos.x + offset), int(pos.y - offset)), 2)
        if self.path:
            target_center = hex_center(*self.path[0])
            draw_arrow(surface, pos, target_center, self.color, TARGET_OUTLINE_WIDTH)

    def draw_conversation(self, surface):
        if self.state != "Talking" or not self.conversation_lines or not self.conversation_partner:
            return
        if self is not min(self, self.conversation_partner, key=id):
            return  # Only draw once per pair

        mid = (self.position + self.conversation_partner.position) / 2
        font = pygame.font.SysFont(None, 18)

        padding = 6
        spacing = 5
        y_offset = -30

        for line, bg_color in self.conversation_lines + self.conversation_partner.conversation_lines:
            text_surf = font.render(line, True, (255, 255, 255))
            rect = text_surf.get_rect(center=(mid.x, mid.y + y_offset))
            pygame.draw.rect(surface, bg_color, rect.inflate(padding * 2, padding))
            surface.blit(text_surf, rect)
            y_offset += rect.height + spacing
