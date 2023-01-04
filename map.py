from load_image import load_image
from animals import Hedgehog, Raccoon
from menu import pygame
from const import FPS, size, clock, period
from controls import Event
import obstacles, const


class Map:
    def __init__(self, screen, hero):
        self.screen = screen
        if hero == 'raccoon':
            self.hero = Raccoon()
            self.enemy = Hedgehog()
        else:
            self.hero = Hedgehog()
            self.enemy = Raccoon()
        self.event = Event()
        self.is_jump = False
        self.jump_count = 10
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

    def start_screen(self):
        all_obstancles = pygame.sprite.Group()
        things = pygame.sprite.Group()
        self.hero.x += 100
        self.t = 0
        chase = True
        while True:
            self.screen.fill((255, 255, 255))
            self.event.proverka(self.hero, all_obstancles)
            self.jump()
            self.check_game_over(chase)
            self.t %= size[0]
            pygame.display.flip()
            clock.tick(FPS)

    def run(self):
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5
        if self.enemy.x >= -100:
            self.enemy.x -= 5

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
