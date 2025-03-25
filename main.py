import sys
import random
import pygame

from core.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR,
    GRID_COLS, GRID_ROWS, FPS, HEX_COLOR, GRID_LINE_COLOR
)
from core.grid import hex_center, hex_corners
from core.blob_base import Blob
from core.colony import Colony
from ui.panels import draw_decision_panel, draw_personality_panel


# Reset button rectangle
RESET_BUTTON = pygame.Rect(10, 10, 100, 30)

# Global state
blobs = []
colonies = []
tile_owner = {}
tile_colour = {}


def new_session():
    global blobs, colonies, tile_owner, tile_colour

    blobs = []
    taken_cells = set()
    for _ in range(5):
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        if (col, row) not in taken_cells:
            blobs.append(Blob(col, row))
            taken_cells.add((col, row))

    colonies = []
    tile_owner = {}
    tile_colour = {}


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Blob Simulation with Colonies")
    clock = pygame.time.Clock()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  
    new_session()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if RESET_BUTTON.collidepoint(event.pos):
                    new_session()

        occupied_cells = {blob.current_cell for blob in blobs}

        for blob in blobs:
            blob.update(blobs, occupied_cells)

            if blob.colony and blob.current_cell not in blob.colony.territory:
                blob.colony.claim(blob.current_cell)
                tile_owner[blob.current_cell] = blob.colony.id
                tile_colour[blob.current_cell] = blob.colony.colour

        # Draw everything
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

        # Draw Reset Button LAST so it's on top
        pygame.draw.rect(screen, (200, 50, 50), RESET_BUTTON)
        font = pygame.font.SysFont(None, 20)
        text = font.render("RESET", True, (255, 255, 255))
        screen.blit(text, (RESET_BUTTON.x + 15, RESET_BUTTON.y + 5))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
