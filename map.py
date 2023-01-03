from load_image import load_image
from animals import Hedgehog, Raccoon
from menu import terminate, pygame
from const import FPS, size, clock
import controls


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
        t = 0
        chase = False
        self.hero.x += size[0] // 2
        while True:
            self.screen.fill((255, 255, 255))
            controls.event()
            t += 20
            self.screen.blit(self.fon, (-t, 0))
            self.screen.blit(self.fon, (-t + size[0], 0))
            if t >= size[0] // 2:
                chase = True
            if chase:
                self.screen.blit(self.hero.img, (self.hero.x, self.hero.y))
                self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
                if self.hero.x > size[0] // 2:
                    self.hero.x -= 5
                if self.enemy.x >= -100:
                    self.enemy.x -= 5
            t %= size[0]
            pygame.display.flip()
            clock.tick(FPS)