import sys
from const import *
from load_image import load_image

pygame.init()


class Images(pygame.sprite.Sprite):

    def __init__(self, group, color, x, y, image):
        super().__init__(group)
        self.color = color
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Rect(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color):
        super().__init__(group)
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    init_intro_text(screen)
    hero1 = draw_heror(screen)
    return hero1


def init_intro_text(screen, text_coord=50,
                    colors=((100, 37, 51), (0, 0, 0), (0, 0, 0)),
                    intro_text=("Pursuit of coffee", "",
                                "Выберите персонажа:")):
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


def draw_heror(screen):
    all_sprites = pygame.sprite.Group()
    raccoon = init_raccoon(all_sprites)
    hedgehog = init_hedgehog(all_sprites)
    start = init_start(all_sprites)
    hero = True
    while hero is True:
        hero = event(raccoon, hedgehog, start, hero)
        draw_rect(screen, raccoon, hedgehog)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return hero


def init_raccoon(all_sprites):
    image_r = pygame.transform.scale(load_image('raccoon.png', -1), (213, 177))
    raccoon = Images(all_sprites, (0, 165, 80), -10, 170, image_r)
    all_sprites.add(raccoon)
    return raccoon


def init_hedgehog(all_sprites):
    image_h = pygame.transform.scale(load_image('hedgehog.png', -1), (203, 167))
    hedgehog = Images(all_sprites, (128, 128, 128), 180, 170, image_h)
    all_sprites.add(hedgehog)
    return hedgehog


def init_start(all_sprites):
    image_s = load_image('start.png', -1)
    start = Images(all_sprites, None, 400, 350, image_s)
    all_sprites.add(start)
    return start


def event(raccoon, hedgehog, start, hero):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
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
    return hero


def draw_rect(screen, raccoon, hedgehog):
    pygame.draw.rect(screen, raccoon.color,
                     (raccoon.rect[0] + 40, raccoon.rect[1] + 30,
                      raccoon.rect[2] - 60, raccoon.rect[3] - 30), 8)
    pygame.draw.rect(screen, hedgehog.color,
                     (hedgehog.rect[0] + 10, hedgehog.rect[1] + 30,
                      hedgehog.rect[2] - 20, hedgehog.rect[3] - 20), 8)
