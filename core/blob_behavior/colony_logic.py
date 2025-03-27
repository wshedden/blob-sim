def claim_tile(self):
    if self.colony and self.current_cell not in self.colony.territory:
        self.colony.claim(self.current_cell)
        
