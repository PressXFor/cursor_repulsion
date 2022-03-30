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
        self.mass = 1
        self.k = 2
        self.b = 1
        self.velocity = pygame.math.Vector2(0, 0)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.pos, self.size))

    def handle_forces(self, dt, mouse_pos):
        dt /= 1000
        vector_from_origin = self.pos - self.origin
        vector_from_mouse = self.pos - mouse_pos
        origin_dist = vector_from_origin.magnitude()
        mouse_dist = vector_from_mouse.magnitude()

        if vector_from_mouse == pygame.Vector2(0, 0):
            options = [pygame.Vector2(i, j) for i in range(-1, 2) for j in range(-1, 2)]
            while vector_from_mouse == pygame.Vector2(0, 0):
                vector_from_mouse += random.choice(options)  # no divide by zero in next step, slightly hacky

        if origin_dist == 0:
            attract = False
        else:
            attract = True

        if mouse_dist < 60:
            repulse = True
        else:
            repulse = False

        if attract and not repulse:
            # as if it is attached to a damped spring
            attract_vector = - self.k * vector_from_origin - self.b * self.velocity
        else:
            attract_vector = pygame.Vector2(0, 0)

        if repulse:
            unit_mouse = vector_from_mouse.normalize()
            repulsion_vector = unit_mouse * self.speed
        else:
            repulsion_vector = pygame.Vector2(0, 0)

        self.net_force = attract_vector + repulsion_vector
        self.acceleration = self.net_force / self.mass
        # self.pos += self.velocity * dt + (self.acceleration * (dt ** 2)) / 2
        self.pos += self.velocity * dt
        self.velocity += self.acceleration * dt


screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

image = pygame.image.load("testimage.png").convert_alpha()
image_rect = image.get_rect(topleft=(100, 100))


def generate_particles(screen, relative_position, image):
    particles = []
    alphas = pygame.surfarray.array_alpha(image)
    colors = pygame.surfarray.array3d(image)
    for i, row in enumerate(alphas[::5]):
        for j, alpha in enumerate(row[::5]):
            if alpha:
                pos = (relative_position[0] + i * 5, relative_position[1] + j * 5)
                color = colors[i][j]
                new_particle = Particle(color, pos, screen, speed=100)
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
        particle.handle_forces(dt, mouse_pos)
        particle.draw()
        # particle.attract()
        # particle.repulsion(dt, mouse_pos)
    pygame.display.flip()

    clock.tick(60)
