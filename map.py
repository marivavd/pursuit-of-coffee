from load_image import load_image
from animals import Hedgehog, Raccoon
from menu import pygame, sys
from const import FPS, size, clock, period
import controls
import obstacles


class Map:
    def __init__(self, screen, hero):
        self.screen = screen
        if hero == 'raccoon':
            self.hero = Raccoon()
            self.enemy = Hedgehog()
        else:
            self.hero = Hedgehog()
            self.enemy = Raccoon()
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

    def start_screen(self):
        all_obstancles = pygame.sprite.Group()
        t = 0
        chase = True
        while True:
            self.event()
            t += 20
            self.screen.blit(self.fon, (-t, 0))
            self.screen.blit(self.fon, (-t + size[0], 0))
            if chase:
                self.run()
            if self.hero.flag_jump:
                self.hero.jump()
            t %= size[0]
            pygame.display.flip()
            clock.tick(FPS)

    def event(self):
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.hero.flag_jump = True
                    self.hero.flag_rise = True
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    self.hero.shift_side(-1)
                elif event.key == pygame.K_RIGHT:
                    self.hero.shift_side()

    def run(self):
        # чёт не особо относительно солид, не уверен, но, мне кажежется,
        # что перемещение персонажей должно быть в этих персонажах
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5
        if self.enemy.x >= -150:
            self.enemy.x -= 5
