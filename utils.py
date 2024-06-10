import pygame
from settings import WHITE, BUTTON_COLOR, BUTTON_HOVER_COLOR, COLORS

def draw_tetromino(screen, tetromino, x, y, index, block_size):
    for i in range(len(tetromino)):
        for j in range(len(tetromino[i])):
            if tetromino[i][j] == 1:
                pygame.draw.rect(screen, COLORS[index], (x + j * block_size, y + i * block_size, block_size, block_size))

def draw_text(screen, text, x, y, font, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(screen, font, text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height), border_radius=8)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height), border_radius=8)
    draw_text(screen, text, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2, font, WHITE)
