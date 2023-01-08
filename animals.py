from load_image import load_image
import pygame
from const import width, height, sl_fons


class Animal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pose = []
        self.x = 400
        self.y = 430
        self.z = 2
        self.measuring = 'normal'
        self.alive = True
        self.is_jump = False
        self.jump_count = 16

    def shift_side(self, k=1):
        shift = 12 * k
        if 0 <= self.z - k <= 2:  # 3 = кол-во дорожек
            self.y += shift
            self.z -= k

    def jump(self):
        if self.is_jump:
            if self.jump_count >= -16:
                if self.jump_count > 0:
                    self.y -= (self.jump_count ** 2) / 6
                else:
                    self.y += (self.jump_count ** 2) / 6
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 16


class Raccoon(Animal):
    def __init__(self):
        super(Raccoon, self).__init__()
        self.img = pygame.transform.scale(load_image('raccoon.png'), (width // 7, height // 7))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.y += 20
        self.name = 'raccoon'


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'hedgehog'


class Goose(Animal):
    def __init__(self):
        super(Goose, self).__init__()
        self.y -= 48
        self.img = pygame.transform.scale(load_image('goose.png'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'goose'
