import pygame

size = width, height = 800, 600
FPS = 20
period = 10
coffee = 5
clock = pygame.time.Clock()
ground_level = 500
track_width = 12
all_obstancles = pygame.sprite.Group()  # все препятствия
things = pygame.sprite.Group()  # кепка и очки
weapon = pygame.sprite.Group()  # нож и мина
cofe = pygame.sprite.Group()  # кофе
groups = [all_obstancles, things, weapon, cofe]
