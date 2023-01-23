import sys
from const import pygame, load_image, width, height, clock, FPS, size
from settings import open_settings

pygame.init()


class Images(pygame.sprite.Sprite):

    def __init__(self, group, color, x, y, image):
        super().__init__(group)
        self.color = color
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def start_screen(screen, music, hell):
    """начать рисовать меню"""
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    init_intro_text(screen)
    hero1, music, hell = draw_heror(screen, music, hell)
    return hero1, music, hell


def init_intro_text(screen, text_coord=50,
                    colors=((100, 37, 51), (0, 0, 0), (0, 0, 0)),
                    intro_text=("Pursuit of coffee", "",
                                "Выберите персонажа:")):
    """вывести текст"""
    font = pygame.font.Font(None, 70)
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, colors[n])
        font = pygame.font.Font(None, 50)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def draw_heror(screen, music, hell):
    """нарисовать персонажей"""
    all_sprites = pygame.sprite.Group()
    raccoon = init_raccoon(all_sprites)
    hedgehog = init_hedgehog(all_sprites)
    start = init_start(all_sprites)
    settings_button = init_settings_button(all_sprites)
    hero = True
    while hero is True:
        hero, music, hell = check_event(raccoon, hedgehog, start, hero, settings_button, screen, music, hell)
        draw_rect(screen, raccoon, hedgehog)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return hero, music, hell


def init_raccoon(all_sprites):
    """наривать енота (Кофия)"""
    image_r = pygame.transform.scale(load_image('raccoon.png', -1), (213, 177))
    raccoon = Images(all_sprites, (0, 165, 80), -10, 170, image_r)
    all_sprites.add(raccoon)
    return raccoon


def init_hedgehog(all_sprites):
    """нарисовать ёжика"""
    image_h = pygame.transform.scale(load_image('hedgehog.png', -1), (203, 167))
    hedgehog = Images(all_sprites, (128, 128, 128), 180, 170, image_h)
    all_sprites.add(hedgehog)
    return hedgehog


def draw_rect(screen, raccoon, hedgehog):
    """нарисовать прямоугольники"""
    pygame.draw.rect(screen, raccoon.color,
                     (raccoon.rect[0] + 40, raccoon.rect[1] + 30,
                      raccoon.rect[2] - 60, raccoon.rect[3] - 30), 8)
    pygame.draw.rect(screen, hedgehog.color,
                     (hedgehog.rect[0] + 10, hedgehog.rect[1] + 30,
                      hedgehog.rect[2] - 20, hedgehog.rect[3] - 20), 8)


def init_start(all_sprites):
    """начать"""
    image_s = load_image('start.png', -1)
    start = Images(all_sprites, None, 400, 350, image_s)
    all_sprites.add(start)
    return start


def init_settings_button(all_sprites):
    """нарисовать кнопку настрок"""
    image_b = pygame.transform.scale(load_image('settings_button.png', -1), (115, 75))
    settings_button = Images(all_sprites, None, 700, 0, image_b)
    all_sprites.add(settings_button)
    return settings_button


def check_event(raccoon, hedgehog, start, hero, settings_button, screen, music, hell):
    """проверка всех возможных событий, которые согут произойти в меню"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if start.rect.collidepoint(x, y):
                hero = 'raccoon' if raccoon.color == (0, 165, 80) else 'hedgehog'
            elif hedgehog.rect.collidepoint(x, y) and hedgehog.color != (0, 165, 80):
                hedgehog.color = (0, 165, 80)
                raccoon.color = (128, 128, 128)
            elif raccoon.rect.collidepoint(x, y) and raccoon.color != (0, 165, 80):
                raccoon.color = (0, 165, 80)
                hedgehog.color = (128, 128, 128)
            elif settings_button.rect.collidepoint(x, y):
                music, hell = open_settings()
                fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
                screen.blit(fon, (0, 0))
                init_intro_text(screen)
    return hero, music, hell
