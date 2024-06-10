import pygame
import random
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, COLORS, BLACK, WHITE, RED, SHADOW_COLOR, OUTLINE_COLOR
from shapes import SHAPES
from utils import draw_tetromino, draw_text, draw_button

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.reset()

    def reset(self):
        self.grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.tetromino = None
        self.next_tetromino = None
        self.held_tetromino = None
        self.held_tetromino_index = -1
        self.score = 0
        self.game_over = False
        self.can_hold = True
        self.tetromino_x, self.tetromino_y = GRID_WIDTH // 2 - 2, 0
        self.new_tetromino()
        self.gravity_counter = 0
        self.move_delay = 100  # milliseconds
        self.last_move_time = 0

    def new_tetromino(self):
        if self.next_tetromino is not None:
            self.tetromino = self.next_tetromino
            self.tetromino_index = self.next_tetromino_index
        else:
            self.tetromino_index = random.randint(0, len(SHAPES) - 1)
            self.tetromino = SHAPES[self.tetromino_index]
        self.next_tetromino_index = random.randint(0, len(SHAPES) - 1)
        self.next_tetromino = SHAPES[self.next_tetromino_index]

    def check_collision(self, tetromino, x, y):
        for i in range(len(tetromino)):
            for j in range(len(tetromino[i])):
                if tetromino[i][j] == 1:
                    if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or self.grid[y + i][x + j] != 0:
                        return True
        return False

    def merge_tetromino(self, tetromino, x, y):
        for i in range(len(tetromino)):
            for j in range(len(tetromino[i])):
                if tetromino[i][j] == 1:
                    if 0 <= y + i < GRID_HEIGHT and 0 <= x + j < GRID_WIDTH:
                        self.grid[y + i][x + j] = self.tetromino_index + 1

    def check_lines(self):
        lines = 0
        for i in range(len(self.grid)):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for x in range(GRID_WIDTH)])
                lines += 1
        self.score += lines ** 2

    def drop_tetromino(self):
        while not self.check_collision(self.tetromino, self.tetromino_x, self.tetromino_y + 1):
            self.tetromino_y += 1

    def hold_tetromino(self):
        if self.can_hold:
            if self.held_tetromino is None:
                self.held_tetromino = self.tetromino
                self.held_tetromino_index = self.tetromino_index
                self.new_tetromino()
            else:
                self.tetromino, self.held_tetromino = self.held_tetromino, self.tetromino
                self.tetromino_index, self.held_tetromino_index = self.held_tetromino_index, self.tetromino_index
            self.tetromino_x, self.tetromino_y = GRID_WIDTH // 2 - 2, 0
            self.can_hold = False

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_delay:
            if keys[pygame.K_LEFT] and not self.check_collision(self.tetromino, self.tetromino_x - 1, self.tetromino_y):
                self.tetromino_x -= 1
                self.last_move_time = current_time
            if keys[pygame.K_RIGHT] and not self.check_collision(self.tetromino, self.tetromino_x + 1, self.tetromino_y):
                self.tetromino_x += 1
                self.last_move_time = current_time
            if keys[pygame.K_DOWN] and not self.check_collision(self.tetromino, self.tetromino_x, self.tetromino_y + 1):
                self.tetromino_y += 1
                self.last_move_time = current_time

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.game_over:
                if event.key == pygame.K_UP:
                    rotated_tetromino = list(zip(*self.tetromino[::-1]))
                    if not self.check_collision(rotated_tetromino, self.tetromino_x, self.tetromino_y):
                        self.tetromino = rotated_tetromino
                if event.key == pygame.K_SPACE:
                    self.drop_tetromino()
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.hold_tetromino()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                x, y = event.pos
                if SCREEN_WIDTH // 2 - 50 <= x <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 20 <= y <= SCREEN_HEIGHT // 2 + 70:
                    self.reset()

    def update(self):
        if not self.game_over:
            self.gravity_counter += 1
            if self.gravity_counter >= FPS // 2:
                self.gravity_counter = 0
                if not self.check_collision(self.tetromino, self.tetromino_x, self.tetromino_y + 1):
                    self.tetromino_y += 1
                else:
                    self.merge_tetromino(self.tetromino, self.tetromino_x, self.tetromino_y)
                    self.check_lines()
                    self.new_tetromino()
                    self.tetromino_x, self.tetromino_y = GRID_WIDTH // 2 - 2, 0
                    self.can_hold = True
                    if self.check_collision(self.tetromino, self.tetromino_x, self.tetromino_y):
                        self.game_over = True

            self.handle_movement()

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != 0:
                    pygame.draw.rect(self.screen, COLORS[self.grid[i][j] - 1], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        draw_tetromino(self.screen, self.tetromino, self.tetromino_x * BLOCK_SIZE, self.tetromino_y * BLOCK_SIZE, self.tetromino_index, BLOCK_SIZE)
        draw_text(self.screen, "Score: " + str(self.score), SCREEN_WIDTH + 10, 10, self.font, WHITE)
        draw_text(self.screen, "Next:", SCREEN_WIDTH + 10, 50, self.font, WHITE)
        draw_tetromino(self.screen, self.next_tetromino, SCREEN_WIDTH + 10, 80, self.next_tetromino_index, BLOCK_SIZE)
        draw_text(self.screen, "Hold:", SCREEN_WIDTH + 10, 200, self.font, WHITE)
        if self.held_tetromino is not None:
            draw_tetromino(self.screen, self.held_tetromino, SCREEN_WIDTH + 10, 230, self.held_tetromino_index, BLOCK_SIZE)
        if self.game_over:
            self.draw_text_with_shadow_and_outline("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text(self.screen, "Score: " + str(self.score), SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20, self.font, WHITE)
            draw_button(self.screen, self.font, "Retry", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20, 100, 50)
        pygame.display.flip()

    def draw_text_with_shadow_and_outline(self, text, x, y):
        shadow_offset = 5
        outline_thickness = 2
        img = self.large_font.render(text, True, RED)
        text_width = img.get_width()
        text_height = img.get_height()

        x -= text_width // 2  # Adjust x to center the text

        # Draw shadow
        draw_text(self.screen, text, x + shadow_offset, y + shadow_offset, self.large_font, SHADOW_COLOR)

        # Draw outline
        for dx in [-outline_thickness, outline_thickness]:
            for dy in [-outline_thickness, outline_thickness]:
                draw_text(self.screen, text, x + dx, y + dy, self.large_font, OUTLINE_COLOR)

        # Draw main text
        draw_text(self.screen, text, x, y, self.large_font, RED)
