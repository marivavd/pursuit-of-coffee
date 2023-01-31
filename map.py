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
from win_window import open_victory_window
from welcome_to_normal_window import open_welcome_home_window


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
        self.was_hell = ...
        self.flag_end_generated = False

    def start_screen(self, level, music, hell, time_pl, was_hell):
        """Метод запускающий обработку карты"""
        self.was_hell = was_hell
        self.level = level
        if self.was_hell:
            self.hero.img = pygame.transform.flip(self.hero.img, False, True)
            self.hero.rect.y += 400
            self.hero.old_y += 400
            for i in range(len(self.sp_enemies)):
                self.sp_enemies[i].img = pygame.transform.flip(self.sp_enemies[i].img, False, True)
                self.sp_enemies[i].rect.y += 400
                self.sp_enemies[i].old_y += 400
        self.music = music
        self.hell = hell
        if self.hero.measuring == 'normal':
            self.change_fon(level)
        self.time_pl1 = perf_counter() if self.level == 1 and self.hero.measuring == 'normal' else time_pl
        self.was_hell = False
        self.run()

        return self.hero, self.sp_enemies, self.time_pl1, self.level

    def run(self):
        """Метод отвечающий за движение всего по карте"""
        if self.music:
            pygame.mixer.music.unpause()

        time_sleep = 0
        while self.check_game_over():
            if self.hero.flag_move:
                self.move()
                self.draw_fon()
                if self.chase:
                    self.draw_chas()
            else:
                self.event.raw_check_event()

            if self.hero.flag_end_behind:
                if not time_sleep:
                    time_sleep = perf_counter()
                elif perf_counter() - time_sleep > 2:
                    open_victory_window(self.time_pl1)

            for i in [self.hero, *self.sp_enemies]:
                i.update_img()

            pygame.display.flip()
            clock.tick(FPS)
            self.t %= size[0]

    def move(self):
        """Метод смещающий всё на period[0] количесво пикселей"""
        self.t += period[0]
        self.s += period[0]
        self.not_event += 1

    def change_fon(self, level):
        """Метод для обработки (выбора фона)"""
        self.level = 1 + level
        self.flag_weapon = False
        if self.level != 6 and self.was_hell is False:
            new_level(self.level)
        elif self.level == 1:
            open_win_window()
        if self.level != 1 and self.level != 6 and self.was_hell is False:
            fon = choice(self.sp_fons)
            self.sp_fons.remove(fon)
            self.fon = pygame.transform.scale(load_image(fon), size)

    def draw_chas(self):
        """Отрисовка погони догоняющего за убегающим и всех событий вокруг них"""
        self.draw_coffee_sensor()
        self.draw_hero()
        self.draw_enemies()
        self.draw_obj()
        self.draw_event()
        for group in groups:
            group.draw(self.screen)

    def draw_event(self):
        """Проверка на то, что ничего не происходит | если происходит, то отображение этого"""
        self.event.check_contact(self.hero, *groups)
        self.event.check_event(self.hero)
        self.check_goose()
        self.check_mina_explosion()
        self.check_throw_knife()
        self.check_swap()

        if self.level == 6:
            self.generation_end()
        elif self.not_event > 100:
            self.generation_obj()
        if self.hero.is_jump:
            self.hero.jump()
        if not self.s % 500:
            self.event.check_cofe(self.hero, self.sp_enemies, self.hell, self.screen)

    def draw_fon(self):
        """Метод для рисования фона"""
        self.screen.blit(self.fon, (-self.t, 0))
        self.screen.blit(self.fon, (-self.t + size[0], 0))

    def draw_hero(self):
        """Метод для рисования галавного героя"""
        self.screen.blit(self.hero.img, (self.hero.rect.x, self.hero.rect.y))
        if self.hero.rect.x > size[0] // 2:
            self.hero.rect.x -= 5

    def draw_enemies(self):
        """Метод для рисования врагов"""
        for enemy in self.sp_enemies:
            if enemy.rect.x >= -100:
                enemy.rect.x -= 5
            self.screen.blit(enemy.img, (enemy.rect.x, enemy.rect.y))

    def check_swap(self):
        """Метод меняющий местами героя и врага"""
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
            old_pos_hero = self.hero.get_pos()  # смена координат
            self.hero.redefine_pos(*self.enemy.get_pos())
            self.enemy.redefine_pos(*old_pos_hero)

            self.sp_enemies[0] = self.enemy
            magic()

    def check_game_over(self):
        """Метод для проверки продолжается ли игра"""
        if self.event.game_over:
            self.chase = False
            pygame.mixer.music.pause()
            self.kill_all()
            return False
        return True

    @staticmethod
    def kill_all():
        """УБИТЬ ВСЁ И ВСЯ"""
        for group in groups:
            for item in group:
                item.kill()

    def draw_obj(self):
        """Рисование объектов"""
        for group in groups:
            for obj in group:
                if self.fon_new == 'hell.jpg' and obj.rotate is False:
                    if obj.name == 'bush':
                        obj.image = pygame.transform.scale(load_image('hell_bush.png', -1), (100, 100))
                    obj.rotate = True
                    obj.image = pygame.transform.flip(obj.image, False, True)
                obj.rect.x -= 5

    def take_all_atributes_for_goose(self, goose):
        """Перенос всех вещей от персонажа к гусю"""
        if self.hero.is_jump:
            goose.jump_count = self.hero.jump_count
            goose.is_jump = self.hero.is_jump
        if self.hero.knife:
            goose.take_knife(self.hero.rect.x, self.hero.rect.y)
            self.hero.reset_to_standard_img()
        if self.hero.mina:
            goose.take_mina(self.hero.rect.x, self.hero.rect.y)
            self.hero.reset_to_standard_img()

    def check_goose(self):
        """если превращение в гуся должно произойти, то оно произойдёт"""
        if self.event.goose and len(self.sp_enemies) == 1:
            goose = Goose()
            # перенос координат x героя на координаты гуся
            goose.rect.y = self.hero.rect.y
            goose.rect.x = self.hero.rect.x
            goose.old_y = self.hero.old_y
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
        """Взять список вероятностей появления предметов"""
        return self._probability_sp[:]

    def generation_obj(self):
        """Метод для генерации объектов"""
        self.not_event = 0

        cls_obj = self.generation_cls_obj()
        track = randint(0, 2)
        ground_level = sl_fons[self.fon_new]['ground_level']
        track_width = sl_fons[self.fon_new]['track_width']
        cls_obj(size[0], ground_level - track_width * track, track)

    def generation_cls_obj(self):
        """Генерация класса объекта концовок"""
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
        """Генерация объектов концовок"""
        if not self.flag_end_generated:
            self.flag_end_generated = True

            ground_level = sl_fons[self.fon_new]['ground_level']
            if type(self.hero) is Hedgehog:
                House(size[0], ground_level, 0)
                oven_x = Oven(size[0], ground_level, 0).rect.x
                Bed(size[0] + oven_x, ground_level, 0)
            elif type(self.hero) is Raccoon:
                Large_coffee(size[0], ground_level, 0)
            elif type(self.hero) is Goose:
                Flagpole(size[0], ground_level, 0)

    def check_throw_knife(self):
        """Метод при помощи которого осуществляется правильное движение ножа во время полёта"""
        if len(self.event.throw_knife) != 0:
            self.draw_knife()
            if perf_counter() - self.event.throw_knife[2] >= 5:
                pygame.mixer.music.pause()
                self.event.throw_knife = []
                self.start_screen(self.level, self.music, self.hell, self.time_pl1, self.was_hell)

    def draw_knife(self):
        """Функция отрисовки ножа"""
        self.screen.blit(pygame.transform.scale(load_image('knife.png', -1), (100, 100)),
                         (self.event.throw_knife[0], self.event.throw_knife[1]))
        self.event.throw_knife[0] -= 10

    def check_mina_explosion(self):
        """Выпущена ли мина? Если да, то отрисовать её и сменить уровень"""
        mina = self.event.active_mine
        if mina.check_activate():
            if not mina.move(self.screen):
                self.event.active_mine = ActiveMine(0, 0, 0)
                pygame.mixer.music.pause()
                self.start_screen(self.level, self.music, self.hell, self.time_pl1, self.was_hell)

    def draw_coffee_sensor(self):
        """Отрисовка датчика кофе"""
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
        """Вспомогательная функция для рисования заполненной дуги (кусочка пирога)"""
        radius -= 3
        theta = start_angle
        while theta <= stop_angle:
            pygame.draw.line(scr, color, center,
                             (center[0] + radius * cos(radians(theta)), center[1] + radius * sin(radians(theta))), 2)
            theta += 0.01


