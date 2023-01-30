from const import pygame, width, height, load_image, house
from time import perf_counter


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
        self.knife = False
        self.mina = False
        self.flag_end_behind = False
        self.flag_move = True

        self.jump_count = 19
        self.koef = 6
        self.minus = 530

        self.count_img = 2
        self.n_img = 1

        self.img = ...
        self.rect = ...
        self.mask = ...
        self.name = ...
        self.old_y = ...

        self.reset_to_standard_img()

    def shift_side(self, k=1):
        """выполняет перемещение по оси z, т.е. переход между дорожками"""
        shift = 12 * k
        if 0 <= self.z - k <= 2:  # 2 = кол-во дорожек - 1
            self.rect.y += shift
            self.old_y += shift
            self.z -= k

    def jump(self):
        """выолняет прыжок"""
        # мне кажется, что сюда можно ввести несколько констант и не париться с ифами
        if self.jump_count >= -19:
            if self.measuring == 'normal':
                if self.jump_count > 0:
                    self.rect.y -= (self.jump_count ** 2) / 10
                else:
                    self.rect.y += (self.jump_count ** 2) / 10
                    if self.rect.y >= self.old_y:
                        self.rect.y = self.old_y
                        self.is_jump = False
                        self.jump_count = 19
            elif self.measuring == 'hell':
                if self.jump_count > 0:
                    self.rect.y += (self.jump_count ** 2) / 10
                else:
                    self.rect.y -= (self.jump_count ** 2) / 10
                    if self.rect.y <= self.old_y:
                        self.rect.y = self.old_y
                        self.is_jump = False
                        self.jump_count = 19
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 19
            self.rect.y = self.old_y

    def drop_mima(self, x, y, mina):
        """выбрасывает мину"""
        # y выразить через координаты
        if self.mina:
            self.mina = False
            self.reset_to_standard_img()
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
            self.rect.x, self.rect.y = x, y
            mina.redefine_pos(self.rect.x, self.rect.y + 40)
            mina.activate()

    def drop_knife(self, x, y):
        """выбросить нож"""
        if self.knife:
            self.knife = False
            self.reset_to_standard_img()
            if self.measuring == 'hell':
                self.img = pygame.transform.flip(self.img, False, True)
            self.rect.x, self.rect.y = x, y
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

    def take_mina(self, x=False, y=False, mina=None):
        """поднять мину"""
        x = x if x else self.rect.x
        y = y if y else self.rect.y
        self.mina = True
        self.img = pygame.transform.scale(load_image(f'{self.name}_with_mina.gif'), (width // 6, height // 6))
        if self.measuring == 'hell':
            self.img = pygame.transform.flip(self.img, False, True)
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

    def update_img(self):
        self.n_img %= self.count_img
        self.n_img += 1
        if self.mina:
            self.reset_with_mina_img()
        if self.knife:
            self.reset_with_knife_img()
        if not (self.knife or self.mina):
            self.reset_to_standard_img()

    def reset_img(self):
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.rect.x, self.rect.y = self.x, self.y

    def reset_to_standard_img(self):
        self.reset_img()

    def reset_with_knife_img(self):
        self.reset_img()

    def reset_with_mina_img(self):
        self.reset_img()


class Raccoon(Animal):
    def __init__(self):
        super(Raccoon, self).__init__()
        self.name = 'raccoon'
        self.minus += 10
        self.rect.x = 400
        self.rect.y = 430
        self.old_y = 430

    def reset_to_standard_img(self):
        self.img = pygame.transform.scale(load_image(f'Raccoon/raccoon_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Raccoon, self).reset_to_standard_img()

    def reset_with_knife_img(self):
        self.img = pygame.transform.scale(load_image(f'Raccoon/raccoon_with_knife_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Raccoon, self).reset_to_standard_img()

    def reset_with_mina_img(self):
        self.img = pygame.transform.scale(load_image(f'Raccoon/raccoon_with_mina_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Raccoon, self).reset_to_standard_img()

    def end(self):
        """функция запуска сна"""
        self.flag_end_behind = True


class Hedgehog(Animal):
    def __init__(self):
        super(Hedgehog, self).__init__()
        self.name = 'hedgehog'
        self.rect.x = 400
        self.rect.y = 430
        self.old_y = 430

    def reset_to_standard_img(self):
        self.img = pygame.transform.scale(load_image(f'Hedgehog/hedgehog_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Hedgehog, self).reset_to_standard_img()

    def reset_with_knife_img(self):
        self.img = pygame.transform.scale(load_image(f'Hedgehog/hedgehog_with_knife_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Hedgehog, self).reset_to_standard_img()

    def reset_with_mina_img(self):
        self.img = pygame.transform.scale(load_image(f'Hedgehog/hedgehog_with_mina_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Hedgehog, self).reset_to_standard_img()

    def end(self):
        """функция запуска сна"""
        self.img = pygame.transform.scale(load_image('Hedgehog/hedgehog_in_the_bed.png'),
                                          (width // self.koef, height // self.koef))
        self.flag_move = False
        self.flag_end_behind = True


class Goose(Animal):
    def __init__(self):
        super(Goose, self).__init__()
        self.name = 'goose'
        self.rect.x = 400
        self.rect.y = 430
        self.old_y = 430

    def end(self):
        """функция запуска сна"""
        self.flag_end_behind = True

    def reset_to_standard_img(self):
        self.img = pygame.transform.scale(load_image(f'Goose/goose_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Goose, self).reset_to_standard_img()

    def reset_with_knife_img(self):
        self.img = pygame.transform.scale(load_image(f'Goose/goose_with_knife_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Goose, self).reset_to_standard_img()

    def reset_with_mina_img(self):
        self.img = pygame.transform.scale(load_image(f'Goose/goose_with_mina_{self.n_img}.png'),
                                          (width // self.koef, height // self.koef))
        super(Goose, self).reset_to_standard_img()
