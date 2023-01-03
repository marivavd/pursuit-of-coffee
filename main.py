from menu import *
from map import Map
import controls

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    hero = start_screen(screen)
    map = Map(screen, hero)
    map.start_screen()