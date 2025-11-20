class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def addScore(self, points: int) -> None:
        self.score += points

    def __str__(self) -> str:
        return f"{self.name}: {self.score} points"

    def serialize(self) -> str:
        return f"{self.name}:{self.score}"