from animals import Raccoon, Hedgehog, Goose
from time import perf_counter
from const import pygame, load_image, FPS, size, clock, period, sl_fons, groups, width, height, time
from Items import MiniCoffee, StandartCoffee, BigCoffee, Glasses, \
    Cap, Knife, Stone, Bush, Book, Mina, ActiveMine, House, Bed, Oven, Large_coffee, Flagpole
from controls import Event
from magic import magic
from new_level import new_level
from math import sin, cos, radians
from random import randint, choice
from final_window_win import open_win_window


class Map:
    """класс для обработки карты на которой происходят все события в обычном мире"""

    def __init__(self, screen, hero, sp_enemies):
        self.screen = screen
        self.hero, self.enemy = hero, sp_enemies[0]
        self.sp_enemies = sp_enemies
        self.hero.rect.x += 100  # 100 - рандомное число, нужно для того, чтобы персонаж был дальше, чем враг
        self.fon_new = 'fon.jpg'
        self.chase = True
        self.flag_weapon = True
        self.t, self.s = 0, 0
        self.time_pl1 = 0
        self.level = 1
        self.not_event = 0
        pygame.mixer.music.load(f'sounds/normal_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
        self.event = Event()
        self.time = time
        if self.hero.measuring == 'normal':
            self.fon = pygame.transform.scale(load_image('fon.jpg'), size)
            self.sp_fons = ['fon1.jpg', 'fon2.jpg', 'fon3.jpg', 'fon4.jpg']
        self._probability_sp = [[Stone] * 100,
                                [Bush] * 100,
                                [Book] * 100,
                                [MiniCoffee] * 25,
                                [StandartCoffee] * 10,
                                [BigCoffee] * 5,
                                [Glasses] * 1,
                                [Cap] * 1,
                                [Mina] * 2,
                                [Knife] * 2]

        self.music = ...
        self.hell = ...
        self.flag_end_generated = False

    def start_screen(self, level, music, hell, time_pl):
        """метод запускающий обработку карты"""
        self.music = music
        self.hell = hell
        if self.level == 1 and self.hero.measuring == 'normal':
            self.time_pl1 = perf_counter()
        else:
            self.time_pl1 = time_pl
        self.change_fon(level)
        if self.music:
            pygame.mixer.music.unpause()
        while self.check_game_over():
            self.t += period[0]
            self.s += period[0]
            self.not_event += 1

            self.draw_fon()
            if self.chase:
                self.draw_chas()

            pygame.display.flip()
            clock.tick(FPS)
            self.t %= size[0]

        return self.hero, self.sp_enemies, self.time_pl1

    def change_fon(self, level):
        self.level = 1 + level
        self.flag_weapon = False
        if self.level != 1:
            new_level(self.level)
        else:
            open_win_window()
        if self.level != 1 and self.level != 6:
            fon = choice(self.sp_fons)
            self.sp_fons.remove(fon)
            self.fon = pygame.transform.scale(load_image(fon), size)

    def draw_chas(self):
        """отрисовка погони догоняющего за убегающим и всех событий вокруг них"""
        self.draw_coffee_sensor()
        self.draw_hero()
        self.draw_enemies()
        self.draw_obj()
        self.draw_event()
        for group in groups:
            group.draw(self.screen)

    def draw_event(self):
        """проверка на то, что ничего не происходит | если происходит, то отображение этого"""
        self.event.check_contact(self.hero, *groups)
        self.event.check_event(self.hero)
        self.check_goose()
        self.check_mina_explosion()
        self.check_throw_knife()
        self.check_swap()

        if self.level == 1:
            self.generation_end()
        elif self.not_event > 100:
            self.generation_obj()
        if self.hero.is_jump:
            self.hero.jump(self.fon_new)
        if not self.s % 500:
            self.event.check_cofe(self.hero, self.sp_enemies, self.hell, self.screen)

    def draw_fon(self):
        """метод для рисования фона"""
        self.screen.blit(self.fon, (-self.t, 0))
        self.screen.blit(self.fon, (-self.t + size[0], 0))

    def draw_hero(self):
        """метод для рисования галавного героя"""
        self.screen.blit(self.hero.img, (self.hero.rect.x, self.hero.rect.y))
        if self.hero.rect.x > size[0] // 2:
            self.hero.rect.x -= 5

    def draw_enemies(self):
        """метод для рисования врагов"""
        for enemy in self.sp_enemies:
            if enemy.rect.x >= -100:
                enemy.rect.x -= 5
            self.screen.blit(enemy.img, (enemy.rect.x, enemy.rect.y))

    def check_swap(self):
        if self.event.swap:
            self.event.swap = False

            self.hero, self.enemy = self.enemy.copy(), self.hero.copy()  # смена ролей
            # сменя вещей
            if self.enemy.knife:
                self.hero.take_knife()
                self.enemy.reset_to_standard_img()
            if self.enemy.mina:
                self.hero.take_mina()
                self.enemy.reset_to_standard_img()
            old_pos_hero = self.hero.get_pos()   # смена координат
            self.hero.redefine_pos(*self.enemy.get_pos())
            self.enemy.redefine_pos(*old_pos_hero)

            self.sp_enemies[0] = self.enemy
            magic()

    def check_game_over(self):
        """метод для проверки продолжается ли игра"""
        if self.event.game_over:
            self.chase = False
            pygame.mixer.music.pause()
            self.kill_all()
            return False
        return True

    @staticmethod
    def kill_all():
        for group in groups:
            for item in group:
                item.kill()

    def draw_obj(self):
        """рисование объектов"""
        for group in groups:
            for obj in group:
                if self.fon_new == 'hell.jpg' and obj.rotate is False:
                    if obj.name == 'bush':
                        obj.image = pygame.transform.scale(load_image('hell_bush.png', -1), (100, 100))
                    obj.rotate = True
                    obj.image = pygame.transform.flip(obj.image, False, True)
                obj.rect.x -= 5

    def take_all_atributes_for_goose(self, goose):
        # переноc всех вещей
        if self.hero.is_jump:
            goose.jump_count = self.hero.jump_count
            goose.is_jump = self.hero.is_jump
        if self.hero.knife:
            goose.take_knife(self.hero.rect.x, self.hero.rect.y)
            self.hero.img = pygame.transform.scale(load_image(f'{self.hero.name}.png'), (width // 6, height // 6))
            self.hero.rect = self.hero.img.get_rect()
            self.hero.mask = pygame.mask.from_surface(self.hero.img)
        if self.hero.mina:
            goose.take_mina(self.hero.rect.x, self.hero.rect.y)
            self.hero.img = pygame.transform.scale(load_image(f'{self.hero.name}.png'), (width // 6, height // 6))
            self.hero.rect = self.hero.img.get_rect()
            self.hero.mask = pygame.mask.from_surface(self.hero.img)

    def check_goose(self):
        """если превращение в гуся должно произойти, то оно произойдёт"""
        if self.event.goose and len(self.sp_enemies) == 1:
            goose = Goose()
            # перенос координат x героя на координаты гуся
            goose.rect.y = self.hero.rect.y
            goose.rect.x = self.hero.rect.x
            while goose.z != self.hero.z:
                goose.z -= 1
            self.take_all_atributes_for_goose(goose)

            goose.measuring = self.hero.measuring

            # перенос координат врага на координаты героя
            self.hero.rect.y = self.enemy.rect.y
            self.hero.rect.x = self.enemy.rect.x + 100
            self.hero.z = self.enemy.z

            self.sp_enemies.append(self.hero)
            self.hero = goose
            magic()

    def get_probability(self):
        """взять список вероятностей появления предметов"""
        return self._probability_sp[:]

    def generation_obj(self):
        """метод для генерации объетов"""
        self.not_event = 0

        cls_obj = self.generation_cls_obj()
        track = randint(0, 2)
        ground_level = sl_fons[self.fon_new]['ground_level']
        track_width = sl_fons[self.fon_new]['track_width']
        cls_obj(size[0], ground_level - track_width * track, track)

    def generation_cls_obj(self):
        sp = self.get_probability()
        if self.flag_weapon:
            while [Mina] in sp or [Knife] in sp:
                sp.remove([Mina])
                sp.remove([Knife])

        cls_obj = choice(sp)[0]
        if cls_obj in (Mina, Knife) and not self.flag_weapon:
            self.flag_weapon = True
        return cls_obj

    def generation_end(self):
        """генерация объектов концовок"""
        if not self.flag_end_generated:
            self.flag_end_generated = True

            ground_level = sl_fons[self.fon_new]['ground_level']
            if type(self.hero) is Hedgehog:
                House(size[0], ground_level, 0)
                oven_x = Oven(size[0] + 10, ground_level, 0).rect.x
                Bed(size[0] + 20 + oven_x, ground_level, 0)
            elif type(self.hero) is Raccoon:
                Large_coffee(size[0], ground_level, 0)
            elif type(self.hero) is Goose:
                Flagpole(size[0], ground_level, 0)

    def check_throw_knife(self):
        """метод при помощи которого осуществляется правельное движение ножа во время полёта"""
        if len(self.event.throw_knife) != 0:
            self.draw_knife()
            if perf_counter() - self.event.throw_knife[2] >= 2:
                pygame.mixer.music.pause()
                self.event.throw_knife = []
                self.start_screen(self.level, self.music, self.hell, self.time_pl1)

    def draw_knife(self):
        """функция отрисовки ножа"""
        self.screen.blit(pygame.transform.scale(load_image('knife.png', -1), (100, 100)),
                         (self.event.throw_knife[0], self.event.throw_knife[1]))
        self.event.throw_knife[0] -= 10

    def check_mina_explosion(self):
        """выпущена ли мина? Если да, то отрисовать её и сменить уровень"""
        mina = self.event.active_mine
        if mina.check_activate():
            if not mina.move(self.screen):
                self.event.active_mine = ActiveMine(0, 0, 0)
                pygame.mixer.music.pause()
                self.start_screen(self.level, self.music, self.hell, self.time_pl1)

    def draw_coffee_sensor(self):
        """отрисовка датчика кофе"""
        center = (700, 50)

        # отображение самого счётчика
        self.draw_pie(self.screen, (122, 122, 122), center, 40, 0, 180)
        self.draw_pie(self.screen, (0, 125, 0), center, 40, 180, 225)
        self.draw_pie(self.screen, (125, 125, 0), center, 40, 225, 270)
        self.draw_pie(self.screen, (125, 0, 0), center, 40, 270, 315)
        self.draw_pie(self.screen, (0, 0, 0), center, 40, 315, 360)
        pygame.draw.circle(self.screen, (255, 0, 0), center, 40, 3)

        # рисование стрелки на счётчике
        coffe = period[0] - 5
        angle = 180 + 360 * coffe // 40
        pygame.draw.line(self.screen, (255, 0, 0), center,
                         (center[0] + 40 * cos(radians(angle)),
                          center[1] + 40 * sin(radians(angle))), 3)

    @staticmethod
    def draw_pie(scr, color, center, radius, start_angle, stop_angle):
        """вспомогательная фанкция для рисования заполненой дуги (кусочка пирога)"""
        radius -= 3
        theta = start_angle
        while theta <= stop_angle:
            pygame.draw.line(scr, color, center,
                             (center[0] + radius * cos(radians(theta)), center[1] + radius * sin(radians(theta))), 2)
            theta += 0.01


class Hell(Map):
    """класс для обработки карты на которой происходят все события в нижнем мире"""
    def __init__(self, screen, hero, sp_enemies):
        global fon_new
        super().__init__(screen, hero, sp_enemies)
        self.fon = pygame.transform.scale(load_image('hell.jpg'), size)
        self.fon = pygame.transform.rotate(self.fon, 180)
        self.fon_new = 'hell.jpg'
        self.hero.img = pygame.transform.flip(self.hero.img, False, True)
        self.hero.rect.y -= 400
        self.hero.old_y -= 400
        for i in range(len(self.sp_enemies)):
            self.sp_enemies[i].img = pygame.transform.flip(self.sp_enemies[i].img, False, True)
            self.sp_enemies[i].rect.y -= 400
        pygame.mixer.music.load(f'sounds/hell_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

    def check_goose(self):
        if self.event.goose and len(self.sp_enemies) != 2:
            super().check_goose()
            self.hero.img = pygame.transform.flip(self.hero.img, False, True)

    def draw_knife(self):
        """функция отрисовки ножа"""
        self.screen.blit(pygame.transform.scale(load_image('knife.png', -1), (100, 100)),
                         (self.event.throw_knife[0], self.event.throw_knife[1]))
        self.event.throw_knife[0] -= 10

    def check_mina_explosion(self):
        """выпущена ли мина? Если да, то отрисовать её и перейти в нормальный мир"""
        mina = self.event.active_mine
        if mina.check_activate():
            if not mina.move(self.screen, -1):
                self.event.active_mine = ActiveMine(0, 0, 0)
                pygame.mixer.music.pause()
                self.hero.measuring = 'normal'
                for enemy in self.sp_enemies:
                    enemy.measuring = 'normal'

    def draw_event(self):
        """проверка на то, что ничего не происходит | если происходит, то отображение этого"""
        self.event.check_contact(self.hero, *groups)
        self.event.check_event(self.hero)
        self.check_goose()
        self.check_mina_explosion()
        self.check_throw_knife()
        self.check_swap()

        if self.not_event > 100:
            self.generation_obj()
        if self.hero.is_jump:
            self.hero.jump(self.fon_new)

    def change_fon(self, level):
        ...
