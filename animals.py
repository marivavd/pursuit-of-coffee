from const import pygame, width, height, sl_fons, load_image
from time import perf_counter


class Animal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pose = []
        self.z = 2
        self.measuring = 'normal'

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
        """выполняет перемещение по оси z, т.е. переход между дорожками"""
        shift = 12 * k
        if 0 <= self.z - k <= 2:  # 2 = кол-во дорожек - 1
            self.rect.y += shift
            self.z -= k

    def jump(self, fon: str):
        """выолняет прыжок"""
        # мне кажется, что сюда можно ввести несколько констант и не париться с ифами
        if self.jump_count >= -16:
            if self.measuring == 'normal':
                if self.jump_count > 0:
                    self.rect.y -= (self.jump_count ** 2) / 7
                else:
                    self.rect.y += (self.jump_count ** 2) / 7
            elif self.measuring == 'hell':
                if self.jump_count > 0:
                    self.rect.y += (self.jump_count ** 2) / 7
                else:
                    self.rect.y -= (self.jump_count ** 2) / 7
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 16

            # выразить через координаты травы (sl_fons[fon]['ground_level'])
            if self.measuring == 'normal':
                self.rect.y = 430
            else:
                self.rect.y = 30

            # перенесём героев на нужную дорожку
            if self.z <= 1:
                self.rect.y += 12
            if self.z == 0:
                self.rect.y += 12

    def rise(self, name):
        """подъём персонажа"""
        self.koef -= 0.5
        self.rect.y = self.minus - (height // self.koef)
        self.img = pygame.transform.scale(load_image(f'{name}.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)

    def drop_mima(self, mina):
        """выбросывает мину"""
        # y выразить через координаты
        if self.mina:
            self.mina = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = 400
                self.rect.y = 30
            else:
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = 400
                self.rect.y = 430
            mina.redefine_pos(self.rect.x, self.rect.y + 40)
            mina.activate()

    def drop_knife(self):
        """выбросить нож"""
        if self.knife:
            self.knife = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = 400
                self.rect.y = 30
            else:
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = 400
                self.rect.y = 430
            return [self.rect.x, self.rect.y + 40, perf_counter()]
        return []

    def take_knife(self, knife=None):
        """поднять нож"""
        self.knife = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_knife.gif'), (width // 6, height // 6))
        if self.measuring == 'hell':
            self.img = pygame.transform.flip(self.img, False, True)
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = 400
            self.rect.y = 30
        else:
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = 400
            self.rect.y = 430
        if knife is not None:
            knife.kill()

    def take_mina(self, mina=None):
        """поднять нож"""
        self.mina = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_mina.gif'), (width // 6, height // 6))
        if self.measuring == 'hell':
            self.img = pygame.transform.flip(self.img, False, True)
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = 400
            self.rect.y = 30
        else:
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = 400
            self.rect.y = 430
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
        self.rect.x = 400
        self.rect.y = 430


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.img = pygame.transform.scale(load_image('hedgehog.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'hedgehog'
        self.rect.x = 400
        self.rect.y = 430


class Goose(Animal):
    def __init__(self):
        super(Goose, self).__init__()
        self.img = pygame.transform.scale(load_image('goose.png'), (width // self.koef, height // self.koef))
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.name = 'goose'
        self.rect.x = 400
        self.rect.y = 430
