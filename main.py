import pygame
from const import *
from menu import *


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()