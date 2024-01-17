import pygame
import time
import random
import pickle

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)  # Define the black color

# Load background image
background_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/background.jpg")  # Replace with the actual path

# Resize background image dynamically
background_img = pygame.transform.scale(background_img, (width, height))

# Load food image with reduced size
food_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/food.png")  # Replace with the actual path
food_size = 20  # Replace with the desired size in pixels
food_img = pygame.transform.scale(food_img, (food_size, food_size))

# Load border images with reduced size
border_size = 10  # Replace with the desired size in pixels
top_border_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/top_border.png")  # Replace with the actual path
bottom_border_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/bottom_border.png")  # Replace with the actual path
left_border_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/left_border.png")  # Replace with the actual path
right_border_img = pygame.image.load("C:/Users/Aditya/Desktop/SC/snake/right_border.png")  # Replace with the actual path

# Resize border images dynamically with reduced size
top_border_img = pygame.transform.scale(top_border_img, (width, border_size))
bottom_border_img = pygame.transform.scale(bottom_border_img, (width, border_size))
left_border_img = pygame.transform.scale(left_border_img, (border_size, height))
right_border_img = pygame.transform.scale(right_border_img, (border_size, height))

# Snake
snake_block = 20
initial_snake_speed = 10
speed_increment = 1
max_speed = 20

font_medium = pygame.font.SysFont(None, 35)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, white, [segment[0], segment[1], snake_block, snake_block])

def draw_background():
    screen.blit(background_img, (0, 0))

def draw_food(foodx, foody):
    screen.blit(food_img, (foodx, foody))

def display_score(score):
    score_text = font_medium.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])

def draw_borders():
    screen.blit(top_border_img, (0, 0))
    screen.blit(bottom_border_img, (0, height - border_size))
    screen.blit(left_border_img, (0, 0))
    screen.blit(right_border_img, (width - border_size, 0))

def message(msg, color, y_displace=0):
    mesg = font_medium.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_displace])

def save_game(snake, length_of_snake, foodx, foody, score):
    with open("snake_save.pkl", "wb") as file:
        pickle.dump((snake, length_of_snake, foodx, foody, score), file)

def load_game():
    try:
        with open("snake_save.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(black)
        message("Welcome to Snake Game", white, -100)
        message("Press C to Play or Q to Quit", white, 50)
        pygame.display.update()

def game_pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_s:
                    save_game(snake, length_of_snake, foodx, foody, score)
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(black)
        message("Game Paused", white, -100)
        message("Press C to Continue, S to Save, or Q to Quit", white, 50)
        pygame.display.update()

def gameLoop():
    global snake, length_of_snake, foodx, foody, score
    game_over = False
    game_close = False

    # Initial snake position
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    # Initial snake length and speed
    snake = []
    length_of_snake = 1
    snake_speed = initial_snake_speed

    # Initial food position
    foodx, foody = round(random.randrange(0, width - snake_block) / 20.0) * 20.0, round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Score
    score = 0

    while not game_over:

        while game_close:
            screen.fill(black)
            message("You Lost! Press C-Play Again, L-Load Game, or Q-Quit", red, y_displace=-50)
            message(f"Your Score: {score}", white, y_displace=50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        game_close = False
                    if event.key == pygame.K_l:
                        loaded_data = load_game()
                        if loaded_data:
                            snake, length_of_snake, foodx, foody, score = loaded_data
                            game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_pause()
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        draw_background()
        draw_food(foodx, foody)
        draw_snake(snake)
        draw_borders()

        display_score(score)

        if x1 == foodx and y1 == foody:
            foodx, foody = round(random.randrange(0, width - snake_block) / 20.0) * 20.0, round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 10
            snake_speed = min(snake_speed + speed_increment, max_speed)

        pygame.display.update()

        if (x1, y1) in snake[:-1]:
            game_close = True

        if len(snake) > length_of_snake:
            del snake[0]

        snake.append((x1, y1))

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

game_intro()
gameLoop()
