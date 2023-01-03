import pygame, load_image


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image.load_image('stone.png', -1), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

class Bush(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image.load_image('bush.png', -1), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y