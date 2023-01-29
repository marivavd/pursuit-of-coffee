import sys
from time import perf_counter
from magic import magic
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(intro_text, text_coord=50):
    font = pygame.font.Font('fonts/20216.ttf', 100)
    top = -30
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (255, 255, 0))
        font = pygame.font.Font(None, 40)
        text_coord += 10
        text_x = width // 2 - string_rendered.get_width() // 2
        text_y = height // 2 - string_rendered.get_height() // 2 + top
        top += 30
        screen.blit(string_rendered, (text_x, text_y))


def open_victory_window(time_pl):
    time_begin = perf_counter()
    time_of_game = int(time_begin - time_pl)
    f = open("count_victories.txt", "r", encoding="utf8")
    count_win = int(f.read()) + 1
    f.close()
    f = open("count_victories.txt", "w", encoding="utf8")
    f.write(str(count_win))
    f.close()
    clock = pygame.time.Clock()
    running = True
    sound = pygame.mixer.Sound(f'sounds/fanfara.mp3')
    sound.play()
    magic()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        init_intro_text(("You win", "", "", "", '', f'Вы играли {time_of_game} секунд', '', '',
                         f'Общее количество ваших побед равно {count_win}'))
        pygame.display.flip()
        clock.tick(50)
        if perf_counter() - time_begin >= 7:
            running = False
