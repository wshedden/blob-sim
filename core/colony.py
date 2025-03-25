class Colony:
    def __init__(self, founder, colour):
        self.id = f"colony_{founder.id}"
        self.members = {founder}
        self.territory = set()
        self.colour = colour

    def add_member(self, blob):
        self.members.add(blob)
        self.colour = self._blend(self.colour, blob.colour_bias)

    def claim(self, cell):
        self.territory.add(cell)

    def owns(self, cell):
        return cell in self.territory

    def _blend(self, c1, c2):
        return tuple((c1[i] + c2[i]) // 2 for i in range(3))
