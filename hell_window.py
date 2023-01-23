import time
import sqlite3
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(line):
    """создать текст ада"""
    font = pygame.font.Font('fonts/ofont.ru_Blood Cyrillic.ttf', 100)
    string_rendered = font.render(line, True, (255, 255, 255))
    intro_rect = string_rendered.get_rect(center=(width // 2, height // 2))
    screen.blit(string_rendered, intro_rect)



def open_hell_window():
    """поприветствовать в аду"""
    time_begin = time.perf_counter()
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    init_intro_text('Welcome to hell')
    sound = pygame.mixer.Sound(f'sounds/welcome_to_hell.mp3')
    sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        init_intro_text('Welcome to hell')
        pygame.display.flip()
        clock.tick(50)
        if time.perf_counter() - time_begin >= 7:
            running = False
