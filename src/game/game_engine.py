from .player import Player
from .dice import Dice
from .scoring import Scoring
from .turnCheck import turnCheck
from collections import Counter

class gameEngine:
    # Initialize the game with players and winning score
    def __init__(self, players: list[str]):
        # Create Player instances for each player name
        self.players = [Player(name) for name in players]
        # Set the winning score
        self.winningScore = 10000  # Default value is 10000
        
        self.gameOver = False
        # Use a loop to force valid input
        while True:
            try:
                print(f"Either press Enter to accept the default winning score of {self.winningScore}\nor")
                scoreInput = input("Enter the winning score : ")
                if not scoreInput:
                    print(f"\nSetting winning score to default: {self.winningScore}!")
                    break

                trueScore = int(scoreInput)
                
                if trueScore < 1000:
                    print("\nWinning score must be at least 1000. Please try again.")
                    continue
                
                self.winningScore = trueScore
                break
        
            except ValueError:
                print("\nInvalid input. Please enter a valid whole number without commas.")
                continue
            
    def startGame(self):
        print("")
        for player in self.players:
            print(f"{player.name} - {player.score} points.")
        # Start the game loop
        turnIndex = -1
        currentDiceCount = 6
        tempScore = 0
        while not self.gameOver:
            turnIndex = turnCheck.turnCheck(self.players, turnIndex)
            playerTurn = True
            currentPlayer = self.players[turnIndex]
            
            print(f"\n--- {currentPlayer.name}'s turn! ---")
            print(f"Current score: {currentPlayer.score}\n")
            
            while playerTurn == True:
                print(f"Rolling {currentDiceCount} dice!")
                diceRoll = Dice.roll(currentDiceCount)
                print(f"Rolled: {diceRoll}!")
                countedRoll = Counter(diceRoll)
                # Check for Farkle
                if (
                    all(count < 3 for count in countedRoll.values()) and
                    1 not in diceRoll and
                    5 not in diceRoll and
                    sorted(diceRoll) != [1,2,3,4,5,6]
                    ):
                    print("Farkle! No scoring dice rolled. Turn over, no points earned.")
                    tempScore = 0
                    playerTurn = False
            
                rollScore, currentDiceCount = Dice.keepDice(diceRoll)
                tempScore += rollScore
                print(f"Current score this turn: {tempScore}")
                    
                # Check if player wants to continue or bank score
                while True:
                    choice = input("\nWould you like to end your turn? y/n : ").lower()
                    if choice not in ['y', 'n']:
                        print(choice)
                        continue
                    if choice == 'y':
                        currentPlayer.addScore(tempScore)
                        print(f"{currentPlayer.name}'s total score: {currentPlayer.score}")
                        # Check for winning condition
                        if currentPlayer.score >= self.winningScore:
                            print(f"\n🎉 {currentPlayer.name} wins with {currentPlayer.score} points! 🎉")
                            self.gameOver = True
                            break
                        currentDiceCount = 6
                        playerTurn = False
                        break
                    elif choice == 'n':
                        break
                    else:
                        if currentDiceCount == 0:
                            currentDiceCount = 2
                        break
                if self.gameOver:
                    break