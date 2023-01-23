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

        self.jump_count = 17
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
        if self.jump_count >= -17:
            print(self.measuring)
            if self.measuring == 'normal':
                if self.jump_count > 0:
                    self.rect.y -= (self.jump_count ** 2) / 9
                else:
                    self.rect.y += (self.jump_count ** 2) / 9
            elif self.measuring == 'hell':
                if self.jump_count > 0:
                    self.rect.y += (self.jump_count ** 2) / 9
                else:
                    self.rect.y -= (self.jump_count ** 2) / 9
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 17

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

    def drop_mima(self, x, y, mina):
        """выбрасывает мину"""
        # y выразить через координаты
        if self.mina:
            self.mina = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = x
                self.rect.y = y
            else:
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = x
                self.rect.y = y
            mina.redefine_pos(self.rect.x, self.rect.y + 40)
            mina.activate()

    def drop_knife(self, x, y):
        """выбросить нож"""
        if self.knife:
            self.knife = False
            self.img = pygame.transform.scale(load_image(f'{self.name}.png'), (width // 6, height // 6))
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = x
                self.rect.y = y
            else:
                self.rect = self.img.get_rect()
                self.mask = pygame.mask.from_surface(self.img)
                self.rect.x = x
                self.rect.y = y
            return [self.rect.x, self.rect.y + 10, perf_counter()]
        return []

    def take_knife(self, x=False, y=False, knife=None):
        """поднять нож"""
        x = x if x else self.rect.x
        y = y if y else self.rect.y
        self.knife = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_knife.gif'), (width // 6, height // 6))
        if self.measuring == 'hell':
            self.img = pygame.transform.flip(self.img, False, True)
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = x
            self.rect.y = y
        if knife is not None:
            knife.kill()

    def take_mina(self, x, y, mina=None):
        """поднять мину"""
        self.mina = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_mina.gif'), (width // 6, height // 6))
        if self.measuring == 'hell':
            self.img = pygame.transform.flip(self.img, False, True)
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = self.img.get_rect()
            self.mask = pygame.mask.from_surface(self.img)
            self.rect.x = x
            self.rect.y = y
        if mina is not None:
            mina.kill()

    def redefine_pos(self, pos_x=0, pos_y=0, z=0):
        """переопределяет координаты героя"""
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.z = z

    def get_pos(self):
        return self.rect.x, self.rect.y, self.z

    def copy(self):
        obj = type(self)()
        obj.redefine_pos(*self.get_pos())
        obj.measuring = self.measuring
        obj.img = self.img

        obj.is_jump = self.is_jump
        self.jump_count = self.jump_count
        self.koef = self.koef
        self.minus = self.minus

        if self.knife:
            obj.take_knife()
        if self.mina:
            obj.take_mina()

        return obj


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
