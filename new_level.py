import time
import sqlite3
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(line):
    """создать текст нового уровня"""
    font = pygame.font.Font('fonts/ofont.ru_Blood Cyrillic.ttf', 100)
    string_rendered = font.render(line, True, (255, 255, 255))
    intro_rect = string_rendered.get_rect(center=(width // 2, height // 2))
    screen.blit(string_rendered, intro_rect)


def check_level(level):
    con = sqlite3.connect("sounds.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT levels.name, levels.sound FROM levels
               WHERE levels.numer = {level}""").fetchall()
    return result[0][0], result[0][1]


def new_level(level):
    """переключить уровень на следующий"""
    time_begin = time.perf_counter()
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    line, sound = check_level(level)
    init_intro_text(line)
    sound = pygame.mixer.Sound(f'sounds/{sound}')
    sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        init_intro_text(line)
        pygame.display.flip()
        clock.tick(50)
        if time.perf_counter() - time_begin >= 3:
            running = False
