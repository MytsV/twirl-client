import pygame
import sys

from graphics.common import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics.screens import ScreenManager, LoginScreen

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Twirl")


def main():
    clock = pygame.time.Clock()
    screen_manager = ScreenManager()
    screen_manager.set_screen(LoginScreen(screen_manager))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen_manager.handle_event(event)

        screen_manager.update()
        screen_manager.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
