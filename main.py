import pygame
import random
import socket
import re
from snake import Snake
from grid_square import GridSquare

# colors:
WHITE = (255, 255, 255)
BOARD_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (90, 90, 90)
BLACK = (0, 0, 0)
SNAKE_COLOR = (48, 184, 61)
APPLE_COLOR = (255, 0, 0)
HEAD_COLOR = (0, 100, 0)
YELLOW = (245, 252, 33)
YELLOW_HEAD = (110, 92, 3)

# grid
GRID_SIZE = 40
GRID = [[GridSquare(i, j, BACKGROUND_COLOR, 0) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

# window:
SQUARE_SIZE = 11
PADDING = 3
SCREEN_SIZE = PADDING*(GRID_SIZE + 1) + SQUARE_SIZE*GRID_SIZE

# display:
size = (SCREEN_SIZE, SCREEN_SIZE)
SCREEN = pygame.display.set_mode(size)

# global variables:
AVAILABLE_SPOTS = []

NUMBER_OF_APPLES = 10

APPLE_EATEN = ''

IS_HOST = False

def draw_frame():
    for row in GRID:
        for column in row:
            draw_square(column.x, column.y, column.color)
    pygame.display.flip()

def draw_square(x, y, color):
    pygame.draw.rect(SCREEN, color, pygame.Rect(x*(SQUARE_SIZE + PADDING) + PADDING, y*(SQUARE_SIZE + PADDING) + PADDING, SQUARE_SIZE, SQUARE_SIZE))

def update_grid(snakes, my_socket):
    # part 1(the apple): 
    for snake in snakes:
        if GRID[snake.row][snake.col].count == -1:
            if IS_HOST:
                apple_position = add_apple_host()
                my_socket.send(f'AA({apple_position[0]},{apple_position[1]})'.encode())
                my_socket.recv(1024)
            else:
                apple_position = my_socket.recv(1024).decode()
                apple_numbers = re.findall(r'\d+', apple_position)
                apple_numbers = list(map(int, apple_numbers)) 
                add_apple(apple_numbers[0], apple_numbers[1])
            snake.apple_eaten = True
        GRID[snake.row][snake.col].count = snake.head + 1
        GRID[snake.row][snake.col].id = snake.id
        if GRID[snake.row][snake.col] in AVAILABLE_SPOTS:
            AVAILABLE_SPOTS.remove(GRID[snake.row][snake.col])
        if snake.apple_eaten:
            snake.head += 1
    # part 2(the grid)
    for row in GRID:
        for column in row:
            for snake in snakes:
                if column.id == snake.id:
                    if column.count > 0 and not snake.apple_eaten:
                        column.count -= 1
                        if column.count == 0:
                            AVAILABLE_SPOTS.append(column)
                    if column.count > 0:
                        column.color = snake.color
                    elif column.count == -1:
                        column.color = APPLE_COLOR
                    if column.count == snake.head:
                        column.color = snake.head_color
            if column.count == 0:
                column.color = BACKGROUND_COLOR
                continue
    for snake in snakes:
        snake.apple_eaten = False

def add_apple_host():
    if len(AVAILABLE_SPOTS) > 0:
        new_apple_spot = AVAILABLE_SPOTS[random.randint(0, len(AVAILABLE_SPOTS) - 1)]
        new_apple_spot.count = -1
        new_apple_spot.color = APPLE_COLOR
        AVAILABLE_SPOTS.remove(new_apple_spot)
    return new_apple_spot.x, new_apple_spot.y

def add_apple(x, y):
    new_apple_spot = None
    for row in GRID:
        for column in row:
            if column.x == x and column.y == y:
                new_apple_spot = column
    new_apple_spot.count = -1
    new_apple_spot.color = APPLE_COLOR

def death(snake):
    for row in GRID:
        for column in row:
            if column.id == snake.id:
                column.color = BACKGROUND_COLOR
                column.count = 0
    snake.head = 4

def enter_snake(snakes):
    for snake in snakes:
        for i in range(4, 8):
            GRID[i][snake.col].count = i - 3
            GRID[i][snake.col].color = snake.color
            GRID[i][snake.col].id = snake.id
        GRID[snake.row][snake.col].color = snake.head_color

def main():
    global APPLE_EATEN
    DEAD_SNAKES = [] 
    my_socket = socket.socket()
    my_socket.connect(('10.0.0.14', 8820))
    print('connected')
    pygame.init()
    while True:
        # draw the board
        SCREEN.fill(BLACK)
        snake1 = Snake(7, 7, SNAKE_COLOR, HEAD_COLOR, 1)
        snake2 = Snake(7, 20, YELLOW, YELLOW_HEAD, 2)
        snakes = [snake1, snake2] 
        # add snake to grid
        enter_snake(snakes)
        # add available spots for the apple to the according list
        for row in GRID:
            for column in row:
                if column.count == 0:
                    AVAILABLE_SPOTS.append(column)
        # add apples:
        if IS_HOST:
            apples = ''
            for i in range(0, NUMBER_OF_APPLES):
                apple_position = add_apple_host()
                apples += f':({apple_position[0]},{apple_position[1]})'  # add apple to the grid
            my_socket.send(('AA' + apples).encode())
            my_socket.recv(1024)
        else:
            apples = my_socket.recv(1024).decode().split(':')
            if apples[0] == 'AA':
                for i in range(1, len(apples)):
                    apple_numbers = re.findall(r'\d+', apples[i])
                    apple_numbers = list(map(int, apple_numbers)) 
                    add_apple(apple_numbers[0], apple_numbers[1])
        draw_frame()  # draw the beginning frame
        # wait for the space_bar to be pressed
        if IS_HOST:
            start_game = False
            while not start_game:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            start_game = True
                            my_socket.send('BG'.encode()) 
                    if event.type == pygame.QUIT:
                            pygame.quit()
        my_socket.recv(1024)
        quit_game = False
        while not quit_game:
            draw_frame()
            snake1.update_position()
            my_socket.send(f'id={snake1.id}({snake1.row},{snake1.col})'.encode()) 
            head_infos = my_socket.recv(1024).decode().split(':')
            # id=1(2,5)
            for head_info in head_infos:
                numbers = re.findall(r'\d+', head_info)
                numbers = list(map(int, numbers))
                if not IS_HOST and head_info[:2] == 'AA':
                    add_apple(numbers[0], numbers[1])
                else:
                    for snake in snakes:
                        if snake.id == numbers[0]:
                            snake.set_position(numbers[1], numbers[2])
            for snake in snakes:
                if not 0 <= snake.row < GRID_SIZE or not 0 <= snake.col < GRID_SIZE or GRID[snake.row][snake.col].count > 1:
                    DEAD_SNAKES.append(snake)
                for check_snake in snakes:
                    if snake is check_snake:
                        continue
                    if snake.row == check_snake.row  and snake.col == check_snake.col:
                        DEAD_SNAKES.append(snake)
                        DEAD_SNAKES.append(check_snake)
            DEAD_SNAKES = list(set(DEAD_SNAKES)) 
            for snake in DEAD_SNAKES:
                death(snake)
                snakes.remove(snake)
            DEAD_SNAKES.clear()
            update_grid(snakes, my_socket)
            draw_frame()
            pygame.time.delay(120)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake1.true_direction != 'right':
                        snake1.direction = 'left'
                    if event.key == pygame.K_RIGHT and snake1.true_direction != 'left':
                        snake1.direction = 'right'
                    if event.key == pygame.K_UP and snake1.true_direction != 'down':
                        snake1.direction = 'up'
                    if event.key == pygame.K_DOWN and snake1.true_direction != 'up':
                        snake1.direction = 'down'
                if event.type == pygame.QUIT:
                    pygame.quit()


if __name__ == '__main__':
    main()