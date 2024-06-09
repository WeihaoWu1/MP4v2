import pygame
import random
from asteroid import Asteroid
from spaceship import Spaceship
from laser import Laser

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 30)
pygame.display.set_caption("Space Shooter")

# set up variables for the display
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 700
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# set up intro background display
intro_screen_image = pygame.image.load("space_shooter.png")
intro_screen_image = pygame.transform.scale(intro_screen_image, (700, 600))

# set up start button
start_button_image = pygame.image.load("start_button.png")
start_button_image = pygame.transform.scale(start_button_image, (150, 80))
start_button_image_size = start_button_image.get_size()
start_button_rect = pygame.Rect(500, 500, start_button_image_size[0], start_button_image_size[1])

# set up game background
background_image = pygame.image.load("space_background.png")
background_image = pygame.transform.scale(background_image, (700, 600))


r = 50
g = 0
b = 100
user = Spaceship(350, 500)
laser = Laser(999, 999)
a = Asteroid(200, 200)
asteroids = []
score = 0
moving_x = a.direction_x()
moving_y = a.direction_y()
x_start = random.randint(0, 650)
run = True
start_screen = True
shoot_laser = False
game_end = False
display_score = my_font.render("Score: " + str(score), True, (255, 255, 255))


def keep_score():
    

while run:
    display_score = my_font.render("Score: " + str(score), True, (255, 255, 255))
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and start_button_rect.collidepoint(event.pos):
            start_screen = False
    if len(asteroids) < 5:
        x_pos = random.randint(50, 600)
        a = Asteroid(x_pos, 0)
    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_d] and not start_screen:
        user.move_to_direction("right")
    if keys[pygame.K_a] and not start_screen:
        user.move_to_direction("left")
    if keys[pygame.K_w] and not start_screen:
        user.move_to_direction("up")
    if keys[pygame.K_s] and not start_screen:
        user.move_to_direction("down")
    if keys[pygame.K_SPACE] and not start_screen:
        laser.set_location(user.x + 30, user.y - 30)
        shoot_laser = True

    if shoot_laser:
        laser.shoot()

    if not laser.rect.colliderect(a.rect) and ((a.x > 0 or a.x < 700) or (a.y < 600)) and not start_screen:
        a.obstacle_move(moving_x, moving_y)

    if laser.rect.colliderect(a.rect):
        moving_x = a.direction_x()
        moving_y = a.direction_y()
        x_start = random.randint(50, 600)
        a.set_location(x_start, 0)
        laser.set_location(-999, -999)
        score += 1

    if laser.y < 0:
        laser.set_location(-999, -999)

    if user.rect.colliderect(a.rect):
        game_end = True

    if (a.x < 0 or a.x > 700) or (a.y > 600):
        game_end = True

    screen.fill((0, 0, 0))
    if start_screen:
        screen.blit(intro_screen_image, (0, 0))
        screen.blit(start_button_image, start_button_rect)
    if not start_screen and not game_end:
        screen.blit(background_image, (0, 0))
        screen.blit(user.image, user.rect)
        screen.blit(a.image, a.rect)
        screen.blit(laser.image, laser.rect)
    if game_end:
        screen.blit(background_image, (0, 0))
        screen.blit(display_score, (300, 400))
    pygame.display.update()

pygame.quit()
