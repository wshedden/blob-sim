import pygame
from core.grid import hex_center
from core.constants import EYE_COLOR, TARGET_OUTLINE_WIDTH
from ui.drawing import draw_arrow

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
        return

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
