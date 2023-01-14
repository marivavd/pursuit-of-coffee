import sys
from Items import *


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False
        self.change = False
        self.goose = False

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
            hero.is_jump = True
        elif event.key == pygame.K_LEFT:
            hero.shift_side(-1)
        elif event.key == pygame.K_RIGHT:
            hero.shift_side()
        elif event.key == pygame.K_DOWN:  # оставлять мину
            self.mina_time = hero.drop_mima()
        elif event.key == pygame.K_SPACE:  # пулять ножом во врага
            hero.drop_knife()

    def check_contact(self, hero, *groups):
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
        hero.alive = False
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
            hero.take_knife(i)
        elif type(i) is Mina:
            hero.take_mina(i)
        i.kill()

    @staticmethod
    def crash_coffee(hero, i):
        i.invigorating(i)
        i.kill()

    def check_cofe(self, hero):
        period[0] -= 1
        if not 5 <= period[0] <= 20:
            self.game_over = True
            hero.measuring = 'hell'

# при гейм овер удалять все объекты!
