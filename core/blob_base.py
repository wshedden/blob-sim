import random
import uuid
from pygame.math import Vector2
from core.grid import hex_center


class Blob:
    def __init__(self, col, row):
        self.current_cell = (col, row)
        self.position = Vector2(hex_center(col, row))
        self.path = []
        self.progress = 1

        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.colour_bias = tuple(min(255, int(c + random.randint(-20, 20))) for c in self.color)

        # Identity & social state
        self.id = str(uuid.uuid4())[:6]
        self.markov_state = "Move"
        self.state = "Idle"
        self.decision = "Idle"
        self.path = []
        self.conversation_partner = None
        self.conversation_timer = 0
        self.convo_cooldown = 0
        self.last_conversed_with = None
        self.conversation_lines = []

        # Personality
        self.sociability = round(random.uniform(0.0, 1.0), 2)
        self.territorial = round(random.uniform(0.0, 1.0), 2)
        self.loyalty = round(random.uniform(0.0, 1.0), 2)
        self.boldness = round(random.uniform(0.0, 1.0), 2)

        # Colony state
        self.colony = None
        self.wants_colony = False


# --- Method Binding ---
import core.blob_behavior as blob_behavior
import core.blob_draw as blob_draw

Blob.update = blob_behavior.update
Blob.decide_path = blob_behavior.decide_path
Blob.get_nearby_blobs = blob_behavior.get_nearby_blobs
Blob.markov_decision = blob_behavior.markov_decision
Blob.wants_colony_with = blob_behavior.wants_colony_with
Blob._colony_chat = blob_behavior._colony_chat

Blob.draw = blob_draw.draw
Blob.draw_conversation = blob_draw.draw_conversation
