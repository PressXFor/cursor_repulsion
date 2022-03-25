import pygame
import random
import math

pygame.init()


def distance_to(pos_1, pos_2):
    return math.sqrt((pos_2[0] - pos_1[0]) ** 2 + (pos_2[1] - pos_1[1]) ** 2)


def angle_to(pos_1, pos_2):
    return math.atan2(pos_2[1] - pos_1[1], pos_2[0] - pos_1[0])


def get_movement(angle, speed):
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    return dx, dy


class Particle:
    def __init__(self, color, position, screen, speed):
        self.color = color
        self.pos = pygame.math.Vector2(position)
        self.screen = screen
        self.size = (2, 2)
        self.speed = speed
        self.origin = pygame.math.Vector2(position)

    def attract(self):
        v = self.origin - self.pos  # order may need to be changed
        if v.x == v.y == 0:
            return
        if self.speed > v.magnitude():
            v_scaled = self.speed * v.normalize()
            self.pos += v_scaled
        else:
            self.pos += v

    def move(self):
        self.pos = (self.pos[0] + random.uniform(-1, 1), self.pos[1] + random.uniform(-1, 1))

    def repulsion(self, dt, mouse_pos):
        if distance_to(self.pos, mouse_pos) < 60:
            angle = pygame.Vector2.angle_to(self.pos, mouse_pos)
            dx, dy = get_movement(angle, self.speed)
            self.pos[0] -= dx * dt
            self.pos[1] -= dy * dt

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.pos, self.size))


screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

image = pygame.image.load("testimage.png").convert_alpha()
image_rect = image.get_rect(topleft=(100, 100))


def generate_particles(screen, relative_position, image):
    particles = []
    alphas = pygame.surfarray.array_alpha(image)
    colors = pygame.surfarray.array3d(image)
    for i, row in enumerate(alphas[::2]):
        for j, alpha in enumerate(row[::2]):
            if alpha:
                pos = (relative_position[0] + i*2, relative_position[1] + j*2)
                color = colors[i][j]
                new_particle = Particle(color, pos, screen, speed=0.5)
                particles.append(new_particle)
    return particles


particles = generate_particles(screen, (100, 100), image)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    # cursor = pygame.draw.circle(screen, 'Red', mouse_pos, 20)

    mouse_pos = pygame.math.Vector2(mouse_pos)

    dt = clock.tick() / 2
    dt *= 60

    for particle in particles:
        particle.draw()
        # particle.attract()
        particle.repulsion(dt, mouse_pos)
        # particle.move()
    pygame.display.flip()

    clock.tick(60)
