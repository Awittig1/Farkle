class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def addScore(self, points: int) -> None:
        self.score += points

    def __str__(self) -> str:
        return f"{self.name}: {self.score} points"

    @staticmethod
    def getPlayers():
        while True:
            try:
                numPlayers = int(input("How many players? "))
            except:
                print("Invalid input. Please enter a valid whole number.")
                continue
            if numPlayers < 2:
                print("At least 2 players are required to play. Please try again.")
                continue
            playerNames = [input(f"Enter name for Player {i+1} : ") for i in range(numPlayers)]
            return(playerNames)