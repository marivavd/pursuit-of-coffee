from random import choice
from const import pygame, load_image, size, width, height

pygame.init()
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, all_sprites):
        super().__init__(all_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.2

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, all_sprites):
    particle_count = 50
    numbers = range(-10, 1)
    for i in range(particle_count):
        Particle(position, choice(numbers), choice(numbers), all_sprites)


def magic():
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    create_particles((400, 300), all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)
        if len(all_sprites) <= 5:
            running = False
