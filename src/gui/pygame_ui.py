import pygame
import sys
import os

#ez find (100, 160, 210)(60, 110, 150)
# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game_engine import gameEngine
from game.dice import Dice

# Initialize PyGame and load font
pygame.init()

try:
    whatFont = pygame.font.Font("src/gui/components/fonts/TitanOne-Regular.ttf", 36)
except:
    print("Custom font not found, using system font")
    whatFont = None

print("Using font:", whatFont)

def get_font(size):
    """Helper function to get font with proper handling of None"""
    if whatFont:
        try:
            return pygame.font.Font("src/gui/components/fonts/TitanOne-Regular.ttf", size)
        except:
            return pygame.font.SysFont(None, size)
    else:
        return pygame.font.SysFont(None, size)

def intro_screen(screen):
    # Load dice images
    try:
        d1 = pygame.image.load("src/gui/components/pictures/die_1.png")
        d1 = pygame.transform.scale(d1, (d1.get_width() / 2.5, d1.get_height() / 2.5))
        d2 = pygame.image.load("src/gui/components/pictures/die_2.png")
        d2 = pygame.transform.scale(d2, (d2.get_width() / 2.5, d2.get_height() / 2.5))
        d3 = pygame.image.load("src/gui/components/pictures/die_3.png")
        d3 = pygame.transform.scale(d3, (d3.get_width() / 2.5, d3.get_height() / 2.5))
        d4 = pygame.image.load("src/gui/components/pictures/die_4.png")
        d4 = pygame.transform.scale(d4, (d4.get_width() / 2.5, d4.get_height() / 2.5))
        d5 = pygame.image.load("src/gui/components/pictures/die_5.png")
        d5 = pygame.transform.scale(d5, (d5.get_width() / 2.5, d5.get_height() / 2.5))
        d6 = pygame.image.load("src/gui/components/pictures/die_6.png")
        d6 = pygame.transform.scale(d6, (d6.get_width() / 2.5, d6.get_height() / 2.5))
    except:
        # Placeholder dice if images can't be loaded
        dice_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                      (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        dice = []
        for color in dice_colors:
            die = pygame.Surface((80, 80))
            die.fill(color)
            dice.append(die)
    else:
        dice = [d1, d2, d3, d4, d5, d6]
    
    # Font setup
    title_font = get_font(172)
    button_font = get_font(36)
    rules_font = get_font(16)
    copyright_font = get_font(14)  # Smaller font for copyright notice
    
    # Button definitions
    button_width, button_height = 200, 60
    button_x = screen.get_width() // 2 - button_width // 2
    
    play_button = pygame.Rect(button_x, 380, button_width, button_height)
    rules_button = pygame.Rect(button_x, 460, button_width, button_height)
    quit_button = pygame.Rect(button_x, 540, button_width, button_height)
    
    # Rules text
    rules_text = [
        "Farkle Rules:",
        "- Roll 6 dice to start",
        "- Combine groups of 3-6 of a kind",
        "- 1s = 100 pts, 5s = 50 pts by themselves",
        "- Three 1s = 1000 pts, three of a kind = 100 x face value",
        "- A straight (1-6) = 1500 pts",
        "- Four Pair = Three pair x 2 pts",
        "- Five Pair = Three pair x 2 pts",
        "- Six Pair = Three pair x 2 pts",
        "- Two sets of three = 2500 pts",
        "- You can bank your points or risk rolling again",
        "- If you roll and score no points, you FARKLE and lose your turn"
    ]
    
    # Animation variables - updated for falling animation
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Initialize dice with staggered starting positions
    import random
    dice_data = []
    for i in range(6):
        dice_data.append({
            'x': random.randint(100, screen_width - 100),
            'y': random.randint(-600, -100),  # Start much higher for smoother entry
            'speed': random.uniform(60, 40),  # Slower initial speed
            'angle': 0,
            'rotation_speed': random.uniform(1, 3),
            'delay': i * 10  # Stagger the start of each die
        })
    
    clock = pygame.time.Clock()
    frame_count = 0
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    return "play"
                elif quit_button.collidepoint(mouse_pos):
                    return "quit"
        
        frame_count += 1
        
        # Update dice animation - falling and rotation
        for i, die in enumerate(dice_data):
            # Only start moving after the delay period
            if frame_count > die['delay']:
                # Update rotation
                die['angle'] = (die['angle'] + die['rotation_speed']) % 360
                
                # Update position (falling down)
                die['y'] += die['speed']
                
                # Gradually increase speed for natural falling effect
                die['speed'] = random.uniform(5,10)  # Cap at max speed
                
                # If dice falls below screen, reset to top
                if die['y'] > screen_height + 100:
                    die['y'] = random.randint(-600, -100)
                    die['x'] = random.randint(100, screen_width - 100)
                    die['speed'] = random.uniform(1, 2)  # Reset to slower speed
        
        # Draw everything
        screen.fill((255, 235, 219))
        
        # Draw title
        title_text = title_font.render("FARKLE", True, (50, 50, 150))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))
        
        # Draw copyright notice in top right corner
        copyright_text = copyright_font.render("Font: Titan One by Rodrigo Fuenzalida (OFL)", True, (135, 75, 25))
        screen.blit(copyright_text, (screen.get_width() - copyright_text.get_width() - 20, 20))
        
        # Draw animated falling dice
        for i, die in enumerate(dice_data):
            # Only draw if the die has started moving (after its delay)
            if frame_count > die['delay']:
                rotated_dice = pygame.transform.rotate(dice[i], die['angle'])
                new_rect = rotated_dice.get_rect(center=(die['x'] + dice[i].get_width() // 2, 
                                                        die['y'] + dice[i].get_height() // 2))
                screen.blit(rotated_dice, new_rect.topleft)
        
        # Draw buttons with hover effects
        button_color = (100, 160, 210)
        hover_color = (60, 110, 150)
        
        # Play button
        play_color = hover_color if play_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, play_color, play_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), play_button, 2, border_radius=10)
        play_text = button_font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, 
                               play_button.centery - play_text.get_height() // 2))
        
        # Rules button
        rules_color = hover_color if rules_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, rules_color, rules_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), rules_button, 2, border_radius=10)
        rules_button_text = button_font.render("Rules", True, (255, 255, 255))
        screen.blit(rules_button_text, (rules_button.centerx - rules_button_text.get_width() // 2, 
                                       rules_button.centery - rules_button_text.get_height() // 2))
        
        # Quit button
        quit_color = hover_color if quit_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, quit_color, quit_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), quit_button, 2, border_radius=10)
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, 
                               quit_button.centery - quit_text.get_height() // 2))
        
        # Show rules if hovering over rules button
        if rules_button.collidepoint(mouse_pos):
            rules_bg = pygame.Rect(40, 550, 575, 230)
            pygame.draw.rect(screen, (255, 255, 255), rules_bg, border_radius=10)
            pygame.draw.rect(screen, (30, 30, 30), rules_bg, 2, border_radius=10)
            
            for i, line in enumerate(rules_text):
                rules_line = rules_font.render(line, True, (30, 30, 30))
                screen.blit(rules_line, (rules_bg.x + 10, rules_bg.y + 15 + i * 17))
        
        pygame.display.flip()
        clock.tick(60)

