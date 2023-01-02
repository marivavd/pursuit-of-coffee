import pygame, sys
from const import *
from load_image import load_image



def terminate():
    pygame.quit()
    sys.exit()

def start_screen(screen):
    intro_text = ["Pursuit of coffee", "",
                  "Выберите персонажа:",]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    all_sprites = pygame.sprite.Group()
    image_s = load_image('start.png', -1)
    start = pygame.sprite.Sprite(all_sprites)
    start.image = image_s
    start.rect = start.image.get_rect()
    start.rect.x = 300
    start.rect.y = 350
    image_r = pygame.transform.scale(load_image('raccoon.png', -1), (203, 167))
    raccoon = pygame.sprite.Sprite(all_sprites)
    raccoon.image = image_r
    raccoon.rect = raccoon.image.get_rect()
    raccoon.rect.x = 400
    raccoon.rect.y = 100
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
                    print(0)
                    return  # начинаем игру
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
