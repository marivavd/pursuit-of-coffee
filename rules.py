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

def init_images(all_sprites):
    cross = Images(all_sprites, 725, 0, pygame.transform.scale(load_image('cross.png', -1), (76, 75)), 'cross')
    return cross


def init_intro_text(intro_text, text_coord=50):
    font = pygame.font.Font(None, 30)
    for n, line in enumerate(intro_text):
        string_rendered = font.render(line, True, (244, 255, 219))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def open_rules():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    cross = init_images(all_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if cross.rect.collidepoint(x, y):
                    return
        all_sprites.update()
        screen.fill((80, 200, 200))
        init_intro_text(['Доброго времени суток, дорогой пользователь!', 'Вас приветствуют енот Кофий, ёжик Торопыга и гусь Антон в своей игре.',
                         'Всего в ней 5 уровней.', 'Чтобы перейти на следующий уровень, нужно выпустить мину или нож.',
                         'Для выживания нужно собирать кофе.', 'Но не перестарайтесь с его количеством, так как много кофе вредно.',
                         'Пройди все уровни, чтобы увидеть концовку каждого персонажа!', '', '-> сместиться на дорожку правее',
                         '<- сместиться на дорожку левее', 'Стрелка вниз - выпустить мину', 'Стрелка вверх - прыжок', 'Пробел – выпустить во врага нож'])
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)