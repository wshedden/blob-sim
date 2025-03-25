import random
import pygame
from pygame.math import Vector2

from core.constants import MOVE_DURATION, EYE_COLOR, GRID_COLS, GRID_ROWS, TARGET_OUTLINE_WIDTH
from core.grid import hex_center, get_hex_neighbors
from core.pathfinding import a_star_hex
from ui.drawing import draw_arrow


class Blob:
    def __init__(self, col, row):
        self.current_cell = (col, row)
        self.position = Vector2(hex_center(col, row))
        self.path = []
        self.progress = 1  # 1 = finished moving
        self.decision = "Idle"
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.markov_state = "Move"

    def markov_decision(self):
        r = random.random()
        if self.markov_state == "Move":
            self.markov_state = "Move" if r < 0.6 else "Stay"
        else:
            self.markov_state = "Stay" if r < 0.99 else "Move"

    def decide_path(self):
        self.markov_decision()

        if self.markov_state == "Stay":
            self.path = []
            self.decision = "Staying"
            return

        possible = [
            (c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)
            if (c, r) != self.current_cell
        ]
        if possible:
            target = random.choice(possible)
            new_path = a_star_hex(self.current_cell, target)
            if len(new_path) <= 1:
                neighbors = get_hex_neighbors(self.current_cell)
                if neighbors:
                    target = random.choice(neighbors)
                    new_path = a_star_hex(self.current_cell, target)
            if len(new_path) > 1:
                self.path = new_path[1:]  # exclude current
                self.decision = f"Target {target}"
            else:
                self.path = []
                self.decision = "No path"
        else:
            self.decision = "No options"

    def update(self):
        if not self.path:
            self.decide_path()
            return

        start_pos = Vector2(hex_center(*self.current_cell))
        next_cell = self.path[0]
        target_pos = Vector2(hex_center(*next_cell))
        self.progress += 1 / MOVE_DURATION

        if self.progress >= 1:
            overshoot = self.progress - 1
            self.position = target_pos
            self.current_cell = next_cell
            self.path.pop(0)
            self.progress = overshoot
            if not self.path:
                self.decide_path()
            if self.path:
                start_pos = Vector2(hex_center(*self.current_cell))
                next_cell = self.path[0]
                target_pos = Vector2(hex_center(*next_cell))
                self.position = start_pos.lerp(target_pos, self.progress)
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
