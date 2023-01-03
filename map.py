from load_image import load_image
from animals import Hedgehog, Raccoon
from menu import terminate, pygame
from const import FPS, size, clock


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.hedgehog = Hedgehog()
        self.raccoon = Raccoon()
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)

    def start_screen(self):
        t = 0
        chase = False
        self.hedgehog.x += size[0] // 2
        while True:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            t += 20
            self.screen.blit(self.fon, (-t, 0))
            self.screen.blit(self.fon, (-t + size[0], 0))
            if t >= size[0] // 2:
                chase = True
            if chase:
                self.screen.blit(self.hedgehog.img, (self.hedgehog.x, self.hedgehog.y))
                self.screen.blit(self.raccoon.img, (self.raccoon.x, self.raccoon.y))
                if self.hedgehog.x > size[0] // 2:
                    self.hedgehog.x -= 5
                if self.raccoon.x >= -100:
                    self.raccoon.x -= 5
            t %= size[0]
            pygame.display.flip()
            clock.tick(FPS)