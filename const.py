import pygame

size = width, height = 800, 600
FPS = 50
period = [10, 10]
clock = pygame.time.Clock()
all_obstacles = pygame.sprite.Group()  # все препятствия
things = pygame.sprite.Group()  # кепка и очки
weapon = pygame.sprite.Group()  # нож и мина
cofe = pygame.sprite.Group()  # кофе
groups = (all_obstacles, things, weapon, cofe)

sl_fons = {'fon.jpg': {'ground_level': 500,
                       'track_width': 12},
           'fon1.jpg': {'ground_level': 500,
                        'track_width': 12}}
