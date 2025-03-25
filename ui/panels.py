import pygame
from core.constants import (
    PANEL_WIDTH, GRID_PIXEL_WIDTH, MARGIN, WINDOW_HEIGHT,
    PANEL_BG, DETAIL_PANEL_BG, TEXT_COLOR
)

def draw_decision_panel(surface, blobs):
    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + MARGIN, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)

    font = pygame.font.SysFont(None, 20)
    x = panel_rect.x + 10
    y = 20
    icon_radius = 8
    spacing = 40

    for i, blob in enumerate(blobs):
        pygame.draw.circle(surface, blob.color, (x, y), icon_radius)

        if blob.path:
            status = ">>"
        elif blob.decision == "No path":
            status = "X"
        else:
            status = "||"

        status_surf = font.render(status, True, TEXT_COLOR)
        surface.blit(status_surf, (x + icon_radius + 10, y - status_surf.get_height() // 2))

        label = font.render(str(i + 1), True, TEXT_COLOR)
        surface.blit(label, (x - icon_radius - 20, y - label.get_height() // 2))

        y += spacing


def draw_personality_panel(surface, blobs):
    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + MARGIN + PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, DETAIL_PANEL_BG, panel_rect)

    font = pygame.font.SysFont(None, 20)
    x = panel_rect.x + 10
    y = 20

    for i, blob in enumerate(blobs):
        name = f"Blob {i+1}"
        if blob.colony:
            name += f" [{blob.colony.id}]"
        name_text = font.render(name, True, TEXT_COLOR)
        surface.blit(name_text, (x, y))
        y += name_text.get_height() + 2

        for label, value in [
            ("Sociability", blob.sociability),
            ("Territorial", blob.territorial),
            ("Loyalty", blob.loyalty),
            ("Boldness", blob.boldness),
        ]:
            line = font.render(f"- {label}: {value:.2f}", True, TEXT_COLOR)
            surface.blit(line, (x, y))
            y += line.get_height() + 1

        y += 10
