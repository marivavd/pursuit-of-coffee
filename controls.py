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

    def proverka_event(self, hero):
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.isjump = True
                elif event.key == pygame.K_LEFT:
                    hero.shift_side(-1)
                elif event.key == pygame.K_RIGHT:
                    hero.shift_side()

    def proverka_contact(self, hero, all_obstacles, things, weapon, cofe):
        for i in all_obstacles:  # проверка на соприкосновение с препятствием
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0:
                self.game_over = True
        for i in things:  # проверка на соприкосновение с кепкой и очками
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0:
                if i.name == 'cap':
                    self.goose = True
                else:
                    self.change = True
        for i in weapon:  # проверка на соприкосновение с миной и ножом
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0:
                if i.name == 'knife':
                    self.knife = True
                else:
                    self.mina = True
        for i in cofe:
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0:
                i.invigorating(i.name)
