import sys
import pygame


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False
        self.change = False
        self.goose = False
        self.knife = False
        self.mina = False

    def proverka(self, hero, all_obstacles, things, weapon, cofe):
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
                for i in all_obstacles:  # проверка на соприкосновение с препятствием
                    if not pygame.sprite.collide_mask(i, hero):
                        self.game_over = True
                for i in things:  # проверка на соприкосновение с кепкой и очками
                    if not pygame.sprite.collide_mask(i, hero):
                        if i.name == 'cap':
                            self.goose = True
                        else:
                            self.change = True
                for i in weapon:  # проверка на соприкосновение с миной и ножом
                    if not pygame.sprite.collide_mask(i, hero):
                        if i.name == 'knife':
                            self.knife = True
                        else:
                            self.mina = True
                for i in cofe:
                    if not pygame.sprite.collide_mask(i, hero):
                        i.invigorating()
