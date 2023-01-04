import sys
import pygame
Isjump = False
game_over = False

def event(hero, all_obstacles):
    global Isjump, Jumpcount
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Isjump = True
            elif event.key == pygame.K_LEFT:
                hero.shift_side(-1)
            elif event.key == pygame.K_RIGHT:
                hero.shift_side()
        elif True:
            for i in all_obstacles:
                if not pygame.sprite.collide_mask(i, hero):
                    game_over = True

def check_jump():
    global Isjump
    if Isjump:
        Isjump = False
        return True
    return False

def check_crash():
    global game_over
    if game_over:
        game_over = False
        return True
    return False



