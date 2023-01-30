import pygame
import os

pygame.init()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        return False
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


size = width, height = 800, 600
FPS = 50
period = [20, 20]
clock = pygame.time.Clock()
time = -1

all_obstacles = pygame.sprite.Group()  # все препятствия
things = pygame.sprite.Group()  # кепка и очки
weapon = pygame.sprite.Group()  # нож и мина
coffee = pygame.sprite.Group()  # кофе
house = pygame.sprite.Group()  # всё то, что находиться в доме
groups = (all_obstacles, things, weapon, coffee, house)
sl_fons = {'fon.jpg': {'ground_level': 500,
                       'track_width': 12},
           'hell.jpg': {'ground_level': 100,
                        'track_width': 12}}
