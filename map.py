from load_image import load_image, pygame
from animals import Goose
from const import FPS, size, clock, period, sl_fons, groups, width, height, fon_new
from Items import MiniCoffee, StandartCoffee, BigCoffee, Glasses, Cap, Knife, Stone, Bush, Book, Mina
from controls import Event
from magic import magic
from new_level import new_level
from math import sin, cos, radians
from time import perf_counter
from random import randint, choice


class Map:
    """класс для обработки карты на которой происходят все события"""

    def __init__(self, screen, hero, sp_enemies):
        self.screen = screen
        self.hero, self.enemy = hero, sp_enemies[0]
        self.sp_enemies = sp_enemies
        self.hero.x += 100  # 100 - рандомное число, нужно для того, чтобы персонаж был дальше, чем враг

        self.chase = True
        self.t, self.s = 0, 0
        self.level = 1
        self.not_event = 0

        self.event = Event()
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

        self._probability_sp = [[Stone] * 100,
                                [Bush] * 100,
                                [Book] * 100,
                                [MiniCoffee] * 25,
                                [StandartCoffee] * 10,
                                [BigCoffee] * 5,
                                [Glasses] * 1,
                                [Cap] * 10000,
                                [Mina] * 2,
                                [Knife] * 2]

    def start_screen(self):
        """метод запускающий обработку карты"""
        # new_level(self.level)
        while self.check_game_over():
            self.t += period[0]
            self.s += period[0]
            self.not_event += 1

            self.draw_fon()
            if self.chase:
                self.draw_chas()

            pygame.display.flip()
            clock.tick(FPS)
            self.t %= size[0]

        return self.hero, self.sp_enemies

    def draw_chas(self):
        """отрисовка погони догоняющего за убегающим и всех событий вокруг них"""
        self.draw_coffee_sensor()
        self.draw_hero()
        self.draw_enemies()
        self.draw_obj()
        self.draw_event()

        self.mina_explosion()
        self.throw_knife()
        for group in groups:
            group.draw(self.screen)

    def draw_event(self):
        """проверка на то, что ничего не происходит,| а если происходит, то отображение этого"""
        self.event.check_contact(self.hero, *groups)
        self.check_goose()
        self.event.check_event(self.hero)

        if self.not_event > 100:
            self.generation_obj()
        if self.hero.is_jump:
            self.hero.jump()
        if self.s > 10_000:
            self.end()
        if not self.s % 500:
            self.event.check_cofe(self.hero)

    def draw_fon(self):
        self.screen.blit(self.fon, (-self.t, 0))
        self.screen.blit(self.fon, (-self.t + size[0], 0))

    def draw_hero(self):
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5

    def draw_enemies(self):
        for enemy in self.sp_enemies:
            if enemy.x >= -100:
                enemy.x -= 5
            self.screen.blit(enemy.img, (enemy.x, enemy.y))

    def check_game_over(self):
        if self.event.game_over:
            self.chase = False
            return False
        return True

    @staticmethod
    def draw_obj():
        for group in groups:
            for obj in group:
                obj.rect.x -= 5

    def check_goose(self):
        if self.event.goose and len(self.sp_enemies) != 2:
            goose = Goose()
            goose.y = self.hero.y
            goose.x = self.hero.x
            goose.z = self.hero.z

            self.hero.y = self.enemy.y
            self.hero.x = self.enemy.x + 100
            self.hero.z = self.enemy.z

            self.sp_enemies.append(self.hero)
            self.hero = goose

            if self.hero.knife:
                self.hero.take_knife()
            if self.hero.mina:
                self.hero.take_mina()

            magic()

    def get_probability(self):
        return self._probability_sp

    def generation_obj(self):
        cls_obj = choice(self.get_probability())[0]
        track = randint(0, 2)
        cls_obj(600, sl_fons[fon_new]['ground_level'] - track * sl_fons[fon_new]['track_width'], track)
        self.not_event = 0

    def throw_knife(self):
        # не прошло рефакторинг
        if len(self.event.throw_knife):
            for el in self.event.throw_knife:
                self.screen.blit(pygame.transform.scale(load_image('knife.png', -1), (100, 100)), (el.x, el.y))
                el.x -= 10
                for (index, enemy_el) in self.sp_enemies:
                    if el.colliderect(enemy_el):
                        self.event.throw_knife.pop(index)
                        self.start_screen(self.level)

    def end(self):
        ...

    def mina_explosion(self):
        if len(self.event.mina_time):
            print(self.event.mina_time)
            now = perf_counter()
            self.event.mina_time[0] -= self.t
            if now - self.event.mina_time[2] >= 3:
                self.screen.blit(pygame.transform.scale(load_image('bang.png', -1), (100, 100)),
                                 (self.event.mina_time[0], self.event.mina_time[1]))
                self.event.mina_time = []
                sound = pygame.mixer.Sound('sounds/bang.mp3')
                sound.play()
                while perf_counter() - now < 2:
                    pass
                self.start_screen()
            else:
                self.screen.blit(pygame.transform.scale(load_image('mina.png', -1), (100, 100)),
                                 (self.event.mina_time[0], self.event.mina_time[1]))

    def draw_coffee_sensor(self):
        center = (700, 50)

        # отображение самого счётчика
        self.draw_pie(self.screen, (122, 122, 122), center, 40, 0, 180)
        self.draw_pie(self.screen, (0, 125, 0), center, 40, 180, 225)
        self.draw_pie(self.screen, (125, 125, 0), center, 40, 225, 270)
        self.draw_pie(self.screen, (125, 0, 0), center, 40, 270, 315)
        self.draw_pie(self.screen, (0, 0, 0), center, 40, 315, 360)
        pygame.draw.circle(self.screen, (255, 0, 0), center, 40, 3)

        # рисование стрелки на счётчике
        coffe = period[0] - 5
        angle = 180 + 360 * coffe // 40
        pygame.draw.line(self.screen, (255, 0, 0), center,
                         (center[0] + 40 * cos(radians(angle)),
                          center[1] + 40 * sin(radians(angle))), 3)

    @staticmethod
    def draw_pie(scr, color, center, radius, start_angle, stop_angle):
        radius -= 3
        theta = start_angle
        while theta <= stop_angle:
            pygame.draw.line(scr, color, center,
                             (center[0] + radius * cos(radians(theta)), center[1] + radius * sin(radians(theta))), 2)
            theta += 0.01


class Hell(Map):
    ...
