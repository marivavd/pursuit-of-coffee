import sys
from const import *
from load_image import load_image


class Images(pygame.sprite.Sprite):

    def __init__(self, group, x, y, image):
        super().__init__(group)
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
    intro_text = ["Pursuit of coffee", "",
                  "Выберите персонажа:"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    all_sprites = pygame.sprite.Group()
    image_r = pygame.transform.scale(load_image('raccoon.png', -1), (213, 177))
    raccoon = Images(all_sprites, -10, 170, image_r)
    all_sprites.add(raccoon)
    rect_r = raccoon.rect
    color_r = (0, 165, 80)
    image_h = pygame.transform.scale(load_image('hedgehog.png', -1), (203, 167))
    hedgehog = Images(all_sprites, 180, 170, image_h)
    all_sprites.add(hedgehog)
    rect_h = hedgehog.rect
    color_h = (128, 128, 128)
    image_s = load_image('start.png', -1)
    start = Images(all_sprites, 400, 350, image_s)
    all_sprites.add(start)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    colors = [(100, 37, 51), (0, 0, 0), (0, 0, 0)]
    n = 0
    for line in intro_text:
        string_rendered = font.render(line, True, colors[n])
        n += 1
        font = pygame.font.Font(None, 50)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if start.rect.collidepoint(x, y):
                    if color_r == (0, 165, 80):
                        return 'raccoon'
                    else:
                        return 'hedgehog'
                elif hedgehog.rect.collidepoint(x, y):
                    if color_h != (0, 165, 80):
                        color_h = (0, 165, 80)
                        color_r = (128, 128, 128)
                elif raccoon.rect.collidepoint(x, y):
                    if color_r != (0, 165, 80):
                        color_r = (0, 165, 80)
                        color_h = (128, 128, 128)
        pygame.draw.rect(screen, color_r,
                         (rect_r[0] + 40, rect_r[1] + 30, rect_r[2] - 60, rect_r[3] - 30), 8)
        pygame.draw.rect(screen, color_h,
                         (rect_h[0] + 10, rect_h[1] + 30, rect_h[2] - 20, rect_h[3] - 20), 8)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
