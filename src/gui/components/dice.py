import pygame
import os
from typing import Optional, Tuple
from src.game.dice import Die

class DiceSpot:
    """
    A visual spot on the screen that displays a die and handles mouse interactions.
    """
    
    def __init__(self, 
                 x: int, 
                 y: int, 
                 size: int = 80,
                 spot_id: int = 0):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.spot_id = spot_id
        self.die: Optional[Die] = None
        self.is_hovered = False
        self.is_selected = False
        
        # Load dice images or create fallback
        self.dice_images = self._load_dice_images()
        
        # Colors for different states
        self.colors = {
            'default': (200, 200, 200),
            'hover': (150, 200, 255),
            'selected': (100, 255, 100),
            'empty': (100, 100, 100)
        }
    
    def _load_dice_images(self) -> dict:
        """Load dice images or create fallback surfaces."""
        images = {}
        
        # Create simple colored dice surfaces for each value
        for value in range(1, 7):
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            
            # Different colors for different dice values
            dice_colors = {
                1: (255, 255, 255),   # White
                2: (255, 200, 200),   # Light red
                3: (200, 255, 200),   # Light green
                4: (200, 200, 255),   # Light blue
                5: (255, 255, 200),   # Light yellow
                6: (255, 200, 255)    # Light purple
            }
            
            # Draw dice background
            pygame.draw.rect(surface, dice_colors[value], (0, 0, self.size, self.size), border_radius=10)
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.size, self.size), 2, border_radius=10)
            
            # Draw dots based on value
            dot_color = (0, 0, 0)
            dot_radius = self.size // 10
            
            # Dot positions (relative coordinates)
            dot_positions = {
                1: [(0.5, 0.5)],
                2: [(0.25, 0.25), (0.75, 0.75)],
                3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
                4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
                5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
                6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]
            }
            
            for pos in dot_positions.get(value, []):
                dot_x = int(pos[0] * self.size)
                dot_y = int(pos[1] * self.size)
                pygame.draw.circle(surface, dot_color, (dot_x, dot_y), dot_radius)
            
            images[value] = surface
        
        # Add empty die image
        empty_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(empty_surface, (150, 150, 150), (0, 0, self.size, self.size), border_radius=10)
        pygame.draw.rect(empty_surface, (100, 100, 100), (0, 0, self.size, self.size), 2, border_radius=10)
        pygame.draw.line(empty_surface, (100, 100, 100), (10, 10), (self.size-10, self.size-10), 3)
        pygame.draw.line(empty_surface, (100, 100, 100), (self.size-10, 10), (10, self.size-10), 3)
        images[0] = empty_surface  # 0 represents empty
        
        return images
    
    def set_die(self, die: Optional[Die]) -> None:
        """Set the die for this spot."""
        self.die = die
        self.is_selected = die.selected if die else False
    
    def get_die_value(self) -> int:
        """Get the current die value, returns 0 if no die."""
        if self.die and hasattr(self.die, 'value'):
            return self.die.value
        return 0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for this dice spot.
        Returns True if the die was clicked.
        """
        if event.type == pygame.MOUSEMOTION:
            # Check hover state
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.die:
                # Toggle selection state
                self.die.toggle_selected()
                self.is_selected = self.die.selected
                return True
        
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the dice spot and its die."""
        # Determine background color based on state
        if not self.die:
            bg_color = self.colors['empty']
        elif self.is_selected:
            bg_color = self.colors['selected']
        elif self.is_hovered:
            bg_color = self.colors['hover']
        else:
            bg_color = self.colors['default']
        
        # Draw spot background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=12)
        
        # Draw the die image
        die_value = self.get_die_value()
        if die_value in self.dice_images:
            surface.blit(self.dice_images[die_value], self.rect)
        
        # Draw selection indicator
        if self.is_selected:
            selection_rect = self.rect.inflate(-8, -8)
            pygame.draw.rect(surface, (0, 255, 0), selection_rect, 3, border_radius=8)
    
    def update(self, current_time: int) -> None:
        """Update any animations or timed behaviors."""
        # Can be used for animations later
        pass