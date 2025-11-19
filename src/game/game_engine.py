# game_engine.py
from .player import Player
from .dice import Dice
from .scoring import Scoring
from .turnCheck import turnCheck
from collections import Counter

class GameState:
    def __init__(self):
        self.current_player_index = -1
        self.current_dice_count = 6
        self.temp_score = 0
        self.dice_roll = []
        self.remaining_dice = []
        self.game_over = False
        self.winner = None
        self.last_action = ""

class gameEngine:
    def __init__(self, players: list[str], winning_score: int = 10000):
        self.players = [Player(name) for name in players]
        self.winning_score = winning_score
        self.state = GameState()
        
    def start_game(self):
        """Initialize game state"""
        self.state.current_player_index = -1
        self.state.current_dice_count = 6
        self.state.temp_score = 0
        self.state.game_over = False
        self.state.winner = None
        
    def next_turn(self):
        """Move to next player's turn"""
        self.state.current_player_index = turnCheck.turnCheck(
            self.players, self.state.current_player_index
        )
        self.state.current_dice_count = 6
        self.state.temp_score = 0
        self.state.dice_roll = []
        self.state.remaining_dice = []
        
    def roll_dice(self):
        """Roll dice for current turn"""
        if self.state.game_over:
            return False
            
        self.state.dice_roll = Dice.roll(self.state.current_dice_count)
        self.state.remaining_dice = self.state.dice_roll.copy()
        self.state.last_action = "roll"
        
        # Check for Farkle
        if Dice.is_farkle(self.state.dice_roll):
            self.state.temp_score = 0
            self.state.last_action = "farkle"
            return True
            
        return True
    
    def validate_keep_dice(self, kept_dice: list[int]) -> tuple[bool, str]:
        """Validate if kept dice selection is valid"""
        return Dice.validate_kept_dice(kept_dice, self.state.remaining_dice)
    
# In your game_engine.py, update the keep_dice method:

    def keep_dice(self, kept_dice: list[int]) -> bool:
        """Keep selected dice and update score"""
        is_valid, message = self.validate_keep_dice(kept_dice)
        if not is_valid:
            return False
            
        roll_score, new_remaining = Dice.calculate_kept_score(kept_dice, self.state.remaining_dice)
        self.state.temp_score += roll_score
        self.state.remaining_dice = new_remaining
        self.state.current_dice_count = len(self.state.remaining_dice)
        self.state.last_action = "keep"
        
        # Update the dice_roll to show only remaining dice
        self.state.dice_roll = self.state.remaining_dice.copy()
        
        # If all dice kept, reset to 6
        if self.state.current_dice_count == 0:
            self.state.current_dice_count = 6
            
        return True
            
        roll_score, new_remaining = Dice.calculate_kept_score(kept_dice, self.state.remaining_dice)
        self.state.temp_score += roll_score
        self.state.remaining_dice = new_remaining
        self.state.current_dice_count = len(self.state.remaining_dice)
        self.state.last_action = "keep"
        
        # If all dice kept, reset to 6
        if self.state.current_dice_count == 0:
            self.state.current_dice_count = 6
            
        return True
    
    def bank_score(self):
        """Bank current turn score"""
        if self.state.game_over:
            return False
            
        current_player = self.players[self.state.current_player_index]
        current_player.addScore(self.state.temp_score)
        
        # Check for win
        if current_player.score >= self.winning_score:
            self.state.game_over = True
            self.state.winner = current_player.name
            self.state.last_action = "win"
        else:
            self.state.last_action = "bank"
            
        return True
    
    def get_current_player(self):
        """Get current player object"""
        if self.state.current_player_index < 0:
            return None
        return self.players[self.state.current_player_index]
    
    def get_game_state(self):
        """Return current game state for GUI"""
        return {
            'current_player': self.get_current_player(),
            'current_player_index': self.state.current_player_index,
            'dice_roll': self.state.dice_roll,
            'remaining_dice': self.state.remaining_dice,
            'temp_score': self.state.temp_score,
            'current_dice_count': self.state.current_dice_count,
            'scores': {player.name: player.score for player in self.players},
            'game_over': self.state.game_over,
            'winner': self.state.winner,
            'last_action': self.state.last_action
        }