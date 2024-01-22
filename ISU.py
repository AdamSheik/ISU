import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game')

# colors
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

# making the buttons fit the screen
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
    global game_active, current_world
    game_active = True
    current_world = setup_level(1)
    print("Level 1 selected")

def level_2_action():
    global game_active, current_world
    game_active = True
    current_world = setup_level(2)
    print("Level 2 selected")

def level_3_action():
    global game_active, current_world
    game_active = True
    current_world = setup_level(3)
    print("Level 3 selected")

def back_action():
    global game_active
    game_active = False
    print("Back to the main menu")

# Create buttons
buttons = [
    Button(50, 250, level1_sprite, level_1_action),
    Button(300, 250, level2_sprite, level_2_action),
    Button(550, 250, level3_sprite, level_3_action),
    Button(10, 10, back_sprite, back_action)  # Back button at the top left
]

# Game active flag
game_active = False

# Function to set up the level based on the level index
def setup_level(level_index):
    if level_index == 1:
        return World(level_1_data)

# Function to render the current level
def render_level():
    screen.blit(bg_img, (0, 0))
    current_world.draw()
    draw_grid()

# Function to draw grid lines
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, WHITE, (0, line * tile_size), (width, line * tile_size))
        pygame.draw.line(screen, WHITE, (line * tile_size, 0), (line * tile_size, height))

# world class
class World:
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('Background/dirt.png')
        grass_img = pygame.image.load('Background/grass.jpg')
        water_img = pygame.image.load('Background/water.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(water_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def is_collision(self, rect):
        for tile in self.tile_list:
            if tile[1].colliderect(rect):
                return True
        return False

# Level 1
level_1_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 2, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 7, 0, 2], 
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 2, 2, 2, 0, 0], 
    [1, 7, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0], 
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0], 
    [1, 0, 4, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 4, 4, 0, 0, 4, 4, 4, 0, 0, 4, 0, 0, 4, 0], 
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2], 
]


bg_img = pygame.image.load('Background/realbg.jpg')


tile_size = 50

# This is just a place holder for the character ill get the sprite later
player = pygame.Rect(width - tile_size, height - 2 * tile_size, tile_size, tile_size)

# Current world variable
current_world = None

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

    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_w]:
            player.y -= 5
            if current_world.is_collision(player):
                player.y += 5
        if keys[pygame.K_s]:
            player.y += 5
            if current_world.is_collision(player):
                player.y -= 5
        if keys[pygame.K_a]:
            player.x -= 5
            if current_world.is_collision(player):
                player.x += 5
        if keys[pygame.K_d]:
            player.x += 5
            if current_world.is_collision(player):
                player.x -= 5

    screen.fill(BLACK)

    if not game_active:
        title_surf = font.render('My nice game', True, WHITE)
        screen.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 50))

        for button in buttons[:-1]:
            button.draw(screen)
    else:
        render_level()
        pygame.draw.rect(screen, RED, player)
        buttons[-1].draw(screen)

    pygame.display.flip()

pygame.quit()
