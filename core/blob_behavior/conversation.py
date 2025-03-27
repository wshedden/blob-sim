def wants_colony_with(self, other):
    return (
        self.colony is None and
        other.colony is None and
        self.sociability > 0.3 and
        other.loyalty > 0.3
    )

def _colony_chat(self, other):
    self.state = other.state = "Talking"
    self.conversation_partner = other
    other.conversation_partner = self
    self.last_conversed_with = other
    other.last_conversed_with = self
    self.conversation_timer = other.conversation_timer = 40
    self.convo_cooldown = other.convo_cooldown = 180
    self.conversation_lines = [("Glad we formed this colony.", self.color)]
    other.conversation_lines = [("Yeah. Feels right.", other.color)]