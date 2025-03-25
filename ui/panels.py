import pygame
from core.constants import (
    PANEL_WIDTH, PANEL_BG, DETAIL_PANEL_BG, TEXT_COLOR,
    GRID_PIXEL_WIDTH, WINDOW_HEIGHT
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
    Draw a vertical panel showing each blob's current decision.
    """
    big_font = pygame.font.SysFont(None, 24)
    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + 50, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)

    x = panel_rect.x + 10
    y = 20
    for i, blob in enumerate(blobs):
        lines = wrap_text(f"Blob {i+1}: {blob.decision}", big_font, PANEL_WIDTH - 20)
        for line in lines:
            rendered = big_font.render(line, True, TEXT_COLOR)
            surface.blit(rendered, (x, y))
            y += rendered.get_height() + 2
        y += 10

def draw_decision_detail_panel(surface, blobs):
    """
    Draw a second panel showing path details for each blob.
    """
    font = pygame.font.SysFont(None, 20)
    panel_rect = pygame.Rect(GRID_PIXEL_WIDTH + 50 + PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, DETAIL_PANEL_BG, panel_rect)

    x = panel_rect.x + 10
    y = 20
    for i, blob in enumerate(blobs):
        detail = f"Path: {blob.path}"
        lines = wrap_text(f"Blob {i+1}: {detail}", font, PANEL_WIDTH - 20)
        for line in lines:
            rendered = font.render(line, True, TEXT_COLOR)
            surface.blit(rendered, (x, y))
            y += rendered.get_height() + 2
        y += 10
