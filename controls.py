import sys
import pygame
from const import width, height
from load_image import load_image


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False
        self.change = False
        self.goose = False
        self.knife = 0
        self.mina = 0
        self.throw_knife = []

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
                elif event.key == pygame.K_DOWN:  # оставлять мину
                    if self.mina > 0:
                        ...
                elif event.key == pygame.K_SPACE:  # пулять ножом во врага
                    if self.knife > 0:
                        self.throw_knife.append(pygame.transform.scale(load_image('cofe.png', -1), (100, 100)).get_rect(
                            topleft=(hero.x - 30, hero.y)))
                        self.knife -= 1
                        if self.knife == 0:
                            if hero.name == 'raccoon':
                                hero.img = pygame.transform.scale(load_image('raccoon.png'), (width // 6, height // 6))
                            elif hero.name == 'hedgehog':
                                hero.img = pygame.transform.scale(load_image('hedgehog.png'), (width // 6, height // 6))
                            else:
                                hero.img = pygame.transform.scale(load_image('goose.png'), (width // 6, height // 6))

    def proverka_contact(self, hero, all_obstacles, things, weapon, cofe):
        for i in all_obstacles:  # проверка на соприкосновение с препятствием
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0 and i.z == hero.z:
                self.game_over = True
        for i in things:  # проверка на соприкосновение с кепкой и очками
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0 and i.z == hero.z:
                if i.name == 'cap':
                    self.goose = True
                else:
                    self.change = True
        for i in weapon:  # проверка на соприкосновение с миной и ножом
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0 and i.z == hero.z:
                if i.name == 'knife':
                    self.knife += 1
                    self.take_knife(hero, i)
                else:
                    self.mina += 1
        for i in cofe:
            offset = (abs(hero.x - i.rect.x), abs(hero.y - i.rect.y))
            if hero.mask.overlap_area(i.mask, offset) > 0 and i.z == hero.z:
                i.invigorating(i.name)
            else:
                print(i.z, hero.z)

    @staticmethod
    def take_knife(hero, knife=None):
        if hero.name == 'raccoon':
            hero.img = pygame.transform.scale(load_image('raccoon_with_knife.gif'), (width // 6, height // 6))
        elif hero.name == 'hedgehog':
            hero.img = pygame.transform.scale(load_image('hedgehog_with_knife.gif'), (width // 6, height // 6))
        else:
            hero.img = pygame.transform.scale(load_image('goose_with_knife.gif'), (width // 6, height // 6))
        hero.rect = hero.img.get_rect()
        hero.mask = pygame.mask.from_surface(hero.img)
        if knife is not None:
            knife.kill()

    @staticmethod
    def take_mina(hero, mina=None):
        if hero.name == 'raccoon':
            hero.img = pygame.transform.scale(load_image('raccoon_with_mina.gif'), (width // 6, height // 6))
        elif hero.name == 'hedgehog':
            hero.img = pygame.transform.scale(load_image('hedgehog_with_mina.gif'), (width // 6, height // 6))
        else:
            hero.img = pygame.transform.scale(load_image('goose_with_mina.gif'), (width // 6, height // 6))
        hero.rect = hero.img.get_rect()
        hero.mask = pygame.mask.from_surface(hero.img)
        if mina is not None:
            mina.kill()