def player_count_screen(screen):
    """Screen to select number of players"""
    font = get_font(48)
    button_font = get_font(36)
    title_font = get_font(72)
    
    clock = pygame.time.Clock()
    selected_players = 2  # Default
    
    # Player count buttons (2-6 players) 
    player_buttons = []
    for i in range(2, 7):
        button = pygame.Rect(400 + (i-2) * 120, 300, 80, 80)
        player_buttons.append((button, i))
    
    continue_button = pygame.Rect(screen.get_width() // 2 - 100, 500, 200, 60)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check player count buttons
                for button, count in player_buttons:
                    if button.collidepoint(mouse_pos):
                        selected_players = count
                
                # Check continue button
                if continue_button.collidepoint(mouse_pos):
                    return selected_players
        
        # Draw
        screen.fill((255, 235, 219))
        
        # Title
        title = title_font.render("Select Players", True, (50, 50, 150))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
        
        # Instruction
        instruction = font.render("How many players?", True, (30, 30, 30))
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, 200))
        
        # Player count buttons
        for button, count in player_buttons:
            color = (60, 110, 150) if count == selected_players else (100, 160, 210)
            pygame.draw.rect(screen, color, button, border_radius=10)
            pygame.draw.rect(screen, (30, 30, 30), button, 2, border_radius=10)
            
            count_text = font.render(str(count), True, (255, 255, 255))
            screen.blit(count_text, (button.centerx - count_text.get_width() // 2, 
                                   button.centery - count_text.get_height() // 2))
        
        # Continue button 
        continue_color = (60, 110, 150) if continue_button.collidepoint(mouse_pos) else (100, 160, 210)
        pygame.draw.rect(screen, continue_color, continue_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), continue_button, 2, border_radius=10)
        continue_text = button_font.render("Continue", True, (255, 255, 255))
        screen.blit(continue_text, (continue_button.centerx - continue_text.get_width() // 2, 
                                   continue_button.centery - continue_text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(60)

def player_names_screen(screen, num_players):
    """Screen to enter player names"""
    title_font = get_font(72)
    font = get_font(36)
    input_font = get_font(32)
    
    clock = pygame.time.Clock()
    
    # Create input boxes
    input_boxes = []
    for i in range(num_players):
        input_box = pygame.Rect(400, 200 + i * 70, 400, 50)
        input_boxes.append({"rect": input_box, "text": f"Player {i+1}", "active": False})
    
    start_button = pygame.Rect(screen.get_width() // 2 - 100, 650, 200, 60)
    
    # Activate first input box
    if input_boxes:
        input_boxes[0]["active"] = True
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check input boxes
                for box in input_boxes:
                    box["active"] = box["rect"].collidepoint(mouse_pos)
                
                # Check start button
                if start_button.collidepoint(mouse_pos):
                    # Get all player names
                    player_names = [box["text"] for box in input_boxes]
                    # Remove empty names
                    player_names = [name for name in player_names if name.strip()]
                    if len(player_names) >= 2:  # Need at least 2 players
                        return player_names
            
            if event.type == pygame.KEYDOWN:
                for box in input_boxes:
                    if box["active"]:
                        if event.key == pygame.K_RETURN:
                            box["active"] = False
                        elif event.key == pygame.K_BACKSPACE:
                            box["text"] = box["text"][:-1]
                        else:
                            # Limit name length
                            if len(box["text"]) < 15:
                                box["text"] += event.unicode
        
        # Draw
        screen.fill((255, 235, 219))
        
        # Title
        title = title_font.render("Enter Player Names", True, (50, 50, 150))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
        
        # Input boxes
        for i, box in enumerate(input_boxes):
            color = (255, 255, 255) if box["active"] else (200, 200, 200)
            pygame.draw.rect(screen, color, box["rect"], border_radius=5)
            pygame.draw.rect(screen, (30, 30, 30), box["rect"], 2, border_radius=5)
            
            # Player label
            label = font.render(f"Player {i+1}:", True, (30, 30, 30))
            screen.blit(label, (box["rect"].x - 175, box["rect"].y + 5))
            
            # Text
            text_surface = input_font.render(box["text"], True, (30, 30, 30))
            screen.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 5))
        
        # Start button
        # Check if we have at least 2 non-empty names
        valid_names = len([box["text"] for box in input_boxes if box["text"].strip()]) >= 2
        start_color = (60, 110, 150) if (start_button.collidepoint(mouse_pos) and valid_names) else (
            (100, 160, 210) if valid_names else (150, 150, 150)
        )
        
        pygame.draw.rect(screen, start_color, start_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), start_button, 2, border_radius=10)
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, 
                               start_button.centery - start_text.get_height() // 2))
        
        # Instruction
        if not valid_names:
            instruction = font.render("Enter at least 2 player names", True, (200, 0, 0))
            screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, 450))
        
        pygame.display.flip()
        clock.tick(60)

