import pygame
import random
import socket
import re
from tk_handler import Tk_Handler
from snake import Snake
from grid_square import GridSquare

# colors:
WHITE = (255, 255, 255)
BOARD_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (90, 90, 90)
BLACK = (0, 0, 0)
GREEN = (48, 184, 61)
APPLE_COLOR = (255, 0, 0)
GREEN_HEAD = (0, 100, 0)
YELLOW = (245, 252, 33)
YELLOW_HEAD = (110, 92, 3)

# grid
GRID_SIZE = 40
GRID = [[GridSquare(i, j, BACKGROUND_COLOR, 0) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

# window:
SQUARE_SIZE = 11 
PADDING = 3
SCREEN_SIZE = PADDING*(GRID_SIZE + 1) + SQUARE_SIZE*GRID_SIZE
SCORE_FONT_SIZE = 30

# display:
size = (SCREEN_SIZE + 150, SCREEN_SIZE)

# global variables:
AVAILABLE_SPOTS = []

NUMBER_OF_APPLES = 100

APPLE_EATEN = ''

IS_HOST = False

def draw_frame(snakes, SCREEN):
    for row in GRID:
        for column in row:
            draw_square(column.x, column.y, column.color, SCREEN)

    # Clear the area where scores are displayed
    pygame.draw.rect(SCREEN, BOARD_COLOR, pygame.Rect(SCREEN_SIZE, 0, 150, SCREEN_SIZE))

    # Display scores next to the board
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    score_x_offset = GRID_SIZE * (SQUARE_SIZE + PADDING) + PADDING + 10
    for i in range(len(snakes)):
        name = 'green' if snakes[i].id == 1 else 'yellow' 
        score_text = score_font.render(f"{name}: {snakes[i].head-4}", True, snakes[i].color)
        score_text_rect = score_text.get_rect(
            left=score_x_offset,
            top=i * (SCORE_FONT_SIZE + 5)
        )
        SCREEN.blit(score_text, score_text_rect)

    pygame.display.flip()

def draw_square(x, y, color, SCREEN):
    pygame.draw.rect(SCREEN, color, pygame.Rect(x*(SQUARE_SIZE + PADDING) + PADDING, y*(SQUARE_SIZE + PADDING) + PADDING, SQUARE_SIZE, SQUARE_SIZE))

def update_grid(snakes, my_socket):
    global GRID
    global IS_HOST
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
                column.id = 0
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

def enter_snake(snakes):
    global GRID
    for snake in snakes:
        for i in range(4, 8):
            GRID[i][snake.col].count = i - 3
            GRID[i][snake.col].color = snake.color
            GRID[i][snake.col].id = snake.id
        GRID[snake.row][snake.col].color = snake.head_color

def main():
    global APPLE_EATEN
    global IS_HOST
    global GRID
    DEAD_SNAKES = []
    my_socket = socket.socket()
    my_socket.connect(('10.0.0.14', 8820))
    print('connected')
    need_to_login = True
    while True:
        tkinter_handler = Tk_Handler(my_socket, need_to_login)
        tkinter_handler.start_program()
        need_to_login = False
        # if need_to_login:
        #     tkinter_handler.start_program()
        #     need_to_login = False
        # else:
        #     print(1)
        #     tkinter_handler.root.mainloop()
        #     tkinter_handler.select()
        print(2)
        SCREEN = pygame.display.set_mode(size)
        pygame.init()
        IS_HOST = tkinter_handler.type_player == 1
        my_row = 7 if tkinter_handler.type_player == 1 else 20
        my_color = GREEN if tkinter_handler.type_player == 1 else YELLOW
        my_head_color = GREEN_HEAD if tkinter_handler.type_player == 1 else YELLOW_HEAD
        in_game = True
        while in_game:
            for row in GRID:
                for col in row:
                    col.count = 0
                    col.color = BACKGROUND_COLOR
                    col.id = 0
            snake1 = Snake(7, my_row, my_color, my_head_color, tkinter_handler.type_player)
            snakes = []
            total_snakes = []
            my_socket.send(f'SK{snake1.row},{snake1.col},{snake1.color},{snake1.head_color},{snake1.id}'.encode())
            snakes_info = my_socket.recv(1024).decode().split(':')
            print(snakes_info)
            for snake_info in snakes_info:
                snake_numbers = re.findall(r'\d+', snake_info)
                snake_numbers = list(map(int, snake_numbers))
                new_snake = Snake(
                    snake_numbers[0], 
                    snake_numbers[1], 
                    (snake_numbers[2], snake_numbers[3], snake_numbers[4]),
                    (snake_numbers[5], snake_numbers[6], snake_numbers[7]),
                    snake_numbers[8])
                snakes.append(new_snake)
                total_snakes.append(new_snake)

        # while True:
            # draw the board
            SCREEN.fill(BLACK)
            # add snake to grid
            enter_snake(snakes)
            # add available spots for the apple to the according list
            AVAILABLE_SPOTS.clear()
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
            draw_frame(total_snakes, SCREEN)  # draw the beginning frame
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
                draw_frame(total_snakes, SCREEN)
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
                        if snake.row == check_snake.row and snake.col == check_snake.col:
                            DEAD_SNAKES.append(snake)
                            DEAD_SNAKES.append(check_snake)
                DEAD_SNAKES = list(set(DEAD_SNAKES)) 
                for snake in DEAD_SNAKES:
                    death(snake)
                    snakes.remove(snake)
                DEAD_SNAKES.clear()
                update_grid(snakes, my_socket)
                draw_frame(total_snakes, SCREEN)
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
                        my_socket.send(f'goodbye'.encode())
                if len(snakes) < 2:
                    print(4)
                    quit_game = True
                    pygame.quit()
                    in_game = False
                    my_socket.send('EG'.encode())


if __name__ == '__main__':
    main()