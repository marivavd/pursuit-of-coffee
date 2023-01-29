from time import perf_counter
from const import load_image
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


def init_intro_text(intro_text, text_coord=50):
    font = pygame.font.Font('fonts/Paper.otf', 100)
    top = -30
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (200, 0, 0))
        font = pygame.font.Font(None, 40)
        text_coord += 10
        text_x = width // 2 - string_rendered.get_width() // 2
        text_y = height // 2 - string_rendered.get_height() // 2 + top
        top += 30
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        screen.blit(string_rendered, (text_x, text_y))


def open_loss_window(time_pl):
    time_begin = perf_counter()
    time_of_game = int(time_begin - time_pl)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    sound = pygame.mixer.Sound(f'sounds/death_music.mp3')
    sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        init_intro_text(("Game is over", "", "", "", '', f'Вы играли {time_of_game} секунд'))
        screen.blit(pygame.transform.scale(load_image('blood.png'), (width // 3, height // 3)), (100, 10))
        screen.blit(pygame.transform.scale(load_image('grave.png'), (173, 213)), (550, 350))
        pygame.display.flip()
        clock.tick(50)
        if perf_counter() - time_begin >= 5:
            running = False