def winning_score_screen(screen):
    """Screen to select winning score"""
    title_font = get_font(72)
    font = get_font(36)
    input_font = get_font(32)
    
    clock = pygame.time.Clock()
    
    # Common winning scores
    common_scores = [5000, 10000, 15000, 20000]
    score_buttons = []
    
    for i, score in enumerate(common_scores):
        button = pygame.Rect(300 + i * 200, 300, 150, 80)
        score_buttons.append((button, score))
    
    # Custom score input
    custom_input = pygame.Rect(600, 450, 200, 50)
    custom_text = "10000"
    custom_active = False
    
    start_button = pygame.Rect(screen.get_width() // 2 - 100, 550, 200, 60)
    selected_score = 10000  # Default
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check common score buttons
                for button, score in score_buttons:
                    if button.collidepoint(mouse_pos):
                        selected_score = score
                        custom_text = str(score)
                
                # Check custom input
                if custom_input.collidepoint(mouse_pos):
                    custom_active = True
                else:
                    custom_active = False
                
                # Check start button
                if start_button.collidepoint(mouse_pos):
                    try:
                        return int(custom_text)
                    except ValueError:
                        # If invalid, use selected_score
                        return selected_score
            
            if event.type == pygame.KEYDOWN and custom_active:
                if event.key == pygame.K_RETURN:
                    custom_active = False
                elif event.key == pygame.K_BACKSPACE:
                    custom_text = custom_text[:-1]
                else:
                    # Only allow numbers
                    if event.unicode.isdigit() and len(custom_text) < 6:
                        custom_text += event.unicode
        
        # Draw
        screen.fill((255, 235, 219))
        
        # Title
        title = title_font.render("Select Winning Score", True, (50, 50, 150))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
        
        # Instruction
        instruction = font.render("Choose a winning score or enter custom:", True, (30, 30, 30))
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, 200))
        
        # Common score buttons 
        for button, score in score_buttons:
            color = (60, 110, 150) if score == selected_score else (100, 160, 210)
            pygame.draw.rect(screen, color, button, border_radius=10)
            pygame.draw.rect(screen, (30, 30, 30), button, 2, border_radius=10)
            
            score_text = font.render(str(score), True, (255, 255, 255))
            screen.blit(score_text, (button.centerx - score_text.get_width() // 2, 
                                   button.centery - score_text.get_height() // 2))
        
        # Custom input
        custom_color = (255, 255, 255) if custom_active else (200, 200, 200)
        pygame.draw.rect(screen, custom_color, custom_input, border_radius=5)
        pygame.draw.rect(screen, (30, 30, 30), custom_input, 2, border_radius=5)
        
        custom_label = font.render("Custom:", True, (30, 30, 30))
        screen.blit(custom_label, (custom_input.x - 175, custom_input.y + 5))
        
        custom_text_surface = input_font.render(custom_text, True, (30, 30, 30))
        screen.blit(custom_text_surface, (custom_input.x + 10, custom_input.y + 5))
        
        # Start button
        start_color =  (60, 110, 150) if start_button.collidepoint(mouse_pos) else (100, 160, 210)
        pygame.draw.rect(screen, start_color, start_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), start_button, 2, border_radius=10)
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, 
                               start_button.centery - start_text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(60)

def main_game_screen(screen, player_names, winning_score):
    """Main game screen that handles the actual Farkle gameplay"""
    # Initialize game engine
    game = gameEngine(player_names, winning_score)
    game.start_game()
    game.next_turn()
    
    # Load dice images
    dice_images = {}
    try:
        for i in range(1, 7):
            img = pygame.image.load(f"src/gui/components/pictures/die_{i}.png")
            img = pygame.transform.scale(img, (100, 100))
            dice_images[i] = img
    except:
        # Create placeholder dice
        dice_colors = {
            1: (255, 0, 0),    # Red
            2: (0, 255, 0),    # Green  
            3: (0, 0, 255),    # Blue
            4: (255, 255, 0),  # Yellow
            5: (255, 0, 255),  # Magenta
            6: (0, 255, 255)   # Cyan
        }
        for i in range(1, 7):
            die = pygame.Surface((80, 80))
            die.fill(dice_colors[i])
            # Add number to placeholder
            font = get_font(48)
            text = font.render(str(i), True, (0, 0, 0))
            text_rect = text.get_rect(center=(40, 40))
            die.blit(text, text_rect)
            dice_images[i] = die
    
    # Font setup
    title_font = get_font(48)
    font = get_font(36)
    small_font = get_font(24)
    
    # Button definitions - moved down 100 pixels
    roll_button = pygame.Rect(100, 700, 150, 60)
    bank_button = pygame.Rect(300, 700, 150, 60)
    keep_button = pygame.Rect(500, 700, 150, 60)
    
    # Game state
    selected_dice = []
    message = ""
    message_timer = 0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        game_state = game.get_game_state()
        current_player = game_state['current_player']
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Roll button
                if roll_button.collidepoint(mouse_pos) and not game_state['game_over']:
                    success = game.roll_dice()
                    if success:
                        selected_dice = []
                        if game_state['last_action'] == 'farkle':
                            message = "FARKLE! No points earned."
                            message_timer = 180  # 3 seconds at 60 FPS
                            game.next_turn()
                    else:
                        message = "Cannot roll dice right now."
                        message_timer = 120
                
                # Bank button
                elif bank_button.collidepoint(mouse_pos) and not game_state['game_over']:
                    if game_state['temp_score'] > 0:
                        game.bank_score()
                        if not game_state['game_over']:
                            game.next_turn()
                        selected_dice = []
                    else:
                        message = "No points to bank!"
                        message_timer = 120
                
                # Keep button
                elif keep_button.collidepoint(mouse_pos) and not game_state['game_over']:
                    if selected_dice:
                        # Convert selected indices to dice values
                        kept_dice_values = [game_state['dice_roll'][i] for i in selected_dice]
                        success = game.keep_dice(kept_dice_values)
                        if success:
                            # Clear selected dice and update display immediately
                            selected_dice = []
                            # The dice roll display will now show the remaining dice
                            # from the game state
                        else:
                            message = "Invalid dice selection!"
                            message_timer = 120
                    else:
                        message = "Select dice to keep first!"
                        message_timer = 120
                
                # Dice selection - only allow selection if there are dice to select
                if game_state['dice_roll'] and not game_state['game_over']:
                    for i, die_value in enumerate(game_state['dice_roll']):
                        # Updated dice positions to match the display positions
                        x_pos = 200 + i * 150
                        y_pos = 550
                        die_rect = pygame.Rect(x_pos, y_pos, 100, 100)
                        if die_rect.collidepoint(mouse_pos):
                            if i in selected_dice:
                                selected_dice.remove(i)
                            else:
                                selected_dice.append(i)
        
        # Update message timer
        if message_timer > 0:
            message_timer -= 1
        
        # Draw everything
        screen.fill((255, 235, 219))
        
        # Draw title and game info
        title_text = title_font.render("FARKLE", True, (50, 50, 150))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))
        
        # Draw player scores
        y_offset = 80
        for i, (name, score) in enumerate(game_state['scores'].items()):
            color = (60, 110, 200) if name == current_player.name else (120, 180, 230)
            score_text = font.render(f"{name}: {score} points", True, color)
            screen.blit(score_text, (50, y_offset + i * 40))
        
        # Draw current turn info
        if current_player:
            turn_text = font.render(f"Current Player: {current_player.name}", True, (135, 75, 25))
            screen.blit(turn_text, (600, 80))
            
            temp_score_text = font.render(f"Turn Score: {game_state['temp_score']}", True, (135, 75, 25))
            screen.blit(temp_score_text, (600, 120))
            
            dice_count_text = font.render(f"Dice to roll: {game_state['current_dice_count']}", True, (135, 75, 25))
            screen.blit(dice_count_text, (600, 160))
        
        # Draw dice - show remaining dice after keeping
        # After keeping dice, game_state['dice_roll'] should be updated to show remaining dice
        if game_state['dice_roll']:
            dice_label = font.render("Available Dice:", True, (30, 30, 255))
            screen.blit(dice_label, (200, 500))
            
            for i, die_value in enumerate(game_state['dice_roll']):
                x_pos = 200 + i * 150
                y_pos = 550
                screen.blit(dice_images[die_value], (x_pos, y_pos))
                
                # Draw selection indicator - FIXED to properly go around the dice
                if i in selected_dice:
                    # Draw a border around the selected die
                    pygame.draw.rect(screen, (255, 215, 0), (x_pos - 5, y_pos - 5, 110, 110), 4)
                    # Optional: Add a glow effect with a semi-transparent overlay
                    highlight = pygame.Surface((100, 100), pygame.SRCALPHA)
                    highlight.fill((255, 215, 0, 50))  # Gold color with transparency
                    screen.blit(highlight, (x_pos, y_pos))
        
        # Draw buttons 
        button_color = (100, 160, 210)
        hover_color = (60, 110, 150)
        mouse_pos = pygame.mouse.get_pos()
        
        # Roll button
        roll_color = hover_color if roll_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, roll_color, roll_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), roll_button, 2, border_radius=10)
        roll_text = font.render("Roll", True, (255, 255, 255))
        screen.blit(roll_text, (roll_button.centerx - roll_text.get_width() // 2, 
                              roll_button.centery - roll_text.get_height() // 2))
        
        # Bank button
        bank_color = hover_color if bank_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, bank_color, bank_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), bank_button, 2, border_radius=10)
        bank_text = font.render("Bank", True, (255, 255, 255))
        screen.blit(bank_text, (bank_button.centerx - bank_text.get_width() // 2, 
                              bank_button.centery - bank_text.get_height() // 2))
        
        # Keep button
        keep_color = hover_color if keep_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, keep_color, keep_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), keep_button, 2, border_radius=10)
        keep_text = font.render("Keep", True, (255, 255, 255))
        screen.blit(keep_text, (keep_button.centerx - keep_text.get_width() // 2, 
                              keep_button.centery - keep_text.get_height() // 2))
        
        # Draw message
        if message_timer > 0:
            message_surface = font.render(message, True, (200, 0, 0))
            screen.blit(message_surface, (screen.get_width() // 2 - message_surface.get_width() // 2, 600))
        
        # Check for game over
        if game_state['game_over']:
            winner_screen(screen, game_state['winner'], game_state['scores'])
            running = False
        
        pygame.display.flip()
        clock.tick(60)
             
def winner_screen(screen, winner, scores):
    """Display winner screen"""
    font = get_font(72)
    small_font = get_font(36)
    
    clock = pygame.time.Clock()
    
    continue_button = pygame.Rect(screen.get_width() // 2 - 100, 500, 200, 60)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(mouse_pos):
                    return
        
        # Draw
        screen.fill((255, 235, 219))
        
        # Winner announcement
        winner_text = font.render(f"{winner} WINS!", True, (50, 150, 50))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, 100))
        
        # Final scores
        y_offset = 200
        for i, (name, score) in enumerate(scores.items()):
            color = (50, 150, 50) if name == winner else (30, 30, 30)
            score_text = small_font.render(f"{name}: {score} points", True, color)
            screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, y_offset + i * 50))
        
        # Continue button
        button_color = (60, 110, 150) if continue_button.collidepoint(mouse_pos) else (100, 160, 210)
        pygame.draw.rect(screen, button_color, continue_button, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), continue_button, 2, border_radius=10)
        continue_text = small_font.render("Continue", True, (255, 255, 255))
        screen.blit(continue_text, (continue_button.centerx - continue_text.get_width() // 2, 
                                  continue_button.centery - continue_text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(60)

def run_pygame():
    """Main function to run the PyGame Farkle game"""
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("Farkle Game")
    
    # Main game loop that allows returning to main menu
    while True:
        # Run intro screen
        result = intro_screen(screen)
        
        if result == "quit":
            break  # Exit the loop and quit the game
            
        if result == "play":
            # Get number of players
            num_players = player_count_screen(screen)
            if num_players is None:
                break

            # Get player names
            player_names = player_names_screen(screen, num_players)
            if player_names is None:
                break

            # Get winning score
            winning_score = winning_score_screen(screen)
            if winning_score is None:
                break

            # Run main game
            main_game_screen(screen, player_names, winning_score)
            # After main game finishes, the loop continues and goes back to intro screen
    
    pygame.quit()

if __name__ == "__main__":
    run_pygame()