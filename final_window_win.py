import sys
from time import perf_counter
from const import load_image
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(intro_text, text_coord=50):
    """вывод текста"""
    font = pygame.font.Font('fonts/Zaychik-Regular.ttf', 80)
    top = -30
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (255, 105, 0))
        font = pygame.font.Font('fonts/Zaychik-Regular.ttf', 60)
        text_coord += 10
        text_x = width // 2 - string_rendered.get_width() // 2
        text_y = height // 2 - string_rendered.get_height() // 2 + top
        top += 100
        screen.blit(string_rendered, (text_x, text_y))


def open_win_window():
    """открытие окна выигрыша после пятого уровня перед кноцовкой"""
    time_begin = perf_counter()
    clock = pygame.time.Clock()
    running = True
    sound = pygame.mixer.Sound(f'sounds/breath.mp3')
    sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((10, 50, 40))
        init_intro_text(("You are still breathing", 'You are lucky'))
        screen.blit(pygame.transform.scale(load_image('great work.png'), (256, 256)), (550, 350))
        pygame.display.flip()
        clock.tick(50)
        if perf_counter() - time_begin >= 5:
            running = False
