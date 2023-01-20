import pygame
from load_image import load_image
from const import coffee, weapon, things, all_obstacles, period


class Item(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, k, group):
        super(Item, self).__init__(group)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        # не понимаю, как сделать так, чтоб нижний край маски изображения = pos_y
        self.rect.y = pos_y - 50
        self.z = k
        self.rotate = False


class Coffee(Item):
    def __init__(self, *args):
        super(Coffee, self).__init__(*args, coffee)
        coffee.add(self)

    @staticmethod
    def invigorating(coffe):
        if type(coffe) is MiniCoffee:
            period[0] += 1
        elif type(coffe) is StandartCoffee:
            period[0] += 3
        elif type(coffe) is BigCoffee:
            period[0] += 5
        coffe.kill()


class MiniCoffee(Coffee):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(MiniCoffee, self).__init__(*args)
        self.name = 'minicofe'


class StandartCoffee(Coffee):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(StandartCoffee, self).__init__(*args)
        self.name = 'standartcofe'


class BigCoffee(Coffee):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(BigCoffee, self).__init__(*args)
        self.name = 'bigcoffee'


class Things(Item):
    def __init__(self, *args):
        super(Things, self).__init__(*args, things)
        things.add(self)


class Glasses(Things):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(Glasses, self).__init__(*args)
        self.name = 'glasses'


class Cap(Things):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(Cap, self).__init__(*args)
        self.name = 'cap'


class Weapon(Item):
    def __init__(self, *args):
        super(Weapon, self).__init__(*args, weapon)
        weapon.add(self)
        self.rect.y += 40


class Knife(Weapon):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('knife.png', -1), (100, 100))
        super(Knife, self).__init__(*args)
        self.name = 'knife'


class Mina(Weapon):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('mina.png', -1), (100, 100))
        super(Mina, self).__init__(*args)
        self.name = 'mina'
        self.rect.y += 40


class Obstacle(Item):
    def __init__(self, *args):
        super(Obstacle, self).__init__(*args, all_obstacles)
        all_obstacles.add(self)


class Stone(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('stone.png', -1), (100, 100))
        super().__init__(*args)
        self.name = 'stone'


class Bush(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('bush.png', -1), (100, 100))
        super().__init__(*args)
        self.name = 'bush'


class Book(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('book.png', -1), (100, 100))
        super().__init__(*args)
        self.name = 'stone'
