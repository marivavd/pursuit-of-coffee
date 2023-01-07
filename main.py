from menu import start_screen, pygame, size
from map import Map, Hell

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    hero = start_screen(screen)
    game_map = Map(screen, hero)
    hero = game_map.start_screen(0)
    while hero.alive:
        if hero.measuring == 'hell':
            game_map = Hell(screen, hero.name)
            hero = game_map.start_screen(0)
        else:
            game_map = Map(screen, hero.name)
            hero = game_map.start_screen(0)
