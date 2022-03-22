import pygame
import random

pygame.init()


class Particle:
    def __init__(self, color, position, screen, startDir):
        self.color = color
        self.pos = pygame.math.Vector2(position)
        self.dir = pygame.math.Vector2(startDir).normalize()
        self.screen = screen
        self.size = (1, 1)

    # def move(self):
    #     self.pos = (self.pos[0] + random.uniform(-1, 1), self.pos[1] + random.uniform(-1, 1))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.pos, self.size))

    # def reflect(self, newDir):
    #     self.dir = self.dir.reflect(pygame.math.Vector2(newDir))


screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

image = pygame.image.load("testimage.png").convert_alpha()
image_rect = image.get_rect(topleft=(100, 100))


def generate_particles(screen, relative_position, image, startDir):
    particles = []
    alphas = pygame.surfarray.array_alpha(image)
    colors = pygame.surfarray.array3d(image)
    for i, row in enumerate(alphas):
        for j, alpha in enumerate(row):
            if alpha:
                pos = (relative_position[0] + i, relative_position[1] + j)
                color = colors[i][j]
                new_particle = Particle(color, pos, screen, startDir)
                particles.append(new_particle)
    return particles


particles = generate_particles(screen, (100, 100), image, startDir=(0, 1))

# d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
# def collision():
#     if generate_particles() <= mouse_pos:
#         print('hellos')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    cursor = pygame.draw.circle(screen, 'Red', mouse_pos, 20)

    # for new_particle in particles:
    #     d = new_particle.pos.distance_to(mouse_pos)
    #     if d <= 20:
            # new_particle.pos[0]
            # new_particle.pos[1]

    # collision()
    for particle in particles:
        particle.draw()
        # particle.move()
    pygame.display.flip()

    clock.tick(60)
