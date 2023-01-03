from menu import *
from map import Map


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    map = Map(screen)
    map.start_screen()