import sys
import pygame


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False

    def proverka(self, hero, all_obstacles):
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.isjump = True
                elif event.key == pygame.K_LEFT:
                    hero.shift_side(-1)
                elif event.key == pygame.K_RIGHT:
                    hero.shift_side()
            elif True:
                for i in all_obstacles:
                    if not pygame.sprite.collide_mask(i, hero):
                        self.game_over = True
