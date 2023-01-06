import time
import pygame
from const import size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(screen, line):
    font = pygame.font.Font('fonts/ofont.ru_Blood Cyrillic.ttf', 100)
    string_rendered = font.render(line, True, (255, 255, 255))
    intro_rect = string_rendered.get_rect(center=(width // 2, height // 2))
    screen.blit(string_rendered, intro_rect)


def check_level(level):
    if level == 1:
        return '1 level'
    elif level == 2:
        return '2 level'
    elif level == 3:
        return '3 level'
    elif level == 4:
        return '4 level'
    else:
        return '5 level'


def new_level(level):
    time_begin = time.perf_counter()
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    line = check_level(level)
    init_intro_text(screen, line)
    sound = pygame.mixer.Sound(f'sounds/{line}.mp3')
    sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        init_intro_text(screen, line)
        pygame.display.flip()
        clock.tick(50)
        if time.perf_counter() - time_begin >= 3:
            running = False
