import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 1000
# Screen length and width
bottom_panel_height = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + bottom_panel_height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hello')

# Load images
background_img = pygame.image.load('Background/backgroundnice.jpeg').convert_alpha()
panel_img = pygame.image.load('Panel/real.png').convert_alpha()

# Scale images to fit the screen
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT - bottom_panel_height))
panel_img = pygame.transform.scale(panel_img, (SCREEN_WIDTH, bottom_panel_height))

def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - bottom_panel_height))

# The size of the rectangle (x, y)
player = pygame.Rect(0, 0, 50, 50)

run = True
while run:

    clock.tick(fps)
    # Screen color
    screen.fill((0, 0, 0))

    # Background
    draw_bg()
    # Draw panel
    draw_panel()

    pygame.draw.rect(screen, (255, 0, 0), player)

    # Rectangle movement
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-1, 0)
        if player.left < 0:  # Check if player is going out of the left edge
            player.left = 0

    elif key[pygame.K_d]:
        player.move_ip(1, 0)
        if player.right > SCREEN_WIDTH:  # Check if player is going out of the right edge
            player.right = SCREEN_WIDTH

    elif key[pygame.K_w]:
        player.move_ip(0, -1)
        if player.top < 0:  # Check if player is going out of the top edge
            player.top = 0

    elif key[pygame.K_s]:
        player.move_ip(0, 1)
        if player.bottom > SCREEN_HEIGHT - bottom_panel_height:  # Adjust for panel height
            player.bottom = SCREEN_HEIGHT - bottom_panel_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()