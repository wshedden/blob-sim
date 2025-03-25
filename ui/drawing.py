import math
import pygame

def draw_arrow(surface, start, end, color, width=3, head_length=10, head_angle=30):
    """
    Draw a line with an arrowhead pointing from start to end.
    """
    pygame.draw.line(surface, color, start, end, width)
    
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left_angle = angle + math.radians(head_angle)
    right_angle = angle - math.radians(head_angle)

    left_point = (
        end[0] - head_length * math.cos(left_angle),
        end[1] - head_length * math.sin(left_angle)
    )
    right_point = (
        end[0] - head_length * math.cos(right_angle),
        end[1] - head_length * math.sin(right_angle)
    )

    pygame.draw.polygon(surface, color, [end, left_point, right_point])
