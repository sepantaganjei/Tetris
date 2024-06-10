import pygame  # type: ignore
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
GRID_WIDTH = 15
GRID_HEIGHT = 25
BLOCK_SIZE = 25
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (225, 0, 0)
SHADOW_COLOR = (50, 50, 50)
OUTLINE_COLOR = (0, 0, 0)
BUTTON_COLOR = (255, 50, 50)
BUTTON_HOVER_COLOR = (200, 0, 0)
CYAN = (0, 225, 225)
BLUE = (0, 0, 225)
ORANGE = (225, 165, 0)
YELLOW = (225, 225, 0)
GREEN = (0, 225, 0)
PURPLE = (128, 0, 128)
COLORS = [
    CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1], [1, 1]], # O
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH + 150, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize clock
clock = pygame.time.Clock()

# Initialize font
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # Larger font for the Game Over text

# Initialize variables
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
tetromino = None
next_tetromino = None
tetromino_index = 0
next_tetromino_index = 0
held_tetromino = None
held_tetromino_index = -1
can_hold = True
score = 0
game_over = False

move_delay = 100  # milliseconds
last_move_time = 0

def new_tetromino():
    global tetromino, next_tetromino, tetromino_index, next_tetromino_index
    if next_tetromino is not None:
        tetromino = next_tetromino
        tetromino_index = next_tetromino_index
    else:
        tetromino_index = random.randint(0, len(SHAPES) - 1)
        tetromino = SHAPES[tetromino_index]
    next_tetromino_index = random.randint(0, len(SHAPES) - 1)
    next_tetromino = SHAPES[next_tetromino_index]

def draw_tetromino(tetromino, x, y, index):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j] == 1:
                pygame.draw.rect(screen, COLORS[index], (x + j * BLOCK_SIZE, y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(tetromino, x, y):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j] == 1:
                if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or grid[y + i][x + j] != 0:
                    return True
    return False

def merge_tetromino(tetromino, x, y):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j] == 1:
                if 0 <= y + i < GRID_HEIGHT and 0 <= x + j < GRID_WIDTH:  # Add this check
                    grid[y + i][x + j] = tetromino_index + 1

def check_lines():
    global score
    lines = 0
    for i in range(len(grid)):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0 for x in range(GRID_WIDTH)])
            lines += 1
    score += lines ** 2

def draw_grid():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, COLORS[grid[i][j] - 1], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_text(text, x, y, font, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height), border_radius=8)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height), border_radius=8)
    draw_text(text, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2, font, WHITE)

def draw():
    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(tetromino, tetromino_x * BLOCK_SIZE, tetromino_y * BLOCK_SIZE, tetromino_index)
    draw_text("Score: " + str(score), SCREEN_WIDTH + 10, 10, font, WHITE)
    draw_text("Next:", SCREEN_WIDTH + 10, 50, font, WHITE)
    draw_tetromino(next_tetromino, SCREEN_WIDTH + 10, 80, next_tetromino_index)
    draw_text("Hold:", SCREEN_WIDTH + 10, 200, font, WHITE)
    if held_tetromino is not None:
        draw_tetromino(held_tetromino, SCREEN_WIDTH + 10, 230, held_tetromino_index)
    if game_over:
        draw_text_with_shadow_and_outline("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text("Score: " + str(score), SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20, font, WHITE)
        draw_button("Retry", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20, 100, 50)
    pygame.display.flip()

def draw_text_with_shadow_and_outline(text, x, y):
    shadow_offset = 5
    outline_thickness = 2
    img = large_font.render(text, True, RED)
    text_width = img.get_width()
    text_height = img.get_height()

    x -= text_width // 2  # Adjust x to center the text

    # Draw shadow
    draw_text(text, x + shadow_offset, y + shadow_offset, large_font, SHADOW_COLOR)

    # Draw outline
    for dx in [-outline_thickness, outline_thickness]:
        for dy in [-outline_thickness, outline_thickness]:
            draw_text(text, x + dx, y + dy, large_font, OUTLINE_COLOR)

    # Draw main text
    draw_text(text, x, y, large_font, RED)

def reset():
    global grid, tetromino, next_tetromino, tetromino_index, next_tetromino_index, held_tetromino, held_tetromino_index, can_hold, score, game_over
    grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    tetromino = None
    next_tetromino = None
    held_tetromino = None
    held_tetromino_index = -1
    score = 0
    game_over = False
    can_hold = True
    new_tetromino()

def drop_tetromino():
    global tetromino_y
    while not check_collision(tetromino, tetromino_x, tetromino_y + 1):
        tetromino_y += 1

def hold_tetromino():
    global tetromino, tetromino_index, held_tetromino, held_tetromino_index, can_hold
    if can_hold:
        if held_tetromino is None:
            held_tetromino = tetromino
            held_tetromino_index = tetromino_index
            new_tetromino()
        else:
            tetromino, held_tetromino = held_tetromino, tetromino
            tetromino_index, held_tetromino_index = held_tetromino_index, tetromino_index
        tetromino_x, tetromino_y = GRID_WIDTH // 2 - 2, 0
        can_hold = False

def handle_movement():
    global tetromino_x, tetromino_y, last_move_time
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_delay:
        if keys[pygame.K_LEFT] and not check_collision(tetromino, tetromino_x - 1, tetromino_y):
            tetromino_x -= 1
            last_move_time = current_time
        if keys[pygame.K_RIGHT] and not check_collision(tetromino, tetromino_x + 1, tetromino_y):
            tetromino_x += 1
            last_move_time = current_time
        if keys[pygame.K_DOWN] and not check_collision(tetromino, tetromino_x, tetromino_y + 1):
            tetromino_y += 1
            last_move_time = current_time

def main():
    global tetromino, tetromino_x, tetromino_y, game_over, can_hold

    tetromino_x, tetromino_y = GRID_WIDTH // 2 - 2, 0
    new_tetromino()
    gravity_counter = 0

    while True:
        clock.tick(FPS)
        gravity_counter += 1
        if not game_over and gravity_counter >= FPS // 2:
            gravity_counter = 0
            if not check_collision(tetromino, tetromino_x, tetromino_y + 1):
                tetromino_y += 1
            else:
                merge_tetromino(tetromino, tetromino_x, tetromino_y)
                check_lines()
                new_tetromino()
                tetromino_x, tetromino_y = GRID_WIDTH // 2 - 2, 0
                can_hold = True
                if check_collision(tetromino, tetromino_x, tetromino_y):
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        rotated_tetromino = list(zip(*tetromino[::-1]))
                        if not check_collision(rotated_tetromino, tetromino_x, tetromino_y):
                            tetromino = rotated_tetromino
                    if event.key == pygame.K_SPACE:
                        drop_tetromino()
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        hold_tetromino()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    x, y = event.pos
                    if SCREEN_WIDTH // 2 - 50 <= x <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 20 <= y <= SCREEN_HEIGHT // 2 + 70:
                        reset()

        if not game_over:
            handle_movement()
        draw()

if __name__ == "__main__":
    reset()
    main()

# Run the game
pygame.quit()
