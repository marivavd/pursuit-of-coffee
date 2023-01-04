from load_image import load_image
from animals import Hedgehog, Raccoon, Goose
from menu import pygame
from const import FPS, size, clock, period
from controls import Event
import obstacles, const


class Map:
    def __init__(self, screen, hero):
        self.screen = screen
        if hero == 'raccoon':
            self.hero, self.enemy = Raccoon(), Hedgehog()
        else:
            self.hero, self.enemy = Hedgehog(), Raccoon()
        self.sp_enemies = [self.enemy]
        self.event = Event()
        self.is_jump = False
        self.jump_count = 10
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)
        self.all_obstancles = pygame.sprite.Group()  # все препятствия
        self.things = pygame.sprite.Group()  # кепка и очки
        self.weapon = pygame.sprite.Group()  # нож и мина

    def start_screen(self):
        self.hero.x += 100
        self.t = 0
        chase = True
        while True:
            self.screen.fill((255, 255, 255))
            self.event.proverka(self.hero, self.all_obstancles, self.things, self.weapon)
            self.check_goose()
            self.jump()
            self.check_game_over(chase)
            self.t %= size[0]
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
            if self.sp_enemies[1].x >= -100:
                self.sp_enemies[1].x -= 5
            if self.sp_enemies[0].x >= -100:
                self.sp_enemies[0].x -= 5
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5

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
            self.screen.blit(self.fon, (-self.t, 0))
            self.screen.blit(self.fon, (-self.t + size[0], 0))
            if chase:
                self.run()
        else:
            print('Game over')

    def check_goose(self):
        if self.event.goose and len(self.sp_enemies) != 2:
            self.sp_enemies.append(self.hero)
            self.hero = Goose()
            self.hero.x = self.sp_enemies[1].x
            self.sp_enemies[1].x = self.enemy.x + 100
