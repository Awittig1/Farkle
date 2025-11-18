import pygame
import sys
from ..game.game_engine import gameEngine
from ..game.player import Player
from ..game.dice import Dice
from ..game.scoring import Scoring
from .components.dice_renderer import DiceRenderer
from .components.buttons import Button

class PyGameUI:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Farkle Game - Mouse Controlled")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.game_engine = None
        self.current_state = "PLAYER_SETUP"
        self.dice_renderer = DiceRenderer()
        
        # Game state
        self.selected_dice = []
        self.current_roll = []
        self.turn_score = 0
        self.current_dice_count = 6
        
        # UI Elements
        self.buttons = {}
        self.setup_buttons()
        
        # Player setup
        self.player_names = []
        self.current_player_input = ""
        self.setup_active = True
        
    def setup_buttons(self):
        """Initialize all clickable buttons"""
        button_style = {
            'width': 200,
            'height': 50,
            'color': (70, 130, 180),
            'hover_color': (100, 160, 210),
            'text_color': (255, 255, 255),
            'font': self.font
        }
        
        # Gameplay buttons
        self.buttons['roll'] = Button(
            x=800, y=500, 
            text="Roll Dice", 
            **button_style
        )
        
        self.buttons['bank'] = Button(
            x=800, y=570,
            text="Bank Score", 
            **button_style
        )
        
        self.buttons['save'] = Button(
            x=800, y=640,
            text="Save Game",
            **button_style
        )
        
        # Player setup buttons
        self.buttons['add_player'] = Button(
            x=500, y=400,
            text="Add Player",
            **button_style
        )
        
        self.buttons['start_game'] = Button(
            x=500, y=480,
            text="Start Game",
            **button_style
        )
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN and self.current_state == "PLAYER_SETUP":
                    self.handle_player_input(event)
            
            # Update button hover states
            for button in self.buttons.values():
                button.update_hover(mouse_pos)
            
            self.render()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
    
    def handle_click(self, pos, button):
        """Handle all mouse clicks in the game"""
        if button != 1:  # Only left clicks
            return
            
        if self.current_state == "PLAYER_SETUP":
            self.handle_setup_click(pos)
        elif self.current_state == "PLAYING":
            self.handle_gameplay_click(pos)
        elif self.current_state == "GAME_OVER":
            self.handle_gameover_click(pos)
    
    def handle_setup_click(self, pos):
        """Handle clicks during player setup"""
        if self.buttons['add_player'].is_clicked(pos) and self.current_player_input.strip():
            self.player_names.append(self.current_player_input.strip())
            self.current_player_input = ""
            print(f"Added player: {self.player_names[-1]}")
            
        elif self.buttons['start_game'].is_clicked(pos) and len(self.player_names) >= 2:
            self.start_game()
    
    def handle_gameplay_click(self, pos):
        """Handle clicks during gameplay"""
        # Check dice selection
        if self.current_roll:
            hovered_die = self.dice_renderer.render_dice(
                self.screen, self.current_roll, self.selected_dice, pos, 100, 300
            )
            if hovered_die is not None:
                self.toggle_dice_selection(hovered_die)
        
        # Check button clicks
        if self.buttons['roll'].is_clicked(pos):
            self.roll_dice()
            
        elif self.buttons['bank'].is_clicked(pos) and self.selected_dice:
            self.bank_score()
            
        elif self.buttons['save'].is_clicked(pos):
            self.save_game()
    
    def handle_gameover_click(self, pos):
        """Handle clicks on game over screen"""
        # Could add "Play Again" or "Quit" buttons here
        pass
    
    def handle_player_input(self, event):
        """Handle keyboard input for player names during setup"""
        if event.key == pygame.K_RETURN and self.current_player_input.strip():
            self.player_names.append(self.current_player_input.strip())
            self.current_player_input = ""
        elif event.key == pygame.K_BACKSPACE:
            self.current_player_input = self.current_player_input[:-1]
        else:
            self.current_player_input += event.unicode
    
    def toggle_dice_selection(self, die_index):
        """Toggle selection of a die"""
        if die_index in self.selected_dice:
            self.selected_dice.remove(die_index)
        else:
            self.selected_dice.append(die_index)
        
        # Auto-calculate potential score
        self.calculate_potential_score()
    
    def calculate_potential_score(self):
        """Calculate score for currently selected dice"""
        if self.selected_dice and self.current_roll:
            selected_values = [self.current_roll[i] for i in self.selected_dice]
            self.turn_score = Scoring.calculateScore(selected_values)
        else:
            self.turn_score = 0
    
    def roll_dice(self):
        """Handle dice roll with mouse control"""
        if not self.game_engine or self.game_engine.gameOver:
            return
            
        # Use your existing dice logic
        self.current_roll = Dice.roll(self.current_dice_count)
        self.selected_dice = []
        self.turn_score = 0
        
        print(f"Rolled: {self.current_roll}")
        
        # Check for Farkle
        if self.is_farkle(self.current_roll):
            print("Farkle! Turn over.")
            self.farkle_penalty()
    
    def bank_score(self):
        """Bank the current turn's score"""
        if self.turn_score > 0 and self.game_engine:
            current_player = self.game_engine.players[self.game_engine.current_player_index]
            current_player.addScore(self.turn_score)
            
            print(f"{current_player.name} banked {self.turn_score} points! Total: {current_player.score}")
            
            # Check win condition
            if current_player.score >= self.game_engine.winningScore:
                self.current_state = "GAME_OVER"
                return
            
            # Reset for next turn
            self.next_turn()
    
    def farkle_penalty(self):
        """Handle Farkle penalty"""
        self.turn_score = 0
        self.current_roll = []
        self.selected_dice = []
        self.next_turn()
    
    def next_turn(self):
        """Move to next player's turn"""
        if self.game_engine:
            self.game_engine.current_player_index = (
                self.game_engine.current_player_index + 1
            ) % len(self.game_engine.players)
            self.current_dice_count = 6
            self.current_roll = []
            self.selected_dice = []
            self.turn_score = 0
    
    def start_game(self):
        """Start the main game"""
        self.game_engine = gameEngine(self.player_names)
        self.current_state = "PLAYING"
        print("Game started!")
    
    def save_game(self):
        """Save game state"""
        if self.game_engine:
            print("Save game feature to be implemented")
            # Integrate with your existing save system
    
    def is_farkle(self, dice_roll):
        """Use your existing Farkle detection"""
        from collections import Counter
        counted_roll = Counter(dice_roll)
        
        return (
            all(count < 3 for count in counted_roll.values()) and
            1 not in dice_roll and
            5 not in dice_roll and
            sorted(dice_roll) != [1, 2, 3, 4, 5, 6]
        )
    
    def render(self):
        """Render the entire game UI"""
        self.screen.fill((25, 25, 40))  # Dark background
        
        if self.current_state == "PLAYER_SETUP":
            self.render_player_setup()
        elif self.current_state == "PLAYING":
            self.render_gameplay()
        elif self.current_state == "GAME_OVER":
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_player_setup(self):
        """Render player setup screen"""
        title = self.font.render("Farkle Game - Add Players", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 100))
        
        # Current input
        input_text = self.font.render(f"Player Name: {self.current_player_input}", True, (200, 200, 200))
        self.screen.blit(input_text, (400, 300))
        
        # Player list
        players_text = self.small_font.render("Players:", True, (255, 255, 255))
        self.screen.blit(players_text, (400, 350))
        
        for i, name in enumerate(self.player_names):
            player_display = self.small_font.render(f"{i+1}. {name}", True, (180, 180, 255))
            self.screen.blit(player_display, (420, 380 + i * 25))
        
        # Render setup buttons
        self.buttons['add_player'].render(self.screen)
        self.buttons['start_game'].render(self.screen)
        
        # Instructions
        instructions = [
            "Click 'Add Player' to add current name",
            "Need at least 2 players to start",
            "Press Enter to quickly add player"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (150, 150, 150))
            self.screen.blit(text, (400, 550 + i * 25))
    
    def render_gameplay(self):
        """Render main gameplay screen"""
        if not self.game_engine:
            return
            
        current_player = self.game_engine.players[self.game_engine.current_player_index]
        
        # Player info
        self.render_text(f"Current Player: {current_player.name}", 50, 50, (255, 255, 255))
        self.render_text(f"Total Score: {current_player.score}", 50, 90, (200, 200, 100))
        self.render_text(f"Winning Score: {self.game_engine.winningScore}", 50, 130, (180, 180, 255))
        
        # Turn info
        self.render_text(f"Turn Score: {self.turn_score}", 50, 180, (100, 255, 100) if self.turn_score > 0 else (255, 100, 100))
        self.render_text(f"Dice to roll: {self.current_dice_count}", 50, 220, (200, 200, 200))
        
        # Render dice
        if self.current_roll:
            mouse_pos = pygame.mouse.get_pos()
            self.dice_renderer.render_dice(
                self.screen, self.current_roll, self.selected_dice, mouse_pos, 100, 300
            )
        
        # Render buttons
        self.buttons['roll'].render(self.screen)
        self.buttons['bank'].render(self.screen)
        self.buttons['save'].render(self.screen)
        
        # Instructions
        instructions = [
            "Click dice to select/deselect",
            "Click Roll to roll remaining dice",
            "Click Bank to score points",
            "Click Save to save game"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (150, 150, 150))
            self.screen.blit(text, (800, 350 + i * 25))
    
    def render_game_over(self):
        """Render game over screen"""
        if self.game_engine:
            winner = max(self.game_engine.players, key=lambda p: p.score)
            win_text = self.font.render(f"🎉 {winner.name} Wins! 🎉", True, (255, 215, 0))
            score_text = self.font.render(f"Final Score: {winner.score} points", True, (255, 255, 255))
            
            self.screen.blit(win_text, (self.screen_width//2 - win_text.get_width()//2, 300))
            self.screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, 350))
    
    def render_text(self, text, x, y, color):
        """Helper for rendering text"""
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))

def run_pygame():
    """Entry point for PyGame UI"""
    ui = PyGameUI()
    ui.run()