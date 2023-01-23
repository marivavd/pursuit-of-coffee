import time
from time import perf_counter
from map import time
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(intro_text, text_coord=50):
    font = pygame.font.Font('fonts/Paper.otf', 100)
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (255, 0, 0))
        font = pygame.font.Font(None, 40)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

def open_loss_window():
    time_begin = perf_counter()
    time_of_game = int(time_begin - time)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        init_intro_text(("Game is over", "", "", "", '', f'Вы играли {time_of_game} секунд'))
        pygame.display.flip()
        clock.tick(50)
        if perf_counter() - time_begin >= 3:
            running = False
