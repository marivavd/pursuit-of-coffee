import sys
from const import width, height
from death import death
from Items import *


class Event:
    def __init__(self):
        self.game_over = False
        self.swap = False
        self.goose = False

        self.throw_knife = []
        self.active_mine = ActiveMine(0, 0, 0)

    def check_event(self, hero):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_key(event, hero)

    @staticmethod
    def raw_check_event():
        """Сокращённая обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    def check_key(self, event, hero):
        """Обработка нажатия на кнопки"""
        if event.key == pygame.K_UP:  # прыжок
            hero.is_jump = True
        elif event.key == pygame.K_LEFT:
            hero.shift_side(-1)
        elif event.key == pygame.K_RIGHT:
            hero.shift_side()
        elif event.key == pygame.K_DOWN:  # оставлять мину
            hero.drop_mima(mina=self.active_mine)
        elif event.key == pygame.K_SPACE:  # пулять ножом во врага
            self.throw_knife = hero.drop_knife()

    def check_contact(self, hero, *groups):
        """Проверка столкновения с объектами"""
        sl_group = {all_obstacles: self.crash_obstacles,
                    things: self.crash_things,
                    weapon: self.crash_weapon,
                    coffee: self.crash_coffee,
                    house: self.crash_end_obj}
        for group in groups:
            for i in group:
                if pygame.sprite.collide_mask(i, hero):
                    sl_group[group](hero, i)

    def crash_obstacles(self, hero, i):
        """Проверка столкновения с препятствиями"""
        hero.alive = False
        self.game_over = True
        i.kill()

    def crash_things(self, _, i):
        """Проверка столкновения с вещами (кепкой или очками)"""
        if type(i) is Cap:
            self.goose = True
        elif type(i) is Glasses:
            self.swap = True
        i.kill()

    @staticmethod
    def crash_weapon(hero, i):
        """Проверка столкновения с оружием (ножом или миной)"""
        if type(i) is Knife:
            hero.take_knife(knife=i)
        elif type(i) is Mina:
            hero.take_mina(mina=i)
        i.kill()

    @staticmethod
    def crash_coffee(_, i):
        """Проверка столкновения с кофе"""
        i.invigorating(i)
        i.kill()

    @staticmethod
    def crash_end_obj(hero, i):
        """Провера на концовки"""
        if type(i) in (Bed, Flagpole, Large_coffee):
            pygame.mixer.music.pause()
            hero.end()

    def check_coffee(self, hero, enemies, hell, screen):
        """Проверка на уровень кофе в крови"""
        period[0] -= 1
        if not 5 <= period[0] <= 20 and hell and hero.measuring != 'hell':
            self.game_over = True
            hero.measuring = 'hell'
            for enemy in enemies:
                enemy.measuring = 'hell'

            rect = pygame.Rect(0, 0, 800, 600)
            sub = screen.subsurface(rect)
            screenshot = pygame.Surface((800, 600))
            screenshot.blit(sub, (0, 0))
            pygame.image.save(screenshot, "images/screenshot.jpg")
            death(pygame.transform.scale(load_image('death.png'), (width // 4, height // 4)), hero)
