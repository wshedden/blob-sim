import sys
import pygame
import random

from core.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR,
    GRID_COLS, GRID_ROWS, FPS
)
from core.grid import hex_center, hex_corners
from core.blob import Blob
from ui.panels import draw_decision_panel, draw_decision_detail_panel
from core.constants import HEX_COLOR, GRID_LINE_COLOR

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hex Grid Blobs with Movement Arrows")
clock = pygame.time.Clock()

# --- Create Blobs ---
# blobs = [
#     Blob(col=pygame.rand.randint(0, GRID_COLS - 1),
#          row=pygame.rand.randint(0, GRID_ROWS - 1))
#     for _ in range(5)
# ]


blobs = [Blob(random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1)) for _ in range(5)]


# --- Main Loop ---
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    for blob in blobs:
        blob.update()

    # --- Draw ---
    screen.fill(BG_COLOR)

    # Draw hex grid
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS):
            center = hex_center(col, row)
            corners = hex_corners(center)
            pygame.draw.polygon(screen, HEX_COLOR, corners)
            pygame.draw.polygon(screen, GRID_LINE_COLOR, corners, 1)

    # Draw blobs and UI
    for blob in blobs:
        blob.draw(screen)

    draw_decision_panel(screen, blobs)
    draw_decision_detail_panel(screen, blobs)

    pygame.display.flip()

# --- Shutdown ---
pygame.quit()
sys.exit()
