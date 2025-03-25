import pygame
from core.constants import (
    PANEL_WIDTH, PANEL_BG, DETAIL_PANEL_BG, TEXT_COLOR,
    GRID_PIXEL_WIDTH, WINDOW_HEIGHT, MARGIN
)



def wrap_text(text, font, max_width):
    """
    Break text into lines that fit within max_width.
    """
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def draw_decision_panel(surface, blobs):
    """
    Draws a panel with simple visual indicators for each blob's decision.
    """
    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + MARGIN, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)

    font = pygame.font.SysFont(None, 20)

    x = panel_rect.x + 20
    y = 20
    icon_radius = 8
    spacing = 40

    for i, blob in enumerate(blobs):
        # Draw blob colour circle
        pygame.draw.circle(surface, blob.color, (x, y), icon_radius)

        # Draw movement status indicator
        if blob.path:
            status = ">>"
        elif blob.decision == "No path":
            status = "X"
        elif blob.decision == "No options":
            status = "X"
        else:
            status = "||"

        status_surf = font.render(status, True, TEXT_COLOR)
        surface.blit(status_surf, (x + icon_radius + 10, y - status_surf.get_height() // 2))

        # Optional: show blob number
        label = font.render(str(i + 1), True, TEXT_COLOR)
        surface.blit(label, (x - icon_radius - 20, y - label.get_height() // 2))

        y += spacing


def draw_personality_panel(surface, blobs):
    """
    Draws the right-hand panel showing each blob's personality traits.
    """
    from core.constants import PANEL_WIDTH, GRID_PIXEL_WIDTH, MARGIN, WINDOW_HEIGHT, DETAIL_PANEL_BG, TEXT_COLOR

    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + MARGIN + PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, DETAIL_PANEL_BG, panel_rect)

    font = pygame.font.SysFont(None, 20)
    x = panel_rect.x + 10
    y = 20

    for i, blob in enumerate(blobs):
        name_text = font.render(f"Blob {i+1}", True, TEXT_COLOR)
        surface.blit(name_text, (x, y))
        y += name_text.get_height() + 2

        for trait_name, value in [
            ("Sociability", blob.sociability),
            ("Territorial", blob.territorial),
            ("Loyalty", blob.loyalty),
            ("Boldness", blob.boldness),
        ]:
            trait_text = font.render(f"- {trait_name}: {value:.2f}", True, TEXT_COLOR)
            surface.blit(trait_text, (x, y))
            y += trait_text.get_height() + 1

        y += 10
