import pygame
import time
import random

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
snake_color = (0, 128, 0)

# Snake
snake_block = 20
initial_snake_speed = 5
speed_increment = 1
max_speed = 20

font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, snake_color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_large.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_displace])

def gameLoop():
    clock = pygame.time.Clock()
    game_over = False
    game_close = False

    # Initial snake position
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    # Initial snake length and speed
    snake_list = []
    length_of_snake = 1
    snake_speed = initial_snake_speed

    # Initial food position
    foodx, foody = round(random.randrange(0, width - snake_block) / 20.0) * 20.0, round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Score
    score = 0

    while not game_over:

        while game_close:
            screen.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red, y_displace=-50)
            message(f"Your Score: {score}", black, y_displace=50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x1_change = -snake_block
            y1_change = 0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x1_change = snake_block
            y1_change = 0
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            y1_change = -snake_block
            x1_change = 0
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y1_change = snake_block
            x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(white)
        pygame.draw.rect(screen, blue, [foodx, foody, snake_block, snake_block])
        our_snake(snake_block, snake_list)

        # Draw boundaries
        pygame.draw.line(screen, red, (0, 0), (width, 0), 5)
        pygame.draw.line(screen, red, (0, 0), (0, height), 5)
        pygame.draw.line(screen, red, (width, 0), (width, height), 5)
        pygame.draw.line(screen, red, (0, height), (width, height), 5)

        # Display score
        score_text = font_medium.render(f"Score: {score}", True, black)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = round(random.randrange(0, width - snake_block) / 20.0) * 20.0, round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 10
            snake_speed = min(snake_speed + speed_increment, max_speed)

        # Update snake speed
        clock.tick(snake_speed)

        # Update snake list
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

    pygame.quit()
    quit()

gameLoop()
