import sys
from const import load_image
from const import pygame, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


class Images(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image, name):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name


def init_intro_text(text_coord=50, intro_text=("Настройки", "", "Музыка", "", 'Ад')):
    """вывод текста"""
    font = pygame.font.Font('fonts/Paper.otf', 100)
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (0, 0, 0))
        font = pygame.font.Font('fonts/Paper.otf', 50)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def init_images(all_sprites):
    """создание кнопки выхода и кнопок <on off>"""
    cross = Images(all_sprites, 725, 0, pygame.transform.scale(load_image('cross.png', -1), (76, 75)), 'cross')
    music_but = Images(all_sprites, 290, 200, pygame.transform.scale(load_image('on.png', -1), (128, 128)), 'music_on')
    hell_but = Images(all_sprites, 290, 330, pygame.transform.scale(load_image('on.png', -1), (128, 128)), 'hell_on')
    return cross, music_but, hell_but


def open_settings():
    """настройки игры"""
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    cross, music_but, hell_but = init_images(all_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if cross.rect.collidepoint(x, y):
                    sp = []
                    if music_but.name == 'music_on':
                        sp.append(True)
                    else:
                        sp.append(False)
                    if hell_but.name == 'hell_on':
                        sp.append(True)
                    else:
                        sp.append(False)
                    return sp
                elif music_but.rect.collidepoint(x, y):
                    if music_but.name == 'music_on':
                        music_but.image = pygame.transform.scale(load_image('off.png', -1), (128, 128))
                        music_but.name = 'music_off'
                    else:
                        music_but.image = pygame.transform.scale(load_image('on.png', -1), (128, 128))
                        music_but.name = 'music_on'
                elif hell_but.rect.collidepoint(x, y):
                    if hell_but.name == 'hell_on':
                        hell_but.image = pygame.transform.scale(load_image('off.png', -1), (128, 128))
                        hell_but.name = 'hell_off'
                    else:
                        hell_but.image = pygame.transform.scale(load_image('on.png', -1), (128, 128))
                        hell_but.name = 'hell_on'

        all_sprites.update()
        screen.fill((200, 200, 200))
        init_intro_text()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)
