# Snake game
# the game where snake is continiously moving and you need to collect 
# as many apples as you can without colliding with yourself
# author: Nick Poberezhnyk


import sys, pygame, random
from pygame.locals import *
pygame.init()

# set up clock ticks for the main function
# FPS represents amount of ticks per second
fps_clock = pygame.time.Clock()
FPS = 8

# set title for the game window
pygame.display.set_caption("Snake")

# game window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 576

# size of one tile (snake segment, apple)
TILE_SIZE = 32

# set up the surface to draw on
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# calculate the amount of tiles in x and y direction
MAX_TILES_X = WINDOW_WIDTH // TILE_SIZE
MAX_TILES_Y = WINDOW_HEIGHT // TILE_SIZE

# types of tiles
TILE_EMPTY = 0
TILE_SNAKE_HEAD = 1
TILE_SNAKE_BODY = 2
TILE_APPLE = 3

# colors
GREEN = 0, 255, 0
BLACK = 0, 0, 0
CYAN = 0, 255, 125
RED = 255, 0, 0
WHITE = 255, 255, 255

# snake head position
snake_x, snake_y = 0, 0
# the direction in which snake moves
snake_move = "right"
# data structure to keep track of all snake segments
snake_tiles = [[snake_x, snake_y]]
# score
score = 0
# state of the game
game_over = False

# create a grid and set all tiles to empty
tile_grid = [[TILE_EMPTY for y in range(MAX_TILES_Y)] for x in range(MAX_TILES_X)]
# generate random location of an apple
apple_x, apple_y = random.randrange(MAX_TILES_X), random.randrange(MAX_TILES_Y)

# make a list with all tiles in the grid
coordinate_grid = []
for y in range(MAX_TILES_Y):
    for x in range(MAX_TILES_X):
        coordinate_grid.append([x, y])

# set all elements of the grid to empty
def reset_grid():
    global tile_grid
    tile_grid = [[TILE_EMPTY for y in range(MAX_TILES_Y)] for x in range(MAX_TILES_X)]

# put apple onto the grid
def render_apple():
    tile_grid[apple_x][apple_y] = TILE_APPLE

# find difference between two lists
def find_list_difference(l1, l2):
    return [x for x in l1 if x not in l2]

# display the score
def display_score(score):
    font = pygame.font.SysFont(None, 32)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (0, 0))

# display message when game is over
def display_game_over():
    large_font = pygame.font.SysFont(None, 128)
    game_over_text = large_font.render("GAME OVER", True, WHITE)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = ((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    regular_font = pygame.font.SysFont(None, 32)
    press_button_text = regular_font.render("press Space to play again", True, WHITE)
    press_button_text_rect = press_button_text.get_rect()
    press_button_text_rect.center = ((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3 * 2))
    
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(press_button_text, press_button_text_rect)

# check each element of the grid and place recpective tile on the screen
def draw_grid():
    for y in range(MAX_TILES_Y):
        for x in range(MAX_TILES_X):
            if tile_grid[x][y] == TILE_SNAKE_BODY:
                pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE,
                                        TILE_SIZE, TILE_SIZE))
            elif tile_grid[x][y] == TILE_APPLE:
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE,
                                        TILE_SIZE, TILE_SIZE))
            elif tile_grid[x][y] == TILE_SNAKE_HEAD:
                pygame.draw.rect(screen, CYAN, (x * TILE_SIZE, y * TILE_SIZE,
                                        TILE_SIZE, TILE_SIZE))

# change tiles that correspond to locations of snake tiles
# head renders different from other parts of snake 
def render_snake():
    for segment in snake_tiles[1:]:
        tile_grid[segment[0]][segment[1]] = TILE_SNAKE_BODY
    tile_grid[snake_tiles[0][0]][snake_tiles[0][1]] = TILE_SNAKE_HEAD

# main loop
while True:
    screen.fill(BLACK)
    # check key events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_DOWN and snake_move != "up":
                snake_move = "down"
            elif event.key == K_UP and snake_move != "down":
                snake_move = "up"
            elif event.key == K_LEFT and snake_move != "right":
                snake_move = "left"
            elif event.key == K_RIGHT and snake_move != "left":
                snake_move = "right"
            # reset if space key is pressed after game over
            elif event.key == K_SPACE and game_over:
                snake_x, snake_y = 0, 0
                snake_move = "right"
                snake_tiles = [[snake_x, snake_y]]
                score = 0
                game_over = False
                tile_grid = [[TILE_EMPTY for y in range(MAX_TILES_Y)] for x in range(MAX_TILES_X)]
                apple_x, apple_y = random.randrange(MAX_TILES_X), random.randrange(MAX_TILES_Y)

    # update snake position
    if not game_over:
        if snake_move == "down":
            if snake_y >= MAX_TILES_Y - 1:
                snake_y = 0
            else:
                snake_y += 1
        elif snake_move == "up":
            if snake_y <= 0:
                snake_y = MAX_TILES_Y - 1
            else:
                snake_y -= 1
        elif snake_move == "right":
            if snake_x >= MAX_TILES_X - 1:
                snake_x = 0
            else:
                snake_x += 1
        elif snake_move == "left":
            if snake_x <= 0:
                snake_x = MAX_TILES_X - 1
            else:
                snake_x -= 1

        # if snake collides with itself
        if [snake_x, snake_y] in snake_tiles:
            game_over = True
            
        # insert new tile in the first position of the snake data structure
        snake_tiles.insert(0, [snake_x, snake_y])
        # remove last segment of the snake and store it in variable last
        last = snake_tiles.pop()

        # if current tile is an apple
        if tile_grid[snake_x][snake_y] == TILE_APPLE:
            score += 1
            # add last tile back to the end of the snake
            snake_tiles.append(last)
            # make sure that apple doesn't appear where snake is
            free_tiles = find_list_difference(coordinate_grid, snake_tiles)
            new_apple_tile = random.choice(free_tiles)
            apple_x, apple_y = new_apple_tile[0], new_apple_tile[1]
            
            
        # clear the grid, put apple and snake on the grid
        # and then draw it
        reset_grid()
        render_apple()
        render_snake()
        draw_grid()
    else:
        render_apple()
        render_snake()
        draw_grid()
        display_game_over()
    display_score(score)
    pygame.display.update()
    fps_clock.tick(FPS)
        
        