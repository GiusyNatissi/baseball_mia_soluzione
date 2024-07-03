from dataclasses import dataclass
@dataclass
class Team:
    ID:int
    year: int
    teamCode: str
    name: str
    def __hash__(self):
        return hash(self.ID)
    def __eq__(self, other):
        return self.ID == other.ID
    def __str__(self):
        return f"{self.teamCode} ({self.name})"