class Hell(Map):
    """Класс для обработки карты на которой происходят все события в нижнем мире"""

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
            self.sp_enemies[i].old_y -= 400
        pygame.mixer.music.load(f'sounds/hell_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

    def check_goose(self):
        if self.event.goose and len(self.sp_enemies) != 2:
            super().check_goose()
            self.hero.img = pygame.transform.flip(self.hero.img, False, True)

    def draw_knife(self):
        """Функция отрисовки ножа"""
        self.screen.blit(pygame.transform.scale(load_image('knife.png', -1), (100, 100)),
                         (self.event.throw_knife[0], self.event.throw_knife[1]))
        self.event.throw_knife[0] -= 10

    def check_throw_knife(self):
        """метод при помощи которого осуществляется правельное движение ножа во время полёта"""
        if len(self.event.throw_knife) != 0:
            self.draw_knife()
            if perf_counter() - self.event.throw_knife[2] >= 2:
                pygame.mixer.music.pause()
                self.event.throw_knife = []
                self.hero.measuring = 'normal'
                for enemy in self.sp_enemies:
                    enemy.measuring = 'normal'
                self.was_hell = True
                pygame.mixer.music.pause()
                open_welcome_home_window()
                self.event.game_over = True

    def check_mina_explosion(self):
        """Выпущена ли мина? Если да, то отрисовать её и перейти в нормальный мир"""
        mina = self.event.active_mine
        if mina.check_activate():
            if not mina.move(self.screen, -1):
                self.event.active_mine = ActiveMine(0, 0, 0)
                pygame.mixer.music.pause()
                self.hero.measuring = 'normal'
                for enemy in self.sp_enemies:
                    enemy.measuring = 'normal'
                self.was_hell = True
                pygame.mixer.music.pause()
                open_welcome_home_window()
                self.event.game_over = True

    def draw_event(self):
        """Проверка на то, что ничего не происходит | если происходит, то отображение этого"""
        self.event.check_contact(self.hero, *groups)
        self.event.check_event(self.hero)
        self.check_goose()
        self.check_mina_explosion()
        self.check_throw_knife()
        self.check_swap()

        if self.not_event > 100:
            self.generation_obj()
        if self.hero.is_jump:
            self.hero.jump()

    def change_fon(self, level):
        ...
