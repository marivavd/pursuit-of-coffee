from load_image import load_image
from animals import Hedgehog, Raccoon
from menu import pygame
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
        is_jump = False
        jump_count = 10
        while True:
            self.screen.fill((255, 255, 255))
            controls.event(self.hero, all_obstancles)
            flag_jump = controls.check_jump()
            flag_game_over = controls.check_crash()
            if flag_jump:
                is_jump = True
            if is_jump:
                if jump_count >= -10:
                    if jump_count > 0:
                        self.hero.y -= (jump_count ** 2) / 2
                    else:
                        self.hero.y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 10
            if not flag_game_over:
                t += period
                self.screen.blit(self.fon, (-t, 0))
                self.screen.blit(self.fon, (-t + size[0], 0))
                if chase:
                    self.run()
            else:
                print('Game over')
            t %= size[0]
            pygame.display.flip()
            clock.tick(FPS)

    def run(self):
        self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if self.hero.x > size[0] // 2:
            self.hero.x -= 5
        if self.enemy.x >= -100:
            self.enemy.x -= 5
