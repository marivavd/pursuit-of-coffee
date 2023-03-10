from animals import Raccoon, Hedgehog, Goose
from time import perf_counter
from const import pygame, load_image, FPS, size, clock, period, sl_fons, groups, time, del_period
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
    """Класс для обработки карты на которой происходят все события в обычном мире"""

    def __init__(self, screen, hero, sp_enemies):
        # перенос всех вводных данных в поля класса
        self.screen = screen
        self.hero, self.enemy = hero, sp_enemies[0]
        self.sp_enemies = sp_enemies

        # сдвиг главного героя на случайное число 100, чтобы герой не находился в одном месте с врагом
        self.hero.rect.x += 100

        # инициализация фона
        self.fon_new = 'fon.jpg'
        self.fon = pygame.transform.scale(load_image('fon.jpg'), size)
        self.sp_fons = ['fon1.jpg', 'fon2.jpg', 'fon3.jpg', 'fon4.jpg']

        # импорт из других модулей
        self.event = Event()
        self.time = time

        # инициализация флагов погони, наличия на карте оружия и флага того, что требуется генерировать погоню
        self.chase = True
        self.flag_weapon = False
        self.flag_end_generated = False

        # инициализация общего расстояния,
        # расстояния через которое нужно проверить кофе и
        # расстояние от предыдущего события
        # и времени после концовки
        self.t, self.s, self.not_event = 0, 0, 0
        self.time_pl1 = 0
        self.level = 1
        self.time_end_behind = 0

        # инициализация музыки
        pygame.mixer.music.load(f'sounds/normal_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

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

        # инициализация заглушек (вводных данных для start_screen)
        self.music = ...
        self.hell = ...
        self.was_hell = ...

        # установка нормальной скорости при переходе из одного мира в другой
        del_period()

    def start_screen(self, level, music, hell, time_pl, was_hell):
        # несколько напрягает количество аргументов, при добавлении нового нужно будет разгружать метод
        """Метод запускающий обработку карты"""
        self.input_arg(level, music, hell, time_pl, was_hell)  # хорошо б перенести в декоратор

        if self.was_hell:
            self.recovery_all_from_hell()
        if self.hero.measuring == 'normal':
            self.change_fon(level)
        if self.music:
            pygame.mixer.music.unpause()

        self.was_hell = False
        self.flag_weapon = False

        while self.check_game_over():
            self.run()
        return self.hero, self.sp_enemies, self.time_pl1, self.level

    def input_arg(self, level, music, hell, time_pl, was_hell):
        """При вызове start_screen запоминает все аргументы"""
        # возможен перенос в декоратор
        self.level = level
        self.music = music
        self.hell = hell
        self.time_pl1 = perf_counter() if self.level == 1 and self.hero.measuring == 'normal' else time_pl
        self.was_hell = was_hell

    def recovery_all_from_hell(self):
        """Переносит всех персонажей из нижнего мира"""
        self.hero.recovery_from_hell()
        for enemy in self.sp_enemies:
            enemy.recovery_from_hell()

    def run(self):
        """Метод отвечающий за движение всего по карте"""
        if self.hero.flag_move:
            self.move()
        else:
            self.event.raw_check_event()
        if self.hero.flag_end_behind:
            self.draw_behind_end()

    def move(self):
        """Метод для перемещения персонажа по карте, вызывается в run, в том случае, если персонаж бежит"""
        self.start_move()

        self.draw_fon()
        if self.chase:
            self.draw_chas()

        self.end_move()

    def start_move(self):
        """Метод начала сдвига персонажа"""
        if self.hero.flag_move:
            self.t += period[0]
            self.s += period[0]
            self.not_event += 1
            for i in [self.hero, *self.sp_enemies]:
                i.update_img()

    def end_move(self):
        """Метод конец сдвига персонажа"""
        if self.hero.flag_move:
            self.t %= size[0]

        pygame.display.flip()
        clock.tick(FPS)

    def draw_behind_end(self):
        if not self.time_end_behind:
            self.time_end_behind = perf_counter()
        elif perf_counter() - self.time_end_behind > 2:
            open_victory_window(self.time_pl1)

    def change_fon(self, level):
        """Метод для обработки (выбора фона)"""
        if self.level != 6 and self.was_hell is False:
            new_level(self.level)
        elif self.level == 6:
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
            self.event.check_coffee(self.hero, self.sp_enemies, self.hell, self.screen)

    def draw_fon(self):
        """Метод для рисования фона"""
        self.screen.blit(self.fon, (-self.t, 0))
        self.screen.blit(self.fon, (-self.t + size[0], 0))

    def draw_hero(self):
        """Метод для рисования главного героя"""
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

            # смена координат
            old_pos_hero = self.hero.get_pos()
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

    def take_all_attribute_for_goose(self, goose):
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
        """Если превращение в гуся должно произойти, то оно произойдёт"""
        if self.event.goose and len(self.sp_enemies) == 1:
            goose = Goose()
            # перенос координат героя на координаты гуся
            goose.rect.y = self.hero.rect.y
            goose.rect.x = self.hero.rect.x
            goose.old_y = self.hero.old_y
            while goose.z != self.hero.z:
                goose.z -= 1

            self.take_all_attribute_for_goose(goose)
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
            if perf_counter() - self.event.throw_knife[2] >= 3:
                pygame.mixer.music.pause()
                self.event.throw_knife = []
                self.start_screen(self.level + 1, self.music, self.hell, self.time_pl1, self.was_hell)

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
                self.start_screen(self.level + 1, self.music, self.hell, self.time_pl1, self.was_hell)

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
        coffee = period[0] - 5
        angle = 180 + 360 * coffee // 40
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
        super().__init__(screen, hero, sp_enemies)
        # инициализация фона
        self.fon_new = 'hell.jpg'
        self.fon = pygame.transform.scale(load_image(self.fon_new), size)
        self.fon = pygame.transform.rotate(self.fon, 180)

        # инициализация музыки
        pygame.mixer.music.load(f'sounds/hell_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        self.recovery_all_in_hell()

    def recovery_all_in_hell(self):
        """Изменение координат всех героев на нижне-мирские"""
        self.hero.recovery_in_hell()
        for enemy in self.sp_enemies:
            enemy.recovery_in_hell()

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
        """Метод при помощи которого осуществляется правильное движение ножа во время полёта"""
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
