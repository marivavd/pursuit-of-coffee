from load_image import load_image
from const import width, height
import pygame
import time


class Animal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pose = []
        self.x = 400
        self.y = 430
        self.z = 2
        self.measuring = 'hell'

        self.alive = True
        self.is_jump = False
        self.knife = False
        self.mina = False

        self.jump_count = 16
        self.koef = 6
        self.minus = 530

        self.img = ...
        self.rect = ...
        self.mask = ...
        self.name = ...

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

    def rise(self, name):
        self.koef -= 0.5
        self.y = self.minus - (height // self.koef)
        self.img = pygame.transform.scale(load_image(f'{name}.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)

    def drop_mima(self):
        if self.mina:
            self.mina = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            return [self.x, self.y + 40, time.perf_counter()]
        return []

    def drop_knife(self):
        if self.knife:
            self.knife = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            return [self.x, self.y + 40, time.perf_counter()]
        return []

    def take_knife(self, knife=None):
        self.knife = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_knife.gif'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        if knife is not None:
            knife.kill()

    def take_mina(self, mina=None):
        self.mina = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_mina.gif'), (width // 6, height // 6))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        if mina is not None:
            mina.kill()


class Raccoon(Animal):
    def __init__(self):
        super(Raccoon, self).__init__()
        self.img = pygame.transform.scale(load_image('raccoon.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'raccoon'
        self.minus += 10


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.img = pygame.transform.scale(load_image('hedgehog.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'hedgehog'


class Goose(Animal):
    def __init__(self):
        super(Goose, self).__init__()
        self.y -= 48
        self.img = pygame.transform.scale(load_image('goose.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'goose'
