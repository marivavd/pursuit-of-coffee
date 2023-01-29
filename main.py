from menu import start_screen, pygame, size
from map import Map, Hell
from final_window_loss import open_loss_window
from animals import Raccoon, Hedgehog
from time import perf_counter

music, hell = True, True  # музыка и ад включены по умолчанию


def main():
    global music, hell
    sl_measuring = {'hell': Hell,
                    'normal': Map}
    sl_hero = {'raccoon': (Raccoon(), [Hedgehog()]),
               'hedgehog': (Hedgehog(), [Raccoon()])}

    pygame.init()
    screen = pygame.display.set_mode(size)
    hero, music, hell = start_screen(screen, music, hell)
    hero, enemies = sl_hero[hero]
    time_pl = perf_counter()
    while hero.alive:  # пока персонаж жив, при его псевдо-смерти мы пермещаем его в соответствии с измерением
        cls_map = sl_measuring[hero.measuring]
        hero, enemies, time_pl = cls_map(screen, hero, enemies).start_screen(0, music, hell, time_pl)
    open_loss_window(time_pl)


while 1:
    main()
