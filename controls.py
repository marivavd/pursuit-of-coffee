import sys
from const import width, height
from death import death
from Items import *


class Event:
    def __init__(self):
        self.isjump = False
        self.game_over = False
        self.swap = False
        self.goose = False

        self.throw_knife = []
        self.active_mine = ActiveMine(0, 0, 0)

    def check_event(self, hero):
        """обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_key(event, hero)
                # сделать так, чтобы при смене персонажа, и нож, и мина оставались у него

    def check_key(self, event, hero):
        """обработка нажатия на кнопки"""
        if event.key == pygame.K_UP:  # прыжок
            hero.is_jump = True
        elif event.key == pygame.K_LEFT:
            hero.shift_side(-1)
        elif event.key == pygame.K_RIGHT:
            hero.shift_side()
        elif event.key == pygame.K_DOWN:  # оставлять мину
            hero.drop_mima(hero.rect.x, hero.rect.y, self.active_mine)
        elif event.key == pygame.K_SPACE:  # пулять ножом во врага
            self.throw_knife = hero.drop_knife(hero.rect.x, hero.rect.y)

    def check_contact(self, hero, *groups):
        """проверка столкновения с объектами"""
        sl_group = {all_obstacles: self.crash_obstacles,
                    things: self.crash_things,
                    weapon: self.crash_weapon,
                    coffee: self.crash_coffee}
        for group in groups:
            for i in group:
                if pygame.sprite.collide_mask(i, hero):
                    sl_group[group](hero, i)

    def crash_obstacles(self, hero, i):
        """проверка столкновения с препятствиями"""
        hero.alive = False
        self.game_over = True
        i.kill()

    def crash_things(self, hero, i):
        """проверка столкновения с вещами (кепкой или очками)"""
        if type(i) is Cap:
            self.goose = True
        elif type(i) is Glasses:
            self.swap = True
        i.kill()

    @staticmethod
    def crash_weapon(hero, i):
        """проверка столкновения с оружием (ножом или миной)"""
        if type(i) is Knife:
            hero.take_knife(hero.rect.x, hero.rect.y, i)
        elif type(i) is Mina:
            hero.take_mina(hero.rect.x, hero.rect.y, i)
        i.kill()

    @staticmethod
    def crash_coffee(hero, i):
        """проверка столкновения с кофе"""
        i.invigorating(i)
        i.kill()

    def check_cofe(self, hero, enemies, hell, screen):
        """проверка на уровень кофе в крови"""
        period[0] -= 1
        if not 5 <= period[0] <= 20 and hell:
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
# при гейм овер удалять все объекты!



