import sys
import pygame
Isjump = False

def event(hero):
    global Isjump, Jumpcount
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Isjump = True

def check():
    global Isjump
    if Isjump:
        Isjump = False
        return True

