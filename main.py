import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH + 150, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    game = Game(screen, clock)

    while True:
        clock.tick(FPS)
        game.update()
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            game.handle_event(event)

if __name__ == "__main__":
    main()
    pygame.quit()
