import sys
import random
import pygame

from core.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR,
    GRID_COLS, GRID_ROWS, FPS, HEX_COLOR, GRID_LINE_COLOR
)
from core.grid import hex_center, hex_corners
from core.blob import Blob
from ui.panels import draw_decision_panel, draw_decision_detail_panel

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hex Grid Blobs with Movement & Interaction")
    clock = pygame.time.Clock()

    # --- Create Blobs ---
    blobs = []
    taken_cells = set()
    while len(blobs) < 5:
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        if (col, row) not in taken_cells:
            blobs.append(Blob(col, row))
            taken_cells.add((col, row))

    # --- Main Loop ---
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Compute current occupied cells
        occupied_cells = {blob.current_cell for blob in blobs}

        # Update all blobs
        for blob in blobs:
            blob.update(blobs, occupied_cells)

        # --- Drawing ---
        screen.fill(BG_COLOR)

        # Draw hex grid
        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                center = hex_center(col, row)
                corners = hex_corners(center)
                pygame.draw.polygon(screen, HEX_COLOR, corners)
                pygame.draw.polygon(screen, GRID_LINE_COLOR, corners, 1)

        # Draw blobs
        for blob in blobs:
            blob.draw(screen)

        # Draw any conversations
        for blob in blobs:
            blob.draw_conversation(screen)

        # Draw UI panels
        draw_decision_panel(screen, blobs)
        draw_decision_detail_panel(screen, blobs)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
