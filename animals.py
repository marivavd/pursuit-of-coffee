from load_image import load_image
import pygame
from const import width, height, ground_level


class Animal:
    def __init__(self):
        self.pose = []
        self.x = 400
        self.y = 430
        self.max_y = 420
        self.min_y = 470

    def shift_side(self, k=1):
        shift = 12 * k
        if ground_level - abs(shift * 3) < self.min_y + shift < ground_level:  # 3 = колл дорожек
            self.y += shift
            self.max_y += shift
            self.min_y += shift


class Raccoon(Animal):
    def __init__(self):
        super(Raccoon, self).__init__()
        self.img = pygame.transform.scale(load_image('raccoon.png'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)


class Goose(Animal):
    ...
