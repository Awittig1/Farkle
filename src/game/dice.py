# dice.py
import random
from collections import Counter
from .scoring import Scoring

class Dice:
    @staticmethod
    def roll(num_dice: int = 6) -> list[int]:
        return [random.randint(1, 6) for _ in range(num_dice)]

    @staticmethod
    def validate_kept_dice(kept_dice: list[int], available_dice: list[int]) -> tuple[bool, str]:
        """
        Validate if kept dice are available and scoring
        Returns: (is_valid: bool, message: str)
        """
        available_counter = Counter(available_dice)
        kept_counter = Counter(kept_dice)
        
        # Check if all kept dice are available
        for die, count in kept_counter.items():
            if available_counter[die] < count:
                return False, f"Invalid selection. Die {die} not available."
        
        # Check if kept dice score points
        dice_score = Scoring.calculateScore(kept_dice)
        if dice_score == 0:
            return False, "Invalid selection. No scoring dice in kept selection."
        
        return True, "Valid selection"

    @staticmethod
    def calculate_kept_score(kept_dice: list[int], available_dice: list[int]) -> tuple[int, list[int]]:
        """
        Calculate score for kept dice and return remaining dice
        Returns: (score: int, remaining_dice: list[int])
        """
        score = Scoring.calculateScore(kept_dice)
        remaining_dice = available_dice.copy()
        
        # Remove kept dice from remaining
        for die in kept_dice:
            remaining_dice.remove(die)
        
        return score, remaining_dice

    @staticmethod
    def is_farkle(dice_list: list[int]) -> bool:
        """
        Check if the roll is a Farkle (no scoring dice)
        """
        counted_roll = Counter(dice_list)
        return (
            all(count < 3 for count in counted_roll.values()) and
            1 not in dice_list and
            5 not in dice_list and
            sorted(dice_list) != [1, 2, 3, 4, 5, 6]
        )

    @staticmethod
    def update_dice_count(kept_dice_count: int) -> int:
        remaining = 6 - kept_dice_count
        return remaining if remaining > 0 else 6