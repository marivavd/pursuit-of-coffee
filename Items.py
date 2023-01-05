import pygame
from load_image import load_image
from const import cofe, weapon, things, all_obstacles


class Item(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super(Item, self).__init__(group)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y


class Cofe(Item):
    def __init__(self, *args):
        super(Cofe, self).__init__(*args, cofe)
        cofe.add(self)

    def invigorating(self):
        ...


class MiniCofe(Cofe):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(MiniCofe, self).__init__(*args)


class StandartCofe(Cofe):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(StandartCofe, self).__init__(*args)


class BigCofe(Cofe):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(BigCofe, self).__init__(*args)


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


class Knife(Weapon):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(Knife, self).__init__(*args)
        self.name = 'knife'


class Mina(Weapon):
    def __init__(self, *args):
        super(Mina, self).__init__(*args)
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        self.name = 'mina'


class Obstacle(Item):
    def __init__(self, *args):
        super(Obstacle, self).__init__(*args, all_obstacles)
        all_obstacles.add(self)


class Stone(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('stone.png', -1), (100, 100))
        super().__init__(*args)


class Bush(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('bush.png', -1), (100, 100))
        super().__init__(*args)


class Book(Obstacle):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('book.png', -1), (100, 100))
        super().__init__(*args)
