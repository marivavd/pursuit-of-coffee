from load_image import load_image
from animals import Hedgehog, Raccoon, Goose
from menu import pygame
from const import FPS, size, clock, period, \
    ground_level, track_width, groups
from random import randint, choice
from Items import MiniCofe, StandartCofe, BigCofe, Glasses, Cap, Knife, Stone, Bush, Book
from controls import Event


class Map:
    def __init__(self, screen, hero):
        self.screen = screen
        if hero == 'raccoon':
            self.hero, self.enemy = Raccoon(), Hedgehog()
        else:
            self.hero, self.enemy = Hedgehog(), Raccoon()
        self.sp_enemies = [self.enemy]
        self.event = Event()
        self.a = 0
        self.t = 0
        self.not_event = 0
        self.is_jump = False
        self.jump_count = 10
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

    def start_screen(self):
        self.hero.x += 100
        chase = True
        while True:
            self.screen.fill((255, 255, 255))
            self.event.proverka(self.hero, *groups)
            self.check_goose()
            self.jump()
            self.check_game_over(chase)
            self.t %= size[0]
            for i in groups:
                i.draw(self.screen)
            pygame.display.flip()
            clock.tick(FPS)

    def run(self):
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        if len(self.sp_enemies) != 2:
            self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
            if self.enemy.x >= -100:
                self.enemy.x -= 5
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
            if self.jump_count >= -10:
                if self.jump_count > 0:
                    self.hero.y -= (self.jump_count ** 2) / 2
                else:
                    self.hero.y += (self.jump_count ** 2) / 2
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10

    def check_game_over(self, chase):
        if not self.event.game_over:
            self.t += period
            self.not_event += 1
            self.screen.blit(self.fon, (-self.t, 0))
            self.screen.blit(self.fon, (-self.t + size[0], 0))
            if chase:
                self.run()
                self.generation_obj()
        else:
            print('Game over')

    def check_goose(self):
        self.a += 1
        # if self.event.goose and len(self.sp_enemies) != 2:
        if self.a == 56:
            self.sp_enemies.append(self.hero)
            self.hero = Goose()
            self.hero.x = self.sp_enemies[1].x
            self.sp_enemies[1].x = self.enemy.x + 100
            self.hero.y = self.sp_enemies[1].y
            self.sp_enemies[1].y = self.enemy.y

    def generation_obj(self):
        if self.not_event > 100:
            probability_sp = [[Stone] * 100,
                              [Bush] * 100,
                              [Book] * 100,
                              [MiniCofe] * 25,
                              [StandartCofe] * 10,
                              [BigCofe] * 5,
                              [Glasses] * 1,
                              [Cap] * 1,
                              [Knife] * 2]
            if 1 <= (track := randint(0, 3)) <= 3:
                cls_obj = choice(probability_sp)[0]
                cls_obj(600, ground_level - track * track_width)
                self.not_event = 0