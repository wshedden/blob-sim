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

        # Movement / Decision
        self.markov_state = "Move"
        self.decision = "Idle"

        # Talking system
        self.state = "Idle"
        self.conversation_partner = None
        self.conversation_timer = 0
        self.last_conversed_with = None
        self.conversation_text = ""

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

    def decide_path(self, blobs, occupied_cells):
        self.markov_decision()

        if self.markov_state == "Stay":
            self.path = []
            self.decision = "Staying"
            return

        # Avoid occupied cells
        possible = [
            (c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)
            if (c, r) != self.current_cell and (c, r) not in occupied_cells
        ]

        if not possible:
            self.path = []
            self.decision = "No options"
            return

        # Pick a target and find a path
        target = random.choice(possible)
        new_path = a_star_hex(self.current_cell, target)

        # Remove invalid paths or blocked steps
        if len(new_path) > 1 and all(cell not in occupied_cells for cell in new_path[1:]):
            self.path = new_path[1:]
            self.decision = f"Target {target}"
        else:
            self.path = []
            self.decision = "No valid path"

    def update(self, blobs, occupied_cells):
        # Handle talking
        if self.state == "Talking":
            self.conversation_timer -= 1
            if self.conversation_timer <= 0:
                self.state = "Idle"
                self.conversation_partner = None
                self.last_conversed_with = None
            return

        # Start conversation if adjacent and idle
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

                        duration = random.randint(60, 120)
                        self.conversation_timer = other.conversation_timer = duration

                        self.last_conversed_with = other
                        other.last_conversed_with = self

                        msg = random.choice([
                            "Nice weather.",
                            "Where are you headed?",
                            "I like your colour.",
                            "Do you ever stay still?"
                        ])
                        self.conversation_text = msg
                        other.conversation_text = msg
                        return

        # Decide where to go
        if not self.path:
            self.decide_path(blobs, occupied_cells)
            return

        # Step toward next cell
        next_cell = self.path[0]
        if next_cell in occupied_cells:
            self.path = []  # abort path due to collision
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
        if self.state != "Talking" or not self.conversation_text or not self.conversation_partner:
            return
        mid = (self.position + self.conversation_partner.position) / 2
        font = pygame.font.SysFont(None, 18)
        text_surf = font.render(self.conversation_text, True, (255, 255, 255))
        bubble_rect = text_surf.get_rect(center=(mid.x, mid.y - 25))
        pygame.draw.rect(surface, (0, 0, 0), bubble_rect.inflate(8, 4))
        surface.blit(text_surf, bubble_rect)
