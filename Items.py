import pygame
from load_image import load_image
from const import coffee, weapon, things, all_obstacles, period
from time import perf_counter


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


class ActiveMine(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, z):
        super(ActiveMine, self).__init__()

        self.image = pygame.transform.scale(load_image('mina.png', -1), (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = pos_x
        self.rect.y = pos_y
        self.z = z

        self.timer = -1
        self.time_band = -1
        self.fly_height = 12
        self.band = False

    def redefine_pos(self, pos_x=0, pos_y=0, z=0):
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.z = z

    def activate(self):
        self.timer = perf_counter()

    def check_activate(self):
        return True if self.timer != -1 else False

    def move(self, screen, upheaval=1):
        if self.fly_height >= -12:
            self.fly(upheaval)
        self.rect.x -= 10
        self.draw_mina(screen)

        if self.rect.x <= 0:
            return self.explosion(screen)

    def draw_mina(self, screen):
        screen.blit(pygame.transform.scale(load_image('mina.png', -1), (100, 100)),
                    (self.rect.x, self.rect.y))

    def draw_band(self, screen):
        screen.blit(pygame.transform.scale(load_image('bang.png', -1), (200, 200)),
                    (self.rect.x, self.rect.y - 40))

    def fly(self, upheaval):
        if self.fly_height > 0:
            self.rect.y -= (self.fly_height ** 2) / 6 * upheaval
        else:
            self.rect.y += (self.fly_height ** 2) / 6 * upheaval
        self.fly_height -= 1

    def explosion(self, screen):
        if not self.band:
            self.band = True
            self.draw_band(screen)
            self.time_band = perf_counter()
            sound = pygame.mixer.Sound('sounds/bang.mp3')
            sound.play()
        else:
            if perf_counter() - self.time_band >= 2:
                return True
            else:
                self.draw_band(screen)
