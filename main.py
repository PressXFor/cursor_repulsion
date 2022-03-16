import pygame
import random

pygame.init()


class Particle:
    def __init__(self, color, position, screen):
        self.color = color
        self.pos = position
        self.screen = screen
        self.size = (1, 1)
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def move(self):
        self.pos = (self.pos[0] + random.uniform(-1, 1), self.pos[1] + random.uniform(-1, 1))
        self.rect.topleft = self.pos

    def draw(self):
        self.screen.blit(self.image, self.rect)


screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 32)
image = font.render(input("Enter your text\n"), True, (255, 0, 0))
# image = pygame.image.load("testimage.png").convert_alpha()
image_rect = image.get_rect(topleft=(100, 100))


def generate_particles(screen, relative_position, image):
    particles = []
    alphas = pygame.surfarray.array_alpha(image)
    colors = pygame.surfarray.array3d(image)
    for i, row in enumerate(alphas):
        for j, alpha in enumerate(row):
            if alpha:
                pos = (relative_position[0] + i, relative_position[1] + j)
                color = colors[i][j]
                new_particle = Particle(color, pos, screen)
                particles.append(new_particle)
    return particles


particles = generate_particles(screen, (100, 100), image)
particle_rects = [p.rect for p in particles]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255, 255))
    for particle in particles:
        particle.draw()
        # particle.move()
    pygame.display.update()

    print(clock.get_fps())
    clock.tick(60)