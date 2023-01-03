from menu import *
from map import Map

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    hero = start_screen(screen)
    game_map = Map(screen, hero)
    game_map.start_screen()
