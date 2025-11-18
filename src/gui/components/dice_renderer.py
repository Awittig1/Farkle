import pygame

class DiceRenderer:
    def __init__(self):
        self.dice_size = 80
        self.colors = {
            'background': (240, 240, 240),
            'dot': (30, 30, 30),
            'selected': (100, 200, 100),
            'hover': (150, 150, 255)
        }
        self.hovered_die = None
        
    def render_dice(self, screen, dice_values, selected_dice=None, mouse_pos=None, x=100, y=200):
        """Render dice on the screen with hover effects"""
        if selected_dice is None:
            selected_dice = []
        
        self.hovered_die = None
        
        for i, value in enumerate(dice_values):
            dice_x = x + i * (self.dice_size + 20)
            dice_rect = pygame.Rect(dice_x, y, self.dice_size, self.dice_size)
            is_selected = i in selected_dice
            is_hovered = dice_rect.collidepoint(mouse_pos) if mouse_pos else False
            
            if is_hovered:
                self.hovered_die = i
            
            # Choose color based on state
            if is_selected:
                color = self.colors['selected']
            elif is_hovered:
                color = self.colors['hover']
            else:
                color = self.colors['background']
            
            # Draw dice with smooth corners (PyGame CE has better rendering)
            pygame.draw.rect(screen, color, dice_rect, border_radius=12)
            pygame.draw.rect(screen, (0, 0, 0), dice_rect, width=2, border_radius=12)
            
            # Draw dots based on dice value
            self.draw_dots(screen, value, dice_x, y)
            
        return self.hovered_die
    
    def draw_dots(self, screen, value, x, y):
        """Draw dice dots using PyGame CE's improved rendering"""
        dot_radius = 8
        positions = {
            1: [(self.dice_size // 2, self.dice_size // 2)],
            2: [(20, 20), (60, 60)],
            3: [(20, 20), (40, 40), (60, 60)],
            4: [(20, 20), (60, 20), (20, 60), (60, 60)],
            5: [(20, 20), (60, 20), (40, 40), (20, 60), (60, 60)],
            6: [(20, 20), (20, 40), (20, 60), (60, 20), (60, 40), (60, 60)]
        }
        
        for pos in positions[value]:
            dot_pos = (x + pos[0], y + pos[1])
            # PyGame CE has improved circle rendering
            pygame.draw.circle(screen, self.colors['dot'], dot_pos, dot_radius)
            # Add a slight highlight for better visual appeal
            pygame.draw.circle(screen, (255, 255, 255), dot_pos, dot_radius - 6)