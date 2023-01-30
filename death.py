from const import pygame, load_image, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


class Death(pygame.sprite.Sprite):

    def __init__(self, x, y, picture, all_sprites):
        super().__init__(all_sprites)
        self.image = picture
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.conflict = False

    def update(self, hero):
        self.rect.y += 2
        if pygame.sprite.collide_mask(self, hero):
            self.conflict = True


def death(picture, hero):
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    death_player = Death(hero.rect.x, -20, picture, all_sprites)
    running = True
    fon = pygame.transform.scale(load_image('screenshot.jpg'), size)
    sound = pygame.mixer.Sound(f'sounds/scary_laughter.mp3')
    sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update(hero)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        if death_player.conflict:
            running = False
        clock.tick(50)

