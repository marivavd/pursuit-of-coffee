import sys
import time
from Items import *


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False
        self.change = False
        self.goose = False
        self.knife = 0
        self.mina = 0
        self.throw_knife = []
        self.mina_time = []

    def check_event(self, hero):
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_key(event, hero)
                # сделать так, чтобы при смене персонажа, и нож, и мина оставались у него

    def check_key(self, event, hero):
        # обработка нажатия на кнопку
        if event.key == pygame.K_UP:  # прыжок
            self.isjump = True
        elif event.key == pygame.K_LEFT:
            hero.shift_side(-1)
        elif event.key == pygame.K_RIGHT:
            hero.shift_side()
        elif event.key == pygame.K_DOWN:  # оставлять мину
            if self.mina > 0:
                self.mina_time.append([hero.x, hero.y + 40, time.perf_counter()])
                self.mina -= 1
            if not self.mina:
                hero.img = pygame.transform.scale(load_image(f'{hero.name}.png'), (width // 6, height // 6))
        elif event.key == pygame.K_SPACE:  # пулять ножом во врага
            if self.knife > 0:
                self.throw_knife.append(pygame.transform.scale(load_image('knife.png', -1), (100, 100)).get_rect(
                    topleft=(hero.x - 30, hero.y)))
                self.knife -= 1
                if self.knife == 0:
                    if hero.name == 'raccoon':
                        hero.img = pygame.transform.scale(load_image('raccoon.png'), (width // 6, height // 6))
                    elif hero.name == 'hedgehog':
                        hero.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 6, height // 6))
                    else:
                        hero.img = pygame.transform.scale(load_image('goose.png'), (width // 6, height // 6))
        elif event.key == pygame.K_SPACE and self.knife > 0:  # пулять ножом во врага
            self.knife -= 1
            if not self.knife:
                hero.img = pygame.transform.scale(load_image(f'{hero.name}.png'), (width // 6, height // 6))

    def check_contact(self, hero, groups):
        sl_group = {all_obstacles: self.crash_obstacles,
                    things: self.crash_things,
                    weapon: self.crash_weapon,
                    coffee: self.crash_coffee}
        for group in groups:
            for i in group:
                offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
                if hero.mask.overlap_area(i.mask, offset) > 0:
                    sl_group[group](hero, i)

    def crash_obstacles(self, hero, i):
        self.game_over = True
        i.kill()

    def crash_things(self, hero, i):
        if type(i) is Cap:
            self.goose = True
        elif type(i) is Glasses:
            self.change = True
        i.kill()

    def crash_weapon(self, hero, i):
        if type(i) is Knife:
            self.knife += 1
            self.take_knife(hero, i)
        elif type(i) is Mina:
            self.mina += 1
            self.take_mina(hero, i)
        i.kill()

    @staticmethod
    def crash_coffee(hero, i):
        i.invigorating(i)
        i.kill()

    @staticmethod
    def take_knife(hero, knife=None):
        hero.img = pygame.transform.scale(load_image(f'{hero.name}_with_knife.gif'), (width // 6, height // 6))
        hero.rect = hero.img.get_rect()
        hero.mask = pygame.mask.from_surface(hero.img)
        if knife is not None:
            knife.kill()

    @staticmethod
    def take_mina(hero, mina=None):
        hero.img = pygame.transform.scale(load_image(f'{hero.name}_with_mina.gif'), (width // 6, height // 6))
        hero.rect = hero.img.get_rect()
        hero.mask = pygame.mask.from_surface(hero.img)
        if mina is not None:
            mina.kill()

    def check_cofe(self, hero):
        period[0] -= 1
        if not 5 <= period[0] <= 20:
            self.game_over = True
            hero.measuring = 'hell'

# при гейм овер удалять все объекты!
