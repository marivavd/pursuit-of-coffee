from menu import start_screen, pygame, size
from map import Map, Hell, Raccoon, Hedgehog

sl_hero = {'raccoon': (Raccoon(), [Hedgehog()]),
           'hedgehog': (Hedgehog(), [Raccoon()])}


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    hero, enemies = sl_hero[start_screen(screen)]

    sl_measuring = {'hell': Hell,
                    'normal': Map}

    while hero.alive:  # пока персонаж жив, при его псевдо-смерти мы пермещаем его в соответствии с измерением
        cls_map = sl_measuring[hero.measuring]
        hero, enemies = cls_map(screen, hero, enemies).start_screen(0)
