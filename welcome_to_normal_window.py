import sys
import time
import sqlite3
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(line):
    """создать текст нового уровня"""
    font = pygame.font.Font('fonts/HomechristmasRegular.otf', 100)
    string_rendered = font.render(line, True, (200, 200, 255))
    intro_rect = string_rendered.get_rect(center=(width // 2, height // 2))
    screen.blit(string_rendered, intro_rect)


def open_welcome_home_window():
    """переключиться из ада в нормальный мир"""
    time_begin = time.perf_counter()
    clock = pygame.time.Clock()
    sound = pygame.mixer.Sound(f'sounds/welcome_home.mp3')
    sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((70, 170, 100))
        init_intro_text('Welcome home')
        pygame.display.flip()
        clock.tick(50)
        if time.perf_counter() - time_begin >= 5:
            running = False