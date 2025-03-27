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

        self.sociability = round(random.uniform(0.3, 1.0), 2)
        self.territorial = round(random.uniform(0.0, 1.0), 2)
        self.loyalty = round(random.uniform(0.3, 1.0), 2)
        self.boldness = round(random.uniform(0.0, 1.0), 2)

        self.colony = None
        self.wants_colony = False

# Bind external methods
from core.blob_behavior import (
    markov_decision,
    decide_path,
    claim_tile,
    wants_colony_with,
    _colony_chat,
    is_loyal,
    is_bold,
)
import core.blob_draw as blob_draw

Blob.markov_decision = markov_decision
Blob.decide_path = decide_path
Blob.claim_tile = claim_tile
Blob.wants_colony_with = wants_colony_with
Blob._colony_chat = _colony_chat
Blob.is_loyal = is_loyal
Blob.is_bold = is_bold

# Bind draw and draw_conversation methods
Blob.draw = blob_draw.draw
Blob.draw_conversation = blob_draw.draw_conversation

import core.blob_behavior as bh

Blob.update = bh.update
Blob.decide_path = bh.decide_path
Blob.get_nearby_blobs = bh.get_nearby_blobs
Blob.markov_decision = bh.markov_decision
Blob.wants_colony_with = bh.wants_colony_with
Blob._colony_chat = bh._colony_chat
Blob.claim_tile = bh.claim_tile  # if you're using that too
Blob.is_loyal = bh.is_loyal
Blob.is_bold = bh.is_bold
Blob.draw = blob_draw.draw