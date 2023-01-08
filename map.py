from load_image import load_image
from animals import Hedgehog, Raccoon, Goose
from menu import pygame
from const import FPS, size, clock, period, \
    ground_level, track_width, groups, width, height
from random import randint, choice
from Items import MiniCoffee, StandartCoffee, BigCoffee, Glasses, Cap, Knife, Stone, Bush, Book, Mina
from controls import Event
from magic import magic
import time, new_level
from math import sin, cos, radians


class Map:
    def __init__(self, screen, hero, enemies):
        self.screen = screen
        self.hero, self.enemy = hero, enemies[0]
        self.sp_enemies = enemies
        self.event = Event()
        self.t = 0
        self.s = 0
        self.a = 0
        self.not_event = 0
        self.is_jump = False
        self.jump_count = 16
        self.hero.x += 100
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

    def start_screen(self, last_level):
        self.level = last_level + 1
        new_level.new_level(self.level)
        chase = True
        while True:
            self.screen.fill((255, 255, 255))
            self.jump()
            self.event.proverka_contact(self.hero, *groups)
            if self.check_game_over(chase):
                break
            self.check_goose()
            self.event.proverka_event(self.hero)
            if self.s > 10_000:
                self.end()
            if not self.s % 500:
                self.event.check_cofe(self.hero)
            self.throw_knife()
            self.mina_explosion()
            self.t %= size[0]
            for i in groups:
                i.draw(self.screen)
            pygame.display.flip()
            clock.tick(FPS)
        return self.hero

    def run(self):
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        if len(self.sp_enemies) != 2:
            self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        else:
            self.screen.blit(self.sp_enemies[0].img, (self.sp_enemies[0].x, self.sp_enemies[0].y))
            self.screen.blit(self.sp_enemies[1].img, (self.sp_enemies[1].x, self.sp_enemies[1].y))
        self.offset()
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5

    def offset(self):
        for i in self.sp_enemies:
            if i.x >= -100:
                i.x -= 5
        for i in groups:
            for j in i:
                j.rect.x -= 5

    def jump(self):
        if self.event.isjump:
            self.event.isjump = False
            self.is_jump = True
        if self.is_jump:
            if self.jump_count >= -16:
                if self.jump_count > 0:
                    self.hero.y -= (self.jump_count ** 2) / 6
                else:
                    self.hero.y += (self.jump_count ** 2) / 6
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 16

    def check_game_over(self, chase):
        # перевести в декораторы и обернуть в него старт скрин
        if not self.event.game_over:
            self.t += period[0]
            self.s += period[0]
            self.not_event += 1
            self.screen.blit(self.fon, (-self.t, 0))
            self.screen.blit(self.fon, (-self.t + size[0], 0))
            if chase:
                self.draw_coffee_sensor()
                self.run()
                self.generation_obj()
        else:
            return True

    def check_goose(self):
        if self.event.goose and len(self.sp_enemies) != 2:
            if self.hero.name == 'raccoon':
                self.hero.img = pygame.transform.scale(load_image('raccoon.png'), (width // 6, height // 6))
            else:
                self.hero.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 6, height // 6))
            self.sp_enemies.append(self.hero)
            self.hero = Goose()
            self.hero.x = self.sp_enemies[1].x
            self.sp_enemies[1].x = self.enemy.x + 100
            self.hero.y = self.sp_enemies[1].y
            self.sp_enemies[1].y = self.enemy.y
            self.hero.z = self.sp_enemies[1].z
            if self.event.knife > 0:
                self.event.take_knife(self.hero)
            if self.event.mina > 0:
                self.event.take_mina(self.hero)
            magic()

    def generation_obj(self):
        if self.not_event > 100:
            probability_sp = [[Stone] * 100,
                              [Bush] * 100,
                              [Book] * 100,
                              [MiniCoffee] * 25,
                              [StandartCoffee] * 10,
                              [BigCoffee] * 5,
                              [Glasses] * 1,
                              [Cap] * 1,
                              [Mina] * 2,
                              [Knife] * 2]
            cls_obj = choice(probability_sp)[0]
            track = randint(0, 2)
            cls_obj(600, ground_level - track * track_width, track)
            self.not_event = 0

    def throw_knife(self):
        if len(self.event.throw_knife) != 0:
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
        if len(self.event.mina_time) != 0:
            for index in range(len(self.event.mina_time)):
                now = time.perf_counter()
                self.event.mina_time[index][0] -= self.t
                if now - self.event.mina_time[index][2] >= 3:
                    self.screen.blit(pygame.transform.scale(load_image('bang.png', -1), (100, 100)),
                                     (self.event.mina_time[index][0], self.event.mina_time[index][1]))
                    del self.event.mina_time[index]
                    sound = pygame.mixer.Sound('sounds/bang.mp3')
                    sound.play()
                    while time.perf_counter() - now < 2:
                        pass
                    self.start_screen(self.level)
                else:
                    self.screen.blit(pygame.transform.scale(load_image('mina.png', -1), (100, 100)),
                                     (self.event.mina_time[index][0], self.event.mina_time[index][1]))

    def draw_coffee_sensor(self):
        center = (700, 50)
        self.draw_pie(self.screen, (122, 122, 122), center, 40, 0, 180)
        self.draw_pie(self.screen, (0, 125, 0), center, 40, 180, 225)
        self.draw_pie(self.screen, (125, 125, 0), center, 40, 225, 270)
        self.draw_pie(self.screen, (125, 0, 0), center, 40, 270, 315)
        self.draw_pie(self.screen, (0, 0, 0), center, 40, 315, 360)
        coffe = period[0] - 5
        angle = 180 + 360 * coffe // 40
        pygame.draw.line(self.screen, (255, 0, 0), center,
                         (center[0] + 40 * cos(radians(angle)),
                          center[1] + 40 * sin(radians(angle))), 3)
        pygame.draw.circle(self.screen, (255, 0, 0), center, 40, 3)

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
