import pygame
from load_image import load_image


class Item(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super(Item, self).__init__(group)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y


class Cofe(Item):
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


class Glasses(Item):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(Glasses, self).__init__(*args)


class Cap(Item):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))
        super(Cap, self).__init__(*args)


class Knife(Item):
    def __init__(self, *args):
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))

        super(Knife, self).__init__(*args)


class Dynamite(Item):
    def __init__(self, *args):
        super(Dynamite, self).__init__(*args)
        self.image = pygame.transform.scale(load_image('cofe.png', -1), (100, 100))


class Obstacle(Item):
    ...


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
