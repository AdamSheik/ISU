import pygame
from pygame.locals import *
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define game variables
tile_size = 50
font = pygame.font.SysFont(None, 55)

# load images
bg_img = pygame.image.load('Background/realbg.jpg')

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load('Background/character.png')
            img_right = pygame.transform.scale(img_right, (30, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height  # Adjusted the initial y position
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision, excluding tile 4
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and tile[2] != 4:
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and tile[2] != 4:
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

                # check for collision with water (tile 3)
                if tile[2] == 3:
                    game_over_text = font.render('Game Over!', True, (255, 0, 0))
                    screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2))
                    pygame.display.update()
                    pygame.time.delay(2000)  # Display the text for 2 seconds
                    pygame.quit()
                    sys.exit()

        # check for winning condition (reaching the door)
        if self.rect.colliderect(world.door_rect) and not self.jumped:
            you_win_text = font.render('You Win!', True, (255, 255, 255))
            screen.blit(you_win_text, (screen_width // 2 - 100, screen_height // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # Display the text for 2 seconds
            pygame.quit()
            sys.exit()

        # check for collision with the enemy
        if pygame.sprite.spritecollide(self, world.enemy_list, False):
            game_over_text = font.render('Game Over!', True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # Display the text for 2 seconds
            pygame.quit()
            sys.exit()

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto the screen
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Background/monster.png')  # Change to the actual enemy image
        self.image = pygame.transform.scale(self.image, (20, 40))  # Scale down the monster
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.movement_range = 100  # Adjust the range the enemy moves left and right

    def update(self):
        movement_speed = 2  # Adjust the speed of the enemy's movement

        self.rect.x += self.move_direction * movement_speed
        self.move_counter += movement_speed
        if abs(self.move_counter) > self.movement_range:
            self.move_direction *= -1
            self.move_counter *= -1

class World():
    def __init__(self, data):
        self.tile_list = []
        self.enemy_list = pygame.sprite.Group()

        # load images
        dirt_img = pygame.image.load('Background/dirt.png')
        grass_img = pygame.image.load('Background/grass.jpg')
        water_img = pygame.image.load('Background/water.png')
        door_img = pygame.image.load('Background/door.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 1)  # 1 represents dirt
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 2)  # 2 represents grass
                    self.tile_list.append(tile)
                elif tile == 3:
                    img = pygame.transform.scale(water_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 3)  # 3 represents water
                    self.tile_list.append(tile)
                elif tile == 4:
                    img = pygame.transform.scale(door_img, (200, 150))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 4)  # 4 represents door
                    self.tile_list.append(tile)
                    self.door_rect = img_rect  # store the door rectangle separately
                elif tile == 5:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    self.enemy_list.add(enemy)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.enemy_list.draw(screen)

# Define the new level 1 map
level_1_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2],
]

player = Player(screen_width - 50, screen_height - 80)  # Adjusted the initial position
world = World(level_1_data)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    world.draw()
    player.update()

    for enemy in world.enemy_list:
        enemy.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
sys.exit()
