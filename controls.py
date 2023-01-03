import sys, pygame


def event():
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
