import pygame

class Buttons:
    def __init__(self, 
                x: 100, 
                y: 100, 
                width=200, 
                height=50, 
                text="Button", 
                color=(70, 130, 180), 
                hover_color=(100, 160, 210), 
                text_color=(255, 255, 255), 
                font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font or pygame.font.Font(None, 32)
        self.is_hovered = False
        
    def update_hover(self, mouse_pos):
        """Update hover state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos)
        
    def render(self, screen):
        """Render the button"""
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button with rounded corners
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=8)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)