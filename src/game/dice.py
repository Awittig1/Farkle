import random
from collections import Counter
from .scoring import Scoring

class Dice:
    @staticmethod
    def roll(num_dice: int = 6) -> list[int]:
        # Roll a given number of dice and return their values.
        return [random.randint(1, 6) for _ in range(num_dice)]

    @staticmethod
    def keepDice(diceList):
        rolledCounter = Counter(diceList)
        # Check for Farkle (no scoring dice)
        if (
            all(dCount < 3 for dCount in rolledCounter.values()) and
            1 not in diceList and
            5 not in diceList and
            sorted(diceList) != [1,2,3,4,5,6]
            ):
            return (0, 6)
 
        endScore = 0
        remainingDice = sorted(diceList.copy())
        
        while True:
            print("\nWhat dice would you like to keep? (Enter as space-separated values)")
            print(f"Remaining dice to choose from: {remainingDice}")
    
            try:
                keptInput = input()
                keptDice = list(map(int, keptInput.split()))

                # Validate that kept dice are actually in remaining dice
                tempCounter = Counter(remainingDice)
                for die in keptDice:
                    if die not in tempCounter or tempCounter[die] == 0:
                        print(f"Invalid selection. Die {die} not available.")
                        raise ValueError("Invalid dice selection")
                    tempCounter[die] -= 1
                    
                diceScore = Scoring.calculateScore(keptDice)
                if diceScore == 0:
                    print("Invalid selection. No scoring dice in kept selection. Please try again.")
                    continue
                
                print(f"\nYou have chosen to keep: {keptDice} for a score of {diceScore}!")
                endScore += diceScore
                
                # Remove kept dice from remaining dice
                for die in keptDice:
                    remainingDice.remove(die)
                    
                if not remainingDice:
                    print("All dice kept! You get a fresh set of 6 dice next roll.")
                    freshDice = 6
                    return endScore, freshDice
                print(remainingDice)
                moreDiceCheck = input("\nWould you like to keep more dice? (y/n) : ").lower()
                if moreDiceCheck != 'y':
                    return endScore, len(remainingDice)

            except (ValueError, Exception) as e:
                if"Invalid dice selection" not in str(e):
                    print("Invalid input. Please enter numbers separated by spaces.")
                continue
            
    @staticmethod
    def update_dice_count(kept_dice_count: int) -> int:
        # Update the number of dice to roll next time based on kept dice.
        remaining = 6 - kept_dice_count
        return remaining if remaining > 0 else 6