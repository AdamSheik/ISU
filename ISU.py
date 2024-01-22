import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define font
font = pygame.font.Font(None, 36)

# Function to resize sprite
def resize_sprite(image, scale_factor):
    original_rect = image.get_rect()
    scaled_size = (int(original_rect.width * scale_factor), int(original_rect.height * scale_factor))
    return pygame.transform.scale(image, scaled_size)

# Load and resize sprites
level1_sprite = resize_sprite(pygame.image.load('buttons/level1.png'), 0.5)
level2_sprite = resize_sprite(pygame.image.load('buttons/level2.png'), 0.5)
level3_sprite = resize_sprite(pygame.image.load('buttons/level3.png'), 0.5)
back_sprite = resize_sprite(pygame.image.load('buttons/backer.png'), 0.3)

# Define button class
class Button:
    def __init__(self, x, y, sprite, action=None):
        self.sprite = sprite
        self.rect = sprite.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, win):
        win.blit(self.sprite, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def execute_action(self):
        if self.action:
            self.action()

# Define actions for each button
def level_1_action():
    global game_active
    game_active = True
    print("Level 1 selected")

def level_2_action():
    global game_active
    game_active = True
    print("Level 2 selected")

def level_3_action():
    global game_active
    game_active = True
    print("Level 3 selected")

def back_action():
    global game_active
    game_active = False
    print("Back to main menu")

# Create buttons
buttons = [
    Button(50, 250, level1_sprite, level_1_action),
    Button(300, 250, level2_sprite, level_2_action),
    Button(550, 250, level3_sprite, level_3_action),
    Button(10, 10, back_sprite, back_action)  # Back button at the top left
]

# Player square
player = pygame.Rect(100, 100, 50, 50)

# Game active flag
game_active = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    button.execute_action()

    # Handle key presses
    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_w]:
            player.y -= 5
        if keys[pygame.K_s]:
            player.y += 5
        if keys[pygame.K_a]:
            player.x -= 5
        if keys[pygame.K_d]:
            player.x += 5

    # Fill the screen with black
    screen.fill(BLACK)

    if not game_active:
        # Draw title
        title_surf = font.render('My nice game', True, WHITE)
        screen.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 50))

        # Draw buttons
        for button in buttons[:-1]:  # Exclude the back button from the main menu
            button.draw(screen)
    else:
        # Draw the player square
        pygame.draw.rect(screen, RED, player)
        # Draw the back button
        buttons[-1].draw(screen)  # Only draw the back button when the game is active

    # Update the display
    pygame.display.flip()

pygame.quit()
