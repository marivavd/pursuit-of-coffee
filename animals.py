from load_image import load_image
import pygame
from const import width, height


class Animal:
    def __init__(self):
        self.x = 1000
        self.y = 470
        self.z = 1
        self.pose = []


class Raccoon(Animal):
    def __init__(self):
        super(Raccoon, self).__init__()
        self.img = pygame.transform.scale(load_image('raccoon.png'), (width // 10, height // 10))


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 10, height // 10))


class Goose(Animal):
    ...
