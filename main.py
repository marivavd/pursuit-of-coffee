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
    is_hell = False
    was_hell = False
    level = 0
    while hero.alive:  # пока персонаж жив, при его псевдо-смерти мы пермещаем его в соответствии с измерением
        cls_map = sl_measuring[hero.measuring]
        if cls_map == Hell:
            is_hell = True
        if cls_map == Map and is_hell:
            is_hell = False
            was_hell = True
        hero, enemies, time_pl, now_level = cls_map(screen, hero, enemies).start_screen(level, music, hell, time_pl, was_hell)
        was_hell = False
        if not(now_level - 1 < level):
            level = now_level - 1
    open_loss_window(time_pl)


while 1:
    main()