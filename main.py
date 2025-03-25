import sys
import random
import pygame

from core.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR,
    GRID_COLS, GRID_ROWS, FPS, HEX_COLOR, GRID_LINE_COLOR
)
from core.grid import hex_center, hex_corners
from core.blob import Blob
from core.colony import Colony
from ui.panels import draw_decision_panel, draw_personality_panel

# Global colony state
colonies = []
tile_owner = {}   # (col, row) → colony_id
tile_colour = {}  # (col, row) → RGB


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Blob Simulation with Colonies")
    clock = pygame.time.Clock()

    # Create initial blobs
    blobs = []
    taken_cells = set()
    while len(blobs) < 5:
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        if (col, row) not in taken_cells:
            blobs.append(Blob(col, row))
            taken_cells.add((col, row))

    # Main loop
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        occupied_cells = {blob.current_cell for blob in blobs}

        for blob in blobs:
            blob.update(blobs, occupied_cells)

            # Claim territory if in a colony
            if blob.colony and blob.current_cell not in blob.colony.territory:
                blob.colony.claim(blob.current_cell)
                tile_owner[blob.current_cell] = blob.colony.id
                tile_colour[blob.current_cell] = blob.colony.colour

        # Drawing
        screen.fill(BG_COLOR)

        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                center = hex_center(col, row)
                corners = hex_corners(center)
                cell = (col, row)
                fill = tile_colour.get(cell, HEX_COLOR)
                pygame.draw.polygon(screen, fill, corners)
                pygame.draw.polygon(screen, GRID_LINE_COLOR, corners, 1)

        for blob in blobs:
            blob.draw(screen)
        for blob in blobs:
            blob.draw_conversation(screen)

        draw_decision_panel(screen, blobs)
        draw_personality_panel(screen, blobs)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
